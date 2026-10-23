# TP-Link TL-SG108E — 1U, ports flush, keyhole detents + rear stop (2026-10-23)

PROPOSED — UNVALIDATED. Replaces both 2026-10-22 TL-SG108E deliveries after Brian's print (ports sat well behind the
faceplate). Hand-patched (`build.py` on the app's generated source), not an app feature.

- Switch depth **100 mm (Brian measured)**; 158 × 25 mm nominal. Ports on the edge with the folded strip + screws.
- **Ports flush:** switch front at the faceplate front (Y = −4). Nothing covers the switch face.
- **Back:** solid rear stop across the sleeve (tray Y 96–100 mm).
- **Front:** two spring detents in the tray floor catch the switch's wall-mount keyholes (Brian: round parts 48.5 mm
  behind the port face, centred on the width, 110 mm apart, 8–9 mm across, very shallow). Each is an 8 × 26 mm arm,
  1.8 mm thick, with a 5 × 4 mm bump **0.6 mm** above the floor: 45° ramp toward the front, 60° face toward the rear.
  About ±1.5 mm of play front/back once caught; firm pull releases it.
- **Assembly:** screw the faceplate on, slide the switch in from the front (ports out) until it clicks over the bumps
  and touches the rear stop.
- Sleeve height clearance 0.8 mm. Layout: 15 mm left, keystone at +88, "UPLINK" with a separate inlay part
  (3MF faceplate object = `faceplate` + `UPLINK label`).
- UNKNOWN: keyhole depth (0.6 mm bump may not hold), exact keyhole position, arm spring/fatigue, fit, strength.

Source revision: 78f2a90e56184516b5944537fbafb2a449b53006d69a43f4c5d63e0f0202ce19 (`.scad` is the patched source).
