from enum import Enum, auto
from typing import Dict, Optional

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction
from numpy.typing import ArrayLike

from primawera.canvasbase import CanvasBase
from primawera.filters import logarithm_stretch, linear_stretch
from primawera.lut import apply_lut
from primawera.visualiser import Visualiser


class ShowEnum(Enum):
    MAGNITUDE = auto()
    PHASE = auto()
    REAL_PART = auto()
    IMAG_PART = auto()


class CanvasComplex(CanvasBase):

    def __init__(self, data: ArrayLike, mode: str,
                 desktop_height: int, desktop_width: int,
                 filters: Optional[Dict[str, bool]] = None,
                 filters_options: Optional[Dict[str, int]] = None, *args,
                 **kwargs) -> None:
        super().__init__(data, mode, desktop_height, desktop_width,
                         filters, filters_options, *args, **kwargs).__init__(
            *args, **kwargs)
        if self.mode != "C":
            raise RuntimeError("CanvasComplex expects complex data!")

        if filters:
            self.filters = filters
        else:
            self.filters = {"linear_stretch": True}

        self.show = ShowEnum.MAGNITUDE

        self._init_interface()
        self._create_actions()
        self._set_actions_checkable()
        self._reset_checked_states()
        self._connect_actions()
        self._show_magnitude()
        self.get_luts()[0].setChecked(True)

    def _init_interface(self):
        super()._init_interface()
        maximum_width = int(self.desktop_width * 0.8)
        maximum_height = int(self.desktop_height * 0.8)
        processed_data = self._process_data()
        self.visualiser = Visualiser(processed_data, (0, 1, 2), self.mode,
                                     maximum_height, maximum_width, True)
        self.view_layout.addWidget(self.visualiser, 0, 0, Qt.AlignTop)
        self.main_layout.addLayout(self.view_layout)

        self.setLayout(self.main_layout)

    def _connect_info_window_and_canvas(self):
        self.visualiser.signal_position.connect(
            self.changed_coordinates_signal)

    def _process_data(self) -> ArrayLike:
        super()._process_data()
        data = self.data.copy()
        if self.show == ShowEnum.MAGNITUDE:
            data = np.abs(data)
        elif self.show == ShowEnum.PHASE:
            data = np.arctan2(data.imag, data.real)
        elif self.show == ShowEnum.REAL_PART:
            data = np.real(data)
        else:
            data = np.imag(data)

        if self.filters.get("logarithm_stretch", False):
            data = logarithm_stretch(data)
            data = linear_stretch(data) * 255.0
        elif self.filters.get("linear_stretch", False):
            data = linear_stretch(data) * 255.0

        # Clip data
        data = np.clip(data, 0, 255.0).astype(np.uint8)

        # Apply LUT
        if self.lut is not None:
            self.mode_visualisation = "rgb"
            data = apply_lut(data, self.lut)

        self.menus_changed_signal.emit()
        return data

    def _reset_view(self):
        self._reset_checked_states()
        self.get_luts()[0].setChecked(True)
        self.lut = None
        self.mode_visualisation = self.mode

    def _show_magnitude(self):
        self._reset_view()
        self.show_magnitude_action.setChecked(True)
        self.linear_stretch_action.setChecked(True)
        self.show = ShowEnum.MAGNITUDE
        self.menus_changed_signal.emit()
        self._linear_stretch()

    def _show_phase(self):
        self._reset_view()
        self.show_phase_action.setChecked(True)
        self.linear_stretch_action.setChecked(True)
        self.show = ShowEnum.PHASE
        self.menus_changed_signal.emit()
        self._linear_stretch()

    def _show_real_part(self):
        self._reset_view()
        self.show_real_part_action.setChecked(True)
        self.linear_stretch_action.setChecked(True)
        self.show = ShowEnum.REAL_PART
        self.menus_changed_signal.emit()
        self._linear_stretch()

    def _show_imag_part(self):
        self._reset_view()
        self.show_imag_part_action.setChecked(True)
        self.linear_stretch_action.setChecked(True)
        self.show = ShowEnum.IMAG_PART
        self.menus_changed_signal.emit()
        self._linear_stretch()

    def _reset_checked_states(self):
        for action in self.get_actions():
            action.setChecked(False)

    def _redraw(self, new_data):
        # Showing phase/magnitude
        if self.show == ShowEnum.MAGNITUDE:
            showing = "Magnitude"
        elif self.show == ShowEnum.PHASE:
            showing = "Phase"
        elif self.show == ShowEnum.REAL_PART:
            showing = "Real part"
        else:
            showing = "Imaginary part"

        self.current_filter_name = self.current_filter_name + "\nShowing" \
                                                              f" {showing}"
        self.signal_changed_filter.emit(self.current_filter_name)

        self.visualiser.update_data(new_data, self.axes_orientation,
                                    self.mode_visualisation)
        self.visualiser.redraw()

    def _create_actions(self):
        super()._create_actions()
        self.show_magnitude_action = QAction("Show magnitude")
        self.show_phase_action = QAction("Show phase")
        self.show_real_part_action = QAction("Show real part")
        self.show_imag_part_action = QAction("Show imaginary part")

    def _connect_actions(self):
        super()._connect_actions()
        self.show_magnitude_action.triggered.connect(self._show_magnitude)
        self.show_phase_action.triggered.connect(self._show_phase)
        self.show_real_part_action.triggered.connect(self._show_real_part)
        self.show_imag_part_action.triggered.connect(self._show_imag_part)

    def get_filters(self):
        return [self.linear_stretch_action, self.logarithm_stretch_action]

    def get_luts(self):
        return [action for _, action in self.lut_actions]

    def get_views(self):
        return [self.show_magnitude_action, self.show_phase_action,
                self.show_real_part_action, self.show_imag_part_action]

    def get_actions(self):
        result = self.get_filters()
        result.extend(self.get_luts())
        result.extend(self.get_views())
        return result

    def get_menus(self):
        base_menu = super().get_menus()
        view_filters = ("View", self.get_views())
        if self.show == ShowEnum.PHASE:
            result = [
                ("Filters", [
                    self.linear_stretch_action
                ]),
                view_filters,
                ("LUT", self.get_luts()),
            ]
        else:
            result = [
                ("Filters", self.get_filters()),
                view_filters
            ]
        return result + base_menu

    def _increase_zoom_level(self):
        self.visualiser.increase_zoom_level()

    def _decrease_zoom_level(self):
        self.visualiser.decrease_zoom_level()
