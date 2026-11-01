import time

from mbot import *

print("[UPLINK] Initiating Canyon Floor Line Patrol (Port 2)...")
rover = mbot()
print("[STATUS] Telemetry Link: SECURE 🟢")

# Line follower sensor states (Port 2):
#   0 = Both sensors on dark track (Dead Ahead)
#   1 = Left sensor on track, right off (Veering Right -> Turn Left)
#   2 = Left sensor off, right on track (Veering Left  -> Turn Right)
#   3 = Both sensors off dark track (Track Lost -> Search/Backup)

try:
    for step in range(15):
        state = int(rover.get_line_follower(port=2))
        if state == 0:
            print(f"[PATROL #{step + 1:02d}] State 0: On track -> Full ahead")
            rover.rgb_led(0, 0, 0, 255, 0)
            rover.move(100, 100)
        elif state == 1:
            print(f"[PATROL #{step + 1:02d}] State 1: Drift right -> Correcting left")
            rover.rgb_led(0, 1, 0, 255, 0)
            rover.rgb_led(0, 2, 0, 0, 0)
            rover.move(40, 110)
        elif state == 2:
            print(f"[PATROL #{step + 1:02d}] State 2: Drift left -> Correcting right")
            rover.rgb_led(0, 1, 0, 0, 0)
            rover.rgb_led(0, 2, 0, 255, 0)
            rover.move(110, 40)
        else:
            print(f"[PATROL #{step + 1:02d}] State 3: Off track -> Reversing slowly")
            rover.rgb_led(0, 0, 255, 80, 0)
            rover.move(-80, -80)

        time.sleep(0.25)

    print("[STATUS] Canyon patrol complete. Engaging parking brake...")
    rover.stop()
    rover.rgb_led(0, 0, 0, 0, 0)

except KeyboardInterrupt:
    print("\n[ABORT] Emergency stop triggered by Flight Control!")
    rover.stop()
    rover.rgb_led(0, 0, 0, 0, 0)
