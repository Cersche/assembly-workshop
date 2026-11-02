# CM1000 one-piece bracket — test-print ID CM1P-F (2026-11-02)

PROPOSED — UNPRINTED. CM1P-E with a tighter modem channel and squared front edges. Brian printed E: still too loose, it barely holds the modem, and a thin strip looks missing at the top of the plate from the front. Fit of this version, rack fit, side screw and strength UNKNOWN. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA): personal use, never redistribute.

## Print

`CM1P-F_CM1000_one_piece_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, same setup as CM1P-A (slicer not run). 254 x 44.45 x 137.62 mm, about 191 cm3 of solid volume. Assign filaments to the colour parts as on the baseline. ID engraved on the plate's top face.

## What changed from CM1P-E

- Side clearance 0.50 to 0.25 per side, so total side play 1.0 to 0.5. Floors 212.69 to 212.19 apart, measured from both meshes at Y 100. The slopes move in with the floors, about 0.33 per side in height.
- Front edges squared between the ears, top and bottom. The ear fills added on CM1P-A square off the baseline's 0.5 front chamfer on the ears only, so at the front face the plate middle stopped about 0.45 short of the ears (Z 0.45..44.0 against 0.05..44.4 at Y 0.1). All of it now reads Z 0.05..44.4. That this is the strip Brian saw is an inference from the mesh, not confirmed.
- The new ID. Nothing else.

## Not addressed

The rails hang off a plate about 0.4 thin at the V apex, and the modem's weight on the sloped faces pushes them apart. If that flex is part of the looseness, tighter clearance won't fully cure it. Not measured.

## Checks run (digital only)

FreeCAD reports one valid solid, one shell. `python pack_check.py`: 0 bad edges on the body, 16336/32668 vertex/triangle tags, 16 objects. No sampled surface point inside the modem envelope (same assumptions as CM1P-A). No slicer check.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_f_freecad.py').read())"`; `python pack_check.py`.
