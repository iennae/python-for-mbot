import ast
from pathlib import Path

import pytest

import lib
from lib.mBot import mBot, mHID, mSerial

REPO_ROOT = Path(__file__).resolve().parent.parent
PYTHON_FILES = sorted(REPO_ROOT.glob("*.py")) + sorted((REPO_ROOT / "lib").glob("*.py"))


@pytest.mark.parametrize("py_file", PYTHON_FILES, ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_python_files_parse_cleanly(py_file: Path) -> None:
    """Verify every Python file in the repository parses with Python 3 syntax."""
    source = py_file.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(py_file))
    assert tree is not None


def test_public_exports() -> None:
    """Verify core classes can be imported without hardware attached."""
    assert hasattr(lib, "mBot")
    assert mBot is not None
    assert mSerial is not None
    assert mHID is not None
