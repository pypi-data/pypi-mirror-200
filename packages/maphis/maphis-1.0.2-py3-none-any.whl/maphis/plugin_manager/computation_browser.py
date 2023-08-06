from importlib import resources
import os
import platform
import subprocess
import typing
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from maphis.common.action import GeneralAction, PropertyComputation, RegionComputation, Action
from maphis.common.new_plugin import ActionType, new_computation, make_snake_case
from maphis.common.plugin import Plugin
from maphis.common.tool import Tool
from maphis.common.utils import open_with_default_app
from maphis.plugin_manager.new_class_dialog import NewClassDialog
from maphis.plugin_manager.ui_computation_browser import Ui_ComputationBrowser
from maphis.plugin_manager.action_info_view import ActionInfoView


class ComputationBrowser(QWidget):
    def __init__(self, parent: typing.Optional[QWidget] = None,
                 f: Qt.WindowFlags = Qt.WindowFlags()):
        super().__init__(parent, f)

        self.ui = Ui_ComputationBrowser()
        self.ui.setupUi(self)

        self.current_plugin: typing.Optional[Plugin] = None
        self.current_cls: typing.Optional[typing.Type[Action]] = None
        self.current_actions: typing.List[Action] = []
        self.current_action: typing.Optional[Action] = None
        self.current_action_type: ActionType = ActionType.GeneralAction

        self._new_class_dialog = NewClassDialog()

        self.action_info_view: ActionInfoView = ActionInfoView()
        self.ui.layoutActionInfoView.addWidget(self.action_info_view)

        self._connect_signals()

    def _connect_signals(self):
        self.ui.cmbComputations.currentIndexChanged.connect(self.switch_to_action_by_idx)
        self.ui.btnOpenEditor.clicked.connect(self._open_action_in_editor)
        self.ui.btnCreateComputation.clicked.connect(self._new_class_dialog.show)
        self.ui.btnReload.clicked.connect(self._reload_computation)

        self._new_class_dialog.accepted.connect(self._create_new_computation)
        self._new_class_dialog.rejected.connect(self._new_class_dialog.close_dialog)

    def _reload_computation(self):
        self.current_plugin.reload()
        curr_action = self.ui.cmbComputations.currentData()
        self.initialize_with(self.current_plugin, self.current_cls, self.current_action_type)
        if curr_action is None:
            return
        idx = [action.info.key for action in self.current_actions].index(curr_action.info.key)
        self.ui.cmbComputations.setCurrentIndex(idx)

    def _create_new_computation(self):
        comp_path: Path = new_computation(self.current_plugin.info.key, self.current_cls, self._new_class_dialog.name,
                       self._new_class_dialog.description, self._new_class_dialog.key)
        open_with_default_app(comp_path)
        self._reload_computation()

    def _open_action_in_editor(self):
        action: Action = self.ui.cmbComputations.currentData()
        if action is None:
            return
        splits = action.info.key.split('.')
        package = '.'.join(splits[:-1])
        py_file = splits[-1] + '.py'
        with resources.path(package, py_file) as p:
            open_with_default_app(p)

    def switch_to_action_by_idx(self, idx: int):
        action: Action = self.ui.cmbComputations.currentData()
        # if action is None:
        #     self.ui.txtDescription.setPlainText('')
        #     return
        # self.ui.txtDescription.setPlainText(action.info.description)
        self.action_info_view.set_action(action)
        self.current_action = action

    def initialize_with(self, plugin: typing.Optional[Plugin], cls: typing.Union[
        typing.Type[RegionComputation], typing.Type[PropertyComputation], typing.Type[GeneralAction], typing.Type[Tool]],
                        action_type: ActionType):
        self.ui.cmbComputations.clear()
        if plugin is None:
            # TODO clear the UI
            return
        self.current_actions = plugin.get_actions(cls)

        self.current_action_type = action_type
        self.current_cls = cls
        self.current_plugin = plugin
        for action in self.current_actions:
            self.ui.cmbComputations.addItem(action.info.name, action)
        self.ui.cmbComputations.setEnabled(len(self.current_actions) > 0)
        self.ui.btnReload.setEnabled(len(self.current_actions) > 0)
        self.ui.btnOpenEditor.setEnabled(len(self.current_actions) > 0)