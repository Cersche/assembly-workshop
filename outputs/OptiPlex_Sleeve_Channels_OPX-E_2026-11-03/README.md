# OPX-E: looser post rails for the printed OPX-D sleeve (2026-11-03)

**Status:** unprinted. Print only these two rails: `OPX-E_OptiPlex_post_rails.3mf`, also in `outputs/Final_3MF/`. 2 objects, 2446/4892 tags, 0 open edges. Not opened in a slicer. Fit and strength are UNKNOWN.

Brian printed OPX-D and reported that inserting the PC and faceplate into the rack was just a tiny bit too tight. He asked for about 0.5 more on each side between the rails and the faceplate's runners.

## What changed
Only the rail channel, moved 0.5 outward on each rail. Everything else stays as the printed OPX-D parts: `OPX-D-FRONT`, `OPX-D-L`, `OPX-D-R` are reused and not reprinted. Their modules in `src/OPX-E.scad` are unchanged and keep their OPX-D IDs.

| Runner gap to the rail (mm) | OPX-D | OPX-E |
|---|---|---|
| Down to the 45 degree ledge | 0.1 | 0.6 |
| Up to the hold-down | 0.35 | 0.85 |
| Outward at the tip | 0.25 | 0.75 |
| Sideways before a slope touches | 0.1 | 0.6 |

## Parts
| ID | File | Print |
|---|---|---|
| OPX-E-RL, OPX-E-RR | `OPX-E-RL.stl`, `OPX-E-RR.stl` | Flat, as installed |

Each rail still takes 1 x M6 x 8 from behind into the front post's middle hole.

## Things to watch
- The rails no longer carry the sleeve until it drops about 0.6, so the plate screws take the front's weight first. How far the front sags is UNKNOWN.
- The rail's lip at its inner edge drops from 1.9 to 1.4 thick. Its strength is UNKNOWN.

## Digital checks
`python src/OPX-E_build.py <post.stl>` runs the OPX-D checks with the new rails against the OPX-D sleeve, channels, dummy PC and 4U post mesh (kept local, not in this folder). Last run 2026-11-03: controls overlapped, rear stops catch the PC, 0 overlaps. The sleeve clears each rail when moved 0.5 down, 0.8 up and 0.5 sideways, and hits it at 0.7 down, 0.95 up and 0.7 sideways, so it is still captured. These use a middle section of the 4U post, not the slot the PC lands in.

`python src/pack_3mf.py <out.3mf>` builds the 3MF.
