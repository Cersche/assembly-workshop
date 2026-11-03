# CM1000 one-piece bracket — test-print ID CM1P-K (2026-11-02)

PROPOSED — UNPRINTED. CM1P-J with both plate lips recut parallel to the modem's front slope. Everything else as CM1P-J. Fit, rack fit, side screw, light visibility, insert fit and strength UNKNOWN. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA); V dimensions from CM1000_1U_Mount (source not recorded). In-house only.

## Print

`CM1P-K_CM1000_one_piece_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, same setup as CM1P-A (slicer not run). 254 x 44.45 x 137.62 mm, about 244 cm3 of solid volume (CM1P-J 203). Assign filaments to the logo and icon parts. ID engraved on the plate's top face.

## What changed from CM1P-J

- **Lip slope:** 39.6 degrees off the front-to-back line, the modem's slope, instead of 54. Brian's readings: top flat 106 and underside flat 106, so 25 deep on both.
- **Gap to the modem:** 0.5 measured up and down all along the slope, about 0.39 square to the surface. CM1P-J had 1.2 at the nose, opening to 8.4 at its lip end.
- **Lip end:** Y 26.75 instead of Y 17.18, ending blunt and 1.4 thick, about the same as CM1P-J.
- **Floor beside the nose:** half height 2.0 instead of 2.7, with the nose relief's edges moved to match. The modem still stops on the end walls at Y 4.1.
- **Window tunnel:** same 54 x 8 opening and bevel. Lengthened through the thicker lip: top edge 16.2 deep (was 10.8), bottom edge 6.5 (was 5.1).

Why the gap is 0.5: with 0.25 play per side at the arm tips, the modem can move about 0.35 up or down on its end slopes, so 0.5 shouldn't bind on the design numbers. It is a starting point, not a proven number.

## Carried over from CM1P-J unchanged

V and arm tips (0.25 per side), 220.46 rails with 0.52 lean, modem front at Y 4.1, side screw slot, icons, logo, and the four M3 insert bores in the rail tips (4.2 x 4 deep, X 22.5 and 231.5, Z 5.5 and 38.95).

## Assumptions, not measurements

- Light positions come from the old pipes, not a lit modem. The deeper tunnel may shade the lights from low angles.
- The lean figures come from CM1P-E, which had a different channel.
- E's unexplained 1 of side play stays unexplained.
- Modem corners about R 8.5 from a photo, left square in the check.

## Report

Empty: width across the rail tips, outside (design 220.46). With the modem: does it go in by hand all the way, does the nose seat, side play at the tips (design about 0.5 total), firm at the front without squeezing, side screw, lights visible, rack fit.

## Checks run (digital only)

FreeCAD: one valid solid, one shell. `python pack_check.py` from `src/`: 0 bad edges on the body, 13168/26316 vertex/triangle tags, 14 objects. Sampled surface points inside the modem envelope (131 deep, 25 front slope, square corners): 0 with the drawn lean removed; a few as drawn from Y 82 back, up to 0.25 per side at the tips, the intended overlap. Side-on cuts at X 45, 70, 90, 127, 165, 190 and 210: smallest up-and-down gap to the modem 0.5, no cut edge inside the modem.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: `python make_icons.py`; OpenSCAD.exe `-o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_k_freecad.py').read())"`; `python pack_check.py`.
