import cv2
import numpy as np

from maphis.common.photo import Photo, LabelImg
from maphis.common.plugin import RegionComputation
from typing import Set, Optional


class Reflections(RegionComputation):
    """
    NAME: Reflections
    DESCRIPTION: Generates reflections mask based on lightness.
    """

    def __init__(self) -> None:
        RegionComputation.__init__(self)
        self.k = 2.0

    def __call__(
        self, photo: Photo, labels: Optional[Set[int]] = None
    ) -> Set[LabelImg]:
        copy = photo['Reflections'].clone()

        mask = photo['Labels'].label_image
        light = cv2.cvtColor(photo.image, cv2.COLOR_RGB2HLS)[:, :, 1]
        reflections_mask = np.zeros_like(mask, dtype=bool)
        background_label = photo['Labels'].label_hierarchy.label('0:0:0:0')

        for label in np.unique(mask):
            if label != background_label:
                average = np.mean(light[mask == label])
                deviation = np.std(light[mask == label])
                reflections_mask[mask == label] = (
                    light[mask == label] > self.k * deviation + average
                )

        reflection_label = copy.label_hierarchy.labels[-1]
        copy.label_image = np.where(
            reflections_mask, reflection_label, 0
        ).astype(np.uint32)

        return [copy]
