import typing
from enum import IntEnum
from typing import Optional

import PySide6.QtCore
import PySide6.QtWidgets

from maphis.common.choice import Choice
from maphis.common.choice_popup_panel import ChoicePopupPanel
from maphis.common.photo import Photo
from maphis.common.state import State
from maphis.common.storage import Storage


class TagsSource(IntEnum):
    Storage = 0,
    Photo = 1


class TagsPopupPanel(ChoicePopupPanel):
    def __init__(self, state: State, popup_timeout_millis: int = 200,
                 parent: Optional[PySide6.QtWidgets.QWidget] = None,
                 f: PySide6.QtCore.Qt.WindowType = PySide6.QtCore.Qt.WindowType.Popup) -> None:
        super().__init__(None, popup_timeout_millis, parent, f)
        self.state: State = state
        self.storage: typing.Optional[Storage] = None
        self.photo: typing.Optional[Photo] = None
        self.new_choice_field.returnPressed.disconnect(super()._create_new_choice)

    def set_choice_list(self, choices: typing.Sequence[typing.Union[str, int, float]]):
        super().set_choice_list(choices)

    def add_new_choice(self, choice_str: str) -> Choice:
        return super().add_new_choice(choice_str)

    def clear_choices(self):
        super().clear_choices()

    @property
    def selection(self) -> typing.List[str]:
        return super().selection

    def delete_choice(self, choice: Choice):
        super().delete_choice(choice)

    def allow_adding_choices(self, allow: bool):
        super().allow_adding_choices(allow)

    def allow_deleting_choices(self, allow: bool):
        # super().allow_deleting_choices(allow)
        pass

    def _populate_choice_list(self):
        self.clear_choices()
        for tag in sorted(self.storage.used_tags):
            choice_widg = self.add_new_choice(tag)
            if self.photo is not None:
                if tag in self.photo.tags:
                    choice_widg.blockSignals(True)
                    choice_widg.checkbox.setChecked(True)
                    choice_widg.blockSignals(False)

    def set_storage(self, storage: Storage):
        if self.storage is not None:
            self.storage.photo_tags_update.disconnect(self.handle_photo_tags_update)
            self.storage.storage_update.disconnect(self.handle_storage_tags_update)
        self.storage = storage
        self.storage.photo_tags_update.connect(self.handle_photo_tags_update)
        self.photo = None
        self._populate_choice_list()

    def set_photo(self, photo: Photo):
        self.photo = photo
        self.new_choice_field.setVisible(True)
        self.add_new_option_label.setVisible(True)
        self._populate_choice_list()

    def unset_photo(self):
        self.photo = None
        self._populate_choice_list()

    def _create_new_choice(self):
        if self.photo is not None:
            self.photo.add_tag(self.new_choice_field.text())

    def handle_photo_tags_update(self, photo: Photo, tags_added: typing.List[str], tags_removed: typing.List[str]):
        if self.photo is None or photo.image_path != self.photo.image_path:
            return
        self.clear_choices()
        self._populate_choice_list()