# CSB-C cable span bracket (2026-11-07)

Third revision of the one-U cable trough from the front post to the rear post on one side of the rack. **The same part fits either side:** for the left, turn it 180 degrees about the vertical axis. Made from CSB-B (`../Cable_Span_Bracket_CSB-B_2026-11-05/`). Released when Brian said he is printing it.

| File | What |
| --- | --- |
| `CSB-C_1-parts-print-layout.3mf` | Print file, 1 object. Prints as installed: floor on the bed |
| `CSB-C_bracket.stl` | Same part in rack position (right side, slot frame: Y 0 front of front post, Z 0 slot bottom) |
| `src/span_bracket.scad` | Source; set `OPENSCADPATH` to `src/lib`. `part="demo_key"` shows the hex key in the front screw |
| `release_report.md` | Release checks: 0 failed, 0 warnings |

## Changes from CSB-B
- **Screw seat 4.5 under the head** (CSB-B 2.5), for **M6 x 10** button heads (Brian). On CSB-B an M6 x 10 stuck out 2 past the post; here it should come out about flush. The head recess is 3.5 deep.
- **Entry notch** between each pad and its drop-out: a rounded U, 8 wide, cut through the low inner wall and the floor from the inner edge to X 119. Cables from below come straight up into the channel (Brian). The mouth corners are rounded.
  - **Section at the notch:** up/down 24k mm4, sideways 0.3k (3.7k beside it). Only the side wall carries this short stretch next to the bolted pad.
- **Hex key:** a 30 mm short arm still turns from -30 to +30 degrees in the model; the limit is now about 31 (CSB-B about 33).
- Zip-tie anchors on the side wall were tried in the draft and removed (Brian).
- **ID:** `CSB-C`, engraved 0.6 deep in the outer face of the outer wall, mid-length.

## Unchanged from CSB-B
- **Size and fit:** 227.4 x 24 x 44.4, X 110.5 to 134.5. The nearest gap to the post mesh is 0.22.
- **Tool windows:** each is 6 tall.
- **Drop-outs:** Y 44..62 and 178..196.
- **Zip-tie slot pairs:** four in the floor.
- **Trough:** 7 weave fingers, soft corners.

## Hardware
- 2 x M6 x 10 button head.
- 2 x M6 x 5 x 8 heat-set inserts, in the posts' middle holes.
- Zip ties up to 4.8 wide.

## Install
1. Remove that U's faceplate.
2. Slide the bracket in through the front.
3. Move it sideways onto the posts.
4. Screw both ends with the L-key through the tool windows. That U must be empty while you screw.

It can't share a U on the same side with a post-rail bracket (SG8, OPX, CM1P).

## UNKNOWN
- Screw end flush with an M6 x 10 (worked out from Brian's CSB-B report, not tested).
- Sideways stiffness at the entry notches.
- Strength of the floor over the tie grooves.
- Insert fit, rocking, strength, cable capacity, slicer result.
