# Task 32 report — 2026-10-20

Implemented protrusion screening, mandatory unanswered questions (no default answer), editable bounds, orange preview boxes, case-relative remeasurement, keep-clear persistence, rotated warnings and rear-bracket cuts. No user data, server, exports, prints, installs, commits or pushes were touched. Task README restrictions were followed. A final integration regression correction retains unflagged short bumps/large secondary case bodies in the envelope; direct execution of the wizard frame-sync function now tests holes, feet and both port lists on left/front/bottom exclusions. See task 33 for the final combined check run (155 Python, 1 skipped; 204 JS passed) and temporary PNG-only rendering of a solid rear-bracket keep-clear cut.

## Detection and coordinates

Front is -Y, back +Y, left -X, right +X, bottom -Z, top +Z after wizard orientation. Components weld shared vertices to 0.001 mm. Main body is largest absolute signed enclosed volume. Separate bodies below 10% of it and extending at least 2 mm are candidates. The main body is sliced on all three axes at up to 0.5 mm spacing, capped at 600 slices per axis. Oriented triangle/plane segments give signed solid sectional area (including holes), rather than a bounding-box area. Full-case slices have at least 50% of maximum area; small-area end runs at least 2 mm become fused candidates. Bounds include clipped triangle/plane intersections. Foot-height bottom runs (within 0.5 mm slice tolerance), internal bodies and shorter bumps are not questions. At most 32 questions. Foot exclusion tolerance is the named `footToleranceMM=0.5`. Unflagged short bumps and large secondary case bodies remain in the measured envelope. Fused bounds have up to one slice of uncertainty; orientation, closed coherent winding and a recognizable main case are assumptions. Questions permit correcting numbers and retaining uncertain features as case.

The existing feet-inclusive vertical size convention is preserved so floor pockets/case height are not applied twice. X/Y origin is the selected case front-left. Answers recompute size and translate detected holes, feet, pending ports and entered front/rear ports (including centre-relative X compensation). Keeping as case includes that box; space/omit excludes it. Only space saves `protrusions: [{face,x,y,z,w,d,h,keep_clear:true}]`. List maximum 32, coordinates -500..500 mm, sizes 0.1..500 mm, finite values, six faces, explicit true required. Empty list is omitted from clean output.

## Keep-clear use

Device-local boxes rotate with placement, then translate by device lift/offset. Boxes intersecting assembled rear plate Y=240..244 produce rectangular openings with 0.5 mm clearance, including solid brackets and any inner lips. No tray geometry is cut. Existing rear_ports are planning-only in the code inspected, so this adds a conditional cut path through rear_geometry/template_source instead of assuming rear_ports already cut holes. Warnings cover faceplate, depth, nominal posts, walls, allocated height and rear openings, each with unknown extra cable bend space. They do not certify bands, remaining joints, retention or strength. Summary counts zones only when present.

## Checks actually run

- `git pull`: initial sandbox FETCH_HEAD denial, approved retry: already up to date.
- `powershell -NoProfile -ExecutionPolicy Bypass -File outputs/Mechanical_Design_App/run_checks.ps1`: first baseline run transiently returned incomplete; immediate baseline repeat passed (148 Python, 1 render test skipped; all JS).
- Same command after implementation: initial failures in the legacy isolated import stub, archived-module template lookup and fused synthetic fixture were fixed. Final log: `docs/archive/codex/2026-10-20/task32/check-pass.log`: 150 Python, 1 skipped, all JS passed. Synthetic separate and fused cylinders, feet-only/internal/short bump, three answers, left/front/bottom origins, rotated zones, backend list/range validation, bracket cuts and unchanged legacy source covered.
- Direct Node run of js-tests/protrusions.js during debugging; final full suite passes its seven tests. 50,000-triangle screening: 198.0 ms in final full run (includes component grouping and all three slice directions). This is synthetic timing, not a measured OptiPlex or Pi mesh benchmark.

## Review limits / open questions

No desktop session or real SG108 browser review was authorized by this task. Claude's specified disposable-data review remains. Detection is heuristic: malformed/open meshes, nested or unusually segmented shells, broad tapered ends and overlapping components need user review. Case origin is constrained by existing feet-inclusive Z semantics. Rear-zone cuts may reduce bands/joints; warnings require inspecting the exact result. Physical fit, cable bend allowance and strength remain UNKNOWN.

## SHA-256 (raw file bytes)

Before copies are byte-for-byte under docs/archive/codex/2026-10-20/task32/. Shared-file hashes below are the task-32 completion snapshot, before task 33 (preserved by task-33 before copies). The wizard and new protrusion-test hashes include the final integration correction; their final versions remain task-32 changes. Task 33 lists the final hashes of shared files.

| App-relative file | Before | After |
| --- | --- | --- |
| `equipment-wizard.js` | 2ba068086547b00ed264f0dcab990bfb00b1825beaf3961a0a44eea26e46be91 | 31f242a41c65f81b02a2a47465f634a55ef0f3f9be08ce29c2db08ea262d86de |
| `equipment.py` | 9b2926a8aca9c66ad0d85351659dfc5c839f460629fae931535fcafa9df98796 | 13ccc58b1b9731d99a8217aed467b43a9004c6d1dbdae66b9a418d7c808de7e3 |
| `tray-placement.js` | cf78ad80d53ffd9533bf1aa55d2242d2c4f57689531b1e34bdcd99caade43f66 | 25a30337fb4521f437f9028b9390c084da90968a9e9b6caf9a2717382b5a6fb4 |
| `asset-manifest.json` | 4b2d87b12c869053fd24a91677568246ef4d5c8e5d41a829a47dcafbc0cd8733 | 221b973798bf27933c0db1bf148846a40b1fce070096942d70ce73923da1f04e |
| `test_port_openings.py` | 432d51d17ce37e0002eb4e64b02fe190e5154347ea20551ea00e0309ba8813c3 | b81193d81e5cf2a668ec6d6e83266478f49ea3b94c0f898aeba8c36440db9b98 |
| `js-tests/run.js` | 6d2e33a6b09ab1a9e69eeb06fab20be04d9e1629498273890fc18d45eda697f1 | f1853bb30607cbfed2116703fa557637e7d432e179094e2c5ec9ce485080bf04 |
| `js-tests/flat-floor.js` | dea65bd652f3a70224211c4022cf6c4f88db88596587b810665938ff424a07a6 | b258e71004ac1f809ddf927edda7dd19b3b4ccf3771406473b368a98b9920272 |
| `js-tests/protrusions.js` | NEW | 7d490ae133fff111a32aaefe6a8cf4ed2fedd76a702e73be7f2b9f1b821c6b2c |

## Claude review — 2026-10-20

**Verdict: accepted, with one small fix made by Claude and polish queued as [task 34](34-protrusion-polish.md).**

- **Checks:** `run_checks.ps1` → 155 Python (1 skipped, the opt-in render test) + 204 JS, "RESULT: all checks passed", before and after Claude's fixes.
- **Old specs unchanged:** 1,445 variants of the 5 disposable-library items (every mount, 1U/2U, 0°/90°, every rear style, both joints) give byte-identical SCAD source or the identical error compared with HEAD `72ea798`.
- **Real SG108 in the browser** (disposable app on 127.0.0.1:8799, data `%TEMP%\aw-beta-data`; Brian's `Downloads\TP-Link TL-SG108.stp`, read in place, not copied). With **Y is up**: 4 feet (1.5 mm), and three questions at the back (cable 76.3 mm, plug 29.1 mm, plug tip 15.1 mm, all "separate body"). Orange boxes appear in the 3D preview. Nothing is preselected. Next and the step tabs stay locked until all three are answered, and the note says "Part of the case" is the safe choice. Size comes from the case: 158 × 101.1 × 26.5 mm (real case 158 × 101 × 25, plus 1.5 mm feet). Setting the tip to "Part of the case" grows the depth to 105.6 mm; "leave it out" returns it to 101.1. Saved as flat: `protrusions` holds the two "keep space" zones only, and the summary says "4 feet, 2 keep-clear zones".
- **Rear bracket opening:** in Place on tray, Set back 70 mm + Rear support gives the warning "Keep-clear zone extends past the rack depth; needs a rear bracket opening; check remaining bands and joints. Real cables need extra bend space the app cannot know." Exact OpenSCAD render of that slot: a closed mesh (0 bad edges, 1 body), opening X −71.4…−59.4, Z 10.8…22.9 (zone + 0.5 mm). It merges into the Reinforced lower-left window and leaves a **2.1 mm band** (task 34 will report this number).
- **Fixed by Claude:** keep-clear rectangles were also added to `rear_geometry()['windows']`, which Cable slots/Vents cut as radius-5 rounded hulls. A 7 × 7 mm zone became about 13 × 13 mm (it reached Z 20 instead of 23). They now go under `rear_geometry()['keep_clear']` and are cut only by the plain `keep_clear_cut()` on every style. The re-render cut stops exactly at the zone + 0.5 mm. A regression assertion was added to `test_port_openings.py`. Also rounded the protrusion number boxes to 0.1 mm for display (they showed raw floats); the manifest hash was updated.
- **Follow-ups (task 34):** merge touching bodies on one face into one question (the SG108 asked three times about one plug); give the remaining band in the warning; remove a duplicated flat-mount message.
- Detection is heuristic, and fit, bend space and strength stay UNKNOWN.
