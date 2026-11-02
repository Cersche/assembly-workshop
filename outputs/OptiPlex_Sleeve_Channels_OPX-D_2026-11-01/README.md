# OPX-D: OPX-C plus front post rails and rear ear middle screws (2026-11-01)

**Status:** CONCEPT for Brian's review, not packaged for print. OPX-C is still the current print file. Fit, strength and insert retention are UNKNOWN.

OPX-B with the PC 2.3 further forward (Brian, 2026-11-01): the case front is flush with the plate face and the raised bezel stands 2.3 proud of it. OPX-A and OPX-B stay in their own folders.

Brian chose this layout over the settled full-tray layout (2026-11-01, after being reminded of the "do not let me change this" note). PC orientation is unchanged: power button at the faceplate, ports toward the rear posts.

## Added to OPX-C (Brian: the PC is heavy)
- **Front post rails (OPX-D-RL, OPX-D-RR):** SG8-M6-F pattern, Y 6.2..60, 1 x M6 x 8 from behind into each front post's middle hole. They print flat, as installed.
- **Sleeve runners:** on both walls, riding the rails' 45 degree ledges with a hold-down. The front gussets are cut back to X 102.6 to clear the rails.
- **Rear ears:** a middle slot in each, 1 more M6 x 8 into the rear post's middle hole.
- **Hardware now:** 12 x M6 x 8, plus M6 inserts in 4 middle post holes (2 front, 2 rear).
- **Install order:** rails, then channels, then sleeve and PC from the front, then plate screws.

## Parts
| ID | File | Print |
|---|---|---|
| OPX-D-FRONT | `OPX-D-FRONT.stl` | Plate down |
| OPX-D-L, OPX-D-R | `OPX-D-L.stl`, `OPX-D-R.stl` | Ear down |

`PC_dummy.stl` is a check model, not a part. The rear add-ons on it are approximate, read off Brian's photos.

## Assembly
1. Screw both channels to the back of the rear posts: 4 x M6 x 8, 2 per channel.
2. Slide the PC into the sleeve from the sleeve's rear until its front feet click into the dips.
3. Slide the sleeve and PC in from the front of the rack, feeding the PC's rear into the channels. Screw the plate to the front posts: 4 x M6 x 8.

## Dimensions (mm)
- **PC, measured by Brian:** 182.5 wide, 178 deep including the bezel, 36 tall. The bezel starts at the left, is 122.5 x 23 from the bottom, and stands 2.3 proud. The old 194.5 depth is retired for this design.
- **Feet, measured by Brian:** 5 wide x 20 long (front to back), 15 from each side edge. Front pair 15 from the case front (17.3 from the bezel face), rear pair 10 from the rear edge. 2.8 tall.
- **Kept from printed SLV-F:** plate 252 x 44.4 x 4, four-corner slots, window +-91.75 x Z 3.5..40.8, 2.3 groove depth, dip through the floor.
- **Changed foot detail:** tracks are 6 wide and match the measured feet. Each dip is 21 long (SLV-F's 16 is too short for a 20 foot). The track is open at the rear and ends in a solid forward stop at Y 10.5, because the PC now enters from the rear. The rear side of the dip keeps the ramp.
- **Sleeve:** 65 deep, 4 mm walls, one piece with the plate, scooped floor and roof, gussets to the plate.
- **Channels:** Y 130.7..240, 41 mm grip on the case, 4 mm web. Ledge and roof are 12 wide along the case and narrow to 6 behind it. 1.5 mm lead-in at the front. Ear 4 mm thick, gusset to the web.

## Rear stops
Each channel has a stop, 5 wide and full height, with its face at Y 172.5, catching the case's rear corners. The seated case has 0.8 of play back to it, and a foot only reaches its ramp after 1.3, so the PC can't climb out of the dips once the plate is screwed on. Forward stop is still the feet. Loading is unchanged: the PC enters the bare sleeve from the rear, and the sleeve and PC go into the rack from the front.

## Dropped from SLV-F
Full tray floor, floor cable opening, rear crossbar, and the hidden plate screws (no plate joint is left).

## Digital checks
`python src/OPX-D_build.py <post.stl>` intersects the source modules against each other and the 4U post mesh (kept local, not in this folder). Controls must overlap or the run stops.

## Credits
Ideas, not meshes: Psychobob, "10" rack Optiplex shelf & rear bracket support" (one-piece flush shelf, scooped floor and roof); scubaroboto, "Optiplex 3060 Rear Support Bracket for 10" Rack" (rear C-channel, ear gusset). Geometry here is redrawn with our own dimensions.
