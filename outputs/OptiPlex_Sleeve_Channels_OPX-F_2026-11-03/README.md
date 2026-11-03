# OPX-F: looser post rails, second step (2026-11-03)

**Status:** unprinted. Print only these two rails: `OPX-F_OptiPlex_post_rails.3mf`, also in `outputs/Final_3MF/`. 2 objects, 2444/4888 tags, 0 open edges. Not opened in a slicer. Fit and strength are UNKNOWN.

Brian printed the OPX-E rails: the fit improved but is still a little too tight in the rails. The rear stops and feet line up fine. He gave no amount this time, so another 0.5 per side is Claude's choice.

## What changed
The rail channel moved another 0.5 outward on each rail, 1.0 in total from OPX-D. The rail's inner face moved out 0.5 with it, so the lip at the inner edge stays 1.4 thick as on OPX-E. The printed `OPX-D-FRONT`, `OPX-D-L` and `OPX-D-R` are reused and not reprinted. Their modules in `src/OPX-F.scad` are unchanged and keep their OPX-D IDs.

| Runner gap to the rail (mm) | OPX-D | OPX-E | OPX-F |
|---|---|---|---|
| Down to the 45 degree ledge | 0.1 | 0.6 | 1.1 |
| Up to the hold-down | 0.35 | 0.85 | 1.35 |
| Outward at the tip | 0.25 | 0.75 | 1.25 |
| Sideways before a slope touches | 0.1 | 0.6 | 1.1 |

## Parts
| ID | File | Print |
|---|---|---|
| OPX-F-RL, OPX-F-RR | `OPX-F-RL.stl`, `OPX-F-RR.stl` | Flat, as installed |

Each rail still takes 1 x M6 x 8 from behind into the front post's middle hole.

## Things to watch
- The rails only carry the sleeve after it drops about 1.1, so the plate screws take the front's weight first. How far the front sags is UNKNOWN.
- The wall behind the channel tip, in the narrow rear part of the rail, is now 2.25 thick (3.25 on OPX-D). Its strength is UNKNOWN.
- OPX-E already had 0.6 on every face and still felt tight. Clearance may not be the only cause: each rail hangs on one screw and can pivot, and the runners' 45 degree faces can wedge under the PC's weight. Neither is tested.

## Digital checks
`python src/OPX-F_build.py <post.stl>` runs the OPX-D checks with the new rails against the OPX-D sleeve, channels, dummy PC and 4U post mesh (kept local, not in this folder). Last run 2026-11-03: controls overlapped, rear stops catch the PC, 0 overlaps. The sleeve clears each rail when moved 1.0 down, 1.3 up and 1.0 sideways, and hits it at 1.2 down, 1.45 up and 1.2 sideways, so it is still captured. These use a middle section of the 4U post, not the slot the PC lands in.

`python src/pack_3mf.py <out.3mf>` builds the 3MF.
