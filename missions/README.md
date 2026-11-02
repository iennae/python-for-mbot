# 🛰️ Ares VII Rover — Python Mission Curriculum (`missions/`)

This directory contains the mission briefings and starter Python templates for the **Original Makeblock mBot (`mCore`)**.

> **Offline Website**: Open [`../site/index.html`](../site/index.html) directly in any browser (by double-clicking the file in Finder / File Explorer) for the interactive **Ares VII Mission Control** interface with collapsible hints, copyable starter templates, and interactive success metric checklists!

---

## 📋 Mission Roster

| Mission | Briefing File | Starter Template | Focus |
| :--- | :--- | :--- | :--- |
| **Mission 00** | [`00_launchpad_readiness.md`](00_launchpad_readiness.md) | *(Pre-Flight Setup)* | Wiring check, Arduino IDE (`mbot_firmware.ino`), and Thonny setup |
| **Mission 01** | [`01_ignition.md`](01_ignition.md) | [`mission_01_ignition.py`](mission_01_ignition.py) | USB serial handshake, RGB LEDs, piezo buzzer, and S.O.S. Morse challenge |
| **Mission 02** | [`02_thrusters.md`](02_thrusters.md) | [`mission_02_thrusters.py`](mission_02_thrusters.py) | Differential drive thrusters (`M1`/`M2`), reverse, pivot turns, and braking |
| **Mission 03** | [`03_solar_beacon.md`](03_solar_beacon.md) | [`mission_03_solar_beacon.py`](mission_03_solar_beacon.py) | Polling the onboard light sensor and automatic Dusk Protocol headlights |
| **Mission 04** | [`04_radar_sweep.md`](04_radar_sweep.md) | [`mission_04_radar_sweep.py`](mission_04_radar_sweep.py) | Ultrasonic rangefinder (`Port 3`) 3-zone proximity alerts and boulder evasion |
| **Mission 05** | [`05_canyon_patrol.md`](05_canyon_patrol.md) | [`mission_05_canyon_patrol.py`](mission_05_canyon_patrol.py) | Dual IR line-follower (`Port 2`) 4-state canyon conduit navigation |

---

## ➕ How to Add a New Mission

The website (`site/`) is generated automatically from the files in this `missions/` folder using only Python's standard library:

1. **Create the Starter Script**: Copy [`template_mission.py`](template_mission.py) to `missions/mission_06_<slug>.py` and customize Phase 1 (working demo) and Phase 2 (`# TODO` Field Challenge).
2. **Create the Mission Briefing**: Copy [`TEMPLATE.md`](TEMPLATE.md) to `missions/06_<slug>.md` and fill in the sections (`Story Briefing`, `Primary Objectives`, `Systems Check`, `Field Challenge`, `Progressive Hints`, `Mission Success Metrics`, and `Flight Engineer Debrief`), setting `- **Script**: mission_06_<slug>.py`.
3. **Rebuild the Website Data**:
   ```bash
   python scripts/build_site.py
   ```
   *(You can also open `scripts/build_site.py` directly in Thonny and press **▶ Run**!)*
