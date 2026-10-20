# Assembly Workshop — beta 0.8

**Phase 4 of 7: Geometry integration, in progress.** Three roadmap phases are complete. Mesh generation and comparison are implemented; live browser verification of this release is pending.

## Start or update

Stop the previous app with Ctrl+C. Copy all files from this release into the app folder, retaining its existing `data/` directory. Run `start.bat`, then open http://127.0.0.1:8765 and refresh the browser. On another machine use Python 3.10+ and `python app.py`.

Mesh generation uses the local OpenSCAD command-line executable. This PC has it at `C:/Program Files/OpenSCAD/openscad.exe`. Other installations can set `OPENSCAD_EXE`, or put openscad on PATH. Rendering runs without opening a desktop window. Source-only export still works if OpenSCAD is unavailable. There is no purchasing, printing, desktop control or cloud upload feature.

## Generate and compare the trial revision

1. Select Accu M3 x 8 and McMaster M3 heat-set 5.7 mm.
2. Set the installation pilot to **4.0 mm** as a trial. Retain stack 3.3, available pocket 8 and boss diameter 9 mm.
3. Click **Generate & show proposal**. The render can take about a minute. Both tray and faceplate are rendered from the exact proposed source and checked for closed mesh edges.
4. Use **Show baseline v2** and **Show generated proposal** to switch views. The canvas label identifies the displayed revision. Show the faceplate to inspect its bores; Reveal right joint intentionally hides it.
5. Click **Download matching revision package**. It includes `pi4_proposed.scad`, `tray.stl`, `faceplate.stl`, `assembly.json` and `revision.json` with pinned hardware, unresolved checks, render logs, mesh hashes and build ID.

Draft generation does not overwrite the baseline or save project selections. Save project / Save & check are explicit persistence actions. Changing an input invalidates the current build controls and returns the view to baseline. Repeating an identical build reuses its matching cache under `data/revisions/`. The bundle is tied to the build ID, not later form changes.

The current Pi4 adapter changes **only the faceplate insert-pilot parameter**, within 3–4.2 mm, for M3 x 0.5 hardware. Unsupported geometry changes or failed dimensional checks block generation/export. The 4 mm supplier limit is not a confirmed printed-hole recommendation. Insert outside diameter, usable thread depth and required wall guidance remain unknown in the partial catalog entries. All generated proposals remain **PROPOSED — UNVALIDATED**.

## Other implemented features

- Local SQLite hardware library, immutable revisions, atomic JSON imports and pinned project selections.
- Six sourced M3 starter records with supplier links; common M1–M8 size families show actual catalog coverage. Full catalog expansion is Phase 6.
- Live draft axial and 3D hardware envelopes. Missing insert outside diameter is represented by a labeled dashed axis, not a fabricated body.
- Read-only assembly orbit, zoom, hide/show, joint focus and baseline/proposal comparison.
- Screw reach, thread compatibility, open-insert bore envelope, pocket, hole maximum and documented wall checks; unknowns stay unknown.
- BOM and project JSON exports. The BOM quantities are fixed at two screws and two inserts for this Pi4 project.

## Validation and limits

Thirteen automated Python tests pass. JavaScript syntax checks and mocked-canvas controls/model-switching tests pass. A real OpenSCAD integration test rendered both parts, verified mesh closure, exercised cache reuse, and checked that each packaged STL hash matches the viewer asset and the exported source is exact.

This release has not been visually exercised in a live browser. Earlier viewer versions were visually confirmed using Brian's screenshots. No desktop control or printing occurred during this update.

Mesh closure and rendering do not establish interference-free assembly, strength or physical fit. The viewer does not include the Pi reference yet and performs no collision check. Full Pi4 reference validation is Phase 5. Material, actual insert installation, tool access, rack fit and physical prototype testing remain outstanding. The simple triangle painter can show surface-order artifacts.

Hardware records use millimeters; see `hardware-records.md`. Examples are fictional and clearly labeled. CAD models for hardware are not bundled. Catalog verification status is a recorded assertion rather than independent certification. Source data and downloaded models retain their original use restrictions.

Run `python -m unittest -v test_app.py` for the automated test suite. Back up `data/` with the app stopped to preserve catalog, selections and generated revisions.
