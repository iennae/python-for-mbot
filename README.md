# Python for mBot (`iennae` Original mBot Fork)

A Python 3.10+ interface and **Ares VII Rover Mission Curriculum** for controlling the **Original Makeblock mBot (`mCore` / `ATmega328P`)** over USB Serial, Bluetooth Serial, or 2.4G Wireless HID.

---

## What This Project Is & What This Fork Does Differently

This repository is a modernized fork of [`xeecos/python-for-mbot`](https://github.com/xeecos/python-for-mbot), updated for modern Python 3 and paired with **[`iennae/Makeblock-Libraries`](https://github.com/iennae/Makeblock-Libraries)**.

While newer kits like the mBot2 support Python natively at a significantly higher price point, the **original Makeblock mBot (`mCore`)** is a widely available, affordable platform. Once a builder has assembled the original mBot and explored its pre-built remote-control modes and block-based programming, this project provides a direct bridge into introductory Python programming using the hardware they already own:

- Adds a beginner-friendly synchronous API (`from mbot import *`, `rover = mbot()`) alongside automatic USB serial port discovery.
- Provides a guided **Ares VII Rover** mission curriculum (`missions/`) with starter templates (`# TODO` challenges) and an offline-ready **Mission Control** website (`site/index.html`).
- Removes legacy build requirements (`cython` is no longer needed; `pyserial` is the only default dependency).

For release notes and technical changes, see **[`CHANGELOG.md`](CHANGELOG.md)**. For original upstream context and classic callback API details, see **[`ATTRIBUTION.md`](ATTRIBUTION.md)**.

---

## ⚠️ Use at Your Own Risk & Scope Disclaimer

> **IMPORTANT — USE AT YOUR OWN RISK:**
> This software and documentation are provided **"AS IS"**, without warranty of any kind, express or implied. By downloading, installing, or running these scripts with physical hardware, you assume all risks associated with their operation.
>
> - **Hardware Scope**: This fork is focused on and tested exclusively with the **original Makeblock mBot (`mCore` / `ATmega328P`)**. Other Makeblock robots or mainboards are not tested in this fork.
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

Clone or download this repository (`iennae/python-for-mbot`):

```bash
git clone https://github.com/iennae/python-for-mbot.git
cd python-for-mbot
```

### Option A: Using Thonny (Recommended Beginner Editor)
1. Download and open **[Thonny](https://thonny.org/)** (which includes Python 3 built in).
2. Install the package in Thonny:
   * Click **`Tools -> Open system shell...`** and run `pip install -e .` inside the `python-for-mbot` folder *(or click **`Tools -> Manage packages...`**, search for **`pyserial`**, and click **Install**)*.
3. Click **`File -> Open...`**, select [`missions/ignition.py`](missions/ignition.py) (or validate first with [`missions/test_ignition.py`](missions/test_ignition.py)), and click the green **▶ Run (`F5`)** button!

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

* **Offline Mission Control Website**: Double-click [`site/index.html`](site/index.html) in your file manager (`Finder` / `File Explorer`) to open the interactive **Ares VII Rover — Mission Control** guide directly in your browser (works 100% offline via `file://` with no web server required), or view the deployed GitHub Pages site.
* **Manifest-Ordered Missions (`missions/missions.json`)**: Each mission defines its story briefing (`*.md`), starter code (`*.py`), and Digital Twin pre-flight unit test (`test_*.py`) without hardcoded numbers in filenames:
  * **Mission 00 — Launchpad Readiness**: [`missions/launchpad_readiness.md`](missions/launchpad_readiness.md) (Wiring check, Arduino IDE firmware upload, and Thonny setup)
  * **Mission 01 — Ignition & Telemetry Handshake**: [`missions/ignition.py`](missions/ignition.py) & [`missions/test_ignition.py`](missions/test_ignition.py)
  * **Mission 02 — Digital Twin & Pre-Flight Unit Testing**: [`missions/preflight_testing.py`](missions/preflight_testing.py) & [`missions/test_preflight_testing.py`](missions/test_preflight_testing.py)
  * **Mission 03 — Drive Thruster Calibration**: [`missions/thrusters.py`](missions/thrusters.py) & [`missions/test_thrusters.py`](missions/test_thrusters.py)
  * **Mission 04 — Solar Array & Dusk Protocol**: [`missions/solar_beacon.py`](missions/solar_beacon.py) & [`missions/test_solar_beacon.py`](missions/test_solar_beacon.py)
  * **Mission 05 — Ultrasonic Radar & Boulder Evasion**: [`missions/radar_sweep.py`](missions/radar_sweep.py) & [`missions/test_radar_sweep.py`](missions/test_radar_sweep.py)
  * **Mission 06 — Canyon Conduit Navigation**: [`missions/canyon_patrol.py`](missions/canyon_patrol.py) & [`missions/test_canyon_patrol.py`](missions/test_canyon_patrol.py)
* **Adding or Reordering Missions**: Copy [`missions/TEMPLATE.md`](missions/TEMPLATE.md), [`missions/template_mission.py`](missions/template_mission.py), and [`missions/test_template_mission.py`](missions/test_template_mission.py), add an entry in [`missions/missions.json`](missions/missions.json), and run `python scripts/build_site.py` to update `site/missions_data.js`.
* **Running Pre-Flight Unit Tests (Thonny or `pytest`, No Hardware Required)**:
  * In **Thonny**: Open any `missions/test_*.py` file and press **▶ Run (`F5`)**.
  * In a **Terminal**:
    ```bash
    pytest
    ```

---

## Repository Structure

```text
python-for-mbot/
├── pyproject.toml          # Modern PEP 621 package configuration
├── requirements.txt        # Runtime dependency (pyserial>=3.5)
├── CHANGELOG.md            # Release notes and modernization changelog
├── ATTRIBUTION.md          # Original project context and classic callback API
├── src/
│   ├── mbot/               # Core mbot package (`from mbot import *`)
│   └── lib/                # Backward-compatible shim (`from lib.mBot import *`)
├── missions/               # Ares VII Rover starter templates & mission briefings
├── scripts/                # Zero-dependency static site generator (`build_site.py`)
├── site/                   # Offline-ready static website (also deployed to GitHub Pages)
├── examples/               # Classic callback-based example scripts
└── tests/                  # Pytest protocol, simulation, site build, and smoke tests
```
