# Mission 02: Drive Thruster Calibration

- **Badge**: Differential Mobility & Braking
- **Script**: mission_02_thrusters.py
- **Requires Battery**: true

## Story Briefing
Heartbeat confirmed, Cadet! Before driving off the landing pad into the Ares VII basin, Flight Control needs you to calibrate the port (`M1`) and starboard (`M2`) drive thrusters, test reverse retro-burns, and verify that the emergency parking brake halts the rover on command.

## Primary Objectives
- **Forward Burn**: Test positive motor thrust (`rover.move(120, 120)`) on a test stand first.
- **Reverse Retro-Burn**: Use negative motor speeds (`rover.move(-120, -120)`) with an amber warning beacon.
- **Differential Pivot**: Spin one wheel forward and the opposite wheel backward to rotate in place.
- **Field Challenge**: Program the rover to trace a 4-sided perimeter around the landing pad and come to a full stop.

## Systems Check
- **Battery Power Required**: Battery pack plugged in and mBot chassis switch toggled **`ON`** *(USB power alone will not spin the drive motors!)*.
- **Rover Test Stand**: Prop the rover's wheels off the desk on a small box for your first run so it doesn't drive off the table.
- **Motor Cables**: Left motor connected to `M1`, Right motor connected to `M2`.

## Field Challenge
Open `missions/mission_02_thrusters.py` and run Phase 1 with the wheels propped on your test stand. Then complete **Phase 2 (`# TODO`)**:
1. Add a 1.0-second reverse burn (`rover.move(-120, -120)`) with amber LEDs (`255, 140, 0`).
2. Add a starboard pivot turn (`rover.move(120, -120)`) where the left LED (`slot=1`) is green and the right LED (`slot=2`) is blue.
3. **Bonus**: Place a `for side in range(4):` loop to drive forward and pivot 90 degrees four times to trace a square!

## Progressive Hints
- **Hint 1 — Reverse Speeds**: Passing negative numbers (`-100` to `-255`) reverses the DC motor polarity: `rover.move(-120, -120)`.
- **Hint 2 — Zero-Radius Pivot Turn**: Passing opposite signs (`rover.move(120, -120)`) spins the left wheel forward and the right wheel backward so the rover pivots on its center point. Adjust `time.sleep(0.55)` until the turn is roughly 90 degrees on your floor surface.
- **Hint 3 — Individual Turn-Signal LEDs**: Use `rover.rgb_led(0, 1, 0, 255, 0)` for the left LED (`slot=1`) and `rover.rgb_led(0, 2, 0, 0, 255)` for the right LED (`slot=2`).

## Mission Success Metrics
- With the battery switch `ON`, both wheels spin forward during Phase 1.
- Reverse burn spins both wheels backward while lighting the amber beacon.
- Pivot command rotates the rover in place with left/right turn-signal LEDs.
- `rover.stop()` halts both motors completely at the end of the script (and if `Ctrl+C` is pressed).

## Flight Engineer Debrief
| Code Command | Real-World Translation |
| :--- | :--- |
| `rover.move(120, 120)` | Applies ~47% forward PWM power (`120` out of `255`) to both the left (`M1`) and right (`M2`) drive motors. |
| `rover.move(-120, -120)` | Reverses the H-bridge polarity to drive both wheels backward. |
| `rover.move(120, -120)` | Differential steering: left wheel drives forward while right wheel drives in reverse, pivoting the chassis right. |
| `rover.stop()` | Shortcut for `rover.move(0, 0)` — cuts power to both drive motors immediately. |
