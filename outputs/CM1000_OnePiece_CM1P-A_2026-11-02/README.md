# CM1000 one-piece bracket — test-print ID CM1P-A (2026-11-02)

PROPOSED — UNPRINTED. First full-length print of the one-piece bracket, built from CM1P-T3, which went on the modem by hand with 1.5 total side play and looked seated as far as T2 (read from photos, not measured). Fit over the full rail, rack fit, side screw and strength UNKNOWN. Replaces CM6A and CM6C; neither should be printed. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA): personal use, never redistribute.

## Print

`CM1P-A_CM1000_one_piece_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, no supports needed by the design (slicer not run). 254 x 44.45 x 137.62 mm, about 183 cm3 of solid volume. Assign filaments to the colour parts (5 light pipes, 7 logo parts, 2 details) as on the baseline. `CM1P-A_body_only.stl` is the body with empty pipe holes and recesses. ID engraved on the plate's top face.

## What it is

- Modem channel and nose pocket exactly as T3: 0.75 per side, 8 flat floor, 1.2 nose clearance, modem front stops 1.6 behind the plate front.
- Plain solid rails to Y 137.62 (baseline depth), outer width 220.46, no trusses or windows, no frame or other additions (Brian).
- Kept from the baseline: 4 corner rack slots, ears, logo, icons, 5 light pipes as separate colour parts. No joints, inserts or joint screws: it's one piece.
- Light pipes' rear ends trimmed from 8.72 to 8.34 by the pocket, as on T3. T3 had a plain front; this one has the real front back.
- Side screw slot on the left rail only (seen from the front), as on the baseline: baseline position, 1 longer at each end (Brian): Y 61.52..76.06, head recess Y 59.87..77.7 x 1.5 deep. Height changed: Z 20.55..24.69, because the baseline slot centre (22.99) and the reported modem hole height (22.25) disagree and this covers both. Screw centre range 61.4 to 73.0 behind the modem's front, 22.05 to 23.19 up. Brian checked the modem hole is inside the earlier 62.4 to 72.0 range; exact distance not recorded.

Rails are 0.05 short of the plate at top and bottom (coplanar faces lost the plate in the boolean), below one layer.

## Checks run (digital only)

From `src/`: FreeCAD reports one valid solid, one shell. `python pack_check.py`: all 15 parts closed with 0 bad edges, 17866/35728 vertex/triangle tags, 16 objects. No sampled surface point inside the modem envelope; cross-sections at Y 60, Y 69, X 18, X 90, Z mid and Y 0.1 inspected. The envelope assumes a straight nose taper, a 6 flat strip and 136 depth. No slicer check.

The plate's thinnest point is about 0.4 at the old V apex between X 40 and 214 (0.2 behind the logo recesses), unchanged from the baseline mesh.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_a_freecad.py').read())"`; `python pack_check.py`.
