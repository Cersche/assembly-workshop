# TF-B: rack top fan edges for the real 195 mm CT200 frame (2026-11-06)

Thermaltake's dimension drawing (sent by Brian) gives the CT200 frame as **195 x 195 x 30**, not the 200 from the listings. TF-A's 201 cavity would let the fan slide about 3 mm each way, so these edges replace TF-A's edges only.

- Change: fan 200 -> 195, so the cavity is 196 x 196 (fit 0.5 each side, unchanged), front face at Y 22. Fan thickness 30, ledges, air gap, chamfer, grille seat, joint, screw inserts and DC jack are all unchanged. Clearances are not tightened.
- Parts (`TF-B_2-parts-print-layout.3mf`, turned for printing): edge_front **TFE-B**, edge_rear **TRE-B**. Rotate each 45 deg on the 256 bed. Each needs a small support under its two plugs.
- Still from TF-A, unchanged: rail TSR-A (print 2), grille TFG-A, coupons TFE-T1 and TSR-T1 (`outputs/Rack_Top_Fan_TF-A_2026-11-06/`). **Don't print TF-A's edges (TFE-A, TRE-A).**
- Checks: 0 failed, 0 warnings (release_report.md).
- The fan rests on the 2 mm ledges at its corner tabs and the ring, within about 12.5 mm of the front and rear sides.
- UNKNOWN: 195/30 come from Thermaltake's drawing, not a caliper. The joint uses stock values. Fit, strength, airflow, DC jack, handle screws and cross-hole hardware also UNKNOWN.

Fit report: as in the TF-A README, using TFE-B / TRE-B for the edges, and add whether the fan sits square without rattling.
