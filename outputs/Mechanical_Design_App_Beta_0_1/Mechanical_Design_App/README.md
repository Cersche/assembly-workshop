# Assembly Workshop â€” local beta 0.1

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
