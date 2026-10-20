# Equipment wizard: end-to-end acceptance run (2026-10-19)

**Verdict: the wizard works end to end.** Every stage passed in the built-in browser on disposable data. Two small display bugs were fixed. No blocking bugs were found. There are some design questions for Brian (below). Nothing is committed. Fit, retention and strength stay UNKNOWN.

**Setup:** a fresh copy of the latest scratch data (from the rack-view check), served on port 8791 (`.claude/launch.json` entry `disposable-e2e-8791`). data/normal-use and the live 8765 server were not touched. Test equipment was generic boxes made with local FreeCAD, not the Pi 4. Screenshots are in [e2e-screens/](e2e-screens/).

## Stage by stage

| Stage | Result | What was checked |
| --- | --- | --- |
| 1a. Wizard, typed size only | PASS | "E2E Typed Box" 120 × 80 × 25 mm, 2 holes, front RJ45 "LAN" at X −30, rear DC barrel "Power". Saved to the library. ([1a](e2e-screens/1a_typed_saved.jpg)) |
| 1b. Wizard, STL import | PASS | 140 × 90 × 30 mm box STL read correctly (size filled in). 1 hole, front USB-A, rear RJ45. The wizard blocked a bad rear-port Z with a clear message. ([1b](e2e-screens/1b_stl_imported.jpg), [saved](e2e-screens/1b_stl_saved.jpg)) |
| 1c. Wizard, STEP import | PASS | FreeCAD 1.1 is installed. A 160 × 110 × 35 mm STEP (with a small front button) converted in about 2 s and read as 160 × 113 × 35. 2 holes, front HDMI, rear IEC. ([1c](e2e-screens/1c_step_imported.jpg), [saved](e2e-screens/1c_step_saved.jpg)) |
| 2. Place on tray | PASS | Rack set to 10U through Rack settings to get free slots. All three placed. The window opened each time. Tested: mouse drag (11 mm), Centre/offset field, 90°/180°/270°, 1U→2U, keystones, pegs/clips/straps, standoff 8 and 5 mm, rear support. The keystone collar guard blocked a keystone too close to a wide clip tray. 3U at slot 9 of 10 was refused at Apply. ([2a](e2e-screens/2a_place_on_tray_slot5.jpg), [2b](e2e-screens/2b_place_on_tray_slot7.jpg), [3U refused](e2e-screens/2c_3U_refused_slot9.jpg)) |
| 3. Rack view | PASS | Each slot shows a 2U sketch over the right slots, with the port and keystone openings where they were entered. Front cable markers sit on the openings. Rear-port markers moved with each slot's rotation and offset (Power on the Typed Box sits at the device's left edge after 90°, as expected). ([front](e2e-screens/3a_front_view_sketches.jpg), [markers](e2e-screens/3b_cables_markers.jpg), [rear](e2e-screens/3c_rear_markers.jpg)) |
| 4. Save and reload | PASS | Saved tray settings for all three slots were in rack-workspace.json. After a page reload, the slot 5 window showed the same values (11 mm, 90°, pegs, 8 mm, 2U, keystone 70). ([4](e2e-screens/4_after_reload_slot5.jpg)) |
| 5. Exact preview and STLs | PASS | Slot 5: Render exact preview in about 15 s, then Generate proposed STL files. The tray and faceplate STLs pass `read_mesh` with no repair nudge. The zip's revision.json matches the slot's settings. The rack view switched to the exact mesh and stayed exact after reload. Slots 7 (clips, 180°) and 9 (straps, 270°, rear support + bracket) also rendered with no nudge. ([5a](e2e-screens/5a_exact_preview.jpg), [5b](e2e-screens/5b_rack_exact_mesh.jpg)) |
| 6. Review tab | PASS | Clearance screening lists all three with sensible numbers (rotated sizes used). A new cable (Typed Box LAN → STL Hub USB, C4) was planned and saved. Parts order shows C4 and 4 keystone jacks (1 old + 3 new). Wiring sheet SVG, schedule CSV, labels and parts CSV were all produced from the saved rack, and the sheet draws all three 2U items and C4 in the right place. ([parts](e2e-screens/6a_review_parts_order.jpg), [sheet](e2e-screens/6b_wiring_sheet.jpg)) |

## Bugs fixed

1. **Status line shown twice on library cards.** New items showed "Matches current source; build process unknown" twice (badge plus reason with the same text). Now the reason only shows when it adds something. `equipment-wizard.js`; test in `js-tests/equipment-rebuild.js` (fails on the old code).
2. **Wizard summary miscounted ports.** It said "1 ports" for an item with one front and one rear port. It now says "1 front opening, 1 rear port" with correct plurals. `equipment-wizard.js` (`summary()`); test in `js-tests/equipment-wizard-steps.js`.

Both were checked in the browser after the fix. `run_checks.ps1`: **102 Python (1 skipped) + 155 JS, all pass** (was 102 + 153).

## Notes from the run (not app bugs)

- **The Generate button also downloads the zip.** In the built-in browser it landed in Downloads as a `.tmp` file. I moved it to the session scratchpad. Brian's real Downloads folder has no files from this test.
- The built-in browser pane does not open new tabs, so "Open printable sheet" and "Labels" were checked by capturing the page they produce, not in a real tab. The earlier Chrome check covered real tabs.
- While the browser pane is hidden, the rack view pauses drawing, so a slot can read "sketch" for a moment after reload. On screen it switches to the exact mesh as expected.

## Questions for Brian (design choices, not decided)

1. **Front openings stay where they were entered.** When you drag, rotate or change the standoff in Place on tray, the device moves but its front-port openings do not (the code says this is on purpose). Example: after an 11 mm drag, the LAN opening is 11 mm away from the real LAN jack. After 90°, the jack faces the side, but the opening is still cut. Options: keep as is; make openings follow offset and standoff; or warn when they no longer line up.
2. **Rear-support trays always screen as TIGHT** (240 of 240 mm), because the tray runs to the back posts by design. Should that read OK-by-design instead?
3. **2U plate across a support extension.** After resizing to 10U, the 1U extension sits at U06. The Typed Box plate spans U05–U06 across that joint, and nothing flags it. Is that allowed?
4. **Mixed-connector cables.** A cable from an RJ45 port to a USB-A port is accepted with no warning (it lists as RJ45).
5. **Port type does not set a size.** Choosing RJ45 or HDMI keeps the default 15 × 8 mm opening.
6. **Plain wording:** "Choose a whole slot range within the rack" (3U at slot 9 of 10) could say "3U from slot 9 doesn't fit; this rack ends at slot 10". Also, brand-new items show "build process unknown" and offer "Rebuild as new item", which may confuse.
7. **Old milestone wording in the app:** a hidden dashboard still says "Phase 7 of 7 · closed with limitations" and "Complete with limitations".

## Codex

Task 18 ([spec](../codex-tasks/18-placement-render-sweep.md), prompt in `docs/prompts/codex/2026-10-19_wizard-e2e_task-18.md`): a report-only render sweep of about 30 Place on tray combinations (all mounts × rotations, offsets, standoffs, rear support, 1/2/4U, Draft/Fine, single piece). This run only rendered three combinations. Not run yet.
