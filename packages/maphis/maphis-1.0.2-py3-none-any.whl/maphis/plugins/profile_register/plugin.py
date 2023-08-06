from typing import Optional

from maphis.common.common import Info
from maphis.common.plugin import Plugin
from maphis.common.state import State


class ContourRegisterPlugin(Plugin):
    """
    NAME: Contour register
    DESCRIPTION: Contour register plugin
    """
    def __init__(self, state: State, info: Optional[Info] = None):
        super().__init__(state, info)
