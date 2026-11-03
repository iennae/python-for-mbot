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

"""Capture headless Chromium screenshots of `site/index.html` for GitHub PR previews."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SITE_INDEX = REPO_ROOT / "site" / "index.html"


def capture_screenshots(output_dir: Path, site_index: Path = SITE_INDEX) -> list[dict[str, str]]:
    """Render `site/index.html` in headless Chromium and save preview screenshots."""
    from playwright.sync_api import sync_playwright

    if not site_index.is_file():
        raise FileNotFoundError(f"Site entry point not found: {site_index}")

    output_dir.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    manifest: list[dict[str, str]] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))
        page.on(
            "console",
            lambda msg: (
                errors.append(f"console.error: {msg.text}") if msg.type == "error" else None
            ),
        )

        page.goto(site_index.resolve().as_uri(), wait_until="networkidle")
        page.wait_for_selector("#mission-stage-container .card")

        # 1. Mission 00: Launchpad Readiness
        shot_01 = "01-mission-00-launchpad.png"
        page.screenshot(path=str(output_dir / shot_01), full_page=True)
        manifest.append(
            {
                "filename": shot_01,
                "title": "Mission 00: Launchpad Readiness (Default Landing View)",
            }
        )

        # 2. Mission 01: Ignition & Telemetry (with Hint #1 expanded)
        page.click("#nav-btn-mission-01")
        page.wait_for_selector("#starter-code-pre")
        hint_summary = page.locator("#hint-mission-01-0 > summary")
        if hint_summary.count() > 0:
            hint_summary.click()
        shot_02 = "02-mission-01-ignition.png"
        page.screenshot(path=str(output_dir / shot_02), full_page=True)
        manifest.append(
            {
                "filename": shot_02,
                "title": "Mission 01: Ignition & Telemetry (Starter Template & Hints)",
            }
        )

        # 3. How to Add a Mission Modal
        page.evaluate("window.scrollTo(0, 0)")
        page.click("#open-add-mission-modal-btn")
        page.wait_for_selector("#add-mission-modal:not([hidden])")
        shot_03 = "03-add-mission-modal.png"
        page.screenshot(path=str(output_dir / shot_03), full_page=False)
        manifest.append(
            {
                "filename": shot_03,
                "title": "How to Add a New Mission Modal",
            }
        )

        browser.close()

    if errors:
        for err in errors:
            print(f"[ERROR] {err}", file=sys.stderr)
        raise RuntimeError(
            f"Detected {len(errors)} browser error(s) while rendering site/index.html"
        )

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Capture Mission Control site preview screenshots."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("screenshots"),
        help="Directory to write PNG screenshots and manifest.json",
    )
    args = parser.parse_args()
    captured = capture_screenshots(args.output_dir)
    print(f"[PREVIEW] Captured {len(captured)} screenshots in {args.output_dir}")


if __name__ == "__main__":
    main()
