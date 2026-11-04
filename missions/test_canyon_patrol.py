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

import canyon_patrol

from mbot import mbot


def test_canyon_patrol_reads_sensor_and_parks_safely():
    # --- Digital Twin Line-Follower Check ---
    original_sleep = time.sleep
    time.sleep = lambda _seconds: None
    try:
        rover = mbot(simulate=True)
        rover.set_simulated_sensor("line_follower", 0.0)
        canyon_patrol.run_mission(rover)
    finally:
        time.sleep = original_sleep

    actions = [cmd["action"] for cmd in rover.command_log]
    assert "stop" in actions, "Expected rover.stop() to engage parking brake at end of patrol"
    rover.close()


if __name__ == "__main__":
    print("[PRE-FLIGHT] Validating missions/canyon_patrol.py in Digital Twin Simulator...")
    test_canyon_patrol_reads_sensor_and_parks_safely()
    print("✅ [PASS] Canyon Conduit Navigation pre-flight checks passed!")
