# Task 08 — template status and rebuild as new item

2026-10-19. Complete. Task 07 report was finished before this task began. End-of-task checks passed: **67 Python + 72 JavaScript** (20 module + 27 page logic + 16 rack BOM + 9 rebuild UI). No failures/skips/TODOs; no batch stop condition occurred.

## Implemented

- equipment.py template_status(data_dir,item) is read-only. It validates the saved build identifier, current spec, base-source hash/manifest identity, allowed part names and per-STL hashes; missing/malformed evidence remains unknown, hash disagreement is an integrity problem. Invalid retired snap/keystone specs need review. Exact current source still reports unknown build process; source mismatch does not diagnose a specific mechanical defect. No rendering/writing on status.
- rebuild_copy(data_dir,item_id,expected_build) rereads the original, rejects missing/stale/ineligible items, cleans its spec and uses existing render(). It verifies a current cache before reuse and verifies rendered evidence before publication. It appends a NEW library ID and rebuilt_from_item/build. Original source name is retained; automatic display_name suffix is separate.
- Duplicate requests are serialized in this process and find the existing origin/current-target copy instead of appending another. A post-render reread rejects a changed original. Index publication uses a temporary file/replace; the old serialized array entries are retained verbatim before its closing bracket. No original build or placed item is changed. Failure does not publish a copy; a successful but unreferenced cache is preserved.
- Existing normal Edit handles display_name separately and persists its rename while leaving source-producing spec.name unchanged. Existing records without display_name remain readable. Normal Save's established explicit-edit behavior is preserved, including its warning that editing an existing item affects its placements; the NEW rebuild action itself never updates those items.
- app.py adds GET /api/equipment-template-status (ID → status map) and POST /api/equipment-rebuild-copy (id, expected_build). Original GET /api/equipment-library remains an array. New POST inherits existing host/token validation.
- My Equipment gets status/details plus the explicit "Rebuild as new item" action alongside existing Edit/Delete. Final Equipment/Hardware/Racks grouping is unchanged. List/open/focus only use GETs; valid current-source/unknown-process items offer the same low-key action. Invalid/missing/integrity states offer no rebuild. Requests prevent duplicate clicks across list refresh. Success/failure/progress wording preserves UNKNOWNs and says old placements stay unchanged. Rebuild refresh does not reconstruct the wizard or alter rack drafts.
- Registered new Python tests in check_python.py (registration line only) and new Node tests in run_checks.ps1. No Pi4 path, faceplate_color.py, rack source/schema or data/ file was edited in task 08.

## Temporary fixture results (render mocked)

These are asserted outcomes from test_equipment_rebuild.py and equipment-rebuild.js in the captured run, not observations from any user's library.

| Synthetic case | Status/result |
| --- | --- |
| Legacy item eq-0123456789ab with old-source fixture | older_source; change details unavailable; no writes/render on status |
| Old keystone source or arbitrary different source | older_source without invented feature-specific diagnosis |
| Current base source and valid stored hashes | matches_source_unknown_pipeline; copy action offered |
| Retired tray snap spec / conflicting keystone collar spec | needs_review with retired/collar reason; no renderer call or replacement |
| Missing build / malformed JSON or manifest | unknown_evidence |
| Wrong source hash, manifest ID or tampered STL | integrity_problem; copy blocked |
| Valid old-source rebuild | New random eq-ID, current source-addressed build, display_name "Router (current template copy)", original spec.name "Router" |
| Source already matches | New item references verified existing build; reused_build=true; no claim of a new pipeline |
| Two concurrent clicks plus repeat request | One new copy, same returned ID, renderer mocked once |
| Stale/missing ID/build | Rejected before renderer call |
| Original edited during mocked rendering | Rejected at publication; concurrent edit retained; no added item |
| Render timeout/mesh rejection fixture | Index bytes unchanged |
| Index replacement fails | Original index bytes unchanged; successful current cache retained |
| Corrupt current target cache | Rejected before render; all existing fixture bytes unchanged |
| Existing placed item after new copy | Still resolves old ID/build; old build, rack/history and hardware sentinel bytes unchanged |
| Planning ports and display rename | Front/rear planning metadata preserved; display rename does not suffix source name |
| UI list/open/focus | Read requests only; no rebuild/download/save; unsaved rack/wizard fixtures preserved |
| Endpoint guard | Wrong token/host rejected; array library contract retained |

Fixture STL payloads are synthetic integrity bytes and do not represent rendered or physically approved meshes. Rendering is mocked; no OpenSCAD or production export route ran. Route tests invoke handler methods in memory, with no socket/server.

## Tests added and actual commands

15 stdlib Python tests cover read-only legacy arrays/status, old keystone/arbitrary source, matching unknown pipeline/reuse, missing/malformed/tampered evidence, wrong source/manifest identity, invalid snap/collar, immutable originals/copy/placements/ports, planning-only/name source behavior, separate display rename on normal Save, render/index failures, duplicate/concurrent clicks, stale/missing identities, post-render original changes, corrupt target, and in-memory route/token/host contracts.

9 Node built-in tests execute the actual Equipment-list closures and name-edit handler in a VM. They cover read-only list/focus/open and drafts/grouping, explicit request/copy with unchanged placed lookup, double click across focus refresh, low-key current-source action/cache wording, three ineligible states, failure/retry/draft retention, and separate display rename.

Commands performed:
- UTF-8 Get-Content of the approved proposal and relevant equipment/app/wizard/runner/test source ranges; targeted rg for routes, handler fixtures, naming and UI helpers.
- Python 3.10 stdlib saved exact original bytes of the five permitted existing files under docs/archive/codex/2026-10-19/task08/ with repository-relative subpaths before edits.
- apply_patch/Python text edits changed only those permitted files and added two new test files. check_python.py changed only its module-registration line.
- `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1` ran once at task end: exit 0, 67 Python + 72 JS passed. Complete output below.
- Python stdlib hashlib computed before/after hashes and difflib asserted check_python.py has exactly one changed registration line.
- apply_patch wrote this report; Get-FileHash recorded its completion hash.

## Files changed (SHA-256)

| File | Before | After |
| --- | --- | --- |
| outputs/Mechanical_Design_App/equipment.py | 980f30a4e5d0002184054a1f963f907157520b0ba873efe1f08ce9b4152ff8a2 | 28db8de3432903b67cb7c5abc37158705f84d656300b569ff9d8755a322dcbd0 |
| outputs/Mechanical_Design_App/app.py | d11fd6f172441ebcbf61f66e8b0b4437f452fd69b0d818689544108b85ef0c4d | e89504f81d9aa2bf8cd324e92cb8f4846441f4e9fd409b8518836ae2e33b11ea |
| outputs/Mechanical_Design_App/equipment-wizard.js | df08eec6e6d3bce64a3894d41a8fa33720f589595afcd87777cd88ccea11c21f | 2c2aff9e17a8216c3d5227ce8a9beeede4ddd72dd6a7138df4bb4edf936a9518 |
| outputs/Mechanical_Design_App/run_checks.ps1 | d7912968f77499d76ffb78abad9defffdd8f191b801c3eb05764b33945077e08 | cf869ad11747e50ea4235630bd8d1da98fe7e3ea8b7f282c29001a7a68f80e7f |
| work/gui-refinement/check_python.py | 644ea87ec194945f8d3f68394c8adc2c32e5fd95b55ea1dbd9f81ae306eb45e7 | d796351edb7ce215acf170ac5d50b7fe1407c48a15ba372d066ca53ee3c3fbca |
| outputs/Mechanical_Design_App/test_equipment_rebuild.py | absent (new) | eac48172a0e5f8203a4c2b8d80340f7063dec7b934cf13bf7ef1a32e7c28dd9c |
| outputs/Mechanical_Design_App/js-tests/equipment-rebuild.js | absent (new) | c64b63eda43b9bfb63f4741b4882e4097e91583ec7ad56d658413cffcb78f1a1 |

New report work/codex-tasks/08-library-rebuild-copy-REPORT.md: before absent; after hash recorded in completion tool output (self-hash excluded). Archives contain original bytes, not normalized rewrites. Task 07's workspace/rack test/report were not modified in task 08.

## Deferred follow-ups and limits

As explicitly requested, pipeline namespace/version migration and cross-writer compare-and-swap extras are NOT implemented. Builds continue to use the existing source-hash identity/render cache; a same-source rebuild can reuse its old verified cache and still has unknown pipeline provenance. This is disclosed in status/UI, not promoted to current-process certification.

REBUILD_LOCK serializes rebuild requests within this process only. The original is rechecked and index bytes compared before publication, but another normal Save/delete process or external writer can still race after that check. Comprehensive shared writer locking/CAS and cross-process transactions remain follow-ups. No new automatic migration, cleanup, build pinning, render-pipeline version or status hashing cache was introduced. Status GET currently hashes saved evidence on each request; a future read-only cache could reduce repeated work.

No browser/visual session or live runtime acceptance was performed. Node VM UI and temporary handler fixtures cover bounded logic, not full browser/OpenSCAD integration. No physical approval results from hash matching. Printed fit, strength, keystone retention and unsupported dimensions remain UNKNOWN. No open question blocks the scoped implementation; follow-ups above are deliberately outside it.

**Nothing in data/normal-use was read or written.** Other user data was also untouched. The live 8765 server was not contacted, inspected, started, stopped or restarted. No desktop session, commit, push, explicit deletion, export, printing, purchase, install, upload or publishing. Temporary test fixture cleanup is confined to freshly created disposable directories. Changes are on disk only; no claim that the running server has loaded them.

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
test_changed_original_during_render_is_not_published (test_equipment_rebuild.EquipmentRebuildTests) ... ok
test_copy_normal_edit_persists_display_rename_without_source_name_suffix (test_equipment_rebuild.EquipmentRebuildTests) ... ok
test_copy_preserves_original_build_records_placements_and_planning_ports (test_equipment_rebuild.EquipmentRebuildTests) ... ok
test_corrupt_current_target_blocks_reuse_without_overwrite (test_equipment_rebuild.EquipmentRebuildTests) ... ok
test_current_source_reports_unknown_pipeline_and_still_rebuilds_copy (test_equipment_rebuild.EquipmentRebuildTests) ... ok
test_duplicate_and_double_click_requests_append_one_copy (test_equipment_rebuild.EquipmentRebuildTests) ... ok
test_invalid_snap_and_keystone_specs_need_review_without_substitution (test_equipment_rebuild.EquipmentRebuildTests) ... ok
test_missing_malformed_and_tampered_evidence_are_separate_states (test_equipment_rebuild.EquipmentRebuildTests) ... ok
test_old_keystone_and_arbitrary_source_flag_without_inventing_reason (test_equipment_rebuild.EquipmentRebuildTests) ... ok
test_planning_only_metadata_does_not_change_source_name_only_change_does (test_equipment_rebuild.EquipmentRebuildTests) ... ok
test_render_failure_or_index_failure_preserves_original_index (test_equipment_rebuild.EquipmentRebuildTests) ... ok
test_stale_missing_or_invalid_identity_rejected_before_render (test_equipment_rebuild.EquipmentRebuildTests) ... ok
test_status_and_rebuild_routes_preserve_array_contract_and_token_guard (test_equipment_rebuild.EquipmentRebuildTests) ... ok
test_status_is_read_only_legacy_array_older_source (test_equipment_rebuild.EquipmentRebuildTests) ... ok
test_wrong_source_hash_and_manifest_id_are_integrity_problems (test_equipment_rebuild.EquipmentRebuildTests) ... ok
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
Ran 67 tests in 6.105s

OK
== JavaScript (js-tests/run.js) ==
✔ every app script parses (8.8247ms)
✔ every script index.html loads from /rack-references/ is in the asset manifest (1.507ms)
✔ RackLayout.checkRange rejects out-of-range and overlapping ranges (0.4954ms)
✔ RackLayout.change moves an allocation and resets fit to UNKNOWN (0.2014ms)
✔ RackLayout.release and restore round-trip; restore keeps fit UNKNOWN (0.7351ms)
✔ WorkshopCatalog.filter: latest revision, kind, exact diameter, unknown material, length bounds (0.3811ms)
✔ WorkshopCatalog.changes lists changed fields with their effect (0.2686ms)
✔ LabRaxScene.frame stacks posts in levels of at most 5U that sum to the rack height (0.6639ms)
✔ LabRaxScene.guidePose puts the cable guide plate flat on the post face at the slot hole pair (3.1046ms)
✔ WorkshopClearance.screen grades height, width and depth against nominal rack numbers (0.5421ms)
✔ WorkshopClearance.screen keeps unspecified rack numbers UNKNOWN and flags span mismatch (0.1752ms)
✔ LabRaxStudio.artworkRect stays inside the 216 x 34 mm faceplate field (0.2324ms)
✔ LabRaxStudio.artworkWindow generalizes the Pi4 window to wizard faceplates of any U span (0.3917ms)
✔ LabRaxStudio.artworkRect keeps wizard images clear of port and keystone openings (2.347ms)
✔ LabRaxStudio.selectionRect follows the plate front at any U height (0.2106ms)
✔ LabRaxPorts Pi 4 preset: nine ports, face UNKNOWN, front-edge ports point front and USB/Ethernet right (0.4841ms)
✔ LabRaxPorts wizard ports: front openings, rear ports and keystone pass-through pairs (0.3315ms)
✔ LabRaxPorts overrides merge, reset, custom ports and prune (0.6201ms)
✔ LabRaxPorts marker rotations are proper rotations and parts sit at the allocation base (0.406ms)
✔ LabRaxPorts marker meshes exist for every connector type (5.5314ms)
ℹ tests 20
ℹ suites 0
ℹ pass 20
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 40.1541
== JavaScript page logic (js-tests/page-logic.js) ==
✔ page Save: layout/hardware dirty status enables Save without persistence (2.5599ms)
✔ page Save: one atomic request commits layout, appearance and hardware then clears dirty state (1.5641ms)
✔ page Save: rejected request keeps draft and hardware, reports error and permits retry (0.8207ms)
✔ page Save: edits during in-flight Save remain dirty and double Save is rejected (0.9828ms)
✔ page Save: precondition capable=false blocks writes (0.617ms)
✔ page Save: precondition openingAssembly=true blocks writes (0.5408ms)
✔ page Save: precondition artworkPending=1 blocks writes (1.1952ms)
✔ page Save: precondition byId("mountWizard").hidden=false blocks writes (0.5607ms)
✔ page Save: precondition byId("rackDialog").open=true blocks writes (0.6087ms)
✔ page check: dirty guard blocks action without silently saving (3.1131ms)
✔ page bom: dirty guard blocks action without silently saving (1.4226ms)
✔ page project: dirty guard blocks action without silently saving (2.0573ms)
✔ page designExport: dirty guard blocks action without silently saving (1.8995ms)
✔ page buildRevision: dirty guard blocks action without silently saving (1.7489ms)
✔ page checks and BOM: clean actions use saved state without issuing Save (1.5499ms)
✔ viewer startup: actual script loads, binds events and paints its first frame (16.0918ms)
✔ viewer startup: missing reports error without drawing or unhandled rejection (1.1305ms)
✔ viewer startup: network reports error without drawing or unhandled rejection (0.9369ms)
✔ viewer startup: bad-json reports error without drawing or unhandled rejection (0.792ms)
✔ viewer startup: no-canvas reports error without drawing or unhandled rejection (0.7479ms)
✔ viewer startup: missing optional Pi reference still renders assembly (1.6233ms)
✔ viewer startup: failed studio renderer falls back with a visible reason (2.2044ms)
✔ rack viewer startup: required and optional meshes load then schedule both views (2.9711ms)
✔ rack viewer startup: optional-404 keeps required meshes usable (1.0432ms)
✔ rack viewer startup: optional-network keeps required meshes usable (0.94ms)
✔ rack viewer startup: required failure retains diagnostic (0.8927ms)
✔ rack viewer startup: renderer failure retains diagnostic (0.6797ms)
ℹ tests 27
ℹ suites 0
ℹ pass 27
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 56.8278
== JavaScript rack BOM (js-tests/rack-bom.js) ==
✔ rack BOM worked example: 5U default (4.3806ms)
✔ rack BOM worked example: 5U custom (0.7617ms)
✔ rack BOM worked example: 9U default (0.7053ms)
✔ rack BOM worked example: 9U custom (0.7295ms)
✔ rack BOM worked example: 14U default (0.6847ms)
✔ rack BOM worked example: 14U custom (0.6484ms)
✔ rack BOM missing side defaults only the missing stack; 1U has no joints (0.7559ms)
✔ rack BOM rejects explicitly invalid stacks and heights without fabricated parts (0.9057ms)
✔ rack BOM locked and unlocked stacks count identically (0.7844ms)
✔ rack BOM side panels toggle only segmented panels, never top/bottom (0.7954ms)
✔ rack BOM ignores cable guides, ports and artwork (0.7118ms)
✔ rack BOM agrees with real rackFrame source placements and all fixed parts (1.9213ms)
✔ rack BOM requires extensions independently of missing preview assets (1.075ms)
✔ rack setup height edits retain chosen saved stacks only at unchanged height, clamp at 14U and do not mutate (1.1319ms)
✔ rack BOM shows explicit allowances/UNKNOWNs and invalid layout error (0.674ms)
✔ moving a support refreshes a visible editing BOM; locked layout stays unchanged (0.9523ms)
ℹ tests 16
ℹ suites 0
ℹ pass 16
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 24.3215
== JavaScript equipment rebuild (js-tests/equipment-rebuild.js) ==
✔ equipment list: read-only status on list/focus/open keeps both drafts and grouping (3.7562ms)
✔ equipment list: explicit rebuild posts original identity once and preserves placed item lookup/drafts (1.2045ms)
✔ equipment list: double click and focus refresh while rebuilding do not duplicate requests (1.5007ms)
✔ equipment list: source match with unknown process offers low-key rebuild and verified-cache wording (0.9101ms)
✔ equipment list: needs_review has no rebuild and performs no write (0.7891ms)
✔ equipment list: unknown_evidence has no rebuild and performs no write (0.7185ms)
✔ equipment list: integrity_problem has no rebuild and performs no write (0.604ms)
✔ equipment list: rebuild failure keeps drafts and permits retry with exact error text (0.7841ms)
✔ equipment copy: normal Edit changes separate display name without changing source-producing spec.name (0.9273ms)
ℹ tests 9
ℹ suites 0
ℹ pass 9
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 16.9315
RESULT: all checks passed

```

