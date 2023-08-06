import bisect
import typing
from enum import IntEnum
from typing import Optional

import PySide6.QtCore
import PySide6.QtWidgets
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit

from maphis.common.popup_widget import PopupWidget
from maphis.common.choice import Choice


class ChoiceOrder(IntEnum):
    Alphabetical = 0,
    Chronological = 1,


class ChoicePopupPanel(PopupWidget):
    selection_changed = PySide6.QtCore.Signal(list)

    def __init__(self, choice_list: typing.Optional[typing.Sequence[typing.Any]],
                 choice_order: ChoiceOrder = ChoiceOrder.Alphabetical,
                 popup_timeout_millis: int = 200, parent: Optional[PySide6.QtWidgets.QWidget] = None,
                 f: PySide6.QtCore.Qt.WindowType = PySide6.QtCore.Qt.WindowType.Popup) -> None:
        super().__init__(popup_timeout_millis, parent, f)

        self.choice_list: typing.Optional[typing.List[typing.Union[str, int, float]]] = None
        self.choice_widgets: typing.List[Choice] = []
        self.choices_deletable: bool = False

        # main layout for the whole widget
        self.main_layout: QVBoxLayout = QVBoxLayout()

        # layout for the choice entries
        self.choices_layout: QVBoxLayout = QVBoxLayout()

        # layout for the qlabel, lineedit
        self.add_new_choice_layout: QHBoxLayout = QHBoxLayout()
        self.add_new_option_label: QLabel = QLabel("Add new option:")
        self.add_new_choice_layout.addWidget(self.add_new_option_label)

        self.new_choice_field: QLineEdit = QLineEdit()
        self.new_choice_field.setPlaceholderText('enter new option')
        self.new_choice_field.returnPressed.connect(self._create_new_choice)
        # self.new_choice_field.returnPressed.connect(lambda: self.add_new_choice(self.new_choice_field.text()))

        self.add_new_choice_layout.addWidget(self.new_choice_field)

        self.main_layout.addLayout(self.choices_layout)
        self.main_layout.addLayout(self.add_new_choice_layout)

        self.setLayout(self.main_layout)

        self.choice_order: ChoiceOrder = choice_order

        if choice_list is not None:
            self.set_choice_list(choice_list)

        self.allow_adding_choices(False)

    def set_choice_list(self, choices: typing.Sequence[typing.Union[str, int, float]]):
        self.clear_choices()
        self.choice_list = []

        for choice in choices:
            self.add_new_choice(str(choice))

    def add_new_choice(self, choice_str: str) -> Choice:
        choice = Choice(choice_str)
        choice.delete_requested.connect(self.delete_choice)
        choice.check_state_changed.connect(lambda: self.selection_changed.emit(self.selection))
        choice.btnDelete.setVisible(self.choices_deletable)
        insert_idx = self._new_choice_position(choice_str)
        self.choice_widgets.insert(insert_idx, choice)
        self.choice_list.insert(insert_idx, choice_str)
        self.choices_layout.insertWidget(insert_idx, choice)

        return choice

    def clear_choices(self):
        for choice in self.choice_widgets:
            choice.setVisible(False)
            self.choices_layout.removeWidget(choice)
            choice.deleteLater()
        self.choice_widgets.clear()
        self.choice_list = []
        self.selection_changed.emit(self.selection)

    @property
    def selection(self) -> typing.List[str]:
        selection = []
        for choice_widg in self.choice_widgets:
            if choice_widg.checkbox.isChecked():
                selection.append(choice_widg.checkbox.text())
        return selection

    @selection.setter
    def selection(self, selection: typing.List[str]):
        for choice_widg in self.choice_widgets:
            choice_widg.checkbox.setChecked(choice_widg.checkbox.text() in selection)

    def delete_choice(self, choice: Choice):
        choice.setVisible(False)
        self.choice_list.remove(choice.checkbox.text())
        self.choices_layout.removeWidget(choice)
        self.choice_widgets.remove(choice)
        self.selection_changed.emit(self.selection)

    def allow_adding_choices(self, allow: bool):
        self.add_new_option_label.setVisible(allow)
        self.new_choice_field.setVisible(allow)

    def allow_deleting_choices(self, allow: bool):
        self.choices_deletable = allow
        for choice in self.choice_widgets:
            choice.btnDelete.setVisible(self.choices_deletable)

    def _create_new_choice(self):
        self.add_new_choice(self.new_choice_field.text())
        self.new_choice_field.clear()

    def choice_position(self, choice: str) -> int:
        try:
            return self.choice_list.index(choice)
        except ValueError:
            return -1

    def _new_choice_position(self, choice: str) -> int:
        if self.choice_order == ChoiceOrder.Chronological:
            return len(self.choice_list)
        else:
            return bisect.bisect(self.choice_list, choice)

    def choice_enabled_tuples(self) -> typing.List[typing.Tuple[Choice, bool]]:
        return [(choice, choice.is_checked) for choice in self.choice_widgets]

    @property
    def choices(self) -> typing.List[Choice]:
        return self.choice_widgets
