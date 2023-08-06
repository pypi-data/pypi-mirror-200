import inspect
import logging
from enum import Enum
from importlib import resources, import_module
import os
import typing
from pathlib import Path

from maphis import MAPHIS_PATH
from maphis.common.action import RegionComputation, PropertyComputation, GeneralAction
from maphis.common.tool import Tool

logger = logging.getLogger('plugin_utils')


class ActionFolder(str, Enum):
    GeneralAction = 'general',
    RegionComputation = 'regions',
    PropertyComputation = 'properties',
    Tool = 'tools',


def get_plugin_folders() -> typing.List[Path]:
    plugins_path = MAPHIS_PATH / 'plugins'
    return [dir_entry.path for dir_entry in os.scandir(plugins_path) if dir_entry.is_dir()]


def load_tools(plugin_key: str) -> typing.List[Tool]:
    tools: typing.List[Tool] = []
    try:
        tools_folder = MAPHIS_PATH / 'tools'
        if not tools_folder.exists():
            return []
        for file in os.scandir(tools_folder):
            if file.is_dir() or file.name.startswith('_') or not file.name.endswith('.py'):
                continue
            module_name = file.name.split('.')[0]
            module = import_module(f'{plugin_key}.tools.{module_name}')
            tool_cls = inspect.getmembers(module, is_tool)
            tools.extend(tool_cls)
    except FileNotFoundError:
        return []
    return tools


def is_computation(obj) -> bool:
    return (inspect.isclass(obj) and obj != RegionComputation and obj != PropertyComputation and obj != GeneralAction and obj != Tool and
            (issubclass(obj, RegionComputation) or issubclass(obj, PropertyComputation) or issubclass(obj, GeneralAction) or issubclass(obj, Tool)))


def is_tool(obj) -> bool:
    return inspect.isclass(obj) and obj != Tool and issubclass(obj, Tool)


def get_plugin_folder(plugin_key: str) -> Path:
    with resources.path(plugin_key, 'plugin.py') as path:
        return path.parent