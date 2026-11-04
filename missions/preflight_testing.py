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

from mbot import *

MIN_SAFE_VOLTAGE = 6.0


def evaluate_battery_safety(rover, voltage):
    # --- Healthy Battery Check ---
    if voltage >= MIN_SAFE_VOLTAGE:
        rover.rgb_led(0, 0, 0, 255, 0)
        return "NOMINAL"

    # --- Field Challenge (TODO: Low-Voltage Emergency Cutoff) ---
    # When voltage drops below MIN_SAFE_VOLTAGE:
    #   - Call rover.stop() so the drive motors halt immediately
    #   - Set the onboard LEDs to Red: rover.rgb_led(0, 0, 255, 0, 0)
    #   - Return "CRITICAL_LOW"
    #
    # TODO: Add rover.stop() and rover.rgb_led(0, 0, 255, 0, 0) below!
    rover.stop()
    rover.rgb_led(0, 0, 255, 0, 0)
    return "CRITICAL_LOW"


def run_mission(rover):
    print("[SIMULATOR] Running Digital Twin battery safety check...")
    healthy_status = evaluate_battery_safety(rover, 7.4)
    print(f"[TELEMETRY] 7.4V status: {healthy_status}")
    low_status = evaluate_battery_safety(rover, 5.4)
    print(f"[TELEMETRY] 5.4V status: {low_status}")
    print(f"[COMMAND LOG] Recorded {len(rover.command_log)} commands: {rover.command_log}")


if __name__ == "__main__":
    rover = mbot(simulate=True)
    run_mission(rover)
