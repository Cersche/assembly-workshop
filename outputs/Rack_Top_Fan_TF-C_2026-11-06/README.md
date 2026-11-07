# TF-C: rack top for the 200 mm-class CT200 fan, complete set (2026-11-06)

**Print this set. It replaces TF-A and TF-B, which were never printed.** Design story, hardware and fit report: see `../Rack_Top_Fan_TF-A_2026-11-06/README.md` (TF-A) and `../Rack_Top_Fan_TF-B_2026-11-06/README.md` (TF-B: the CT200 frame is 195, so the cavity is 196).

## What changed in TF-C (Brian: "we're using buttonhead M6x8 screws, just like the original geometry of the rack")
- The cross joints now match the stock rack. An M6 x 8 button head goes in from inside the rack, through a Ø6.4 hole in the edge plug or tongue, and into an M6 heat-set insert in the post (stock post, plug joint) or in our rail (tongue joint).
- Edges: Ø10.8 x 2 head recess on the inner face of each plug and tongue (stock value). Holes moved to the stock centres, Z 390.05 (plug) and **Z 412.55 (tongue; TF-A/B had 416, which was wrong)**.
- Rails: M6 insert bore Ø7.6, blind, from the pocket face out to X 139.48, leaving 1.5 mm of skin outside as on the stock rail. The old Ø6.4 through-hole is gone. The inside of each tongue pocket is open to the rack, like the stock rail, so the screw and a 4 mm hex key can reach it.
- Head keep-outs (Ø12.5 x 6 inward) added for all 8 cross screws.

## Parts (`TF-C_6-parts-print-layout.3mf`, turned for printing)
edge_front **TFE-C**, edge_rear **TRE-C** (each rotated 45 deg on the 256 bed, small support under the 2 plugs), rail **TSR-B** (print 2), grille **TFG-A** (unchanged), coupons **TFE-T2** and **TSR-T2**.

## Hardware
- 8 x M6 x 8 button head for the cross joints, 4 x M6 x 5 x 8 inserts in the two rails (the post inserts are the stock ones).
- 4 x M3 countersunk + 4 x M3 x 3 x 5 inserts for the grille.
- Handles: stock screws into 4 x M6 x 5 x 8 inserts in the rail tops.

## Checks
0 failed, 3 warnings, all kept:
- grille: dia 4.23 near 4.2. This is a slice of the countersink cone, not a bore.
- rail and rail_coupon: M6 insert bores about 5.25 deep, under the 6 mm guidance. This is the stock rail's depth (5.5 minus 0.15 pocket room); 6 deep would leave 0.85 skin on the outer face. The insert is 5 long.

Screw engagement in the rail insert is about 3 mm (8 - 4.86 tongue - 0.15 gap), the same as stock.

UNKNOWN: fit, insert retention, strength, airflow. Fan 195 x 30 is from Thermaltake's drawing, not measured. DC jack model.
