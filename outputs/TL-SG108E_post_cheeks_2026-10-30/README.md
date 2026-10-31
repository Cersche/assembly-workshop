# SG8-M6-F — TP-Link TL-SG108E 1U tray on post cheeks (2026-10-30)

Test-print ID **SG8-M6-F** is engraved on each part: plate back above the window, outside of the tray's left sleeve wall, inner face of each cheek. **Not printed. Fit and strength UNKNOWN.**

Concept A, Brian's pick: the **rack posts carry the tray, not the faceplate**. Two cheeks bolt to the front posts; the tray slides in from the front on two runners that sit on the cheeks' ledges; the faceplate is only a cover. No plate bosses, no tray uprights, so the faceplate/tray clash from B–E cannot happen.

| File | What |
|---|---|
| `SG8-M6-F_TL-SG108E_post-cheeks_set.3mf` | Tray, left cheek, right cheek, faceplate + UPLINK label (one object, two parts). Plain vertex/triangle tags |
| `SG8-M6-F_tray.stl`, `SG8-M6-F_cheek_left.stl`, `SG8-M6-F_cheek_right.stl`, `SG8-M6-F_faceplate.stl`, `SG8-M6-F_UPLINK-label-inlay.stl` | Separate parts in assembled position (all closed, 0 open edges; inlay = D's, unchanged) |
| `src/SG8-M6-F_build.py` | Build: `python src/SG8-M6-F_build.py <out_dir>`. Patches D's exact source (`../TL-SG108E_M6_2026-10-28/previous_SG8-M6-D/SG8-M6-D.scad`) and writes `src/SG8-M6-F.scad` |
| `src/clash_check.py`, `src/pack_3mf.py` | Clash checks (`python src/clash_check.py . <post1u.stl>`), 3MF packing |

## How it goes together

1. **Cheeks** (one per side, in the rack slot behind each front post). Each takes **3 × M6 x 8 button head**:
   - the front flange's **middle hole**, from behind (driver along the rack depth, through the open pocket at the cheek's rear);
   - both **side-flange holes** (Y 22.5, Z 10.0 and 34.5), from inside the rack (pockets open to the cheek's inner face).
   Every screw has 2.5 mm of plastic under the head and reaches ~5.5 mm into the post.
   Fit the cheeks with the tray out: put each cheek into the slot from the middle of the rack, slide it outward, then forward into the post corner.
2. **Tray** slides in from the front (faceplate off). Its runners sit on the cheeks' 45° ledges; a hold-down lip above each runner stops it lifting; the cheeks' rear stops stop it at the back.
3. **Faceplate** goes on last with its usual four corner screws. It stops the tray sliding forward (tray front 0.3 mm behind the plate). It carries no weight.

No screws hold the tray itself, and none show at the front. To take the switch out: faceplate off, slide the tray forward.

## Geometry (frame: X centred, plate back Y = 0, Z = 0 slot bottom)

- **Tray** = SG8-M6-D tray minus its two uprights, front trimmed to Y 0.3, plus two runners (X ±100.5..107.5, Y 0.3..80.3; 45° bearing face underneath, 45° top) and, on the right, a floor wing X 70.5..100.5, Z 0.5..6.5 that passes under the keystone (keystone block bottom Z 7.2). Width now 215 mm (was 174).
- **Cheek**: wall X ±103..111, Y 6.2..85, Z 0.5..44.0 with the runner channel and rear stop; block behind the front flange to X ±125 (Y 6.2..38) and out to X ±133.9 against the side flange (Y 11.8..38).
- **No strap slots** (Brian, 2026-10-30): the wall notches and floor slots at quarter depth are gone; this switch never used them.
- **Faceplate** = D faceplate without bosses; the switch window bottom is 0.3 mm lower (tolerance for the tray resting on the ledges). Keystone +88, UPLINK inlay and four corner slots unchanged.
- **Clearances**: runner on the ledge 0.1 below nominal (tray rests 0.1 low; window has 0.3); 0.25 elsewhere in the channel (normal); cheek to post 0.2–0.3.

**Post shape found during the checks** (from the 1U post mesh slices; corrects the brief): the side flange is X 134.12..141.12 (7 mm thick); there is an inner-corner fillet out to X 127.1 up to Y ~11.3, and a **rib on the side flange's inner face at X 127.12..134.12, Z 20.0..24.45, full depth**. The cheek has a slot for that rib and stays at X ≤ 125 ahead of Y 11.8. Side holes confirmed Ø7.6 at Y 22.5, Z 10.0 / 34.5; middle front hole confirmed Ø7.6 at X ±118.26, Z 22.225. The cheek also has Ø9 x 10 relief pockets behind the faceplate's two screw holes (screw tips/insert ends).

**Switch fit = SG8-M6-D (proven numbers kept):** device 158 x 100 x 25, offset X −15, sleeve side play 0.5, sleeve top 1.35, switch 1.3 mm set back, keyhole detents, rear stop, flush ports, keystone +88, UPLINK inlay, rounded tray corners (R5 front / R20 rear on the sleeve footprint, R4 on the runner/wing corners).

## Checks (OpenSCAD intersections, digital only) — all clear

Tray × faceplate, tray × each cheek, faceplate × each cheek, cheek × its post, tray × posts, faceplate × posts, switch box (resting 0.1 low) × faceplate and cheeks, and the tray slid forward 5/15/30/45/60/75/90 mm × cheeks and posts (slide-in path). Right cheek moved back 3/10/20/35 mm × its post: clear (it slides forward into place over the post rib). Post = creator's 1U post mesh placed `translate([s*126.12,17.5,22.225]) scale([-s,1,1])` (local only, not in the repo outputs or viewer). Keystone jack body and cables behind the plate were not modelled (they sit over the right wing, above Z 7.2).

## BOM

6 × M6 x 8 button head (3 per cheek) + the faceplate's usual 4 rack screws. **Needs M6 inserts in each front post's middle hole and both side-flange holes** (UNKNOWN whether yours have them). Nothing else.

## Print notes

Tray and cheeks print as installed (flat bottom down); faceplate on its front face. Horizontal screw pockets (Ø11.5) print as bridges. The tray is 215 x 104 mm. Supports, bed fit and warping: UNKNOWN.

UNKNOWN: inserts in the middle/side holes, cheek stiffness and screw hold, runner slide and seating, whether the side area X ±103..134 next to the switch is free in Brian's rack (side panels, cable guides), physical fit of everything.
