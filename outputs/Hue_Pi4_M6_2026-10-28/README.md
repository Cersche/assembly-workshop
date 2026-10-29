# HP4-M6-A — Hue + Pi 4 wide-lane 1U bracket, M6 hardware (2026-10-28)

Test-print ID **HP4-M6-A** is engraved 0.6 mm into the plate rear face (centred X=-35, baseline Z=8) and open tray floor behind the cradle (centred X=-35, baseline Y=119).
M6 redesign of the printed baseline `outputs/Hue_Pi4_WideLane_2026-10-24/` (unchanged). **This revision is not printed. Fit and strength UNKNOWN.**

| File | What |
|---|---|
| `HP4-M6-A_Hue_Pi4_M6_set.3mf` | Tray + faceplate side by side, two descriptively named objects, both bed-normalized |
| `HP4-M6-A_tray.stl`, `HP4-M6-A_faceplate.stl` | Assembly-coordinate parts; one closed shell each, every edge shared by exactly two triangles |
| `src/HP4-M6-A_build.py` | `python src/HP4-M6-A_build.py [out_dir]` renders with OpenSCAD.exe, checks, then packs using `tools/plate_layout_stl.py` |
| `src/HP4-M6-A.scad` | Hand-patched copy of the exact baseline; reads the cradle STL in place from Downloads |
| `checks/acceptance.json` | Counts, bounds, contact check and packed object evidence; render logs alongside |

**Bracket BOM:** 3 × rack M6 heat-set insert + 3 × M6 x 8 button-head screw.

**Pi board mounting (unchanged, pending Brian):** four device insert mounts, 3.2 mm pilots, 6 mm standoffs, Pi holes 2.7 mm. These are separate from the bracket BOM; the Pi board inserts were not converted to M6. Insert specification and board screws remain pending Brian.

What changed vs the baseline (everything else retained):
- Three hidden joints at the same X=-58 / -12 / +29.5: 14 mm bosses, 7.6 mm insert bores (8 mm inside the boss, starting 0.1 mm into the plate rear), 6.6 mm screw clearance, rounded 20 x 6 mm tabs with the generator's tongue foot and 4 mm coves, 11.5 x 3.5 mm counterbores, 2.5 mm under the head. Original tongue/slot dimensions retained.
- One screw per joint, Z=32.225 mm (= tray_z+24). Boss top 39.225, rounded tab top 42.225, both below plate top 44.425. No clipping required. Nominal M6 x 8 engagement is 5.2 mm after the 2.5 mm seat and 0.3 mm joint gap; usable thread depth remains UNKNOWN.
- Engraved IDs on both parts. No edge stiffening walls: the keystone gap and cable lane stay open.

Kept: 33 mm cable lane; cradle position and base cut; Pi 270° position and all three openings; golden keystone at -92.5 with ks_tight=0.2; two 3 x 12 cable-tie slots; rectangular floor X=-82.5..102, depth 123.4; 252 x 44.4 x 4 nominal plate; four corner rack slots only; no front screw holes; no joint at the Pi end.

Why not the generator's `m6_joint`: it does not reproduce this second-device layout, asymmetric floor, third joint and imported cradle. Only its joint geometry was reused; the generator and user data were untouched. `Swanky Rottis.stl` remains at `C:/Users/brian/Downloads/Swanky Rottis.stl`, required to rebuild, never copied.

Digital checks: tray 6,908 triangles / 10,362 edges; plate 4,884 triangles / 7,326 edges; each one connected shell, 0 bad edges and consistent winding. Behind-plate X: tray -82.5..102; plate -102.4..36.5; combined -102.4..102, inside ±104.

Assembled intersection: **contact only, 0 volume**. All 628 exported contact triangles lie exactly on Y=0. Brian explicitly accepted the intended tray/feet contact, as on the printed baseline; no clearance relief was added. OpenSCAD returns non-manifold contact surfaces for that zero-thickness result; the actual part renders have no invalid/empty-geometry warnings. Inherited variable-override notices remain in the logs.

UNKNOWN: insert OD/length, insertion bulging, retention, usable thread engagement, printed fit, strength, load capacity and cable bend room. Exact ASCII triangulations contain one collinear triangle at the unchanged cradle seam (also in baseline) and two at the plate ID baseline; edge closure still passes without rounding or mesh repair. Slicer behaviour is untested. No physical work authorized or performed. Local/personal use; licensed geometry is not redistributed.
