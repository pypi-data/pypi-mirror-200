from os import listdir, path
from os.path import isdir, isfile
from typing import Tuple

import h5py
import numpy as np
from PIL import Image
from numpy.typing import ArrayLike


class UnsupportedFormatError(Exception):
    pass


def tiff_to_array(image) -> ArrayLike:
    """
    Takes a Tiff image and returns the raw data as a numpy array.
    :param image: Tiff image (PIL).
    :return: Numpy array with data.
    """
    result = []
    for i in range(image.n_frames):
        image.seek(i)
        current_frame = np.array(image)
        result.append(current_frame)
    return np.array(result)


def load_data(data_path: str) -> Tuple[ArrayLike, str]:
    """
    Takes a path to a file or a folder and tries to load the image data.

    Parameters
    ----------
    data_path: string
        Path to the data.

    Returns
    -------
    out: tuple with arraylike data and a string
        The loaded data and its mode.

    Raises
    ------
    RuntimeError
        If the specified path is not valid.

    """
    if isdir(data_path):
        raw_data, mode = load_folder(data_path)
    elif isfile(data_path):
        raw_data, mode = load_file(data_path)
    else:
        raise RuntimeError(
            f"'{data_path}' is neither a regular file nor a directory!")
    return raw_data, mode


def load_folder(path_to_dir: str):
    raw_data = []
    mode = ""
    for file in listdir(path_to_dir):
        if file.endswith(".png"):
            file_data, file_mode = load_file(
                path.join(path_to_dir, file))

            # Check if files are compatible
            if mode != "" and mode != file_mode:
                print(
                    f"[Error] Not all images in the directory '{path_to_dir}'\
                     have the same color mode!")
                return raw_data, mode

            # If this is the first file, set the mode accordingly
            if mode == "":
                mode = file_mode

            raw_data.append(file_data[0])
    return np.array(raw_data), mode


def load_file(file_path: str):
    # TODO: decompose this if else
    if file_path.endswith((".tif", ".tiff")):
        with Image.open(file_path) as tiff_file:
            mode = tiff_file.mode
            raw_data = tiff_to_array(tiff_file)
    elif file_path.endswith(".h5"):
        with h5py.File(file_path) as h5_file:
            h5_dataset = h5_file["Image"]
            type = h5_dataset.dtype
            if type in [np.float64, np.double, np.float32, np.float16,
                        np.single]:
                mode = "F"
            elif type == np.complex128:
                mode = "C"
            else:
                mode = "L"
            raw_data = np.zeros(h5_dataset.shape, dtype=type)
            h5_dataset.read_direct(raw_data)
    elif file_path.endswith((".jpg", ".png")):
        with Image.open(file_path) as image_file:
            raw_data = np.array(image_file, dtype=np.uint8).copy()
            mode = image_file.mode
        if mode == "RGB":
            raw_data = np.array([raw_data])
    else:
        raise UnsupportedFormatError("Unsupported file format!")

    if mode == "I;16" or mode == "I;16B":
        mode = "grayscale"
    elif mode == "L":
        mode = "grayscale"
    elif mode == "RGB":
        mode = "rgb"
    elif mode == "1" or mode == "F" or mode == "C":
        pass
    else:
        err = UnsupportedFormatError(f"Mode: \"{mode}\" is not implemented.")
        err.add_note(
            "See: https://pillow.readthedocs.io/en/stable/handbook/"
            "concepts.html")
        raise err

    # grayscale single frame data
    if len(raw_data.shape) == 2:
        raw_data = np.array([raw_data])

    return raw_data, mode
