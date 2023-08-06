import typing

from PySide6.QtWidgets import QWidget

from maphis.common.action import GeneralAction
from maphis.common.common import Info
from maphis.common.plugin import ActionContext
from maphis.common.state import State
from maphis.common.user_params import UserParam


class CLASS_NAME(GeneralAction):
    """
    NAME: <NAME>
    DESCRIPTION: <DESCRIPTION>
    KEY: <KEY>
    """
    def __init__(self, info: typing.Optional[Info] = None):
        super(CLASS_NAME, self).__init__(info)

    def __call__(self, state: State, context: ActionContext) -> None:
        super(CLASS_NAME, self).__call__(state, context)

    @property
    def user_params(self) -> typing.List[UserParam]:
        return super().user_params

    @property
    def can_be_executed(self) -> typing.Tuple[bool, str]:
        return super().can_be_executed

    @property
    def group(self) -> str:
        return super().group

    def setting_widget(self) -> typing.Optional[QWidget]:
        return super().setting_widget()

