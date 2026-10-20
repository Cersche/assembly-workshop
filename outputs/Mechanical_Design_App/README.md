# Assembly Workshop

Current local app status — 2026-10-19. Configure a Lab Rax rack, select a slot, then design the equipment/tray/faceplate assembly. The app delivers STL files. See [project](../../PROJECT.md), [roadmap](../../ROADMAP.md) and [standing guidance](../../AGENTS.md) for current scope and decisions; dated evidence describes its own snapshot.

## Start and preserve data

Use `start.bat`, which selects `--existing-library --data …/data/normal-use`. Check whether an app server is already running before starting another. Never run bare `python app.py`: its default selects the preserved historical app-local data instead. The usual address is http://127.0.0.1:8765/. Preserve unsaved browser drafts before any separately authorized refresh or restart. Do not replace the app folder or merge data copies as an update procedure.

`../../data/normal-use/` is the official user data. Preserve its database (including any journals/WAL/SHM), immutable revisions and caches, rack workspace/history, equipment assets and artwork together. This app's `data/` and the original beta data are preserved historical copies. Git alone is not a backup. See [data locations](../../docs/housekeeping/Data_Locations.md); do not use active user data for acceptance tests.

Python 3.10 standard library is the development baseline. The documented renderer is `C:/Program Files/OpenSCAD/openscad.exe`; other locations can use `OPENSCAD_EXE` or PATH. The `.com` launcher was reported broken. STEP import uses local FreeCAD. No printer, slicer or filament-profile integration is required.

## Rack studio and explicit Save

The dark hybrid studio uses real source meshes in its rack viewport. The final left grouping is Racks & slots, Equipment and Hardware library; the inspector collapses and has Setup/Hardware/Appearance tabs. Click selects; ellipsis/right-click provides actions. Rack layouts have independent slot assemblies, each with its own hardware pins, inputs and revisions. The legacy shared project is preserved and copied once when creating a new assembly.

One explicit atomic Save persists the draft. Draft edits, checks and exports do not silently save. History restores earlier rack versions as unsaved drafts. Appearance includes presets, custom colors, recent colors and local artwork controls. Rack-view artwork on historical reference and wizard-made faceplates is a preview; selection outlines follow the plate's U height. Wizard clearance screening reports OK/TIGHT/OVER/UNKNOWN against nominal dimensions; width/depth warnings do not block the wizard and do not establish fit.

## Supported manufacturing paths

The equipment wizard is **Device → Holes → Ports**: record equipment size/model, mounting holes and ports. Tray choices live in **Place on tray**, which opens when placing a library item in a slot or from that slot's button. Choose position, rotation, mounting, standoff, faceplate height, keystones, joint and rear support there. Apply changes only the draft; explicit Save persists `placement.tray`, containing only values that differ from the library item.

Cable ports and clearance screening use each slot's tray settings. With no slot tray settings, the rack shows the library item's build. Otherwise it uses an existing exact render from Place on tray → Render exact preview or Generate; `/api/equipment-placement-mesh` only looks it up, never renders. Without one, it shows a box sketch of plate U height, tray size/offset/rotation, rear bracket and dark blocks for keystone/port openings; the inspector identifies the sketch. Keystone faceplates now pass the mesh check; fit, retention and strength remain UNKNOWN.

Preview quality **Low / Medium / High** is a per-viewer browser preference only. Export quality **Draft / Standard / Fine** sets OpenSCAD `$fn` to **24 / 48 / 96** for `equipment_tray.scad` STLs (`equipment.EXPORT_QUALITY`). It changes curve detail; fit and strength remain UNKNOWN at every level.

- All equipment uses the generic `equipment_tray.scad` adapter (1U–5U), including the bundled historical board example. The example is not selected on startup. Reading the library never builds geometry or writes user data; an unrendered example shows a box sketch.
- Rack-frame STLs remain a separate PRINT THE RACK export. Creator assets stay local.
- Legacy slot ids migrate to the example in memory; the original saved document is preserved byte-for-byte in rack history. The converted draft requires explicit Save. Hardware snapshots, artwork and port overrides are retained; historical physical fit does not transfer to the generic geometry.
- Artwork stays preview-only for generic equipment. Print in color is not available for these faceplates yet: the retired color adapter uses a fixed 3 mm front face and fixed artwork window; generic faceplates use 4 mm and variable heights/openings. Saved artwork and filament settings remain preserved. Printed color result, fit and strength remain UNKNOWN.

## Cabling planner

Rear view, Cables see-through mode and saved cable-guide placement are implemented. Port planning includes library planning ports, wizard Ports step, markers, selection and mesh-click placement. The example's port face is UNKNOWN; its solid faceplate does not imply connector openings. Ports are planning data, not STL changes. Cables connect ports or outside endpoints through automatic or manual routes and exits. Review offers routing suggestions and a saved-rack wiring sheet, cable schedule CSV and wrap labels. Suggestions are advice only; Apply changes the draft. Lengths are planning estimates; guide/cable fit, capacity and strength remain UNKNOWN.

The Lab Rax Cable Guide by mklements (MakerWorld Exclusive License) is local preview only: never redistributed or included in PRINT THE RACK. See the [ports](../../work/cable-management/Step2_Report.md), [routes](../../work/cable-management/Step3_Report.md), [suggestions](../../work/cable-management/Step4_Report.md) and [wiring sheet](../../work/cable-management/Step5_Report.md) reports.

## Hardware library and checks

The local SQLite library supports immutable hardware revisions, explicit atomic JSON imports, pinned selections, structured filters, replacement comparisons and optional local catalog packs. Imports do not repin projects; draft does not save. Pack availability and metadata coverage do not certify geometry or physical fit. See [hardware-records](hardware-records.md) for schema, provenance and UNKNOWN limits. Supplier/Pi assets with unresolved rights stay local.

Checks cover screw reach, thread compatibility, open-insert bore envelopes, pockets, supplier hole maxima and applicable documented wall limits. Missing outside diameter is displayed as a labeled unknown rather than an invented body. The historical reference BOM uses two screws and two inserts; do not infer a full rack BOM from that adapter count.

## Artifact integrity and local reference limits

historical reference renders use the separate `historical reference-mesh-v2-triangulation1` identity namespace. `integrity.json` hashes source, STLs, viewer geometry and revision report; cache reuse/download revalidates exact correspondence. Old immutable caches are preserved. Entries lacking the manifest cannot use the integrity-checked download endpoint; corrupt entries are blocked rather than overwritten.

A bounded export operation removes an exact zero-area collinear triangle and splits its unique long-edge neighbor at the existing interior vertex, retaining coordinates, surface and orientation. Ambiguous repairs are rejected. Raw and processed hashes and the repair trace are recorded in revision.json; strict mesh checks follow. This is not general mesh repair.

Mesh checks cover finite coordinates, nondegenerate unique triangles, two incident triangles per edge, consistent winding and positive signed volume. They do not establish self-intersection absence, vertex manifoldness, full clearance, containment, strength or fit. Reference meshes remain separate from manufacturing parts. Historical reference/joint checks are bounded surface screens, not whole-Pi conversion or access validation. Their immutable evidence is preserved; do not rerun old geometry scripts as routine setup.

## Verification and remaining UNKNOWNs

Run `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1` from the project root. It starts no server and runs no OpenSCAD build; tests use temporary data. Verified 2026-10-19: **95 Python + 152 JS tests passed**, including page-level Save, viewer startup, tray placement and cable inventory. See the [baseline report](../../work/codex-tasks/01-run-checks-baseline-REPORT.md) for the earlier run and the [page-logic report](../../work/codex-tasks/03-page-logic-tests-REPORT.md) for the expanded suite. ExecutionPolicy Bypass applies only to this process and changes no persistent system setting. Test results do not establish physical approval.

Brian confirmed qualitative fit only for the earlier two-hole, 3 mm, square-corner Clearance v2 specimen. That evidence does not transfer to the four-hole 4 mm plate, wizard parts, rack-frame exports or Print in color result. Physical testing is deferred until Brian directs it. Strength, retention, installation, usable depth, unsupported dimensions, generic FDM wall/process/load guidance, whole-solid containment, tool/insertion paths and service/cable access remain UNKNOWN where not established. No printer details are needed to continue software work.

No automatic builds, printing, purchases, uploads, release packaging, publishing, deployments or pushes. Fresh desktop control requires approval. Niche insert research is parked; preserve baseline assets, project pins, all work/outputs and historical evidence.
