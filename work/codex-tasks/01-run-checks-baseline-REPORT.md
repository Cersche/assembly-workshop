# Task 01 — checks baseline

Date: 2026-10-19. Complete; no fixes made.

## Result

52 Python tests and 20 JavaScript tests passed; zero failing, skipped or incomplete tests. Every test and its result is listed in the captured output below. Counts in the task/roadmap were estimates and are stale. Task 03 may proceed.

## Commands actually run

- `powershell -File outputs/Mechanical_Design_App/run_checks.ps1`: exit 1 before any tests ran because Windows PowerShell disabled scripts. Full error below.
- `powershell -ExecutionPolicy Bypass -File outputs/Mechanical_Design_App/run_checks.ps1`: exit 0, 52 Python + 20 JS passed. Execution policy applies to this child process only; no persistent policy changed.
- Python 3.10 stdlib `subprocess.run` repeated that same process-scoped command to capture this report's exact complete output: exit 0.
- Read UTF-8 AGENTS.md, PROJECT.md, HANDOFF.md, ROADMAP.md, task standing rules, task specs 01–03 and run_checks.ps1 using Get-Content.

## Initial invocation error (full text)

```text
File C:\Users\brian\Documents\Codex\2026-10-17\Assembly Workshop\outputs\Mechanical_Design_App\run_checks.ps1 cannot 
be loaded because running scripts is disabled on this system. For more information, see about_Execution_Policies at 
https:/go.microsoft.com/fwlink/?LinkID=135170.
    + CategoryInfo          : SecurityError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : UnauthorizedAccess
```

## Complete test output (capture run)

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
Ran 52 tests in 5.210s

OK
== JavaScript (js-tests/run.js) ==
✔ every app script parses (9.261ms)
✔ every script index.html loads from /rack-references/ is in the asset manifest (1.6524ms)
✔ RackLayout.checkRange rejects out-of-range and overlapping ranges (0.5327ms)
✔ RackLayout.change moves an allocation and resets fit to UNKNOWN (0.2059ms)
✔ RackLayout.release and restore round-trip; restore keeps fit UNKNOWN (0.7774ms)
✔ WorkshopCatalog.filter: latest revision, kind, exact diameter, unknown material, length bounds (0.4186ms)
✔ WorkshopCatalog.changes lists changed fields with their effect (0.2725ms)
✔ LabRaxScene.frame stacks posts in levels of at most 5U that sum to the rack height (0.5631ms)
✔ LabRaxScene.guidePose puts the cable guide plate flat on the post face at the slot hole pair (3.014ms)
✔ WorkshopClearance.screen grades height, width and depth against nominal rack numbers (0.5109ms)
✔ WorkshopClearance.screen keeps unspecified rack numbers UNKNOWN and flags span mismatch (0.1593ms)
✔ LabRaxStudio.artworkRect stays inside the 216 x 34 mm faceplate field (0.2324ms)
✔ LabRaxStudio.artworkWindow generalizes the Pi4 window to wizard faceplates of any U span (0.3816ms)
✔ LabRaxStudio.artworkRect keeps wizard images clear of port and keystone openings (2.2828ms)
✔ LabRaxStudio.selectionRect follows the plate front at any U height (0.172ms)
✔ LabRaxPorts Pi 4 preset: nine ports, face UNKNOWN, front-edge ports point front and USB/Ethernet right (0.5122ms)
✔ LabRaxPorts wizard ports: front openings, rear ports and keystone pass-through pairs (0.336ms)
✔ LabRaxPorts overrides merge, reset, custom ports and prune (0.7907ms)
✔ LabRaxPorts marker rotations are proper rotations and parts sit at the allocation base (0.4013ms)
✔ LabRaxPorts marker meshes exist for every connector type (5.107ms)
ℹ tests 20
ℹ suites 0
ℹ pass 20
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 40.5639
RESULT: all checks passed
```

## Files changed and hashes

Only this new report was written. Before SHA-256: absent. Its after SHA-256 is supplied in the final task summary (a report cannot contain its own final hash). No existing file changed.

## Assumptions and open questions

The process-scoped script invocation resolves a launcher-policy issue, not a failing check. The runner's documented temporary-data behavior is relied on; no server, export, build or user-data action was requested or performed. Physical fit/strength remain UNKNOWN. No open question blocks task 02 or 03.
