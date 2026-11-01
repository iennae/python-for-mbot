import time

from mbot import *

print("[UPLINK] Initiating Ultrasonic Radar Sweep (Port 3)...")
rover = mbot()
print("[STATUS] Telemetry Link: SECURE 🟢")

SAFE_DISTANCE_CM = 20.0

try:
    for sweep in range(10):
        distance_cm = rover.get_distance(port=3)
        print(f"[RADAR #{sweep + 1:02d}] Forward range: {distance_cm:.1f} cm")

        if 0 < distance_cm < SAFE_DISTANCE_CM:
            print("  -> [WARNING] Obstacle within safety perimeter! Evading...")
            rover.rgb_led(0, 0, 255, 0, 0)
            rover.buzzer(880, 150)
            rover.move(-100, -100)
            time.sleep(0.4)
            rover.move(100, -100)
            time.sleep(0.3)
            rover.stop()
        else:
            rover.rgb_led(0, 0, 0, 200, 80)
            rover.move(100, 100)
            time.sleep(0.3)

    print("[STATUS] Radar sweep complete. Disengaging drive...")
    rover.stop()
    rover.rgb_led(0, 0, 0, 0, 0)

except KeyboardInterrupt:
    print("\n[ABORT] Emergency stop triggered by Flight Control!")
    rover.stop()
    rover.rgb_led(0, 0, 0, 0, 0)
