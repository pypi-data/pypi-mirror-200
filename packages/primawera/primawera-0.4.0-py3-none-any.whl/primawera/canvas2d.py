from typing import Dict, List, Tuple, Optional

import numpy as np
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QAction, QMessageBox
from numpy.typing import ArrayLike, NDArray

from primawera.canvasbase import CanvasBase
from primawera.filters import linear_stretch, gamma_correction, \
    linear_contrast, logarithm_stretch
from primawera.lut import apply_lut
from primawera.visualiser import Visualiser


class Canvas2D(CanvasBase):
    menus_changed_signal = pyqtSignal()

    def __init__(self, data: ArrayLike, mode: str,
                 desktop_height: int, desktop_width: int,
                 filters: Optional[Dict[str, bool]] = None,
                 filters_options: Optional[Dict[str, int]] = None,
                 overlay_data: Optional[NDArray[int]] = None,
                 overlay_is_grayscale: bool = True,
                 *args, **kwargs) -> None:
        super(Canvas2D, self).__init__(data, mode, desktop_height,
                                       desktop_width, filters, filters_options,
                                       overlay_data, overlay_is_grayscale,
                                       *args, **kwargs)
        self._init_interface()
        self._create_actions()
        self._set_actions_checkable()
        self._connect_actions()

        if self.overlay_data is not None:
            self._add_overlay(self.overlay_data, self.overlay_is_grayscale)

        if self.mode != 'F':
            self._no_filter()
        else:
            self._linear_stretch()

        # Check default options
        self.get_filters()[0].setChecked(True)
        if self.mode == "grayscale":
            self.get_luts()[0].setChecked(True)

    def _process_data(self) -> ArrayLike:
        super()._process_data()
        if self.mode == "1":
            return (self.data * 255).astype(np.uint8)
        processed_data = self.data.astype(float)

        # Apply filters
        if self.filters.get("linear_stretch", False):
            processed_data = 255.0 * linear_stretch(processed_data)
        elif self.filters.get("gamma_correction", False):
            gamma_factor = self.filters_options.get("factor", 0.5)
            processed_data = gamma_correction(processed_data, gamma_factor)
        elif self.filters.get("linear_contrast", False):
            stretch_factor = self.filters_options.get("factor", 2)
            processed_data = linear_contrast(processed_data, stretch_factor)
        elif self.filters.get("logarithm_stretch", False):
            processed_data = logarithm_stretch(processed_data, factor=10.0)
            # Normalise to range [0,255]
            processed_data = 255.0 * linear_stretch(processed_data)

        # Clip data
        processed_data = np.clip(processed_data, 0, 255.0).astype(np.uint8)

        # Apply LUT
        if self.lut is not None:
            self.mode_visualisation = "rgb"
            processed_data = apply_lut(processed_data, self.lut)

        self.menus_changed_signal.emit()
        return processed_data

    def _init_interface(self) -> None:
        super()._init_interface()

        maximum_width = int(self.desktop_width * 0.80)
        maximum_height = int(self.desktop_height * 0.80)
        processed_data = self._process_data()
        self.visualiser = Visualiser(processed_data, (0, 1, 2), self.mode,
                                     maximum_height, maximum_width, True)

        self.view_layout.addWidget(self.visualiser, 0, 0, Qt.AlignTop)
        self.main_layout.addLayout(self.view_layout)
        self.setLayout(self.main_layout)
        self._connect_info_window_and_canvas()

    def _connect_info_window_and_canvas(self) -> None:
        self.visualiser.signal_position.connect(
            self.changed_coordinates_signal)

    def get_actions(self) -> List[QAction]:
        result = self.get_filters()
        result.extend(self.get_luts())
        return result

    def get_filters(self) -> List[QAction]:
        if self.mode == "F":
            return [self.linear_stretch_action, self.logarithm_stretch_action]

        result = [self.no_filter_action]
        if self.mode == "1":
            return result

        if self.mode == "grayscale" or self.mode == "F":
            result.append(self.linear_stretch_action)

        result.extend([self.linear_contrast_action,
                       self.gamma_correction_action])
        return result

    def get_luts(self) -> List[QAction]:
        if self.mode == "grayscale" or self.mode == "F":
            return [action for _, action in self.lut_actions]
        return []

    def get_menus(self) -> List[Tuple[str, List[QAction]]]:
        base_menu = super().get_menus()
        lut_entry = ("LUT", self.get_luts())
        filter_entry = ("Filters", self.get_filters())
        overlay_entry = "Overlay", [self.add_overlay_action,
                                    self.remove_overlay_action],
        result = [filter_entry, lut_entry, overlay_entry] if lut_entry[1] \
            else [filter_entry, overlay_entry]
        return result + base_menu

    def _redraw(self, new_data: ArrayLike) -> None:
        self.visualiser.update_data(new_data, self.axes_orientation,
                                    self.mode_visualisation)
        self.visualiser.redraw()

    def _increase_zoom_level(self):
        self.visualiser.increase_zoom_level()

    def _decrease_zoom_level(self):
        self.visualiser.decrease_zoom_level()

    def _add_overlay(self, overlay_data: NDArray[int],
                     is_grayscale: bool = True) -> None:
        if self.visualiser.has_overlay():
            self.visualiser.remove_overlay()

        overlay_original = overlay_data
        overlay_reshaped = self._reshape_overlay_data(overlay_data,
                                                      is_grayscale)
        data_dims = len(self.data.shape)

        # The overlay can have more dimensions if it is coloured and the data
        # under it is in grayscale.
        if (data_dims == 3
            and overlay_reshaped.shape[:-1] != self.data.shape) \
                or (
                data_dims == 4 and overlay_reshaped.shape != self.data.shape):
            QMessageBox.critical(
                self, "Error", f"The shape {overlay_original.shape} is not"
                               f" compatible with underlying image. It was "
                               f"automatically reshaped to "
                               f"{overlay_reshaped.shape}",
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok)
            return

        # TODO: right now the opacity is fixed
        opacity_mask_shape = list(overlay_reshaped.shape)
        opacity_mask_shape[-1] = 1
        opacity_mask = np.zeros(shape=tuple(opacity_mask_shape)).astype(
            np.uint8)
        opacity_mask[overlay_reshaped[:, :, :, 0] != 0] = 255

        # Add opacity (alpha channel) to the overlay data
        overlay_reshaped = np.append(overlay_reshaped, opacity_mask, axis=3)

        self.visualiser.update_overlay(overlay_reshaped)
        # TODO: It does not make sense to reset the overlay_data when
        #       new filter or LUT is applied.
        #       => Separate this behaviour in other functions.
        self.visualiser.redraw()

    def _remove_overlay(self) -> None:
        # TODO: consider if redrawing is necessary in all cases
        self.visualiser.remove_overlay()
        self.visualiser.redraw()

    def _hide_overlay(self) -> None:
        self.visualiser.hide_overlay()

    def _show_overlay(self) -> None:
        self.visualiser.show_overlay()
