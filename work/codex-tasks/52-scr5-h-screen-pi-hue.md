# Task 52 — SCR5-H: SCR5-G flush screen front + Pi 4 + Hue tray (Codex)

Goal (Brian, 2026-10-30): one 2U unit that houses the measured 5" screen, the Pi 4 and the Hue Bridge, like SCR5-C..F did. Front = SCR5-G (flush glass, side lips, rear frame, wedge pins). Behind = the SCR5-F floor/walls + Hue deck, adapted. This reverses "Pi stays on its own U5 bracket"; HP4-M6-B becomes reference only. SCR5-B..G and SCR5-WP-A stay immutable. Fit/strength/airflow UNKNOWN; do not print.

## Files
- New folder `outputs/Screen_Pi_Hue_SCR5-H_2026-10-30/`: `src/SCR5-H.scad` (+ copied helpers), `SCR5-H_plate.stl`, `SCR5-H_frame.stl`, `SCR5-H_floor.stl`, `SCR5-H_deck.stl`, `SCR5-H_pin1..3.stl`, `SCR5-H_screen_pi_hue_set.3mf`, `checks/`, `README.md`.
- Sources (copy, never edit): `outputs/Screen_5in_SCR5-G_2026-10-30/src/` (plate, frame, pins, screen dummy, build/verify scripts) and `outputs/Screen_Pi_Hue_SCR5-F_2026-10-29/src/` (floor, deck, Pi/Hue/fan dummies, plate tongues + M6 tabs, meshcheck, packer).
- Measurements: `work/screen-5in/Dimensions.md` (all 2026-10-30 entries, incl. layer stack, DSI W = 5.0 measured, PCB centred under glass CONFIRMED).
- Do not touch: data/normal-use, SCR5-B..G, SCR5-WP-A, Final_3MF, HP4-M6-*, IDEAS.md, HANDOFF.md, Dimensions.md.

## Design
1. Plate = SCR5-G plate (window, chamfer, left/right lips, pin channels, glass placement X 33 / Z 41.5, rounded corners, rack slots) PLUS the SCR5-F tray interface (tongues / joint features and the M6 tab mounting) so the tray slides on as in SCR5-F. Any SCR5-F plate opening for Pi USB/Ethernet or keystone: keep only if it does not clash with the SCR5-G window/pins/frame; report what was kept.
2. Rear frame and pins = SCR5-G unchanged (DROP 0.45, parameter at top).
3. Floor/walls and deck = SCR5-F geometry, re-registered to the new plate. Hard rule: zero-volume intersection with the SCR5-G frame, its screw heads + driver paths, the pins' full stroke envelope (rest to hard stop), leaves, the DSI connector keep-out (keep the 8 mm + 3 mm envelope), and the screen dummy. If the deck/floor front edge must move back, move it and report by how much; keep supportless printing (SCR5-E rule).
4. DSI ribbon: route from the screen connector (front-view LEFT edge, 30–51 mm up from PCB bottom) to the Pi's DSI connector inside the tray. Report path length; target ≤ 140 mm so the stock 160 mm cable fits with slack. Keep the ≥ 18 mm open corridor in the frame on that side. Any cut-out needed in the deck/floor for the ribbon: add it, supportless.
5. Keep from SCR5-F: Pi standoffs, fan, vents, Hue cradle, open-top rear cable notches, 5 × M2.5 insert bosses, r 6 rounded tray corners, M6 tabs (M6 x 8 into rack hardware as SCR5-F).
6. IDs "SCR5-H" on plate rear, frame rear, floor top, deck underside (mirrored as SCR5-F).

## Acceptance checks
- Each STL one closed shell, 0 bad edges, 0 degenerate.
- Assembled reference (all parts + screen, Pi, Hue, fan, standoffs, buttons, DSI dummies + pin stroke envelopes + screw driver paths): pairwise intersection volumes table; only intended zero-volume contacts.
- Verify glass flush Y=0, lit centre within 0.1 of plate centre, window 0.2 clearance, lips left/right only (reuse SCR5-G verify script).
- Ribbon path length estimate with the route drawn as a diagnostic STL.
- 3MF: parts side by side, print orientations as SCR5-E/G, report plain vertex/triangle tag counts, no ns0.
- README: decisions, BOM delta vs SCR5-F/G, assembly order, print orientation, UNKNOWNs, test-print ID SCR5-H.
- Write `work/codex-tasks/52-scr5-h-screen-pi-hue-REPORT.md`. No print, commit or push.
