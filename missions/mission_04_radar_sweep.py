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

from mbot import *

print("[UPLINK] Initiating Ultrasonic Radar Sweep (Port 3)...")
rover = mbot()
print("[STATUS] Telemetry Link: SECURE 🟢")

SAFE_DISTANCE_CM = 20.0
CAUTION_DISTANCE_CM = 40.0

try:
    # --- Single Rangefinder Ping ---
    distance_cm = rover.get_distance(port=3)
    print(f"[RADAR] Initial forward range: {distance_cm:.1f} cm")

    # --- Field Challenge (TODO: Proximity Alert & Evasion) ---
    # Poll `rover.get_distance(port=3)` in a loop (e.g., `for sweep in range(10):`):
    #   - DANGER (`0 < distance_cm < SAFE_DISTANCE_CM`):
    #       Flash Red (`255, 0, 0`), sound an 880 Hz alarm, reverse `rover.move(-100, -100)`
    #       for 0.4s, pivot `rover.move(100, -100)` for 0.3s, and `rover.stop()`.
    #   - CAUTION (`SAFE_DISTANCE_CM <= distance_cm < CAUTION_DISTANCE_CM`):
    #       Set LEDs to Amber (`255, 140, 0`) and creep slowly `rover.move(60, 60)`.
    #   - CLEAR (`distance_cm >= CAUTION_DISTANCE_CM`):
    #       Set LEDs to Emerald (`0, 200, 80`) and cruise `rover.move(100, 100)`.
    #
    # TODO: Implement your radar sweep loop below!

    # --- Disengage Drive ---
    print("[STATUS] Radar sweep complete. Disengaging drive...")
    rover.stop()
    rover.rgb_led(0, 0, 0, 0, 0)

except KeyboardInterrupt:
    print("\n[ABORT] Emergency stop triggered by Flight Control!")
    rover.stop()
    rover.rgb_led(0, 0, 0, 0, 0)
