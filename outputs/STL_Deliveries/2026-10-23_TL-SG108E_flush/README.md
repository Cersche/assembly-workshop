# TP-Link TL-SG108E — 1U, ports flush, keyhole detents + rear stop (2026-10-23)

PROPOSED — UNVALIDATED. Replaces both 2026-10-22 TL-SG108E deliveries after Brian's print (ports sat well behind the
faceplate). Hand-patched (`build.py` on the app's generated source), not an app feature.

- Switch depth **100 mm (Brian measured)**; 158 × 25 mm nominal. Ports on the edge with the folded strip + screws.
- **Ports flush:** switch front at the faceplate front (Y = −4). Nothing covers the switch face.
- **Back:** solid rear stop across the sleeve (tray Y 96–100 mm).
- **Front:** two spring detents in the tray floor catch the switch's wall-mount keyholes (Brian: round parts 48.5 mm
  behind the port face, centred on the width, 110 mm apart). Bump **3 mm** high (coupon KD-D locked very nicely); floor
  **6.5 mm** (coupon KD-E) so the 8 × 26 × 1.8 mm arm bends into a pocket inside the floor instead of out the bottom.
  The switch and window sit 3.5 mm higher than with a 3 mm floor (still 1U).
- **Assembly:** screw the faceplate on, slide the switch in from the front (ports out) until it clicks over the bumps
  and touches the rear stop.
- Sleeve height clearance 0.8 mm. Layout: 15 mm left, keystone at +88, "UPLINK" with a separate inlay part
  (3MF faceplate object = `faceplate` + `UPLINK label`).
- UNKNOWN: thick-floor version unprinted (KD-E), exact keyhole position, arm spring/fatigue, fit, strength.

Source revision: 151cccb37788878415b720d7806eb9b4b3b659b400a279192379f2bd7a2775f2 (`.scad` is the patched source).
