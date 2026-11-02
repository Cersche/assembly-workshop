# CM1000 one-piece bracket, skeleton rails — test-print ID CM1P-B (2026-11-02)

PROPOSED — UNPRINTED fitment draft. [CM1P-A](../CM1000_OnePiece_CM1P-A_2026-11-02/README.md) with windows in the rails to shorten the print (Brian). Everything else as CM1P-A: same 0.75 per side channel and nose pocket as T3, 4 ears, plate 254 x 44.45, left-rail side slot, colour parts. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA): personal use, never redistribute.

## Print

`CM1P-B_CM1000_one_piece_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed. 254 x 44.45 x 137.62 mm, 136.6 cm3 of solid volume (CM1P-A 184.9). Slicer not run, so real print time saved is unknown. ID engraved on the plate's top face.

## Rail windows

Four windows per rail wedge pair (two top, two bottom, each rail): Y 30..65 and Y 86.5..116 at the channel side, open to the rail's outer and top/bottom faces, roofs rising 45 deg to about Y 81 and Y 132 at the outer face so front-down printing needs no supports. Left: the full channel face as a 2 thick shell, a centre bar Z 15..29.45 (holds the floor and the side slot), the solid first 30 as T3, a rib at about Y 81..86.5 and the rear 5.4.

## Limits

Thinner rails can flex open, so a good slide here is weaker evidence of channel fit than on a solid rail, and rail strength under the modem's weight is worse than CM1P-A's. Fit, rack fit, side screw and strength UNKNOWN.

## Checks run (digital only)

FreeCAD: one valid solid, one shell. `python pack_check.py`: 0 bad edges, 16456/32908 vertex/triangle tags, no sampled point inside the modem envelope (same assumptions as CM1P-A). Sections at Y 50, Y 84, X 18, X 25 and Z 6 inspected.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_b_freecad.py').read())"`; `python pack_check.py`.
