import time

from mbot import *

print("[UPLINK] Initiating handshake with Rover...")
rover = mbot()
print("[STATUS] Telemetry Link: SECURE 🟢")

try:
    # --- PHASE 1: Optical Beacon Diagnostic ---
    print("[DIAGNOSTIC] Pulsing optical sensors (Emerald Green)...")
    # Syntax: rgb_led(port, slot, Red, Green, Blue) -> values 0 to 255
    rover.rgb_led(0, 0, 0, 255, 0)
    time.sleep(1.5)  # Hold signal for 1.5 seconds

    # --- PHASE 2: Audio Transponder Check ---
    print("[DIAGNOSTIC] Transmitting 440Hz standard beacon...")
    # Syntax: buzzer(frequency_hz, duration_ms)
    rover.buzzer(440, 300)
    time.sleep(0.5)

    # --- PHASE 3: Standby Mode ---
    print("[STATUS] Diagnostic complete. Entering dark standby...")
    rover.rgb_led(0, 0, 0, 0, 0)  # Extinguish LEDs

except KeyboardInterrupt:
    print("\n[ABORT] Manual abort received from Flight Control!")
    rover.rgb_led(0, 0, 0, 0, 0)
