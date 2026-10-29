"""Assemble task-43 report from saved acceptance evidence; no builds or user data."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
pres=json.loads((HERE/'preservation-results.json').read_text(encoding='utf-8'))
measure=json.loads((HERE/'acceptance-measurements.json').read_text(encoding='utf-8'))
export=json.loads((HERE/'final-http-export-verification.json').read_text(encoding='utf-8'))
hash_rows='\n'.join('| '+c['label'].replace('|','/')+' | `'+c['before']+'` | identical |' for c in pres['source_cases'])
mesh_rows='\n'.join('| '+name+' | '+str(p['triangles'])+' | closed; 1 connected solid | 0.500 |' for name,p in measure['CM6B'].items())
text='''# Task 43 — M6 split rails report

2026-10-28. **PROPOSED — UNPRINTED. Digital acceptance passes; physical fit, strength, insert retention and key access remain UNKNOWN.**

## Result and boundaries

Implemented the opt-in generator branch, Python and JavaScript validation, Place on tray switch, explicit joint X/Z controls, three-part preview/export, and three-object 3MF packing. Delivery is `outputs/CM1000_M6_generated_2026-10-28/`: three named STLs, one 3MF, CM6B spec, exact source and README. The delivered parts contain generated primitives and text; there is no imported remix mesh. Keep the delivery private. The comparison HTML embeds licensed CM6A meshes and must remain uncommitted and private.

`git pull` was the first command and fast-forwarded main from a2c9545 to 2825628. App-thread inventory showed no other active Codex editor for this project. The other known checkout had no tracked edits; process inventory showed Claude sessions, so Brian explicitly confirmed **“Yes, those files are free”** before generator editing. No session was interrupted. All edits are in this C: workspace; the D: checkout and its normal-use server were not changed.

No printing, purchases, uploads, automatic builds, commits, pushes or HANDOFF edits. The only builds were explicit task acceptance renders and explicitly clicked exact preview/export. Tests use new scratch data, including a new browser DB and rack at port **8819**. The sole active-data read was a byte copy of `data/normal-use/equipment-library.json`; all library regression evaluation used that copy. There are **nine** library items after the pull, rather than the two mentioned in the older brief; all nine were covered. Pre-existing `work/task37-screenshots/` was left alone.

## Brian's formula correction and coordinate convention

Brian directed: use the shaped pocket and CM6A joint positions; the bounding-box pilot formula is wrong for this case. Consequently **joint X/Z are explicit settings**, `m6_joint_x` / `m6_joint_z`, not calculated from the CM1000 envelope. The general switch has a fixed narrow-fixture default; a different device requires suitable explicit coordinates and a validated pocket. CM6B saves X **[-104.4,+104.4]**, Z **[8.6,35.85]**. The Place on tray window exposes all four positions.

Generator → CM6A frame: **X_A=X_B+127, Y_A=Y_B+4, Z_A=Z_B**. The wizard plate front is Y_B=-4; CM6A front is Y_A=0. Both use the slot bottom as Z=0. CM6B's joints therefore land at **22.6 / 231.4 and 8.6 / 35.85**, with no intended coordinate difference; STL sections agree within far less than 0.1 mm. Small CM6A section deviations come from its tessellated pilot surface.

Envelope dimensions **212.6 × 136 × 38 mm** come from `work/equipment-models/netgear_cm1000/netgear_cm1000.scad`. The generated 16-point transverse pocket is a simplified reconstruction using the reference's narrow end channel and the envelope's maximum dimensions. Its outer end channel is **6.2 mm** high, centred at Z=22.225, corresponding to CM6A sections around X_A=22.6. The stand-in model instead describes an 18.3 mm end thickness. **The saved pocket is not a certified fit to that model or to the real modem.** The reconstruction omits the reference's longitudinal sculpting. This source disagreement and fit UNKNOWN are explicit; no envelope dimension was silently relabelled as a measured device dimension.

## Acceptance results

| Requirement | Result and evidence |
|---|---|
| `run_checks.ps1` | PASS: 228 Python tests, 2 skipped; 244 reported JS tests. `work/m6-rails-43/checks-final-3.log`. Skips are not passes. |
| New setting and validation | PASS: `SplitRailsTests` in `test_m6_joint.py` covers M6 dependency, front opening, keystone, excessive width/rack-slot crowding, insufficient pilot wall, depth, explicit CM6A positions, thickness, ID limits, unsupported combinations, Python/JS agreement, legacy hashes, disconnected solids and three-object layout. |
| Every required legacy source hash | PASS: all 14 before/after UTF-8 `source(clean(spec))` hashes identical, including `m6_joint` and explicit `m6_rails:false`. Full pairs in `work/m6-rails-43/preservation-results.json`; table below. |
| HDT-M6-A geometry | PASS: explicit OpenSCAD.exe renders of generator and a **new scratch copy** of HDT-M6-A with only its two engraved ID statements removed match triangle-for-triangle: faceplate 3,388 triangles; tray 10,836. Current generator source is byte-identical to the rendered regression source. `hdt-regression.json` and four render logs. Original source, STLs, IDs and the documented old sliver issue remain untouched. |
| CM6B exact renders | PASS: OpenSCAD.exe, standard $fn=48, zero nudge. Three closed single solids; component counts independently measured, not inferred from closure. `cm6b-measurements.json`, `acceptance-measurements.json`, cached revision logs. |
| Faceplate intersect rails | PASS: exact STL intersection reports **Current top level object is empty** (OpenSCAD exit 1 is expected for empty output). `intersection.scad` / `intersection.log`. |
| Dimensions / IDs / slots | PASS: STL sections below; all three suffix IDs have 0.500 mm engraved floor surfaces. Exactly four corner rack slots on CM6B's 1U plate, verified by two separated gaps on each corner row and no middle rack slots. |
| Three-object 3MF | PASS: built through `tools/plate_layout_stl.py`; three separate named objects, each at Z=0, with 10 mm separation along layout Y. `layout-verification.json`. No printer/slicer settings. |
| Browser Place on tray | PASS: fresh task DB/rack, port 8819; M6-off hides the split switch, M6-on displays it, split-on displays three sketch parts; exact preview reads **3 parts (faceplate, rail_l, rail_r)**. `browser-m6-off.txt`, `browser-m6-on.txt`, `browser-final-exact.txt` and `.jpg`. Brian approved this fresh browser session. |
| Browser export / final HTTP parity | PASS: explicit browser export completed with three STLs and a 3MF. The final HTTP export after centring the rail IDs matches the delivery's source and all three STLs byte-for-byte and contains a three-object 3MF. `browser-export-verification.json`, `final-http-export-verification.json`, `final-http-export.zip`. Final source SHA-256: **SOURCE_HASH**. |
| Comparison viewer | PASS: regenerated from all six final/reference STLs with `tools/mesh_viewer.py`, `work/mesh-viewer/CM6A_vs_CM6B.html`, six parts / 52,822 triangles. Not committed; embeds licensed reference geometry. |
| Protected files | PASS: 85 historical files, including all CM6A, CM1000 2026-10-16 baseline, HDT-M6-A, specified TL-SG108E output files and HANDOFF, match their post-pull pre-edit SHA-256 values. Only the two intentionally edited generator files differ in the original 87-file manifest. Other TL-SG108E files have no Git changes. |

The pre-edit check suite already failed its rack-BOM JavaScript extractor on Windows CRLF (`window is not defined`). The test-only extractor now accepts `\\r?\\n`, restoring the intended isolation; no rack behaviour changed. The asset manifest stores the updated LF-normalized tray-placement script hash. Existing allocation-key expectations were expanded for the new settings.

The opt-in template block is stripped, including its marker line breaks, for every non-rails source. New rails use marker/text substitutions and a separate dispatch. Legacy M6 hooks are unchanged. Split builds reject undefined OpenSCAD dimensions and disconnected meshes and do not try geometry nudges. Development scratch retains an initial undefined-dimension attempt and a later coplanar-contact attempt, clearly outside the final output. These exposed that a closed mesh can contain multiple solids; the new connected-component check prevents that mistake from exporting. A 0.05 mm rail/stub separation makes exact intersection empty. Current delivery and final acceptance refer only to SOURCE_HASH.

## CM6A versus CM6B measurements

All values are mm. STL sections use the standard-library scripts `measure_reference.py` / `measure_acceptance.py`; raw probe coordinates and material intervals are saved. Measurements are section-specific where indicated, not certification of global physical walls.

| Feature | CM6A reference STL / source | CM6B generated STL | Difference / explanation |
|---|---|---|---|
| Joint X in CM6A frame | 22.6 / 231.4 target; section agrees within ~0.004 | 22.6 / 231.4 | Explicit settings, within 0.1 target. |
| Joint Z | 8.6 / 35.85 | 8.6 / 35.85 | Preserved target, independent of envelope formula. |
| Pilot diameter | ~7.600 (polygonal surface; Z section ~7.59984) | 7.600 | Same nominal bore, tessellation/rounding differences only. |
| Pilot depth from rear surface | 7.000, Y_A=9..16 | 7.000, Y_B=5..12 → Y_A=9..16 | Reference cutter goes to 16.5, but its solid ends at 16; actual depth is 7, not 7.5. |
| Minimum pilot ligament in transverse bore section | 2.03587 at Y_A=12; README states ≥2 | 2.000 at Y_B=8 | New stub has 2 mm planar lateral ligaments. Full extruded new pocket boundary is also checked geometrically; reference section is not a global wall certification. |
| Clearance hole diameter | 6.600 | 6.600 | Equal. |
| Front flange thickness | 4.000, Y_A=16..20 | 4.000, Y_B=12.05..16.05 | +0.05 Y translation after frame transform, giving the explicit joint gap. |
| Flange lateral wall beside clearance | ~2.533 at outside | 2.500 | New rectangular flange follows the 2.5 minimum. |
| Access-bay cutter target | 12 high × 34 deep, Y_A=20..54 | 12 high × 34 deep, Y_A=20.05..54.05 | Target dimensions reproduced with the explicit 0.05 gap. |
| **Actual sampled clear bay height** | **14.3556** (lower 2.6..16.9556, upper 27.4944..41.85), outer-wall X_A=18 / 236 | **12.000** (2.6..14.6 and 29.85..41.85), X_B=-109 / +109 | CM6A already has larger mesh cutouts; new generated bays are exactly the specified cuts. CM6A is more open here; key/head access for CM6B stays UNKNOWN. |
| **Actual sampled clear bay Y length** | **44.6842**, Y_A=20..64.6842 before first surviving web | **34.000**, Y_B=16.05..50.05 | Existing CM6A windows exceed the nominal cutter. No claim that the generated access envelope duplicates those windows. |
| Rail floor/top at bay, planar nominal region | 2.600 / 2.600 at pilot X | 2.575 / 2.575 | Wizard plate/rail bottom is Z=.025 and top 44.425; cuts remain Z=2.6 / 41.85. Both exceed 2.5. At CM6A's rounded outer edge the sampled floor/top are about 2.572, not a global 2.6 minimum. |
| Uncut new rail floor/top | Baseline setting 3.3; shaped/rounded reference varies | 3.300 / 3.300 at X_B=±104.4, Y_B=80 | New setting defaults to baseline 3.3; ID floors leave ≥2.5. IDs need ≥3 mm top stock before their 0.5 cut. |
| Rail length | 121.620, Y_A=16..137.62 | 138.000, Y_B=12.05..150.05 | +16.380 length, per task's **device depth 136 + 2** rule; rear end in CM6A frame is 154.05, +16.43 from reference. Actual rear/rack clearance UNKNOWN. |
| Faceplate height | 44.450, Z=0..44.45 | 44.400, Z=.025..44.425 | Required current wizard standard; no plate dimension constants changed. STL grid error <0.00001. |
| Faceplate width | 254.000 | 252.000 | Existing wizard width retained; CM6B spans X_A=1..253. |
| Rack slot count | 4 corner slots | **4 corner slots** | No empty-middle-post slots added. Generator's existing slot X and Z constants unchanged; reference corner row Z differs by ~0.002 mm. |
| Top-face ID depth | 0.5 by reference source | **0.500 measured on all three parts** | CM6B-F/L/R; rail lettering centred along length, scaled down for short rails / long optional IDs. |

| CM6B part | STL triangles | Integrity | ID depth (mm) |
|---|---:|---|---:|
MESH_ROWS

For the new shape, the polygon, plate and rack-slot checks supplement the STL section: every pilot must be outside the pocket with ≥2 mm ligament; full-height stubs stay at least 2 mm inboard of the inner rack-slot bound. CM6B's outer stub edge is X_B=±110.2 versus the corner slot's inner bound at about ±113.2625: about 3.0625 mm separation. No physical tolerance or installation approval follows.

## Validation and implementation limits

Both Python and JS block rails without M6 (**“Split rails need M6 hardware turned on.”**), opening/keystone in front of a stub, a device too wide for stubs and rack-slot clearance, and rails longer than the selected usable length. They also block insufficient pilot wall/plate-edge space, inadequate bay floor/top/connecting web, crossed or out-of-envelope pocket outlines, invalid IDs and unsupported combinations. X/Z are saved in generator coordinates. `m6_rail_t` defaults to 3.3 and permits 2.5..8; engraved IDs additionally require 3 mm of top stock before engraving so the remaining material is ≥2.5.

Supported split configuration is an unrotated flat device with screw joint, no feet, offset in depth, rear bracket, second device, drive mode, coupon, protrusion keep-clear zones, faceplate labels or bezel. Side offset and openings still undergo validation. The narrow fixture defaults are not general hardware positions; wider/shaped devices need explicit joint and pocket settings. The free-form pocket is currently a library/spec setting; the UI exposes joint positions and thickness, but has no polygon editor. This is a current gap, not new geometry support for every equipment type.

The 240 mm usable-length default is a nominal planning constraint, **not a measured usable depth**. It limits rail length; total end location includes the front stub/flange position. The generated width (~220.4 mm across outside rails) is compared to rack-slot/stub bounds in this opt-in branch, replacing the old full rectangular 204 mm tray-width screen only for rails. Post/body clearance through the actual rack has not been established and stays UNKNOWN. Ordinary legacy trays keep their existing width screen.

## Gaps and every physical UNKNOWN

Not included: light pipes; logo and other multi-colour pieces (future Print in color art or separate work); empty middle post holes or a rear tie-in; sleeves; rear brackets; a second device. The generated parts also omit the remix's longitudinal nose/pocket sculpting, rail scallops and repeated web openings, original rounded contours, and the left case-retention screw slot. There is no newly invented substitute fastener for that slot. Artwork, cable/port accommodation and full visual equivalence are not established. The normal STLs contain no colour/artwork.

UNKNOWN: (1) pocket fit against the remix, stand-in model and real modem, including the 6.2-versus-18.3 mm end-channel disagreement, nose shape, rear shape, orientation, sliding fit, clearance, grip and retention; (2) printed insert OD/length match, installation process, retention, pull-out and splitting; (3) screw/head dimensions beyond nominal, seating, clamp-up across the 0.05 gap, torque, actual engagement (nominal insertion reach is 8−4−.05=3.95 mm), loosening and service life; (4) ability to insert and turn a real 4 mm L-key and seat a Ø10.5 button head in the smaller new bays; (5) rail stiffness, sag, loads, strength, thermal/long-term behaviour and joint strength; (6) actual usable rack depth, post/rail/slot and neighbouring equipment clearance, rear cable space, cable bends and port access; (7) printed dimensional accuracy, material/process effects, wall suitability, ID readability and all manufactured fit. Manufacturer-certified dimensions, strength and generic FDM wall/process guidance remain UNKNOWN. No printing, fitting or load test was authorized or performed, and no printer/slicer integration is required.

## Legacy SHA-256 proof

For each row the full **before** digest below equals the **after** digest; `preservation-results.json` records both explicitly. Inputs are saved in `legacy-before.json`; the failed initial helper-fixture attempt is retained separately and was replaced with valid flat/sleeve/pair fixtures before any generator edit. One built-in example, all nine copied library entries and four dedicated regressions give 14 cases. These tested inputs plus exact marker stripping substantiate preservation; no exhaustive claim over every mathematically possible spec is made from a finite corpus.

| Spec | Before SHA-256 = after SHA-256 | Result |
|---|---|---|
HASH_ROWS

Evidence scripts, scratch caches, closed-mesh sections, final HTTP zip and browser evidence are under `work/m6-rails-43/`. Protected-file hashes and the original clean Git status were captured after the requested pull. No historical cache or saved revision was regenerated in place.
'''
text=text.replace('SOURCE_HASH',export['source_sha256']).replace('MESH_ROWS',mesh_rows).replace('HASH_ROWS',hash_rows)
(ROOT/'work/codex-tasks/43-m6-split-rails-REPORT.md').write_text(text,encoding='utf-8')
print('Wrote task 43 report')
