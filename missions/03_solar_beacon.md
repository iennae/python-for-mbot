# Mission 03: Solar Array & Dusk Protocol

- **Badge**: Onboard Light Telemetry & Conditionals
- **Script**: mission_03_solar_beacon.py
- **Requires Battery**: false

## Story Briefing
A Martian dust squall is rolling across the Ares VII basin and solar flux is dropping fast! Poll the rover's onboard photo-sensor to measure ambient light levels in real time and program an automatic **Dusk Protocol** that ignites the high-beam white headlights whenever darkness falls.

## Primary Objectives
- **Poll Telemetry**: Read live floating-point light values using `rover.get_light()`.
- **Threshold Calibration**: Observe the sensor reading in normal room light vs. when covered by your hand.
- **Field Challenge**: Write a telemetry loop with an `if / else` decision branch that switches on bright white headlights (`255, 255, 255`) whenever light drops below `NIGHT_THRESHOLD`.

## Systems Check
- **Umbilical Line**: USB cable connected.
- **Onboard Light Sensor**: Located on the top front of the mCore board (`Port 6` internal). Keep it unobstructed for your baseline reading, then shade it with your hand to simulate a Martian dust storm.

## Field Challenge
Open `missions/mission_03_solar_beacon.py` and run it once to see your room's baseline `lux` value printed in the terminal. Then complete **Phase 2 (`# TODO`)**:
1. Create a loop (`for sample in range(15):`) that reads `lux = rover.get_light()` every `0.5` seconds.
2. Print each reading to the terminal.
3. If `lux < NIGHT_THRESHOLD`, turn both LEDs bright white (`255, 255, 255`) and print a low-light alert; otherwise, set a dim green status light (`0, 60, 0`).

## Progressive Hints
- **Hint 1 — Polling in a Loop**:
  ```python
  for sample in range(15):
      lux = rover.get_light()
      print(f"Sample {sample + 1}: {lux:.1f}")
      time.sleep(0.5)
  ```
- **Hint 2 — Decision Branching (`if / else`)**:
  ```python
  if lux < NIGHT_THRESHOLD:
      rover.rgb_led(0, 0, 255, 255, 255)
  else:
      rover.rgb_led(0, 0, 0, 60, 0)
  ```
- **Hint 3 — Tuning `NIGHT_THRESHOLD`**: If your room is naturally dim, check the number printed in Phase 1 (e.g., `180.0`) and set `NIGHT_THRESHOLD` halfway between your bright and shaded readings!

## Mission Success Metrics
- Terminal prints live ambient light values every 0.5 seconds.
- Shading the mCore board with your hand drops the reading below `NIGHT_THRESHOLD` and immediately switches the LEDs to bright white (`255, 255, 255`).
- Removing your hand restores the low-power green indicator (`0, 60, 0`).
- Rover extinguishes LEDs cleanly when the sweep finishes.

## Flight Engineer Debrief
| Code Command | Real-World Translation |
| :--- | :--- |
| `lux = rover.get_light()` | Sends a sensor request packet (`GET LIGHT_SENSOR`) to Port 6 and waits for the mCore ADC (`0..1023`) reply. |
| `f"Flux: {lux:.1f}"` | Formats the floating-point sensor reading to 1 decimal place for clean telemetry logs. |
| `if lux < NIGHT_THRESHOLD:` | Evaluates a boolean condition so the rover can react autonomously to its environment. |
