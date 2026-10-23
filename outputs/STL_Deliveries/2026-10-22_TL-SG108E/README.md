# TP-Link TL-SG108E — 1U sleeve tray + faceplate with UPLINK keystone (2026-10-22)

PROPOSED — UNVALIDATED. Generic `equipment_tray.scad`, sleeve mount, screw joint, 44.4 mm faceplate, four-corner slots.
- Device size used: 158 × 101 × 25 mm (nominal, not measured; measure your unit first).
- Switch slides in **port side (8 × RJ45 + DC power) facing out**; LEDs end up at the back.
- Switch and tray shifted 15 mm left (`tray_follow`); tray spans X −100…+70 mm.
- Golden keystone at X = +88 mm (moved in from +102: its back stays ~5.5 mm inside the 208 mm rack opening, clear of the post), "UPLINK" engraved 0.6 mm deep below it (Liberation Sans Bold, 4.5 mm).
Fit, retention, strength, keystone retention, label legibility and cable bend space are UNKNOWN.
Source revision: 042f4cd20c369a47cabb263db77e1e24d2a643bf31d9f2547d899fc6d4f94398
Spec: {"dev_w":158,"dev_d":101,"dev_h":25,"u":1,"device_mount":"sleeve","joint":"screw","dev_off_x":-15,
"keystones":[88],"tray_follow":true,"labels":[{"text":"UPLINK","x":88,"z":3.8,"size":4.5}]}
