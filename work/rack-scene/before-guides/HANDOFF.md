# Assembly Workshop — current handoff

Updated 2026-10-18. Read AGENTS.md, this file and PROJECT.md first. Canonical home: `C:/Users/brian/Documents/Codex/2026-10-17/Assembly Workshop`.

## Purpose and current state

Design equipment assemblies inside a Lab Rax rack context: **configure rack → select slot → create equipment/tray/faceplate/bracket**. Pi4 is the first supported geometry adapter, not the whole product. Recovered user decisions from the original ChatGPT chat restore the dark three-panel GUI direction.

Phase7 remains **CLOSED WITH LIMITATIONS**. The earlier specimen has Brian's positive qualitative fit report; it is not physical validation of the later digital build or general strength/installation approval. No new numbered phase has started.

## What works

- Current app: `outputs/Mechanical_Design_App/`, Python3.10 standard library/SQLite + local HTML/JS. Offline local resources; STL delivery, no printer integration.
- Dark studio with dashboard, Rack/Assemble/Review/Prepare, Equipment Library/Assembly Explorer, contextual Properties, searchable shortcuts. `workspace.js`, `workspace.css` wrap the existing controls.
- Multiple named rack layouts, optional user-supplied dimensions, orbitable schematic, selectable slots and explicit Pi4 slot allocations. Overlap/out-of-range allocations and shrinking past occupied slots are blocked.
- Rack persistence: `rack_workspace.py`, separate `rack-workspace.json` beside the chosen hardware DB, explicit Save layout, stale-writer protection, atomic replacement and prior JSON snapshots in `rack-history/`.
- Hardware imports/revisions/pins, Pi4 checks, generation/export safeguards retained. Viewer per-pixel depth testing fixes false overlap at the join and full-view framing fits the model.
- Rack toolbar now has **Lab Rax references**: supplied creator photos, read-only orbitable views of all21 individual source components, source bounds/provenance/license metadata and Brian's attributed M6 insert note. Exact source coordinates are retained; assembly transforms, rack export, fit and strength remain unsupported/UNKNOWN. Source/handler checks passed; live visual acceptance is pending.

## Exact app/data location and running state

- App: `outputs/Mechanical_Design_App/`.
- **Normal-use data: `data/normal-use/`**, copied in full from `outputs/Mechanical_Design_App_Beta_0_8/Mechanical_Design_App/data/` at Brian's direction. Original remains untouched. Six hardware revisions, M3x8/94459A140 r1 pins, pilot4, fixed stack3.3/pocket8/boss9. One legacy cached revision retained.
- Normal-use startup: `outputs/Mechanical_Design_App/start.bat`. It supplies `--existing-library` and an absolute resolved data path, skips starter imports and refuses to create a missing replacement DB. Direct app.py without the flag retains historical automatic-start behavior: use the configured launcher.
- Server left running at `http://127.0.0.1:8765/` with the real new dashboard; session9610 was still running during handoff checks. Do not blindly start a second server. A previous user-launched server had to be identified/restarted because it served old route handlers with new disk assets.
- No real rack layout has been saved yet at final inspection; no `data/normal-use/rack-workspace.json` exists. Do not confuse the five-slot disposable acceptance rack with user data.
- Browser tests used `work/gui-restoration/acceptance-data/`, port8767; test server stopped and test tab closed. Fresh browser/desktop sessions require Brian's approval.

## Critical limitations — do not lose these again

**Rack building is currently layout planning only.** Rack posts/rails/allocation shelves are schematic primitives, never STL geometry. The original HTML files and supplied rack component sources were recovered in this automation run; see `work/rack-geometry-recovery/Recovery_Report.md`. The complete HTML is a component assembly/import planner; no rack-frame manufacturing STL writer was located. The shortened code-only copy has20 unusable mesh payload pairs. Do not claim the historical app or full specification was restored. Verified assembled interfaces/usable clearances and physical rack fit remain missing/UNKNOWN.

Only the existing Pi4 geometry adapter works. Slot allocations reference a **shared Pi4 hardware project**, not independent per-slot pins or revisions. Current exports retain documented Pi4 assembly coordinates; they do not include rack frames or slot transforms. Drag-and-drop, arbitrary equipment/CAD editing, synchronized revision comparison and many older specification features are unimplemented.

Legacy cache lacks an integrity manifest: preserved, but matching downloads are blocked until separately authorized regeneration. No mesh builds were generated during GUI work. No automatic pack imports. Unsupported dimensions, usable depth, loads, wall/process guidance, strength and installation remain UNKNOWN. M3x0.5/pilot3–4.2/fixed stack3.3/pocket8/boss9 limits unchanged.

Four-corner mounting stays TABLED; niche insert research stays parked. No printer/slicer integration. No printing, purchases, uploads, release packaging, publishing, deployment or pushes authorized by handoff work. Supplier/Pi assets with unresolved rights stay local.

## Evidence and recovery

- `work/gui-restoration/Recovered_GUI_Decisions.json`:98 recovered user-authored decisions with turn IDs. Original ChatGPT chat `Create Claude App Prompt`, ID `6ad39502-fa44-83e8-a1ce-5a357df4d02e`, began October17 08:32 Pacific. Older pagination became accessible; many assistant messages remain placeholders. Recovered historical plans do not override later scope constraints.
- `work/gui-restoration/Restoration_Report.md`, `Verification.json`, `HTTP_Checks.json`, `Rack_Workspace.png`, `Normal_Use_Dashboard.png`.
- Before-GUI app safety copy: `work/gui-restoration/before-app/`. Do not restore it wholesale over current user data.
- Data identification/copy evidence: `outputs/Normal_Use_Location_Review/`.
- Phase7 evidence: `outputs/Phase7_Closeout/Closeout_Report.md`, digital acceptance report, physical observation/provenance and prior preservation reports. Keep historical assets intact.
- Current closeout: `outputs/Session_Handoff_20261018/`; prior HANDOFF/PROJECT/AGENTS archived there, along with final checks, next-chat prompt and preservation report once complete. Current working app/assets/data remain mostly untracked: **Git alone is not a backup**.

## Verification actually completed

GUI work:7 rack-document tests and12 existing app tests PASS (mounting-specific test intentionally excluded). Node catalog and Phase7 handlers, viewer controls, depth pixel tests and syntax PASS. HTTP checks exercised asset/API delivery, save/reload, stale writes and session token enforcement in disposable data. Authorized browser checks passed creation, selected-slot Pi4 allocation, persistence after reload, overlap/shrink rejection, equipment card flow, assembly inspection, review/prepare navigation and shortcut search; no console errors. No renderer/export/import buttons clicked.

Handoff: read-only SQLite integrity `ok`; all12 original+normal-use data file hashes still match the pre-GUI manifest. Protected SCAD/assembly/Pi reference/mounting files unchanged. See final checks. No need to rerun rendering or historical acceptance for unchanged code.

## Next steps

1. Read the recovery report and recovered decisions; keep the rack-first product purpose central.
2. Original HTML and the three requested creator rack assets are now preserved with hashes in `work/rack-geometry-recovery/sources/`; no need to ask Brian to identify/upload them again. Read that recovery report and `Reference_Inspection.json`. The full HTML hash and all three3MF hashes match historical Sigma records. Rights stay unresolved/local-only.
3. Next is a read-only assembly-transform audit against source mating features and creator visual evidence. Recover discrete component support first; do not stretch meshes, treat3MF print-plate transforms as rack poses, copy old cloud/assistant hooks or claim a parametric rack exporter. Brian's M6 statement is supplied design information; insert part/bore/fit/strength remain UNKNOWN and Pi4 M3 pins remain unchanged.
4. Preserve the functioning UI, normal-use data, pins, immutable caches and baseline. Use fresh disposable data for checks, and request permission before browser control or any new render. Do not reopen Phase7 or the parked mounting/research matters.

## Rack recovery run activation and checks — 2026-10-18

Current source includes new reference routes/assets. Sandbox denied loopback access to8765; no live server state was established and no server was started/stopped. The existing process, if running, needs a controlled restart with the configured launcher before the new reference routes work. Do not start a duplicate. No fresh desktop/browser session was opened.

3 reference tests PASS (all21 exact source coordinate/index comparisons, tamper/traversal blocking, read-only routes); all7 rack tests PASS in new project-local disposable temp data; new reference UI handler/canvas harness PASS all21 selections/stale requests/error recovery/finite projection; existing catalog/Phase7 frontend handlers and new/recovered JS syntax PASS. This is not browser visual acceptance. All12 preserved data files and protected baseline hashes match; read-only SQLite integrity `ok`; no normal rack saved. See `work/rack-geometry-recovery/Verification.json`. No geometry builds/exports, imports, physical work, release packaging or publishing.

## Run and targeted checks

### Startup repair after Brian's screenshot — 2026-10-18

The screenshot showed the light server-template page with a network error. An approved check outside the sandbox confirmed port8765 refused connections: no app server was listening. Started the current app hidden with `--existing-library --data data/normal-use --port8765`, PID28892, without starter imports (6 existing revisions,0 added). GET checks for the root, studio JS/CSS, rack reference script/catalog, rack workspace, state and assembly all returned200. All6 existing normal-use file hashes are unchanged; no rack was saved. The current source is active, superseding the earlier pending-restart note. Open `http://127.0.0.1:8765/` rather than an HTML file preview. No fresh browser/desktop-control session was opened.

Added a file-URL startup guard to index.html so direct opening shows launcher instructions instead of the broken fallback UI. Its file/HTTP behavior and existing catalog/Phase7/reference frontend handlers pass Node checks. Evidence and server logs: `work/startup-repair/`. Server must stay running for normal use. No CAD generation, hardware changes or physical work occurred.

From the canonical root in PowerShell. Normal use only if port8765 is not already occupied:

```powershell
& 'C:/Program Files/Python310/python.exe' outputs/Mechanical_Design_App/app.py --existing-library --data data/normal-use --port 8765
# or use outputs/Mechanical_Design_App/start.bat
& 'C:/Program Files/Python310/python.exe' -B -m unittest discover -s outputs/Mechanical_Design_App -p test_rack_workspace.py -v
& 'C:/Users/brian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe' --check outputs/Mechanical_Design_App/workspace.js
```

Rack tests use new temporary data; atomic replacement and localhost checks may require sandbox escalation. Additional existing Node checks: app `test_catalog_workflow.cjs`, `test_phase7_workflow.cjs`; work `test_viewer_v08.cjs`, `test_viewer_depth.cjs`. `work/gui-restoration/check_http.py` uses fresh temporary data, no render; inspect before running. For other acceptance choose a NEW data path under work/, never active data. OpenSCAD.exe is the documented renderer, not the broken .com launcher; no render is needed for handoff.
