# CM1000 one-piece bracket — test-print ID CM1P-P (2026-11-03)

PROPOSED — UNPRINTED. CM1P-O with its 5 light pipes cut back to the icon-only part, because CM1P-O passed no light and the icon-only hole passed the most on the CM1P-T6 test slice. Light on the full bracket, rail length, rack fit and strength UNKNOWN. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA); V dimensions from CM1000_1U_Mount (source not recorded). In-house only.

## Print

`CM1P-P_CM1000_one_piece_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, same setup as CM1P-O. 254 x 44.45 x 147.62 mm, about 255 cm3 of solid volume. Assign filaments as on CM1P-O: 5 light pipes, 7 logo parts, 2 details. ID engraved on the plate's top face. 2 walls, 10% infill is the only setting proven for this fit.

## What changed from CM1P-O

- **Light pipes:** each is the icon face plus round section to Y 1.5, the part CM1P-T6 tested as icon only. CM1P-O's ran up to 16.14 back.
- **Tunnels:** unchanged, now open from Y 1.5 back to the modem, about 10.5 of air to the LED on the centre line. The LED position is from the pipe height, not measured.
- **ID text:** CM1P-P.

Rails, V, lips, side screw slot, rack slots, logo and M3 bores are unchanged. `python compare_to_o.py` cuts both bodies every 0.5 mm: 9 of 295 slices differ, all at the ID text.

## Report

Light through all 5 on the full bracket? Fit same as before, rail length right, anything behind the rails hit in the rack?

## Checks run (digital only)

FreeCAD: one valid solid, one shell, 254.6 cm3; each pipe one valid solid. `python pack_check.py` from `src/`: 0 bad edges on the body and pipes, 20616/41228 vertex/triangle tags, 16 objects. Sampled surface points inside the modem envelope: 0 with the drawn lean removed; 8 as drawn, the intended overlap at the arm tips, same as CM1P-O. No slicer check.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_p_freecad.py').read())"`; `python pack_check.py`; `python compare_to_o.py`.
