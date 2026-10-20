# Cable management Step 2 — ports (2026-10-19)

Ports are **planning data only**. Pi4 manufacturing paths, STL exports and hardware pins are unchanged; `equipment.source()` (and so wizard build hashes) ignores port `type`, `id` and `rear_ports`. Connector fit, plug and cable access, and clearance stay **UNKNOWN**. Which face (front or rear) a cable reaches each Pi 4 port from stays **UNKNOWN** until the user sets it (the faceplate has no openings; the USB-C, micro-HDMI and audio connectors face its rear side about 11 mm away; USB and Ethernet point to the rack's right side, +X).

## What was done this pass

- `register_step2.py` refreshed the `rack-studio.js` SHA-256 in `rack-references/asset-manifest.json` (nothing else touched).
- Wizard Ports step (`equipment-wizard.js`): each row has Type and Face selectors. Choosing Rear moves the row to `spec.rear_ports` (X/Z only, no opening); choosing Front moves it back with a 15 × 8 mm, r 1 default opening. New and suggested ports get `p-` + random ids. A note says keystones become front/rear pass-through ports. Older library items without `rear_ports` get an empty list on edit.
- Code read; fixes made:
  - `cable-ports.js` `basePorts` had an unbalanced parenthesis (a syntax error), so the whole module, and with it the rack view's port features, would not load. Fixed.
  - `positionFromHit` now clamps to the ranges `cable_ports.py` accepts, so a stray mesh click can't make the rack unsaveable.
- Tests:
  - Python `test_cable_ports.py` (added to `work/gui-refinement/check_python.py`): overrides round trip through `rack_workspace` save/read and 16 rejections; `equipment.clean` type, ids, rear ports, reserved `ks-` ids and rejections; `source()` unchanged when type/id/rear ports are added.
  - Node `js-tests/run.js` (5 new): Pi 4 preset, wizard ports and keystone pairs, override merge/reset/custom/prune, proper marker rotations (det = 1, correct outward direction) and allocation base heights, marker meshes for every type.
- `powershell -File outputs/Mechanical_Design_App/run_checks.ps1`: **RESULT: all checks passed** (JS 20/20).

## Browser check (disposable copy of data/normal-use in the session scratchpad, port 8773)

Observed: the slot 1 Pi 4 lists 9 ports, each with face UNKNOWN. Markers are visible inside the see-through trays in Cables view, and clicking one selected Ethernet. In the Port panel, the label, face (Rear) and X edits applied. Mesh-click placement on the slot 1 faceplate set X −49.3, Y −3.0 (the plate front face), Z 13.8. A custom port was added. Save → reload kept "Uplink · RJ45 · Rear · moved" and the custom port. No console errors. In the wizard Ports step, the Type/Face selectors work: Rear removed W/H/r and kept rj45, and the keystone note shows. The wizard spec was not saved (that would build meshes).

Not verified in the browser: wizard-made equipment markers and rear ports in the rack view (the copied data has no wizard equipment). Those code paths are covered by the Node tests only. Normal-use data was not touched. No exports, prints, commits or pushes.
