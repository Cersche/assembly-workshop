# 15 — Docs refresh: wizard, Place on tray, quality sliders

**Goal:** ROADMAP "Now" item 4. Bring `outputs/Mechanical_Design_App/README.md` and `outputs/Mechanical_Design_App/hardware-records.md` up to date with what the app does today. Plain language, short. No phase numbers.

Facts to reflect (read the sources to confirm; do not invent):
- Equipment wizard is now Device → Holes → Ports (`equipment-wizard.js`). Tray choices moved to the **Place on tray** window (`tray-placement.js`), opened when a library item is placed in a slot or from the slot's "Place on tray" button. Per-slot choices are saved as `placement.tray` (only values that differ from the library item). See HANDOFF.md "Option 1 step 3/4".
- Cable ports and clearance screening use each slot's tray settings; the rack view still shows the library mesh with a "Placement not rendered yet" note.
- Quality sliders (`render-quality.js`): Preview Low/Medium/High per viewer (browser preference only); Export Draft/Standard/Fine = $fn 24/48/96 for `equipment_tray.scad` STLs (`equipment.EXPORT_QUALITY`). Fit/strength UNKNOWN at every level.
- Cable planner: ports, guides, cables, suggestions, wiring sheet exist (see work/cable-management/). Guide mesh is local preview only.
- Check counts: run `run_checks.ps1` once and quote the actual numbers.

Keep every existing scope limit and UNKNOWN in both files. Do not change code.

**May change:** those two files only (archive copies first). Then write `15-docs-refresh-wizard-placement-REPORT.md` per the standing rules.
