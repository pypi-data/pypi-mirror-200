import typing
from typing import Optional

import PySide6
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout

from maphis.common.state import State
from maphis.common.storage import StorageUpdate, Storage
from maphis.common.utils import is_cursor_inside
from maphis.tags_widget import TagsPopupPanel
from maphis.tags.tag_chooser import TagsChooser


class TagFilterWidget(QWidget):
    def __init__(self, state: State, parent: typing.Optional[PySide6.QtWidgets.QWidget] = None,
                 f: PySide6.QtCore.Qt.WindowFlags = Qt.WindowFlags()):
        super().__init__(parent, f)

        self._state = state
        self._state.storage_changed.connect(self.change_storage)

        self._container = QVBoxLayout()
        self._main_layout = QHBoxLayout()

        self._label = QLabel(text='Tag filter:')
        self._main_layout.addWidget(self._label)

        self.tag_chooser: TagsChooser = TagsChooser(self._state, self)
        self.tag_chooser.set_button_visible(True)
        self.tag_chooser.button.setText('Clear')
        self.tag_chooser.matching_photo_count_label.setVisible(False)

        self.tag_chooser.selection_changed.connect(self._state.set_active_tags_filter)

        self._main_layout.addWidget(self.tag_chooser)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._container.addLayout(self._main_layout)

        self._lblPhotoCount = QLabel("")
        self._container.addWidget(self._lblPhotoCount)

        self.setLayout(self._container)

        self._state.tags_filter_changed.connect(self.handle_active_tags_changed)

    # def tag_checked(self, tag: str):
    #     self._state.toggle_filtering_tag(tag, True)
    #
    # def tag_unchecked(self, tag: str):
    #     self._state.toggle_filtering_tag(tag, False)

    # def initialize(self):
    #     self.tags_widget.storage = self._state.storage
    #     self._state.storage.storage_update.connect(self.handle_storage_update)
    #     self.tags_widget.populate()
    #     self.handle_active_tags_changed(self._state.active_tags_filter)

    def change_storage(self, old_storage: typing.Optional[Storage], new_storage: Storage):
        self._state.storage.storage_update.connect(self.handle_storage_update)

    def handle_active_tags_changed(self, active_tags: typing.List[str]):
        # self.tags_widget.update_tag_states()
        # self._tags_list.setText(', '.join(active_tags))
        # self._tags_list.setToolTip(self._tags_list.text())
        self.tag_chooser.set_selected_tags(active_tags, emit_signal=False)
        self._update_photo_count_message()

    def handle_storage_update(self, _: StorageUpdate):
        # self.tags_widget.populate()
        # self.tags_widget.update_tag_states()
        self.tag_chooser.tag_list_widget.popup.populate()
        self.handle_active_tags_changed(self._state.active_tags_filter)
        self._update_photo_count_message()

    def _update_photo_count_message(self):
        hidden_count = self._state.hidden_photos_count
        shown_count = self._state.storage.image_count - hidden_count
        self._lblPhotoCount.setText(f'Showing {shown_count} photo{"s" if shown_count != 1 else ""}{"" if hidden_count == 0 else f" ({hidden_count} hidden)"}.')

    # def handle_tags_filter_changed(self, _: typing.List[str]):
    #     self._tags_list.setText(', '.join(self._state.active_tags_filter))

    # def show_tags_panel_popup(self):
    #     if not self.isEnabled():
    #         return
    #     pos = self._tags_list.mapToGlobal(self._tags_list.rect().topRight())
    #     self.tags_widget.move(pos)
    #     self.tags_widget.show()

    # def deactivate(self):
    #     self._tags_list.blockSignals(True)
    #
    # def activate(self):
    #     self._tags_list.blockSignals(False)

    def enterEvent(self, event:PySide6.QtCore.QEvent):
        super(TagFilterWidget, self).enterEvent(event)

    def leaveEvent(self, event:PySide6.QtCore.QEvent):
        super(TagFilterWidget, self).leaveEvent(event)
        # cursor_pos = QCursor.pos()
        # tag_list_rect = self.tags_widget.rect().translated(self.tags_widget.pos())
        # if tag_list_rect.contains(cursor_pos):
        #     return
        # if is_cursor_inside(self.tags_widget):
        #     return
        # self.tags_widget.close()
