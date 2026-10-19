# Assembly Workshop — current handoff

Updated 2026-10-18 from Brian's explicit housekeeping confirmations. Read [AGENTS](AGENTS.md), [PROJECT](PROJECT.md), then this handoff. AGENTS was deliberately not edited: its stale four-corner/Pi4-only/no-rack-export clauses are listed in [AGENTS updates needed](docs/housekeeping/AGENTS_Updates_Needed.md). Brian's current decisions below supersede those clauses. Preserve every other boundary.

## Current state and Brian's confirmed direction

- Rack-first local studio: configure Lab Rax rack → select slot → create an equipment/tray/faceplate assembly. STL delivery; no printer/slicer integration. Source meshes remain the rack preview; independent slot assemblies keep their own hardware snapshots, inputs and revisions. M3 x 0.5 Pi4 limits and immutable mechanical baseline remain intact.
- **C1 confirmed:** every faceplate U gets four rack holes, two per side. Corner radius is limited to 2.5 mm. Fit/strength of this four-hole design remains UNKNOWN. Brian's earlier positive fit applies to the old two-hole, 3 mm, square-corner specimen only and does not transfer.
- **C1b confirmed:** each support extension occupies its own 1U between stacked posts; post U plus extension U equals rack height. Joints are movable. This supersedes the earlier zero-height joint model; it does not certify physical fit.
- **C2 confirmed:** generic equipment_tray.scad and the hardware import wizard are in scope as a second adapter beside Pi4: dimensions, STL, SCAD and STEP via local FreeCAD. Keep the Pi4 path untouched. Snap tabs, clips, pegs, straps, keystones, single-piece joints, rear support and multi-U spacing are unprinted; fit/strength UNKNOWN.
- **C3 confirmed:** PRINT THE RACK and /api/rack-stl are in scope. Creator parts remain local under Brian's BY-NC-SA/personal-use direction; never redistribute them. Rack fit/strength UNKNOWN. This housekeeping did not run any export.
- Selected GUI remains **1C/2C/3A/4A/5A/6A/7A/8A**: collapsible inspector and left groups; select then ellipsis/right-click actions; Setup/Hardware/Appearance tabs; one explicit atomic Save; presets/custom colors; artwork fit/center/size/position/remove. **2C remains provisional pending Brian's review.** Artwork/colors are preview-only; image-to-STL work is deferred. Draft does not save; checks/exports must not silently save.
- Phase 6 and Phase 7 are **CLOSED WITH LIMITATIONS**. Digital checks and the earlier qualitative specimen report are recorded evidence, not blanket physical certification. Niche insert research remains parked. No printing or new physical testing is authorized here.

## Data locations — C4 SETTLED (Brian, 2026-10-18)

**data/normal-use is the official user data.** The server was restarted 2026-10-18 with start.bat's arguments (`--existing-library --data …\data\normal-use`) and serves My Lab Rax with 2 allocations. Never start bare `python app.py`; that falls back to outputs/Mechanical_Design_App/data, which is now a preserved historical copy (older 1-allocation rack saved 14:49; wizard cache 20:59). Do not delete or merge it. [Data_Locations](docs/housekeeping/Data_Locations.md) records file hashes and database-copy inspection: both DBs have six parts/one project but different hashes; saved rack documents contain two versus one allocations. These are disk snapshots, not evidence of current active process or unsaved browser state.

The launcher outputs/Mechanical_Design_App/start.bat:3 explicitly selects data/normal-use with --existing-library. app.py's --data default selects its own data directory (outputs/Mechanical_Design_App/app.py:897). Historical reports record both folders in use at different times. No process/browser/listener was inspected or started in housekeeping. Never rely on an old PID or refresh a tab casually; preserve unsaved drafts.

## Next steps and open limits

1. Done: AGENTS.md updated with C1/C1b/C2/C3/C4 (see its "Confirmed scope expansion" section).
2. C4 settled (above). Library-built equipment cached only in the app-local folder may need re-saving from the wizard. Preserve databases, any journal/WAL/SHM, revisions, rack documents/history, equipment caches and artwork together. A scratch DB copy is not a consistent live backup guarantee.
3. Await Brian's 2C grouping review. Other recorded gaps include recent colors, history/recovery UI, complete per-instance component editing and verified installed-equipment clearance. These are backlog, not an instruction to implement.
4. Keep unsupported dimensions, usable thread depth, generic wall/process guidance, load/strength/retention, installation, service access and new-feature fit UNKNOWN. [Open_Unknowns](docs/housekeeping/Open_Unknowns.md) retains source-specific limits. No evidence regeneration or physical work by default.

## Where things live and what was checked

- Runnable source: outputs/Mechanical_Design_App; [Code_Map](docs/housekeeping/Code_Map.md) maps source files and HTTP routes by static reading only.
- Current selected-GUI evidence: work/gui-refinement/Report.md and Decisions.json; renderer/repair/startup reports are linked in the [archive index](docs/archive/README.md). Read only relevant reports; older reports describe earlier snapshots.
- Acceptance/specimen provenance: outputs/Phase7_Closeout/Closeout_Report.md and outputs/Phase7_Physical_Observations. Readiness plans stay in docs/phase7-readiness as historical planning; they are not software-completion gates.
- The [decision log](docs/housekeeping/Decision_Log.md) distinguishes explicit Brian directions, superseded intent and unestablished chronology. [Changes](docs/housekeeping/Changes.md) lists exact operations and reversals; the [manifest summary](docs/housekeeping/Backup_Manifest_Summary.md) inventories assets without creating a backup.
- Full pre-housekeeping handoff is preserved in [the archive](docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md). Protected outputs/work/data were read only. No tests, app, geometry, render/export, restart, commit, push, upload or install was run. Earlier acceptance claims were not rerun. Most assets remain untracked; Git alone is not a backup.
