# Task 25 · 44.4 mm faceplate becomes the standard (and fix the slot offset)

Brian, 2026-10-20: he printed coupons FP44-A..D (`outputs/Physical_Test_Coupons_2026-10-20_FP44_plate_height/`) and reports a perfect fit: "Coupons will be our new standard." From now on, every new faceplate is **44.4 mm tall per 1U**, not 42. Width (252), thickness (4), corner radius (2.5) and the four-corner rack slots (10 × 7 capsules at x = ±118.2625, ±15.902 from each U's centre) stay exactly as they are. Fit beyond those specimens and strength stay UNKNOWN.

Standing rules in [README.md](README.md) apply.

## Background (found by the coupon session, checked by Claude)

- On the real rack the plate is **centred in its slot**. The slot boundary is at plate Z −1.225 / 43.225 today, but most code treats plate Z=0 as the slot bottom.
- Consequences today:
  - The rack views draw wizard plates 1.225 mm too low against the post holes (`equipment-wizard.js` ~459, `rack-studio.js` ~169). Cable guides and slot middles already use the centred position (`rack-scene.js` guidePose, `workspace.js` ~1226).
  - The height check (`equipment.py` ~260 `needed_height(s) > u*44.45`, and the JS copies in `port-openings.js` / `tray-placement.js`) lets a device poke up to 1.225 mm into the next U.
  - Task 23's flat `floor_z=0.5` is really 1.725 mm above the slot bottom.

## Build

1. **One coordinate rule:** Z=0 is the slot bottom, in SCAD, Python and JS.
   - The plate spans `plate_gap/2` to `u*44.45 − plate_gap/2`, with `plate_gap = 0.05` (44.4 per 1U; `plate_h = u*44.45 − 0.05`).
   - Rack slots are centred in each U: `i*44.45 + 22.225 ± hole_dz`. That is the same rack position as today, just in the new frame.
   - Replace every hard-coded `−2.45` / `+21` plate formula. The coupon session found them in: `equipment_tray.scad:35,70`, `equipment.py:266`, `port_openings.py:47`, `port-openings.js:33`, `tray-placement.js:33`, `cable-ports.js:41`, `equipment-wizard.js:185,199`, `viewer.js:198`, `rack-studio.js:13`. Grep for more.
   - Use one named constant per language, not a repeated literal.
2. **Tray floors keep their real height in the rack.**
   - For every existing mount except `flat`, the device must end up at the same height above the true slot bottom as today. That means old `floor_z` 7 becomes 8.225 in the new frame. Check it the same way for standoffs and the joint.
   - For `flat`, use 0.5 mm above the true slot bottom. That is the clearance task 23 intended.
   - Keystone blocks, ports, the joint tongue/boss/riser and strap slots follow the plate and floor. The golden keystone geometry itself must not change; only its centre moves with the plate centre.
3. **Height check:** the device top (plus anything the tray adds above it) must stay ≤ `u*44.45` measured from the true slot bottom. Same rule in Python and JS.
4. **Rack views:** draw wizard plates and trays at the true position, so the plate slots line up with the post holes.
5. **Port/keystone limits** that depend on plate height (`equipment.py:277-280`, `port_openings.py:56-60`, `port-openings.js:38-39`) use the new plate extent.
6. **Old saved revisions stay as they are.** Don't rewrite saved data or revision folders. Rebuilding an old saved spec (rebuild copy, or a new build) gives the 44.4 plate; that is intended. Remove or adjust the task 23 "byte-identical legacy source" compatibility path only where it now contradicts the new standard, and say exactly what you did. The archived historical evidence stays untouched.
7. **Print in color** (`faceplate_color.py`) is not offered for wizard faceplates. Don't change it; note in the report whether anything reachable still assumes 42 mm.
8. Update asset-manifest.json hashes for changed front-end files (LF-normalized).

## Tests

- A 1U plate's bounding box is X ±126, Z 0.025 to 44.425; 2U is Z 0.025 to 88.875.
- Slot centres are at 6.323 / 38.127 (1U).
- The device height in the rack is unchanged for the inserts/pegs/clips/straps fixtures.
- `flat` tray bottom is at 0.5.
- The OptiPlex `flat` spec (182.5 × 194.5 × 38.8, 1U) still validates.
- A device that would poke into the next U is rejected.
- Rack-view placement lines up the slots with the post holes.
- Update the tests that expect 42 mm (`js-tests/run.js`, `js-tests/tray-placement.js`, `js-tests/flat-floor.js`, `js-tests/cable-sheet-view.js`, `test_tray_placement.py`, and others you find).
- No STL exports.

## May change

`equipment_tray.scad`, `equipment.py`, `port_openings.py`, `port-openings.js`, `tray-placement.js`, `cable-ports.js`, `equipment-wizard.js`, `viewer.js`, `rack-studio.js`, `rack-scene.js` and `workspace.js` (only for plate/tray placement), `asset-manifest.json`, `test_*.py`, `js-tests/`. Nothing else. Don't touch `faceplate_mounting.json` (it is source evidence; it says "matching 42 mm height"; note it in the report), `faceplate_color.py`, `rack_stl.py`, the coupon folder or data/normal-use.

## Checks and report

Run `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1` before and after. Write `work/codex-tasks/25-faceplate-44-standard-REPORT.md` with:
- files changed with before/after SHA-256;
- the new constants and where they live;
- every place you changed `floor_z` or the joint, with old → new rack heights;
- the check results;
- open questions.

Claude browser-checks afterwards.
