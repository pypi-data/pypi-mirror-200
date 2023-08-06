import typing
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout

from maphis.common.action import Action, GeneralAction, RegionComputation, PropertyComputation
from maphis.common.new_plugin import create_new_plugin, ActionType
from maphis.common.plugin import Plugin, load_plugin
from maphis.common.plugin_utils import get_plugin_folders, get_plugin_folder
from maphis.common.state import State
from maphis.common.tool import Tool
from maphis.common.utils import open_with_default_app
from maphis.plugin_manager.computation_browser import ComputationBrowser
from maphis.plugin_manager.new_class_dialog import NewClassDialog
from maphis.plugin_manager.ui_plugin_browser import Ui_PluginBrowser
from maphis.plugin_manager.plugin_store import PluginStore


class PluginBrowser(QWidget):
    def __init__(self, state: State, plugin_store: PluginStore, parent: typing.Optional[QWidget] = None,
                 f: Qt.WindowFlags = Qt.Window):
        super().__init__(parent, f)

        self.ui = Ui_PluginBrowser()
        self.ui.setupUi(self)
        self.setVisible(False)

        self.state = state
        self.plugin_store: PluginStore = plugin_store

        self.plugin_store.plugins_updated.connect(lambda _: self.initialize())

        self._new_plugin_dialog: NewClassDialog = NewClassDialog()

        # self.plugins: typing.List[Plugin] = []

        self.initialize()

        self._initialize_tabs()

        self._connect_signals()

    def _connect_signals(self):
        self.ui.cmbPlugins.currentIndexChanged.connect(self.switch_to_plugin_by_idx)
        self.ui.btnCreatePlugin.clicked.connect(self._new_plugin_dialog.show)
        self.ui.btnReload.clicked.connect(self._reload_current_plugin)
        self.ui.btnOpenPluginFolder.clicked.connect(self._open_plugin_folder)

        self._new_plugin_dialog.accepted.connect(self._create_plugin)
        self._new_plugin_dialog.rejected.connect(self._new_plugin_dialog.close_dialog)

    def _open_plugin_folder(self):
        plugin: Plugin = self.ui.cmbPlugins.currentData()
        if plugin is None:
            return
        plugin_folder: Path = get_plugin_folder(plugin.info.key)
        open_with_default_app(plugin_folder)

    def _create_plugin(self):
        self.plugin_store.create_new_plugin(self._new_plugin_dialog.name, self._new_plugin_dialog.description)
        self._new_plugin_dialog.close_dialog()
        # self.load_plugins()

    def _reload_current_plugin(self):
        curr_plugin: Plugin = self.ui.cmbPlugins.currentData()
        if curr_plugin is None:
            return
        # reloaded = load_plugin(get_plugin_folder(curr_plugin.info.key))
        reloaded = self.plugin_store.reload_plugin(curr_plugin)
        if reloaded is None:
            return
        self.plugins[self.ui.cmbPlugins.currentIndex()] = reloaded
        self.ui.cmbPlugins.setItemData(self.ui.cmbPlugins.currentIndex(), reloaded)
        self.switch_to_plugin_by_idx(self.ui.cmbPlugins.currentIndex())

    def _initialize_tabs(self):
        self.computation_browser: typing.Dict[typing.Type[Action], typing.Tuple[ComputationBrowser, QWidget, ActionType]] = {
            GeneralAction: (ComputationBrowser(parent=self), self.ui.tabGeneralActions, ActionType.GeneralAction),
            RegionComputation: (ComputationBrowser(parent=self), self.ui.tabRegions, ActionType.RegionTemplate),
            PropertyComputation: (ComputationBrowser(parent=self), self.ui.tabProperties, ActionType.PropertyComputation),
            Tool: (ComputationBrowser(parent=self), self.ui.tabTools, ActionType.Tool)
        }

        for cls in [GeneralAction, Tool, RegionComputation, PropertyComputation]:
            layout: QVBoxLayout = QVBoxLayout()
            layout.addWidget(self.computation_browser[cls][0])
            self.computation_browser[cls][1].setLayout(layout)

    def switch_to_plugin_by_idx(self, idx: int):
        plugin: typing.Optional[Plugin] = self.ui.cmbPlugins.currentData()
        if plugin is None:
            return

        self.switch_to_plugin(plugin.info.key)
        # self.setWindowTitle(f'Plugin Browser - {plugin.info.name}')
        # self.ui.lblPluginDescription.setText(plugin.info.description)
        #
        # for cls, (cbrowse, _, action_type) in self.computation_browser.items():
        #     cbrowse.initialize_with(plugin, cls, action_type)

    def switch_to_plugin(self, plugin_key: str):
        plugin = self.plugin_store.plugins[plugin_key]
        self.setWindowTitle(f'Plugin Browser - {plugin.info.name}')
        self.ui.lblPluginDescription.setText(plugin.info.description)
        for cls, (cbrowse, _, action_type) in self.computation_browser.items():
            cbrowse.initialize_with(plugin, cls, action_type)

    def initialize(self):
        self.ui.cmbPlugins.clear()
        for plugin in self.plugin_store.plugins.values():
            self.ui.cmbPlugins.addItem(plugin.info.name, plugin)
