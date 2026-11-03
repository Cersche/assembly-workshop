# CM1000 one-piece bracket — test-print ID CM1P-M (2026-11-02)

PROPOSED — UNPRINTED. CM1P-K with the side screw slot centred on 80 from the faceplate front. Brian printed a test run of CM1P-K and reports a perfect fit: no sagging, no play, not tight. The only fault was the slot sitting too far forward; he puts the screw at approximately 80. Side screw on this revision, rack fit, light visibility, insert fit and strength UNKNOWN. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA); V dimensions from CM1000_1U_Mount (source not recorded). In-house only.

## Print

`CM1P-M_CM1000_one_piece_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, same setup as CM1P-K. 254 x 44.45 x 137.62 mm, about 244 cm3 of solid volume. Assign filaments to the logo and icon parts. ID engraved on the plate's top face.

## What changed from CM1P-K

- **Side screw slot, left rail:** Y 72.73 to 87.27, centre 80.0 (was 64.02 to 78.56, centre 71.29). Same size and height.
- **Screw head recess, outer face of the left rail:** Y 71.08 to 88.91 (was 62.37 to 80.2). Same size, height and depth.
- **ID text:** CM1P-M.

Nothing else changed. CM1P-K's fit report applies to CM1P-K as printed. The test-run slicer settings aren't recorded here, so if this print uses different walls or infill, the rails may not spread the same.

CM1P-L (slot moved 5 back) was built first and superseded before printing.

## Assumptions, not measurements

- 80 is Brian's approximate figure from the printed part. It replaces the earlier 62.4 to 72 hole measurement in the modem model (`build_modem.py`, now 75.9 from the modem's front, which sits at Y 4.1).

## Report

Does the screw go into the modem's hole, and where does it sit in the slot? Fit still the same as CM1P-K? Lights visible, rack fit.

## Checks run (digital only)

FreeCAD: one valid solid, one shell, 243.9 cm3, same outer size as CM1P-K. `python pack_check.py` from `src/`: 0 bad edges on the body, 13192/26364 vertex/triangle tags, 14 objects. Sampled surface points inside the modem envelope: 0 with the drawn lean removed; 8 as drawn from Y 82.2 back, the intended overlap at the arm tips. Slot and recess positions confirmed from the finished mesh.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: `python make_icons.py`; OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_m_freecad.py').read())"`; `python pack_check.py`.
