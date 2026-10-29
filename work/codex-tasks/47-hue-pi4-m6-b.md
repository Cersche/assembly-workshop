# Task 47 — Hue + Pi 4 bracket HP4-M6-B (Pi left, Hue right)

Spec by Claude 2026-10-28. Nothing gets printed; fit, strength and DSI ribbon reach stay UNKNOWN.

## Goal
New revision **HP4-M6-B** of the U5 Hue + Pi 4 bracket: the Pi 4 moves to the LEFT of the tray (X negative), the Hue Bridge cradle to the RIGHT. Reason: a Waveshare 5" DSI screen will sit upright and centred in a 2U plate at U4–U3 directly below; its DSI connector is on its left edge seen from the front (about X -52). This is a **swap, not a mirror**: the Pi board, its port openings, the Hue cradle and its keystone are translated, never mirrored (`mirror()` is not allowed on the Pi, its openings, the cradle or the keystone).

## Source (patch, don't regenerate)
Copy `outputs/Hue_Pi4_M6_2026-10-28/src/HP4-M6-A.scad` to `outputs/Hue_Pi4_M6-B_2026-10-28/src/HP4-M6-B.scad` and change only the values below. HP4-M6-A is itself a patch of the printed baseline `outputs/Hue_Pi4_WideLane_2026-10-24/ext.scad`; keep its M6 joint modules (`m6_tray_joint_add/cut`, bosses, pilots, counterbores, `jzx`=24) exactly. The cradle is still imported in place from `C:/Users/brian/Downloads/Swanky Rottis.stl` (never copy it into the repo).

## Changes (X is seen from the front, + = right)
Brian, 2026-10-28: the keystone belongs to the Hue, so it moves with it. The whole layout swaps sides: every item below is **translated** to its new X (never mirrored). If a check below fails, stop and report rather than inventing a fix.

| Item | HP4-M6-A | HP4-M6-B |
|---|---|---|
| Tray outline `tray_x0`/`tray_x1` (depth 123.4 unchanged) | -82.5 / 102 | **-102 / 82.5** (keystone cable gap now X 82.5..104 on the right) |
| Golden keystone `keystones` (`ks_tight=0.2`, geometry unchanged, NOT mirrored) | -92.5 | **92.5** |
| Pi footprint (`dev2_off_x`) | 74 → X 46..102 | **-74 → X -102..-46** |
| Pi rotation / Y | `dev2_rot=270`, `dev2_off_y=-12` | unchanged (ports at the plate, board Y 0..85) |
| Pi openings `ports` X (Z, sizes, radii unchanged) | 55, 73, 91.7 | **-93, -75, -56.3** (each moved by -148, same as the board) |
| Hue cradle `cradle_x` (and `dev_off_x` ghost) | -34.5 | **34.5** (Hue X -10.85..79.85) |
| Cable lane (Pi ↔ Hue) | X 12.9..46 (33.1 mm) | **X -46..-12.9 (33.1 mm)** |
| Lane tie slots `lane_tie_cut` X (Y=96, 3 x 12 unchanged) | 16.5, 39.5 | **-42.5, -19.5** (same gaps to the Pi and the Hue side as A) |
| M6 joints `joint_x` (last assignment, line ~387) | -58, -12, 29.5 | **-29.5, 11, 57** (lane centre; the two Hue joints at the same offsets -23.5/+22.5 from the cradle centre as A) |
| Plate ID (rear face, Z=8) | X -35, "HP4-M6-A" | **X 34.5, "HP4-M6-B"** |
| Tray ID (floor, Y=119) | X -35, "HP4-M6-A" | **X 34.5, "HP4-M6-B"** |
| Comments / module names | "HP4-M6-A", "keystone lane on the left, Pi edge at the right limit" | rename to HP4-M6-B; update the layout comments (keystone lane right, Pi edge at the left limit) |

Unchanged: four corner rack slots only, 44.4 mm / 4 mm / 252 mm plate, Pi inserts (`dev2_holes`, 3.2 pilots, 6 standoff), cradle cut/Z, tongue/slot, joint height and every M6 dimension. No new features (no ribbon slot, no extra openings) unless Brian adds them.

## Clearance checks (report numbers)
1. Keystone golden block (now X 82..103) vs tray floor, Hue cradle posts and the right Hue joint (57): no overlap beyond what A had at the mirrored spot (A: tray edge -82.5 against block -82).
2. Pi openings vs the plate's left rack slots (X -118.26 ±5) and plate edge: report the solid web widths.
3. Each M6 joint (tab ±10 mm, boss Ø14, tongue foot to Y 14.3) vs Pi footprint, Pi openings, cradle posts, tie slots and keystone block: report the smallest gap per joint. The lane joint at -29.5 must clear the Pi edge (-46) by ≥ 5 mm.
4. Cradle posts (imported mesh, after the cut) stay inside the tray (X ≤ 82.5) and clear the tie slots and joints.
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
