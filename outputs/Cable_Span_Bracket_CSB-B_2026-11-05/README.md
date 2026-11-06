# CSB-B cable span bracket (2026-11-05)

Second revision of the cable trough that spans from the front post to the rear post on one side of the rack, one U tall. **The same part fits either side:** for the left, turn it 180 degrees about the vertical axis. Made from printed CSB-A (`../Cable_Span_Bracket_CSB-A_2026-11-05/`), which fits but left no room for a driver. Released when Brian said he is printing it.

| File | What |
| --- | --- |
| `CSB-B_1-parts-print-layout.3mf` | Print file, 1 object. Prints as installed: floor on the bed |
| `CSB-B_bracket.stl` | Same part in rack position (right side, slot frame: Y 0 front of front post, Z 0 slot bottom) |
| `src/span_bracket.scad` | Source; set `OPENSCADPATH` to `src/lib`. `part="demo_key"` shows the hex key in the front screw |
| `release_report.md` | Release checks: 0 failed, 0 warnings |

## Changes from CSB-A
- **Tool windows:** between each end pad and its drop-out, the inner wall is cut down to 6 tall. A 4 mm hex L-key with a 30 mm short arm (Brian) reaches the screw and turns from -30 to +30 degrees in the model. Arms up to about 33 fit. The key's long arm points into the rack, so that U must be empty while you screw it in.
- **Drop-outs** moved 4 mm away from the ends, to Y 44..62 and 178..196, with their fingers. The drop-out section is still stiff: 58k mm4 up/down and 10k sideways.
- **Zip-tie slot pairs** replace the cross floor slots (Brian). Four pairs sit between the fingers. Each slot is 6.5 x 3 against a wall, for ties up to 4.8 wide. A 1.6 deep groove under the floor joins each pair so the band sits flush, leaving 1.4 of floor over it.
- **ID:** `CSB-B`, engraved 0.6 deep in the outer face of the outer wall, mid-length.

## Unchanged from CSB-A (printed, fits)
- **Size:** 227.4 x 24 x 44.4, X 110.5 to 134.5.
- **Gaps:** 0.3 at each end to the flanges and 0.32 to the post side walls. The nearest gap to the post mesh is 0.22.
- **Mounting:** one M6 x 8 button head at each end into the middle-hole insert of that U. The pads are 8 thick, with 2.5 under the head, a 6.6 hole and an 11.5 head recess.
- **Trough:** 3 floor, 2.5 walls, 7 weave fingers with an 8 gap, soft corners.

## Hardware
- 2 x M6 x 8 button head.
- 2 x M6 x 5 x 8 heat-set inserts in the posts' middle holes.
- Zip ties up to 4.8 wide.

## Install
1. Remove that U's faceplate.
2. Slide the bracket in through the front.
3. Move it sideways onto the posts.
4. Screw both ends with the L-key through the tool windows.

It can't share a U on the same side with a post-rail bracket (SG8, OPX, CM1P).

## UNKNOWN
- Driver access in real life (checked only with a modelled key).
- Strength of the 1.4 floor over the tie grooves.
- Insert fit, rocking, strength, cable capacity and power plug sizes.
- Slicer result.
