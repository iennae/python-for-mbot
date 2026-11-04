# 🛰️ Ares VII Rover — Python Mission Curriculum (`missions/`)

This directory contains the mission manifest ([`missions.json`](missions.json)), story briefings (`*.md`), starter Python scripts (`*.py`), and Digital Twin pre-flight unit tests (`test_*.py`) for the **Original Makeblock mBot (`mCore`)**.

> **Offline Website**: Open [`../site/index.html`](../site/index.html) directly in any browser (by double-clicking the file in Finder / File Explorer) for the interactive **Ares VII Mission Control** interface with collapsible hints, syntax-highlighted starter templates and unit tests, and interactive success metric checklists!

---

## 📋 Mission Roster (Ordered via [`missions.json`](missions.json))

| Order | Mission ID | Story File | Starter Code | Pre-Flight Unit Test | Focus |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **00** | `launchpad_readiness` | [`launchpad_readiness.md`](launchpad_readiness.md) | *(Pre-Flight Setup)* | *(Pre-Flight Setup)* | Wiring check, Arduino IDE (`mbot_firmware.ino`), and Thonny setup |
| **01** | `ignition` | [`ignition.md`](ignition.md) | [`ignition.py`](ignition.py) | [`test_ignition.py`](test_ignition.py) | USB serial handshake, RGB LEDs, piezo buzzer, and S.O.S. Morse challenge |
| **02** | `preflight_testing` | [`preflight_testing.md`](preflight_testing.md) | [`preflight_testing.py`](preflight_testing.py) | [`test_preflight_testing.py`](test_preflight_testing.py) | Digital Twin simulator (`mbot(simulate=True)`), `rover.command_log`, and `assert` unit testing |
| **03** | `thrusters` | [`thrusters.md`](thrusters.md) | [`thrusters.py`](thrusters.py) | [`test_thrusters.py`](test_thrusters.py) | Differential drive thrusters (`M1`/`M2`), reverse, pivot turns, and braking |
| **04** | `solar_beacon` | [`solar_beacon.md`](solar_beacon.md) | [`solar_beacon.py`](solar_beacon.py) | [`test_solar_beacon.py`](test_solar_beacon.py) | Polling the onboard light sensor and automatic Dusk Protocol headlights |
| **05** | `radar_sweep` | [`radar_sweep.md`](radar_sweep.md) | [`radar_sweep.py`](radar_sweep.py) | [`test_radar_sweep.py`](test_radar_sweep.py) | Ultrasonic rangefinder (`Port 3`) proximity alerts and boulder evasion |
| **06** | `canyon_patrol` | [`canyon_patrol.md`](canyon_patrol.md) | [`canyon_patrol.py`](canyon_patrol.py) | [`test_canyon_patrol.py`](test_canyon_patrol.py) | Dual IR line-follower (`Port 2`) 4-state canyon conduit navigation |

---

## ➕ How to Add or Reorder a Mission

All mission ordering and file associations live in [`missions.json`](missions.json)—no filenames contain numbers, so you can insert or reorder missions at any time without renaming files:

1. **Create the Files**: Copy [`TEMPLATE.md`](TEMPLATE.md), [`template_mission.py`](template_mission.py), and [`test_template_mission.py`](test_template_mission.py) to descriptive, unnumbered filenames (e.g., `servo_arm.md`, `servo_arm.py`, and `test_servo_arm.py`).
2. **Register in `missions.json`**: Insert an entry at the desired position in [`missions.json`](missions.json) with `"files": { "story": "servo_arm.md", "starter": "servo_arm.py", "test": "test_servo_arm.py" }`.
3. **Rebuild the Website Data**:
   ```bash
   python scripts/build_site.py
   ```
   *(You can also open `scripts/build_site.py` directly in Thonny and press **▶ Run**!)*
