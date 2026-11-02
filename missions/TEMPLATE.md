# Mission XX: Your Mission Title Here

- **Badge**: Short Subsystem Tag (e.g., Servo Arm / IR Remote)
- **Script**: template_mission.py
- **Requires Battery**: false

## Story Briefing
Write a 2–3 sentence narrative hook setting the scene on Mars in the Ares VII basin. Explain why the rover needs this subsystem calibrated or programmed.

## Primary Objectives
- **Objective 1**: Describe the first milestone.
- **Objective 2**: Describe the second milestone.
- **Field Challenge**: Summarize what the learner will implement in the `# TODO` section.

## Systems Check
- **Umbilical Line**: USB cable connected.
- **Sensor / Actuator Port**: Specify which mCore RJ25 port (`Port 1..4`) or motor port (`M1`/`M2`) is used.

## Field Challenge
Describe the step-by-step instructions for opening the starter `.py` script in Thonny, running Phase 1, and completing the `# TODO` challenge block.

## Progressive Hints
- **Hint 1 — Concept Name**: Give a small syntax snippet or parameter tip.
- **Hint 2 — Loop or Conditional Tip**: Show how the building block fits together without giving away the entire solution.

## Mission Success Metrics
- Observable checkpoint 1 (what prints in the terminal).
- Observable checkpoint 2 (what lights up, beeps, or moves on the rover).
- Field Challenge verified.

## Flight Engineer Debrief
| Code Command | Real-World Translation |
| :--- | :--- |
| `rover = mbot()` | Connects to the mBot over USB serial. |
| `rover.rgb_led(0, 0, r, g, b)` | Sets both onboard RGB LEDs to `(r, g, b)`. |
