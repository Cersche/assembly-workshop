# Assembly Workshop

Current local app status — 2026-10-19. Configure a Lab Rax rack, select a slot, then design the equipment/tray/faceplate assembly. The app delivers STL files. See [project](../../PROJECT.md), [roadmap](../../ROADMAP.md) and [standing guidance](../../AGENTS.md) for current scope and decisions; dated evidence describes its own snapshot.

## Start and preserve data

Use `start.bat`, which selects `--existing-library --data …/data/normal-use`. Check whether an app server is already running before starting another. Never run bare `python app.py`: its default selects the preserved historical app-local data instead. The usual address is http://127.0.0.1:8765/. Preserve unsaved browser drafts before any separately authorized refresh or restart. Do not replace the app folder or merge data copies as an update procedure.

`../../data/normal-use/` is the official user data. Preserve its database (including any journals/WAL/SHM), immutable revisions and caches, rack workspace/history, equipment assets and artwork together. This app's `data/` and the original beta data are preserved historical copies. Git alone is not a backup. See [data locations](../../docs/housekeeping/Data_Locations.md); do not use active user data for acceptance tests.

Python 3.10 standard library is the development baseline. The documented renderer is `C:/Program Files/OpenSCAD/openscad.exe`; other locations can use `OPENSCAD_EXE` or PATH. The `.com` launcher was reported broken. STEP import uses local FreeCAD. No printer, slicer or filament-profile integration is required.

## Rack studio and explicit Save

The dark hybrid studio uses real source meshes in its rack viewport. The final left grouping is Racks & slots, Equipment and Hardware library; the inspector collapses and has Setup/Hardware/Appearance tabs. Click selects; ellipsis/right-click provides actions. Rack layouts have independent slot assemblies, each with its own hardware pins, inputs and revisions. The legacy shared project is preserved and copied once when creating a new assembly.

One explicit atomic Save persists the draft. Draft edits, checks and exports do not silently save. History restores earlier rack versions as unsaved drafts. Appearance includes presets, custom colors, recent colors and local artwork controls. Rack-view artwork on Pi4 and wizard-made faceplates is a preview; selection outlines follow the plate's U height. Wizard clearance screening reports OK/TIGHT/OVER/UNKNOWN against nominal dimensions; width/depth warnings do not block the wizard and do not establish fit.

## Supported manufacturing paths

- Raspberry Pi 4 tray and faceplate retain their M3 x 0.5 adapter limits and immutable mechanical baseline. The insert-pilot parameter is supported within 3–4.2 mm; catalog breadth does not add geometry support.
- The equipment wizard accepts dimensions, STL, SCAD and STEP (local FreeCAD), using `equipment_tray.scad` as a second adapter. Generic trays and faceplates support 1U–5U. Snap tabs, clips, pegs, straps, keystones, single-piece joints, rear support and multi-U spacing remain unprinted.
- PRINT THE RACK (`/api/rack-stl`) is in scope. Each 1U support extension occupies its own U between posts; post U plus extension U equals rack height. Joints are movable. Creator meshes stay local under the documented BY-NC-SA/personal-use direction and are never redistributed.
- Every faceplate U gets four rack holes, two per side. Corner radius is limited to 2.5 mm. These choices do not establish printed fit or strength.

STLs follow the project's millimeter convention and assembly coordinates; STL itself has no unit field. Normal tray/faceplate STLs, rack STLs and wizard equipment STLs never contain color or artwork. Failed checks block the affected proposed export. All proposals remain **PROPOSED — UNVALIDATED**.

## Faceplate artwork and Print in color

Local PNG, JPEG, WebP, GIF, BMP, AVIF and SVG artwork is converted to a PNG preview of at most 1024 px / 1.4 MB. Rack-view images on wizard faceplates are preview-only and kept clear of openings; wizard Print in color is not supported.

The opt-in Pi4 **Print in color** path (`faceplate_color.py`, `/api/faceplate-colors/preview|export`) uses saved image/settings to produce one STL per filament color for the Raspberry Pi 4 faceplate only. Printed color result, fit and strength remain UNKNOWN. Further artwork-to-STL work requires Brian's direction. See [artwork report](../../work/faceplate-refinement/Report.md). The standing guidance's older sentence saying wizard faceplates do not show images is superseded by the later implementation recorded in HANDOFF.md; it does not expand artwork-to-STL scope.

## Cabling planner

Rear view, Cables see-through mode and saved cable-guide placement are implemented. Port planning includes the Pi4 preset, wizard Ports step, markers, selection and mesh-click placement. The Pi4 preset's face is UNKNOWN; its solid faceplate does not imply connector openings. Ports are planning data, not STL changes. Cable routing, suggestions and the wiring sheet are not built. Lengths are planning estimates; guide/cable fit, capacity and strength remain UNKNOWN.

The Lab Rax Cable Guide by mklements (MakerWorld Exclusive License) is local preview only: never redistributed or included in PRINT THE RACK. See [cabling reports](../../work/cable-management/Step2_Report.md).

## Hardware library and checks

The local SQLite library supports immutable hardware revisions, explicit atomic JSON imports, pinned selections, structured filters, replacement comparisons and optional local catalog packs. Imports do not repin projects; draft does not save. Pack availability and metadata coverage do not certify geometry or physical fit. See [hardware-records](hardware-records.md) for schema, provenance and UNKNOWN limits. Supplier/Pi assets with unresolved rights stay local.

Checks cover screw reach, thread compatibility, open-insert bore envelopes, pockets, supplier hole maxima and applicable documented wall limits. Missing outside diameter is displayed as a labeled unknown rather than an invented body. The Pi4 BOM uses two screws and two inserts; do not infer a full rack BOM from that adapter count.

## Artifact integrity and local reference limits

Pi4 renders use the separate `pi4-mesh-v2-triangulation1` identity namespace. `integrity.json` hashes source, STLs, viewer geometry and revision report; cache reuse/download revalidates exact correspondence. Old immutable caches are preserved. Entries lacking the manifest cannot use the integrity-checked download endpoint; corrupt entries are blocked rather than overwritten.

A bounded export operation removes an exact zero-area collinear triangle and splits its unique long-edge neighbor at the existing interior vertex, retaining coordinates, surface and orientation. Ambiguous repairs are rejected. Raw and processed hashes and the repair trace are recorded in revision.json; strict mesh checks follow. This is not general mesh repair.

Mesh checks cover finite coordinates, nondegenerate unique triangles, two incident triangles per edge, consistent winding and positive signed volume. They do not establish self-intersection absence, vertex manifoldness, full clearance, containment, strength or fit. Reference meshes remain separate from manufacturing parts. Historical reference/joint checks are bounded surface screens, not whole-Pi conversion or access validation. Their immutable evidence is preserved; do not rerun old geometry scripts as routine setup.

## Verification and remaining UNKNOWNs

Run `powershell -File outputs/Mechanical_Design_App/run_checks.ps1` from the project root. It starts no server and runs no OpenSCAD build; tests use temporary data. The 2026-10-19 task-01 baseline passed 52 Python and 20 JS tests. See [baseline report](../../work/codex-tasks/01-run-checks-baseline-REPORT.md) for exact results and the process-scoped PowerShell invocation used on this PC. Page-level save/viewer coverage is separate work; test counts describe a dated run, not physical approval.

Brian confirmed qualitative fit only for the earlier two-hole, 3 mm, square-corner Clearance v2 specimen. That evidence does not transfer to the four-hole 4 mm plate, wizard parts, rack-frame exports or Print in color result. Physical testing is deferred until Brian directs it. Strength, retention, installation, usable depth, unsupported dimensions, generic FDM wall/process/load guidance, whole-solid containment, tool/insertion paths and service/cable access remain UNKNOWN where not established. No printer details are needed to continue software work.

No automatic builds, printing, purchases, uploads, release packaging, publishing, deployments or pushes. Fresh desktop control requires approval. Niche insert research is parked; preserve baseline assets, project pins, all work/outputs and historical evidence.
