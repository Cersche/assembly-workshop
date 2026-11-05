# MRT-T3 jig and MRT-F channel covers (2026-11-04)

PROPOSED, UNPRINTED. Fit, retention and strength are UNKNOWN. Built from `src/MRT-F.scad`.

Load `MRT-T3_jig_and_covers.3mf` (four objects, 422 mm wide in a row, so split across plates as needed), or the STLs.

## MRT-T3 channel forming jig
MRT-T1 plus the ten cover pillars, about 94 cm3. Set the real gear on it, form the coax, cut and crimp the jumpers, then try the covers. If MRT-T1 is already printed, it still works for forming and cutting; only the covers need T3.

## Covers (print underside down, no supports)
| ID | Covers | Screws |
| --- | --- | --- |
| MRT-F-C1 | ScreenBeam-to-splitter jumper | 3 |
| MRT-F-C2 | Modem coax OUT | 3 |
| MRT-F-C3 | Coax IN and the power + LAN cords, one piece | 4 |

## Hardware
10 M3 countersunk screws and 10 M3 x 3 x 5 inserts (4.2 bore, 4 deep, in 9.5 pillars). Each pillar has a clearance hole 12 deeper, so a longer screw won't bottom out. Minimum screw length is about 6. Screw lengths on hand aren't known.

## Not tested by these
The M6 plate joint, the shoes and the rack fit. MRT-T2 (lip gaps) is unchanged, in `../Physical_Test_Coupons_2026-11-04_MRT-T1_T2/`.
