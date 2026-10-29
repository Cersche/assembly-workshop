# Task 47 — Hue + Pi 4 bracket HP4-M6-B (Pi left, Hue right)

Spec by Claude 2026-10-28. Nothing gets printed; fit, strength and DSI ribbon reach stay UNKNOWN.

## Goal
New revision **HP4-M6-B** of the U5 Hue + Pi 4 bracket: the Pi 4 moves to the LEFT of the tray (X negative), the Hue Bridge cradle to the RIGHT. Reason: a Waveshare 5" DSI screen will sit upright and centred in a 2U plate at U4–U3 directly below; its DSI connector is on its left edge seen from the front (about X -52). This is a **swap, not a mirror**: the Pi board, its port openings and the Hue cradle are translated, never mirrored (`mirror()` is not allowed on the Pi, its openings or the cradle).

## Source (patch, don't regenerate)
Copy `outputs/Hue_Pi4_M6_2026-10-28/src/HP4-M6-A.scad` to `outputs/Hue_Pi4_M6-B_2026-10-28/src/HP4-M6-B.scad` and change only the values below. HP4-M6-A is itself a patch of the printed baseline `outputs/Hue_Pi4_WideLane_2026-10-24/ext.scad`; keep its M6 joint modules (`m6_tray_joint_add/cut`, bosses, pilots, counterbores, `jzx`=24) exactly. The cradle is still imported in place from `C:/Users/brian/Downloads/Swanky Rottis.stl` (never copy it into the repo).

## Changes (X is seen from the front, + = right)
All X values are planned numbers. If a check below fails, stop and report rather than inventing a fix.

| Item | HP4-M6-A | HP4-M6-B |
|---|---|---|
| Pi footprint (`dev2_off_x`) | 74 → X 46..102 | **-53 → X -81..-25** (1 mm clear of the keystone block at X ≤ -82) |
| Pi rotation / Y | `dev2_rot=270`, `dev2_off_y=-12` | unchanged (ports at the plate, board Y 0..85) |
| Pi openings `ports` X (Z, sizes, radii unchanged) | 55, 73, 91.7 | **-72, -54, -35.3** (each moved by -127, same as the board) |
| Hue cradle `cradle_x` (and `dev_off_x` ghost) | -34.5 | **54** (Hue X 8.65..99.35; same 2.65 mm margin to the tray edge as A had on the left) |
| Cable lane (Pi ↔ Hue) | X 12.9..46 (33.1 mm) | **X -25..6.6 (31.6 mm)**: 1.5 mm narrower because the Pi must clear the keystone block. Report the real width |
| Lane tie slots `lane_tie_cut` X (Y=96, 3 x 12 unchanged) | 16.5, 39.5 | **-21.5, 0** (same gaps to the Pi and lane edges as A) |
| M6 joints `joint_x` (last assignment, line ~387) | -58, -12, 29.5 | **-9.2, 30.5, 76.5** (lane centre; and the two Hue joints at the same offsets -23.5/+22.5 from the cradle centre as A) |
| Plate ID (rear face, Z=8) | X -35, "HP4-M6-A" | **X 54, "HP4-M6-B"** |
| Tray ID (floor, Y=119) | X -35, "HP4-M6-A" | **X 54, "HP4-M6-B"** |
| Comments / module names | hp4_* "HP4-M6-A" | rename text to HP4-M6-B; update the wide-lane layout comment block |

Unchanged: tray outline X -82.5..102 / depth 123.4, golden keystone at X -92.5 (`ks_tight=0.2`), four corner rack slots only, 44.4 mm / 4 mm / 252 mm plate, Pi inserts (`dev2_holes`, 3.2 pilots, 6 standoff), cradle cut/Z, tongue/slot, joint height and every M6 dimension. No new features (no ribbon slot, no extra openings) unless Brian adds them.

## Clearance checks (report numbers)
1. Pi footprint (X -81..-25, Y 0..85) vs keystone golden block (X -103..-82): no overlap.
2. Pi openings vs keystone opening/block on the plate: report the solid web width between them on the front face (expected ≈ 5.6 mm) and behind (≈ 2.5 mm).
3. Each M6 joint (tab ±10 mm, boss Ø14, tongue foot to Y 14.3) vs Pi footprint, Pi openings, cradle posts and tie slots: report the smallest gap for each joint. The lane joint at -9.2 must clear the Pi edge (-25) by ≥ 5 mm.
4. Cradle posts (imported mesh, after the cut) stay inside X ≤ 102 and do not overlap the lane tie slots or joints.
5. IDs do not touch bosses, openings, slots or cradle posts.

## Output folder `outputs/Hue_Pi4_M6-B_2026-10-28/`
- `src/HP4-M6-B.scad`, `src/HP4-M6-B_build.py` (adapt `HP4-M6-A_build.py`; OpenSCAD.exe, not the .com launcher; same validation as task 45).
- `HP4-M6-B_tray.stl`, `HP4-M6-B_faceplate.stl`, `HP4-M6-B_Hue_Pi4_M6_set.3mf` (two separate named objects side by side via `tools/plate_layout_stl.py`, both min Z = 0).
- `README.md` in the style of the HP4-M6-A README: ID, files, BOM (3 rack M6 heat-set inserts + 3 M6 x 8 button heads; Pi board mounting unchanged, pending Brian), what changed vs A, the DSI reason, UNKNOWNs.
- `checks/` acceptance JSON + logs.

## Acceptance
- Both parts render with OpenSCAD.exe, no empty/invalid geometry warnings; each one closed shell (every edge shared exactly twice, consistent winding); report counts.
- Faceplate ∩ tray: empty or contact only (every vertex exactly at Y=0, zero volume), as accepted for A.
- Everything behind the plate within X -104..104 (report min/max).
- Diff of `HP4-M6-B.scad` vs `HP4-M6-A.scad` shows only the table's changes (put the full diff in `work/hue-pi4-m6-47/source.diff`).
- 3MF: count plain `<vertex` / `<triangle` tags per object (no `ns0:` prefixes) and match the STL triangle counts.
- Clearance checks 1–5 reported.
- Protected hashes unchanged (before/after SHA-256 into `work/hue-pi4-m6-47/`).

## Do not touch
`outputs/Hue_Pi4_M6_2026-10-28/`, `outputs/Hue_Pi4_*_2026-10-24/`, `outputs/Final_3MF/`, other bracket folders, `equipment.py`, `equipment_tray.scad`, `tools/`, `data/normal-use/`. No printing, no commit, no push. Don't copy the cradle STL.

## Report
`work/codex-tasks/47-hue-pi4-m6-b-REPORT.md`: changes, check results with numbers, anything deviating or UNKNOWN.
