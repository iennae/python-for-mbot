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

import time

import template_mission

from mbot import mbot


def test_template_mission_runs_and_stops_safely():
    # --- Digital Twin Template Check ---
    original_sleep = time.sleep
    time.sleep = lambda _seconds: None
    try:
        rover = mbot(simulate=True)
        template_mission.run_mission(rover)
    finally:
        time.sleep = original_sleep

    actions = [cmd["action"] for cmd in rover.command_log]
    assert "stop" in actions, "Expected rover.stop() at standby"
    rover.close()


if __name__ == "__main__":
    print("[PRE-FLIGHT] Validating missions/template_mission.py in Digital Twin Simulator...")
    test_template_mission_runs_and_stops_safely()
    print("✅ [PASS] Template mission pre-flight checks passed!")
