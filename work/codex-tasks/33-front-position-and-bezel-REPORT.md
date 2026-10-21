# Task 33 report — 2026-10-20

Completed after task 32. Added per-slot Front position and Bezel controls, validation, conditional front windows, bounded bevel geometry, hints and regression coverage. No normal-use/historical user data, immutable revisions, coupons, third-party assets or live server were changed. No STL exports, printing, installs, uploads, commits or pushes. Stopping after task 33. Existing user edits to the queue README and other untracked work were left alone. The task's explicit May change list was followed; HANDOFF/ROADMAP were not edited.

## Position rules

Saved per-slot fields: `front_position` = `today` / `flush` / `setback`, `front_setback` = 0–100 mm, measured from the outside front face. Default amount 16 mm, active only for Set back. As today preserves the original mount-specific placement. Flush gives device Y=-4 mm. Set back gives Y=-4+amount. Geometry, foot pockets, holes, rear clearances and keep-clear zones use that position. Rotation still uses the existing oriented footprint convention. Fields join equipment.PLACEMENT_KEYS and JS KEYS, validated by placement_settings/clean and included in allocation diffs. Default As today + None does not add source text or alter source bytes.

A device front at or ahead of the plate rear face (Y<=0) gets the existing Sleeve-style rectangular front window: 0.5 mm side clearance, 0.3 mm top clearance, band checks >=1.5 mm above/below, device-height/lift positioning. Front ports wholly inside it are omitted and crossing ports block, as for Sleeve. The normal 204 mm tray width limit remains. Live sketches show the window; the optional exact render shows Bezel.

Blocked combinations have messages before Apply/Save/render, and again in Python:

- Non-Sleeve with screw joint and Y<11.5 mm: choose Sleeve, a single printed piece joint, or at least 15.5 mm Set back. This conservative joint envelope protects near-front arrangements.
- Flat corner stops need Y>=6.2 mm (at least 10.2 mm Set back), plus the existing 11.5 mm front screw-joint rule where applicable.
- Clip support ledges need Y>=1 mm (at least 5 mm Set back), or Sleeve.
- For inserts/pegs entering the plate, each rotated mounting-hole centre must remain at least 5 mm inside the floor; move the hole back, increase Set back or choose Sleeve.
- Window bands that cannot fit: choose more U or lower the device.
- Existing rear-support depth, single-piece restriction, pockets, keystone collar and joint rules still apply.

**Sleeve Set back greater than zero is blocked.** Its side-wall joint heights/front strap layout and flush access were designed together; moving the case back without redesigning that geometry is not offered here. As today, Flush and Set back 0 remain flush. The plain message explains how to proceed. Vertical moves/rotation retain their prior opening limitations. Dragging in non-default front-position modes changes X only, so the explicit front-position amount remains authoritative.

## Bezel geometry and web rules

Fields: `bezel` = `none` / `chamfer` / `rounded`, default None; `bezel_size` = 0.5–1.5 mm, default 1.0 mm. Unknown enum values, out-of-range/non-finite sizes and boolean numeric values are rejected. Bezel applies only to the front edges of front ports and the case window. Keystone cuts, rack slots, plate outline and rear-bracket geometry are unchanged.

Optional source text cuts from the front Y=-4 face inward by the selected size. Chamfer hulls two thin offset outlines for a 45-degree taper. Rounded uses eight short hulls between offset outlines sampled on a circular profile. Slice overlap 0.02 mm prevents coplanar gaps. No whole-plate minkowski; the original SCAD template file itself remains byte-for-byte unchanged. Generated geometry is conditional so existing source identities remain stable.

Minimum web is **2.0 mm**, the larger of the proposed 2 mm minimum and existing port_openings.problems() top/bottom allowance (2 mm; it has no pairwise web rule and permits lateral edges up to the outline). Conservative axis-aligned boxes account for plate edges, every rack-slot envelope, keystone collar keep-outs, neighbouring front openings/window and Sleeve joint screw holes. Neighbours each receive at most half the available gap after reserving the web. Sizes are rounded down to 0.001 mm and reduced to zero if necessary; a one-line warning names the reduction/omission. The base opening is never changed or rejected for Bezel. If an existing base gap is already below 2 mm, Bezel is omitted rather than claiming to repair that gap.

**OptiPlex-size Sleeve with screw joints:** the window-to-joint-hole gap is already only about 1.3 mm, so a full-window bezel is omitted. This is visible in warnings and source comments. A Sleeve single-piece window or the new inserts flush window can receive a bezel when the budget allows it. These are digital rules, not physical approval.

## Print-face finding

`outputs/Physical_Test_Coupons_2026-10-20_SLV-A/README.md`, table and printing instructions (lines 28 and 76), specifies the plate flat with its **front face up**. That is the recovered applicable guidance, not an assumption of front face on the bed. The UI still includes the helpful conditional-orientation advice: “Rounded prints best with the front face up; Chamfer prints either way”. Nothing was printed.

## Checks and commands actually run

- Task 33 baseline: the task-32 final run of `powershell -NoProfile -ExecutionPolicy Bypass -File outputs/Mechanical_Design_App/run_checks.ps1` passed immediately before task-33 edits (150 Python, 1 skipped; all JS).
- Same command after changes: initial test failures from floating-point source formatting and a test expecting Bezel on an intentionally skipped Sleeve screw-joint window were corrected. Final `docs/archive/codex/2026-10-20/task33/check-complete.log`: **155 Python, 1 skipped; 204 JavaScript tests passed; RESULT all checks passed**. The skipped test is the existing opt-in STL render test. New checks cover four old default sources byte-for-byte (OptiPlex-size Sleeve, inserts with port, flat, 2U), device Y/window activation, plain blocked combinations, allocation round-trip, field validation, bezel webs/reduction/omission and unchanged keystone/rear geometry. JS executes the wizard transition/Save guards and actual case-origin rebasing.
- `C:/Program Files/Python310/python.exe -B outputs/Mechanical_Design_App/test_front_geometry.py`: manual image-only OpenSCAD benchmark, never auto-run by checks. First run used temporary sandbox storage (6 PNG renders succeeded; images unavailable to later tools after sandbox lifetime ended). Repeated with `AW_PREVIEW_DIR=C:/Users/brian/.codex/visualizations/2026/10/21/01a15c36-3f51-70d3-8ea6-73cec89386ac/task33-previews` for visible evidence, plus new-window and rear-opening coverage. Ten image renders succeeded, no OpenSCAD errors. Used documented OpenSCAD.exe, `--render --autocenter --viewall --imgsize=1000,600 --camera=140,-350,200,0,-2,22`, selected part faceplate or rear_bracket, PNG output. No STL output/build/export API was called. Visually inspected four-port Chamfer/Rounded, new flush-window Rounded and keep-clear rear-bracket PNGs with view_image.
- `git status --short` / `git diff --stat` / scoped source reads were used to check scope. A session-start git pull was already handled under task 32. No desktop-control session was started.

### Image-render wall time (seconds, full faceplate)

| Dimension-only specimen | None | Chamfer | Rounded |
| --- | ---: | ---: | ---: |
| OptiPlex-size 1U Sleeve, screw joint | 2.093 | 1.987 | 1.987 |
| Synthetic 1U inserts tray, four 14x8 mm ports | 3.195 | 7.775 | 27.563 |
| New flush window, inserts/single joint | 0.839 | 1.161 | 1.535 |

OptiPlex-size fixture is 182.5 x 194.5 x 36.8 mm without feet, not Brian's saved equipment. Its Bezel is omitted by the web check, so its timings do not measure a new bevel. Four-port Chamfer adds about 4.6 seconds; Rounded about 24.4 seconds (roughly 2.4x/8.6x total time). These are single-run local PNG/CGAL timings including launch/image work, not mesh-export timings or guarantees. Solid rear bracket with a confirmed keep-clear cut: 3.897 seconds. The source and images remain in the disposable visualization folder; no delivery package was made.

## Review limits / open questions

Claude's specified browser review on disposable data, actual SG108 review, exact mesh closure/measurement and real fit/appearance/strength remain pending/UNKNOWN. PNG CGAL renders demonstrate that the source renders and show the feature; they do not establish mesh closure or physical approval. Rounded is visibly more expensive with several ports. Sleeve set-back is explicitly unsupported and the current Sleeve screw-joint window often cannot receive a bezel without changing its established hole/web layout. Existing base webs under 2 mm remain as they were; warnings do not silently mark them safe. No further task started.

## SHA-256 (raw file bytes)

Before files preserved byte-for-byte in docs/archive/codex/2026-10-20/task33/. Files below are task-33 changes; task-32-only wizard/protrusion tests are recorded in task 32's report. Shared files here include the final combined implementation.

| App-relative file | Before | After |
| --- | --- | --- |
| `equipment.py` | 13ccc58b1b9731d99a8217aed467b43a9004c6d1dbdae66b9a418d7c808de7e3 | e0197ce284fe4dce0683378eeb9df396d39e7effdfea8aa0091188af95e9f6ef |
| `port_openings.py` | 97d2f820cdfcaec775ad1e510ce8e7f1145aabcf98f284dcd9e0cfb719dc4e9b | cd9dbc1454c4fd30ff0711dd590b39d07aba438ab116790299bdd71b6be92a7d |
| `port-openings.js` | a693f28a3f373385c99ae25f7613169fe93cad975813eec7d64d7f78a59d7af1 | ab8e861b3c99095edca19147b722eeadf37fceff771d3d12f7d429bd82ad084f |
| `tray-placement.js` | 25a30337fb4521f437f9028b9390c084da90968a9e9b6caf9a2717382b5a6fb4 | 655d256f658f257079b487938c3e4704340caf956d019968337852bb7bcae6e4 |
| `asset-manifest.json` | 221b973798bf27933c0db1bf148846a40b1fce070096942d70ce73923da1f04e | 03a69a85b52559cb2ae2baccce089d60317f3275a3e8c00b78f1a26ce8e8bf6a |
| `test_port_openings.py` | b81193d81e5cf2a668ec6d6e83266478f49ea3b94c0f898aeba8c36440db9b98 | 2daba4327331f23409f756585756fbfe1802a75775db36a21ef6c4a57b28cd43 |
| `test_allocation_tray.py` | d54ea5bc264bc4a660ac1d2fc9a7a17457fca4134e159be20128c208dc7576ef | 0ad782d37ce94e914d124f40a0094d3a39f0b6927d74bd262907e22cce10763e |
| `js-tests/run.js` | f1853bb30607cbfed2116703fa557637e7d432e179094e2c5ec9ce485080bf04 | 651c031fefb47b3d4f5ed6fe013109f3e1ac1c4247c5a9f96c8b303848af7b07 |
| `js-tests/front-position-bezel.js` | NEW | f1505e87a0afa06c0a2a879bd2c9d78a31d3f3f7e4b4df8a86df6b9887bcb6d0 |
| `test_front_geometry.py` | NEW | a064826853cca51178d62d41809428f5f55fc7933ded0d8a1da00f8419783ac7 |

## Claude review — 2026-10-20

**Verdict: accepted.** Geometry lives in `equipment.template_source()` as conditional text added to the unchanged `equipment_tray.scad`. The five anchors it replaces each occur exactly once in the template, and the defaults add nothing (byte-identical, see task 32 review). Sound, but a future template edit to those lines would silently drop the feature, so keep the source tests.

- **Checks:** 155 Python (1 skipped) + 204 JS pass.
- **Exact renders** (OpenSCAD.exe `--render`, STL to Claude's scratchpad only, never the repo): 18 faceplate/tray/bracket meshes are all closed (0 bad edges, 1 body).
  - **Disposable OptiPlex 7010 sleeve (1U, 4 feet):** As today/Flush gives the same faceplate. Chamfer with the screw joint is omitted with a note (the existing web is 1.3 mm). The single-piece joint gets Rounded 1.0 mm on the window, with a 2.48 mm bottom band at the front face. Set back on Sleeve is blocked with the plain message.
  - **1U inserts, four 14 × 8 ports + keystone:** Set back 20 gives device Y 16. Chamfer 1.5 measures 1.49 / 1.00 / 0.75 mm wider at depths 0.01 / 0.5 / 0.75 mm, a true 45°. Rounded 1.5 measures 0.389 mm at 0.5 mm depth (8-step arc; the ideal is 0.382). Ports 4.5 mm apart are reduced to 1.25 mm each and keep a 2.002 mm web.
  - **Flush window** (single joint): 141 × 16.3 mm behind the bezel, 1 mm larger at the front.
  - **Keystones, rack slots and plate outline:** identical to the baseline at every section. From Y −2 back, the plate is identical to the no-bezel plate.
  - Render times are in line with the report: four-port Chamfer 11 s, Rounded 32 s, None 7 s.
- **Browser (SG108, flat mount):** Flush shows the plain "needs the Sleeve mount or a single printed piece joint" and corner-stop reasons, and Apply is disabled. Set back 70 mm is accepted; the Bezel chips, size field and print hint show. The flat corner-stop line appears twice (task 34).
- Looks after printing, fit and strength stay UNKNOWN. No coupon was made; one needs Brian's request and its own ID.
