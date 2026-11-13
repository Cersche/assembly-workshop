# RX5-C: MoCA receiver base with the cradle bosses 9 mm left (2026-11-09), replaces the RX5-B base only

Brian, 2026-11-09 (marked slicer picture): move the four ScreenBeam cradle bosses on the base 9 mm to the left; change nothing else on any part.

- **Only the base changed.** Its four insert bosses (10 OD, 4.2 x 4 insert bores) moved -9 in X (seen from the front; also left in the slicer, the base prints as modelled): X 46.5 / 188.5 -> 37.5 / 179.5, Y unchanged. Plate, lip, notches and the 4 corner screw holes are unchanged.
- Engraved ID on the underside is now **RX5-C**. Body, lid, shelf, cradle and washers stay RX5-B: reuse the RX5-B files (`../MoCA_Receiver_RX5-B_2026-11-03/`).
- Source: `src/RX5-C.scad` (copy of `work/wall-box-wizard/receiver1/rx5.scad`; `base_dx=-9` applies to the base only). Rendered with OpenSCAD 2021.01 like RX5-B. Needs `concept15/body15.scad`.

## Files
- `RX5-C_base.3mf` (1 object, 2136 vertex / 4284 triangle tags, no ns0), also `outputs/Final_3MF/RX5-C_moca_receiver_base.3mf`.
- `RX5-C_base.stl`: closed (0 bad edges), 222 x 142 x 6.5, on Z = 0.

## Effect on the rest (arithmetic, not a modelled cord check)
The cradle and ScreenBeam now sit 9 mm further left. The left plug bay shrinks from 55 to 46 mm: the 35 mm power plug ends about 11 mm from the left inner wall (was 20), the LAN plug about 18. The right side gains 9 mm for the coax right-angle. The power cord's route up the bay was not re-checked; cords stay ASSUMED.

PROPOSED - UNVALIDATED: fit, insert pull-out and strength UNKNOWN. Not printed.
