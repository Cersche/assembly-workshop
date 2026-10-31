# SG8-M6-F — TP-Link TL-SG108E 1U tray on post rails (2026-10-30)

Test-print ID **SG8-M6-F** is engraved on every part: plate back above the window, outside of the tray's left sleeve wall, inner face of each post rail. **Not printed. Fit and strength UNKNOWN.**

The tray rides on **two post rails** bolted to the front posts and is also screwed to the faceplate with the hidden M6 joint. The faceplate is held by its usual four rack screws. So the tray is carried by the posts at both sides and tied to the plate at the front.

| File | What |
|---|---|
| `SG8-M6-F_TL-SG108E_post-rails_set.3mf` | Tray, left post rail, right post rail, faceplate + UPLINK label (one object, two parts). Plain vertex/triangle tags |
| `SG8-M6-F_tray.stl`, `SG8-M6-F_post-rail_left.stl`, `SG8-M6-F_post-rail_right.stl`, `SG8-M6-F_faceplate.stl`, `SG8-M6-F_UPLINK-label-inlay.stl` | Separate parts in assembled position (all closed, 0 open edges; inlay = D's) |
| `src/SG8-M6-F_build.py` | Build: `python src/SG8-M6-F_build.py <out_dir>`. Patches D's exact source (`outputs/TL-SG108E_M6_2026-10-28/previous_SG8-M6-D/SG8-M6-D.scad`), writes `src/SG8-M6-F.scad` (rails are module `cheek()` there) |
| `src/clash_check.py`, `src/pack_3mf.py` | Clash checks (`python src/clash_check.py . <post.stl> [post_z]`), 3MF packing |

## How it goes together

1. **Post rails** (one per side, behind each front post). Each takes **1 × M6 x 8** into the post's **middle front hole**, from behind (driver along the rack depth through the open pocket at the rail's rear). 2.5 mm under the head, ~5.5 mm into the post. The rail's pad sits flat on the back of the post face and its outer side rests against the post's thick side wall (0.22 gap). **Your middle holes have no insert yet: set an M6 insert in each first.**
2. **Tray** slides in from the front (faceplate off): runners on the rails' 45° ledges, hold-down lip above each runner, rear stop at each rail's end.
3. **Faceplate** on with its four rack screws, then **2 × M6 x 8 from behind** through the tray's two uprights into the M6 inserts in the plate's two bosses (the D hidden-screw joint).

To take the switch out: the 2 joint screws, the faceplate, then slide the tray forward.

## Geometry (frame: X centred, plate back Y = 0, Z = 0 slot bottom)

- **Tray** = SG8-M6-D tray: front trimmed to Y 0.3, strap slots removed (Brian), runners X ±100.5..107.5 (Y 0.3..80.3; 45° bearing face underneath, 45° top), right floor wing X 70.5..100.5, Z 0.5..6.5 under the keystone. Uprights 16 x 6 at Y 8.3..14.3 at **X −88 / +56**; sleeve lip notched 12.6 wide, Y 0..8.3 under each boss. Width 215 mm.
- **Faceplate** = D faceplate with its two bosses (Ø12, Ø7.6 insert bore 7 deep, centre Z 38.425) moved to **X −88 / +56**, off the sleeve walls, so they sit over the switch top (0.4 mm above it) instead of on a wall or the lip: the B–E boss/lip clash can't happen. Switch window bottom 0.3 lower (tolerance). Keystone +88, UPLINK inlay, corner slots unchanged.
- **Post rail**: wall X ±103..111, Y 6.2..85, Z 0.5..44.0 with the runner channel and rear stop; block behind the front flange to X ±125 (Y 6.2..38), and to X ±126.9 (Y 11.8..38) against the post's side wall. Ø9 x 10 relief behind the faceplate's two screw holes.
- **Clearances**: runner on the ledge 0.1 below nominal; 0.25 elsewhere in the channel; rail to post 0.2–0.3; boss to tray uprights 0.3.

**Posts (Brian's rack, corrected 2026-10-30):** the rack uses the creator's **4U posts**. At U8 (third U of the top 4U post) the side wall is solid, 14 mm thick (inner face X ±127.12), with **no holes**; side holes exist only near the post ends. Inner-corner fillet out to X 127.1 up to Y ~11.3. The first version of F was modelled on the 1U post (side holes, thinner wall) and was wrong for this rack. Middle front holes: Ø7.6 at X ±118.26, Z 22.225, no insert in Brian's rack yet (photo).

**Switch fit = SG8-M6-D (proven numbers kept):** device 158 x 100 x 25, offset X −15, sleeve side play 0.5, sleeve top 1.35, 1.3 mm set back, keyhole detents, rear stop, flush ports, keystone +88, UPLINK inlay, rounded tray corners.

## Checks (OpenSCAD intersections, digital only) — all clear

Tray × faceplate (incl. bosses), tray × each rail, faceplate × each rail, rail × its post, tray × posts, faceplate × posts, switch box (resting 0.1 low) × faceplate and rails, tray slid forward 5/15/30/45/60/75/90 mm × rails and posts. Post = creator's 4U post (object_190) placed `translate([s*126.12,17.5,0]) scale([-s,1,1])` (its third U in the slot); local only, not in the repo outputs or the artifact viewer. Keystone jack body and cables were not modelled.

## BOM

4 × M6 x 8 button head (1 per rail + 2 tray-to-plate) + the faceplate's usual 4 rack screws; **4 × M6 heat-set insert** (2 in the plate bosses, 2 in the posts' middle holes).

## Print notes

Tray and rails print as installed (flat bottom down); faceplate on its front face. Each tray upright overhangs ~6 mm past the lip toward the switch (as on D). Horizontal screw pockets print as bridges. Supports, bed fit, warping: UNKNOWN.

UNKNOWN: insert OD/length (boss wall 2.2 mm), rail stiffness on one screw, runner slide and seating, joint hole alignment between rail-located tray and rack-located plate (Ø6.6 clearance gives ±0.3), whether X ±103..127 beside the switch is free in the rack, physical fit.
