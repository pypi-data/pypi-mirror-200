import abc
import dataclasses
import importlib
import inspect
import logging
import os
import typing
from importlib import import_module
from pathlib import Path
from typing import Optional, Set, List, Union, Type
import sys

from PySide6.QtWidgets import QWidget

from maphis.common.action import RegionComputation, PropertyComputation, GeneralAction, Action
from maphis.common.common import Info
from maphis.common.label_image import RegionProperty, LabelImg
from maphis.common.photo import Photo
from maphis.common.plugin_utils import load_tools, is_computation, get_plugin_folder, ActionFolder
from maphis.common.regions_cache import RegionsCache
from maphis.common.state import State
from maphis.common.storage import Storage
from maphis.common.tool import Tool
from maphis.common.units import Unit, BaseUnit, SIPrefix, UnitStore
from maphis.common.user_params import UserParam
from maphis.common.utils import get_dict_from_doc_str

logging.basicConfig(filename='arthropod_logger.log', level=logging.INFO, format="%(asctime)s %(filename)-30s %(levelname)-8s %(message)s")
logger = logging.getLogger("plugin.py")


class Plugin:
    def __init__(self, state: State, info: Optional[Info] = None):
        self.state = state
        self._plugin_id = -1
        self.info = Info.load_from_doc_str(self.__doc__) if info is None else info
        self.info.key = '.'.join(self.__module__.split('.')[:-1])
        self._region_computations: List[RegionComputation] = []
        self._property_computations: List[PropertyComputation] = []
        self._general_actions: List[GeneralAction] = []
        self._tools: List[Tool] = []
        self._folder: Path = get_plugin_folder(self.info.key)

    @property
    def plugin_id(self) -> int:
        return self._plugin_id

    @property
    def region_computations(self) -> Optional[List[RegionComputation]]:
        return self._region_computations

    @property
    def property_computations(self) -> Optional[List[PropertyComputation]]:
        return self._property_computations

    @property
    def general_actions(self) -> Optional[List[GeneralAction]]:
        return self._general_actions

    @property
    def tools(self) -> Optional[List[Tool]]:
        return self._tools

    def _load_info_from_doc(self) -> Info:
        doc_str = self.__doc__
        lines = [line for line in doc_str.splitlines() if len(line) > 0]

        name = lines[0].split(':')[1].strip()
        desc = lines[1].split(':')[1].strip()

        return Info(name, desc)

    def register_computation(self, cls):
        try:
            obj: Union[RegionComputation, PropertyComputation, GeneralAction] = cls()
            obj.info.key = cls.__module__
            if issubclass(cls, RegionComputation):
                self._region_computations.append(obj)
            elif issubclass(cls, PropertyComputation):
                self._property_computations.append(obj)
            else:
                self._general_actions.append(obj)
        except AttributeError:
            logger.error(f'Could not register computation {cls}.')

    def register_tool(self, cls: Type[Tool]):
        try:
            obj: Tool = cls(self.state)
            obj.info.key = cls.__module__
            self._tools.append(obj)
        except AttributeError:
            logger.error(f'Could not register tool {cls}')

    def get_actions(self, cls: typing.Type[Action]) -> typing.List[Action]:
        if cls == GeneralAction:
            return self._general_actions
        elif cls == Tool:
            return self._tools
        elif cls == RegionComputation:
            return self._region_computations
        elif cls == PropertyComputation:
            return self._property_computations
        else:
            return []

    def reload(self):
        for action_cls in [GeneralAction, RegionComputation, PropertyComputation, Tool]:
            comps: typing.List[Type[Action]] = load_computations(self._folder / action_cls.FOLDER)
            if len(comps) == 0:
                continue
            actions: typing.List[action_cls] = self.get_actions(action_cls)
            actions.clear()
            for comp_name, comp_cls in comps:
                if issubclass(comp_cls, Tool):
                    obj = comp_cls(self.state)
                else:
                    obj = comp_cls()
                obj.info.key = comp_cls.__module__
                actions.append(obj)


def global_computation_key(global_property_key: str) -> str:
    return '.'.join(global_property_key.split('.')[:-1])


def local_property_key(global_property_key: str) -> str:
    return global_property_key.split('.')[-1]


@dataclasses.dataclass
class ActionContext:
    tools: typing.List[Tool]
    plugins: typing.List[Plugin]
    general_actions: typing.Dict[str, GeneralAction]
    region_computations: typing.Dict[str, RegionComputation]
    property_computations: typing.Dict[str, PropertyComputation]
    storage: typing.Optional[Storage] = None
    current_label_name: str = ''
    units: typing.Optional[UnitStore] = None


def load_plugin(plugin_folder: Path) -> typing.Optional[Plugin]:
    try:
        plugin_key = f'maphis.plugins.{plugin_folder.name}'
        module_key = plugin_key + '.plugin'
        if module_key in sys.modules:
            module = importlib.reload(sys.modules[module_key])
        else:
            module = import_module(module_key)
    except ModuleNotFoundError:
        logger.error(f'Cannot load {plugin_folder} plugin.')
        return None
    plug_cls = [member for member in inspect.getmembers(module, lambda o: inspect.isclass(o) and issubclass(o, Plugin))
                if member[1] != Plugin]
    if len(plug_cls) == 0:
        return
    name, cls = plug_cls[0]

    plug_inst: Plugin = cls(None)
    plug_inst.reload()

    return plug_inst

    if (regions_path := plugin_folder / 'regions').exists():
        reg_comps = load_computations(regions_path)
        for comp_name, comp_cls in reg_comps:
            plug_inst.register_computation(comp_cls)
    if (props_path := plugin_folder / 'properties').exists():
        prop_comps = load_computations(props_path)
        for comp_name, comp_cls in prop_comps:
            plug_inst.register_computation(comp_cls)
    if (actions_path := plugin_folder / 'general').exists():
        general_actions = load_computations(actions_path)
        for action_name, action_cls in general_actions:
            plug_inst.register_computation(action_cls)
    if (tools_path := plugin_folder / 'tools').exists():
        tools = load_tools(plug_inst.info.key)
        for tool_name, tool_cls in tools:
            plug_inst.register_tool(tool_cls)

    return plug_inst


def load_computations(comp_folder: Path) -> typing.Union[typing.List[RegionComputation], typing.List[PropertyComputation], typing.List[GeneralAction]]:
    comp_type = comp_folder.name
    computations: typing.Union[typing.List[RegionComputation], typing.List[PropertyComputation], typing.List[GeneralAction], typing.List[Tool]] = []
    if not comp_folder.exists():
        return []
    for file in os.scandir(comp_folder):
        if file.is_dir() or file.name.startswith('_') or not file.name.endswith('.py'):
            continue
        module_name = file.name.split('.')[0]
        comp_key = f'maphis.plugins.{comp_folder.parent.name}.{comp_type}.{module_name}'
        if comp_key not in sys.modules:
            module = import_module(comp_key)
        else:
            module = importlib.reload(sys.modules[comp_key])
        comp_cls = inspect.getmembers(module, is_computation)
        computations.extend(comp_cls)
    return computations
