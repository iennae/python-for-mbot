import time

from mbot import *

print("[UPLINK] Initiating Ultrasonic Radar Sweep (Port 3)...")
rover = mbot()
print("[STATUS] Telemetry Link: SECURE 🟢")

SAFE_DISTANCE_CM = 20.0
CAUTION_DISTANCE_CM = 40.0

try:
    # --- PHASE 1: Single Rangefinder Ping ---
    distance_cm = rover.get_distance(port=3)
    print(f"[RADAR] Initial forward range: {distance_cm:.1f} cm")

    # --- PHASE 2: Field Challenge (TODO: 3-Zone Proximity Alert & Evasion) ---
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

    # --- PHASE 3: Disengage Drive ---
    print("[STATUS] Radar sweep complete. Disengaging drive...")
    rover.stop()
    rover.rgb_led(0, 0, 0, 0, 0)

except KeyboardInterrupt:
    print("\n[ABORT] Emergency stop triggered by Flight Control!")
    rover.stop()
    rover.rgb_led(0, 0, 0, 0, 0)
