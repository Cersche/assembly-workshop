# CM1000 one-piece bracket, test slice 2 — test-print ID CM1P-T2 (2026-11-01)

PROPOSED — UNPRINTED. CM1P-T1 was too tight: it had to be really forced on and its tie strips bowed. T2 is deliberately loose, so the play can be measured and the final clearance set from it. No rack slots: it does not test rack fit or strength.

Print `CM1P-T2_test_slice.3mf`: one object, front face on the bed, no supports. 220.46 x 44.45 x 30 mm.

## Changes from T1

- Clearance across the width 1.5 per side (was 0.4). Channel tip wall 2.73.
- Flat channel floor 8 wide, for the modem's flat end strip (the strip's width is unmeasured; it looks narrower).
- Nose clearance 1.2 (was 0.7); the modem's front stops on the wall.
- 1.6 front wall across the whole width, with a 134 x 16 window, so the frame can't bow. This is closer to the real faceplate.

## How to test

Press it on by hand. Report: does it go on without force, how far does it slide side to side (total play), and does the modem's front reach the wall (look through the window)?

## Checks run (digital only)

`python pack_check.py` from `src/`: closed mesh, no sampled point inside the modem envelope, tags counted. Printed fit UNKNOWN.

## Rebuild (PC)

From `src/`: OpenSCAD.exe `-o ../CM1P-T2_test_slice.stl cm1p_t2.scad`, then `python pack_check.py`.
