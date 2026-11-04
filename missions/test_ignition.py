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

import ignition

from mbot import mbot


def test_ignition_optical_and_audio_handshake():
    # --- Digital Twin Pre-Flight Check ---
    original_sleep = time.sleep
    time.sleep = lambda _seconds: None
    try:
        rover = mbot(simulate=True)
        ignition.run_mission(rover)
    finally:
        time.sleep = original_sleep

    actions = [cmd["action"] for cmd in rover.command_log]
    assert "rgb_led" in actions, "Expected rover.rgb_led(...) to be called"
    assert "buzzer" in actions, "Expected rover.buzzer(...) to be called"

    # Verify the mission finishes in dark standby (Red=0, Green=0, Blue=0)
    led_commands = [cmd for cmd in rover.command_log if cmd["action"] == "rgb_led"]
    last_led = led_commands[-1]
    assert (last_led["r"], last_led["g"], last_led["b"]) == (0, 0, 0), (
        "Expected final LED command to extinguish LEDs (0, 0, 0) for standby"
    )
    rover.close()


if __name__ == "__main__":
    print("[PRE-FLIGHT] Validating missions/ignition.py in Digital Twin Simulator...")
    test_ignition_optical_and_audio_handshake()
    print("✅ [PASS] Ignition & Telemetry Handshake pre-flight checks passed!")
