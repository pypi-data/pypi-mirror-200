from importlib.metadata import version, PackageNotFoundError

from primawera.app import create_window


def start():
    create_window()


# Taken from:
# https://www.moritzkoerber.com/posts/versioning-with-setuptools_scm/
try:
    __version__ = version("primawera")
except PackageNotFoundError:
    __version__ = "unknown version"
