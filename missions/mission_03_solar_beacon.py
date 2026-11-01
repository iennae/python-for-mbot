import time

from mbot import *

print("[UPLINK] Initiating Solar Array & Night-Vision Diagnostic...")
rover = mbot()
print("[STATUS] Telemetry Link: SECURE 🟢")

NIGHT_THRESHOLD = 300.0

try:
    for sample in range(10):
        lux = rover.get_light()
        print(f"[TELEMETRY #{sample + 1:02d}] Ambient Solar Flux: {lux:.1f}")

        if lux < NIGHT_THRESHOLD:
            print("  -> [ALERT] Low light detected! Activating high-beam LEDs.")
            rover.rgb_led(0, 0, 255, 255, 255)
        else:
            print("  -> [NOMINAL] Daylight nominal. Running low-power indicator.")
            rover.rgb_led(0, 0, 0, 60, 0)

        time.sleep(0.5)

    print("[STATUS] Solar sweep complete. Entering dark standby...")
    rover.rgb_led(0, 0, 0, 0, 0)

except KeyboardInterrupt:
    print("\n[ABORT] Manual abort received from Flight Control!")
    rover.rgb_led(0, 0, 0, 0, 0)
