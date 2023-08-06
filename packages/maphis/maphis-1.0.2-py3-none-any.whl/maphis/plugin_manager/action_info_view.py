import typing
from typing import Optional

import PySide6.QtCore
import PySide6.QtWidgets
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget
from maphis.common.action import Action, PropertyComputation
from maphis.plugin_manager.ui_action_info_view import Ui_ActionInfoView


class ActionInfoView(QWidget):
    def __init__(self, parent: Optional[PySide6.QtWidgets.QWidget] = None,
                 f: PySide6.QtCore.Qt.WindowType = Qt.WindowType.Widget) -> None:
        super().__init__(parent, f)

        self.ui = Ui_ActionInfoView()
        self.ui.setupUi(self)

        self.displayed_action: typing.Optional[Action] = None

        self.clear_ui()

    def set_action(self, action: Action):
        self.clear_ui()
        self.displayed_action = action
        # TODO clear the UI
        if self.displayed_action is None:
            return
        self.ui.txtDescription.setPlainText(action.info.description)
        # TODO set `user params` ui
        if issubclass(type(self.displayed_action), PropertyComputation):
            self.ui.grpComputes.setVisible(True)
            # set `computes`
            pass

    def clear_ui(self):
        self.ui.txtDescription.clear()

        self.ui.tableComputes.clear()
        self.ui.grpComputes.setVisible(False)

        self.ui.tableUserParameters.clear()
        self.ui.grpUserParameters.setVisible(False)