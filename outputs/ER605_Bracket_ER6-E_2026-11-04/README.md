# TP-Link ER605 one-piece bracket — test-print ID ER6-E (2026-11-04)

PROPOSED — UNPRINTED. Current design. Simplified from [ER6-D](../ER605_Bracket_ER6-D_2026-11-04/README.md) after Brian's cue picture: honeycomb on the floor, open top, plain sloped side walls. Remix of Mixmeister's ER605 mount (MakerWorld, BY-NC-SA). Router fit, detent click, rack fit and strength are UNKNOWN.

`ER6-E_ER605_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, no supports. 252 x 44.4 x 106.7 mm, 102.0 cm3 solid volume.

## Install

No stick-on feet. Slide the router in from the front, ports forward, under the collar, until the bumps click into the keyholes. To remove: press both arms down through the floor slots and slide it out.

## What changed from ER6-D

| Feature | ER6-D | ER6-E |
|---|---|---|
| Top | Full wall with 17 hexes | Open behind a 12 deep collar at the plate |
| Floor | Open to the rear, 10 wide ledges each side | Full floor, 18 whole hexes (16 wide, 4 struts, 45° roofs) |
| Side walls | Full height, pointed windows | Solid, slope from the collar down to 10 above the floor at the rear |
| Detent arms | Stand in the bottom opening | Stand in their own pointed slots through the floor, free about 38 long |

Kept: faceplate standard, pocket 158.7 wide, 26.0 at the collar, stop at 101.7 from the plate front, 45° wedges (now 10 tall), 4.5 root chamfer, bump size and position, ID on the plate back.

Nothing holds the router down behind the collar except its weight and the detents; the top is open.

## Checks (digital only)

`python src/pack_check.py . <SG8-M6-F_faceplate.stl> <source.stl>`: closed mesh; case box 25.98 tall with Ø8 holes seated: clear; path from the front: clear apart from the bumps; faces past 45°: none that print; plate matches SG8-M6-F within 0.12 mm; 3MF plain tags 1790 vertex / 3676 triangle.

## UNKNOWN

Height fit at the collar (no designed gap on the 26 case). Arm durability and click force; arms print vertically and stand free about 38. Whether the router rocks in the open top. Right keyhole assumed symmetric. Strength.
