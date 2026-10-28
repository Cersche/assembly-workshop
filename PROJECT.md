# Assembly Workshop — project entry point

Updated 2026-10-19. Read [AGENTS](AGENTS.md), [current HANDOFF](HANDOFF.md) and the [ROADMAP](ROADMAP.md), then the [evidence/archive map](docs/archive/README.md) only if you need history. Brian explicitly confirmed four-hole-per-U mounting, the 1U extension rule, a second equipment adapter and rack-frame STL export. AGENTS.md has been updated with these decisions (and C4) by Claude. All other preservation and safety boundaries remain.

Checks (from the project root): `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1` — 80 Python + 134 JS tests on temporary data; no server or OpenSCAD build.

## Product and scope

Local rack-context design app: configure Lab Rax rack → select slot → design equipment/tray/faceplate assembly. STL delivery; printer/slicer integration is outside scope. Pi4 retains its documented M3 x 0.5 path and immutable baseline. The generic equipment_tray.scad and dimensions/STL/SCAD/STEP wizard (local FreeCAD) are a confirmed second adapter. PRINT THE RACK /api/rack-stl is confirmed scope; creator parts stay local, BY-NC-SA/personal use, never redistributed. Existing code presence and historical acceptance do not establish physical approval.

Selected dark hybrid GUI: 1C/2C/3A/4A/5A/6A/7A/8A, independent slot assemblies, Setup/Hardware/Appearance and one explicit atomic Save. Left grouping 2C is final (Brian, 2026-10-19). Source-mesh preview, colors and artwork do not certify dimensions; normal STLs never contain artwork. The opt-in Pi4 "Print in color" multi-color faceplate export is the one artwork-to-STL path (Brian, 2026-10-19; PROPOSED — UNVALIDATED; see AGENTS.md). Drafts remain unsaved until explicit Save. Current source/route references are in [Code_Map](docs/housekeeping/Code_Map.md); dated reports are historical evidence, not startup scripts.

## Locations and startup warning

| Location | Role |
| --- | --- |
| outputs/Mechanical_Design_App/ | Runnable app.py, start.bat, Python/JS/CSS and local reference assets |
| data/normal-use/ | **Official** user database, immutable revisions, rack workspace/history and artwork |
| outputs/Mechanical_Design_App/data/ | Preserved historical copy (older rack, wizard cache); not used |
| outputs/Mechanical_Design_App_Beta_0_8/Mechanical_Design_App/data/ | Preserved original beta data |
| work/gui-refinement/ | Chosen hybrid decisions and recorded acceptance |
| work/rack-geometry-recovery/ | Recovered original HTML/3MFs and provenance |
| outputs/Phase7_Closeout/, outputs/Phase7_Physical_Observations/ | Preserved history: earlier digital acceptance record and the old two-hole specimen photos/report. Folder names are historical, not current status |
| outputs/Session_Handoff_20261018/ | Earlier local preservation record; not proof of today's complete backup |
| docs/housekeeping/ | Audit, applied changes, decisions, UNKNOWNs, data comparison, source/link maps and inventory |

**C4 settled (Brian, 2026-10-18): data/normal-use is official.** Always start via start.bat (`--existing-library --data …\data\normal-use`). Never run bare `python app.py`; app.py:897 falls back to the app-local folder. Before starting, check no other app.py is already running. Do not merge or delete the app-local copy. See [Data_Locations](docs/housekeeping/Data_Locations.md). Historical localhost address: http://127.0.0.1:8765/; direct-file HTML cannot use app APIs.

**3D preview of print files (2026-10-27):** `python tools/mesh_viewer.py part.3mf other.stl -o work/mesh-viewer/name.html -t "Title"` writes one standalone HTML (own WebGL renderer, no CDN, works offline) to spin, zoom and pan parts; send it with SendUserFile (display "render") to view it in the Claude app panel. 3MF objects become separate parts at their build positions; several STLs are laid side by side (`--as-is` keeps their coordinates). Preview only, changes no geometry. Don't commit viewer HTML that embeds third-party/licensed meshes.

Marking: Pin taps a spot, Circle draws around something; each mark gets a note. "Copy notes" puts text (mm coordinates, part names, notes, view) on the clipboard to paste to Claude; "Copy picture"/"Save picture" give a PNG with the marks. If the panel blocks the clipboard, the notes appear selected in a box for Ctrl+C.

## Limits and preservation

What's next lives in [ROADMAP](ROADMAP.md); the old numbered-phase plan is retired. Four rack holes per faceplate U and 2.5 mm corner-radius limit are Brian-confirmed design direction; fit/strength UNKNOWN. Each extension takes its own 1U; joints movable. Earlier positive physical fit applies only to the old two-hole/3 mm/square-corner specimen. Snap/clip/peg/strap/keystone/single-piece/rear-support/multi-U features are unprinted. Usable depth, applicable wall/process/load/installation/retention guidance and general strength remain UNKNOWN. Niche insert research is parked; 2C is final. See [Open_Unknowns](docs/housekeeping/Open_Unknowns.md).

Preserve all outputs/work, both data locations and beta data, immutable revisions/caches, pins, rack history/artwork and unsaved drafts. No automatic builds. Failed checks block affected proposed exports; imports do not repin. Supplier/Pi assets with unresolved rights stay local. Python 3.10 standard library and UTF-8 remain the development baseline; no installs here. Printing, physical tests, uploads, release packaging, publishing/deployment and pushes need explicit direction. Fresh desktop control needs approval.

Git tracks only a small part of the project. [Backup_Manifest_Summary](docs/housekeeping/Backup_Manifest_Summary.md) compares the pre-housekeeping file checkpoint with the earlier snapshot manifest; no new backup was created. [Changes](docs/housekeeping/Changes.md) preserves originals and inverse operations. The former PROJECT is [archived byte-for-byte](docs/archive/handoffs/PROJECT_pre_housekeeping_20261018.md).
