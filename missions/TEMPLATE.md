# Your Mission Title Here

## Story Briefing
Write a 2–3 sentence narrative hook setting the scene on Mars in the Ares VII basin. Explain why the rover needs this subsystem calibrated or programmed.

## Primary Objectives
- **Baseline Check**: Describe the first milestone.
- **Subsystem Verification**: Describe the second milestone.
- **Field Challenge**: Summarize what the learner will implement in the `# TODO` section.

## Systems Check
- **Umbilical Line**: USB cable connected.
- **Sensor / Actuator Port**: Specify which mCore RJ25 port (`Port 1..4`) or motor port (`M1`/`M2`) is used.

## Field Challenge
Describe the instructions for opening the starter `.py` script in Thonny, running the pre-flight unit test (`test_*.py`), and completing the `# TODO` challenge block.

## Progressive Hints
- **Hint — Concept Name**: Give a small syntax snippet or parameter tip.
- **Hint — Loop or Conditional Tip**: Show how the building block fits together without giving away the entire solution.

## Mission Success Metrics
- Pre-flight unit test passes in Thonny (`▶ Run`) or `pytest`.
- Observable checkpoint in the terminal or on the physical rover.
- Field Challenge verified.

## Flight Engineer Debrief
| Code Command | Real-World Translation |
| :--- | :--- |
| `rover = mbot()` | Connects to the mBot over USB serial. |
| `rover.rgb_led(0, 0, r, g, b)` | Sets both onboard RGB LEDs to `(r, g, b)`. |
