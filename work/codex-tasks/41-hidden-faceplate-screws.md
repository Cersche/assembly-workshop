# Task 41 — Hidden faceplate screws for the sleeve mount (opt-in `hidden_joint`)

Status: SPEC (Claude, 2026-10-22). Brian's direction: the screws that hold the faceplate to the tray must be used but NOT SEEN. The tray is always assembled (faceplate + tray) BEFORE equipment goes in, so the joint must be reachable with the tray open. Opt-in. Too early for coupons: no test print is planned, so no test ID is needed yet.

PROPOSED — UNVALIDATED: fit, screw engagement and strength stay UNKNOWN. Use only NEW disposable data, never data/normal-use. No printing, no pushes, no auto-builds. OpenSCAD.exe is the renderer.

## What is visible today
Only the sleeve mount (`device_mount="sleeve"`, `joint="screw"`) shows screws: `faceplate()` cuts 3.4 mm holes through the plate from the front (`m3_clear`, `equipment_tray.scad` ~line 226, positions `sl_joints` x `sl_joint_z`), and the tray takes them in a 4.0 mm wall pilot or, with `insert_bosses`, heat-set inserts in bosses (~lines 272, 349-353). Every other mount (inserts, pegs, clips, straps, flat) already uses the hidden joint: plate rear has two tongues (12 x 7 x 3) plus a 9 mm boss (8 deep) with a blind 4.0 pilot cut from behind; the tray has slots, an 18 x 8 x 5 floor block, a 14 x 3 x 19 upright and guide rails, and an M3 clearance hole through the upright; the screw enters from behind (y = 11.4) and runs forward into the boss. That joint was printed and fits well. It is disabled for sleeves (`!sleeve||rear`) because at x = +/-40 it lands inside the window.

## Goal
New opt-in key `hidden_joint` (boolean, default false). When true (sleeve + `joint="screw"` only) the sleeve's FRONT joint is replaced by the proven tongue/boss/upright joint, moved OUTSIDE the sleeve walls:
- joint centres `hj_x = dev_off_x +/- (sl_half + sl_wall + hj_gap + hj_half)` with `hj_half = 9` (the 18 mm floor block) and `hj_gap = 2`; same Z as today (`tray_z+14`), same tongue/boss/upright/rail dimensions, one joint each side, first U only (as today).
- The front face of the plate has NO screw holes: skip the line-226 holes. The sleeve wall front pilots and the insert-boss geometry are not generated.
- Tray gets wider to hold the joints: half-width = `|dev_off_x| + fp_w/2 + sl_side + sl_wall + hj_gap + 2*hj_half`. The existing hard limit (tray <= 204 mm, `max_tray`) applies and its error message must name the hidden joint and suggest Rotate 90 or switching it off. Roughly: devices up to ~155 mm wide fit; wider ones must fail with the clear message (a wide-device fallback is out of scope for now).
- `hidden_joint` and `insert_bosses` are mutually exclusive (assert in SCAD, Python and JS).
- Rear joints are UNCHANGED: with `rear_support` the rear bracket still uses `joint_x` (+/-40). Note in the report: the front screws are driven from behind BEFORE the rear bracket is attached; a fitted rear bracket plate would block that access. Do not add rear holes.
- Assert in SCAD and Python: boss/upright edges keep at least 3 mm from the rack-slot capsules (x +/-118.26, +/-5 half length, z +/-15.902 about each U centre) and the joint stays inside the plate outline with its 2.5 mm corners.

## Files (mirror how `insert_bosses` was added; grep it for the full list)
`outputs/Mechanical_Design_App/`: `equipment_tray.scad`, `equipment.py` (V2 option list ~lines 66, 95, 334-351 text substitutions, validation ~762, geometry ~867), `tray-placement.js` (KEYS, DEFAULTS, widths ~lines 31/40, `sleeveGeometry`, validation ~99, preview posts ~232, toggle ~381 with the hint "Sleeve + screw joint; hidden screws, strength UNKNOWN"), `port_openings` (sleeve joints), and the tests `test_tray_placement.py`, `test_allocation_tray.py`, `js-tests/sleeve-v2.js`.
Also remove the sleeve-joint keep-out circles when `hidden_joint` is on: `faceplate_color.py` ~lines 176-178 and its mirror in `equipment-wizard.js` openings (AGENTS.md: keep these two in step, and `rack-studio.js clearWindow`). With the flag off, behaviour is unchanged. Do not touch the plate dimensions, golden keystones, `ks_tight`, rack slots or any existing joint geometry numbers.
Legacy safety: generated SCAD and source hashes for every spec WITHOUT `hidden_joint` must stay byte-identical (use the same text-substitution mechanism as `insert_bosses`; prove it by regenerating the sources of the existing library items and a sleeve with/without v2 options and comparing hashes). Old saved revisions stay immutable.

## Acceptance (record all in the report)
1. Existing checks pass: `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1`, plus new tests: option accepted/rejected (non-boolean, non-sleeve, `insert_bosses` combined, too-wide device message), joint x/z numbers, front plate has no through holes beyond the window/keystones/slots.
2. Exact renders on disposable data (a sleeve test spec at ~100 mm and ~150 mm device width, 1U and 2U): faceplate, tray and combined STLs are closed manifolds; plate genus/hole count equals the same plate without screw holes; boss axis x/z equals the tray clearance-hole axis x/z (report the numbers); tray width and clearance to rack slots reported.
3. Same spec with `hidden_joint` false renders to triangle-identical meshes vs. before the change (library items too).
4. Place on tray preview (browser, disposable data): toggle appears for sleeve + screw only, preview shows the joints outside the walls, width error appears for a wide device. Screenshot or read_page evidence.
5. Print in color preview for a hidden-joint plate: no 3.4 mm keep-out circles on the front; other keep-outs unchanged.
6. Report every UNKNOWN (fit, thread engagement of M3 into the 4.0 pilot at this new location, strength, access with a real driver).

Offload nothing else; Claude reviews the report and hashes. Write `work/codex-tasks/41-hidden-faceplate-screws-REPORT.md` with files changed, before/after SHA-256, commands run and results.
