# Mission 01: Ignition & Telemetry Handshake

- **Badge**: Optical & Audio Transponder
- **Script**: mission_01_ignition.py
- **Requires Battery**: false

## Story Briefing
Cadet Engineer, your rover has survived descent and safely touched down in the Ares VII basin. However, the telemetry array is dead, and the primary computer is unresponsive. Before we ignite the drive thrusters, we must establish a biological heartbeat: test the communication transponder and verify that command packets can be sent from Mission Control (your laptop) to the Rover Core.

## Primary Objectives
- **Establish Link**: Establish a high-speed data uplink via the primary umbilical (USB cable).
- **Visual Beacon**: Activate the optical status diodes (RGB LEDs) to verify power distribution.
- **Audio Transponder**: Broadcast a standard confirmation beacon (piezo buzzer).
- **Field Challenge**: Transmit the universal emergency code **S.O.S.** in optical Morse code.

## Systems Check
- **Umbilical Line**: USB Cable connected and secured between laptop and mBot.
- **Core Power**: mBot switch toggled to `ON` (or USB power active).
- **Translator Module**: `python-for-mbot` (`pyserial`) installed in Thonny or `.venv`.
- **Firmware**: `mbot_firmware.ino` flashed via Arduino IDE (and Arduino IDE closed).

## Field Challenge
Open `missions/mission_01_ignition.py` in Thonny and press **▶ Run (`F5`)** to verify that the Emerald Green LED and 440 Hz tone work. Then scroll to the **Field Challenge (`# TODO`)** section and program the rover to transmit **S.O.S.** (`... --- ...`):
- **S**: 3 short pulses (`0.2` seconds ON, `0.2` seconds OFF)
- **O**: 3 long pulses (`0.6` seconds ON, `0.2` seconds OFF)
- **S**: 3 short pulses (`0.2` seconds ON, `0.2` seconds OFF)

## Progressive Hints
- **Hint 1 — Turning an LED On and Off**: Call `rover.rgb_led(0, 0, 255, 40, 0)` followed by `time.sleep(0.2)` to keep it lit, then `rover.rgb_led(0, 0, 0, 0, 0)` and `time.sleep(0.2)` to create a gap between pulses.
- **Hint 2 — Repeating Pulses with a Loop**: Instead of copy-pasting the same lines 3 times, use a `for` loop:
  `for _ in range(3):`
- **Hint 3 — Adding Audio to Each Pulse**: Inside your loop, call `rover.buzzer(880, 200)` for a short beep (`200` ms) or `rover.buzzer(880, 600)` for a long beep (`600` ms) right when you turn the LED on!

## Mission Success Metrics
- Terminal prints `[STATUS] Telemetry Link: SECURE 🟢` without serial errors.
- Both onboard RGB LEDs glow Emerald Green (`0, 255, 0`) for 1.5 seconds during the optical beacon diagnostic.
- The onboard buzzer sounds a 440 Hz tone during the audio transponder check.
- Field Challenge: Rover transmits 3 short pulses, 3 long pulses, and 3 short pulses (`S.O.S.`) and finishes in dark standby (`0, 0, 0`).

## Flight Engineer Debrief
| Code Command | Real-World Translation |
| :--- | :--- |
| `from mbot import *` | Requests the specialized toolset needed to communicate with the rover hardware. |
| `rover = mbot()` | Scans the serial lines to lock onto the rover's communication port. |
| `time.sleep(1.5)` | Halts the computer program temporarily so the physical lights have time to stay visible to human eyes. |
| `rover.rgb_led(0, 0, 0, 255, 0)` | Sends an 8-bit signal to paint the light with `0` Red, `255` Green, `0` Blue (`slot=0` lights both LEDs; `1` or `2` lights a single LED). |
| `rover.buzzer(440, 300)` | Pulses the piezo buzzer at `440` Hz for `300` milliseconds. |
