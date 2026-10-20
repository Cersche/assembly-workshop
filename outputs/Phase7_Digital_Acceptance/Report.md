# Phase 7 — points 2–6 digital acceptance

Completed 2026-10-18 WITH LIMITATIONS. Phase 7 remains open; no physical test or overall physical sign-off is claimed. Printer/slicer integration is outside scope.

## Disposition by point

2. **Supported M3 hardware/rules — audit complete with explicit gaps.** Exact screw page and insert catalog row reviewed; stored trial remains7 PASS /0 FAIL /6 UNKNOWN. Thirty-four identities and38 revisions imported into fresh disposable data; reimport is idempotent and saved revision1 pins stay unchanged. Installed insert length is not usable thread depth. See Hardware_Source_Review.md and Hardware_Audit.json.
3. **STL generation/integrity — PASS within bounded digital scope.** Fresh OpenSCAD2021.01 rendering completed for the current4 mm trial. Tray10,340 triangles; faceplate1,628. Finite coordinates, nondegenerate unique triangles, closed edges, consistent winding and positive signed volume pass. Overall bounds match baseline within0.01 mm; millimeter scale and untransformed assembly coordinates are recorded. No bed orientation is prescribed. Viewer geometry matches the actual processed STLs exactly. Full self-intersection and vertex-manifold certification are not claimed.
4. **Revision/export behavior — PASS.** Exact source and configuration bind the new build ID. Cache reuse and download validate all artifact hashes and viewer/STL correspondence. Input changes create distinct identities; corrupted artifacts, stale configurations and incomplete/legacy caches block reuse/download. Renderer failure/timeouts cannot publish a partial revision. Existing cache entries remain untouched. Export inspection used the normal download pathway in memory; no release ZIP was saved.
5. **User workflow/limits — reviewed through source and automated handlers.** Real frontend handlers cover build status, units, input invalidation, stale-render completion, failure states and integrity errors. Existing viewer/catalog tests pass. UI explains STL millimeter convention, optional legacy regeneration, unvalidated physical fit and printer/slicer scope. No fresh visual desktop/browser review occurred; see Workflow_Review.md.
6. **Digital acceptance — PASS WITH LIMITATIONS.**46 Python tests passed,0 failures/errors. One preexisting mounting-specific test was deliberately excluded while that matter stays tabled. Catalog, Phase7 frontend and viewer behavioral checks pass; catalog/viewer/extracted frontend syntax pass. Seven pack manifests and three baseline/reference hashes pass. Nine actual localhost endpoints return200, including cached build and in-memory download; the acceptance server is stopped.

## Defects found and fixed

- A duplicate pair of coplanar triangles passed the former edge-count-only mesh check. New checks reject duplicate/degenerate/non-finite geometry and inconsistent winding/nonpositive signed volume.
- An assembly-only cache entry was formerly accepted without its source, STL or revision files. New integrity manifests bind artifacts, source/configuration identity and viewer geometry, and are checked before cache reuse/download.
- The real OpenSCAD tray export contains an exact collinear zero-area triangle in both ASCII and binary formats. Switching formats did not resolve it. The new narrowly bounded export step removes that empty face and splits its unique long-edge neighbor at the same existing interior vertex. It adds/moves no coordinates and preserves the same neighbor surface/winding. Ambiguous or repeated-vertex cases are rejected. Strict checks run afterward. Raw/processed hashes and each repair are recorded in revision.json; diagnostic renders are preserved under work/phase7-digital/render-diagnostics/. The new unit tests verify coordinate set, bounds, signed volume and no-op repeat behavior. Mechanical source and historical meshes were not changed.

## Compatibility and evidence

New cache namespace: pi4-mesh-v2-triangulation1. Legacy entries remain immutable. The new endpoint rejects legacy entries lacking integrity.json; explicitly generate the current configuration to create a separate new entry. No automatic migration or repinning occurs. A corrupted new entry is preserved and blocked; use a new data directory to regenerate the same configuration rather than editing/deleting the old entry.

Build ID:7c639ef2c4594d8157ef4839b23b01a9d8b8dfa09de8f5c9a0fa73795925c2db.
Source SHA-256:2d3db7e8a20e5b6a063eff6f253cf46a1b2db1ec70633e95668bd96c7825ec47.
Disposable artifact/cache path and per-STL hashes are in Digital_Integration.json. It also records the renderer version, part bounds/volumes, HTTP checks and preservation evidence. These are acceptance artifacts, not approved production files.

The protected baseline source, baseline assembly, Pi reference and both tabled mounting files retained their exact hashes. All35 files in the referenced historical build cache were hash-checked unchanged. User/active databases were not opened for acceptance; all save/import actions used new disposable data. Existing hardware revisions/pins, supplier packs and baseline/reference evidence were not rewritten. No desktop control, printing, purchase, upload, release packaging, deployment, publication or push occurred.

Windows sandbox permissions initially blocked fixture-folder renames; the approved acceptance run outside the sandbox passed. Two harness setup assertions were corrected (create the new database parent; compare Store.import_parts state instead of expecting a return count). They did not require app-data repairs. A first real render was correctly rejected by the stronger validator; the documented triangulation fix resolved it. Earlier failed runs are not counted as acceptance passes.

## What remains UNKNOWN/deferred

Exact insert OD/tolerances, usable threaded depth, generic wall recommendation, installation/process applicability and actual bottom clearance remain unresolved. Tool/Pi/cable/rack access, whole-Pi solid conversion/containment/global clearance, printed fit, strength, arbitrary geometry profiles and upstream Pi provenance/redistribution remain limited or UNKNOWN. Nominal screening is not physical approval. Mounting-layout validation stays tabled. Physical work is NOT STARTED.

Next: report back to Brian before point7. Any late-Phase7 physical work requires Brian's direction and printing needs separate approval. Point8 closeout is a separate disposition after Brian reviews these results. No additional software tests or render runs are needed unless new changes or concerns justify them.
