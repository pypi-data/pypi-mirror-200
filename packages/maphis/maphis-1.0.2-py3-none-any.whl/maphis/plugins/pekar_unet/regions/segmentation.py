import importlib
import importlib.resources
import os
import pathlib
import shutil
import sys
import typing
from typing import Set, Optional, Tuple

import cv2
import math
import arthseg
# import torch
from numpy import ndarray
import numpy as np

from maphis.common.download import DownloadDialog
from maphis.common.storage import Storage
from maphis.common.photo import Photo, LabelImg
from maphis.common.plugin import RegionComputation


class UNetRegions(RegionComputation):
    """
    NAME: Arthropod segmentation
    DESCRIPTION: Labels the parts of an arthropod.
    """

    def __init__(self) -> None:
        RegionComputation.__init__(self, None)
        # self.model = torch.jit.load(os.path.join(dir, 'model.pt'))
        path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
        self.model_path = path / 'model.pt'
        self.model = None
        self.torch = None
        self.conv_depth = 64  # need to pad the image to be divisible by 64

    def __call__(
        self, photo: Photo, labels: Optional[Set[int]] = None, storage: typing.Optional[Storage] = None) -> Set[LabelImg]:
        label_hierarchy = photo['Labels'].label_hierarchy

        leg_label = label_hierarchy.label('1:2:0:0')

        # leg_segment_labels = {
        #     label_hierarchy.label('1:2:1:0'): [
        #         label_hierarchy.label('1:2:1:1'),
        #         label_hierarchy.label('1:2:1:2'),
        #         label_hierarchy.label('1:2:1:3'),
        #     ],
        #     label_hierarchy.label('1:2:2:0'): [
        #         label_hierarchy.label('1:2:2:1'),
        #         label_hierarchy.label('1:2:2:2'),
        #         label_hierarchy.label('1:2:2:3'),
        #     ],
        #     label_hierarchy.label('1:2:3:0'): [
        #         label_hierarchy.label('1:2:3:1'),
        #         label_hierarchy.label('1:2:3:2'),
        #         label_hierarchy.label('1:2:3:3'),
        #     ],
        #     label_hierarchy.label('1:2:4:0'): [
        #         label_hierarchy.label('1:2:4:1'),
        #         label_hierarchy.label('1:2:4:2'),
        #         label_hierarchy.label('1:2:4:3'),
        #     ],
        #     label_hierarchy.label('1:2:5:0'): [
        #         label_hierarchy.label('1:2:5:1'),
        #         label_hierarchy.label('1:2:5:2'),
        #         label_hierarchy.label('1:2:5:3'),
        #     ],
        #     label_hierarchy.label('1:2:6:0'): [
        #         label_hierarchy.label('1:2:6:1'),
        #         label_hierarchy.label('1:2:6:2'),
        #         label_hierarchy.label('1:2:6:3'),
        #     ],
        #     label_hierarchy.label('1:2:7:0'): [
        #         label_hierarchy.label('1:2:7:1'),
        #         label_hierarchy.label('1:2:7:2'),
        #         label_hierarchy.label('1:2:7:3'),
        #     ],
        #     label_hierarchy.label('1:2:8:0'): [
        #         label_hierarchy.label('1:2:8:1'),
        #         label_hierarchy.label('1:2:8:2'),
        #         label_hierarchy.label('1:2:8:3'),
        #     ],
        # }

        leg_segment_labels = {
            leg_node.label: [leg_section.label for leg_section in leg_node.children]
            for leg_node in label_hierarchy.get_child_nodes(leg_label)
        }

        leg_pair_labels = [
            (
                label_hierarchy.label('1:2:1:0'),
                label_hierarchy.label('1:2:2:0'),
            ),
            (
                label_hierarchy.label('1:2:3:0'),
                label_hierarchy.label('1:2:4:0'),
            ),
            (
                label_hierarchy.label('1:2:5:0'),
                label_hierarchy.label('1:2:6:0'),
            ),
            (
                label_hierarchy.label('1:2:7:0'),
                label_hierarchy.label('1:2:8:0'),
            ),
        ]

        body_labels = {
            label_hierarchy.label('1:1:1:0'),
            label_hierarchy.label('1:1:2:0'),
        }

        back_label = label_hierarchy.label('1:1:3:0')

        output = self.predict(photo.image)
        output[output == 1] = label_hierarchy.label('1:1:1:0')
        output[output == 2] = label_hierarchy.label('1:1:2:0')
        output[output == 3] = label_hierarchy.label('1:1:3:0')
        output[output == 4] = label_hierarchy.label('1:2:0:0')

        # refine prediction
        output = arthseg.remove_dirt(
            output, keep=True, max_distance=20, min_area=0.05
        )
        output = arthseg.fill_holes(
            output,
            fill_value=label_hierarchy.label('1:1:1:0'),
            hole_area=0.001,
        )
        output = arthseg.refine_regions(
            output,
            body_labels={*body_labels, back_label},
            min_area=0.01,
        )
        output = arthseg.refine_legs(
            output,
            leg_labels={leg_label},
            pair_labels=leg_pair_labels,
            body_labels=body_labels,
            alternative_labels={back_label},
        )
        output = arthseg.leg_segments(
            output,
            labels=leg_segment_labels,
            body_labels=body_labels,
            alternative_labels={back_label},
        )

        lab = photo['Labels'].clone()
        lab.label_image = output
        return [lab]

    def get_padding(self, image: ndarray) -> Tuple[float, float]:
        height_padding = (
            (self.conv_depth - image.shape[0] % self.conv_depth)
            % self.conv_depth
        ) / 2
        width_padding = (
            (self.conv_depth - image.shape[1] % self.conv_depth)
            % self.conv_depth
        ) / 2

        return height_padding, width_padding

    def add_padding(
        self, image: ndarray, height_padding: float, width_padding: float
    ) -> ndarray:
        if width_padding >= 0.5 or height_padding >= 0.5:
            image = cv2.copyMakeBorder(
                image,
                int(height_padding),
                math.ceil(height_padding),
                int(width_padding),
                math.ceil(width_padding),
                cv2.BORDER_CONSTANT,
                value=0,
            )

        return image

    def remove_padding(
        self, image: ndarray, height_padding: float, width_padding: float
    ) -> ndarray:
        if height_padding >= 0.5:
            image = image[int(height_padding) : -math.ceil(height_padding), :]
        if width_padding >= 0.5:
            image = image[:, int(width_padding) : -math.ceil(width_padding)]

        return image

    def initialize(self) -> typing.Tuple[bool, str]:
        path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
        model_path = path / 'model.pt'
        if not model_path.exists():
            download = DownloadDialog("https://gitlab.fi.muni.cz/xmraz3/maphis_pekar_segmentation/-/raw/main/model.pt",
                                      dst=model_path,
                                      label='Downloading segmentation model',
                                      title='First time initialization of plugin')
            if not download.start():
                return False, "Could not download the segmentation model."
        if self.torch is None:
            self.torch = importlib.import_module('torch')
            self.model = self.torch.jit.load(model_path)
        return True, ''

    def predict(self, image: ndarray) -> ndarray:
        height_padding, width_padding = self.get_padding(image)
        image = self.add_padding(image, height_padding, width_padding)

        # (height, width, channels) -> (batch, channels, height, width)
        input = self.torch.from_numpy(image).permute(2, 0, 1).float().unsqueeze(0)

        prediction = self.model(input / 255).detach()
        prediction *= prediction > 0.5

        # (batch, channels, height, width) -> (height, width, channels)
        prediction = prediction.squeeze(0).permute(1, 2, 0)

        mask: ndarray = np.insert(prediction.numpy(), 0, 0, axis=-1).argmax(-1)
        mask = self.remove_padding(mask, height_padding, width_padding)
        return mask.astype(np.uint32)
