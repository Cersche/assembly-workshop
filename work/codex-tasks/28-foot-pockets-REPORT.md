# Task 28 report — device foot detection and floor pockets

Implemented foot detection in wizard step 1, selection/editing and manual foot entry, per-slot pocket sketches, and exact-source pocket geometry for flat and sleeve mounts. The detector separates triangle bodies by shared vertices, casts vertical columns per body, merges the solid intervals, then finds the modal main underside and lower connected clusters. The OptiPlex STEP/browser check is still pending; the numbers below are conditional calculations from the 38.8 mm envelope and 2.0 mm feet described in the study, not a claim that this wizard run detected those feet.

## Geometry and OptiPlex calculation

PROPOSED constants: pocket clearance **0.5 mm per side**, extra pocket depth **0.3 mm**, and minimum blind-pocket floor **0.8 mm**. Foot-bearing sleeves use a **3.0 mm top lip**; sleeves without feet keep the previous 1.5 mm lip. A pocket deeper than 2.2 mm in the 3 mm tray floor passes through; the placement warning explains why.

| | Before feet | With 2.0 mm feet kept |
|---|---:|---:|
| Device envelope height | 38.8 mm | 38.8 mm |
| Case height used for the U budget | 38.8 mm | 36.8 mm |
| Sleeve window | 183.5 × 39.1 mm, Z 3.5–42.6 | 183.5 × 37.1 mm, Z 3.2–40.3 |
| Lower / upper plate band | 3.475 / 1.825 mm | 3.175 / 4.125 mm |
| Top lip | 1.5 mm | 3.0 mm; top at Z 43.3, leaving 1.15 mm to the 1U limit |
| Pocket depth | — | 2.3 mm; through the 3 mm floor because a blind pocket would leave 0.7 mm |

The 2 mm shorter window frees height for a 2.3 mm thicker upper band; the 0.3 mm lower-band reduction comes from the pocket-depth allowance at the window bottom. The top lip grows by 1.5 mm and remains below the 1U top. The calculated tray checks at 1U. This design remains PROPOSED; fit, retention and strength are UNKNOWN.

## Detection performance

The registered synthetic test finds four separate overlapping-body feet with the expected footprints and 2 mm height, finds none on a plain case, and verifies a quarter-turn changes the reported device-frame positions. A generated 50,000-triangle synthetic input took **137.3 ms** in the final full check. This is a local synthetic timing, not a timing claim for the OptiPlex STEP or every 50k-triangle topology.

## Verification

- Baseline `run_checks.ps1` passed before edits.
- Final `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1`: **134 Python tests passed; one existing OpenSCAD render test skipped; all 188 JavaScript tests passed**.
- Focused Python runs: `test_port_openings.py` (9 passed) and `test_equipment_placement.py` (7 passed).
- `node --test outputs/Mechanical_Design_App/js-tests/feet.js`: 5 passed, including the 50k-triangle timing.
- `git diff --check` passed. The front-end asset manifest hash check passed in the full suite.
- No OpenSCAD render, STL export, live server, browser session, user-data access, print or third-party file access was performed.

## Open questions and limits

- The pending Claude browser check must confirm whether the imported OptiPlex STEP detects feet after orientation/rotation, and confirm their locations and dimensions. The coordinate values in the bracket study describe grooves; they were not treated as measured coordinates for the imported device feet.
- Exact mesh appearance and OpenSCAD rendering were not verified here. The existing optional render test was skipped by the project check command.
- Physical pocket fit, sleeve fit, retention and strength remain UNKNOWN; printing is not authorized.

## Files and SHA-256

Byte-for-byte before copies of every edited existing file are in `docs/archive/codex/2026-10-20/task28/`. “NEW” means no before file existed.

| File | Before SHA-256 | After SHA-256 |
|---|---|---|
| `outputs/Mechanical_Design_App/equipment-wizard.js` | `31582b5f047d55dab9e4d899176458b30994e64491ea736f84f480a498fdf530` | `ff8acf2af1e925d9ed9a4b156d7a3b0c7d98a4a889eedb0263408903dbfc89be` |
| `outputs/Mechanical_Design_App/tray-placement.js` | `7591e0828a5de09514f30cb5a85dd29a73c8a4f7fe2be2070521ad7ccb1b3ba5` | `3f5fea865f132224968cde0e494a5f06e898a3f2da6c70c4dfa504f9761a542c` |
| `outputs/Mechanical_Design_App/port-openings.js` | `5cc93f646299c084382f9c34cc15e67c7a434f4bc1ea1fb04aae06fb5d640c75` | `19f1a35e1b33798c6cc623eb5ed8b7599e2c373fb569b3dbbd4501f74b8fc2a4` |
| `outputs/Mechanical_Design_App/port_openings.py` | `f85b75efff62f424b121a7ec3319858c83a31e1c3afed7c3c894481d36148c48` | `bf991be21a0efd1ed02f4aca6100fe72902e49f45848a05ea039ed44d306bfc2` |
| `outputs/Mechanical_Design_App/equipment.py` | `a493f7d50b7fcf9701686e77f3ca3cb182c7e6c6b5305e6ef628e926bf659abd` | `52b66c18c1dad2716a275effde76790d0546abaae7444cb0e4b8b18feac91da8` |
| `outputs/Mechanical_Design_App/equipment_tray.scad` | `8afba648cd2537814bf375baffad3705c226b00c5a25a19d01cab4ac4b5676ab` | `e81002845f7419180f1d90c1ccd2adf4554674fc1d99366d80e1a28334ad81ad` |
| `outputs/Mechanical_Design_App/asset-manifest.json` | `2089f52ba8e205963c94e2d3bc8d74d3a8446551a47e8ef3207ceb52575828f2` | `29c19df81d3d776db49b4c3d91428cec22b0e892bfa05e16209cdb7230419e11` |
| `outputs/Mechanical_Design_App/test_port_openings.py` | `4cca9a512da0c068522d5231a6c23c56c05d6c457544b7fef859f7f3d3997451` | `159bbdec6df77d6e71aed736010810d06e59593748f7c19afb70e5c5859e6b58` |
| `outputs/Mechanical_Design_App/test_equipment_placement.py` | `9e3a5aecfd225c38ce6fdec6b723677a1dc35b2276a6f29de1e0805baa2e6279` | `f4dd3146f46a2ce1f9754cb40dda72ccd371e3ba5a79b3420845598afea65151` |
| `outputs/Mechanical_Design_App/js-tests/run.js` | `b0d1c0ec60f8ec34f7448890e9a8b4d2e8f965089774ec12bd347dd49397759f` | `6d2e33a6b09ab1a9e69eeb06fab20be04d9e1629498273890fc18d45eda697f1` |
| `outputs/Mechanical_Design_App/js-tests/feet.js` | NEW | `9d718bb023563ec432ae2ca0b81147847194913d60ee166f5776bf7034b469a5` |

## Claude review (2026-10-20)

- **Bug fixed — case sat 0.3 mm inside the floor.** The device was lowered by foot height plus the 0.3 mm extra pocket depth. So the case bottom (3.2) was below the floor top (3.5), and the sleeve window top equalled the case top (zero top clearance). Now the case rests on the floor top and the feet hang in pockets 0.3 mm deeper than the feet. Fixed in equipment.py, port_openings.py, port-openings.js and equipment_tray.scad (sleeve bottom and the preview box). The two tests that had locked in the wrong numbers were corrected. For 2 mm feet: window 3.5–40.6, needed height 40.3.
- **Claude's own slip, fixed:** a trailing comment I added to the SCAD swallowed `sl_window_top` on the same line. Renders failed while the source tests passed. Added `test_sleeve_scad_assignments_are_not_commented_out`.
- **Checks:** 135 Python (1 skipped), all JS pass.
- **Browser, OptiPlex STEP** (disposable data, X is up + Rotate 90° ×3): **found 4 feet, 5 × 15 mm, 2.8 mm tall**, at X 15 / 163 and Y 26 / 162 from the front-left corner. The case is therefore 36.0 mm, matching Dell's spec. The front pair lines up with the third-party bracket's grooves.
- **Saved as sleeve 1U with rear support; exact preview:**
  - tray, faceplate and rear bracket are each 1 body with 0 open edges;
  - window Z 3.5–39.8, upper plate band **4.6 mm** (was 1.8), lips 3 mm;
  - 4 through pockets, 6 × 16 mm (5 × 16 mm on the right side), at the foot positions;
  - feet bottom at 0.7 mm, above the slot bottom.
- **Small gaps, not fixed:**
  - the wizard's save summary doesn't count feet;
  - `mesh_study.recesses` reports blind grooves but not through holes in a floor.
