# Task 23 — flat device / low tray floor report

2026-10-20. Implemented; automated checks pass. Physical fit, retention and strength remain **UNKNOWN**. No server, browser, renderer, STL export, printing, commit or push was run. Stopping for Claude review as requested; HANDOFF.md and queue README were not edited.

## Behavior and geometry

- New `flat` mount: “Sits flat on the tray (PCs, boxes)” in Place on tray. No holes or standoffs required. Standoff input is hidden for flat and straps, with a floor/retention explanation.
- `floor_z=0.5` mm for flat; 7 mm for all previous mounts; floor thickness stays 3 mm. `tray_z` remains an internal alias for `floor_z` so existing joint expressions move together. This is a nominal 0.5 mm clearance above Z=0, chosen rather than putting the underside on the slot boundary. Geometry imposes no unique smallest positive clearance; this is a design allowance, not measured rack clearance.
- OptiPlex envelope 182.5 × 194.5 × 38.8: floor top 3.5 + device 38.8 = **42.3 mm**, within **44.45 mm / 1U**, with 2.15 mm nominal remaining. Inserts still need 54.8 mm / 2U at the default 6 mm standoff. Straps now correctly omit standoff but retain the old 10 mm floor top.
- Screw tongue spans Z=4–7; its clearance slot spans 3.85–7.15. Boss centre is Z=14.5, its 9 mm diameter spans 10–19. The 4 mm pilot spans 12.5–16.5. Riser top is 22.5. These features remain inside the 42 mm 1U faceplate height and above the lower boundary. The unchanged tongue/slot relative dimensions preserve nominal engagement only, not physical approval.
- Lowering the device exposed an actual interference: existing gussets reached Y=22, into the default device starting at Y=12. Flat mode shortens their rear endpoint from 20 to 9.5 (including cube thickness, ends at 11.5). Riser ends at Y=11.3. Python, JS and SCAD enforce at least 11.5 mm device gap at screw joints, including the mirrored rear bracket. Flat single-piece mode requires at least 6.2 mm front gap so front stops stay supported by the floor.
- Retention: eight small blocks forming stops along both edges at each corner, outside the device footprint with 0.2 mm nominal clearance. Blocks are up to 6 × 6 mm, height min(6, device height); footprint dimensions also clamp for very small devices. They constrain lateral sliding; they do not clamp down. Existing strap slots are enabled for flat so a strap can restrain lift. Strap capacity, clearance and retention remain UNKNOWN. Live box sketches show these stops.

## Height and compatibility implementation

`port-openings.js` owns shared JS `floorZ`, `usesStandoffs`, `deviceLift`, `neededHeight`, `autoU` and `flatHint` functions. Wizard import/orientation auto-U, model and port lift, placement checks/sketches, front openings and rear/custom cable markers consume these. Python uses corresponding helpers in equipment.py. Inserts, pegs and clips add standoff; straps and flat do not.

Step 1 shows the short flat hint for imported models only when flat reduces the needed U count, with required and available height. It never changes the mount automatically; mounting remains in Place on tray. Rotated front openings retain the established keep-as-entered behavior.

The allowed-file list excludes `port_openings.py`. Its historical helper remains untouched; equipment.allocation_spec corrects its height delta using the shared Python device-lift rule. Direct callers of that old standalone helper do not acquire flat semantics; the manufacturing allocation path and JS consumers do. Joint opening exclusion still conservatively uses the existing 29 mm top, rather than reducing the exclusion to the flat joint's 22.5 mm top. This can reject some otherwise possible opening arrangements; it does not relax clearance.

To meet exact generated-source compatibility, equipment.template_source removes explicitly marked flat-only template sections and restores the three changed legacy expressions for non-flat specs. No runtime archive dependency is introduced. Generated SCAD remains exactly the previous text for old mount modes; fixed pre-edit SHA-256 regression fixtures cover inserts, pegs, clips and straps. Existing export-quality tests now compare against that compatibility template; the new independent fixed hashes prevent the compatibility assertion becoming circular. Existing saved data, revisions and caches were not rewritten.

Four changed frontend hashes were updated using LF-normalized UTF-8. Edited source files are now LF on disk; archive copies retain original bytes. No new frontend script or app.py change was needed.

## Commands and observed results

- Read AGENTS.md, PROJECT.md, HANDOFF.md, ROADMAP.md, task queue README and task 23 with `Get-Content`; inspected relevant source/tests with `Get-Content` and `rg`.
- `git status --short`: pre-existing README modification and untracked task/prompt files; left untouched.
- `git pull --ff-only`: first attempt could not write .git/FETCH_HEAD in sandbox; approved escalated retry returned **Already up to date**.
- Baseline command (run twice before editing): `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1` — **114 Python tests: 113 passed, 1 skipped; 172 JS passed; all checks passed**. The second run recovered compact results after the first batched output was truncated.
- Inline Python 3.10 (`C:/Program Files/Python310/python.exe -B -`) copied originals byte-for-byte before editing, captured old generated-source hashes, applied scoped edits, updated manifest hashes and wrote this report. No installs.
- Intermediate checks before manifest refresh: **114 Python tests, 1 skip; JS manifest test failed on changed cable-ports.js hash**. This was corrected by refreshing the four changed asset entries.
- After new tests and manifest refresh: **119 Python tests: 118 passed, 1 skipped; 176 JS passed; all checks passed**.
- Final rerun after adding the single-piece corner-stop support guard: same **119 Python / 1 skipped, 176 JS passed**, command exit **0**. The skipped test is the pre-existing opt-in OpenSCAD keystone render test. No rendering was enabled.
- `git diff --check`: passed, including final invocation. Git reported LF-to-CRLF checkout-policy warnings on inspection; no whitespace errors. `git diff --stat`, scoped `git diff` and final `git status --short` reviewed scope.

Tests cover each mount's exact height boundary, no-hole flat OptiPlex acceptance and inserts rejection at 1U, old source hashes, front-opening floor transitions in both directions, rotated opening preservation, front/rear joint guards, single-piece stop support, executed wizard-import auto-U, hint content/wiring, sketch floor/device levels and front/rear/custom cable Z.

## Remaining review / assumptions

Claude's browser check with the OptiPlex STEP is still pending. No new mesh was rendered: digital geometry reasoning and source/logic tests do not establish mesh closure or physical fit. The shortened gussets, stops and nominal 0.5 mm underside clearance need review and later physical validation only at Brian's direction. Device feet, protrusions and port access depend on the imported envelope and entered ports; no additional clearance is claimed.

Task-specific no-commit/no-push and report-then-stop instructions were followed. No user data was accessed for testing. Existing tests use disposable fixtures (some mock the build/export path; no real STL export). No approval is inferred for printing or release.

## Files and SHA-256

Paths below are relative to `outputs/Mechanical_Design_App/`. Originals are under `docs/archive/codex/2026-10-20/task23/` at the same relative paths. Each archived copy's hash is the Before value; all ten copies were created before edits. New report and archive copies are the required task deliverables in addition to the allowed implementation files.

| File | Before (original/archive bytes) | After (current bytes) |
| --- | --- | --- |
| `equipment.py` | `55f4ce2c94e362bf35f490ee37a36aa233c65cc8ce38d67069ac43512d27c607` | `cc722910da57641a6da6ef67ea9f95548ae885207549992ec3376151eaf81210` |
| `equipment_tray.scad` | `4c98aa5ba251a87edf641276f71a022f09b273633fec2421c5f63606c903f5fa` | `a51f4a6d4fcd586c4e1d63db84ff6c8662277ab06775a90ad5b5e5e411f11c77` |
| `equipment-wizard.js` | `92bfbd3db89351fec51d3a83c020300886f987e62611cc24b819e0d99b510cd1` | `08baa1202dd18f1201e400428c9b4d3218b329ded372162f2ce42a71dce7b947` |
| `tray-placement.js` | `fc4d85dba575b0e76716316870e05caa54650b6dee78c4a99f98ba4daadfefa3` | `e7df6306a0638f78d79fd54a8a2236d6151bc34fd5d1bf7ba1144cad255888fa` |
| `port-openings.js` | `7e865f7d4861ea8e7f02d0d8c94084f66a6fc07bfe12582f0357a64a693725e7` | `0a1436e9cc7d23d7459c602ba9dd0c724a0fe1e924cce782805752e153463b92` |
| `cable-ports.js` | `43430bfe347f05bedf12a16ec201dd201600efad1fe796fd579c572373ed423f` | `1df78e24bba2b7929ddc77c1322a37c47fa111a1d5173bdf0f3050618adf5632` |
| `asset-manifest.json` | `3fe5f50acbc3083af7f2563ef9d9e6e7b3a1ff4c6c0c73d215cc440b581fa734` | `7d0e3e7a25645b24c4f92a1e5ab72123b266250e71f9e732d65ed5c8807682ff` |
| `test_export_quality.py` | `8775806fc580ebf6ccf9751a97fd819289fbb23ca0825c67e683d4fdb35e9a83` | `df22e4b3630c64ae556baed4d03cc67dcb4b8b8da8f9282e46a50b477c181b40` |
| `test_tray_placement.py` | `3097224ce71887e519878aa6c875d3e46f50c4527316a626c87b1b321b16010b` | `be1f4e8b14ceb6a520c74464b6578476b6ccad1c050ac009552ae61339271821` |
| `js-tests/run.js` | `a1d3bb22cd6f21c67d4fa88c2d3014b2320ce68eb920a9f5517095480625351d` | `08f09edd9a7e7973434997d7127c9572de129a75e79ad946087e91786c1eedfd` |
| `js-tests/flat-floor.js` | `NEW` | `07d52fd198da37b4350f79e2ef2702f1113951959e316a4f0eff88328ab95228` |
