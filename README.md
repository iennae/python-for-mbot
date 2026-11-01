# Python for mBot (`iennae` Original mBot / mCore Fork)

A modernized Python 3.10+ interface and **Ares VII Rover Mission Curriculum** for controlling the **Original Makeblock mBot (`mCore` / `ATmega328P`)** over USB Serial, Bluetooth Serial, or 2.4G Wireless HID.

---

## About This Fork (`iennae/python-for-mbot`)

This repository is a modernized fork of [`xeecos/python-for-mbot`](https://github.com/xeecos/python-for-mbot), updated for Python 3.10–3.13 and paired with **[`iennae/Makeblock-Libraries`](https://github.com/iennae/Makeblock-Libraries)**.

While newer kits like the mBot2 support Python natively at a significantly higher price point, the **original Makeblock mBot (`mCore`)** is a widely available, affordable platform. Once a builder has assembled the original mBot and explored its pre-built remote-control modes and block-based programming, this project provides a direct bridge into introductory Python programming using the hardware they already own.

### What Was Modernized in This Fork
- **Standard `src/` Package Layout**: Organized into `src/mbot/` (with a backward-compatible `src/lib/` shim so legacy `from lib.mBot import *` scripts continue to work), `missions/`, `examples/`, and `tests/`.
- **Python 3 Binary Protocol & Auto-Discovery**: Fixed Python 3 `bytes`/`struct` packing and unpacking against `mbot_firmware.ino`, added automatic USB serial port detection (`CH340` / `FTDI` / `CP210x`), and added a hardware-free simulation mode (`MBOT_SIMULATE=1`).
- **Streamlined Dependencies**: Uses `pyserial` as the sole required dependency (`cython` is no longer needed, and `hidapi` is an optional `[hid]` extra for legacy 2.4G wireless USB dongles).
- **Ares VII Rover Mission Curriculum (`missions/` & `site/`)**: Guided starter templates, mission briefings, and an offline-compatible static website.

---

## ⚠️ Use at Your Own Risk & Safety Disclaimer

> **IMPORTANT — USE AT YOUR OWN RISK:**
> This software and documentation are provided **"AS IS"**, without warranty of any kind, express or implied. By downloading, installing, or running these scripts with physical hardware, you assume all risks associated with their operation.
>
> - **Moving Parts & Pinch Hazards**: Keep fingers, hair, loose clothing, and USB cables clear of spinning wheels, gears, and motors.
> - **Drop & Collision Hazards**: Motor commands execute immediately over serial and can drive the robot off desks or tables. Prop the mBot's wheels off the surface on a small block ("test stand") when testing new motor scripts, or operate on the floor.
> - **Power & Battery Safety**: Onboard LEDs, the buzzer, and sensors can run off USB 5V power alone, but **the drive motors (`M1`/`M2`) require the battery pack connected with the chassis power switch toggled `ON`**. Turn the chassis switch `OFF` when not in use.

---

## Step 1: Prepare Your Original mBot (`mCore` Firmware — One-Time Setup)

Because the original mBot (`mCore`) uses an 8-bit `ATmega328P` (Arduino Uno) microcontroller, Python runs on your computer ("Mission Control") and sends real-time commands over the USB cable to the mBot.

Before running Python scripts, flash the **Online Serial Firmware (`mbot_firmware.ino`)** onto the mBot **once** using the Arduino IDE:

1. **Install Arduino IDE**: Download from [arduino.cc/en/software](https://www.arduino.cc/en/software).
   * *(USB Driver Note: The original mBot uses a WCH `CH340` USB-to-serial chip. Linux includes this driver automatically; on Windows or macOS, if no serial port appears when the mBot is plugged in, install the standard [WCH CH340 driver](https://learn.sparkfun.com/tutorials/how-to-install-ch340-drivers/all).)*
2. **Install [`iennae/Makeblock-Libraries`](https://github.com/iennae/Makeblock-Libraries) in Arduino IDE**:
   * **Option A — `.zip` Installer in Arduino IDE (Easiest)**:
     1. Download **[`iennae/Makeblock-Libraries` (`main.zip`)](https://github.com/iennae/Makeblock-Libraries/archive/refs/heads/main.zip)**.
     2. In Arduino IDE, click **`Sketch -> Include Library -> Add .ZIP Library...`** and select the downloaded `.zip` file.
   * **Option B — `git clone` into your Arduino Sketchbook `libraries/` folder**:
     ```bash
     # macOS / Windows (Git Bash):
     git clone https://github.com/iennae/Makeblock-Libraries.git ~/Documents/Arduino/libraries/Makeblock-Libraries

     # Linux:
     git clone https://github.com/iennae/Makeblock-Libraries.git ~/Arduino/libraries/Makeblock-Libraries
     ```
     *(Restart the Arduino IDE if it was already open.)*
3. **Upload `mbot_firmware.ino`**:
   * Plug your mBot into your computer via the USB cable.
   * In Arduino IDE, open **`File -> Examples -> MakeBlock Drive Updated -> Firmware_For_mBlock -> mbot_firmware`**.
   * Select **`Tools -> Board -> Arduino AVR Boards -> Arduino Uno`**.
   * Select **`Tools -> Port`** and choose your mBot's USB serial port (`COM*` on Windows, `/dev/cu.usbserial-*` or `/dev/cu.wchusbserial*` on macOS, `/dev/ttyUSB0` on Linux).
   * Click **Upload (`→`)** and wait for **"Done uploading."**
   * **Important**: **Close the Arduino IDE** after uploading so it releases the USB serial port for Python!

---

## Step 2: Prime Mission Control (Thonny or Python Virtual Environment)

Clone or download this repository (`iennae/python-for-mbot`), not the original upstream repo:

```bash
git clone https://github.com/iennae/python-for-mbot.git
cd python-for-mbot
```

### Option A: Using Thonny (Recommended Beginner Editor)
1. Download and open **[Thonny](https://thonny.org/)** (which includes Python 3 built in).
2. Install the serial communication library using either method:
   * **Point-and-Click in Thonny**: Click **`Tools -> Manage packages...`**, search for **`pyserial`**, and click **Install**.
   * **Or via Thonny's Shell**: Click **`Tools -> Open system shell...`** and run `pip install -e .` inside the `python-for-mbot` folder.
3. Click **`File -> Open...`**, select [`missions/mission_01_ignition.py`](missions/mission_01_ignition.py), and click the green **▶ Run (`F5`)** button!

### Option B: Using Terminal / VS Code (`venv`)
```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -e .
```
* For development (linting with `ruff` and testing with `pytest`): `pip install -e ".[dev]"`
* For optional 2.4G wireless USB HID dongle support: `pip install -e ".[hid]"`

---

## Step 3: Launch the Ares VII Rover Missions (`missions/` & `site/`)

* **Offline Mission Control Website**: Double-click `site/index.html` in your file manager (`Finder` / `File Explorer`) to open the interactive **Ares VII Rover — Mission Control** guide directly in your browser (works 100% offline via `file://` with no web server required).
* **Starter Mission Scripts (`missions/`)**:
  * [`missions/mission_01_ignition.py`](missions/mission_01_ignition.py) — **Ignition & Telemetry Handshake** (RGB LEDs & Audio Transponder)
  * [`missions/mission_02_thrusters.py`](missions/mission_02_thrusters.py) — **Drive Thruster Calibration** (Forward, Reverse, Pivot & Stop)
  * [`missions/mission_03_solar_beacon.py`](missions/mission_03_solar_beacon.py) — **Solar Array & Dusk Protocol** (Onboard Light Sensor)
  * [`missions/mission_04_radar_sweep.py`](missions/mission_04_radar_sweep.py) — **Ultrasonic Radar & Boulder Evasion** (Ultrasonic Rangefinder)
  * [`missions/mission_05_canyon_patrol.py`](missions/mission_05_canyon_patrol.py) — **Canyon Conduit Navigation** (Dual IR Line Follower)
* **Dry-Run Simulation Mode (No Hardware Required)**:
  ```bash
  MBOT_SIMULATE=1 python missions/mission_01_ignition.py
  ```

---

## Repository Structure

```text
python-for-mbot/
├── pyproject.toml          # Modern PEP 621 package configuration
├── requirements.txt        # Runtime dependency (pyserial>=3.5)
├── src/
│   ├── mbot/               # Core mbot package (`from mbot import *`)
│   └── lib/                # Backward-compatible shim (`from lib.mBot import *`)
├── missions/               # Ares VII Rover starter templates & mission briefings
├── site/                   # Offline-ready static website (also deployed to GitHub Pages)
├── examples/               # Classic callback-based example scripts
└── tests/                  # Pytest protocol, simulation, and smoke tests
```

---

## Original Project Context & Attribution

> *The section below is preserved from the original [`xeecos/python-for-mbot`](https://github.com/xeecos/python-for-mbot) repository to retain historical context and attribution.*

### Original Description
A Python interface to control and communicate with mBot robot kit from Makeblock.

This has been tested with:
* the Raspberry PI.
* the Intel Edison.

It works on Linux, Windows 7/10 and OS X.

### Classic Callback API Usage (`examples/`)
```python
from lib.mBot import *


def onLight(value):
    print("light = ", value)


if __name__ == "__main__":
    bot = mBot()
    bot.startWithSerial()  # Auto-detects USB serial port (or pass e.g. "COM15" / "/dev/ttyUSB0")
    try:
        while True:
            bot.requestLightOnBoard(1, onLight)
            sleep(0.5)
    except KeyboardInterrupt:
        bot.close()
```

Using wireless HID (requires `pip install -e ".[hid]"`):
```python
bot.startWithHID()
```
