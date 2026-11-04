# So You've Built Your mBot — Time to Take It to Mars

## Story Briefing
You have finished assembling your mBot rover on Earth! Right now, its onboard computer only knows the factory remote-control demo. Before launching to the Ares VII basin on Mars, we must inspect the rover's wiring, load the **Mars Telemetry Firmware (`mbot_firmware.ino`)** onto its core, and prime your laptop as **Mission Control**.

## Primary Objectives
- **Chassis & Cable Audit**: Verify the motors and sensors are plugged into the standard mCore ports so your Python scripts talk to the right hardware.
- **Rover Core Firmware Upload**: Use the Arduino IDE to flash `mbot_firmware.ino` from `iennae/Makeblock-Libraries` onto the mBot (done **once**).
- **Mission Control Setup**: Set up **Thonny** (recommended) or VS Code with `iennae/python-for-mbot` so you can run Python scripts live over the USB cable.

## Systems Check
- **Left Wheel Motor**: Plugged into port `M1` on the mCore board.
- **Right Wheel Motor**: Plugged into port `M2` on the mCore board.
- **Line-Follower Sensor (Underneath)**: Plugged into RJ25 `Port 2`.
- **Ultrasonic Sensor ("Eyes")**: Plugged into RJ25 `Port 3`.
- **Battery Pack**: 4x AA battery holder (or 3.7V LiPo) plugged into the power jack.

## Field Challenge
Follow the three launchpad preparation stages below to get your rover and laptop ready for ignition:

1. **Stage A — Flash the Rover Brain in Arduino IDE (One-Time Setup)**:
   - Install the **[Arduino IDE](https://www.arduino.cc/en/software)** *(if on Windows/macOS and no USB port appears when the mBot is plugged in, install the [WCH CH340 USB driver](https://learn.sparkfun.com/tutorials/how-to-install-ch340-drivers/all))*.
   - Download **[`iennae/Makeblock-Libraries` (main.zip)](https://github.com/iennae/Makeblock-Libraries/archive/refs/heads/main.zip)**, then in Arduino IDE click **`Sketch -> Include Library -> Add .ZIP Library...`** and select the downloaded ZIP file *(or clone `https://github.com/iennae/Makeblock-Libraries.git` into your `Arduino/libraries/` folder)*.
   - Open **`File -> Examples -> MakeBlock Drive Updated -> Firmware_For_mBlock -> mbot_firmware`**.
   - Select **`Tools -> Board -> Arduino AVR Boards -> Arduino Uno`** and choose your mBot's USB port under **`Tools -> Port`**.
   - Click **Upload (`→`)**, wait for **"Done uploading."**, and **close the Arduino IDE** so it releases the USB serial port!
2. **Stage B — Prime Mission Control in Thonny**:
   - Download and open **[Thonny](https://thonny.org/)** (Python 3 is built right in).
   - Clone or download **[`iennae/python-for-mbot`](https://github.com/iennae/python-for-mbot)**.
   - In Thonny, click **`Tools -> Open system shell...`** and run `pip install -e .` inside the `python-for-mbot` folder *(or click **`Tools -> Manage packages...`**, search for **`pyserial`**, and click **Install**)*.
3. **Stage C — Verify the Rover Test Stand Rule**:
   - LEDs, the buzzer, and sensors work on USB cable power alone, but **the drive motors (`M1`/`M2`) only spin when the battery pack is connected and the mBot power switch is toggled `ON`**. Keep a small block handy to prop the wheels off the desk when testing motor scripts!

## Progressive Hints
- **Why do we close the Arduino IDE after uploading?** Only one program on your laptop can lock onto the USB serial port at a time. If the Arduino IDE (or its Serial Monitor) stays open, Python won't be able to connect.
- **How do I restore the original blue remote-control mode later?** Open `File -> Examples -> MakeBlock Drive Updated -> Firmware_For_mBlock -> mbot_factory_firmware` in Arduino IDE and click Upload!
- **Can I view this Mission Control website completely offline?** Yes! Just double-click `site/index.html` on your computer—no internet connection or web server required.

## Mission Success Metrics
- Left motor (`M1`), Right motor (`M2`), Line Follower (`Port 2`), and Ultrasonic Sensor (`Port 3`) are securely connected.
- `mbot_firmware.ino` from `iennae/Makeblock-Libraries` uploaded to the mBot (`Board: Arduino Uno`) with "Done uploading."
- Arduino IDE is closed so the USB serial port is free for Python.
- Thonny (or VS Code) is open with `iennae/python-for-mbot` and `pyserial` installed.

## Flight Engineer Debrief
| Component | Role in the Mission Control Architecture |
| :--- | :--- |
| `mCore` (`ATmega328P`) | The 8-bit Arduino Uno microcontroller onboard the original mBot. |
| `mbot_firmware.ino` | The C++ transceiver program flashed once onto the mBot so it understands live serial commands at `115200` baud. |
| `USB Umbilical Cable` | Carries live command packets from Python on your laptop to the rover and returns sensor telemetry. |
| `Thonny IDE` | Your ground-station code editor where you edit `missions/*.py` and press **▶ Run (`F5`)**. |
