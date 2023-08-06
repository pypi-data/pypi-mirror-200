import copy
import typing
from typing import Optional

import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QHBoxLayout, QLabel, QLineEdit
from skimage import img_as_ubyte
from skimage.color import rgb2hsv
from skimage.feature import graycoprops, graycomatrix

from maphis.common.common import Info
from maphis.common.label_image import RegionProperty, PropertyType
from maphis.common.photo import Photo
from maphis.common.plugin import PropertyComputation
from maphis.common.regions_cache import RegionsCache
from maphis.common.units import UnitStore, convert_value, Unit, BaseUnit, SIPrefix
from maphis.common.choice_popup_panel import ChoicePopupPanel, ChoiceOrder
from maphis.common.param_widget import ParamWidget
from maphis.common.user_param import Param, ParamBuilder


def _safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


class GLCM(PropertyComputation):
    """
    GROUP: Pattern measurements
    NAME: GLCM properties
    DESCRIPTION: Various GLCM properties
    KEY: glcm
    """
    def __init__(self, info: Optional[Info] = None):
        super().__init__(info)
        self._props: typing.List[str] = ['ASM', 'contrast', 'correlation', 'dissimilarity', 'energy', 'homogeneity']
        self._settings_widget: QWidget = self._build_settings_widget()
        self.distances_in_mm = [1.0/32, 2.0/32, 3.0/32, 4.0/32, 5.0/32, 6.0/32, 7.0/32, 8.0/32]  # TODO: This particular setting is for a testing run
        self.angles_in_degrees = [0, 90, 180, 270] # The GLCM will be calculated for these angles (in radians). TODO: Maybe turn on the symmetry in graycomatrix(), and only use half the range of the angles?

        self._setup_params()

    def _setup_params(self):
        self._user_params: typing.Dict[str, Param] = {
            'distances_mm': ParamBuilder()
                        .name('Distances in mm')
                        .key('distances_mm')
                        .string_param()
                        .default_value('0.03125, 0.0625, 0.09375, 0.125, 0.15625, 0.1875, 0.21875, 0.25')
                        .build(),
            'angles_degrees': ParamBuilder()
                        .name('Angles in degrees')
                        .key('angles_degrees')
                        .string_param()
                        .default_value('0, 90').build()
        }
        self.__widget = ParamWidget(list(self._user_params.values()))
        self._param_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.__widget.widget)
        self.choices_widget = ChoicePopupPanel(self._props, choice_order=ChoiceOrder.Alphabetical)
        self.choices_widget.set_popup_mode(False)
        layout.addWidget(self.choices_widget)
        self._param_widget.setLayout(layout)

    def _build_settings_widget(self) -> QWidget:
        widg = QWidget()
        layout = QVBoxLayout()
        hlay = QHBoxLayout()
        lab = QLabel('Distances in mm')
        txt = QLineEdit()
        txt.setObjectName('distances_mm')
        hlay.addWidget(lab)
        hlay.addWidget(txt)
        layout.addLayout(hlay)

        hlay = QHBoxLayout()
        lab = QLabel('Angles in degrees')
        txt = QLineEdit()
        txt.setObjectName('angles_degrees')
        hlay.addWidget(lab)
        hlay.addWidget(txt)
        layout.addLayout(hlay)

        widg.setLayout(layout)
        for prop in self._props:
            chkbox = QCheckBox(prop)
            chkbox.setObjectName(prop)
            chkbox.setChecked(True)
            layout.addWidget(chkbox)
        return widg

    def __call__(self, photo: Photo, region_labels: typing.List[int], regions_cache: RegionsCache, prop_names: typing.List[str]) -> \
            typing.List[RegionProperty]:

        if 'photo_hsv' not in regions_cache.data_storage:
            regions_cache.data_storage['photo_hsv'] = rgb2hsv(photo.image)

        photo_image_hsv = regions_cache.data_storage['photo_hsv']
        props: typing.List[RegionProperty] = []

        lab_img = photo['Labels'].label_image
        refl = photo['Reflections'].label_image

        self.distances_in_mm = self._parse_distances()
        if photo.image_scale is not None and photo.image_scale.value > 0:
            unit_store = UnitStore()
            scale_in_px_per_mm = convert_value(photo.image_scale, unit_store.units["px/mm"])
            distances_in_px = [round(x * scale_in_px_per_mm.value) for x in self.distances_in_mm]
        else:
            distances_in_px = list(range(len(self.distances_in_mm)))

        self.angles_in_degrees = self._parse_angles()
        angles = [x / 180.0 * np.pi for x in self.angles_in_degrees]

        for label in region_labels:
            # Prepare a list of all GLCM properties requested for the current label, e.g. ["contrast", "homogeneity"].
            # properties_for_current_label = [glcm_property for glcm_property, label_list in prop_labels.items() if label in label_list]

            # Binary mask of the current region, excluding the reflections.
            # current_region_mask = np.logical_and(lab_img == label, refl == 0)
            if label not in regions_cache.regions:
                for prop_name in prop_names:
                    prop = self.example(prop_name)
                    vals = []
                    for _i in range(prop.num_vals):
                        vals.append(np.nan * np.ones((len(distances_in_px), len(angles))))
                    prop.value = (np.array(vals), Unit(BaseUnit.none, SIPrefix.none, dim=0))
                    prop.label = label
                    props.append(prop)
                continue

            region_obj = regions_cache.regions[label]
            top, left, height, width = region_obj.bbox
            refl_roi = refl[top:top + height, left:left + width]

            current_region_mask = np.logical_and(region_obj.mask, refl_roi == 0)
            photo_image_hsv_roi = photo_image_hsv[top:top+height, left:left+width]

            # Prepare the GLCMs for all channels.
            filtered_glcms: typing.List[typing.Any] = []
            for current_channel in range(3):
                current_channel_values = img_as_ubyte(photo_image_hsv_roi[:, :, current_channel])
                # Make sure no pixel has the max value, so we can do the +1 in the next step, and use "0" exclusively as "pixels to be ignored".
                current_channel_values[current_channel_values == np.iinfo(current_channel_values.dtype).max] = np.iinfo(current_channel_values.dtype).max - 1
                current_channel_values_masked = current_channel_values + 1
                current_channel_values_masked[current_region_mask == 0] = 0
                # Whole image GLCM with pixels outside the current region zeroed-out, as a base for the filtered version.
                glcm = graycomatrix(current_channel_values_masked, distances_in_px, angles)
                # GLCM of only the pixels belonging to the current region.
                filtered_glcms.append(glcm[1:, 1:, :, :])

            # Extract the requested properties from the GLCMs for each channel and append to props.
            for prop_name in prop_names:
                current_property_values_for_all_channels = []
                for current_channel in range(3):
                    current_property_values_for_current_channel = graycoprops(filtered_glcms[current_channel], prop=prop_name).tolist()
                    current_property_values_for_all_channels.append(current_property_values_for_current_channel)
                # Append the results to props -- each requested property as one item containing three matrices (one for each HSV channel).
                prop = self.example(prop_name)
                prop.label = int(label)
                prop.value = (np.array(current_property_values_for_all_channels), self._no_unit)
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
        prop.value = (np.zeros((3, 3)), Unit(BaseUnit.none, SIPrefix.none, dim=0))
        prop.val_names = ['H', 'S', 'V']
        prop.row_names = [f'distance {x} mm' for x in self.distances_in_mm]
        prop.col_names = [f'angle {x}°' for x in self.angles_in_degrees]
        prop.num_vals = 3
        prop.prop_type = PropertyType.NDArray
        prop.info = copy.deepcopy(self.info)
        prop.info.name = prop_name
        prop.prop_comp_key = self.info.key
        prop.local_key = prop_name
        return prop

    def target_worksheet(self, prop_name: str) -> str:
        return "GLCM"

    @property
    def group(self) -> str:
        return super().group

    @property
    def setting_widget(self) -> typing.Optional[QWidget]:
        return self._param_widget

    @property
    def requested_props(self) -> typing.List[str]:
        return self.choices_widget.selection

    def _parse_distances(self) -> typing.List[float]:
        result = []
        for str_val in self._user_params['distances_mm'].value.split(','):
            val = _safe_cast(str_val, float)
            if val is not None:
                result.append(val)
        return result

    def _parse_angles(self) -> typing.List[float]:
        result = []
        for str_val in self._user_params['angles_degrees'].value.split(','):
            val = _safe_cast(str_val, float)
            if val is not None:
                result.append(val)
        return result

    def current_settings_to_str_dict(self) -> typing.Dict[str, typing.Dict[str, str]]:
        sett_dict = super().current_settings_to_str_dict()
        sett_dict['custom_parameters'] = {
            'glcm_props': self.choices_widget.selection
        }

        return sett_dict

    def setup_settings_from_dict(self, _dict: typing.Dict[str, typing.Dict[str, str]]):
        super().setup_settings_from_dict(_dict)
        custom_parameters = _dict['custom_parameters']

        self.choices_widget.selection = []
        self.choices_widget.selection = custom_parameters['glcm_props']
