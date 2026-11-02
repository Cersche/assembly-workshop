# CM1000 one-piece bracket — test-print ID CM1P-G (2026-11-02)

SUPERSEDED, do not print: the modem end wedge is 15, this uses 14. Print CM1P-H.

PROPOSED — UNPRINTED. CM1P-F with the V matched to the modem and the rails drawn leaning inward, built from Brian's measurements of the printed CM1P-E. Built without printing CM1P-T4 first (Brian's call), so the matched V is untested. Fit, rack fit, side screw and strength UNKNOWN. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA): personal use, never redistribute.

## Print

`CM1P-G_CM1000_one_piece_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, same setup as CM1P-A (slicer not run). 254 x 44.45 x 137.62 mm, about 198 cm3 of solid volume. Assign filaments to the colour parts as on the baseline. ID engraved on the plate's top face.

## What changed from CM1P-F

- V floor 8 to 4 wide with slopes re-aimed parallel to the modem's. Brian measured its end strip at 3. Largest slope gap about 0.6 on the assumed straight slope (F about 1.9).
- Rails lean in straight from the plate to the tips, 0.52 per side at the tips. E measured empty at its tips: outside 221.5 (design 220.46), V floors 214 (design 212.69). The outside growth of 1.04 sets the lean. The other 0.27 of floor growth is read as the print coming out slightly wide, which T2 and T3's play also suggest against the modem's measured 212.
- Side screw recess moved in with the rail, still 1.5 deep. Slot position unchanged.
- The new ID. Nothing else.

## As drawn (read from the mesh)

| Y back from the plate front | Outside | V floors |
| --- | --- | --- |
| 20 | 220.30 | 212.04 |
| 30 | 220.24 | 211.96 |
| 100 | 219.70 | 211.44 |
| 137.5 (tips) | 219.42 | 211.16 |

These are smaller than the modem past about Y 70 on purpose. The rails should print out to about 220.46 outside and 212.5 floors at the tips, about 0.5 total play. Check that with the bracket empty before forcing the modem in.

## Assumptions, not measurements

- The lean is straight and repeats on this print. Mid-rail on E was not measured. The heavier V could change how far the rails move.
- The modem's slopes are straight between the strip and full height.
- E's side play of 3 is about 1 more than 214 less 212. Not explained.
- If the rails print straighter than E's, the tips will be tight on the modem.

## Report

Empty: width across the rail tips, outside. With the modem: does it go in by hand all the way, side play at the tips (design about 0.5), does it feel firm without squeezing, side screw, rack fit.

## Checks run (digital only)

FreeCAD: one valid solid, one shell. `python pack_check.py` from `src/`: 0 bad edges on the body, 16454/32904 vertex/triangle tags, 16 objects. Sampled surface points inside the modem envelope: 0 with the drawn lean removed; 156 as drawn, starting at Y 69.6, which is the intended overlap. No slicer check.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_g_freecad.py').read())"`; `python pack_check.py`.
