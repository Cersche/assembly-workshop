# 9U extrusion rack frame — BOM (PROPOSED, 2026-10-31)

**Chosen: option A (Brian, 2026-10-31).** 2020 aluminium extrusion box frame joined by printed, rounded 3-way socket corner nodes (style per Brian's reference picture, "a little more rounded"). Faceplates and hole strips stand ~12 mm proud of the frame front. Concept model: work/rack-frame/concept-AB/A_*.stl, viewer work/mesh-viewer/Rack_frame_A_vs_B.html (left = A).
Fit, stiffness, strength and hole alignment are UNKNOWN until printed parts prove them. Nothing ordered or printed by Claude.

## Layout
- 9U = 9 x 44.45 = 400.05 mm usable height; posts sit on the node cores (first U starts at the node top).
- Inside width 208 mm (as the current rack); hole line ±118.26 on the post front face.
- Front-to-rear mounting depth 240 mm (OptiPlex sleeve / SLV-B frame depth).
- Nodes, sockets and column trim share one 28 mm rounded section (R6), so all outer faces are flush. Post socket is open at the front/rear so the hole strip runs down to the node.
- Overall ~256 W x 248 D x 456 H mm.

## Order list

| # | Item | Qty | Spec / note |
|---|---|---|---|
| 1 | 2020 extrusion, posts | 4 | 400 mm (9U is 400.05; the 0.05 is irrelevant because the strips locate off the node). End tapping not needed: the sockets clamp with T-nuts |
| 2 | 2020 extrusion, width members | 4 | 200 mm (4 mm slack each end in the sockets) |
| 3 | 2020 extrusion, depth rails | 4 | 180 mm (184 mm gap, 2 mm slack each end); if 180 isn't sold, buy 200 and cut 16–20 mm off |
| 4 | M5 roll-in T-nuts for 2020 (6 mm slot) | ~140 | nodes 48 (8 x 3 sockets x 2), trim 24 (12 x 2), strips 36 (12 x 3), braces 16 (2 x 8) = 124, plus spares |
| 5 | M5 x 10 button or socket head screws | ~100 | nodes, trim, braces |
| 6 | M5 x 10–12 countersunk screws | ~40 | hole strips; heads below the strip front face |
| 7 | M6 x 5 x 8 heat-set inserts | 72 + spares | 2 per U per post x 9U x 4 posts (108 for all 3 EIA holes) |
| 8 | M6 x 8 button-head screws | on hand | mounting gear |
| 9 | Rubber feet (optional) | 4 | under the bottom nodes |

All extrusion, T-nuts and screws for the same 2020 profile / 6 mm slot. M5 approved by Brian 2026-10-31 for the frame hardware only; printed parts keep the normal fastener rules.

## Printed later (not ordered)
- 8 corner nodes, 12 column trim pieces (3 per post), 12 hole strips (3U, 133.35 mm, M6 inserts), 2 side brace panels (middle 3U, one per side).
- Coupon first (one node + short post section + one strip), with a test ID.

## Open items
- Hole spacing: strict EIA 15.875 or Lab Rax 15.902. Does not affect this order.
- 180 mm 2020 availability not checked.
- Generator: work/rack-frame/frame_ab.py (`python work/rack-frame/frame_ab.py work/rack-frame/concept-AB`).

## Checked against the model (2026-10-31)
Post gap inside 208 → width member 200 (4 mm slack/end). Front-to-rear post gap 184 → depth rail 180 (2 mm slack/end). Mounting faces Y 25 / 265 = 240. Nothing intrudes into the 208 inside width above the bottom node. Overall 256 x 248 x 456 incl. plates. Insert count 2 x 9 x 4 = 72. Screw/T-nut counts above assume 2 screws per socket, 3 per strip, 2 per trim piece, 8 per brace.
- Socket hollows, key ribs, screw slots, trim mounting and strip thickness are not drawn yet.

## History
Earlier same-day concepts (metal corner brackets; stacked corner blocks; option B flush bezel frame) were superseded by option A.
