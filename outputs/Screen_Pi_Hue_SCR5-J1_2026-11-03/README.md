# SCR5-J1: screen + Pi 4 + Hue, 4-port access panel (2026-11-03)

Brian asked for 4 ports. New design, replaces the H11 layout. Test-print ID **SCR5-J1** on plate, deck, underframe, fan mount and all 3 frame pieces (`J1` on the two small ones). The wedge pins are H8's, unchanged. **Not printed.** Fit, snap, sag, heat and strength are UNKNOWN. Exploration behind it: [work/scr5-access/README.md](../../work/scr5-access/README.md).

## What it is
- **4 golden keystones**, 2 columns x 2 rows, upright, `ks_tight` 0.2, same block as H11. Screen stays where it was.
- **Pi on the screen's own 4 standoffs**, 4 M2.5 socket heads. USB-C edge up, USB and Ethernet to the right from the front. 50 mm DSI ribbon from the screen's box (route about 29).
- **Hue between the keystone rows**, deck Z 28..31, Hue Z 31..57.7. Top-row cables pass over, bottom-row cables under.
- **4 M6 joints**, 2 high and 2 low at X -60 and -47, Z 15 and 73, 58 apart. Hidden from the front. Two tongues on the plate take the weight into the deck wall.
- **Fan mount still tool-free:** snaps over the frame's top and bottom bars, fan facing the Pi's chip from behind.
- **The free strip** on the plate (X -68..-28) stays blank for labels.

| | H11 | J1 |
|---|---|---|
| Hue centre behind plate rear | 93 | 78 |
| Tray rear Y | 142 | 130 |
| Weight on the tray (assumed Hue 150 g) | 360 g | 238 g |
| Bending at the plate | 27,463 g.mm | 17,371 g.mm (63%) |
| Height between top and bottom fastening | 58 | 58 |

Pi and fan add about 1,100 g.mm through the frame instead. Hue centre was held at 78 rather than the 67 in the concept so the Hue no longer depends on the assumed jack size: it starts behind the jacks.

## Parts (3MF `SCR5-J1_screen_pi_hue_4port_set.3mf`, print orientation)
Plate (face down), frame (3 separate pieces), deck (flat, cradle posts up), underframe (top face down), fan mount (fan face down), 3 H8 wedge pins.

## Assembly order
1. Screen into the plate from the front, wedge pins, frame pieces on the corner standoffs (M2.5) and plate bosses (M3 countersunk).
2. DSI ribbon on both ends, then the Pi on its 4 standoffs.
3. Deck on the underframe, 9 M3 countersunk from above (Hue off).
4. Slide the tray onto the plate tongues, then 4 M6 x 8 (4 mm L-key or driver, straight in).
5. Snap on the fan mount with the fan fitted.
6. Keystones, then slide the Hue in from behind: tilt its rear end over the 6 mm rear posts.

## BOM
4 M6x5x8 inserts + 4 M6 x 8 button heads. 17 M3x3x5 inserts (4 plate, 9 underframe, 4 fan mount). M3 countersunk: 4 frame, 9 deck (6 to 8 long), 4 fan (about 14 long). M2.5 socket heads: 4 screen corners, 4 Pi (length to confirm against the standoffs). No new screw type. New item to confirm: a right-angle USB-C plug.

## Changed or gone from H11 (Brian was told, not yet explicitly agreed)
Pi ports through the plate, the floor and inner walls, plate ledge and T-rails, and the low M3 joint are gone. The clip-on side fan mount became the frame-mounted one. Cradle rear posts are cut to 6 tall because the Hue can't lift straight out past the top-row plugs. Frame is now 3 pieces because the Pi and its plugs cut through it.

## Access
- **M6:** all 4 reachable straight in, even with the Hue on.
- **Deck M3:** Hue off.
- **Pi screws:** fan off.
- **SD card:** worse than H11. Hue off, then over the front right cradle post (X -27..-7.5, top Z 58.7) with fingers or tweezers, lifting the ribbon. 20 mm gap between post and Pi. Or take the tray off.
- **Hue button:** from behind over the right half of the Hue.
- **Micro-HDMI and audio** have no room for normal plugs; USB-C needs the right-angle plug.

## Still to check
- Fan snap: calculated about 0.2 per side; could be too tight or rattle. The top frame piece it snaps on is only held at one end.
- Heat: Pi 4.2 mm off the screen back, fan on the chip side. UNKNOWN. **Fan voltage:** H11's 40 x 10 is listed 12 V, but only 5 V is available here (Pi GPIO, the FAN pads on the screen).
- Underside of the Pi vs parts on the screen's back: the screen's own holes are made for this, but the 4.2 gap is not measured against the DIP switch, FPC latch and inductor.
- Jack, plug and Pi connector shapes are not measured. Ribbon reach, tongue fit and print of the plate with its 19 mm tongues are unproven.

## Checks (digital only)
- Plate, deck, underframe, fan mount: one closed shell, 0 bad edges, 0 degenerate faces. Frame: 3 closed shells, on purpose.
- `checks/pairwise.json`, 123 pairs by ray parity on a 0.25 mm grid (OpenSCAD intersection returned empty on a test cube in the concept plate, so it is not used), all 0 except by design: plate vs jacks (jack sits in the block), deck vs Hue box (assumed Hue box vs cradle posts, also seen in H11), deck M3 tools vs Hue, SD path vs Hue, ribbon and cradle post. Includes both rack posts and all 4 M6 driver paths.
- Final positions only; no motion simulated.
- 3MF: 8 objects, 18,359 vertex / 36,898 triangle tags, no ns0.

## Rebuild
`SCR5-J1_deck.stl` and the 3MF contain the third-party Hue cradle, so they stay on the PC and out of git. `checks/ref_deck_no_cradle.stl` is the deck without it.

`python src/SCR5-J1_build.py`, then `python src/SCR5-J1_finish.py`. Needs OpenSCAD, trimesh, numpy and the local Hue cradle `C:/Users/brian/Downloads/Swanky Rottis.stl`.
