# Assembly Workshop — roadmap

Updated 2026-10-19. Three loose horizons: no dates, no gates, no numbered stages. Items move when Brian says so. Anything physical (printing, fitting, strength) only happens at Brian's direction.

## Goal — version 1 is done when (Brian, 2026-10-19)

1. I can configure a rack.
2. I can add any equipment through the wizard.
3. I can export STLs I trust.
4. I can plan the cabling (ports, guides, cable routes and estimated lengths), so the build and the parts order are predictable.
5. The rack is built.

Then development pauses and the app gets used. Focus is on function, not polish: cosmetic work waits unless it blocks one of the five points above. New ideas go to [IDEAS.md](IDEAS.md), not into Now. After v1, brainstorm ways to use the rack to make life easier and more fun.

## Where it stands

A local app that runs on this PC. You configure a Lab Rax rack, pick a slot, and design what goes in it. It exports STL files.

- **Works today:** rack configuration with the real source meshes; per-slot assemblies, each with its own hardware, inputs and revisions; the Pi4 tray and faceplate (M3 x 0.5); the equipment wizard (dimensions, STL, SCAD or STEP via local FreeCAD) with generic trays and faceplates from 1U to 5U; PRINT THE RACK frame STLs; the hybrid GUI with one explicit Save, save history, colors and faceplate artwork previews; Pi4 "Print in color"; clearance screening for wizard equipment.
- **Checks:** `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1` runs 52 Python + 47 JS tests on temporary data.
- **Physically proven:** only the old two-hole, 3 mm, square-corner tray and faceplate specimen (qualitative fit, confirmed by Brian). Nothing designed since then has been printed.

## Now — make what exists dependable

0. **Cable management Steps 1–5 built** (views and guides, ports, cables and exits, suggestions, wiring sheet); see `work/cable-management/`. Equipment wizard Option 1 steps 1–4 and quality sliders committed (6f4f26c).
1. Automated tests for the page-level logic (save controller, viewer startup). These are only checked by hand today.
2. Per-instance component editing: mostly covered now. Each slot already keeps its own hardware pins/inputs/revisions, tray placement (Place on tray), port overrides and appearance. Remaining gap: the rack view still draws the library mesh, not the slot's placed tray ("Placement not rendered yet"). Brian to say if anything else is missing.
3. Done 2026-10-19: backup AssemblyWorkshop_20261019-2058 (both locations, verified) and 8765 restarted via start.bat (PID 27700).
4. Done: app README and hardware-records.md refreshed (Codex task 15).

## Next — cable inventory and parts order (after cable management Step 5)

Turn the cable plan into a shopping list so the build and the order are predictable: how many cables of each type and estimated length, plus keystones, guides and other parts to buy or print. Supports v1 goal point 4. Proposed defaults: [Parts_Order_Decisions.md](work/cable-management/Parts_Order_Decisions.md) (Brian to confirm); logic is Codex task 14, the Review card is Claude's. Lengths stay planning estimates.

## Next — first real print round (when Brian says go)

The goal is one small, deliberate test kit instead of open-ended "validation":

- the four-hole, 4 mm faceplate (1U);
- one wizard-made tray and faceplate, including a 2U+ plate and a keystone or port opening;
- a short section of rack frame from PRINT THE RACK;
- a Pi4 "Print in color" faceplate.

For each part, write down what was printed, on what, and whether it fit. The result covers only that specimen, material and process.

## Later — ideas, not commitments

- Cabling backlog: a quicker way back to the rack-level panel from a slot (today it's the rack dropdown).
- Print in color for wizard-made faceplates (needs Brian's direction; artwork-to-STL is Pi4 only today).
- Better wizard detection: non-circular slots, solid-box features, recessed or touching ports.
- SCAD imports that `include`/`use` other files.
- Confirm the four-post BOM assumption, and let the BOM follow the exact segments chosen.
- Re-save path for older library items that still carry the old plate.

## Parked

- Niche insert research (Brian's direction).

## Not doing

- Printer, slicer or filament integration. The app hands over STLs, and that's where it stops.
- Publishing, release packaging or redistributing creator, supplier or Pi assets.
- Claiming fit, strength or retention from digital checks alone.
