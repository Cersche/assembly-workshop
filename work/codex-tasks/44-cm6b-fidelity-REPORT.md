# Task 44 Revision 2 — CM6B fidelity report

2026-10-28. **All seven items built and measured; overall fidelity FAIL (item 1). PROPOSED — UNVALIDATED.** Items 2–7 pass the stated Revision 2 digital checks. The closest completed candidate replaces the unprinted task-43 CM6B delivery as Brian explicitly directed. It must not be described as a fidelity-approved or physically approved bracket.

Revision 2 overrides the first run's 0.3 mm cosmetic limit and stop-on-miss instruction. Work continued through every item. No protected-file or legacy-source preservation failure occurred. The original first-run report, including all its measurements, is reproduced in Appendix A and retained separately in `work/m6-fidelity-44/revision2/first-run-report.md`.

## CM6A versus rebuilt CM6B — all seven items

Measurements are millimetres in CM6A coordinates unless specified. Conversion: X_A=X_B+127, Y_A=Y_B+4, Z_A=Z_B. A comparison is a digital measurement, not a printed-fit claim.

| Item | Measured CM6A | Rebuilt CM6B | Revision 2 tolerance / verdict |
|---|---|---|---|
| **1. Pocket and longitudinal nose/rear sculpting** | At Y_A=12 / X_A=30: Z=8.951786..35.498263. At Y_A=125 / X_A=22.6: channel 19.126800..25.323199, height **6.196399**; right height **6.195741**. CM6A also has a central nose bridge which ends in a rounded tip near Y_A=14.8. | Replaced active constant 16-point pocket construction with measured rail X/Z profiles, **49 longitudinal stub sections per side** (0.25 mm nose spacing), and the measured central bridge side extrusion. Nose sampled vertical-boundary error max **0.017890** at Y=15.900000, X=35. However, worst sampled side-pocket **2D nearest-boundary discrepancy is 2.015540**, at Y=75.000000, point [20.7017, 22.10108], A to B. A separate vertical-ray gap comparison reaches **14.599531** at Y=30, X=230: A [2.6, 41.85], B [17.196914, 27.250469]. | **FAIL**, boundary ±0.3. 72 stations, including a ≤5 mm regular sweep and 20 fixed-seed random interior stations. Every geometric shape-change station and global surface fidelity remain unproven. The ray error is an axial gap difference, not a Hausdorff distance. |
| **2. Left case-retention slot** | Bounds Y=60.7723..76.7997, Z=19.7358..26.2382; centre **(68.786,22.987)**; size **16.0274 × 6.5024**, long direction Y. No right slot. | Through-wall stadium cut at the same centre and extents. Measured X_A=18 section bounds **[[60.7723, 19.7358], [76.7997, 26.2382]]**, centre **[68.786, 22.987000000000002]**, size **[16.0274, 6.502399999999998]**. Position and size errors round to **0.0000**. | **PASS**, position ±0.3, size ±0.5; stadium allowed. Intended screw/fastener type, head and engagement **UNKNOWN**. Through-width fillet matching is not claimed. |
| **3. Rail length/rear end; joint positions** | Rail Y_A=16..137.620, length **121.620**. Joints X_A=22.6/231.4 and Z=8.6/35.85. | `m6_rail_len=121.62`; actual Y_A=16.05..137.620, length **121.570**. Deliberate 0.05 stub/rail separation retained. Rear error **0.000**, length error **−0.050**. Joint centres unchanged, coordinate error **0.000**; Ø6.6 clearance bores and Ø7.6 pilots retained. | **PASS**, rail length/rear ±0.1 and joints ±0.1. Nominal screw reach across the gap is not physical engagement evidence. |
| **4. Access bays and material beneath/above** | At X_A=18/236: Z=2.6..16.9556 and 27.4944..41.85 (**14.3556 high**). At screw-centre Z=8.6: Y=20..64.684186 / 64.684189 (**44.684186 / 44.684189 deep**). Original inner rounded margins can have only 1.223562 vertical thickness. | Both clear heights **14.36001**; measured depth **44.697811** on each side. Curved outline envelope setting `m6_bay_d=46.91` yields that clear depth (it is the envelope setting, not a rectangular inscribed opening). Added 2.5 mm horizontal skins across each bay's full rail width/envelope. Sampled floor/top minimum **2.50000 / 2.50000**, both rails; 160 grid points include X_A=34.9/219.1 inner margins. At X_A=18/236, Y_A=30: **2.57499 / 2.57500**. | **PASS**, clear height ≥14.36 and depth ≥44.68; floor/top ≥2.5 digitally under the bay envelopes. These are curved openings, not proof of an inscribed 14.36×44.68 rectangle or physical L-key access. Generic normal-wall minima elsewhere remain **UNKNOWN**. |
| **5. Cosmetic windows/scallops/rounding** | Three lower and three upper main windows on each rail; sculpted through-width transitions. Volumes left **41,246.062830**, right **41,896.160257 mm³**. | Same six-window count/layout, plus the left-only retention opening. Primitive extruded side outlines and measured faceted profile rounding; added bay skins. Volumes left **41120.765943** (**-0.303779%**), right **41497.418414** (**-0.951738%**). Worst sampled per-window boundary distances: left **0.934612**, right **0.935036**; 7 through-width planes ×6 windows per rail. | **PASS**, every sampled window ≤2 mm, each rail volume within 5%. This is sampled section evidence, not a certified global surface maximum or an exact analytic edge radius. |
| **6. Five light pipes/holes, seven letters, two details** | Five approximately Ø8 light pipes, depth **8.718392**, centres X≈104/150/138.5/127/115.5, Z≈30.225. Seven letter vector bounds and two detail bounds measured separately. Logo depth 0.2; original details 0.4. | Five matching holes and **five separate Ø8 ×8.72 flat-ended pipes**, measured centre/bounds error max **0.001608**. Seven traced vector letters + two detail vectors, all **0.2 mm** inlays. Largest letter bound error **0.005763**; details max **0.003310**. **17 separate 3MF objects**: 3 structures, 5 pipes, 7 letters, 2 details, with two colour/material definitions. | **PASS**, pipes/holes ±0.2, each letter bounds ±0.3, 0.2 inlays; flat rear and omitted front symbols allowed. Pipe volumes differ because of the permitted simple cylinder and absent front symbols. Empty body/colour intersection verified. |
| **7. Wizard plate and rack slots** | **254 ×44.4500008**, 4 mm front plate; four corner rack slots. | **252 ×44.400006**, 4 mm plate, Z≈0.0249939..44.425; four corner slots only, centres X_B=±118.2625, Z=6.323/38.127. Width −2.000, height −0.050; centred in the slot. | **PASS**, intentional FP44 wizard-standard difference. No middle rack holes. |

## What was built and why item 1 still fails

The generator reads only numeric polygons, stations and dimensions saved in `CM6B_spec.json`. It never imports CM6A/remix meshes. Measurement scripts read the references separately. Runtime primitives are polygon extrusions, section loft polyhedra, cylinders, a stadium slot and vector inlays. The centre nose bridge is also a measured side-outline extrusion; the front symbols are intentionally omitted under Revision 2. The seven letter outlines are simplified vector traces, not imported triangles.

The remaining pocket mismatch is real. A constant rear transverse rail profile intersected with a side outline cannot reproduce all three-dimensional through-width window/pocket transitions or the rear tip's rounding. Longitudinal stub lofts and the restored bridge improve the nose, but do not repair that rail failure. Reported boundary distances compare actual section edges; rail volume and closure do not override this FAIL. There are **12** reference vertical gap samples without a matching two-sided candidate gap; these are explicitly retained in the audit, not treated as zero error.

The legacy `m6_pocket_profile` remains in the spec for the existing joint-wall screening and dormant legacy rail module. It no longer drives the active measured-section geometry. That screening alone cannot establish minimum wall/clearance against every new measured section. The source keeps the legacy module for optional profiles-off behaviour. All active measured geometry is saved in the new numeric settings.

New optional settings: `m6_rail_len`, `m6_bay_h`, `m6_bay_d`, `m6_rail_profiles`, `m6_side_windows`, `m6_stub_sections`, `m6_nose_bridge`, `m6_edge_radius`, `m6_retention_slot`, `m6_light_pipes`, `m6_vectors`. Section groups, dimensions, finite coordinates, outline area/structure, increasing loft stations, point-count correspondence, slot dimensions, pipe dimensions and inlay depths are validated. The default rail length remains device depth +2 for other devices. The CM1000 spec uses measured polygon rounding with additional edge offset radius 0; the optional offset radius remains available. Settings survive the Python/JS allocation key paths. No normal-use allocation was opened or saved.

## Exact integrity, checks and preservation

- **PASS:** `run_checks.ps1`, **233 Python tests, 2 skipped** (231 executed successfully), **244 JavaScript tests passed**. Five added fidelity test methods cover every new setting's round trip/validation, profiles-off defaults, non-finite inputs, and shared colour placement/3MF objects. Skips remain skips. Final log: `revision2/checks-verified.log`.
- **PASS:** 17 explicit OpenSCAD.exe ASCII STL renders; every part closed and one connected solid. No mesh-repair promotion. Per-part triangles/volumes/bounds are below and in `revision2/audit.json`.
- **PASS:** faceplate ∩ (left ∪ right rail) is empty; faceplate body ∩ all 14 colour parts is empty. OpenSCAD empty-output exit 1 is expected and logged. The inlay/pipe cuts create the intended voids; zero-volume contact is not manufactured clearance.
- **PASS:** 17-object /17-build-item 3MF. Colours share the faceplate's rigid placement; the rails have their separate placement. Every packaged triangle matches its source STL under that layout at the packer's 6-decimal coordinate precision. Material definitions are colour hints; no printer/slicer profile is included. `revision2/3mf-proof.json`.
- **PASS:** all **14** historical source SHA-256 cases, including explicit `m6_rails=false`, match the pre-task-43 hashes. Complete table below and `revision2/preservation.json`.
- **PASS:** all **85** protected files match task-44 starting hashes: CM6A, 2026-10-16 CM1000 baseline, HDT-M6-A, specified TL-SG108E files and HANDOFF.md. The preservation helper normalizes Windows separators before excluding the authorized generator files; an earlier precheck's path-exclusion mismatch was not a protected-file change.
- **PASS:** HDT-M6-A fresh scratch renders remain triangle-identical to the reference with only ID engraving statements removed from a scratch source: **3,388 faceplate /10,836 tray triangles**. Both comparisons true. Originals byte-identical. Existing historical sliver limitations are not reclassified. `revision2/hdt-regression.json`.

## Detailed per-part and colour checks

| Part | Triangles | Volume mm³ | Closed / one solid |
|---|---:|---:|---|
| faceplate | 31220 | 91089.145168 | PASS |
| rail_l | 3000 | 41120.765943 | PASS |
| rail_r | 3356 | 41497.418414 | PASS |
| pipe_1 | 188 | 437.063400 | PASS |
| pipe_2 | 188 | 437.063400 | PASS |
| pipe_3 | 188 | 437.062661 | PASS |
| pipe_4 | 188 | 437.063800 | PASS |
| pipe_5 | 188 | 437.064881 | PASS |
| vector_1 | 28 | 1.790425 | PASS |
| vector_2 | 40 | 3.263104 | PASS |
| vector_3 | 44 | 2.394028 | PASS |
| vector_4 | 64 | 2.539277 | PASS |
| vector_5 | 44 | 2.394038 | PASS |
| vector_6 | 344 | 3.052201 | PASS |
| vector_7 | 180 | 2.779344 | PASS |
| vector_8 | 60 | 0.152338 | PASS |
| vector_9 | 68 | 0.158884 | PASS |

Colour bounds are in CM6A coordinates. Letters/details compare X/Z bounds; the deliberate detail-depth change is covered by the 0.2 mm inlay instruction.

| Part | Reference bounds (min; max) | Candidate bounds (min; max) | Max bound error mm | Result |
|---|---|---|---:|---|
| pipe_1 | [[100.000001, 2e-06, 26.225374], [107.999644, 8.718392, 34.224835]] | [[99.9998, 0.0, 26.2251], [107.9998, 8.719999999999999, 34.2251]] | 0.001608 | PASS |
| pipe_2 | [[146.000001, 2e-06, 26.225374], [153.999644, 8.718392, 34.224835]] | [[145.9998, 0.0, 26.2251], [153.9998, 8.719999999999999, 34.2251]] | 0.001608 | PASS |
| pipe_3 | [[134.499999, 2e-06, 26.225374], [142.499644, 8.718392, 34.224835]] | [[134.49982, 0.0, 26.2251], [142.4998, 8.719999999999999, 34.2251]] | 0.001608 | PASS |
| pipe_4 | [[123.0, 2e-06, 26.225374], [130.999644, 8.718392, 34.224835]] | [[122.99982, 0.0, 26.2251], [130.99982, 8.719999999999999, 34.2251]] | 0.001608 | PASS |
| pipe_5 | [[111.5, 2e-06, 26.225015], [119.49994, 8.718392, 34.22489]] | [[111.5, 0.0, 26.225], [119.49997, 8.719999999999999, 34.225]] | 0.001608 | PASS |
| vector_1 | [[36.236027, 2e-06, 19.834272], [40.077526, 0.200002, 24.598667]] | [[36.236000000000004, 0.0, 19.8343], [40.0775, 0.20000000000000018, 24.5987]] | 0.000033 | PASS |
| vector_2 | [[25.898262, 2e-06, 19.841503], [30.66433, 0.200002, 24.606249]] | [[25.897999999999996, 0.0, 19.8415], [30.664299999999997, 0.20000000000000018, 24.6062]] | 0.000262 | PASS |
| vector_3 | [[46.906944, 2e-06, 19.833002], [50.07737, 0.200002, 24.590838]] | [[46.907, 0.0, 19.833], [50.0774, 0.20000000000000018, 24.5908]] | 0.000056 | PASS |
| vector_4 | [[50.852726, 2e-06, 19.823656], [55.841839, 0.200002, 24.586911]] | [[50.8527, 0.0, 19.8245], [55.841800000000006, 0.20000000000000018, 24.5869]] | 0.000844 | PASS |
| vector_5 | [[32.186493, 2e-06, 19.843802], [35.356918, 0.200002, 24.601638]] | [[32.186499999999995, 0.0, 19.8438], [35.356899999999996, 0.20000000000000018, 24.6016]] | 0.000038 | PASS |
| vector_6 | [[40.622337, 2e-06, 19.701108], [45.774208, 0.200002, 24.740692]] | [[40.6281, 0.0, 19.7011], [45.77419999999999, 0.20000000000000018, 24.7407]] | 0.005763 | PASS |
| vector_7 | [[56.63802, 2e-06, 19.818684], [60.795803, 0.200002, 24.585169]] | [[56.638000000000005, 0.0, 19.8193], [60.7958, 0.20000000000000018, 24.5852]] | 0.000616 | PASS |
| vector_8 | [[117.016631, 2e-06, 31.306643], [118.298514, 0.400002, 32.39141]] | [[117.01662999999999, 0.0, 31.3066], [118.29701, 0.20000000000000018, 32.3881]] | 0.003310 | PASS |
| vector_9 | [[112.411708, 2e-06, 28.775583], [113.593047, 0.400002, 29.975847]] | [[112.4121, 0.0, 28.7767], [113.59309999999999, 0.20000000000000018, 29.9754]] | 0.001117 | PASS |

## Every sampled cosmetic window

The maximum for each window across all seven independent X planes is listed below. The raw audit retains both directions, points and planes; these are sampled lower bounds on global discrepancy.

| Rail | Window Y range | Lower/upper Z range | Max error mm | ≤2 mm |
|---|---|---|---:|---|
| l | (20, 67) | (2.5, 17) | 0.921405 | PASS |
| l | (20, 67) | (27.4, 41.9) | 0.917018 | PASS |
| l | (71.9, 92.4) | (2.5, 17) | 0.934063 | PASS |
| l | (71.9, 92.4) | (27.4, 41.9) | 0.930889 | PASS |
| l | (97.3, 117.8) | (2.5, 17) | 0.934612 | PASS |
| l | (97.3, 117.8) | (27.4, 41.9) | 0.930975 | PASS |
| r | (20, 67) | (2.5, 17) | 0.916614 | PASS |
| r | (20, 67) | (27.4, 41.9) | 0.920933 | PASS |
| r | (71.9, 92.4) | (2.5, 17) | 0.929502 | PASS |
| r | (71.9, 92.4) | (27.4, 41.9) | 0.935036 | PASS |
| r | (97.3, 117.8) | (2.5, 17) | 0.929209 | PASS |
| r | (97.3, 117.8) | (27.4, 41.9) | 0.935010 | PASS |

## Legacy SHA-256 re-proof

Before, after and explicit-false values are separately stored in the JSON proof; all three agree. These 14 cases are a preservation corpus, not an exhaustive proof over every possible input.

| Case | Before = after = explicit false SHA-256 | Result |
|---|---|---|
| example-0-Raspberry Pi 4 (example) | `fe6bff2a485ce7814614000a90da9c6679509ed8b4b69dd5d6dac30023f6baec` | PASS |
| library-copy-0-Raspberry Pi 4 (example) | `fe6bff2a485ce7814614000a90da9c6679509ed8b4b69dd5d6dac30023f6baec` | PASS |
| library-copy-1-Dell OptiPlex Micro 7010 (sleeve) | `fcb9dff6521aaa19ec3753e7781fd80968556b0f70d6663181bfcef44be751e3` | PASS |
| library-copy-2-Drive tray (3.5" HDD + 2.5" SSD) | `3297879222e50ed29b4a51dcc9ea8518a326ef2e217f4fc07f27b30240562a4e` | PASS |
| library-copy-3-7" touch screen plate (placeholder) | `2046c1b868b97fee6086d32a6624dffc2ccdf1685b9c15af4d2708fa05a25745` | PASS |
| library-copy-4-Keystone panel, 10 (3 USB, 4 LAN, 3 blank) | `2a641ad48c0a91ea8649abebe33a2d6b3ce556039f36bb23b2d3af4d4b173635` | PASS |
| library-copy-5-TP-Link TL-SG108E | `8252da3ca3388b62cc2033c067866604e6f9efb072810d4c19ac83ae31beb26b` | PASS |
| library-copy-6-Modem ECB7250 (placeholder) | `733df8f95e2d357cfd9848858db6b9c3e20abf346619d0150108599493efdb77` | PASS |
| library-copy-7-Netgear CM1000 (bracket: faceplate + rails v2) | `37de9848c08753bdc88d624a3c0615aa66412defb78c942c9b0f053d4fbef9f8` | PASS |
| library-copy-8-Philips Hue Bridge + Raspberry Pi 4 (keystone) | `a9d706913e20e313aed44020250df824b77606ae60d526ad1b1e7491b9d9485d` | PASS |
| HDT-M6-A | `5c95b78d4e34bc1214a90c1211bd29aafa9ab146d777f32b6ffa094b67e3e117` | PASS |
| flat | `0af470dbcf9c5329c5d357f95f637ac9d600c31ff8f2198cf55c833f31aac456` | PASS |
| sleeve | `bb538705be18bedcda86387540f93509ae2192adaf492992abc5b28f369a5113` | PASS |
| two-device-pair | `fda9389e0f7d4113f432a783aac5f9a54cd9159aff34d23ea8e27aa2a6c8564c` | PASS |

## Every remaining gap and UNKNOWN

1. **Known FAIL:** full pocket/rail longitudinal and through-width fidelity, including the quantified mismatches and missing-gap samples above. Every-shape-change coverage, unmeasured surfaces, a global Hausdorff maximum and an exact common analytic edge radius remain UNKNOWN. The nominal 6.2-vs-18.3 question is superseded by the measured reference channel; channel height depends on the X station.
2. **Permitted differences:** simple cylindrical flat-ended light pipes, omitted front symbols, 0.2 rather than 0.4 mm detail inlays, simplified vector traces, extruded side outlines and polygon rounding, added bay skins, the 0.05 rail separation, and wizard 252×44.4 plate. Each is disclosed above; none grants physical approval.
3. **Physical fit remains UNKNOWN:** modem pocket, nose/rear and orientation, sliding clearance, grip, retention and compatibility of every newly generated part. Brian's earlier fit report applies to the printed baseline specimen only.
4. **Slot hardware UNKNOWN:** intended fastener type/size, head shape, seating, engagement and engagement depth; the stadium is geometry, not a hardware identification.
5. **M6 insert hardware UNKNOWN:** measured insert bore/OD/length compatibility, certified maximum OD, usable engagement, installation process, splitting, pull-out, retention. Ø7.6 remains the selected rack-post bore, not a certified insert OD.
6. **Screw/joint performance UNKNOWN:** actual screw/head dimensions beyond nominal, Ø10.5 seating, clamp-up, torque, insertion reach, real thread engagement, loosening, service life, assembly sequence, service/installation access. Nominal 8−4−0.05=3.95 reach is not physical proof. Real 4 mm L-key insertion and turning space remain UNKNOWN despite the digital bay extents.
7. **Walls/loads UNKNOWN:** normal-to-surface global minima outside the explicit bay skins; generic FDM wall/process suitability; stiffness, sag, heavy-device load capacity, rail/joint strength, thermal and long-term performance, retention/security under use. Sampled bay vertical thickness is not a blanket wall/strength certification.
8. **Rack integration UNKNOWN:** actual usable rack depth, posts/slots/rails, neighbours, rear cables/bend space, rear clearance, ports and image/colour accommodation. The 240 mm default remains a planning limit. No printer/material detail is required for software continuation.
9. **Manufacturing UNKNOWN:** printed accuracy, process/material effects, printability, inlay fit and colour appearance, light transmission, front-symbol function, ID readability, wear and manufactured fit/strength. Zero digital intersection/contact and mesh closure do not certify manufactured clearance. Generic process guidance and blanket installation approval remain UNKNOWN.
10. **App/UI validation limit:** no fresh desktop session, server, active allocation edit or browser-export acceptance was performed. The settings, render part enumeration and 3MF packaging are integrated and unit-checked, but this report does not claim a new UI walkthrough. The available tools have no SendUserFile capability; the rebuilt local viewer is linked/opened with Codex's file tool instead.
11. **Rights:** reference meshes and resulting comparisons remain local/private; no redistribution or rights clearance is claimed. No imported remix meshes are used by the generator.

## Delivery and reproducibility

`outputs/CM1000_M6_generated_2026-10-28/` now holds source, the complete measured spec, all 17 part STLs, the 17-object colour 3MF, README and validation evidence. The previously unprinted task-43 delivery is retained under `revision2/task43-delivery/`. This is explicitly a **FAILED-pocket candidate** issued under Brian's Revision 2 instruction to build the closest result and continue.

Read the scripts before rerunning. `revision2_prepare.py` measures numeric profiles into new disposable data; `revision2_build.py` explicitly invokes `C:/Program Files/OpenSCAD/openscad.exe`; `revision2_audit.py` measures and checks intersections; `revision2_hdt.py` runs the fresh HDT proof; `revision2_preserve.py` compares legacy/protected hashes; `revision2_deliver.py` verifies and replaces only the authorized unprinted CM6B candidate; `revision2_report.py` writes this report. No daemon, watcher or automatic build was added.

`work/mesh-viewer/CM6A_vs_CM6B.html` is rebuilt with all structural and colour reference/candidate parts, in a common orientation, side by side, explicitly labelled pocket FAIL. The viewer uses `tools/mesh_viewer.py`; it is uncommitted, preview-only and embeds local/private mesh data. Comparison coordinates in the page are translated display coordinates; the side-by-side displacement and original-coordinate conversion are retained in `revision2/viewer-placement.json`.

The same checkout and all existing task-43/44 changes were retained. No git pull/revert/reset/commit/push, printing, purchase, upload, publishing, deployment, normal-use data access, automatic build, protected-original write, HANDOFF edit, fresh desktop-control session or subagent was performed.

## Appendix A — first-run report and measurements (historical, superseded)

Everything below is the preserved first-run report. Its STOPPED status, tolerances, unchanged-delivery statements and stop instruction describe that historical run only. The Revision 2 results above are current. Its measurements are intentionally retained verbatim, not regenerated.

---

# Task 44 — CM6B fidelity report

2026-10-28. **STOPPED — INCOMPLETE; fidelity acceptance FAIL. PROPOSED — UNVALIDATED.**

The section-based primitive rail trial did not match CM6A's window surfaces within 0.3 mm. Following Brian's instruction to stop and list anything that could not be matched, geometry work stopped at that failed trial. **No generator changes were made and no replacement CM6B delivery was issued.** This is not a completed implementation of task 44, and task 43's delivery must not be described as having passed task 44.

## What failed, and what the experiment proves

`rail_trial.py` measured a transverse X/Z rail section at Y_A=125.123, plus a side Y/Z section at X_A=18 (left) / 236 (right). It simplified those contours to numeric polygons and generated intersecting OpenSCAD `linear_extrude` primitives, with independent Ø6.6 screw-hole cylinders. **There is no mesh import in either trial SCAD.** Measurements are outside the generator; no remix triangle data was added to the generator.

The resulting rails are closed single solids and their volume errors are only −0.4483% (left) and −1.0692% (right), inside 3%. However, a single extruded side outline does not reproduce the window boundaries as they vary through the rail width. Independent transverse-position checks give these failure witnesses in CM6A coordinates (mm):

| Rail | Section X_A | Direction | Sample point (Y_A, Z_A) | Distance to the other section boundary | Limit | Result |
|---|---:|---|---|---:|---:|---|
| Left | 20 | trial → CM6A | (60.7928, 22.6299) | 1.549802 | 0.3 | FAIL |
| Left | 20 | CM6A → trial | (62.74214, 21.86867) | 1.547166 | 0.3 | FAIL |
| Left | 17 | CM6A → trial | (96.58769, 39.61519) | 1.083196 | 0.3 | FAIL |
| Right | 237 | CM6A → trial | (93.10659, 4.83497) | 1.082912 | 0.3 | FAIL |
| Right | 228 | trial → CM6A | (78.45897, 14.44765) | 0.935139 | 0.3 | FAIL |

These are sampled lower bounds on the worst discrepancy, not a certified global Hausdorff maximum. The checks compare actual section boundaries; they do not infer fidelity from volume or closure. At the fitted planes X_A=18 / 236 the match is close, which is insufficient: it misses the rounded/sculpted transitions elsewhere. Engraved top-face IDs were excluded from this window comparison. `trial-window-errors.json` records every sampled plane, direction, witness and nearest target segment.

I could not match those three-dimensional window/edge transitions with this primitive trial. This is a failed construction, **not proof that a different primitive reconstruction is mathematically impossible**. It was not promoted into optional generator settings. The rejected trials are measurement experiments, not test coupons or print files.

## CM6A versus CM6B: all seven requested items

“Current CM6B” below means the **unchanged task-43 delivery**, re-rendered in a new folder with OpenSCAD.exe. The rejected trial is identified separately. Coordinate conversion: X_A=X_B+127, Y_A=Y_B+4, Z_A=Z_B. Millimetres throughout.

| Item | Measured CM6A reference | Current CM6B / experiment | Tolerance and result |
|---|---|---|---|
| **1. Pocket and longitudinal sculpting** | Example Y_A=12, X_A=30: pocket boundaries Z=8.951786 / 35.498263. At Y_A=125, X_A=22.6, the channel is Z=19.126800..25.323199, **6.196399 high**; right X_A=231.4 gives **6.195741**. Farther toward the narrow tip, X_A=20.702, Y_A=125.123 gives Z=21.739187..22.710813, **0.971626 high**. “End channel” therefore needs its X position specified. | Still the task-43 16-point constant profile, with a nominal 6.2 channel. The Y12/X30 measured reference boundary is about 1.5586 from that profile, already over tolerance; the actual current stub does not even extend to X_A=30 at that station. No measured longitudinal pocket loft was installed. | **FAIL**, 0.2. Read-only audit includes 51 Y stations, with 20 deterministic random stations (seed 44). It is **not** the required complete every-shape-change acceptance sweep. No 18.3-mm envelope-model decision is requested: measured baseline sections are authoritative. |
| **2. Left case-retention screw slot** | A left-only side-section opening at X_A=18 has Y_A=60.7723..76.7997 and Z=19.7358..26.2382: section envelope **16.0274 × 6.5024**, long direction along Y. Rounded/through-width shape varies: this is not a rectangular-slot specification. No corresponding right-side opening. | Omitted in current CM6B. The trial captures the outline at X18, but misses its shape through width (the left X20 failure above is in this region). No accepted generic slot primitive or orientation/size proof. | **FAIL**, 0.2. Intended fastener type, screw size, head shape and engagement **UNKNOWN** from this opening's geometry. No fastener was invented. |
| **3. Rail length / rear end** | Y_A=16..137.62, length **121.620**. | Length **138.000**, Y_B=12.05..150.05 → Y_A=16.05..154.05; rear error **+16.430**. Trial spans exactly Y_A=16..137.62 but is rejected for other shape failures. `m6_rail_len` was **not implemented**. | **FAIL** for current delivery, rear tolerance 0.1. Trial rear position passes only; it is not an accepted rail. |
| **4. Real access bays / remaining material** | At X_A=18 / 236, Y_A=30, clear Z=2.6..16.9556 and 27.4944..41.85: **14.3556 high** each. At Z=8.6 clear Y_A=20..64.684186 (left) / 64.684189 (right): **44.684186 / 44.684189 deep**. The curved outlines extend to about Y_A=66.89715 elsewhere (46.89715 envelope depth). Planar floor/top nominal 2.6; the rounded outer-wall section is about 2.572. | Clear height **12.000**; depth **34.000**, starting Y_A=20.05. Sampled floor/top **2.575**, passing the local ≥2.5 check. Trial side outline follows the real curved bays at the sampled planes but fails their three-dimensional transitions. `m6_bay_h` / `m6_bay_d` were **not implemented**. | **FAIL**: required bay shape/dimensions not reproduced. No separate numerical shape tolerance was specified for item 4. The local floor/top check passes; **a global ≥2.5 guarantee is not established**. |
| **5. Scallops, windows, edge rounding** | Rail volumes: left **41,246.062830 mm³**, right **41,896.160257 mm³**. At X18/236 there are three lower and three upper main windows; the left also has the retention opening. For example, second-window Y bounds are 71.99745..92.29705; third about 97.39745..117.69693. Reference rounded/sculpted window boundaries vary with X. | Current volumes: left **34,233.432502** (−17.002%), right **34,232.429597** (−18.292%). Rejected trial volumes: **41,061.161606** / **41,448.213049** (−0.4483% / −1.0692%). Trial window witnesses reach **1.549802** error. No accepted side-window/edge-radius settings. | Current volume **FAIL**, ±3%; trial volume **PASS** but window boundary **FAIL**, 0.3. A single nominal edge radius was not established from the sampled sculpted surfaces. |
| **6. Five light pipes, logo and two details** | **14 colour parts**: pipes fp_4..8; seven separate logo letters fp_9..15; details fp_2..3. Pipe front extents are about Ø8, Z=26.225..34.225; depth Y_A≈0.000002..8.718392, with sloping rear ends and distinct front symbols. Centre X positions by extents are approximately **104, 150, 138.5, 127, 115.5**. Logo Y_A≈0.000002..0.200002; details to 0.400002. Full bounds/volumes/contours below and in sections.json. | Current CM6B has **0 light-pipe holes, 0 pipes, 0 logo letters and 0 details**; its 3MF still has only the three structural mesh objects. No colour reconstruction was implemented before the stop. No colour/plate inlay intersection render was performed. | **FAIL**, pipes/holes 0.2, logo outline 0.3, separate objects required. Primitive matching of all five pipe bodies/front symbols, seven letter outlines and both detail outlines is **UNPROVEN**, not silently omitted from scope. |
| **7. Wizard plate and corner slots** | Width **254.000**, Z=0..44.4500008; four corner rack slots. | Width **252.000**, Z≈0.0249939..44.425000, height≈**44.400006** (STL precision). Width −2.000, height −0.050, centred in the slot. Four corner slots retained. Current source unchanged from task 43; no middle rack holes. | **PASS** for the required wizard-standard dimensions and four-corner-only policy. This is an intentional difference, not a CM6A fidelity failure. |

The current-volume percentages are rounded; raw volumes are in `current-audit.json` and `sections.json`.

The 2.5 floor/top requirement is not resolved by quoting a nominal 2.6. For example, the reference at X_A=34.9, Y_A=25 has a lower material interval Z=0.911345..2.134907 (vertical thickness 1.223562) in its rounded/tapering inner edge. This is a **local vertical section**, not a normal-to-surface wall measurement or a global minimum. The meaning/extent of a global minimum across these shaped margins has not been established. No global wall claim or physical approval is made.

## Colour geometry measurements (reference only)

Bounds below are CM6A coordinates. These are measured reference shapes, not reconstructed parts or certified hardware dimensions.

| Part | X bounds | Y bounds | Z bounds | Volume mm³ |
|---|---|---|---|---:|
| Detail 1 (`fp_2`) | 117.016631..118.298514 | 0.000002..0.400002 | 31.306643..32.391410 | 0.306285 |
| Detail 2 (`fp_3`) | 112.411708..113.593047 | 0.000002..0.400002 | 28.775583..29.975847 | 0.319276 |
| Light pipe 1 (`fp_4`) | 100.000001..107.999644 | 0.000002..8.718392 | 26.225374..34.224835 | 279.586080 |
| Light pipe 2 (`fp_5`) | 146.000001..153.999644 | 0.000002..8.718392 | 26.225374..34.224835 | 276.320167 |
| Light pipe 3 (`fp_6`) | 134.499999..142.499644 | 0.000002..8.718392 | 26.225374..34.224835 | 275.949684 |
| Light pipe 4 (`fp_7`) | 123.000000..130.999644 | 0.000002..8.718392 | 26.225374..34.224835 | 275.949694 |
| Light pipe 5 (`fp_8`) | 111.500000..119.499940 | 0.000002..8.718392 | 26.225015..34.224890 | 279.409366 |
| Logo 1 (`fp_9`) | 36.236027..40.077526 | 0.000002..0.200002 | 19.834272..24.598667 | 1.790429 |
| Logo 2 (`fp_10`) | 25.898262..30.664330 | 0.000002..0.200002 | 19.841503..24.606249 | 3.259138 |
| Logo 3 (`fp_11`) | 46.906944..50.077370 | 0.000002..0.200002 | 19.833002..24.590838 | 2.394058 |
| Logo 4 (`fp_12`) | 50.852726..55.841839 | 0.000002..0.200002 | 19.823656..24.586911 | 2.542787 |
| Logo 5 (`fp_13`) | 32.186493..35.356918 | 0.000002..0.200002 | 19.843802..24.601638 | 2.394059 |
| Logo 6 (`fp_14`) | 40.622337..45.774208 | 0.000002..0.200002 | 19.701108..24.740692 | 3.054944 |
| Logo 7 (`fp_15`) | 56.638020..60.795803 | 0.000002..0.200002 | 19.818684..24.585169 | 2.782313 |

## Checks and preservation actually performed

- **PASS — `run_checks.ps1`:** 228 Python tests reported, 2 skipped; 244 JavaScript tests reported, all passing. `checks.log`. Skips are not passes. There are no task-44 setting tests because no new settings were implemented; that acceptance requirement remains **NOT DONE**.
- **PASS — fresh unchanged CM6B renders:** OpenSCAD.exe, three closed single solids, zero geometry repair. Faceplate 3,620 triangles; left rail 2,272; right rail 2,488. Faceplate ∩ rails renders empty (expected empty-output exit 1). `current-render/` and `current-audit.json`. Its generated source is byte-identical to task 43's delivered source. These are regression facts, **not fidelity acceptance**.
- **PASS — rejected trial integrity only:** both primitive rails closed, one component each; 992 / 1,136 triangles. Window fidelity fails as documented above.
- **PASS — HDT-M6-A:** four fresh OpenSCAD.exe renders in `hdt-regression/`. Generator vs a new scratch copy of the reference with only its engraved ID statements removed is triangle-for-triangle identical: 3,388 faceplate / 10,836 tray triangles, the same comparison used by task 43. Original HDT-M6-A files, including their existing IDs and original STLs, stay byte-identical. This does not repair or reclassify the historically documented sliver issue.
- **PASS — protected originals:** all 85 non-generator protected files in task 43's manifest match the task-44 starting snapshot, including CM6A, the 2026-10-16 CM1000 baseline, HDT-M6-A, the specified TL-SG108E files and HANDOFF.md. All seven files in the existing CM6B delivery also remain byte-identical. `starting-hashes.json` / `preservation.json`.
- **PASS — legacy sources:** all 14 saved task-43 input cases were recalculated using `source(clean(spec))` and equal their pre-task-43 SHA-256 values. Inputs came from task 43's already-disposable fixture JSON; **no access to data/normal-use**. Explicit false/no-rails cases remain covered. Full proof below; this corpus is not an exhaustive enumeration of every possible input.
- **NOT DONE — colour/inlay integrity:** no reconstructed colour objects exist, so no purported colour overlap or colour-solid acceptance is claimed.

## Legacy SHA-256 re-proof

Each before and after digest below is exactly equal; both columns are stored separately in `preservation.json`.

| Case | Before = after SHA-256 | Result |
|---|---|---|
| example-0-Raspberry Pi 4 (example) | `fe6bff2a485ce7814614000a90da9c6679509ed8b4b69dd5d6dac30023f6baec` | PASS, identical |
| library-copy-0-Raspberry Pi 4 (example) | `fe6bff2a485ce7814614000a90da9c6679509ed8b4b69dd5d6dac30023f6baec` | PASS, identical |
| library-copy-1-Dell OptiPlex Micro 7010 (sleeve) | `fcb9dff6521aaa19ec3753e7781fd80968556b0f70d6663181bfcef44be751e3` | PASS, identical |
| library-copy-2-Drive tray (3.5" HDD + 2.5" SSD) | `3297879222e50ed29b4a51dcc9ea8518a326ef2e217f4fc07f27b30240562a4e` | PASS, identical |
| library-copy-3-7" touch screen plate (placeholder) | `2046c1b868b97fee6086d32a6624dffc2ccdf1685b9c15af4d2708fa05a25745` | PASS, identical |
| library-copy-4-Keystone panel, 10 (3 USB, 4 LAN, 3 blank) | `2a641ad48c0a91ea8649abebe33a2d6b3ce556039f36bb23b2d3af4d4b173635` | PASS, identical |
| library-copy-5-TP-Link TL-SG108E | `8252da3ca3388b62cc2033c067866604e6f9efb072810d4c19ac83ae31beb26b` | PASS, identical |
| library-copy-6-Modem ECB7250 (placeholder) | `733df8f95e2d357cfd9848858db6b9c3e20abf346619d0150108599493efdb77` | PASS, identical |
| library-copy-7-Netgear CM1000 (bracket: faceplate + rails v2) | `37de9848c08753bdc88d624a3c0615aa66412defb78c942c9b0f053d4fbef9f8` | PASS, identical |
| library-copy-8-Philips Hue Bridge + Raspberry Pi 4 (keystone) | `a9d706913e20e313aed44020250df824b77606ae60d526ad1b1e7491b9d9485d` | PASS, identical |
| HDT-M6-A | `5c95b78d4e34bc1214a90c1211bd29aafa9ab146d777f32b6ffa094b67e3e117` | PASS, identical |
| flat | `0af470dbcf9c5329c5d357f95f637ac9d600c31ff8f2198cf55c833f31aac456` | PASS, identical |
| sleeve | `bb538705be18bedcda86387540f93509ae2192adaf492992abc5b28f369a5113` | PASS, identical |
| two-device-pair | `fda9389e0f7d4113f432a783aac5f9a54cd9159aff34d23ea8e27aa2a6c8564c` | PASS, identical |

## Outstanding work and every gap

1. Replace the 16-point pocket guess with measured longitudinal sections and a validated non-convex loft; implement its optional generic settings/validation. Complete ≥5-mm/every-shape-change stations plus 20 random interior-station **boundary acceptance**, not just the partial ray audit here. Store accepted measured numbers in CM6B_spec.json. None of this is done.
2. Match the left case-retention opening through the rail width, including position, dimensions, orientation and rounded transition surfaces. The trial's single side section fails this; fastener purpose remains UNKNOWN.
3. Implement/validate `m6_rail_len`, keep the default device depth +2 for other devices, set CM1000 to 121.62 and verify the actual rear coordinate. Not done.
4. Implement/validate bay settings with the real curved openings, resolve/verify the floor/top measurement extent, and preserve ≥2.5 where required. A 14.3556 ×44.6842 rectangle alone does not reproduce the measured opening. Not done.
5. Reconstruct the through-width scallops/web openings and rounded transitions; implement optional generic outlines/edge rounding; test volume **and every window boundary**. Trial passes only volume. No accepted geometry.
6. Reconstruct five pipe holes and five sloped/symbol-bearing pipes, all seven logo letters and two details as separate colour parts; validate shape/placement, individual closed solids, intended inlays and 3MF structure. None implemented; no imported-mesh fallback used.
7. Keep the wizard plate standard/four slots while making those changes. Already retained in current task-43 source; further changed-part checks remain necessary.
8. No new setting/validation tests; no final task-44 all-part render; no accepted colour intersections; no accepted task-44 3MF or export parity proof. No app/UI session or library save was attempted.
9. **Delivery not rebuilt, CM6B_spec.json not changed, delivery README not changed.** Replacing task 43's files with a candidate that failed fidelity would contradict the failed-check/export boundary. They remain the task-43 version; use this report to distinguish their status. No report or HANDOFF wording was silently updated to claim completion.

## Every UNKNOWN retained

- Pocket fit to the actual modem, nose/rear geometry and orientation, sliding clearance, grip and retention; exact global boundary fidelity and full-shape station coverage. The earlier 6.2-versus-18.3 envelope question is superseded by measured baseline sections; **physical fit of new CM6B remains UNKNOWN**. Brian's fit report applies to the printed 2026-10-16 specimen, not these candidates.
- Full primitive match of the rail sculpting/rounded windows/retention slot and colour parts; nominal edge-radius interpretation; global floor/top and normal-wall minima. Sampled dimensions do not establish unsampled surfaces.
- Retention-slot fastener type, size, head shape and engagement. No geometry-only hardware certification.
- Insert measured bore/OD/length compatibility, installation process, retention, pull-out and splitting. Ø7.6 is the selected rack-post bore, not a measured/certified insert OD or usable engagement.
- Actual screw/head dimensions beyond nominal, seating, clamp-up across task 43's 0.05 gap, torque, insertion reach, actual thread engagement, loosening, service life and installation/service access. Task 43's nominal 8−4−0.05=3.95 reach is not physical proof.
- Real 4-mm L-key access/turning space, Ø10.5 head seating, screw/insert retention and joint assembly sequence suitability.
- Rail stiffness/sag, heavy-device loads, strength, joint strength, thermal and long-term behaviour; retention/security under use.
- Actual usable rack depth, posts/slots/rails, neighbours, rear-end clearance, rear cables, bend space, ports and artwork/colour accommodation. The 240 default is a planning limit, not a measured usable depth.
- Printed dimensional accuracy, material/process effects, wall suitability, printability, inlay fit/colour results, ID readability, manufactured fit and strength. Manufacturer-certified dimensions, generic FDM wall/process guidance and blanket installation approval remain UNKNOWN. No printer/slicer integration is required.
- Current colour/plate intersection behaviour and reconstructed multi-colour 3MF equivalence: **UNVERIFIED because not implemented**.

## Files, viewers and boundaries

Evidence is new disposable data under `work/m6-fidelity-44/`. `measure.py` stores raw axis-section loops and original bounds/volumes in `sections.json`; `rail_trial.py` writes numeric primitive-only trial sources; `compare_trial.py` records sampled failure witnesses; `audit_current.py` renders unchanged current source in a fresh folder; `preserve.py` and `verify_hdt.py` prove preservation. No old evidence was regenerated in place.

Rebuilt `work/mesh-viewer/CM6A_vs_CM6B.html` from the six unchanged structural meshes, labelled **FAILED fidelity**. Additional viewers: `task44-rejected-trial-and-colours.html` (rejected rails plus CM6A colour reference set), and `task44-hdt-preservation.html` (fresh HDT regression renders). All use `tools/mesh_viewer.py`; these generated pages are private, uncommitted previews and change no geometry. The available tools do not include SendUserFile, so the pages are provided as local file links instead of claiming a SendUserFile render.

Worked in the same C: checkout and retained all task-43 uncommitted changes. No pull, revert, reset, commit, push, printing, purchases, upload, publishing, deployment, automatic build, normal-use data access, desktop-control session, server start, or subagent delegation. OpenSCAD.exe was used only for the explicit disposable trial/regression renders documented here. CM6A, baseline, HDT-M6-A, TL-SG108E and HANDOFF.md were read only and remain unchanged.
