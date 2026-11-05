# CSB-A cable span bracket (2026-11-05)

A cable trough one U tall that spans from the front post to the rear post on one side of the rack. **The same part fits either side:** for the left, turn it 180 degrees about the vertical axis, so its front end goes to the rear. First revision; nothing earlier printed. Released when Brian said he is printing it.

| File | What |
| --- | --- |
| `CSB-A_1-parts-print-layout.3mf` | Print file, 1 object. Prints as installed: floor on the bed |
| `CSB-A_bracket.stl` | Same part in rack position (right side, slot frame: Y 0 front of front post, Z 0 slot bottom) |
| `src/span_bracket.scad` | Source; set `OPENSCADPATH` to `src/lib`. Switches: `soft`, `vented`, `wall_windows`, `dropout`, `hooks`; `part="left"` shows the left-side pose |
| `release_report.md` | Release checks: 0 failed, 0 warnings |

## Shape
- **Size:** 227.4 long x 24 wide x 44.4 tall, X 110.5 to 134.5 in the rack.
- **Mounting:** one M6 x 8 button head at each end, into the M6 insert in the **middle hole** of that U, front and rear posts. Each end pad is 8 thick, with 2.5 under the head, a 6.6 clearance hole and an open 11.5 head recess. Corner holes get only Ø9 x 4 reliefs behind any faceplate screws.
- **Fit gaps:** 0.3 at each end to the flanges, 0.32 to the post side walls. Pads are notched round the flange/side-wall fillet. Nearest gap to the post mesh is 0.22.
- **Trough:** 3 floor, 2.5 walls. The inner wall is 20 tall between the fingers, so cables can leave sideways, except beside the drop-outs, where it is full height.
- **Fingers:** 7, alternating from each wall, each leaving an 8 gap. 45 degree undersides, so no supports. There is one finger over each drop-out (Brian).
- **Drop-outs:** one 18 x 13.5 near each end, Y 40..58 and 182..200, through the floor in the outer lane. An 8 mm strip of outer wall is left across the top as a bridge, which keeps it stiff sideways (8.1k mm4 against 0.7k fully open).
- **Styling:** soft (rounded outside corners and finger tips) and floor slots. The outer wall windows were tried and closed again (Brian); the hooks option is off.
- **ID:** `CSB-A`, engraved 0.6 deep in the outer face of the outer wall, mid-length.

## Values used
- **Measured by Brian:** C = 16.0, flange edge to the inner face of the side wall.
- **From the source model,** on Brian's direction to continue with them (see `docs/devices/lab-rax-4u-post.md`; still UNKNOWN as measurements):
  - A: 228.0 flange to flange
  - B: 29.0 side wall length
  - D: 6.0 flange thickness
  - E: 3.3 flange edge to the middle hole
  - F: 15.9 hole spacing
- **No earlier printed clearances** apply to this part.

## Hardware
2 x M6 x 8 button head and 2 x M6 x 5 x 8 heat-set inserts, one in each post's middle hole for that U (front and rear). Insert fit in the posts is UNKNOWN.

## Install
1. Remove that U's faceplate.
2. Slide the bracket straight in through the front, inside the flanges.
3. Move it sideways onto the posts and fit both screws.

It can't share a U on the same side with a post-rail bracket (SG8, OPX, CM1P), because those use the same front middle hole.

## UNKNOWN
- Printed fit, especially length A.
- Insert fit, and room for the screwdriver at the recesses.
- Rocking about the two-screw line.
- Stiffness and strength, cable capacity and retention.
- Power plug sizes through the drop-outs.
- Whether the lane below each drop-out is clear in other U's (only checked against the SG8 rail sizes).
- Slicer result, bridges over the head recesses and drop-outs.
