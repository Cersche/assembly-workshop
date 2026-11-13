# TF-A: rack top for a 200 mm exhaust fan (released 2026-11-06)

Our own top for the 9U Lab Rax rack (option B, Brian 2026-11-05/06): new front and rear top edges, new side rails and a swirl grille. A Thermaltake CT200 ARGB (200 x 200 x 30) sits fully recessed on ledges in the edges, and the grille clamps it down, flush with the top. The top is 50 tall (stock 35), which leaves a 15 mm air gap above the CM1000 in slot 1. The stock handles go back on the new rails, 15 higher. The stock side panels slide into the same groove as before. Source: `work/rack-top-fan/rack_top_fan.scad` (frozen in `src/`), rendered with the OpenSCAD 2026.11.01 snapshot and Manifold.

## Parts (`TF-A_6-parts-print-layout.3mf`, already turned for printing)

| Object | ID on part | Print | Lies on | Size on the bed |
|---|---|---|---|---|
| edge_front | TFE-A | 1 | flat front face | 282.2 x 69.9, 54.8 tall: **rotate 45° on a 256 bed** (about 3.5 mm spare) |
| edge_rear | TRE-A | 1 | flat back face (DC jack hole) | same, rotate 45° |
| rail | TSR-A | **2** (the same part serves both sides) | outer face | 50 x 170, 30 tall |
| grille | TFG-A | 1 | underside | 221 x 205.4, 3 tall |
| coupon | TFE-T1 | 1, optional | front face | edge end, X 101..141: tests the plug, tongue and cross-holes on the real post |
| rail_coupon | TSR-T1 | 1, optional | outer face | rail front end: tests the tongue pocket, groove and an M6 insert |

The 3MF holds all six on one stack, so split them onto plates in the slicer. Each edge plug sticks out sideways about 20 mm and needs a small support under it (2 per edge). No other supports should be needed. IDs are engraved 0.6 mm deep: edges and rails on the inner face, the grille on its underside.

## Hardware
- Grille: 4 x M3 countersunk screws into M3 x 3 x 5 heat-set inserts (4.2 bore, 5 deep), one in each corner of the edges. Countersink 7.0 mm, 90°.
- Handles: the stock handles, with M6 x 5 x 8 inserts (7.6 bore, 10 deep) in the rail tops at the stock positions. The handles seat on the rail tops as on the stock rails, so the stock screws should reach. Their length into the 10 mm deep inserts is UNKNOWN.
- Cross-holes Ø6.4 at the stock positions: what goes through them is UNKNOWN (stock design).
- DC panel jack: Ø8 hole low in the rear edge's back face (X 85, Z 407.5), with a pocket behind it that opens down into the rack. Jack model UNKNOWN, 5.5 x 2.1 assumed. The pocket allows a body about 33 mm deep.

## Values
- Joint (plug, tongue, cross-holes, rail pocket fit 0.15/0.15/0.1, side-panel groove) uses stock source values, per Brian. These are not measurements.
- Fan 200 x 200 x 30 comes from listings and is not measured. Fit 0.5 each side, on 2 mm ledges. Opening Ø192.
- Grille fit 0.3 each side. Swirl: 16 blades 2.4 wide, one ring at r 62, hub r 14.
- 45° chamfer 15 x 15 on the outer top corner of each edge.

## Checks (release_report.md)
0 failed, 1 warning: grille "dia 4.23 close to the M3 insert bore", which is a slice of the countersink cone, not a bore. Every part is a closed single body, the IDs are on the meshes, the 36 grille openings are separate and the screw heads are clear. Codex task 53 and the draft checks found no clashes with the stock posts, raised handles or each other; draft 4 only removed material. Legibility of the IDs was not checked.

## UNKNOWN
Fit of the plug/tongue joint and rail pockets, fan fit, insert retention, strength, airflow, temperatures, handle screw length, cross-hole hardware, DC jack, buck converter and ARGB controller models, and printability on Brian's printer (256 x 256 bed assumed from his answer).

## Fit report to send back
For each ID (TFE-T1, TSR-T1, TFE-A, TRE-A, TSR-A x2, TFG-A):
- Fits or not; where tight or loose, and by how much if measured.
- Plug into the post top, tongue into the rail pocket, side panel into the rail groove.
- Fan in the cavity (side play, does the grille sit flush?).
- Grille screws and inserts; handle screws reaching the M6 inserts.
- DC jack fit, if one is fitted.
- Walls/infill used, and whether the plug supports came off cleanly.
