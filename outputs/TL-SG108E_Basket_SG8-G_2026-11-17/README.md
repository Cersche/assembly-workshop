# TL-SG108E one-piece basket: test-print ID SG8-G (2026-11-17)

RELEASED FOR PRINTING, UNPRINTED. Replaces [SG8-M6-F](../Chunky_Revisions/TL-SG108E_post_rails_2026-10-30/README.md) (tray + 2 post rails + faceplate + 2 hidden M6 screws) with one part in the ER605 [ER6-H](../ER605_Bracket_ER6-H_2026-11-04/README.md) basket style, and adds a second keystone on the right (Brian). Fit, detent click, flushness, strength and the basket system itself are UNKNOWN: ER6-H is unprinted too.

| File | What |
|---|---|
| `SG8-G_2-parts-print-layout.3mf` | Bracket + label inlay, both turned front face down on the bed. Also in `outputs/Final_3MF/` |
| `SG8-G_bracket.stl`, `SG8-G_inlay.stl` | In rack position (X centred, plate back Y 0, Z 0 slot bottom) |
| `release_report.md` | `tools/release_part.py` report: 0 fails, 0 warnings |
| `src/` | `sg108e_basket.scad` + frozen `lib/workshop.scad`; re-render with OPENSCADPATH=src/lib, `part="bracket"`/`"inlay"` |

## How it goes in
The bracket hangs on the faceplate's 4 rack screws only, like ER6-H. Slide the switch in from the front through the window until the keyhole bumps click. To remove: lift the front edge slightly over the bumps and pull. No inserts, no other screws.

## What was kept (SG8-M6-D/F pocket, printed and fits well)
Switch 158 x 100 x 25; side play 0.5; room above 1.35 (not the 0.8 library default); rear stop at 97.3 (the printed position that left the ports flush); keyholes ±55 from the switch centre, 48.5 back from its front; KD-E bump: 5 wide, 2 high, 4 flat, 45° ramp in front, 60° face behind; arm 8 x 1.8 x 26 with a 1.2 slot. Golden keystone (ks_tight 0.2) from `lib/workshop.scad`.

## What changed
- One piece, ER6-H body: 4 walls, 12 mm top collar, open top behind it, side walls sloping to 10 at the rear, 45° rear stop ears, 4.5 root chamfer. 100.5 cm3 (SG8-M6-F set about 270).
- Switch centre X −15 → **−21.5**, so two keystones fit on the right at **X +78 and +99**. Margins: sleeve chamfer 1.0 from the inner keystone block; left chamfer 1.6 from the post flange; outer keystone block 1.6 from the post flange.
- Labels **UPLINK** (X +78) and **WLAN** (X +99, upstairs WLAN), text 3.5 (was 4.5), 4.7 apart; engraved 0.6, optional inlay in a second colour.
- Floor: 3 long slots like ER6-H but 23 wide (ER6-H 28), centres X −50.5 / −21.5 / +7.5, to stay 9.3 from the detent slots. Detent arms hang in through-floor slots (ER6-H style) instead of SG8-M6-F's pocket.
- Hidden M6 joint, plate bosses, post rails and rail inserts all gone.
- ID SG8-G engraved on the collar top.

## Checks (digital only)
Release script: closed single body, ID on the mesh, 5 separate floor openings, no overlap with the real U7 posts both sides (plate back touches the post flange as intended). Own OpenSCAD intersections: switch seated (face flush) clear except the bump zones, switch path above the bumps clear, keystone room behind the plate clear. Keystone jack bodies and cables not modelled. Not sliced: print time UNKNOWN.

## Print notes
Front face on the bed, no supports (as ER6-H). Bed fit 252 wide: same width as every faceplate. Warping, bridges over the floor slots and the collar: UNKNOWN.

## Fit report to send back
ID on the part (SG8-G); switch slides in and clicks, or where it binds and by how much; ports flush, proud or sunk (mm); keystones snap in; plate fits the rack; any sag under the switch; walls and infill used.
