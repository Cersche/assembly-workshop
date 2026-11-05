# OPX-G: rear channels with a cable pass-through (2026-11-04)

**Status:** unprinted. Print only these two channels: `OPX-G_OptiPlex_rear_channels.3mf`, also in `outputs/Final_3MF/`. 2 objects, 2422/4868 tags, 0 open edges. Not opened in a slicer. Fit and strength are UNKNOWN.

Brian printed the OPX-F rails and reports a good fit, then asked for a cable pass-through on the rear brackets. He did not give a position or size, so both are Claude's choice.

## What changed
Each channel's web gets one window, so cables can go from behind the PC out to the side, into the space beside the rear post. Everything else on the channels matches printed OPX-D-L and OPX-D-R. Reused and not reprinted: `OPX-D-FRONT` and the OPX-F rails. Their modules in `src/OPX-G.scad` are unchanged and keep their IDs.

- **Window:** about 31 long (Y 181..212) x 28 tall (Z 8.2..36.2), through the 4 mm web, R3 corners. It sits behind the rear stop and ahead of the gusset.
- **Shape:** the front end is a 45 degree peak, so it should print ear-down without support. Only Y 194..212 is full height.
- **Left in the web:** 8 mm above and below the window, plus the ledge and roof.

## Parts
| ID | File | Print |
|---|---|---|
| OPX-G-L, OPX-G-R | `OPX-G-L.stl`, `OPX-G-R.stl` | Ear down |

Screws are unchanged: 3 x M6 x 8 per channel into the rear post.

## Things to watch
- All of the PC's rear load passes through this stretch of web to the ear. How much the window reduces stiffness is UNKNOWN.
- Whether your plugs fit through is UNKNOWN: no plug sizes were given.
- The window edges are not chamfered, so check for rubbing on cables.

## Digital checks
`python src/OPX-G_build.py <post.stl>` runs the earlier checks with the new channels against the OPX-D sleeve, OPX-F rails, dummy PC and 4U post mesh (kept local, not in this folder). Last run 2026-11-04: controls overlapped, rear stops catch the PC, 0 overlaps. A block filling each window from inside the channel out to 0.6 short of the post's side wall touches nothing; moved 40 forward it hits the web. These use a middle section of the 4U post, not the slot the PC lands in.

`python src/pack_3mf.py <out.3mf>` builds the 3MF.
