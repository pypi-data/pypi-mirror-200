from typing import Tuple

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from numpy.typing import DTypeLike, ArrayLike

from primawera.modeutils import print_mode


class InformationWindow(QWidget):
    def __init__(self, parent=None) -> None:
        """
        Auxiliary window showing information about the visualised data.

            Parameters
            ----------
            shape: tuple of ints
                Tuple describing the data's shape.
            datatype: DTypeLike object
                Dtype of numpy array.
            mode: str
                Used image mode.
            filter_name: str
                Name of the used filter.
        """
        super().__init__(parent)
        self.setWindowTitle("Primawera - Info panel")
        self.label_format_info = QLabel()
        self.main_layout = QVBoxLayout()

        self.label_format_info.setAlignment(Qt.AlignTop)
        self.label_used_filter = QLabel("")
        self.label_used_filter.setContentsMargins(20, 0, 0, 0)
        info_layout = QHBoxLayout()
        info_layout.addWidget(self.label_format_info)
        info_layout.addWidget(self.label_used_filter)
        self.main_layout.addLayout(info_layout)

        self.label_coordinates = QLabel("")
        self.label_coordinates.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(self.label_coordinates)

        self.setLayout(self.main_layout)

    def update_data_format(self, shape: Tuple[int, ...], datatype: DTypeLike,
                           mode: str) -> None:
        """
        Updates the information about the format.
            Parameters
            ----------
            shape: tuple of ints
                Tuple describing the data's shape.
            datatype: DTypeLike object
                Dtype of numpy array.
            mode: str
                Used image mode.
        """
        self.label_format_info.setText(
            f"Data shape: {self._transform_shape(shape)}\n"
            f"Data type: {datatype}\n"
            f"Data mode: {print_mode(mode)}")

    @pyqtSlot(str)
    def update_filter_name_slot(self, filter_name: str) -> None:
        self.label_used_filter.setText(filter_name)

    @pyqtSlot(int, int, int, object, object, object)
    def update_coordinates_slot(self, frame: int, row: int, col: int,
                                mapped_value: ArrayLike,
                                original_value: ArrayLike,
                                overlay_label: ArrayLike) -> None:
        # Note: numpy is row-centric, that's why y and x are switched
        text = f"frame={frame}, row={row}, col={col}\n " \
               f"original value={original_value})\n" \
               f"mapped value={mapped_value}\n"
        if overlay_label[0][0] != -1:
            text += f"overlay label={overlay_label}"

        self.label_coordinates.setText(text)

    @staticmethod
    def _transform_shape(shape: Tuple[int, ...]) -> str:
        dimensions = [str(x) for x in shape]
        if dimensions[0] == '1':
            dimensions = dimensions[1:]
        return "(" + ",".join(dimensions) + ")"
