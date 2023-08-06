from typing import Optional

from maphis.common.common import Info
from maphis.common.plugin import Plugin


class ReflectionsPlugin(Plugin):
    """
    NAME: Reflections Pekar
    DESCRIPTION: Generates reflections mask.
    """

    def __init__(self, info: Optional[Info] = None) -> None:
        super().__init__(info)
