# Task 36 — OptiPlex sleeve v2 REPORT

Date: 2026-10-21. Implemented in the C: checkout supplied with this task. The D: project named in HANDOFF.md was not edited. Physical fit, retention, click-in behavior, cable access and strength remain UNKNOWN.

## Result

Added opt-in `sleeve_top`, `feet_style`, `rear_floor_opening` and `insert_bosses` to cleaning, allocation settings, source generation, Place on tray controls and mirrored validation. Defaults are omitted from cleaned specs; the v2 SCAD section and hooks are removed for legacy sources. No active data, historical specimens, coupon folders, revisions or third-party assets were changed.

All five new Python tests and five new JS tests pass. A final audit checked 1,416 distinct successful legacy fixtures observed during the complete Python checks: serialized cleaned JSON and generated SCAD UTF-8 bytes match the archived implementation exactly. This includes SLV-B/D/E, explicit defaults, and the retained regression fixtures. The permanent legacy matrix additionally checks 183 combinations/specimens.

The full check command is NOT green: one unrelated JS rack-BOM test already failed before editing and still fails afterward (`js-tests/rack-bom.js:92`, `ReferenceError: window is not defined`). It was left unchanged. Final totals: 177 Python tests, OK with 1 skipped; 222 JS tests, 221 passed and that 1 existing failure. There are no new suite failures.

## OptiPlex analytical numbers

Input: read-only SLV-B JSON with `sleeve_top=0.8`, `feet_style="grooves"`, `rear_floor_opening=true`, `insert_bosses=true`. No modified specimen spec or coupon was written. The existing oriented dimensions are 182.5 × 194.5 × 38.8 mm, including the STEP's 2.8 mm feet; case height is 36.0 mm. Orientation, source foot locations and rear stop are unchanged.

| Feature | Result, mm unless stated otherwise |
| --- | --- |
| Floor top / ordinary floor bottom | Z=3.5 / 0.5; ordinary thickness 3 |
| Side play | 0.5, unchanged |
| Top play / sliding ride lift | 0.8 / 0.5 |
| Front opening | 183.5 wide × 37.3 high; Z=3.5..40.8 |
| Band above opening | 3.625, measured to plate top Z=44.425; existing 1.5 minimum retained |
| Top lips | 3 thick, Z=40.8..43.8; still fit below the slot top 44.45 |
| Left groove | X=-76.75..-70.75, width 6 |
| Right groove | X=71.25..76.25, width 5 |
| Both grooves | Y=-4..165.8; 2.3 deep; groove bottom Z=1.2 |
| Local floor thickening | Down to Z=0 only, with 0.8 side attachment webs; 1.2 remains under the smooth grooves |
| Four dip boxes | Two tracks × Y=13.5..29.5 and 148.5..164.5, including 0.5 foot clearance |
| Dip cuts | Through the floor to Z=-0.1 cutter overshoot; no added material below Z=0 |
| Dip ramps | 1.3 horizontal run and 1.3 vertical fall, 45 degrees on front and rear; tails extend to Y=12.2/30.8 and 147.2/165.8 |
| Sleeve rear stop | Y=190.5..194.5, unchanged; no second stop on the rear bracket |
| Cable opening | X=-28..28, Y=198.5..225.7; 56 × 27.2; corner radius 2 |
| Floor to rear stop | 4 from stop's rear edge to opening |
| Rear joint clearance | 3 to the ±40 joint envelopes (half-width 9); 3 to the rear upright envelope starting at Y=228.7 |
| Sleeve wall clearance | 63.75 or more from the cable opening; exceeds 5 |
| Groove/cable separation | 32.7 along Y; no groove, dip or strap-slot overlap |
| Front insert pilots | X=±95.75; Z=6.5 and 37.8; existing 4 mm pilot diameter and 8 mm blind depth retained |
| Boss extent along Y | 0..12 |
| Hole to inside sleeve face | 2.0 minimum; bosses clipped at inside faces X=±91.75 |
| Boss outer wall | At least 3.0; nominal radius 5 is corrected to 5/cos(pi/48)=5.010728354 with fixed 48 facets so the polygon flats also retain 3 |
| Tray width including bosses | 201.521456708 (nominal circular estimate 201.5), below the 204 limit |

Grooves cut through the faceplate's lower strip at the two track entrances as well as through the tray: the feet need a continuous path from Y=-4 into the tray. Material additions start at Y=0. The lower band elsewhere, the four rack slots, side play, front-post plate, 240 mm tray, rear bracket and two rear tongue screws retain their existing geometry. The new plate holes follow `sl_joints`.

The 1.3 mm dip ramp, rather than 0.8, accounts for the existing through-pocket rule: a 3.1 mm nominal dip would leave less than 0.8 mm, so its cutter passes through the locally thickened floor. The case settles onto the unchanged Z=3.5 floor; the intended case drop remains 0.5 mm, not 1.3 mm. These are geometric intentions, not a tested detent force.

For Brian's measured 2.75 mm feet the same formulas give 2.25 mm groove depth and 1.25 mm remaining floor after local thickening. Acceptance uses the requested unchanged SLV-B 2.8 mm STEP feet.

## Implementation and validation details

- One continuous groove is formed for each overlapping X track; rotations and offsets use the existing foot transforms. All feet sharing a track must have equal heights (0.001 mm tolerance); inconsistent heights raise a clear error rather than introducing steps. Feet too short for the 0.5 mm lift or too tall to retain 0.8 above slot bottom are rejected. Ramp tails participate in interference checks.
- The cable opening is a simple centered rectangle, capped at 60 × 30, conservatively reduced around the existing rear joint envelopes. A minimum usable opening of 10 × 10 is a named design choice; insufficient space or overlap blocks it. Non-sleeve rear-support builds also account for moved rear joints.
- Bosses remain outside the sleeve and are clipped vertically between the existing floor bottom and lip top. Python, JS and SCAD width guards include their full envelope. No physical insert performance is inferred.
- Place on tray exposes the four requested controls in the sleeve/rear-support area. Defaults produce an empty allocation diff. Draft and Save behavior is unchanged. The approximate sketch marks grooves and the floor opening and shows boss envelopes; it is not an exact mesh.
- New grooves/cable opening on a two-device tray are explicitly blocked in Python and the window rather than silently duplicating or dropping geometry. Sleeve pair placement was already unsupported. New flat single-device grooves are supported and tested at all four rotations.
- Existing tests that compare older equipment implementations now point to the byte-preserved pre-task SCAD template instead of giving those older implementations the new template. The allocation-key expectation includes the four added keys. No legacy expected output was rewritten.
- Modified text files use LF; source comparison uses actual `source()` UTF-8 output, whose template reads normalize line endings as before. All original file bytes are archived.

## Commands actually run and outcomes

Commands ran from the supplied project root unless a directory is stated.

1. `Get-Content -Encoding UTF8 AGENTS.md, PROJECT.md, HANDOFF.md, ROADMAP.md`; task/queue reads; targeted `rg`, `Get-Content`, `Get-Item`, `Get-ChildItem` inspections of the three implementation files, relevant tests, checks runner and SLV-B/D/E folders/specs. No whole-project asset scan.
2. `git pull`: initial sandbox attempt failed opening `.git/FETCH_HEAD`; approved escalated retry returned `Already up to date.` No commit or push.
3. `powershell -NoProfile -ExecutionPolicy Bypass -File outputs/Mechanical_Design_App/run_checks.ps1` before editing (twice, second capture to identify the failure): 172 Python, OK with 1 skipped; JS 216/217 passed, the rack-BOM VM harness failure above. Both full runs reported `FAILED or incomplete`.
4. `New-Item`, `Copy-Item`, `Get-FileHash -Algorithm SHA256`: created byte-for-byte pre-edit backups under `docs/archive/codex/2026-10-21/task36/`, retaining relative paths. The extra allocation test was likewise copied before editing. No archive was overwritten.
5. Inline UTF-8 Python editing scripts via `@' ... '@ | & 'C:/Program Files/Python310/python.exe' -B -`, plus `apply_patch`: changed only the allowed implementation/tests/manifest and archived originals. Scripts updated the normalized JS asset hash and analytically inspected the new spec in memory; no render or export call.
6. `& 'C:/Program Files/Python310/python.exe' -B -m unittest test_tray_placement.SleeveV2Tests` from the app directory: initial run found a mistaken test assumption about the flat front joint; fixed the fixture to exercise the rear joint, then 5/5 passed. One invocation from project root failed to import the module; a `Get-Content` in the app directory also used an erroneously repeated relative path. Corrected invocations succeeded; neither failure changed data.
7. `& "$env:USERPROFILE/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe" outputs/Mechanical_Design_App/js-tests/sleeve-v2.js`: 5/5 passed. The final registered run also passes all five.
8. Full `run_checks.ps1` during implementation exposed an allocation-key test expectation requiring the four new keys; updated that test after archiving it. Final full run: 177 Python OK (1 skipped); JS 221/222 passed, only the same pre-existing rack-BOM failure. The new JS tests are registered in `js-tests/run.js`. The OpenSCAD test stays skipped.
9. Inline final compatibility audit: loaded archived `equipment.py` with archived `equipment_tray.scad`; instrumented `equipment.clean()` while running `work/gui-refinement/check_python.py` via `runpy`; after mocks finished, compared serialized cleaned specs and source bytes for all 1,416 distinct successful legacy inputs. **Zero differences.** The Python suite also passed (177, 1 skipped). SLV-B/D/E are explicitly covered in the permanent test.
10. Inline analytical parity audit using Python and a Node subprocess receiving in-memory JSON: 108 combinations of foot height (2.4/2.75/2.8/3.1/3.2/3.3), top play (0.3/0.8/2), offset (0/1/2) and U (1/2). Python/JS agreed on all 60 accepted and 48 rejected cases; accepted window, groove, floor, cable and width numbers agreed within 1e-9.
11. `git diff --stat`, `git diff --numstat`, targeted `git diff`, `git status --short`, `git diff --check`: inspected scope; removed one trailing space. Final whitespace check passed. Git warns that its future text conversion may use CRLF; no Git mutation followed.
12. Final inline Python SHA-256 calculation and UTF-8 REPORT write: the table below records byte hashes. New files have no before hash. No report self-hash is embedded because it would be recursive.

## Files and SHA-256

Paths below are relative to `outputs/Mechanical_Design_App/`. Each before hash is also the hash of the corresponding preserved archive copy in `docs/archive/codex/2026-10-21/task36/`. Archives are new copies, not modified originals.

| File | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `equipment.py` | `dd0ce94a179ac18b32c6f76899ce463dda4de95da443b128bb8b77b51fa286a7` | `ff4e34527918db03171aceedc50cf7b6ddc9fab956660d0dd92604acb8256bbd` |
| `equipment_tray.scad` | `03d5ad8929babd2e26c006757a71af2a05f762297cf8dc6688e8ed81c8a35a9f` | `11da492a09085dc0d0609879f00d482649fe443bb1d77372df1a56509f5c9b9e` |
| `tray-placement.js` | `2e2ad2766a7497f164d1c8b70c55cec1ae6fa8c8bee2e96db17f45c439a57679` | `1b762ed85bc71a31f5a9c8b7b965bb56e72d7cdbbdf2b7004ae918e943adb38f` |
| `asset-manifest.json` | `6ea84a328ccb9394e9247e3ab3ba9a06c4b4e91fcc9a0537a43f29ea606b005c` | `3ccfb123092e7a4d1ed0c5b6cd05d9fa91786d57a2af76063d39e4f93292c199` |
| `test_allocation_tray.py` | `0ad782d37ce94e914d124f40a0094d3a39f0b6927d74bd262907e22cce10763e` | `2df11eff75d46d71a20bbd23d9c11502b15a2cf352e17d3756a63eb822823fa3` |
| `test_port_openings.py` | `4b675b894ef66edae0a12e172349e8359acd31f3525bd076c0c417192f68e120` | `d1ae0ffb4ee794ac1ae55a654936e9830aaa538eb8b6eea20e9b4cb27483e61f` |
| `test_tray_placement.py` | `eb17043ab707f46d3b539585509d553873dca09ae375493cf61e152fbf91bba4` | `d392555896d6271888a60f78cc082da82b60e4c1d0784431e6830b5f91ac5e41` |
| `js-tests/run.js` | `106e66fe790ad50052f016df8215461fbac6213f923f05aa873643d3f757b853` | `d75c6916e57cc3599eeacd4dad318e1d29df00b3c3527e7a0e6ef92c539b5afb` |
| `js-tests/sleeve-v2.js` | `NEW` | `1062d4de13a31ab1dda537a7abd85207e749729542f730e8cac39dfcedb54fd7` |

New report: `work/codex-tasks/36-optiplex-sleeve-v2-REPORT.md` (this file). Eight new archive copies accompany the eight changed existing files.

## Remaining review and open questions

- Claude still needs to review the source, render the updated parts and create the next uniquely identified front coupon. No OpenSCAD render, STL/export, printing, physical testing, browser/desktop session, server start/restart, commit, push, install or upload was performed here. No proposed STL is being approved by this report.
- The full check runner remains red because of the existing rack-BOM harness failure. Repair it separately before claiming a clean overall suite.
- The allowed files exclude the shared `port_openings.py`/`port-openings.js`, artwork and Print in color consumers. The Place on tray logic and equipment source use the adapted new window. Other consumers that call the old shared sleeve helper directly can still describe the old top clearance/joint positions; review those integrations before artwork/Print in color is used with these new options. Bezel planning in the allowed files gets the new window height, but its shared planner still models the legacy joint X; check optional bezel combinations in that follow-up. Existing no-option behavior is byte-identical.
- The equal-height-per-track and single-device restrictions above are explicit implementation limits. No additional Brian decision is needed for the requested SLV-B configuration. Pull-out force, the intended click, cable passage, real 7060/7010 case equivalence, wall durability and strength remain UNKNOWN until Brian directs physical testing.

Stopped after writing this REPORT, per the task instruction. HANDOFF.md, ROADMAP.md and the task queue were not edited because they are outside May change.
