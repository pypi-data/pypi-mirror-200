import pathlib
import typing
from datetime import datetime
from pathlib import Path
from typing import List

import PySide6
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, QSortFilterProxyModel, QLocale
from PySide6.QtWidgets import QWidget

from maphis.common.local_storage import Storage
from maphis.common.photo import Photo, UpdateContext, UpdateEvent, PhotoUpdate, PhotoUpdateType
from maphis.common.storage import StorageUpdate
from maphis.thumbnail_storage import ThumbnailStorage_

ROLE_IMAGE_NAME = Qt.UserRole + 1
ROLE_THUMBNAIL = Qt.UserRole + 3
ROLE_IS_APPROVED = Qt.UserRole + 42
ROLE_APPROVAL_COUNT = Qt.UserRole + 4
ROLE_IS_HIGHLIGHTED = Qt.UserRole + 5
ROLE_HAS_UNSAVED_CHANGES = Qt.UserRole + 6
ROLE_SCALE_MARKER_IMAGE = Qt.UserRole + 7
ROLE_IMAGE_PATH = Qt.UserRole + 8
ROLE_TAGS = Qt.UserRole + 9
ROLE_IMPORT_TIME = Qt.ItemDataRole.UserRole + 10
ROLE_PHOTO = Qt.ItemDataRole.UserRole + 11


class ImageListModel(QAbstractListModel):

    def __init__(self, parent: QWidget = None):
        QAbstractListModel.__init__(self, parent)

        self.highlighted_indexes: List[int] = []
        self.image_paths: List[Path] = []
        # self.thumbnails: Optional[ThumbnailStorage] = None
        self.dragging = False
        self.storage: typing.Optional[Storage] = None
        # self.thumbnail_storage: typing.Optional[Storage] = None

    def initialize(self, image_paths: List[Path], thumbnail_storage: ThumbnailStorage_, processed_count: int, storage: Storage) -> bool:
        self.storage = storage
        self.storage.update_photo.connect(self._handle_photo_update)
        self.storage.storage_update.connect(self._handle_storage_update)
        self.thumbnail_storage = thumbnail_storage
        self.thumbnail_storage.update_photo.connect(self._handle_thumbnail_update)
        self.highlighted_indexes = []
        # if self.thumbnails is not None:
        #     self.thumbnails.thumbnails_loaded.disconnect(self.handle_thumbnails_loaded)
        # self.thumbnails = thumbnail_storage
        # self.thumbnails.thumbnails_loaded.connect(self.handle_thumbnails_loaded)
        self.beginResetModel()
        self.image_paths = image_paths
        self.endResetModel()
        self.dataChanged.emit(self.index(0, 0), self.index(len(self.image_paths), 0))

    def rowCount(self, parent: QModelIndex = QModelIndex()):
        return 0 if self.storage is None else self.storage.image_count

    def columnCount(self, parent: QModelIndex = QModelIndex()):
        return 1

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        photo = self.storage.get_photo_by_idx(index.row(), load_image=False)
        if role == Qt.DisplayRole:
            if index.column() == 0:
                # return self.storage.image_names[index.row()]
                return '.'.join(self.storage.image_names[index.row()].split('.')[:-1])
            return None
        if role == Qt.ItemDataRole.ToolTipRole:
            locale = QLocale.system()
            datetime_format = locale.dateTimeFormat()
            # return f'Imported at: {datetime.fromtimestamp(self.storage.get_photo_by_idx(index.row(), load_image=False).import_time)}'
            return f'Imported at: {photo.import_time.toString(datetime_format)}'
        if role == ROLE_IMAGE_NAME:
            return self.storage.image_names[index.row()]

        if role == ROLE_THUMBNAIL and index.column() == 0:
            photo = self.storage.get_photo_by_idx(index.row(), load_image=False)
            return photo.thumbnail

        if role == ROLE_IS_APPROVED:
            return self.storage.is_approved(index.row())

        if role == ROLE_APPROVAL_COUNT:
            photo = self.storage.get_photo_by_idx(index.row(), load_image=False)
            approval = photo.approved['Labels']
            mask_names = self.storage.get_label_hierarchy('Labels').mask_names
            approval_count = 0 if approval is None else mask_names.index(approval) + 1
            return approval_count, len(mask_names)
        if role == ROLE_IS_HIGHLIGHTED:
            if len(self.highlighted_indexes) > 0:
                return index.row() in self.highlighted_indexes
            return True
        if role == ROLE_HAS_UNSAVED_CHANGES:
            return self.storage.get_photo_by_idx(index.row(), load_image=False).has_unsaved_changes

        if role == ROLE_SCALE_MARKER_IMAGE:
            photo = self.storage.get_photo_by_idx(index.row(), load_image=False)
            if photo.scale_setting is None:
                return None
            return photo.scale_setting.scale_marker_img
        if role == ROLE_IMAGE_PATH:
            return self.storage.get_photo_by_idx(index.row(), load_image=False).image_path

        if role == ROLE_TAGS:
            return self.storage.get_photo_by_idx(index.row(), load_image=False).tags

        if role == ROLE_IMPORT_TIME:
            return self.storage.get_photo_by_idx(index.row(), load_image=False).import_time

        if role == ROLE_PHOTO:
            return self.storage.get_photo_by_idx(index.row(), load_image=False)

        return None

    def highlight_indexes(self, idxs: List[int]):
        self.highlighted_indexes = idxs
        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(self.rowCount() - 1, 0))

    def handle_slider_pressed(self):
        self.dragging = True

    def handle_slider_released(self, first_index: QModelIndex, last_index: QModelIndex):
        self.dragging = False
        # self.thumbnails.load_thumbnails(first_index.row() - 50, last_index.row() + 50)

    def handle_thumbnails_loaded(self, indices: List[int]):
        fidx = self.index(indices[0], 0, QModelIndex())
        lidx = self.index(indices[-1], 0, QModelIndex())
        self.dataChanged.emit(fidx, lidx, [ROLE_THUMBNAIL])

    def handle_approval_changed(self, photo: Photo):
        idx = self.storage.image_names.index(photo.image_name)
        index = self.index(idx, 0, QModelIndex())
        self.dataChanged.emit(index, index, [ROLE_IS_APPROVED])

    # def _handle_photo_update(self, img_name: str, ctx: UpdateContext, data: typing.Dict[str, typing.Any]):
    def _handle_photo_update(self, update: UpdateEvent):
        index = self.index(self.storage.image_names.index(update.photo.image_name), 0, QModelIndex())
        # if 'tags' in data:
        event_obj: PhotoUpdate = update.update_obj
        roles: typing.List[int] = [ROLE_HAS_UNSAVED_CHANGES]
        if event_obj.update_type == PhotoUpdateType.TagsUpdated:
            roles.append(ROLE_TAGS)
        self.dataChanged.emit(index, index, roles)

    def _handle_storage_update(self, update: StorageUpdate):
        # if 'photos' in data:
        #     if 'deleted' in data['photos']:
        if len(update.photos_removed) > 0:
            self.beginResetModel()
            self.endResetModel()

    # def _handle_thumbnail_update(self, img_name: str, ctx: UpdateContext, data: typing.Dict[str, typing.Any]):
    def _handle_thumbnail_update(self, update: UpdateEvent):
        i = self.storage.image_names.index(update.photo.image_name)
        idx = self.index(i, 0, QModelIndex())
        self.dataChanged.emit(idx, idx, [ROLE_THUMBNAIL])

    def fetch_photo(self, idx: int) -> typing.Optional[Photo]:
        index = self.index(idx, 0, QModelIndex())
        if not index.isValid():
            return None
        return index.data(ROLE_PHOTO)

    def fetch_first_photo(self) -> typing.Optional[Photo]:
        return self.fetch_photo(0)

    def fetch_last_photo(self) -> typing.Optional[Photo]:
        return self.fetch_photo(self.rowCount() - 1)


class ImageListSortFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, parent: typing.Optional[PySide6.QtCore.QObject] = None):
        super().__init__(parent)
        # self._state = state
        self._filter_tags: typing.Set[str] = set()
        self.source_model: typing.Optional[ImageListModel] = None

    def filterAcceptsRow(self, source_row: int, source_parent: PySide6.QtCore.QModelIndex) -> bool:
        index = self.sourceModel().index(source_row, 0, source_parent)
        tags: typing.Set[str] = self.sourceModel().data(index, ROLE_TAGS)
        # return self.filterRegExp().pattern() in tags
        return self._filter_tags.issubset(tags)
        # return set(self._state.active_tags_filter).issubset(tags)

    def setSourceModel(self, source_model: ImageListModel) -> None:
        self.source_model = source_model
        super().setSourceModel(source_model)

    # @property
    # def storage(self) -> Storage:
    #     return self._state.storage

    def fetch_photo(self, index: int) -> typing.Optional[Photo]:
        index = self.mapToSource(self.index(index, 0, QModelIndex()))
        if not index.isValid():
            return None
        return index.data(ROLE_PHOTO)

    def fetch_first_photo(self) -> typing.Optional[Photo]:
        return self.fetch_photo(0)

    def fetch_last_photo(self) -> typing.Optional[Photo]:
        return self.fetch_photo(self.rowCount(QModelIndex()) - 1)

    @property
    def image_paths(self) -> typing.List[pathlib.Path]:
        paths: typing.List[Path] = []
        for row in range(self.rowCount(QModelIndex())):
            photo_idx = self.index(row, 0, QModelIndex())
            photo: Photo = photo_idx.data(ROLE_PHOTO)
            paths.append(photo.image_path)
        return paths

    @property
    def image_names(self) -> typing.List[str]:
        return [path.name for path in self.image_paths]

    def set_filter_tags(self, tags: typing.Collection[str]):
        self._filter_tags = set(tags)
        self.invalidate()