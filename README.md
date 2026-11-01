# Python for mBot (Original mBot / mCore Edition)

A modernized Python 3.11+ interface and **Cadet Engineer Mission Curriculum** for controlling the **Original Makeblock mBot v1 (mCore / ATmega328P)** over USB Serial, Bluetooth Serial, or 2.4G Wireless HID.

---

## Table of Contents
* [Hardware & Firmware Preparation](#hardware--firmware-preparation)
* [Installation](#installation)
* [Quick Start: Cadet Engineer API (`from mbot import *`)](#quick-start-cadet-engineer-api-from-mbot-import-)
* [Cadet Engineer Missions (`missions/`)](#cadet-engineer-missions-missions)
* [Classic Callback API (`from lib.mBot import *`)](#classic-callback-api-from-libmbot-import-)
* [Simulation Mode (No Hardware Required)](#simulation-mode-no-hardware-required)

---

## Hardware & Firmware Preparation

Before running Python scripts from your computer, your **Original mBot (`mCore`)** needs the Makeblock Online Serial Firmware installed:

1. Clone or install the companion Arduino library from [`iennae/Makeblock-Libraries`](https://github.com/iennae/Makeblock-Libraries) into your `Arduino/libraries/` directory.
2. Open the **Arduino IDE** and select:
   * **Board**: `Tools -> Board -> Arduino AVR Boards -> Arduino Uno`
   * **Port**: Your mBot's USB serial port (e.g., `/dev/ttyUSB0`, `/dev/cu.usbserial-*`, or `COM3`)
3. Open `File -> Examples -> MakeBlock Drive Updated -> Firmware_For_mBlock -> mbot_firmware`.
4. Click **Upload** to flash the online firmware to your mBot.

---

## Installation

Create and activate a Python 3.11+ virtual environment, then install the package:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

* For development (linting with `ruff` and testing with `pytest`):
  ```bash
  pip install -e ".[dev]"
  ```
* For optional 2.4G wireless USB dongle support (`hidapi`):
  ```bash
  pip install -e ".[hid]"
  ```

---

## Quick Start: Cadet Engineer API (`from mbot import *`)

The `mbot` module automatically scans your USB serial ports to connect to the rover (or you can pass `mbot(port="/dev/ttyUSB0")` or set the `MBOT_PORT` environment variable):

```python
import time
from mbot import *

rover = mbot()

# Pulse both onboard RGB LEDs Emerald Green (port=0, slot=0, R, G, B)
rover.rgb_led(0, 0, 0, 255, 0)
time.sleep(1.0)

# Play a 440 Hz tone for 300 ms
rover.buzzer(440, 300)
time.sleep(0.5)

# Read sensors synchronously
print("Light sensor:", rover.get_light())
print("Ultrasonic distance (cm):", rover.get_distance(port=3))

# Drive forward and stop
rover.move(100, 100)
time.sleep(1.0)
rover.stop()

# Turn off LEDs
rover.rgb_led(0, 0, 0, 0, 0)
```

---

## Cadet Engineer Missions (`missions/`)

Explore the guided mission briefings in [`missions/README.md`](missions/README.md):

1. [`missions/mission_01_ignition.py`](missions/mission_01_ignition.py) — **Ignition & Telemetry Handshake** (RGB LEDs & Audio Transponder)
2. [`missions/mission_01_sos_challenge.py`](missions/mission_01_sos_challenge.py) — **Field Challenge: S.O.S. Optical & Audio Morse Beacon**
3. [`missions/mission_02_thrusters.py`](missions/mission_02_thrusters.py) — **Drive Thruster Calibration** (Forward, Reverse, Pivot & Stop)
4. [`missions/mission_03_solar_beacon.py`](missions/mission_03_solar_beacon.py) — **Solar Array & Night-Vision Beacon** (Onboard Light Sensor)
5. [`missions/mission_04_radar_sweep.py`](missions/mission_04_radar_sweep.py) — **Ultrasonic Radar & Crater Avoidance** (Ultrasonic Rangefinder)
6. [`missions/mission_05_canyon_patrol.py`](missions/mission_05_canyon_patrol.py) — **Canyon Floor Line Navigation** (Dual IR Line Follower)

---

## Classic Callback API (`from lib.mBot import *`)

All classic scripts remain supported and now auto-detect USB serial ports when `bot.startWithSerial()` is called without arguments:

```python
from lib.mBot import *


def onLight(value):
    print("light = ", value)


if __name__ == "__main__":
    bot = mBot()
    bot.startWithSerial()  # Auto-detects USB serial port (or pass e.g. "/dev/ttyUSB0")
    try:
        while True:
            bot.requestLightOnBoard(1, onLight)
            sleep(0.5)
    except KeyboardInterrupt:
        bot.close()
```

---

## Simulation Mode (No Hardware Required)

To test any script or mission without a physical mBot plugged in, set `MBOT_SIMULATE=1`:

```bash
MBOT_SIMULATE=1 python missions/mission_01_ignition.py
```
