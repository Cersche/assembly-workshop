# CM1000 light pipe test slice — test-print ID CM1P-T6 (2026-11-03)

PROPOSED — UNPRINTED. Brian asked for the whole test in one piece, so this replaces the two CM1P-T5 slices. Brian printed CM1P-O: lights line up with the tubes but none gets through, and in a flashlight test much more light passes the old plate. He had also switched to gyroid infill. This slice separates pipe length from infill. It tests light only: no rails, no rack slots, no strength. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA): in-house only.

## Print

`CM1P-T6_light_pipe_test_slice.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, no supports. 127 x 44.45 x 26.75 mm, about 79 cm3 of solid volume. ID and hole labels A1 to B5 are engraved on the top face.

Parts are named in the 3MF. Assign the same pipe filament as CM1P-O to all 10 pipes and 4 icon details, then set per part in the slicer:

- **A1 to A5:** as CM1P-O was printed (2 walls, 10% gyroid).
- **B1 to B5:** 100% infill.

Body settings don't matter.

## The holes

Labels run left to right, looking at the front, 11.5 apart. A and B hold the same 5 types.

| Hole | Pipe | Plastic on the centre line | Air to the LED |
|---|---|---|---|
| A1, B1 | Icon only | 1.5 | 10.5 |
| A2, B2 | Earlier faceplate's pipe, unchanged | 5.8 | 6.1 |
| A3, B3 | Halfway, end parallel to the slope | 8.5 | 3.5 |
| A4, B4 | CM1P-O's pipe | 11.3 | 0.6 |
| A5, B5 | Short, flat end | 6.5 | 5.5 |

The icons are test markers: each hole's icon isn't meant to match the LED under it. The LED position is the one from the pipe height, not measured on the modem.

## How to test

1. Sit the modem flat on the table, powered, and sit the slice on the same table. Push it onto the modem's front until it stops. The top lip goes over the upper slope. The 6 at each end of the slice is what the modem's front stops on, as the bracket does.
2. The slice slides sideways along the modem. Pick one steady bright LED, in a dim room, and slide the slice so each hole in turn sits over it. That takes different LED brightness out of the comparison.

## Report

Rank the 10 holes. A4 dark and B4 lit means infill was the cause. A4 and B4 both dark while A2 or B2 is bright means length.

## Checks run (digital only)

FreeCAD: body one valid solid, one shell, 79.3 cm3; each pipe valid. `python pack_check.py` from `src/`: 0 bad edges on every part, 0 of 417340 sampled surface points inside the modem envelope, no body wall in any tunnel, 29812/59620 vertex/triangle tags, 16 objects, 1 build item. Cuts of the front skin, tunnels and top face looked right. No slicer check. Light through any of these, slide-on fit and the stop are UNKNOWN.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: `OpenSCAD.exe -o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_t6_freecad.py').read())"`; `python pack_check.py`.
