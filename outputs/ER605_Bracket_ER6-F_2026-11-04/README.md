# TP-Link ER605 one-piece bracket — test-print ID ER6-F (2026-11-04)

PROPOSED — UNPRINTED. Current design. [ER6-E](../ER605_Bracket_ER6-E_2026-11-04/README.md) with the router face flush with the plate front (Brian). Everything else, including install and UNKNOWNs, as ER6-E. Router fit, flushness, detent click, rack fit and strength are UNKNOWN.

`ER6-F_ER605_bracket.3mf`, also in `outputs/Final_3MF/`: one object, front face on the bed, no supports. 252 x 44.4 x 106 mm.

## What changed from ER6-E

| Value | ER6-E | ER6-F |
|---|---|---|
| Rear stop start, from plate front | 101.7 | 101.0 (the measured case depth) |
| Router face to plate front | 0.7 behind | 0 |
| Detent bump centre Y | 47.7 | 47.0 (moved with the router, still 50 from its rear edge) |
| Part height in print | 106.7 | 106.0 |

Flushness depends on the 101 measurement and on the case's rear corners meeting the wedge start. Rounded corners run a little into the wedges and leave the face slightly behind flush. To shift it after a print, change `pk_end`; the detents follow.

## Checks (digital only)

`python src/pack_check.py . <SG8-M6-F_faceplate.stl> <source.stl>`: closed mesh; case box 25.98 tall with Ø8 holes, front at the plate front: clear; path from the front: clear apart from the bumps; faces past 45°: none that print; plate matches SG8-M6-F within 0.12 mm. Tag counts printed by the script.
