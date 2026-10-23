# KD keyhole-detent coupons — TL-SG108E front retention (2026-10-23)

PROPOSED — UNVALIDATED. Picks the bump height for the TL-SG108E tray detents
(`outputs/STL_Deliveries/2026-10-23_TL-SG108E_flush`, Brian: keyholes very shallow).

| ID | Bump above floor | File |
| --- | --- | --- |
| KD-A | 0.6 mm (current tray) | `KD-A_keyhole-detent_bump-0.6mm.stl` |
| KD-B | 0.8 mm | `KD-B_keyhole-detent_bump-0.8mm.stl` |
| KD-C | 1.0 mm | `KD-C_keyhole-detent_bump-1.0mm.stl` |
| KD-D | 3.0 mm, **6 mm floor, 35 mm arm** (Brian: keyholes deeper than thought) | `KD-D_keyhole-detent_bump-3.0mm_floor-6mm.stl` |

All three in one file: `KD-A-D_keyhole-detent_coupons.3mf` (separate objects). ID engraved by the front edge,
bump height engraved by the wall. Same arm as the tray: 8 × 26 mm, 1.8 mm thick, 1.2 mm slot; 5 × 4 mm bump,
45° ramp toward the front, 60° face toward the wall. Rear stop face 51.5 mm behind the bump centre, as on the tray.

**Test:** lay the coupon flat, set the switch on it ports away from the wall, with
one keyhole over the bump line, and slide it back until it touches the wall. Note: does it ride over the bump easily,
does the bump drop into the keyhole when it touches the wall, how hard is it to pull forward, does the switch rock?
Specimen-specific; fit, retention and strength stay UNKNOWN elsewhere. Source: `KD_coupon.scad`.

KD-D: the arm must bend 3 mm down to let the switch pass (it cannot lift: 0.8 mm top play), so its floor is 6 mm with the
arm at the bottom (4.2 mm bend room) and 35 mm long. Using it on the tray means a 6 mm tray floor: switch and window
3 mm higher (still 1U), ports still flush. Built with `-D id="KD-D" -D bump_up=3 -D tray_t=6 -D arm_l=35`.
