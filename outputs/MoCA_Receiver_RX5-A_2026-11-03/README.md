# RX5-A: MoCA receiver box with all ports at the rear (2026-11-03), replaces RX4-C

Test-print ID **RX5-A**, engraved 0.6 mm on hidden faces: base and lid undersides, cradle underside, shelf top in front of the switch, inside of the body's back wall. Washers are too small for text (ID in the name only). Source: `src/RX5-A.scad` (copy of `work/wall-box-wizard/receiver1/rx5.scad`, needs `concept15/body15.scad` for the golden keystone).

For an entertainment stand: every port faces a grommet in the stand's back, plain front wall. Holds a ScreenBeam ECB7250 (adjustable cradle) and a TP-Link TL-SG105 (on a shelf above it). Outside 222 x 142 x 69.25 mm, plus 2.5 mm lid.

## Changes from RX4-C
- Switch turned 180 and centred in the box, ports out a smoothed window in the back wall; the front wall is plain.
- Depth 136 -> 142 for the switch power cord's U-turn (assumed 10 bend radius, 4 dia cord; about 1 mm spare).
- Back wall symmetric about the centre: 11 mm power holes either side of the window (Z 55.25), keystones below them (X 34.5 and 187.5, Z 25.75).
- Removed: front keystone, ETH2 keystone and the inside patch. Google Wifi LAN plugs straight into a switch port.
- New: a zip-tie fin beside each power hole, inside the back wall (slot 4.5 x 2.5).
- Lid lip notch, ribs and side tabs follow the switch; shelf rails, front stop and pins moved to match.
- ScreenBeam jack order corrected (Brian): LAN 24, power 43 from the front side. Cable routing only.

## Print set: `RX5-A_moca_receiver_set.3mf` (9 objects, one per part, flat on the bed)
| Part | Orientation | Notes |
|---|---|---|
| body | upright, open bottom on the bed | open tube; 2 back keystone frames, switch window, 2 power holes, 2 tie fins, 45 deg shelf ledges, 2 shelf pins |
| base | plate down, lip up | 4 countersunk M3 into the post inserts; 4 cradle insert bosses |
| lid | top face down, lip, ribs and tabs up | 4 countersunk M3; 2 ribs clamp the switch; 2 side tabs |
| shelf | flat | 2 holes over the ledge pins; rails + front stop for the switch |
| cradle | plate down | foot pockets; 4 ears with slot + 2.4 deep track |
| washer x4 | flat | 10 x 2.4 slide washers, countersunk |

`RX5-A_devices.stl` and `RX5-A_cords.stl` are context only, never printed.

## Hardware
- M3 x 3 x 5 heat-set inserts (4.2 x 4 bores): 12 (4 lid posts top, 4 posts bottom, 4 base bosses).
- M3 countersunk screws: 4 lid, 4 base (about 6-8 long), 4 cradle (about 8-10 long, through washer + pad into the base inserts). Lengths UNVERIFIED.
- 2 keystone jacks (ETH1, coax F). Golden keystone fit (ks_tight 0.2).
- 2 small zip ties, up to about 4 wide.

## Measured vs assumed
- Measured by Brian: ScreenBeam Coax In (22 from the box-back side, 15.25 up from the case bottom); switch power jack (12 from the left side seen from the ports, 13 up) and plug (sticks out 26, 8.5 wide).
- ScreenBeam LAN and power jacks: Brian says close enough with the order swapped (2026-11-02).
- Switch size 100 x 98 x 25: retailer listing.
- ASSUMED: cord diameter and bend radius. Rear cable room in the stand not checked.

## Checks
- All 9 objects closed (0 bad edges), all on Z = 0. 3MF: 12050 vertex / 24376 triangle tags, no ns0.
- Modelled clash checks: cords and ETH1 patch clear of body, shelf, lid, cradle and each other where checked. Models only.

PROPOSED - UNVALIDATED: fit, cord bend, zip-tie grip, insert pull-out, slide-washer grip, heat and strength UNKNOWN. Not printed yet.
