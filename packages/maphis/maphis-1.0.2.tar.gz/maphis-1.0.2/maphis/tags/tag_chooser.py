import typing
from typing import Optional

import PySide6.QtCore
import PySide6.QtGui
from PySide6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from maphis.common.state import State
from maphis.tags_widget import TagsPopupPanel

Tags = typing.List[str]


# TODO rename this to clearly communicate its purpose
class TagList(QLineEdit):
    hovered = PySide6.QtCore.Signal()
    tags_selection_changed = PySide6.QtCore.Signal(list)

    def __init__(self, state: State, placeholder: str, parent: typing.Optional[QWidget] = None):
        QLineEdit.__init__(self, parent)
        self._active_tags: typing.List[str] = []
        self.setReadOnly(True)
        self.setPlaceholderText(placeholder)
        self.state = state
        self.popup = TagsPopupPanel(state, parent=self)
        self.popup.populate()
        self.state.storage_changed.connect(lambda o, n: self.popup.populate())
        self.popup.tags_selection_changed.connect(self.update_tags_view_and_fire_signal)
        self._tag_separator: str = ' & '

    def update_tags_view_and_fire_signal(self, tags: typing.List[str]):
        self.setText(self._tag_separator.join(tags))
        self.tags_selection_changed.emit(tags)

    def enterEvent(self, event: PySide6.QtGui.QEnterEvent):
        super().enterEvent(event)
        self.hovered.emit()
        self.popup.show()
        self.popup.makePopup(self, event.pos() - PySide6.QtCore.QPoint(1, 0))

    def clear_tags(self, emit_signal: bool = True):
        self.popup.uncheck_all_tags(emit_signal)

    @property
    def tag_separator(self) -> str:
        return self._tag_separator

    @tag_separator.setter
    def tag_separator(self, sep: str):
        self._tag_separator = sep
        self.setText(self._tag_separator.join(self.popup.get_active_tags()))


class TagsChooser(QWidget):
    selection_changed = PySide6.QtCore.Signal(list)

    def __init__(self, state: State, parent: Optional[PySide6.QtWidgets.QWidget] = None,
                 f: PySide6.QtCore.Qt.WindowType = PySide6.QtCore.Qt.WindowType.Widget,
                 preceding_label='') -> None:
        super().__init__(parent, f)
        self._main_layout: QVBoxLayout = QVBoxLayout()

        self._layout: QHBoxLayout = QHBoxLayout()
        self.setLayout(self._main_layout)

        self.placeholder: str = 'hover to select tags'
        self.tag_list_widget: TagList = TagList(state, self.placeholder)
        self.tag_list_widget.tags_selection_changed.connect(self.selection_changed.emit)
        self.tag_list_widget.tags_selection_changed.connect(self._update_photo_count_label)

        self.button: QPushButton = QPushButton('x')
        self.button.setSizePolicy(PySide6.QtWidgets.QSizePolicy.Policy.Fixed,
                                  PySide6.QtWidgets.QSizePolicy.Policy.Fixed)

        if preceding_label:
            self.lblMedianOf = QLabel(preceding_label)
            self._layout.addWidget(self.lblMedianOf)
        self._layout.addWidget(self.tag_list_widget)
        self._layout.addWidget(self.button)

        self._main_layout.addLayout(self._layout)

        self.matching_photo_count_label: QLabel = QLabel()
        self._main_layout.addWidget(self.matching_photo_count_label)

        self.state = state

        self.button_handler: typing.Optional[typing.Callable[[], None]] = None

        self.make_button_clear_tags()
        self.set_button_visible(False)

    def set_placeholder(self, placeholder: str):
        self.placeholder = placeholder
        self.tag_list_widget.setPlaceholderText(self.placeholder)

    def set_button_visible(self, visible: bool):
        self.button.setVisible(visible)

    def make_button_clear_tags(self):
        self.clear_button_handler()
        self.button.clicked.connect(self.clear_tags)
        self.button_handler = self.clear_tags

    def clear_tags(self):
        self.tag_list_widget.clear_tags()

    def clear_button_handler(self):
        if self.button_handler is not None:
            self.button.clicked.disconnect(self.button_handler)
            self.button_handler = None

    def set_button_handler(self, handler: typing.Callable[[], None]):
        self.clear_button_handler()
        self.button.clicked.connect(handler)

    def set_selected_tags(self, tags: typing.List[str], emit_signal: bool = True):
        self.tag_list_widget.popup.uncheck_all_tags(emit_signal)
        for tag in tags:
            self.tag_list_widget.popup.tag_lines[tag].activate_tag(True, emit_signal)

    def selected_tags(self) -> Tags:
        return [tag_line.tag for tag_line in self.tag_list_widget.popup.tag_lines.values() if tag_line.is_checked]

    def set_popup_timeout(self, millis: int):
        self.tag_list_widget.popup.set_popup_timeout(millis)

    def _update_photo_count_label(self, selected_tags: typing.List[str]):
        if self.state.storage is None:
            self.matching_photo_count_label.clear()
        self.matching_photo_count_label.setText(f'{self.matching_photos_count} matching photo{"s" if self.matching_photos_count != 1 else ""}')

    @property
    def matching_photos_count(self) -> int:
        if self.state.storage is None:
            return 0
        return len(self.state.storage.photos_satisfying_tags(set(self.tag_list_widget.popup.get_active_tags())))
