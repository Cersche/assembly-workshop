# Task 38 · Wall-mount box: parametric SCAD template + Python spec (no GUI yet)

Brian (2026-10-22) wants a separate wall-mount box wizard (indoor, NID-box style). Scope and decisions: [work/wall-box-wizard/Scope.md](../wall-box-wizard/Scope.md). This task builds only the geometry back end; the wizard GUI is a later task.

Standing rules in [README.md](README.md) apply. New adapter: PROPOSED — UNVALIDATED. Fit, hinge/latch/snap function, wall load and strength stay UNKNOWN. No change to existing templates (`equipment_tray.scad` etc.), existing specs, saved data or exports. Python 3.10 stdlib, UTF-8.

## Build

1. **`wall_box.scad`** (new, next to `equipment_tray.scad`): box body + lid as separate parts (`part = "body" | "lid" | "cleat" | "all"`). Parameters:
   - inner W/D/H; wall thickness (default 2.5, a parameter, not a recommendation); corner radius; outer size must be ≤ 250 mm on every axis (assert).
   - `lid_style`: `screw` (M3 heat-set insert bosses in the body corners, matching clearance holes in the lid; reuse the project's existing M3 insert numbers, do not invent new ones), `hinge` (print-in-place-free two-part pin hinge on one long edge + a latch on the opposite edge), `snap` (perimeter lip with snap tabs).
   - `mount_style`: `keyhole`, `tabs`, `cleat` (45° cleat on the box back + a separate `cleat` rail part with screw holes). One per box.
   - `vents`: per wall (left/right/top/bottom/back/lid) on/off; slot vents kept clear of other features.
   - `cutouts`: list of openings on any wall: `keystone` (use the golden keystone geometry, ks_tight 0.2, unchanged), `gland` (PG7 / PG9 clearance holes), `round` (d), `rect` (w×h), each with wall + position.
   - `standoffs`: list of (x, y, height, hole) on the inside back for boards/devices.
2. **`wall_box.py`**: validate a JSON spec (ranges, 250 mm limit, cutouts inside their wall with ≥ 2 mm margin, no cutout overlapping another cutout, vent zone, boss or mount feature), produce the SCAD source deterministically, plain-language error messages. Unknown keys rejected.
3. **Parts presets** (`wall_box_parts.json`): keystone, PG7, PG9, barrel jack (5.5/2.1 panel), USB-C panel, rocker switch, ScreenBeam ECB7250 entry with **dimensions `null` / UNKNOWN** (Brian will measure; never guess). Each preset says what cutout or standoff pattern it makes.

## May change

New files only: `wall_box.scad`, `wall_box.py`, `wall_box_parts.json`, `test_wall_box.py`, registration in `run_checks.ps1` if tests are auto-discovered there. Nothing else; never data/normal-use.

## Tests

- Validation: 250 mm limit, overlapping cutouts, cutout too close to an edge, unknown key, ECB7250 with null size refused as a sized part.
- Determinism: same spec → byte-identical SCAD.
- Render (opt-in like `AW_RENDER_TESTS=1`): one spec per lid style × mount style renders with OpenSCAD.exe to closed meshes; body + lid volumes reported.

## Checks and report

`run_checks.ps1` before and after. Render the 9 lid × mount combinations once (OpenSCAD.exe) into a temporary folder, plus one box with vents, two keystones, a PG9 gland and four standoffs; screenshots/PNG renders of each. No printing. Write `work/codex-tasks/38-wall-box-template-REPORT.md`: files + SHA-256, test results, render table (closed? volume), images, open questions. Do not commit; Claude reviews.
