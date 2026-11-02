# CM1000 one-piece bracket, plain fitment draft — test-print ID CM1P-C (2026-11-02)

PROPOSED — UNPRINTED. For fitment and mounting only (Brian). [CM1P-B](../CM1000_OnePiece_CM1P-B_2026-11-02/README.md) without light pipes, logo, icons or colour parts. Same 0.75 per side channel and nose pocket as T3, rail windows as CM1P-B, 4 ears, 4 corner rack slots, left-rail side slot, plate 254 x 44.45. The final bracket still needs the pipes, logo and icons back. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA): personal use, never redistribute.

## Print

`CM1P-C_CM1000_one_piece_bracket.3mf`, also in `outputs/Final_3MF/`: one object, one filament, front face on the bed. 254 x 44.45 x 137.62 mm, 136.7 cm3 of solid volume. Slicer not run. ID engraved on the plate's top face.

## Front

The band X 25..156, Z 19..35 holding the logo, icons and pipe holes is closed with a 0.6 skin, as T3. The pipe holes stay as blind pockets behind it. The skin sits 0.02 back from the front face, below one layer.

## Limits

As CM1P-B: thin rails can flex open, so a good slide is weaker fit evidence than on solid rails, and the rails are weaker under load. Fit, rack fit, side screw and strength UNKNOWN.

## Checks run (digital only)

FreeCAD: one valid solid, one shell. `python pack_check.py`: 0 bad edges, 6460/12936 vertex/triangle tags, no sampled point inside the modem envelope (same assumptions as CM1P-A). Sections at Y 0.3, Y 5 and X 127 inspected.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_c_freecad.py').read())"`; `python pack_check.py`.
