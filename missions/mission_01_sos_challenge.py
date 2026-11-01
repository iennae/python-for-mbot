import time

from mbot import *

print("[UPLINK] Initiating S.O.S. Optical & Audio Transponder...")
rover = mbot()
print("[STATUS] Telemetry Link: SECURE 🟢")


def pulse_signal(duration_sec: float, freq_hz: int = 880) -> None:
    """Transmit a single Morse pulse on the onboard RGB LEDs and piezo buzzer."""
    rover.rgb_led(0, 0, 255, 40, 0)
    rover.buzzer(freq_hz, int(duration_sec * 1000))
    time.sleep(duration_sec)
    rover.rgb_led(0, 0, 0, 0, 0)
    time.sleep(0.15)


try:
    # S: three short pulses (. . .)
    print("[BEACON] Transmitting 'S' (. . .)...")
    for _ in range(3):
        pulse_signal(0.2)
    time.sleep(0.3)

    # O: three long pulses (- - -)
    print("[BEACON] Transmitting 'O' (- - -)...")
    for _ in range(3):
        pulse_signal(0.6)
    time.sleep(0.3)

    # S: three short pulses (. . .)
    print("[BEACON] Transmitting 'S' (. . .)...")
    for _ in range(3):
        pulse_signal(0.2)

    print("[STATUS] S.O.S. transmission complete. Entering dark standby...")
    rover.rgb_led(0, 0, 0, 0, 0)

except KeyboardInterrupt:
    print("\n[ABORT] Manual abort received from Flight Control!")
    rover.rgb_led(0, 0, 0, 0, 0)
