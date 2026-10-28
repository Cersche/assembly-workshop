# Task 43 — Generator: M6 "split rails" bracket (rebuild CM1000 CM6A from the engine)

Status: SPEC (Claude, 2026-10-28). Brian's direction: every bracket uses the generator engine (`m6_joint`). CM6A (`outputs/CM1000_M6_2026-10-28/`) was built by hand on a licensed remix mesh; Brian chose "option A": add a split-rails bracket to the generator and rebuild the CM1000 as a generated bracket (CM6B), compared side by side with CM6A.

PROPOSED — UNVALIDATED: fit, strength and insert retention stay UNKNOWN. Use only NEW disposable data, never data/normal-use. No printing, no pushes, no commits, no auto-builds. OpenSCAD.exe is the renderer. Python 3.10 stdlib, UTF-8.

**Do not run while another session edits the generator** (the TL-SG108E session may touch `equipment_tray.scad` / `equipment.py`). Brian starts this only when that session is finished; `git pull` first.

## Reference (read, don't change)
- CM6A: `outputs/CM1000_M6_2026-10-28/README.md`, `src/cm1000_m6.scad`, `src/faceplate_freecad.py`, the three STLs. Its numbers are the target.
- Existing M6 option: `@m6` block in `outputs/Mechanical_Design_App/equipment_tray.scad`, `M6_HOOKS` / `m6_joints` / validation in `equipment.py` (~430–460, ~886–895, ~1049), `test_m6_joint.py`.
- Modem envelope: `work/equipment-models/netgear_cm1000/netgear_cm1000.scad` (derived from the baseline pocket, which fits).

## Goal
New opt-in tray setting `m6_rails: true` (only valid together with `m6_joint: true`; UI: in Place on tray, under the "M6 hardware" switch, a switch "Split rails (3 pieces)"). It produces three parts instead of tray + faceplate:
1. **Faceplate** (normal wizard faceplate: 4 corner rack slots ONLY, no middle slots, plate height from `u` as today) plus two **rear stubs**, one per side, that grip the device's sides. Each stub holds two M6 heat-set pilots Ø7.6 × 7 deep, axis along Y (into the stub from the rear face).
2. **Rail L / Rail R**: L-shaped rails (side wall + floor lip) running back from the stubs, carrying the device. Each has a 4 mm front flange with two Ø6.6 clearance holes in line with the pilots, and behind each hole an open **access bay** 12 mm tall × 34 mm deep (Y) so an M6 × 8 button head (Ø10.5) and a 4 mm L-key's short arm fit. Screws go in from behind (hidden from the front).
- Joint positions follow the device: pilots at X = device side ± (pilot_d/2 + 2 mm wall) outward, Z at 8.6 and (device top − 8.6) above the floor, clamped so every pilot keeps ≥ 2.0 mm wall to the pocket and the plate edge. With the CM1000 envelope this must land within 0.1 mm of CM6A: x 22.6 / 231.4, z 8.6 / 35.85 (CM6A frame: X 0..254, faceplate front Y=0, Z=0 slot bottom; state the transform to the generator frame in the report).
- Rail wall/floor thickness setting `m6_rail_t` (default 3.3 = baseline; floor and top under the bays may thin to 2.6 like CM6A, never below 2.5). Rail length = device depth + 2 mm, capped by usable depth (fail with a plain message if it doesn't fit).
- Each part gets an engraved ID 0.5 mm deep on its top face from a new optional `test_id` setting (`<ID>-F`, `-L`, `-R`), placed off the joints.
- Export: three STLs plus one 3MF with the parts as separate objects side by side (`tools/plate_layout_stl.py`), descriptive names.

Out of scope (list in the report as gaps): light pipes, logo and other multi-colour parts of the remix (later: Print in color art or a separate task); the empty middle post holes; sleeves; rear brackets; second device.

Validation messages (Python + JS, plain words): `m6_rails` without `m6_joint`; a front opening/keystone in front of a stub; device too wide for stubs + rack slot clearance; rails longer than usable depth.

Legacy safety (most important): sources for every spec WITHOUT `m6_rails` stay byte-identical, including `m6_joint` specs (HDT-M6-A must still match `HDT-M6-A.scad` triangle-for-triangle). Use the same text-substitution/marker mechanism as `@m6`. Prove with SHA-256 of `eq.source(eq.clean(spec))` before vs after for every item in `equipment-examples.json`, both library items in a COPY of data/normal-use/equipment-library.json (read only), the HDT-M6-A spec, a sleeve, a flat and a two-device pair.

Do not touch: plate dimensions, golden keystones/`ks_tight`, rack slot positions, CM6A files, the baseline `outputs/STL_Deliveries/2026-10-16_CM1000_bracket/`, old saved revisions, TL-SG108E files, HANDOFF.md.

## Deliverable CM6B
Build, on disposable data, a CM1000 spec (envelope from the modem model, 1U, `m6_joint` + `m6_rails`, `test_id: "CM6B"`) into `outputs/CM1000_M6_generated_2026-10-28/` (date = build day): three STLs, the 3MF, the spec JSON and a README (PROPOSED — UNPRINTED, hardware one-item BOM: 4 M6 inserts + 4 M6 × 8 button heads, every UNKNOWN). The remix mesh is NOT used, so this folder has no licensing limit; still keep it in the private repo only.

## Acceptance (record all in `43-m6-split-rails-REPORT.md`)
1. `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1` passes, plus new tests in `test_m6_joint.py` (or `test_m6_rails.py`): setting accepted only with `m6_joint`; each validation message; joint positions for the CM1000 envelope match CM6A within 0.1 mm; legacy hashes identical.
2. Exact renders of CM6B: three closed single solids; faceplate ∩ rails renders empty; measured from the STLs: pilot Ø and depth, clearance Ø, min pilot wall, bay size, rail floor/top under bays, plate height, slot count (exactly 4) — table next to CM6A's values, every difference explained.
3. Viewer: `python tools/mesh_viewer.py` with CM6A and CM6B parts on one page → `work/mesh-viewer/CM6A_vs_CM6B.html` (not committed: CM6A is a licensed mesh).
4. Place on tray (browser, disposable data, port in 8700–8899): the Split rails switch appears only with M6 hardware on; preview/exact build shows three parts. Screenshot or read_page evidence.
5. Report every UNKNOWN (fit of the generated pocket vs the remix, insert retention, rail stiffness, key access) and every remix feature CM6B lacks.
