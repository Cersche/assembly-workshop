# CM1000 one-piece bracket — test-print ID CM1P-H (2026-11-02)

PROPOSED — UNPRINTED. CM1P-G with the V re-aimed for the modem's 15 end wedge: Brian marked 14 as 15 on the modem render. Everything else as CM1P-G. Matched V untested (CM1P-T4 used 14 and was not printed). Fit, rack fit, side screw and strength UNKNOWN. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA): personal use, never redistribute.

## Print

`CM1P-H_CM1000_one_piece_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, same setup as CM1P-A (slicer not run). 254 x 44.45 x 137.62 mm, about 203 cm3 of solid volume. Assign filaments to the colour parts as on the baseline. ID engraved on the plate's top face.

## The channel

- 0.25 per side at the plate end, 4 V floor, slopes running 15 across over the height. Largest slope gap about 0.6, next to the floor, on the assumed straight slope. With G's 14 it would have been about 1.25 at the shoulders.
- Rails lean in straight from the plate to the tips, 0.52 per side at the tips, from CM1P-E's measured 221.5 outside and 214 floors against design 220.46 and 212.69.

## As drawn (read from the mesh)

| Y back from the plate front | Outside | V floors |
| --- | --- | --- |
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

FreeCAD: one valid solid, one shell. `python pack_check.py` from `src/`: 0 bad edges on the body, 16406/32808 vertex/triangle tags, 16 objects. Sampled surface points inside the modem envelope: 0 with the drawn lean removed; 153 as drawn, starting at Y 69.6, which is the intended overlap. No slicer check.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_h_freecad.py').read())"`; `python pack_check.py`.
