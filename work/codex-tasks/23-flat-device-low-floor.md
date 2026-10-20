# Task 23 · "Sits flat" mount with a low tray floor (fit a 38.8 mm PC in 1U)

Brian (2026-10-20, equipment-wizard beta): his Dell OptiPlex Micro 7010 (182.5 × 194.5 × 38.8 mm after "X is up") is confirmed to fit 1U in a bracket someone else made, but the wizard calls it 2U. Brian chose the fix: a mount for box-shaped devices that sit flat, with a lower tray floor in that mode only. Fit stays UNKNOWN until printed; printing is not authorized.

Standing rules in [README.md](README.md) apply (no commits/pushes/exports; Claude reviews, browser-checks and commits).

## Cause (confirmed by Claude)

Height budget today, from the slot bottom: tray floor starts at `tray_z=7`, is `tray_t=3` thick (floor top 10), then `standoff=6`. 1U = 44.45, so a 1U device can be at most 28.45 mm tall. 38.8 + 6 + 10 = 54.8 → 2U.

The same rule is copied in four places:

- equipment_tray.scad: `tray_t=3; tray_z=7;`, `floor_top=tray_z+tray_t`; the screw joint hangs off `tray_z` (tongue at `tray_z+3.5`, boss/pilot at `tray_z+14`, risers to `tray_z+22`, gussets from `tray_z+2.7`); strap slots cut at `tray_z`.
- equipment.py ~223: `if s['dev_h'] + s['standoff'] + 10 > s['u'] * 44.45` (also the device lift used for port/opening Z in `allocation_spec()`).
- equipment-wizard.js ~83: `spec.u=…ceil((spec.dev_h+spec.standoff+10)/44.45)`; ~76 and ~104 `lift=10+(straps?0:standoff)`.
- tray-placement.js ~10 `TRAY_Z=7,TRAY_T=3`, ~32 lift, ~68 U check, ~96 preview boxes.
- port-openings.js (and cable-ports.js if it uses the lift): front-opening Z follows the device lift.

Small bug in the same code: the "straps" mount has no standoffs (the device sits on the floor, as the .scad and the lift formulas already say), but the U checks in equipment.py, the wizard and tray-placement.js still add `standoff`. Fix that too.

## Build

1. New mount `flat` ("Sits flat on the tray (PCs, boxes)") alongside inserts / pegs / clips / straps. No standoffs, no holes required. The device rests on the floor; it is held by low side rails or corner stops (keep them under the device's own height, e.g. 6 × 6 mm corner stops like the clips mode uses, and leave strap slots so it can also be strapped). Keep it simple; say in the report what holds it.
2. Floor height becomes a parameter: `floor_z` (replaces the hard-coded `tray_z=7`). Default stays 7 for every existing mount, so **every existing saved spec renders byte-identically** (add a test that a default spec's generated .scad text matches the current output exactly). For `flat`, use the lowest floor that keeps the screw joint working inside the faceplate (the joint geometry moves with `floor_z`) and keeps the tray bottom above the slot's lower boundary; pick the value from the geometry, explain it in the report, and keep `tray_t=3` unless a thinner floor is clearly needed. Target: a 38.8 mm device fits 1U (floor top ≤ 44.45 − 38.8 = 5.65).
3. One shared height rule: `needed height = floor_z + tray_t + (standoff if mount uses standoffs) + dev_h`. Use it in equipment.py, the wizard (auto U), tray-placement.js (U check, lift, preview boxes) and port-openings / cable-ports wherever the lift is used. Mounts that use standoffs: inserts, pegs, clips (check the .scad). straps and flat: none.
4. Wizard: when the imported model would fit fewer U with `flat`, show one short line on step 1, e.g. "Fits 1U if it sits flat (no standoffs). Choose 'Sits flat' under Mounting." Don't switch the mount automatically. Show the needed height vs the U height in that line.
5. Update the asset-manifest.json sha256 for every changed front-end file (CRLF normalized to LF; a test checks this). If app.py needs to serve a new file, add it (it serves an explicit list).

## Tests

- Python: U rule for each mount (inserts adds standoff; straps/flat don't); a 182.5 × 194.5 × 38.8 `flat` spec validates as 1U; same spec with inserts needs 2U; default spec .scad output unchanged.
- JS: wizard auto-U and the hint; tray-placement U check and lift for `flat`; front-opening Z follows the lower floor.
- Do NOT run STL exports. A render test inside a disposable temp folder is allowed only if the existing tests already do that.

## May change

equipment_tray.scad, equipment.py, equipment-wizard.js, tray-placement.js, port-openings.js, cable-ports.js (only if it uses the lift), asset-manifest.json, test_*.py and js-tests/ for the tests above (register new JS tests in js-tests/run.js). Nothing else. Never touch data/normal-use.

## Checks

Before and after, report exact results:

```
powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1
```

Do not start or stop servers. Claude checks it in the browser afterwards with the OptiPlex STEP.

## Report

work/codex-tasks/23-flat-device-low-floor-REPORT.md: files changed with before/after SHA-256, the chosen `floor_z` for `flat` and why (joint clearance, slot boundary), what holds the device, check results, open questions. Fit and strength stay UNKNOWN.
