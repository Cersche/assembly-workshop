# Clip retention coupon — 2026-10-19

Brian's direction (2026-10-19): the snap-fit **faceplate-to-tray** joint is retired. The printed coupon was too brittle to carry the tray, so the screw joint stays. Snap-fit is only kept for **holding equipment on the tray**. This coupon tests that: the wizard's "Snap-fit clips" mount (`device_mount="clips"`).

| File | Size (mm) | What to check |
|---|---|---|
| `3_Clip_retention__tray.stl` | 22 × 76 × 13 | Right-hand strip of an 85 × 56 mm board tray: two corner ledges (6 mm high) and one flexing side clip. |
| `3_Clip_retention__test_board.stl` | 12.5 × 56 × 1.6 | Stand-in board edge (1.6 mm, a typical PCB). You can use a real board instead. |

To test: rest the board on the two ledges and press its edge down past the clip's hook. (1) Does the clip flex out and snap back over the board without cracking or turning white? (2) Does the board stay put when you lift or tug it? (3) Can you release it by pushing the clip outward?

Print the tray strip flat (floor down); the clip prints upright with no supports. On a real tray the other side has a matching clip. Fit, retention and strength are UNKNOWN, and any result applies only to your printer and material.

Source: `outputs/Mechanical_Design_App/equipment_tray.scad` with the overrides at the end of `3_Clip_retention__source.scad`. Preview: `renders/clip_preview.png`.
