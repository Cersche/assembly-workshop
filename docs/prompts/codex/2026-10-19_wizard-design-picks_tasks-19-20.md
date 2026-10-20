# Codex prompt · 2026-10-19 · Wizard design picks (tasks 19–20)

Paste this into Codex:

```
Do work/codex-tasks/19-front-openings-logic.md, then work/codex-tasks/20-adapter-cable-warning.md. Follow the standing rules in work/codex-tasks/README.md. Write both REPORT files, then stop. Do not run or change task 18. Note: before task 19, run_checks fails with "No module named 'port_openings'" because Claude's integration in equipment.py already imports it; creating port_openings.py fixes that. Also expected: test_tray_placement.py FrontOpeningsFollowTheDevice needs both of your modules; do not edit it, report any failure.
```

What it does: task 19 writes the pure math that moves faceplate front openings with the device (plus the warning when it is turned, the opening guards, and the starting opening size per port type) in JavaScript and Python with tests. Task 20 adds the "needs an adapter cable" warning to the existing cable modules (Cable panel, wiring sheet, suggestions, parts order). Claude wires both into the app afterwards. Background: [E2E_Acceptance_Report.md](../../../work/equipment-wizard-options/E2E_Acceptance_Report.md), Brian's picks 2026-10-19.
