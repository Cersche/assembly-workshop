# SCR5-J2: screen + Pi 4 + Hue, 3-port access panel (2026-11-03)

Brian chose 3 keystones across the top with the Hue low: "3 is enough". Replaces J1. Test-print ID **SCR5-J2** on the plate (rear face), tray (underside), fan mount and all 3 frame pieces (`J2` on the two small ones). The wedge pins are H8's, unchanged. **Not printed.** Fit, snap, sag, heat and strength are UNKNOWN. Exploration behind it: [work/scr5-access/README.md](../../work/scr5-access/README.md).

## What it is
- **3 golden keystones** in one row across the top, upright, `ks_tight` 0.2, same block as H11. Screen stays where it was, frame is J1's.
- **Pi on the screen's own 4 standoffs**, as J1. 50 mm DSI ribbon from the screen's box (route about 29).
- **Hue low on a one-piece tray:** floor Z 2..5, Hue Z 5..31.7, Brian's cradle posts at full height, centre 64.5 behind the plate's rear face. All 3 cables run over it.
- **3 M6 joints** in one row, X -95, -71, -47, Z 45. Hidden from the front. M6x5x8 inserts in the plate bosses, bore 7.6 x 6.6 deep.
- **2 tongues low on the plate** (X -90, -60, Z 7..10) hang the tray. New since the concept: a **pad** around each tongue (Z 3..14, back to Y 14.6). The tray's wall pushes on these pads, otherwise the wall's low end would have nothing to bear on and the tray would pivot on the screw row.
- **Fan mount still tool-free**, as J1.
- **The plate below the keystones** stays blank for labels.

| | H11 | J1 | J2 |
|---|---|---|---|
| Keystones | | 4 | 3 |
| Hue centre behind plate rear | 93 | 78 | 64.5 |
| Tray rear Y | 142 | 130 | 116 |
| Weight on the tray (assumed Hue 150 g) | 360 g | 238 g | 231 g |
| Bending at the plate | 27,463 g.mm | 17,371 g.mm (63%) | 13,710 g.mm (50%) |
| Printed tray parts | | 2 + 9 M3 | 1 |

M6 row pull is about 376 g in total, with the row 36.5 above the pads. J1 had two rows 58 apart, so its pull was lower (about 299 g per row) even with more bending.

## Parts (3MF `SCR5-J2_screen_pi_hue_3port_set.3mf`, print orientation)
Plate (face down), frame (3 separate pieces), tray (flat, cradle posts up), fan mount (fan face down), 3 H8 wedge pins.

## Assembly order
1. Screen into the plate from the front, wedge pins, frame pieces on the corner standoffs (M2.5) and plate bosses (M3 countersunk).
2. DSI ribbon on both ends, then the Pi on its 4 standoffs.
3. Slide the tray onto the plate tongues, then 3 M6 x 8 (straight in from behind).
4. Snap on the fan mount with the fan fitted.
5. Keystones, then the Hue down into the cradle.

## BOM
3 M6x5x8 inserts + 3 M6 x 8 button heads. 8 M3x3x5 inserts (4 plate, 4 fan mount). M3 countersunk: 4 frame, 4 fan (about 14 long). M2.5 socket heads: 4 screen corners, 4 Pi (length to confirm against the standoffs). No new screw type. New item to confirm: a right-angle USB-C plug.

## Access
- **M6:** all 3 reachable straight in, even with the Hue on.
- **SD card:** straight in from behind over the Hue, Hue on. Lift the ribbon aside.
- **Pi screws:** fan off. Driver paths clear of the tray; the right tray wall sits at X -10..-7 for this.
- **Hue out:** lift about 20, tip the rear up about 6 degrees over the rear posts, ease back and up about 10, level, slide out the back. Checked at 5 still positions, assumed Hue box and jacks. At the tipped position, the Hue's front right corner reaches about 3 mm into the ribbon's assumed path, so hold the ribbon forward. The front posts are still around the Hue's front corners there, about 0.8 further than at rest, so ease it back as you tip. The Hue box is assumed: it also overlaps the posts at rest.

## Changed or gone from J1
One keystone, the underframe and its 9 M3, 1 M6, the top-row cable lane split. Hue moved from between the rows to the bottom. Cradle rear posts are full height again. From H11 (Brian told, not yet explicitly agreed): Pi ports through the plate, floor and inner walls, plate ledge and T-rails, low M3 joint.

## Still to check
- **The joint is new:** one screw row plus pads has not been tried on any printed part. Tongue and slot fit (0.3 clearance) unproven.
- Fan snap, heat (Pi 4.2 mm off the screen back) and **fan voltage** (40 x 10 listed 12 V, only 5 V here): same as J1.
- Underside of the Pi vs parts on the screen's back: same as J1.
- Jack, plug, Hue and Pi connector shapes are not measured. Ribbon reach unproven.

## Checks (digital only)
- Plate, tray, fan mount: one closed shell, 0 bad edges, 0 degenerate faces. Frame: 3 closed shells, on purpose.
- `checks/pairwise.json`, 133 pairs by ray parity on a 0.25 mm grid, including both rack posts, 3 M6 driver paths and 4 Pi driver paths. All 0 except: plate vs jacks (jack sits in the block), tray vs Hue box at rest and first 2 removal positions (assumed box vs cradle posts), SD path vs ribbon (lifted aside), tipped Hue vs ribbon (above). Positions 3 to 5 of the removal are clear of everything.
- 3MF: 7 objects, 13,710 vertex / 27,492 triangle tags, no ns0.

## Rebuild
`python src/SCR5-J2_build.py`, then `python src/SCR5-J2_finish.py`. Needs OpenSCAD, trimesh, numpy and the Hue cradle `C:/Users/brian/Downloads/STL/Swanky Rottis.stl`.
