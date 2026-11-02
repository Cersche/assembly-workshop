# CM1000 one-piece bracket, test slice 3 — test-print ID CM1P-T3 (2026-11-02)

PROPOSED — UNPRINTED. CM1P-T2 went on very easily with about 3.31 total play and the modem's front touching the end-block walls. T3 sets the clearance from that and tests what T2's open middle could not: the real faceplate's nose pocket and light pipes. No rack slots and no side slot: it does not test rack fit, the side screw or strength.

Print `CM1P-T3_test_slice.3mf`: one object, front face on the bed, no supports. 220.46 x 44.45 x 30 mm, about 92 cm3 of solid volume, so much heavier than T2.

## Changes from T2

- Clearance across the width 0.75 per side, about 1.5 total play (T2 1.5 per side). Channel floors 213.19 apart, tip wall 3.64. Modem width 211.69 = 215 less 3.31 play, assuming nothing flexed.
- Middle is the real faceplate (baseline mesh) with the light pipes merged in, not an open frame.
- The old pocket was recut across the whole width to T2's nose clearance (1.2 in height), which also trims about 0.8 off the pipes' rear ends. The old pocket left about 0.1 at the pipes.
- The modem's front stops on 1.6 walls at each end, as T2 (they run from the channel floor to X 25, short of where the icons will go).
- Plain front: the logo and icon recesses are left out (they cracked the mesh and don't affect fit). The full bracket will need them back.

Choosing 0.75 is a judgement, not a tested number. It also has to work over the full bracket's 120 mm of rail, which this 30 mm slice cannot show.

## How to test

Before taking T2 off the modem, seat it and draw a pencil line on the modem along T2's rear edge. Then press T3 on by hand. Report:

1. Does it go on without force?
2. Total side play (design about 1.5).
3. Does T3's rear edge reach the pencil line? Both slices are 30 deep, so if it does, the nose and pipes aren't holding the modem back.

## Checks run (digital only)

`python pack_check.py` from `src/`: closed mesh, 0 bad edges, 552/1100 vertex/triangle tags. The point check found nothing inside the modem envelope, but it samples few points on this coarse mesh; cross-sections at X 23, 90 and 127 and Y 25 were also inspected and clear. The modem envelope assumes a straight nose taper and a 6 flat strip. Printed fit UNKNOWN.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/` (`extract.py` there). From `src/`: OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_t3_freecad.py').read())"`; `python pack_check.py`. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA): personal use, never redistribute.
