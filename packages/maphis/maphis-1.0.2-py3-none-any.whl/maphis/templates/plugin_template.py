import typing
from typing import Type, Optional, List

from maphis.common.action import Action, GeneralAction, PropertyComputation, RegionComputation
from maphis.common.common import Info
from maphis.common.plugin import Plugin
from maphis.common.state import State
from maphis.common.tool import Tool


class CLASS_NAME(Plugin):
    """
    NAME: <NAME>
    DESCRIPTION: <DESCRIPTION>
    KEY: <KEY>
    """

    def __init__(self, state: State, info: Optional[Info] = None):
        super().__init__(state, info)

    @property
    def plugin_id(self) -> int:
        return super().plugin_id

    @property
    def region_computations(self) -> Optional[List[RegionComputation]]:
        return super().region_computations

    @property
    def property_computations(self) -> Optional[List[PropertyComputation]]:
        return super().property_computations

    @property
    def general_actions(self) -> Optional[List[GeneralAction]]:
        return super().general_actions

    @property
    def tools(self) -> Optional[List[Tool]]:
        return super().tools

    def _load_info_from_doc(self) -> Info:
        return super()._load_info_from_doc()

    def register_computation(self, cls):
        super().register_computation(cls)

    def register_tool(self, cls: Type[Tool]):
        super().register_tool(cls)

    def get_actions(self, cls: typing.Type[Action]) -> typing.List[Action]:
        return super().get_actions(cls)
