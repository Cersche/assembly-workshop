# Assembly Workshop — roadmap

Updated 2026-10-19. Three loose horizons: no dates, no gates, no numbered stages. Items move when Brian says so. Anything physical (printing, fitting, strength) only happens at Brian's direction.

## Where it stands

A local app that runs on this PC. You configure a Lab Rax rack, pick a slot, and design what goes in it. It exports STL files.

- **Works today:** rack configuration with the real source meshes; per-slot assemblies, each with its own hardware, inputs and revisions; the Pi4 tray and faceplate (M3 x 0.5); the equipment wizard (dimensions, STL, SCAD or STEP via local FreeCAD) with generic trays and faceplates from 1U to 5U; PRINT THE RACK frame STLs; the hybrid GUI with one explicit Save, save history, colors and faceplate artwork previews; Pi4 "Print in color"; clearance screening for wizard equipment.
- **Checks:** `outputs/Mechanical_Design_App/run_checks.ps1` runs 47 Python and 14 JS tests on temporary data.
- **Physically proven:** only the old two-hole, 3 mm, square-corner tray and faceplate specimen (qualitative fit, confirmed by Brian). Nothing designed since then has been printed.

## Now — make what exists dependable

1. Automated tests for the page-level logic (save controller, viewer startup). These are only checked by hand today.
2. Per-instance component editing, so one slot's parts can be changed without affecting the others.
3. Restart the normal server (8765) on the current app.py, then take a fresh timestamped backup to both backup locations.
4. Bring the app README and hardware-records.md up to date. Both still contain old status text.

## Next — first real print round (when Brian says go)

The goal is one small, deliberate test kit instead of open-ended "validation":

- the four-hole, 4 mm faceplate (1U);
- one wizard-made tray and faceplate, including a 2U+ plate and a keystone or port opening;
- a short section of rack frame from PRINT THE RACK;
- a Pi4 "Print in color" faceplate.

For each part, write down what was printed, on what, and whether it fit. The result covers only that specimen, material and process.

## Later — ideas, not commitments

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
