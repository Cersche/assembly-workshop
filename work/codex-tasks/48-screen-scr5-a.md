# Task 48 — SCR5-A, upright 2U Waveshare 5inch DSI LCD (C) plate

Brian's approved concept, 2026-10-29. This is the build specification for Codex; Claude reviews the resulting report and geometry. **Planning only so far: no SCR5-A geometry, STL, 3MF or physical approval exists.** No printing.

## Read first and preserve

Run `git pull`, then read AGENTS.md, PROJECT.md, HANDOFF.md (HP4-M6-B and Rack layout and 5" screen plan), ROADMAP.md, `work/screen-5in/Dimensions.md`, `work/codex-tasks/25-faceplate-44-standard.md`, and this spec. Inspect `outputs/Hue_Pi4_M6-B_2026-10-28/README.md` and its source's `dsi_slot_cut()`; the post-task-47 slot is newer than task 47's original report. Do not rerun that build or alter the bracket. Do not scan the repository broadly.

Preserve all historical parts, Final_3MF, normal-use data, library/revisions, rack-history, artwork, caches and unsaved GUI drafts. Build a new standalone part, without modifying the generic wizard or adding Pi-specific application code. Use Python 3.10 standard library, explicit UTF-8, and OpenSCAD.exe. Do not use OpenSCAD.com. No printing, purchases, public publication, unrelated exports, app restarts, fresh desktop control or physical tests. No subagents for this task. Commit/push to the existing private main branch is authorized; never force-push or make the repository public.

## Deliverables

New folder `outputs/Screen_5in_SCR5-A_2026-10-29/`:

- `src/SCR5-A.scad`, a parameterized source with plate, frame and assembled-preview selectors; `src/SCR5-A_build.py`, a reproducible explicit build/check/pack entry point.
- `SCR5-A_plate.stl` (faceplate with integrated short pocket) and `SCR5-A_frame.stl` (removable rear clamp frame), in a documented common assembly frame.
- `SCR5-A_screen_plate_and_frame.3mf`: exactly two separate named mesh objects, `SCR5-A plate` and `SCR5-A rear frame`, laid flat side by side with a documented positive gap, min print Z=0 each. No screen dummy, hardware, route line or reference bracket in the delivery 3MF.
- `SCR5-A_parameters.json`, `README.md`, and `checks/` with dimensional, topology, clearance, preservation and 3MF round-trip evidence. Parameters and README distinguish Brian's requirements, vendor nominal dimensions, provisional design choices and UNKNOWN measurements.
- `work/codex-tasks/48-screen-scr5-a-REPORT.md`; local viewers under `work/mesh-viewer/SCR5-A-*.html` (not committed). Report references precise source and mesh SHA-256 hashes.

If hardware or geometry checks block an honest delivery, retain source and review previews, label them incomplete, and report the specific blocker. Do not issue a manufacturing-ready set with silently invented hardware.

## Coordinate contract and rack mounting

Use X horizontal (negative left **viewed from the front**), Y positive into rack, and Z up from the bottom of U3. Plate front Y=-4, rear Y=0. Screen upright, centred at X=0 and Z=44.45. U4 is immediately above U3; U5 starts at Z=88.90 in this local frame. Global rack U1 starts at Z=0, so this part's local Z adds 88.90 for a rack-space overlay.

**Explicit dimension reconciliation:** Brian requests exactly 252 x **88.8** x 4 mm, radius 2.5 mm. Task 25's older multi-U formula gives 88.85 mm for 2U, although it calls the standard 44.4 per U. For this standalone SCR5-A, use Brian's explicit 88.8 mm height, centred across two 44.45 mm rack units: X=-126..126, Y=-4..0, Z=0.05..88.85. Do not change the app's formula or the rack pitch. Report this 0.05 mm difference explicitly.

Eight through rack slots, four per U, each the existing horizontal 10 x 7 mm capsule:

| X | local Z centres |
|---|---|
| -118.2625 and +118.2625 | 6.323, 38.127, 50.773, 82.577 |

These are `i*44.45 + 22.225 +/- 15.902` for i=0,1. Preserve slot shape and orientation from the standard. No M6 tray joints, tray, rack-frame changes or extra visible front fasteners. Rear structure must fit the rack's documented clear envelope; use +/-104 mm as the inherited screening boundary, not a physical fit guarantee.

## Vendor envelope and front lip

All dimensions below are Waveshare drawing nominal values transcribed in Dimensions.md, not measurements:

| Feature | mm |
|---|---|
| Glass W x H | 120.7 x 77.2 |
| Active area W x H | 109 x 65.8 |
| Total glass-front to rear component depth | 12.6 |
| PCB W x H | 121 x 76 |
| Four M2.5 corner-hole pattern | 113 x 68, nominal 4 from PCB edges |

The glass/PCB registration, active-area offset inside glass, PCB thickness, component heights, hole construction and glass thickness are not established. Do not confuse the screen's nominal M2.5 x 4 stand-hole callout with Brian's screw length or insert dimensions. Do not use the separate Pi mounting pattern.

Glass loads from behind into a clearance pocket, against a front retaining lip on the glass black border. Initial lip target is 3 mm on each side: a rectangular 114.7 x 71.2 aperture if the glass is centred. This leaves a nominal 2.85 mm horizontal / 2.7 mm vertical margin around a **centred** active area, and 5.8 mm of plate above/below nominal glass. Those margins are arithmetic, not proof of border placement. Aperture corner rounding must not intrude into the active area. Do not enlarge the lip simply to hide mounting bosses.

Expose separate parameters for glass X/Z clearance per side, PCB X/Z clearance, glass-to-PCB registration, screen seating depth, lip overlap for each edge, aperture corner radius, active-area X/Z offset, active-area keepout margin, pocket wall thickness, pocket depth and rear-frame clearance. Explicitly define the datum and units for each. Default active-area offsets of zero may be used for a concept preview only, with an unresolved-registration warning. Check the full active rectangle and its corners against every opaque lip/boss/rib in front projection; UNKNOWN registration precludes a verified "never covered" claim. Ask for registration evidence only if it prevents the next step; never treat a presumed centred active area as measured.

The nominal PCB is wider than the glass: the pocket must clear both, including the rear insertion path. Never size a passage from glass width alone. Show the insertion/removal sequence, not merely assembled clearance.

## Pocket, clamp and hardware

Integrated rear pocket target is approximately 20 mm **from the plate rear Y=0 to its rear-most fixed structure**; frame and screws are included in an overall envelope report. Compare that space with the screen's 12.6 mm envelope and seating position. Do not treat the remaining nominal space as a proven ribbon bend allowance. Keep the back mostly open for components, connectors and service.

Rear clamp frame engages the screen's four corner holes at nominal screen-centred X=+/-56.5, Z=44.45+/-34 (10.45, 78.45), adjusted only by explicit PCB registration parameters. Use Brian's M2.5 heat-set inserts in printed parts and existing M2.5 screws. Design the actual fastening stack in section: identify insert host, insertion direction, screw entry, frame/PCB bearing surfaces, screw path, engagement, tip clearance and how the frame retains to the plate. A frame attached only to the PCB but free to leave the pocket is not a retaining design. Reuse these four fastening positions where feasible; do not quietly add a different hardware system.

**Hardware status at spec creation:** Brian replied `2.5x4x3.5`. This is his exact notation, not yet a confirmed ordering of thread/length/OD. Likely interpretation M2.5 thread, 4 mm length, 3.5 mm OD awaits confirmation. Screw length under the head remains UNKNOWN. Record subsequent confirmation in this spec and the report; until then `insert_od`, `insert_length` and `screw_length` are UNKNOWN, not guessed production values. Screw head diameter/height, PCB hole type and usable thread engagement also need evidence where relevant. An insert pilot diameter is a separate design/process parameter, not the nominal OD itself; no generic press-fit subtraction is certified.

Expose insert seat/pilot diameter, insert length/OD, boss wall, clearance-hole diameter, frame thickness, PCB bearing/stand-off height, screw length/head envelope, insertion lead-in and tip clearance. No M6 is required here: this screen mounting is Brian's explicit M2.5 exception to bracket-joint redesign guidance.

Critical feasibility checks: at +/-56.5 and +/-34 the nominal corner axes project into the proposed aperture's outer border. Boss radii can intrude into the active-area keepout or interfere with the glass while loading. Check their full geometry and tool access, including the top/bottom plate margins; do not assume the 113 x 68 pattern alone proves clearance. Keep rigid stops/support on suitable PCB mounting regions and avoid squeezing unsupported glass, components or ribbon connectors. Contact pressure, compression, material and strength remain UNKNOWN; no torque or load claim.

Engrave **SCR5-A** on the rear frame, not the visible front. Make depth/size parameters, keep positive remaining wall, and place it clear of screws, contact surfaces, buttons and ribbon. Verify the engraving exists in the delivered mesh. Use SCR5-A in filenames, folder, README and report. No coupon or printing is authorized.

## Ribbon and buttons

Screen connector location is approximate: about 8 mm inward from its left edge **seen from front**, in the upper half. Nominal X is roughly -52 mm; exact X/Z, connector projection, ribbon width, thickness, contact orientation and bend radius remain UNKNOWN. Do not mirror the screen or rotate it to align the cable.

Provide an adjustable top-left pocket/frame notch or slot with rounded contact edges, preserving glass retention and fastening strength as UNKNOWN. Define notch X/Z centre, width, depth and edge radius as parameters; label any provisional values. Allow the ribbon to exit upward, without removal of the plate or screw pinching.

Route toward HP4-M6-B's existing floor slot **X=-86..-62, Y=87..95** in the U5 tray source frame. U5's local Z must be translated +88.90 relative to this screen part; verify Y datums before combining frames. The screen connector and floor slot are not at the same X or Y: show the lateral and rearward route. Keep HP4-M6-B unchanged. Provide an assembled route sketch/coordinate table and a path-length estimate with explicit assumptions for connector insertion/slack/bends. The 160 mm ribbon is borderline in the handoff; never claim it reaches from straight-line distance or a nominal connector estimate. **Ribbon reach/bend room stays UNKNOWN.** Source-level inspection and a diagram suffice; if a reference STL/3MF is opened, apply the viewer rule below and keep its licensed mesh out of distributable assets.

Provide rear finger access to top-edge backlight and brightness buttons, with parameterized opening position/width/height/depth and tool/finger approach. Button positions and actual access remain UNKNOWN. Keep the touch header and mid-board FPC clear. Model provisional keepout envelopes for review with clearly labelled provenance, not as measured component geometry. Confirm notch and button access do not sever the frame, close the insertion path or remove required fastener support.

## Acceptance and evidence

1. Record source/data baselines and hashes for protected files before work. Only new SCR5-A outputs, task report and handoff should change by default. No historical regeneration. Run focused checks for the new standalone builder; run the existing app suite only if app code is changed (scope expansion must be explained).
2. Validate finite positive parameters and meaningful inequalities. UNKNOWN hardware cannot quietly become zero or a guessed value; allow an explicitly labelled concept preview but block hardware-dependent final exports until configured. Check pocket/PCB/glass insertion clearance, aperture versus active keepout, fastening stack, screw engagement/tip clearance, component keepouts, notch/buttons and engraving wall. Separate conditional digital checks from unresolved dimensions.
3. Explicitly render with OpenSCAD.exe. Each printable part must be one closed connected shell with consistent winding, no zero-area faces, nonmanifold edges or self-intersection. Check parsed exact coordinates before any tolerant comparison; do not hide defects by rounding/welding or nudging parts. Verify plate bounds, all eight slots and orientation, screen centre and overall rear envelope from geometry. Include assembly intersections with intended contacts distinguished from material collisions. Report every skipped/conditional check.
4. Package without scaling or changing geometry: exactly two named mesh resources/build items, mm units, side by side, positive spacing and Z minima zero. Write standard 3MF ZIP content-types and relationships; use a default core namespace so literal `<vertex ...>` and `<triangle ...>` tags appear (no `ns0:`). Parse it back independently; check object names, build references, finite vertices, valid triangle indices, counts, shell closure, positive volumes, transforms/bounds and triangle equivalence to the two input STLs after rigid print placement. Record a load proof from `tools/mesh_viewer.py` too. XML parsing alone does not prove slicer compatibility. Do not claim a slicer load unless actually tested with separately authorized desktop control.
5. Run `python tools/mesh_viewer.py <files...> -o work/mesh-viewer/SCR5-A-review.html -t "SCR5-A — plate and rear frame"` for **every STL/3MF produced, changed or examined**, including review/test meshes retained as evidence. Use additional pages if needed; label assembly versus print coordinates. Check both individual STLs and the final 3MF load. Provide front, rear, assembled and separate-part review views; no false screen mesh in the manufacturing package.
6. Send the viewer page using SendUserFile (`display="render"`) and publish as a **private Artifact** where the host provides those capabilities; return its usable private link. Never substitute a public site. If unavailable in Codex, deliver the local viewer page and explicitly return "private Artifact publishing pending in Claude" for Claude's review step. Do not fabricate an Artifact URL or treat a local file link as publication. Do not commit generated viewer HTML, especially pages embedding reference/licensed meshes.
7. README/report include BOM with UNKNOWN entries, parameters/provenance, assembly sequence, manufacturing files and checks, hashes, unresolved questions and limitations. **Vendor nominal; printed fit, glass retention, ribbon reach, access and strength UNKNOWN. Not printed.** Claude reviews before any approval claim. Do not copy into Final_3MF as a final approved part.
8. Optional equipment integration is deferred by default. If performed after geometry exists: back up the rack document first, preserve library/history/artwork/revisions, prove saved geometry matches the item, use disposable data for acceptance, and place at U4-U3 (U1 bottom), keeping U2 reserved for cooling and U5 unchanged. Do not substitute a generic tray/blank plate for the exact screen design. Do not silently save an existing browser draft. If exact integration needs app work, report it for a separate task.
9. Update HANDOFF.md with actual results and outstanding hardware questions; commit only task-owned changes and push to private main. If the push is rejected, pull/merge without force. Finish with report, files, viewer/Artifact link or precise publication limitation, validation results and remaining UNKNOWNs.
