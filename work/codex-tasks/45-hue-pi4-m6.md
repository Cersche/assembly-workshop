# Task 45 — Hue + Pi 4 bracket, M6 hardware (test-print ID HP4-M6-A)

Bracket overhaul (AGENTS.md "M6 bracket hardware", work/bracket-overhaul/README.md). Spec by Claude 2026-10-28. Nothing gets printed; fit and strength stay UNKNOWN.

## Goal
Rebuild the printed Hue + Pi 4 wide-lane bracket with the rack's M6 heat-set inserts (7.6 mm bores) and M6 x 8 button-head screws in place of the M3 tray joints, keeping every other feature.

## Baseline (immutable — do not edit anything in it)
`outputs/Hue_Pi4_WideLane_2026-10-24/` — `ext.scad` (hand-edited generated source), STLs, 3MF, README. The Hue cradle is imported in place from `C:/Users/brian/Downloads/Swanky Rottis.stl` (never copy it into the repo).

## Why not the generator's `m6_joint`
`m6_joint` (equipment.py `M6_HOOKS` + the `@m6` block of `equipment_tray.scad`) cannot build this bracket: it has no second device (the Pi is `dev2`), no hand-set asymmetric tray (`tray_x0=-82.5, tray_x1=102`), no hand-placed third joint, no imported cradle mesh, and its 15.5 mm front gap / edge joints would move the Pi off the plate's rear face. So: hand patch, but **reuse the `@m6` geometry** (same tab, coves, boss, counterbore numbers) so the joint matches the approved HDT-M6-A / SG8-C1 pattern.

## Output folder
`outputs/Hue_Pi4_M6_2026-10-28/` with:
- `src/HP4-M6-A.scad` — copy of the baseline `ext.scad` with the changes below (keep the cradle import path).
- `src/HP4-M6-A_build.py` — renders tray + faceplate with `OpenSCAD.exe` (not the .com launcher) and packs the 3MF via `tools/plate_layout_stl.py`.
- `HP4-M6-A_tray.stl`, `HP4-M6-A_faceplate.stl`, `HP4-M6-A_Hue_Pi4_M6_set.3mf` (both parts side by side, separate objects, descriptive names).
- `README.md` in the style of `outputs/TL-SG108E_M6_2026-10-28/README.md` (ID, files, BOM, what changed vs baseline, why not `m6_joint`, UNKNOWNs).

## Changes (only these)
1. **Joints → M6**, at the same X as the baseline: `joint_x=[-58,-12,29.5]`. Copy the `@m6` block geometry: `boss_d=14`, `joint_pilot=7.6` (insert bore, 7 mm deep min), `m3_clear=6.6` clearance, tray tab = `m6_tray_joint_add/cut` (20 x 6 rounded tab, tongue foot, 4 mm coves, 11.5 x 3.5 counterbore, 2.5 mm under the head). One screw per joint at a single height that fits a 1U plate (the generator's `jzx` = 32 may push the 14 mm boss past the plate top at 44.4 mm: if so, lower the screw or clip the boss top flush with the plate top as SG8-M6-B does, and say which). Tongue/slot joint stays.
   - Do **not** add the generator's edge stiffening side walls unless they clear the keystone cable gap (X -104..-82.5) and the cable lane (X 12.9..46); if unsure, leave them out and say so.
   - The floor-front tongue under each tab must not hit the cradle posts or the Pi board (Pi X 46..102, Y 0..85).
2. **Faceplate:** only the four corner rack slots (unchanged); no screw holes through the front; keep the golden keystone at X -92.5 (`ks_tight=0.2`) and the three Pi openings exactly as baseline.
3. **Test-print ID `HP4-M6-A`**, engraved 0.6 mm: on the plate rear face in a clear spot (not on a boss, keystone block or Pi opening), and on the tray floor top in open floor away from joints, cradle posts, tie slots and the Pi (e.g. behind the cradle). Same ID in folder, file names, README.

## Keep unchanged (Brian: ask before dropping any)
Wide 33 mm cable lane, Brian's cradle corner posts (position, base cut), Pi 4 at 270° with ports at the plate, Pi openings (sizes/Z), golden keystone, the two 3 x 12 cable-tie slots, tray outline X -82.5..+102 / depth 123.4, no joint at the Pi end, 44.4 mm / 4 mm / 252 mm plate.

**Pi board mounting:** the Pi sits on four device inserts (`dev2_insert_pilot=3.2`, the Pi's 2.7 mm holes). M6 can't go through those holes, so leave them as they are and list them separately in the README as "Pi board mounting (unchanged, pending Brian)". Do not change them.

## Acceptance checks
- Both STLs render with OpenSCAD.exe without warnings about empty/invalid geometry; each is one closed solid (every edge shared by exactly two triangles); report counts.
- Faceplate ∩ tray (assembled positions) renders empty.
- Nothing behind the plate is outside X -104..+104 (report min/max X).
- Diff of `src/HP4-M6-A.scad` vs baseline `ext.scad` shows only the joint, ID and comment changes (paste the diff summary in the report).
- `git status` shows no change under `outputs/Hue_Pi4_WideLane_2026-10-24/`, CM1000 or TL-SG108E folders.
- Bracket BOM in README: N × rack M6 heat-set insert + N × M6 x 8 button-head screw (N = joints), plus the Pi mounting note.

## Do not touch
Baseline folder, `outputs/CM1000_M6_*`, `outputs/TL-SG108E_M6_*`, the app generator (`equipment.py`, `equipment_tray.scad`), `data/normal-use/`. No commit, no push. Don't copy the cradle STL anywhere.

## Report
`work/codex-tasks/45-hue-pi4-m6-REPORT.md`: what changed, screw height chosen and why, check results, anything left UNKNOWN or deviating from this spec.
