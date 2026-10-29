# Task 46 — CM6B rev 3 packaging and rail-top report

2026-10-28. **PROPOSED — UNVALIDATED. Task 46 digital checks PASS; fit, strength and retention UNKNOWN. Slicer behaviour UNTESTED.**

Worked in `D:\Projects\assembly-workshop`, after reading AGENTS.md/PROJECT.md/HANDOFF.md/ROADMAP.md and a successful direct `git pull` (already up to date). Other Codex sessions were idle; Brian explicitly confirmed that no other session was editing the five shared generator files before edits began. No desktop-control session or subagents. HANDOFF.md was not changed. No commit, push, printing, purchases, automatic builds, server start or user-data writes. All explicit render/regression inputs and evidence are new disposable task-46 files; data/normal-use was not used.

## 3MF structure and placement

`print_layout.layout_3mf` selects the new component path only when rail parts and `pipe_` or `vector_` colour parts coexist. Vector-only colour builds are covered too. The original path and `place()` are unchanged for all other builds. All m6_rails colour builds use the same new path; no hardware-specific mesh imports or CM1000-specific packing branch.

Inspected CM6A's actual package: three entries (content types, relationships, model), three component-parent build items; 15 mesh children for the faceplate and one child per rail. **No slicer config/part metadata and no materials** exist in that reference. Rev 3 copies its hierarchy and adds standard 3MF base-material properties, one independently assignable property per colour part, preserving the prior body/dark and colour/white display intent. These are material hints, not tested slicer filament-spool settings.

Actual rev 3 tree (`unit="millimeter"`):

```
build item 16: faceplate assembly
  1: faceplate body                 material 1000/0
  2..6: pipe_1..pipe_5              material 1000/1..5
  7..13: vector_1..vector_7 letters material 1000/6..12
  14..15: vector_8..vector_9 details material 1000/13..14
build item 18: rail L
  17: rail_l                       material 1000/0
build item 20: rail R
  19: rail_r                       material 1000/0
```

Thus 20 resource objects (17 mesh resources + 3 parents), **3 build items**, and **no colour mesh directly in build**. All child transforms are identity; meshes already contain their common print placement. The faceplate rotation/translation is `(x, -z + plate_dy, y - plate_z)`; it is shared by all colour meshes. No colour mesh is independently lowered onto the bed. All 17 meshes in the package equal their expected placed STL triangle coordinates after 6-decimal encoding (≤0.0000005 mm coordinate rounding, below 0.001 mm). The permanent synthetic test independently calculates the transform for 14 distinct placements, verifies all 15 children, checks 14 distinct material indices, three parents/build items, and the vector-only case. This replaces the previous shallow colour-object counting assertion; dated task-44 scripts/evidence remain historical.

Rebuilt the delivery and copied it to `outputs/Final_3MF/CM6B_CM1000_generated_split_rails.3mf`. Exact bytes match; SHA-256 **40c22e6198d4295cc73129f8e101d064b132e7be0272d5fffc7dbe44b2543b69**. The Final_3MF README row explicitly says rev 3, packaging + rail-top fix. No Bambu/Orca or other slicer was opened. **Import, unit prompts and slicer-specific filament mapping are UNTESTED**; structural validation is not a slicer-import claim.

## Rail stripes: cause, correction, measurements

`m6_edge_radius` was already **0**. This was not stepped rounding and not a bay reaching the top. The measured right side silhouette had captured a cross-section of CM6A's original engraved letters: repeated steps down to **Z=43.95** at Y≈81.4933..101.357. `mf_side` extruded those silhouette steps through the whole width, producing parallel grooves in addition to CM6B's separately engraved ID. CM6A instead has local letter-shaped cuts and a flat surrounding top. CM6A's centre strip measured constant Z=44.450000 over the corresponding longitudinal range.

Corrected only the numeric **outer top outline** in CM6B_spec.json, then regenerated its source with the existing primitive generator. Removed the captured letter notches and made the two outer top edges horizontal at **Z=44.425** (the existing CM6B top datum). No new smoothing offset or rounding operation was added. X/Z profile edge facets remain; CM6B's own ID text is still engraved by `mr_id` with its original settings. All inner-window loops and all other spec keys are exact-equal to rev 2.

| Change / measurement (generator coordinates, mm) | Left | Right |
|---|---:|---:|
| Old top-strip range around ID | 44.421000..44.421000 | 43.950000..44.421500 |
| New top-strip range | 44.425000..44.425000 | 44.425000..44.425000 |
| Measured new flatness (max Z−min Z) | **0.000000** | **0.000000** |
| Samples per rail | 332 | 332 |
| Maximum ordinary outline-top lift | 0.004050 | 0.003980 at the rear top endpoint (front 0.003090) |
| Added height at erroneous groove bottoms | none | **0.475000** |
| Maximum sampled fit-feature boundary change below Z43.9 | **0.000000** | **0.000000** |
| Actual longitudinal bounds, unchanged | 12.05..133.62 | 12.05..133.62 |
| Actual rail length, unchanged | 121.570000 | 121.570000 |

Flatness samples: Y=64.123..105.123 at 0.5 mm spacing; X offsets −3.8, −2.4, +2.4, +3.8 from each joint centre ±104.4. These flank the intentional 3 mm lettering; rounded edge transitions and engraved text are excluded. Values are measured from triangles, reported to 0.000001 mm; this is digital surface flatness at the sampled patches, not manufactured flatness.

Every outline change is above **Z43.90662**. The top of the rear chamfer meets the corrected datum; its low endpoint is unchanged, with at most 0.00405 mm top adjustment. No X coordinate, rail endpoint, bay/window contour, retention-slot value, screw/pilot diameter/centre, nose loft, bridge, or pocket profile was edited. For each rail, 190 independent X/Y/Z axis probes compare material-interval boundaries below Z43.9: **0.000000 mm** difference. These cover front joints, bays, pocket/web regions, retention region and rear; 380 total probes. Rail bounding boxes are exact-equal before/after. This is below the 0.05 mm fit-feature limit, with unchanged source geometry providing the stronger preservation evidence; unmeasured global surface fidelity to CM6A is not claimed. The deliberately filled cosmetic grooves change by 0.475 mm and are explicitly not classified as fit features.

The prior CM6B/CM6A pocket discrepancy remains (worst task-44 sampled boundary difference 2.015540 mm, with other section/ray differences documented there). This task does not reclassify those results or transfer CM6A/printed-baseline fit evidence.

## Tests, rebuilt parts and preservation

- **run_checks.ps1 PASS:** 234 Python tests reported, 2 skipped; **244 JavaScript tests**, all passed. The two skipped render suites remain skips. New component/position/material and rail-top tests run in this suite; it starts no build. `checks.log`.
- **Explicit OpenSCAD.exe rebuild PASS:** all 17 CM6B STLs render; exact undirected-edge counts show closure and each has one connected component. Faceplate/14 colour meshes are triangle-identical to rev 2. Rails contain 3,000 / 2,960 triangles. Rebuilt source is self-contained numeric primitive code; no remix mesh imports.
- **All 14 legacy SHA-256 source cases PASS**, including explicit `m6_rails=False`. Before/after digests are listed below and in acceptance.json.
- **No-colour packaging PASS:** HDT-M6-A and the ordinary `flat` tray use the unchanged packer branch. Old/new packers receive identical actual STL fixtures and the same ZIP clock: resulting 3MF bytes and laid-out STL bytes are exactly equal. Fresh before/after source bytes are equal; independently rendered geometry is triangle-identical for both fixtures. Raw fresh OpenSCAD ASCII STL bytes differ because facet ordering varies across processes; no claim of independently rendered raw ASCII byte identity is made. ZIP timestamps are frozen at 2026-10-28 12:00:00 for this comparison only, since otherwise identical ZIPs encode different run times. Existing protected delivered HDT STLs/3MFs remain byte-identical to the starting files.
- **HDT-M6-A triangle proof PASS:** fresh generated faceplate/tray match the preserved task-44 ID-free reference renders triangle-for-triangle (3,388 / 10,836 triangles). Only the reference's ID is excluded, as in the established comparison. Original approved source/mesh files remain unchanged. The historical HDT sliver-edge limitation is not fixed or reclassified.
- **Protected files PASS:** all **110 starting SHA-256 snapshots** unchanged, including CM6A, 2026-10-16 CM1000 baseline, HDT-M6-A, SG8 and HP4 output directories, other Final_3MF entries and HANDOFF.md. Additional audit covers 40 tracked SG8/HP4/switch-baseline files: exact starting snapshots where available, otherwise clean-start Git blob equality with checkout line endings normalized. m6_rails.py, m6_fidelity.py, equipment.py and equipment_tray.scad are byte-identical to their task-46 snapshots. Only print_layout.py and test_m6_joint.py changed in app source. No live server was used or restarted.

The primary no-colour output SHA-256 values (both old/new packers):

| Case | 3MF SHA-256 | Layout STL SHA-256 |
|---|---|---|
| HDT-M6-A | `f76a79d9b5f043ab3ecbf09a10a8f3a015afb5a6f1fb4b5552964d24c9447cd4` | `263ac1769ef3b6c8d8633ea09e07b74bebd8d8524d9a0b03bad787125d80a349` |
| flat | `23c258c9882cb976d7f30a5a756a4339d54de8aae18d5d52e234005c769a3247` | `24f1de5d39bdc64fd85e490ca0dbaadf6ca5621fe7c326be691e4fb05d1dc10c` |

Legacy source before = after = explicit-false:

| Case | SHA-256 |
|---|---|
| example-0-Raspberry Pi 4 (example) | `fe6bff2a485ce7814614000a90da9c6679509ed8b4b69dd5d6dac30023f6baec` |
| library-copy-0-Raspberry Pi 4 (example) | `fe6bff2a485ce7814614000a90da9c6679509ed8b4b69dd5d6dac30023f6baec` |
| library-copy-1-Dell OptiPlex Micro 7010 (sleeve) | `fcb9dff6521aaa19ec3753e7781fd80968556b0f70d6663181bfcef44be751e3` |
| library-copy-2-Drive tray (3.5" HDD + 2.5" SSD) | `3297879222e50ed29b4a51dcc9ea8518a326ef2e217f4fc07f27b30240562a4e` |
| library-copy-3-7" touch screen plate (placeholder) | `2046c1b868b97fee6086d32a6624dffc2ccdf1685b9c15af4d2708fa05a25745` |
| library-copy-4-Keystone panel, 10 (3 USB, 4 LAN, 3 blank) | `2a641ad48c0a91ea8649abebe33a2d6b3ce556039f36bb23b2d3af4d4b173635` |
| library-copy-5-TP-Link TL-SG108E | `8252da3ca3388b62cc2033c067866604e6f9efb072810d4c19ac83ae31beb26b` |
| library-copy-6-Modem ECB7250 (placeholder) | `733df8f95e2d357cfd9848858db6b9c3e20abf346619d0150108599493efdb77` |
| library-copy-7-Netgear CM1000 (bracket: faceplate + rails v2) | `37de9848c08753bdc88d624a3c0615aa66412defb78c942c9b0f053d4fbef9f8` |
| library-copy-8-Philips Hue Bridge + Raspberry Pi 4 (keystone) | `a9d706913e20e313aed44020250df824b77606ae60d526ad1b1e7491b9d9485d` |
| HDT-M6-A | `5c95b78d4e34bc1214a90c1211bd29aafa9ab146d777f32b6ffa094b67e3e117` |
| flat | `0af470dbcf9c5329c5d357f95f637ac9d600c31ff8f2198cf55c833f31aac456` |
| sleeve | `bb538705be18bedcda86387540f93509ae2192adaf492992abc5b28f369a5113` |
| two-device-pair | `fda9389e0f7d4113f432a783aac5f9a54cd9159aff34d23ea8e27aa2a6c8564c` |

## Every remaining UNKNOWN and limitation

- **Physical fit, strength and retention remain UNKNOWN**, including pocket sliding clearance/grip, nose/rear seating, heavy-device support, rail sag, joint strength, security, thermal behaviour, fatigue and service life. No new CM6B specimen has been printed/tested. Earlier fit reports do not transfer.
- Prior pocket and through-width fidelity gaps remain; complete shape-change station coverage, unsampled surfaces, global Hausdorff maximum and exact analytic rounding are UNKNOWN. Sampled section fidelity is not whole-surface approval. Bay skins retain their earlier sampled support; generic global normal-wall minima remain UNKNOWN.
- Retention-slot fastener type, size/head, engagement and function remain UNKNOWN. The slot centre/size is unchanged, not physically certified.
- Insert measured OD/length/bore compatibility, usable depth, installation process, pull-out/retention/splitting remain UNKNOWN. Ø7.6 is Brian's selected rack-post pilot, not a certified maximum insert diameter or thread engagement.
- Actual screw/head dimensions beyond nominal, seating, clamp-up over the 0.05 separation, torque, reach/engagement, loosening, assembly sequence and installation/service access remain UNKNOWN. Nominal M6 x 8 reach is not physical evidence. Real 4 mm L-key access/turning space and head seating remain UNKNOWN.
- Actual usable rack depth, post/slot/neighbour fit, rear-end clearance, cable bend/port access and colour accommodation remain UNKNOWN; the planning depth setting is not a measured rack approval.
- Material/process effects, dimensional accuracy, wall suitability, printability, ID readability, inlay adhesion/fit/colour outcome, light transmission and manufacture remain UNKNOWN. Flat pipe rears, absent original symbols and prior simplified vector/detail geometry remain deliberate earlier simplifications. No generic wall/process/load guidance, manufacturer certification or blanket installation approval is inferred.
- Slicer import, the prior unit-warning symptom and per-part filament mapping in Bambu/Orca are **UNTESTED**. The package has standard component/material properties; actual slicer handling has not been observed. No printer/slicer integration or settings were added.

## Evidence, viewer and delivery

New disposable evidence: `work/cm6b-46/` (before snapshot, build.py, verify.py, verify_regression.py, regression.py, render logs, checks.log, acceptance.json, regression-proof.json, protected manifests and outline-changes.json). `validation/task46/` copies the current compact proof files; previous validation files are preserved as historical task-44 evidence. Rebuilt 17 STLs, source/spec, 3MF and README in the requested CM6B output directory; only its new 3MF and row were changed in Final_3MF.

Required viewer built with `python tools/mesh_viewer.py <all 17 CM6B STLs> -o work/mesh-viewer/CM6B_rev3.html -t "CM6B rev 3"`; 38,992 triangles. Also built task46-reference-regression.html for examined reference/regression meshes. These are uncommitted local previews. SendUserFile is unavailable in this session; the viewer was queued with open_in_codex and supplied as a local link, without claiming a SendUserFile render or visual/slicer inspection.
