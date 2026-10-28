# HDT-M6-A — 3.5" HDD + 2.5" SSD 1U drive tray, M6 hardware (2026-10-28)

Test-print ID **HDT-M6-A** is engraved on the tray floor (rear, left) and on the back of the faceplate.
Redesign of the printed baseline `outputs/Hard_Drive_Tray_2026-10-25/` (kept unchanged) for the bracket overhaul: every M3 heat-set insert is replaced by the rack's M6 insert, fastened with M6 x 8 button-head screws. Brian approved the mockup on 2026-10-28 ("blue tray and orange faceplate are good to go"). **Not printed. Fit and strength UNKNOWN.**

## Files
| File | What |
|---|---|
| `HDT-M6-A_drive_tray.3mf` | Both parts side by side, print orientation: "HDT-M6-A tray (blue)", "HDT-M6-A faceplate (orange)" |
| `HDT-M6-A_tray.stl` | Tray, floor down (195.45 x 184 x 42 mm) |
| `HDT-M6-A_faceplate.stl` | 1U faceplate, front face down, bosses up (252 x 44.4 x 12 mm) |
| `HDT-M6-A.scad` | Exact source (generated drive-tray source from the baseline spec, hand-edited); render with OpenSCAD.exe `-D part="tray"` / `"faceplate"` |

Both meshes are closed (every edge shared by exactly two faces). The faceplate/tray intersection renders empty.

## Changes from the baseline
- **Insert holes:** 7.6 mm bore, copied from the rack posts' M6 insert holes (Lab Rax 1U post mesh: 7.60 mm, 6 mm deep). Brian: those holes fit the inserts perfectly. Faceplate bosses are 14 mm across, 8 mm deep.
- **Joints:** 4 faceplate-to-tray joints (X ±40 and ±87.2). The outer two have 2 screws each (Z 16.5 and 32.5); the inner two have only the upper screw. Total: 6 inserts, 6 screws. The screws go in from behind the faceplate and stay hidden.
- **Tray tabs:** one rounded-top 20 mm plate, 6 mm thick, with the tongue-slot foot built in and coves at the floor. Each hole is a 6.6 mm clearance hole with an 11.5 x 3.5 mm counterbore, so the button head (about 10.5 x 3.3) sits below the surface. 2.5 mm of tab under the head means the screw reaches about 5.5 mm into the 6 mm insert.
- **Sag:** 2.5 x 15 mm stiffening walls along both tray edges. Rear floor corners have a 6 mm radius and the wall ends are rounded.
- **Drives:** 3.5 mm further back (front gap 12 → 15.5 mm) to clear the tabs.
- Faceplate: unchanged 44.4 mm 1U standard, four corner rack slots only.
- 3.5" HDD side rails (uncommitted generator work) are present but off (`hdd_rails=false`).

## Hardware
- Faceplate to tray: 6 x M6 heat-set insert (rack insert) + 6 x M6 x 8 button head
- Faceplate to rack: 4 x M6 x 8 button head into the existing post inserts
- 3.5" HDD: 4 x 6-32 x 1/4 in; 2.5" SSD: 4 x M3 x 4 (into the drives; heads/torque UNKNOWN)

## Limits
PROPOSED — UNVALIDATED. Insert installation in printed bosses, screw engagement, sag, fit, strength, drive fit and airflow are UNKNOWN. The 7.6 mm bore comes from the creator post mesh plus Brian's statement, not a supplier spec. The middle post hole tie-in was discussed and not used in this revision. Not yet in the generator (`equipment_tray.scad`); `HDT-M6-A.scad` is a one-off.
