from typing import Optional

import PySide6.QtCore
import PySide6.QtWidgets
from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QCheckBox


class Choice(QWidget):
    delete_requested = PySide6.QtCore.Signal(QWidget)
    check_state_changed = PySide6.QtCore.Signal(QWidget, bool)

    def __init__(self, choice_str: str, deletable: bool = False, parent: Optional[PySide6.QtWidgets.QWidget] = None,
                 f: PySide6.QtCore.Qt.WindowType = PySide6.QtCore.Qt.WindowType.Window) -> None:
        super().__init__(parent, f)

        self.main_layout: QHBoxLayout = QHBoxLayout()

        self.checkbox: QCheckBox = QCheckBox(text=choice_str)
        self.checkbox.toggled.connect(lambda b: self.check_state_changed.emit(self, b))

        self.btnDelete: QPushButton = QPushButton(text='x')
        self.btnDelete.clicked.connect(lambda: self.delete_requested.emit(self))
        self.btnDelete.setVisible(deletable)

        self.main_layout.addWidget(self.checkbox)
        self.main_layout.addWidget(self.btnDelete)

        self.setLayout(self.main_layout)

    @property
    def is_checked(self) -> bool:
        return self.checkbox.isChecked()