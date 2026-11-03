# CM1000 one-piece bracket — test-print ID CM1P-L (2026-11-02)

SUPERSEDED BEFORE PRINTING by CM1P-M: don't print this one. Brian then put the screw at about 80, near this slot's rear end. CM1P-K with the side screw slot moved 5 toward the rear. Brian printed a test run of CM1P-K and reports a perfect fit: no sagging, no play, not tight. The only fault was the mounting screw slot sitting about 5 too far forward. Side screw on this revision, rack fit, light visibility, insert fit and strength UNKNOWN. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA); V dimensions from CM1000_1U_Mount (source not recorded). In-house only.

## Print

`CM1P-L_CM1000_one_piece_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, same setup as CM1P-K. 254 x 44.45 x 137.62 mm, about 244 cm3 of solid volume. Assign filaments to the logo and icon parts. ID engraved on the plate's top face.

## What changed from CM1P-K

- **Side screw slot, left rail:** Y 69.02 to 83.56 (was 64.02 to 78.56). Same size and height.
- **Screw head recess, outer face of the left rail:** Y 67.37 to 85.2 (was 62.37 to 80.2). Same size, height and depth.
- **ID text:** CM1P-L.

Nothing else changed. CM1P-K's fit report applies to CM1P-K as printed. The test-run slicer settings weren't recorded here, so if this print uses different walls or infill, the rails may not spread the same.

## Assumptions, not measurements

- The 5 is Brian's estimate from the printed part.
- The slot was centred on the hole position from the modem measurement (62.4 to 72 back from the modem's front, centre Y 71.3 in the bracket). If the 5 is right, the hole centre is near Y 76.3 and the earlier measurement or the model is off by that much. `work/equipment-models/netgear_cm1000/understanding/side_screw_hole.stl` is unchanged; the viewer draws it 5 further back, labelled.

## Report

Does the screw reach the modem's hole, and does it sit near the middle of the slot? Fit still the same as CM1P-K? Lights visible, rack fit.

## Checks run (digital only)

FreeCAD: one valid solid, one shell, 243.9 cm3, same outer size as CM1P-K. `python pack_check.py` from `src/`: 0 bad edges on the body, 13154/26288 vertex/triangle tags, 14 objects. Sampled surface points inside the modem envelope: 0 with the drawn lean removed; 8 as drawn from Y 82.2 back, the intended overlap at the arm tips. Slot and recess positions confirmed from the finished mesh.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: `python make_icons.py`; OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_l_freecad.py').read())"`; `python pack_check.py`.
