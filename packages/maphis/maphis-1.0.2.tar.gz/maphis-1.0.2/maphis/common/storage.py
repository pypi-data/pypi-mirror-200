import abc
import dataclasses
import re
import typing
from enum import IntEnum
from pathlib import Path
from typing import List, Dict, Set, Optional, Union, Any

import PySide6
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget

from maphis.common.label_hierarchy import LabelHierarchy
from maphis.common.label_image import LabelImgInfo, RegionProperty
from maphis.common.photo import Photo, Subscriber, UpdateContext, PhotoUpdate, UpdateEvent

TIF_REGEX = re.compile(".*\.tif")
IMAGE_REFEX = re.compile(".*\.(png|PNG|tiff|TIFF|tif|TIF|jpg|JPG|jpeg|JPEG)$")


TAG_PREFIX_REGEX = re.compile("(\w+\D+)\d*$")


@dataclasses.dataclass
class StorageUpdate:
    storage: 'Storage'
    tags_removed: typing.Set[str] = dataclasses.field(default_factory=set)
    tags_added: typing.Set[str] = dataclasses.field(default_factory=set)
    photos_included: typing.List[str] = dataclasses.field(default_factory=list)
    photos_removed: typing.List[str] = dataclasses.field(default_factory=list)
    # all_labels_properties_up_to_date: typing.Dict[str, bool] = dataclasses.field(default_factory=dict)


AddedTags = list
RemovedTags = list


class Storage(Subscriber):
    # update_photo = Signal([str, UpdateContext, dict])
    update_photo = Signal(UpdateEvent)
    photo_tags_update = Signal(Photo, AddedTags, RemovedTags)
    storage_update = Signal(StorageUpdate)
    all_labels_properties_up_to_date = Signal(str)

    def __init__(self, parent: typing.Optional[PySide6.QtCore.QObject] = None):
        super().__init__(parent)

    @property
    @abc.abstractmethod
    def storage_name(self) -> str:
        return ''

    @storage_name.setter
    def storage_name(self, name: str):
        pass

    @property
    @abc.abstractmethod
    def image_names(self) -> List[str]:
        return []

    @property
    @abc.abstractmethod
    def location(self) -> Path:
        return Path()

    @property
    @abc.abstractmethod
    def image_count(self) -> int:
        return 0

    @property
    @abc.abstractmethod
    def image_paths(self) -> List[Path]:
        return []

    @property
    @abc.abstractmethod
    def images(self) -> List[Photo]:
        return []

    @abc.abstractmethod
    def get_photo_by_name(self, name: str, load_image: bool=True) -> Photo:
        return Photo()

    @abc.abstractmethod
    def get_photo_by_idx(self, idx: int, load_image: bool=True) -> Photo:
        return Photo()

    @classmethod
    def load_from(cls, folder: Path, image_regex: re.Pattern=TIF_REGEX):
        return Storage()

    def reset_photo(self, photo: Photo):
        pass

    @property
    def label_hierarchy(self) -> LabelHierarchy:
        return LabelHierarchy()

    @label_hierarchy.setter
    def label_hierarchy(self, lab_hier):
        pass

    @property
    def label_image_names(self) -> Set[str]:
        return set()

    def get_label_hierarchy(self, label_name: str) -> Optional[LabelHierarchy]:
        return LabelHierarchy()

    def set_label_hierarchy(self, label_name: str, lab_hier: LabelHierarchy):
        pass

    def is_approved(self, index: int) -> bool:
        return False

    def save(self) -> bool:
        return False

    def include_photos(self, photo_names: List[str], scale: Optional[int]):
        pass

    def get_approval(self, name_or_index: Union[str, int], label_name: str) -> str:
        return ''

    def used_regions(self, label_name: str) -> Set[int]:
        return set()

    @property
    @abc.abstractmethod
    def default_label_image(self) -> str:
        return ''

    @property
    @abc.abstractmethod
    def label_img_info(self) -> Dict[str, LabelImgInfo]:
        return dict()

    # def notify(self, img_name: str, ctx: UpdateContext, data: Optional[Dict[str, typing.Any]] = None):
    def notify(self, event: UpdateEvent):
        pass

    @abc.abstractmethod
    def delete_photo(self, img_name: str, parent: QWidget) -> bool:
        return False

    def close_storage(self):
        pass

    @property
    def used_tags(self) -> typing.Set[str]:
        return set()

    def photos_satisfying_tags(self, tags: typing.Set[str]) -> typing.List[Photo]:
        return list()

    @property
    def tag_prefixes(self) -> typing.Set[str]:
        return {TAG_PREFIX_REGEX.match(tag).groups()[0] for tag in self.used_tags}

    @property
    def properties(self) -> typing.Dict[str, typing.Dict[str, RegionProperty]]:
        return dict()


_Storage = Storage()