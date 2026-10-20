# Cable management Step 3: cables, exits and outside endpoints (2026-10-19)

Built from Brian's 14 decisions in [Step3_Decisions.md](Step3_Decisions.md). Claude and Codex split the work so they never edited the same file. Cabling stays **planning data only**: no geometry, STLs or hardware pins. It saves only through the explicit Save and lands in rack history. Lengths are planning estimates. Cable outer diameter, stiffness, connector depth, guide capacity and rear clearance stay **UNKNOWN**. The Pi 4 is only sample equipment: nothing here is Pi-specific.

## What was built
- **Codex [task 09](../codex-tasks/09-cable-schema-REPORT.md):** `cable_plan.py` plus `rack_workspace._cabling`. Save validates `exits`, `endpoints`, `cables` and `settings`: references, one cable per port, unconnected ends, bounds and unknown keys. Brian approved updating one obsolete Step 1 test (`cables` used to be an unknown key).
- **Codex [task 10](../codex-tasks/10-cable-routes-logic-REPORT.md):** `cable-routes.js` (`LabRaxCables`) handles automatic routing through the nearest guides on one post, exit choice, length estimates, keystone links, port-in-use checks, C-numbers, crowding, upkeep and warnings. 18 Node tests. The API matches the contract exactly. Known limit: on a manual route, a *moved* guide is detected only within one page session; a removed one is always detected.
- **Claude:**
  - `cable-view.js`: tubes with sag and side-by-side bundling, grommets and exit rotations. 4 Node tests in `js-tests/run.js`.
  - `rack-studio.js`: parts can carry their own mesh; cable and exit colours with brighten and dim; `pickCable` and `pickExit`. The asset manifest hash was refreshed.
  - `workspace.js`: Connect mode, the one-time face question, reattaching an unconnected end, the Cable panel, rack-level Setup lists (exit points, outside endpoints, cables, settings), a **Cable runs** toolbar toggle, endpoint arrows labelled with the endpoint's name, and upkeep on every draft change and before Save.
  - `index.html` and `app.py` load and serve the two new scripts. Some CSS was added.
- **Existing bugs fixed:**
  - Removing the last cable guide deleted the whole `cabling` block, including port edits.
  - Editing the rack settings dropped `cabling` when it held no guides.

## Verified
- `run_checks.ps1`: **all checks passed**, 71 Python tests and 94 JavaScript tests (24 module, 27 page logic, 16 BOM, 9 rebuild, 18 cable routes).
- Browser check on a disposable copy of `data/normal-use` (server `disposable-cables3-8775`, my scratchpad; the original was only copied, never written), with no console errors:
  - Added two RR guides, a bottom-rear exit and an "Office wall outlet" endpoint.
  - Pi Ethernet → Connect → endpoint created C1, routed RR U01 → RR U02 → exit, ≈ 0.7 m.
  - The face question appeared; "Rear" saved as a port face edit.
  - Save → the file on disk held all of it → reload → the tube drew in the Rear view with the label "C1 → Office wall outlet". Clicking the tube selected C1.
  - Removing a guide re-routed the automatic cable (≈ 0.6 m). Choosing an exit made the route manual. Removing that exit showed "route changed" and "no exit" warnings.
  - Releasing the Pi's slot left C1 with "From: Unconnected" and Reattach. That saved correctly, and the released Pi's port edits were dropped.
- Two bugs found during the check were fixed:
  - The renderer's bounds calculation crashed on parts that carry their own mesh.
  - Cables starting at an endpoint drew in the wrong order.
- Wording fix: with no exit, the length reads "to the last guide (no exit yet)".

## Not verified
- **Not clicked in the browser:** a port-to-port connection. The Browser pane went hidden mid-test, so the page stopped redrawing. The logic is covered by the Node tests.
- **Not seen in a browser at all:** the keystone link, crowding warnings and wizard-equipment cables. The copied data has no wizard equipment; Node tests only.
- **Not looked at after their last edits:** the label clamp and the drawing order for endpoint-first cables. The code was checked and the tests pass.
- No exports, printing, commits or pushes. The normal 8765 server still runs the old code until Brian restarts it with start.bat.

## Next
Step 4 is suggestions and Step 5 is the wiring sheet. The backlog: a quicker way back to the rack-level panel from a slot (today it's the rack dropdown).
