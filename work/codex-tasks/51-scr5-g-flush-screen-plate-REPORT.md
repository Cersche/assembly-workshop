# Task 51 — SCR5-G flush-screen plate report

2026-10-30, built in `D:\Projects\assembly-workshop`.

**SCR5-G built to the updated task 51 specification, including the cosmetic lips on LEFT and RIGHT only.** Brian clarified the layer stack and measured approximately 1.5 mm from each glass side to the metal LCD frame; top/bottom have cables/FPCs and no lip. `LIP=0.8`, `LIP_ON=true`, `LIP_EDGES=[true,true,false,false]`. The rear frame on the standoffs holds the screen and sets depth; the lips are cosmetic only. **Not printed; fit, strength and retention UNKNOWN.** Final digital acceptance results are below.

## Deliverables and decisions

New folder: `outputs/Screen_5in_SCR5-G_2026-10-30/`. Contains parameterized `src/SCR5-G.scad`, five manufacturing STLs, `SCR5-G_screen_plate_set.3mf`, README, copied original helpers, adapted stdlib build/pack/check scripts, and `checks/` evidence/reference/viewers. No build output was written outside that folder. This requested report is the only additional document written.

Plate 252 x 88.8 x 4, outline R2.5, eight SCR5-F rack slots at unchanged centres. Glass X=33, Z=41.5; glass/plate front Y=0. Window 121.1 x 77.6, square corners, exact 0.3 front chamfer. Nominal lit centre Z=44.4 matches plate centre; its bezel input remains a scaled estimate from Dimensions.md. Left/right cosmetic lips occupy Y=2.5..3.3 and extend 0.8 inward from the window, leaving 0.9 nominal clearance to the metal frame; no top/bottom lip. Frame seat 13.3 + SHIM (default 0), four measured 112.9 x 68 corner standoffs; M2.5 x 6 screws through a 3 mm frame. Four printed-in Ø2.1 pilots in OD8 plate bosses attach the frame with four additional M2.5 x 6 screws (nominal 3 mm engagement). Pilot/usable thread fit UNKNOWN; no heat-set dimensions invented.

DSI clearance box spans 30..51 above PCB bottom, Y=9.1..14.35, inflated 3 mm around the assumed connector envelope. Frame has an open 18 mm left/up ribbon corridor and no crossbar over the touch FPC. Pins at X=78.5/68.5/58.5 retain the coupon leaf/nub/bump/ramp/notch/cap design; all use DROP=0.45. The cap/stem joint has a hidden 0.02 mm overlap to ensure one shell; functional ramp and hard-stop dimensions are unchanged. Plate rear has readable engraved SCR5-G.

All screen measurements were taken from updated `work/screen-5in/Dimensions.md`. Layers are cover glass 0.9 + second glass 1.6 (Y=0..2.5), metal LCD frame 3.0 (Y=2.5..5.5), gap 2.0 (Y=5.5..7.5), PCB 1.6 (Y=7.5..9.1). The metal-frame dummy has the measured ~1.5 inset at each side, independently of lip settings; top/bottom extent conservatively follows the glass because exact outline/cable envelopes remain UNKNOWN. PCB centred beneath glass is explicitly UNKNOWN. PCB 121 x 76 is the task's nominal dummy, not the ~77 photo estimate. The 13.3 measured seat controls over the separately summed 13.1 stack: the dummy corner standoff span is 4.2 above PCB back, exposing that 0.2 discrepancy rather than claiming the measured 4.0 and total stack agree. DSI inward width is an explicit 8 mm assumption; touch dummy lateral footprint is an assumption. Actual connector shape, insertion, screw access, ribbon reach and moving-pin behaviour remain UNKNOWN.

## Digital acceptance results

`python outputs/Screen_5in_SCR5-G_2026-10-30/src/build_check.py` completed successfully. Copied SCR5-F meshcheck and the stricter zero-area/winding/connectivity check agree on the five manufacturing parts:

| Part | Vertices | Triangles | Shells | Bad edges | Degenerate | Volume mm³ |
|---|---:|---:|---:|---:|---:|---:|
| Plate | 2,990 | 6,024 | 1 | 0 | 0 | 51,705.009494 |
| Frame | 986 | 1,996 | 1 | 0 | 0 | 8,840.625382 |
| Pin 1 | 120 | 236 | 1 | 0 | 0 | 236.970230 |
| Pin 2 | 216 | 428 | 1 | 0 | 0 | 236.722830 |
| Pin 3 | 312 | 620 | 1 | 0 | 0 | 236.475431 |

OpenSCAD emitted one exactly collinear plate triangle at a leaf root. The deterministic repair removes it and splits the adjacent long-edge triangle without moving any vertex or changing volume; the final mesh has no zero-area triangles. Initial tests also caught the copied coupon's face-only cap/stem connection; the overlap described above resolved it. No historical source or mesh was edited to address either issue.

The assembled reference includes plate, frame, three pins, glass, LCD box, PCB, four corner standoffs, measured button bodies/plungers, DSI box and touch FPC envelope. Pairwise **intersection volumes in mm³** follow (dash means self/already listed). All 45 pairs were checked; exact delivered-mesh AABB separation/boundary contact establishes zero where applicable, and overlapping bounds use OpenSCAD CSG on the delivered STLs. Zero-volume contact at boss/frame and screen/frame seats is intended.

| Other part | Plate | Frame | Pin 1 | Pin 2 | Pin 3 |
|---|---:|---:|---:|---:|---:|
| Frame | 0 | — | — | — | — |
| Pin 1 | 0 | 0 | — | — | — |
| Pin 2 | 0 | 0 | 0 | — | — |
| Pin 3 | 0 | 0 | 0 | 0 | — |
| Glass | 0 | 0 | 0 | 0 | 0 |
| LCD | 0 | 0 | 0 | 0 | 0 |
| PCB | 0 | 0 | 0 | 0 | 0 |
| Corner standoffs | 0 | 0 | 0 | 0 | 0 |
| Button bodies/plungers | 0 | 0 | 0 | 0 | 0 |
| DSI connector | 0 | 0 | 0 | 0 | 0 |
| Touch FPC | 0 | 0 | 0 | 0 | 0 |

Extra envelope checks: frame ∩ DSI-plus-3 mm = **0 mm³**; plate ∩ DSI-plus-3 mm = **0 mm³**; frame ∩ 18 mm ribbon corridor = **0 mm³**. These results are conditional on the documented unmeasured lateral connector envelope. No full actuation/flex simulation or physical button approval is claimed.

Independent `src/verify_geometry.py` completed successfully on delivered meshes:

- Glass and plate front Y=0; nominal lit centre Z=44.4 vs plate centre 44.4, error 0.000 mm (requirement ≤0.1).
- Window section at Y=1 and 2, Z=41.5: X=-27.55..93.55 (121.1), giving 0.2 to each glass side. Vertical section at X=33, Y=1: Z=2.7..80.3 (77.6), giving 0.2 above/below glass.
- At Y=0.15, the chamfer section is X=-27.7..93.7, confirming 0.15 extra opening halfway through the 0.3 mm / 45 degree bevel. The earlier hull version was corrected after this independent check detected its small depth error.
- Side-lip section at Y=2.9: X=-26.75..92.75, confirming the 0.8 inward reach from each window edge. At Y=2.4 and 3.4 the window returns to X=-27.55..93.55. The vertical opening at X=33 remains Z=2.7..80.3, confirming no top/bottom lip. The independent metal-frame bounds are X=-25.85..91.85, Y=2.5..5.5, giving minimum side-lip clearance **0.8999996 mm** (0.9 nominal). Cosmetic glass-back boundary contact has 0 volume; depth and retention come from the screwed rear frame.
- Five-object 3MF reopened: **4,624 plain `<vertex>` tags; 9,304 plain `<triangle>` tags; no `ns0`**. Counts match the table. Each object has print min Z=0 and 12 mm X spacing. Triangle indices are identical to the delivered STLs; transformed coordinate roundtrip error ≤0.0000005 mm (six-decimal XML rounding).

Machine-readable results: `checks/acceptance.json`, `checks/independent_geometry.json`, `checks/meshcheck.log`; individual intersection/render logs and SCAD probes are retained. Check/dummy/assembled reference STLs are diagnostic geometry, not additional manufacturing parts.

## Review and preservation

README records decisions, assumptions, print orientation, test-print ID and UNKNOWNs. Local viewers generated with `tools/mesh_viewer.py`:

- `outputs/Screen_5in_SCR5-G_2026-10-30/checks/SCR5-G-print-review.html` — five named delivered parts.
- `outputs/Screen_5in_SCR5-G_2026-10-30/checks/SCR5-G-assembly-review.html` — assembled union reference including screen dummy.
- `checks/SCR5-G_rear.png` — command-line assembly image, visually inspected during development.

Viewer pages stay inside the new folder to respect the task's output boundary. SendUserFile/private Artifact display is unavailable on this Codex host; no public publication or upload was substituted.

232 targeted protected files hashed before/after the build match, including old screen revisions/coupon, Hue/Pi M6 references, Final_3MF, IDEAS.md, HANDOFF.md and Dimensions.md. Original helpers were copied, never edited in place. No data/normal-use access or app launch, printing, physical test, purchases, upload, desktop-control session, subagents, commit or push. No git pull was performed because an incoming update could alter explicitly protected paths during the commit hold. HANDOFF.md was not changed.

The earlier unidentified-edge blocker was resolved by Brian's measured side-step clarification and updated spec. No further design decision is pending for this digital task. Fit, strength, retention, button operation and physical screen clearances remain UNKNOWN; no printing is authorized.
