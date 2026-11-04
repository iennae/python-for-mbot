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

import preflight_testing

from mbot import mbot


def test_healthy_battery_lights_green_beacon():
    # --- Healthy Voltage Unit Test ---
    rover = mbot(simulate=True)
    status = preflight_testing.evaluate_battery_safety(rover, 7.4)

    assert status == "NOMINAL"
    assert len(rover.command_log) == 1
    assert rover.command_log[0]["action"] == "rgb_led"
    assert rover.command_log[0]["g"] == 255
    rover.close()


def test_low_battery_triggers_emergency_stop():
    # --- Low Voltage Emergency Cutoff Unit Test ---
    rover = mbot(simulate=True)
    status = preflight_testing.evaluate_battery_safety(rover, 5.4)

    assert status == "CRITICAL_LOW"
    actions = [cmd["action"] for cmd in rover.command_log]
    assert "stop" in actions, "Expected rover.stop() when voltage is critically low"

    led_commands = [cmd for cmd in rover.command_log if cmd["action"] == "rgb_led"]
    assert led_commands, "Expected a Red warning LED command when voltage is critically low"
    assert led_commands[-1]["r"] == 255
    rover.close()


if __name__ == "__main__":
    print("[PRE-FLIGHT] Running Digital Twin unit tests for preflight_testing.py...")
    test_healthy_battery_lights_green_beacon()
    print("✅ [PASS] test_healthy_battery_lights_green_beacon")
    test_low_battery_triggers_emergency_stop()
    print("✅ [PASS] test_low_battery_triggers_emergency_stop")
    print("🟢 All Digital Twin unit tests passed!")
