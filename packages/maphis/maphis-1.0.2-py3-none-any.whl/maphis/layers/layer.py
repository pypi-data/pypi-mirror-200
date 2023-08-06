import abc
import typing
from typing import Optional

import PySide6
from PySide6.QtCore import QRectF
from PySide6.QtWidgets import QGraphicsObject, QGraphicsSceneMouseEvent, QGraphicsSceneHoverEvent, \
    QGraphicsSceneWheelEvent

from maphis.common.photo import Photo
from maphis.common.state import State
from maphis.common.tool import Tool, EditContext


class Layer(QGraphicsObject):
    def __init__(self, state: State, parent: Optional[PySide6.QtWidgets.QGraphicsItem] = None):
        super().__init__(parent)

    @abc.abstractmethod
    def set_tool(self, tool: Optional[Tool], reset_current: bool = True):
        pass

    @abc.abstractmethod
    def _create_context(self) -> Optional[EditContext]:
        pass

    @abc.abstractmethod
    def set_photo(self, photo: typing.Optional[Photo], reset_tool: bool = True):
        pass

    def initialize(self):
        pass

    def boundingRect(self) -> PySide6.QtCore.QRectF:
        return QRectF()

    def paint(self, painter: PySide6.QtGui.QPainter, option: PySide6.QtWidgets.QStyleOptionGraphicsItem,
              widget: typing.Optional[PySide6.QtWidgets.QWidget] = ...):
        pass

    def mouse_press(self, event: QGraphicsSceneMouseEvent):
        pass

    def mouse_release(self, event: QGraphicsSceneMouseEvent):
        pass

    def mouse_move(self, event: QGraphicsSceneMouseEvent):
        pass

    def mouse_double_click(self, event: QGraphicsSceneMouseEvent):
        pass

    def mouse_wheel(self, event: QGraphicsSceneWheelEvent):
        pass

    def hover_enter(self, event: QGraphicsSceneHoverEvent):
        pass

    def hover_move(self, event: QGraphicsSceneHoverEvent):
        pass

    def hover_leave(self, event: QGraphicsSceneHoverEvent):
        pass

    def reset(self):
        pass


