# Task 30 report — rear bracket styles

Implemented 2026-10-20, ready for Claude's render review. No renders, STL exports, printing, desktop control, server restart, user-data writes, commits or pushes. Fit, stiffness, airflow and strength remain UNKNOWN.

## Implementation

Added spec/placement `rear_style`: solid, open, reinforced, slots, vents. Explicit style wins over the legacy boolean. Missing style falls back to rear_openings; neither key means solid. Regression checks confirm unchanged legacy solid and task-29 open generated sources. Invalid styles are rejected; support off drops rear_style in cleaned specs and explicit disabled placement settings.

Place on tray now has the conditional five-chip row, individual hints ending “stiffness/airflow UNKNOWN”, and a sketch style note. Newly enabling rear support selects reinforced. Existing rear-supported items retain their saved/legacy choice when opened; they are not silently upgraded. The wizard delegates tray choices, so equipment-wizard.js needed no edit. Asset manifest hash updated.

New bounds are calculated in equipment.rear_geometry and serialized directly into SCAD arrays. Marked SCAD modules are stripped from legacy sources. Old revisions and coupons remain untouched.

## PROPOSED style rules and constants (mm)

- Solid: original plain plate, no cuts or flanges.
- Open: task-29 layout unchanged; margin 4, bands 3.5, minimum strip 4, radius 2, X limit 100.2625.
- Reinforced: same window arrangement, REAR_MARGIN=6, REAR_BAND=5, REAR_STRIP=6, REAR_LIMIT=96, radius 2, outer flanges.
- Cable slots: reinforced safe bounds, upper and centre openings only; radius 5.
- Vents: centre cable slot (radius 5), round holes entirely inside conservative free rectangles above/beside the joint keep-outs; outer flanges. REAR_VENT_D=6, REAR_VENT_PITCH=9, alternate row offset 4.5; rows 9 apart. Each hole uses 24 facets. No partial holes or holes in bands, ears, joint keep-outs or centre-slot territory.
- All windows/slots under REAR_MIN=10 in either dimension are omitted. Joint exclusions and opening bands repeat per U, through 5U. New cuts stop at X +/-96.
- Flanges: REAR_LIP_T=2.5, REAR_LIP_DEPTH=8, REAR_LIP_LIMIT=100, REAR_EDGE_INSET=0.5 vertically. Four continuous lips at the overall top/bottom and ends, only on reinforced/vents.

## OptiPlex numbers

Read-only reference: SLV-B_spec.json, 182.5 x 194.5 x 38.8, four 2.8 mm feet, sleeve low floor 0.5, 1U. This is an analytical fixture, not a new coupon. Coordinates are rack X and slot-bottom Z; dimensions are bounding rectangles.

| Style | Windows / slots (mm) | Vent count | Flanges |
|---|---|---:|---:|
| solid | none | 0 | 0 |
| open | X [-100.263, 100.263], Z [23, 40.925] (200.525 x 17.925); X [-100.263, -50], Z [3.525, 19] (50.2625 x 15.475); X [-30, 30], Z [3.525, 19] (60 x 15.475); X [50, 100.263], Z [3.525, 19] (50.2625 x 15.475) | 0 | 0 |
| reinforced | X [-96, 96], Z [25, 39.425] (192 x 14.425); X [-96, -52], Z [5.025, 19] (44 x 13.975); X [-28, 28], Z [5.025, 19] (56 x 13.975); X [52, 96], Z [5.025, 19] (44 x 13.975) | 0 | 4 |
| slots | X [-96, 96], Z [25, 39.425] (192 x 14.425); X [-28, 28], Z [5.025, 19] (56 x 13.975) | 0 | 0 |
| vents | X [-28, 28], Z [5.025, 19] (56 x 13.975) | 30 | 4 |

Reinforced/vents flange assembled Y is [244,252], wholly behind the outer bracket face Y=244. Top/bottom lips: X [-100,100], Z [41.425,43.925] / [0.525,3.025]. End lips: X [-100,-97.5] and [97.5,100], Z [0.525,43.925]. Cut-to-lip separation is at least 1.5 at ends and 2 vertically. Rack slots begin at |X|=113.2625, at least 13.2625 from lips. Lips stay 4 mm inside the nominal 208 mm post opening and far from plate corner rounding. They do not project inward into the modeled tray/device/joints; adjacent U lips stay inside their plate bounds. This checks analytical nominal envelopes, not rendered source-mesh collisions, actual post tolerance, cable routes, plugs or service access.

Vent counts: sleeve 1U: 30, inserts 1U: 18, sleeve 2U: 60, inserts 2U: 36, sleeve 3U: 90, inserts 3U: 75, sleeve 4U: 99, inserts 4U: 93, sleeve 5U: 129, inserts 5U: 111.

2U inserts fixture: 85 x 100 x 20, floor 8.225. Its upper windows/slots are omitted (available height 6.725/6.7, below 10); centre/side windows remain. Round vents can fit the upper region. No bands or margins are reduced to force an opening.

## Commands and results

- `git pull`: initial sandbox FETCH_HEAD permission failure; approved escalated retry succeeded, already up to date.
- Get-Content/rg: read required guidance and targeted app/test/check-runner references. A guessed test_rear_openings.py was absent and a Windows wildcard rg path failed; actual tests were found in test_tray_placement.py.
- `& outputs/Mechanical_Design_App/run_checks.ps1` before editing: passed, 139 Python (one existing skip), 189 JavaScript.
- First after-edit run: 142 Python, one expected placement-key-set assertion failed; one existing skip; JS passed. Added rear_style to the expected key set.
- Final same checks command: passed, 142 Python (one existing skip), 189 JavaScript. Temporary data only; no OpenSCAD builds.
- Added checks cover legacy source identity, explicit style precedence, validation/drop, all five styles on sleeve/inserts for 1U–5U, margins/bands/web, boss/tongue/rack-slot exclusion, flange bounds/orientation and serialized geometry. Extended existing registered JS tests for style choices/drop and UI markup; no new JS test file required registration.
- Python 3.10 stdlib inline scripts: byte-for-byte backups before edits, scoped edits, manifest update, analytical values and report. Initial report calculation omitted mounting holes on the inserts fixture and correctly failed validation before writing anything; rerun used the valid fixture.
- `git diff --stat`, `git status --short`, scoped `git diff`, `git diff --check`: reviewed, no whitespace errors. Git warns about future LF-to-CRLF normalization. Edits are UTF-8/LF; archived originals retain their bytes. Unrelated untracked work/gene-success/ left untouched.

## Files and SHA-256

Byte-for-byte originals are in docs/archive/codex/2026-10-20/task30/ with matching relative names. These seven application/test files changed; this report is new (no before hash, self-hash not embedded).

| File (under outputs/Mechanical_Design_App/) | Before SHA-256 | After SHA-256 |
|---|---|---|
| equipment.py | c386dc37e8fdc7408387b7b6d45d84460acdb851a25ad04d56dd6a61faba6f8b | 0d246b4d695a2276f0b758510db9c7920fd5ce50be8fa4dcb560875c139ba1a5 |
| equipment_tray.scad | 7c8ccb3beff49bda8dc02e93da445b7dec42956ceef2fdaf80eaa80759a9833f | 03d5ad8929babd2e26c006757a71af2a05f762297cf8dc6688e8ed81c8a35a9f |
| tray-placement.js | 2e3d1801d4ba1146cbe698c2cb730a5c0d3a587af646c873fa67cc7286514c1c | 090d31d69dee0e5451a7fa92794d3e8977fe232ab08d3fe80c65e8b13d4f7ca0 |
| asset-manifest.json | 66d6e839f9a4acf62a63ba8bdd67362babdcbe5695348121baf47d2505d71c71 | 0669e0ec9f877b157de1e27f92249aca7c755edc8e8242f4e0ee878030a425b8 |
| test_tray_placement.py | 3101fac3cceb784e2e0adecda0f4229e5e3677edff670187bd92920e6e702cf8 | 51b72e1f3b7c9a71f1dec2a2a6f751f57b2f2fc76768b5a7a0f31da8a362cac6 |
| test_allocation_tray.py | 0df89f924f1253e6129d9e79a1e477d767a60b432c1a44feae28d3474c8650bd | d54ea5bc264bc4a660ac1d2fc9a7a17457fca4134e159be20128c208dc7576ef |
| js-tests/tray-placement.js | a1bdf011b08cf6e32c96cec165e9d62f0ac6d124620a94171fa0a88f9c85bda0 | dc94fc27957d6ddb266643fe070ef5731d11d86caa4ffa1eaec3b801c8d22ebe |

## Assumptions and open review

Reinforced remains the requested default. Vent rectangles conservatively preserve the reinforced horizontal web and reserve centre-slot territory even when a slot cannot fit. Review the appearance with Brian.

Claude must still render every OptiPlex style, check mesh closure/clearances and show Brian. Render speed is unmeasured; counts and 24 facets bound vent complexity. No live GUI check was performed; UI checks were static/pure-logic tests. Fit, stiffness, airflow, strength, cable access and actual rack collision approval remain UNKNOWN.

Stopped after writing this report under the explicit task/standing rules. HANDOFF.md was outside the May change list and was not edited; no commit or push.

## Claude review (2026-10-20)

- **Accepted, with two follow-ups.** The legacy sources are unchanged: the SLV-B spec gives byte-identical solid source and the SLV-D spec byte-identical task-29 open source. `run_checks.ps1` passes (142 Python, 1 skipped; all JS).
- OpenSCAD.exe renders of `part="rear_bracket"` for the OptiPlex sleeve on rear support, one per style: all are **1 body, 0 open edges**. Times were 5–6 s, and 10 s for vents. Measured openings equal the report:
  - reinforced: X ±96 × Z 25–39.5, plus X −28..28 and ±52..96 × Z 5–19;
  - slots: the upper and centre windows only;
  - vents: 30 round holes and the centre slot.
- Rendered in place behind the Dell model with stand-in posts, and shown to Brian.
- **Follow-up 1 (printability, my spec's gap):** the outer-face lips put 8 mm features on *both* faces (bosses/tongues inside, lips outside). The bracket can no longer print flat on its outer face as it does today. A fix is lips on the inner face: a full-width top lip, and end lips starting above the tray floor (a bottom inner lip would hit the floor at Z 0.5–3.5).
- **Follow-up 2 (airflow):** vents gives only 30 × Ø6 holes (about 850 mm² open) behind the PC's large exhaust grille. The free area between the rows is unused. A denser pattern (smaller pitch, or slots) would serve the exhaust better.
