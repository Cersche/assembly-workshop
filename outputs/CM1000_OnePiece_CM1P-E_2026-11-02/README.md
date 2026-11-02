# CM1000 one-piece bracket — test-print ID CM1P-E (2026-11-02)

PROPOSED — UNPRINTED. CM1P-A with a tighter modem channel. Brian printed A: the whole modem goes in easily, with a little too much play. Fit of this version, rack fit, side screw and strength UNKNOWN. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA): personal use, never redistribute.

## Print

`CM1P-E_CM1000_one_piece_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, same setup as CM1P-A (slicer not run). 254 x 44.45 x 137.62 mm, about 188 cm3 of solid volume. Assign filaments to the colour parts (5 light pipes, 7 logo parts, 2 details) as on the baseline. ID engraved on the plate's top face.

## What changed from CM1P-A

- Side clearance 0.75 to 0.50 per side, so total side play 1.5 to 1.0. Floors 213.19 to 212.69 apart, measured from both meshes at Y 100.
- The slopes move in with the floors, so the channel also closes up by about 0.33 in height per side on the slopes. Height play on the printed modem was not measured.
- The new ID. Nothing else: same pocket, rails, ears, slots, front and colour parts. See `outputs/CM1000_OnePiece_CM1P-A_2026-11-02/README.md`.

## Checks run (digital only)

FreeCAD reports one valid solid, one shell. `python pack_check.py`: 0 bad edges on the body, 16336/32668 vertex/triangle tags, 16 objects. No sampled surface point inside the modem envelope (same assumptions as CM1P-A). No slicer check.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_e_freecad.py').read())"`; `python pack_check.py`.
