# Assembly Workshop — current handoff

Updated 2026-10-18 from Brian's explicit housekeeping confirmations. Read [AGENTS](AGENTS.md), [PROJECT](PROJECT.md), then this handoff. AGENTS.md has since been updated with C1/C1b/C2/C3/C4 ([AGENTS updates needed](docs/housekeeping/AGENTS_Updates_Needed.md) is now historical). Dated work reports (e.g. work/gui-refinement/Report.md "Pi4 remains the only manufacturing adapter… no frame STL") describe their own snapshot and are superseded by C2/C3. Preserve every other boundary.

## 2026-10-19 session summary (read first)

- **Single home:** this PC only; laptop/phone steer sessions via Remote Control. Normal server restarted via start.bat (PID 41408 at handoff) on data/normal-use.
- **Checks:** `powershell -File outputs/Mechanical_Design_App/run_checks.ps1` → 38 Python (temp data) + 11 JS (js-tests/run.js, Node from PATH or the local Codex runtime). Page-closure logic (save controller, viewer startup) is still verified by hand only.
- **UI cleanup:** Equipment "My Equipment" list ([report](work/equipment-list/Report.md)); slimmer sidebar Hardware library ([report](work/hardware-section/Report.md)); 2C left grouping FINAL. assembly-studio.js restored to the asset manifest (3D inspection viewer had silently fallen back).
- **New features** ([report](work/save-history/Report.md), [screening](work/clearance-screening/Report.md)): Save **History** (restore earlier rack versions as an unsaved draft); **Recent colors** (per-browser); **clearance screening** in Review for wizard equipment (OK/TIGHT/OVER/UNKNOWN, nominal numbers, fit UNKNOWN); wizard width/depth **warnings never block** (Brian's direction).
- **Testing pattern:** disposable server via `.claude/launch.json` "disposable-8767" on a scratch copy of data; never test on data/normal-use.
- **Next chat:** refine the existing faceplate painting / artwork tools (slot Appearance tab: colors, local image fit/center/size/position/remove; "Print in color" multi-color export via /api/faceplate-colors/preview|export, test_faceplate_color.py). Read that code first; refine, don't rebuild. AGENTS.md still says artwork is preview-only and image-to-STL deferred — only change that scope on Brian's explicit word.

## Current state and Brian's confirmed direction

- Rack-first local studio: configure Lab Rax rack → select slot → create an equipment/tray/faceplate assembly. STL delivery; no printer/slicer integration. Source meshes remain the rack preview; independent slot assemblies keep their own hardware snapshots, inputs and revisions. M3 x 0.5 Pi4 limits and immutable mechanical baseline remain intact.
- **C1 confirmed:** every faceplate U gets four rack holes, two per side. Corner radius is limited to 2.5 mm. Fit/strength of this four-hole design remains UNKNOWN. Brian's earlier positive fit applies to the old two-hole, 3 mm, square-corner specimen only and does not transfer.
- **C1b confirmed:** each support extension occupies its own 1U between stacked posts; post U plus extension U equals rack height. Joints are movable. This supersedes the earlier zero-height joint model; it does not certify physical fit.
- **C2 confirmed:** generic equipment_tray.scad and the hardware import wizard are in scope as a second adapter beside Pi4: dimensions, STL, SCAD and STEP via local FreeCAD. Keep the Pi4 path untouched. Snap tabs, clips, pegs, straps, keystones, single-piece joints, rear support and multi-U spacing are unprinted; fit/strength UNKNOWN.
- **C3 confirmed:** PRINT THE RACK and /api/rack-stl are in scope. Creator parts remain local under Brian's BY-NC-SA/personal-use direction; never redistribute them. Rack fit/strength UNKNOWN. This housekeeping did not run any export.
- Selected GUI remains **1C/2C/3A/4A/5A/6A/7A/8A**: collapsible inspector and left groups; select then ellipsis/right-click actions; Setup/Hardware/Appearance tabs; one explicit atomic Save; presets/custom colors; artwork fit/center/size/position/remove. **2C confirmed final by Brian 2026-10-19** after the Equipment/Hardware library cleanup. Artwork/colors are preview-only; image-to-STL work is deferred. Draft does not save; checks/exports must not silently save.
- Phase 6 and Phase 7 are **CLOSED WITH LIMITATIONS**. Digital checks and the earlier qualitative specimen report are recorded evidence, not blanket physical certification. Niche insert research remains parked. No printing or new physical testing is authorized here.

## Data locations — C4 SETTLED (Brian, 2026-10-18)

**data/normal-use is the official user data.** The server was restarted 2026-10-18 with start.bat's arguments (`--existing-library --data …\data\normal-use`) and serves My Lab Rax with 2 allocations. Never start bare `python app.py`; that falls back to outputs/Mechanical_Design_App/data, which is now a preserved historical copy (older 1-allocation rack saved 14:49; wizard cache 20:59). Do not delete or merge it. [Data_Locations](docs/housekeeping/Data_Locations.md) records file hashes and database-copy inspection: both DBs have six parts/one project but different hashes; saved rack documents contain two versus one allocations. These are disk snapshots, not evidence of current active process or unsaved browser state.

The launcher outputs/Mechanical_Design_App/start.bat:3 explicitly selects data/normal-use with --existing-library. app.py's --data default selects its own data directory (outputs/Mechanical_Design_App/app.py:897). Historical reports record both folders in use at different times. No process/browser/listener was inspected or started in housekeeping. Never rely on an old PID or refresh a tab casually; preserve unsaved drafts.

## Backups (Brian, 2026-10-18)

Destinations: `D:\Backups\Assembly Workshop` (local) and `C:\Users\brian\OneDrive\Backups\Assembly Workshop` (private OneDrive; Brian authorized this personal online copy). One timestamped subfolder per backup; never overwrite. Keep the OneDrive copy unshared (creator parts BY-NC-SA personal use; Pi/supplier rights unresolved).

## Next steps and open limits

1. Done: AGENTS.md updated with C1/C1b/C2/C3/C4 (see its "Confirmed scope expansion" section).
2. C4 settled (above). Library-built equipment cached only in the app-local folder may need re-saving from the wizard. Preserve databases, any journal/WAL/SHM, revisions, rack documents/history, equipment caches and artwork together. A scratch DB copy is not a consistent live backup guarantee.
3. 2C review done (final, 2026-10-19). Recent colors, history/recovery UI and envelope screening done 2026-10-19. Remaining gaps: complete per-instance component editing, artwork-to-STL scope, automated tests for page-closure logic. These are backlog, not an instruction to implement.
4. Keep unsupported dimensions, usable thread depth, generic wall/process guidance, load/strength/retention, installation, service access and new-feature fit UNKNOWN. [Open_Unknowns](docs/housekeeping/Open_Unknowns.md) retains source-specific limits. No evidence regeneration or physical work by default.

## Where things live and what was checked

- Runnable source: outputs/Mechanical_Design_App; [Code_Map](docs/housekeeping/Code_Map.md) maps source files and HTTP routes by static reading only.
- Current selected-GUI evidence: work/gui-refinement/Report.md and Decisions.json; renderer/repair/startup reports are linked in the [archive index](docs/archive/README.md). Read only relevant reports; older reports describe earlier snapshots.
- Acceptance/specimen provenance: outputs/Phase7_Closeout/Closeout_Report.md and outputs/Phase7_Physical_Observations. Readiness plans stay in docs/phase7-readiness as historical planning; they are not software-completion gates.
- The [decision log](docs/housekeeping/Decision_Log.md) distinguishes explicit Brian directions, superseded intent and unestablished chronology. [Changes](docs/housekeeping/Changes.md) lists exact operations and reversals; the [manifest summary](docs/housekeeping/Backup_Manifest_Summary.md) inventories assets without creating a backup.
- Full pre-housekeeping handoff is preserved in [the archive](docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md). Protected outputs/work/data were read only. No tests, app, geometry, render/export, restart, commit, push, upload or install was run. Earlier acceptance claims were not rerun. Most assets remain untracked; Git alone is not a backup.
