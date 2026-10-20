# SLV-A — OptiPlex Micro 7010 sleeve, front coupon — 2026-10-20

**Question:** before printing the full 240 mm sleeve tray, does the real OptiPlex fit the front of it (window, side play, top play under the lips, front feet in their pockets, the plate-to-wall screw joint, flush front)?
**Status:** PRINTED AND FITTED. **Brian, 2026-10-20: "coupon fits perfect"; "feet stopped where they should have when inserting from the front".** The real PC slid in through the window and its front feet dropped into the pockets. This fit applies to these printed specimens on Brian's printer and his PC only. Strength and retention stay **UNKNOWN**. The full 240 mm tray is still unprinted, and the rear feet's full-length travel under the lips is untested. Per-point details (play, insert bulge, lip quality) were not reported.

**The STOP note below did not happen in practice.** The digital numbers predicted a 2.5 mm conflict, but the real PC went in. Likely causes, not confirmed: the real rubber feet are lower than the 2.8 mm in Dell's STEP model, or they squash, or the print came out slightly larger. Measuring the real foot height with calipers would show whether the STEP feet are too tall. The note is kept below as a record of the digital check.

## Digital insertion check (STOP note written before printing; NOT borne out by the print, see Status)

While checking the coupon against the full design I found a conflict **in the app's current sleeve design**. It is a digital, geometric fact, not a guess:

| | Height |
|---|---|
| Window in the plate, and gap between floor top and lips | **36.3 mm** (Z 3.5 to 39.8) |
| PC case alone (what the window was sized for: feet already sunk in the pockets) | 36.0 mm |
| PC **with its feet riding on the floor** (how it is while you slide it in) | **38.8 mm** |

The sleeve is filled by sliding the PC in through the front window, but its feet only reach their pockets at the very end. On the way in, the PC is 38.8 mm tall, which is **2.5 mm too tall** for the window and for the gap under the lips. It can't be lowered in from above, because the 163.5 mm gap between the lips is narrower than the 182.5 mm case. It can't go in from the rear because of the rear stop, and tilting only makes it taller. So **the full sleeve as the app builds it today cannot take this PC.** The lower window came in with the foot pockets (Codex task 28). Before that, the window was 39.1 mm tall (Z 3.5 to 42.6) and the PC could slide in on its feet.

Brian's working third-party bracket avoids this with a taller opening that fits the case plus its feet (a "tight squeeze") and two long grooves (bracket study, follow-up section).

**What this coupon still shows if printed as is:** the screw joint and heat-set inserts, the flush plate-to-wall fit, how the 10 mm lips print, and the window and side-wall *width*. To check width, hold the PC's front end against the window. **It will not show the PC sliding in**: its feet will hit the plate below the window. That would only confirm the problem above. Choosing a fix is Brian's call (see "Choices" at the end); no app code was changed.

## Parts and IDs

| ID | File | What it is | Print size (as laid out) |
|---|---|---|---|
| **SLV-A-PLATE** | `SLV-A-PLATE.stl` | The full 1U faceplate (44.4 mm standard, 4 mm, four rack slots) with the sleeve window and the 4 M3 joint holes | 252 × 44.4 × 4 mm, front face up |
| **SLV-A-TRAY** | `SLV-A-TRAY.stl` | The front 38 mm of the sleeve tray at full width: floor, both walls, both lips, both front foot pockets, the 4 joint pilots | 198.5 × 38 × 42.3 mm, floor on the bed |

The IDs are engraved 0.6 mm deep, away from every tested surface:
- **plate:** on the front face of the right ear, reading bottom to top, between the joint hole and the rack slot;
- **tray:** on the outside face of the left wall, mid-height, 6 mm in from each end.

## How it was made (app geometry, not a look-alike)

- `SLV-A_spec.json` is the spec. It is the Dell OptiPlex Micro 7010 imported from Dell's STEP with **X is up + Rotate 90° once**, which puts the power button at the orange front edge (Brian confirmed, 2026-10-20). That gives a case 182.5 wide × 194.5 deep × 38.8 tall. The rest of the spec: 1U, `sleeve`, screw joint, no rear-post support, and 4 feet 2.8 mm tall at (x, y, w, d) = (15, 18, 5, 15), (163, 18, 4, 15), (15, 153, 5, 15) and (163, 153, 4, 15). The feet were found by the wizard's own `findFeet()` code, run on that STEP mesh. The same code reproduces the earlier (reversed) numbers exactly.
- `SLV-A_app_source.scad` is exactly what the app writes: `equipment.clean()` + `equipment.source()` on that spec, plus the template's own `coupon=[-130,130,38]` parameter. Its first 260 lines are identical to `equipment_tray.scad`.
- `SLV-A_coupon.scad` only `use`s that file. It calls the app's own `clip_coupon()`, `faceplate()` and `tray()`, engraves the IDs and lays the parts flat. Nothing is redrawn.
- **Depth 38 mm, not 45–50:** with the power button at the front, the front pockets sit at Y 13.5–29.5. The wall strap slots start at Y 38.6, so a deeper cut would have sliced through them and left ragged notches. At 38 mm the cut is 0.6 mm clear of them.
- **Cut rear end:** the app's coupon cut (an OpenSCAD intersection) leaves one flat, closed face at Y = 38 across the floor, walls and lips. No capping was needed; it prints as a plain square end.
- Exported with OpenSCAD.exe (`C:\Program Files\OpenSCAD\openscad.exe`), 2026-10-20:
  `openscad.exe -o SLV-A-PLATE.stl -D part="\"plate\"" SLV-A_coupon.scad` (and `part="tray"` → `SLV-A-TRAY.stl`).

## Digital checks

`python -I outputs/Mechanical_Design_App/mesh_study.py info` on each STL:

| File | Bodies | Open edges | Size (mm) | Volume |
|---|---|---|---|---|
| SLV-A-PLATE.stl | 1 | 0 | 252.00 × 44.40 × 4.00 | 16 970 mm³ (full plate 16 994; the difference is the engraving) |
| SLV-A-TRAY.stl | 1 | 0 | 198.50 × 38.00 × 42.30 | 41 880 mm³ |

Measured from the meshes, against a full exact render of the same spec without the coupon cut (scratch files, not kept):

| Feature | Full design | Coupon |
|---|---|---|
| Window | X −91.75..91.75, Z 3.50..39.75 (183.5 × 36.25 at the 0.25 mm grid; 36.3 designed) | identical |
| Rack slots / joint holes in plate | 4 × 10 × 7 capsules at X ±113.25..123.25; 4 × Ø3.4 at X ±94.75, Z 6.5 / 36.8 | identical |
| Walls (at Y 20, Z 20) | X ±91.75..97.75 (6 mm) | identical |
| Lips (at Z 41.3) | X ±81.75..97.75 (10 mm inward, Z 39.8–42.8, 3 mm thick) | identical |
| Front foot pockets (through the floor) | X −76.75..−70.75 (6 × 16) and 71.25..76.25 (5 × 16), Y 13.5..29.5 | identical |
| Joint pilots | 4 × Ø4.0, 8.0 mm deep into the wall front ends, X ±94.75, Z 6.5 / 36.8 | identical |

`run_checks.ps1` was run afterwards: 135 Python tests (1 skipped) and all JavaScript checks pass. No app file was changed.

## Hardware

- 4 × M3 heat-set inserts that fit a **4.0 mm pilot** no deeper than **8 mm**: the same 4.0 mm pilot as the Pi4 trial that printed well.
- 4 × M3 screws, **8 or 10 mm long** (4 mm plate + up to 6 mm into the wall; longer ones would bottom out in the 8 mm pilot).
- The usual rack screws, only if you also hang it in the rack.
- Note: the wall is 6 mm and the pilot is 4.0 mm, so about 1 mm of wall remains each side of an insert. Watch for bulging, especially on the inner face (the PC side has only 0.5 mm nominal side play).

## Printing

- **Plate:** flat, front face up (the ID is on top). It is 252 mm long, so it needs a bed at least that long.
- **Tray:** floor on the bed. The two lips overhang 10 mm inward at the top of each wall (3 mm thick), so **support under the lips**, as the full tray would need. The horizontal M3 pilots are small and print without support.
- The foot pockets go right through the 3 mm floor (2.8 mm feet + 0.3 mm extra depth is more than a blind pocket allows).

## What each part tests and how to check it

1. **Screw joint:** melt the 4 inserts into the front ends of the walls (2 per wall), then screw the plate on with 4 M3. Do the holes line up? Did any insert bulge the wall, especially inward? Is the joint stiff, or does the plate rock on the walls?
2. **Front flush:** with the plate screwed on, the window edges should line up with the inner wall faces and the floor top. Look for steps.
3. **Window and side play (width only, see STOP):** hold the PC's front (power-button end) against the window from behind. Is the window wider than the case on both sides? How much play is there? Designed: 0.5 mm per side.
4. **Top play under the lips:** this can't be tried by sliding, because of the STOP problem. With the PC's feet held over the pockets, measure the gap from the floor top to the lip underside (designed 36.3) and compare it with the case height without feet (36.0).
5. **Front feet into the pockets:** with the tray loose (no plate), set the PC's front end down so its two front feet drop into the pockets, front face 4 mm proud of the tray's front edge (where the plate would be). Do both feet drop in fully? How much play front/back and left/right? Designed: 0.5 mm per side.
6. **Lips:** did the 10 mm overhangs print flat? Are they stiff?

## What to report back

For each ID: printed OK yes/no. Then: insert fit, and whether any wall bulged; joint stiffness; flush front (steps?); measured window width and height, and side play per side; gap floor-top to lip; front feet into the pockets (fully? play?); lip print quality. Also any printed size you measure with calipers.

## What this coupon cannot test

The rear stop, the rear feet and their pockets, rear-post support (this spec has none), full-length stiffness and sag, strap slots, and the full insertion slide (blocked, see STOP). Fit and strength apply only to these printed specimens on Brian's printer and rack.

## Choices for Brian (no code changed)

*Superseded by the print (2026-10-20): the PC slid in, so no fix is needed on this evidence. The options below are kept only in case the full tray binds on the rear feet.*

The fix belongs in the app (`equipment_tray.scad` / `port_openings.sleeve`), which this task was not allowed to change. Options:

- **A. Taller window, keep the feet riding on the floor.** Size the window and lips for the full 38.8 mm again, as before task 28: window Z 3.5–42.6, 1.5 mm lips, 1.8 mm top band. Pockets would then catch the feet on the way in, so drop them or turn them into the bracket's long grooves.
- **B. Grooves from the front.** Run each foot channel from the front edge back to its pocket, with matching notches in the plate under the window, so the feet slide in sunk. The feet need 3.1 mm but the floor is 3 mm, so these become long slots right through the floor (the rear feet travel about 170 mm). That weakens the floor.
- **C. Reprint this coupon after the fix.** A later SLV-B coupon from the fixed design could then test the full slide-in.
