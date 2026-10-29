"""Write current complete report and keep the first-run measurements as an appendix."""
import json
from pathlib import Path
from measure import ROOT,HERE
REV=HERE/'revision2'
OUT=ROOT/'outputs/CM1000_M6_generated_2026-10-28'

def main():
    a=json.loads((REV/'audit.json').read_text(encoding='utf-8'))
    p=json.loads((REV/'preservation.json').read_text(encoding='utf-8'))
    h=json.loads((REV/'hdt-regression.json').read_text(encoding='utf-8'))
    proof=json.loads((REV/'3mf-proof.json').read_text(encoding='utf-8'))
    worst=a['pocket']['worst_boundary'];axial=a['pocket']['worst']
    windows={s:max(r['error'] for r in a['windows'][s]) for s in ['l','r']}
    parts=a['parts'];nose=[r for r in a['pocket']['samples'] if r['y']<16 and r['error'] is not None]
    noseworst=max(nose,key=lambda r:r['error'])
    text=f'''# Task 44 Revision 2 — CM6B fidelity report

2026-10-28. **All seven items built and measured; overall fidelity FAIL (item 1). PROPOSED — UNVALIDATED.** Items 2–7 pass the stated Revision 2 digital checks. The closest completed candidate replaces the unprinted task-43 CM6B delivery as Brian explicitly directed. It must not be described as a fidelity-approved or physically approved bracket.

Revision 2 overrides the first run's 0.3 mm cosmetic limit and stop-on-miss instruction. Work continued through every item. No protected-file or legacy-source preservation failure occurred. The original first-run report, including all its measurements, is reproduced in Appendix A and retained separately in `work/m6-fidelity-44/revision2/first-run-report.md`.

## CM6A versus rebuilt CM6B — all seven items

Measurements are millimetres in CM6A coordinates unless specified. Conversion: X_A=X_B+127, Y_A=Y_B+4, Z_A=Z_B. A comparison is a digital measurement, not a printed-fit claim.

| Item | Measured CM6A | Rebuilt CM6B | Revision 2 tolerance / verdict |
|---|---|---|---|
| **1. Pocket and longitudinal nose/rear sculpting** | At Y_A=12 / X_A=30: Z=8.951786..35.498263. At Y_A=125 / X_A=22.6: channel 19.126800..25.323199, height **6.196399**; right height **6.195741**. CM6A also has a central nose bridge which ends in a rounded tip near Y_A=14.8. | Replaced active constant 16-point pocket construction with measured rail X/Z profiles, **49 longitudinal stub sections per side** (0.25 mm nose spacing), and the measured central bridge side extrusion. Nose sampled vertical-boundary error max **{noseworst['error']:.6f}** at Y={noseworst['y']:.6f}, X={noseworst['x']}. However, worst sampled side-pocket **2D nearest-boundary discrepancy is {worst['error']:.6f}**, at Y={worst['y_A']:.6f}, point {worst['point']}, {worst['direction']}. A separate vertical-ray gap comparison reaches **{axial['error']:.6f}** at Y={axial['y']}, X={axial['x']}: A {axial['reference']}, B {axial['candidate']}. | **FAIL**, boundary ±0.3. {len(a['pocket']['stations'])} stations, including a ≤5 mm regular sweep and 20 fixed-seed random interior stations. Every geometric shape-change station and global surface fidelity remain unproven. The ray error is an axial gap difference, not a Hausdorff distance. |
| **2. Left case-retention slot** | Bounds Y=60.7723..76.7997, Z=19.7358..26.2382; centre **(68.786,22.987)**; size **16.0274 × 6.5024**, long direction Y. No right slot. | Through-wall stadium cut at the same centre and extents. Measured X_A=18 section bounds **{a['retention_slot']['candidate']['bounds']}**, centre **{a['retention_slot']['candidate']['centre']}**, size **{a['retention_slot']['candidate']['size']}**. Position and size errors round to **0.0000**. | **PASS**, position ±0.3, size ±0.5; stadium allowed. Intended screw/fastener type, head and engagement **UNKNOWN**. Through-width fillet matching is not claimed. |
| **3. Rail length/rear end; joint positions** | Rail Y_A=16..137.620, length **121.620**. Joints X_A=22.6/231.4 and Z=8.6/35.85. | `m6_rail_len=121.62`; actual Y_A=16.05..137.620, length **121.570**. Deliberate 0.05 stub/rail separation retained. Rear error **0.000**, length error **−0.050**. Joint centres unchanged, coordinate error **0.000**; Ø6.6 clearance bores and Ø7.6 pilots retained. | **PASS**, rail length/rear ±0.1 and joints ±0.1. Nominal screw reach across the gap is not physical engagement evidence. |
| **4. Access bays and material beneath/above** | At X_A=18/236: Z=2.6..16.9556 and 27.4944..41.85 (**14.3556 high**). At screw-centre Z=8.6: Y=20..64.684186 / 64.684189 (**44.684186 / 44.684189 deep**). Original inner rounded margins can have only 1.223562 vertical thickness. | Both clear heights **14.36001**; measured depth **{a['bays']['l']['bay_y_A'][1][0]-20:.6f}** on each side. Curved outline envelope setting `m6_bay_d=46.91` yields that clear depth (it is the envelope setting, not a rectangular inscribed opening). Added 2.5 mm horizontal skins across each bay's full rail width/envelope. Sampled floor/top minimum **2.50000 / 2.50000**, both rails; 160 grid points include X_A=34.9/219.1 inner margins. At X_A=18/236, Y_A=30: **2.57499 / 2.57500**. | **PASS**, clear height ≥14.36 and depth ≥44.68; floor/top ≥2.5 digitally under the bay envelopes. These are curved openings, not proof of an inscribed 14.36×44.68 rectangle or physical L-key access. Generic normal-wall minima elsewhere remain **UNKNOWN**. |
| **5. Cosmetic windows/scallops/rounding** | Three lower and three upper main windows on each rail; sculpted through-width transitions. Volumes left **41,246.062830**, right **41,896.160257 mm³**. | Same six-window count/layout, plus the left-only retention opening. Primitive extruded side outlines and measured faceted profile rounding; added bay skins. Volumes left **{parts['rail_l']['volume']:.6f}** (**{parts['rail_l']['volume_error_percent']:+.6f}%**), right **{parts['rail_r']['volume']:.6f}** (**{parts['rail_r']['volume_error_percent']:+.6f}%**). Worst sampled per-window boundary distances: left **{windows['l']:.6f}**, right **{windows['r']:.6f}**; 7 through-width planes ×6 windows per rail. | **PASS**, every sampled window ≤2 mm, each rail volume within 5%. This is sampled section evidence, not a certified global surface maximum or an exact analytic edge radius. |
| **6. Five light pipes/holes, seven letters, two details** | Five approximately Ø8 light pipes, depth **8.718392**, centres X≈104/150/138.5/127/115.5, Z≈30.225. Seven letter vector bounds and two detail bounds measured separately. Logo depth 0.2; original details 0.4. | Five matching holes and **five separate Ø8 ×8.72 flat-ended pipes**, measured centre/bounds error max **{max(a['colours'][f'pipe_{i}']['bounds_error'] for i in range(1,6)):.6f}**. Seven traced vector letters + two detail vectors, all **0.2 mm** inlays. Largest letter bound error **{max(a['colours'][f'vector_{i}']['bounds_error'] for i in range(1,8)):.6f}**; details max **{max(a['colours'][f'vector_{i}']['bounds_error'] for i in range(8,10)):.6f}**. **17 separate 3MF objects**: 3 structures, 5 pipes, 7 letters, 2 details, with two colour/material definitions. | **PASS**, pipes/holes ±0.2, each letter bounds ±0.3, 0.2 inlays; flat rear and omitted front symbols allowed. Pipe volumes differ because of the permitted simple cylinder and absent front symbols. Empty body/colour intersection verified. |
| **7. Wizard plate and rack slots** | **254 ×44.4500008**, 4 mm front plate; four corner rack slots. | **252 ×44.400006**, 4 mm plate, Z≈0.0249939..44.425; four corner slots only, centres X_B=±118.2625, Z=6.323/38.127. Width −2.000, height −0.050; centred in the slot. | **PASS**, intentional FP44 wizard-standard difference. No middle rack holes. |

## What was built and why item 1 still fails

The generator reads only numeric polygons, stations and dimensions saved in `CM6B_spec.json`. It never imports CM6A/remix meshes. Measurement scripts read the references separately. Runtime primitives are polygon extrusions, section loft polyhedra, cylinders, a stadium slot and vector inlays. The centre nose bridge is also a measured side-outline extrusion; the front symbols are intentionally omitted under Revision 2. The seven letter outlines are simplified vector traces, not imported triangles.

The remaining pocket mismatch is real. A constant rear transverse rail profile intersected with a side outline cannot reproduce all three-dimensional through-width window/pocket transitions or the rear tip's rounding. Longitudinal stub lofts and the restored bridge improve the nose, but do not repair that rail failure. Reported boundary distances compare actual section edges; rail volume and closure do not override this FAIL. There are **{a['pocket']['missing_count']}** reference vertical gap samples without a matching two-sided candidate gap; these are explicitly retained in the audit, not treated as zero error.

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
'''
    for n,v in parts.items():text+=f"| {n} | {v['triangles']} | {v['volume']:.6f} | {'PASS' if v['closed'] and v['components']==1 else 'FAIL'} |\n"
    text+='\nColour bounds are in CM6A coordinates. Letters/details compare X/Z bounds; the deliberate detail-depth change is covered by the 0.2 mm inlay instruction.\n\n| Part | Reference bounds (min; max) | Candidate bounds (min; max) | Max bound error mm | Result |\n|---|---|---|---:|---|\n'
    for n,v in a['colours'].items():text+=f"| {n} | {v['reference_bounds']} | {v['candidate_bounds_A']} | {v['bounds_error']:.6f} | PASS |\n"
    text+='\n## Every sampled cosmetic window\n\nThe maximum for each window across all seven independent X planes is listed below. The raw audit retains both directions, points and planes; these are sampled lower bounds on global discrepancy.\n\n| Rail | Window Y range | Lower/upper Z range | Max error mm | ≤2 mm |\n|---|---|---|---:|---|\n'
    for side,rows in a['windows'].items():
        groups={}
        for r in rows:
            key=(tuple(r['y_range']),tuple(r['z_range']));groups[key]=max(groups.get(key,0),r['error'])
        for (yr,zr),value in groups.items():text+=f'| {side} | {yr} | {zr} | {value:.6f} | {"PASS" if value<=2 else "FAIL"} |\n'
    text+='\n## Legacy SHA-256 re-proof\n\nBefore, after and explicit-false values are separately stored in the JSON proof; all three agree. These 14 cases are a preservation corpus, not an exhaustive proof over every possible input.\n\n| Case | Before = after = explicit false SHA-256 | Result |\n|---|---|---|\n'
    for row in p['source_cases']:text+=f"| {row['label']} | `{row['before']}` | PASS |\n"
    text+='''
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

'''
    text+=(REV/'first-run-report.md').read_text(encoding='utf-8')
    (ROOT/'work/codex-tasks/44-cm6b-fidelity-REPORT.md').write_text(text,encoding='utf-8',newline='\n')
    readme=f'''# CM6B — task 44 Revision 2 candidate

**PROPOSED — UNVALIDATED. Pocket fidelity FAIL. Do not treat as a fit-approved bracket.**

All seven requested items were built and measured. Items 2–7 pass the Revision 2 sampled digital checks; item 1 misses the strict 0.3 mm pocket boundary tolerance. Worst sampled side-pocket boundary discrepancy: {worst['error']:.6f} mm. The complete table, every known gap/UNKNOWN and the first run's measurements are in `work/codex-tasks/44-cm6b-fidelity-REPORT.md`.

`CM6B_source.scad` is the self-contained primitive-only generator output; `CM6B_spec.json` contains every measured numeric setting, including the nose lofts and bridge. No remix mesh import. `CM6B_CM1000_generated_split_rails.3mf` has 17 separate named objects: faceplate, two rails, five light pipes, seven logo letters and two details. Pipes and vector inlays share the faceplate transform and use separate colour material hints. All 17 individual STLs are included. STL/3MF only, no printer/slicer setup.

Plate 252×44.4×4 mm with four corner slots. Joints X=±104.4, Z=8.6/35.85; selected Ø7.6 pilots/Ø6.6 clearance bores; rail length setting121.62, actual121.57 due to the0.05 gap, rearY_B133.62. Bays ≥14.36 high and44.68 clear depth, with2.5 floor/top skins. Five Ø8×8.72 pipes; nine0.2 mm vector inlays. The46.91 bay depth setting describes the curved outline envelope. Measured rail volume errors: {parts['rail_l']['volume_error_percent']:+.6f}% / {parts['rail_r']['volume_error_percent']:+.6f}%.

Explicit OpenSCAD.exe renders: 17 closed single solids; body/rail and body/colour intersections empty. 233 Python tests (2 skipped),244 JS passed. Fourteen legacy SHA-256 cases preserved;85 protected originals byte-identical; HDT-M6-A triangle-identical. Evidence in `validation/`. The restored baseline nose bridge is included, but full longitudinal/through-width pocket fidelity still fails. The legacy pocket polygon is joint-wall screening only; active geometry uses the new measured numeric settings.

Physical fit, retention, loads, strength, insert dimensions/compatibility, screw engagement/access, usable rack depth, manufacturing accuracy, walls/process suitability and printed colour/light performance remain UNKNOWN. Flat pipe rears and omitted symbols are permitted simplifications. No printing is authorized. Local/private reference-derived work; do not redistribute.

Rebuilt viewer: `work/mesh-viewer/CM6A_vs_CM6B.html`. Prior task-43 delivery retained at `work/m6-fidelity-44/revision2/task43-delivery/`. This unprinted candidate was replaced at Brian's explicit direction despite the reported pocket FAIL.
'''
    (OUT/'README.md').write_text(readme,encoding='utf-8',newline='\n')
    print('report and README written')

if __name__=='__main__':main()
