# Rack cooling: decisions so far (Brian + Claude, 2026-11-05)

Discussion only. Nothing has been designed or printed yet. Airflow, temperatures, fit and strength are all UNKNOWN.

## Airflow plan (chimney)
- **Exhaust:** one **200 mm fan in the top of the rack, blowing up and out.** Brian chose 200 mm; the stock Lab Rax top is too shallow for it (see below), so **we redesign the top pieces our own way** to fit it.
- **Intake:** a **vented bottom plate with filter mesh** (the rack is wall-mounted, so the underside is open air; no feet needed). Use a coarse mesh over a large area: big, slow fans don't push hard against restrictions.
- **Side panels:** fitted. Put vents **low only** (beside slots 8-9, the MoCA and the OptiPlex), also with filter mesh. Keep the upper sides solid so the fan pulls air up through the whole stack. High side vents would short-circuit the fan.
- Every tray in the stack should leave open floor or side area. No solid full-width, full-depth shelves.
- Wall gap behind the rack for the OptiPlex's rear exhaust: not yet answered (20-30 mm suggested).

## Fan and power
- 200 mm candidates (from memory, check the listing): Noctua NF-A20 PWM (200 x 30, ~87 CFM, ~18 dBA, no RGB); Cooler Master MasterFan MF200R ARGB (200 x 25, ~90 CFM, ~28 dBA, ARGB). Brian likes RGB as a bonus. **Model not chosen yet.** Hole spacing differs between 200 mm models (e.g. 154 vs 170), so the model must be known before the mounting holes are designed.
- Power: a 12 V AC adapter mounted near the fan (on or in the top). A 12 to 5 V converter if the fan is ARGB (needs a 5 V ARGB controller). The same supply could also feed the fan on top of the Pi (Pi fans are usually 5 V; powering it from the Pi is simpler and lets the Pi control it).

## Rack layout (saved, commit 901fca2)
Slot 1 is the top (U9), slot 9 the bottom (U1). Assembly names in the app still carry older U labels.

| Slot | Equipment | Heat |
|---|---|---|
| 1 | Netgear CM1000 (right under the fan) | warm, no fan |
| 2 | TP-Link ER605: **physically in the rack, not yet in the equipment library**, so the slot shows empty | low-medium |
| 3 | TP-Link TL-SG108E | low |
| 4 | Keystone panel, 10 | none |
| 5-6 | Screen + Pi + Hue (2U) | low-medium |
| 7 | HDD/SSD tray | low; HDD wants to stay cool |
| 8 | MoCA: ECB7250 placeholder (real tray is MRT-F, unprinted) | medium |
| 9 | OptiPlex 7010 Micro | hottest |

OptiPlex (182.5 W x 178 D x 36 H) leaves ~12.75 mm each side and ~62 mm behind it in the 208 x 240 rack, about 17,000 mm² of open path.

## Stock Lab Rax top (from `work/rack-geometry-recovery/sources/5U+Lab+Rax+X2D.3mf`)
Creator parts (mklements, BY-NC-SA, local personal use only, never redistributed): Top Panel 228 x 171.5 x 3; Top Front Edge (front and rear, ~282 long, the honeycomb vent edge); Top Left Edge x4 (side handles, 30 x 170 x 35). The bottom has the same layout (Bottom Panel, Bottom Front Edge). The creator's photo shows a 120 mm fan hung under the top panel.
- Usable top area ≈ **228 wide x ~170 deep**: wider than a bay (208), much shallower (bay ~240). A 200 mm fan needs a redesigned top.
- Headroom under the top panel: **not measured.** The measuring diagram is `work/rack-cooling/top_fan_space_measure.svg` (expected 228 / 170; headroom unknown).

## Top redesign session (2026-11-05, later)
- The stock top's flat area is only ~175 deep: both top edges are 45° sloped vents, Y 0..35 each. Only screw points on top: the 4 M6 handle holes (`docs/devices/lab-rax-top.md`).
- **Brian chose option B:** new front and rear top edges with a square top (flat top 240 deep), same plug + tongue joint as the stock edges; **fan recessed in the top's own 35 mm height (Brian: no fan body sticking out)**: it rests on ledges in the hollowed edges and a 3 mm grille, flush with the rail tops, clamps it (no fan screw holes needed); no panel. **Draft 3:** the top is 15 taller (50) with our own side rails, leaving a 15 mm air gap over the CM1000 (Brian chose this over keeping the fan 2 mm above the modem or moving the modem). Joint values: stock, per Brian. Solid edge faces: no high vents (chimney).
- **Fan: Thermaltake CT200 ARGB** (`docs/devices/fan-200mm.md`). **Power (updated 2026-11-07):** GuanTing 12 V 2 A wall wart in the power strip, 5.5 x 2.1 DC jack in the rear edge; it feeds the CT200 and the Pi's 12 V 40 mm fan. No buck board: the Pi drives the CT200's ARGB (5 V + GPIO18 data). Details on the device card.
- Draft: `work/rack-top-fan/rack_top_fan.scad`, viewer https://claude.ai/artifact/T6HSpFzBcET4bHky9yfyev (our parts only). Waiting on the measurements in `work/rack-cooling/top_edge_joint_measure.svg`.

- **Matching bottom (Brian 2026-11-06):** after the top is printed, design a matching bottom section with an open intake grille (same chamfered look, swirl/open grille), replacing the stock bottom panel. Filter, fit and airflow UNKNOWN.
