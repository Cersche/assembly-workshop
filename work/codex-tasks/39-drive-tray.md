# Task 39 — Drive tray: 3.5" HDD + 2.5" SSD on one tray (blank faceplate)

Status: SPEC (Claude, 2026-10-22). Brian's direction: both drives on one tray if it makes sense; bottom screws as default, tool-free sleeve offered as a choice to compare; blank faceplate.

## Goal
Add drive mounting to the generic `equipment_tray.scad` path (no new manufacturing adapter) so the app can make one 1U tray carrying a 3.5" HDD and a 2.5" SSD side by side, with a blank faceplate. Two mount styles are selectable:
- `drive_mount="screws"` (default): bottom-screw clearance holes + countersink/counterbore from below, drives sit on 3 mm pads.
- `drive_mount="sleeve"`: tool-free U-channel per drive: side walls with rails that engage the drive's side screw holes via printed pegs on a flexing tab (one tab per side, near the rear), front stop, open rear for SATA. Keep the existing `device_mount="sleeve"` (OptiPlex) code path untouched; this is a separate drive sleeve.

## Drive data (standard spec values, PROPOSED until Brian measures)
- 3.5": 101.6 W × 147 D × 26.1 H. Bottom holes 6-32: X 3.18 and 98.43 from left edge; Y 41.28, 85.72 (and 3rd row 44.45 apart not needed) from front. Side holes: Z 6.35, Y 28.5 / 70.0 / 129.6 from front.
- 2.5": 69.85 W × 100 D × 7 H (allow 9.5 via parameter). Bottom M3: X 4.07 and 65.73; Y 14.0 and 90.6 from front. Side M3: Z 3.0, Y 14.0 / 90.6.
Codex: verify these against SFF-8301 / SFF-8201 from a public source and cite it in the report; if any differ, use the spec and list the change.

## Layout
- Rack inner width 208, max tray 204 (`max_tray`). HDD + SSD = 171.45 mm; choose gap/walls so the total fits ≤ 204 in both modes. If the sleeve mode cannot fit both, report it and fall back to a clear check failure (no silent overlap).
- HDD front edge sits `front_gap` behind the faceplate; rear ≥ 25 mm SATA/power clearance kept clear of joints, feet and rear bracket. Check total depth against `rack_depth=240` and report the margin; usable depth stays UNKNOWN.
- 1U, blank faceplate (no ports/keystones), standard 44.4 mm plate, four-corner slots, existing screw joint.
- Floor vent slots under the HDD (airflow), kept clear of screw holes by ≥ 3 mm.

## Files
- `outputs/Mechanical_Design_App/equipment_tray.scad` — new params `drives=[]` (list of `[type,x_off,y_off]`, type "3.5"/"2.5"), `drive_mount`, `ssd_h`. Empty `drives` must produce byte-identical output to today for existing items.
- `equipment.py` / `equipment-wizard.js` — wizard preset "Drives (3.5" + 2.5")" filling `drives`, mount style selector, faceplate blank. Hardware list: 4× 6-32 × 1/4" + 4× M3 × 4 for screws mode; none for sleeve.
- Tests: new `test_drive_tray.py` + JS test for the preset; follow existing test style.

## Acceptance checks
1. All existing Python and JS tests pass (commands in PROJECT.md/HANDOFF.md).
2. Regression: render 3 existing library items with `drives=[]` → STL hashes identical to before the change (record before/after hashes).
3. Render both modes (OpenSCAD.exe on the PC; if unavailable, say so) as `assembly`, `tray`, `faceplate`, `combined`: closed manifold, no overlap with drive envelopes, holes within 0.1 mm of spec positions, tray width ≤ 204.
4. Preview screenshot of each mode in the rack view, using NEW disposable data (never data/normal-use).
5. Report: depth margin, width margin, any spec corrections, every UNKNOWN (fit, peg retention, tab fatigue, vibration, strength).

## Do not
- Touch data/normal-use, old revisions, the OptiPlex sleeve, keystone defaults, or Print in color.
- Print, export to users, push, or regenerate historical evidence.
- Mark fit or strength as passed. Label output PROPOSED — UNVALIDATED.
- Add a test print without a modeled unique ID (e.g. DRV39-A/B).
