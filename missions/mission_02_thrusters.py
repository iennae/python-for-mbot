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

print("[UPLINK] Initiating Drive Thruster Calibration...")
rover = mbot()
print("[STATUS] Telemetry Link: SECURE 🟢")

try:
    # --- Forward Thruster Check ---
    # Syntax: rover.move(left_speed, right_speed) -> values -255 to 255
    print("[THRUSTERS] Engaging forward drive (speed 120)...")
    rover.rgb_led(0, 0, 0, 180, 255)
    rover.move(120, 120)
    time.sleep(1.0)
    rover.stop()
    time.sleep(0.5)

    # --- Field Challenge (TODO: Reverse & Landing Pad Perimeter) ---
    # - Engage reverse retro-thrusters using negative speeds: rover.move(-120, -120)
    #   with an amber warning beacon (Red=255, Green=140, Blue=0) for 1.0 second.
    # - Execute a starboard (right) pivot by spinning the left wheel forward and
    #   the right wheel backward: rover.move(120, -120) for ~0.6 seconds.
    # - Bonus: Use a `for side in range(4):` loop to drive a 4-sided perimeter!
    #
    # TODO: Add your reverse and pivot thruster commands here!

    # --- Parking Brake & Standby ---
    print("[STATUS] Thruster calibration complete. Parking brake engaged.")
    rover.stop()
    rover.buzzer(523, 200)
    time.sleep(0.25)
    rover.rgb_led(0, 0, 0, 0, 0)

except KeyboardInterrupt:
    print("\n[ABORT] Emergency stop triggered by Flight Control!")
    rover.stop()
    rover.rgb_led(0, 0, 0, 0, 0)
