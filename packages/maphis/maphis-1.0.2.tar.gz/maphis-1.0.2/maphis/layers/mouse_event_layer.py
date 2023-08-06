import typing
from typing import Optional

import PySide6
from PySide6.QtCore import Qt, QRectF

from maphis.common.photo import Photo
from maphis.common.state import State
from maphis.common.tool import EditContext, Tool
from maphis.layers.layer import Layer


class MouseEventLayer(Layer):
    def __init__(self, state: State, parent: Optional[PySide6.QtWidgets.QGraphicsItem] = None):
        super().__init__(state, parent)
        self.layers: typing.List[Layer] = []

    def initialize(self):
        self.setAcceptedMouseButtons(Qt.LeftButton | Qt.RightButton)
        self.setAcceptHoverEvents(True)

    def set_photo(self, photo: Photo, reset_tool: bool = True):
        self.prepareGeometryChange()

    def _create_context(self) -> Optional[EditContext]:
        return None

    def set_tool(self, tool: Tool, reset_current: bool = True):
        pass

    def boundingRect(self) -> PySide6.QtCore.QRectF:
        if len(self.layers) == 0:
            return QRectF()
        return self.layers[0].boundingRect()

    def hoverEnterEvent(self, event: PySide6.QtWidgets.QGraphicsSceneHoverEvent):
        for layer in self.layers:
            layer.hover_enter(event)

    def hoverLeaveEvent(self, event: PySide6.QtWidgets.QGraphicsSceneHoverEvent):
        for layer in self.layers:
            layer.hover_leave(event)

    def hoverMoveEvent(self, event: PySide6.QtWidgets.QGraphicsSceneHoverEvent):
        for layer in self.layers:
            layer.hover_move(event)

    def mouseMoveEvent(self, event: PySide6.QtWidgets.QGraphicsSceneMouseEvent):
        if event.buttons() & Qt.MiddleButton:
            event.ignore()
            return
        for layer in self.layers:
            layer.mouse_move(event)

    def mousePressEvent(self, event: PySide6.QtWidgets.QGraphicsSceneMouseEvent):
        if event.buttons() & Qt.MiddleButton:
            event.ignore()
            return
        for layer in self.layers:
            layer.mouse_press(event)

    def mouseReleaseEvent(self, event: PySide6.QtWidgets.QGraphicsSceneMouseEvent):
        if event.buttons() & Qt.MiddleButton:
            event.ignore()
            return
        for layer in self.layers:
            layer.mouse_release(event)

    def mouseDoubleClickEvent(self, event:PySide6.QtWidgets.QGraphicsSceneMouseEvent):
        if event.buttons() & Qt.MiddleButton:
            event.ignore()
            return
        for layer in self.layers:
            layer.mouse_double_click(event)

    def wheelEvent(self, event: PySide6.QtWidgets.QGraphicsSceneWheelEvent):
        for layer in self.layers:
            layer.mouse_wheel(event)
