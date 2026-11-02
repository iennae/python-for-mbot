# Copyright 2026 Jennifer Davis
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ast
import runpy
import time
from pathlib import Path

import pytest

import lib
import mbot
from lib.mBot import mBot, mHID, mSerial

REPO_ROOT = Path(__file__).resolve().parent.parent
PYTHON_FILES = (
    sorted((REPO_ROOT / "src" / "mbot").glob("*.py"))
    + sorted((REPO_ROOT / "src" / "lib").glob("*.py"))
    + sorted((REPO_ROOT / "examples").glob("*.py"))
    + sorted((REPO_ROOT / "missions").glob("*.py"))
    + sorted((REPO_ROOT / "scripts").glob("*.py"))
    + sorted((REPO_ROOT / "tests").glob("*.py"))
)


@pytest.mark.parametrize("py_file", PYTHON_FILES, ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_python_files_parse_cleanly(py_file: Path) -> None:
    """Verify every Python file in the repository parses with Python 3 syntax."""
    source = py_file.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(py_file))
    assert tree is not None


def test_public_exports() -> None:
    """Verify core classes can be imported via both `mbot` and legacy `lib.mBot`."""
    assert hasattr(lib, "mBot")
    assert hasattr(mbot, "mbot")
    assert mBot is not None
    assert mSerial is not None
    assert mHID is not None


@pytest.mark.parametrize(
    "mission_script",
    sorted((REPO_ROOT / "missions").glob("mission_*.py")),
    ids=lambda p: p.name,
)
def test_missions_execute_in_simulation_mode(
    mission_script: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verify every Cadet Engineer mission script executes cleanly with MBOT_SIMULATE=1."""
    monkeypatch.setenv("MBOT_SIMULATE", "1")
    monkeypatch.setattr(time, "sleep", lambda _sec: None)
    runpy.run_path(str(mission_script), run_name="__main__")
