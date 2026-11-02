import time

from mbot import *

print("[UPLINK] Initiating Drive Thruster Calibration...")
rover = mbot()
print("[STATUS] Telemetry Link: SECURE 🟢")

try:
    # --- PHASE 1: Forward Thruster Check ---
    # Syntax: rover.move(left_speed, right_speed) -> values -255 to 255
    print("[THRUSTERS] Engaging forward drive (speed 120)...")
    rover.rgb_led(0, 0, 0, 180, 255)
    rover.move(120, 120)
    time.sleep(1.0)
    rover.stop()
    time.sleep(0.5)

    # --- PHASE 2: Field Challenge (TODO: Reverse & Landing Pad Perimeter) ---
    # 1. Engage reverse retro-thrusters using negative speeds: rover.move(-120, -120)
    #    with an amber warning beacon (Red=255, Green=140, Blue=0) for 1.0 second.
    # 2. Execute a starboard (right) pivot by spinning the left wheel forward and
    #    the right wheel backward: rover.move(120, -120) for ~0.6 seconds.
    # 3. Bonus: Use a `for side in range(4):` loop to drive a 4-sided perimeter!
    #
    # TODO: Add your reverse and pivot thruster commands here!

    # --- PHASE 3: Parking Brake & Standby ---
    print("[STATUS] Thruster calibration complete. Parking brake engaged.")
    rover.stop()
    rover.buzzer(523, 200)
    time.sleep(0.25)
    rover.rgb_led(0, 0, 0, 0, 0)

except KeyboardInterrupt:
    print("\n[ABORT] Emergency stop triggered by Flight Control!")
    rover.stop()
    rover.rgb_led(0, 0, 0, 0, 0)
