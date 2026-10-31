# SCR5-H — screen, Pi and Hue draft — 2026-10-30

**NOT ACCEPTED. Not for printing. Fit, strength and airflow UNKNOWN.** Strict acceptance fails at the inherited conservative Hue box versus the retained F cradle: 5,171.005978 mm³. This reproduces F's documented envelope overlap; actual fit is not established. No unmeasured rounded Hue body was invented to erase it. Root STLs are development drafts. The normal `SCR5-H_screen_pi_hue_set.3mf` export is withheld; `checks/SCR5-H_UNVALIDATED_candidate_set.3mf` is a diagnostic candidate only.

## Decisions and source registration

- Front = G: glass centre X33/Z41.5, front Y0; window121.1×77.6 (0.2 clearance each side),0.3 front chamfer,0.8 cosmetic left/right lips only; R2.5 corners and eight rack slots. Lips do not retain the screen.
- G rear frame is unchanged except the required rear H engraving. All three G pins retain DROP0.45; module source and canonical triangle sets match G exactly. Full stroke1.4, rest to cap stop. Frame, plate rear, floor top and mirrored deck underside carry SCR5-H.
- F tray datum Y0→H plate rear Y4. Pi-zone front0→4; rear-zone front36→40; rear148→152. This is a4 mm registration shift, with no additional whole-edge setback. Pi/Hue/fan move+4Y with the tray. The copied F tray definitions differ only in ID strings; H wrappers add registration and clearance.
- Retain F four Pi standoffs, seven floor vents, twelve right-wall vents, R6 floor/deck corners, fan, Hue cradle, five wall-top M2.5 insert bosses, open-top rear cable notches and two M6 tabs.
- Added Ø6 frame-tool clearance channels locally through the floor (0.25 radial clearance around Ø5.5 tool envelopes). All five insert seats remain intact; floor stays one shell. The corresponding deck subtraction removes no material.
- Retain both F USB openings15×17.5 and Ethernet17.5×15, plus the golden keystone atX−92.5/Z66: these clear G's screen window/frame/pins. Its old0.08 proud golden face is shifted back0.08 so H front minimum isY0, without changing the aperture dimensions.

## Measured values and limits

`work/screen-5in/Dimensions.md` is the screen authority and remains unchanged. Glass2.5 (0.9+1.6), metal3.0, gap2.0, PCB1.6 give PCB backY9.1. Preserve G's direct-caliper rear seat13.3. Nominal4.0 standoffs plus layer sum give13.1: the0.2 disagreement remains UNKNOWN; G's conservative4.2 standoff envelope is not a new measured height. PCB centred under glass is CONFIRMED. Actual screen DSI dummy W=5.0; retain G's deliberately larger8 mm inward envelope plus3 mm around it. Connector span is PCB-bottom+30..51, above-PCB height5.25. Corner pattern112.9×68 and button dimensions follow G/Dimensions.

Only corner screen standoffs are localized; inner standoff registration is not measured. Button centre precision and touch lateral extent remain limited by the documented assumptions. The old F screen config is copied for provenance/dependencies; H uses the G screen definitions, not F's old12.6-depth screen envelope.

The *model's vertical* lit centre41.5+(8.6−2.8)/2=44.4 matches the plate centre, error0. This is the G centring criterion: screen intentionally sits atX+33. Borders are drawing estimates±0.5, so physical0.1 mm lit registration remains UNKNOWN.

## Ribbon

Assembly route(mm): `(-24,14.5,44) → (-40,24,44) → (-40,32,33) → (-74,85,22)`.

Centreline96.1311 + explicit15 bend/endpoint allowance = **111.1311 mm**, under140; estimated slack on160 cable48.8689. Descent is behind the deck tab pad. The1 mm diameter diagnostic path intersects neither floor nor deck. Frame∩G18 mm corridor is zero. `checks/SCR5-H_ribbon_route.stl` is a centreline diagnostic, not a verified flat-ribbon swept envelope. Pi connector dummy and endpoint are approximate F-layout assumptions. Actual bend radius, twist, engagement and reach remain UNKNOWN; connector/Pi endpoint overlaps remain visible in the table.

## Checks

| Part | Triangles | Shells | Bad edges | Degenerate |
|---|---:|---:|---:|---:|
| plate | 7,740 | 1 | 0 | 0 |
| frame | 3,968 | 1 | 0 | 0 |
| floor | 9,016 | 1 | 0 | 0 |
| deck | 7,404 | 1 | 0 | 0 |
| pin1 | 236 | 1 | 0 | 0 |
| pin2 | 428 | 1 | 0 | 0 |
| pin3 | 620 | 1 | 0 | 0 |

[All378 pairwise rows](checks/Pairwise_Intersections.md), [CSV](checks/pairwise_intersections.csv), [acceptance JSON](checks/acceptance.json), [independent geometry/roundtrip](checks/independent_geometry.json), [datums](checks/datums.json), [source reuse](checks/source_reuse.json).

- Floor/deck vs frame, screen layers, corner standoffs, buttons, touch, leaves, DSI8+3 keep-out, all three full pin strokes, frame screw heads and driver paths: zero volume.
- Actual-rest part/dummy pairs are zero except Hue box∩deck/cradle5,171.005978 mm³. This prevents strict acceptance. Hue also blocks frame drivers2,481.502186 and M6 driver paths18,725.917361 mm³; remove Hue for service. These are reported obstructions, not access passes.
- Diagnostic self-containment is intentionally nonzero: leaves are part of plate; pins sit inside their sweeps; DSI/PCB/Pi overlap their annotation/envelope solids. Sweeps overlap undeformed flexible leaves0.900009 mm³ each, representing the intended actuation, not proven spring behavior. The broad G corridor solid overlaps part of the deck/M6 field; the **frame-only** corridor and the separate drawn route pass their stated checks. No nonzero row was suppressed.
- Delivered-mesh sections verify flush glass/plateY0,121.1×77.6 window,0.2 per-side clearance,0.3 chamfer, side lips and no top/bottom lips; nominal lip-to-metal side clearance0.9.
- Candidate3MF:7 named objects,12 mm gaps,min printZ0; **14,608 plain `<vertex>` and29,412 plain `<triangle>` tags, no `ns0`**. All triangle indices match source STLs after rigid orientation; max coordinate error<0.00000051 mm. Serialization pass does not mean acceptance.
- Each printable STL is one closed wound shell,0 bad edges,0 degenerate. Geometry-preserving collinear triangulation repair on plate/deck only. Diagnostics/reference are not printable unions and may contain multiple independent solids.
-359 protected file SHA-256 hashes unchanged. data/normal-use was not read or used.

## BOM delta vs F and G

From F, replace its old screen retention with G's frame/pins and four existing female screen corner standoffs. Use4 M2.5 frame-to-screen screws plus4 frame-to-printed-plate-pilot screws (nominal printed pilots2.1×6), rather than assuming new screen-clamp inserts. Nominal M2.5×7 through3 mm frame gives4 mm engagement; usable engagement, screw-head envelopes and pilot fit remain unverified.

Retain2 M6 inserts +2 M6×8 tray screws,4 Pi standoff insert/screw pairs,5 deck M2.5 inserts (4 long×3.5 OD nominal) +5 M2.5×7,30×30×7 fan with4 fixings, keystone/Hue cradle,8 rack fasteners. M6 pilot7.6 and tab/counterbore geometry remain F assumptions, not certification of actual insert OD/depth. Relative to G, add those F tray/device/fan items; no extra printed support part.

## Assembly order and supportless orientation — planning only

1. Under later physical direction, fit the tray/Pi/deck and M6 plate hardware. No heating, assembly test or printing now.
2. Screen from rear; frame on corner standoffs/plate bosses; fit pins atDROP0.45. Lips stay cosmetic.
3. Pi, fan and wiring on floor/deck; connect ribbon; secure deck with5 screws.
4. Hue out: slide tray onto plate tongues and fit2 M6×8. Hue goes in last. Remove Hue for M6/frame service and detach tray as needed; no all-parts-installed access claim.
5. Rack fitting uses all8 slots only when Brian directs it.

| Part | Proposed supportless orientation |
|---|---|
| Plate | Front down, G |
| Frame | Rear down, G |
| Floor/walls | Floor down, F/E |
| Hue deck | Underside down, F/E |
| Pins | Side down, G |

No captive shelf/deck was merged with the floor. Rear notches stay open-top. Tool channel roofs/bridges are≤6 mm; inherited M6 counterbores have shortØ11.5 bridges. Designed without supports; actual bridges, thin channel roofs, warping and strength UNKNOWN. No slicer/process validation.

## Reproduce and inspect

From project root: `python outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/src/SCR5-H_build_check.py` builds H only and runs the checks. `SCR5-H_finalize.py` refreshes changed diagnostics/serialization; `SCR5-H_verify_geometry.py` independently checks mesh sections and candidate roundtrip. Copied historical helpers are provenance, not entry points. OpenSCAD.exe required. The existing local `C:/Users/brian/Downloads/Swanky Rottis.stl` cradle is imported in place, never copied. Embedded licensed outputs/viewers stay local.

Local viewers: [assembly](checks/SCR5-H_assembly_viewer.html), [candidate print layout](checks/SCR5-H_print_layout_viewer.html), [ribbon](checks/SCR5-H_ribbon_viewer.html). Assembly parts remain individually inspectable at assembly coordinates; reference STL concatenates independent diagnostic meshes, never a manufacturing union. Viewer notes use those files' names/coordinates. SendUserFile is unavailable; links are supplied without upload/publishing.

Test-print ID **SCR5-H**. No print, purchase, physical test, app/data change, Final_3MF promotion, upload, commit or push. Protected historical revisions and HANDOFF.md, IDEAS.md, Dimensions.md unchanged. Fit, strength, airflow, button performance, hardware fits and actual cable behavior remain UNKNOWN.

All28 diagnostic solids, including both DSI annotations, full pin sweeps, leaves, screen heads and frame/M6 driver paths, also share one assembled reference: [viewer](checks/SCR5-H_all_checks_viewer.html). `checks/SCR5-H_all_checks_reference.stl` preserves their independent surfaces; it is not for manufacture.

Acceptance command exits2 while strict acceptance is failed;0 is reserved for a strict pass. Independent mesh/serialization verification may still exit0.

## Accepted by Brian — 2026-10-30
Brian accepted the candidate as the normal print set: `SCR5-H_screen_pi_hue_set.3mf` (copy of `checks/SCR5-H_UNVALIDATED_candidate_set.3mf`, 14,608 vertex / 29,412 triangle plain tags, no ns0). The strict-acceptance failures are the inherited SCR5-F Hue-box/cradle overlap and Hue-blocks-service-drivers items (Hue goes in last). Not printed; fit, strength, airflow and button feel UNKNOWN.

## Rev 2 — trench removed (Claude, 2026-10-30, Brian's slicer screenshot)
Codex cut 6 mm x 180 mm screwdriver channels straight back through the floor/deck from every frame screw; one nearly split the floor. Not needed: the frame is screwed on before the tray goes on (assembly order). `frame_access_clearance` is now a 6 mm x 4 mm head pocket only. Floor/deck re-rendered (closed, 0 bad edges); 3MF repacked: 14,800 vertex / 29,796 triangle plain tags, no ns0. The `checks/` intersection table predates rev 2 (driver-path rows now non-zero by design; heads still clear). Not printed.

## Rev 3 — right-wall cable windows TRIED AND REVERTED (Brian: "look terrible"); vents restored, floor = rev 2.
The 12 right-wall vent slots are now two cable-access windows (Y 47–87 and 93–133, same height as the vents, r3 ends, 6 mm centre rib). Top edges are ~40 mm horizontal bridges (printability UNKNOWN). Floor closed, 0 bad edges. DSI stays on its inside route (~111 mm): the Pi's DSI port is at the far left, so leaving through the right wall would lengthen it.

## Rev 4 — one cable slot (Claude, 2026-10-31, Brian's choice)
Right wall: one rounded 25 x 10 mm slot, low (centre 8 mm above the floor top), Y 112–142 envelope (centres 117/137). Vents behind Y 106 dropped; the 8 front vents stay. Floor closed, 0 bad edges; 3MF 14,486 vertex / 29,156 triangle plain tags, no ns0. Slot top is a short ~25 mm bridge.
