# CM1000 one-piece bracket — test-print ID CM1P-J (2026-11-02)

PROPOSED — UNPRINTED. CM1P-I plus four M3 insert bores in the rail tips for a later rear bar. Everything else as CM1P-I: one piece, the 86 degree V slope of Brian's CM1000_1U_Mount, a beveled window for the status lights instead of light pipes. Fit, rack fit, side screw, light visibility and strength UNKNOWN. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA); V dimensions from CM1000_1U_Mount (source not recorded). In-house only, Brian's workshop, never redistribute.

## Print

`CM1P-J_CM1000_one_piece_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, same setup as CM1P-A (slicer not run). 254 x 44.45 x 137.62 mm, about 203 cm3 of solid volume. Assign filaments to the logo and icon parts. ID engraved on the plate's top face.

## What changed from CM1P-I

- **Four insert bores:** 4.2 x 4 deep (M3 x 3 x 5), in the rail end faces at X 22.5 and 231.5, Z 5.5 and 38.95, entering from the rear. A 9 boss fits in solid rail around each. Open upward as printed. No bar yet; empty bores do no harm.

## Carried over from CM1P-H changes

- **V:** slope 43 degrees off vertical, as the mount. The modem's slope is 35.9, so it rides on the arm tips, not its end strip. 0.25 per side at the tips at the plate end. Arm tips 1.5 thick. Flat floor 8.64 tall, 215.3 across, 1.65 off the modem's end strip per side. The mount's full point would need 222.84 across, too wide for this rail.
- **Rails:** 220.46 outside and 0.52 lean per side at the tips, as H. Wall behind the floor 2.58. Length unchanged, 137.62. Lean is assumed to repeat on this V.
- **Window:** 54 x 8 clear at the old pipes' span, 2.5 bevel at 45 degrees, 59 x 13 at the front face. No pipes.
- **Modem 2.5 further back:** front at Y 4.1. Plate is 2.86 thick at the nose relief, about 2.5 under the window. Side screw slot moved back 2.5 with it (Y 64.02 to 78.56), the same place on the modem as the proven CM1P-E slot (Brian: keep it).
- **Icons:** the old pipes' icon shapes at 62%, inlaid 0.4 above the window, each over its light. The two detail specks in icon 2 are now plate-coloured islands.
- **Left out:** the mount's fins, because the modem slots are unconfirmed and deep fins can't slide in from the rear.

## Assumptions, not measurements

- Modem as Brian measured it: 212 x 131 x 44.4. The rails run about 2.5 past its rear. Corners about R 8.5 from a photo, left square in the check.

- Light positions come from the old pipes, not a lit modem.
- The hold depends on the 15 wedge, backed by Brian's 182 flat top (212 less 2 x 15). His front slope is 25, against the 15 this bracket's pocket assumes: no clash, but the arm tips start gripping about 23 back from the modem's front.
- The lean figures come from CM1P-E, which had a different channel.
- E's unexplained 1 of side play stays unexplained.

## Report

Empty: width across the rail tips, outside. With the modem: does it go in by hand all the way, side play at the tips (design about 0.5 total), firm without squeezing, side screw, lights visible, rack fit.

## Checks run (digital only)

FreeCAD: one valid solid, one shell. `python pack_check.py` from `src/`: 0 bad edges on the body, 13186/26352 vertex/triangle tags, 14 objects. Sampled surface points inside the modem envelope (131 deep, 25 front slope, square corners): 0 with the drawn lean removed; a few as drawn from Y 77.4 back, up to 0.25 per side at the tips, the intended overlap. Bores checked in a section 2 in from the rail end. No slicer check.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: `python make_icons.py`; OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_j_freecad.py').read())"`; `python pack_check.py`.
