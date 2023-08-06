import sys
from importlib.resources import files
from os import listdir
from os.path import isdir
from pathlib import Path
from typing import TextIO

import numpy as np
from numpy.typing import ArrayLike

LUT = ArrayLike
LUTS = dict()


def add_file(file_descriptor: TextIO, name: str) -> None:
    # Load the LUT
    file_lut = [0 for _ in range(256)]
    for line in file_descriptor:
        parts = [int(x) for x in line.rstrip().split(";")]
        val, map_val = parts[0], parts[1:]
        file_lut[val] = map_val
    file_lut = np.array(file_lut)
    LUTS[name] = file_lut


def add_luts_at_path(path_to_luts: str) -> None:
    if not isdir(path_to_luts):
        raise RuntimeWarning(f"{path_to_luts} is not a directory!")

    for file in listdir(path_to_luts):
        if path_to_luts is None:
            file = str(file)

        if not file.endswith(".lut"):
            print(
                f"Warning: Skipped f{file} as it does not end with \'.lut\'.",
                file=sys.stderr)
            continue

        # Create name
        name = Path(file).stem.capitalize()
        with open(path_to_luts + file) as file_input:
            add_file(file_input, name)


def fill_luts() -> None:
    resource = files("primawera.luts")
    if not resource.is_dir():
        raise RuntimeWarning("Cannot find LUTs resource inside the package!")

    for resource_file in resource.iterdir():
        if not resource_file.name.endswith(".lut"):
            print(
                f"Warning: Skipped f{resource_file} as it does not end with \'"
                f".lut\'.",
                file=sys.stderr)
            continue

        # Create name
        name = resource_file.name.capitalize()
        with open(resource_file) as file_input:
            add_file(file_input, name)


def get_lut(name: str) -> LUT:
    return LUTS.get(name, [])


def apply_lut(data: ArrayLike, lut: LUT) -> ArrayLike:
    result = lut[data]
    return result.astype(np.uint8)


if __name__ == "__main__":
    add_luts_at_path("luts/")
    lut = get_lut("Sepia")
    print(lut)
    a = (np.random.rand(10, 10) * 255).astype(np.uint8)
    print(a)
    print(apply_lut(np.array([a]), lut))
