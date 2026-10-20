# Wizard design picks — built (2026-10-19)

Brian's seven answers to the questions in the [end-to-end report](E2E_Acceptance_Report.md) are built. Nothing is committed yet. Fit, retention and strength stay UNKNOWN.

## What changed

1. **Front openings follow the device.** In Place on tray, the faceplate openings for front ports now move with the left/right offset and the standoff change (also strap mounting, which has no standoff). This applies to the STL source (`equipment.allocation_spec`), the rack sketch, the cable port markers, the Place on tray top view (orange outlines on the faceplate strip) and the image-clearance area. A slot with no tray changes builds exactly as before.
   - **Turned device (90°, 180°, 270°):** the openings stay where they were entered, with no guessing. Place on tray shows a plain warning saying the openings no longer line up and that the STL keeps them where they were entered. 180° says the ports now face the rear.
   - **Guards:** a moved opening that runs past the plate edge, off the top or bottom, or into a keystone is blocked, in plain words, both in the window and on the server. The existing checks are unchanged.
2. **Rear-support depth** now reads "OK (by design)" when the tray runs exactly to the 240 mm back posts. A device that goes past them is still graded normally.
3. **Plate across a support extension:** a multi-U plate covering a 1U extension slot gets a warning (slot Setup, Review, Place on tray). It never blocks.
4. **Mixed connectors:** a cable joining two different connector types, for example RJ45 to USB-A, warns "Needs an adapter cable". The warning shows in the Cable panel, the wiring sheet notes and CSV, the Review suggestions (INFO) and the parts order. It never blocks.
5. **Starting opening sizes:** a new front port added by hand gets a size for its type (RJ45 17×14, USB-A 15×8, USB-C 12×7, HDMI 17×8, micro-HDMI 11×7, DC barrel 11×11, IEC 28×20, other 15×8), labelled "a guess, not a measured size". Changing the type updates it until you edit W/H/r. Saved ports and ports found from a model keep their sizes.
6. **Plain wording:** "3U from slot 9 doesn't fit; this rack ends at slot 10." Items built from the current template now say "Up to date: built from the current template" and offer no Rebuild. Only older-template items offer "Rebuild as new item".
7. **No phase wording:** the hidden "Phase 7 of 7 · closed with limitations" card is now a short "Project status" note.

## Tray screw joints move clear of openings (Brian, 2026-10-19, after Codex task 18)

Codex's render sweep (task 18: 24 pass, 2 fail, 4 skip) found one real defect. A front opening sitting in front of a tray screw joint is blocked by the joint's block and post, which stand up to about 29 mm behind the faceplate. When an opening edge lands exactly on the screw hole, the faceplate also fails the mesh check (1U straps case). Brian chose option 3:

- Each screw joint now sits where it clears the openings (joint ± 9 mm, up to 29 mm high, plus 1 mm clearance) and the keystones (16 mm, as before). The default spot (±40 mm, or nearer the centre on narrow trays) is kept whenever it is clear, so those designs build exactly as before. Otherwise the nearest clear spot on that side is used, between 10 mm from the centre and 12 mm inside the tray edge. Example: a 101 mm tray with an opening at −30 mm gets its left joint at −12 mm.
- The moved spots go into the STL source as `joint_x` (the template file is unchanged). Place on tray draws the real joint spots and says, without blocking, "The tray screw joints were moved to X = … mm".
- The build is blocked, in plain words, only when no clear spot exists on the tray.
- The single printed piece joint is unaffected.
- **Effect on saved items:** an item whose opening sat in front of a default joint now builds with a moved joint. Its next build differs from the saved one, so the library offers "Rebuild as new item"; saved builds and revisions are not changed. Brian's real library (data/normal-use) has no wizard items yet.
- **Render check (scratch folder, deleted afterwards):** I re-rendered 20 of the task 18 cases plus the 4 scratch test devices in their library and slot settings. 23 had moved joints, and all 23 pass the mesh check with no nudge, including the case that failed in task 18. The other 5 kept their default joints.
- **Export repair fix found by that check:** OpenSCAD sometimes writes two zero-area triangles stacked on one edge. The existing exact repair (`mesh_revision.normalize_collinear_faces`) now retries starting with the longest one when its normal order fails. No coordinate moves, the mesh check is unchanged, and anything that passed before produces the same bytes. A new test covers it in `test_mesh_integrity.py` (that file is not part of run_checks; run directly, 9 pass).
- **Unknown:** the strength of an off-centre or asymmetric joint pair is UNKNOWN; nothing is printed.

## Who did what

- Codex task 19 (`port-openings.js`, `port_openings.py`: opening math, guards, size table) and task 20 (adapter warning in cable-routes/suggest/inventory). Reviewed: both match the spec.
- Claude did the wiring into equipment.py, Place on tray, cable ports, the rack view, the wizard and the screening, plus items 2, 3, 6 and 7, and two fixes Codex reported: a test that was not reading UTF-8, and one old test expecting unmoved openings.
- **Found in the browser:** editing `rack-references/rack-layout.js` needs its hash updated in `asset-manifest.json`, or the server refuses the script. Fixed (old manifest copy in `docs/archive/pre_design_picks_20261019/`). A new check in `test_rack_references.py` now catches this.

## Checks

- `run_checks.ps1`: **111 Python (1 render test skipped) + 164 JS pass.**
- Browser, on disposable data (port 8793, copy of the end-to-end data; data/normal-use not touched): turned-device warning; opening moved −30 → −19 mm at 0° with an 11 mm offset; cable marker at (−19, 23) after the standoff change; server blocked a keystone overlap with the plain message; rear-support "OK (by design)"; joint warning in Setup, Review and Place on tray; adapter INFO in Review for cable C4; starting sizes and the note; slot-range message; library status line; Project status card. Screenshot: [design-picks-screens/place-on-tray-warnings.jpg](design-picks-screens/place-on-tray-warnings.jpg).
- **Not done:** no exact render or STL export was run in this session (Codex task 18 is sweeping renders now). Nothing was printed.

## Notes

- The normal 8765 server still runs the old code until it is restarted with start.bat.
- Opening sizes are planning guesses. Real connector fit is UNKNOWN until printed.
