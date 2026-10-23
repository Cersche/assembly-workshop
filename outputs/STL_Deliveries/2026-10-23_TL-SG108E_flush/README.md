# TP-Link TL-SG108E — 1U, ports flush, rear stop (2026-10-23)

PROPOSED — UNVALIDATED. Replaces both 2026-10-22 TL-SG108E deliveries after Brian's print: ports sat behind the
faceplate, and the switch must not be able to fall out the back.

- Switch depth **100 mm (Brian measured)**; 158 × 25 mm still nominal.
- Switch slides in **from the front**, port side out, until it touches a solid **rear stop** (tray Y 96–100 mm,
  full sleeve height). Its front then sits at the faceplate front (Y = −4): ports flush.
- Sleeve height clearance **0.8 mm** (`sleeve_top`; first tray was tight top to bottom).
- Same layout: switch and tray 15 mm left (`tray_follow`), golden keystone at +88 mm, "UPLINK" engraved with a
  separate inlay part for a second filament (3MF faceplate object = `faceplate` + `UPLINK label`).
- Screws: **visible**, through the faceplate into the sleeve walls (app standard). The hidden joint needs room the
  158 mm switch doesn't leave without setting it back.
- Nothing holds the switch from sliding out the front except friction and cables; fit, retention, strength UNKNOWN.

Source revision: 9c973e2d67a3629258988cb068db29cab882dffc7e768f2304446dadbc8eaae7
Spec: {"dev_w":158,"dev_d":100,"dev_h":25,"u":1,"device_mount":"sleeve","joint":"screw","dev_off_x":-15,"keystones":[88],
"tray_follow":true,"sleeve_top":0.8,"labels":[{"text":"UPLINK","x":88,"z":3.8,"size":4.5}]}
