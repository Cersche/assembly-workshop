# Task 31 · Rear bracket: lips on the inside, denser vents

Do this after task 30 (done). Read the Claude review at the end of `30-rear-bracket-styles-REPORT.md`.

Brian, 2026-10-20, approved both fixes from that review.

1. **Printability:** the `reinforced` and `vents` lips stick out of the bracket's *outer* face, while the bosses and tongues stick out of the *inner* face. With 8 mm features on both faces the bracket can't print flat any more. Today it prints outer face down, with everything else pointing up.
2. **Airflow:** `vents` has only 30 × Ø6 holes (about 850 mm² open) behind the OptiPlex's large rear exhaust grille. The free plate area between rows is unused.

Standing rules in [README.md](README.md) apply. Fit, stiffness, airflow and strength stay UNKNOWN. Printing and exports are not authorized.

## Build

1. **Move the lips to the inner face**, the tray side, Y < 240, for `reinforced` and `vents`. The outer face (Y = 244) must be **completely flat** again.
   - **Top lip:** full width X ±100, the same 2.5 mm thickness and 8 mm depth, along the top edge of the plate (keep the 0.5 mm edge inset).
   - **End lips:** at X ±97.5..100, running from **above the tray floor** (tray floor top + 0.5 mm clearance) up to the top lip.
   - **No bottom lip.** The tray floor runs to Y 240 there.
   - **Clearance (≥ 0.5 mm) from everything the app models behind the plate:**
     - the tray floor (including trays up to the 204 mm limit, whose edges reach X ±102);
     - the tray's rear uprights, tongues and slots, wherever `joint_x` puts them;
     - the bracket's own bosses;
     - the device's maximum rear position (the asserts already keep it ≥ 11.5 mm in front of the rear joint);
     - the rear posts (X ≥ 108, so the lips stay within X ±100).
   - For multi-U plates the top lip goes along the overall top. End lips run the full height above the floor.
   - Name the constants. If a lip would collide in some configuration, shorten or leave out that piece and say so in a one-line note, rather than rejecting the design.
2. **Denser vents** in the `vents` style.
   - Fill the same free rectangles that `reinforced` opens: the upper window area, and the two lower outer areas outside the bosses. Keep the centre cable slot and the 6 mm strip, margins and bands.
   - Use a staggered round-hole or hexagonal-hole pattern (your choice; say why), with **bars no thinner than 2.0 mm**.
   - Aim for **at least 40 % open area** within those rectangles. No partial holes.
   - Name the constants.
   - Report the hole count, the open area in mm² and the % for the OptiPlex 1U, and the render-complexity impact (triangles / facets per hole).
3. **No other style changes.** Solid, open and slots stay byte-identical. Old specs stay unchanged.
4. Update the Place on tray hints if they mention lips. Update asset-manifest.json hashes for any changed JS.

## Tests

- `reinforced` and `vents`: nothing is beyond Y 244 (the outer face is flat), and all lip geometry is on the inner side.
- Lips clear the tray floor, uprights/tongues, bosses and the device envelope by ≥ 0.5 mm. Test the OptiPlex sleeve, a 1U inserts tray, a 204 mm wide flat tray and a 2U plate.
- Vents: bar ≥ 2.0, no partial holes, open area ≥ 40 % of the free rectangles, and the centre slot and keep-outs untouched.
- Solid / open / slots sources and old specs are unchanged.
- No STL exports.

## May change

`equipment_tray.scad`, `equipment.py`, `tray-placement.js` (hints only), `asset-manifest.json`, `test_*.py`, `js-tests/` (register new tests in `js-tests/run.js`). Nothing else; never data/normal-use, the coupon folders or third-party files.

## Checks and report

Run `run_checks.ps1` before and after. Write `work/codex-tasks/31-rear-bracket-lips-and-vents-REPORT.md` with:
- files with SHA-256;
- the lip rule, clearances and constants;
- the vent pattern, hole count, open area and %;
- check results;
- open questions.

Claude reviews it and renders both styles for the OptiPlex (mesh closure, flat outer face, clearances), then shows Brian.
