from enum import IntEnum
from typing import Optional

import PySide6.QtCore
import PySide6.QtWidgets
from PySide6 import QtCore
from PySide6.QtWidgets import QWidget


class PopupLocation(IntEnum):
    TopLeft = 0,
    TopRight = 1,
    BottomLeft = 2,
    BottomRight = 3


class PopupWidget(QWidget):
    def __init__(self, popup_timeout_millis: int = 200, parent: Optional[PySide6.QtWidgets.QWidget] = ...,
                 f: PySide6.QtCore.Qt.WindowType = ...) -> None:
        super().__init__(parent, f)
        self.popup_timeout: int = popup_timeout_millis
        self.timer_id: int = -1
        self.popup_location: PopupLocation = PopupLocation.TopLeft
        self.in_popup_mode: bool = True

    def leaveEvent(self, event:PySide6.QtCore.QEvent):
        if not self.in_popup_mode:
            return
        self.timer_id = self.startTimer(self.popup_timeout, PySide6.QtCore.Qt.TimerType.CoarseTimer)

    def timerEvent(self, event: PySide6.QtCore.QTimerEvent) -> None:
        self.hide()
        self.killTimer(self.timer_id)
        self.timer_id = -1

    def enterEvent(self, event:PySide6.QtCore.QEvent):
        if self.timer_id >= 0:
            self.killTimer(self.timer_id)
            self.timer_id = -1

    def show(self):
        if self.timer_id >= 0:
            self.killTimer(self.timer_id)
            self.timer_id = -1
        QWidget.show(self)
        self.adjustSize()

    def makePopup(self, callWidget: QWidget, spawn_point: QtCore.QPointF=QtCore.QPointF()):
        """
        Turns the dialog into a popup dialog.
        callWidget is the widget responsible for calling the dialog (e.g. a toolbar button)
        """
        if not self.in_popup_mode:
            return
        self.setContentsMargins(0,0,0,0)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Popup)
        self.setObjectName('ImportDialog')

        # Move the dialog to the widget that called it
        if spawn_point.isNull():
            point = callWidget.rect().topLeft()
            if self.popup_location == PopupLocation.TopLeft:
                offset = QtCore.QPoint(0, 0)
            elif self.popup_location == PopupLocation.TopRight:
                offset = QtCore.QPoint(callWidget.rect().width(), 0)
            elif self.popup_location == PopupLocation.BottomLeft:
                offset = QtCore.QPoint(0, callWidget.rect().height())
            else:
                offset = QtCore.QPoint(callWidget.rect().width(), callWidget.rect().height())
            global_point = callWidget.mapToGlobal(point)
            target_point = global_point + offset
        else:
            target_point = callWidget.mapToGlobal(spawn_point)
        self.move(target_point)

    def set_popup_location(self, popup_location: PopupLocation):
        self.popup_location = popup_location

    def set_popup_mode(self, is_popup_mode: bool):
        self.in_popup_mode = is_popup_mode
