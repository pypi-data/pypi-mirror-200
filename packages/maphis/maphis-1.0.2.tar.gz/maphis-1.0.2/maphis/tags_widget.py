import bisect
import typing
from enum import IntEnum

import PySide6
from PySide6 import QtCore
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QPushButton, QVBoxLayout, QScrollArea, QSizePolicy, \
    QDialog, QLineEdit, QLabel, QToolButton, QTableWidget, QTableWidgetItem, QGridLayout, QGroupBox

from maphis.common.photo import Photo, UpdateContext, UpdateEvent, PhotoUpdate, PhotoUpdateType
from maphis.common.state import State
from maphis.common.popup_widget import PopupWidget


class TagLine(QWidget):
    tag_delete_request = Signal(str)
    tag_toggled = Signal(str, bool)
    tag_assign_global = Signal(str)
    tag_checked = Signal(str)
    tag_unchecked = Signal(str)

    def __init__(self, tag: str, enabled: bool = True, parent: typing.Optional[PySide6.QtWidgets.QWidget] = None,
                 f: PySide6.QtCore.Qt.WindowFlags = Qt.WindowFlags()):
        super().__init__(parent, f)

        self.tag = tag
        self._layout = QHBoxLayout()
        self._checkbox = QCheckBox(text=tag)
        self._checkbox.setChecked(enabled)
        self._checkbox.toggled.connect(lambda b: self.tag_checked.emit(self.tag) if b else self.tag_unchecked.emit(self.tag))
        self._checkbox.toggled.connect(lambda b: self.tag_toggled.emit(self.tag, b))
        self._btn_delete = QToolButton(text="x")
        self._btn_delete.setToolTip("Delete tag from the project.")
        self._btn_delete.clicked.connect(lambda: self.tag_delete_request.emit(self.tag))

        self._btn_assign_global = QToolButton(text='all')
        self._btn_assign_global.setToolTip("Assign tag to all photos.")
        self._btn_assign_global.clicked.connect(lambda: self.tag_assign_global.emit(self.tag))

        self._layout.addWidget(self._checkbox)

        self.setLayout(self._layout)

    @property
    def is_checked(self) -> bool:
        return self._checkbox.isChecked()

    def activate_tag(self, activate: bool, emit_signal: bool = True):
        if not emit_signal:
            self._checkbox.blockSignals(True)
        self._checkbox.setChecked(activate)
        if not emit_signal:
            self._checkbox.blockSignals(False)


class TagsPopupPanel(PopupWidget):
    widget_left = Signal()
    tag_checked = Signal(str)
    tag_unchecked = Signal(str)
    tags_selection_changed = Signal(list)

    def __init__(self, state: State, title: str = 'Photo tags', parent: typing.Optional[PySide6.QtWidgets.QWidget] = None,
                 f: PySide6.QtCore.Qt.WindowType = PySide6.QtCore.Qt.WindowType.Popup |
                 PySide6.QtCore.Qt.WindowType.FramelessWindowHint):
        PopupWidget.__init__(self, parent=parent, f=f)
        self._state = state
        self.storage = self._state.storage
        self.setVisible(False)

        self.tag_lines: typing.Dict[str, TagLine] = {}

        self.main_layout = QVBoxLayout()

        self._tags_grid_layout = QGridLayout()
        self._tags_widget = QGroupBox()
        self._tags_widget.setTitle(title)
        self._tags_widget.setLayout(self._tags_grid_layout)

        self._tags_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.tags_sorted: typing.List[str] = []

        self.main_layout.addWidget(self._tags_widget)

        self.setLayout(self.main_layout)
        self.setMaximumHeight(200)

        self.is_hovered: bool = False

        self._lblNoTags = QLabel(text="no tags")
        self._tags_grid_layout.addWidget(self._lblNoTags, 0, 0)

        self.popup_timeout: int = 200
        self.timer_id: int = -1

    def _add_tag_line(self, tag: str, enabled: bool = True) -> TagLine:
        tag_widget = TagLine(tag, enabled)
        if len(self.tag_lines) == 0:
            self._lblNoTags.hide()
            self._tags_grid_layout.removeWidget(self._lblNoTags)
        return tag_widget

    def _connect_tag_line_signals(self, tag_line: TagLine):
        tag_line.tag_checked.connect(self.tag_checked.emit)
        tag_line.tag_unchecked.connect(self.tag_unchecked.emit)

        tag_line.tag_checked.connect(self.relay_tags_selection)
        tag_line.tag_unchecked.connect(self.relay_tags_selection)

    def relay_tags_selection(self):
        tags: typing.List[str] = [tag_line.tag for tag_line in self.tag_lines.values() if tag_line.is_checked]
        self.tags_selection_changed.emit(tags)

    def clear_tags(self):
        for tag in self.tag_lines.values():
            self._tags_grid_layout.removeWidget(tag)
            tag.deleteLater()
        self.tag_lines.clear()
        self.tags_sorted.clear()

    def populate(self):
        self.clear_tags()
        if self._state.storage is None:
            return
        self.tags_sorted = list(sorted(self._state.storage.used_tags))
        if len(self.tags_sorted) == 0:
            self._tags_grid_layout.addWidget(self._lblNoTags, 0, 0)
            self._lblNoTags.show()
        else:
            self._lblNoTags.hide()
            self._tags_grid_layout.removeWidget(self._lblNoTags)
        for row, tag in enumerate(self.tags_sorted):
            if tag not in self.tag_lines:
                tag_widget = self._add_tag_line(tag, False)
                self._connect_tag_line_signals(tag_widget)
                self.tag_lines[tag] = tag_widget
                self._tags_grid_layout.addWidget(tag_widget, row, 0)

    def update_tag_states(self):
        for tag, tag_line in self.tag_lines.items():
            tag_line.blockSignals(True)
            tag_line._checkbox.setChecked(tag in self._state.active_tags_filter)
            tag_line.blockSignals(False)

    def uncheck_all_tags(self, emit_signal: bool = True):
        for tag_line in self.tag_lines.values():
            # tag_line._checkbox.setChecked(False)
            tag_line.activate_tag(False, emit_signal)
        if emit_signal:
            self.tags_selection_changed.emit([tag_line.tag for tag_line in self.tag_lines.values() if tag_line.is_checked])

    def check_all_tags(self, emit_signal: bool = True):
        for tag_line in self.tag_lines.values():
            # tag_line._checkbox.setChecked(True)
            tag_line.activate_tag(True, emit_signal)
        if emit_signal:
            self.tags_selection_changed.emit([tag_line.tag for tag_line in self.tag_lines.values() if tag_line.is_checked])

    def set_popup_timeout(self, millis: int):
        self.popup_timeout = max(0, millis)

    def get_active_tags(self) -> typing.List[str]:
        return [tag_line.tag for tag_line in self.tag_lines.values() if tag_line.is_checked]


class PhotoTagsPopupPanel(TagsPopupPanel):
    def __init__(self, photo: Photo, state: State, parent: typing.Optional[PySide6.QtWidgets.QWidget] = None,
                 f: PySide6.QtCore.Qt.WindowFlags = Qt.WindowFlags()):
        super().__init__(state, parent=parent, f=f)
        self.photo = photo
        self.tags = photo.tags

        self.populate()

        lay = QHBoxLayout()
        self.lblNewTag = QLabel(text="New tag: ")
        self.txtNewTag = QLineEdit()
        self.txtNewTag.setPlaceholderText('enter a new tag and confirm with <Enter>')

        self.txtNewTag.returnPressed.connect(self._handle_confirm_new_tag)

        lay.addWidget(self.lblNewTag)
        lay.addWidget(self.txtNewTag)

        self.main_layout.addLayout(lay)

        state.storage.update_photo.connect(self.handle_photo_update)

    def _handle_confirm_new_tag(self):
        if len(self.txtNewTag.text()) == 0 or self.txtNewTag.text().isspace():
            return
        self.photo.add_tag(self.txtNewTag.text())
        self.txtNewTag.clear()

    def _add_tag_line(self, tag: str, enabled: bool = True) -> TagLine:
        tag_widget = super(PhotoTagsPopupPanel, self)._add_tag_line(tag, enabled)
        return tag_widget

    def handle_photo_update(self, update: UpdateEvent):
        if update.photo.image_name != self.photo.image_name:
            return
        event_obj: PhotoUpdate = update.update_obj
        if event_obj.update_type != PhotoUpdateType.TagsUpdated:
            return
        for tag in event_obj.tags_added: #data['tags']['added']:
            if tag not in self.tag_lines:
                tag_widget = self._add_tag_line(tag)
                self._connect_tag_line_signals(tag_widget)
                self.tag_lines[tag] = tag_widget
                position = bisect.bisect(self.tags_sorted, tag)
                for i in range(position, len(self.tags_sorted)):
                    tag_to_move = self.tags_sorted[i]
                    tag_widget_to_move = self.tag_lines[tag_to_move]
                    self._tags_grid_layout.removeWidget(tag_widget_to_move)
                self.tags_sorted.insert(position, tag)
                for row in range(position, len(self.tags_sorted)):
                    tag_to_insert = self.tags_sorted[row]
                    tag_widget_to_insert = self.tag_lines[tag_to_insert]
                    self._tags_grid_layout.addWidget(tag_widget_to_insert, row, 0)
            else:
                self.tag_lines[tag].blockSignals(True)
                self.tag_lines[tag]._checkbox.setChecked(True)
                self.tag_lines[tag].blockSignals(False)

    def _connect_tag_line_signals(self, tag_line: TagLine):
        tag_line.tag_toggled.connect(self.photo.toggle_tag)

    def populate(self):
        super().populate()
        for tag in self.photo.tags:
            tag_widget = self.tag_lines[tag]
            tag_widget.blockSignals(True)
            tag_widget._checkbox.setChecked(True)
            tag_widget.blockSignals(False)

