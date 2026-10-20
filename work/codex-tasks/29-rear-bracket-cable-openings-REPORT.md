# Task 29 report — rear bracket cable openings

Completed 2026-10-20. PROPOSED — UNVALIDATED. Fit, cable access, stiffness and strength UNKNOWN.

Implemented boolean `rear_openings` as a per-allocation tray setting. `clean()` keeps it only with rear support and rejects non-boolean values when support is on. Missing/false keys retain the solid bracket and byte-identical generated source: marked opt-in template additions are stripped before source generation. Saved revisions remain untouched.

Place on tray shows the requested checkbox and exact hint only with rear support. Turning support on defaults openings on; explicit false survives reopening. Opening an older rear-supported item in the editor defaults its unsaved choice on; Cancel changes nothing and Apply is explicit. Pure saved-spec resolution stays false for missing keys, preserving old previews/build identities. The wizard has no rear-support selector: it delegates those choices to Place on tray, so no wizard edit was needed. The box sketch explicitly notes that enabled cutouts are not depicted. The JS asset hash is updated.

## Rule and constants

Rounded rectangles are cut in the rear plate's 2D outline before extrusion. Bosses, tongues and slots remain unchanged. Named PROPOSED constants (mm): rear_margin=4, rear_band=3.5, rear_ear_keep=13, rear_radius=2, rear_min_window=10.

Horizontal limit = hole_x minus half the 10 mm slot capsule minus 13 = ±100.2625. Joint exclusion half-width = max(boss_d/2,tongue_w/2)+4, currently 10. Exclusion top = max(tray_z+14+boss_d/2,tongue_z+tongue_h)+4. Per U: one full-width upper candidate above that top, and three lower candidates outside/between min/max joint_x. Lower candidates stop at min(U midpoint, upper bottom minus two corner radii). This retains a 4 mm horizontal strip. Actual plate bounds and per-U boundaries keep ≥3.5 mm bands. Any candidate under 10 mm wide or high is omitted. Higher U rows conservatively repeat the joint keepout, although actual joints occur only at the tray floor.

## SLV-B versus SLV-C

The reference files were read only. SLV-B has floor Z=0.5, joints ±40, boss diameter 9 and tongue width 12.

| Opening | Implemented X | Implemented Z | SLV-C X / Z |
| --- | --- | --- | --- |
| Upper | −100.2625..100.2625 | 23..40.925 | −100..100 / 22..40.5 |
| Centre lower | −30..30 | 3.525..19 | −30..30 / 3.5..22.2 |
| Outer lower | −100.2625..−50 and 50..100.2625 | 3.525..19 | −100..−50 and 50..100 / 3.5..22.2 |

SLV-C leaves only 3 mm above the boss top (19→22); the task requires ≥4 mm (19→23). Exact capsule spacing yields ±100.2625. Actual plate edges are Z=0.025 and 44.425, giving opening edges 3.525 and 40.925. Lower windows stop at 19 to keep an additional 4 mm horizontal strip, whereas SLV-C's upper/lower windows overlap vertically. This strip is a conservative design assumption, not evidence of stiffness.

For inserts (floor 8.225), the upper opening starts at 30.725 and lower windows end at 22.225. In 2U the next row shifts by 44.45. Candidates too short/narrow are omitted rather than cutting retained material.

## Commands and verification

- Get-Content and rg read project/task guidance, SLV-B README/spec, SLV-C SCAD and relevant app/tests. A read of nonexistent test_equipment.py failed; the existing test_tray_placement.py was used.
- `git pull`: sandbox FETCH_HEAD permission failure; approved retry returned Already up to date.
- `powershell -NoProfile -ExecutionPolicy Bypass -File outputs/Mechanical_Design_App/run_checks.ps1`: baseline passed (135 Python, one skip, all JS). Initial modified runs failed because new fixtures lacked required joint/mount/hole inputs and the existing placement-key expectation needed updating. Corrected fixtures and expectation; complete rerun passed. Added the SLV-B reference test and reran: **139 Python tests, one skipped; all JavaScript passed**. Log: docs/archive/codex/2026-10-20/task29/checks-final-reference.txt.
- Python 3.10 `-B` scripts performed backups, scoped edits, manifest hashes and report creation. Each existing changed file was copied byte-for-byte before editing to docs/archive/codex/2026-10-20/task29/ with relative paths retained. First report-generation attempt failed while unnecessarily reading the log as UTF-16; no report had been written; this retry omits that read.
- `git diff --stat`, targeted `git diff`, and `git status --short` reviewed changes. Unrelated existing work/gene-success/ was untouched.
- Tests compare full legacy source against the archived template for all six mounts × 1U–5U, cover explicit false, validation and placement roundtrip, dropping the key with support off, SLV-B enabled source, analytical SCAD clearance/band expressions, and UI/sketch wiring. Tests were added to existing registered files; no new JS module required registration.

No OpenSCAD execution/render, STL export, browser/desktop session, live-server restart, printing or user-data changes. Numbers are analytical, not mesh measurements. Following the explicit task/README stop instruction: no HANDOFF edit, commit or push.

## Changed-file SHA-256

Before hashes identify the byte-for-byte archive copies. Edited text uses UTF-8/LF; legacy generated-source equality was tested with the app's text-loading behavior. Paths below are relative to outputs/Mechanical_Design_App.

| File | Before | After |
| --- | --- | --- |
| `equipment.py` | `a1ebc19d441bb1041132caaad933aabbe09251db2d999fc85aca39018768dc7c` | `c386dc37e8fdc7408387b7b6d45d84460acdb851a25ad04d56dd6a61faba6f8b` |
| `equipment_tray.scad` | `a5a3001f03c05fcb1d0a4e0fa1075932bc7c481e3283c035a67698c580e554c9` | `7c8ccb3beff49bda8dc02e93da445b7dec42956ceef2fdaf80eaa80759a9833f` |
| `tray-placement.js` | `a66f66c940505fb2ddabe517230415e4a8d89f25f41de55c2ef4ce00c351bf5a` | `2e3d1801d4ba1146cbe698c2cb730a5c0d3a587af646c873fa67cc7286514c1c` |
| `asset-manifest.json` | `09ab9487b4f8ce9abccfc55e5f4b003eb6bc2fced4742632820ca006e5e07b64` | `66d6e839f9a4acf62a63ba8bdd67362babdcbe5695348121baf47d2505d71c71` |
| `test_tray_placement.py` | `350d0932ad6c3508546e0b548fe2fb37475df023a15e2b3f875ade8038fda5b8` | `3101fac3cceb784e2e0adecda0f4229e5e3677edff670187bd92920e6e702cf8` |
| `test_allocation_tray.py` | `f7934baf060a6284047d2a146a3566df1804a8e967cc45d237d0d440b3ec82a2` | `0df89f924f1253e6129d9e79a1e477d767a60b432c1a44feae28d3474c8650bd` |
| `js-tests/tray-placement.js` | `1acfaa016ed7976433c333411cba052296b3aafc12d272f3cf0669c1131d0cd4` | `a1bdf011b08cf6e32c96cec165e9d62f0ac6d124620a94171fa0a88f9c85bda0` |

## Open questions and remaining verification

Claude's planned render must check mesh closure and actual opening clearances. Review the conservative horizontal strip and omitted-window behavior on SLV-B, higher floors, relocated joints and multi-U brackets. Browser behavior was checked through static/Node tests only. Cable connector passage, fit, stiffness and strength remain UNKNOWN. No further decision was needed for this implementation.

## Claude review (2026-10-20)

- Accepted. Diff read in full. `template_source()` strips the marked block when `rear_openings` is not set. `Path.read_text` reads universal newlines, so a CRLF checkout still matches.
- Verified independently:
  - the SLV-B spec (no key) gives source byte-identical to the saved SLV-B source;
  - `run_checks.ps1` passes (139 Python, 1 skipped; all JS).
- OpenSCAD.exe renders of `part="rear_bracket"`:
  - **OptiPlex sleeve + rear_openings:** 1 body, 0 open edges. Openings measured from the mesh: upper X ±100.25 × Z 23–41, lower X −30..30 and ±50..100.25 × Z 3.5–19. These equal the report's analytical numbers.
  - **2U inserts tray:** 1 body, 0 open edges. Two rows of windows. Row 1's upper window starts at Z 30.75, above the higher bosses; row 2 repeats the joint keep-out (the conservative choice the report notes).
- Accepted as is: the box sketch only adds a note (no cutouts drawn), which the task allowed.
- New coupon **SLV-D-REAR** made from this app output; it supersedes the hand-cut SLV-C (unprinted).
