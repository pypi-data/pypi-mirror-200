import importlib.resources
import typing
from typing import List, Tuple, Dict

import numpy as np
import skimage.draw
import skimage.measure
from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QPainter, QColor, QPen, QIcon, QImage
from PySide6.QtWidgets import QWidget
from skimage.morphology import binary_dilation, disk

from maphis.common.param_widget import ParamWidget
from maphis.common.label_change import LabelChange, CommandEntry
from maphis.common.state import State
from maphis.common.tool import Tool, EditContext, PaintCommand, line_command
from maphis.common.user_param import IntParam, ParamBuilder, Param


class Tool_Knife(Tool):
    def __init__(self, state: State):
        Tool.__init__(self, state)
        self._tool_name = "Knife"
        self._active = False
        self._first_endpoint: Tuple[int, int] = (-1, -1)
        # self._user_params = {'Cut width': UserParam('Cut width', ParamType.INT, 3, min_val=1, max_val=9, step=2)}
        self._width_param: IntParam = ParamBuilder().int_param().name('Cut width').key('cut_width').\
            description('Width of cut').min_value(1).max_value(9).default_value(3).build()
        # self._width_param_widget = self._width_param.get_default_ui_control()
        self._width_param_widget = ParamWidget([self._width_param])
        with importlib.resources.path("maphis.tools.icons", "cutter.png") as path:
            self._tool_icon = QIcon(str(path))
        self.pen = QPen()
        self.state = state
        self._current_cut_line_points: typing.Tuple[QPoint, QPoint] = (QPoint(), QPoint())

    @property
    def tool_name(self) -> str:
        return self._tool_name

    @property
    def active(self) -> bool:
        return self._active

    @property
    def viz_active(self) -> bool:
        return self._active

    @property
    def user_params(self) -> typing.Dict[str, Param]:
        return {'cut_width': self._width_param}

    def left_press(self, painter: QPainter, pos: QPoint, context: EditContext) -> Tuple[
        typing.Optional[CommandEntry], QRect]:
        return None, QRect()

    def left_release(self, painter: QPainter, pos: QPoint, ctx: EditContext) -> Tuple[
        typing.Optional[CommandEntry], QRect]:
        ctx.tool_viz_commands = []
        line_coords = skimage.draw.line(*self._first_endpoint, *(pos.toTuple()[::-1]))

        line_width = self._width_param.value
        if line_width > 1:

            top, left = np.min(line_coords[0]) - line_width // 2, np.min(line_coords[1]) - line_width // 2
            bottom, right = np.max(line_coords[0]) + line_width // 2, np.max(line_coords[1]) + line_width // 2

            line_box = np.zeros((bottom - top + 1, right - left + 1), np.bool)

            local_coords = (line_coords[0] - top, line_coords[1] - left)
            line_box[local_coords[0], local_coords[1]] = 1
            dil = binary_dilation(line_box, disk(line_width // 2))
            line_coords = np.nonzero(dil)
            line_coords = line_coords[0] + top, line_coords[1] + left

        rr_cc = [(r, c) for r, c in zip(line_coords[0], line_coords[1]) if 0 <= r < ctx.label_img.label_image.shape[0] and 0 <= c < ctx.label_img.label_image.shape[1]]
        line_coords = [r for r, c in rr_cc], [c for r, c in rr_cc]

        label_profile = np.where(~ctx.clip_mask > 0, ctx.label_img.label_image, 0)[line_coords]
        labels = np.unique(label_profile)

        if len(labels) < 2:
            return None, QRect()
        #labels = set()

        lab_coords: Dict[int, Tuple[List[int], List[int]]] = {label: ([], []) for label in labels}
        painter = QPainter(ctx.label_viz)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        for i, y, x in zip(range(len(label_profile)), *line_coords):
            label = label_profile[i]
            if label == 0:
                continue
            lab_coords[label][0].append(y)
            lab_coords[label][1].append(x)

            color = QColor.fromRgb(*ctx.colormap[ctx.label])
            if ctx.label == 0:
                color.setAlpha(0)
            painter.setPen(color)
            painter.drawPoint(x, y)
        painter.end()
        if 0 in lab_coords:
            del lab_coords[0]
        cmd = CommandEntry([LabelChange(coords, ctx.label, label, ctx.label_img.label_semantic) for label, coords in lab_coords.items()])
        cmd.source = self.tool_name
        return cmd, cmd.bbox

    def mouse_move(self, painter: QPainter, new_pos: QPoint, old_pos: QPoint, ctx: EditContext) -> List[LabelChange]:
        #ctx.tool_viz_commands = [draw_line(QPoint(*self._first_endpoint[::-1]), new_pos, ctx)]
        return super().mouse_move(painter, new_pos, old_pos, ctx)

    def viz_left_press(self, pos: QPoint, canvas: QImage) -> List[PaintCommand]:
        self._first_endpoint = pos.toTuple()[::-1]
        color = self.state.label_hierarchy.nodes[self.state.primary_label].color
        self.pen.setColor(QColor(*color, 255))
        self.pen.setWidth(self._width_param.value)
        self._active = True
        return self.viz_mouse_move(pos, pos, canvas)

    def viz_mouse_move(self, new_pos: QPoint, old_pos: QPoint, canvas: QImage) -> List[PaintCommand]:
        self._current_cut_line_points = (QPoint(*self._first_endpoint[::-1]), new_pos)
        return [line_command(self._current_cut_line_points[0], self._current_cut_line_points[1], self.pen)]

    def viz_mouse_wheel(self, delta: int, pos: QPoint, canvas: QImage) -> List[PaintCommand]:
        return self.viz_mouse_move(self._current_cut_line_points[1], QPoint(), canvas)

    def viz_left_release(self, pos: QPoint, canvas: QImage) -> List[PaintCommand]:
        self._active = False
        return []

    def mouse_wheel(self, delta: int, painter: QPainter, pos: QPoint, context: EditContext) -> Tuple[
        typing.Optional[CommandEntry], QRect]:
        my_delta = 2 if delta > 0 else -2
        curr_width = self._width_param.value
        new_width = max(1, curr_width + my_delta)
        self._width_param.set_value(new_width)
        self.pen.setWidth(self._width_param.value)
        # self.cursor_changed.emit(self.tool_id, self.cursor_image)
        return None, QRect()



    @property
    def setting_widget(self) -> typing.Optional[QWidget]:
        return self._width_param_widget.widget


def draw_line(pos1: QPoint, pos2: QPoint, ctx: EditContext):
    def draw(painter: QPainter):
        painter.save()
        pen = QPen(QColor.fromRgb(*ctx.colormap[ctx.label]))
        pen.setWidth(4)
        painter.setPen(pen)
        painter.drawLine(pos1, pos2)
        painter.restore()

    return draw
