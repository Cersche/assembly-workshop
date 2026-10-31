# Task 51 — SCR5-G flush-glass 2U screen plate (Codex)

Goal: build SCR5-G, a new revision of the 5" screen faceplate using the MEASURED screen (work/screen-5in/Dimensions.md, 2026-10-30) and Brian's SCR5-G decisions. SCR5-B..F and SCR5-WP-A stay immutable. Fit/strength UNKNOWN; do not print.

## Files
- New folder `outputs/Screen_5in_SCR5-G_2026-10-30/` with `src/SCR5-G.scad`, `SCR5-G_plate.stl`, `SCR5-G_frame.stl`, 3 pin STLs, `SCR5-G_screen_plate_set.3mf`, `checks/`, `README.md`.
- Reuse (copy, don't edit): faceplate outline/slots from `outputs/Screen_Pi_Hue_SCR5-F_2026-10-29/src/SCR5-F.scad`; mesh check and 3MF packer from that src/ (pattern as in `outputs/Screen_WedgePin_Coupon_SCR5-WP-A_2026-10-30/src/`); wedge-pin geometry from `.../SCR5-WP-A/src/SCR5-WP-A.scad` (keep its parameters at the top so the coupon winner's DROP can be dropped in).
- Do not touch: data/normal-use, SCR5-B..F, Final_3MF, HP4-M6-*, IDEAS.md, HANDOFF.md (Claude updates it).

## Geometry
1. Plate 252 x 88.8 x 4, 44.4 mm/U, four-corner rack slots as SCR5-F, rounded outline corners 2.5 mm (AGENTS limit).
2. Window = glass 120.7 x 77.2 + 0.2 clearance per side, square corners, 0.3 mm chamfer on the front edge. Glass front FLUSH with plate front (Y=0). Lit area (bezels top 2.8 / bottom 8.6 / left 6.0 / right 5.7, front view) centred on the plate vertically: glass centre 2.9 mm below plate centre. Same horizontal placement as SCR5-F's screen centre unless it clashes.
3. Cosmetic lip (params LIP=0.8, LIP_ON=true): a thin ledge on the window's rear edge, Y 2.5..3.3 (right behind the glass, in front of the metal LCD frame C at Y 2.5..5.5), reaching 0.8 inward, on the LEFT and RIGHT edges ONLY (measured step to the frame ~1.5 there). No lip on top or bottom (cables/FPCs). Cosmetic only: it must not carry the screen; depth and retention come from the rear frame. Layer stack (Dimensions.md 2026-10-30): glass 0.9 + 1.6, frame 3.0, gap 2.0, PCB 1.6.
4. Rear frame: screws (M2.5 x 6 socket cap) to the 4 corner standoffs 112.9 x 68.0 (centred on the glass, assumed PCB centred under glass), seat face 13.3 mm behind the plate front; joins the plate rear with 4 x M2.5 heat-set or printed-in bosses (state which). Provide a `SHIM` parameter (default 0) that moves the seat back.
5. Clearances behind the screen (front-view frame): DSI connector at the front-view LEFT edge, 30–51 mm up from the bottom PCB edge, 5.25 above PCB back (Y 14.35): frame must leave ≥ 3 mm round it and an open slot ≥ 18 mm wide toward the left/up for the ribbon to the Pi in U5 above. Touch FPC 2.0 tall mid-board: frame stays off the board centre.
6. Buttons: 3 wedge pins top RIGHT (front view) at X = glass-centre + 45.5 / 35.5 / 25.5, through the plate band above the glass, same leaf/bump/notch/hard-stop design as SCR5-WP-A (leaves anchored to the plate rear, bump under each pin). DROP default 0.45 until the coupon reports.
7. Engrave/emboss "SCR5-G" on the plate rear.

## Acceptance checks
- Each STL one closed shell, 0 bad edges, 0 degenerate (meshcheck).
- Assembled reference: plate + frame + pins + a screen dummy (glass box, LCD box, PCB 121 x 76 x 1.6, standoffs, button bodies, DSI box) — no volume overlaps except intended contact (report the intersect volumes).
- Glass front at Y=0 with plate front; lit-area centre within 0.1 of plate centre (Z); window clearance 0.2.
- 3MF plain tags: report vertex/triangle tag counts; no `ns0`.
- README: decisions, assumptions (PCB centred UNKNOWN), print orientation, UNKNOWNs, test-print ID SCR5-G.
- Write `work/codex-tasks/51-scr5-g-flush-screen-plate-REPORT.md`.
