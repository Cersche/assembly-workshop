# CM1000 one-piece bracket — test-print ID CM1P-O (2026-11-02)

PROPOSED — UNPRINTED. CM1P-N's fitted geometry on the baseline faceplate front: logo, 5 light pipes with their icons, and the 2 small details. Replaces CM1P-N's window and the small icons above it. Light through the pipes, pipe fit in the tunnels, rail length, rack fit and strength UNKNOWN. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA); V dimensions from CM1000_1U_Mount (source not recorded). In-house only.

## Print

`CM1P-O_CM1000_one_piece_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, same setup as CM1P-N. 254 x 44.45 x 147.62 mm, about 255 cm3 of solid volume. Assign filaments as on the baseline: 5 light pipes, 7 logo parts, 2 details. ID engraved on the plate's top face. 2 walls, 10% infill is the only setting proven for this fit.

## What changed from CM1P-N

- **Window, its bevel and the small icons above it:** gone, the plate is solid there again.
- **Baseline front back:** pipe icons, details and logo. The front face matches CM1P-H's cut for cut at Y 0.1 and 0.3.
- **Light pipes are longer than the baseline's:** they end 8.72 back at most on the baseline, 16.14 here. The modem now sits 2.5 further back on a 25 slope, so baseline-length pipes would stop up to about 7.5 short of it. Each pipe's end follows the lip surface, 0.5 off the modem's slope.
- **ID text:** CM1P-O.

Rails, V, lips, side screw slot, rack slots and the M3 bores are unchanged. `python compare_to_n.py` cuts both bodies every 0.5 mm from Y 0.13 to 147.13 on a 0.1 mm grid: every difference is in the window and icon area, at the ID, or a pipe's edge at the tunnel, and none lies past Y 16.13.

## Pipe and tunnel sizes

Behind Y 1.5 the pipe is 7.94 across and its tunnel 8.04, against the baseline's 7.99 in a same-size hole. The small differences were needed so FreeCAD doesn't hang on near-coincident faces. Ahead of Y 1.5 it's the baseline's own mesh, with its hole unchanged.

## Report

Pipes sit properly in the plate? Lights visible through all 5? Fit same as before, rail length right, anything behind the rails hit in the rack?

## Checks run (digital only)

FreeCAD: one valid solid, one shell, 254.6 cm3; each pipe one valid solid. `python pack_check.py` from `src/`: 0 bad edges on the body and pipes, 21333/42662 vertex/triangle tags, 16 objects. Sampled surface points inside the modem envelope: 0 with the drawn lean removed; 8 as drawn, the intended overlap at the arm tips. No slicer check.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_o_freecad.py').read())"`; `python pack_check.py`; `python compare_to_n.py`.
