# 08 — Flag outdated library items and "Rebuild as new item" (implementation)

**Goal:** implement the create-copy design in [05-library-resave-proposal-REPORT.md](05-library-resave-proposal-REPORT.md), with Brian's answers (2026-10-19):
1. **Create a copy.** Rebuild makes a NEW library item ID. The old item, its build folder and every rack placement stay byte-identical. No updating of placed items.
2. **Automatic name suffix, editable later.** Copy display name = original + " (current template copy)"; the user may rename via the normal Edit flow. Render the copy with the original spec.name so the suffix alone does not change geometry identity; store the display name separately (e.g. `display_name`), and keep old items without it readable.
3. **Source matches but build process unknown:** show "Matches current source; build process unknown" AND still offer "Rebuild as new item" (low-key, not a warning).
4. Invalid old specs (retired snap joint, keystone v2 conflict): "Needs review" with the specific reason; no rebuild, no automatic substitution.

**Do (keep it to this scope; skip the proposal's pipeline-namespace/CAS extras and list them in the report as follow-ups):**
- equipment.py: read-only `template_status(data_dir, item)` → older_source / matches_source_unknown_pipeline / needs_review(reason) / unknown_evidence / integrity_problem, per proposal steps 1–5. No rendering, no writes on status.
- equipment.py: `rebuild_copy(data_dir, item_id, expected_build)` → rereads item, rejects stale/missing, clean()s the spec, renders via existing render(), appends a new item with `rebuilt_from_item` / `rebuilt_from_build`; failures leave the index unchanged. Idempotent for a repeat of the same request (no duplicate copies).
- app.py: GET status (new endpoint or an added field that keeps the existing array shape) and POST rebuild endpoint with the existing token checks. Do not change existing route contracts.
- equipment-wizard.js: badge + "Rebuild as new item" beside the existing My Equipment Edit/Delete, using the proposal's exact wording. No render on list/open/focus; refresh keeps unsaved rack and wizard drafts. Do NOT rearrange the final left groups.
- Tests: proposal tests 1–7, 9 (render mocked), 10 (double-click), 11, 12 in new stdlib Python and Node test files on temporary data only; register them in the existing checks. No real OpenSCAD runs in tests.

**May change:** outputs/Mechanical_Design_App/equipment.py, app.py, equipment-wizard.js, run_checks.ps1, work/gui-refinement/check_python.py (registration only), new test files. Archive copies first. Pi4 paths, faceplate_color.py, rack files and data/ are off limits.

**Done when:** run_checks.ps1 passes, the report shows the status/rebuild results on a temporary fixture library, and states nothing in data/normal-use was read or written.
