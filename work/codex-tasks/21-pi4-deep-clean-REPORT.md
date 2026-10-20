# Task 21 — deep-clean REPORT

Completed 2026-10-19. Source changes and disposable checks complete; live app not restarted. Physical fit, strength, retention and printed color result remain UNKNOWN.

## Result

- Removed the supported-baseline card, special create flow, fallback names, inspection labels, reset/ports/artwork wording and implicit equipment defaults from the active UI. New placements use the explicitly chosen library id and generic geometry id. New assembly snapshots copy hardware pins/inputs without copying historical reference metadata.
- Added one saved bundled example record in `outputs/Mechanical_Design_App/equipment-examples.json`. Its dimensions are 85 × 56 × 20 mm, mounting holes use 58 × 49 mm pitch, and its nine measured connectors are generic planning ports. It is not selected on startup and uses `equipment_tray.scad`. Library reads expose it without writing user data or building geometry. Unrendered equipment shows an explicitly labeled generic box sketch.
- Isolated legacy equipment-id recognition in `equipment_migration.py`. Loading a saved legacy rack preserves the original bytes in `rack-history/<generation>.json`, returns a converted draft with `migration_pending`, and makes Save available without saving automatically. Assembly ids/revisions, hardware snapshots, inputs, reference metadata, appearance/artwork and port overrides remain preserved. Multi-U connector coordinates are translated to keep their old world positions when switching from top-U to bottom-U preview origins. Saved geometry changes to the generic adapter; old physical fit does not transfer.
- Archived the dedicated source, validation, baseline viewer meshes/evidence and obsolete GUI backup after hash verification. Mixed modules retain shared mesh/hardware logic and their generic tests; their removed historical sections/tests are preserved in the archive and complete source checkpoint.
- The protected `rack-references/` tree was not edited. New active root `rack-studio.js` / `assembly-studio.js` use generic identifiers and remove the old default equipment geometry; the equipment painter provides per-item meshes/sketches. Actual source rack meshes are still used. `index.html` loads these root modules. The existing reference manifest remains valid and unchanged; the new root `asset-manifest.json` covers every root front-end file and is tested.
- Print in color remains gated with “not available for this faceplate yet.” Inspection found a real geometry dependency: `FRONT_Y=-3`, a fixed 216 × 34 mm artwork window at Z=21, and a direct `faceplate()` call. Current generic plates use a 4 mm front, variable U heights and openings. Simply removing an equipment-id gate would not be correct. Saved artwork/filament settings stay intact; generic artwork remains preview-only. No artwork-to-STL expansion or color export was run.

## Verification actually run

| Command | Result |
| --- | --- |
| `powershell -ExecutionPolicy Bypass -File outputs/Mechanical_Design_App/run_checks.ps1` before editing | Exit 0: 111 Python tests run, 1 existing render test skipped; 164 JavaScript tests passed. |
| `node outputs/Mechanical_Design_App/js-tests/run.js` before editing | Exit 0: 26 passed. |
| Same main check command during editing | First two runs failed on retired fixtures/library overlay handling; corrected. The next three runs passed. Final log: `docs/archive/pi4-retired-20261019/checks-final-record.log`. |
| Same main check command after final changes | Exit 0: 113 Python tests run (112 passed, 1 existing render test skipped); all 166 JavaScript tests passed. |
| Same standalone Node command after editing | Exit 0: 29 passed; `js-final.log`. Earlier intermediate standalone run: 28 passed before the behavioral new-placement test was added. |
| `& 'C:/Program Files/Python310/python.exe' -B -m unittest -v test_equipment_examples` from app directory | First attempt failed with sandbox WinError 5 at the temporary render-cache rename. Approved rerun outside sandbox passed 1 test in 6.833 s: generic tray and faceplate render, exact source match, closed/finite/nondegenerate/positive-volume meshes. Fresh disposable data only; no export. Current source digest still matches that tested source. |
| `& 'C:/Program Files/Python310/python.exe' -B -m unittest -v test_mesh_integrity test_catalog_phase6 test_installation_evidence` from app directory | Exit 0: 12 shared mesh/catalog/evidence tests passed. These are existing historical module names. |

Added checks cover a synthetic copy of the documented v2 saved shape (no real normal-use folder access), exact recovery bytes, migration idempotence and explicit Save, history-conflict rejection without overwrite, generic example placement checks/planning-only ports, first-run wording, chosen-item placement behavior, omission of historical reference metadata from new snapshots, and root asset hashes.

Other commands were targeted `Get-Content`, `Get-ChildItem`, `rg` and `git diff --stat` reads, plus UTF-8 Python editing/hash/inventory scripts and patches. The first search used an overly narrow data-exclusion glob and returned text from the preserved app-local historical data; it made no changes. Subsequent source counts/inventories explicitly excluded data/cache directories. Official `data/normal-use` was never read or written. One final diagnostic print hit Windows stdout encoding while printing a checkmark; the files and test results were already written correctly.

No server was started/stopped, no desktop-control session opened, no production render/export run, and no commit, push, install, print, upload, release or deployment performed. Unrelated working-tree changes shown by Git were not attributed to this task.

## Match counts and every remaining source match

Case-insensitive matching lines for `pi ?_?4|raspberry`: **117 lines / 35 files before → 11 lines / 6 files after**. Same inventory scope: top-level app text/source files plus `js-tests/`, extensions `.py/.js/.json/.html/.css/.scad/.md/.ps1/.bat`, excluding `pi_reference.json`. This deliberately excludes user data, caches, catalog packs, protected reference trees and the external archive. It does not claim those preserved histories contain no mentions. `before-matches.json` and `after-matches.json` retain the inventories.

| Remaining location | Why retained |
| --- | --- |
| `outputs/Mechanical_Design_App/equipment-examples.json:4` | The single requested saved example: display name and spec name of the same record. |
| `outputs/Mechanical_Design_App/equipment-examples.json:7` | The single requested saved example: display name and spec name of the same record. |
| `outputs/Mechanical_Design_App/equipment_migration.py:22` | Legacy id recognition, isolated inside migration only. |
| `outputs/Mechanical_Design_App/equipment_tray.scad:2` | Unchanged shared-template historical comments. The task allows template edits only if the example needs them; it did not. No dedicated code branch remains. |
| `outputs/Mechanical_Design_App/equipment_tray.scad:53` | Unchanged shared-template historical comments. The task allows template edits only if the example needs them; it did not. No dedicated code branch remains. |
| `outputs/Mechanical_Design_App/pi_reference_manifest.json:8` | Unchanged local reference provenance/rights metadata; not loaded by the active viewer. |
| `outputs/Mechanical_Design_App/test_rack_workspace.py:23` | Disposable legacy migration/conflict fixtures only; never real user data. |
| `outputs/Mechanical_Design_App/test_rack_workspace.py:24` | Disposable legacy migration/conflict fixtures only; never real user data. |
| `outputs/Mechanical_Design_App/test_rack_workspace.py:65` | Disposable legacy migration/conflict fixtures only; never real user data. |
| `outputs/Mechanical_Design_App/js-tests/run.js:422` | Negative tests rejecting retired wording and implicit ids from first-run UI. |
| `outputs/Mechanical_Design_App/js-tests/run.js:423` | Negative tests rejecting retired wording and implicit ids from first-run UI. |

Protected reference inventory: 33 matching lines in 5 files. These are unmodified historical copies and the former renderer modules; active UI uses the new generic root copies instead. Full excerpts are in `protected-reference-matches.json`. Every location follows:

| Protected file | Matching lines | Why retained |
| --- | --- | --- |
| `outputs/Mechanical_Design_App/rack-references/before-app/app.py` | 376, 390, 398, 408, 419, 459, 463, 485, 813 | Explicit task prohibition on editing/moving `rack-references/`; preserved local history, not the active renderer source. |
| `outputs/Mechanical_Design_App/rack-references/before-app/assembly_records.py` | 54, 73 | Explicit task prohibition on editing/moving `rack-references/`; preserved local history, not the active renderer source. |
| `outputs/Mechanical_Design_App/rack-references/before-app/workspace.js` | 19, 20, 24, 54, 56, 77, 190, 202, 203, 252 | Explicit task prohibition on editing/moving `rack-references/`; preserved local history, not the active renderer source. |
| `outputs/Mechanical_Design_App/rack-references/fixture-0li3pv2o/rack-workspace.json` | 19, 39, 49, 56, 59 | Explicit task prohibition on editing/moving `rack-references/`; preserved local history, not the active renderer source. |
| `outputs/Mechanical_Design_App/rack-references/rack-studio.js` | 13, 14, 17, 36, 38, 209, 259 | Explicit task prohibition on editing/moving `rack-references/`; preserved local history, not the active renderer source. |

Archive matches are intentional historical source/evidence. `README.md` in the retired archive identifies every retained original or extracted section and its purpose. Printed `outputs/Lab_Rax_Pi4_*` evidence, the local reference asset, user data, immutable revisions/caches and catalog packs remain preserved and are not included in this source-only count.

## Files changed and SHA-256

Before-edit checkpoint: `docs/archive/codex/2026-10-19/task21/`. All 80 existing source/test checkpoint copies were reverified against `before-sha256.json`. Full machine-readable before/after changes: `docs/archive/pi4-retired-20261019/changes-sha256.json`. `artifact-sha256.json` lists every created archive/checkpoint artifact with its digest (excluding its own self-hash); the REPORT likewise has no self-referential digest. A dash means a new file or a moved original, as indicated.

| App file | Operation | Before SHA-256 | After SHA-256 |
| --- | --- | --- | --- |
| `README.md` | edited | `df14a30a7123bd621eb31a7e85e3726e16a951a6d1bd3e9a3a9ea663594d8647` | `5d205f646d948ca59493545f7509667e9baddabc8b5dfe147f0b64e034ace5b1` |
| `app.py` | edited | `16c1531cca5aab465c17c5c32a9c1a2fd72d18937abde2acde789396bcefeb99` | `4ae24b088577b48bf0d67eb331d2dc439486a64bec1dae932d41ee1cd31a00ad` |
| `assembly-studio.js` | new | `—` | `296729e6f1e68c4df1ba5dcb798327a266592beabcd1b6341d8476163aac4c13` |
| `assembly.json` | moved to archive | `ef1050c5e535e0616f50d8b2c34a22ce1b94c7954050d2f9c30096306f485436` | `—` |
| `assembly_records.py` | edited | `107421263fc5bd412aa451d683544d94b1dee611f75575ebebd3d42db5b01906` | `696e81c7166af0c465ffaac1341b06b03af28db78d925155929adc24958482f5` |
| `asset-manifest.json` | new | `—` | `a536c02d0a50535ec71f92125b149e7bd9638caab6f22b1eb0bde53988b46bdd` |
| `cable-ports.js` | edited | `d6019d3b6f51b922e080369460f3f9f8b2efe82c09d5f0fd35f5a2dd23c9d35b` | `43430bfe347f05bedf12a16ec201dd201600efad1fe796fd579c572373ed423f` |
| `cable_ports.py` | edited | `8cbbc5d83bed9fe401f2f9e1fd175d879f6baeaf3fcc4193658223d3fc5f7136` | `f437e6789b0d95806a394b503eda2e2336ddd51820e59657786e438f02bdfabe` |
| `catalog_evidence.py` | edited | `2ac237b5fda7091e84c237cf48a39640750333db0474a672909441766bc181eb` | `2ab8c41440c78fbef1d7545966650b08774d52a0c04ce15223644e100ccb88fa` |
| `clearance.js` | edited | `c102f2f40c412cecb713fe02800b828f89dc6eaa3bbe4967f77a0cf9b7feef32` | `2dbf27fa0e6c225d62ab192705a1994d1d35d0284ac48586c13c69e7fdb0fb8f` |
| `equipment-examples.json` | new | `—` | `454d09a320602d0e14852ff5a6183e31fad92e077f0d78cdaaf6e1993b897e5e` |
| `equipment-wizard.js` | edited | `04b567d2abc1ba2b27ff25e3e221bec77efd0690a2ed28506c01754572f0548e` | `38d5b88f32854c05fc79da54bd812e1924b44df7a6885d93e75bfcfc3426ada1` |
| `equipment.py` | edited | `f872227a4fdd63f1cbe5959b9e56b9ea1ab8aef873f34e504ac1a0a42befb3c6` | `55f4ce2c94e362bf35f490ee37a36aa233c65cc8ce38d67069ac43512d27c607` |
| `equipment_examples.py` | new | `—` | `d48ce1b0c88f9fc34bc2d852e51989928eb9d8d753a805be12882c5782f68d13` |
| `equipment_migration.py` | new | `—` | `9d1eecab432f64197af9f415d410aed3613fc7b12744bf778be78510aa863b13` |
| `faceplate_color.py` | edited | `cff95233b06a3e4bc2a3cd58744a022c7570387395e04c6e1d9280f0b60ffe9c` | `e6cc29cfdc8f5a92572917f101ea9495d9e1267e7dbdab6f2cc94c6b5770f667` |
| `hardware-records.md` | edited | `9470c7b4b3290261e41c8d3df04d9422426d74a367b7047da5b47f7a739827cb` | `4f916040b366757d2ca7bd70b4ea66a0688ba47acbaafd7a5d6a131297290d4b` |
| `index.html` | edited | `376c7e211e7d4bd367f37b8ee652cdaa8090fef4e9d3eb080bcaf848ebc10366` | `fa8b33406ab66d89541addcfb40d93fbf15b9778c3dab42ed86720bbd61e5ca1` |
| `joint_validation.json` | moved to archive | `10723eb1df2d6e3cfdd1fdbf527ec46329cf8798525bc8f8add784af6b8ab2ec` | `—` |
| `js-tests/cable-routes.js` | edited | `af0a53f388c5dbf21328db8f63afed5adc08242e8d39c346809badefa2e26917` | `84a8298af85c7970dfd49ce8c0a469442cfcb19ce5ec936c73632d456e289092` |
| `js-tests/cable-sheet-view.js` | edited | `08112c8d0e5d4d2720b5eccbe11cbc891cd38010070c51890567f2f46d275ae5` | `267328a7dcbdf9849c8d4a9f1f2cc17468e668f5cdd8778683a4cefa2cb6dc0f` |
| `js-tests/cable-sheet.js` | edited | `aa73cdc0ff07b29937887b4888227755688bc998eb9565a5412ed60c4dad80e7` | `059eae7681388e438b81a9156b5af2acce768918d972a0c2a9cc9de2962a8d47` |
| `js-tests/cable-suggest.js` | edited | `3731068628db35030fcee41772c45301647fedb3c1319a6c4b6fa8b4c49c7592` | `cca144649b80806f209962bbc548878cd4b5d0c31858e200e6cdf240a484ec98` |
| `js-tests/example-fixture.js` | new | `—` | `f99a798cd1b4e4eeb6c0793dd1a4e263b0680e7f192862c88544ede2ba5dbf9f` |
| `js-tests/page-logic.js` | edited | `c9132668e178221c013c0de9dabc8609c1593092d6619ad8c2d3387e083ada2d` | `d55fc7b41ee0a9143eb46fb627627f75ad9f76da4cb74f1aa1ab89ff0e635cf0` |
| `js-tests/run.js` | edited | `442867d8e352119f142050093966ca161f37a8bb7368369aa6ebba3a352cd622` | `6b4e0c77fe857eb1ee8a840e962224e89557be506b1dd6e1951b7c01c76394fd` |
| `js-tests/tray-placement.js` | edited | `81c1177a353bcf4e0429562281db178cb4388abeba7d232b0ea6cdc5159a0771` | `e1b806b13b1e2e453dde5905f48832cb7ff6d5892a85183194bed1ccc45717e1` |
| `mesh_revision.py` | edited | `4afafbd290cea9c2828a9efe91238f89d1e617c0aeed805f78c3084be71290df` | `60e1d7d4f226f06ae1e144ea734f9df45c7a03392d375c55c7a81ce2746f3416` |
| `pi4_baseline.scad` | moved to archive | `1136215f33e87d8e943ab62f4cb627010123a8d37dae423e478696a9f9437de4` | `—` |
| `pi_validation.py` | moved to archive | `2803477a55e419e91dda49ae951850bd299dd6324d477ec4b6a6012f91ec4e06` | `—` |
| `rack-reference.js` | edited | `bbc6df6c94f974861af719c4a4868466ab4bca5ec1bf7cc6bb3d9bf14bde6b5f` | `ea00cfe4b2c11b252de7dda4b4003177a4ed37005742010cd31a508b2149d6d8` |
| `rack-studio.js` | new | `—` | `ab296315ab0ae9ce168983187dc06981754608eda5817d094fa32f27c92df74a` |
| `rack_workspace.py` | edited | `79347ddd34878f61a0b4b803e5d3a6fb340fef63dab36522fd662034c0cc0ab2` | `3a98de2fdd0b0ef8b6d6cae9139e6b42b1a04cef7d83bd01f1d6e1a44562bc02` |
| `test_allocation_tray.py` | edited | `3f1a20a14e5074243c07fc522b636f9a0deb29549bf4ef93de4e64ffb3dec3a6` | `f7934baf060a6284047d2a146a3566df1804a8e967cc45d237d0d440b3ec82a2` |
| `test_app.py` | edited | `62ebce520b542b72d938bc33dcae61d885bfdc52602c46fe358ec24e23fead2a` | `6a4a6843fc33a8c373f4567782506c4d85b522e8f09dde9e08d2d680c419657a` |
| `test_assembly_records.py` | edited | `291c108ad5d8030c09ce7c476436023b0ccfe1153cb8b1091505bc23908e1b4c` | `ef457cf0ef7ecef28eda6c0b9691be9cbcda60eb353b5155332d6f86f20f016f` |
| `test_cable_plan.py` | edited | `f3fbd53a86718f0a0cd489efcb705eebb05aff651e1b52e248d03948b88786d5` | `0866553ee557b316203b11d540f88afba07e7cb2136680d1103c10c7f6fd8a3b` |
| `test_cable_ports.py` | edited | `32f39e30962a64303cde92db3250422f7dcfb52391573fbba7c5e8d78eb31f08` | `4e917fb6aeb84febfc09122bc79237aef9f35f0a6e6940dea3627794cb901a2c` |
| `test_catalog_phase6.py` | edited | `8fae41d033238f2704be4d8f43344f96a1b60bc875ebe4e58014471755d53a17` | `ffed1360146f98e79fb745f97d1d552a662f23ad0fb80f96d203ee264333b487` |
| `test_equipment_examples.py` | new | `—` | `3faf178cbcdbe68ae2e86c1655b373b9bcc59994731c1adbf332fc79671d54ba` |
| `test_equipment_rebuild.py` | edited | `eac48172a0e5f8203a4c2b8d80340f7063dec7b934cf13bf7ef1a32e7c28dd9c` | `0955a7d22d39b9221e0da1adabed65f44fcb80cb379df73c68034604db216d41` |
| `test_faceplate_color.py` | edited | `9defb5c2b939c94d79cf73884ddaeb4031132c949dd7dfac8e3198951f87d712` | `9aea4a9755684032439d5181ad534337278d6f4db43345b716158fbc48512275` |
| `test_mesh_integrity.py` | edited | `c6d5ea28ebbb121a976436617d271de19448bd31cec20ee05c81d1ea52784891` | `66852e645692855c4da0031a8e6cf81f4fc7b3870febbe899806c6d473dbb27b` |
| `test_pi_validation.py` | moved to archive | `a9c344ef2d84d888a87ee0af94c6bff763e5f5af419fd28736e0b5c16e12de27` | `—` |
| `test_rack_workspace.py` | edited | `92feaa6024a6b37447d74743813ed58c4111400bd120f5a3affbd6a11c415f7d` | `b2bacfea7f2fcf1a3cdc6a11889e7f49cfc182f379ace96d3a8f96122bde49d9` |
| `viewer.js` | edited | `5e20055ee087b326f7234eadc31351ed7d013d32ce2975f15afe54c13b13cae5` | `b0072bc08ae061a3732e3d1be333f59d46c126890c87f968027f9038c965d153` |
| `workspace.js` | edited | `1b6f38fc56fa10e9319ed72b347a66981bc81630a0154f772834155a3af194ab` | `b726126399f7f17b8a554b71d171c741ffb36fe26911f70a7734b06283169234` |
| `workspace.js.bak` | moved to archive | `dca4c58264510ef4edd62ab83a02c8c8a38020116d3a6cf43c9b01ae7c55b9d0` | `—` |

All listed paths are under `outputs/Mechanical_Design_App/`. Some edited files were normalized to LF; their full originals remain byte-for-byte in the checkpoint. New archive artifacts and this REPORT are the only writes outside the app source tree.

| Verified moved original → archive file | SHA-256 of both original and archived bytes |
| --- | --- |
| `outputs/Mechanical_Design_App/pi4_baseline.scad` → `docs/archive/pi4-retired-20261019/pi4_baseline.scad` | `1136215f33e87d8e943ab62f4cb627010123a8d37dae423e478696a9f9437de4` |
| `outputs/Mechanical_Design_App/pi_validation.py` → `docs/archive/pi4-retired-20261019/pi_validation.py` | `2803477a55e419e91dda49ae951850bd299dd6324d477ec4b6a6012f91ec4e06` |
| `outputs/Mechanical_Design_App/test_pi_validation.py` → `docs/archive/pi4-retired-20261019/test_pi_validation.py` | `a9c344ef2d84d888a87ee0af94c6bff763e5f5af419fd28736e0b5c16e12de27` |
| `outputs/Mechanical_Design_App/assembly.json` → `docs/archive/pi4-retired-20261019/assembly.json` | `ef1050c5e535e0616f50d8b2c34a22ce1b94c7954050d2f9c30096306f485436` |
| `outputs/Mechanical_Design_App/joint_validation.json` → `docs/archive/pi4-retired-20261019/joint_validation.json` | `10723eb1df2d6e3cfdd1fdbf527ec46329cf8798525bc8f8add784af6b8ab2ec` |
| `outputs/Mechanical_Design_App/workspace.js.bak` → `docs/archive/pi4-retired-20261019/workspace.js.bak` | `dca4c58264510ef4edd62ab83a02c8c8a38020116d3a6cf43c9b01ae7c55b9d0` |

The archived-source README explains each move. Complete originals and extracted mixed-module sections/tests are local preservation, not runnable release packaging.

## Assumptions, limits and open questions

- The bundled saved JSON record is the example library item. To obey “never touch user data” and “no automatic builds,” it is exposed by a read-only library overlay until an explicit equipment save materializes a same-id record in user data. An absent same-id record causes the bundled seed to appear again; permanent removal of bundled examples was not specified. No active library was seeded or modified during this task.
- No fresh browser/desktop session was authorized or used. Interactive layout, selection and appearance were checked through existing page/module tests and source inspection, not a visual acceptance session. The live server continues running its prior loaded code until Brian separately authorizes a restart.
- Legacy assemblies keep their saved names/notes/reference snapshots, even if those historical user values mention the board. Only fallback/default wording is replaced; rewriting saved evidence would contradict preservation.
- The shared SCAD template was not changed because the example works without changing it. Its two historical comments and local provenance manifest remain as documented above. The tested example source SHA-256 is `bc1d4aa2b5d58fb9536db101005272be900be78f184527565971f474972c370d`.
- Generic color-STL support remains unavailable for the geometry reasons above; extending it requires separate work/direction. Neither mesh closure nor these software checks establish printed fit, strength, retention, installation access or cable capacity.
- No required decision remains for the implemented cleanup scope. Current-status edits to AGENTS/HANDOFF/ROADMAP/PROJECT remain for Claude, as the task directs.

REPORT written; task work stops here.
