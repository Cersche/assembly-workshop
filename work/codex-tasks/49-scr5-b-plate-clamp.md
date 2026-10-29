# Codex task 49 — SCR5-B: plate-anchored rear clamp (rework of SCR5-A)

Claude spec, 2026-10-29, Brian approved "Yes, redo it". Read task 48 spec + REPORT first.

## Why
SCR5-A (task 48) fastens into a carrier ring between glass and PCB, assuming a 6 mm free gap that likely doesn't exist (LCD panel/spacers occupy it) and can't be reached without disassembly; its `--final` gate blocks export, and its bosses overlap the assumed active area by ~1.3 mm. SCR5-A stays as immutable history.

## New architecture (SCR5-B)
- Nothing fastens into the screen. The screen's corner holes are not used.
- Plate: keep SCR5-A plate geometry (252 x 88.8 x 4, slots, 3 mm lip, aperture 114.7 x 71.2, ~20 mm rear pocket) except the fastening. Add four M2.5 heat-set bosses inside the rear pocket, OUTSIDE the glass/PCB outline: beside the screen at about X +/-66, Z ~22 and ~67 (Codex to place; at least 1 mm clear of glass 120.7 x 77.2 / PCB 121 x 76 plus their clearances, inside the pocket wall). Inserts: Brian's M2.5, 4 mm long, 3.5 mm OD; pilot is a separate process parameter. Inserts go in from the rear, axis along Y.
- Rear clamp frame: one removable part screwed to those four bosses with M2.5 socket caps (head 4.5 x 2.5 default parameter; length chosen from stack, documented range). It presses the PCB/glass forward against the lip through contact pads near the four PCB corners/edges only, avoiding components, the touch header/FPC and the buttons. Preload = parameterized small interference/compression gap (default 0.3 mm), tunable once Brian measures the screen. Total screen depth 12.6 nominal is the only depth input.
- Frame openings: top-left ribbon pass (connector ~8 mm from the left edge seen from front, upper half) routed toward HP4-M6-B floor slot X -86..-62, Y 87..95; finger access to the top-edge buttons; open centre for cooling/the ribbon. Smooth edges where the ribbon touches.
- Engrave SCR5-B on the frame rear, positive wall left. Plate keeps no visible engraving on the front.

## Rounded corners (Brian, 2026-10-29, marked on the SCR5-A viewer)
Round every sharp corner Brian circled; all radii are parameters:
- Plate front window (aperture) corners: default R4. Check the rounded aperture still leaves the nominal active area (109 x 65.8, centred assumption) uncovered; corner inset is R x 0.414 along the diagonal, so R4 stays well inside the 2.85 mm margin. Keep registration UNKNOWN.
- Plate rear pocket inner corners: the glass/PCB are square-cornered, so a plain fillet would block them. Use corner reliefs (dog-bone or overcut) or a radius no larger than the configured clearance; prove the nominal glass/PCB still seat on the lip.
- Clamp frame: outer corners default R3, inner opening corners default R3; round tab/pad corners where practical.
- Plate outer corners stay 2.5 mm (four-corner standard, unchanged).

## Deliverables
New folder `outputs/Screen_5in_SCR5-B_2026-10-29/`: parameterized SCAD (may reuse task 48 source as a base; do not edit task 48 outputs), Python 3.10 stdlib + OpenSCAD.exe builder, parameters JSON, README, checks. `SCR5-B_plate.stl`, `SCR5-B_frame.stl`, `SCR5-B_screen_plate_and_frame.3mf` (two named objects, flat, side by side, min Z 0, plain vertex/triangle tags, no ns0). Report `work/codex-tasks/49-scr5-b-plate-clamp-REPORT.md`.

## Checks
Closed single shell per part, positive volume, no degenerate faces; plate bounds and eight slots unchanged from SCR5-A; bosses clear of nominal glass/PCB outline plus clearances and of the aperture; assembly (plate + nominal screen box + frame) has only intended contacts at the configured preload; screw length range vs boss depth/insert/tip reserve; `--final` gate must PASS (no unresolved architecture blocker; numeric unknowns stay as documented parameters). Ribbon route: recompute with the same datums as task 48; reach stays UNKNOWN. Viewer: `tools/mesh_viewer.py` -> `work/mesh-viewer/SCR5-B-*.html` (not committed).

## Don't
Touch SCR5-A, HP4-M6-A/B, Final_3MF, user data or app code. No printing. Fit, preload, retention, reach and strength stay UNKNOWN; vendor dims nominal. Commit task-owned files and push to main; never force-push. Update HANDOFF.md.
