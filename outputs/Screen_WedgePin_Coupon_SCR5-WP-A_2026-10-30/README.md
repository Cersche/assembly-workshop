# SCR5-WP-A — wedge-pin button test coupon (2026-10-30)

Test-print ID **SCR5-WP-A** (embossed on the roof). PROPOSED — UNVALIDATED: fit, feel and strength UNKNOWN. Not printed; printing needs Brian's direction.

Purpose: test the SCR5-G option (b) wedge-pin buttons on the real Waveshare 5" DSI LCD (C) before the 2U plate is built.

## How it works
- The body screws to the screen's two **top corner standoffs** (M2.5 x 6 socket cap, from the rear), seat 13.3 mm behind the glass front. A 4 mm front stub stands in for the faceplate, 0.8 mm above the glass top edge, front flush with the glass.
- Three pins slide straight back through the stub (front view: top right, over power / bright+ / bright−, 15/25/35 mm from the rear-view left PCB edge).
- Each pin's underside ramp (1:2) pushes a bump on a 0.8 mm leaf spring down; the leaf's nub presses the side-push plunger. The leaf pushes the pin back out. The bump sits in a notch, so the pin can't fall out forward (snap it in from the front; the leaf flexes ~0.5 mm).
- **Hard stop:** the cap's back face hits the stub after stroke = 2 x drop + 0.5 (0.1 lead-in, 0.4 flat dwell that adds no more drop).
- Pins are interchangeable; dots on the cap: 1 dot drop 0.35, 2 dots 0.45, 3 dots 0.55. Nub-to-plunger gap at rest 0.10, button travel 0.25, so 1 dot = exact, 2/3 dots = 0.1/0.2 overtravel. Try each pin on each button and report which one clicks cleanly without crushing.

## Files
- `SCR5-WP-A_wedge_pin_coupon.3mf` — body (front face down) + 3 pins (on their side), side by side. 2090 vertex / 4184 triangle tags.
- `SCR5-WP-A_body.stl`, `SCR5-WP-A_pin1..3.stl` — model frame (front view, glass front Y=0).
- `src/` — SCAD (all dimensions parametric at the top), mesh check, 3MF packer. `checks/` — render logs, assembled reference STL (pins separate shells, no overlap).

## Print notes (when authorized)
Body: support only under the two screw pads/rear bar overhang. Pins: no support. 0.2 mm layers; the 0.35/0.45/0.55 drops are below a layer on a horizontal print, but the pins print on their side so the ramp is in-plane.

## Assumptions / UNKNOWN
- PCB centred under the glass (PCB top edge 38.0, glass top 38.6 from centre). Not measured.
- Button centres 15/25/35 measured by Brian; plunger depth assumed mid-body (10.9 mm behind glass front).
- Leaf strain at 0.55 drop ~1.3 % (PLA estimate); fatigue UNKNOWN.
