import copy
import typing
from typing import Optional

import cv2
import numpy as np
from PySide6.QtWidgets import QWidget

from maphis.common.common import Info
from maphis.common.label_image import RegionProperty, PropertyType
from maphis.common.photo import Photo
from maphis.common.plugin import PropertyComputation
from maphis.common.regions_cache import RegionsCache
from maphis.common.units import Value
from maphis.common.param_widget import ParamWidget
from maphis.common.user_param import ParamBuilder, Param


class OBBoxDims(PropertyComputation):
    """
    GROUP: Length & area measurements
    NAME: Oriented bounding box dimensions
    DESCRIPTION: Width and heigth of the oriented bounding box of a region
    KEY: oriented_bbox
    """

    def __init__(self, info: Optional[Info] = None):
        super().__init__(info)
        self._user_params: typing.Dict[str, Param] = {
            'width': ParamBuilder().bool_param().true().name('Width').key('width').build(),
            'length': ParamBuilder().bool_param().true().name('Length').key('length').build()
        }

        self._setting_widget: ParamWidget = ParamWidget(list(self._user_params.values()))

    def __call__(self, photo: Photo, region_labels: typing.List[int], regions_cache: RegionsCache, prop_names: typing.List[str]) -> \
            typing.List[RegionProperty]:
        props: typing.List[RegionProperty] = []

        for label in region_labels:
            if label not in regions_cache.regions:
                continue

            reg_obj = regions_cache.regions[label]

            mask = (255 * reg_obj.mask.copy()).astype(np.uint8)
            mask = cv2.copyMakeBorder(mask, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=0)

            points = np.argwhere(mask != 0)[:, ::-1]
            rot_rect = cv2.minAreaRect(points)

            rect_points = np.round(cv2.boxPoints(rot_rect)).astype(np.int32)

            ax1 = rect_points[0] - rect_points[-1]
            ax1_n = np.linalg.norm(ax1)
            ax1 = ax1 / (np.linalg.norm(ax1) + 1e-9)
            ax2 = rect_points[-1] - rect_points[2]
            ax2_n = np.linalg.norm(ax2)
            ax2 = ax2 / (np.linalg.norm(ax2) + 1e-9)

            dims = {
                'width': 0.0,
                'length': 0.0
            }
            if np.abs(np.dot(ax1, np.array([1.0, 0]))) > np.abs(np.dot(ax2, np.array([1.0, 0]))):
                dims['width'] = ax1_n
                dims['length'] = ax2_n
            else:
                dims['width'] = ax2_n
                dims['length'] = ax1_n
            for prop_name in prop_names:
                prop = self.example(prop_name)
                prop.prop_type = PropertyType.Scalar
                prop.label = label
                if photo.image_scale is not None:
                    prop.value = Value(float(dims[prop_name]), self._px_unit) / photo.image_scale
                else:
                    prop.value = Value(float(dims[prop_name]), self._px_unit)
                prop.num_vals = 1
                props.append(prop)
        return props

    @property
    def user_params(self) -> typing.List[Param]:
        return super().user_params

    @property
    def region_restricted(self) -> bool:
        return super().region_restricted

    @property
    def computes(self) -> typing.Dict[str, Info]:
        return {self.info.key: self.info}

    def example(self, prop_name: str) -> RegionProperty:
        prop = super().example(prop_name)
        prop.label = 0
        prop.info = copy.deepcopy(self.info)
        prop.info.name = prop_name
        prop.num_vals = 1
        prop.prop_type = PropertyType.Scalar
        prop.val_names = [prop_name.capitalize()]
        return prop

    def target_worksheet(self, prop_name: str) -> str:
        return super().target_worksheet(self.info.key)

    @property
    def group(self) -> str:
        return super().group

    @property
    def requested_props(self) -> typing.List[str]:
        return [par.key for par in self._user_params.values() if par.value]

    @property
    def setting_widget(self) -> typing.Optional[QWidget]:
        return self._setting_widget.widget
