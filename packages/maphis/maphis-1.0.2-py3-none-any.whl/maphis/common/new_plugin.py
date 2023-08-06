import shutil
from enum import Enum
from importlib import resources
from pathlib import Path
from typing import Type

from maphis import MAPHIS_PATH
from maphis.common.action import Action
from maphis.common.plugin_utils import get_plugin_folder


class ActionType(str, Enum):
    GeneralAction = 'general',
    RegionTemplate = 'regions',
    PropertyComputation = 'properties',
    Tool = 'tools',


def new_module(path: Path) -> bool:
    path.mkdir(exist_ok=True)
    f = open(path / '__init__.py', 'w')
    f.close()
    return True


def create_new_plugin(plugin_name: str, description: str) -> Path:
    path = MAPHIS_PATH / 'plugins'
    plugin_folder_name = plugin_name.strip().lower().replace(' ', '_')
    new_module(path / plugin_folder_name)
    with resources.path('maphis.templates', 'plugin_template.py') as template_path:
        shutil.copy2(template_path, path / plugin_folder_name / 'plugin.py')
    class_name = ''.join([word.capitalize() for word in plugin_name.lower().split(' ')])
    key = plugin_name.strip().lower().replace(' ', '_')
    interpolate_class_doc(path / plugin_folder_name / 'plugin.py', class_name, description, key)
    return path / plugin_folder_name


def make_snake_case(name: str) -> str:
    return name.strip().lower().replace(' ', '_')


def make_camel_case(name: str) -> str:
    return ''.join([word.capitalize() for word in name.lower().split(' ')])


def new_computation(plugin_key: str, action_cls: Type[Action], comp_name: str, desc: str, key: str) -> Path:
    plugin_folder = get_plugin_folder(plugin_key)
    if not (plugin_folder / action_cls.FOLDER).exists():
        new_module(plugin_folder / action_cls.FOLDER)
    # if action_type == ActionType.GeneralAction:
    #     template = 'general_action_template.py'
    # elif action_type == ActionType.RegionTemplate:
    #     template = 'region_computation_template.py'
    # elif action_type == ActionType.PropertyComputation:
    #     template = 'property_computation_template.py'
    # else:
    #     template = 'tool_template.py'
    comp_path = plugin_folder / action_cls.FOLDER / f'{make_snake_case(comp_name)}.py'
    with resources.path('maphis.templates', action_cls.TEMPLATE) as template_path:
        shutil.copy2(template_path, comp_path)
    class_name = make_camel_case(comp_name)
    interpolate_class_doc(comp_path, class_name, desc, key)

    return comp_path


def interpolate_class_doc(path: Path, class_name: str, description: str, key: str):
    py_f = open(path, 'r')
    py_class = py_f.read()
    py_f.close()
    py_class = py_class.replace('CLASS_NAME', class_name)
    py_class = py_class.replace('<NAME>', class_name)
    py_class = py_class.replace('<DESCRIPTION>', description)
    py_class = py_class.replace('<KEY>', key)

    with open(path, 'w') as py_f:
        py_f.write(py_class)
