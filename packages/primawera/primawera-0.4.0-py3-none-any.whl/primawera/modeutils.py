from typing import Optional

BOOL_ALIASES = {"1", "BOOL"}
GRAYSCALE_ALIASES = {"GRAY", "GRAYSCALE", "GREY", "GREYSCALE", "I;16", "I;16B"}
COLOR_ALIASES = {"RGB", "COLOR", "COLOUR"}
FLOATING_ALIASES = {"F", "FLOATING", "FLOAT"}
COMPLEX_ALIASES = {"C", "COMPLEX"}
RECOGNIZED_MODES = {None}.union(BOOL_ALIASES, GRAYSCALE_ALIASES, COLOR_ALIASES,
                                FLOATING_ALIASES, COMPLEX_ALIASES)

HUMAN_NAMES = [(BOOL_ALIASES, "Bool"), (GRAYSCALE_ALIASES, "Grayscale"),
               (COLOR_ALIASES, "Color"), (FLOATING_ALIASES, "Floating"),
               (COMPLEX_ALIASES, "Complex")]


def is_mode_grayscale(mode: str) -> bool:
    return mode.upper() in GRAYSCALE_ALIASES


def is_mode_color(mode: str) -> bool:
    return mode.upper() in COLOR_ALIASES


def translate_mode(mode: str) -> Optional[str]:
    if mode.upper() not in RECOGNIZED_MODES:
        return None
    if mode.upper() in BOOL_ALIASES:
        return "1"
    elif mode.upper() in GRAYSCALE_ALIASES:
        return "grayscale"
    elif mode.upper() in COLOR_ALIASES:
        return "rgb"
    elif mode.upper() in FLOATING_ALIASES:
        return "F"
    elif mode.upper() in COMPLEX_ALIASES:
        return "C"
    return None


def print_mode(mode: str) -> Optional[str]:
    for name_set, human_name in HUMAN_NAMES:
        if mode.upper() in name_set:
            return human_name
    return None
