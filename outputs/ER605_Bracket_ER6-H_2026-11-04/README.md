# TP-Link ER605 one-piece bracket — test-print ID ER6-H (2026-11-04)

PROPOSED — UNPRINTED. Current design. [ER6-G](../ER605_Bracket_ER6-G_2026-11-04/README.md) with 3 long floor slots instead of the hexes (Brian). Everything else, including keystones, flush router and detents, as ER6-G. Router fit, flushness, detent click, rack fit and strength are UNKNOWN.

`ER6-H_ER605_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, no supports. 252 x 44.4 x 106.08 mm, 96.1 cm3 solid volume (ER6-G 101.7). Not sliced: print time unknown.

## Floor slots

Three slots, 28 wide with 6 mm ribs, centres X 0, ±34. Each runs Y 18 to an apex at Y 90, 45° point at the rear, 3 mm chamfered front corners. The field ends X ±48, leaving 8.55 to each detent slot. Each layer crosses 3 openings, plus the 2 detent slots up to about Y 57. Router's underside has no vents (Brian's photo), so these only save plastic.

## Checks (digital only)

`python src/pack_check.py . <SG8-M6-F_faceplate.stl> <source.stl>`: closed mesh; case box 25.98 tall with Ø8 holes, front at the plate front: clear; path from the front: clear apart from the bumps; plate and keystones match SG8-M6-F as on ER6-G; 3MF plain tags 2228 vertex / 4500 triangle. Faces past 45° away from the keystones and ID: none that print. (The script's overhang total counts the plate front, 0.08 off the bed; ignore it.)
