# SCR5-H7: screen + Pi 4 + Hue, rev 7 (2026-10-31)

New revision folder. Rev 6 (`outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/`) stays immutable. Test-print ID **SCR5-H7** is embossed on the plate, frame, floor and deck.

## Changes from rev 6 (Brian's fastener standard, 2026-10-31)
- **Plate:** the 4 frame bosses are now 9 mm OD with M3x3x5 heat-set insert bores (4.2 mm x 5 deep). They replace the 2.1 mm self-tap pilots.
- **Frame:** the 4 corner holes are now 3.4 mm, with M3 countersinks in the rear face. The screen-standoff holes stay 2.8 mm (M2.5, forced by the screen).
- **Floor:** the 5 deck bosses are now 9 mm OD with M3x3x5 insert bores (4.2 x 5). The Pi standoffs keep 3.2 mm bores for M2.5x4x3.5 inserts.
- **Deck:** all 5 holes are 3.4 mm with M3 countersinks (6.4 mm at the top, 1.5 deep), so the heads sit flush under the Hue.
- **Pins:** unchanged (DROP 0.45).

## BOM
| Joint | Screw | Insert | Qty |
|---|---|---|---|
| Frame to plate | M3 x 8 countersunk | 4 x M3x3x5 | 4 |
| Deck to floor | M3 x 8 countersunk | 5 x M3x3x5 | 5 |
| Frame to screen standoffs | M2.5 socket head | (screen's own standoffs) | 4 |
| Pi to floor | M2.5 socket head | 4 x M2.5x4x3.5 | 4 |
| Plate to tray | M6 x 8 button head | M6x5x8 (as rev 6) | as rev 6 |
| Fan 40x10, 12 V external | fan screws | - | 4 |

## Checks
- All 7 STLs are one closed shell each, with 0 degenerate faces and 0 bad edges.
- Clash checks: frame with floor and deck, plate with floor, deck and Pi, floor with fan and Hue, deck with Pi: all empty. Deck with fan: 0 (touching only). Plate with frame: 0 (touching only).
- Same overlaps as rev 6, unchanged: deck with Hue box 5096 mm3 (5170 in rev 6, slightly less because of the countersinks); plate with screen dummy 1539 mm3 and frame with screen dummy 13.7 mm3, identical to rev 6.
- 3MF has 15983 vertex and 32162 triangle tags, no ns0.

UNKNOWN: insert fit and pull-out, screw lengths (M3 x 8 assumed), print fit, strength and airflow. Not printed.
