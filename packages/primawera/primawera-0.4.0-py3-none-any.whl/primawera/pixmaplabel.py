from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtWidgets import QLabel


class CompositionError(Exception):
    pass


# TODO: rename
class PixmapLabel(QLabel):
    mouse_position_signal = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()
        self.handle_mouse_movement = False
        self._overlay_pixmap = None
        self._background_pixmap = None
        self._hide_overlay = False

    def setPixmap(self, pixmap: QPixmap) -> None:
        self.handle_mouse_movement = True
        self.setMouseTracking(True)
        self._background_pixmap = pixmap
        # TODO: remove
        # super().setPixmap(pixmap)

    # TODO: rename
    def setOverlay(self, image: QImage) -> None:
        if self._background_pixmap is None:
            raise CompositionError("Cannot overlay data when background is "
                                   "equal to None!")
        if self._background_pixmap.height() != image.size().height():
            raise CompositionError(
                f"Height mismatch! bg: {self._background_pixmap.height()} "
                f" overlay: {image.size().height()}")
        if self._background_pixmap.width() != image.size().width():
            raise CompositionError(
                f"Width mismatch! bg: {self._background_pixmap.width()} "
                f"overlay: {image.size().width()}")
        self._overlay_pixmap = image

    def remove_overlay(self) -> None:
        self._overlay_pixmap = None

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        if self._background_pixmap is None:
            event.accept()
            return

        width, height = self._background_pixmap.width(), \
            self._background_pixmap.height()
        painter.drawPixmap(0, 0, width, height, self._background_pixmap)

        if self._overlay_pixmap is None or self._hide_overlay:
            event.accept()
            return
        painter.drawPixmap(0, 0, width, height, self._overlay_pixmap)
        event.accept()

    def mouseMoveEvent(self, event):
        if not self.handle_mouse_movement or self._background_pixmap is None:
            event.ignore()
            return

        event_x = event.pos().x()
        event_y = event.pos().y()
        if event_x < 0 or event_y < 0:
            event.ignore()
            return
        pixmap_width = self._background_pixmap.width()
        pixmap_height = self._background_pixmap.height()
        if event_x > pixmap_width or event_y > pixmap_height:
            event.ignore()
            return

        position_x = (event_x / pixmap_width)
        position_y = (event_y / pixmap_height)
        event.accept()
        self.mouse_position_signal.emit(position_x, position_y)

    def hide_overlay(self) -> None:
        self._hide_overlay = True
        self.update()  # To generate a paint event

    def show_overlay(self) -> None:
        self._hide_overlay = False
        self.update()
