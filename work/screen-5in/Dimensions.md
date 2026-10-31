# Waveshare 5inch DSI LCD (C) — vendor dimensions

Source: Waveshare product drawing pasted by Brian, 2026-10-28. Vendor nominal values; NOT measured. Confirm on the real part.

| Item | mm |
|---|---|
| Glass outline (W x H) | 120.70 x 77.20 |
| Active area | 109.00 x 65.80 (offset inside glass not dimensioned) |
| Total thickness, glass to rear parts | 12.60 |
| PCB outline | 121.00 x 76.00 |
| Corner holes (stand), M2.5 x 4 mm | 4.00 from each edge -> 113.00 x 68.00 pattern |
| Pi mounting holes (Pi pattern) | 58.00 x 49.00; nearest hole 41.5 from PCB edge (4 + 37.5), rear view |

Rear view, read off the picture only (approx.): DSI FPC connector stands vertical about 8 mm in from the rear-view right edge, i.e. the **left edge seen from the front**, in the upper half. Buttons (backlight, brightness +/-) sit on the top edge, rear side. The touch I2C header and a small FPC are mid-board.

Plan (Brian, 2026-10-28): option A, 2U plate at U4-U3 (88.8 mm tall; 5.8 mm per side around the glass). Driven by the U5 HP4-M6-A Pi (board X 46..102) over the 160 mm cable. Fit and ribbon reach UNKNOWN.

## Measured on the real screen — Brian, 2026-10-30

Photos and annotated asks: `work/screen-5in/photos-2026-10-30/`. Orientation = rear view as in `2_back_ask.jpg` (buttons on the top edge, Waveshare logo bottom, DSI connector at the right).

| Item | mm | Note |
|---|---|---|
| Glass thickness | 2.5 | measured |
| Gap glass to PCB (LCD module/backlight) | 5.0 | measured |
| PCB thickness | 1.6 | measured |
| Glass front to PCB back | 9.1 | sum; photo estimate ~9.3 agrees |
| Standoffs (all 8) | 4.0 above PCB, female M2.5 | measured; glass front to standoff top = **13.3 calipers** (sum of layers 13.1; vendor 12.6) |
| DSI connector | spans 30–51 from bottom PCB edge (centre 40.5, 21 long), 5.25 tall above PCB | measured; at the right edge in rear view |
| Touch FPC | 2.0 above PCB | measured |
| Buttons (3, side-push) | outer face flush with top PCB edge (PCB notched there); centres ~13/24/35 mm from left edge | flush: measured; centres: photo estimate |
| PCB height | ~77 | photo estimate (vendor 76.0) |
| Inner standoffs | ~58 x 50 | photo estimate = Pi 4 pattern 58 x 49 |
| Glass tab at lower left | — | packaging protector tab, removed in use |

Fasteners on hand: M2.5 socket cap screws (Brian). Still open: glass overhang past PCB on each edge; exact corner-hole spacing (vendor 113 x 68); button centres with calipers.
Decision (Brian, 2026-10-30): the Pi is NOT mounted on the screen; it stays on its own bracket (U5).
| Corner standoff spacing (centres) | 112.9 x 68.0 | measured by Brian 2026-10-30: outside 118.4 / 73.5 minus standoff OD 5.5 (vendor 113 x 68 confirmed) |
| Glass overhang past LCD module (ledge room) | 0.91 on one edge | measured by Brian 2026-10-30 (calipers); which edge, and the other three: open |

Bezel borders scaled from the vendor drawing (Brian re-posted it 2026-10-30), glass front view; approx ±0.5, to confirm with calipers: top ~2.8, bottom ~8.6, left ~6.0, right ~5.7 (totals fit 120.7-109 and 77.2-65.8). Glass corners drawn square. Centring the lit area in the 88.8 plate means moving the glass ~2.9 mm down: ~8.7 mm plate above the glass, ~2.9 below.

## SCR5-G design decisions — Brian, 2026-10-30
- Glass flush with the faceplate front; 0.3 mm chamfer on the window; lit area centred on the plate (glass ~2.9 mm low); plate corners rounded.
- Depth set by a rear frame screwed to the four corner standoffs (13.3 measured); thin 0.8 mm cosmetic lip; shim option.
- Buttons kept: option (b) wedge pins (front pin slides back, ramp drives a stem down onto each side-push button). Test coupon first.
- Comfortable DSI routing (left side, connector 30-51 mm from bottom PCB edge). Pi stays in U5, NOT on the screen.

## Buttons — measured by Brian, 2026-10-30 (rear view, buttons on the top PCB edge, press toward board centre)
| Item | mm |
|---|---|
| Plunger | 3.0 wide, sticks out 1.0 from the body (ends ~at the notched PCB edge) |
| Body | 7.0 wide, 2.4 deep (without plunger), 3.6 tall above PCB |
| Centres from left PCB edge (rear view) | power 15, brightness + 25, brightness − 35 |
| Travel | 0.25 |
Note: rear-view left = front-view right, so from the front the buttons sit at the top right.

## Layer stack and edge step — measured by Brian, 2026-10-30 (photo `overhang` A–E)
Front to back: A cover glass 0.9, B second glass 1.6 (A+B = 2.5 "glass"), C metal LCD frame 3.0, D black gap 2.0 (C+D = 5.0), E PCB 1.6. Sum 9.1 = glass front to PCB back (matches).
Step from glass edge A in to frame C: ~1.5 on LEFT and RIGHT. Top and bottom carry cables/FPCs: no lip there.
Decision (Brian): the display is NOT held by the lip. Lip = cosmetic, left and right only; the rear frame on the standoffs holds the screen.
| DSI connector reach in from the PCB edge (W) | 5.0 | measured by Brian 2026-10-30, latch open incl. ribbon exit. SCR5-G keeps Codex's 8 mm envelope (+3 extra clearance) on purpose, plus its 3 mm keep-out. |
| PCB centred under the glass | yes | confirmed by Brian 2026-10-30 (SCR5-WP-A and SCR5-G assumption now confirmed) |
