import time

from mbot import *

print("[UPLINK] Initiating Drive Thruster Calibration...")
rover = mbot()
print("[STATUS] Telemetry Link: SECURE 🟢")

try:
    # --- PHASE 1: Forward Burn ---
    print("[THRUSTERS] Engaging forward drive (speed 120)...")
    rover.rgb_led(0, 0, 0, 180, 255)
    rover.move(120, 120)
    time.sleep(1.0)

    # --- PHASE 2: Reverse Burn ---
    print("[THRUSTERS] Engaging reverse retro-thrusters (speed -120)...")
    rover.rgb_led(0, 0, 255, 140, 0)
    rover.move(-120, -120)
    time.sleep(1.0)

    # --- PHASE 3: Rotational Pivot Check ---
    print("[THRUSTERS] Executing starboard pivot...")
    rover.rgb_led(0, 1, 0, 255, 0)
    rover.rgb_led(0, 2, 0, 0, 255)
    rover.move(120, -120)
    time.sleep(0.6)

    # --- PHASE 4: All Stop ---
    print("[STATUS] Thruster calibration complete. Parking brake engaged.")
    rover.stop()
    rover.buzzer(523, 200)
    time.sleep(0.25)
    rover.rgb_led(0, 0, 0, 0, 0)

except KeyboardInterrupt:
    print("\n[ABORT] Emergency stop triggered by Flight Control!")
    rover.stop()
    rover.rgb_led(0, 0, 0, 0, 0)
