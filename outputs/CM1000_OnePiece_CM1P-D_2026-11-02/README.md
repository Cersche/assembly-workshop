# CM1000 one-piece bracket, solid fitment draft — test-print ID CM1P-D (2026-11-02)

PROPOSED — UNPRINTED. For fitment and mounting only (Brian). [CM1P-A](../CM1000_OnePiece_CM1P-A_2026-11-02/README.md)'s solid rails with [CM1P-C](../CM1000_OnePiece_CM1P-C_2026-11-02/README.md)'s plain front: no light pipes, logo, icons or colour parts. Brian dropped the rail windows because they saved no print time. Same 0.75 per side channel and nose pocket as T3, 4 ears, 4 corner rack slots, left-rail side slot, plate 254 x 44.45. The final bracket still needs the pipes, logo and icons back. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA): personal use, never redistribute.

## Print

`CM1P-D_CM1000_one_piece_bracket.3mf`, also in `outputs/Final_3MF/`: one object, one filament, front face on the bed. 254 x 44.45 x 137.62 mm. Slicer not run. ID engraved on the plate's top face.

## Limits

Full-length fit, rack fit, side screw and strength UNKNOWN. Checks are digital only: run `python pack_check.py` from `src/` (mesh edges, tags, modem envelope with the same assumptions as CM1P-A).

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_d_freecad.py').read())"`; `python pack_check.py`.
