# SCR5 access panel: layout exploration (2026-11-03)

Brian's idea: Pi on the back of the screen, Hue stays in its bay, the saved space becomes front keystones. Concept model only, nothing to print, no test-print ID yet. Fit, sag, heat and strength stay UNKNOWN. Jack and plug boxes, Pi connectors and the Hue shape (88 x 88 x 26) are assumed, not measured. Hue weight 150 g is assumed; printed parts are 1.24 g/cm3 solid.

`access_concept.scad` (opt A, B, S, T). `build.py A B` exports STLs to `stl/` (not committed). `check_ray.py A B` writes `checks_*.json`. `figures.py` writes `work/mesh-viewer/SCR5-AP_*.png`. Uses the H11 keystone block and screen dummy; the Hue cradle is left out, so these meshes are safe to share.

## Pi mount
The screen's four inner standoffs (female M2.5, 58 x 49, measured in the H7 work) take the Pi directly, Y 13.3. Only one orientation works: USB-C edge up, USB/Ethernet to the right from the front, SD edge next to the screen's DSI connector. Turned the other way, the board lands on the DSI connector (X -27.5..-22.5, board reaches X -28.15 at Y 13.3 under the connector's 14.35 top). The Pi DSI connector lines up in height with the screen's (Z 36.6..54.6 vs 33.5..54.5), so the 50 mm cable that came with the screen should reach (route about 29). Frame needs a notch on the top bar and gaps for USB-C and the right bar.

## Keystone count
Limits: plate rear from X -110.85 (post flange) to the window at X -27.75, 83.1 wide, block 21 x 33.5. Everything possible behind the plate: 222.2 between flanges, less 121.5 window = 100.7.
- A: 3 upright x 2 rows = 6. Screen stays. Strip X -47.85..-27.75 keeps the frame bosses and takes M6 at (-40, 21.5), (-40, 59), plus (-69, 44.4).
- B: 4 upright x 2 rows = 8. Screen +5. Left frame bosses become one at mid height; M6 only in the 18.8 mid gap.
- S: 2 sideways x 4 rows = 8. Middle rows point into the Hue, so the Hue would sit behind the plugs (lever about 112).
- T: 2 sideways x 4 + 1 upright x 2 = 10, wall to window 0.7, room for 1 M6, and that gap is also the only place for the left frame screw. Most that physically fit.
- 12 (3 sideways x 4) needs 100.5 of 100.7 with no walls, joints or frame screws: not real.

## Hue bay
With the Pi gone the deck drops to Z 28..31 and the Hue sits between the rows (Z 31..57.7): top row cables pass over it, bottom row under the deck. Nothing is in front of it but the M6 tabs and ribbon, so it comes forward: front edge Y 27 (was 52), centre 67 behind the plate (was 93). Top row jack clears Hue by 0.6 and the bottom jack clears the deck by 0.5 on assumed jack size; measure a real jack before building.

| | H11 | A or B |
|---|---|---|
| Hue centre behind plate rear | 93 | 67 |
| Tray rear Y | 142 | 119 |
| Moment at plate (tray + load) | 27,463 g.mm | about 15,000 (55%) |

Pi and fan add about 1,100 g.mm through the screen frame instead. Pull on screws (moment / height between joint and bearing point): about 400 g in A (37.5 apart), about 1,070 g in B (14 apart). Left post rail (M6 into the post hole at X -118.26, Z 22.2) fits with 0 clashes on both and carries the deck's left edge.

## Checks (`checks_A.json`, `checks_B.json`)
69 pairs, 0 mm3 except by design: M6 driver vs Hue (Hue out first for the joints above the deck), SD path vs Hue and ribbon (Hue out, lift ribbon). OpenSCAD intersection returned empty on a test cube inside the keystone plate mesh, so the checks use a ray parity script instead. Final positions only; no motion was simulated.

## Would change from H11 (needs Brian's OK)
Dropped: Pi ports in the plate, floor and inner walls, plate ledge with T-rails and the low M3 joint (bottom row sits there). Fan mount stays tool-free but clips to the frame, fan facing the Pi's chip. Hue cradle rear posts would go so the Hue slides out the back; lifting up is blocked by top-row plugs.

## Open
Brian picks a layout and says what plugs in. Then: new revision folder with a new print ID, real jack measurement with a diagram, right-angle USB-C confirmed, M2.5 screw length, fan voltage (H11's 40 x 10 is listed 12 V; the Pi and the screen's FAN pads give 5 V).
