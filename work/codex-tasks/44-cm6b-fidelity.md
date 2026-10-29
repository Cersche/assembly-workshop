# Task 44 — CM6B fidelity: bring the generated CM1000 bracket up to CM6A

**REVISION 2 (Brian, 2026-10-28) — read first; overrides the tolerances and the stop rule below.** The first run stopped at the rail windows (0.94–1.55 mm off vs 0.3). Reuse everything in `work/m6-fidelity-44/` (sections.json, rail_trial.py, measured colour parts) and FINISH all 7 items.
- **Fit-critical, strict:** pocket boundary ±0.3 mm at the measured stations; joints ±0.1; rail length/rear end ±0.1; access bays: clear opening at least CM6A's 14.36 × 44.68 (larger is fine), floor/top ≥ 2.5; retention slot position ±0.3 and size ±0.5 (a rounded slot / stadium shape through the rail wall is fine).
- **Cosmetic, loose:** rail windows, scallops and edge rounding: same count and layout, each window within 2 mm, rail volume within 5 %. Extruded side outlines like the trial are acceptable.
- **Colour parts:** 5 light-pipe holes + pipes at the measured centres/sizes ±0.2 (Ø8, depth 8.72; a flat or simple sloped rear is fine; front symbols optional); 7 logo letters + 2 details as vector shapes, each letter's bounds ±0.3, 0.2 mm inlays; separate colour objects in the 3MF like CM6A. Pixel-perfect letter outlines are not required.
- **No stopping on one miss:** if an item can't meet its tolerance, build the closest version, keep going with the rest, and mark that item FAIL with numbers in the report. Only stop for a safety/preservation problem (legacy hash change, HDT-M6-A change, protected file touched).
- Deliver: rebuild CM6B in `outputs/CM1000_M6_generated_2026-10-28/` with all settings, tests and the 3MF; viewer `work/mesh-viewer/CM6A_vs_CM6B.html` rebuilt. Report in `44-cm6b-fidelity-REPORT.md` (replace the stopped version, keep its measurements as an appendix).

Status: SPEC (Claude, 2026-10-28). Follows task 43 (report `43-m6-split-rails-REPORT.md`). Brian: fix every CM6B gap in Codex. Continue in the SAME checkout where task 43 was done (its uncommitted task 43 changes are the starting point; do not revert them).

PROPOSED — UNVALIDATED: fit, strength and retention stay UNKNOWN. Same rules as task 43: disposable data only, never data/normal-use; no printing, commits, pushes or automatic builds; OpenSCAD.exe; Python 3.10 stdlib, UTF-8. Do not touch CM6A, the 2026-10-16 baseline, HDT-M6-A, TL-SG108E files or HANDOFF.md. Every source without `m6_rails` stays byte-identical (re-prove the 14 SHA-256 cases), HDT-M6-A stays triangle-identical.

**Principle:** the printed baseline (`outputs/STL_Deliveries/2026-10-16_CM1000_bracket/`, rails_v2) FITS; CM6A keeps its shapes. CM6B must match CM6A's shapes, not the envelope model. Where the envelope model disagrees with the baseline, the baseline wins. Measure from CM6A / baseline STLs (sections), store the result as numbers/polygons in the CM1000 spec (`CM6B_spec.json`), and generate primitives from them. Do not import the remix meshes into the generator.

## Fixes (each new geometry setting is generic and optional; the CM1000 spec sets the CM6A values)
1. **Pocket = baseline pocket.** Replace the 16-point guess. Measure the baseline pocket as transverse sections at enough Y stations (at least every 5 mm plus every shape change) and generate it as a loft/hull chain of those sections, so the longitudinal (nose/rear) sculpting is kept. Acceptance: at every station and at 20 random interior stations, CM6B pocket boundary within 0.2 mm of CM6A. Drop the 6.2 vs 18.3 mm question: the baseline value is the answer; record the measured end-channel height.
2. **Case-retention screw slot** on the left side: reproduce position, size and orientation from CM6A (within 0.2 mm). Report what fastener it was for (from geometry; UNKNOWN if unclear).
3. **Rail length** = CM6A's (Y_A 16..137.62 → 121.62 mm rail). New setting `m6_rail_len` (default stays device depth + 2 for other devices); CM1000 spec sets the CM6A value. Rear end must match CM6A within 0.1 mm.
4. **Access bays** = CM6A's real openings (about 14.36 tall × 44.68 deep; measure exactly). Settings `m6_bay_h`, `m6_bay_d`; floor/top under the bays never below 2.5 (CM6A has 2.6 nominal).
5. **Rail scallops, web openings, rounded edges**: reproduce CM6A's rail window pattern and edge rounding (generic setting: list of side-window outlines + edge radius). Acceptance: rail volume within 3 % of CM6A's, each window within 0.3 mm.
6. **Light pipes and Netgear logo** (Brian wants both kept): 5 light-pipe holes and the 5 light-pipe parts at CM6A's positions/shapes (within 0.2 mm), plus the logo and the 2 detail parts, generated as separate colour objects in the 3MF exactly like CM6A's set. Light pipes as primitives from measured sizes; logo redrawn as vector shapes (like the HDT-M6-A icon) matching CM6A's logo outline within 0.3 mm. If a part's shape can't be matched by primitives, stop and list it in the report instead of importing the mesh.
7. **Keep** the wizard standard plate 252 × 44.4 (Brian's FP44 standard) and the four corner slots only; record the difference from CM6A's 254 × 44.45.

Rebuild CM6B into `outputs/CM1000_M6_generated_2026-10-28/` (replace task 43's files there; they are not printed), update its README, rebuild `work/mesh-viewer/CM6A_vs_CM6B.html` (not committed).

## Acceptance (append a "Task 44" section to the task 43 report or write `44-cm6b-fidelity-REPORT.md`)
1. `run_checks.ps1` passes plus new tests for each new setting and its validation.
2. Exact renders: all parts closed single solids; faceplate ∩ rails empty; light pipes/logo don't intersect the plate body beyond their intended inlay.
3. A CM6A vs CM6B table for every item 1–7 with measured numbers and pass/fail against the tolerances above. Anything not matched is listed plainly, not hidden.
4. Legacy hashes and HDT-M6-A identical.
5. Every UNKNOWN restated.
