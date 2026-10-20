# Cable management Step 1: views and cable guides (2026-10-19)

This is Step 1 of the [proposal](Proposal.html), built after Brian's decisions: the guide is a local preview only, ports will come from both a preset/wizard and clicks on the mesh, and Step 1 goes first. Planning notes and placement math are in [Step1_Notes.md](Step1_Notes.md).

## Implemented
- **Cable guide asset:** the supplied Lab Rax Cable Guide (mklements, MakerWorld Exclusive License) is now `rack-references/cable_guide.json`, an exact copy of 352 vertices and 708 triangles made by `convert_guide.py`. It is listed in the asset manifest. Provenance is in [Guide_Provenance.json](Guide_Provenance.json). It is a local preview only: it is not in the catalog or `RACK_PART_SOURCES`, so PRINT THE RACK and `/api/rack-stl` cannot include it. The original 3MF stays in Downloads.
- **Saved guides:** an optional rack field `cabling.guides[]` (`id, kind, post FL/FR/RL/RR, slot`), validated in `rack_workspace._cabling`. It allows one guide per post per U and stays inside the slot count. Racks without it are unchanged. Guides save through the existing explicit Save and rack history. Changing the rack height keeps each guide at the same height above the floor and drops any that no longer fit.
- **Placement:** `LabRaxScene.guidePose` puts the plate flat on the post face (y = 0 for front posts, y = 240 for rear posts), centred on that slot's outer faceplate hole pair (|X| 118.26, U middle ± 15.9), with the loops pointing away from the rack. It uses rotations only.
- **Viewport:** a **Rear** view (straight-on from behind, with back post labels on) and a **Cables** mode. Cables mode hides the side, top and bottom panels and shows the beams, rails, handles, feet and extensions see-through. See-through parts cast no shadows and can't be clicked, so guides behind them can still be selected. Guides render in their own color, independent of the rack paint.
- **Selection and editing:** clicking a guide in the viewport selects it (blue) and opens the Setup tab. With no slot selected, Setup shows **Cable guides**: Add (post + U), select, change post, move up or down 1U, and Remove. All edits stay in the draft until Save. If a guide sits on a 1U support extension, a note says the hole position there is UNKNOWN.

## Verified
- `run_checks.ps1`: 47 Python tests (adds `test_cable_guides_round_trip_and_reject_invalid`) and 15 JS tests (adds a `guidePose` test covering plate on the post face, 1U centred on the slot, the hole column, a proper rotation, and rejection of bad input). All pass.
- Browser check on a disposable server (`disposable-cables-8771`, a fresh copy of the data in this session's scratchpad). Added RL U01 and RR U03, saved, confirmed both in the disposable `rack-workspace.json`, reloaded, and the guides persisted. Checked the Rear view, Cables mode, and click-to-select in the viewport. No console errors. Screenshots: [Rear_View_Guides.jpg](Rear_View_Guides.jpg) was taken before the guide-color fix, so the guide there shows the rack's magenta; [Cables_View_Selected_Guide.jpg](Cables_View_Selected_Guide.jpg) shows Cables mode with a selected guide.
- data/normal-use was only copied, never written. The normal 8765 server was not restarted. It still serves the old code until Brian restarts it.

## Not done or not verified
- The rack STL export was not run. Its exclusion of guides was checked by reading the code only.
- No canvas right-click menu for guides (the list buttons cover the actions), no drag-to-move, and no guides on the front-view post labels.
- Ports, cables, exits and endpoints, suggestions and the wiring sheet are Steps 2–5.
- Guide fit, M6 hole compatibility, cable capacity, retention and strength are UNKNOWN. Nothing was printed.
