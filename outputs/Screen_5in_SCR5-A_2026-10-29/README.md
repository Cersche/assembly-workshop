# SCR5-A — incomplete concept review, NOT manufacturing ready

2026-10-29. Upright, centred Waveshare 5inch DSI LCD (C), U4–U3 under the unchanged U5 HP4-M6-B. **Not printed. Vendor dimensions nominal; printed fit, glass retention, access, ribbon reach and strength UNKNOWN. Claude/Brian geometry review required.** No Final_3MF copy or equipment integration.

The requested STL names and two-object 3MF exist for review. Their presence is not an accepted manufacturing delivery. `--final` deliberately rejects this configuration before rendering or replacing files. The specific blocker is the fastening carrier: its insert ring fits **between the glass and PCB**, requiring a currently unmeasured gap and a preassembly path into that gap. The ring is not a proven clamp that can simply be fitted behind a complete delivered display. Four side hooks capture it to the faceplate pocket, so it is not merely a loose frame attached to the PCB; hook flex, preload and assembly feasibility remain unverified.

Brian's follow-up: the screen has not arrived. Keep the glass/PCB gap UNKNOWN and tunable; assume plain PCB through-holes without treating that as confirmation. Default the screw-head envelope to ISO 4762 socket cap, 4.5 diameter × 2.5 high; actual screw type/size UNKNOWN. These assumptions permit a concept build, not hardware certification. No purchase or physical work is authorized.

## Files and explicit build

- `SCR5-A_plate.stl`, `SCR5-A_frame.stl`: common assembly datums below, review only.
- `SCR5-A_screen_plate_and_frame.3mf`: exactly `SCR5-A plate` and `SCR5-A rear frame`, separate mesh objects, no screen dummy/hardware/route/reference mesh.
- `SCR5-A_parameters.json`: requirements, vendor provenance, provisional numeric choices and separate null UNKNOWN measurements.
- `src/SCR5-A.scad`: plate/frame/assembled/screen/no_id/intersection selectors. The assembled selector includes nominal glass/PCB and labelled-in-source provisional touch/FPC keepout boxes; these are never manufacturing objects.
- `src/SCR5-A_build.py`: Python 3.10 standard-library builder, strict mesh checks, independent 3MF reopen, focused geometry checks and viewers. `SCR5-A_config.scad` is generated from JSON; do not edit it as an independent parameter source.
- `src/SCR5-A_geometry_checks.py`, `src/SCR5-A_review.py`: focused checks and review/route generation.
- `checks/`: machine-readable actual results, logs, hashes, route diagram, baseline/preservation and retained rejected/comparison probes.

From the project root, explicitly run:

```powershell
python outputs/Screen_5in_SCR5-A_2026-10-29/src/SCR5-A_build.py --review
python outputs/Screen_5in_SCR5-A_2026-10-29/src/SCR5-A_build.py --check-only
python outputs/Screen_5in_SCR5-A_2026-10-29/src/SCR5-A_build.py --final
```

The last command must fail with `FINAL EXPORT BLOCKED`; its rejection is recorded in `checks/final-gate.log`. No background/automatic build. Renderer: `C:/Program Files/OpenSCAD/openscad.exe`; no `.com` launcher, dependency installs, font download, app launch, desktop control or slicer test. OpenSCAD font lookup can vary by host; exact output hashes and local build context are recorded rather than promising byte identity across hosts.

## Coordinate contract and geometry

X negative is left viewed from the front; Y positive is rearward, plate rear Y=0; Z up from U3 bottom. Screen centre X=0, Z=44.45. Rack global Z = local Z +88.90. U5 starts screen-local Z=88.90; HP4's source also uses plate rear Y=0, so Y needs no translation.

Brian explicitly requests **252 × 88.8 × 4**, corners 2.5: X ±126, Y −4..0, Z 0.05..88.85. Task 25's older 2U formula is 2×44.45−0.05=88.85, Z 0.025..88.875. This standalone plate is 0.05 shorter, centred on the same 44.45 datum. App geometry and rack pitch are unchanged. Exact parsed float32 limits are in topology.json; OpenSCAD's grid/export gives Z 0.0500059128..88.8499908447 before any tolerant dimensional comparison. No vertex welding, rounding, repair or part nudging.

Eight horizontal 10×7 capsule slots: X ±118.2625; Z 6.323, 38.127, 50.773, 82.577. Parsed boundary measurements and ray checks verify all eight, including their horizontal orientation and through openings. No tray or M6 joint.

Nominal glass 120.7×77.2, PCB 121×76, active 109×65.8, glass-front to rear component depth 12.6; screen holes 113×68. These are drawing transcriptions, not measurements. Hole axes X ±56.5, Z 10.45/78.45. The separate Pi pattern is unused. Vendor “M2.5 × 4” stand callout does not establish screw length, insert dimensions or threaded PCB holes.

Four independent 3 mm lip overlaps produce a 114.7×71.2 aperture, radius 0.75. A centred active rectangle would leave arithmetic margins 2.85 horizontal / 2.7 vertical before the 0.25 keepout. Its full four keepout corners clear the rounded aperture **only under the zero-offset assumption**. Actual active/glass/PCB registration UNKNOWN. Each 3.25-radius boss overlaps that assumed keepout in front projection (signed radial gap −1.30449); the boss sits behind nominal glass, but this is not evidence of optical or internal display clearance. The lip was not enlarged to conceal bosses.

Pocket inner X ±65.75, Z 4.85..84.05; wall 3, outer X ±68.75, Z 1.85..87.05; rear Y=20. The widened cavity clears both the larger PCB and nominal glass, and gives the side clips room to retract. This is within the inherited ±104 digital screening boundary, with no rack-fit guarantee. The two outer retaining hooks reach X ±67.75. Each retracts nominally 2.25, leaving 2 mm to the assumed PCB edge; clip strain/material/process and clearance to unknown peripheral components remain UNKNOWN. Rear force is reacted by hooks at Y=18.5 against pocket-window rear shoulders at Y=19, with 0.5 free play. Nominal beam contact with the pocket is at X ±65.75 only; actual CGAL intersection has zero volume on these two planes.

Glass front seats against the lip rear at Y=0. `glass_t=2` and **`glass_pcb_gap=6` are unmeasured concept choices**. The latter is free space from glass back to PCB front, not the vendor total depth. Derived `pcb_front_y=seat_y+glass_t+glass_pcb_gap=8`; PCB thickness assumption 1.6 gives rear Y=9.6; nominal overall screen depth still ends at Y=12.6. `frame_front_y=pcb_front_y-frame_t-bearing_h=3`, frame ring 3..8, clips to 18.5. Overall assembly rear remains 20, not 20+12.6. Nominal spare depth is not a ribbon-bend certification.

Tuning the gap moves the insert ring without rewriting SCAD. The builder rejects a gap that cannot contain the 5 mm ring behind glass; reducing ring thickness is constrained by the 4 mm inserts, seat floor and wall checks. If the real screen lacks this space or has inaccessible/interconnected glass/PCB structure, this architecture needs redesign. No parametrization can prove that unknown assembly path.

## Conditional hardware stack and BOM

| Quantity | Item | Evidence / limit |
| --- | --- | --- |
| 1 each | SCR5-A plate and carrier frame | Concept geometry only |
| 4 | M2.5 heat-set, length 4, OD 3.5 | Brian confirmed nominal dimensions; printed fit/usable engagement UNKNOWN |
| 4 | M2.5 × 5 screws | Selected conditional length; existing inventory/actual head UNKNOWN |
| 8 | Existing rack faceplate fasteners | Normal rack mounting; no new M6 tray joints |

Insert host is the carrier ring, inserted from its rear Y=8 toward the front, nominal metal span Y=4..8. Pilot is separately adjustable Ø3.4, depth 4.2, rear 0.3 lead-in; nominal OD 3.5 is not a certified pilot recommendation. Pilot floor is 0.8. Screws enter from behind the PCB toward −Y, heads bear on assumed suitable PCB corner mounting lands at Y=9.6, pass the assumed plain holes, then engage the inserts. No torque/compression claim and no washer silently added.

With 1.6 PCB and zero additional bearing offset, selected under-head length 5 gives nominal engagement 3.4, tip Y=4.6 and 0.6 to the nominal insert front. Chosen screening minimum engagement 2.5 and tip reserve 0.4 give an arithmetic length range **4.1..5.2**. Neither minimum engagement nor usable insert thread has physical validation. Tune `pcb_t`, `bearing_h`, insert geometry and `screw_length` together; length outside the configured range blocks review export. Screw length is not a missing fixed user decision.

Assumed head Ø4.5×2.5 gives rear Y=12.1. `head_clearance_d=0.6`, `head_clearance_h=0.3` produce a Ø5.1×2.8 counterbore-shaped access envelope; tool diameter 5.5. In this carrier architecture that relief opens into free space behind the PCB: there is **no printed rear head seat/counterbore to claim**. The source subtracts the access envelope to keep it clear if adjoining frame geometry changes. The requested conventional rear clamp with actual counterbores is consequently not established by this concept. Head/driver/body access remains UNKNOWN.

Conditional assembly path: install inserts before bringing heat near electronics; gain access to the glass/PCB interspace, place the carrier ring against suitable PCB front corner lands, then install screws from the rear. This first step is unproven on the vendor assembly. With the resulting screen/carrier subassembly, retract the four hooks, load straight from the back through the pocket and let the glass meet the lip; release hooks into side windows. Reverse by squeezing/retracting clips from the sides, supporting the screen, and removing the whole unit rearward. No plate removal is assumed for button/ribbon access. Actual heat-set process, interspace access, release force, screen pressure and removal clearance remain UNKNOWN.

## Access, ID and routing

Top-left ribbon opening: X=−52, width 18, Z centre 83.05, rounded X/Z contact silhouette radius 1, cut Y=11..20, above the nominal glass border and behind the insert ring. Top-button rear approach: X=0, width 38, Z=84.05, height 12, Y=11..26, silhouette radius 1. These are provisional openings; 3D mouth-edge finishing, actual button/finger access, cable width/bend radius/contact orientation and connector clearances are unverified. Neither cut removes the four bosses or severs the frame. Touch/FPC boxes are visibly provisional in the SCAD assembled selector; measured devices may differ.

SCR5-A is engraved **only on the frame rear**, 0.5 deep, size 3, at X=0/Z=8.3, rounded/5° angled lettering. The mesh comparison to the unengraved probe proves removed material and the engraving floor; 4.5 mm ring wall remains. Plate front is unmarked. Initial default text produced three exact zero-area triangles and was rejected; retained probe is explicitly not a manufacturing part. A separate intermediate bridge had an 80 mm³ collision, also retained/rejected; the final bridge has boundary contact only.

HP4 source was read, never rebuilt/opened as a mesh. Its `dsi_slot_cut()` is X −86..−62, Y 87..95, through U5 floor Z=8.225..11.225: screen-local Z=97.125..100.125. Route points and source verification are in `checks/ribbon-route.json`; diagram `checks/SCR5-A-route.svg`. The assumed connector (−52,13.1,66.45) exits upward, shifts left to X=−74, runs rearward to Y=91, passes the slot and returns toward the assumed Pi connector (−74,81,110.4). A polyline estimate plus separately stated insertion/slack/bend reserves is illustrative only. It does not establish 160 mm reach or absence of obstructions.

## Digital checks, packaging and viewer status

Both delivery meshes: one closed consistently wound shell, positive volume, no degenerate faces, bad edges or winding errors. Exact coordinates checked first. Numerical AABB/triangle screen finds no nonincident transverse intersections or coplanar area overlap; incident edges are excluded, predicates use 1e−9 mm. This is not an exact-arithmetic self-intersection certificate. CGAL assembly intersection is contact only, zero volume. Provisional touch/FPC boxes clear frame triangle bounds; actual components and screen preassembly remain UNKNOWN. No actual screen mesh or physical insertion test.

3MF rotation `(x,y,z)→(x,−z,y)` followed by translation only: plate front down, carrier ring front down, separate objects with a 12 mm X gap and exact print minima Z=0. No scaling. Each resource's triangle indices and every rigidly placed vertex are independently compared to its STL. mm units, object/build names/counts, index validity, topology, positive volumes, ZIP content types/relationships, literal plain `<vertex>`/`<triangle>` tags and absence of `ns0:` are checked. Slicer loading NOT TESTED. The long combined bed footprint is a layout only; no printer integration or bed-fit claim.

Local review hub: `work/mesh-viewer/SCR5-A-index.html`; generated by the explicit builder. Front, rear, assembled/common-datum, separate STL, 3MF and retained-probe pages all derive from `tools/mesh_viewer.py`. Parser/load checks ran; interactive visual inspection did not run. Viewer HTML stays uncommitted. **Private Artifact publishing pending in Claude**: this Codex host has no SendUserFile/private Artifact publication capability. Local links are not publication; no public hosting substituted.

149 protected hashes compare unchanged (HANDOFF excluded for its authorized update), including the previous run's local-preservation folder, both HP4 revisions, Final_3MF and official user data. The preservation record is a targeted checkpoint, not a full backup or live-draft inspection. Existing app code/data were not modified, no app checks/restart or rack saves were needed. No printing, purchases, public publication or desktop control. Commit/push to private main is authorized by this task; exact session result is in task 48 report/HANDOFF.

Task-local `.gitattributes` disables line-ending conversion inside this new output folder so the exact recorded source/config/parameter/mesh bytes survive Git synchronization. It changes no historical folder attributes.
