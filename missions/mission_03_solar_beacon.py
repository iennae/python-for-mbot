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

print("[UPLINK] Initiating Solar Array & Dusk Protocol...")
rover = mbot()
print("[STATUS] Telemetry Link: SECURE 🟢")

NIGHT_THRESHOLD = 300.0

try:
    # --- PHASE 1: Single Solar Flux Reading ---
    lux = rover.get_light()
    print(f"[TELEMETRY] Initial Ambient Solar Flux: {lux:.1f}")

    # --- PHASE 2: Field Challenge (TODO: Automatic Dusk Headlights Loop) ---
    # Poll the onboard light sensor in a loop (e.g., `for sample in range(10):`):
    #   1. Read `lux = rover.get_light()` and print the reading.
    #   2. If `lux < NIGHT_THRESHOLD`:
    #        - Activate high-beam white headlights: rover.rgb_led(0, 0, 255, 255, 255)
    #        - Optional: chirp a brief alert tone with rover.buzzer(660, 100)
    #   3. Else:
    #        - Keep the low-power green status beacon on: rover.rgb_led(0, 0, 0, 60, 0)
    #   4. Pause `time.sleep(0.5)` between samples.
    #
    # TODO: Write your solar monitoring loop below!

    # --- PHASE 3: Standby Mode ---
    print("[STATUS] Solar check complete. Entering dark standby...")
    rover.rgb_led(0, 0, 0, 0, 0)

except KeyboardInterrupt:
    print("\n[ABORT] Manual abort received from Flight Control!")
    rover.rgb_led(0, 0, 0, 0, 0)
