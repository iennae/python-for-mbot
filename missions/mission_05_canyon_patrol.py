import time

from mbot import *

print("[UPLINK] Initiating Canyon Conduit Line Patrol (Port 2)...")
rover = mbot()
print("[STATUS] Telemetry Link: SECURE 🟢")

# Line follower sensor states (Port 2):
#   0 = Both sensors on dark track (Dead Ahead)
#   1 = Left sensor on track, right off (Drifting Right -> Correct Left)
#   2 = Left sensor off, right on track (Drifting Left  -> Correct Right)
#   3 = Both sensors off dark track (Track Lost -> Reverse / Search)

try:
    # --- PHASE 1: Single Sensor Readout ---
    state = int(rover.get_line_follower(port=2))
    print(f"[PATROL] Initial Line Follower State (0..3): {state}")

    # --- PHASE 2: Field Challenge (TODO: Autonomous Line-Following Loop) ---
    # In a loop (`for step in range(20):`), read `state = int(rover.get_line_follower(port=2))`
    # and steer the rover based on `state`:
    #   - If `state == 0`: Both LEDs Green, drive straight `rover.move(100, 100)`
    #   - If `state == 1`: Left LED Green (`slot=1`), steer left `rover.move(40, 110)`
    #   - If `state == 2`: Right LED Green (`slot=2`), steer right `rover.move(110, 40)`
    #   - Else (`state == 3`): Both LEDs Amber, reverse slowly `rover.move(-80, -80)`
    # Pause `time.sleep(0.2)` at the end of each step.
    #
    # TODO: Implement your canyon navigation loop below!

    # --- PHASE 3: Parking Brake ---
    print("[STATUS] Canyon patrol complete. Engaging parking brake...")
    rover.stop()
    rover.rgb_led(0, 0, 0, 0, 0)

except KeyboardInterrupt:
    print("\n[ABORT] Emergency stop triggered by Flight Control!")
    rover.stop()
    rover.rgb_led(0, 0, 0, 0, 0)
