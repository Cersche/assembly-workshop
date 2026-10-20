# Keystone v3 "golden" coupon — 2026-10-19

LOCAL / PERSONAL USE ONLY. The keystone geometry is copied from Brian's SG108 faceplate:
"10 inch shelf TP-Link SG108 Plus Keystone" by Goul (MakerWorld remix of unknown_one's "Remix of TP-Link SG108PE v2 Rack Mount"), license BY-NC-SA.
Credit Goul and the original authors. Never bundle, publish or redistribute this file or app STLs containing it.

Why: v2 (14.8 × 16.6 opening) printed loose (play up/down and left/right). Brian's printed SG108 faceplate fits a jack perfectly and is the golden standard.

What was found: the SG108 opening is also 14.8 × 16.6, so the difference is in the details. The SG108 has collar side walls 9.9 mm deep (v2: 9.2), a 2.6 mm hook groove closed at the back (v2: 3.4 mm), no open latch slot through the collar top, rounded rear edges, and a 1.6 mm relief groove in the plate back around the collar.

How: cross-sections of `C:\Users\brian\Downloads\SG108_Keystone_faceplate.stl` were taken in 6 bands across the keystone and placed into `equipment_tray.scad` (`ks_style="golden"`, the new default; `"v2"` keeps the old rebuild). Check of this STL against the SG108 at 9 slices: at most 7 mismatched cells of ~9,000 on a 0.1 mm grid. Keystone face sits 0.08 mm proud of the plate, as in the source.

| File | What to check |
|---|---|
| `1_Keystone_golden__faceplate.stl` | Jack goes in from the front with its latch on top, clicks, and holds with no play — compare to the SG108 plate with the same jack. |

Print front-face down, same settings as the SG108 print if possible. Fit, strength and retention remain UNKNOWN until printed; any result applies only to this printer/material. Printing is Brian's call.
