# Task 33 · Front position (flush or set back) and Bezel

Do this after task 32 (both change `equipment.py`).

Brian, 2026-10-20, beta test: the user should choose whether the device's front (its ports) sits **flush** with the outside of the faceplate or **set back**, with an adjustable amount. Openings in the faceplate should get a subtle softened edge so a set-back doesn't look jarring. Brian approved the name **Bezel** with **None / Chamfer / Rounded**.

Today there is no choice:
- normal trays put the device front `front_gap` = 12 mm behind the plate's rear face, about 16 mm behind the front face;
- Sleeve puts the device front flush with the plate front (`dev_y = -plate_t`).

Standing rules in [README.md](README.md) apply. Fit, looks after printing and strength stay UNKNOWN. Printing and exports are not authorized. **The keystone openings stay untouched** (the settled `ks_tight` fit depends on their exact shape).

## Build

1. **Front position** (a per-slot Place on tray setting, saved like `rear_style`; the wizard's tray defaults may offer it too):
   - **As today** (default, nothing changes);
   - **Flush with faceplate**: the device front lines up with the plate's front face;
   - **Set back**: a number in mm, measured from the plate's front face to the device front. Name the limits.
   - When the device front would sit inside or in front of the plate's rear face, the plate needs one opening the size of the device's front. Reuse the Sleeve's flush-window approach (bands above/below, side clearance) rather than inventing a second one.
   - The existing rules still apply (front screw joint ≥ 11.5 mm for flat mounts, plate bands, the 204 mm width limit, rear support). Where a combination can't work, block it with a plain-language reason and say what to change, e.g. "Flush needs the Sleeve mount or a glued joint". Don't let OpenSCAD asserts be the only message.
   - Sleeve is already flush; for Sleeve, "Set back" moves the case back inside the sleeve. Say in the report whether that is supported or blocked, and why.
2. **Bezel** (per-slot setting): **None** (default) / **Chamfer** / **Rounded**, plus a size in mm (name the range; suggested 0.5–1.5 mm, default 1.0).
   - It goes on the **front edge** of the front port openings (`ports`) and of the flush window, sloping outward toward the front face.
   - Not on keystone openings, the rack mounting slots or the plate's outer edge.
   - **Wall check:** a bezel thins the plastic between neighbouring openings and toward the plate edge, the mounting slots and keystones. Name a minimum web, compare it with what `port_openings.problems()` keeps today, and use the larger. Where the bezel would break it, shrink the bezel for that opening (or leave it out) and show a one-line note. Never reject the design for it.
   - **Printing:** find out which face of the plate the app expects to print on the bed, from the docs, export notes or coupon READMEs. Say it in the report. A 45° chamfer on the bed face prints fine. A rounded edge on the bed face makes a near-flat overhang. If Rounded is on the bed face, show a short hint ("Rounded prints best with the front face up; Chamfer prints either way").
   - **Geometry:** keep the render cheap. Chamfer: a tapered cut (e.g. `linear_extrude` with `scale`, or a hull of two offset outlines). Rounded: a few stacked `offset` layers (name the step count). Avoid `minkowski` on the whole plate. Report render-time impact for the OptiPlex 1U and a 1U inserts tray with several ports.
3. **Defaults:** As today + None must give **byte-identical** SCAD source to today for every existing spec and saved slot. Old saved revisions stay unchanged.
4. **UI wording:** "Front position: As today / Flush with faceplate / Set back __ mm" and "Bezel: None / Chamfer / Rounded, __ mm". Add short hints in `tray-placement.js`. Update `asset-manifest.json` hashes for any changed JS.

## Tests

- Defaults: unchanged source for the OptiPlex sleeve, a 1U inserts tray, a flat tray and a 2U plate.
- Flush and Set back give the expected device Y position. The flush window appears only when needed. Blocked combinations give the plain message.
- Bezel: present on port openings and the window, absent on keystones and slots. Shrunk or skipped where the web would be too thin, with the note. The minimum web holds after the bezel.
- Validation of the new fields (allowed values, ranges, unknown values rejected).
- No STL exports.

## May change

`equipment_tray.scad`, `equipment.py`, `port_openings.py`, `port-openings.js`, `tray-placement.js`, `equipment-wizard.js` (tray defaults only), `asset-manifest.json`, `test_*.py`, `js-tests/` (register new tests in `js-tests/run.js`). Nothing else; never data/normal-use, the coupon folders or third-party files.

## Checks and report

Run `run_checks.ps1` before and after. Write `work/codex-tasks/33-front-position-and-bezel-REPORT.md` with:
- files with SHA-256;
- the position rules, limits and blocked combinations;
- the bezel geometry, constants, web rule and print-face finding;
- render times;
- check results;
- open questions.

Claude reviews it with exact renders (mesh closure, bezel present and measured, webs) and shows Brian. A test coupon (with its own ID) only if Brian asks for one.
