# TP-Link TL-SG108E — 1U, ports flush, keyhole detents + rear stop (2026-10-23)

PROPOSED — UNVALIDATED. Replaces both 2026-10-22 TL-SG108E deliveries after Brian's print (ports sat well behind the
faceplate). Hand-patched (`build.py` on the app's generated source), not an app feature.

- Switch depth **100 mm (Brian measured)**; 158 × 25 mm nominal. Ports on the edge with the folded strip + screws.
- **Ports flush:** switch front at the faceplate front (Y = −4). Nothing covers the switch face.
- **Back:** solid rear stop across the sleeve (tray Y 96–100 mm).
- **Front:** two spring detents in the tray floor catch the switch's wall-mount keyholes (Brian: round parts 48.5 mm
  behind the port face, centred on the width, 110 mm apart). Bump **2 mm** high (Brian, after coupon KD-D at 3 mm locked very nicely); floor
  **6.5 mm** (coupon KD-E) so the 8 × 26 × 1.8 mm arm bends into a pocket inside the floor instead of out the bottom.
  The switch and window sit 3.5 mm higher than with a 3 mm floor (still 1U).
- **Hidden screws:** no holes through the faceplate front. Two 9 mm bosses on the plate back above the window
  (4.0 mm pilot, 7 mm deep: heat insert or self-tap), X = −92.5 and +62.5, Z ≈ 39.4; two 12 × 6 mm uprights on the
  sleeve's top lips, 0.3 mm behind the bosses. **2 × M3 ~12 mm**, driven from behind over the top of the switch.
- **Assembly:** set the faceplate against the sleeve front, screw it on from behind, then slide the switch in from the
  front (ports out) until it clicks over the bumps and touches the rear stop.
- Sleeve inside height **26.35 mm** (25 mm switch + 1.35 mm, Brian). Layout: 15 mm left, keystone at +88, "UPLINK" with a separate inlay part
  (3MF faceplate object = `faceplate` + `UPLINK label`).
- UNKNOWN: thick-floor version unprinted (KD-E), exact keyhole position, arm spring/fatigue, fit, strength.

Source revision: 8996fd7e4dbfd993e97bdee6d7720fe838209e5a9291b36f9a3b5827d70f50d5 (`.scad` is the patched source).
