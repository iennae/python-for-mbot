# 🛰️ Ares VII Rover — Cadet Engineer Python Missions

Welcome to Flight Control! This curriculum guides Cadet Engineers through programming the **Original Makeblock mBot (mCore)** in Python using real-time serial telemetry.

---

## ⚙️ Systems Check & Engineering Tools

Ensure your workstation is primed before executing any mission script:
- **Umbilical Line**: USB Cable connected and secured (or serial port specified via `MBOT_PORT`).
- **Core Power**: mBot switch toggled to `ON`.
- **Translator Module**: `pip install -e .` installed in your virtual environment.
- **Firmware**: Online Firmware (`mbot_firmware.ino`) flashed via Arduino IDE or mBlock.
- **Dry-Run Simulation (No Rover Needed)**: Set `MBOT_SIMULATE=1` in your terminal to test any script without hardware attached!

---

## Mission 01: Ignition & Telemetry Handshake (`mission_01_ignition.py`)

### 🛰️ Mission Briefing
Cadet Engineer, your rover has survived descent and safely touched down in the Ares VII basin. However, the telemetry array is dead, and the primary computer is unresponsive.
Before we ignite the drive thrusters, we must establish a biological heartbeat: test the communication transponder and verify that command packets can be sent from Mission Control (your laptop) to the Rover Core.

### 🎯 Primary Objectives
- **Establish Link**: Establish a high-speed data uplink via the primary umbilical (USB cable).
- **Visual Beacon**: Activate the optical status diodes (RGB LEDs) to verify power distribution.
- **Audio Transponder**: Broadcast a standard confirmation beacon (piezo buzzer).
- **Field Challenge**: Transmit the universal emergency code **S.O.S.** in optical Morse code (see `mission_01_sos_challenge.py`).

### 💻 Telemetry Script: `mission_01_ignition.py`
Copy the following bootstrap code into your ground station editor or run `python missions/mission_01_ignition.py`:

```python
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
```

### 🧠 Flight Engineer Debrief: What Just Happened?

| Code Command | Real-World Translation |
| :--- | :--- |
| `from mbot import *` | Requests the specialized toolset needed to communicate with the rover hardware. |
| `rover = mbot()` | Scans the serial lines to lock onto the rover's communication port. |
| `time.sleep(1.5)` | Halts the computer program temporarily so the physical lights have time to stay visible to human eyes. |
| `rover.rgb_led(0, 0, 0, 255, 0)` | Sends an 8-bit signal to paint the light with `0` Red, `255` Green, `0` Blue (`slot=0` lights both onboard LEDs; `slot=1` or `2` targets a single LED). |
| `rover.buzzer(440, 300)` | Vibrates the piezo speaker at 440 Hz (concert A) for 300 milliseconds. |

---

## Mission 02: Drive Thruster Calibration (`mission_02_thrusters.py`)

### 🛰️ Mission Briefing
With telemetry verified, Flight Control has cleared you to test the twin differential drive motors (`M1` port and `M2` starboard).

### 🎯 Primary Objectives
- Execute a controlled forward burn (`rover.move(120, 120)`).
- Execute a reverse retro-burn (`rover.move(-120, -120)`).
- Perform an in-place rotational pivot (`rover.move(120, -120)`).
- Engage the emergency parking brake (`rover.stop()`).

---

## Mission 03: Solar Array & Night-Vision Beacon (`mission_03_solar_beacon.py`)

### 🛰️ Mission Briefing
Martian dust storms can block sunlight in seconds. Use the rover's onboard photoresistor (`rover.get_light()`) to monitor ambient light and automatically switch on the high-intensity white LEDs when darkness falls.

---

## Mission 04: Ultrasonic Radar & Crater Avoidance (`mission_04_radar_sweep.py`)

### 🛰️ Mission Briefing
Navigate boulder fields using the forward-facing ultrasonic rangefinder (`rover.get_distance(port=3)`). When an obstacle appears within 20 cm, sound a warning tone, flash red, back up, and pivot to safety.

---

## Mission 05: Canyon Floor Line Navigation (`mission_05_canyon_patrol.py`)

### 🛰️ Mission Briefing
Follow the high-contrast thermal conduit along the Ares VII canyon floor using the dual infrared reflective sensor array (`rover.get_line_follower(port=2)`).
