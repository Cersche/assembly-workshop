# Assembly Workshop — project entry point

Updated 2026-10-18, housekeeping only. Read [AGENTS](AGENTS.md), [current HANDOFF](HANDOFF.md), then the [evidence/archive map](docs/archive/README.md). Brian explicitly confirmed four-hole-per-U mounting, the 1U extension rule, a second equipment adapter and rack-frame STL export. AGENTS remains unedited by request; [stale clauses for Claude](docs/housekeeping/AGENTS_Updates_Needed.md) identify the exact lines. All other preservation and safety boundaries remain.

## Product and scope

Local rack-context design app: configure Lab Rax rack → select slot → design equipment/tray/faceplate assembly. STL delivery; printer/slicer integration is outside scope. Pi4 retains its documented M3 x 0.5 path and immutable baseline. The generic equipment_tray.scad and dimensions/STL/SCAD/STEP wizard (local FreeCAD) are a confirmed second adapter. PRINT THE RACK /api/rack-stl is confirmed scope; creator parts stay local, BY-NC-SA/personal use, never redistributed. Existing code presence and historical acceptance do not establish physical approval.

Selected dark hybrid GUI: 1C/2C/3A/4A/5A/6A/7A/8A, independent slot assemblies, Setup/Hardware/Appearance and one explicit atomic Save. Left grouping 2C remains provisional. Source-mesh preview, colors and artwork do not certify dimensions or change STL artwork. Drafts remain unsaved until explicit Save. Current source/route references are in [Code_Map](docs/housekeeping/Code_Map.md); dated reports are historical evidence, not startup scripts.

## Locations and startup warning

| Location | Role |
| --- | --- |
| outputs/Mechanical_Design_App/ | Runnable app.py, start.bat, Python/JS/CSS and local reference assets |
| data/normal-use/ | Preserved user database, immutable revisions, rack workspace/history and artwork |
| outputs/Mechanical_Design_App/data/ | Separate preserved database/rack document and equipment cache |
| outputs/Mechanical_Design_App_Beta_0_8/Mechanical_Design_App/data/ | Preserved original beta data |
| work/gui-refinement/ | Chosen hybrid decisions and recorded acceptance |
| work/rack-geometry-recovery/ | Recovered original HTML/3MFs and provenance |
| outputs/Phase7_Closeout/ | Milestone acceptance/limits; physical observations in adjacent Phase7_Physical_Observations |
| outputs/Session_Handoff_20261018/ | Earlier local preservation record; not proof of today's complete backup |
| docs/housekeeping/ | Audit, applied changes, decisions, UNKNOWNs, data comparison, source/link maps and inventory |

**C4 remains UNRESOLVED.** Launcher start.bat:3 uses data/normal-use with --existing-library; app.py:897 defaults to its own data directory. Later historical reports used the app-local folder. Do not switch or merge them. See [Data_Locations](docs/housekeeping/Data_Locations.md). No active listener, process data path or browser drafts were verified in housekeeping. No startup/restart is authorized by this document; do not duplicate an existing server or initialize replacement data. Historical localhost address: http://127.0.0.1:8765/; direct-file HTML cannot use app APIs.

## Limits and preservation

Phase 6 and Phase 7 are CLOSED WITH LIMITATIONS. Four rack holes per faceplate U and 2.5 mm corner-radius limit are Brian-confirmed design direction; fit/strength UNKNOWN. Each extension takes its own 1U; joints movable. Earlier positive physical fit applies only to the old two-hole/3 mm/square-corner specimen. Snap/clip/peg/strap/keystone/single-piece/rear-support/multi-U features are unprinted. Usable depth, applicable wall/process/load/installation/retention guidance and general strength remain UNKNOWN. Niche insert research is parked; 2C review and C4 are open. See [Open_Unknowns](docs/housekeeping/Open_Unknowns.md).

Preserve all outputs/work, both data locations and beta data, immutable revisions/caches, pins, rack history/artwork and unsaved drafts. No automatic builds. Failed checks block affected proposed exports; imports do not repin. Supplier/Pi assets with unresolved rights stay local. Python 3.10 standard library and UTF-8 remain the development baseline; no installs here. Printing, physical tests, uploads, release packaging, publishing/deployment and pushes need explicit direction. Fresh desktop control needs approval.

Git tracks only a small part of the project. [Backup_Manifest_Summary](docs/housekeeping/Backup_Manifest_Summary.md) compares the pre-housekeeping file checkpoint with the earlier snapshot manifest; no new backup was created. [Changes](docs/housekeeping/Changes.md) preserves originals and inverse operations. The former PROJECT is [archived byte-for-byte](docs/archive/handoffs/PROJECT_pre_housekeeping_20261018.md).
