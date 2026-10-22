# SLV-F — OptiPlex Micro sleeve v2, full print package — 2026-10-21

**What it is:** the complete OptiPlex mount with everything from Brian's SLV-A feedback. **No coupon first**: Brian chose to print the full set directly ("just gonna yolo the thing").
**Status:** PROPOSED, UNVALIDATED. Fit, click-in retention, insert strength and stiffness are **UNKNOWN** until Brian prints it.
**SETTLED, unchanged:** orientation (power button at the faceplate), the 44.4 mm faceplate on the front posts, the full 240 mm sleeve tray on rear support, the rear bracket on the rear posts, 4 front M3 inserts, 2 rear tongue screws.
**Replaces** SLV-A-PLATE (its opening is now taller and its holes moved), SLV-B-TRAY, and SLV-D/SLV-E-REAR (same brackets, new IDs). Don't mix SLV-F parts with older plates or trays.

## Parts and IDs

| ID | File | Print as laid out |
|---|---|---|
| **SLV-F-PLATE** | `SLV-F-PLATE.stl` | 252 × 44.4 × 4 mm, front face up |
| **SLV-F-TRAY** | `SLV-F-TRAY.stl` | 201.5 × 240 × 43.8 mm, flat underside on the bed |
| **SLV-F-REAR-R** | `SLV-F-REAR-R.stl` | Reinforced rear bracket (stiffer, smaller openings). 252 × 44.4 × 12, outer face on the bed |
| **SLV-F-REAR-O** | `SLV-F-REAR-O.stl` | Open rear bracket (bigger openings, lighter). Same size and orientation |

Print **one** rear bracket (R or O); both are included so Brian can choose in the slicer. IDs are engraved 0.6 mm deep:
- plate: front face, right ear;
- tray: outside of the left wall, near the front;
- bracket: outer face, left ear.

## What changed from SLV-A/B (Brian's feedback)

- **Opening 1 mm taller: 37.3 mm** above the floor (was 36.3). That's 0.5 mm Brian measured, plus 0.5 mm so the PC can slide in riding on its feet. Seated, there's about 1.3 mm above the PC. That's on purpose. The sides are unchanged (0.5 mm each).
- **Foot grooves with a click-in dip** instead of pockets:
  - The PC slides in on its feet along two smooth grooves (2.3 mm deep), lifted 0.5 mm.
  - At the end its feet drop into dips with 45° ramps and the case settles onto the floor.
  - The rear feet cross the front dips on the way in, so expect a mild bump halfway.
  - Loading: the PC slides into the bare tray from the front, then the faceplate goes on (Brian, 2026-10-22). So the plate has **no groove notches** (removed 2026-10-22; the plate was re-exported, the tray is unchanged).
- **Backstop:** the tray's existing rear stop (unchanged).
- **Cable opening** in the floor behind the PC, between the rear uprights: X −28..28, Y 198.5..225.7 (56 × 27 mm, 2 mm corners). For the barrel plug and the network cable.
- **Insert bosses:** the 4 front heat-set holes moved outward to X ±95.75. They now have ≥ 2.0 mm of plastic inside and ≥ 3.0 mm outside (was 1 mm), in round bosses 12 mm long. The faceplate's screw holes moved to match. Because of the bosses, the tray is 201.5 mm wide (limit 204).
- **Flat underside:** under the grooves the floor reaches down to the slot bottom (Z 0) across the full tray, so it prints flat (Claude fix; see below).

## How it was made

- Specs `SLV-F_spec_R.json` / `_O.json` = the SLV-B spec + `sleeve_top=0.8`, `feet_style="grooves"`, `rear_floor_opening=true`, `insert_bosses=true`, and `rear_style` `reinforced` / `open`. The plate and tray are identical in both.
- `SLV-F_app_source_R.scad` / `_O.scad` are exactly what the app writes. `SLV-F_coupon.scad` (plate, tray, rear_r) and `SLV-F_coupon_O.scad` (rear_o) only engrave IDs and lay parts flat.
- Exported with OpenSCAD.exe on 2026-10-21. `SLV-F_tray_preview.png` is a render of the tray, seen from the back.
- **Claude fixes to Codex task 36, made before export:**
  1. The new settings were defined at the end of the SCAD file. OpenSCAD evaluates a variable where it is first assigned, so the first render came out with no walls. The tests had only checked the numbers and never rendered.
  2. The floor thickening was only under the grooves, which left 0.5 mm ridges on the underside. It is now a full-width slab, and the strap slots cut through it.
  - Old designs still produce byte-identical source (checked on SLV-B). Checks: 177 Python pass (1 skipped). JS: all pass except the older, unrelated rack-BOM failure.

## Digital checks (2026-10-21)

- All 4 STLs: **1 body, 0 open edges**.
- The PC was modeled as a 182.5 × 194.5 × 36.0 case on 2.75 mm feet (Brian's measurement), at the spec foot positions.
  - **Seated** (case on the floor, feet in the dips): touches nothing.
  - **Sliding in**, lifted 0.5 mm on its feet, at 8, 20, 60, 100 and 150 mm before seated: touches nothing.
  - **Click:** pulling it forward without lifting runs the feet into the ramps (0.43 mm overlap). So the PC must lift about 0.45 mm to come out.
- Tray against the plate, and tray against both brackets: they only touch, with no overlap. The cable opening is clear.

## What to check in the slicer

- The tray's underside lies flat with no support needed, apart from the usual bridges over the dips, strap slots and cable opening.
- The plate has no notches; its bottom strip is solid.

## What to report after printing

1. Does the PC slide in smoothly, and do you feel the bump halfway and a click at the end?
2. Does it stay put when you tug it gently forward? Can you get it out with a firm pull?
3. Did the inserts go into the bosses cleanly? Do the faceplate screws line up?
4. Do the tongues and screws meet the rear bracket with both plates on the posts?
5. Do the barrel plug and network cable reach and pass through?
6. Any flex, cracks or print problems?

## Hardware

- 4 × M3 heat-set inserts in the tray's front bosses (4.0 mm pilot, 8 mm deep), plus 4 × M3 screws through the plate.
- 2 × M3 inserts in the bracket bosses, plus 2 × M3 screws (8–10 mm) through the tray's rear uprights.
- 8 rack screws: 4 for the plate, 4 for the bracket.

## Limits

The STEP model is Dell's 7010 and Brian's PC is a 7060; SLV-A fitted, but the two being the same size is otherwise unconfirmed. This package is digital checks only. Fit, retention, insert strength and stiffness are **UNKNOWN**.
