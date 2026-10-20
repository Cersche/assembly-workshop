# Test coupons v2 — 2026-10-19 (replaces the 2026-10-18 coupons)

Why v2: the printed v1 keystone opening (14.5 × 16 mm) was too narrow. Also, the v1 snap barb's ramp faced the wrong way, so the tray could not snap on just by sliding it in.

| File | Size (mm) | What changed / what to check |
|---|---|---|
| `1_Keystone_and_corner_holes__faceplate.stl` | 48 × 10.4 × 42 | Re-modelled from measurements of Brian's reference keystone frame: opening **14.8 × 16.6**, plus a collar on the back (19.8 × 27.85, reaching 9.2 mm behind the front face, with a bottom lip to 10.4). The collar holds the latch ramp (top), the hook groove (bottom) and the rear catches. Check: the jack goes in from the front with its **latch on top**, clicks, and holds. The 2 rack holes are unchanged. |
| `2_Snap_joint__faceplate.stl` + `2_Snap_joint__tray.stl` | 24 × 20 × 42 and 24 × 30 × 3 | Barb flipped: the flat catch face now faces the plate and the ramp slopes down toward the back. The window is now 3.2 mm long, so the whole barb fits in it. To assemble, butt the tray against the plate and slide it forward; its front edge pushes the arm down until the barb pops up into the window. Pulling the tray back should be blocked. To release, push the barb down through the window and slide the tray back. |

Print the faceplate pieces front-face down. The collar prints straight up from the plate with no supports needed; the top latch slot is open. Fit, strength and retention are UNKNOWN, and any result applies only to your printer and material.

Source: `outputs/Mechanical_Design_App/equipment_tray.scad` (keystone v2 + barb v2). The pre-change template is in `docs/archive/pre_keystone_v2_20261019/`. Keystones are now spaced at least 21 mm apart, kept at least 24 mm in from each plate end, and must clear the tray (the wizard checks this).
