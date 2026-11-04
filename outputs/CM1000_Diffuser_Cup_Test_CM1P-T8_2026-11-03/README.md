# CM1000 diffuser cup test — test-print ID CM1P-T8 (2026-11-03)

PROPOSED — UNPRINTED. Brian chose option C: five clear cups that go in from behind, down the existing tunnels, each with its own raised icon on the face. This slice tests the cup fit and the light. It has no rails, no rack slots and says nothing about strength. Remix of noyoustupid / Jsmaz3 (CC BY-NC-SA): in-house only.

## Print

`CM1P-T8_diffuser_cup_test.3mf`, also in `outputs/Final_3MF/`: 6 separate objects, no supports, front faces on the bed.

- **Body:** 70 x 44.45 x 26.75 mm, about 44 cm3, opaque filament. ID engraved on the top face.
- **5 cups:** about 8.4 across x 5.6 tall, clear filament. The icon side is on the bed. A smooth bed helps the first two layers. Each is named for its icon: network, internet, upstream, downstream, power.

The cups are too small for a readable ID. Each one is identified by its icon, and only fits its own hole.

## What's in it

Same plate, lips and modem stops as CM1P-T7 and CM1P-P, same Y and Z positions. The icons are at X 104 to 150, 11.5 apart, Z 30.225.

| | Size | Notes |
|---|---|---|
| Plate icon holes | 0.4 skin, opened 0.1 per side from CM1P-P | Thinnest skin strip about 0.32, at the network and internet icons |
| Cup icon | 0.4 raised | Trimmed to 3.88 radius so it passes the 7.99 bore. Thinnest stroke about 0.46, on the network icon |
| Cup disc | 7.8 across, 1.1 thick | With the icon, 1.5 of clear plastic in the light path, same as CM1P-T6's best hole |
| Cup skirt | 7.8 outside, 6.3 inside, ends 5.6 back from the front | 4 slits 0.8 wide, each leg about 3.7 long |
| Barb | 8.4 across, 0.2 per side over the skirt's bore | Clicks into a groove 8.7 across at Y 4.2 to 5.0 in each tunnel |

The two small details on the internet icon are gone: they would be loose pieces in the skin. Those spots are clear, so that icon is more of a solid saucer than a ringed planet.

## How to fit and test

1. With no modem in the slice, push each cup in from behind. Turn it until its icon lines up with the hole, then press until the barb clicks and the disc seats on the skin.
2. Sit the modem flat and powered, with the slice on the same table. Push the slice onto the modem's front until it stops, centred on the width.

## Report

- Did the raised icons go into their holes? Did any bind, or did any thin stroke or skin strip fail to print?
- Does each barb click and hold? Does any leg break?
- Do the icons sit flush with the front?
- Do all 5 light on the right LED? Any light in a neighbouring icon?
- Which clear filament was it? Changing filament only means reprinting the cups.

## Checks run (digital only)

FreeCAD: body one valid solid, one shell, 44.0 cm3. Cups network, internet, downstream and power reported valid, 0.12 to 0.13 cm3; cup upstream's report line was lost in the log, and its mesh passes the checks below. `python pack_check.py` from `src/`: 0 bad edges on all 6 parts, 0 sampled surface points inside the modem envelope, 0 overlap between the seated cups and the body on 9 slices from Y 0.2 to 5.3, 12456/24916 vertex/triangle tags, 6 objects, 6 build items. Cuts through the middle icon looked right. The check covers cups sitting seated, not the push-in motion. No slicer check. Fit, barb strength, light and neighbouring-icon bleed are UNKNOWN.

## Rebuild (PC)

Needs `outputs/CM1000_M6_2026-10-28/src/orig/`. From `src/`: `python icons_profile.py`; `OpenSCAD.exe -o id.stl id.scad`; `"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" -c "exec(open('cm1p_t8_freecad.py').read())"`; `python pack_check.py`.
