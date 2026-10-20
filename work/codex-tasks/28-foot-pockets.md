# Task 28 · Find a device's feet and give them pockets in the floor

Do this after task 27.

Brian, 2026-10-20: the third-party OptiPlex bracket fits only because its floor has two grooves for the PC's rubber feet. Claude found them with the new `outputs/Mechanical_Design_App/mesh_study.py` (`recesses`): two grooves 2.00 mm deep and 5.5 mm wide, at X 51–56.5 and 197.5–203, running 14.5–91 mm behind the front. The case then sits on a 37 mm-high floor while the feet drop in. See `work/optiplex-bracket-study/Report.md`.

Today our sleeve and flat mounts budget the full 38.8 mm (feet included). That leaves a 1.8 mm plate band above the window and 1.5 mm lips. With pockets, the case height (about 36.8 mm) sets the budget instead.

Brian: "being able to find and work around stuff like this is the whole point of our app." So the detection itself is part of the task, not just the pockets.

Standing rules in [README.md](README.md) apply. Fit, retention and strength stay UNKNOWN. Printing is not authorized.

## Build

1. **Detect feet in the imported model** (wizard step 1, after orientation and Rotate 90°).
   - Look at the device's underside along the up axis. The main bottom level is the case bottom. Clusters of material that reach lower than it by at least 0.3 mm are feet.
   - Report each foot's footprint (x, y, w, d in the device frame: front-left origin, like holes) and its height. Ignore tiny clusters (fewer than a few samples, or under 2 × 2 mm).
   - Use the same method as `mesh_study.py`:
     - split the mesh into separate bodies (shells sharing vertices);
     - ray-cast each body on its own;
     - merge the solid intervals;
     - only then find the main level and the clusters.

     Imported STEP/STL models are often several overlapping bodies. Do it in JS on the imported triangles (a grid of about 1 mm is fine; keep it fast for a 50k-triangle model). Optionally share a small JS port of `columns`/`recesses` in a new file, served by app.py and listed in asset-manifest.json.
   - Show it like holes and ports: "Found 4 feet, 2.0 mm tall". Each foot gets a checkbox (keep or drop), plus "+ Add foot" for typing one in by hand.
   - Save to `spec.feet = [{x, y, w, d, h}]`. Old specs without feet behave exactly as today.
2. **Height budget.** For `flat` and `sleeve`, when feet are kept, the device's case height is `dev_h − foot height` (use the tallest kept foot). Pockets carry the feet. Apply this in Python and JS (U check, sketches, lift, front window and bands, port/cable Z) with one shared rule.
3. **Pockets in the tray floor** for every kept foot, rotated with `dev_rot` (use the same `dp()` transform as holes).
   - Each pocket is the foot footprint + 0.5 mm clearance per side, and foot height + 0.3 mm deep.
   - Keep at least 0.8 mm of floor under a blind pocket. If the foot is too tall for that, cut the pocket right through the floor and say so in a one-line note.
   - Pockets must not cut into strap slots, joint parts, sleeve walls, the rear stop or the floor strip under the window. If one would, reject with a plain message.
   - PROPOSED defaults as named constants: clearance 0.5, extra depth 0.3, minimum floor 0.8.
4. **Sleeve and window follow.** With the lower case height, the sleeve walls, lips, window and bands use the freed height. Prefer a thicker top lip and plate band over a taller window. Report the new OptiPlex numbers (it was band 1.825 / lip 1.5) and how you spent the freed millimetres.
5. **Place on tray** shows the pockets in the live sketch, and the exact preview contains them.
6. Update asset-manifest.json hashes, and app.py's served-file list if you add a JS file.

## Tests

- **JS detection** on a synthetic device: a box case plus 4 small feet as separate overlapping bodies, so the even/odd trap is covered. It finds exactly 4 feet with the right footprints and height. A device without feet finds none. Turning the device (orientation and Rotate 90°) moves the feet correctly.
- **OptiPlex flat and sleeve with feet kept:** validates 1U, the pockets are inside the floor and clear of joints and straps, and the bands/lip are thicker than without feet.
- **Feet too tall for a blind pocket** gives a through pocket plus the note.
- **A pocket hitting a strap slot or joint** is rejected.
- **Old specs** with no `feet` give unchanged results for every mount.
- `test_mesh_study.py` keeps passing (don't change `mesh_study.py` unless you find a bug; if so, say so).
- No STL exports.

## May change

`equipment_tray.scad`, `equipment.py`, `equipment-wizard.js`, `tray-placement.js`, `port-openings.js`, `port_openings.py`, `cable-ports.js` (only if the lift changes), one new JS helper file if needed plus `app.py` (only to serve it), `asset-manifest.json`, `test_*.py`, `js-tests/` (register new tests in `js-tests/run.js`). Nothing else; never data/normal-use or third-party files.

## Checks and report

Run `run_checks.ps1` before and after. Write `work/codex-tasks/28-foot-pockets-REPORT.md` with:
- files with SHA-256;
- how detection works and how fast it is on a 50k-triangle model;
- the new constants;
- the OptiPlex numbers before and after (band, lip, window, case height);
- check results;
- open questions.

Claude browser-checks with the OptiPlex STEP afterwards. That check confirms whether the STEP model's feet are found, and where.
