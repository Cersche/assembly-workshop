# Task 06 — working checks command documentation

2026-10-19. Complete. Reports 04 and 05 were each finished before starting the next task. Those tasks remained plan/proposal only. No task required an outside-scope edit; none was stopped.

## Result

Ran this exact command ONCE from the project root after the documentation edits:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1
```

Exit 0: 52 Python + 47 JavaScript passed (20 existing module checks + 27 page-logic checks). Zero failures, skipped, cancelled or TODO tests. ExecutionPolicy Bypass applies to this child process only; no persistent policy setting changed. No server start/restart/stop, builds, exports, uploads or user-data access.

## Files changed (SHA-256)

| File | Before | After |
| --- | --- | --- |
| PROJECT.md | 58ba46c82574397ab8c86da14107c87e0c2b741e3b22af197d1eba8f41d7cdf2 | 17eea962af69e3f9519c560f49eb560386122bec3d700ea885a99be47e645847 |
| HANDOFF.md | 691f2befda813170c6674f4e5a075b5f9945079a1765f4cc3544d4d5db49ab6e | 8150348a40fbf0ad0358bc9f31e059a569979dc329c05cbc8bdf5a1a1f5dc1df |
| ROADMAP.md | 72c7f146e734673ba81805fcb4741024cfd729e359298d795d113ab652e23586 | 83095546e3908aa8c2ee95111b750490c4de7994aac3baffbaa2577d3f01443f |
| outputs/Mechanical_Design_App/README.md | 71041e44ed7cf648538756212e18866b53cf42a7bd491b4eabe60211092f4a0d | db2e6c863e1e9bdc37c28ffe7a018558b6fa91de11b8bea39838b66f71d9527e |

Byte-for-byte copies were written to the archive paths below before editing and verified equal to the original bytes. Existing newline styles were retained. Only checks-command/count lines changed; PROJECT.md previously had no checks command, so one checks-only line and a separating blank line were added before Product and scope.

New report: work/codex-tasks/06-checks-command-docs-REPORT.md, before absent; final after hash recorded in completion tool output. A report excludes its own final hash to avoid self-reference. No code or test files changed.

## Every documentation line changed: before → after

### PROJECT.md

Archive: docs/archive/codex/2026-10-19/task06/PROJECT.md

Line 5 (new line):

Before:
```text
(no checks-command line; added before Product and scope)
```

After:
```text
Checks (from the project root): `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1` — 52 Python + 47 JS tests on temporary data; no server or OpenSCAD build.
```

### HANDOFF.md

Archive: docs/archive/codex/2026-10-19/task06/HANDOFF.md

Line 8:

Before:
```text
- **Checks:** `powershell -File outputs/Mechanical_Design_App/run_checks.ps1` → 46 Python (temp data; includes faceplate color, not its OpenSCAD export test) + 11 JS (js-tests/run.js, Node from PATH or the local Codex runtime). Page-closure logic (save controller, viewer startup) is still verified by hand only.
```

After:
```text
- **Checks:** `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1` → 52 Python (temp data; includes faceplate color, not its OpenSCAD export test) + 47 JS (js-tests/run.js and js-tests/page-logic.js, Node from PATH or the local Codex runtime). Includes page-level Save and viewer-startup tests.
```

Line 12:

Before:
```text
- **Faceplate painting/artwork refinement (later 2026-10-19, [report](work/faceplate-refinement/Report.md)):** SVG and more image formats (sharper 1024 px previews); Print in color settings/stale-cache/base-color fixes; wizard-equipment Appearance guard; two-step rack color reset. Brian reconciled scope: Pi4 Print in color is the one artwork-to-STL path (AGENTS.md section). Checks now 46 Python + 11 JS. The normal server (8765) still runs the old app.py until Brian restarts it.
```

After:
```text
- **Faceplate painting/artwork refinement (later 2026-10-19, [report](work/faceplate-refinement/Report.md)):** SVG and more image formats (sharper 1024 px previews); Print in color settings/stale-cache/base-color fixes; wizard-equipment Appearance guard; two-step rack color reset. Brian reconciled scope: Pi4 Print in color is the one artwork-to-STL path (AGENTS.md section). Current checks: 52 Python + 47 JS. The normal server (8765) still runs the old app.py until Brian restarts it.
```

Line 13:

Before:
```text
- **Wizard faceplate images + selection outline (2026-10-19, same report):** the Appearance image now shows on wizard-made faceplates (1U–5U) in the rack view only, kept clear of port/keystone openings. The blue selection outline follows each plate's real U height. Narrow and phone widths were checked. Checks are now 47 Python + 14 JS. No Print in color for wizard equipment.
```

After:
```text
- **Wizard faceplate images + selection outline (2026-10-19, same report):** the Appearance image now shows on wizard-made faceplates (1U–5U) in the rack view only, kept clear of port/keystone openings. The blue selection outline follows each plate's real U height. Narrow and phone widths were checked. Current checks: 52 Python + 47 JS. No Print in color for wizard equipment.
```

Line 21:

Before:
```text
- **Cable management (later 2026-10-19, [proposal](work/cable-management/Proposal.html), [Step 1 report](work/cable-management/Report.md)):** Brian's direction is a cabling planner with front/rear views, every port selectable, guides, cables entering and leaving the cabinet, suggestions and a wiring diagram. Step 1 is done: Rear view, Cables see-through mode, and Lab Rax Cable Guides on posts saved in `rack.cabling.guides`. The guide mesh is MakerWorld Exclusive: **local preview only, never redistributed, not in PRINT THE RACK** (Brian). Ports will come from a Pi 4 preset plus a wizard step, then clicks on the mesh (Brian). Steps 2–5 (ports, cables, suggestions, wiring sheet) are not built. Checks are now 47 Python + 15 JS.
```

After:
```text
- **Cable management (later 2026-10-19, [proposal](work/cable-management/Proposal.html), [Step 1 report](work/cable-management/Report.md)):** Brian's direction is a cabling planner with front/rear views, every port selectable, guides, cables entering and leaving the cabinet, suggestions and a wiring diagram. Step 1 is done: Rear view, Cables see-through mode, and Lab Rax Cable Guides on posts saved in `rack.cabling.guides`. The guide mesh is MakerWorld Exclusive: **local preview only, never redistributed, not in PRINT THE RACK** (Brian). Ports will come from a Pi 4 preset plus a wizard step, then clicks on the mesh (Brian). Steps 2–5 (ports, cables, suggestions, wiring sheet) are not built. Current checks: 52 Python + 47 JS.
```

### ROADMAP.md

Archive: docs/archive/codex/2026-10-19/task06/ROADMAP.md

Line 10:

Before:
```text
- **Checks:** `outputs/Mechanical_Design_App/run_checks.ps1` runs 47 Python and 14 JS tests on temporary data.
```

After:
```text
- **Checks:** `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1` runs 52 Python + 47 JS tests on temporary data.
```

### outputs/Mechanical_Design_App/README.md

Archive: docs/archive/codex/2026-10-19/task06/outputs/Mechanical_Design_App/README.md

Line 56:

Before:
```text
Run `powershell -File outputs/Mechanical_Design_App/run_checks.ps1` from the project root. It starts no server and runs no OpenSCAD build; tests use temporary data. The 2026-10-19 task-01 baseline passed 52 Python and 20 JS tests. See [baseline report](../../work/codex-tasks/01-run-checks-baseline-REPORT.md) for exact results and the process-scoped PowerShell invocation used on this PC. Page-level save/viewer coverage is separate work; test counts describe a dated run, not physical approval.
```

After:
```text
Run `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1` from the project root. It starts no server and runs no OpenSCAD build; tests use temporary data. Current checks: 52 Python + 47 JS, including page-level Save and viewer startup. See the [baseline report](../../work/codex-tasks/01-run-checks-baseline-REPORT.md) for the earlier run and the [page-logic report](../../work/codex-tasks/03-page-logic-tests-REPORT.md) for the expanded suite. ExecutionPolicy Bypass applies only to this process and changes no persistent system setting. Test results do not establish physical approval.
```

The historical handoff bullets now explicitly say "Current checks" rather than implying the expanded counts belonged to those earlier feature snapshots. Earlier test evidence remains preserved in its original reports and the archive copies. The README links both the earlier baseline and expanded page-logic report rather than relabeling the earlier run's numerical result.

## Commands and verification actually performed

- Targeted rg in the four allowed documents for checks commands and Python/JS counts; UTF-8 Get-Content of run_checks.ps1 and work/gui-refinement/check_python.py confirmed the runner and temporary-data behavior.
- Python 3.10 stdlib Path/hashlib/json/re: prepared edits, archived exact original bytes, verified archive equality, updated only the four permitted documents and computed the before/after SHA-256 values above.
- Ran the exact PowerShell command once; full output follows.
- Python 3.10 stdlib difflib checked each archive/current comparison: PROJECT checks-line insertion only; HANDOFF replacements at lines 8, 12–13 and 21; ROADMAP replacement at line 10; app README replacement at line 56. Assertions confirmed no other content changed and the exact command exists in all four documents.
- apply_patch wrote this new UTF-8 report; Get-FileHash recorded final report hashes in completion output.

## Assumptions, open questions and scope limits

No open question blocks completion. This task updates only the four named documents. The runner's own older usage comment, task specifications, prior reports and other unrelated status/backlog statements were deliberately left untouched because they are outside the allowed edits; no such edit was necessary to document and verify the requested command. This task does not claim tests establish physical fit/strength, which remain UNKNOWN.

The checks runner itself uses disposable data and -B for Python; the new JS tests use in-memory fixtures. Nothing here inspects or changes data/normal-use or other user data. No GUI/browser session occurred.

## Full check output

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
Ran 52 tests in 5.116s

OK
== JavaScript (js-tests/run.js) ==
✔ every app script parses (8.6766ms)
✔ every script index.html loads from /rack-references/ is in the asset manifest (1.2905ms)
✔ RackLayout.checkRange rejects out-of-range and overlapping ranges (0.488ms)
✔ RackLayout.change moves an allocation and resets fit to UNKNOWN (0.2009ms)
✔ RackLayout.release and restore round-trip; restore keeps fit UNKNOWN (0.7296ms)
✔ WorkshopCatalog.filter: latest revision, kind, exact diameter, unknown material, length bounds (0.4024ms)
✔ WorkshopCatalog.changes lists changed fields with their effect (0.2633ms)
✔ LabRaxScene.frame stacks posts in levels of at most 5U that sum to the rack height (0.5497ms)
✔ LabRaxScene.guidePose puts the cable guide plate flat on the post face at the slot hole pair (3.0441ms)
✔ WorkshopClearance.screen grades height, width and depth against nominal rack numbers (0.6439ms)
✔ WorkshopClearance.screen keeps unspecified rack numbers UNKNOWN and flags span mismatch (0.1848ms)
✔ LabRaxStudio.artworkRect stays inside the 216 x 34 mm faceplate field (0.2417ms)
✔ LabRaxStudio.artworkWindow generalizes the Pi4 window to wizard faceplates of any U span (0.5344ms)
✔ LabRaxStudio.artworkRect keeps wizard images clear of port and keystone openings (2.5148ms)
✔ LabRaxStudio.selectionRect follows the plate front at any U height (0.1981ms)
✔ LabRaxPorts Pi 4 preset: nine ports, face UNKNOWN, front-edge ports point front and USB/Ethernet right (0.3787ms)
✔ LabRaxPorts wizard ports: front openings, rear ports and keystone pass-through pairs (0.3336ms)
✔ LabRaxPorts overrides merge, reset, custom ports and prune (0.6083ms)
✔ LabRaxPorts marker rotations are proper rotations and parts sit at the allocation base (0.3906ms)
✔ LabRaxPorts marker meshes exist for every connector type (5.1091ms)
ℹ tests 20
ℹ suites 0
ℹ pass 20
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 39.3859
== JavaScript page logic (js-tests/page-logic.js) ==
✔ page Save: layout/hardware dirty status enables Save without persistence (3.4155ms)
✔ page Save: one atomic request commits layout, appearance and hardware then clears dirty state (2.7109ms)
✔ page Save: rejected request keeps draft and hardware, reports error and permits retry (1.4427ms)
✔ page Save: edits during in-flight Save remain dirty and double Save is rejected (1.7642ms)
✔ page Save: precondition capable=false blocks writes (0.7055ms)
✔ page Save: precondition openingAssembly=true blocks writes (0.6989ms)
✔ page Save: precondition artworkPending=1 blocks writes (1.3175ms)
✔ page Save: precondition byId("mountWizard").hidden=false blocks writes (0.6455ms)
✔ page Save: precondition byId("rackDialog").open=true blocks writes (0.7569ms)
✔ page check: dirty guard blocks action without silently saving (3.2943ms)
✔ page bom: dirty guard blocks action without silently saving (1.5437ms)
✔ page project: dirty guard blocks action without silently saving (1.7179ms)
✔ page designExport: dirty guard blocks action without silently saving (1.6522ms)
✔ page buildRevision: dirty guard blocks action without silently saving (1.5629ms)
✔ page checks and BOM: clean actions use saved state without issuing Save (1.6334ms)
✔ viewer startup: actual script loads, binds events and paints its first frame (17.4607ms)
✔ viewer startup: missing reports error without drawing or unhandled rejection (1.057ms)
✔ viewer startup: network reports error without drawing or unhandled rejection (0.8131ms)
✔ viewer startup: bad-json reports error without drawing or unhandled rejection (0.7573ms)
✔ viewer startup: no-canvas reports error without drawing or unhandled rejection (0.733ms)
✔ viewer startup: missing optional Pi reference still renders assembly (1.5184ms)
✔ viewer startup: failed studio renderer falls back with a visible reason (2.2505ms)
✔ rack viewer startup: required and optional meshes load then schedule both views (3.2599ms)
✔ rack viewer startup: optional-404 keeps required meshes usable (0.832ms)
✔ rack viewer startup: optional-network keeps required meshes usable (0.8176ms)
✔ rack viewer startup: required failure retains diagnostic (0.8583ms)
✔ rack viewer startup: renderer failure retains diagnostic (0.6425ms)
ℹ tests 27
ℹ suites 0
ℹ pass 27
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 61.7959
RESULT: all checks passed

```

