import time

from mbot import *

print("[UPLINK] Initiating handshake with Rover...")
rover = mbot()
print("[STATUS] Telemetry Link: SECURE 🟢")

try:
    # --- PHASE 1: Baseline Diagnostic ---
    print("[DIAGNOSTIC] Running baseline systems check...")
    rover.rgb_led(0, 0, 0, 180, 255)
    time.sleep(1.0)

    # --- PHASE 2: Field Challenge (TODO) ---
    # Describe the challenge steps in comments here so the learner
    # has a clear starting point in their editor.
    #
    # TODO: Write your mission code here!

    # --- PHASE 3: Safe Standby ---
    print("[STATUS] Mission complete. Entering dark standby...")
    rover.stop()
    rover.rgb_led(0, 0, 0, 0, 0)

except KeyboardInterrupt:
    print("\n[ABORT] Manual abort received from Flight Control!")
    rover.stop()
    rover.rgb_led(0, 0, 0, 0, 0)
