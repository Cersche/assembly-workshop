# SLV-D — OptiPlex sleeve rear bracket, app-made cable openings — 2026-10-20

**Question:** does the app's own rear bracket with cable openings (Codex task 29) hold the sleeve tray on the rear posts, and do the PC's rear cables pass through it?
**Status:** PROPOSED, UNVALIDATED. Fit, stiffness and strength are **UNKNOWN** until Brian prints it and reports back.
**Replaces SLV-C-REAR**, whose openings were cut by hand (unprinted; don't print it) **and SLV-B-REAR**, which was solid. Print it together with **SLV-B-TRAY** and reuse **SLV-A-PLATE**. The orientation and mounting layout are SETTLED by Brian (see [SLV-B](../Physical_Test_Coupons_2026-10-20_SLV-B/README.md)).

## Part and ID

| ID | File | Print size (as laid out) |
|---|---|---|
| **SLV-D-REAR** | `SLV-D-REAR.stl` | 252 × 44.4 × 12 mm, outer face on the bed, bosses and tongues up, no support |

The ID is engraved 0.6 mm deep on the outer face's left ear, between the openings and the rack slots. It reads bottom to top from behind the rack.

## How it was made (all app geometry)

- `SLV-D_spec.json` is the SLV-B spec plus `"rear_openings": true`.
- `SLV-D_app_source.scad` is exactly what the app writes for it (`equipment.clean()` + `equipment.source()`).
- `SLV-D_coupon.scad` only engraves the ID and lays the part flat. Nothing is cut or redrawn by hand.
- Exported with OpenSCAD.exe, 2026-10-20: `openscad.exe -o SLV-D-REAR.stl SLV-D_coupon.scad`.

## Digital checks

`mesh_study.py info`: **1 body, 0 open edges**, 252.00 × 44.40 × 12.00 mm.

Openings measured from the rendered mesh, in rack X / Z with Z from the slot bottom:

| Window | X | Z |
|---|---|---|
| Upper | −100.25..100.25 | 23.0–41.0 |
| Lower centre | −30..30 | 3.5–19.0 |
| Lower outer | ±50..100.25 | 3.5–19.0 |

What stays solid:
- 4 mm of plate around the bosses (X ±40, Z 10–19) and the tongues;
- a full-width 4 mm strip between the upper and lower windows;
- 3.5 mm bands at the top and bottom;
- the rack ears.

Compared with SLV-C, the upper window starts 1 mm higher, the lower windows end at Z 19 instead of 22.2, and the openings reach 0.26 mm further out.

## Hardware

2 × M3 heat-set inserts in the bosses (4.0 mm pilot, 8 mm deep), 2 × M3 screws 8–10 mm long through the tray's rear uprights, and 4 rack screws on the rear posts.

## What to check and report

1. Do the tongues and screws line up with the SLV-B-TRAY rear uprights while the faceplate and bracket are both on the posts?
2. Is it stiff enough? Look for flex in the bands when you push on the tray's rear.
3. Can all the PC's cables (power, display, network, USB) plug in and pass through? Which plugs, if any, hit a bar?
4. Did it print OK?

## Limits

This is a test part only. Stiffness, strength and plug clearance are **UNKNOWN**.
