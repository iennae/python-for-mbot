#!/usr/bin/env python3
"""Build `site/missions_data.js` from Markdown briefings and starter `.py` scripts in `missions/`.

Uses only the Python standard library so it can be run offline from a terminal or directly
inside Thonny by pressing Run (F5).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MISSIONS_DIR = REPO_ROOT / "missions"
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
        # Skip header and alignment separator rows
        if cells[0].startswith(":-") or cells[0].startswith("--"):
            continue
        if cells[0].lower() in {"code command", "component"}:
            continue
        cmd = cells[0]
        if cmd.startswith("`") and cmd.endswith("`") and len(cmd) >= 2:
            cmd = cmd[1:-1]
        rows.append({"command": cmd, "translation": cells[1]})
    return rows


def parse_mission_file(md_path: Path) -> dict[str, object]:
    """Parse a numbered `missions/XX_*.md` file and attach its starter `.py` code."""
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or not lines[0].startswith("# "):
        raise ValueError(f"{md_path}: First line must be a '# Mission XX: ...' heading")

    full_title = lines[0][2:].strip()
    match = re.match(r"^Mission\s+(\d+)\s*:\s*(.+)$", full_title, re.IGNORECASE)
    if match:
        number = match.group(1)
        title = match.group(2).strip()
    else:
        number = md_path.name.split("_", 1)[0]
        title = full_title

    # Split by `## ` headings
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

    # Parse metadata bullets in `_meta`
    meta: dict[str, str] = {}
    for item in _parse_bullets(sections.get("_meta", "")):
        meta_match = re.match(r"^\*\*(.+?)\*\*\s*:\s*(.+)$", item)
        if meta_match:
            meta[meta_match.group(1).strip().lower()] = meta_match.group(2).strip()

    script_raw = meta.get("script", "None")
    script_name = None if script_raw.lower() == "none" else script_raw
    starter_code = None
    if script_name:
        script_path = MISSIONS_DIR / script_name
        if not script_path.is_file():
            raise FileNotFoundError(f"{md_path}: Referenced script '{script_name}' not found")
        starter_code = script_path.read_text(encoding="utf-8")

    requires_battery = meta.get("requires battery", "false").lower() == "true"

    return {
        "id": f"mission-{number}",
        "number": number,
        "title": title,
        "fullTitle": full_title,
        "badge": meta.get("badge", "Rover Mission"),
        "scriptName": script_name,
        "scriptPath": f"missions/{script_name}" if script_name else None,
        "requiresBattery": requires_battery,
        "story": sections.get("Story Briefing", ""),
        "objectives": _parse_bullets(sections.get("Primary Objectives", "")),
        "systemsCheck": _parse_bullets(sections.get("Systems Check", "")),
        "challenge": sections.get("Field Challenge", ""),
        "hints": _parse_bullets(sections.get("Progressive Hints", "")),
        "successMetrics": _parse_bullets(sections.get("Mission Success Metrics", "")),
        "debrief": _parse_debrief_table(sections.get("Flight Engineer Debrief", "")),
        "starterCode": starter_code,
    }


def load_all_missions(missions_dir: Path = MISSIONS_DIR) -> list[dict[str, object]]:
    """Discover and parse all `XX_*.md` files in `missions/` in numeric order."""
    md_files = sorted(path for path in missions_dir.glob("[0-9][0-9]_*.md") if path.is_file())
    return [parse_mission_file(md_file) for md_file in md_files]


def build_site_data(output_path: Path = OUTPUT_JS) -> list[dict[str, object]]:
    """Compile all missions into `site/missions_data.js` for offline (`file://`) and web use."""
    missions = load_all_missions()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(missions, indent=2, ensure_ascii=False)
    content = (
        "// Auto-generated by scripts/build_site.py from missions/*.md and missions/*.py\n"
        "// Do not edit directly; edit files in missions/ and run: python scripts/build_site.py\n"
        f"window.MISSIONS_DATA = {payload};\n"
    )
    output_path.write_text(content, encoding="utf-8")
    return missions


if __name__ == "__main__":
    compiled = build_site_data()
    print(f"[BUILD] Wrote {len(compiled)} missions to {OUTPUT_JS.relative_to(REPO_ROOT)}")
