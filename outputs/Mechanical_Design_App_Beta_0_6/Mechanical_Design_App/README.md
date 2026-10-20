# Assembly Workshop â€” local beta 0.2

First runnable implementation of the new mechanical design app baseline. This release implements the local hardware and joint-check workflow; it is not yet a CAD editor.

## Run

On Brian's current PC, double-click `start.bat`, then open **http://127.0.0.1:8765** in a browser. The launcher uses the existing Python 3.10 installation. It does not open or control any desktop app automatically. Close the terminal or press Ctrl+C to stop.

On another machine with Python 3.10+, run `python app.py`. No third-party packages or internet connection are needed. Use `--port 8766` if the default port is occupied, or `--data PATH` for a different local data directory. The server listens only on the loopback interface.

## Implemented

- Local SQLite catalog with immutable part revisions and atomic JSON-array imports.
- M1â€“M8 size coverage, including common intermediate sizes. Empty categories are explicitly awaiting sourced parts.
- Search/filter, record inspection, custom example records and JSON file import.
- One persisted Pi4 beta project with pinned hardware snapshots and editable joint dimensions.
- Thread/pitch, screw reach, usable engagement, threaded-shank, insert pocket, installation-hole and boss-wall checks. Missing data stays unknown.
- Saved project JSON and a BOM for the two Pi4 joint screws/inserts. Quantities are specific to this project.
- No desktop control, printing, ordering or external uploads.

## Try it

1. Click **Show custom examples**, then **Import records**. These are fictional records, conspicuously labeled; they do not represent sourced products.
2. Select the example screw and insert. Save and check the joint. The short example screw fails the default engagement target; changing the stack demonstrates the rule without claiming physical suitability.
3. Import exact manufacturer records to replace example selections. To change an existing record, increase its revision; existing projects keep their pinned selection.
4. Export the BOM and project. Back up the `data/library.sqlite3` file with the app stopped to preserve the full catalog.

Part fields and units are described in `hardware-records.md`. Source completeness is declared by the importer, not independently certified by the app. Hardware CAD files, local asset import, geometry feature generation, project re-import/multiple-project UI, installation-tool envelopes and 3D visualization are not implemented yet. No supplier catalog is bundled, and full M1â€“M8 product coverage is not complete.

Checks are dimensional aids. They cannot establish strength, torque, material suitability or physical fit. An open-ended insert always leaves screw-tip clearance unresolved until geometry is checked. Countersunk screws are intentionally reported as unsupported for reach calculation.

## Validation

Run `python -m unittest -v test_app.py`. Tests exercise persistence, immutable revisions, atomic import rollback, numeric validation, thread mismatch, reach and bottoming, pinning after updates, HTTP request handlers in memory, session-token enforcement and exports. The five tests pass. An attempted live loopback HTTP integration test was blocked by Windows socket permissions in this execution environment; end-to-end browser operation remains unverified. UI markup is included but visual browser testing has not been performed in this session, because desktop access was not requested.


## Version 0.2 — sourced starter hardware

Six records now load automatically on startup: Accu M3 socket-cap screws at 6, 8 and 10 mm, and McMaster M3 brass inserts at installed lengths 3.4, 4.3 and 5.7 mm. Supplier links and retrieval date are stored per part in starter-hardware.json. Screw records are documented nominal dimensions; insert records are partial because outside diameter, usable thread depth and minimum wall were not established. No CAD models are bundled.

The McMaster 4 mm value is a maximum installation-hole diameter, not an exact target. The app now checks the maximum separately and keeps the exact printed-hole recommendation unknown. With the current provisional 4.2 mm Pi4 pilot, that maximum check fails. The app does not alter the tray or auto-select hardware.

To update an existing installation: stop the old server with Ctrl+C, copy these application files into its existing folder, and keep its data directory. Start it again and refresh the browser. Startup adds missing starter records without overwriting existing records or project selections. Alternatively extract to a new folder for a separate installation. Do not run both versions on the same port simultaneously.

Version 0.2 validation: seven automated tests pass, including catalog seeding without duplicate records or selection changes and the distinction between a maximum and an exact hole recommendation. Browser visual testing remains based on Brian's supplied version 0.1 screenshot; no desktop control occurred for this update.


## Version 0.3 — joint axial geometry

Save & check now shows a to-scale axial preview of screw length, insert body length and available bore depth. Geometry JSON can be exported. Open inserts now receive a separate screw-tip/bore-envelope check, while physical bottom clearance remains unknown. The assumed continuous bore and entered stack are stated in the preview; this is not a full 3D geometry check. No CAD/STL modifications occur.

For the screenshot combination (10 mm screw, 4.3 mm insert, 3.3 mm stack and 8 mm available bore), the computed reach is 6.7 mm, extension beyond the insert body is 2.4 mm and modeled bore-end gap is 1.3 mm. Actual usable thread depth and insert outside diameter are still not verified from the accessible supplier source. We do not substitute body length for usable thread depth. The original 4.2 mm pilot still fails the supplier maximum check.

Eight automated tests pass, covering the geometry endpoint and open-insert bore overrun. Desktop/browser inspection was not performed. Update by stopping the server, replacing application files while retaining data/, restarting and refreshing the browser.


## Version 0.4 — Phase 4 of 7

The app displays the seven-phase roadmap with Phase 4 (geometry integration) in progress and three phases complete. This is milestone position, not a percentage-of-effort estimate.

The axial preview loads on startup and updates automatically when selections or dimensions change. Draft previews do not save or change project selections; Save project and Save & check remain explicit persistence actions. Exports save current inputs first. Pending preview responses are discarded when a newer edit is made. A bore envelope is visible even before hardware is selected. This also addresses the blank initial preview shown in the previous screenshot.

Nine backend tests pass, including HTTP preview handling and confirmation that drafts never alter the saved project. Frontend JavaScript passes Node syntax checking. This update has not been visually inspected in a live browser. No desktop access, printer actions or manufacturing geometry changes occurred.

Update: stop the server, replace application files while retaining data/, restart start.bat, and refresh the browser. Next Phase 4 milestone is integrating actual assembly/reference geometry; this release still uses an axial model.


## Version 0.5 — actual assembly inspection (Phase 4 of 7)

Includes an offline, rotatable orthographic canvas view of the actual clearance-v2 tray and faceplate: 10,340 and 1,220 triangles respectively. Controls support drag/arrow-key rotation, zoom, top view, reset, hiding parts and focusing the right joint. Original millimeter coordinates are preserved; assembly.json records source STL SHA-256 hashes and bounds. No external JavaScript libraries, model downloads or network services are needed.

The assembly view is read-only and independent of the hardware-input axial preview. It excludes the Pi board, screws and inserts. Changes to pilot or hardware selections do not regenerate assembly meshes. The software painter renderer may show ordering artifacts at intersecting surfaces and is not a boolean or collision engine.

Validation: ten Python tests pass, both JavaScript files pass Node syntax checks, and a mocked-canvas runtime check exercises finite projection coordinates, initial rendering, visibility, joint focus, top and reset. These do not replace browser visual QA, which remains pending. No desktop access or printing occurred.

Update by stopping the server, copying all application files (including assembly.json and viewer.js) into the existing app folder while keeping data/, restarting start.bat and refreshing the browser.


## Version 0.6 — selected hardware at actual joints (Phase 4 of 7)

Draft selections now drive nominal 3D hardware envelopes at both clearance-v2 joint axes, X=+/-40, Z=21 mm, along Y. Screw bearing surfaces stay at Y=11.3 mm. Shanks extend toward -Y by under-head length; head envelopes use recorded head diameter and height. The insert entrance is Y=11.3 minus the entered stack. Changing the stack moves the insert reference only; it does not move the actual ear or regenerate its geometry.

An insert with unknown outside diameter shows a dashed axis of the known body length, not an invented cylinder. Dashed axes are drawn through surfaces for visibility. If the user supplies an outside diameter, a nominal cylindrical outer envelope is shown; it is not a knurled/threaded solid. The starter McMaster records still lack that dimension.

Toggle Selected hardware to hide all hardware references. Clear or invalid draft inputs remove stale hardware geometry while the new preview is pending. No model mesh changes, thread rendering or collision-validation results are produced. The Pi remains excluded from this release.

Validation: eleven Python tests pass, both JavaScript files pass syntax checks, and a mocked-canvas runtime test checks hardware event rendering, visibility and camera controls. Live browser inspection remains pending; no desktop control occurred. Update by stopping the app, replacing application files while keeping data/, restarting and refreshing.
