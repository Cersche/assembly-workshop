"""Assemble the explicit failed-fidelity report from new disposable evidence."""
import json
from pathlib import Path
from measure import HERE, ROOT

preservation = json.loads((HERE/'preservation.json').read_text(encoding='utf-8'))
current = json.loads((HERE/'current-audit.json').read_text(encoding='utf-8'))
trial = json.loads((HERE/'rail-trial.json').read_text(encoding='utf-8'))
sections = json.loads((HERE/'sections.json').read_text(encoding='utf-8'))
hdt = json.loads((HERE/'hdt-regression.json').read_text(encoding='utf-8'))
errors = json.loads((HERE/'trial-window-errors.json').read_text(encoding='utf-8'))
checks = (HERE/'checks.log').read_text(encoding='utf-8-sig')
assert 'RESULT: all checks passed' in checks
assert preservation['all_14_identical'] and preservation['protected_identical']
assert all(hdt[p]['triangle_for_triangle'] for p in ['faceplate','tray'])
assert current['source_identical_to_task43_delivery'] and current['intersection_empty']

report = '''# Task 44 — CM6B fidelity report

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
'''
for n in range(2,16):
    d = sections[f'colour_{n}']
    lo,hi = d['bounds']
    role = f'Detail {n-1}' if n<4 else f'Light pipe {n-3}' if n<9 else f'Logo {n-8}'
    report += f"| {role} (`fp_{n}`) | {lo[0]:.6f}..{hi[0]:.6f} | {lo[1]:.6f}..{hi[1]:.6f} | {lo[2]:.6f}..{hi[2]:.6f} | {d['volume']:.6f} |\n"
report += '''
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
'''
for r in preservation['source_cases']:
    report += f"| {r['label']} | `{r['after']}` | PASS, identical |\n"
report += '''
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
'''
target = ROOT/'work/codex-tasks/44-cm6b-fidelity-REPORT.md'
target.write_text(report,encoding='utf-8',newline='\n')
print(target)
