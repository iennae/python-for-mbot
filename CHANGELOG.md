# Changelog

## `iennae/python-for-mbot` (`v0.2.0` — Original mBot / `mCore` Modernization)

### Added
- **Ares VII Rover Mission Curriculum (`missions/`)**:
  - Added structured mission briefings (`missions/00_launchpad_readiness.md` through `missions/05_canyon_patrol.md`) paired with starter Python templates (`missions/mission_01_ignition.py` through `missions/mission_05_canyon_patrol.py`) featuring guided `# TODO` Field Challenges.
  - Added reusable `missions/TEMPLATE.md` and `missions/template_mission.py` for authoring new missions.
- **Offline-Ready Mission Control Website (`site/` & `scripts/build_site.py`)**:
  - Added zero-dependency static site generator (`scripts/build_site.py`) and offline-compatible (`file://` double-clickable) Mission Control interface (`site/index.html`, `site/styles.css`, `site/app.js`, `site/missions_data.js`).
  - Added GitHub Pages deployment workflow (`.github/workflows/deploy-pages.yml`).
- **Top-Level `mbot` Module & Synchronous Helpers (`src/mbot/`)**:
  - Added `from mbot import *` and `rover = mbot()` interface with synchronous helpers (`rgb_led`, `buzzer`, `move`, `stop`, `get_light`, `get_distance`, `get_line_follower`).
  - Mapped `rover.rgb_led(0, slot, r, g, b)` to mCore onboard `PORT_7` (`port=7, slot=2`) so the two onboard WS2812 RGB LEDs work without resetting `MeRGBLed` to `NC`.
  - Added automatic USB-serial port detection (`CH340`, `FTDI`, `CP210x`, and `MBOT_PORT` override) and hardware-free simulation mode (`MBOT_SIMULATE=1`).
- **CI & Automated Testing (`.github/workflows/ci.yml`, `tests/`)**:
  - Added GitHub Actions CI running `ruff` and `pytest` across Python 3.11, 3.12, and 3.13 (`35` tests covering binary protocol frames, sensor parsing, mission simulation, and site generation).

### Changed
- **Modern `src/` Package Layout**:
  - Reorganized source into `src/mbot/` with a backward-compatible `src/lib/` shim (`from lib.mBot import *`) and moved legacy root-level scripts into `examples/`.
- **Python 3 Binary Protocol Fixes**:
  - Fixed `float2bytes`, `short2bytes`, `readFloat`, `readShort`, `readDouble`, `readString`, `doIROnBoard`, and ACK frame parsing in `src/mbot/mBot.py` for Python 3 `bytes`/`bytearray` semantics.
- **Streamlined Dependencies**:
  - Removed obsolete `cython` dependency; `pyserial>=3.5` is the sole default runtime requirement, with `hidapi>=0.14.0` available as an optional `[hid]` extra for 2.4G wireless USB dongles.
