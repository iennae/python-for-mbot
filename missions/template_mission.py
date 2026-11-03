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

print("[UPLINK] Initiating handshake with Rover...")
rover = mbot()
print("[STATUS] Telemetry Link: SECURE 🟢")

try:
    # --- Baseline Diagnostic ---
    print("[DIAGNOSTIC] Running baseline systems check...")
    rover.rgb_led(0, 0, 0, 180, 255)
    time.sleep(1.0)

    # --- Field Challenge (TODO) ---
    # Describe the challenge steps in comments here so the learner
    # has a clear starting point in their editor.
    #
    # TODO: Write your mission code here!

    # --- Safe Standby ---
    print("[STATUS] Mission complete. Entering dark standby...")
    rover.stop()
    rover.rgb_led(0, 0, 0, 0, 0)

except KeyboardInterrupt:
    print("\n[ABORT] Manual abort received from Flight Control!")
    rover.stop()
    rover.rgb_led(0, 0, 0, 0, 0)
