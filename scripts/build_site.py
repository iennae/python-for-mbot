#!/usr/bin/env python3
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

"""Build `site/missions_data.js` from `missions/missions.json` and associated mission files.

Uses only the Python standard library so it can be run offline from a terminal or directly
inside Thonny by pressing Run (F5).
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MISSIONS_DIR = REPO_ROOT / "missions"
MANIFEST_JSON = MISSIONS_DIR / "missions.json"
SITE_DIR = REPO_ROOT / "site"
OUTPUT_JS = SITE_DIR / "missions_data.js"


def _parse_bullets(section_text: str) -> list[str]:
    """Parse top-level markdown bullet items from a section, preserving multiline bullets."""
    items: list[str] = []
    for raw_line in section_text.strip().splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line.startswith("- "):
            items.append(line[2:].strip())
        elif items and (line.startswith("  ") or line.startswith("\t")):
            items[-1] += "\n" + line.strip()
    return items


def _parse_debrief_table(section_text: str) -> list[dict[str, str]]:
    """Parse a 2-column Markdown table under `## Flight Engineer Debrief`."""
    rows: list[dict[str, str]] = []
    for raw_line in section_text.strip().splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        if cells[0].startswith(":-") or cells[0].startswith("--"):
            continue
        if cells[0].lower() in {"code command", "component"}:
            continue
        cmd = cells[0]
        if cmd.startswith("`") and cmd.endswith("`") and len(cmd) >= 2:
            cmd = cmd[1:-1]
        rows.append({"command": cmd, "translation": cells[1]})
    return rows


def _strip_license_header(code_text: str) -> str:
    """Strip leading Apache 2.0 `# Copyright ...` boilerplate so the web UI displays clean code."""
    lines = code_text.splitlines()
    if not lines or not lines[0].startswith("# Copyright "):
        return code_text
    idx = 0
    while idx < len(lines) and lines[idx].startswith("#"):
        idx += 1
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    return "\n".join(lines[idx:]) + "\n"


def _parse_story_sections(md_path: Path) -> tuple[str, dict[str, str]]:
    """Parse heading and `## ` sections from a mission story Markdown file."""
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError(f"{md_path}: First line must be a '# ...' heading")

    heading_title = lines[0][2:].strip()
    sections: dict[str, str] = {}
    current_heading = "_meta"
    buffer: list[str] = []

    for line in lines[1:]:
        if line.startswith("## "):
            sections[current_heading] = "\n".join(buffer).strip()
            current_heading = line[3:].strip()
            buffer = []
        else:
            buffer.append(line)
    sections[current_heading] = "\n".join(buffer).strip()
    return heading_title, sections


def parse_mission_entry(
    entry: dict[str, object], index: int, missions_dir: Path = MISSIONS_DIR
) -> dict[str, object]:
    """Build a mission record from a `missions/missions.json` entry and its associated files."""
    number = f"{index:02d}"
    mission_id = str(entry.get("id") or f"mission-{number}")
    files = entry.get("files")
    if not isinstance(files, dict) or not files.get("story"):
        raise ValueError(f"Mission '{mission_id}' must define files.story in missions.json")

    story_name = str(files["story"])
    story_path = missions_dir / story_name
    if not story_path.is_file():
        raise FileNotFoundError(f"Mission '{mission_id}': story file '{story_name}' not found")

    heading_title, sections = _parse_story_sections(story_path)
    title = str(entry.get("title") or heading_title)
    full_title = f"Mission {number}: {title}"

    starter_raw = files.get("starter")
    starter_name = str(starter_raw) if starter_raw else None
    starter_code = None
    if starter_name:
        starter_path = missions_dir / starter_name
        if not starter_path.is_file():
            raise FileNotFoundError(
                f"Mission '{mission_id}': starter file '{starter_name}' not found"
            )
        starter_code = _strip_license_header(starter_path.read_text(encoding="utf-8"))

    test_raw = files.get("test")
    test_name = str(test_raw) if test_raw else None
    test_code = None
    if test_name:
        test_path = missions_dir / test_name
        if not test_path.is_file():
            raise FileNotFoundError(f"Mission '{mission_id}': test file '{test_name}' not found")
        test_code = _strip_license_header(test_path.read_text(encoding="utf-8"))

    return {
        "id": f"mission-{number}",
        "slug": mission_id,
        "number": number,
        "title": title,
        "fullTitle": full_title,
        "badge": str(entry.get("badge", "Rover Mission")),
        "files": {
            "story": f"missions/{story_name}",
            "starter": f"missions/{starter_name}" if starter_name else None,
            "test": f"missions/{test_name}" if test_name else None,
        },
        "scriptName": starter_name,
        "scriptPath": f"missions/{starter_name}" if starter_name else None,
        "testName": test_name,
        "testPath": f"missions/{test_name}" if test_name else None,
        "requiresBattery": bool(entry.get("requires_battery", False)),
        "story": sections.get("Story Briefing", ""),
        "objectives": _parse_bullets(sections.get("Primary Objectives", "")),
        "systemsCheck": _parse_bullets(sections.get("Systems Check", "")),
        "challenge": sections.get("Field Challenge", ""),
        "hints": _parse_bullets(sections.get("Progressive Hints", "")),
        "successMetrics": _parse_bullets(sections.get("Mission Success Metrics", "")),
        "debrief": _parse_debrief_table(sections.get("Flight Engineer Debrief", "")),
        "starterCode": starter_code,
        "testCode": traveled_code if (traveled_code := test_code) else None,
    }


def load_all_missions(missions_dir: Path = MISSIONS_DIR) -> list[dict[str, object]]:
    """Load all missions in the order defined by `missions/missions.json`."""
    manifest_path = missions_dir / "missions.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Mission manifest not found: {manifest_path}")
    entries = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise ValueError(f"{manifest_path}: Expected a top-level JSON array of mission objects")
    return [
        parse_mission_entry(entry, idx, missions_dir=missions_dir)
        for idx, entry in enumerate(entries)
    ]


def build_site_data(output_path: Path = OUTPUT_JS) -> list[dict[str, object]]:
    """Compile all missions into `site/missions_data.js` for offline (`file://`) and web use."""
    missions = load_all_missions()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(missions, indent=2, ensure_ascii=False)
    content = (
        "/*\n"
        " * Copyright 2026 Jennifer Davis\n"
        " *\n"
        ' * Licensed under the Apache License, Version 2.0 (the "License");\n'
        " * you may not use this file except in compliance with the License.\n"
        " * You may obtain a copy of the License at\n"
        " *\n"
        " *     http://www.apache.org/licenses/LICENSE-2.0\n"
        " *\n"
        " * Unless required by applicable law or agreed to in writing, software\n"
        ' * distributed under the License is distributed on an "AS IS" BASIS,\n'
        " * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n"
        " * See the License for the specific language governing permissions and\n"
        " * limitations under the License.\n"
        " */\n\n"
        "// Auto-generated by scripts/build_site.py from missions/missions.json\n"
        "// Do not edit directly; edit files in missions/ and run: python scripts/build_site.py\n"
        f"window.MISSIONS_DATA = {payload};\n"
    )
    output_path.write_text(content, encoding="utf-8")
    return missions


if __name__ == "__main__":
    compiled = build_site_data()
    print(f"[BUILD] Wrote {len(compiled)} missions to {OUTPUT_JS.relative_to(REPO_ROOT)}")
