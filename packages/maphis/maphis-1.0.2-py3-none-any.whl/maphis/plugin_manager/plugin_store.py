from __future__ import annotations

import functools
import typing
from pathlib import Path

import PySide6
from PySide6.QtCore import QObject, Signal

from maphis.common.new_plugin import create_new_plugin
from maphis.common.plugin import Plugin, load_plugin
from maphis.common.plugin_utils import get_plugin_folders, get_plugin_folder
from maphis.common.action import GeneralAction, RegionComputation, PropertyComputation, Action
from maphis.common.tool import Tool


class PluginStore(QObject):
    plugin_registered = Signal(Plugin)
    plugin_unregistered = Signal(Plugin)
    plugins_updated = Signal(dict)
    plugin_updated = Signal(Plugin)

    _instance: typing.Optional[PluginStore] = None

    def __init__(self, parent: typing.Optional[PySide6.QtCore.QObject] = None) -> None:
        super().__init__(parent)

        # self.plugins: typing.List[Plugin] = []
        self.plugins: typing.Dict[str, Plugin] = {}
        self.load_plugins()

    @classmethod
    def instance(cls) -> PluginStore:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_plugins(self):
        self.plugins.clear()
        for plugin_path in get_plugin_folders():
            plugin = load_plugin(Path(plugin_path))
            print(f'loading {plugin_path}')
            if plugin is None:
                continue
            # self.plugins.append(plugin)
            self.plugins[plugin.info.key] = plugin
        self.plugins_updated.emit(self.plugins)

    def create_new_plugin(self, plugin_name: str, plugin_desc: str):
        # TODO check for name clashes
        create_new_plugin(plugin_name, plugin_desc)
        self.load_plugins()

    def reload_plugin(self, plugin: Plugin) -> typing.Optional[Plugin]:
        if plugin.info.key not in self.plugins:
            return None
        # TODO handle possible failure to load
        reloaded = load_plugin(get_plugin_folder(plugin.info.key))
        self.plugins[plugin.info.key] = reloaded
        self.plugin_updated.emit(reloaded)
        return reloaded

    @property
    def all_general_actions(self) -> typing.List[GeneralAction]:
        return functools.reduce(list.__add__, [plugin.general_actions for plugin in self.plugins.values()], [])

    @property
    def all_region_computations(self) -> typing.List[RegionComputation]:
        return functools.reduce(list.__add__, [plugin.region_computations for plugin in self.plugins.values()], [])

    @property
    def all_property_computations(self) -> typing.List[PropertyComputation]:
        return functools.reduce(list.__add__, [plugin.property_computations for plugin in self.plugins.values()], [])

    @property
    def all_tools(self) -> typing.List[Tool]:
        return functools.reduce(list.__add__, [plugin.tools for plugin in self.plugins.values()], [])

    @property
    def get_actions_of_type(self, action_type: typing.Type[Action]) -> typing.List[Action]:
        if action_type == GeneralAction:
            return self.all_general_actions
        elif action_type == RegionComputation:
            return self.all_region_computations
        elif action_type == PropertyComputation:
            return self.all_property_computations
        else:
            return []
