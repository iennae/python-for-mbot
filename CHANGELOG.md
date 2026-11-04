# Changelog

## `iennae/python-for-mbot` (`v0.2.0` — Original mBot / `mCore` Modernization)

### Added
- **Ares VII Rover Mission Curriculum & Metadata Manifest (`missions/`)**:
  - Added [`missions/missions.json`](missions/missions.json) as the single source of truth defining mission ordering and per-mission file associations (`story`, `starter`, and `test`), allowing missions to be reordered or inserted without renaming files.
  - Added 7 structured mission briefings (`launchpad_readiness.md`, `ignition.md`, `preflight_testing.md`, `thrusters.md`, `solar_beacon.md`, `radar_sweep.md`, and `canyon_patrol.md`) paired with number-free starter Python scripts (`ignition.py` through `canyon_patrol.py`) and dual-mode pre-flight unit test suites (`test_ignition.py` through `test_canyon_patrol.py`) that run both directly in Thonny (`F5`) and via `pytest`.
  - Added reusable `missions/TEMPLATE.md`, `missions/template_mission.py`, and `missions/test_template_mission.py` for authoring new missions.
- **Offline-Ready Mission Control Website (`site/` & `scripts/build_site.py`)**:
  - Added zero-dependency static site generator (`scripts/build_site.py`) and offline-compatible (`file://` double-clickable) Mission Control interface (`site/index.html`, `site/styles.css`, `site/app.js`, `site/missions_data.js`) with offline Python syntax highlighting for both Starter Code and Pre-Flight Unit Test cards.
  - Added GitHub Pages deployment workflow (`.github/workflows/deploy-pages.yml`) and privileged-only headless Chromium PR preview screenshot workflow (`.github/workflows/site-pr-preview.yml`, `scripts/capture_site_screenshots.py`).
- **Top-Level `mbot` Module, Synchronous Helpers & Digital Twin Telemetry (`src/mbot/`)**:
  - Added `from mbot import *` and `rover = mbot()` interface with synchronous helpers (`rgb_led`, `buzzer`, `move`, `stop`, `get_light`, `get_distance`, `get_line_follower`).
  - Mapped `rover.rgb_led(0, slot, r, g, b)` to mCore onboard `PORT_7` (`port=7, slot=2`) so the two onboard WS2812 RGB LEDs work without resetting `MeRGBLed` to `NC`.
  - Added automatic USB-serial port detection (`CH340`, `FTDI`, `CP210x`, and `MBOT_PORT` override) and hardware-free Digital Twin simulation mode (`mbot(simulate=True)` / `MBOT_SIMULATE=1`) with `rover.command_log`, `rover.clear_command_log()`, and `rover.set_simulated_sensor(sensor_name, value)` for unit testing.
- **CI & Automated Testing (`.github/workflows/ci.yml`, `tests/`, `missions/test_*.py`)**:
  - Added GitHub Actions CI running `ruff` and `pytest` across Python 3.11, 3.12, and 3.13 (`60` tests covering binary protocol frames, sensor parsing, mission simulation, pre-flight unit tests, and site generation).

### Changed
- **Modern `src/` Package Layout**:
  - Reorganized source into `src/mbot/` with a backward-compatible `src/lib/` shim (`from lib.mBot import *`) and moved legacy root-level scripts into `examples/`.
- **Python 3 Binary Protocol Fixes**:
  - Fixed `float2bytes`, `short2bytes`, `readFloat`, `readShort`, `readDouble`, `readString`, `doIROnBoard`, and ACK frame parsing in `src/mbot/mBot.py` for Python 3 `bytes`/`bytearray` semantics.
- **Streamlined Dependencies**:
  - Removed obsolete `cython` dependency; `pyserial>=3.5` is the sole default runtime requirement, with `hidapi>=0.14.0` available as an optional `[hid]` extra for 2.4G wireless USB dongles.
