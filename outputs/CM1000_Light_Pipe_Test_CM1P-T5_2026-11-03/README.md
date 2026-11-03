# CM1000 light pipe test slices — test-print IDs CM1P-T5A and CM1P-T5B (2026-11-03)

SUPERSEDED, do not print: Brian asked for the whole test in one piece, see CM1P-T6.

PROPOSED — UNPRINTED. Brian printed CM1P-O: lights line up with the tubes but none gets through, and in a flashlight test much more light passes the old plate. He had also switched to gyroid infill. These slices separate pipe length from infill. They test light only: no rails, no rack slots, no strength. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA): in-house only.

## Print

`CM1P-T5_light_pipe_test_slices.3mf`, also in `outputs/Final_3MF/`: two objects side by side, front faces on the bed, no supports. Each 70 x 44.45 x 26.75 mm, about 44 cm3 of solid volume. The ID is engraved on the top face with hole numbers 1 to 5 above the holes.

Assign the same pipe filament as CM1P-O to the 5 "Pipe" parts and 2 "Icon detail" parts on both slices. Only the pipe settings differ:

- **CM1P-T5A:** pipes as CM1P-O was printed (2 walls, 10% gyroid).
- **CM1P-T5B:** pipes 100% infill, set per part in the slicer. Body settings don't matter.

## The holes

Numbers run left to right, looking at the front. Same CM1P-O position, tunnel and front icon as each hole's baseline pipe.

| Hole | Pipe | Plastic on the centre line | Air to the LED |
|---|---|---|---|
| 1 | Icon only | 1.5 | 10.5 |
| 2 | Earlier faceplate's pipe, unchanged | 5.8 | 6.1 |
| 3 | Halfway, end parallel to the slope | 8.5 | 3.5 |
| 4 | CM1P-O's pipe, the control | 11.3 | 0.6 |
| 5 | Short, flat end | 6.5 | 5.5 |

The LED position is the one from the pipe height, not measured on the modem.

## How to test

1. Sit the modem flat on the table, powered, and sit the slice on the same table. Push it onto the modem's front until it stops. The top lip goes over the upper slope. The 6 at each end of the slice is what the modem's front stops on, as the bracket does.
2. The slice slides sideways along the modem, so the LEDs and pipes needn't be matched. Pick one steady bright LED and slide the slice so each hole in turn sits over it (11.5 between holes). That takes different LED brightness out of the comparison.
3. Compare T5A and T5B hole by hole, in a dim room.

## Report

Rank the holes on each slice, and say whether T5B is clearly brighter than T5A. Hole 4 lit on T5B but dark on T5A means infill was the cause. Hole 4 dark on both while hole 2 is bright means length.

## Checks run (digital only)

FreeCAD: each body one valid solid, one shell; each pipe valid. `python pack_check.py` from `src/`: 0 bad edges on every part, 0 sampled surface points inside the modem envelope, 29720/59432 vertex/triangle tags, 18 objects, 2 build items. No slicer check. Light through any of these, slide-on fit and the stop are UNKNOWN.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: `OpenSCAD.exe -D "tag=\"A\"" -o id_A.stl id.scad`, the same for B; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_t5_freecad.py').read())"`; `python pack_check.py`.
