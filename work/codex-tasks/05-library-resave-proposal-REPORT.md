# Task 05 — outdated equipment library items: proposal only

2026-10-19. Complete as a proposal. Task 04's report was finished before this investigation began. No code changes, builds, exports or user-data reads/writes. Only this new report was written. This proposal can be delivered within the May change list; implementation described below is future work, not an action performed here.

## Observed storage and behavior (source inspection only)

`outputs/Mechanical_Design_App/equipment.py:136` library(data_dir) reads equipment-library.json as a plain array, or returns an empty array if absent. There is no library schema/template version field today. No actual library file was opened.

save_item():141 cleans the submitted spec, builds/reuses the source-addressed mesh cache, reads revision.json from its in-memory ZIP, and writes an item with fields id, name, span, spec, build, parts, status. A valid supplied eq- plus 12 hex ID REPLACES that item's array entry; otherwise a new random ID is created. A temporary JSON file replaces the index. This is not immutable item-history storage or a concurrent compare-and-swap transaction.

render():255 cleans the spec, appends geometry overrides to the complete current equipment_tray.scad text, and computes SHA-256 of that UTF-8 source as the build ID. Builds live under equipment-revisions/<hash>/. Existing folders are returned without rebuilding/revalidating; new builds render inside a temporary directory and rename it to the final folder under a process-local lock. Rendering can use per-part nudge values and normalized STL triangles. revision.json records id/spec/parts, descriptive template name, nudge_mm, per-STL SHA-256, logs, limitations and status, but no template fingerprint or render-pipeline version. equipment.scad records the unn udged base source (the word "unnudged" here means nudge=0); nonzero nudges also retain per-part SCAD files. A source hash alone does not identify the OpenSCAD version or normalization algorithm.

source():126 emits selected manufacturing fields plus numeric front-port openings. Rear ports, port types/IDs and labels are planning metadata, not geometry overrides; the equipment NAME nevertheless enters a comment in generated source and can change the current build hash. Exact source difference therefore means "not current source", not proof of a particular mechanical defect.

Current template has plate_t=4, plate_r=2.5, four rack holes per U and keystone v2 opening/collar geometry. Current clean() rejects the retired faceplate-to-tray snap joint and applies keystone collar/tray/joint clearance constraints. Device-retention clips remain a different feature. Do not silently convert retired snap specs to screw, remove keystones, alter dimensions, widen slots or repair a legacy spec.

`equipment-wizard.js:276` warns that saving an edited item updates it everywhere placed. loadLibrary():286 renders My Equipment inside the existing Equipment section; editItem():305 copies the item spec with the same ID. partsFor():319 resolves a rack allocation's equipment ID to the current library item/build, caching meshes by build ID. `rack_workspace.py:109` stores equipment identity, not an equipment build pin. This is distinct from each assembly's hardware revision/pins. Replacing an existing library item's build would change all allocations resolving that ID, including historical rack documents reopened later.

App routes: GET/POST /api/equipment-library, POST /api/equipment-preview and /api/equipment-build, GET /api/equipment-mesh/<build>/<part>. None provides outdated status or a safe create-copy rebuild contract today. Old cache folders survive item edits/deletion, but keeping those folders alone does not keep old rack views pinned to them.

## Proposed detection rule (read-only; no build on list/open)

Expose a computed template status separately from PROPOSED — UNVALIDATED and physical fit. Never rewrite old item/build metadata to make it appear current.

1. Validate item/build ID shape and locate its immutable manifest/source in the configured data directory only when this feature is implemented. Missing or malformed evidence yields "Template status unknown — build evidence unavailable"; integrity/hash disagreement yields "Build integrity problem" and blocks rebuild-from-untrusted-evidence. Never treat missing evidence as current or silently regenerate it.
2. Attempt current clean(item.spec), without rendering. A retired snap joint or a now-invalid keystone/other spec yields "Needs review before rebuild" with the specific error. Preserve the original exactly. Offer Edit a copy; require an explicit decision on any geometry changes.
3. Compute expected_current_source = source(clean(item.spec)) and expected_current_source_sha256. Validate saved base source hash against its legacy build ID (for the known legacy format), and manifest ID/part mesh hashes against their files. This is read-only evidence verification, not a mesh build. Cache status by item/build plus current template/validator/pipeline fingerprint, so listing does not repeatedly hash large meshes; stale/incomplete checks remain visible.
4. If verified saved source differs from expected current source: "Older template/source — rebuild available". It is a conservative flag, not proof that the old plate specifically has 3 mm/two holes or v1 keystones. Use explicit historical fingerprint mappings only if independently established; otherwise show "Change details unavailable". Do not diagnose a template generation from dates, names or a descriptive template string.
5. If the source matches: "Matches current source". For legacy records without pipeline provenance, append "Build process version unknown"; do not claim current-pipeline identity or validated geometry. Mesh integrity failure remains a separate blocking state. Planning-only metadata changes do not alone require a new geometry build; name-only source changes can conservatively flag a new source without claiming a mechanical difference.
6. New builds should record manifest_schema, template_sha256, normalized geometry-spec hash, source_sha256, explicit pipeline_version, OpenSCAD identity/version, per-part effective source/nudge and raw/final STL hashes. Derive the future build identity from canonical source plus declared pipeline namespace/version; retain legacy source-hash lookup unchanged. A pipeline change can require a new build even if source text matches. Do not use template version labels as physical approval.

No source-content heuristic can certify that a legacy STL actually matches its source without additional evidence. Report hash identity/integrity as bounded provenance only; unsupported fit/strength remain UNKNOWN.

## Recommended one-click rebuild flow

The safe default is **create a new library item ID**, not replacing the old item's build field. This keeps existing allocations and their old lookup identity intact without a rack schema migration. A future build-pinning migration is a separate proposal.

1. A user explicitly clicks "Rebuild as new item" for a valid, outdated item. This single click authorizes rendering and saving a COPY; no automatic render on detection, focus, load or selection. No download/export is triggered.
2. Server receives only origin item ID and expected origin build/spec fingerprint. It rereads the authoritative item and compares fingerprints; reject stale requests or missing/deleted originals. Do not trust a client-supplied template/source or arbitrary data path. Retain normal local authentication/token checks.
3. Copy the complete saved spec, including planning-only port metadata. Run current validation. If invalid, stop with a specific reason and zero item/rack changes; any user-adjusted copy is handled separately by the wizard. Keep equipment name unchanged for initial source identity calculation so a display suffix does not create a misleading geometry change.
4. Render using the current template and declared pipeline identity into a NEW immutable cache identity when source/pipeline differs. Validate all resulting files and record current provenance. Never modify an old folder, revision report, SCAD or STL. Existing corrupt target folders block the operation; do not overwrite/repair them. If an identical valid current build already exists, reuse it after verification and say so; it is a new item revision/reference, not a claim that fresh geometry was generated.
5. Under a library-index transaction/lock with generation or content-hash compare-and-swap, recheck the origin and append a NEW eq-ID, retaining every old item exactly. Record rebuilt_from_item, rebuilt_from_build and new build/provenance. A unique item display name such as "Router (current template copy)" can be separate from source-producing spec.name; decide the display-name contract before implementation.
6. Publish the new item only after build success and atomic index update. Render/validation/index/conflict failures leave original item/racks/history/pins untouched. A completed immutable build left by a failed index update is an unreferenced cache entry, not grounds for deleting anything. Use an operation token to avoid duplicate library copies on retry/double-click; do not hold a global index lock for the whole OpenSCAD render.
7. Refresh only the equipment list/status; keep unsaved workspace drafts, selection and wizard drafts. Do not silently switch placed equipment, rewrite hardware pins or change allocation span. Existing placements keep the old ID/build. The new item is available for explicit placement in an empty slot. Replacing an occupied slot would require a separate reviewed draft action and explicit atomic Save, not part of this button.
8. Success message identifies the old/new items and whether geometry was newly rendered or a verified cache reused. New build remains PROPOSED — UNVALIDATED. This feature does not touch Pi4 rendering, Print in color or normal STL artwork scope.

## UI placement and exact wording

Keep Racks & slots / Equipment / Hardware library grouping and order unchanged. Put a small status badge and action alongside each existing My Equipment item's Edit/Delete actions, inside Equipment. A compact details/action surface can carry the explanation without moving groups.

- Badge: "Older template/source"; details: "A newer equipment template is available. The saved build is unchanged. Printed fit and strength remain UNKNOWN."
- Action: "Rebuild as new item". Adjacent explanation before clicking: "Creates a new library item with the current template. Existing rack placements keep the original. No STL download."
- In progress: "Rebuilding a copy…"; disable duplicate clicks but keep unrelated draft edits available.
- Success: "Created ‘Router (current template copy)’. Existing placements are unchanged. PROPOSED — UNVALIDATED; fit and strength UNKNOWN."
- Cache reuse: "Created a new item using its verified current-template build. Existing placements are unchanged."
- Invalid legacy snap: "Needs review: the snap-fit tray joint is retired. Edit a copy and choose an allowed joint before rebuilding." Never select screw automatically.
- Missing evidence: "Template status unknown — build evidence unavailable." Offer review/details, not automatic regeneration.
- Render failure: "Rebuild failed. The original item and your rack draft are unchanged. [specific reason]"
- Stale item: "This item changed while rebuilding. Reload its library details and try again. Your rack draft is still available."

Do not call this physical validation or label the copy "fixed", "approved" or "fit checked". Do not use an "Update everywhere" action as the default.

## Proposed implementation surface (not modified)

- equipment.py: read-only status/provenance helpers, explicit create-copy rebuild operation, immutable namespace-aware manifest/cache verification and safe index concurrency. Existing save_item replacement semantics should remain distinguishable, not reused blindly.
- app.py: explicit status/rebuild endpoints (or backward-compatible enriched library response) with token, ID and stale-origin checks. Preserve current array consumers if adding metadata; do not silently change GET's schema.
- equipment-wizard.js: status/action within current Equipment list; copy-review UI for invalid old specs; preserve rack/wizard drafts on refresh and display current versus legacy evidence carefully.
- New stdlib Python and Node built-in tests; register in existing checks runner when separately authorized. No rack schema/hardware record change is necessary for the recommended create-copy default. Any later per-placement build pinning requires its own schema/history design.

## Proposed tests

1. Legacy array remains readable without mutation; absent template version is UNKNOWN, not automatically current.
2. Verified old 3 mm/two-hole source versus current source flags an update; old keystone source versus v2 flags an update; arbitrary source mismatch does not invent a specific mechanical reason.
3. Current base source matches; legacy pipeline is explicitly unknown. Future current source/pipeline and verified hashes classify current provenance without physical PASS.
4. Missing/malformed manifest/source, mismatched base-source hash/ID, missing part and tampered STL are separate diagnostics; no status endpoint renders or writes.
5. Retired snap and new keystone collar conflicts block rebuild; original spec stays byte-identical. Mount clips remain allowed and distinct. No auto-conversion or dropped ports.
6. Planning-only rear ports/types/IDs survive the copy without changing manufacturing source. Name-only source change gets conservative wording; display suffix does not masquerade as template change.
7. Valid outdated fixture creates new build namespace and new item ID; source item/build and all existing placements/history/pins remain byte-identical. New manifest records parent IDs, source/pipeline and effective nudge provenance.
8. Identical valid target build is verified/reused; corrupt target is rejected without overwrite. Pipeline change with same source selects a different immutable identity.
9. Renderer failure, timeout, mesh rejection and index write failure preserve old index/data; unreferenced successful cache is retained. Mock render boundaries for normal tests; no automatic OpenSCAD runs.
10. Double-click/retry is idempotent; concurrent rebuilds of distinct items preserve both; stale edit/delete is rejected on index commit. External writers need compare-and-swap protection beyond process-local LOCK.
11. UI button/badge stay in final Equipment grouping; no render on open/focus/list and no automatic downloads. Correct explicit-action request only, progress and failure messages, refresh retains unsaved rack/wizard edits.
12. A placed item continues to resolve its original ID/build after a new copy is created; the copy can be selected independently for a new placement. No slot resize, auto-repin or silent Save.
13. Pi4 and faceplate artwork-to-STL scope remain unchanged; local-only supplier/reference assets are never bundled by this action.

All acceptance fixtures must use new temporary directories or in-memory data, never real library files. Existing tests remain meaningful but were not run for this proposal.

## Open questions for Brian

- Approve the recommended create-copy behavior and label, so existing placements stay on their old item. Updating every placed instance is deliberately a different future decision.
- Should the display suffix be automatic, or should the copy name be editable after creation? The name currently affects source identity through a comment.
- Should source-only matches with unknown historical pipeline remain labeled "Matches current source; build process unknown", or should an explicit rebuild still be offered?
- When an old spec is invalid (retired snap or v2 collar conflict), user review is required; no substitute dimensions/joints are proposed as established fit.

No answer is required to finish this proposal. Physical fit, strength, keystone retention and color results remain UNKNOWN where not specifically evidenced. The handoff's coupon observations are specimen-specific; they do not certify the revised template.

## Commands and changed-file record

Commands actually run: targeted rg in equipment.py, equipment-wizard.js, app.py, equipment_tray.scad, assembly_records.py and rack_workspace.py; UTF-8 Get-Content ranges covering clean/source/library/save/render, library UI/cache resolution and template constants. Read CODE only; did not call library(), render(), build(), app routes or inspect any data directory. apply_patch wrote this new report.

Only work/codex-tasks/05-library-resave-proposal-REPORT.md changed; before SHA-256 absent (new). Final after hash recorded in completion tool output; excluded here to avoid self-reference. No existing file changed and no archive copy was needed. No out-of-scope edit was needed; no implementation was attempted.
