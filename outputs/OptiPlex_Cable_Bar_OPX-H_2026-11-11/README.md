# OPX-H: rear channels with a cable bar rail, plus the cable bar (2026-11-11)

**Status:** unprinted. Print file: `OPX-H_3-parts-print-layout.3mf`, also in `outputs/Final_3MF/OPX-H_OptiPlex_rear_channels_and_cable_bar.3mf` (3 objects, 6134 vertices / 12448 triangles, all on the bed). Not opened in a slicer. Fit and strength are UNKNOWN.

Brian asked for a bar left to right between the OptiPlex rear channels, so cables crossing the rack (the OptiPlex is at the bottom, U1) have a path behind the PC. Of six drafted ideas he picked a dovetail rail on each channel with a bar that slides on from the rear and clicks. He then asked for: a wider cable entry where the bar meets the channel, zip-tie slots on the walls and floor, recesses for the tie bands, rounded edges, a cleaner window, rounded gusset ends, and rounded-rectangle walls.

## Parts
| ID on part | File | Print |
|---|---|---|
| OPX-H-L, OPX-H-R | `OPX-H_rear_left.stl`, `OPX-H_rear_right.stl` | Ear down, as OPX-G (the 3MF already has them turned) |
| OPX-H-BAR | `OPX-H_bar.stl` | Upright, floor on the bed |

The STLs stay in the rack position (frame as OPX-G); the 3MF has the print orientation. Reused, not reprinted: the printed OPX-D front sleeve and OPX-F rails.

## What changed from OPX-G (channels)
- **Rail:** a dovetail on the web's inner face, Y 219..240, 4 proud, Z 5.6..12.6 at the tip (7.1..11.1 at the web), with a 1.4 deep dimple 3 from its front end for the click, and a 1 mm step-down at its rear (entry) end.
- **Window:** one smooth outline, larger: low part Y 194..217 from Z 8.2, ramping up to Z 15.2 at Y 219, then running back above the rail to Y 234; top Z 36.2. Corners r 3 outside and r 8 inside, 1 mm 45 deg edge break on both faces.
- **Gusset:** starts at Y 222 (it was Y 215) with its front corners rounded r 2, and is cut 3 clear of the window so cables leave sideways.
- **Unchanged from OPX-G (which kept OPX-D's printed dimensions):** grip on the PC, ledges, roof, rear stop, lead-ins, ear plate and its three screw slots.

## The bar
- **Two-lane trough:** behind the PC, Y 214..236 (42 behind the PC's rear). Front wall 30 tall, divider 22 tall, both rounded rectangles; the back lip is 13 tall. The walls stop short of the end pieces so cables from the windows drop in at each end.
- **End pieces:** 14.6 tall with chamfered tops; each holds a groove for the rail.
  - Sliding it on: push the bar forward onto the rails from the rear. The closed back of each groove stops on the rail end (Y 240).
  - The click: a 1.5 thick spring strip in the groove's inner wall has a nub (0.9 interference) that drops into the rail's dimple. Pull firmly to remove.
- **Zip ties:** slots 5.5 x 2.6 (ties up to about 4.8 wide) at X -55, -33, -11, 11, 33, 55.
  - Front wall: 3 slots at the middle four stations, 2 at the outer two.
  - One slot in the back lip and two in the floor (one per lane) at every station.
  - Band recesses 6 wide x 1.2 deep: up the front face, across the underside and up the lip, so ties sit flush and nothing hangs below the bar (3.6 clear underneath).
- **ID:** OPX-H-BAR, on the flat top of the left end piece.

## Clearances
- Rail in the groove: 0.3 all round. The bar sits 0.3 above the channel's floor ledge and 0.3 inside the web faces.
- No fit values from a printed part were changed. The rail and bar clearances are new and unproven.

## Screws
3 per channel into the rear post's corner and middle holes, unchanged from OPX-G. The standard for new designs is now M6 x 10 button head (Brian, 2026-11-11). Through the 4 mm ear that puts 6 mm into the post's M6 insert; whether that bottoms out is UNKNOWN. If it does, use M6 x 8 as on OPX-G.

## Digital checks (`release_report.md`)
- `tools/release_part.py` with the PC dummy and the real rack posts placed for U1: 0 FAIL.
  - The two WARNs are the click dimples (3.2 dia, 1.4 deep) read as shallow M2.5 bores. They are intended.
- **Rack posts:** the ear touches the rear post face (gap 0.00, as designed); nothing overlaps.
- **PC:** nearest gap 0.20.
- **Screw heads:** a keep-out 1 mm around each M6 head behind the ears is clear.
- **Tie slots:** all 34 through slots are separate.
- **Done on the working file before release:**
  - The bar is clear of both channels when fitted, and along its slide-in path from 40 back (nub left off, since it flexes).
  - Moved 2 back, the nub hits the rail (the click catches). Moved 0.6 forward, the groove's back hits the rail end (the stop works).
- IDs checked on renders: present and bold; legibility after printing UNKNOWN.

## UNKNOWN
- Fit of the rail in the groove, click force and how many on/off cycles the spring strip takes.
- Stiffness of the channel web and the split gusset with the bigger window, carrying the PC's rear.
- Plug lengths: 42 from the PC's rear to the bar's front wall.
- Whether the groove's upper lip (4 mm overhang with the bar upright) prints cleanly.
- Strength of walls and floor at the band recesses (1.8 left).
- M6 x 10 depth in the post.

## Fit report to send back
- ID on each part (OPX-H-L, OPX-H-R, OPX-H-BAR).
- Channels: PC grip, rear stop and screws as OPX-G? Any sag at the PC's rear?
- Bar: slides on? Click felt and holds? Tight or loose in the groove, and by how much if measured?
- Cables: room at the windows and over the end pieces? Plugs clear of the front wall?
- Zip ties: width used, do they pass the slots and sit in the recesses?
- Screws used (M6 x 10 or x 8), walls and infill.

## Source
`src/OPX-H.scad` (frozen). Working file: `work/optiplex-cable-bar/cable_bar_v2.scad`.
