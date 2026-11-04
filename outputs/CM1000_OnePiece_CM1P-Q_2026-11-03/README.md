# CM1000 one-piece bracket — test-print ID CM1P-Q (2026-11-03)

PROPOSED — UNPRINTED. CM1P-P with a white printed liner in each of the 5 light tunnels, to bounce more LED light forward. How much it helps, fit, rail length, rack fit and strength are UNKNOWN. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA); V dimensions from CM1000_1U_Mount (source not recorded). In-house only.

## Print

`CM1P-Q_CM1000_one_piece_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, same setup as CM1P-O. 254 x 44.45 x 147.62 mm, about 254 cm3 of solid volume. 2 walls, 10% infill is the only setting proven for this fit.

Assign filaments per part:

- **White liner 1 to 5:** white. New in this revision; they get no filament from the file, so set them by hand.
- **Light pipe 1 to 5, Detail 1 and 2, Logo 1 to 7, Bracket body:** as on CM1P-O.

## What changed from CM1P-P

- **Tunnels:** 9.64 across behind the icon instead of 8.04, from Y 1.5 back. The icon's own 8 hole in front of Y 1.5 is unchanged. Wall between neighbouring tunnels 1.86.
- **White liners:** 0.8 wall (2 print lines), 9.54 outside, 7.94 bore, 0.05 clear of the tunnel. Each starts on the back of the icon at Y 1.5 and ends along the lip surface, 0.5 off the modem's slope, up to Y 17.11.
- **ID text:** CM1P-Q.

Icons, logo, V, lips, rails, side screw slot, rack slots and M3 bores are unchanged. The modem stays at Y 4.1 and the lip end stays 1.47 thick: Brian dropped the 2.5 forward move and the thinner lip on 2026-11-03.

`python compare_to_p.py` cuts both bodies every 0.5 mm: 32 of 295 slices differ, and the widened tunnels and ID text stop at about Y 17.13. In the slices read, the differences are material removed only.

## Report

Light through all 5 compared with CM1P-O and the T6 icon-only hole? White showing around the icons from the front? Fit same as CM1P-O?

## Checks run (digital only)

FreeCAD: one valid solid, one shell, 253.5 cm3. `python pack_check.py` from `src/`: 0 bad edges on the body and liners, 18888/37772 vertex/triangle tags, 21 objects. Sampled surface points inside the modem envelope, liners included: 0 with the drawn lean removed; 8 as drawn, the intended overlap at the arm tips, same as CM1P-P. No slicer check.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_q_freecad.py').read())"`; `python pack_check.py`; `python compare_to_p.py`.
