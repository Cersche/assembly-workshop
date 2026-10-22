# Task 37 · Rack view: feet clip through the floor

Brian (2026-10-22, screenshot, see `work/notes/2026-10-22-feet-floor-and-wall-box-wizard.md`): in the 3D rack view the feet (round pads) sit through / below the dark floor plane.

Claude's diagnosis: `rack-studio.js` line ~136 builds the floor at a fixed height, `floor.box(-900,900,-700,900,-43,-42)` (top at Z = -42). The mesh viewers (`assembly-studio.js` ~37, `viewer.js` ~74) instead put the floor top 0.65 mm below the scene's lowest point. The foot meshes very likely reach below Z = -42. Not yet measured: confirm first.

Standing rules in [README.md](README.md) apply. Preview only: no change to any STL, SCAD, rack STL export, foot placement data or saved data.

## Build

1. Measure: on disposable data, log the lowest Z of every scene part (feet, posts, panels) for a rack with feet. Record it in the report.
2. Fix: put the floor top just under the lowest point of the rack's visible parts (same 0.65 mm gap as `viewer.js`), recomputed when the scene changes (rack height, feet on/off). Keep the floor's X/Y extent and look. Update anything that assumes the floor is at -42 (e.g. the floor fade `uFloorParams`, shadow framing, the pick ray's `-3` plane only if it is meant to be the floor; leave it if it isn't, and say which).
3. Do not move the feet or any rack part: they are where the source meshes put them.

## May change

`rack-studio.js`, `workspace.js` (only if the scene min Z must be passed in), `js-tests/` (register in `js-tests/run.js`), `asset-manifest.json`. Nothing else.

## Tests

- Pure helper: given part bounds, the floor top = min Z − 0.65; with no parts, it falls back to -42.
- A rack with feet: no foot vertex is below the floor top.

## Checks and report

Run `run_checks.ps1` before and after. Browser check on disposable data only (temporary `--data` folder, spare port 8700–8899; never data/normal-use, never stop the app on 8765): front and low-angle screenshots before/after showing the feet resting on the floor, with and without feet if that's an option. Write `work/codex-tasks/37-rack-floor-feet-REPORT.md` with files + SHA-256, the measured Z values, screenshots and open questions. Do not commit; Claude reviews.
