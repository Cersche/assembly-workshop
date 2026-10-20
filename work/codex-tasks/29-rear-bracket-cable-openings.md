# Task 29 · Cable openings in the rear bracket

Brian, 2026-10-20. The OptiPlex sleeve's orientation and rack mounting are **SETTLED**: the faceplate is on the front posts, the tray runs 240 mm, and a rear bracket goes on the rear posts. See `outputs/Physical_Test_Coupons_2026-10-20_SLV-B/README.md`. But the app's rear bracket (`rear_bracket()` in `equipment_tray.scad`) is a **solid plate** across the whole U. It walls off every rear port of the device: power, display, network, USB.

Claude made a one-off test part with openings cut by hand: `outputs/Physical_Test_Coupons_2026-10-20_SLV-C/SLV-C_coupon.scad` (read it, don't copy it blindly). Build the same idea into the app, for any device on rear-post support.

Standing rules in [README.md](README.md) apply. Fit, stiffness and strength stay UNKNOWN. Printing and exports are not authorized.

## Build

1. **New spec key `rear_openings`** (boolean).
   - New items from the wizard, and Place on tray, default it to **true** whenever rear support is on.
   - A spec **without** the key builds exactly as today (solid bracket). Its source must stay byte-identical, like the other placement keys.
   - `clean()` keeps the key only when rear support is on.
2. **Openings in `rear_bracket()`**, cut in the 2D plate outline (the cleaner meshes, like the faceplate window). Derive them from the real joint geometry (`joint_x`, `boss_d`, `tongue_w`, `tongue_z`, `tongue_h`, `tray_z`) and the plate height, so they work for every mount, floor height and 1U–5U:
   - keep **≥ 4 mm** of plate around each boss and tongue;
   - keep a band of **≥ 3.5 mm** along the bottom and the top edge;
   - keep **13 mm** between the openings and the rack-slot capsules, so openings stay within about X ±100;
   - use **2 mm** corner radii;
   - per U: one window above the bosses across the width, plus a window between the bosses and one outside each boss, below the boss top. Leave out any window narrower or lower than 10 mm.
   - For the OptiPlex sleeve on rear support (1U, the SLV-B spec), the result should match SLV-C. That's X −100..100 × Z 22–40.5 above, and X −30..30 and ±50..100 × Z 3.5–22.2 below. Explain any difference.
   - PROPOSED constants, named: margin 4, band 3.5, ear keep 13, radius 2, minimum window 10.
3. **Switch in Place on tray** (and the wizard, wherever rear support is chosen): a "Cable openings in the rear bracket" checkbox, on by default, shown only when rear support is on. Its hint: "Lets the device's rear cables pass the rear posts. Bracket stiffness UNKNOWN."
4. **Sketches:** the box sketch for the rear bracket (tray-placement.js) shows the openings, or at least a note. Update the asset-manifest.json hashes for any changed JS.

## Tests

- Old specs with rear support and no key: the source and the rear bracket are unchanged.
- OptiPlex sleeve rear-support spec with `rear_openings: true`: the generated source has the openings, and the numbers match SLV-C (or the documented differences).
- An inserts-mount tray (higher floor, bosses higher) and a 2U plate: the openings still clear the bosses/tongues by ≥ 4 mm and keep the bands.
- `rear_openings` is dropped when rear support is off.
- No STL exports.

## May change

`equipment_tray.scad`, `equipment.py`, `equipment-wizard.js`, `tray-placement.js`, `port_openings.py` / `port-openings.js` (only if shared constants belong there), `asset-manifest.json`, `test_*.py`, `js-tests/` (register new tests in `js-tests/run.js`). Nothing else; never data/normal-use, the coupon folders or third-party files.

## Checks and report

Run `run_checks.ps1` before and after. Write `work/codex-tasks/29-rear-bracket-cable-openings-REPORT.md` with:
- files with SHA-256;
- the opening rule and constants;
- the OptiPlex numbers compared with SLV-C;
- check results;
- open questions.

Claude reviews it and renders the OptiPlex bracket afterwards.
