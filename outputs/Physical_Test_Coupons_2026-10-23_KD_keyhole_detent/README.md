# KD keyhole-detent coupons — TL-SG108E front retention (2026-10-23)

PROPOSED — UNVALIDATED. Picks the bump height for the TL-SG108E tray detents
(`outputs/STL_Deliveries/2026-10-23_TL-SG108E_flush`, Brian: keyholes very shallow).

| ID | Bump above floor | File |
| --- | --- | --- |
| KD-A | 0.6 mm (current tray) | `KD-A_keyhole-detent_bump-0.6mm.stl` |
| KD-B | 0.8 mm | `KD-B_keyhole-detent_bump-0.8mm.stl` |
| KD-C | 1.0 mm | `KD-C_keyhole-detent_bump-1.0mm.stl` |
| KD-D | 3.0 mm (Brian: keyholes deeper than thought; everything else as KD-A) | `KD-D_keyhole-detent_bump-3.0mm.stl` |
| KD-E | 3.0 mm, **6.5 mm floor**, arm 1.2 mm below the floor top over a 3.5 mm pocket | `KD-E_keyhole-detent_bump-3.0mm_floor-6.5mm.stl` |

All three in one file: `KD-A-E_keyhole-detent_coupons.3mf` (separate objects). ID engraved by the front edge,
bump height engraved by the wall. Same arm as the tray: 8 × 26 mm, 1.8 mm thick, 1.2 mm slot; 5 × 4 mm bump,
45° ramp toward the front, 60° face toward the wall. Rear stop face 51.5 mm behind the bump centre, as on the tray.

**Test:** lay the coupon flat, set the switch on it ports away from the wall, with
one keyhole over the bump line, and slide it back until it touches the wall. Note: does it ride over the bump easily,
does the bump drop into the keyhole when it touches the wall, how hard is it to pull forward, does the switch rock?
Specimen-specific; fit, retention and strength stay UNKNOWN elsewhere. Source: `KD_coupon.scad`.

KD-D note: the arm can only bend 1.2 mm down inside the 3 mm floor (less on a table: it rests on the arm's
support), so a 3 mm bump will mostly have to lift the switch. With 0.8 mm top play in the sleeve that may block it; the
coupon (no sleeve) shows the catch. Built with `-D id="KD-D" -D bump_up=3`.

**Result 2026-10-23 (Brian):** KD-D (3 mm) locks very nicely, but the tab sticks out of the bottom when bent.
KD-E fixes that: bent the full 3 mm, the arm stays 0.5 mm above the floor bottom. Built with
`-D id="KD-E" -D bump_up=3 -D tray_t=6.5`. KD-E is unprinted.
