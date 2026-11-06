# Lab Rax rack top (Brian's 9U rack, stock creator top parts)

Device card for parts that replace or sit on the rack top. Source = creator's meshes in `work/rack-geometry-recovery/sources/5U+Lab+Rax+X2D.3mf` (mklements, BY-NC-SA, local only), placed with the rack view's recovered poses (`outputs/Mechanical_Design_App/rack-references/rack-scene.js`, 9 slots). Frame: X across (0 = centre), Y front 0 to rear 240, Z up, Z 0 = bottom of slot 9. Source values are not measurements; the recovered poses themselves are visual placements, fit UNKNOWN. Measuring diagrams: `work/rack-cooling/top_fan_options.svg` (C..J) and `work/rack-cooling/top_edge_joint_measure.svg` (P, T, X, K), both 2026-11-05.

| Ref | Value | Expected (source) | Measured by Brian | Status |
| --- | --- | --- | --- | --- |
| C | Flat top, front to rear (top of front 45° edge to top of rear one) | 175 (Y 32.5 to 207.5, Z 435.05) | | UNKNOWN |
| D | Between the handles, inside faces | 226.6 (X ±113.29) | | UNKNOWN |
| E | Top of the CM1000 to the top of the rack | 35 (Z 400.05 to 435.05; modem envelope 44.4 tall fills slot 1) | about 35 (2026-11-05) | Measured |
| F | Handle screw holes, across, centre to centre | 249.5 (X ±124.73) | | UNKNOWN |
| G | Handle screw holes, front to rear | 130 (Y 55 and 185) | | UNKNOWN |
| H | Screw holding each handle (size x length) | hole Ø7.6 in the rail top = M6 insert bore | | UNKNOWN |
| I | Stock top panel L x W x T | 228.05 x 171.5 x 3 (X ±114.03, Y 34.25..205.75, Z 430.05..433.05) | | UNKNOWN |
| J | Brian's printer bed | | | UNKNOWN |
| K | How the stock top panel goes in (before handles, slid, snapped past the rail lip) | panel overlaps the rail lip X 110.98..114.03, Z 430..435, like a trapped seat | | UNKNOWN |
| P1 | Edge plug length (front to rear) | 23.85 (Y 11.15..35) | | UNKNOWN |
| P2 | Plug drop below the edge body | 19.85 (Z 380.2..400.05) | | UNKNOWN |
| P3 | Edge front corner to plug front face | 11.15 (post solid Y 0..11 at the top) | | UNKNOWN |
| P4 | Plug thickness (along the edge) | 6.86 (X 127.12..133.98) | | UNKNOWN |
| P5 | Plug outer face to edge end | 7.14 (edge end X 141.12) | | UNKNOWN |
| T1 | Tongue into the side rail, length | 19.85 (Y 35..54.85) | | UNKNOWN |
| T2 | Tongue height | 23.85 (Z 400.05..423.9) | | UNKNOWN |
| X | Cross-holes through plug and tongue, along the edge | Ø6.4, centres about Y 22.5 Z 390 and Y 45 Z 416; what goes in them UNKNOWN | | UNKNOWN |

Other source shapes:
- Front and rear top edges ("Top Front Edge", 282.25 long): hollow 45° profiles, Z 380.2 to 435.05, wrapping over the post tops; inner face at Y 35 / 205. No holes on their top.
- Side rails ("Top Left Edge"): X ±110.98..140.98, Y 35..205, Z 400.05..435.05, hollow; a ledge for the panel at X ±113.98 from Z ~430; two Ø7.6 vertical holes per rail at X ±124.73, Y 55 / 185 (handle screws).
- Handles: X ±113.29..136.29, Y 35..205, Z 435.05..472.55, on the rails. They overlap the panel edge by ~0.7, which seems to be what holds the panel down (UNKNOWN).
- Stock panel: a 120 mm fan grille (cut-outs within ~55 radius of X 0, Y 120).
- The bottom of the rack has the same layout (bottom panel and edges), see `work/rack-cooling/Decisions.md`.

2026-11-05 (Brian): use the stock values for the joint (P, T, X) and the panel/handle shapes; everything else on the rack has worked from stock values. They stay UNKNOWN as measurements. Rows C, D, F, G, H, I, K are not needed by the recessed-fan design.
