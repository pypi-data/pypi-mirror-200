from typing import Union, Callable, Tuple, List, Optional

import numpy as np
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, \
    QDoubleSpinBox, QMessageBox, QHBoxLayout, QPushButton, QCheckBox
from numpy.typing import ArrayLike

from primawera.visualiser import Visualiser

ConstraintType = Union[int, float]
Bound = Union[int, float]
Constraint = Tuple[str, ConstraintType, Bound, Bound, float]


class PreviewDialog(QDialog):
    return_signal = pyqtSignal(list)
    maximum_width = 400
    maximum_height = 400

    def __init__(self, data: ArrayLike, constraints: List[Constraint],
                 mode: str, function: Callable[
                [ArrayLike, Union[int, float]], ArrayLike]):
        super().__init__()
        self.function = function
        self.data = data
        self.mode = mode
        self._init_interface(constraints)

    def _init_interface(self, constraints: List[Constraint]) -> None:
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(QLabel("Preview:"))
        processed_data = np.clip(self.data, 0, 255.0).astype(np.uint8)
        self.visualiser = Visualiser(processed_data, (0, 1, 2), self.mode,
                                     self.maximum_height, self.maximum_width,
                                     True)
        self.main_layout.addWidget(self.visualiser)

        self.sliders = []
        for name, constraint, max_val, min_val, step in constraints:
            name_label = QLabel(name)
            slider: Optional[Union[QSpinBox, QDoubleSpinBox]] = None
            # TODO: Maybe it is better to always use float
            if constraint == int:
                slider = QSpinBox()
            elif constraint == float:
                slider = QDoubleSpinBox()
            else:
                QMessageBox \
                    .warning(self, "Warning",
                             f"Invalid constraints ({type(constraint)})"
                             f" provided.",
                             buttons=QMessageBox.Ok,
                             defaultButton=QMessageBox.Ok)
                self.reject()
            assert slider is not None
            # for mypy
            if isinstance(slider, QSpinBox):
                max_val = int(max_val)
                min_val = int(min_val)
                step = int(step)
                slider.setRange(min_val, max_val)
                slider.setValue(min_val)
                slider.setSingleStep(step)
            else:
                slider.setRange(min_val, max_val)
                slider.setValue(min_val)
                slider.setSingleStep(step)

            self.sliders.append(slider)
            slider.valueChanged.connect(self._constrained_changed_slot)

            line_layout = QHBoxLayout()
            line_layout.addWidget(name_label)
            line_layout.addWidget(slider)
        self.main_layout.addLayout(line_layout)

        self.preview_button = QPushButton("Refresh preview")
        self.preview_button.clicked.connect(self._refresh_preview)
        self.preview_button.setDisabled(True)
        self.auto_refresh_checkbox = QCheckBox("Automatically refresh preview")
        self.auto_refresh_checkbox.clicked.connect(self._toggle_auto_refresh)
        self.auto_refresh_checkbox.setChecked(True)
        accept_button = QPushButton("Apply")
        accept_button.clicked.connect(self.accept)
        reject_button = QPushButton("Cancel")
        reject_button.clicked.connect(self.reject)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.preview_button)
        button_layout.addWidget(self.auto_refresh_checkbox)
        button_layout.addWidget(accept_button)
        button_layout.addWidget(reject_button)

        self.main_layout.addLayout(button_layout)
        self.setLayout(self.main_layout)

    def _refresh_preview(self) -> None:
        inputs = list(map(lambda x: x.value(), self.sliders))
        if np.issubdtype(self.data.dtype, np.integer):
            # Bump up the bitdepth
            data = self.data.astype(int)
        else:
            data = self.data.astype(float)
        new_data = self.function(data, inputs[0])
        new_data = np.clip(new_data, 0, 255.0).astype(np.uint8)
        self.visualiser.update_data(new_data, (0, 1, 2), self.mode)
        self.visualiser.redraw()

    @pyqtSlot()
    def _constrained_changed_slot(self):
        if not self.preview_button.isEnabled():
            self._refresh_preview()

    @pyqtSlot(bool)
    def _toggle_auto_refresh(self, val: bool):
        self.preview_button.setEnabled(not val)

    def accept(self) -> None:
        self.return_signal.emit(list(map(lambda x: x.value(), self.sliders)))
        super().accept()
