# RX4-B: MoCA receiver box, living-room shelf (2026-11-01), replaces RX4-A

Test-print ID **RX4-B**, engraved 0.6 mm on hidden faces: base and lid undersides, cradle underside, shelf top behind the switch, inside of the body's back wall. Washers are too small for text (ID in the name only). Source: `src/RX4-B.scad` (copy of `work/wall-box-wizard/receiver1/rx4.scad`, needs `concept15/body15.scad` for the golden keystone).

Holds a ScreenBeam ECB7250 (on an adjustable cradle) and a TP-Link TL-SG105 (on a shelf above it, ports out a front window). Outside 222 x 136 x 69.25 mm, plus 2.5 mm lid.

## Changes from RX4-A (never printed)
- Side vents: 14 vertical round-ended slots per end wall, 3 wide, Z 14.5-51.5, every 6 from Y 28 to 106.
- Switch window smoothed: R2.5 corners, 1.2 x 45-degree outer chamfer (lip unchanged).
- Switch front face measured (model only): 5 ports as one 76.5 group, 6.5 from the left, 6.55 up; power LED 7 from the right, 10 up (shows through the window). Port height ASSUMED 13.

## Print set: `RX4-B_moca_receiver_set.3mf` (9 objects, one per part, flat on the bed)
| Part | Orientation | Notes |
|---|---|---|
| body | upright, open bottom on the bed | open tube; 3 back keystones + 1 front keystone frames, switch window, 2 power holes, 45 deg shelf ledges, 2 shelf pins |
| base | plate down, lip up | 4 countersunk M3 into the post inserts; 4 cradle insert bosses |
| lid | top face down, lip and ribs up | 4 countersunk M3; 2 ribs clamp the switch |
| shelf | flat | 2 holes over the ledge pins; rails + back stop for the switch |
| cradle | plate down | foot pockets; 4 ears with slot + 2.4 deep track |
| washer x4 | flat | 10 x 2.4 slide washers, countersunk |

## Hardware
- M3 x 3 x 5 heat-set inserts (4.2 x 4 bores): 12 (4 lid posts top, 4 posts bottom, 4 base bosses).
- M3 countersunk screws: 4 lid, 4 base (about 6-8 long), 4 cradle (about 8-10 long, through washer + pad into the base inserts). Lengths UNVERIFIED.
- 4 keystone jacks (3 back: ETH1, ETH2, coax F; 1 front: Ethernet). Golden keystone fit (ks_tight 0.2).

## Measured vs assumed
- Measured by Brian (2026-11-01): ScreenBeam Coax In (22 from the box-back side, 15.25 up from the case bottom); switch power jack (12 from the left side seen from the front, 13 up) and plug (sticks out 26, 8.5 wide).
- ScreenBeam size, feet: Brian. Switch size 100 x 98 x 25: retailer listing.
- ASSUMED: ScreenBeam power and LAN jack positions (24 / 43 from the front side, mid-height).

## Checks
- All 9 objects closed (0 bad edges), all on Z = 0. 3MF: 12606 vertex / 25488 triangle tags, no ns0.

PROPOSED - UNVALIDATED: fit, insert pull-out, slide-washer grip, heat and strength UNKNOWN. Not printed yet.
