# TP-Link ER605 one-piece bracket — test-print ID ER6-C (2026-11-04)

**ER6-D lowers this pocket to 26.0 at Brian's direction. ER6-C is the 0.5-taller fallback.**

PROPOSED — UNPRINTED. Current design. [ER6-B](../ER605_Bracket_ER6-B_2026-11-04/README.md) with the pocket raised for the measured case. Detents, wedges, vents and faceplate standard as ER6-B; see its README for those. Remix of Mixmeister's ER605 mount (MakerWorld, BY-NC-SA). Router fit, detent click, rack fit and strength are UNKNOWN.

## Print

`ER6-C_ER605_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, no supports. 252 x 44.4 x 106.7 mm, 96.9 cm3 solid volume.

## Install

No stick-on feet (Brian). Slide the router in from the front, ports forward, until the bumps click into the keyholes. To remove: press both arms down from under the sleeve and slide it out.

## What changed from ER6-B

| Value | ER6-B | ER6-C | Why |
|---|---|---|---|
| Pocket height | 25.7 | 26.5 | Case measured 26 (Brian), so 25.7 would not go in. 0.5 total is the up-and-down gap CM1P-K fits with |
| Sleeve outside height | 33.7 | 34.5 | Walls stay 4 |
| Root chamfer | 5 | 4.5 | Stops 0.45 inside the plate edge, so the 44.4 plate outline is untouched |

Pocket width 158.7 and stop at 101.7 stay. Bump stays 2 tall; the 4 mm of room above the keyhole (Brian) clears it.

## Router (Brian, 2026-11-04, calipers)

158 wide, 101 deep, 26 tall without feet. Room above the keyhole 4. Keyholes as in ER6-B's README.

## Checks (digital only)

`python src/pack_check.py . <SG8-M6-F_faceplate.stl> <source.stl>`: closed mesh; 158 x 101 x 26 box with Ø8 holes seated: clear; path from the front: clear apart from the bumps it rides over; faces past 45°: none that print; plate matches SG8-M6-F within 0.12 mm; 3MF plain tags 2102 vertex / 4296 triangle.

## UNKNOWN

Whether the two screw heads on the ports-end bar stand proud of the case bottom (they pass over the bottom wall's front band going in). Detent arm durability and click force, printed vertically. Right keyhole assumed symmetric. Strength.
