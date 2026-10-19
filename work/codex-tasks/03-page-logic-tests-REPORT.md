# Task 03 — automated page-logic tests

Date: 2026-10-19. Complete. Task 01 passed; task 02's report was finished before task 03 began.

## Result

Before: 52 Python + 20 JS passed, exit 0.
After: 52 Python + 20 existing JS + 27 new page-logic JS passed, exit 0.
No failing, skipped, cancelled or known-failure tests in the final run. No app-source fixes.

## Files changed and SHA-256

| File | Before | After |
| --- | --- | --- |
| outputs/Mechanical_Design_App/run_checks.ps1 | 9bf819beb6d14edb7351d8f304685ef41e582153db115e6a7cf2fc73bda0d3a1 | f8952eca8d02db07d9efaf97577e864a219d843bcdad82255dfdfbcbe6d284e3 |
| outputs/Mechanical_Design_App/js-tests/page-logic.js | absent (new) | c9132668e178221c013c0de9dabc8609c1593092d6619ad8c2d3387e083ada2d |

Runner's byte-for-byte original: docs/archive/codex/2026-10-19/task03/run_checks.ps1 (Before hash above). The runner now executes the new file using the same Node built-ins/spec reporter and failure aggregation as its existing JS file. Existing js-tests/run.js is unchanged.

This new report: before absent; its final after SHA-256 appears in the completion output, excluded here to avoid self-reference.

Completion hashes for preceding reports (their final bytes were not edited during subsequent tasks):
- 01-run-checks-baseline-REPORT.md: 141d0fe506b3108c05d569141be749c78d1d971b51547386ede563dbdc2b38ba
- 02-readme-refresh-REPORT.md: cf89fde2b8ecc44522e3c2387a04683526dd129affdf97ca6e486ed171182dfa

## Every new test and coverage

1. Save dirty status: layout/hardware changes enable Save and block guarded actions without writing.
2. Atomic Save success: exactly one studio-save request includes layout, appearance and hardware; response updates generation/pins and clears dirty state.
3. Save rejection: draft/hardware/revision remain, error is reported, busy state clears and retry stays available.
4. In-flight Save: duplicate Save and exports are blocked; newer layout/hardware edits survive completion as unsaved drafts.
5. Capability guard: incompatible server prevents Save.
6. Assembly-opening guard: pending selection prevents Save.
7. Artwork guard: pending image preparation prevents Save.
8. Allocation editor guard: open wizard prevents Save.
9. Rack editor guard: open dialog prevents Save.
10. Check handler: dirty workspace blocks checking without Save or API request.
11. BOM handler: dirty workspace blocks export without Save or fetch.
12. Project handler: dirty workspace blocks export without Save or fetch.
13. Design export handler: dirty workspace blocks export without Save or fetch.
14. Build handler: dirty workspace blocks build without Save or API request.
15. Clean check/BOM: actual handlers check/export the saved assembly without issuing Save; BOM URL preserves assembly identity.
16. Assembly viewer startup: actual viewer script fetches fixtures, binds controls/events and paints its first frame with the software renderer.
17. Missing assembly asset: non-OK response yields visible diagnostic and no frame.
18. Assembly network failure: rejection becomes visible diagnostic, no frame.
19. Invalid assembly JSON: parsing failure becomes visible diagnostic, no frame.
20. Missing canvas context: visible diagnostic, no asset request.
21. Optional Pi reference absent: assembly still paints.
22. Studio renderer construction failure: software fallback paints with visible reason.
23. Rack viewer boot: required/optional meshes populate state and schedule rack/setup preview.
24. Optional rack assets return 404: required mesh remains usable and both previews schedule.
25. Optional rack assets reject: required mesh remains usable and both previews schedule.
26. Required rack asset loader rejects: diagnostic retained, initial rack redraw scheduled, setup preview withheld.
27. Rack renderer construction fails: diagnostic retained and mesh state stays unavailable.

## Method and limits

Node test/assert/fs/path/vm built-ins only. Tests read source, never user data, and use synthetic in-memory racks, hardware, mesh triangles, DOM/canvas, API and fetch fixtures. No real exports, servers, geometry builds, desktop sessions, installs or network requests.

Save/status and rack-startup closures are extracted verbatim from workspace.js with unique checked anchors. This avoids editing production code or duplicating controller logic. It does not execute the entire workspace DOM reconstruction. Inline index handlers execute with only their unrelated automatic refresh disabled, following the existing VM-test pattern. The installed real Save guard is shared with these handlers. The whole viewer.js executes; its final startup call is assigned to a test-only promise so failures are awaited. The first software frame executes the actual rasterizer on a synthetic triangle. Rack loader/renderer boundaries are mocked; real WebGL output, HTTP serving, real catalog loading, complete DOM integration and visual quality remain outside this coverage. Existing JS checks separately cover asset-manifest registration.

Atomic backend persistence is covered by the existing Python tests; these new tests verify frontend request/state behavior with mocked responses. No broad claim about every export route is made: guarded check/BOM/project/design/build handlers are covered. Artwork export, rack export and existing rendered-bundle download are not individually covered here. Physical fit/strength remain UNKNOWN.

## Commands actually run

- UTF-8 Get-Content and targeted rg reads of js-tests/run.js, workspace.js, viewer.js, index.html, rack-reference assembly-studio.js/rack-studio.js/rack-scene.js and the existing frontend VM test; targeted filename inventory. Two initial guessed root-level renderer paths did not exist; corrected to rack-references. No whole-repository scan.
- powershell -ExecutionPolicy Bypass -File outputs/Mechanical_Design_App/run_checks.ps1 before modification: exit 0 (full output below). This is a process-scoped policy setting, not a persistent policy change.
- apply_patch created/adjusted the new JS test file.
- Python 3.10 stdlib archived runner bytes before editing, registered page-logic.js and calculated final hashes. Archive/current documentation presence, startup and UNKNOWN assertions passed.
- Node from the bundled Codex runtime, --test-reporter=spec outputs/Mechanical_Design_App/js-tests/page-logic.js: initial exit 1, 26 passed / 1 fixture-expectation failure. Actual BOM URL was /api/bom?assembly=assembly; test incorrectly expected /api/bom. Corrected the expectation to preserve required per-instance scope. No app bug or app-source change.
- powershell -ExecutionPolicy Bypass -File outputs/Mechanical_Design_App/run_checks.ps1 after correction: exit 0 (full output below).
- Generated this UTF-8 report and computed its hash after writing.

## Assumptions and open questions

Source extraction deliberately fails if anchors change rather than silently running stale copied logic. Mocked DOM/API boundaries are sufficient for these bounded controller/startup checks, not browser acceptance. No production bug was exposed by the final tests; no known failures to mark. Normal server was not stopped, restarted or contacted. No user-data path was read or written. Additional full-page/browser and real WebGL integration coverage would be separate work.

## Before — complete output

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
Ran 52 tests in 5.224s

OK
== JavaScript (js-tests/run.js) ==
✔ every app script parses (9.2207ms)
✔ every script index.html loads from /rack-references/ is in the asset manifest (1.4802ms)
✔ RackLayout.checkRange rejects out-of-range and overlapping ranges (0.5729ms)
✔ RackLayout.change moves an allocation and resets fit to UNKNOWN (0.2012ms)
✔ RackLayout.release and restore round-trip; restore keeps fit UNKNOWN (0.7768ms)
✔ WorkshopCatalog.filter: latest revision, kind, exact diameter, unknown material, length bounds (0.3904ms)
✔ WorkshopCatalog.changes lists changed fields with their effect (0.2789ms)
✔ LabRaxScene.frame stacks posts in levels of at most 5U that sum to the rack height (0.5473ms)
✔ LabRaxScene.guidePose puts the cable guide plate flat on the post face at the slot hole pair (2.6693ms)
✔ WorkshopClearance.screen grades height, width and depth against nominal rack numbers (0.66ms)
✔ WorkshopClearance.screen keeps unspecified rack numbers UNKNOWN and flags span mismatch (0.1817ms)
✔ LabRaxStudio.artworkRect stays inside the 216 x 34 mm faceplate field (0.256ms)
✔ LabRaxStudio.artworkWindow generalizes the Pi4 window to wizard faceplates of any U span (0.5366ms)
✔ LabRaxStudio.artworkRect keeps wizard images clear of port and keystone openings (2.4822ms)
✔ LabRaxStudio.selectionRect follows the plate front at any U height (0.2258ms)
✔ LabRaxPorts Pi 4 preset: nine ports, face UNKNOWN, front-edge ports point front and USB/Ethernet right (0.4829ms)
✔ LabRaxPorts wizard ports: front openings, rear ports and keystone pass-through pairs (0.3754ms)
✔ LabRaxPorts overrides merge, reset, custom ports and prune (0.6169ms)
✔ LabRaxPorts marker rotations are proper rotations and parts sit at the allocation base (0.3936ms)
✔ LabRaxPorts marker meshes exist for every connector type (5.7105ms)
ℹ tests 20
ℹ suites 0
ℹ pass 20
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 41.9017
RESULT: all checks passed

```

## After — complete output

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
Ran 52 tests in 5.102s

OK
== JavaScript (js-tests/run.js) ==
✔ every app script parses (8.869ms)
✔ every script index.html loads from /rack-references/ is in the asset manifest (1.1962ms)
✔ RackLayout.checkRange rejects out-of-range and overlapping ranges (0.4881ms)
✔ RackLayout.change moves an allocation and resets fit to UNKNOWN (0.2042ms)
✔ RackLayout.release and restore round-trip; restore keeps fit UNKNOWN (0.7379ms)
✔ WorkshopCatalog.filter: latest revision, kind, exact diameter, unknown material, length bounds (0.3647ms)
✔ WorkshopCatalog.changes lists changed fields with their effect (0.2626ms)
✔ LabRaxScene.frame stacks posts in levels of at most 5U that sum to the rack height (0.545ms)
✔ LabRaxScene.guidePose puts the cable guide plate flat on the post face at the slot hole pair (2.5864ms)
✔ WorkshopClearance.screen grades height, width and depth against nominal rack numbers (0.7264ms)
✔ WorkshopClearance.screen keeps unspecified rack numbers UNKNOWN and flags span mismatch (0.1852ms)
✔ LabRaxStudio.artworkRect stays inside the 216 x 34 mm faceplate field (0.2522ms)
✔ LabRaxStudio.artworkWindow generalizes the Pi4 window to wizard faceplates of any U span (0.4361ms)
✔ LabRaxStudio.artworkRect keeps wizard images clear of port and keystone openings (2.4402ms)
✔ LabRaxStudio.selectionRect follows the plate front at any U height (0.2116ms)
✔ LabRaxPorts Pi 4 preset: nine ports, face UNKNOWN, front-edge ports point front and USB/Ethernet right (0.3917ms)
✔ LabRaxPorts wizard ports: front openings, rear ports and keystone pass-through pairs (0.3309ms)
✔ LabRaxPorts overrides merge, reset, custom ports and prune (0.6225ms)
✔ LabRaxPorts marker rotations are proper rotations and parts sit at the allocation base (0.3865ms)
✔ LabRaxPorts marker meshes exist for every connector type (5.2011ms)
ℹ tests 20
ℹ suites 0
ℹ pass 20
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 39.1159
== JavaScript page logic (js-tests/page-logic.js) ==
✔ page Save: layout/hardware dirty status enables Save without persistence (2.5071ms)
✔ page Save: one atomic request commits layout, appearance and hardware then clears dirty state (1.5276ms)
✔ page Save: rejected request keeps draft and hardware, reports error and permits retry (0.8064ms)
✔ page Save: edits during in-flight Save remain dirty and double Save is rejected (1.0534ms)
✔ page Save: precondition capable=false blocks writes (0.5883ms)
✔ page Save: precondition openingAssembly=true blocks writes (0.5511ms)
✔ page Save: precondition artworkPending=1 blocks writes (0.5702ms)
✔ page Save: precondition byId("mountWizard").hidden=false blocks writes (0.7346ms)
✔ page Save: precondition byId("rackDialog").open=true blocks writes (0.7866ms)
✔ page check: dirty guard blocks action without silently saving (3.7138ms)
✔ page bom: dirty guard blocks action without silently saving (1.853ms)
✔ page project: dirty guard blocks action without silently saving (1.557ms)
✔ page designExport: dirty guard blocks action without silently saving (1.4651ms)
✔ page buildRevision: dirty guard blocks action without silently saving (1.4877ms)
✔ page checks and BOM: clean actions use saved state without issuing Save (1.466ms)
✔ viewer startup: actual script loads, binds events and paints its first frame (16.8892ms)
✔ viewer startup: missing reports error without drawing or unhandled rejection (1.037ms)
✔ viewer startup: network reports error without drawing or unhandled rejection (0.9711ms)
✔ viewer startup: bad-json reports error without drawing or unhandled rejection (0.9386ms)
✔ viewer startup: no-canvas reports error without drawing or unhandled rejection (0.8463ms)
✔ viewer startup: missing optional Pi reference still renders assembly (1.7685ms)
✔ viewer startup: failed studio renderer falls back with a visible reason (2.5442ms)
✔ rack viewer startup: required and optional meshes load then schedule both views (3.3623ms)
✔ rack viewer startup: optional-404 keeps required meshes usable (1.3593ms)
✔ rack viewer startup: optional-network keeps required meshes usable (1.4065ms)
✔ rack viewer startup: required failure retains diagnostic (1.3674ms)
✔ rack viewer startup: renderer failure retains diagnostic (0.9258ms)
ℹ tests 27
ℹ suites 0
ℹ pass 27
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 60.1312
RESULT: all checks passed

```

