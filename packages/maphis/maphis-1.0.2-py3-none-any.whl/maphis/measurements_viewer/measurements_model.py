import typing
from enum import IntEnum
from typing import Dict
import functools

import PySide6
import numpy as np
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QVector3D, QColor, QPixmap
from skimage.color import hsv2rgb

from maphis.common.icon_storage import IconStorage
from maphis import qimage2ndarray
from maphis.common.label_image import PropertyType
from maphis.common.state import State
from maphis.common.utils import vector_to_img

PropCompKey = str
LocalKey = str
Label = int
PropName = str
PhotoName = str


class MeasurementsTableRole(IntEnum):
    Label = Qt.UserRole,
    PropertyComputationKey = Qt.UserRole + 1,
    PropertyName = Qt.UserRole + 2,
    PhotoName = Qt.UserRole + 3,
    RegionProperty = Qt.UserRole + 4,
    Photo = Qt.UserRole + 5,
    LocalKey = Qt.UserRole + 6


class MeasurementsTableModel(QAbstractTableModel):

    def __init__(self, state: State, parent: typing.Optional[PySide6.QtCore.QObject] = None):
        super().__init__(parent)

        self.column_names: typing.List[str] = []
        self.prop_tuple_list: typing.List[typing.Tuple[Label, PropCompKey, LocalKey, PropName]] = []
        self.state: State = state
        self.single_photo_mode: bool = True
        self.header_labels: typing.List[str] = []
        self.labels: typing.List[int] = []
        self.displayed_property_key: str = ''
        self._display_intensity_in_color: bool = True  # color value will either be displayed as QColor(True) or numbers(False)
        self.current_label_name: str = ''
        self._invalid_property_bg_color: QColor = QColor.fromString('#FFEB9C')

    def rowCount(self, parent:PySide6.QtCore.QModelIndex=QModelIndex()) -> int:
        if self.state.storage is None:
            return 0
        # return self.state.storage.image_count
        return self.state.image_list_model.rowCount(parent)
        pass

    def columnCount(self, parent:PySide6.QtCore.QModelIndex=QModelIndex()) -> int:
        if self.state.storage is None:
            return 0
        return len(self.column_names)

    def data(self, index:PySide6.QtCore.QModelIndex, role:int=Qt.DisplayRole) -> typing.Any:
        if self.state.storage is None or index.column() >= self.columnCount():
            return None
        # photo = self.state.storage.get_photo_by_idx(index.row(), load_image=False)
        photo = self.state.image_list_model.fetch_photo(index.row())
        label = self.prop_tuple_list[index.column()][0]
        props = photo[self.current_label_name].get_region_props(label)

        if role == MeasurementsTableRole.Label:
            return label
        elif role == MeasurementsTableRole.PropertyComputationKey:
            return self.prop_tuple_list[index.column()][1]
        elif role == MeasurementsTableRole.PropertyName:
            return self.prop_tuple_list[index.column()][3]
        elif role == MeasurementsTableRole.PhotoName:
            return photo.image_name
        elif role == MeasurementsTableRole.Photo:
            return photo
        elif role == MeasurementsTableRole.LocalKey:
            return self.prop_tuple_list[index.column()][2]

        if props is None:
            if role == Qt.DisplayRole:
                return 'N/A'
            return None
        #if self.displayed_property_key not in props:
        #    return None
        prop_key = f'{self.prop_tuple_list[index.column()][1]}.{self.prop_tuple_list[index.column()][2]}'
        if prop_key not in props:
            if role == Qt.DisplayRole:
                return 'N/A'
            return None
        prop = props[prop_key]
        if role == Qt.DisplayRole:
            if prop.prop_type in {PropertyType.Scalar, PropertyType.String}:
                return str(prop.value)
            if (prop.prop_type == PropertyType.Intensity or prop.prop_type == PropertyType.IntensityHSV) and not self._display_intensity_in_color:
                str_val = ''
                vals = prop.value[0] if prop.num_vals > 1 else [prop.value]
                for i, val in enumerate(vals):
                    if type(val) == float:
                        str_val = str_val + f', {val:.3f} {prop.val_names[i]}'
                    else:
                        str_val = str_val + f', {val} {prop.val_names[i]}'
                return str_val.strip(',')
            # if prop.prop_type == PropertyType.Vector:
            #     return prop.format_value()
            if prop.prop_type == PropertyType.NDArray:
                val: np.ndarray = prop.value[0]
                return f'{val.shape[1:]} matrices for {",".join(prop.val_names)}'
            return None
        if role == Qt.BackgroundRole:
            if self._display_intensity_in_color:
                if prop.prop_type == PropertyType.Intensity:
                    if prop.num_vals == 1:
                        return QColor.fromRgbF(*(prop.value / 255.0, ) * 3)
                    elif prop.num_vals == 3:
                        clr = [val / 255.0 for val in prop.value[0]]
                        return QColor.fromRgbF(*clr)
                elif prop.prop_type == PropertyType.IntensityHSV:
                    val = prop.value[0]
                    arr = np.array([[val[0] / 360.0, val[1] / 100.0, val[2] / 100.0]])
                    clr = hsv2rgb(arr).tolist()[0]
                    return QColor.fromRgbF(*clr)
        if role == Qt.DecorationRole:
            if prop.prop_type == PropertyType.Vector:
                if prop.vector_viz is None:
                    viz = vector_to_img(prop.value[0], (128, 24))
                    # if not prop.up_to_date:
                    #     viz = np.dstack((viz,) * 3)
                    #     mask = np.array(viz[:, :, 0] > 200)[:, :, np.newaxis]
                    #     viz = np.where(mask, [[*self._invalid_property_bg_color.toTuple()[:3]]], [[0, 0, 0]])
                    prop.vector_viz = QPixmap.fromImage(qimage2ndarray.array2qimage(viz))
                return prop.vector_viz
        if role == MeasurementsTableRole.RegionProperty:
            return prop
        if role == Qt.ToolTipRole:
            if prop.prop_type == PropertyType.NDArray:
                val: np.ndarray = prop.value[0]
                return f'Double click to explore {val.shape[1:]} matrices for {",".join(prop.val_names)}'
            elif prop.prop_type in {PropertyType.IntensityHSV, PropertyType.Intensity}:
                return ', '.join([f'{v[0]:.3f} {v[1]}' for v in zip(prop.value[0], prop.val_names)])
        # if role == Qt.ItemDataRole.BackgroundRole and not prop.up_to_date:
        #     return QColor(180, 100, 0)
        # if role == Qt.ItemDataRole.DecorationRole and not prop.up_to_date:
        #     return IconStorage.instance()['caution']
        return None

    def headerData(self, section:int, orientation:PySide6.QtCore.Qt.Orientation, role:int=Qt.DisplayRole) -> typing.Any:
        if self.state.storage is None:
            return None
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.column_names[section]
            if orientation == Qt.Vertical:
                # return self.state.storage.image_names[section]
                return self.state.image_list_model.image_names[section]
        if orientation == Qt.Orientation.Vertical and (role == Qt.ItemDataRole.DecorationRole or role == Qt.ItemDataRole.ToolTipRole):
            photo = self.state.image_list_model.fetch_photo(section)
            if not photo['Labels'].has_valid_measurements():
                if role == Qt.ItemDataRole.DecorationRole:
                    return IconStorage.instance()['caution']
                if role == Qt.ItemDataRole.ToolTipRole:
                    return 'Measurements not updated for the latest segmentation.'
        return None

    def display_property(self, prop_key: str):
        self.displayed_property_key = prop_key
        lab_hierarchy = self.state.label_hierarchy
        header_labels = set()
        labels = set()
        for i in range(self.state.storage.image_count):
            # photo = self.state.storage.get_photo_by_idx(i, load_image=False)
            photo = self.state.image_list_model.fetch_photo(i)
            #header_labels = header_labels.union({self.state.colormap.label_names[prop.label] for prop in photo['Labels'].prop_list})
            labels = labels.union({prop.label for prop in photo['Labels'].prop_list})
        self.labels = list(labels)
        self.labels.sort()
        # TODO REMOVE
        #self.header_labels = [self.state.colormap.label_names[label] for label in self.labels]
        self.header_labels = [lab_hierarchy.nodes[label].name for label in self.labels]
        start = self.index(0, 0)
        end = self.index(self.rowCount() - 1, self.columnCount() - 1)
        self.dataChanged.emit(start, end)

    def display_intensity_in_color(self, in_color: bool = True):
        self._display_intensity_in_color = in_color
        start = self.index(0, 0)
        end = self.index(self.rowCount() - 1, self.columnCount() - 1)
        self.dataChanged.emit(start, end)

    def update_model(self):
        prop_tuple_set: typing.Set[typing.Tuple[Label, PropCompKey, LocalKey, PropName]] = set()
        for i in range(self.state.storage.image_count):
            photo = self.state.storage.get_photo_by_idx(i, load_image=False)
            for prop in photo[self.current_label_name].prop_list:
                #prop_tuple = (prop.info.key, prop.label, prop.info.name)
                prop_tuple = (prop.label, prop.prop_comp_key, prop.local_key, prop.info.name)
                prop_tuple_set.add(prop_tuple)
        self.prop_tuple_list = list(sorted(prop_tuple_set, key=lambda tup: tup[:3]))  # same count as column count
        #self.column_names = [f'{tup[2]}:{self.state.colormap.label_names[tup[1]]}' for tup in self.prop_tuple_list]
        self.column_names.clear()
        #cur_prop_key = ''
        # TODO replace hardcoded `Labels`
        hierarchy = self.state.storage.get_label_hierarchy(self.current_label_name)
        cur_label = -1
        for label, prop_comp_key, local_key, name in self.prop_tuple_list:
            #if cur_prop_key != key:
            #if cur_label != label:
                #col_name = f'{name}:{self.state.colormap.label_names[label]}'
                # TODO REMOVE
                #col_name = f'{self.state.colormap.label_names[label]}:{name}'
            col_name = f'{hierarchy.nodes[label].name}:{name}'
            #cur_label = label
                #cur_prop_key = key
            #else:
                #col_name = f':{self.state.colormap.label_names[label]}'
            #    col_name = f':{name}'
            self.column_names.append(col_name)
        start = self.index(0, 0)
        # end = self.index(self.rowCount()-1, self.columnCount() - 1)
        end = self.index(self.state.storage.image_count - 1, self.columnCount() - 1)
        self.dataChanged.emit(start, end)


