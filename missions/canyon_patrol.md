# Canyon Conduit Navigation

## Story Briefing
You have cleared the boulder field and reached the Ares VII thermal conduit—a high-contrast guide track leading across the canyon floor to the main habitat. Decode the dual infrared reflective sensors underneath the rover (`Port 2`) to steer along the track automatically without drifting off course.

## Primary Objectives
- **Decode Sensor States (`0..3`)**: Read the dual IR line-follower sensor (`rover.get_line_follower(port=2)`) over dark track vs. light ground.
- **Proportional Steering**: Adjust left and right wheel speeds independently to recenter the rover when one sensor crosses the edge of the line.
- **Field Challenge**: Build a 4-state navigation loop that follows a curved dark track and backs up slowly if the track is lost.

## Systems Check
- **Line-Follower Module**: Plugged into RJ25 **`Port 2`** underneath the front of the mBot.
- **Track Surface**: Use the black figure-8 track map included with the mBot kit (or dark electrical/painter's tape on a light floor/posterboard).
- **Battery Power**: Battery pack connected and chassis switch **`ON`**.

## Field Challenge
Open `missions/canyon_patrol.py` and test the baseline readout by placing the rover over the dark line, slightly left, slightly right, and off the line to see all 4 states (`0`, `1`, `2`, `3`)—and run `missions/test_canyon_patrol.py` to test in simulation! Then complete the **Field Challenge (`# TODO`)** section:
- **`state == 0` (Both sensors on dark line)**: Both LEDs Green, drive straight `rover.move(100, 100)`.
- **`state == 1` (Left on line, Right off line — drifting right)**: Left LED Green (`slot=1`), Right LED off (`slot=2`), steer left `rover.move(40, 110)`.
- **`state == 2` (Left off line, Right on line — drifting left)**: Left LED off (`slot=1`), Right LED Green (`slot=2`), steer right `rover.move(110, 40)`.
- **`state == 3` (Both sensors off line)**: Both LEDs Amber (`255, 80, 0`), reverse slowly `rover.move(-80, -80)` to re-acquire the line.

## Progressive Hints
- **Hint — Why Do We Use `int(...)`?**: `rover.get_line_follower(port=2)` returns a float (`0.0`, `1.0`, `2.0`, or `3.0`). Wrapping `int(rover.get_line_follower(port=2))` makes exact integer comparisons (`state == 0`) clean and readable.
- **Hint — Gentle Steering vs. Sharp Spin**: Slowing the inside wheel (`rover.move(40, 110)`) produces a smooth curve along the line, whereas reversing the inside wheel (`rover.move(-80, 110)`) handles tight corners.
- **Hint — Faster Polling**: Keep `time.sleep(0.15)` or `0.2` short so the rover checks the line 5–6 times per second!

## Mission Success Metrics
- Pre-flight test `missions/test_canyon_patrol.py` passes in Thonny (`▶ Run`) or `pytest`.
- Initial sensor readout prints `0` when both IR sensors sit over the black line and `3` when both sit over white background.
- Rover drives straight ahead with both LEDs green when centered (`State 0`) and smoothly steers left (`State 1`) or right (`State 2`) on curves.
- Rover reverses slowly (`State 3`) if pushed completely off the track and halts cleanly when the patrol loop ends.

## Flight Engineer Debrief
| Code Command | Real-World Translation |
| :--- | :--- |
| `rover.get_line_follower(port=2)` | Reads the 2-bit digital state (`s1 * 2 + s2`) of the Left and Right infrared reflectance sensors on Port 2. |
| `state == 1` | Binary `01`: Left IR detector sees dark non-reflective surface (`0`), Right IR detector sees bright reflective surface (`1`). |
| `rover.move(40, 110)` | Drives the right wheel faster than the left wheel, curving the rover gently to the left back onto the conduit. |
