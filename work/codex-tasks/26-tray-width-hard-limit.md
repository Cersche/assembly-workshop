# Task 26 · Block trays wider than the rack opening (and suggest rotating)

Do this after task 25 (it builds on the same files).

Brian, 2026-10-20 (OptiPlex beta): the wizard made a 210.5 mm tray for a rack whose inside width is 208 mm. That was a warning only. The hard limit is 230 mm (`MAX_TRAY=230` in `tray-placement.js:10`, the 230 checks in `equipment.py` ~203/~240, `assert(tray_w<=230)` in `equipment_tray.scad`, and `spec.dev_w>230` in `equipment-wizard.js` ~135). The 208 mm screen in `equipment-wizard.js` ~186 is only a heads-up. Cause and study: `work/optiplex-bracket-study/Report.md`.

Standing rules in [README.md](README.md) apply.

## Build

1. **New hard limit:** the tray (and later any sleeve walls, task 27) must be ≤ `RACK_INNER_W − 2*SIDE_CLEAR`.
   - `RACK_INNER_W = 208` (Lab Rax nominal) and `SIDE_CLEAR = 2` mm per side, so 204 mm. These are PROPOSED defaults; Brian may change the 2 mm. Keep them as named constants in one place per language.
   - Same rule in Python (clean/validate), JS (wizard steps, Place on tray, placement checks) and SCAD (assert).
   - The message is plain language with the numbers, e.g. "This tray is 210.5 mm wide but the rack opening allows 204 mm (208 mm minus 2 mm each side). Try Rotate 90°, or move the device less far sideways."
2. **Suggest rotating:**
   - In the wizard's step 1, when the imported footprint is too wide but the rotated one (width ↔ depth) would fit, say so in one short line: "Too wide this way round; it fits if you press Rotate 90°."
   - In Place on tray, give the same hint for `dev_rot`.
   - Never rotate automatically.
3. **Offsets:** the existing left/right offset limit (`dev_off_x`) uses the same new maximum.
4. **Old saved items:** saved specs that are now too wide still load and show the message. They can't be built until fixed. Don't change saved data.
5. Update asset-manifest.json hashes for changed front-end files.

## Tests

- 194.5-wide flat OptiPlex is rejected with the rotate hint.
- The same device at `dev_rot=90` (182.5 across, tray 198.5) passes.
- A 188 + 16 = 204 boundary passes; 204.1 fails.
- A dev_off_x that pushes the tray past 204 fails.
- The Pi example still passes.
- No STL exports.

## May change

`equipment_tray.scad`, `equipment.py`, `equipment-wizard.js`, `tray-placement.js`, `port-openings.js` (only if it repeats the width rule), `asset-manifest.json`, `test_*.py`, `js-tests/`. Nothing else; never data/normal-use.

## Checks and report

Run `run_checks.ps1` before and after. Write `work/codex-tasks/26-tray-width-hard-limit-REPORT.md` (files with SHA-256, where the constants live, check results, open questions).
