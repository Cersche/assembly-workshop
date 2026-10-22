# Task 38 · Faceplate-only slots: blank plates and keystone panels

Brian (2026-10-22): "make sure we have the options to enable the user to create a faceplate like this. with keystones, or blanks or whatever." Reference part, made by hand today with the current engine: `outputs/Faceplate_1U_10_Keystones_2026-10-22/` (README has the exact settings; Brian approved it).

Today the app only puts keystones on a faceplate through **Place on tray**, always with a device and a tray, and export always builds tray + faceplate (or combined). There is no plate-only part and no blank plate.

Standing rules in [README.md](README.md) apply. PROPOSED, UNVALIDATED: printed fit and strength stay UNKNOWN in all UI text and reports.

## Build

1. **Faceplate-only slot.** A saved slot allocation can be a faceplate with no device and no tray. Offer it from the slot's actions (ellipsis/right-click) next to the existing way of placing equipment, labelled "Faceplate only". It is saved per slot like other allocations, with its own revisions; old documents load unchanged (missing field = today's behaviour).
2. **Layouts** (Setup tab for that slot):
   - **Blank:** plate, rack slots, nothing else.
   - **Keystones:** count and rows; the app spaces them evenly (below). Positions can then be nudged by hand like today's keystones.
   - **Custom openings:** the existing port/window openings, without a device.
   - Height 1U–5U.
3. **Even spacing (pure helper, JS + Python mirror if the server needs it).** Golden keystone block = 21 × 33.5 mm (`ks_box_cut`). Spread N blocks centred at X=0 so the outermost blocks keep the same clearance to the rack slots as the reference (outer centre ±96.75 for N=10 → pitch 21.5). For N ≤ what fits, use the largest equal pitch inside that span, capped at a sensible maximum (state your cap in the report). Rows: one row per U by default, centred on each U (Z = U centre); a 1U plate holds one row only (33.5 mm block in 44.4 mm). If SCAD `keystones` needs a Z per keystone for multi-row, extend it backward-compatibly (`[x]` or `[x,z]`; plain numbers keep `plate_center`).
4. **Engine.** Build with `equipment_tray.scad`, `part="faceplate"`, `joint="none"`. Export only the faceplate STL: no tray, no rear bracket, no combined part. Do not change the default `joint` or any existing slot's output; regression-check that an existing tray slot's SCAD/STL inputs are byte-identical before/after.
5. **Checks** (block export when failing, like other failed checks):
   - Blocks overlap each other (web < 0) or the rack slots, or sit less than 1 mm inside the plate outline → fail.
   - Web between neighbouring blocks < 2 mm → visible warning "thin wall, fit/strength UNKNOWN" (not a failure; the reference has 0.5 mm).
   - Too many keystones for the plate/rows → clear message with the maximum.
6. **Rest of the app treats it like a wizard faceplate:** rack 3D preview, Print in color (`faceplate_color.py` openings must match; keep `faceplate_color.openings` and `equipment-wizard.js openings` in step), Cables view (keystones become front/rear port pairs as today). PRINT THE RACK is unaffected.

## May change

`equipment.py`, `equipment_tray.scad` (keystone Z only, backward-compatible), `equipment-wizard.js`, `tray-placement.js`, `port-openings.js`/`port_openings.py`, `workspace.js`, `rack-studio.js`, `faceplate_color.py`, `app.py` (routes only if needed), `index.html`/CSS for the new controls, `js-tests/` (register in `js-tests/run.js`), Python tests, `asset-manifest.json`. Do not touch saved data, old revisions, `data/normal-use`, historical outputs or the reference folder.

## Tests

- Spacing helper: N=10, 1 row, 1U → centres exactly `[-96.75,-75.25,-53.75,-32.25,-10.75,10.75,32.25,53.75,75.25,96.75]`, web 0.5 mm, warning raised. N=1 → `[0]`. N too large → error with the maximum.
- 2U, 2 rows of 5 → two rows at each U centre, no warning.
- Blank 1U and 3U export: one faceplate STL, no keystone geometry, four rack slots per U.
- Regenerating the 10-keystone 1U panel through the app gives a mesh with the same bounding box and volume (±0.1%) as `outputs/Faceplate_1U_10_Keystones_2026-10-22/Faceplate_1U_10_Keystones.stl`.
- Old rack document loads and its existing tray slots export unchanged.

## Checks and report

Run `run_checks.ps1` before and after. Browser check on disposable data only (temporary `--data` folder, spare port 8700–8899; never data/normal-use, never stop the app on 8765): screenshots of creating a blank 2U plate and a 10-keystone 1U panel, the thin-wall warning, the rack view and Print in color preview. Write `work/codex-tasks/38-faceplate-only-slot-REPORT.md` with files + SHA-256, test output, screenshots, your spacing cap and open questions. Do not commit; Claude reviews.
