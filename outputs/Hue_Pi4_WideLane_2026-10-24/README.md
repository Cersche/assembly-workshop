# Hue + Pi 4 + keystone, 1U: wide cable lane (2026-10-24)

PROPOSED, UNVALIDATED. Not printed. Fit, strength and cable bend room are UNKNOWN.

Brian: "try to fit the pi, keystone, hue in the tray as shown but try to leave some space for the cables. make the tray as wide as needed and keep the screws hidden but still within the confines of the rack."

## Files
- `HuePi4_widelane_tray+faceplate.3mf`: both parts as separate objects side by side (`tools/plate_layout_stl.py`). Print this.
- `HuePi4_widelane_tray.stl`, `HuePi4_widelane_faceplate.stl`: exact OpenSCAD.exe renders. Both are closed (every edge shared by exactly two triangles) and each is one solid.
- `HuePi4_widelane_top.png`: top view. The red lines are the ±104 mm rack opening. Ghost shapes: Hue (khaki), Pi board (green), keystone jack (purple, estimated 19 x 35 mm), straight plugs (orange, estimated 25 mm long).
- `ext.scad`: a hand-edited copy of the previous `ext.scad`. It imports the cradle from `C:\Users\brian\Downloads\Swanky Rottis.stl` in place. The cradle is not in the repo (origin and licence unknown).

## Layout (X = 0 is the rack centre, + is right seen from the front, Y = 0 is the plate's rear face)
Same order and orientation as before: keystone far left, Hue in the middle-left, Pi 4 on the right turned 270°.

| Item | Where | Before |
|---|---|---|
| Keystone (golden, `ks_tight=0.2`) | X = -92.5, block -103 to -82 | X = -100, block reached -110.5 (past the post) |
| Hue cradle posts (base plate cut off) | centre X -34.5, Y 70.2; posts X -81.9 to +12.9 | centre X -42 |
| Cable lane (Pi power, HDMI, audio) | X +12.9 to +46: **33 mm** | 20.5 mm |
| Pi 4 board (ports at the plate) | X 46 to 102, Y 0 to 85 | X 26 to 82 |
| Pi plate openings | USB X 55 / 73: 15 x 17.5, Z 18.05-35.55; Ethernet X 91.7: 17.5 x 15, Z 18.1-33.1. About 0.75 mm clearance round the Pi sockets, centred on them (the first version was 13.5 wide and 1.4 mm low: too narrow). The 12 x 9 "USB cable slot" was removed at Brian's request. | 35 / 53 / 71.7 at 13.5 x 17 / 17 x 14, plus the slot |
| Tray floor | X -82.5 to +102 (184.5 mm), Y 0 to 123.4 | -89.6 to +102 |
| Tray joints (hidden screws) | X -58, -12, +29.5 | -40, +16, +93 |
| Cable-tie slots | two 3 x 12 mm slots across the lane, Y 96 to 108 | none |

## Rack limits checked
- Rack opening ±104 mm: everything behind the plate sits within X -103 to +102. The keystone block is 1 mm inside the post. The old X = -100 keystone crossed the post by 6.5 mm (the open "±112.5" issue). This file fixes that only; the generator still allows it.
- Generator tray limit 204 mm (±102): the floor is -82.5 to +102, inside the limit.
- 252 mm plate, 44.4 mm per U, 4 mm thick, four-corner slots at ±118.2625: unchanged from the generator.
- The width is maxed out. The Pi's right edge is at +102 and the keystone block is 1 mm from the left post. A wider lane would need a smaller cradle or moving the keystone, which would change the layout.

## Cable room (estimates marked)
- **Pi power, micro-HDMI and audio (left side of the Pi):** 33 mm lane. ESTIMATE: straight USB-C and micro-HDMI plugs stick out about 20 to 25 mm (I found no datasheet; the official cable's overmold is described as chunky). That leaves about 8 to 13 mm for the cable to bend toward the rear. Behind the Pi (Y > 85) the space opens up to X +102. A straight USB-C power plug should fit with a tight bend. Straight micro-HDMI is borderline; a right-angle micro-HDMI plug or adapter is the safe choice.
- **Pi USB and Ethernet:** plug in from the front through the plate openings. No room is needed inside.
- **Hue power and Ethernet:** these leave toward the rear. The tray ends 7 mm behind the cradle and nothing behind it blocks the cables. Which side the Hue's ports face depends on how it is dropped into the cradle.
- **Keystone rear cable:** the jack is estimated at up to 19 mm wide and 28 to 42 mm deep (catalogue values for common Cat6 jacks). Its cable runs straight back in the free space between the post (-104) and the tray edge (-82.5), about 21 mm wide. Jack-to-cradle clearance is about 1 mm with a 19 mm jack (ESTIMATE).

## Hidden screws
The tray joints use the app's standard screw joint. An M3 screw goes in from behind through each tray upright (3.4 mm clearance) into a boss on the plate (4.0 mm pilot). The plate front has no screw holes, so the only front openings are the keystone and the Pi ports. There is no joint at the Pi end, because the board sits right on the plate's rear face there. That end of the tray hangs about 72 mm past the +29.5 joint, so its stiffness is UNKNOWN.

## Unchanged features kept
Brian's cradle corner posts (good fit with the rounded corners), the Pi ports at the front, the golden keystone at `ks_tight=0.2`, and the 44.4 mm, 4 mm, four-corner-slot plate.

## UNKNOWN
Printed fit, strength, cable bend room, plug sizes, Pi port flushness (the ports are about 1 to 2 mm short of flush, as before), and clearance between the jack and the post. Library item `eq-de5e30c93309` and the rack view still show the older generator version.
