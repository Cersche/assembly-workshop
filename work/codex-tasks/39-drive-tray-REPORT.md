# Task 39 report — Drive tray (3.5" HDD + 2.5" SSD)

Codex wrote most of the implementation, then ran out of usage mid-regression. Claude finished, verified and committed it (2026-10-22).

## What changed
- `equipment_tray.scad`: opt-in `// @drives-begin … @drives-end` block (`drives`, `drive_mount`, `ssd_h`, `drive_add`, `drive_cut`); tray() calls it only when `drives` is non-empty.
- `equipment.py`: `clean_drives` (one 3.5 + one 2.5, 8 mm gap, ≤ 204 mm wide, ≤ 240 mm deep incl. 25 mm rear connector space, 1U blank plate, screw joint), `drive_hardware`, `DRIVE_LIMITS`. With no drives the block is stripped, so source bytes are unchanged.
- `equipment-wizard.js`: "Drives (3.5" + 2.5")" button on the first step; mount selector (Bottom screws default / Tool-free sleeve experimental), SSD 7 / 9.5 mm. `asset-manifest.json` hash updated.
- Tests: `test_drive_tray.py` (4 tests), registered in `work/gui-refinement/check_python.py`.

## Geometry (PROPOSED — UNVALIDATED)
- Positions from SFF-8301 (3.5") and SFF-8201 (2.5") PDFs saved in `work/task39-checks-20261022/`. Bottom holes are measured from the connector end in the spec, so the spec values in the task file (41.28 / 85.72 from front) were wrong; the code uses 3.5" Y 29.52 / 61.27 / 105.72 and 2.5" Y 9.4 / 86 from the front, connectors facing the rear.
- Screws: 3 mm pads, clearance holes plus counterbores from below. Nominal thread engagement 2.85 mm (6-32 × 1/4") / 1.5 mm (M3 × 4). Vent slots under the HDD, ≥ 3 mm from holes.
- Sleeve: 2 mm side rails, 0.5 mm play, front stop, open rear; one cantilever tab per side with a smooth 2.4 mm peg engaging about 1 mm into the drive's side hole.
- Width 195.45 mm (8.55 mm margin to 204). Depth 184 mm incl. 25 mm behind the HDD (56 mm margin to the 240 mm nominal frame depth; usable depth UNKNOWN).

## Checks
- `run_checks.ps1`: all pass (187 Python incl. 4 new, all JS).
- Regression (Router, Switch, Window, Sleeve; tray + faceplate): SCAD source byte-identical; STLs contain the same facets. OpenSCAD wrote Router's facets in a different order, so the check compares sorted lines, not raw SHA-256.
- Screws and sleeve modes: assembly, tray, faceplate and combined all render and read as closed meshes (`renders.json`).
- Not done: rack-view screenshot of each mode (skipped to save usage); hole positions not measured on the mesh, only set from the spec in code.

## UNKNOWN
Fit on real drives, peg retention and tab fatigue, screw engagement and torque, vibration, airflow and temperature, strength, usable rack depth. Nothing printed. Any test print needs a modeled ID (e.g. DRV39-A).

## Update 2026-10-22: tool-free sleeve removed (Brian)
Brian dropped the tool-free sleeve. Drives mount with bottom screws only; `drive_mount="sleeve"` is rejected and the sleeve SCAD code is gone. The renders in `sleeve/` are history. Screws-only tray re-rendered closed (`screws-only/`); checks pass (187). The OptiPlex `device_mount="sleeve"` is unrelated and untouched.
