import typing
import importlib.resources
import os
from pathlib import Path

from PySide6.QtGui import QIcon

from maphis import MAPHIS_PATH


class IconStorage:
    _instance: typing.Optional['IconStorage'] = None

    def __init__(self):
        self._icons: typing.Dict[str, QIcon] = {}

    def load_icons(self) -> bool:
        try:
            res_path = MAPHIS_PATH / 'resources'
            for dir_entry in os.scandir(res_path):
                if dir_entry.is_dir() or not dir_entry.name.endswith('png'):
                    continue
                icon_path = Path(dir_entry.path)
                icon_name = icon_path.stem   # without the extension
                icon = QIcon(str(icon_path))
                self._icons[icon_name] = icon
        except Exception:
            return False
        return True

    @classmethod
    def instance(cls) -> typing.Optional['IconStorage']:
        if cls._instance is None:
            cls._instance = IconStorage()
            if not cls._instance.load_icons():
                return None
        return cls._instance

    def __getitem__(self, icon_name: str) -> typing.Optional[QIcon]:
        return self._icons.get(icon_name, None)