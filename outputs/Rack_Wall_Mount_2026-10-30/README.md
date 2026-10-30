# Lab Rax 9U wall mount — RW-WP-A / RW-RC-A / RW-SO-A (2026-10-30)

Brian picked **top French cleat + bottom standoffs** (drywall, stud reachable, rack about 6–9 kg, rear-post insert holes face the wall). Source: [rwm1.scad](../../work/rack-wall-mount/rwm1.scad) (`part` = bar / rail / standoff / assembly, `print=true` for print orientation). Our own geometry; no Lab Rax creator mesh is in these files.

**PROPOSED — NOT PRINTED. Fit, cleat hold, screw/anchor holding, insert engagement and load are UNKNOWN.**

## Parts

| ID | Part | Qty | Notes |
|---|---|---|---|
| RW-WP-A | Wall rail | 1 | 282 x 76 x 5 mm plate + 8 mm cleat (45 deg top sloping down to the wall). Exact rack width, doubles as the drilling template. |
| RW-RC-A | Rack cleat bar | 1 | Bolts across both rear posts at U9; 45 deg hook drops onto the cleat. |
| RW-SO-A | Bottom standoff | 2 | Bolts to each rear post at U1; holds the rack plumb, 30 mm from the wall. Left one = the same part turned upside down. |

The rail and bar are 282 mm long (rack width): they print diagonally on a 256 mm bed (like the Lab Rax 282 mm edges). Bed size not checked.

Outline corners are rounded (as seen from the wall, = print footprint): R5 on bar and standoffs (incl. the bar's inner step), R6 on the rail. Mating faces (cleat slope, post faces, wall face) stay flat.

## Layout (rack frame: X 0 = rack centre, Z 0 = bottom of U1, Y 0 = rack rear face)

- Rear post M6 insert holes used: X ±118.26, U9 Z 361.9 / 393.7, U1 Z 6.3 / 38.1 (Lab Rax 3-per-U pattern, same X as the front; inserts must be installed in those 8 rear holes).
- Rack rear face → wall: **30 mm** (cable gap; the saved cable exit is bottom-rear, between the standoffs X ±104).
- Cleat contact top Z 380; to take the rack off: lift ≥ 8 mm, then pull straight out.
- Bar middle (|X| < 104) only spans Z 368–408, leaving the lower part of U9's rear open.

## Hardware

- 8 x **M6 x 8 button head** into the rack's own rear-post M6 inserts (4 bar, 4 standoffs). Under-head flange 3.5 mm, counterbored Ø12 from the wall side (fasten before hanging). Engagement ≈ 4.5 mm: insert length UNKNOWN — if it is short, use M6 x 10.
- Wall: **#8 / 4 mm countersunk wood screws**, holes Ø4.5 with a 9 mm countersink, heads sit 1 mm below the face. Two rows (Z 344 and 400) of 11 holes at 25 mm pitch: drive 2 into a stud (one per row) wherever the stud falls, plus drywall anchors in the end holes (±125, both rows). Anchor and screw size/rating UNKNOWN.
- 2 x **M3 x 30 lock screw** from the top of the bar (X ±60) down into a Ø2.5 pilot in the cleat (self-tapping into the print, or fit an M3 heat-set insert). Stops the rack being lifted off. The wall is 9 mm behind the screw: use an L hex key.

## Hanging

1. Hold the rail level on the wall (V notches = centre and top screw row level line), mark through the holes, drill, screw it on.
2. Install the 8 rear inserts, fasten the bar (U9) and both standoffs (U1) to the rack.
3. Lift the rack, lower the bar's hook onto the cleat, let the standoffs rest on the wall.
4. Fit the two M3 lock screws.

## Checks (OpenSCAD)

- Seated: rack parts ∩ rail volume 0 (surface contact on the 45 deg slope only); hook tip 0.5 mm clear of the rail plate, bar body 0.5 mm clear of the cleat front.
- Lifted 0.3 mm, lifted 9.5 mm, and lifted 9.5 + pulled 20 mm: intersection empty.
- Each STL is one closed shell (Euler genus = hole count: rail 22, bar 6, standoff 2). `RW_wall_mount_set.3mf`: 4 objects (rail, bar, 2 standoffs) side by side, print orientation, plain tags (12,658 vertex / 25,428 triangle). Rebuild: `python work/rack-wall-mount/make_3mf.py outputs/Rack_Wall_Mount_2026-10-30`.
- Print orientation: rail wall-face down (cleat slope = 45 deg overhang), bar post-face down (hook underside 45 deg), standoffs post-face down. No supports expected.
- Rear-post hole X (±118.26) is taken from the 1U support extension mesh (rear holes at the same X as the front); confirm on the real rack before drilling the wall.

Viewers (not committed): seated https://claude.ai/artifact/GpjXS9DK3AJa7ufNtsFwcr, print set https://claude.ai/artifact/GEW6JMk8CDAvPBTrdqsowH.
