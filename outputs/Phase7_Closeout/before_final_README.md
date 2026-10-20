# Assembly Workshop — beta 0.8

> Current status — 2026-10-18: Phase 6 is closed with limitations. Phase 7 digital STL/export acceptance is in progress; printer/slicer integration is outside scope. See `../../outputs/Phase7_Digital_Acceptance/Report.md` for the resulting acceptance record. Older phase/count descriptions below are historical. Physical fit and strength remain UNKNOWN.

## Phase 7 artifact integrity

New renders use the separate `pi4-mesh-v2-triangulation1` identity namespace and include `integrity.json` with SHA-256 values for source, STLs, viewer geometry and revision report. The report binds the exact source/configuration; cache reuse and rendered downloads revalidate the files and viewer/STL correspondence. Mesh checks cover finite coordinates, nondegenerate unique triangles, two incident triangles per edge, consistent winding and positive signed volume. These bounded checks do not establish absence of self-intersections, vertex manifoldness, complete clearance, strength or physical fit.

OpenSCAD can emit an exact zero-area collinear triangle. A bounded export step removes that empty face and splits its unique long-edge neighbor at the same existing interior vertex. Coordinates, surface and orientation stay unchanged; ambiguous repairs are rejected. Both raw renderer and processed STL hashes and the repair trace are recorded in revision.json. Strict mesh checks run afterward. This is not general mesh repair.

Older immutable cache entries are preserved without modification. Entries lacking the new manifest cannot be downloaded through the new integrity-checked endpoint; explicitly generate the current configuration to create a separate v2 entry. Corrupted v2 entries are blocked rather than silently repaired or overwritten. Preserve a damaged entry and use a new data directory to regenerate the same configuration if needed.

STL coordinates follow the project's millimeter convention and remain in assembly orientation. STL does not encode a unit; retain millimeter scale when importing into other software. No printer profile or print-bed orientation is prescribed. The generated revision download is an app feature; acceptance checks inspect it in memory and do not constitute release packaging.

**Phase 5 of 7: Reference integration and bounded digital validation complete, with explicit limitations.** Five phases are complete. Whole-Pi solid conversion, containment, tool/insertion access and physical fit remain inconclusive or unknown; completion does not validate them. Phase 6 is complete with documented beta limitations: representative sourced catalog expansion. The first optional pack is documented in catalog-packs/README.md.

## Start or update

Stop the previous app with Ctrl+C. Copy all files from this release into the app folder, retaining its existing `data/` directory. Run `start.bat`, then open http://127.0.0.1:8765 and refresh the browser. On another machine use Python 3.10+ and `python app.py`.

Mesh generation uses the local OpenSCAD command-line executable. This PC has it at `C:/Program Files/OpenSCAD/openscad.exe`. Other installations can set `OPENSCAD_EXE`, or put openscad on PATH. Rendering runs without opening a desktop window. Source-only export still works if OpenSCAD is unavailable. There is no purchasing, printing, desktop control or cloud upload feature.

## Generate and compare the trial revision

1. Select Accu M3 x 8 and McMaster M3 heat-set 5.7 mm.
2. Set the installation pilot to **4.0 mm** as a trial. Retain stack 3.3, available pocket 8 and boss diameter 9 mm.
3. Click **Generate & show proposal**. The render can take about a minute. Both tray and faceplate are rendered from the exact proposed source and checked for closed mesh edges.
4. Use **Show baseline v2** and **Show generated proposal** to switch views. The canvas label identifies the displayed revision. Show the faceplate to inspect its bores; Reveal right joint intentionally hides it.
5. Click **Download matching revision package**. It includes `pi4_proposed.scad`, `tray.stl`, `faceplate.stl`, `assembly.json` and `revision.json` with pinned hardware, unresolved checks, render logs, mesh hashes and build ID.

Draft generation does not overwrite the baseline or save project selections. Save project / Save & check are explicit persistence actions. Changing an input invalidates the current build controls and returns the view to baseline. Repeating an identical build reuses its matching cache under `data/revisions/`. The bundle is tied to the build ID, not later form changes.

The current Pi4 adapter creates **four-corner faceplate mounting slots** from the supplied 1U reference and adjusts the insert-pilot parameter within 3–4.2 mm, for M3 x 0.5 hardware. Unsupported geometry changes or failed dimensional checks block generation/export. The 4 mm supplier limit is not a confirmed printed-hole recommendation. Insert outside diameter, usable thread depth and required wall guidance remain unknown in the partial catalog entries. All generated proposals remain **PROPOSED — UNVALIDATED**.

## Other implemented features

- Local SQLite hardware library, immutable revisions, atomic JSON imports and pinned project selections.
- Six sourced M3 starter records with supplier links; common M1–M8 size families show actual catalog coverage. Full catalog expansion is Phase 6.
- Live draft axial and 3D hardware envelopes. Missing insert outside diameter is represented by a labeled dashed axis, not a fabricated body.
- Read-only assembly orbit, zoom, hide/show, joint focus and baseline/proposal comparison.
- Screw reach, thread compatibility, open-insert bore envelope, pocket, hole maximum and documented wall checks; unknowns stay unknown.
- BOM and project JSON exports. The BOM quantities are fixed at two screws and two inserts for this Pi4 project.

## Validation and limits

Thirty-three automated Python tests pass. JavaScript syntax checks and mocked-canvas controls/model-switching tests pass. A real OpenSCAD integration test rendered both parts, verified mesh closure, exercised cache reuse, and checked that each packaged STL hash matches the viewer asset and the exported source is exact.

Phase 4 was exercised in a live browser. Phase 5 automated checks and isolated browser testing cover Pi visibility, view controls, validation panel and baseline/proposal labels. Desktop testing was explicitly approved. Nothing was printed.

Mesh closure and rendering do not establish interference-free assembly, strength or physical fit. The viewer includes an optional detailed Pi reference layer. The reference is excluded from manufacturing STL/assembly exports; its manifest and bounded screening report accompany new proposed revisions. Full assembly validation remains incomplete. Material, actual insert installation, tool access, rack fit and physical prototype testing remain outstanding. The simple triangle painter can show surface-order artifacts.

Hardware records use millimeters; see `hardware-records.md`. Examples are fictional and clearly labeled. CAD models for hardware are not bundled. Catalog verification status is a recorded assertion rather than independent certification. Source data and downloaded models retain their original use restrictions.

Run `python -m unittest -v test_app.py` for the automated test suite. Back up `data/` with the app stopped to preserve catalog, selections and generated revisions.


## Phase 5 local reference checks
Toggle Detailed Pi to inspect the existing aligned 122,174-triangle reference. The full reference is retained; painting it may be slow. pi_reference_manifest.json pins its SHA-256, explicit 3MF millimeter units, baked transform and baseline source hash. Unknown upstream provenance/license remains unknown; no redistributable release was packaged.

The validation panel reports live four-gusset triangle clipping after a 0.5 mm downward Pi offset, and ear/standoff convex-envelope screening. Standoff seating contact is excluded by 0.001 mm; clipping uses an inward 0.00001 mm epsilon. These are surface-intersection checks, not containment or global distance checks. A raised-gusset regression must detect the previous USB region clash.

PCB connectivity identifies the documented 6,300-vertex board component. Its bounds are [-44,13,16] to [41,69,17.600006] mm: the underside is exactly Z16. The mounting rings are inset at Z16.01001 and Z17.59001; ring height is not the underside. XY ring sampling uses nominal radius 1.35 mm and the unchanged 0.003 mm radial/center tolerance to verify the four centers and 58 x 49 mm pitch. Nominal seating and XY alignment pass without moving geometry. Printed seating remains unknown.

Joint axes are sampled from the baseline mesh bores at X +/-40, Z21 along Y. Source-based nominal side/vertical tongue clearance is 0.15 mm each, tip 0.2 mm, boss-to-ear 0.3 mm. Complete-Pi bounds establish axis separation from faceplate, socket rails and floor. Fresh OpenSCAD tray/faceplate and nominal PCB intersections pass with documented 0.001 mm contact exclusions; shifting faceplate +0.4 mm Y detects a collision. joint_validation.json binds logs to baseline SHA-256. Reproduce with Python work/validate_phase5_solids.py from repo root; this writes test geometry only in work/ and refreshes the app evidence JSON. Conversion errors/unexpected exit states remain unknown.

Whole-Pi CGAL conversion, connector/driver access, insertion path, rack/cable fit, containment and physical fit remain UNKNOWN. No dimensions or tolerance were changed. Failed assembly checks block new proposed exports; unknowns remain labeled in the report.

Saving a project adds the pinned reference manifest while preserving selections and other existing fields. New revision identity includes the assembly validation report; old immutable cache entries remain untouched. The reference mesh is served separately and never added to printable part lists.


Selected-screw checks now include a nominal head surface screen against Pi/tray/faceplate at both joint axes. The documented M3 cap head is diameter5.5 x height3 mm. A 48-sided inscribed/circumscribed cylinder bracket distinguishes definite surface intersections (FAIL), polygon-boundary ambiguity (UNKNOWN), and no screened surface intersections (PASS). Bearing contact is excluded by +0.001 mm Y; clipping epsilon is0.00001 mm. This does not establish containment, tool access or physical fit. Missing head dimensions and unsupported axes remain UNKNOWN. The 2.5 mm hex drive does not supply a driver shaft/handle envelope; no tool lengths or insertion paths are invented. These results follow the selected screw and enter its immutable build report.


## Phase 5 access disposition
The app report now lists five explicit UNKNOWN access categories with known facts, required evidence, and limits: screwdriver approach, insert installation, Pi insertion/removal, connector/cable/accessory service, and rack/physical sign-off. This completes the evidence assessment, not access validation. Unknowns remain unknown until actual tool/accessory envelopes and paths or separately approved physical results exist. The selected-project report retains the exact recorded drive and insert length. Final updated placement/joint/access rows and selected head checks were reviewed in the approved isolated browser session. No release package is authorized by this status.


## Four-corner mounting default (post-Phase5 correction)
New generated faceplates use four horizontal10x7 mm capsule slots, one per corner. The matching42 mm /1U object in Brian's Blank+Plates+Half,+1+and+2U.3mf supplies the outer-row centers; its middle row is deliberately omitted. X centers remain +/-118.2625 mm. Measured source Z centers -15.90179445 and15.90220645 map by Z+21 to5.09820555 and36.90220645 mm; vertical center pitch31.8040009 mm. Source units are millimeters; printer bed/build transforms are not feature-coordinate transforms. faceplate_mounting.json records source SHA256, XML member and measured boundary loops.

The immutable clearance-v2 baseline and prior two-slot STLs remain unchanged. The initial viewer still shows that historical baseline; Generate & show proposal displays the new four-corner revision. Previous Phase5 baseline evidence is retained with its original scope; revised rack fit, edge strength and physical fit are not validated. No printing or desktop updates are automatic. Use the newly named four-corner STL rather than the earlier two-slot faceplate for this layout.


## Phase 6 catalog expansion — in progress
The optional `catalog-packs/phase6-batch1.json` adds six sourced M2/M4/M8 records through the existing explicit JSON importer. It is not automatically loaded, and active user data is untouched. SPIROL tapered inserts remain partial records with unsupported installation fit reported UNKNOWN. See `catalog-packs/README.md` for sources, hash manifest, test coverage and remaining families. Existing M3 records, project pins and mechanical assets are unchanged.


### Phase 6 batch 2
Seven more optional records add Accu M2.5/M5/M6 screws and SPIROL Series19 straight-hole inserts at M2.5/M3/M5/M6. Sourced straight-hole tolerances now have explicit range comparison; absent tolerances retain legacy behavior. Both packs plus starter total19 records in disposable verification. See catalog-packs/phase6-batch2-README.md. Active user data, selections and mechanical geometry are unchanged.


### Phase 6 batch 3 / current progress
Seven more optional records add M1.4/M1.6/M3.5 screws and Series19 straight-hole M2/M3.5/M4/M8 inserts. Starter plus three packs totals26 records (12screws/14inserts), representing10of14 tracked screw size families and8of14 insert families. These are representative metadata records, not exhaustive or physical-fit coverage. See catalog-packs/phase6-batch3-README.md for the current progress/gap report. Active data remains unchanged.


### Phase 6 catalog workflow checkpoint
Structured diameter/pitch/length/style/material/installation filters and latest-revision search are available. Draft hardware can be compared with saved pins before explicit Save/check. The optional pack picker verifies local SHA256 and imports only on request through the atomic importer; unsaved project changes block imports. Missing/corrupt packs are unavailable. Source-gap evidence is visible. Four packs plus starter now total27 records (13screws/14inserts),11of14 screw and8of14 insert size families. M1 countersunk overall length stays unsupported for reach; no automatic replacement or geometry conversion. Scoped live UI acceptance passed in an approved isolated session (all pack imports/idempotency, numeric filters, replacement differences, unsaved-import guard and save/reload). Other filter categories and corrupt-pack behavior have automated coverage. Test with Python unittest discovery, Node test_catalog_workflow.cjs, both frontend JS syntax checks and viewer mock.


Phase 6 batch5 (2026-10-18): optional five-record source pack closes M1.2 screw and M1/M1.2/M1.4/M1.6 insert source gaps. All five packs plus starter yield32 records. See catalog-packs/phase6-batch5-README.md for conditional installation evidence, tolerance conflict and remaining M4.5/M7 gaps. Explicit import only; active data unchanged.

Phase6 batch6 (2026-10-18): optional exact M4.5/M7 screw pack. All six packs plus starter yield34 records (16screws/18inserts),14/14 screw and12/14 insert families. Remaining insert gaps M4.5/M7 stay awaiting_source. See catalog-packs/phase6-batch6-README.md for source limits and remaining acceptance. Explicit import only; active user data unchanged.

Phase6 evidence review (2026-10-18): catalog_evidence.inspect(part) audits source/missing fields offline without promoting verification. Optional installation_hole_segments is a nonempty array of {z0,z1,diameter0,diameter1,source}; mm positions must be contiguous from0, lengths/diameters positive finite, and each source nonempty. Requires kind heatset and hole_profile segmented. Equal endpoint diameters describe straight segments, unequal endpoints tapered segments, discontinuous diameters at segment boundaries describe steps. Geometry/rule support is deliberately UNKNOWN for these profiles. Custom fictional sources must remain clearly labeled. Replacement comparisons include this metadata, manufacturer_installation_evidence, source_document, field_sources, unknown_fields and rights. Offline support covers metadata only; link-only drawings/CAD require network and are not bundled. Phase6 final acceptance pending review; no physical approval.


LATEST: Phase6 COMPLETE WITH LIMITATIONS (2026-10-18). See catalog-packs/phase6-closeout.md. Batch7 explicitly imports four PEM revision2 records with visually verified catalog dimensions and shared catalog/product-page hole intervals. 34 identities/38 revisions across7packs+starter. Old pins preserved. Physical test fit late Phase7; no test started.
