# CM1000 icon-only test slice — test-print ID CM1P-T7 (2026-11-03)

PROPOSED — UNPRINTED. Brian printed CM1P-T6: the icon-only hole passed the most light. He asked for a test set with icon only as a sanity check. This slice has all 5 icon-only pipes in their real places, so each icon sits on its own LED. It tests light only: no rails, no rack slots, no strength. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA): in-house only.

## Print

`CM1P-T7_icon_only_test_slice.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, no supports. 70 x 44.45 x 26.75 mm, about 44 cm3 of solid volume. ID engraved on the top face.

Assign the pipe filament to the 5 icons and 2 icon details, as on CM1P-T6.

## What's in it

CM1P-T6's plate, lips and modem stops, same Y and Z positions as CM1P-O. Each icon is CM1P-T6's hole 1: 1.5 deep, with the open tunnel behind it, about 10.5 of air to the LED on the centre line. Left to right from the front: network, internet, upstream, downstream, power, at X 104 to 150, centred on X 127, 11.5 apart. The LED position is from the pipe height, not measured.

## How to test

Sit the modem flat and powered, with the slice on the same table. Push the slice onto the modem's front until it stops, and centre it on the modem's width: the middle icon on the middle LED.

## Report

Do all 5 show light? Is each icon lit on the right LED, or does any LED fall off-centre? Any light leaking into a neighbouring icon?

## Checks run (digital only)

FreeCAD: body one valid solid, one shell, 44.0 cm3; each icon valid. `python pack_check.py` from `src/`: 0 bad edges on every part, 0 of 197708 sampled surface points inside the modem envelope, no body wall in any tunnel, 14124/28244 vertex/triangle tags, 9 objects, 1 build item. Cuts of the front skin and through the middle icon looked right. No slicer check. Light, slide-on fit and the stop are UNKNOWN.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: `OpenSCAD.exe -o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_t7_freecad.py').read())"`; `python pack_check.py`.
