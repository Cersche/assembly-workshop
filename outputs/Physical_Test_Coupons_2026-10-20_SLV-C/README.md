# SLV-C — OptiPlex sleeve rear bracket with cable openings — 2026-10-20

**Question:** does a rear bracket with big cable openings still hold the sleeve tray on the rear posts, and do the PC's rear cables pass through it?
**Status:** PROPOSED, UNVALIDATED. Fit and strength are **UNKNOWN** until Brian prints it and reports back.
**Replaces SLV-B-REAR** (a solid plate that walled off the PC's rear ports; don't print that one). Print it together with SLV-B-TRAY and reuse SLV-A-PLATE. The orientation and mounting layout are **SETTLED** by Brian (see [SLV-B README](../Physical_Test_Coupons_2026-10-20_SLV-B/README.md)).

## Part and ID

| ID | File | Print size (as laid out) |
|---|---|---|
| **SLV-C-REAR** | `SLV-C-REAR.stl` | 252 × 44.4 × 12 mm, outer face on the bed, bosses and tongues up |

The ID is engraved 0.6 mm deep on the outer face, on the ear just inside the rack slots. It reads bottom to top from behind the rack.

## How it was made — what is app geometry and what is not

- `SLV-C_app_source.scad` and `SLV-C_spec.json` are byte-identical to SLV-B's: the app's `equipment.clean()` + `equipment.source()` output for the OptiPlex sleeve on rear support.
- `SLV-C_coupon.scad` calls the app's own `rear_bracket()`. **It then cuts openings that the app does not make yet.** That part is hand-added for this test; Codex task 29 is to build it into the app. The openings, in rack X / Z (Z from the slot bottom):
  - **top window:** X −100..100, Z 22–40.5;
  - **bottom windows:** X −30..30, and ±50..100, Z 3.5–22.2;
  - all with 2 mm corners.
- **What stays solid:**
  - 4 mm or more of plate around each joint boss (X ±40, Z 10–19) and tongue (X 34–46, Z 4–7);
  - a 3.5 mm band along the bottom and a 3.9 mm band along the top;
  - the ears with the rack slots (X ±113–123), untouched.
- The openings go through the 4 mm plate only. The tongues and bosses in front of it are whole.
- Exported with OpenSCAD.exe, 2026-10-20: `openscad.exe -o SLV-C-REAR.stl SLV-C_coupon.scad`.

## Digital checks

`mesh_study.py info`: **1 body, 0 open edges**, 252.00 × 44.40 × 12.00 mm. A preview of the whole stack in stand-in posts shows the PC's rear ports (power, display, USB, network) behind the openings.

## Hardware

The same as SLV-B's rear joint: 2 × M3 heat-set inserts in the bosses (4.0 mm pilot, 8 mm deep), 2 × M3 screws 8–10 mm long through the tray's rear uprights, and 4 rack screws on the rear posts.

## What to check and report

1. Do the tongues and screws line up with the SLV-B-TRAY rear uprights while the faceplate and bracket are both on the posts?
2. Is the bracket still stiff enough? Look for flex in the thin bands when you push on the tray's rear.
3. Can you plug in and route the PC's cables (power, display, network, USB) through the openings? Which plugs, if any, are blocked by a bar?
4. Did it print OK?

## Limits

This is a test part only. Stiffness, strength and cable-plug clearance are **UNKNOWN**. The opening layout is a one-off for this PC; the app doesn't make it until task 29 is done.
