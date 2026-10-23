# TP-Link TL-SG108E — 1U sleeve tray + faceplate, hidden screws (2026-10-22)

PROPOSED — UNVALIDATED. Hand-made variant (`build.py`), not an app feature. Same layout as `../2026-10-22_TL-SG108E/`
(switch 15 mm left, ports facing out, golden keystone at +88 with "UPLINK" engraved), but **no screw heads on the front**.

Why hand-made: the app's hidden joint sits outside the sleeve walls and only fits devices up to 150 mm; this switch is 158 mm.
What `build.py` changes on the app's generated source:
- The switch sits **17 mm back** inside the sleeve (tray 17 mm deeper, 122 mm). The two hidden joints (tongue, plate boss,
  tray upright, same dimensions as task 41) sit **in front of the switch**, at X = -91 and +61 mm.
- The faceplate window is narrowed to **130 mm** (the 128 mm port cavity from the STEP + 1 mm each side, assumed centred),
  so the plate is solid behind the bosses.
- **No rear stop:** the switch slides in **from the rear** and stops against the two joint uprights. Hold it with a strap
  through the sleeve strap slots if needed.

Assembly: put the faceplate on, drive the two M3 screws from behind through the uprights into the plate bosses, then slide
the switch in from the rear.

Checked: both STLs closed (watertight); ray probes show plate solid at the joints, pilot holes open, uprights solid, tray
clearance holes open, window open, no rear stop. Not opened in a slicer by Claude.
UNKNOWN: port cavity width/centring (from STEP, not measured), 158 × 101 × 25 case (nominal), whether 17 mm of cable
recess suits the RJ45 latches, fit, retention, strength, driver access.

Files: `…_tray.stl`, `…_faceplate.stl`, `…_2-parts-print-layout.3mf` (both parts flat, separate objects; no colored UPLINK
inlay in this one, the engraving is still there), `TL-SG108E_hidden-screws.scad` (patched source).
