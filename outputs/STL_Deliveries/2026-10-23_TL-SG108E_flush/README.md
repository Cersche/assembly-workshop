# TP-Link TL-SG108E — 1U, front lips + rear stop (2026-10-23)

PROPOSED — UNVALIDATED. Replaces both 2026-10-22 TL-SG108E deliveries after Brian's print: ports sat well behind the
faceplate, and the switch must be held at both the back and the front. Hand-patched (`build.py`), not an app feature.

- Switch depth **100 mm (Brian measured)**; 158 × 25 mm still nominal.
- **Rear stop:** solid wall across the sleeve at tray Y 97.8–101.8 mm; the switch can't go out the back.
- **Front lips:** the faceplate window has a 1.5 mm-thick lip over **4 mm** of each end (left/right) of the switch face.
  The switch sits 1.8 mm back from the plate front (1.5 lip + 0.3 play), so the ports are ~1.8 mm behind the face.
  Assumes the ports leave ≥4 mm of plain case at each end (UNKNOWN; check before printing).
- **Assembly:** slide the switch into the tray sleeve (port side forward) until it touches the rear stop, then screw the
  faceplate on (visible M3 screws into the sleeve walls). The switch is then trapped between lips and stop.
- Sleeve height clearance 0.8 mm. Layout as before: 15 mm left, keystone at +88, "UPLINK" with a separate inlay part
  (3MF faceplate object = `faceplate` + `UPLINK label`).
- Fit, retention, strength, lip strength UNKNOWN.

Source revision: 803b228431541565e5313352d161efd57f175bea65ea28ecabfbd466f8bce7d9 (`…​.scad` is the patched source).
