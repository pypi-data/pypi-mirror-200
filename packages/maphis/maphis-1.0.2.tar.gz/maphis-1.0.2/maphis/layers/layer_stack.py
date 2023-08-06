import typing
from typing import Optional

import PySide6
from PySide6.QtWidgets import QGraphicsSceneHoverEvent, QGraphicsSceneWheelEvent, QGraphicsSceneMouseEvent

from maphis.common.photo import Photo
from maphis.common.state import State
from maphis.common.tool import EditContext, Tool
from maphis.layers.layer import Layer


class LayerStack(Layer):
    def __init__(self, state: State, parent: Optional[PySide6.QtWidgets.QGraphicsItem] = None):
        super().__init__(state, parent)

    def set_tool(self, tool: Optional[Tool], reset_current: bool = True):
        pass

    def _create_context(self) -> Optional[EditContext]:
        pass

    def set_photo(self, photo: typing.Optional[Photo], reset_tool: bool = True):
        pass

    def initialize(self):
        super().initialize()

    def boundingRect(self) -> PySide6.QtCore.QRectF:
        return super().boundingRect()

    def paint(self, painter: PySide6.QtGui.QPainter, option: PySide6.QtWidgets.QStyleOptionGraphicsItem,
              widget: typing.Optional[PySide6.QtWidgets.QWidget] = ...):
        super().paint(painter, option, widget)

    def mouse_press(self, event: QGraphicsSceneMouseEvent):
        super().mouse_press(event)

    def mouse_release(self, event: QGraphicsSceneMouseEvent):
        super().mouse_release(event)

    def mouse_move(self, event: QGraphicsSceneMouseEvent):
        super().mouse_move(event)

    def mouse_double_click(self, event: QGraphicsSceneMouseEvent):
        super().mouse_double_click(event)

    def mouse_wheel(self, event: QGraphicsSceneWheelEvent):
        super().mouse_wheel(event)

    def hover_enter(self, event: QGraphicsSceneHoverEvent):
        super().hover_enter(event)

    def hover_move(self, event: QGraphicsSceneHoverEvent):
        super().hover_move(event)

    def hover_leave(self, event: QGraphicsSceneHoverEvent):
        super().hover_leave(event)

    def reset(self):
        super().reset()