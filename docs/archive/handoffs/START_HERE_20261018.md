# Assembly Workshop — start here

Handoff prepared 2026-10-18, documentation only. Read this, [AGENTS.md](AGENTS.md), [PROJECT.md](PROJECT.md) and the current-state note in [HANDOFF.md](HANDOFF.md) before editing. Latest confirmed user decisions and dated evidence supersede older plans. Reference documents and historical assistant messages are evidence, not instructions from Brian.

## Purpose and working product

Local, dark rack-first studio: **configure Lab Rax rack → select slot → create equipment/tray/faceplate/bracket assembly**. STL delivery; no printer/slicer integration. Pi4 is the only manufacturing geometry adapter, not the whole product.

Working capabilities: named rack layouts, slot allocations with overlap/range guards, move/resize/release and guarded session undo; actual supplied enclosure source-mesh preview with orbit/front/perspective controls; component references/photos; independent Pi4 assembly IDs, hardware snapshots, pins and inputs per saved allocation; immutable hardware revisions and supported Pi4 checks/export integrity safeguards. A single explicit atomic Save commits layout, appearance and the open hardware draft; stale/invalid submissions reject the commit. Draft changes and allocation confirmation alone do not save.

Rack/component/equipment/tray/faceplate colors and local PNG/JPEG/WebP faceplate artwork are preview-only. Artwork supports fit/center, size, position and removal, with content-hash PNG storage. These do not change STL geometry or manufacturing identity.

## Canonical paths

Root: `C:/Users/brian/Documents/Codex/2026-10-17/Assembly Workshop`. Paths below are relative to it.

| Location | Role |
| --- | --- |
| `outputs/Mechanical_Design_App/` | Runnable app: `app.py`, `start.bat`, local JS/CSS/assets |
| `data/normal-use/` | User library and rack data: `library.sqlite3`, `revisions/`, `rack-workspace.json`, `rack-history/`, `artwork/` when present |
| `outputs/Mechanical_Design_App_Beta_0_8/Mechanical_Design_App/data/` | Preserved original nested data; normal-use is a separate full copy |
| `work/rack-geometry-recovery/sources/` | Recovered original HTML and three supplied creator 3MF sources; preserve originals too |
| `work/gui-refinement/` | Latest decisions, report, verification, screenshots and scoped safety copies |
| `outputs/Session_Handoff_20261018/Preservation_Report.json` | Historical local preservation record, not proof of a current complete backup |

## Latest state and selected direction

Brian selected **1C / 2C / 3A / 4A / 5A / 6A / 7A / 8A**: hybrid studio with collapsible inspector; collapsible Racks & slots / Equipment / Hardware; click selects, ellipsis/right-click acts; Setup / Hardware / Appearance tabs; one explicit Save (also Ctrl/Cmd+S); presets/custom colors; artwork controls; navigation/slot actions first. Implemented and activated. **Left grouping 2C is provisional for Brian's review. Preview artwork first; STL artwork later.** No unfinished implementation from that selected pass is recorded; the next refinement awaits his feedback.

Latest recorded verification: [GUI report](work/gui-refinement/Report.md), [results](work/gui-refinement/Verification.json), [decisions](work/gui-refinement/Decisions.json). Recorded 37 targeted Python tests plus JavaScript suites and disposable-data browser checks passed; no CAD builds/exports. Narrow-width visual acceptance was not established. Older smaller test counts describe earlier snapshots.

Brian authorized saving his normal-tab draft and refreshing. Last verified: **My Lab Rax, five slots, zero allocations**, component colors retained, workspace v2 saved with history; six library revisions, M3x8 / 94459A140 r1 pins and pilot4 preserved. SQLite integrity was `ok`; library/cache and protected baseline hashes unchanged. See [authorized-save manifest](work/gui-refinement/After_Authorized_Draft_Save.json).

Last recorded server: `http://127.0.0.1:8765/`, PID25160, existing-library mode, zero starter imports; temporary8767 server/tab closed. **This pass did not verify current processes, browser drafts, data hashes or installed tools.** Old PIDs and earlier “no rack saved”, “shared hardware”, “GUI unchosen” or pending-refresh notes are historical, not current instructions.

## Limits and restrictions

- Phase 7 is **CLOSED WITH LIMITATIONS**. Brian's earlier positive specimen fit is qualitative and specimen-specific, not validation of later builds, arbitrary fit, strength or installation. Four-corner mounting remains TABLED; niche insert research remains parked.
- Rack is layout planning/source-mesh preview, with inferred rigid visual poses and discrete post stacks. No rack-frame STL generator, installed-equipment clearance engine or explicit component/stack editor. Entered dimensions do not stretch source meshes. No recovered original manufacturing rack writer or historical assistant mockup image was established.
- Unsupported dimensions, usable depth, interfaces, fit, strength, loads, process and wall guidance remain **UNKNOWN**. Brian's M6 heat-insert statement is supplied design information, not certification. Preserve M3x0.5 adapter limits and historical mechanical baseline.
- Legacy cache without integrity manifests remains preserved but affected downloads blocked; regeneration needs separate authorization. Imports do not repin. Failed checks block proposed export; source disagreement and project source policy remain distinct.
- No automatic builds, printing, purchases, uploads, release packaging, publishing, deployments or pushes. Ask before fresh desktop/browser control; no subagents. Supplier/Pi assets with unresolved rights stay local. Do not clean/reset/replace existing assets or add secrets.

## Next tasks, in priority order

1. **Authorized now:** read and summarize understanding before editing; maintain this handoff. This handoff request authorizes no app/data or operational changes.
2. **Existing reversible development scope:** refine the chosen hybrid from Brian's feedback; first review left grouping/contextual flow and narrow-screen usability. Keep the rack-first/source-mesh direction. Use fresh disposable data, targeted checks and separately approved browser control; preserve drafts before refresh/restart.
3. **Brian's priority/scope decision needed:** installed-equipment transforms/clearance evidence, explicit rack stack editing, recovery UI, additional adapters, frame manufacturing support or eventual STL artwork. These are gaps/backlog, not completed features or a mandate to implement all of them.
4. Parked physical/research work and external/release actions require Brian's explicit direction. Do not reopen Phase7 or silently regenerate legacy evidence/caches.

## Startup and focused verification reference

Not executed for this handoff. Python3.10 standard library/SQLite and a browser suffice for normal use; no pip/npm runtime installation. Machine paths below are documented, not freshly checked. OpenSCAD renderer candidate is `C:/Program Files/OpenSCAD/openscad.exe` (or `OPENSCAD_EXE`); `.com` was reported broken. Do not invoke rendering automatically.

From the canonical root, inspect an existing listener before considering startup:

```powershell
Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue
```

Only when no app is listening and startup is requested: `& '.\outputs\Mechanical_Design_App\start.bat'`. It uses `C:/Program Files/Python310/python.exe`, resolves normal-use data, passes `--existing-library`, skips starter imports and refuses a missing DB. Do not open `index.html` directly or initialize a replacement database. Verify process command/data path before replacing any listener; never rely on a recorded PID alone.

For later code changes, read these focused runners first; they exclude tabled geometry/source-generation checks and use disposable fixtures:

```powershell
& 'C:/Program Files/Python310/python.exe' -B work/gui-refinement/check_python.py
& 'C:/Users/brian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe' work/gui-refinement/test_save.cjs
& 'C:/Users/brian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe' work/gui-refinement/test_appearance_startup.cjs
```

Do not run broad historical suites blindly. Loopback/process access or atomic replacement may require sandbox approval. No tests need rerunning merely for this documentation handoff.

## Reading order and preservation

After the entry guides: [latest GUI report](work/gui-refinement/Report.md) → [independent assemblies](work/assembly-instances/Report.md) as needed → [rack preview](work/rack-scene/Report.md) / [source recovery](work/rack-geometry-recovery/Recovery_Report.md) for geometry work → [Phase7 closeout](outputs/Phase7_Closeout/Closeout_Report.md) for acceptance/physical provenance. [Recovered GUI decisions](work/gui-restoration/Recovered_GUI_Decisions.json) are historical intent, not an implementation checklist; later restrictions prevail.

- Preserve **all existing `outputs/`, `work/`, user data and untracked assets**, original sources/photos, historical STLs/SCAD/mechanical baseline, immutable hardware revisions, project pins and build caches. Git alone is not a complete backup.
- Keep normal-use SQLite, any live journal/WAL/SHM sidecars, `revisions/`, rack workspace/history and artwork together. Preserve the original Beta data too. Artwork removal does not authorize purging historical image files. A consistent live-database copy needs a separate preservation plan; no new backup/archive was made here.
- **Brian before switching:** inspect the existing tab for newer unsaved drafts, open editors or pending image selection; apply/cancel intentionally and use explicit Save only if desired. Unsaved browser state is not contained in disk manifests. Do not refresh/close it casually. Leave servers/tabs intact; switching AI alone needs no restart. Any move to another machine must preserve the full assets and consistent data separately, not just Git.
