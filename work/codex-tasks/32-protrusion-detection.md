# Task 32 · Tell the case apart from plugs and cables

Brian, 2026-10-20, beta test: he imported the TP-Link SG108 switch. The model includes the power plug sticking out of the back. The wizard measures the outer box of the whole mesh (`equipment-wizard.js`, around line 108: `dev_w/d/h = mx - mn`), so the plug counts as part of the device. That throws off everything built from that size: tray length, rear space, sleeve length and bracket position.

Brian's decisions:
- The app must **find** parts that stick out of the main case and **ask the user** what they are.
- When the user says it's a plug or cable, they can choose either to **keep space for it** or to **just leave it out** of the size. Both options must exist.

Standing rules in [README.md](README.md) apply. Fit, cable bend space and strength stay UNKNOWN. Printing and exports are not authorized.

## Build

1. **Detection** (pure function, e.g. `findProtrusions(v, mn, mx)` beside `findFeet` in `equipment-wizard.js`, or in its own small JS file if that's cleaner). Use both methods:
   - **Separate solids:** STEP/STL files often keep a plug as its own body. The main case is the largest body by volume. Flag a body that is much smaller (name the threshold, e.g. < 10 % of the main body's volume) and extends ≥ 2 mm beyond the main body's bounds on some face.
   - **Fused to the case:** slice the mesh along each axis (X, Y, Z) and measure the solid cross-section area per slice. The case is the run of slices near full size (name the threshold, e.g. ≥ 50 % of the largest). Slices beyond that run at the ends, with much smaller area and ≥ 2 mm long in total, are a protrusion on that face.
   - **Not protrusions:** the feet that `findFeet` already finds (bottom face, up to the foot height); bumps shorter than 2 mm; anything inside the case box.
   - For each protrusion, return the face (front/back/left/right/top/bottom, using the wizard's own front convention; say which in the report), its box relative to the **case** origin (x, y, z, w, d, h), and how it was found (separate body / fused).
   - Name every threshold. Keep it fast enough for the meshes the wizard already handles (OptiPlex STEP, Pi 4). Report the time taken.
2. **Asking the user** (wizard import step, next to the feet list). For each protrusion, show plain wording such as:
   > "Something sticks out of the back: about 35 mm long, 10 × 8 mm. What is it?"
   - **Part of the case**: keep it in the size.
   - **Plug or cable, keep space for it**: leave it out of the size, and save it as a keep-clear zone.
   - **Plug or cable, leave it out**: leave it out of the size, and save nothing.
   - Highlight the protrusion in the 3D preview (a coloured box is fine) while its question is shown.
   - The user **must answer** each question before the wizard moves on or saves. Nothing is preselected. Say clearly that "Part of the case" is the safe choice when unsure.
   - The numbers are editable, like the feet rows.
3. **Size from the case.** When a protrusion is not "Part of the case", `dev_w/d/h` come from the case only. Feet, holes, front ports and rear ports must be measured from the **case** origin, so they don't shift when a plug on the left, front or bottom is left out. Test that.
4. **Saving.** Add `protrusions: [{face, x, y, z, w, d, h, keep_clear: true}]` to the spec, but only for "keep space" answers. Validate it in `clean()` like `feet` (a list, a sensible maximum count, numbers in range). "Leave it out" saves nothing. Specs without `protrusions` must give **byte-identical** SCAD source to today.
5. **Using the keep-clear zones.** No new geometry in the tray itself. Plain-language checks and warnings only, plus one geometry link:
   - **Back:** if the zone runs into the rear bracket plate, the bracket gets an opening for it, the same way `rear_ports` already make cable openings (`rear_geometry`). If it goes past the rack depth or into the rear posts, warn.
   - **Sides / top:** warn if the zone hits a post, the tray walls, a sleeve wall or the top of the U.
   - **Front:** warn that it would go through the faceplate. Don't cut anything automatically.
   - Say in every warning that real cables need extra bend space the app can't know.
6. **Summary:** the save summary counts the zones ("…, 4 feet, 1 keep-clear zone, …"), and leaves the text out when there are none, like feet.

## Tests

- Synthetic meshes:
  - a box plus a separate small cylinder on the back;
  - the same cylinder fused to the box;
  - a box with feet only (no protrusion);
  - a box with a plug on the left (case origin must not shift).
- Detection finds the right face, size and method. Feet are not reported as protrusions.
- All three answers give the right `dev_w/d/h`, and holes/feet/ports stay at the right positions.
- `clean()` accepts, limits and round-trips `protrusions`. Old specs give unchanged source.
- A back keep-clear zone produces a rear bracket opening. Side/top/front zones produce the warnings.
- The wizard can't save while a question is unanswered.
- No STL exports.

## May change

`equipment-wizard.js` (or one new JS file, served the same way and listed in `asset-manifest.json`), `equipment.py`, `equipment_tray.scad` (only if the rear opening needs it), `port_openings.py`, `tray-placement.js` (warnings only), `mesh_study.py` (optional: a `protrusions FILE` command that uses the same rules, for Claude's review), `asset-manifest.json`, `test_*.py`, `js-tests/` (register new tests in `js-tests/run.js`). Nothing else; never data/normal-use, the coupon folders or third-party files.

## Checks and report

Run `run_checks.ps1` before and after. Write `work/codex-tasks/32-protrusion-detection-REPORT.md` with:
- files with SHA-256;
- the detection rules and named thresholds;
- the spec field;
- how keep-clear zones feed the bracket and warnings;
- check results;
- open questions.

Claude reviews it with Brian's real SG108 model in the browser on disposable data.
