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

from pathlib import Path

from scripts.build_site import OUTPUT_JS, build_site_data, load_all_missions

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_missions_load_with_complete_sections() -> None:
    """Verify all numbered missions (00..05) contain required sections and starter templates."""
    missions = load_all_missions()
    assert len(missions) >= 6
    numbers = [m["number"] for m in missions]
    assert numbers[:6] == ["00", "01", "02", "03", "04", "05"]

    for mission in missions:
        assert mission["title"]
        assert mission["story"]
        assert len(mission["objectives"]) >= 2
        assert len(mission["systemsCheck"]) >= 1
        assert mission["challenge"]
        assert len(mission["hints"]) >= 2
        assert len(mission["successMetrics"]) >= 3
        assert len(mission["debrief"]) >= 2
        if mission["number"] != "00":
            assert mission["starterCode"] is not None
            assert "TODO" in mission["starterCode"]


def test_site_missions_data_js_is_in_sync(tmp_path: Path) -> None:
    """Verify `site/missions_data.js` matches the output of `scripts/build_site.py`."""
    generated_file = tmp_path / "missions_data.js"
    build_site_data(output_path=generated_file)
    assert OUTPUT_JS.is_file(), "site/missions_data.js does not exist"
    assert OUTPUT_JS.read_text(encoding="utf-8") == generated_file.read_text(encoding="utf-8")
