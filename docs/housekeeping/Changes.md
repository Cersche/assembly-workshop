# Housekeeping changes — 2026-10-18

Brian approved audit items 1, 3, 4, 5, 6, 7, 8 and additive Part B. Item 2 was NOT approved. Current Brian confirmations supersede the audit's unresolved C1–C3 disposition; C4 remains unresolved. Audit.md remains an unchanged historical Phase 1 record. No commit/push/app/test/build/export/server action. AGENTS.md: zero edits. All timestamps in inventories are UTC.

## Operation log

Pre-edit SHA-256 is the original source hash; an added file has no pre-edit hash. Every overwritten root file has a byte-preserved archived original. Revert instructions are descriptions only: preserve the new version separately first, then restore/copy or move the original; no deletion is necessary.

| Step | Operation | Original → new path | Pre-edit SHA-256 | Inverse operation |
| --- | --- | --- | --- | --- |
| 1 | create | (absent) → docs/housekeeping/Changes.md | N/A | Move this new log to a separate retained review folder if reverting; do not delete it. |
| 2 | preserve copy | HANDOFF.md → docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md | 1dc6e7fc7a2ea1263fb07ae655553a21abd150dd01799ca02d321e2fb3b3e923 | Copy archived bytes back to HANDOFF.md after preserving its replacement; retain archive. |
| 3 | preserve copy | PROJECT.md → docs/archive/handoffs/PROJECT_pre_housekeeping_20261018.md | c5e76a66f80cfeda7af4c5370bfac62a06653ad6383ec794032016aa679f3401 | Copy archived bytes back to PROJECT.md after preserving its replacement; retain archive. |
| 4 | move | START_HERE.md → docs/archive/handoffs/START_HERE_20261018.md | 97f837ce4029087076829ef4176e742f5b6eb12080fb309e08571db8ca46f77e | Retain any new pointer at START_HERE.md elsewhere; move docs/archive/handoffs/START_HERE_20261018.md back to START_HERE.md without replacement. |
| 5 | move | GEMINI_HANDOFF.md → docs/archive/handoffs/GEMINI_HANDOFF_20261018.md | f6cc70b5b2ebb3e7eb73f9b76a23f4cb599d64ce341587a878f63e7c216bb7fd | Retain any new pointer at GEMINI_HANDOFF.md elsewhere; move docs/archive/handoffs/GEMINI_HANDOFF_20261018.md back to GEMINI_HANDOFF.md without replacement. |
| 6 | move | patch_dialog.py → docs/archive/scripts/patch_dialog.py | f84c7d3796a1ea46db523eaf1b1f6f1487a01519510e97ba57c6f16f5f39067c | Retain any new pointer at patch_dialog.py elsewhere; move docs/archive/scripts/patch_dialog.py back to patch_dialog.py without replacement. |
| 7 | edit | HANDOFF.md → HANDOFF.md | 1dc6e7fc7a2ea1263fb07ae655553a21abd150dd01799ca02d321e2fb3b3e923 | Preserve the new HANDOFF.md elsewhere; restore bytes from docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md. |
| 8 | edit | PROJECT.md → PROJECT.md | c5e76a66f80cfeda7af4c5370bfac62a06653ad6383ec794032016aa679f3401 | Preserve the new PROJECT.md elsewhere; restore bytes from docs/archive/handoffs/PROJECT_pre_housekeeping_20261018.md. |
| 9 | create | (absent) → START_HERE.md | N/A | Retain/move this new file outside its active path; no original to restore. |
| 10 | create | (absent) → GEMINI_HANDOFF.md | N/A | Retain/move this new file outside its active path; no original to restore. |
| 11 | create | (absent) → docs/housekeeping/AGENTS_Updates_Needed.md | N/A | Retain/move this new file outside its active path; no original to restore. |
| 12 | create | (absent) → docs/archive/README.md | N/A | Retain/move this new file outside its active path; no original to restore. |
| 13 | create | (absent) → docs/housekeeping/Backup_Manifest.csv | N/A | Retain/move this new file outside its active path; no original to restore. |
| 14 | create | (absent) → docs/housekeeping/Backup_Manifest_Summary.md | N/A | Retain/move this new file outside its active path; no original to restore. |
| 15 | create | (absent) → docs/housekeeping/Data_Locations.md | N/A | Retain/move this new file outside its active path; no original to restore. |
| 16 | create | (absent) → docs/housekeeping/Decision_Log.md | N/A | Retain/move this new file outside its active path; no original to restore. |
| 17 | create | (absent) → docs/housekeeping/Open_Unknowns.md | N/A | Retain/move this new file outside its active path; no original to restore. |
| 18 | create | (absent) → docs/housekeeping/Changes.md | N/A | Move this new log to a separate retained review folder if reverting; do not delete it. |
| 19 | create | (absent) → docs/housekeeping/Code_Map.md | N/A | Retain/move this new file outside its active path; no original to restore. |
| 20 | create | (absent) → docs/housekeeping/Link_Check.md | N/A | Retain/move this new file outside its active path; no original to restore. |

## Verification and skipped actions

All 946 protected checkpoint files retain matching SHA-256; no protected path disappeared. AGENTS.md and Audit.md hashes unchanged. All three readiness docs unchanged/in place. Four archived root originals and moved patcher match original hashes. Every expected destination was collision-checked before changes. No destination collision occurred.

Backup_Manifest.csv covers every file at the pre-change checkpoint (not these later generated docs); the exact cutoff prevents a self-hash fiction. No backup was made. Database copies only were opened read-only. All original file bytes outside the five approved root paths remain unchanged. Source differences C1–C3 resolved by Brian's direction, not by tests. C4, browser drafts/listener, physical outcomes and old snapshot payload completeness remain unverified. No tests/app/server/build/render/export/commit/push/upload/install/subagent.

## Git before

```text
 M AGENTS.md
 M HANDOFF.md
 M PROJECT.md
 M work/gui-restoration/Restoration_Report.md
?? GEMINI_HANDOFF.md
?? START_HERE.md
?? data/
?? docs/
?? outputs/Lab_Rax_Pi4_Assembly_Beta_Clearance_v2/
?? outputs/Lab_Rax_Pi4_Assembly_Beta_Gusset_Fix/
?? outputs/Lab_Rax_Pi4_Clearance_v2.zip
?? outputs/Lab_Rax_Pi4_Gusset_Fix.zip
?? outputs/Mechanical_Design_App/
?? outputs/Mechanical_Design_App_Beta_0_1.zip
?? outputs/Mechanical_Design_App_Beta_0_1/
?? outputs/Mechanical_Design_App_Beta_0_2.zip
?? outputs/Mechanical_Design_App_Beta_0_2/
?? outputs/Mechanical_Design_App_Beta_0_3.zip
?? outputs/Mechanical_Design_App_Beta_0_3/
?? outputs/Mechanical_Design_App_Beta_0_4.zip
?? outputs/Mechanical_Design_App_Beta_0_5.zip
?? outputs/Mechanical_Design_App_Beta_0_5/
?? outputs/Mechanical_Design_App_Beta_0_6.zip
?? outputs/Mechanical_Design_App_Beta_0_6/
?? outputs/Mechanical_Design_App_Beta_0_6_1.zip
?? outputs/Mechanical_Design_App_Beta_0_6_1/
?? outputs/Mechanical_Design_App_Beta_0_7.zip
?? outputs/Mechanical_Design_App_Beta_0_7/
?? outputs/Mechanical_Design_App_Beta_0_8.zip
?? outputs/Mechanical_Design_App_Beta_0_8/
?? outputs/Mechanical_Design_App_Beta_Spec.md
?? outputs/Normal_Use_Location_Review/
?? outputs/Phase7_Closeout/Closeout_Review.md
?? outputs/Phase7_Closeout/Evidence_Check.json
?? outputs/Phase7_Closeout/app_cli_final.log
?? outputs/Phase7_Closeout/before_AGENTS.md
?? outputs/Phase7_Closeout/before_HANDOFF.md
?? outputs/Phase7_Closeout/before_PROJECT.md
?? outputs/Phase7_Closeout/before_final_AGENTS.md
?? outputs/Phase7_Closeout/before_final_HANDOFF.md
?? outputs/Phase7_Closeout/before_final_PROJECT.md
?? outputs/Phase7_Closeout/before_final_README.md
?? outputs/Phase7_Closeout/before_final_index.html
?? outputs/Phase7_Closeout/catalog_handlers_final.log
?? outputs/Phase7_Closeout/extract_frontend_final.log
?? outputs/Phase7_Closeout/frontend_syntax_final.log
?? outputs/Phase7_Closeout/phase7_handlers_final.log
?? outputs/Phase7_Digital_Acceptance/
?? outputs/Phase7_Hardware_Evidence/
?? outputs/Phase7_Physical_Observations/
?? outputs/Phase7_Start/
?? outputs/Physical_Test_Coupons_2026-10-18/
?? outputs/Pi4_fit_inspection.md
?? outputs/Pi4_fit_review_REFERENCE_ONLY.3mf
?? outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/
?? outputs/Session_Handoff_20261018/before_AGENTS.md
?? outputs/Session_Handoff_20261018/before_HANDOFF.md
?? outputs/Session_Handoff_20261018/before_PROJECT.md
?? patch_dialog.py
?? result.json
?? work/add_v08_viewtest.py
?? work/align_pi.py
?? work/analyze_pi.py
?? work/app_frontend_check.js
?? work/app_v03.py
?? work/app_v04.py
?? work/app_v05.py
?? work/app_v06.py
?? work/app_v061.py
?? work/app_v07.py
?? work/app_v08.py
?? work/assemble-selection/
?? work/assemble-studio/
?? work/assembly-instances/
?? work/build_app_assembly.py
?? work/build_v2.py
?? work/check_gusset_pi.py
?? work/check_other_pi.py
?? work/check_pi_closed.py
?? work/check_v2_other_triangles.py
?? work/check_v2_triangles.py
?? work/close_phase6_workflow.py
?? work/extract_frontend.py
?? work/faceplate-selection/
?? work/fix_viewer_harness.py
?? work/four_corner_reference_measurements.json
?? work/four_corner_render_verification.json
?? work/gui-refinement/
?? work/gui-render-repair/
?? work/gui-restoration/Normal_Use_Dashboard.png
?? work/gui-restoration/Rack_Workspace.png
?? work/gui-restoration/acceptance-data/
?? work/gui-restoration/before-app/
?? work/gui-restoration/check_http.py
?? work/gui-restoration/protected-data-hashes.json
?? work/gui-style-delivery/
?? work/hardware-evidence/
?? work/inspect_step.py
?? work/joint_collision.scad
?? work/joint_collision.stl
?? work/make_starter_catalog.py
?? work/pack_v03.py
?? work/pack_v04.py
?? work/pack_v05.py
?? work/pack_v06.py
?? work/pack_v061.py
?? work/pack_v07.py
?? work/pack_v08.py
?? work/package_app.py
?? work/package_revision.py
?? work/package_v2_final.py
?? work/pcb_collision.scad
?? work/pcb_collision.stl
?? work/phase5-browser/
?? work/phase5-solid-checks/
?? work/phase7-digital/
?? work/phase7/
?? work/pi_aligned.stl
?? work/pi_components.json
?? work/pi_fit_review.3mf
?? work/pi_reference.stl
?? work/polish_phase6_workflow.py
?? work/rack-branding/
?? work/rack-geometry-recovery/
?? work/rack-scene/
?? work/render-studio/
?? work/startup-reliability/
?? work/startup-repair/
?? work/step_pcb_analysis.json
?? work/test_viewer.cjs
?? work/test_viewer_depth.cjs
?? work/test_viewer_v06.cjs
?? work/test_viewer_v061.cjs
?? work/test_viewer_v08.cjs
?? work/update_app_tests.py
?? work/update_app_v02.py
?? work/update_v2_package_script.py
?? work/update_viewer_test.py
?? work/usb_candidate.stl
?? work/usb_collision.log
?? work/usb_collision.scad
?? work/usb_collision.stl
?? work/v07_faceplate.stl
?? work/v07_proposed.scad
?? work/v08-build-result.json
?? work/v08-build/
?? work/v2_full_pi.scad
?? work/v2_gusset_triangle_checks.json
?? work/v2_joint.scad
?? work/v2_mesh_checks.json
?? work/v2_other_triangle_checks.json
?? work/v2_pcb.scad
?? work/v2_usb_clearance_05.scad
?? work/v2_verification.json
?? work/validate_phase5_solids.py
?? work/validate_v07_source.py
?? work/validate_v08.py
?? work/validate_v2_mesh.py
?? work/verification.json
?? work/verify_revision.py
?? work/verify_usb_clash.py
?? work/verify_user_export.py
?? work/workflow-audit/
?? work/write_fit_report.py
?? work/zip_app.py
?? work/zip_app_v02.py
```

## Git after

```text
 M AGENTS.md
 M HANDOFF.md
 M PROJECT.md
 M work/gui-restoration/Restoration_Report.md
?? GEMINI_HANDOFF.md
?? START_HERE.md
?? data/
?? docs/
?? outputs/Lab_Rax_Pi4_Assembly_Beta_Clearance_v2/
?? outputs/Lab_Rax_Pi4_Assembly_Beta_Gusset_Fix/
?? outputs/Lab_Rax_Pi4_Clearance_v2.zip
?? outputs/Lab_Rax_Pi4_Gusset_Fix.zip
?? outputs/Mechanical_Design_App/
?? outputs/Mechanical_Design_App_Beta_0_1.zip
?? outputs/Mechanical_Design_App_Beta_0_1/
?? outputs/Mechanical_Design_App_Beta_0_2.zip
?? outputs/Mechanical_Design_App_Beta_0_2/
?? outputs/Mechanical_Design_App_Beta_0_3.zip
?? outputs/Mechanical_Design_App_Beta_0_3/
?? outputs/Mechanical_Design_App_Beta_0_4.zip
?? outputs/Mechanical_Design_App_Beta_0_5.zip
?? outputs/Mechanical_Design_App_Beta_0_5/
?? outputs/Mechanical_Design_App_Beta_0_6.zip
?? outputs/Mechanical_Design_App_Beta_0_6/
?? outputs/Mechanical_Design_App_Beta_0_6_1.zip
?? outputs/Mechanical_Design_App_Beta_0_6_1/
?? outputs/Mechanical_Design_App_Beta_0_7.zip
?? outputs/Mechanical_Design_App_Beta_0_7/
?? outputs/Mechanical_Design_App_Beta_0_8.zip
?? outputs/Mechanical_Design_App_Beta_0_8/
?? outputs/Mechanical_Design_App_Beta_Spec.md
?? outputs/Normal_Use_Location_Review/
?? outputs/Phase7_Closeout/Closeout_Review.md
?? outputs/Phase7_Closeout/Evidence_Check.json
?? outputs/Phase7_Closeout/app_cli_final.log
?? outputs/Phase7_Closeout/before_AGENTS.md
?? outputs/Phase7_Closeout/before_HANDOFF.md
?? outputs/Phase7_Closeout/before_PROJECT.md
?? outputs/Phase7_Closeout/before_final_AGENTS.md
?? outputs/Phase7_Closeout/before_final_HANDOFF.md
?? outputs/Phase7_Closeout/before_final_PROJECT.md
?? outputs/Phase7_Closeout/before_final_README.md
?? outputs/Phase7_Closeout/before_final_index.html
?? outputs/Phase7_Closeout/catalog_handlers_final.log
?? outputs/Phase7_Closeout/extract_frontend_final.log
?? outputs/Phase7_Closeout/frontend_syntax_final.log
?? outputs/Phase7_Closeout/phase7_handlers_final.log
?? outputs/Phase7_Digital_Acceptance/
?? outputs/Phase7_Hardware_Evidence/
?? outputs/Phase7_Physical_Observations/
?? outputs/Phase7_Start/
?? outputs/Physical_Test_Coupons_2026-10-18/
?? outputs/Pi4_fit_inspection.md
?? outputs/Pi4_fit_review_REFERENCE_ONLY.3mf
?? outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/
?? outputs/Session_Handoff_20261018/before_AGENTS.md
?? outputs/Session_Handoff_20261018/before_HANDOFF.md
?? outputs/Session_Handoff_20261018/before_PROJECT.md
?? result.json
?? work/add_v08_viewtest.py
?? work/align_pi.py
?? work/analyze_pi.py
?? work/app_frontend_check.js
?? work/app_v03.py
?? work/app_v04.py
?? work/app_v05.py
?? work/app_v06.py
?? work/app_v061.py
?? work/app_v07.py
?? work/app_v08.py
?? work/assemble-selection/
?? work/assemble-studio/
?? work/assembly-instances/
?? work/build_app_assembly.py
?? work/build_v2.py
?? work/check_gusset_pi.py
?? work/check_other_pi.py
?? work/check_pi_closed.py
?? work/check_v2_other_triangles.py
?? work/check_v2_triangles.py
?? work/close_phase6_workflow.py
?? work/extract_frontend.py
?? work/faceplate-selection/
?? work/fix_viewer_harness.py
?? work/four_corner_reference_measurements.json
?? work/four_corner_render_verification.json
?? work/gui-refinement/
?? work/gui-render-repair/
?? work/gui-restoration/Normal_Use_Dashboard.png
?? work/gui-restoration/Rack_Workspace.png
?? work/gui-restoration/acceptance-data/
?? work/gui-restoration/before-app/
?? work/gui-restoration/check_http.py
?? work/gui-restoration/protected-data-hashes.json
?? work/gui-style-delivery/
?? work/hardware-evidence/
?? work/inspect_step.py
?? work/joint_collision.scad
?? work/joint_collision.stl
?? work/make_starter_catalog.py
?? work/pack_v03.py
?? work/pack_v04.py
?? work/pack_v05.py
?? work/pack_v06.py
?? work/pack_v061.py
?? work/pack_v07.py
?? work/pack_v08.py
?? work/package_app.py
?? work/package_revision.py
?? work/package_v2_final.py
?? work/pcb_collision.scad
?? work/pcb_collision.stl
?? work/phase5-browser/
?? work/phase5-solid-checks/
?? work/phase7-digital/
?? work/phase7/
?? work/pi_aligned.stl
?? work/pi_components.json
?? work/pi_fit_review.3mf
?? work/pi_reference.stl
?? work/polish_phase6_workflow.py
?? work/rack-branding/
?? work/rack-geometry-recovery/
?? work/rack-scene/
?? work/render-studio/
?? work/startup-reliability/
?? work/startup-repair/
?? work/step_pcb_analysis.json
?? work/test_viewer.cjs
?? work/test_viewer_depth.cjs
?? work/test_viewer_v06.cjs
?? work/test_viewer_v061.cjs
?? work/test_viewer_v08.cjs
?? work/update_app_tests.py
?? work/update_app_v02.py
?? work/update_v2_package_script.py
?? work/update_viewer_test.py
?? work/usb_candidate.stl
?? work/usb_collision.log
?? work/usb_collision.scad
?? work/usb_collision.stl
?? work/v07_faceplate.stl
?? work/v07_proposed.scad
?? work/v08-build-result.json
?? work/v08-build/
?? work/v2_full_pi.scad
?? work/v2_gusset_triangle_checks.json
?? work/v2_joint.scad
?? work/v2_mesh_checks.json
?? work/v2_other_triangle_checks.json
?? work/v2_pcb.scad
?? work/v2_usb_clearance_05.scad
?? work/v2_verification.json
?? work/validate_phase5_solids.py
?? work/validate_v07_source.py
?? work/validate_v08.py
?? work/validate_v2_mesh.py
?? work/verification.json
?? work/verify_revision.py
?? work/verify_usb_clash.py
?? work/verify_user_export.py
?? work/workflow-audit/
?? work/write_fit_report.py
?? work/zip_app.py
?? work/zip_app_v02.py
```

The four pre-existing tracked modifications remain the same tracked paths: AGENTS.md, HANDOFF.md, PROJECT.md, work/gui-restoration/Restoration_Report.md. Only HANDOFF/PROJECT received authorized new edits. New archive/housekeeping docs remain untracked; moved untracked patch_dialog.py is now under docs/archive/scripts. Git index/HEAD unchanged.

## Inverse-operation safety

Do not run automatic rollback. First preserve current replacements at unused destinations. Then use the byte-preserved originals and move inverses listed above. New files may be moved to a retained external review folder, not deleted. Restoration must never replace protected app/data assets or discard pre-existing modifications. AGENTS received zero edits.

## Final document review refinements

The helper encountered two housekeeping-only errors (a scratch module name collision during source-map docstring extraction, then an undefined completion-statistic variable after documents/verification were written). Neither executed app/test code or changed protected assets. Resumed only unfinished additive work; no moves/root edits repeated. Before refining generated docs, preserved all four originals (including this log) byte-for-byte in C:\Users\brian\AppData\Local\Packages\sandbox.{a74db76a-fac8-4a64-ab03-6b47e878327b}\AC\Temp\assembly-housekeeping-20261018\review-preserved-v1. These scratch review copies are not a repository/data backup.

| Step | Operation | Original → new path | Pre-edit SHA-256 | Inverse operation |
| --- | --- | --- | --- | --- |
| 21 | edit (generated documentation) | docs/housekeeping/Code_Map.md → docs/housekeeping/Code_Map.md | abe24342943c443755a7f1ab7a667dbad0b362caf3cef44b0a6eeebdb22e950b | Preserve replacement elsewhere, restore C:\Users\brian\AppData\Local\Packages\sandbox.{a74db76a-fac8-4a64-ab03-6b47e878327b}\AC\Temp\assembly-housekeeping-20261018\review-preserved-v1\Code_Map.md; Made HTTP handler names exact and clarified nested historical sources/assets; no route invocation. |
| 22 | edit (generated documentation) | docs/housekeeping/Decision_Log.md → docs/housekeeping/Decision_Log.md | e866b0ac96318e8a45e3b5bb273967e03aa405072d7bc4db368deb340cdbe25d | Preserve replacement elsewhere, restore C:\Users\brian\AppData\Local\Packages\sandbox.{a74db76a-fac8-4a64-ab03-6b47e878327b}\AC\Temp\assembly-housekeeping-20261018\review-preserved-v1\Decision_Log.md; Reordered into historical/undated, dated attestations and latest direct confirmations; no invented event timestamps. |
| 23 | edit (generated documentation) | docs/housekeeping/Link_Check.md → docs/housekeeping/Link_Check.md | e1cd427f0cc8f55400f8f4e00441c98b078f7a658555e67de1878f8920234d8a | Preserve replacement elsewhere, restore C:\Users\brian\AppData\Local\Packages\sandbox.{a74db76a-fac8-4a64-ab03-6b47e878327b}\AC\Temp\assembly-housekeeping-20261018\review-preserved-v1\Link_Check.md; Separated real missing targets from contextual filenames/examples; summarized existing links by source; reran static path checks after final doc refinements. |
| 24 | edit (generated documentation) | docs/housekeeping/Changes.md → docs/housekeeping/Changes.md | 903adf8ef6ee6e5700218cfa95a13470e0801f3ab83f690d49c6ca27775108b8 | Preserve replacement elsewhere, restore C:\Users\brian\AppData\Local\Packages\sandbox.{a74db76a-fac8-4a64-ab03-6b47e878327b}\AC\Temp\assembly-housekeeping-20261018\review-preserved-v1\Changes.md; Append final review and verification record; prior log preserved. |

Final read-only verification: 946 protected files match the pre-change SHA-256 values; all original paths remain. AGENTS/Audit/readiness docs unchanged. All five archived originals/moved files match originals. Current root Markdown links have no missing targets. Full historical-path findings and unresolved examples remain in Link_Check.md.

Manifest cutoff: all 957 files at the pre-change checkpoint are hashed; later housekeeping docs are explicitly outside that checkpoint and listed in this log. 971 files exist after organization (no deletion; moves account for absent root patch_dialog.py). No backup created. No source sidecars were present at initial copy. No timestamp columns existed in either SQLite schema, so no latest row timestamp was inferred. Recovered decision timestamps/order remain undetermined; no fabricated chronological dates. C4 active-folder choice, current listener/drafts, unprinted physical outcomes and earlier backup payload completeness were deliberately not resolved.

Git status after final refinements has the same path set as the after block above. Four tracked modified paths remain the pre-existing set; HANDOFF/PROJECT contain approved changes, AGENTS and protected work report retain their pre-pass hashes. No files staged, no commit/push; HEAD remains f754713.

## Plain absolute-path documentation follow-up

Preserved Link_Check.md and this log before append at C:\Users\brian\AppData\Local\Packages\sandbox.{a74db76a-fac8-4a64-ab03-6b47e878327b}\AC\Temp\assembly-housekeeping-20261018\review-preserved-v2. Added the confirmed historical workspace path from docs/phase7-readiness/Verification_Report.md:3; no protected source edited. This supplements the earlier link counts rather than rewriting source evidence.

| Step | Operation | Original → new path | Pre-edit SHA-256 | Inverse operation |
| --- | --- | --- | --- | --- |
| 25 | append documentation | docs/housekeeping/Link_Check.md → docs/housekeeping/Link_Check.md | a9c29fb0d61b1b6874051fd7f0a6841271c5b27241dc6994fd998f3dede0a63b | Preserve replacement separately; restore C:\Users\brian\AppData\Local\Packages\sandbox.{a74db76a-fac8-4a64-ab03-6b47e878327b}\AC\Temp\assembly-housekeeping-20261018\review-preserved-v2\Link_Check.md |
| 26 | append documentation | docs/housekeeping/Changes.md → docs/housekeeping/Changes.md | 781a8e8eee479591e0984c94f64116bfa04b5363372ab894160461bfe3ad0cba | Preserve replacement separately; restore C:\Users\brian\AppData\Local\Packages\sandbox.{a74db76a-fac8-4a64-ab03-6b47e878327b}\AC\Temp\assembly-housekeeping-20261018\review-preserved-v2\Changes.md |
