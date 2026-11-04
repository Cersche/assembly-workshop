# TP-Link ER605 one-piece bracket — test-print ID ER6-B (2026-11-04)

**Superseded by [ER6-C](../ER605_Bracket_ER6-C_2026-11-04/README.md): the case measured 26 tall, so this 25.7 pocket is too short. Don't print.**

PROPOSED — UNPRINTED. [ER6-A](../ER605_Bracket_ER6-A_2026-11-04/README.md) plus two click-in detents in the router's keyholes, so it can't walk forward when cables are unplugged. Everything else, including the faceplate standard, is unchanged from ER6-A. Remix of Mixmeister's ER605 mount (MakerWorld, BY-NC-SA). Router fit, detent click, rack fit and strength are UNKNOWN.

## Print

`ER6-B_ER605_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, no supports. 252 x 44.4 x 106.7 mm, 97.7 cm3 solid volume. Each detent arm stands free about 30 mm during the print, so watch it on the first run.

## Install

Leave the stick-on feet off (assumed; Brian to confirm). Slide the router in from the front, ports forward, until the bumps click into the keyholes. To remove: press both arms down from under the sleeve and slide it out.

## Router (Brian, 2026-11-04, calipers)

158 wide, 101 deep. Keyhole round part Ø8, centre 17.25 from the side, 50 from the rear edge. Upward slot 4 wide, 8.5 long from centre; sideways slot 8.5 long. Stepped bar is on the ports edge, so the rear corners are plain.

Not measured: case height (J), room above the keyhole (L), feet staying off (M). Right keyhole taken as symmetric, so centre spacing 123.5 (K); photo scale gave about 123.

## Detents

| Value | ER6-B | KD-E on SG8-M6-F (printed, clicks) |
|---|---|---|
| Arm section | 8 wide x 1.8 thick | same |
| Bump width, height | 5, 2 | same |
| Faces | 45° ramp to the front, 60° to the rear | same |
| Flat top | 2 | 4, shortened so the whole 5.15 base fits this Ø8 hole (6.24 chord at 5 wide) |
| Free arm length | about 30 to 36 | 26 |
| Print direction | Arm stands vertical, layers cross it | Flat |

Centres X ±61.75, Y 47.7. Arm lies in the bottom wall's plane, top flush with the pocket floor, from the front band to Y 51.7, and bends down into the free space under the sleeve (arm underside Z 7.6, slot bottom Z 0). The bump needs the router's rear corners against the wedges to line up: seated position is Y -3.3..97.7, so the case sits 0.7 behind the plate front.

The vertical print is the main risk: layer lines run across the bending arm, unlike the flat-printed KD-E. Estimated bending strain at 2 mm travel is about 0.6% (beam estimate), not tested.

## Checks (digital only)

`python src/pack_check.py . <SG8-M6-F_faceplate.stl> <source.stl>`: closed mesh; router box with Ø8 holes seated: clear of the bracket; router path from the front: clear apart from the bumps it is meant to ride over; faces past 45°: none that print (same 0.01 steps as ER6-A); plate matches SG8-M6-F within 0.12 mm; 3MF plain tags 2116 vertex / 4324 triangle.

## UNKNOWN

Case height against the 25.7 pocket. Room above the keyholes (bump needs 2). Arm durability, click force, whether the bump lifts the router rear. Strength.
