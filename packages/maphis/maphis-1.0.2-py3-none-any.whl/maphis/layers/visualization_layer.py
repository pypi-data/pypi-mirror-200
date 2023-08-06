from typing import List, Callable, Optional

import PySide6
from PySide6.QtCore import QRectF, Qt, QPoint
from PySide6.QtGui import QPainter, QPen, QFont, QCursor, QImage, QColor
from PySide6.QtWidgets import QGraphicsObject, QGraphicsSceneMouseEvent, QGraphicsSceneHoverEvent, \
    QGraphicsSceneWheelEvent

from maphis.layers.layer import Layer
from maphis.common.photo import Photo
from maphis.common.tool import Tool, EditContext, ToolCursor


class VisualizationLayer(Layer):
    def __init__(self, parent: Optional[PySide6.QtWidgets.QGraphicsItem] = None):
        super().__init__(parent)
        self.cursor_shape: Optional[Qt.CursorShape] = None
        self._layer_rect: QRectF = QRectF()
        self.paint_commands: List[Callable[[QPainter], None]] = []
        self.font = QFont('monospace')
        self.font.setPointSize(24)
        self.current_tool: Optional[Tool] = None
        self.tool_cursor: ToolCursor = ToolCursor(parent=self)
        self.canvas: Optional[QImage] = None

    def _create_context(self) -> Optional[EditContext]:
        return None

    def initialize(self):
        pass

    def boundingRect(self) -> PySide6.QtCore.QRectF:
        return self._layer_rect

    def set_photo(self, photo: Optional[Photo], reset_tool: bool = True):
        if self.current_tool is not None and reset_tool:
            self.current_tool.reset_tool()
        if photo is None:
            self.setVisible(False)
            return
        else:
            self.setVisible(True)
        self.prepareGeometryChange()
        self._layer_rect = QRectF(0, 0, photo.image.shape[1],
                                  photo.image.shape[0])
        self.canvas = QImage(photo.image.shape[1], photo.image.shape[0], QImage.Format_ARGB32)
        self.canvas.fill(QColor.fromRgb(0, 0, 0, 0))
        if self.current_tool is not None and self.current_tool.viz_active:
            self.paint_commands = self.current_tool.viz_commands
        else:
            self.paint_commands = []
        self.update()

    def set_tool(self, tool: Optional[Tool], reset_current: bool = True):
        if self.current_tool is not None:
            if reset_current:
                self.current_tool.reset_tool()
            self.current_tool.update_viz.disconnect(self._handle_update_tool_viz)
        self.current_tool = tool
        if self.current_tool is not None:
            self.current_tool.update_viz.connect(self._handle_update_tool_viz)
            if isinstance((cursor := self.current_tool.cursor_image), QImage):
                self.tool_cursor.set_cursor(self.current_tool.cursor_image)
                self.cursor_shape = None
            else:
                self.tool_cursor.set_cursor(None)
                self.cursor_shape = cursor
        self.paint_commands = []
        self.update()

    def paint(self, painter:PySide6.QtGui.QPainter, option:PySide6.QtWidgets.QStyleOptionGraphicsItem, widget:Optional[PySide6.QtWidgets.QWidget]=None):
        painter.save()
        if self.canvas is not None:
            painter.drawImage(0, 0, self.canvas)
        painter.setFont(self.font)
        for cmd in self.paint_commands:
            cmd(painter)
        painter.restore()

    def mouse_press(self, event:PySide6.QtWidgets.QGraphicsSceneMouseEvent):
        if self.current_tool is not None:
            if event.button() == Qt.LeftButton:
                self.paint_commands = self.current_tool.viz_left_press(event.pos().toPoint(), self.canvas)
            elif event.button() == Qt.RightButton:
                self.paint_commands = self.current_tool.viz_right_press(event.pos().toPoint(), self.canvas)
            self.update()

    def mouse_move(self, event:PySide6.QtWidgets.QGraphicsSceneMouseEvent):
        if self.current_tool is not None and self.current_tool.viz_active:
            self.tool_cursor.setPos(event.pos())
            self.paint_commands = self.current_tool.viz_mouse_move(event.pos().toPoint(),
                                                                   event.lastPos().toPoint(),
                                                                   self.canvas)
            self.update()

    def mouse_release(self, event:PySide6.QtWidgets.QGraphicsSceneMouseEvent):
        if self.current_tool is not None and self.current_tool.viz_active:
            if event.button() == Qt.LeftButton:
                self.paint_commands = self.current_tool.viz_left_release(event.pos().toPoint(), self.canvas)
            elif event.button() == Qt.RightButton:
                self.paint_commands = self.current_tool.viz_right_release(event.pos().toPoint(), self.canvas)
        else:
            self.paint_commands = []
        self.update()

    def mouse_double_click(self, event: QGraphicsSceneMouseEvent):
        if self.current_tool is not None:
            self.paint_commands = self.current_tool.viz_mouse_double_click(event.pos().toPoint(), self.canvas)
        self.update()

    def mouse_wheel(self, event: QGraphicsSceneWheelEvent):
        if self.current_tool is not None and self.current_tool.viz_active:
            self.paint_commands = self.current_tool.viz_mouse_wheel(event.delta(), event.pos().toPoint(), self.canvas)
        else:
            self.paint_commands = []
        self.update()

    def hover_move(self, event: QGraphicsSceneHoverEvent):
        if self.current_tool is not None:
            last_pos = self.tool_cursor.pos()
            rect = self.tool_cursor.boundingRect()
            rect.setX(last_pos.x())
            rect.setY(last_pos.y())
            self.tool_cursor.setPos(event.pos())
            if self.current_tool.viz_active:
                self.paint_commands = self.current_tool.viz_hover_move(event.pos().toPoint(),
                                                                       event.lastPos().toPoint(),
                                                                       self.canvas)
            self.update()

    def hover_enter(self, event: QGraphicsSceneHoverEvent):
        if self.current_tool is not None:
            if self.cursor_shape is not None:
                self.setCursor(self.cursor_shape)
            else:
                self.setCursor(QCursor(Qt.BlankCursor))
            self.tool_cursor.set_shown(True)
            self.update()

    def hover_leave(self, event: QGraphicsSceneHoverEvent):
        if self.current_tool is not None:
            self.setCursor(QCursor(Qt.ArrowCursor))
            self.tool_cursor.set_shown(False)
            self.update()

    def reset(self):
        if self.current_tool is not None:
            self.current_tool.reset_tool()
        self.paint_commands = []
        self.update()

    def put_qt_painter_command(self, cmd: Callable[[QPainter], None]):
        self.paint_commands.append(cmd)

    def put_line_segment(self, p1: QPoint, p2: QPoint, pen: QPen):
        def paint(painter: QPainter):
            painter.save()
            painter.setPen(pen)
            painter.drawLine(p1, p2)
            painter.restore()
        self.paint_commands.append(paint)
        self.update()

    def put_text(self, p: QPoint, text: str, pen: QPen):
        def paint(painter: QPainter):
            painter.save()
            painter.setPen(pen)
            painter.drawText(p, text)
            painter.restore()
        self.paint_commands.append(paint)
        self.update()

    def _handle_update_tool_viz(self):
        if self.current_tool is None:
            return
        self.paint_commands = self.current_tool.viz_commands
        self.update()
