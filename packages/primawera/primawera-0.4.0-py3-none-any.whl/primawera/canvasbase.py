from functools import partial
from typing import Optional, Dict, List, Union, Tuple

import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QAction, \
    QFileDialog, QMessageBox
from numpy.typing import ArrayLike, NDArray

import primawera.lut as lut
from primawera.filters import linear_contrast, gamma_correction
from primawera.informationwindow import InformationWindow
from primawera.loading import load_data
from primawera.modeutils import is_mode_color, is_mode_grayscale
from primawera.previewwindow import PreviewDialog


class CanvasBase(QWidget):
    menus_changed_signal = pyqtSignal()
    signal_changed_filter = pyqtSignal(str)
    signal_changed_coordinates = pyqtSignal(int, int, int, object, object,
                                            object)

    def __init__(self, data: ArrayLike, mode: str,
                 desktop_height: int, desktop_width: int,
                 filters: Optional[Dict[str, bool]] = None,
                 filters_options: Optional[Dict[str, int]] = None,
                 overlay_data: Optional[NDArray[int]] = None,
                 overlay_is_grayscale: bool = True,
                 *args, **kwargs) -> None:
        super(CanvasBase, self).__init__(*args, **kwargs)
        self.data = np.asanyarray(data)
        if overlay_data is not None \
                and self._check_overlay_dtype(overlay_data):
            self.overlay_data = overlay_data
            self.overlay_is_grayscale = overlay_is_grayscale
        elif overlay_data is not None:
            overlay_data = None
            QMessageBox.information(
                self, "Information",
                f"Could not safely convert the overlay's type "
                f"({overlay_data.dtype}) to an unsigned 8 bit integer. "
                f"Supplied overlay data will be ignored.",
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok)
        else:
            self.overlay_data = None
            self.overlay_is_grayscale = overlay_is_grayscale
        self.filters = filters
        self.filters_options = filters_options
        self.lut = None
        self.mode = mode
        self._showing_info_panel = False
        # This may change, for example when applying LUTs.
        self.mode_visualisation = mode
        self.preview_dialog_value = 0
        self.current_filter_name = None

        self.axes_orientation = (0, 1, 2)
        self.desktop_height = desktop_height
        self.desktop_width = desktop_width
        if self.mode == "":
            raise RuntimeError("Empty mode encountered")

    def _init_interface(self):
        self.main_layout = QVBoxLayout()
        self.view_layout = QGridLayout()
        self._information_window = InformationWindow()
        self._information_window.update_data_format(self.data.shape,
                                                    self.data.dtype, self.mode)
        self._information_window.hide()
        self.signal_changed_filter.connect(
            self._information_window.update_filter_name_slot)

    def _create_actions(self):
        self.no_filter_action = QAction("None")
        self.logarithm_stretch_action = QAction("Logarithm stretch")
        self.linear_stretch_action = QAction("Linear stretch")
        self.linear_contrast_action = QAction("Linear contrast...")
        self.gamma_correction_action = QAction("Gamma correction...")
        self.lut_actions = []
        self.lut_actions.append(("None", QAction("None")))
        for lut_name in lut.LUTS.keys():
            self.lut_actions.append((lut_name, QAction(lut_name)))
        self.show_info_action = QAction("Show info panel")
        self.add_overlay_action = QAction("Add file as overlay...")
        self.remove_overlay_action = QAction("Remove overlay")

    def _connect_info_window_and_canvas(self):
        raise NotImplementedError("CanvasBase should not be directly created!")

    def _connect_actions(self):
        self.no_filter_action.triggered.connect(self._no_filter)
        self.logarithm_stretch_action.triggered.connect(
            self._logarithm_stretch)
        self.linear_stretch_action.triggered.connect(self._linear_stretch)
        self.linear_contrast_action.triggered.connect(self._linear_contrast)
        self.gamma_correction_action.triggered.connect(self._gamma_correction)
        for lut_name, lut_action in self.lut_actions:
            lut_action.triggered.connect(partial(self._apply_lut, lut_name))
        self._connect_info_window_and_canvas()
        self.signal_changed_coordinates.connect(
            self._information_window.update_coordinates_slot)
        self.show_info_action.triggered.connect(self._toggle_information_panel)
        self.add_overlay_action.triggered.connect(self._add_overlay_ui)
        self.remove_overlay_action.triggered.connect(self._remove_overlay)

    def _set_actions_checkable(self) -> None:
        for action in self.get_actions():
            action.setCheckable(True)

    def _no_filter(self):
        self.current_filter_name = "No filter"
        self.filters.clear()
        self._redraw(self._process_data())

    def _linear_stretch(self):
        self.current_filter_name = "Linearly stretched"
        self.filters = {"linear_stretch": True}
        self._redraw(self._process_data())

    def _logarithm_stretch(self):
        self.current_filter_name = "Logarithmically stretched"
        self.filters = {"logarithm_stretch": True}
        self._redraw(self._process_data())

    def _linear_contrast(self):
        self.current_filter_name = "Linearly adjusted contrast"
        dialog = PreviewDialog(self.data, [("Factor", int, 100, 0, 1)],
                               self.mode, linear_contrast)
        dialog.return_signal.connect(self.preview_dialog_slot)
        ret = dialog.exec()
        if ret == 0:
            self.no_filter_action.trigger()
            return
        factor = self.preview_dialog_value
        self.filters = {"linear_contrast": True}
        self.filters_options = {"factor": float(factor)}
        self._redraw(self._process_data())

    def _gamma_correction(self):
        self.current_filter_name = "Gamma corrected"
        dialog = PreviewDialog(self.data, [("Factor", float, 2.0, 0.0, 0.1)],
                               self.mode, gamma_correction)
        dialog.return_signal.connect(self.preview_dialog_slot)
        ret = dialog.exec()
        if ret == 0:
            self.no_filter_action.trigger()
            return
        factor = self.preview_dialog_value
        self.filters = {"gamma_correction": True}
        self.filters_options = {"factor": factor}
        self._redraw(self._process_data())

    def _apply_lut(self, name):
        if name == "None":
            self.mode_visualisation = self.mode
            self.lut = None
        else:
            self.lut = lut.get_lut(name)
        self._redraw(self._process_data())

    def _check_overlay_dtype(self, overlay: NDArray) -> bool:
        return np.can_cast(overlay.dtype, np.uint8)

    def _add_overlay_io(self) -> Optional[Tuple[ArrayLike, bool]]:
        # TODO: duplicate in app.py
        file_name, _ = QFileDialog.getOpenFileName(self, "Open file", ".",
                                                   "Image file (*.jpg *.png"
                                                   " *.h5 *.tif *.tiff)")
        if file_name == "":
            # User did not select a file
            return
        try:
            data, mode = load_data(file_name)
            if not self._check_overlay_dtype(data):
                raise RuntimeError(
                    f"Cannot safely cast {data.dtype} to an unsigned 8 bit "
                    f"integer!")
        except RuntimeError as err:
            QMessageBox.critical(self, "Error",
                                 f"Failed to load data ({file_name}) "
                                 f"with message: {err}",
                                 buttons=QMessageBox.Ok,
                                 defaultButton=QMessageBox.Ok)
            return None
        if is_mode_color(mode):
            is_grayscale = False
        elif is_mode_grayscale(mode):
            is_grayscale = True
        else:
            return None
        return data, is_grayscale

    def _reshape_overlay_data(self, overlay_data: NDArray[int],
                              is_grayscale: bool) -> NDArray[int]:
        overlay_dims = len(overlay_data.shape)

        if is_grayscale and overlay_dims == 2:
            w, h = overlay_data.shape
            overlay_data = np.reshape(overlay_data, (1, w, h))
            overlay_dims = len(overlay_data.shape)
            assert overlay_dims == 3
        elif not is_grayscale and overlay_dims == 3:
            w, h, ch = overlay_data.shape
            overlay_data = np.reshape(overlay_data, (1, w, h, ch))
            overlay_dims = len(overlay_data.shape)
            assert overlay_dims == 4

        if is_grayscale and overlay_dims == 3:
            f, w, h = overlay_data.shape
            overlay_data = np.reshape(overlay_data, (f, w, h, 1))
            orig_overlay = overlay_data
            overlay_data = np.append(overlay_data, overlay_data, axis=3)
            overlay_data = np.append(overlay_data, orig_overlay, axis=3)
            overlay_dims = len(overlay_data.shape)
            assert overlay_dims == 4, "Reshaping overlay into higher" \
                                      " dimension failed!"

        assert overlay_dims == 4, "Reshaping failed due to incorrect " \
                                  "internal logic. Please contact the " \
                                  "developer."
        return overlay_data

    def _add_overlay_ui(self) -> None:
        result = self._add_overlay_io()
        if result is None:
            return

        overlay_data, is_grayscale = result
        self._add_overlay(overlay_data, is_grayscale)

    def _add_overlay(self, overlay_data: NDArray[int],
                     is_grayscale: bool = True) -> None:
        raise NotImplementedError("CanvasBase should not be directly created!")

    def _remove_overlay(self) -> None:
        raise NotImplementedError("CanvasBase should not be directly created!")

    # TODO: this is not a redraw function, but an update function.
    def _redraw(self, new_data) -> None:
        raise NotImplementedError("CanvasBase should not be directly created!")

    def keyPressEvent(self, event: QKeyEvent) -> None:
        actions = [
            (QtCore.Qt.Key_Plus, self._increase_zoom_level),
            (QtCore.Qt.Key_Minus, self._decrease_zoom_level),
            (QtCore.Qt.Key_I, self._toggle_information_panel),
            (QtCore.Qt.Key_Space, self._hide_overlay)
        ]

        entered_actions = list(
            filter(lambda comb: comb[0] == event.key(), actions))
        if len(entered_actions) == 0:
            event.ignore()
            return
        _, action = entered_actions[0]
        action()

    def keyReleaseEvent(self, event) -> None:
        if event.isAutoRepeat():
            event.ignore()
        elif event.key() == QtCore.Qt.Key_Space:
            self._show_overlay()
            event.accept()
        else:
            event.ignore()

    def _increase_zoom_level(self):
        raise NotImplementedError("CanvasBase should not be directly created!")

    def _decrease_zoom_level(self):
        raise NotImplementedError("CanvasBase should not be directly created!")

    def _toggle_information_panel(self):
        self._showing_info_panel = not self._showing_info_panel
        if not self._showing_info_panel:
            self._information_window.hide()
        else:
            self._information_window.show()

    def get_filters(self):
        raise NotImplementedError("CanvasBase should not be directly created!")

    def get_luts(self):
        raise NotImplementedError("CanvasBase should not be directly created!")

    def get_actions(self):
        raise NotImplementedError("CanvasBase should not be directly created!")

    def get_menus(self):
        return [
            ("Other", [self.show_info_action]),
        ]

    def _process_data(self):
        if self.current_filter_name is not None:
            self.signal_changed_filter.emit(self.current_filter_name)

    def update_desktop_size(self, width: int, height: int) -> None:
        # TODO: this does not affect anything.
        self.desktop_width = width
        self.desktop_height = height

    @pyqtSlot(list)
    def preview_dialog_slot(self, data: List[Union[int, float]]) -> None:
        self.preview_dialog_value = data[0]

    @pyqtSlot(int, int, int, list, list)
    def changed_coordinates_signal(self, frame: int, row: int, col: int,
                                   mapped_val: ArrayLike,
                                   overlay_label: ArrayLike) -> None:
        self.signal_changed_coordinates.emit(frame, row, col,
                                             mapped_val,
                                             self.data[frame, row, col],
                                             overlay_label)

    def closeEvent(self, event) -> None:
        self._information_window.close()
        super().closeEvent(event)

    def _hide_overlay(self) -> None:
        raise NotImplementedError("CanvasBase should not be directly created!")

    def _show_overlay(self) -> None:
        raise NotImplementedError("CanvasBase should not be directly created!")
