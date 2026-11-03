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
    # --- Optical Beacon Diagnostic ---
    print("[DIAGNOSTIC] Pulsing optical sensors (Emerald Green)...")
    # Syntax: rgb_led(port, slot, Red, Green, Blue) -> values 0 to 255
    rover.rgb_led(0, 0, 0, 255, 0)
    time.sleep(1.5)  # Hold signal for 1.5 seconds

    # --- Audio Transponder Check ---
    print("[DIAGNOSTIC] Transmitting 440Hz standard beacon...")
    # Syntax: buzzer(frequency_hz, duration_ms)
    rover.buzzer(440, 300)
    time.sleep(0.5)

    # --- Field Challenge (TODO: Transmit S.O.S. in Morse Code) ---
    # S.O.S. consists of:
    #   S = 3 short pulses (e.g., 0.2 seconds on, 0.2 seconds off)
    #   O = 3 long pulses  (e.g., 0.6 seconds on, 0.2 seconds off)
    #   S = 3 short pulses (e.g., 0.2 seconds on, 0.2 seconds off)
    #
    # TODO: Use rover.rgb_led(...), rover.buzzer(...), and time.sleep(...)
    #       (or a `for _ in range(3):` loop!) to broadcast S.O.S. before standby.

    # --- Standby Mode ---
    print("[STATUS] Diagnostic complete. Entering dark standby...")
    rover.rgb_led(0, 0, 0, 0, 0)  # Extinguish LEDs

except KeyboardInterrupt:
    print("\n[ABORT] Manual abort received from Flight Control!")
    rover.rgb_led(0, 0, 0, 0, 0)
