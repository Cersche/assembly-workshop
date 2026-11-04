# TP-Link ER605 one-piece bracket — test-print ID ER6-D (2026-11-04)

PROPOSED — UNPRINTED. Current design. [ER6-C](../ER605_Bracket_ER6-C_2026-11-04/README.md) with the pocket 0.5 lower at Brian's direction: 26.0 instead of 26.5, sleeve outside 34.0. Everything else as ER6-C and [ER6-B](../ER605_Bracket_ER6-B_2026-11-04/README.md). Remix of Mixmeister's ER605 mount (MakerWorld, BY-NC-SA). Router fit, detent click, rack fit and strength are UNKNOWN.

`ER6-D_ER605_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, no supports. 252 x 44.4 x 106.7 mm.

**Fit note:** the case measured 26 tall (Brian), so this pocket has no designed gap top to bottom. ER6-C's 0.5 was the gap CM1P-K fits with. Taken as the pocket height Brian meant; he did not name which height. If it is tight, ER6-C is the same part 0.5 taller.

## Checks (digital only)

`python src/pack_check.py . <SG8-M6-F_faceplate.stl> <source.stl>`: closed mesh; case box 25.98 tall (26 touches by design) with Ø8 holes seated: clear; path from the front: clear apart from the bumps; faces past 45°: none that print; plate matches SG8-M6-F within 0.12 mm. Tag counts printed by the script.

## UNKNOWN

Same as ER6-C: ports-end screw heads, arm durability and click force, right keyhole assumed symmetric, strength.
