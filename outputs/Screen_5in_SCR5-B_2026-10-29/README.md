# SCR5-B — 2U screen plate with plate-anchored rear clamp

Task 49, 2026-10-29. **Vendor dimensions nominal. Not printed. Fit, preload, retention, contact lands, button access, ribbon reach and strength UNKNOWN.** The `--final` gate validates configured digital geometry and packaging; it does not approve physical hardware. Claude/Brian review remains required. SCR5-A is immutable history.

Files: `SCR5-B_plate.stl`, `SCR5-B_frame.stl`, `SCR5-B_screen_plate_and_frame.3mf`; parameterized `src/SCR5-B.scad`, `SCR5-B_parameters.json`, Python 3.10 standard-library builder/checks/review scripts, and `checks/` evidence. No screen, screw, route or reference bracket is included in the delivery 3MF. No Final_3MF copy or app/library integration.

## Architecture and preserved geometry

Nothing fastens into the screen. Four bosses integral to the **plate** carry M2.5 heat-set inserts installed from the rear, axes parallel to Y. A rear frame screws to these bosses and presses four provisional edge lands forward onto the front lip. There is no carrier between glass and PCB, clip capture or screen-hole dependency; total screen depth 12.6 nominal is the sole screen-depth input.

Assembly coordinates: X negative is left viewed from front, Y positive into rack, plate rear Y=0, Z up from U3 bottom. Screen centre X=0/Z=44.45; rack-global Z=local+88.90; U5 starts at local Z=88.90. Explicit plate 252 × 88.8 × 4, X ±126, Y −4..0, intended Z 0.05..88.85, outer R2.5. This is 0.05 shorter than task 25's older 88.85 mm 2U formula; app/rack pitch unchanged. Rendered coordinates have OpenSCAD/float32 discretization, recorded in topology evidence.

Eight horizontal 10 × 7 capsule slots remain at X ±118.2625, Z 6.323/38.127/50.773/82.577. Their exact parsed boundary vertices are compared with SCR5-A. SCR5-A's sidewall envelope is preserved: inner X ±65.75, Z 4.85..84.05; outer X ±68.75, Z 1.85..87.05; depth Y=0..20, 3 mm walls. Old capture windows are removed as part of the fastening replacement. No new visible front fasteners or front engraving.

The four new boss axes X ±65.5, Z 22/67 have radius 3.25 (3.5 OD insert + 1.5 radial wall), merging into the existing sidewalls without extending their outer boundary. Glass clearance is independently 0.5 each side; PCB clearance 0.5 each side, registration offsets 0 by assumption. The boss inboard edge is X ±62.25: **1.25 mm beyond** the widest configured PCB-with-clearance outline at ±61.0, and 4.90 beyond the aperture at ±57.35. Pocket width is independent of screen insertion clearances; SCR5-A's large 5.4/5.25 side values described its widened cavity, not measured required screen clearance. No pocket shrinking is hidden in the new clearance values. Rear fixed structure remains inside inherited ±104 screening boundary; physical rack fit UNKNOWN.

## Rounded corners and seating

Front window 114.7 × 71.2 has R4; four independent lip overlaps remain 3 mm. The centred 109 × 65.8 active rectangle plus a provisional 0.25 keepout passes both analytic rounded-rectangle corner containment and parsed-mesh front-through rays. Active-area registration is UNKNOWN; this is a conditional centred-assumption check only. R4 diagonal inset R(√2−1)=1.657 is below the nominal 2.85/2.70 margins.

Rear pocket retains a complete square cavity and adds outward R1 circular corner overcuts at all four cavity corners. The square glass and PCB, including configured clearances, remain wholly inside the seating/insertion prism. There is no inward fillet blocking a square corner. Remaining minimum wall at the overcuts is 2 mm. Exact CAD insertion-sweep intersection is empty for rearward travel with the frame removed; the lip at Y=0 is the intended seating stop.

Frame outer 137.5 × 77.7 and inner opening 110.5 × 63.5 both use parameterized R3. Its rear ring Y=20..24 rests on the bosses/sidewall rear seats. Four 4 × 4 pads with R0.75 corners at X ±58, Z 14.45/74.45 extend to Y=12.3, giving a configured **0.3 mm interference** with the nominal 12.6 mm screen rear envelope. Pad projection from the ring is 7.7 mm. Preload changes pad reach, not boss/screw seating. This is geometric interference for future tuning, not a spring/compression model or safe pressure claim. The 12.6 envelope does not establish the actual PCB edge plane or a suitable contact surface.

## Hardware and section stack

| Quantity | Item | Basis / limitations |
| --- | --- | --- |
| 1 each | SCR5-B plate / rear frame | New configured geometry; unprinted |
| 4 | M2.5 inserts, 4 long × 3.5 OD | Brian-confirmed nominal sizes |
| 4 | M2.5 × 7 socket-cap screws | Conditional selected under-head length; valid range 6.5..7.6 |
| 8 | Existing rack-faceplate fasteners | Existing four-per-U arrangement; no new rack hardware specification |

Rear-installed inserts occupy Y=16..20. Blind pilot Ø3.4, seat depth 4.2 (floor Y=15.8), lead-in 0.3 to Ø3.8 are independent **process assumptions**, not certified printed fits. The 15.8 mm floor to plate rear and 1.5 nominal radial insert wall stay positive. Source/builder validate dimensions before rendering.

Screws enter from +Y, head bearing on the frame rear at Y=24, shaft through Ø2.9 clearance holes and into the plate bosses. Default head Ø4.5 × 2.5 reaches Y=26.5; Ø5.5 rear tool envelope and extra head clearances are parameters, actual screws/tool access UNKNOWN. There is no counterbore: the head bears on the frame rear. Frame outer-edge margin to the head envelope including 0.6 diametral clearance is 0.70 mm; to the tool envelope it is 0.50 mm. These are screening margins, not strength proof.

Under-head stack is 4 mm. Minimum engagement 2.5 and insert-front tip reserve 0.4 are provisional criteria, yielding length range 4+2.5=6.5 through 4+4−0.4=7.6 mm. Selected 7 gives nominal engagement 3 and insert-front tip reserve 1 mm (screw tip Y=17). Usable thread engagement, insert retention and printed fits remain UNKNOWN. No screen screw holes are used. No purchase or torque/load recommendation.

SCR5-B is engraved 0.5 deep on the frame rear, leaving 3.5 mm wall; unengraved comparison mesh verifies removed volume and actual engraving floor vertices. Plate front has no ID.

## Assembly and access

1. Install the four inserts from the plate rear with electronics absent. Keep the frame removed.
2. Slide the upright, centred screen from the rear through the square clearance passage. Seat the glass black border against the lip at Y=0. No screen disassembly or glass/PCB gap access is required.
3. Route the ribbon upward through the top-left opening. Screen connector estimate X≈−52, upper half; actual position/contact orientation/bend radius UNKNOWN. Opening default X=−52/Z=85.05, 18 × 16, Y=11..27, R1 silhouette. Rounded notch corners and parameterized 0.4 mm mouth reliefs (eight-segment quarter-circle flares) remove sharp path turns and soften front/rear contact edges; actual cable contact, edge finish and bend sweep remain unverified.
4. Place the frame behind the screen, align all four screws to the plate bosses, and seat the frame on the rear boss/wall seats. Pads press only the four modeled edge regions. Their actual component-free suitability and safe preload need screen evidence/tuning. No safe tightening procedure is established.
5. Top button access defaults X=0/Z=84.05, 38 × 12, Y=11..26, R1 with 0.4 mm mouth reliefs, approached from the rear/top. Open centre leaves provisional touch/FPC boxes clear. Actual component envelopes, finger access and buttons remain UNKNOWN. Access cuts clear pads/bosses and leave one connected frame.
6. Support the screen, undo the four frame screws, remove the frame rearward, then lift the screen off the lip and withdraw rearward. No modeled latch deflection required.

## Ribbon route and print placement

Read-only HP4-M6-B source confirms its floor slot X −86..−62, Y 87..95, common plate-rear Y=0. U5 floor Z=8.225..11.225 translates to screen-local Z=97.125..100.125. `checks/ribbon-route.json` and `SCR5-B-route.svg` recompute the same task-48 datum chain: approximate screen connector (−52,13.1,66.45), exit (−52,18,87.5), lateral transition (−74,25,90), slot underside/top (−74,91,97.125/100.125), approximate Pi connector (−74,81,110.4). Polyline 128.56 mm plus illustrative insertion 16, slack 15, bends 10 =169.56 mm. All allowances/connector estimates are assumptions; **160 mm reach and obstruction/bend clearance UNKNOWN**. HP4 geometry was neither rebuilt nor modified.

The 3MF contains exactly `SCR5-B plate` and `SCR5-B rear frame`, mm units, rigid rotations only, separate side-by-side with 12 mm X gap and individual min print Z=0. Plate front is bed-facing; frame rear is bed-facing so pads rise from the ring. Assembly STLs retain common datums. Packaging is not slicer/process approval. Literal plain `<vertex>`/`<triangle>` tags, no `ns0`; independent ZIP/relationship/mesh parse checks exact indexed triangle correspondence after the documented rotations/translations. No slicer load was performed.

## Reproduce and inspect

From project root: `py -3.10 outputs/Screen_5in_SCR5-B_2026-10-29/src/SCR5-B_build.py --final`. Explicit OpenSCAD.exe build only; no automatic build. `--check-only` verifies existing render-input hashes, meshes, retained probes, packaging and preservation without rendering. Edit JSON numeric assumptions deliberately and rebuild with `--final`; stale input hashes block check-only acceptance.

Checks include exact-coordinate closure/winding/single shell/positive volume/no degenerate faces; numerical triangle self-intersection screen (1e−9 predicate tolerance, no mesh repair or welding); plate bounds/slot preservation; active-area containment; rear insertion sweep; bosses/pilot/engagement; nominal assembly intersections and intended pad interference; engraving; provisional component boxes; invalid-parameter rejection; 3MF round trip and all retained mesh loads; protected-file hashes. JSON evidence distinguishes conditional/skipped checks. App code unchanged, so app suite not rerun. No desktop or physical test.

Local viewer hub: `work/mesh-viewer/SCR5-B-index.html`, with front/rear/assembled/separate/print/probe views; generated HTML stays uncommitted. **Private Artifact publishing pending in Claude**: SendUserFile/private Artifact tools are unavailable on this Codex host. Local links are not publication. See task report and `checks/hashes.json` for mesh/source SHA-256 evidence. No printing or physical approval.
