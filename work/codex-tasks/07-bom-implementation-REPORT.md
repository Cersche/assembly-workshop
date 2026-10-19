# Task 07 — chosen-stack BOM implementation

2026-10-19. Complete. End-of-task checks passed: **52 Python + 63 JS** (20 module, 27 page logic, 16 new rack BOM). No stop condition occurred. This report was completed before starting task 08.

## Changes

- Added one pure rackCounts(rack, panels=false) helper beside existing stack helpers. It validates explicitly supplied stacks, defaults missing sides only, copies effective stacks, and returns posts, extensions, optional side panels, fixed frame parts and the full-hole allowance. Invalid layouts return an error without fabricated counts. Four-post topology and three holes per post U remain.
- Rack setup creates an in-memory editing rack from the currently selected saved/draft rack. Unchanged height retains chosen stacks; changed height uses defaults; setup still clamps at 14U. BOM and preview consume that same editing rack and validated counts. Moving a support refreshes a visible matching dialog's BOM/preview.
- BOM includes fixed frame pieces and explicit "Full-hole hardware allowance; installed quantity UNKNOWN" and extension/other-fastener UNKNOWN rows. Setup preview excludes side panels, retaining fixed top/bottom panels; wording states this.
- rackFrame uses validated effective stacks. downloadRackStl obtains logical part counts directly from rackCounts, so missing preview extension meshes cannot drop required parts. Cable guides, ports and artwork are absent from logical counts. No export function was invoked.
- Registered the new Node built-in js-tests/rack-bom.js in run_checks.ps1. No server/schema/Pi4 CSV/14U limit changes.

## Worked examples: computed and asserted by tests

| Rack | Left / right | Posts | Extensions | Bolt / insert allowance | Side panels enabled |
| --- | --- | --- | --- | --- | --- |
| 5U default | [5] / [5] | 4 x 5U | 0 | 60 / 60 | 2 x 5U |
| 5U chosen | [1,3] / [5] | 2 x 1U, 2 x 3U, 2 x 5U | 1 | 54 / 54 | 1 each 1U, 3U, 5U |
| 9U default | [3,5] / [3,5] | 4 x 3U, 4 x 5U | 2 | 96 / 96 | 2 x 3U, 2 x 5U |
| 9U chosen | [3,5] / [4,4] | 2 x 3U, 4 x 4U, 2 x 5U | 2 | 96 / 96 | 1 x 3U, 2 x 4U, 1 x 5U |
| 14U default | [2,5,5] / [2,5,5] | 4 x 2U, 8 x 5U | 4 | 144 / 144 | 2 x 2U, 4 x 5U |
| 14U chosen | [2,5,5] / [4,4,4] | 2 x 2U, 6 x 4U, 4 x 5U | 4 | 144 / 144 | 1 x 2U, 3 x 4U, 2 x 5U |

Every example also has 2 bottom beams, 1 top-front beam, 1 top-rear beam, 4 side rails, 1 top panel, 1 bottom panel, 4 feet and 2 handles. Side panels off removes segmented side panels only. Extension/frame fastener installed quantities and physical fit/strength remain UNKNOWN.

## Verification and limits

The 16 new tests cover all six examples, missing-side defaults and 1U, invalid stacks/heights, lock independence, panels, exclusion of cabling/artwork, actual rackFrame agreement for all examples with both panel modes, missing extension preview asset, dialog height retention/defaults/clamp/no mutation, displayed UNKNOWN wording/error, and visible BOM refresh on a move. Real workspace closures run in Node VM with synthetic data/asset stubs. Existing page/startup tests also pass. No browser/visual acceptance claimed.

Commands actually run:
- UTF-8 Get-Content read required project/standing/task docs and the approved task-04 report; targeted workspace/runner/test ranges.
- Python 3.10 stdlib Path/hashlib/json archived exact original workspace.js and run_checks.ps1 bytes to docs/archive/codex/2026-10-19/task07/ with repository-relative subpaths.
- Python text replacements modified only the permitted source and runner; apply_patch added the new test file. No imports of app/server code or user data.
- `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1`: run once, exit 0. Full output below.
- Python SHA-256 calculation produced the table below; report written with apply_patch.

## Files changed and hashes

| File | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| outputs/Mechanical_Design_App/workspace.js | 85a24e39dbf3b9daa01fd458af808af107fcf617dffce2870142508de29f76bc | b5513013801fa7c1e4e7af4602b1c4c5562ae88c39f3f97989339f7bf81f8cd9 |
| outputs/Mechanical_Design_App/run_checks.ps1 | f8952eca8d02db07d9efaf97577e864a219d843bcdad82255dfdfbcbe6d284e3 | d7912968f77499d76ffb78abad9defffdd8f191b801c3eb05764b33945077e08 |
| outputs/Mechanical_Design_App/js-tests/rack-bom.js | absent (new) | 9b2cab4adffa60021e38acfbcf86d5de976c8d5a15a066c16da3774901e90c9c |

New report work/codex-tasks/07-bom-implementation-REPORT.md: before absent; after hash recorded in completion tool output (self-hash excluded). No other existing files changed in this task. Archive copies are the original bytes, not rewritten text.

## Assumptions and open questions

Brian's four-post and full-hole allowance decisions are implemented. The setup preview has always excluded optional side panels, so that remains explicit; panel-enabled counts are available for rack-part downloads and tested without exporting. Existing chip behavior changes height rather than selecting arbitrary segments; it is preserved. No open question blocks completion. No data/normal-use or other user data was read/written, no live 8765 interaction or desktop session, no build/export/print/delete/commit/push.

## Complete end-of-task output

```text
== Python (work/gui-refinement/check_python.py) ==
test_assignment_retains_unknown_fit (test_rack_workspace.RackWorkspaceTests) ... ok
test_cable_guides_round_trip_and_reject_invalid (test_rack_workspace.RackWorkspaceTests) ... ok
test_empty_read_has_no_side_effect (test_rack_workspace.RackWorkspaceTests) ... ok
test_history_lists_and_restores_draft_without_writing (test_rack_workspace.RackWorkspaceTests) ... ok
test_invalid_dimensions_and_equipment (test_rack_workspace.RackWorkspaceTests) ... ok
test_malformed_history_generation_cannot_be_used_as_path (test_rack_workspace.RackWorkspaceTests) ... ok
test_overlap_and_out_of_range_rejected (test_rack_workspace.RackWorkspaceTests) ... ok
test_round_trip_unknown_dimensions_and_historical_recovery (test_rack_workspace.RackWorkspaceTests) ... ok
test_stale_writer_rejected_without_changes (test_rack_workspace.RackWorkspaceTests) ... ok
test_every_component_retains_exact_source_coordinates_and_indices (test_rack_references.RackReferenceTests) ... ok
test_reference_route_never_accesses_hardware_store (test_rack_references.RackReferenceTests) ... ok
test_tampering_is_rejected_and_unknown_paths_are_not_served (test_rack_references.RackReferenceTests) ... ok
test_appearance_does_not_change_hardware_identity (test_assembly_records.AssemblyRecordTests) ... ok
test_artwork_allows_1024_pixels_and_auto_filament_colors (test_assembly_records.AssemblyRecordTests) ... ok
test_artwork_is_local_verified_png_and_tamper_is_blocked (test_assembly_records.AssemblyRecordTests) ... ok
test_layout_cannot_overwrite_hardware_and_old_client_is_rejected (test_assembly_records.AssemblyRecordTests) ... ok
test_old_shared_editor_cannot_mutate_independent_workspace (test_assembly_records.AssemblyRecordTests) ... ok
test_routes_scope_state_save_bom_and_check_to_instance (test_assembly_records.AssemblyRecordTests) ... ok
test_saved_release_undo_retains_latest_hardware_revision (test_assembly_records.AssemblyRecordTests) ... ok
test_stale_save_rejected_and_noop_does_not_bump_revision (test_assembly_records.AssemblyRecordTests) ... ok
test_two_instances_are_isolated_and_legacy_db_is_unchanged (test_assembly_records.AssemblyRecordTests) ... ok
test_v1_read_migrates_only_in_memory (test_assembly_records.AssemblyRecordTests) ... ok
test_wrong_or_stale_instance_bundle_is_rejected_without_render (test_assembly_records.AssemblyRecordTests) ... ok
test_appearance_only_preserves_hardware_revision (test_studio_save.StudioSaveTests) ... ok
test_atomic_save_route_and_capability (test_studio_save.StudioSaveTests) ... ok
test_combined_save_is_one_workspace_commit (test_studio_save.StudioSaveTests) ... ok
test_invalid_hardware_leaves_layout_and_appearance_unsaved (test_studio_save.StudioSaveTests) ... ok
test_stale_generation_is_rejected_without_partial_save (test_studio_save.StudioSaveTests) ... ok
test_unscoped_hardware_tampering_is_rejected (test_studio_save.StudioSaveTests) ... ok
test_port_edits_rejected (test_cable_ports.CablePortTests) ... ok
test_port_edits_round_trip (test_cable_ports.CablePortTests) ... ok
test_rejections (test_cable_ports.WizardPortTests) ... ok
test_source_ignores_planning_fields (test_cable_ports.WizardPortTests) ... ok
test_type_ids_and_rear_ports (test_cable_ports.WizardPortTests) ... ok
test_auto_colors_stay_automatic (test_faceplate_color.FaceplateColorTests) ... ok
test_color_only_change_changes_export_identity (test_faceplate_color.FaceplateColorTests) ... ok
test_opaque_image_keeps_faceplate_as_base (test_faceplate_color.FaceplateColorTests) ... ok
test_png_round_trip_with_filters (test_faceplate_color.FaceplateColorTests) ... ok
test_preview_reduces_and_cleans (test_faceplate_color.FaceplateColorTests) ... ok
test_same_filament_merges_bodies (test_faceplate_color.FaceplateColorTests) ... ok
test_settings_validation (test_faceplate_color.FaceplateColorTests) ... ok
test_assembly_assets_preserve_design_coordinates (test_app.Tests) ... ok
test_atomic_immutable_import_and_pinning (test_app.Tests) ... ok
test_axial_geometry_and_open_insert_overrun (test_app.Tests) ... ok
test_draft_preview_never_changes_saved_project (test_app.Tests) ... ok
test_hardware_envelopes_follow_actual_joint_axes (test_app.Tests) ... ok
test_invalid_dimensions (test_app.Tests) ... ok
test_maximum_hole_is_not_exact_recommendation (test_app.Tests) ... ok
test_mesh_validation_and_bundle_path_rejection (test_app.Tests) ... ok
test_reach_bottoming_and_unknowns (test_app.Tests) ... ok
test_starter_catalog_is_idempotent_and_keeps_selection (test_app.Tests) ... ok
test_thread_mismatch_and_missing_selection (test_app.Tests) ... ok

----------------------------------------------------------------------
Ran 52 tests in 5.222s

OK
== JavaScript (js-tests/run.js) ==
✔ every app script parses (35.9609ms)
✔ every script index.html loads from /rack-references/ is in the asset manifest (1.6038ms)
✔ RackLayout.checkRange rejects out-of-range and overlapping ranges (0.5844ms)
✔ RackLayout.change moves an allocation and resets fit to UNKNOWN (0.2176ms)
✔ RackLayout.release and restore round-trip; restore keeps fit UNKNOWN (0.8065ms)
✔ WorkshopCatalog.filter: latest revision, kind, exact diameter, unknown material, length bounds (0.3936ms)
✔ WorkshopCatalog.changes lists changed fields with their effect (0.279ms)
✔ LabRaxScene.frame stacks posts in levels of at most 5U that sum to the rack height (0.7886ms)
✔ LabRaxScene.guidePose puts the cable guide plate flat on the post face at the slot hole pair (3.5017ms)
✔ WorkshopClearance.screen grades height, width and depth against nominal rack numbers (0.5364ms)
✔ WorkshopClearance.screen keeps unspecified rack numbers UNKNOWN and flags span mismatch (0.2311ms)
✔ LabRaxStudio.artworkRect stays inside the 216 x 34 mm faceplate field (0.2458ms)
✔ LabRaxStudio.artworkWindow generalizes the Pi4 window to wizard faceplates of any U span (0.6935ms)
✔ LabRaxStudio.artworkRect keeps wizard images clear of port and keystone openings (3.069ms)
✔ LabRaxStudio.selectionRect follows the plate front at any U height (0.2638ms)
✔ LabRaxPorts Pi 4 preset: nine ports, face UNKNOWN, front-edge ports point front and USB/Ethernet right (0.3895ms)
✔ LabRaxPorts wizard ports: front openings, rear ports and keystone pass-through pairs (0.35ms)
✔ LabRaxPorts overrides merge, reset, custom ports and prune (0.6682ms)
✔ LabRaxPorts marker rotations are proper rotations and parts sit at the allocation base (0.4225ms)
✔ LabRaxPorts marker meshes exist for every connector type (5.3938ms)
ℹ tests 20
ℹ suites 0
ℹ pass 20
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 72.8773
== JavaScript page logic (js-tests/page-logic.js) ==
✔ page Save: layout/hardware dirty status enables Save without persistence (2.6775ms)
✔ page Save: one atomic request commits layout, appearance and hardware then clears dirty state (1.5888ms)
✔ page Save: rejected request keeps draft and hardware, reports error and permits retry (0.8235ms)
✔ page Save: edits during in-flight Save remain dirty and double Save is rejected (0.9601ms)
✔ page Save: precondition capable=false blocks writes (0.6054ms)
✔ page Save: precondition openingAssembly=true blocks writes (0.5664ms)
✔ page Save: precondition artworkPending=1 blocks writes (1.1402ms)
✔ page Save: precondition byId("mountWizard").hidden=false blocks writes (0.7762ms)
✔ page Save: precondition byId("rackDialog").open=true blocks writes (0.7497ms)
✔ page check: dirty guard blocks action without silently saving (3.108ms)
✔ page bom: dirty guard blocks action without silently saving (1.402ms)
✔ page project: dirty guard blocks action without silently saving (1.4161ms)
✔ page designExport: dirty guard blocks action without silently saving (1.4548ms)
✔ page buildRevision: dirty guard blocks action without silently saving (1.6358ms)
✔ page checks and BOM: clean actions use saved state without issuing Save (1.896ms)
✔ viewer startup: actual script loads, binds events and paints its first frame (17.2131ms)
✔ viewer startup: missing reports error without drawing or unhandled rejection (1.0778ms)
✔ viewer startup: network reports error without drawing or unhandled rejection (0.8111ms)
✔ viewer startup: bad-json reports error without drawing or unhandled rejection (0.7399ms)
✔ viewer startup: no-canvas reports error without drawing or unhandled rejection (0.7541ms)
✔ viewer startup: missing optional Pi reference still renders assembly (1.9093ms)
✔ viewer startup: failed studio renderer falls back with a visible reason (2.3652ms)
✔ rack viewer startup: required and optional meshes load then schedule both views (3.177ms)
✔ rack viewer startup: optional-404 keeps required meshes usable (0.8625ms)
✔ rack viewer startup: optional-network keeps required meshes usable (0.7404ms)
✔ rack viewer startup: required failure retains diagnostic (0.7753ms)
✔ rack viewer startup: renderer failure retains diagnostic (0.6951ms)
ℹ tests 27
ℹ suites 0
ℹ pass 27
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 57.4191
== JavaScript rack BOM (js-tests/rack-bom.js) ==
✔ rack BOM worked example: 5U default (4.6473ms)
✔ rack BOM worked example: 5U custom (0.7813ms)
✔ rack BOM worked example: 9U default (0.7185ms)
✔ rack BOM worked example: 9U custom (0.7474ms)
✔ rack BOM worked example: 14U default (0.7071ms)
✔ rack BOM worked example: 14U custom (0.6705ms)
✔ rack BOM missing side defaults only the missing stack; 1U has no joints (0.7591ms)
✔ rack BOM rejects explicitly invalid stacks and heights without fabricated parts (0.9123ms)
✔ rack BOM locked and unlocked stacks count identically (0.9278ms)
✔ rack BOM side panels toggle only segmented panels, never top/bottom (1.1481ms)
✔ rack BOM ignores cable guides, ports and artwork (0.887ms)
✔ rack BOM agrees with real rackFrame source placements and all fixed parts (2.5374ms)
✔ rack BOM requires extensions independently of missing preview assets (1.4383ms)
✔ rack setup height edits retain chosen saved stacks only at unchanged height, clamp at 14U and do not mutate (1.3787ms)
✔ rack BOM shows explicit allowances/UNKNOWNs and invalid layout error (0.7399ms)
✔ moving a support refreshes a visible editing BOM; locked layout stays unchanged (0.919ms)
ℹ tests 16
ℹ suites 0
ℹ pass 16
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 26.7472
RESULT: all checks passed

```

