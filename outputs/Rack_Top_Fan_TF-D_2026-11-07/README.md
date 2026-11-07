# TF-D: rack top, CT200 fan screwed down (2026-11-07)

**Print this set together with the TF-C coupons if wanted. It replaces TF-C's edges and grille.** Rails are unchanged (TSR-B, same as TF-C; reprint not needed if your TF-C rails are good). Design story: `../Rack_Top_Fan_TF-C_2026-11-06/README.md`.

## What changed from TF-C (Brian 2026-11-07: "the fan has to be mounted")
- TF-C only clamped the fan under the grille. TF-D screws it down through its own corner holes (155 x 155, Thermaltake drawing; standard fan holes, ~4.3, not measured).
- Edges **TFE-D / TRE-D**: a pad under each fan corner (12 OD x 8, Z 409.05..417.05, X +-77.5, Y 42.5 / 197.5), hanging from the ledge into the 15 mm air gap; M3 x 3 x 5 insert bore 4.2 x 4 from the top, 3.4 hole below for the screw tip. The fan sits on the pads flush with the ledge.
- Grille **TFG-B**: 4 x 7.5 holes over the screws so the M3 socket cap heads (5.5 x 3) sit flush with 1 mm room and a hex key goes in from above.
- Rear edge: DC jack hole and pocket removed. Plain cable notch in the inner face at the left end of the fan cavity (X -98..-108, Y 204..210, full height, open inside and on top; 1.9 mm short of the grille's corner M3 insert bore). Grille covers it.
- Everything else is TF-C unchanged: plugs, tongues, M6 x 8 button-head cross joints, cavity 196, grille corner screws, chamfer, rails.

## Parts (`TF-D_4-parts-print-layout.3mf`)
edge_front **TFE-D** (turned x90), edge_rear **TRE-D** (turned x-90), rail **TSR-B** (print 2), grille **TFG-B**. Edges are 282 long: turn them diagonally on a 256 bed as with TF-C; plugs need a small support each.

## Hardware
- New: 4 x **M3 x 35 socket cap** (new screw type, Brian) + 4 x M3 x 3 x 5 inserts in the pads.
- As TF-C: 8 x M6 x 8 button head + 4 x M6 x 5 x 8 inserts (rails); 4 x M3 countersunk + 4 x M3 x 3 x 5 inserts (grille); handle screws into 4 x M6 x 5 x 8 inserts in the rail tops.

## Checks
0 failed, 3 warnings, all kept:
- grille: dia 7.5 near the M6 insert bore 7.6: it is the socket-cap head hole, not a bore.
- grille: dia 4.23 near 4.2: slice of the countersink cone (as TF-C).
- rail: M6 insert bores about 5.25 deep (stock depth, as TF-C).

UNKNOWN: fan holes run the full 30 (needed for M3 x 35), hole diameter, CT200 cable exit point/thickness (notch 10 x 6), pad strength, insert fit, overall fit, airflow.
