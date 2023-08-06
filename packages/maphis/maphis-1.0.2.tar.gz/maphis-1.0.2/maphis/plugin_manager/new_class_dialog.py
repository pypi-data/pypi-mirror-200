import typing

import PySide6
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QDialog, QDialogButtonBox

from maphis.common.new_plugin import make_snake_case
from maphis.plugin_manager.ui_new_class_dialog import Ui_NewClassDialog


class NewClassDialog(QDialog):
    def __init__(self, parent: typing.Optional[PySide6.QtWidgets.QWidget] = None,
                 f: Qt.WindowFlags = Qt.WindowFlags()):
        super().__init__(parent, f)

        self.ui = Ui_NewClassDialog()
        self.ui.setupUi(self)

        self.ui.txtName.textChanged.connect(self._update_key)
        self.ui.txtKey.setEnabled(False)
        self.ui.txtKey.setVisible(False)
        self.ui.lblKey.setVisible(False)
        self.ui.lblMethods.setVisible(False)
        self.ui.tableMethods.setVisible(False)
        self._btnOk = self.ui.buttonBox.button(QDialogButtonBox.Ok)
        self._btnCancel = self.ui.buttonBox.button(QDialogButtonBox.Cancel)

        self._btnOk.clicked.connect(self.accept)
        self._btnCancel.clicked.connect(self.reject)

    def _update_key(self, text: str):
        self.ui.txtKey.setText(make_snake_case(text.lower()))

    @property
    def name(self) -> str:
        return self.ui.txtName.text()

    @property
    def description(self) -> str:
        return self.ui.txtDescription.text()

    @property
    def key(self) -> str:
        return self.ui.txtKey.text()

    def clear_dialog(self):
        self.ui.txtKey.clear()
        self.ui.txtName.clear()
        self.ui.txtDescription.clear()

    def close_dialog(self):
        self.close()
        self.clear_dialog()
