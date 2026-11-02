# Mission 04: Ultrasonic Radar & Boulder Evasion

- **Badge**: Acoustic Rangefinding & Collision Avoidance
- **Script**: mission_04_radar_sweep.py
- **Requires Battery**: true

## Story Briefing
The exit ramp out of the Ares VII landing crater is littered with boulders! Use the rover's forward-facing ultrasonic rangefinder (`Port 3`) to measure obstacle distance in centimeters and trigger an automatic reverse-and-pivot evasion whenever a boulder breaches your 20 cm safety perimeter.

## Primary Objectives
- **Acoustic Ping**: Measure forward distance (`cm`) using `rover.get_distance(port=3)`.
- **3-Zone Proximity Beacon**: Display Emerald Green (`>= 40 cm`), Amber (`20..40 cm`), or Red (`< 20 cm`) based on distance.
- **Field Challenge**: Combine radar polling with drive thrusters so the rover cruises when clear, slows down in the caution zone, and automatically backs up and pivots when an obstacle is within 20 cm.

## Systems Check
- **Ultrasonic Sensor**: Plugged into RJ25 **`Port 3`** on the mCore board.
- **Battery Power**: Battery pack plugged in and chassis switch toggled **`ON`** for motor evasion maneuvers.
- **Rover Test Stand**: Test first on your desktop stand using your hand as a movable "boulder" in front of the ultrasonic eyes!

## Field Challenge
Open `missions/mission_04_radar_sweep.py` and run Phase 1 to confirm the ultrasonic sensor reports distance in centimeters. Then complete **Phase 2 (`# TODO`)**:
1. Poll `distance_cm = rover.get_distance(port=3)` in a loop.
2. Use `if / elif / else` to implement the 3 proximity zones:
   - **Danger (`0 < distance_cm < SAFE_DISTANCE_CM`)**: LEDs Red (`255, 0, 0`), beep `rover.buzzer(880, 150)`, reverse `rover.move(-100, -100)` for `0.4`s, pivot `rover.move(100, -100)` for `0.3`s, then `rover.stop()`.
   - **Caution (`SAFE_DISTANCE_CM <= distance_cm < CAUTION_DISTANCE_CM`)**: LEDs Amber (`255, 140, 0`), slow speed `rover.move(60, 60)`.
   - **Clear (`distance_cm >= CAUTION_DISTANCE_CM`)**: LEDs Green (`0, 200, 80`), cruise speed `rover.move(100, 100)`.

## Progressive Hints
- **Hint 1 — Chained Comparisons in Python**: Python lets you write range checks naturally:
  `if 0 < distance_cm < SAFE_DISTANCE_CM:`
- **Hint 2 — Multi-Zone `if / elif / else` Structure**:
  ```python
  for sweep in range(15):
      distance_cm = rover.get_distance(port=3)
      print(f"[RADAR #{sweep + 1:02d}] {distance_cm:.1f} cm")
      if 0 < distance_cm < SAFE_DISTANCE_CM:
          # Danger zone: Red LED, buzzer, reverse & pivot
          ...
      elif distance_cm < CAUTION_DISTANCE_CM:
          # Caution zone: Amber LED, slow forward
          ...
      else:
          # Clear zone: Green LED, normal forward
          ...
      time.sleep(0.3)
  ```
- **Hint 3 — Maximum Range**: When no obstacle is within 4 meters, the ultrasonic sensor returns `400.0` cm.

## Mission Success Metrics
- Terminal prints accurate distance readings (`cm`) as you move your hand toward and away from the ultrasonic sensor.
- LEDs transition smoothly between Green (far), Amber (medium), and Red (close).
- Placing an object within 20 cm triggers the warning tone, reverse burn, and pivot turn.
- Rover stops both motors cleanly when the sweep ends.

## Flight Engineer Debrief
| Code Command | Real-World Translation |
| :--- | :--- |
| `rover.get_distance(port=3)` | Emits a 40 kHz ultrasonic pulse on Port 3, measures echo time-of-flight ($\mu\text{s} / 58.0$), and returns distance in `cm`. |
| `0 < distance_cm < 20.0` | Verifies a valid echo was received (`> 0`) inside the 20 cm hazard boundary. |
| `elif distance_cm < 40.0:` | Evaluates the secondary caution band only when the primary danger check is false. |
