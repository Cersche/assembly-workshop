# HP4-M6-B - Hue + Pi 4 bracket, Pi left / Hue right

Test-print ID **HP4-M6-B**; 0.6 mm engraving on the rear plate at X=34.5, Z=8 and floor at X=34.5, Y=119. **Not printed. Fit, strength and DSI ribbon reach UNKNOWN.**

| File | Purpose |
| --- | --- |
| `HP4-M6-B_Hue_Pi4_M6_set.3mf` | Two named objects side by side, both minimum Z=0 |
| `HP4-M6-B_tray.stl`, `HP4-M6-B_faceplate.stl` | Assembly-coordinate parts, one closed shell each |
| `src/HP4-M6-B.scad` | Patch of immutable HP4-M6-A; no generator rebuild |
| `src/HP4-M6-B_build.py` | Python 3.10 standard library; OpenSCAD.exe; topology/contact checks; pack via tools/plate_layout_stl.py |
| `checks/acceptance.json`, `checks/clearance.json` | Numeric acceptance and clearance evidence; logs/probes alongside |

**Bracket BOM:** 3 x rack M6 heat-set insert + 3 x M6 x 8 button-head screw.

**Pi board mounting (unchanged, pending Brian):** four device insert mounts, 3.2 mm pilots, 6 mm standoffs, Pi holes 2.7 mm. Pi insert specification and board screws remain pending Brian; they are separate from the bracket BOM.

Changes from A are translations only: Pi -148 mm (X -102..-46, rotation 270 and Y unchanged); openings X -93/-75/-56.3; Hue cradle +69 mm to X=34.5; golden keystone +185 mm to X=92.5; ties X=-42.5/-19.5; joints X=-29.5/11/57; floor X=-102..82.5, depth 123.4 unchanged; new IDs at X=34.5. The 33.1 mm lane now lies at X=-46..-12.9. No mirroring of devices, openings, cradle or keystone.

The swap puts the Pi on the connector side of the planned upright, centred Waveshare 5-inch DSI screen in U4-U3 beneath the U5 bracket. **Routing and 160 mm cable reach are not validated.** No ribbon slot or other feature was added.

Preserved: complete A M6 joint geometry, 20 mm tabs plus inherited 4 mm low coves, 14 mm bosses, 7.6 mm bores, 6.6 mm screw clearance, 11.5 x 3.5 counterbores, jzx=[24], screw Z=32.225, tongues/slots; four corner rack slots only; nominal 252 x 44.4 x 4 plate; Pi mounts and openings' dimensions/heights; cradle cut/Z; golden geometry and ks_tight=0.2.

Digital checks: tray 7,256 triangles / 10,884 edges; faceplate 5,232 triangles / 7,848 edges. Each has one shell, zero bad edges and zero inconsistent winding edges. Contact intersection: 760 triangles all exactly Y=0, zero volume. Rear X=-102..102.4 lies inside +/-104. 3MF literal plain vertex/triangle tags: tray 3,620/7,256; faceplate 2,602/5,232; no ns0 prefixes. One collinear tray triangle and two collinear plate triangles remain, as in A; no mesh repair or rounding.

Clearances are documented in `checks/clearance.json` and `../../work/codex-tasks/47-hue-pi4-m6-b-REPORT.md`. Full-joint guaranteed minimum gaps to the checked device/port/cradle/tie/keystone envelopes are 6.5 / 8.4 / 8.4 mm. The lane tab is 6.5 mm from the Pi edge. Low coves extend closer in XY below the board; the rendered full joint still clears the Pi box by 6.5 mm. Cradle right inset 0.5 mm; keystone rear-to-floor gap 0.1 mm; tray ID-to-cradle guaranteed gap 1.246 mm.

Rebuild with `py -3.10 src/HP4-M6-B_build.py` from this folder. The builder requires passing `checks/clearance.json` before rendering/packing. Evidence scripts in `../../work/hue-pi4-m6-47/` regenerate probes and check clearances (`probe-clearance.py`, `check-clearance.py`, then `check-joint-coves.py`; the last uses `checks/lane-joint.scad/.stl`). Keep this evidence with the source. Reassess clearances if source or cradle changes. No automatic build.

The cradle remains imported directly from `C:/Users/brian/Downloads/Swanky Rottis.stl`, never copied. Creator/imported geometry stays local/private; no redistribution outside the authorized private repository. No Final_3MF copy.

UNKNOWN: printed fit/strength, load capacity, insert OD/length, retention, insertion bulging, usable thread engagement, Pi mounting hardware, cable bend room, DSI ribbon reach and slicer behaviour. Digital closure does not establish physical approval. No printing, physical testing, commit or push performed.


## DSI ribbon slot (Brian, 2026-10-29)

Added after task 47: a 24 x 8 mm slot through the tray floor at X -86..-62, Y 87..95, right behind the Pi and centred on its estimated DSI connector (X about -74), so the 160 mm ribbon can drop to the planned U4-U3 screen. Estimated path through the slot about 160 mm: borderline. Rebuilt with `src/HP4-M6-B_build.py`: tray 7,276 triangles, closed single shell; faceplate unchanged. Ribbon reach, connector position and fit UNKNOWN.
