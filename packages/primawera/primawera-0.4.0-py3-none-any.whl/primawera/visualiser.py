import numpy as np
from PIL import ImageQt
from PyQt5.QtCore import pyqtSignal, Qt, QSize, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage, QPalette
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from numpy.typing import NDArray

from primawera.HighlightScrollArea import HighlightScrollArea
from primawera.loading import UnsupportedFormatError
from primawera.pixmaplabel import PixmapLabel


class Visualiser(QWidget):
    signal_position = pyqtSignal(int, int, int, list, list)
    value_change_emitter_vertical = pyqtSignal(int)
    value_change_emitter_horizontal = pyqtSignal(int)

    def __init__(self, data, axes_orientation, mode, maximum_height,
                 maximum_width, main_window, *args, overlay_data=None,
                 **kwargs):
        super(Visualiser, self).__init__(*args, **kwargs)
        self.axes_orientation = None
        self.data = None
        self.overlay_data = overlay_data
        self.mode = None
        self.height = 0
        self.width = 0
        self.frames = 0
        self.frame = 0
        self.background_pixmaps = []
        self.overlay_pixmaps = []
        self.main_window = main_window

        self.MAXIMUM_HEIGHT = maximum_height
        self.MAXIMUM_WIDTH = maximum_width
        self.ZOOMED_MAX_SIZE = 32000

        # Set up label
        self.label = PixmapLabel()
        self.label.setAlignment(Qt.AlignLeft)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(
            "padding: 0px; border: 0px; margin: 0px")

        self.zoom_level = 1
        self.update_data(data, axes_orientation, mode)

        # Set up scroll area
        self.scroll_area = HighlightScrollArea(width=1)
        self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setAlignment(Qt.AlignLeft)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)

        # Set up layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.scroll_area)
        self.layout.setAlignment(Qt.AlignLeft)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Set up event handling
        self.connect_horizontal_bar()
        self.connect_vertical_bar()

        self.setStyleSheet(
            "padding: 0px; margin:0px; border: 0px")

        # Set up focus in/out border change
        # self.focusChanged.connect(self.focus_changed)

    def connect_vertical_bar(self):
        self.get_vertical_bar().valueChanged.connect(
            self._value_change_wrapper_vertical)

    def connect_horizontal_bar(self):
        self.get_horizontal_bar().valueChanged.connect(
            self._value_change_wrapper_horizontal)

    def update_data(self, data, axes_orientation, mode):
        # Prepare the data
        # NOTE: Without copy() the program may receive SIGSEV.
        self.axes_orientation = axes_orientation
        self.mode = mode
        if self.mode == "rgb":
            axes_orientation = axes_orientation[0], axes_orientation[1], \
                axes_orientation[2], 3
        self.data = np.transpose(data, axes_orientation).copy()
        self.frames, self.height, self.width = self.data.shape[0], \
            self.data.shape[1], \
            self.data.shape[2]
        self.frame = 0
        self.background_pixmaps = [None] * self.frames
        self.overlay_pixmaps = [None] * self.frames
        self.label.mouse_position_signal.connect(self.print_info)

    def redraw(self):
        self._generate(self.frame)
        self.choose_frame(self.frame)

    def print_info(self, relative_x: float, relative_y: float) -> None:
        if self.mode in {"grayscale", "1", "F", "C"}:
            _, data_rows, data_cols = self.data.shape
        else:
            _, data_rows, data_cols, _ = self.data.shape
        position_x = int(relative_x * data_cols)
        position_y = int(relative_y * data_rows)

        # Now take into account the transposition of the data
        transposed_coords = [self.frame, position_y, position_x]
        real_frame = transposed_coords[self.axes_orientation.index(0)]
        real_x = transposed_coords[self.axes_orientation.index(1)]
        real_y = transposed_coords[self.axes_orientation.index(2)]

        # Note: numpy is row-centric, that's why y and x are switched
        mapped_value = [self.data[self.frame, position_y, position_x]]

        # Overlay label at given position
        if self.overlay_data is not None:
            overlay_label = \
                self.overlay_data[self.frame, position_y, position_x]
        else:
            overlay_label = [-1]
        self.signal_position.emit(real_frame, real_x, real_y, mapped_value,
                                  [overlay_label])

    def _generate(self, frame: int) -> None:
        if self.background_pixmaps[frame] is None:
            self.background_pixmaps[frame] = self._generate_background(frame)

        if self.overlay_data is not None \
                and self.overlay_pixmaps[frame] is None:
            self.overlay_pixmaps[frame] = self._generate_overlay(frame)

    def _generate_background(self, frame: int) -> QPixmap:

        if self.mode in {"grayscale", "1", "F", "C"}:
            qimage = ImageQt.QImage(self.data[frame, :, :], self.width,
                                    self.height,
                                    self.width, QImage.Format_Grayscale8)
        elif self.mode == "rgb":
            qimage = ImageQt.QImage(self.data[frame, :, :], self.width,
                                    self.height,
                                    3 * self.width, QImage.Format_RGB888)
        else:
            # TODO: This isn't handled in Canvas objects.
            raise UnsupportedFormatError(
                f"Combination of mode='{self.mode}' with Canvas is not"
                f" supported.")
        return QPixmap.fromImage(qimage)

    def _generate_overlay(self, frame: int) -> QPixmap:
        # TODO: change to PREMULTIPLIED format
        assert self.overlay_data is not None
        assert np.issubdtype(self.overlay_data.dtype, np.uint8)
        overlay_image = ImageQt.QImage(self.overlay_data[frame, :, :],
                                       self.width, self.height, 4 * self.width,
                                       QImage.Format_RGBA8888)
        return QPixmap.fromImage(overlay_image)

    def choose_frame(self, frame: int) -> None:
        if frame < 0 or frame >= self.frames:
            return
        self.frame = frame

        # Calculate the right size of the image label
        zoomed_width = self.width * self.zoom_level
        zoomed_height = self.height * self.zoom_level
        self._generate(frame)  # TODO: this causes unnecessary operations
        resized_background = self.background_pixmaps[self.frame].scaled(
            QSize(zoomed_width, zoomed_height),
            Qt.KeepAspectRatio)
        # Update the pixmap
        self.label.setPixmap(resized_background)

        if self.overlay_pixmaps[self.frame] is not None:
            resized_overlay = self.overlay_pixmaps[self.frame].scaled(
                QSize(zoomed_width, zoomed_height),
                Qt.KeepAspectRatio)
            self.label.setOverlay(resized_overlay)

        self.label.setStyleSheet("border: 0px")

        # Calculate the size of the container QLabel.
        label_width = min(zoomed_width, self.MAXIMUM_WIDTH)
        label_height = min(zoomed_height, self.MAXIMUM_HEIGHT)

        # Update the container's size
        self.label.setMinimumSize(zoomed_width, zoomed_height)
        self.label.setMaximumSize(zoomed_width, zoomed_height)

        height, width = label_height, label_width

        # Hide the scrollbars
        self.scroll_area.horizontalScrollBar().setStyleSheet(
            "QScrollBar {height:0px;}")
        self.scroll_area.verticalScrollBar().setStyleSheet(
            "QScrollBar {width:0px;}")

        # If the image is too big, show the scrollbars only in the main wind.
        if label_width >= self.MAXIMUM_WIDTH:
            if self.main_window:
                # This is to accomodate the size of the scrollbars
                self.scroll_area.horizontalScrollBar().setStyleSheet(
                    "QScrollBar {height:10px;}")
                height += 10
        if label_height >= self.MAXIMUM_HEIGHT:
            if self.main_window:
                self.scroll_area.verticalScrollBar().setStyleSheet(
                    "QScrollBar {width:10px;}")
                width += 10

        self.scroll_area.setMaximumSize(width + 2, height + 2)
        self.scroll_area.setMinimumSize(width + 2, height + 2)

        self.setMinimumSize(width + 2, height + 2)
        self.setMaximumSize(width + 2, height + 2)

    def next_frame(self) -> None:
        self.choose_frame(self.frame + 1)

    def previous_frame(self) -> None:
        self.choose_frame(self.frame - 1)

    def decrease_zoom_level(self) -> None:
        self.zoom_level = max(self.zoom_level // 2, 1)
        self.choose_frame(self.frame)

    def increase_zoom_level(self) -> None:
        size = max(self.width, self.height) * self.zoom_level
        if size * 2 <= self.ZOOMED_MAX_SIZE:
            self.zoom_level = self.zoom_level * 2
            self.choose_frame(self.frame)

    def get_horizontal_bar(self):
        return self.scroll_area.horizontalScrollBar()

    def get_vertical_bar(self):
        return self.scroll_area.verticalScrollBar()

    def get_scroll_area(self):
        return self.scroll_area

    @pyqtSlot(int)
    def _value_change_wrapper_horizontal(self, value: int):
        if self.scroll_area.in_focus():
            self.value_change_emitter_horizontal.emit(value)

    @pyqtSlot(int)
    def _value_change_wrapper_vertical(self, value: int):
        if self.scroll_area.in_focus():
            self.value_change_emitter_vertical.emit(value)

    def has_focus(self) -> bool:
        return self.scroll_area.in_focus()

    def update_overlay(self, overlay_data: NDArray[int]):
        self.overlay_data = overlay_data

    def remove_overlay(self) -> None:
        self.overlay_pixmaps = [None] * self.frames
        self.overlay_data = None
        self.label.remove_overlay()

    def has_overlay(self) -> bool:
        return self.overlay_data is not None

    def hide_overlay(self) -> None:
        self.label.hide_overlay()

    def show_overlay(self) -> None:
        self.label.show_overlay()
