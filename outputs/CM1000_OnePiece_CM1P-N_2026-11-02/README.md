# CM1000 one-piece bracket — test-print ID CM1P-N (2026-11-02)

PROPOSED — UNPRINTED. CM1P-M with the rails 10 longer at the rear, because Brian's printed bracket fits perfectly but the rails are a little short at the back. Fit of the added length, rack fit behind the modem, rail spread and strength UNKNOWN. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA); V dimensions from CM1000_1U_Mount (source not recorded). In-house only.

## Print

`CM1P-N_CM1000_one_piece_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, same setup as CM1P-M. 254 x 44.45 x 147.62 mm, about 252 cm3 of solid volume (CM1P-M 244). Assign filaments to the logo and icon parts. ID engraved on the plate's top face. 2 walls, 10% infill is the only setting proven for this fit.

## What changed from CM1P-M

- **Rails:** end at Y 147.62, were 137.62. They carry on straight along the same lines, with the same section, the same channel and the same lean per mm.
- **Four M3 rear-bar insert bores:** they sit in the rail end faces, so they moved back 10 with them (same size, X and Z; now Y 143.62 to 147.62). Left behind, they would be sealed voids inside the rails.
- **ID text:** CM1P-N, as every test print needs its own ID.

Nothing else changed. `python compare_to_m.py` cuts both bodies every 0.5 mm from Y 0.13 to 137.13 on a 0.1 mm grid: the only differences are the ID text, the old bores now solid from Y 133.63 back, and 7 stray grid cells in 5 slices (0.02 mm2 or less each slice).

## Not checked

- Length behind the modem: the rails now run about 12.5 past its rear (was 2.5). Clearance to anything behind the slot in the rack is unchecked.
- The rails printed with some outward spread on earlier revisions. 10 more length may add a little at the new tips; the part that holds the modem is the same.

## Report

Rail length right? Fit still the same as CM1P-M? Anything behind the rails hit in the rack?

## Checks run (digital only)

FreeCAD: one valid solid, one shell, 252.1 cm3. `python pack_check.py` from `src/`: 0 bad edges on the body, 13172/26324 vertex/triangle tags, 14 objects. Sampled surface points inside the modem envelope: 0 with the drawn lean removed; 8 as drawn, the intended overlap at the arm tips.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_n_freecad.py').read())"`; `python pack_check.py`; `python compare_to_m.py`.
