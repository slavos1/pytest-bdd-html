"""pytest setup code"""
from enum import Enum, auto, unique
from pathlib import Path

import pytest

from .faker import faker  # pylint:disable=unused-import
from .stylesheet import Stylesheet

pytest_plugins = ["pytester"]


@unique
class CssForTesting(Enum):
    """All possibilities for --bdd-html-css option"""

    DEFAULT = auto()
    CUSTOM = auto()
    NONE = auto()


@pytest.fixture(params=list(CssForTesting))
def stylesheet(request, tmp_path: Path) -> Stylesheet:
    """Return CSS stylesheet for --bdd-html-css"""
    flag = request.param
    if flag == CssForTesting.DEFAULT:
        # return non-existent path so that the default CSS is used
        return Stylesheet(tmp_path.joinpath("non-existent.css"))
    if flag == CssForTesting.CUSTOM:
        return Stylesheet(tmp_path.joinpath("custom.css")).write()
    return Stylesheet()
