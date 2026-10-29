# CM6B — task 44 Revision 2 candidate

**PROPOSED — UNVALIDATED. Pocket fidelity FAIL. Do not treat as a fit-approved bracket.**

All seven requested items were built and measured. Items 2–7 pass the Revision 2 sampled digital checks; item 1 misses the strict 0.3 mm pocket boundary tolerance. Worst sampled side-pocket boundary discrepancy: 2.015540 mm. The complete table, every known gap/UNKNOWN and the first run's measurements are in `work/codex-tasks/44-cm6b-fidelity-REPORT.md`.

`CM6B_source.scad` is the self-contained primitive-only generator output; `CM6B_spec.json` contains every measured numeric setting, including the nose lofts and bridge. No remix mesh import. `CM6B_CM1000_generated_split_rails.3mf` has 17 separate named objects: faceplate, two rails, five light pipes, seven logo letters and two details. Pipes and vector inlays share the faceplate transform and use separate colour material hints. All 17 individual STLs are included. STL/3MF only, no printer/slicer setup.

Plate 252×44.4×4 mm with four corner slots. Joints X=±104.4, Z=8.6/35.85; selected Ø7.6 pilots/Ø6.6 clearance bores; rail length setting121.62, actual121.57 due to the0.05 gap, rearY_B133.62. Bays ≥14.36 high and44.68 clear depth, with2.5 floor/top skins. Five Ø8×8.72 pipes; nine0.2 mm vector inlays. The46.91 bay depth setting describes the curved outline envelope. Measured rail volume errors: -0.303779% / -0.951738%.

Explicit OpenSCAD.exe renders: 17 closed single solids; body/rail and body/colour intersections empty. 233 Python tests (2 skipped),244 JS passed. Fourteen legacy SHA-256 cases preserved;85 protected originals byte-identical; HDT-M6-A triangle-identical. Evidence in `validation/`. The restored baseline nose bridge is included, but full longitudinal/through-width pocket fidelity still fails. The legacy pocket polygon is joint-wall screening only; active geometry uses the new measured numeric settings.

Physical fit, retention, loads, strength, insert dimensions/compatibility, screw engagement/access, usable rack depth, manufacturing accuracy, walls/process suitability and printed colour/light performance remain UNKNOWN. Flat pipe rears and omitted symbols are permitted simplifications. No printing is authorized. Local/private reference-derived work; do not redistribute.

Rebuilt viewer: `work/mesh-viewer/CM6A_vs_CM6B.html`. Prior task-43 delivery retained at `work/m6-fidelity-44/revision2/task43-delivery/`. This unprinted candidate was replaced at Brian's explicit direction despite the reported pocket FAIL.
