# Kickoff items 1–3 — 2026-10-19

Brian chose items 1–3 (then discuss 4). Originals before edits: work/save-history/originals/ (rack_workspace.py, app.py, workspace.js, workspace.css, index.html — index.html ended unchanged).

## 1. Rerunnable checks
- outputs/Mechanical_Design_App/js-tests/run.js — 9 Node tests (built-ins only): every script parses; every /rack-references/ script in index.html is in asset-manifest.json (catches the earlier 404 regression); RackLayout range/change/release/restore with fit kept UNKNOWN; WorkshopCatalog filter/changes; LabRaxScene.frame post levels sum to rack height; LabRaxStudio.artworkRect stays inside the faceplate field.
- outputs/Mechanical_Design_App/run_checks.ps1 — runs work/gui-refinement/check_python.py (temp data) + js-tests; finds node on PATH or the local Codex runtime.
- Gap: the save controller, viewer startup replay and DOM handlers live inside page closures and still have no automated test (verified manually in the browser).

## 2. Save history / undo
- rack_workspace.py: `_latest_history_record` (moved out of save() unchanged), `list_history` (read-only summaries, newest first), `restore_rack` (builds an unsaved rack draft from a history version; each assembly keeps its newest saved hardware; refuses assemblies now in another rack). Nothing is written.
- app.py: GET /api/rack-history and /api/rack-history/restore?generation=&rack=; capability `save_history: 1`.
- workspace.js: "History" button beside Rack settings (shown only when the server reports the capability) → dialog of earlier versions for the active rack → "Restore as draft". Save is still required; reload discards.
- Test: test_rack_workspace.test_history_lists_and_restores_draft_without_writing.
- Browser (disposable server :8767 on a scratch copy of normal-use; never the real data): listed 6 versions; restored an empty older version (disk unchanged until Save; Save added a history entry); restored the replaced 2-assembly version and saved (both assemblies back at revision 1). No console errors. Screenshot History_Dialog.jpg.

## 3. Recent colors
- workspace.js colorField: custom picker colors (on change, excluding presets) remembered newest-first, max 6, in this browser's localStorage (per-browser convenience, not saved with the rack); a "Recent" swatch row appears on every color field and refreshes together.
- Browser (disposable): stored order, preset exclusion, cross-field refresh and applying a recent swatch verified. Screenshot work/recent-colors/Recent_Colors.jpg.

## Status
Python 38/38 and JS 9/9 pass. Normal server (8765) still runs the old app.py: History needs a restart of the normal server (Brian's call; save any drafts first). JS/CSS-only parts load on refresh. Nothing printed, exported, pushed or uploaded.
