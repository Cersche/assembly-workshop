# Task 48 — SCR5-A review build; hardware-configured delivery blocked

2026-10-29, Codex. **INCOMPLETE CONCEPT REVIEW ONLY. Not printed. Vendor dimensions nominal. Printed fit, glass retention, access, ribbon reach and strength UNKNOWN.** Claude/Brian geometry review remains outstanding. The STL/3MF files below are review evidence, not manufacturing approval.

Brian's follow-up during this run: screen has not arrived; gap remains UNKNOWN but adjustable; assume plain PCB holes, unconfirmed; default socket-cap head envelope 4.5×2.5, actual screws unconfirmed. Continue build, commit and push. These defaults are explicit parameters; no fixed screw-length decision was requested again.

## Result and specific blocker

Created `outputs/Screen_5in_SCR5-A_2026-10-29/` with parameterized SCAD, explicit Python 3.10/OpenSCAD.exe builder, JSON provenance/parameters, README, two individually checked STL parts, the named two-object 3MF and checks/probes. Digital mesh/packaging checks pass for these concept meshes. `--final` rejects the configuration before exporting; `checks/final-gate.log` records the actual rejection. This is the spec's retained-source/review-preview fallback for incomplete hardware geometry, not a silent manufacturing-ready set.

**Fastening architecture limitation:** the removable rear-loaded carrier has its insert ring *between the glass and PCB*. Its four integral clips mechanically capture to faceplate-pocket windows. This gives a defined plate→carrier→screw→PCB retention path, rather than a frame screwed only to a freely removable PCB. However, the assumed 6 mm glass-back-to-PCB-front gap and access to preassemble that ring are not established by the vendor's 12.6 mm total depth. There may be no suitable free gap or insertion path on the actual display. The concept therefore does not establish the requested conventional rear clamp behind an assembled screen. Changing `glass_pcb_gap` moves the carrier ring, with inequalities blocking gaps too small for the inserts/ring; an insufficient actual gap will require a different architecture, not a fabricated measurement.

The Ø5.1×2.8 screw-head clearance relief opens into free space behind the PCB in this concept; no printed rear counterbore/head seat exists to certify. The source reserves the head/tool envelope, and the README explicitly records this remaining difference from the requested clamp. No unsupported PCB bearing/contact pressure, usable thread or fit claim.

## Geometry and datums

Plate X ±126, Y −4..0, intended Z 0.05..88.85, 2.5 corners. Brian's **88.8** height is 0.05 shorter than task 25's older 2U **88.85** formula, centred on the same Z=44.45. App geometry/rack pitch unchanged. Eight horizontal 10×7 rack slots at X ±118.2625 and Z 6.323/38.127/50.773/82.577. No tray, M6 joints, app integration or Final_3MF copy.

Screen nominal glass 120.7×77.2, active 109×65.8, PCB 121×76, total depth 12.6, corner pattern 113×68; upright centre X=0/Z=44.45. No Pi pattern substituted. Independent lip parameters default 3 mm, aperture 114.7×71.2, 0.75 corner radius. Centred-assumption active keepout corners clear the aperture, but registration UNKNOWN precludes active-area clearance approval. Full boss radius 3.25 at all four axes overlaps that assumed keepout in projection: radial signed gap −1.30449. Bosses are behind nominal glass; that does not establish optical or internal assembly clearance, and the lip was not enlarged to hide them.

Rear pocket ends at Y=20; outer X ±68.75 lies inside inherited ±104 screening boundary. Glass/PCB clearance parameters are separate; PCB, glass and nominal retracting clips fit the widened cavity. Clip retraction is 2.25 with 2 mm nominal PCB-edge clearance; clip flex/material and actual peripheral components remain UNKNOWN. Hooks at Y=18.5 catch pocket shoulders at Y=19, with 0.5 free play. Contact-only assembly intersection is confined to X ±65.75, with zero volume. Pocket above/below nominal glass and narrow plate margins were screened; physical retention/strength are untested.

Seated glass front Y=0, assumed thickness 2; adjustable assumed gap 6 gives PCB front Y=8, assumed thickness 1.6 gives rear Y=9.6. Carrier ring Y=3..8, clips to 18.5, overall assembly rear 20. The remaining nominal rear space is not certified ribbon bend room. Touch/FPC keepout boxes are provisional, parameterized and shown only by the assembled SCAD selector, never in manufacturing meshes.

## Conditional hardware and assembly

BOM: one plate, one carrier; four Brian-confirmed nominal **M2.5 / 4 mm length / 3.5 mm OD inserts**; four conditionally chosen **M2.5×5 screws**; eight existing rack-faceplate fasteners. No purchases. Vendor “M2.5×4” stand callout is not used as evidence of screw length or threaded PCB holes.

Printed pilot Ø3.4 is a separate process assumption, not a certified OD subtraction. Seat depth 4.2, lead-in 0.3, remaining pilot floor 0.8. Inserts install from ring rear Y=8 toward −Y, nominal metal span Y=4..8. Screw entry is from PCB rear Y=9.6, head bearing on suitable *assumed* corner PCB lands; shaft passes assumed plain holes toward the carrier inserts. The configured 1.6 stack and 5 under-head length give nominal 3.4 engagement and 0.6 front tip reserve. Screening limits (2.5 minimum engagement, 0.4 reserve, both provisional) yield **4.1..5.2** valid length range. Printed fit, usable engagement, PCB lands/hole construction, screw-head/tool envelope and safe compression remain UNKNOWN.

Head default Ø4.5×2.5 reaches Y=12.1; counterbore-shaped access Ø5.1×2.8 and tool Ø5.5 remain parameterized. No actual screw or driver tested. SCR5-A engraving is frame-rear only, 0.5 deep, leaving 4.5 wall; exact mesh comparison to the no-ID probe verifies removal/floor geometry.

Conditional assembly: install inserts away from electronics; access the interspace and place the ring against PCB corner lands; screw from rear into carrier. Preassembly access is an unresolved blocker. If that subassembly is feasible, retract the four side hooks, load glass/PCB/carrier from the rear until glass meets the lip, then release hooks into the pocket windows. Support the screen and retract hooks for rear removal. Nominal retracting-clip envelope clears the PCB outline; actual clip strain, connector/component clearance, preload and release remain UNKNOWN. No physical assembly was performed.

Ribbon opening top-left and top-button access are separate parameters, behind the insert ring; neither source cut removes bosses or severs the carrier. Rounded opening silhouettes are present, while actual contact-edge finishing, finger access and cable bend/contact geometry remain unvalidated. The screen is not mirrored or rotated.

## HP4 source and ribbon route

Read HP4-M6-B README/source only; no reference build or reference geometry parsed/displayed. `dsi_slot_cut()` remains X −86..−62, Y 87..95. Both designs use plate rear Y=0. HP4 floor `tray_z=7+1.225=8.225`, thickness 3; translated into screen-local coordinates it is Z=97.125..100.125. U5 begins at screen-local 88.90; rack-global Z is screen-local +88.90.

Assumed waypoints (screen-local mm):

| Location | X | Y | Z |
| --- | ---: | ---: | ---: |
| Screen connector, approximate | −52 | 13.1 | 66.45 |
| Top-left exit, assumed | −52 | 18 | 87.5 |
| Lateral transition, assumed | −74 | 25 | 90 |
| Slot underside | −74 | 91 | 97.125 |
| Slot top | −74 | 91 | 100.125 |
| Pi connector, assumed | −74 | 81 | 110.4 |

Polyline **128.56 mm**, plus illustrative insertion 16, slack 15 and bend reserve 10 = **169.56 mm**. These reserves and connector locations are assumptions, not measured allowances. The 160 mm cable cannot be approved from this arithmetic; reach/bend room/obstruction clearance UNKNOWN. `checks/ribbon-route.json` and `checks/SCR5-A-route.svg` retain explicit datums and assumptions.

## Actual validation and retained evidence

- Python 3.10.4, OpenSCAD.exe 2021.01, binary STL. Focused new-part checks only; no app code changed, so app suite not rerun. No repair, welding, rounding or nudging of mesh vertices/parts.
- Exact parsed-coordinate topology: one closed shell per delivery part, zero bad edges/winding errors/degenerate faces, positive signed volume. Supplementary numerical self-intersection screen: no reported nonincident crossing/area overlap; incident edges excluded, predicate tolerance 1e−9 mm. Not exact-arithmetic certification.
- Parsed plate bounds, aperture size/centre and eight slot boundaries/through-rays pass. Separate pilot-axis measurements, engraving volume/floor check, component-box broad-phase exclusion and nominal clip retraction checks pass conditionally on their parameters.
- Exact CAD assembly intersection: only intended two side contact planes; zero volume. No positive-volume collision in the configured parts. Physical screen/interspace insertion and clip deformation not simulated/certified.
- Nine invalid configurations rejected before pack: long/short screw, too-deep insert seat, zero pilot, negative gap, NaN clearance, excess aperture radius, through engraving, clip retraction into PCB. Real `--final` rejection also exercised.
- Independent fresh ZIP/XML 3MF reopen: exactly two names/resources/build items; mm; no components; finite coordinates, valid indices/counts, positive volume/closure; exact indexed triangle correspondence after rigid rotation/translation; positive 12 mm separation; both exact min Z=0; correct relationships/content types; literal `<vertex>`/`<triangle>`, no `ns0:`. Viewer parser also reopens it. Slicer load NOT TESTED.
- Initial font profile had three zero-area triangles, retained as `checks/SCR5-A_frame-degenerate-review.stl`. Source lettering was redesigned with rounded/angled outlines and rerendered, not mesh-repaired. One intermediate bridge had an 80 mm³ collision, retained as rejected frame/intersection probes. Corrected source bridge now has zero-volume boundary contact. Comparison/no-ID and final contact probes are also retained and included in viewers; probes are not manufacturing objects.
- Preservation checkpoint: 150 baseline files, 149 compared unchanged with HANDOFF intentionally excluded for update; includes official data, both HP4 revisions, Final_3MF and the prior local-preservation folder. Targeted checkpoint, not a full/live backup. Pre-existing stash and untracked viewers/screenshots untouched. No broad repository scan, app/data saves, restart, desktop control, printing, purchases or public publication.

## Review / publication

Local hub: `work/mesh-viewer/SCR5-A-index.html`, with front/rear presets, common-datum assembly, separate STLs, two-object 3MF and all retained probes. Raw mandated viewer page: `work/mesh-viewer/SCR5-A-review.html`. Every retained/produced current STL/3MF has been read by `tools/mesh_viewer.py`; source-level HP4 inspection avoided reference-mesh redistribution. Generated viewer HTML is not committed. Parser checks ran; no interactive GUI visual review or slicer load claimed.

**Private Artifact publishing pending in Claude.** Tool discovery found no SendUserFile/private Artifact publication capability on this Codex host; no URL fabricated, public host substituted or local link called publication. Claude must publish privately and review geometry with Brian.

All uncertain dimensions/physical behaviours above remain UNKNOWN. Optional library/rack integration is deferred; U2 cooling and U5/data untouched. This run is authorized to commit only task-owned outputs/report/HANDOFF and push private main, without force. Synchronization evidence follows after final checks.

## Final mesh statistics and SHA-256

See the generated table below and `checks/hashes.json` for the exact sources, configuration, meshes and retained probes used in this run.

| Part | Vertices | Triangles | Edges | Volume mm³ |
| --- | ---: | ---: | ---: | ---: |
| SCR5-A plate | 1072 | 2192 | 3288 | 79056.11994031 |
| SCR5-A rear frame | 3042 | 6084 | 9126 | 13635.71311716 |

| File | SHA-256 |
| --- | --- |
| `src/SCR5-A_build.py` | `7bb0ad6854ad0d469b468e3d1ede87859cce7bfb249973674db1918a850e3b8a` |
| `src/SCR5-A_geometry_checks.py` | `2bfc5f4404fe89bbfe23aa0a28e8a2f48741d6190299541cb5b8f3e652a42c07` |
| `src/SCR5-A_review.py` | `66652226189756d610bee646c960403b5b8fe331e1953e30cea42fda6f193ea7` |
| `src/SCR5-A.scad` | `2e38e775ec88467aa1d7a9b3d5ed3b9617ddffd14b80db79cbcf04641fcd6165` |
| `src/SCR5-A_config.scad` | `08f50613bdce14309ae1c3075790457dc977fddca42a7e8b6ac7a55ad88b304a` |
| `SCR5-A_frame.stl` | `4b28cce890982fa81fc87c26a33f994936fde843000b9b50d5a8de16507102d7` |
| `SCR5-A_plate.stl` | `741c764b04538d3ce9d78e75e075c7fa02298216d4e620571e00521ce9169f2d` |
| `checks/SCR5-A_assembly-intersection.stl` | `5611f066bf7e8bfd79313f4787636cbe592e5f7887e5da7bc3f809e7d6fadd26` |
| `checks/SCR5-A_bridge-collision-probe.stl` | `47054ca61a0095ed2e58d6095c9d66c0f474e25a44eb8278d9fe2521b11cc620` |
| `checks/SCR5-A_frame-bridge-collision-probe.stl` | `a0ad3bb20b635d424461177c371db7ab82d578d398d264bbdeeffd030a3761cf` |
| `checks/SCR5-A_frame-degenerate-review.stl` | `7ec5991123db95e3f15d9716bb71801236105e972ba92f4bf3db3c5806bf9188` |
| `checks/SCR5-A_frame-unengraved-probe.stl` | `24c26969fe9d06886f5e12ce128ac955aee47f8b7bff5f19b9d4ff6c06097567` |
| `SCR5-A_parameters.json` | `2baed6416f0de06b78463c97efb9fd633333727cab3c6ce7d5478f7e812e0138` |
| `SCR5-A_screen_plate_and_frame.3mf` | `56120c0b0a5ee7be1c06319bbf8e49f6a758689fe3f20310f23dc25c358ac205` |

## Session synchronization

Initial `git pull`: already up to date on existing `main`. Final explicit `--review` and independent `--check-only` runs passed their digital checks, with hardware final export still blocked. A separate `--final` rejection test verified all three review delivery file hashes unchanged. Only this task’s new output folder, report and HANDOFF are included in the session commit; local viewer HTML, the prior preservation backup, earlier stash and unrelated files remain excluded. Authorized destination is existing private `origin/main` (`Cersche/assembly-workshop`); synchronization result is reported in the final chat after verifying the push. No force push.

The new output folder carries task-local `.gitattributes` (`* -text`) to preserve the exact bytes behind the source/config/parameter/mesh SHA-256 values across Git line-ending settings. Historical/user assets and root attributes are unchanged.
