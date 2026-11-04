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

import thrusters

from mbot import mbot


def test_thrusters_engage_and_park_safely():
    # --- Digital Twin Thruster Safety Check ---
    original_sleep = time.sleep
    time.sleep = lambda _seconds: None
    try:
        rover = mbot(simulate=True)
        thrusters.run_mission(rover)
    finally:
        time.sleep = original_sleep

    move_cmds = [cmd for cmd in rover.command_log if cmd["action"] == "move"]
    assert move_cmds, "Expected rover.move(...) to be called during thruster calibration"

    # Safety rule: final motor command must halt both wheels (left=0, right=0)
    last_move = move_cmds[-1]
    assert (last_move["left"], last_move["right"]) == (0, 0), (
        "Safety Check Failed: rover must finish with rover.stop() so wheels do not keep spinning!"
    )
    rover.close()


if __name__ == "__main__":
    print("[PRE-FLIGHT] Validating missions/thrusters.py in Digital Twin Simulator...")
    test_thrusters_engage_and_park_safely()
    print("✅ [PASS] Drive Thruster Calibration pre-flight safety checks passed!")
