# SCR5-G — flush-glass screen plate, test-print ID SCR5-G

2026-10-30. **Review build; NOT printed. Fit, strength and retention UNKNOWN.**

The five manufacturing meshes and plain-tag 3MF implement updated task 51. Brian confirmed the measured metal-frame inset is approximately 1.5 mm on the LEFT and RIGHT, with cables/FPCs at the top/bottom. `LIP=0.8`, `LIP_ON=true`, `LIP_EDGES=[true,true,false,false]` and `FRAME_STEP=1.5` are exposed at the top of `src/SCR5-G.scad`. The side lips are cosmetic only; the rear frame on the standoffs holds the screen and sets its depth. There is no top or bottom lip.

## Geometry and decisions

- Coordinates: front view, X right, Z up, Y back. Plate front and glass front Y=0; plate rear Y=4. Plate 252 x 88.8 x 4, R2.5 outline. SCR5-F's eight 10 x 7 rack slots and exact centres are copied: X ±118.2625, Z 6.323/38.127/50.773/82.577. Plate centre is Z=44.4 (SCR5-F used 44.45); old slot datums are deliberately retained as requested.
- Glass 120.7 x 77.2 x 2.5 at X=33, Z=41.5. Square window 121.1 x 77.6: 0.2 mm per side at its straight wall; front edge expands by an additional 0.3 mm with a 0.3 mm, 45 degree chamfer. Glass bounds Z=2.9..80.1. Scaled bezel estimates 2.8 top / 8.6 bottom give lit centre Z=44.4, zero nominal vertical error. Bezel values are approximate, not caliper measurements.
- Left/right lips: Y=2.5..3.3, extend 0.8 inward from the window edge (0.6 beneath the glass outline after the 0.2 window clearance), leaving 0.9 to the measured metal-frame side envelope. Ends stop 4 mm short of the glass corners. They do not set depth or retain/carry the display; rear-frame screws provide retention.
- Frame seat Y=`13.3+SHIM`, SHIM=0; frame thickness 3. Corner standoff centres 112.9 x 68, centred on the glass. Four M2.5 x 6 socket-cap screws through 2.8 clearance holes into the screen's female standoffs: nominal thread protrusion 3 mm. Actual usable depth and screw fit UNKNOWN.
- Four **printed-in pilot bosses**, not heat-set inserts, attach the frame to the plate: X=-35/101, Z=10/72, OD8, nominal Ø2.1 x 6 pilot from the rear; four additional M2.5 x 6 screws through the 3 mm frame (3 mm nominal engagement). These pilots require physical validation; no insert OD was invented. The task-specific M2.5 requirement applies here. Rear plate ID is engraved 0.5 deep and reads from behind.
- DSI rear envelope: front-left PCB edge, Z=33.5..54.5 (30..51 above PCB bottom), Y=9.1..14.35. Frame excludes this envelope plus 3 mm in every direction. Connector's inward X width is unmeasured; the dummy assumes a conservative 8 mm inward extent, which is explicitly conditional. Open ribbon corridor is 18 mm wide on the left, with a connected horizontal opening and exit above the plate. The Pi stays on its separate U5 bracket; actual routing/reach UNKNOWN.
- Frame has no material across the board centre; touch FPC height 2.0 is represented in the dummy. Its lateral 20 x 10 dummy footprint is an assumption.
- Pins at X=78.5/68.5/58.5, above the glass in the top-right plate band. DROP=0.45 for all three, pending coupon result. Leaf 0.8, nub, bump, ramp/notch and cap hard stop come from SCR5-WP-A. One/two/three cap dots identify positions, not different DROP values. A hidden 0.02 mm cap/stem overlap makes each pin one connected shell; working dimensions are unchanged. Spring motion, force, full-stroke contact and button travel are not physically validated by rest-pose collision checks.

## Measurements and UNKNOWNs

All screen values come from `work/screen-5in/Dimensions.md`; measured entries supersede vendor estimates. PCB 121 x 76 is the task's nominal reference; the photo estimated roughly 77 high. **PCB centred beneath glass is UNKNOWN.** The measured front-to-back layers are cover glass 0.9 + second glass 1.6 (Y=0..2.5), metal LCD frame 3.0 (Y=2.5..5.5), open gap 2.0 (Y=5.5..7.5), PCB 1.6 (Y=7.5..9.1). The metal-frame dummy is inset 1.5 at each side independently of the lip toggle; its unmeasured top/bottom extent conservatively follows the glass. The measured standoff seat is 13.3. The dummy therefore spans 4.2 from PCB back to seat, explicitly representing the 0.2 discrepancy from the separately measured 4.0 standoff height. The caliper seat datum controls this design; the dummy is not an independently established complete screen model. Only the four corner standoffs are represented; inner standoffs do not mount the Pi here.

Unknowns include the metal frame's exact top/bottom outline, cable/FPC envelopes, registration, connector full shape, usable threads, fastener/tool access, pilot sizing, assembly insertion, pin feel/return/overtravel, cable bend/reach, printed fit, strength and retention. Contact and mesh checks do not resolve them. SHIM moves the rear seat/boss datum for later measured tuning; a positive SHIM is not claimed to preserve flush contact on the unchanged nominal dummy.

## Files, orientation and reproduction

`SCR5-G_plate.stl`, `SCR5-G_frame.stl`, `SCR5-G_pin1.stl` .. `pin3.stl`, and `SCR5-G_screen_plate_set.3mf` are the five-part review set. STL coordinates are assembly coordinates for plate/frame; pins retain coupon-local coordinates. `checks/` contains assembled screen reference, separate dummy component meshes, render/intersection logs, acceptance JSON and local viewers. Diagnostic reference STLs are not individual manufacturing parts.

3MF print orientation: plate front down (bosses/leaves rise); frame rear down (3 mm thick); pins on their flat X side. Every object starts at print Z=0, with 12 mm X spacing. This is a geometric orientation suggestion, not a process/support approval. No print is authorized.

From the project root, with Python 3.10 standard library and `C:\Program Files\OpenSCAD\openscad.exe`:

```text
python outputs/Screen_5in_SCR5-G_2026-10-30/src/build_check.py
python outputs/Screen_5in_SCR5-G_2026-10-30/src/verify_geometry.py
python tools/mesh_viewer.py outputs/Screen_5in_SCR5-G_2026-10-30/SCR5-G_screen_plate_set.3mf -o outputs/Screen_5in_SCR5-G_2026-10-30/checks/SCR5-G-print-review.html -t "SCR5-G print review"
```

`build_check.py` reuses the copied SCR5-F meshcheck and a locally adapted SCR5-WP-A plain-tag packer. Original helper copies in src are provenance only; do not execute the old full SCR5-F assembly. A deterministic triangulation repair removes OpenSCAD's exact collinear triangle by splitting its neighbour; no vertices move and no solid volume changes. The supplemental checker also rejects zero-area triangles, which the original helper's repeated-index check alone does not detect.

All 45 manufactured-part / dummy-component pairs and three extra DSI/corridor envelope checks have reported volumes in `checks/acceptance.json`. Exact delivered STL bounds prove disjoint/contact-only pairs; overlapping bounds are checked by OpenSCAD CSG against the delivered meshes. Rest-pose zero intersection does not certify moving spring behaviour. The assembled union reference is for viewing; individual delivered meshes govern manufacturing checks.

Viewer files remain inside this new output folder as requested. SendUserFile/private Artifact rendering is unavailable on this Codex host; local HTML viewers are provided instead, without publishing. No printer/slicer integration, printing, commit, push, Final_3MF copy, application/user-data write, or HANDOFF edit.
