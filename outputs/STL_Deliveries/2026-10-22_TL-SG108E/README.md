# TP-Link TL-SG108E — 1U sleeve tray + faceplate with UPLINK keystone (2026-10-22)

PROPOSED — UNVALIDATED. Generic `equipment_tray.scad`, sleeve mount, screw joint, 44.4 mm faceplate, four-corner slots.
- Device size used: 158 × 101 × 25 mm (nominal, not measured; measure your unit first).
- Switch slides in **port side (8 × RJ45 + DC power) facing out**; LEDs end up at the back.
- Switch and tray shifted 10 mm left (`tray_follow`); tray spans X −97…+77 mm.
- Golden keystone at X = +102 mm, "UPLINK" engraved 0.6 mm deep below it (Liberation Sans Bold, 4.5 mm).
Fit, retention, strength, keystone retention, label legibility and cable bend space are UNKNOWN.
Source revision: d50bc9b59e5a0eb06ebf35cb70a475b450c707adfe4ab99c8e94685b03ffeee9
Spec: {"dev_w":158,"dev_d":101,"dev_h":25,"u":1,"device_mount":"sleeve","joint":"screw","dev_off_x":-10,
"keystones":[102],"tray_follow":true,"labels":[{"text":"UPLINK","x":101,"z":3.8,"size":4.5}]}
