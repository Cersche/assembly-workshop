# Task 31 — rear bracket lips and vents REPORT

Implemented 2026-10-20. No renders, STL exports, printing, server restart, desktop control, user-data edits, commits or pushes. Fit, stiffness, airflow and strength remain UNKNOWN.

## Changes and preservation

Four files changed, all under outputs/Mechanical_Design_App/. Byte-for-byte originals were saved before editing under docs/archive/codex/2026-10-20/task31/. equipment_tray.scad is unchanged: its existing array-driven geometry consumes the new Python calculations. No old saved specs/revisions were modified. Tests compare cleaned specs and complete generated sources against the archived Python implementation for legacy/default, solid, open and slots, using both specimen fixtures. Those comparisons pass. The existing legacy-source test also passes.

| File | Before SHA-256 (bytes) | After SHA-256 (bytes) |
|---|---|---|
| equipment.py | 0d246b4d695a2276f0b758510db9c7920fd5ce50be8fa4dcb560875c139ba1a5 | 9b2926a8aca9c66ad0d85351659dfc5c839f460629fae931535fcafa9df98796 |
| tray-placement.js | 090d31d69dee0e5451a7fa92794d3e8977fe232ab08d3fe80c65e8b13d4f7ca0 | cf78ad80d53ffd9533bf1aa55d2242d2c4f57689531b1e34bdcd99caade43f66 |
| asset-manifest.json | 0669e0ec9f877b157de1e27f92249aca7c755edc8e8242f4e0ee878030a425b8 | 52c0ca03172b5e46fa4c21b62cddc88c707446f73278028cc2c286bbd724038f |
| test_tray_placement.py | 51b72e1f3b7c9a71f1dec2a2a6f751f57b2f2fc76768b5a7a0f31da8a362cac6 | eb17043ab707f46d3b539585509d553873dca09ae375493cf61e152fbf91bba4 |

This REPORT is new (no before hash; self-hash omitted). The asset manifest uses normalized LF text hashes as required by its existing test; table hashes above are actual file bytes. Edits use UTF-8 and Windows CRLF. The only JS edit changes the two style hints to describe inner lips and shortened ends. No new JS file needed registration.

## Lip rule and clearances

Named constants: REAR_LIP_T=2.5, REAR_LIP_DEPTH=8, REAR_LIP_LIMIT=100, REAR_EDGE_INSET=0.5, REAR_LIP_CLEAR=0.5; conservative joint half-width REAR_JOINT_HALF=9 and height above floor base REAR_JOINT_TOP=22. REAR_RETENTION_REACH accounts for flat rear stops (6.2), sleeve rear stop (4) and clip reach (1), in mm.

The top lip spans X -100..100 at the overall plate top minus 0.5 mm inset, with 2.5 mm thickness. End lips occupy X -100..-97.5 and 97.5..100 and start at floor top +0.5 mm. They meet the underside of the top lip. There is no bottom lip. Multi-U uses one overall top lip and full-height end lips above the floor.

Local lip Y is 0..8; the rear mirror maps it to assembled Y 232..240. The plate remains Y 240..244, so no changed feature projects beyond the flat outer face at 244. OptiPlex 1U top Z is 41.425..43.925; end Z is 4..41.425. These are source-coordinate/analytical checks, not a rendered mesh assertion.

Where an end lip overlaps a joint's inflated X envelope, it starts above floor base +22.5 mm instead. This conservatively clears tongues, bosses, tray joint base and upright, including the upright beginning at local Y=8.3 (only 0.3 mm from an untrimmed lip). It handles moved joint_x values and preserves at least 0.5 mm clearance. The top lip already sits above the highest modeled rear joint in 1U or taller plates. Floor clearance is independent of tray width, including 204 mm trays reaching X ±102. Lips remain 8 mm inboard of rear posts beginning at |X|=108.

Lip depth is capped at 240 minus the actual device rear, rear-retention reach and 0.5 mm. Normally it remains 8 mm; at a flat device's maximum rear position it becomes 4.8 mm to clear its rear stops. This also handles non-flat devices whose general rear margin is only 8 mm (the 11.5 mm rule is specific to flat/sleeve configurations). Geometry notes and one-line generated source comments explain shortened/omitted pieces; designs are not rejected for lip collisions. The Place on tray hints mention joint-related shortening.

Tests cover OptiPlex sleeve, 1U inserts, 2U inserts, and a 204 mm flat tray at its maximum rear position, with normal and deliberately outward joint positions. They check floor, conservative joint/boss envelopes, device/retention envelope, post bounds and inward Y orientation. Existing all-style 1U–5U checks remain passing.

## Vent pattern and measured analytical area

Staggered round holes retain the existing inexpensive 24-sided SCAD circle implementation. Named constants: REAR_VENT_D=6.5 mm, REAR_VENT_BAR=2 mm, REAR_VENT_PITCH=8.5 mm, REAR_VENT_ROW=8.5*sqrt(3)/2 ≈7.3612 mm. Each free rectangle gets its own pattern; choose normal or rotated packing by hole count. Only complete holes fit. Nearest circle boundaries are at least 2 mm apart; inscribed polygon boundaries have at least that clearance.

OptiPlex 1U uses the unchanged reinforced free rectangles:

- Upper: X -96..96, Z 25..39.425.
- Lower outside bosses: X -96..-52 and 52..96, Z 5.025..19.
- Combined rectangle area: 3999.4 mm².
- 62 holes; ideal-circle area 2057.3505 mm² (51.44%).
- Actual 24-sided polygon area: **2033.9295 mm², 50.8559%**.

The centre cable slot, boss keep-outs, 6 mm separating strip, margins and bands are unchanged. Tests require at least 40% polygon open area in each applicable reinforced rectangle for the OptiPlex and 2U inserts fixtures, complete circles, at least 2 mm inter-hole bars, and unchanged slot bounds. Existing all-U tests check hole boundaries and keep-outs. Very small free regions cannot universally guarantee 40% with complete fixed-size holes; no margin is reduced to force holes.

Complexity: 24 polygon edges per hole, giving 24 extruded wall quads / 48 wall triangles per hole; 62 holes give 1488 quads / 2976 wall triangles, versus 720 / 1440 for the former 30 holes. That is 2.067 times the hole-wall work (+1536 wall triangles). Cap triangulation and final total mesh triangles are renderer-dependent and unmeasured. No render timing or STL triangle count is claimed.

## Commands actually run and results

- git pull: sandbox FETCH_HEAD permission failure; approved escalated retry: already up to date.
- Get-Content and targeted rg: required guidance, task/standing rules, task-30 review, affected code/tests and manifest checks. One Windows wildcard rg attempt failed; explicit paths were used instead.
- git status --short: unrelated untracked work/gene-success/ existed; untouched.
- powershell -NoProfile -ExecutionPolicy Bypass -File outputs/Mechanical_Design_App/run_checks.ps1 before edits: all checks passed (142 Python, one existing render skip; 189 JS).
- Python 3.10 -B inline stdlib scripts: byte-copy originals, scoped edits, manifest hash update, analytical measurements and this report. No geometry engine/build invoked.
- Python -B -m unittest test_tray_placement.RearStyleTests: first attempted from repository root and failed module discovery; rerun from app directory. Intermediate checks caught insufficient 2U vent area with Ø6 and drove the change to Ø6.5. Final targeted run: six tests pass.
- Intermediate full run_checks: vent-area test and JS normalized-text manifest hash failed. Both corrected; the manifest now follows the existing LF-normalization contract.
- Final run_checks.ps1 (output filtered for test totals): **145 Python, OK with one existing skipped OpenSCAD test; 189 JS pass; RESULT: all checks passed**. Temporary test data only.
- git diff --stat, git diff --check and scoped equipment.py diff: four changed app/test files; no whitespace errors.

## Review and open questions

Claude still needs to render reinforced and vents for the OptiPlex, inspect mesh closure, the flat outer face and clearances, then show Brian. Analytical envelope tests do not establish mesh closure, printability in practice, airflow performance, fit or strength. No physical claims are added.

No additional decision is needed for this implementation. HANDOFF.md, queue status and other files are outside this task's May change list and were not edited. Per Brian's explicit task instructions and standing task rules, stopped after writing this REPORT; no commit/push.

## Claude review (2026-10-20)

- **Accepted.** Solid, open and slots sources are byte-identical to the task-30 output for the OptiPlex. `run_checks.ps1` passes (145 Python, 1 skipped; all JS).
- OpenSCAD.exe renders of `part="rear_bracket"`, OptiPlex sleeve on rear support:
  - **reinforced:** 1 body, 0 open edges, 2700 triangles;
  - **vents:** 1 body, 0 open edges, 8264 triangles.
  - Both span Y 232..244 only. Nothing is beyond the outer face (244), so it is flat and the bracket prints outer face down again.
- `intersection(){rear_bracket();tray();}` for both styles gives only the zero-volume contact at Y 240 where the tray's rear end meets the plate. The old solid bracket gives exactly the same contact, so the lips add no collision.
- Rendered in place and from the tray side, and shown to Brian. Vents: 62 holes, about 51 % open.
