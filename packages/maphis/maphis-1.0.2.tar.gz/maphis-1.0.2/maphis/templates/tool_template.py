import typing
from typing import List, Tuple, Optional, Any

from PySide6.QtCore import QObject, QPoint, QRect
from PySide6.QtGui import QImage, QIcon, Qt, QPainter
from PySide6.QtWidgets import QWidget

from maphis.common.label_change import CommandEntry
from maphis.common.state import State
from maphis.common.tool import EditContext, PaintCommand, Tool
from maphis.common.user_params import UserParam


class CLASS_NAME(Tool):
    """
    NAME: <NAME>
    DESCRIPTION: <DESCRIPTION>
    KEY: <KEY>
    """
    def __init__(self, state: State, parent: QObject = None):
        super().__init__(state, parent)

    def set_tool_id(self, tool_id: int):
        super().set_tool_id(tool_id)

    @property
    def tool_icon(self) -> Optional[QIcon]:
        return super().tool_icon

    @property
    def tool_name(self) -> str:
        return super().tool_name

    @property
    def cursor_image(self) -> Optional[typing.Union[QImage, Qt.CursorShape]]:
        return super().cursor_image

    @property
    def user_params(self) -> typing.Dict[str, UserParam]:
        return super().user_params

    def set_user_param(self, param_name: str, value: typing.Any):
        super().set_user_param(param_name, value)

    @property
    def active(self) -> bool:
        return super().active

    @property
    def viz_active(self) -> bool:
        return super().viz_active

    @property
    def value_storage(self) -> Optional[Any]:
        return super().value_storage()

    def left_press(self, painter: QPainter, pos: QPoint, context: EditContext) -> Tuple[Optional[CommandEntry], QRect]:
        return super().left_press(painter, pos, context)

    def left_release(self, painter: QPainter, pos: QPoint, context: EditContext) -> Tuple[
        Optional[CommandEntry], QRect]:
        return super().left_release(painter, pos, context)

    def right_press(self, painter: QPainter, pos: QPoint, context: EditContext) -> Tuple[Optional[CommandEntry], QRect]:
        return super().right_press(painter, pos, context)

    def right_release(self, painter: QPainter, pos: QPoint, context: EditContext) -> Tuple[
        Optional[CommandEntry], QRect]:
        return super().right_release(painter, pos, context)

    def middle_click(self, painter: QPainter, pos: QPoint, context: EditContext) -> Tuple[
        Optional[CommandEntry], QRect]:
        return super().middle_click(painter, pos, context)

    def mouse_move(self, painter: QPainter, new_pos: QPoint, old_pos: QPoint, context: EditContext) -> Tuple[
        Optional[CommandEntry], QRect]:
        return super().mouse_move(painter, new_pos, old_pos, context)

    def mouse_double_click(self, painter: QPainter, pos: QPoint, context: EditContext) -> Tuple[
        Optional[CommandEntry], QRect]:
        return super().mouse_double_click(painter, pos, context)

    def mouse_wheel(self, delta: int, painter: QPainter, pos: QPoint, context: EditContext) -> Tuple[
        Optional[CommandEntry], QRect]:
        return super().mouse_wheel(delta, painter, pos, context)

    def get_auto_scroll_distance(self):
        return super().get_auto_scroll_distance()

    def should_auto_scroll_with_left_button_released(self):
        return super().should_auto_scroll_with_left_button_released()

    def viz_left_press(self, pos: QPoint, canvas: QImage) -> List[PaintCommand]:
        return super().viz_left_press(pos, canvas)

    def viz_left_release(self, pos: QPoint, canvas: QImage) -> List[PaintCommand]:
        return super().viz_left_release(pos, canvas)

    def viz_right_press(self, pos: QPoint, canvas: QImage) -> List[PaintCommand]:
        return super().viz_right_press(pos, canvas)

    def viz_right_release(self, pos: QPoint, canvas: QImage) -> List[PaintCommand]:
        return super().viz_right_release(pos, canvas)

    def viz_mouse_move(self, new_pos: QPoint, old_pos: QPoint, canvas: QImage) -> List[PaintCommand]:
        return super().viz_mouse_move(new_pos, old_pos, canvas)

    def viz_mouse_double_click(self, pos: QPoint, canvas: QImage) -> List[PaintCommand]:
        return super().viz_mouse_double_click(pos, canvas)

    def viz_mouse_wheel(self, delta: int, pos: QPoint, canvas: QImage) -> List[PaintCommand]:
        return super().viz_mouse_wheel(delta, pos, canvas)

    def viz_hover_enter(self, pos: QPoint, canvas: QImage) -> List[PaintCommand]:
        return super().viz_hover_enter(pos, canvas)

    def viz_hover_leave(self, pos: QPoint, canvas: QImage) -> List[PaintCommand]:
        return super().viz_hover_leave(pos, canvas)

    def viz_hover_move(self, new_pos: QPoint, old_pos: QPoint, canvas: QImage) -> List[PaintCommand]:
        return super().viz_hover_move(new_pos, old_pos, canvas)

    def update_primary_label(self, label: int):
        return super().update_primary_label(label)

    def update_secondary_label(self, label: int):
        return super().update_secondary_label(label)

    def color_map_changed(self, cmap: typing.Dict[int, typing.Tuple[int, int, int]]):
        return super().color_map_changed(cmap)

    def reset_tool(self):
        super().reset_tool()

    @property
    def viz_commands(self) -> List[PaintCommand]:
        return super().viz_commands

    def set_out_widget(self, widg: typing.Optional[QWidget]) -> bool:
        return super().set_out_widget(widg)

