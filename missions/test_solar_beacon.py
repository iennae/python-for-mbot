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

import solar_beacon

from mbot import mbot


def test_solar_beacon_polls_light_and_enters_standby():
    # --- Digital Twin Solar Sensor Check ---
    original_sleep = time.sleep
    time.sleep = lambda _seconds: None
    try:
        rover = mbot(simulate=True)
        rover.set_simulated_sensor("light", 120.0)
        solar_beacon.run_mission(rover)
    finally:
        time.sleep = original_sleep

    led_cmds = [cmd for cmd in rover.command_log if cmd["action"] == "rgb_led"]
    assert led_cmds, "Expected rover.rgb_led(...) to be called during solar beacon mission"
    last_led = led_cmds[-1]
    assert (last_led["r"], last_led["g"], last_led["b"]) == (0, 0, 0), (
        "Expected final LED command to extinguish LEDs (0, 0, 0) at standby"
    )
    rover.close()


if __name__ == "__main__":
    print("[PRE-FLIGHT] Validating missions/solar_beacon.py in Digital Twin Simulator...")
    test_solar_beacon_polls_light_and_enters_standby()
    print("✅ [PASS] Solar Array & Dusk Protocol pre-flight checks passed!")
