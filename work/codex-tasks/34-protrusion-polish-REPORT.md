# Task 34 report — protrusion and keep-clear polish

Completed 2026-10-20. Software checks only. Physical fit, cable bend space, retention and strength remain UNKNOWN.

Implemented all three requested changes:

- Same-face protrusion candidates merge when their original axis-aligned boxes overlap or have at most **0.5 mm separation on every axis** (`PROTRUSION.mergeToleranceMM`). Connected components merge transitively; their union box becomes one editable question labeled **separate bodies**. Different faces and distant plugs stay separate. Testing original boxes prevents empty corners of a growing union box from swallowing another plug. The existing 32-question cap applies after merging. Case-origin and answer handling stay intact.
- `equipment.keep_clear_bands()` and `TrayPlacement.keepClearBands()` calculate nominal rear-bracket gaps without changing cuts or geometry. The warning gives the band to 0.1 mm, the nearest feature, the style's usual band (Open 3.5 mm; Reinforced/Cable slots/Vents 5 mm), merged openings, and explicit **cuts the joint boss / joint pilot** wording. Solid has no style-band comparison. Warnings neither block Apply nor move openings.
- The older flat-corner message now runs only for As today. Flush and Set back show the newer message with Set back/Sleeve advice once.

## Band rule and limits

Analyze each full rear keep-clear rectangle including its existing 0.5 mm padding. Compute shortest planar Euclidean separation to rounded style windows (2 mm radius), circular vent holes, capsule rack slots, the rounded plate edge, circular joint bosses and pilots, and other keep-clear rectangles. Joint positions and the flat/raised floor follow the existing source calculations. JavaScript mirrors the style-window and staggered-vent calculations in `rear_geometry()`; it does not render.

Intersecting/touching cutouts are named as merged rather than treating their removed intervening material as a remaining band. The band is the minimum remaining positive separation to disjoint cutouts, plate-edge margin, and joint clearance. Plate-edge or joint intersections clamp to zero; joint intersections are also named plainly. This measures local nominal gaps from each opening; it does not assess the connectivity or stiffness of the entire bracket, lips, or tray. Ideal circular envelopes conservatively enclose the SCAD polygonal circles. No numerical result establishes physical approval.

A disposable synthetic fixture reproduces the review's **2.1 mm** band: a padded cut from X -74.5 to -64.5 and Z 12.4 to 22.9 merges into a lower Reinforced window and stops 2.1 mm below the upper window. This is an analytical fixture, not a new import or measurement of Brian's SG108 STEP. Claude's requested browser review with that STEP remains outstanding.

## Files and preservation

Paths below are relative to `outputs/Mechanical_Design_App/`. Before editing, every existing file was copied byte-for-byte under `docs/archive/codex/2026-10-20/task34/`, retaining relative paths. SHA-256 values are raw file-byte hashes; manifest entries intentionally hash LF-normalized script text according to the existing contract.

| File | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `equipment-wizard.js` | `9031edebf7377afa886d317958d0697debbd7fe1d835c555ad7a0029ef9de03a` | `2147e56facb4ee1e29f533d2244467e54e0ca90c19e8c329ce59dd627711db98` |
| `equipment.py` | `51001b2d17f12619616a9c55b29f90ac1fb5e38f68235b6d666e2968732f4668` | `44e9ca76b691a987cb38fea7e65ce9acab764fc056f276aa9846db82c320cebf` |
| `tray-placement.js` | `655d256f658f257079b487938c3e4704340caf956d019968337852bb7bcae6e4` | `110f59eeca752260aa47d581ce455f8d4399f0af8f518f09d9733a0d51b2366d` |
| `asset-manifest.json` | `8e063355d093190b1334b6299650da91b752b36cf9691eff2a6285b089ec1f72` | `5b3e1b042e380164c503a18544ba1080b20ca481a5e17c43b9624db7977374af` |
| `test_port_openings.py` | `737a4821c1e2b23afebca256ebbaa6f0713b55e4424820170d3075658f75958d` | `4b675b894ef66edae0a12e172349e8359acd31f3525bd076c0c417192f68e120` |
| `js-tests/protrusions.js` | `7d490ae133fff111a32aaefe6a8cf4ed2fedd76a702e73be7f2b9f1b821c6b2c` | `112590e3c68f24b2515de8f6a0e92e22068d11cd42841a90fc3e08b2295ad2f9` |

The only other new file is this report (`work/codex-tasks/34-protrusion-polish-REPORT.md`). No historical spec or saved revision was edited. Added tests live in already registered files: `js-tests/run.js` already requires `protrusions.js`, and the Python runner already imports `test_port_openings`, so neither runner needed editing. The pre-existing untracked `work/gene-success/` was left untouched.

## Commands and actual results

From the repository root unless stated otherwise:

- Read `AGENTS.md`, `PROJECT.md`, `HANDOFF.md`, `ROADMAP.md`, task-queue README and task 34. Targeted `Get-Content` / `rg` inspections of the implementation, template and existing checks; some guessed test filenames were absent, then the registered files were located. No broad repository scan.
- **Before:** `powershell -NoProfile -ExecutionPolicy Bypass -File outputs/Mechanical_Design_App/run_checks.ps1` — exit 0, all checks passed (155 Python tests, 1 skipped; 204 JS tests).
- Byte-preserving Python stdlib archive copies and SHA-256 checks; no existing archive overwritten.
- From `outputs/Mechanical_Design_App`: `"C:/Program Files/Python310/python.exe" -B -m unittest test_port_openings.ProtrusionPolishTests` — final run: 4 tests pass. During fixture development, one run rejected a zero-height zone and another rejected the unsupported single-piece rear joint; the fixtures were corrected to valid dimensions and screw joints. Production validation was preserved.
- `"C:/Users/brian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe" outputs/Mechanical_Design_App/js-tests/protrusions.js` — final focused run: 14 tests pass. Includes touching cylinders, union dimensions and edits, tolerance boundary, distant plugs, different faces, empty union-box corners, one flat message, nonblocking warnings and joint-cut wording.
- Python tests compare **360** valid legacy combinations against the archived pre-edit module: cleaned specs equal, input dictionaries unchanged, and generated UTF-8 SCAD bytes equal, including explicit default Front position/Bezel settings. All comparisons pass.
- Node tests compare Python/JS band values and window/vent geometry for **181** disposable fixtures across all five rear styles, three mounts, 1U/2U/5U, four rotations, and a moved-joint fixture. All comparisons pass within 0.000001 mm. Independent numeric checks cover 2.1 mm, rack-slot distance, straight/rounded edges, vent clearance, adjacent keep-clear openings, and boss-only versus boss/pilot cuts.
- Python stdlib updated only the two changed script hashes in `asset-manifest.json`. An initial attempt used a repository-relative path from the app directory and raised FileNotFoundError before writing; rerun from the repository root succeeded.
- **After:** the same `run_checks.ps1` command — exit 0, **159 Python tests (1 skipped), 209 JS tests**, all checks passed. No server or OpenSCAD builds. The existing skipped test remains skipped.
- `git diff --check` — exit 0, no whitespace errors. `git diff --stat`, scoped diff and `git status --short` inspected scope. Git emitted its existing LF-to-CRLF advisory for several tracked files; it did not rewrite them.

## Remaining review and boundaries

Claude should review the one-question SG108 import and warning in the browser on disposable data. No desktop-control session, real STEP import, render, printing, export, installation, server restart, commit, push or pull was performed. No user data, `data/normal-use`, coupon files, third-party files or historical evidence was modified. The task's narrower may-change list governs; HANDOFF and the queue were not edited. No additional design decision is needed for this implementation.

## Claude review (2026-10-20)

Verdict: **done, all three spec items work.** Software checks only; fit, cable bend space and strength stay UNKNOWN.

- **Diff read against the spec.** Changes stay inside the may-change list. Merging uses the original boxes (not the growing union), same face only, 0.5 mm tolerance. Bands are warning-only: `rear_geometry()` and the SCAD are untouched. The JS warning pairs each rear zone with its band using the same condition that builds the cut list, so the order matches.
- **Checks:** `run_checks.ps1` passes: **159 Python (1 skipped) + 209 JS** (was 155 + 204).
- **Byte-identical SCAD vs 09f1734:** the archived `equipment.py` the 360-combination test loads is byte-identical to `git show HEAD:` (09f1734), and `tray-placement.js`/`equipment-wizard.js` archives match HEAD (ignoring CRLF). So the test is a true comparison with the last commit, and it passes.
- **Browser, disposable app only** (`127.0.0.1:8799`, `%TEMP%w-beta-data`, restarted on the new Python). Brian's `TP-Link TL-SG108.stp` was read in place via a throwaway local server in the scratchpad (not copied into the repo).
  - **Y is up:** **one** back question, "about 85.8 mm long, 11.0 × 85.8 × 11.0 mm (separate bodies)" (was three). 4 feet, size 158 × 101.1 × 26.5 mm, as before. Answered keep space, saved as Sits flat.
  - **Slot 1, Set back 70, Rear support, Reinforced:** "Keep-clear zone extends past the rack depth; needs a rear bracket opening; leaves a **2.1 mm band** to the style window (the Reinforced style normally keeps 5 mm); merges with style window." Matches the review number.
  - **Flush + Sits flat:** the 6.2 mm message appears **once** ("…Set back at least 10.2 mm or choose Sleeve.").
- **No render:** task 34 changed no geometry, so no exact render was needed.
- **Claude fix (tiny, pre-existing):** the wizard hint said "133.35000000000002 mm available" for 3U. `port-openings.js` now rounds that number to 0.01 mm; manifest hash updated; checks re-run and pass.
- **Brian asked to correct both notes below (same day), done by Claude:** the band warning now reads "it joins a style window and leaves a 2.1 mm band to the next style window (the Reinforced style normally keeps 5 mm)". Flush/Set back + Sits flat + Screw joint now gives **one** front message: "Flush or a set back under 15.5 mm is too close for the front screw joint and the flat corner stops. Set back at least 15.5 mm or choose Sleeve." (`port-openings.js` + its Python mirror `port_openings.py`; the old 11.5 mm flat joint line now shows only for As today). New JS test added; checks: **159 Python (1 skipped) + 210 JS** pass. Checked by tests, not re-checked in the browser.
- **Original notes:** (1) the band line says "to the style window" and then "merges with style window"; it means it merges into one window and is 2.1 mm from another, which reads a bit oddly. (2) With Flush + Sits flat + Screw joint, three red lines all point at the front gap (Sleeve/single piece under 15.5 mm, corner stops 10.2 mm, front screw joint 11.5 mm). They are each correct but could be one message later. Parked for IDEAS/beta notes, Brian's call.
