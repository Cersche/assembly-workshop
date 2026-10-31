# Task52 — SCR5-H report — 2026-10-30

**Built as a draft; strict acceptance FAILED.** Seven draft STLs, copied/adapted sources, all acceptance evidence, README/BOM/assembly order and local3D viewers are in `outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/`. Failed checks block the normal `SCR5-H_screen_pi_hue_set.3mf` export. A clearly marked seven-part diagnostic candidate is retained only at `checks/SCR5-H_UNVALIDATED_candidate_set.3mf`.

The unresolved conflict is F's conservative Hue box versus its retained cradle: **5,171.005978 mm³**, the same overlap documented in F. Actual device fit is UNKNOWN. Preserving the requested cradle and claiming all assembled physical pairs are zero would be false. No rounded Hue shape was invented. Hue also blocks frame drivers2,481.502186 mm³ and M6 driver paths18,725.917361 mm³; remove Hue for service. These obstructions remain reported. Further device-envelope/design decisions are required before strict acceptance.

## Implemented

G flush front/window/chamfer/side lips/rack slots/pin channels retained; glassX33/Z41.5. Frame changed only for required H rear ID. All pin modules and canonical triangle sets match G, DROP0.45/full stroke1.4. F tray definitions copied unchanged except IDs; new wrapper registers tray+4Y to plate rearY4. Pi-zone front0→4, rear-zone front36→40, rear148→152; no further whole-edge setback. Retain R6 corners, Pi standoffs, fan/vents, Hue cradle,5 wall-top insert bosses, rear open-top notches, M6 tabs. Added localØ6 lower frame-driver channels through floor; it remains one shell. Deck subtraction removes no material. Retained both USB openings, Ethernet and golden keystone, all clear of G screen/frame/pins; corrected golden face0.08 proud offset toY0. IDs are on plate rear/frame rear/floor top/deck underside mirrored.

Screen values use unchanged Dimensions.md: measured DSIW5.0 and centred PCB confirmed, G8 mm+3 clearance preserved. Stack9.1 vs13.3 caliper rear seat is explicit:4 mm nominal standoffs sum to13.1; G conservative4.2 dummy is not a new measurement. Inner screen standoff registration is unmeasured. Physical lit registration stays UNKNOWN because borders are drawing estimates±0.5; model vertical centre is44.4, error0. Screen intentionally remains atX+33.

## Acceptance observations

| Part | Triangles | Shells | Bad edges | Degenerate |
|---|---:|---:|---:|---:|
| plate | 7,740 | 1 | 0 | 0 |
| frame | 3,968 | 1 | 0 | 0 |
| floor | 9,016 | 1 | 0 | 0 |
| deck | 7,404 | 1 | 0 | 0 |
| pin1 | 236 | 1 | 0 | 0 |
| pin2 | 428 | 1 | 0 | 0 |
| pin3 | 620 | 1 | 0 | 0 |

| Check | Result |
|---|---|
| Closed wound shell/0 bad edges/0 degenerate | PASS all7; geometry-preserving collinear repair plate/deck |
| Floor/deck vs screen/frame/leaves/DSI8+3 keep-out | PASS zero volume |
| Floor/deck vs full pin strokes, frame heads and drivers | PASS zero volume after local channels |
| Complete pairwise table | RUN378 rows; strict physical-envelope all-zero FAILS retained cradle/Hue box |
| Glass/plate front | PASS Y0 mesh |
| Lit centre within0.1 | Vertical model error0; physical registration UNKNOWN; intentional X+33 |
| Window/lips | PASS independent sections:121.1×77.6,0.2 clearance,0.3 chamfer,left/right only,no top/bottom,0.9 nominal metal clearance |
| Frame18 mm corridor | PASS zero frame intersection |
| Ribbon route |96.1311+15 allowance=111.1311 mm<140;48.8689 estimated160-cable slack; centreline vs floor/deck zero |
| Candidate3MF |7 objects,12 mm gaps,minZ0,STL triangle indices preserved,max coordinate error<0.00000051 |
| Plain vertex/triangle tags; no ns0 | PASS14,608 /29,412; no ns0 |
| Protected inputs | PASS359 file hashes unchanged; normal-use never read/used |

No nonzero diagnostic row is hidden: pins are contained in their sweeps; leaves are already in the plate; source solids overlap their annotation/keep-out volumes. Each sweep overlaps its undeformed leaf0.900009 mm³ for intended actuation, not a validated spring or a rigid zero-contact pass. The broad G corridor overlaps some deck/M6 material; only its **frame** clearance and the separately drawn route are zero. The route is a1 mm diameter centreline, not a verified flat-ribbon envelope. Screen endpoint uses the measured connector span; Pi DSI endpoint/dummy remains approximate F-layout metadata. Endpoint/Pi overlaps are visible. Bend/twist/reach, fastener envelopes and inner screen standoff positions limit the assembly dummy's completeness.

Supportless design follows G/F/E orientations: plate front down; frame rear down; floor down; deck underside down; pins side down. No trapped shelf/deck. New tool roofs≤6 mm and inheritedØ11.5 M6 bridges remain physically unverified. Do not infer print performance, fit, strength or airflow from mesh closure.

## Evidence

- [README: decisions, BOM delta, assembly, orientation and limits](../../outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/README.md)
- [Full378-pair table](../../outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/checks/Pairwise_Intersections.md), [CSV](../../outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/checks/pairwise_intersections.csv), [acceptance JSON](../../outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/checks/acceptance.json)
- [Independent sections/3MF roundtrip](../../outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/checks/independent_geometry.json), [measured/model datums](../../outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/checks/datums.json), [source reuse](../../outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/checks/source_reuse.json)
- [Assembly viewer](../../outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/checks/SCR5-H_assembly_viewer.html), [candidate print-layout viewer](../../outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/checks/SCR5-H_print_layout_viewer.html), [ribbon viewer](../../outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/checks/SCR5-H_ribbon_viewer.html)

Run `python outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/src/SCR5-H_build_check.py` from project root. Finalizer and independent verifier are in the same src folder. Copied older helpers are provenance, not entry points. All build outputs remain under H; the only outside output is this expressly requested report. Assembly reference preserves independent diagnostic meshes and is not a printable union. Viewers embed the local licensed cradle: no uploads/redistribution. SendUserFile is unavailable, so local links replace delivery through that tool.

No printing, purchase, physical test, app/data operation, Final_3MF copy, upload, commit or push. HANDOFF.md, Dimensions.md, IDEAS.md and protected historical revisions unchanged. Initial standard-sandbox git pull failed with a work-tree/access error; no pull/merge was forced against protected files. D: writes required approved filesystem escalation because configured writable roots still name C:. No desktop-control session started. **Fit, strength, airflow, button behavior, actual ribbon reach and hardware engagement UNKNOWN.**

All28 diagnostic solids, including both DSI annotations, full pin sweeps, leaves, screen heads and frame/M6 driver paths, also share one assembled reference: [viewer](../../outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/checks/SCR5-H_all_checks_viewer.html). `checks/SCR5-H_all_checks_reference.stl` preserves their independent surfaces; it is not for manufacture.

Acceptance command exits2 while strict acceptance is failed;0 is reserved for a strict pass. Independent mesh/serialization verification may still exit0.
