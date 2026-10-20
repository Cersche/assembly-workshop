# SLV-B — OptiPlex Micro 7010 sleeve, full tray on rear-post support — 2026-10-20

**Question:** with the front proven by SLV-A, does the whole sleeve work? That means the PC sliding all the way in, the rear feet and the rear stop, the tray screwed to a bracket on the rear posts, and stiffness over the full length.
**Status:** PROPOSED, UNVALIDATED. Fit, retention and strength are **UNKNOWN** until Brian prints it and reports back.
**SETTLED by Brian, 2026-10-20** (after seeing the rack renders): "OK YES THIS IS PERFECT DO NOT LET ME CHANGE THIS". This covers the orientation (power button at the faceplate; X is up + Rotate 90° once) and the mounting layout (faceplate on the front posts, tray screwed to it and running 240 mm, rear bracket on the rear posts). **Don't print SLV-B-REAR:** it's a solid plate that walls off the PC's rear ports. Print **SLV-D-REAR** instead ([../Physical_Test_Coupons_2026-10-20_SLV-D/](../Physical_Test_Coupons_2026-10-20_SLV-D/README.md)), the app-made bracket with cable openings. SLV-C (hand-cut openings) is superseded and unprinted.
**Builds on SLV-A** ([../Physical_Test_Coupons_2026-10-20_SLV-A/README.md](../Physical_Test_Coupons_2026-10-20_SLV-A/README.md)). Brian, 2026-10-20: "coupon fits perfect"; "feet stopped where they should have when inserting from the front".

## Parts and IDs

| ID | File | What it is | Print size (as laid out) |
|---|---|---|---|
| **SLV-A-PLATE** (reuse) | `../Physical_Test_Coupons_2026-10-20_SLV-A/SLV-A-PLATE.stl` | The faceplate. **Don't reprint it; use the one you have.** Turning rear support on doesn't change it: the triangles are identical. | — |
| **SLV-B-TRAY** | `SLV-B-TRAY.stl` | The full sleeve tray: floor, both walls and lips, all 4 foot pockets, the rear stop, the strap slots, the 4 front joint pilots and the 2 rear uprights with their tongue slots | 198.5 × 240 × 42.3 mm, floor on the bed |
| **SLV-B-REAR** | `SLV-B-REAR.stl` | The plain plate that goes on the rear posts (four rack slots, no window), with 2 tongues and 2 screw bosses | 252 × 44.4 × 12 mm, outer face on the bed, bosses up |

The IDs are engraved 0.6 mm deep, away from every tested surface:
- **tray:** outside of the left wall near the front, the same spot as SLV-A-TRAY;
- **rear bracket:** centre of its outer face, reading from behind the rack. It looks mirrored from the top while it's on the bed.

## How it was made (app geometry)

- `SLV-B_spec.json` is the same spec as SLV-A with `rear_support: true` and no coupon cut. The case is 182.5 × 194.5 × 38.8, 1U, sleeve, screw joint. The 4 feet are 2.8 mm tall at (15, 18, 5, 15), (163, 18, 4, 15), (15, 153, 5, 15) and (163, 153, 4, 15), with the power button at the front (X is up + Rotate 90° once).
- `SLV-B_app_source.scad` is exactly what the app writes (`equipment.clean()` + `equipment.source()`). Its first 260 lines are identical to `equipment_tray.scad`.
- `SLV-B_coupon.scad` `use`s that file. It calls the app's own `tray()` and `rear_bracket()`, engraves the IDs and lays the parts flat. Nothing is redrawn.
- Exported with OpenSCAD.exe, 2026-10-20: `openscad.exe -o SLV-B-TRAY.stl -D part="\"tray\"" SLV-B_coupon.scad` (and `part="rear"` → `SLV-B-REAR.stl`).

## Digital checks

| File | Bodies | Open edges | Size (mm) |
|---|---|---|---|
| SLV-B-TRAY.stl | 1 | 0 | 198.50 × 240.00 × 42.30 |
| SLV-B-REAR.stl | 1 | 0 | 252.00 × 44.40 × 12.00 |

Measured from the tray mesh:
- **Foot pockets** go right through the floor: X −76.75..−70.75 (6 × 16) and 71.25..76.25 (5 × 16), front at Y 13.5..29.5, rear at Y 148.5..164.5.
- **Front joint pilots:** Ø4.0, 8 mm deep, the same as SLV-A.
- **Walls** run from Y 0 to 190.5. The rear stop is behind the PC at Y 190.5–194.5, 6 mm tall.

The front 38 mm is the same geometry as SLV-A-TRAY. No app file was changed.

## Hardware

- **Front joint, plate to walls (as SLV-A; you can reuse those inserts):** 4 × M3 heat-set inserts in the 4.0 mm wall pilots (≤ 8 mm deep) and 4 × M3 screws, 8–10 mm long.
- **Rear joint, tray to rear bracket:** 2 × M3 heat-set inserts in the bracket's two bosses (4.0 mm pilot, 8 mm deep) and 2 × M3 screws, 8–10 mm long, through the tray's rear uprights into them. The bracket's tongues slide into the slots under the uprights.
- **Rack screws:** 4 for the faceplate on the front posts and 4 for the rear bracket on the rear posts.

## Printing

- **Tray:** floor on the bed. The lips overhang 10 mm inward along the full ~190 mm length of each wall (3 mm thick), so **support under both lips**. That's the same as on SLV-A, which printed fine.
- **Rear bracket:** outer face on the bed, bosses and tongues pointing up. No support needed. It's 252 mm long.
- The tray is 240 mm deep, so it needs a 256 mm class bed.

## What it tests and how to check it

1. **Full slide-in:** with the plate screwed to the walls, slide the PC in through the window, back end first. Does it go all the way, rear feet included (they travel ~150 mm under the lips)? Does it drag or catch anywhere along the way, and where?
2. **Rear feet and rear stop:** at the end, do all 4 feet drop into their pockets? Does the PC front end up flush with the plate front while the PC's back sits at the rear stop? Measure any gap at the front (proud or recessed).
3. **Rear-post support:** with the faceplate on the front posts and the bracket on the rear posts, do the bracket's tongues and screw holes line up with the tray's rear uprights without forcing anything? The tray is 240 mm and the frame depth is 240 mm.
4. **Rear joint:** insert fit in the bracket bosses; is the screwed joint stiff?
5. **Stiffness:** with the PC in, does the tray sag in the middle, or twist when you push one corner?
6. **Retention (optional):** pull the PC forward by hand. Does anything hold it? There's no front latch. Straps through the strap slots are the planned retention; strap fit is UNKNOWN.

## What to report back

For each ID, did it print OK? Then:
- full slide-in yes/no, and where it dragged or caught;
- all 4 feet in their pockets;
- front flush or proud/recessed, in mm;
- rear-post alignment (forced or free);
- rear insert and joint stiffness;
- any sag or twist;
- whether the PC slides forward without straps.

## Limits

This is a test print only. Fit and strength apply to these printed specimens on Brian's printer, rack and PC; they don't certify other printers, materials or PCs. Strength, retention, long-term creep, heat and airflow stay **UNKNOWN**.
