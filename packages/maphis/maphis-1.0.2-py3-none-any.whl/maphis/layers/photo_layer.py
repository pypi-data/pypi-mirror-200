from typing import Optional

import PySide6
from PySide6.QtCore import QRectF, QRect, QPointF
from PySide6.QtGui import QPixmap, QImage, Qt
from PySide6.QtWidgets import QGraphicsPixmapItem

from maphis import qimage2ndarray
from maphis.layers.layer import Layer
from maphis.common.photo import Photo
from maphis.common.state import State
from maphis.common.tool import Tool, EditContext


class PhotoLayer(Layer):
    def __init__(self, state: State, parent: Optional[PySide6.QtWidgets.QGraphicsItem] = None):
        super().__init__(state, parent)
        self.state = state

        self._image_pixmap: Optional[QPixmap] = None
        self.image_gpixmap: Optional[QGraphicsPixmapItem] = None

        self.photo_rect = QRect()
        self.setAcceptedMouseButtons(Qt.NoButton)

    def initialize(self):
        self._image_pixmap = QPixmap()
        self.image_gpixmap = self.scene().addPixmap(self._image_pixmap)
        self.image_gpixmap.setZValue(0)

    def set_tool(self, tool: Optional[Tool], reset_current: bool = True):
        pass

    def _create_context(self) -> Optional[EditContext]:
        return None

    def _set_pixmaps(self, image: QImage, pixmap: QPixmap, gpixmap: QGraphicsPixmapItem):
        pixmap.convertFromImage(image, Qt.MonoOnly)
        gpixmap.setPixmap(pixmap)

        gpixmap.setPos(QPointF(0.0, 0.0))
        gpixmap.setTransformOriginPoint(pixmap.rect().center())
        self.photo_rect = gpixmap.boundingRect()
        gpixmap.update()
        gpixmap.setZValue(0)
        # TODO let setting sceneRect be the responsibility of ImageViewer
        self.scene().setSceneRect(self.photo_rect)
        self.scene().update()

    def set_photo(self, photo: Optional[Photo], reset_tool: bool = True):
        self.prepareGeometryChange()
        if photo is None:
            self.setVisible(False)
            self.image_gpixmap.setVisible(False)
            return
        else:
            self.setVisible(True)
            self.image_gpixmap.setVisible(True)
        # img = nd2qimage(photo.image)
        img = qimage2ndarray.array2qimage(photo.image)
        self._set_pixmaps(img,
                          self._image_pixmap,
                          self.image_gpixmap)

    def boundingRect(self) -> PySide6.QtCore.QRectF:
        if self.state.current_photo is not None:
            return self.photo_rect
        return QRectF()

    def paint(self, painter: PySide6.QtGui.QPainter, option: PySide6.QtWidgets.QStyleOptionGraphicsItem,
              widget: Optional[PySide6.QtWidgets.QWidget] = None):
        pass
