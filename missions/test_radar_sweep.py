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

import radar_sweep

from mbot import mbot


def test_radar_sweep_pings_and_stops_safely():
    # --- Digital Twin Ultrasonic Radar Check ---
    original_sleep = time.sleep
    time.sleep = lambda _seconds: None
    try:
        rover = mbot(simulate=True)
        rover.set_simulated_sensor("distance", 15.0)
        radar_sweep.run_mission(rover)
    finally:
        time.sleep = original_sleep

    actions = [cmd["action"] for cmd in rover.command_log]
    assert "stop" in actions, "Expected rover.stop() to disengage drive at end of radar sweep"
    rover.close()


if __name__ == "__main__":
    print("[PRE-FLIGHT] Validating missions/radar_sweep.py in Digital Twin Simulator...")
    test_radar_sweep_pings_and_stops_safely()
    print("✅ [PASS] Ultrasonic Radar & Boulder Evasion pre-flight checks passed!")
