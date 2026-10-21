# SLV-E — OptiPlex sleeve rear bracket, app "Reinforced" style — 2026-10-21

**Question:** compared with SLV-D, is the app's default **Reinforced** rear bracket stiffer on the rear posts, and do the PC's rear cables still pass through its smaller openings?
**Status:** PROPOSED, UNVALIDATED. Fit, stiffness and strength are **UNKNOWN** until Brian prints it and reports back.
**Alternative to SLV-D-REAR** ([../Physical_Test_Coupons_2026-10-20_SLV-D/](../Physical_Test_Coupons_2026-10-20_SLV-D/README.md)), which uses the older "Open" openings. Print it with **SLV-B-TRAY** and reuse **SLV-A-PLATE**. The orientation and mounting layout are SETTLED by Brian (see [SLV-B](../Physical_Test_Coupons_2026-10-20_SLV-B/README.md)).

## Part and ID

| ID | File | Print size (as laid out) |
|---|---|---|
| **SLV-E-REAR** | `SLV-E-REAR.stl` | 252 × 44.4 × 12 mm, outer face on the bed, bosses, tongues and lips up, no support |

The ID is engraved 0.6 mm deep on the outer face's left ear, between the openings and the rack slots. It reads bottom to top from behind the rack (same place as SLV-D).

## How it was made (all app geometry)

- `SLV-E_spec.json` is the SLV-D spec with `rear_openings` removed and `"rear_style": "reinforced"`.
- `SLV-E_app_source.scad` is exactly what the app writes for it (`equipment.clean()` + `equipment.source()`).
- `SLV-E_coupon.scad` only engraves the ID and lays the part flat. Nothing is cut or redrawn by hand.
- Exported with OpenSCAD.exe, 2026-10-21: `openscad.exe -o SLV-E-REAR.stl SLV-E_coupon.scad`.

## Digital checks

`mesh_study.py info`: **1 body, 0 open edges**, 252.00 × 44.40 × 12.00 mm, 31.5 cm³ (SLV-D: 20.8 cm³).

Openings, from the app's `rear_geometry()` (rack X / Z, Z from the slot bottom, same frame as the SLV-D table):

| Window | SLV-E (Reinforced) | SLV-D (Open) |
|---|---|---|
| Upper | X −96..96, Z 25.0–39.4 | X −100.25..100.25, Z 23.0–41.0 |
| Lower centre | X −28..28, Z 5.0–19.0 | X −30..30, Z 3.5–19.0 |
| Lower outer | X ±52..96, Z 5.0–19.0 | X ±50..100.25, Z 3.5–19.0 |

What's different from SLV-D:
- wider solid bands: 5 mm top and bottom, a 6 mm strip between the windows, 6 mm of plate around the bosses;
- **stiffening lips** on the tray side, 2.5 mm thick and 8 mm deep: one along the top edge (X −100..100) and one down each side (X ±97.5..100). They face the tray, so the outer face still prints flat;
- the openings are smaller, so a plug that cleared SLV-D's openings might hit a bar on this one.

## Hardware

Same as SLV-D: 2 × M3 heat-set inserts in the bosses (4.0 mm pilot, 8 mm deep), 2 × M3 screws 8–10 mm long through the tray's rear uprights, and 4 rack screws on the rear posts.

## What to check and report (compare with SLV-D)

1. Do the tongues and screws line up with the SLV-B-TRAY rear uprights? Do the lips clear the tray and the rear posts?
2. Is it stiffer than SLV-D when you push on the tray's rear?
3. Can all the PC's rear cables (power, display, network, USB) plug in and pass through? Which plugs, if any, hit a bar or a lip?
4. Did it print OK?

## Limits

This is a test part only. Stiffness, strength and plug clearance are **UNKNOWN**.
