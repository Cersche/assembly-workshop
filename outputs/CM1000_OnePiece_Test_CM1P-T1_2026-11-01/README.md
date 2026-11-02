# CM1000 one-piece bracket, test slice — test-print ID CM1P-T1 (2026-11-01)

PROPOSED — UNPRINTED. Checks the planned one-piece bracket's pocket and channels on the real modem before the long print. It has no rack slots, so it does not test rack fit or strength. Brian chose one-piece solid rails after rejecting CM6C's rails.

Print `CM1P-T1_test_slice.3mf`: one object, front face on the bed, no supports. 234 x 44.45 x 30 mm, 52 cm3 of solid volume.

## Modem numbers used

Brian measured: 212 tip to tip, 44.4 tall, 14 end wedge, 44.4 just inside the wedge, 3 tall at the very front, 44.4 at 15 back, about 136 deep, side hole 22.25 up.

Assumed, because the shapes are safe or the test print will show them: end tip pointed and centred; nose a straight taper reaching full height 15 back; corners ignored, since rounded corners only add room.

## Design

- Width across the rails 220.46, unchanged. Channel tip x20.6, 0.4 clear across the width, 3.83 wall at the tip.
- Pocket 0.7 clear in height on the nose, front wall 1.6, modem front seats at Y2.
- Two end blocks, 14 mm of channel behind the pocket rim, tied by two 3.5 x 13 strips along the top and bottom faces. The middle is open so the modem's front is visible.

## How to test

Press it on from behind the modem's front, by hand, and note: does it seat without force, does anything rock, and how big is the gap between the modem's front and the front wall (design 0.4)?

## Checks run (digital only)

`python pack_check.py`: closed mesh; no sampled point inside the modem envelope; 328 vertex and 656 triangle tags.

## Open

Brian's numbers predict about 1.3 mm overlap per side on CM6A, but its rails spread 3.8 per side. This is unexplained; it may be rail twist or a modem shape these numbers miss. Printed fit UNKNOWN.

## Rebuild (PC)

From `src/`: OpenSCAD.exe `-o ../CM1P-T1_test_slice.stl cm1p_t1.scad`, then `python pack_check.py`.
