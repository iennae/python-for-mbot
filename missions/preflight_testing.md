# Digital Twin & Pre-Flight Unit Testing

## Story Briefing
In real space missions, flight engineers never beam untested navigation code straight to Mars—a single typo could drive the rover off a crater rim or drain its battery! Before Flight Control unlocks the rover's drive thrusters, you must learn to validate your Python functions against the **Mars Digital Twin Simulator (`mbot(simulate=True)`)** using automated **`assert` unit tests**.

## Primary Objectives
- **Digital Twin Simulation**: Create an in-memory simulated rover (`rover = mbot(simulate=True)`) that runs on your laptop even when the physical mBot is unplugged.
- **Inspect `rover.command_log`**: Verify which commands (`rgb_led`, `buzzer`, `move`, `stop`) your code sent to the rover.
- **Field Challenge**: Complete the low-battery emergency cutoff branch in `evaluate_battery_safety(rover, voltage)` and write unit test assertions in `missions/test_preflight_testing.py` to prove the rover stops and lights a Red warning beacon when voltage drops below `6.0` V.

## Systems Check
- **Hardware Optional**: Because `mbot(simulate=True)` uses the Digital Twin loopback simulator, you can run this mission with or without the mBot plugged in!
- **Two Ways to Run Tests**:
  - In **Thonny**: Open `missions/test_preflight_testing.py` (or `missions/preflight_testing.py`) and press **▶ Run (`F5`)**.
  - In a **Terminal**: Run `pytest missions/test_preflight_testing.py`.

## Field Challenge
Open `missions/preflight_testing.py` and `missions/test_preflight_testing.py` in Thonny:
- In `missions/preflight_testing.py`, inspect `evaluate_battery_safety(rover, voltage)`. Right now it handles healthy battery voltage (`>= 6.0` V), but the low-voltage branch (`< 6.0` V) has a `# TODO`:
  - Call `rover.stop()` to halt the motors immediately.
  - Set the onboard LEDs to Red (`rover.rgb_led(0, 0, 255, 0, 0)`).
  - Return `"CRITICAL_LOW"`.
- Then open `missions/test_preflight_testing.py` and press **▶ Run (`F5`)** to verify that both healthy and low-voltage unit tests pass!

## Progressive Hints
- **Hint — How `mbot(simulate=True)` Works**: Passing `simulate=True` creates a virtual rover in memory. Every time your code calls `rover.rgb_led(...)` or `rover.stop()`, the simulator appends a dictionary to `rover.command_log`.
- **Hint — Completing the Low-Voltage Branch in `preflight_testing.py`**:
  ```python
  if voltage < MIN_SAFE_VOLTAGE:
      rover.stop()
      rover.rgb_led(0, 0, 255, 0, 0)
      return "CRITICAL_LOW"
  ```
- **Hint — Writing `assert` Checks in `test_preflight_testing.py`**:
  ```python
  actions = [entry["action"] for entry in rover.command_log]
  assert "stop" in actions
  ```

## Mission Success Metrics
- Pressing **▶ Run (`F5`)** on `missions/preflight_testing.py` simulates both a healthy `7.4` V check and a low `5.4` V check and prints the recorded `rover.command_log`.
- Completing the `# TODO` in `evaluate_battery_safety` causes low voltage (`< 6.0` V) to call `rover.stop()`, set Red LEDs (`255, 0, 0`), and return `"CRITICAL_LOW"`.
- Pressing **▶ Run (`F5`)** on `missions/test_preflight_testing.py` (or running `pytest`) passes all pre-flight assertions with `✅ [PASS]`.

## Flight Engineer Debrief
| Code Command | Real-World Translation |
| :--- | :--- |
| `rover = mbot(simulate=True)` | Launches the in-memory Digital Twin simulator so you can test code without spinning physical motors. |
| `rover.command_log` | A list of dictionaries recording every command sent to the rover (e.g., `{"action": "stop", "left": 0, "right": 0}`). |
| `rover.set_simulated_sensor("distance", 12.0)` | Injects a fake sensor reading into the Digital Twin to test how your code reacts to obstacles or darkness. |
| `assert status == "CRITICAL_LOW"` | Raises an `AssertionError` immediately if the function returned the wrong value, catching bugs before flight. |
