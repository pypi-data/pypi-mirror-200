from typing import Optional, List

from maphis.common.plugin import Plugin
from maphis.common.common import Info
from maphis.common.state import State
from maphis.common.tool import Tool


class MAPHIS(Plugin):
    """
    NAME: MAPHIS
    DESCRIPTION: Default plugin.
    """
    def __init__(self, state: State, info: Optional[Info] = None):
        super().__init__(state, info)
