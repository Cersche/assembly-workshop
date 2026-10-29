# Task 49 — SCR5-B plate-anchored rear clamp

2026-10-29, Codex. **Implemented; `--final` digital gate PASS. Not printed. Vendor dimensions nominal; fit, preload, retention, contact lands, access, ribbon reach and strength UNKNOWN.** Claude/Brian review remains outstanding.

## Result and scope

New standalone `outputs/Screen_5in_SCR5-B_2026-10-29/` delivers `SCR5-B_plate.stl`, `SCR5-B_frame.stl`, and `SCR5-B_screen_plate_and_frame.3mf`, with parameterized SCAD/JSON, Python 3.10 standard-library builder, README/BOM/assembly sequence and checks. SCR5-A, HP4-M6-A/B, Final_3MF, official user data and app code remain unchanged. No screen fasteners, screen disassembly, interspace assumption, clip capture, app integration, printing or physical tests.

## Geometry and fastening

Preserved plate: 252 x 88.8 x 4, intended X +/-126, Y -4..0, Z 0.05..88.85, outer R2.5. Screen centre X=0/Z=44.45. The explicit 88.8 is 0.05 shorter than the older task-25 2U formula; app/rack pitch unchanged. All eight 10 x 7 horizontal rack slots retain their exact parsed SCR5-A boundary vertices and the complete plate bounds compare exactly. Pocket inner half-width/height 65.75/39.6, 3 mm walls and Y=0..20 envelope retained. Old hook windows removed for the new fastening.

Four integrated plate bosses: X +/-65.5, Z 22/67, radius 3.25, rear Y=20. Each remains within X +/-68.75 and merges into its sidewall. New screen-clearance parameters are 0.5 per side, independent of the preserved wide cavity. Closest boss edge X=62.25 clears the PCB-with-clearance at 61.0 by 1.25 mm; aperture edge 57.35 by 4.90 mm. This replaces SCR5-A's interspace carrier and active-projection overlap. Fixed structure stays inside inherited +/-104 screening boundary; physical rack fit UNKNOWN.

Brian-confirmed nominal inserts: M2.5, 4 mm long, 3.5 OD; install from rear into the plate. Provisional pilot 3.4, seat 4.2 (floor Y=15.8), lead-in 0.3, nominal insert span Y=16..20. Frame ring seats at Y=20..24, screws enter from rear into plate bosses, through frame clearance holes 2.9; nothing engages screen holes. Selected M2.5 x 7 under-head length, conditional allowed range 6.5..7.6, nominal engagement 3, insert-front tip reserve 1. Minimum engagement 2.5 and required reserve 0.4 are unverified screening criteria. Head 4.5 x 2.5 (rear Y=26.5), head/tool margins and pilot/usable thread remain UNKNOWN physically. No counterbore invented.

Frame outer 137.5 x 77.7 / inner 110.5 x 63.5, both R3. Four R0.75, 4 x 4 edge pads at X +/-58, Z 14.45/74.45 extend forward from the ring to Y=12.3. Sole depth input is total screen depth 12.6 nominal. Parameterized 0.3 interference gives 7.7 pad projection; no glass thickness, PCB plane or interspace input. Actual edge bearing lands, component freedom, compression and safe preload remain UNKNOWN. Modeled touch/FPC boxes are explicit provisional keepouts, not PCB depth measurements.

## Rounding, insertion and access

Window remains 114.7 x 71.2, 3 mm lips, now R4. Analytic full-corner containment and parsed front-through rays pass for the centred nominal 109 x 65.8 active rectangle plus 0.25 keepout. Active registration UNKNOWN; no universal optical approval. R4 diagonal inset 1.657 mm is below the nominal 2.85/2.70 margins.

Pocket square cavity plus outward R1 overcuts at its corners preserves the entire square-glass/PCB insertion path; minimum overcut wall 2 mm. An exact CAD swept-clearance intersection is empty with frame removed, from Y=0.01 rearward; the Y=0 lip is the intended stop. Frame loads behind the intact screen, presses only through the four modeled pads, and is removed rearward after undoing its four screws. No screen disassembly needed by this geometry.

Top-left ribbon opening: X=-52/Z=85.05, 18 x 16, Y=11..27. Top-button access X=0/Z=84.05, 38 x 12, Y=11..26. Both have R1 silhouettes and 0.4 mm front/rear mouth reliefs using eight-segment quarter-circle lofts. Access cuts clear pads/bosses/tool projections and leave one connected frame. Actual ribbon contacts, bend envelope, finger approach, buttons and component positions remain UNKNOWN. Frame rear SCR5-B engraving 0.5 deep leaves 3.5 wall, clear of contact/screw areas; no front engraving.

## Actual checks

`py -3.10 outputs/Screen_5in_SCR5-B_2026-10-29/src/SCR5-B_build.py --final` and subsequent `--check-only` both PASS. OpenSCAD.exe 2021.01 and Python 3.10.4; no app changes, so app suite not rerun.

| Part | Vertices | Triangles | Edges | Positive volume mm3 |
| --- | ---: | ---: | ---: | ---: |
| SCR5-B plate | 2440 | 4912 | 7368 | 80580.72015121 |
| SCR5-B rear frame | 4486 | 8988 | 13482 | 13776.74076457 |

- Both delivered parts: one exact-coordinate closed connected shell, zero bad/winding edges, zero degenerate faces; no mesh welding, coordinate rounding, repair or nudge.
- Supplementary triangle self-intersection screens pass (1e-9 mm predicate tolerance, incident edges excluded); numerical screening, not exact-arithmetic certification.
- Plate bounds/slot equality, rounded aperture/active rays, nominal rear insertion sweep, full boss clearance, pilot floors and frame through-bores pass.
- Plate/frame contact is entirely Y=20; numerical signed-volume sum 3.16e-12 mm3, geometrically planar. Plate/screen contact is entirely Y=0, zero volume. Frame/screen overlap is 18.61447940 mm3, exactly confined to intended pad prisms at Y=12.3..12.6; subtracting intended contacts gives an empty CAD solid. This models configured interference; no physical compression/pressure approval.
- Engraving comparison removes 13.44120416 mm3; 1180 actual mesh floor vertices at Y=23.5. Positive remaining wall 3.5 mm.
- Provisional touch/FPC boxes have zero overlapping frame-triangle AABBs. Actual components and edge lands remain UNKNOWN.
- 15 invalid configurations rejected: screw lengths, insert depth/pilot, NaN clearance, active obstruction, through-ID, boss/screen collision or lack of anchorage, excessive preload, pad off PCB, blocked insertion, invalid radius and access/pad collisions.
- Independent 3MF ZIP/XML reopening: exactly two named resources/build items, mm units, finite coordinates/valid indices, closure/positive volumes, exact indexed triangles after rigid placement, 12 mm X gap, both print minima Z=0, plain vertex/triangle tags, no ns0. Plate front down; frame rear down so its pads rise from the ring. No scaling, screen dummy or hardware in delivery package.
- mesh_viewer.py loads both STLs, final 3MF, all six retained probe meshes and original SCR5-A comparison plate. Front/rear/assembled/separate/print/probe pages generated, uncommitted. No slicer or interactive GUI load claimed.
- 383 protected file SHA-256 hashes unchanged; authorized HANDOFF update excluded. Scope includes complete SCR5-A, HP4 A/B, Final_3MF, data/normal-use, Mechanical_Design_App and root instructions/roadmap. Unrelated local viewers/backups/stash preserved.

A first source-level mouth-rounding trial generated degenerate faces and was rejected by the gate. Replacing overlapping thin cutter slices with a single loft produced the passing meshes. OpenSCAD logs record alternate construction for nonplanar cutter quads; delivered meshes are independently checked. Contact-plane probes appropriately trigger manifold warnings as zero-volume sheets; they are checks only. No exported delivery mesh repair or relaxed topology acceptance.

## Ribbon datums and limitations

HP4-M6-B source read only: floor slot X -86..-62/Y 87..95, shared plate rear Y=0. U5 floor Z=8.225..11.225 plus U5 start 88.90 gives screen-local Z=97.125..100.125; rack-global adds another 88.90. Waypoints and front/side route sketch are in checks/ribbon-route.json and SCR5-B-route.svg. Same task-48 datums, no screen mirroring/rotation or bracket rebuild.

Polyline 128.56 mm; illustrative insertion 16 + slack 15 + bend reserve 10 = 169.56 mm. Connector positions and allowances are assumptions. 160 mm ribbon reach, bend room, actual obstructions and contact orientation UNKNOWN.

## Delivery and review

[README and BOM](../../outputs/Screen_5in_SCR5-B_2026-10-29/README.md). Local review hub `work/mesh-viewer/SCR5-B-index.html`; mandated standalone mesh page `SCR5-B-review.html`, plus assembled/front/rear/print/probes/preservation pages. A command-line OpenSCAD rear preview was inspected; no desktop-control session or physical assembly was performed.

**Private Artifact publishing pending in Claude.** No SendUserFile/private Artifact tool is available on this Codex host; local viewer links are provided instead. No public substitute, no fabricated URL. Viewer HTML is excluded from the commit.

Remaining numeric/physical unknowns: active/glass/PCB registration; actual total depth/contact lands; pilot process and usable engagement; actual screws/tools; component/FPC/header/buttons/finger envelopes; safe preload/pressure; ribbon bends/reach; printed fit, insert retention and strength. JSON carries null measurement evidence plus explicit adjustable numeric assumptions. None silently passes from a digital check.

## Source and mesh SHA-256

Complete manifest: `outputs/Screen_5in_SCR5-B_2026-10-29/checks/hashes.json`; protected baseline: checks/baseline.json; verification: checks/preservation.json. Task-local `.gitattributes` preserves bytes across Git line-ending settings.

| File | SHA-256 |
| --- | --- |
| `src/SCR5-B_build.py` | `cf0829437765fd285f237b0cfeecf6c72a6ea1e73c929097cc289eaeadf490ff` |
| `src/SCR5-B_geometry_checks.py` | `5a342c28f1bb2067e9fba94aa365936719e85c4c949b52e667c312f07d91bf17` |
| `src/SCR5-B_review.py` | `af31dc4c3831e7504ffb5f4a6fc9346d68d773876d9fbc1de14413d047f0b8b8` |
| `src/SCR5-B.scad` | `0686fee448e2207c59980467e2a4be8c6efb8f41e0651dac4e26e367c5d995e6` |
| `src/SCR5-B_config.scad` | `d4a3391b8042fb30934419fc83e93f0c7d640017b26200c95a4c5f8a8ad9706c` |
| `SCR5-B_frame.stl` | `38595bffc46861bd00e1836c8b92f63a4432568a6a59c9eb90e006dfa8f834d2` |
| `SCR5-B_plate.stl` | `7ee7809c24f5dc14a06f9543b8e7f8af9b7fe14c568d2dd3020303cb3c27be9d` |
| `SCR5-B_parameters.json` | `5453a138cb86562a461085030085da8478498f33d8f972b91138938ed4439e5a` |
| `SCR5-B_screen_plate_and_frame.3mf` | `9b4a449b8409764974aa8562ed348895e84d006281c540e5351f782a88ccd602` |

## Synchronization

Initial git pull fast-forwarded d97ead0 to 7290591 on existing main, adding the approved task 49 spec/prompt. Only the new SCR5-B folder, this report and HANDOFF are staged for the authorized private origin/main commit/push. Generated viewers, earlier untracked work and preservation copies are excluded. Push outcome and commit ID are verified in the final chat; no force push.
