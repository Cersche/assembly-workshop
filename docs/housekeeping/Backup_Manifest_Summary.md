# Backup manifest summary — inventory only

Backup_Manifest.csv is a complete **pre-housekeeping checkpoint** of every 957 regular file present before this pass changed repository contents, including tracked, untracked and ignored files; only .git internals were skipped. Total 105,009,260 bytes; 14 tracked and 943 untracked. The timestamp column is UTC. No backup was created. Newly generated housekeeping documents and archival destinations are later changes listed in Changes.md, not part of this earlier checkpoint; this explicit cutoff avoids pretending a manifest can contain its own final SHA-256.

All files under outputs/, work/ and data/ are classified protected, as are databases, revisions, rack-history, artwork and caches at any location. This deliberately includes all source assets/evidence in those protected areas. Root governance/docs are editable only as explicitly approved; protected=no is not permission to discard them. No symlinks were encountered. All listed files were readable and stable across each hash read. This is a sequential inventory, not a transactional snapshot of a live database or unsaved browser state.

## Totals at checkpoint

| Area | Files | Bytes | Tracked files | Protected files |
| --- | --- | --- | --- | --- |
| (root) | 7 | 67057 | 3 | 0 |
| data | 14 | 2320342 | 0 | 14 |
| docs | 4 | 48152 | 0 | 0 |
| outputs | 339 | 32200796 | 7 | 339 |
| work | 593 | 70372913 | 4 | 593 |

## Largest 20 files at checkpoint

| Path | Bytes | Tracked | Protected |
| --- | --- | --- | --- |
| work/pi_aligned.stl | 6108784 | no | yes |
| work/pi_reference.stl | 6108784 | no | yes |
| outputs/Mechanical_Design_App/pi_reference.json | 5591210 | no | yes |
| work/gui-restoration/before-app/pi_reference.json | 5591210 | no | yes |
| work/rack-geometry-recovery/sources/5U+Lab+Rax+X2D.3mf | 3250025 | no | yes |
| work/rack-geometry-recovery/sources/index.html | 2213962 | no | yes |
| outputs/Phase7_Physical_Observations/2026-10-18/photos/Photo_1.jpg | 1927419 | no | yes |
| work/phase7-digital/corrupt-copy/revisions/7c639ef2c4594d8157ef4839b23b01a9d8b8dfa09de8f5c9a0fa73795925c2db/tray.stl | 1878130 | no | yes |
| work/phase7-digital/acceptance-data-a68b15c6/revisions/7c639ef2c4594d8157ef4839b23b01a9d8b8dfa09de8f5c9a0fa73795925c2db/tray.stl | 1878120 | no | yes |
| work/phase7-digital/render-diagnostics/tray-normalized.stl | 1878120 | no | yes |
| outputs/Phase7_Physical_Observations/2026-10-18/photos/Photo_2.jpg | 1772576 | no | yes |
| outputs/Lab_Rax_Pi4_Assembly_Beta_Gusset_Fix/tray.stl | 1709448 | no | yes |
| data/normal-use/revisions/ebd6af3164685923c661c7965badd932d98ed6c1da9bfc51742fe934f6a68a78/tray.stl | 1709434 | no | yes |
| outputs/Lab_Rax_Pi4_Assembly_Beta_Clearance_v2/tray.stl | 1709434 | no | yes |
| outputs/Mechanical_Design_App_Beta_0_8/Mechanical_Design_App/data/revisions/ebd6af3164685923c661c7965badd932d98ed6c1da9bfc51742fe934f6a68a78/tray.stl | 1709434 | no | yes |
| work/phase5-browser/revisions/1e05abc6db7199a810e98c419632136fbd401586e2b6c7dd60bedda62ecaae29/tray.stl | 1709434 | no | yes |
| work/phase5-browser/revisions/57742f38bb36e34a81544cd2ceb6c1477da3620ec305f9b3cb8ba6be4dfb54e0/tray.stl | 1709434 | no | yes |
| work/phase7-digital/render-diagnostics/tray-asciistl.stl | 1709434 | no | yes |
| work/v08-build/revisions/1e05abc6db7199a810e98c419632136fbd401586e2b6c7dd60bedda62ecaae29/tray.stl | 1709434 | no | yes |
| work/v08-build/revisions/2d10d88397b095b88b3f6a10998c82ba4570f536d9ffef2676d2cb54d68c9deb/tray.stl | 1709434 | no | yes |

## Untracked-only critical assets

The runnable app source, templates, catalog packs and creator/Pi meshes/photos; both user data folders (DBs, rack JSON/history, revisions/artwork/equipment caches); original beta data and mechanical baselines; physical observation photos/provenance; most recovery/acceptance reports, scripts and safety copies exist only outside tracked history. Exact paths and hashes are in the CSV. A clone/commit does not preserve them. The current data folders are compared in Data_Locations.md; their contents are not interchangeable merely because DB row counts match.

## Comparison with earlier manifest

Reference: outputs/Session_Handoff_20261018/Preservation_Report.json → C:\Users\brian\Documents\ChatGPT\Assembly Workshop\outputs\Assembly_Workshop_Handoff_Preservation_20261018\Snapshot_Manifest.json. Parsed 492 earlier manifest records; compared normalized relative paths and SHA-256 against this pre-housekeeping checkpoint. **465 new / 13 changed / 0 missing / 479 unchanged.** “Missing” means absent at the original relative path, not proof of data loss; renames are not inferred. This compares manifest records, not the actual earlier backup payload. No earlier backup files were repaired or copied.

### New since earlier manifest

| Path | Bytes | SHA-256 |
| --- | --- | --- |
| GEMINI_HANDOFF.md | 6605 | f6cc70b5b2ebb3e7eb73f9b76a23f4cb599d64ce341587a878f63e7c216bb7fd |
| START_HERE.md | 10045 | 97f837ce4029087076829ef4176e742f5b6eb12080fb309e08571db8ca46f77e |
| data/normal-use/artwork/e40e0179e1eeb4a5c98643cba7dbd0f7ed7beb5dac3d18b414a0abfeab3c5582.png | 28616 | e40e0179e1eeb4a5c98643cba7dbd0f7ed7beb5dac3d18b414a0abfeab3c5582 |
| data/normal-use/rack-history/14994e90-8fa0-42ae-ace0-6055b7aaf35e.json | 5032 | d6d73e14350ad38729f84f12dbaed374970cd5d5b6230f137f1e2027c37d5a90 |
| data/normal-use/rack-history/3b04d355-b461-4a86-86d4-3e202e0aff91.json | 4907 | 00990cbc6ac751a41d788a7edb570a9592a4b675fbe89d21176acfc31bb9e92b |
| data/normal-use/rack-history/45d893fe-b1fa-4a6b-b58d-c8348b709769.json | 4899 | be99e0a711ab90a011ef914d5b37fe28efc759cd50627435819b2652da5a2823 |
| data/normal-use/rack-history/7eb64862-d443-436f-95c7-6875b041606d.json | 573 | dfaaa9b0f459f079bbcfa834a3bdf16e33d1ad66c13ac98ec641b024014232a3 |
| data/normal-use/rack-history/aa3ff3ef-24b3-4c78-8b4d-2c39ba12aa34.json | 4899 | 683e34bb377257b120d7fd079e929e0a853a7d987065cfe584e75900b8a1cae1 |
| data/normal-use/rack-history/ea0d424f-ce11-4f7e-8a10-c676f31e859e.json | 311 | e2b6f55acfc6e84300cb761981d2ef2eb0fbf22548ea6ae9b1e4ad7b2589b53f |
| data/normal-use/rack-workspace.json | 9245 | accb584350659344602e78cf3864951896958a680805c40c0660b77e671d1847 |
| docs/housekeeping/Audit.md | 35134 | 6ec718d0c3100dafb98d3ee8379d7d79cf7345dd67ac7c76d4bacbe287541417 |
| outputs/Mechanical_Design_App/__pycache__/assembly_records.cpython-310.pyc | 10648 | c15f5df2f66d8be13c3a3bec2502359e561b115304bbe5001a0dcf3404040500 |
| outputs/Mechanical_Design_App/__pycache__/equipment.cpython-310.pyc | 8913 | 2fc63296e7810fcedf5519d4383b51191c7ab151c9e2cde682190bf2a6330c6e |
| outputs/Mechanical_Design_App/__pycache__/rack_references.cpython-310.pyc | 1169 | 51de14d78b3fbd7a0cafef1dfe6d4caa2fc6c289ac6bade8d68b72f563307893 |
| outputs/Mechanical_Design_App/__pycache__/rack_workspace.cpython-310.pyc | 7044 | 577ac506cdeec22a76943d4bace37693b9dee273900c84be858733eb82652b1f |
| outputs/Mechanical_Design_App/assembly_records.py | 11214 | addc42ed8c33089654fbf424df43599401a76572a2106151a4841d670911876c |
| outputs/Mechanical_Design_App/data/equipment-revisions/52054080bde21f8567f724692d6a588912e7d423c891d7d18b2327fc9e5379b9/equipment.scad | 5826 | 52054080bde21f8567f724692d6a588912e7d423c891d7d18b2327fc9e5379b9 |
| outputs/Mechanical_Design_App/data/equipment-revisions/52054080bde21f8567f724692d6a588912e7d423c891d7d18b2327fc9e5379b9/faceplate.stl | 207575 | 0070f137582cad7a6aaf6dfc18119daf4034789f3b37aec111e867d3b02bbc2b |
| outputs/Mechanical_Design_App/data/equipment-revisions/52054080bde21f8567f724692d6a588912e7d423c891d7d18b2327fc9e5379b9/revision.json | 4876 | f64a8c257d6c8b850b81d081a8da8828527d0b80cf7ca4638d1ce41005a0544c |
| outputs/Mechanical_Design_App/data/equipment-revisions/52054080bde21f8567f724692d6a588912e7d423c891d7d18b2327fc9e5379b9/tray.stl | 219008 | 68a59cf552918e9782be2129307caf5944b5bbd0bb3d54f8dbde7fb91cf68be9 |
| outputs/Mechanical_Design_App/data/library.sqlite3 | 28672 | eb22b03775e9b66b3bdbb74e174ddc8e36b4fc8e1edc3e46a3be14963631932e |
| outputs/Mechanical_Design_App/data/rack-workspace.json | 2434 | 888676fd2a0a78a7e0f7f49e2677427aebf1d903bc36b0d5d0a192ef89f67dc7 |
| outputs/Mechanical_Design_App/equipment-wizard.js | 30858 | 257e89b9810aebc730515d0c5f8e0239a8ed52ad6df0ece480868d11d2ab292d |
| outputs/Mechanical_Design_App/equipment.py | 14233 | aa581885f6f6a879b687d228240e13fac080e59b4faeb5322945e0219a5ea525 |
| outputs/Mechanical_Design_App/equipment_tray.scad | 8420 | 0806c55f6d155f930558a522619735565bee788eb90e26ee5fe096fee269489a |
| outputs/Mechanical_Design_App/rack-reference.js | 7495 | bbc6df6c94f974861af719c4a4868466ab4bca5ec1bf7cc6bb3d9bf14bde6b5f |
| outputs/Mechanical_Design_App/rack-references/Browser_Reloads.json | 277 | f885b5930ee30443b0c66c4b4ea29c60ace68f670c227922aa4ced45b80f542d |
| outputs/Mechanical_Design_App/rack-references/LOCAL_ONLY.md | 425 | 813b1db31dec5cc50324efedee85d2d9e695560dd511e395ea6f249f26b5f70e |
| outputs/Mechanical_Design_App/rack-references/Logo_Custom_Post_Labels.png | 80278 | a5d35ff653afaa0bc7d20738ff99b786b5cf9125fad7a4f91040d5b12a742645 |
| outputs/Mechanical_Design_App/rack-references/Normal_Branding.png | 127140 | f0a3ae8abed7865ecd3608a685697958931580e7406e1c4c852dd08ffdb88e7a |
| outputs/Mechanical_Design_App/rack-references/Post_Labels_Off.png | 80584 | 26484ee5d0258ea49e159e9a8a9d5d053d95e49c950c057468e866bee2086a7d |
| outputs/Mechanical_Design_App/rack-references/Report.md | 4102 | 7f7cfe0ae8652f96099f757899c5973ddc517eb74b0565d927488fd60c908405 |
| outputs/Mechanical_Design_App/rack-references/assembly-studio.js | 6199 | d67896c4734d230f4844bee42d3a169faa1e61a5f6fe1598b3989cddef3f7608 |
| outputs/Mechanical_Design_App/rack-references/asset-manifest.json | 6810 | 372456c0b7780959de03386933b5bbe894730e0e0ca860c2a941a35a19f5f804 |
| outputs/Mechanical_Design_App/rack-references/before-app/app.py | 33006 | aa601703400bdb2f583daaa86785b837b8c5e732a2dea8b20a95efcae27b85a2 |
| outputs/Mechanical_Design_App/rack-references/before-app/assembly_records.py | 10545 | 350d51c9206d5db43d29b9b3075c3cb69d183c6a4d6bc77f939f6ca64299d696 |
| outputs/Mechanical_Design_App/rack-references/before-app/asset-manifest.json | 6111 | 936e87dddf71f14f67acc68059641a564281d2e8bddf316ada8bb70819da7a23 |
| outputs/Mechanical_Design_App/rack-references/before-app/rack-studio.js | 25917 | 7a9d576326e7521210673314e1a57000282ca0d219d80142090a0e70382fece4 |
| outputs/Mechanical_Design_App/rack-references/before-app/workspace.js | 49748 | dca4c58264510ef4edd62ab83a02c8c8a38020116d3a6cf43c9b01ae7c55b9d0 |
| outputs/Mechanical_Design_App/rack-references/catalog.json | 10227 | f6aebdd822520ab27bd9c8db83ed4057b071a74eedd86e6998170ce980e9f19d |
| outputs/Mechanical_Design_App/rack-references/component_0_1.json | 65301 | be60ee10c3b332566ee388174c67e96de48db5ae0738fcfe0b29a3574321275b |
| outputs/Mechanical_Design_App/rack-references/component_0_14.json | 361 | bf129b9e1bc764d60b07289af3c27abf498e53d0a0c58396cae4ba50f41288e3 |
| outputs/Mechanical_Design_App/rack-references/component_0_17.json | 95380 | a3b8e136050a5101f83e987068f737a6d54e47e25e76bad67662d0c268ce331e |
| outputs/Mechanical_Design_App/rack-references/component_0_22.json | 329 | b4640f9cfee3e97e7bae42e37ccb02d0945e47e535a384276940cbfd8284e48f |
| outputs/Mechanical_Design_App/rack-references/component_0_24.json | 103378 | 1683fd9c57a4d29d52fb8df879ee8e146ed6ffb1c8b2435e8ea66baa2e34619a |
| outputs/Mechanical_Design_App/rack-references/component_0_29.json | 361 | 65a2bb87d900bcb18d0d175116c31553232e6be9420d4f32abf8066273869e40 |
| outputs/Mechanical_Design_App/rack-references/component_0_31.json | 109230 | e2c302b75a05711834ae5ac4fcfbf2eb79b139ce76b54820622a529614c6a098 |
| outputs/Mechanical_Design_App/rack-references/component_0_36.json | 361 | fba0ef7aa92c016563b0d2b12561332d1997738a232594680d7b6f75b564b427 |
| outputs/Mechanical_Design_App/rack-references/component_0_6.json | 361 | b4962c43d49451f90a51cb0734dfdef052dcbaa9a48fc018950c5e6f4c33d239 |
| outputs/Mechanical_Design_App/rack-references/component_0_9.json | 85095 | 2c09ae520f6ac62dd45543ce9c6c2c6e915bbb7a631e8d8023ebbc4d2ef0088e |
| outputs/Mechanical_Design_App/rack-references/component_1_1.json | 109230 | e2c302b75a05711834ae5ac4fcfbf2eb79b139ce76b54820622a529614c6a098 |
| outputs/Mechanical_Design_App/rack-references/component_1_11.json | 144820 | 9f8253fd7d89ec8414d2085d81078d750dc4520812cfa07b84c4bca4c597d699 |
| outputs/Mechanical_Design_App/rack-references/component_1_13.json | 377 | 785aab741b5e2200b583a3f17f41ab42d7af673032dd2fe3e9f635fd01c3a63b |
| outputs/Mechanical_Design_App/rack-references/component_1_15.json | 361 | fba0ef7aa92c016563b0d2b12561332d1997738a232594680d7b6f75b564b427 |
| outputs/Mechanical_Design_App/rack-references/component_1_18.json | 611851 | 107f07dc8b78f110b985896e22deea0d921b262c6568386c24806ada47322b61 |
| outputs/Mechanical_Design_App/rack-references/component_1_20.json | 466628 | 2e9e43dbe6997cdbf728d16d6d941cc4d9b8ba074b3a96a997d24c930ec834a5 |
| outputs/Mechanical_Design_App/rack-references/component_1_23.json | 732894 | 0158a87a3105f6f006f040874bf2fb5446d90dddd6ea53b1250d7f6a390ac170 |
| outputs/Mechanical_Design_App/rack-references/component_1_25.json | 263783 | f55d567e398ba5e54e36f0f7238b913b0d2c950d9b2db0a3843bafd313348d9c |
| outputs/Mechanical_Design_App/rack-references/component_1_28.json | 48852 | a101735b3063c6a0b02318c3ccc2bd7574ca7dab1d667ace96cecee08b5db079 |
| outputs/Mechanical_Design_App/rack-references/component_1_6.json | 59351 | 188efa05bb95f0102bc1fca6207c46288b563c4a6175941d7edf0803a5e34ace |
| outputs/Mechanical_Design_App/rack-references/component_2_1.json | 219523 | c57d6a7fb17e6bfc512f8ce231f0051a73ee5f341ef59f87d8e0ac32007c647f |
| outputs/Mechanical_Design_App/rack-references/extract_logo.py | 1492 | 16a4e3465d8eefe9a8ffc160e4dea9566b998bba05aeeed034fed7a0429538c8 |
| outputs/Mechanical_Design_App/rack-references/fixture-0li3pv2o/library.sqlite3 | 28672 | eb22b03775e9b66b3bdbb74e174ddc8e36b4fc8e1edc3e46a3be14963631932e |
| outputs/Mechanical_Design_App/rack-references/fixture-0li3pv2o/rack-history/4d274e74-5d5c-46fb-82a0-023f1b2cc9ea.json | 399 | dd2e7920afee3a4f3eddd25df38fb5f016868b215f0190f038c8e684e21edc01 |
| outputs/Mechanical_Design_App/rack-references/fixture-0li3pv2o/rack-history/814b0610-fa71-440f-aa73-d43a9c9f20f2.json | 327 | 55a52533a5cd9bd0dc9acb9838dbb2e5e4010da5581b76eaebbb17a031fd1e22 |
| outputs/Mechanical_Design_App/rack-references/fixture-0li3pv2o/rack-history/c81445d0-8988-41ee-a511-8eb8eb9314c1.json | 398 | fac8ed1b04915a9362df05b2eff1bda54ce66b7d9e0e6a323b5946099aa4940d |
| outputs/Mechanical_Design_App/rack-references/fixture-0li3pv2o/rack-history/cf29af92-ab4f-452b-bcbf-58c7fe3d8da2.json | 398 | 62145b05123222583983bc5aad55999c3bcfa365c347ed1bba1213b7d3752008 |
| outputs/Mechanical_Design_App/rack-references/fixture-0li3pv2o/rack-workspace.json | 2504 | c50bd7f9cc447a2c1bd98bb21fd8379756e5dc365a576cd0b3e965c454793ddf |
| outputs/Mechanical_Design_App/rack-references/http.log | 17431 | d6db03a63c0f4190d3543491e5106372cc6bdffbf025728460a57e396d818ec5 |
| outputs/Mechanical_Design_App/rack-references/preview_server.py | 1098 | 25d4e932e70e64782f8887a4e3f93eff9e41fa5cda73b762346a568f25733391 |
| outputs/Mechanical_Design_App/rack-references/rack-layout.js | 1737 | 15ee6ff1533c49ffee49cac7a66d8e30278ffaad30ba42f94eed936e1e76c5e4 |
| outputs/Mechanical_Design_App/rack-references/rack-logo-faces.json | 5284 | b34c4f5e390cf45e0a001f29a669841ed7ab6356c01d346e525b8b14a663dbc1 |
| outputs/Mechanical_Design_App/rack-references/rack-scene.js | 7970 | 414214bcbf3f1f40ff7a6be0791741ec721cb3d9585cc4d148b1c68f7ff1c7d2 |
| outputs/Mechanical_Design_App/rack-references/rack-studio.js | 26664 | 905eb37676487820093448ebe73f28b9d6c42c84ede25d0768ee86bb3c63a1ee |
| outputs/Mechanical_Design_App/rack-references/reference_0.webp | 127306 | 256d41a3041864229d72224da23119820372861204c12aef6dc72e2007277c4b |
| outputs/Mechanical_Design_App/rack-references/reference_1.webp | 97522 | 12798038ec8e595e6b3f3f328dfc3ec4cacefc2e4013dfae5d934b57c94d4850 |
| outputs/Mechanical_Design_App/rack-references/reference_2.webp | 182520 | eaf3ef9804c36ecd1e3447f88d14b7362a59e4fedc865df357fddc7fd9c8b7da |
| outputs/Mechanical_Design_App/rack-references/register_assets.py | 747 | b24b71cf959b22a306144059354b31dec5f847f6f2d0e3adb958939d669f6f7b |
| outputs/Mechanical_Design_App/rack-references/server.stderr.log | 3319 | 12def8510d33bb57c0ade286b3daa10ff184d0738d7e3d56a840229735b83ce2 |
| outputs/Mechanical_Design_App/rack-references/server.stdout.log | 125 | ac82f41376ff4a57787f491712d9925a7baed86000383357eab942ab893d68c1 |
| outputs/Mechanical_Design_App/rack-references/test_branding.cjs | 2161 | 97869f969d2b29f6bc48b818dbe0e75a126bb150e3807617410d14a1d975e02b |
| outputs/Mechanical_Design_App/rack-references/test_branding.py | 2227 | 5b01f6bc18cf87a64f7bb9b4a72f760342ccfff3e64b877b16e25724ca5dadfc |
| outputs/Mechanical_Design_App/rack_references.py | 886 | 12fb6c763780ea6bdf59e87553281aaae090c65ba3ed7120b0ec4c11811183eb |
| outputs/Mechanical_Design_App/rack_stl.py | 2876 | c75d9ffb64b6670adcafd0dc73724c0f1f410f6f0240575f9c7bff14455dd996 |
| outputs/Mechanical_Design_App/test_assembly_records.py | 9798 | 80bb9b8399e3256641e5c507b64d3ff00d9004435f452436954147f429960bcf |
| outputs/Mechanical_Design_App/test_rack_references.py | 3625 | 36eb430bc0d2e56878f0fcbdadca6ea650afe06f37b574808e7609f6c0b72d3a |
| outputs/Mechanical_Design_App/test_studio_save.py | 3665 | 86b82a1ce8d454998af5460a34e8c0653ae7da420f81369c860b0ddc9e8c54d8 |
| outputs/Mechanical_Design_App/workspace.js.bak | 49748 | dca4c58264510ef4edd62ab83a02c8c8a38020116d3a6cf43c9b01ae7c55b9d0 |
| outputs/Physical_Test_Coupons_2026-10-18/1_Keystone_and_corner_holes__faceplate.stl | 89992 | b4a0a829574b4da0d95ffbd8617a4ae3c137a2c0e732ba5c4a185a2c32e586d0 |
| outputs/Physical_Test_Coupons_2026-10-18/1_Keystone_and_corner_holes__source.scad | 8748 | bdf685dd94f0483fb00773a1ddf1d42086daffd2e8d8f49892003cdcbbf8f29f |
| outputs/Physical_Test_Coupons_2026-10-18/2_Snap_joint__faceplate.stl | 5564 | e75cbc97a8f2e4d60f5fc134a0b2206c18639021acd832fc0bec62ef4dd00244 |
| outputs/Physical_Test_Coupons_2026-10-18/2_Snap_joint__source.scad | 8727 | 685cdbe111bd3cf1bc5fcef4bd86a07998516656c317543db4cd76797e76da5a |
| outputs/Physical_Test_Coupons_2026-10-18/2_Snap_joint__tray.stl | 4515 | da8ebf94bcf911eceb6e748e1b714002aa8eff33682bff8d249f27280771f23f |
| outputs/Physical_Test_Coupons_2026-10-18/README.md | 1262 | 6d658e10ebc3573897f45e8afff0dafe34c9974697fe4428bbe4247d4d991dbc |
| outputs/Physical_Test_Coupons_2026-10-18/manifest.json | 1136 | d0a8a0e2571ace9981848862526f827ee626a2f5136b28e84e2e56a74c8baecd |
| outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/A_Pi4_inserts_screwjoint_2keystones__faceplate.stl | 271782 | 368a9cdfdfb9f268d1b08712381a4a94f581ed145f521c96cd3aaec8953a3747 |
| outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/A_Pi4_inserts_screwjoint_2keystones__source.scad | 6985 | 6ef6a39c639e83543085960f0663aa26494db2d35882269632ad5def6f856306 |
| outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/A_Pi4_inserts_screwjoint_2keystones__tray.stl | 349174 | b1e4ebec26a08d779e1474938a1c21d86e00787dd2625465de61b42957f3c9db |
| outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/B_Pi4_pegs_snapjoint__faceplate.stl | 108082 | 71a03fc0fdeb076075f46129e72836a6554a3e994bd4056aebee1ef0c55f679d |
| outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/B_Pi4_pegs_snapjoint__source.scad | 6954 | 17bdfb8e04f698e09403ce912935889ee80a35809706dcf3cd5f1bd392ce41ba |
| outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/B_Pi4_pegs_snapjoint__tray.stl | 342152 | 6ad2ce8c79edc7132509785a6ef524d1e7845403ea3699c78426d0a55c33c9eb |
| outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/C_Pi4_clips_singlepiece__combined.stl | 121220 | b6598044fc0530c735edc2d6d52aabcd04ccf5494c93ec0e90564c2928ac14fa |
| outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/C_Pi4_clips_singlepiece__source.scad | 6960 | 3c845f8912516306272aac8569368606c39e4c44d7c00eb63a6085cc1eeb52bd |
| outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/D_Pi4_straps_trayonly__source.scad | 6958 | 4a667fe459faf2ded0744b7667003b2e90975f3e1cb0fb0f34ee6bb862345910 |
| outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/D_Pi4_straps_trayonly__tray.stl | 102030 | a9a30553ca9607ec05aace5fa0ad0da20edd84973154d7164558b0b372da44b4 |
| outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/E_2U_faceplate_slots__faceplate.stl | 310727 | a57d9cb8c92e593fceabc2d7333e3d69e51f0fe6896ea946669fa4b2bcdbcafb |
| outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/E_2U_faceplate_slots__source.scad | 6963 | 41cec5db4c02215458f062749d3f8c8341eb10e1209df513e048140bb6f0c122 |
| outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/README.md | 3036 | 80ed133fef36c6ab5849e8992b5f21731962199916c89451fb6f3fec4d0c24db |
| outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/manifest.json | 2291 | e6d71773799b334c67934637f422097bccaf81ad52b2553cb2f9341883375264 |
| outputs/Session_Handoff_20261018/Preservation_Report.json | 921 | 861a5f6e5990df6544ed8dcf4f5a6eb5094c0242a65e7d73c6cf111b618fddbf |
| patch_dialog.py | 14473 | f84c7d3796a1ea46db523eaf1b1f6f1487a01519510e97ba57c6f16f5f39067c |
| work/assemble-selection/Data_Before.json | 1943 | 392c4de00a60c368dba8f1f1c307e49244b8c806fab637368df51c434086f557 |
| work/assemble-selection/Normal_Assemble_Selection.jpg | 173430 | 936c628cddd95685fca0ea574322f65df78c743b874ecbdcf0cfcc1798d15ebe |
| work/assemble-selection/Report.md | 1817 | 04a35b1aacdc4bf688c08ca72c6564e91862389739f25b37df5e077961f87f29 |
| work/assemble-selection/before-app/index.html | 31786 | 3be2e47aac00a4ac4c5f21647348483d8ab02992511ad80809f5ab57071354af |
| work/assemble-selection/before-app/viewer.js | 11461 | 7633cc2f70f79d16d39a0c21b77ae2fdb1f41925157d3e22a441250c1ae1cbcd |
| work/assemble-selection/integrate.py | 904 | 7b5c6b250a1ff48081974492f3b68cdee209e85315a0b147a79f2f716b9f15a3 |
| work/assemble-selection/test_selection.cjs | 1325 | 4b347f310134326a5bd7f09723e9553c069cf4871bc6f80b9df80183cedb4945 |
| work/assemble-studio/Artwork_Front_GPU.jpg | 89769 | 190a4c2e30a34e26a9aa17b4923d094164788aec1703bb061f15a3f51668c11c |
| work/assemble-studio/Assembly_GPU_Checks.txt | 450 | 21ede056c7b3fe09c5c77359bd3ad90a74cb23c3959b44b189be87279d46012c |
| work/assemble-studio/Data_Before.json | 1943 | 392c4de00a60c368dba8f1f1c307e49244b8c806fab637368df51c434086f557 |
| work/assemble-studio/Local_Test_Artwork.png | 690 | e895b740c9c3e9002e6670af1755daafb46bc1f122f420c42f8b50f0f5e80ec0 |
| work/assemble-studio/Normal_Studio_Assemble.jpg | 174500 | b96462035a70ac423385bbc4e9d293337424b8b9b6180a84823eb3a7ae3918cd |
| work/assemble-studio/Normal_Studio_Selected.jpg | 167740 | c89893c50058b6d05af9ce6b5954c624d29ea888ad5f4147bceff3f32d04b088 |
| work/assemble-studio/Report.md | 4883 | 22151df966099176d244f347bfe728602d30e75004d5e4a59838dabb79b41f72 |
| work/assemble-studio/before-app/asset-manifest.json | 5900 | 6127fb1f6fa43e3e9fd69ce2f34bf9edf04d33349d42164d915f1d22eac5e753 |
| work/assemble-studio/before-app/index.html | 31841 | eb644a94e9639f43c7c15ac872105699245c3476a59539059f6dba55977dd04c |
| work/assemble-studio/before-app/rack-studio.js | 25390 | cd799e817da4c4f0c93f866a6c069237a380cd87aaa886b25a7243eec4c8beb9 |
| work/assemble-studio/before-app/showcase.html | 8190 | 4cccb6a28d9504af6af69c7593a5e399a72f0cb0de1f57557633cbcbe2045f28 |
| work/assemble-studio/before-app/viewer.js | 13595 | 7a6d1469f2a8c6cd9a9991a581e0cb88eea18098fa542f141e0d1371dbc65d15 |
| work/assemble-studio/check_assets.py | 1109 | 45ad77b0b3087c99d182ca4495f3e7ed1c81c52c292df68695dd85ced06d0945 |
| work/assemble-studio/finalize.py | 1158 | c2039faaba7977d73f3e3e34eddc513c0ceed3118d052d6d0793a5237416db54 |
| work/assemble-studio/integrate.py | 5102 | 1c73846961498782d5cc16c17c43e904e7bb32a32609d7a181747f060d8f0a7e |
| work/assemble-studio/make_artwork.py | 1123 | a97e9fb2c13cd0451e0db9f52df1a263421d5d85534cedef9ab4f7252c6bfe1d |
| work/assemble-studio/test_adapter.cjs | 1514 | d5c81bb80ebcabb0f3450dd92fa0910633c8b795db62b3505f78222760ca288e |
| work/assembly-instances/After_State_Manifest.json | 2263 | 2460cfb6d27ad3892a3b687ebdc9a059baebf04b0138af24db4abaf6aee23966 |
| work/assembly-instances/Canvas_First_Option.png | 42354 | 194bd73fac5ba74eaa515619343f6364f42c9adf13b9d86f9d158608f7c59da2 |
| work/assembly-instances/Equipment_Color.png | 90131 | e91ae0c0a2545aa565c23cdc28a71d71962af56b13257c8c462e7049704039c3 |
| work/assembly-instances/Faceplate_Preview.png | 84155 | b000e56d73b249e0df690f42ca4d7f5451f1abef4db984456815892866fcfeeb |
| work/assembly-instances/Focused_Studio_Option.png | 73557 | c996af6dc618172ab767c444a2b62c4a932c1f8118effc64141d853ff94c748a |
| work/assembly-instances/Memory_Append.md | 3152 | 2fa217987082677ae98e8bed6008c256771eaf8fe9b029b4d47858ab3901e70d |
| work/assembly-instances/Normal_Use_Updated.png | 67717 | cc50178bab262fd868cf966ead89dc0494a74fee0d61f9feecefd97748c3e1d5 |
| work/assembly-instances/Protected_Data_Before.json | 1139 | 89519801a29aec88c4ab609f88041e3d31a6990738c34558d85ebb6cb3010ea8 |
| work/assembly-instances/Rack_Colors.png | 1666 | 84af77b9d9878608ef63615829002676d8cb2bf48a6420ba51a916cbc594eecb |
| work/assembly-instances/Rack_Colors_Full.png | 72814 | ff41027c4979f077103194e18cff6a48b812508342160fb177044f8578204b3a |
| work/assembly-instances/Report.md | 5991 | 3143a60513cc3201565769f4f578942ab5307d45425bf2fa6eefc4063dcddb09 |
| work/assembly-instances/Verification.json | 2576 | 8b737a17ff374e1f271a5f7358d454451a9336d4a4cdd85e46b2d7813e924ffa |
| work/assembly-instances/before-app/app.py | 28082 | 541df116d86a0904619e632dfd78f710b6a8f9e345048f836f32b8599209a556 |
| work/assembly-instances/before-app/index.html | 29888 | 8c9adb7a270109a3a5cdde79c95ac36420817d324e7fa9fb9d4499a61fd6153b |
| work/assembly-instances/before-app/rack-references/asset-manifest.json | 5697 | 035508d3a046467516218293dab659e4637ac80980eeb77e99fd9564e4afb912 |
| work/assembly-instances/before-app/rack-references/rack-scene.js | 7970 | 414214bcbf3f1f40ff7a6be0791741ec721cb3d9585cc4d148b1c68f7ff1c7d2 |
| work/assembly-instances/before-app/rack_workspace.py | 5174 | 4f51105a8030ef60fe642f68808a9e70ea72c6ab82fc715733642751003a0cc9 |
| work/assembly-instances/before-app/viewer.js | 8518 | 34b90db810a0ee11d463231ee814c957c013e3cc30112cb30042e3db0222f46f |
| work/assembly-instances/before-app/workspace.css | 14445 | 523272e481889185ebeeea2eb75df531a27dc6c88004ede3bc24e12d337473ed |
| work/assembly-instances/before-app/workspace.js | 30812 | 1a6efcdc1133e2e9318e2e73410c2b123f0d7fddce4a6f611c207b99756b1d90 |
| work/assembly-instances/before-guides/AGENTS.md | 5322 | 57c6e7091f017f8e6033b80e6ad37cbbd3ffe7fe0254c13fd6c8abe6f445ef19 |
| work/assembly-instances/before-guides/HANDOFF.md | 14349 | e3caac2a832e10dece9756da7b2da97b6dfad38d85139db04f4e3937146f9cca |
| work/assembly-instances/before-guides/PROJECT.md | 6330 | 3afd6a21e181c79132963d3ac0ca6810ffc3329a727ddb114b372691413e8372 |
| work/assembly-instances/final_safety_hooks.py | 3006 | 86cd321176e98cff3b3e272db47558ac76debb8ee4b9ddef27faf0bff2acffa5 |
| work/assembly-instances/finalize_evidence.py | 4530 | 799c7ab665bb94c95b4585f44aeb47fd746f7e5a78297e89d3606a2010d79653 |
| work/assembly-instances/finalize_local_run.ps1 | 1053 | 9108c70c25e5c218b73853a1b5046a3f8a235ee4b40303de976e81a26c74dcc2 |
| work/assembly-instances/finish_hooks.py | 2639 | 31b646d067a43418498a565547230eef4497eb9bea6c1fac0a68435050f8a03f |
| work/assembly-instances/make_preview_image.py | 1182 | 8335e1b56e1caba108c6e2e551756a0c6c7277f7630afc371226b265da018b7a |
| work/assembly-instances/normal.stderr.log | 9509 | 70de9f0efd47b4938c694286a657ac206c854946464491869d52e23fb986c692 |
| work/assembly-instances/normal.stdout.log | 125 | ac82f41376ff4a57787f491712d9925a7baed86000383357eab942ab893d68c1 |
| work/assembly-instances/options-final.stderr.log | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| work/assembly-instances/options-final.stdout.log | 24 | 873bbaf8b82ac1ab9c04ea01f846c912312d00e15f944f743619399c46a148a0 |
| work/assembly-instances/options-script.js | 6473 | 08ddd879da654a915b5d85bd1bf1a7b3ee7d5e7b21a903cec4da4907c0a7a44d |
| work/assembly-instances/options.stderr.log | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| work/assembly-instances/options.stdout.log | 24 | 873bbaf8b82ac1ab9c04ea01f846c912312d00e15f944f743619399c46a148a0 |
| work/assembly-instances/prepare_options.py | 677 | a6b9e2abf79a2f613eea50c43e19abea33250e8062470d444683d5097c454390 |
| work/assembly-instances/preview-artwork.png | 1788 | 906807d4622bd95caadae5f3492efdb7f5f968e85b1d6671ae45d49d4c7fa31f |
| work/assembly-instances/rack-studio-options.html | 224271 | f379c8c81f29570f329e8bd631ca80133fe7fb9b8b6738ad0653d214fd42c964 |
| work/assembly-instances/refine_options.py | 803 | 86957a21ff0694cb314ee32dd07c3859612105f827cc0c550b69e84cfe4e6431 |
| work/assembly-instances/run_python_checks.py | 864 | 8fb59ff521df02196c4c2329d463bf7a83a17b7cd9ffbb3790a1dc9828ebbbf4 |
| work/assembly-instances/server.stderr.log | 11584 | 68584e1efbf0e194b8edc861182a9c7899abe5a0c2059263b6a7ce2220990cd5 |
| work/assembly-instances/server.stdout.log | 58 | aa82a471bffbcd4869fde79af3cbe2778dd7599c981e0112faec4c3eb44b9586 |
| work/assembly-instances/test_context.cjs | 3901 | ff76fb3405c7c0c1f43813c41acca7d36c6270cfc10af6d88afd1d4d5057ca77 |
| work/assembly-instances/update_guides.py | 6184 | f4bf700187053d27f84bb273ffce1553b7218f403c460029a83171681f9c50c5 |
| work/assembly-instances/update_workspace.py | 5347 | 1d513dedb924d044a487ff44285e03938833b43debce1eb0ec724a9e4286635d |
| work/assembly-instances/verify_preservation.py | 2696 | fcb66d677fda0aba63871d31cc8172db144dd9fea0730178caad97d351c2fb2d |
| work/assembly-instances/workspace_functions.txt | 10490 | 38f1db406bb953a98b0f9fc3a1f109c8b81358ed6060b291aa9025c59d71cc53 |
| work/faceplate-selection/Data_Before.json | 1943 | 392c4de00a60c368dba8f1f1c307e49244b8c806fab637368df51c434086f557 |
| work/faceplate-selection/Normal_Selected_Faceplate.jpg | 105963 | 3ad5ace5e89a21b58cb980f77d74d7ef67b568cf1a46336ed35eda6341476bd0 |
| work/faceplate-selection/Report.md | 1565 | 29edc354577459bd3f93167ecc629671a5e3bb01cd5623a35689b69c85d41f73 |
| work/faceplate-selection/Selected_Faceplate.jpg | 80718 | 230cbe8bfd4c386c6a1bc03ae1c0b2c87e728ce92e7218f5852dd8f42ab731af |
| work/faceplate-selection/before-app/asset-manifest.json | 5900 | cca09e71de2c206ede1f9cfd60ab0b8f54f9912b09a07a240c2ca20217a1eb4f |
| work/faceplate-selection/before-app/rack-studio.js | 24791 | 3cc3699862f174133bf449b12881a6f11e8465bc96ed6c1a2366f0db6a415147 |
| work/faceplate-selection/before-app/workspace.js | 49735 | 7fc03407f57d175b48e519027ce15e0ab4589a55613e1b02c6b19d73ff0f35b5 |
| work/faceplate-selection/integrate.py | 1481 | 46cce7def51bd12fcac683dd0fee9e9cd5761239372c42a5d7287fb16665f914 |
| work/gui-refinement/After_Authorized_Draft_Save.json | 1285 | fef61ab824b364b9771c69286f613056735141c157c3c395c07615f011955a24 |
| work/gui-refinement/After_State_Manifest.json | 1729 | 7e8704f9368719c7233b8be7e4113f8be0eee8e701c2d900282f9c449b5a974f |
| work/gui-refinement/Authorized_Rack_Draft.json | 573 | dfaaa9b0f459f079bbcfa834a3bdf16e33d1ad66c13ac98ec641b024014232a3 |
| work/gui-refinement/Decisions.json | 491 | b043a076f084a729771345ad629e5e64a8a6e834af42cc59fcec6fef80077f57 |
| work/gui-refinement/Hybrid_Appearance.png | 81413 | 3949ba071793b6ce143c452de3341bc35da791d1308a69f00b5e43720e3ee149 |
| work/gui-refinement/Memory_Append.md | 2633 | 09c46691670f3b9d43ce808e9436d0b25e25b391dc037eb699c9d99c7332aba1 |
| work/gui-refinement/Normal_Hybrid_Studio.png | 99921 | 81c5bd2bec0aa5a7c07f653d2eb7396bafd5b00b1b9d1ed292de15ec595bc6b6 |
| work/gui-refinement/Protected_Data_Before.json | 1137 | f61e54d7c2bb6ce4f8824d2e067f17817dbf22a3995d2fbe7af8df30d118d288 |
| work/gui-refinement/Report.md | 5926 | 20f6760e062a05a70947dd60a1483974c7f5a1b6250a1614d37e95082f514614 |
| work/gui-refinement/Verification.json | 3354 | cf6d67640621a30b19623d0e9d17236623d173a8af09e53d23cf710ceaa8de76 |
| work/gui-refinement/activate_normal.ps1 | 1190 | 26d6e6c295dda7ffd36df414d7a41e092d6241e17e16767b5e4b2467ed7bb1d8 |
| work/gui-refinement/appearance_startup.py | 1421 | 043a083d45e65c84842e8848ad750ded426711da4dd4c50e5fdecb6b8818d104 |
| work/gui-refinement/asset_version.py | 189 | 0eeb549010282b0d43f26bedcecfa42d2ac80e2f58e019e1c424791ea15164cf |
| work/gui-refinement/before-AGENTS.md | 5558 | 0bf542bc326a7567979637aa1ab1bdd31ccf1ff1419851f3427f6644dcec65b9 |
| work/gui-refinement/before-HANDOFF.md | 17627 | f67617724c0f38d97957c949a22f8812427535924695929f5c85446d4ed33721 |
| work/gui-refinement/before-PROJECT.md | 6710 | 8eeb493a232dc91c5085bf59760d3e2f6390e231566864e43dabe91aa36d555c |
| work/gui-refinement/before-app/app.py | 31763 | 6812a351924e6096eb5fe160d24854320f7b348ea7117326f26fbc63d51f9bfb |
| work/gui-refinement/before-app/assembly_records.py | 8755 | 2c42dad9779b29f9eae1aec01238f0c7d63bb806949a6d48ad5f7251532e85be |
| work/gui-refinement/before-app/index.html | 31339 | ae31bf97efcbcaff86fdc67cf39125a4b8b1dd1e6789541ac6dec09340c774e0 |
| work/gui-refinement/before-app/rack_workspace.py | 8345 | b0de25deddc40e70f42c2940c54f7ed132727e051066e29c6db8d89b56d580fb |
| work/gui-refinement/before-app/viewer.js | 11325 | 2e52d0dc8479f83c3936019a70fb7ac5ed8d46391c71a0b28dfcf116185a4d31 |
| work/gui-refinement/before-app/workspace.css | 15416 | 8d8fe1a9130ed0aca3d8f586dddc2278228f536b3e4890ff79020e8fde8e511b |
| work/gui-refinement/before-app/workspace.js | 44191 | ded167045c30ff00b8b48f95f1980f543ab1738174dda3eacd185f107ccc67aa |
| work/gui-refinement/before-layout-actions.cjs | 3187 | 9090c1193c9fa08e55f97fb020202d4c7750a27992223b0a7c4cfc34481f19e1 |
| work/gui-refinement/capture_authorized_save.py | 417 | eb3872ed3051b155159fcdc8170b7ac0120358ae24e47fcb3a8d3f46a95be53a |
| work/gui-refinement/check_python.py | 1125 | 5a729f024171ac490818774d4edef674156d9da400aaf6c653c3fd61ab627d59 |
| work/gui-refinement/compact_slots.py | 292 | 02474e09ef72bcf82016db788a6563b99dd60fe527d74161d9f8db61a1795435 |
| work/gui-refinement/finish.ps1 | 792 | b3fb1ad2aaac6edc3353abb3ae04a7934139b8d638b558e93cd5efd2ad820f46 |
| work/gui-refinement/fix_event.py | 231 | dbc645da3391b87188a86b4dd3a1fb016d9dcf357ce2deb7cd890b74287986fb |
| work/gui-refinement/inspector_controller.txt | 1649 | 86c195de663a40be154b94b69c73da0514fe4eece0c9723343b2099b0a4387fb |
| work/gui-refinement/normal.pid | 7 | b6ff707bd6d991d835c230964b624b66f83461dbea985fe9289c3d54610593e3 |
| work/gui-refinement/normal.stderr.log | 3201 | f2c6a9e03cd1cf2d0fb3f654cc054cfcf66b51dad8ff5730c2c520d190d2c639 |
| work/gui-refinement/normal.stdout.log | 125 | ac82f41376ff4a57787f491712d9925a7baed86000383357eab942ab893d68c1 |
| work/gui-refinement/one_save_button.py | 1121 | c4ee12b8c3ed96d56a539b29fbbc9d17b44cb1c101b07098c6b5f1af09da6be3 |
| work/gui-refinement/preserve.py | 1110 | b9cb23f9fd96ed06b64163cd79c2e25667cd0576a42a6770009eb3dcfb3ee470 |
| work/gui-refinement/refine.py | 10202 | c8d2cca0d80cf4fa354759ddde1afd16fad9c296972184707cbbdf6c954fefa3 |
| work/gui-refinement/save_controller.txt | 2835 | 7c688230d28a420dac524e1dfc62d25d63d5d0956f2930151d1fa0144c38c1db |
| work/gui-refinement/server.stderr.log | 10800 | ca51684b3ccc54369d69777168773dcdbf399162486177f4ef3b5f8f97c39871 |
| work/gui-refinement/server.stdout.log | 58 | aa82a471bffbcd4869fde79af3cbe2778dd7599c981e0112faec4c3eb44b9586 |
| work/gui-refinement/test_appearance_startup.cjs | 2172 | 1742751e22579c2c26436db99c8702ff99c50392fc4babef18c387551b220ead |
| work/gui-refinement/test_save.cjs | 4011 | 030621040d3084494f8417b0032adffd35340f24ba2213fc00433de78081ba33 |
| work/gui-refinement/update_guides.py | 7682 | 7a95af62128bbc2814c9ac0f05356943ad05530de4fad3ed81d812600b3b6e4a |
| work/gui-refinement/update_test.py | 464 | e63a9750e1aa058db6e79989a7e904e9368d932b86731765145c11fb11bd5647 |
| work/gui-refinement/verify.py | 2956 | 641b41640ef5c929f27616a1d4fe910aefec2340bfb00b6d3432c716d9a9ddc4 |
| work/gui-render-repair/Data_Before.json | 1943 | 392c4de00a60c368dba8f1f1c307e49244b8c806fab637368df51c434086f557 |
| work/gui-render-repair/Normal_DOM_Checks.json | 186 | fe9b509a735e0beda0082e4be37b4a8c7bd14ca91ef51f9473ff721ab7e533b8 |
| work/gui-render-repair/Normal_GUI_Repaired.jpg | 100225 | 044e37c23793feb3c50c93dbbeeae2edadc4dea919939a9978ff3a4bc52f67b1 |
| work/gui-render-repair/Report.md | 3848 | 55b7c5f0404033273c95b2cc86bdbaacd5b3709345021fb713a9260ba55bb685 |
| work/gui-render-repair/Runtime_Diagnostics.json | 1767 | deba463d7382302931e68e26503316f0b074e6203654b7d54f5a317a56630c10 |
| work/gui-render-repair/align_defaults.py | 387 | ca558101d887b33208f6687df242bd23873ac5fd73e64135755c0487bf97642c |
| work/gui-render-repair/before-app/app.py | 31930 | 6e9da89d40d6a2497ff3436386231a5b6000bd1639627b17fddef45963d6fb78 |
| work/gui-render-repair/before-app/index.html | 31772 | 69335f5f3810741c178c8a47d478ef4775a250485b7db66bf20a94e2a38e5ebf |
| work/gui-render-repair/before-app/viewer.js | 11461 | 7633cc2f70f79d16d39a0c21b77ae2fdb1f41925157d3e22a441250c1ae1cbcd |
| work/gui-render-repair/before-app/workspace.css | 18208 | 0cc5281b2dcd84cd08e928148931e57198e33afa26bb87c57ed839539ed7fd8e |
| work/gui-render-repair/before-app/workspace.js | 31002 | 934735581e2b183606d2138a6bafd4bc817e1fedcdb7fdf9d45295c306fc4e74 |
| work/gui-render-repair/complete_recovery.py | 2700 | f4bf24309163c921bd5e8d96af0f93328fa740d9a23289f600d6debb452200c5 |
| work/gui-render-repair/finalize_sources.py | 756 | 208185436c543a8927e5906dbea467ac92cf6ed16d9612e25f4254dda93def74 |
| work/gui-render-repair/inspect_runtime.py | 963 | 1db80470eb2bb577064ca798bc89b7839be1e71968bfedeea2c836140fed20c5 |
| work/gui-render-repair/stage/outputs/Mechanical_Design_App/index.html | 31786 | 3be2e47aac00a4ac4c5f21647348483d8ab02992511ad80809f5ab57071354af |
| work/gui-render-repair/stage/outputs/Mechanical_Design_App/viewer.js | 11461 | 7633cc2f70f79d16d39a0c21b77ae2fdb1f41925157d3e22a441250c1ae1cbcd |
| work/gui-render-repair/stage/outputs/Mechanical_Design_App/workspace.js | 49738 | 07620d7bb91e34d50500eb3ddd47b11722233dbe424b38c57e56787deb9690ad |
| work/gui-render-repair/stage/work/gui-refinement/inspector_controller.txt | 1649 | 86c195de663a40be154b94b69c73da0514fe4eece0c9723343b2099b0a4387fb |
| work/gui-render-repair/stage/work/gui-refinement/save_controller.txt | 2835 | 7c688230d28a420dac524e1dfc62d25d63d5d0956f2930151d1fa0144c38c1db |
| work/gui-style-delivery/Browser_Persistence.json | 523 | 41e558b9a40a5009078af36dd4bd41a2758741ccc9716d30c5fed71ed760a274 |
| work/gui-style-delivery/Persistence_Test_Report.md | 2213 | 28473d2c601d859712215aae36d3f97c7a2c3850d48bc462c8b36a901d94485b |
| work/gui-style-delivery/Reload_Startup_Failure.png | 53470 | 45739591e29eebb224833d88b8a39459de1aa7f277aefd63898b79d1e977c50e |
| work/gui-style-delivery/Repaired_GUI.png | 100225 | 044e37c23793feb3c50c93dbbeeae2edadc4dea919939a9978ff3a4bc52f67b1 |
| work/gui-style-delivery/Report.md | 2381 | 7256d9761870211d6d92f157c5efb22f53f3f19a25d6e1676fb8131a3047aaac |
| work/gui-style-delivery/app.before.py | 31930 | 6e9da89d40d6a2497ff3436386231a5b6000bd1639627b17fddef45963d6fb78 |
| work/gui-style-delivery/browser-fixture-0ek8ft3q/library.sqlite3 | 28672 | eb22b03775e9b66b3bdbb74e174ddc8e36b4fc8e1edc3e46a3be14963631932e |
| work/gui-style-delivery/browser-fixture-0ek8ft3q/rack-workspace.json | 327 | e658f0497baf78aa0ef4a0c9b6f0ef46887e74176512d3bcacb04eb99ceb862e |
| work/gui-style-delivery/browser-fixture-rp_mi71z/library.sqlite3 | 28672 | eb22b03775e9b66b3bdbb74e174ddc8e36b4fc8e1edc3e46a3be14963631932e |
| work/gui-style-delivery/browser-fixture-rp_mi71z/rack-workspace.json | 327 | 42765aa48b2340753b02e32372d5cdcbc9891fa432c6108bc2175027800cce0c |
| work/gui-style-delivery/browser-http.log | 8436 | 39c9d5d9372b76af18dcc89e887de533bb8a2320210cfa0293f92183ff3cd375 |
| work/gui-style-delivery/data-before.json | 2455 | 38f61fd8a7d5a29c3bd2cb86f61ea2418935b3185e32a87d88a22c8e60d4ae1d |
| work/gui-style-delivery/disposable_server.py | 1474 | c9b3a3413507642c67310f57e97f18a9169fff6a61d6fbbb1db5c650e8f5180c |
| work/gui-style-delivery/server.stderr.log | 3222 | 8642df3fbe7a28b0917258363e19000a20658e54e5894b2fd47aef8a032bbd9d |
| work/gui-style-delivery/server.stdout.log | 125 | ac82f41376ff4a57787f491712d9925a7baed86000383357eab942ab893d68c1 |
| work/gui-style-delivery/test_persistence.py | 2637 | b9fef3e5274297a1bf5ef6990f36f0412813e5d4f45e80813c1545d703591802 |
| work/gui-style-delivery/verify.py | 1964 | 578e6cdf9c49a24180eacd4a0a53fad5f5a9eba796b7b8500f2a5b3ba011a390 |
| work/rack-branding/Browser_Reloads.json | 277 | f885b5930ee30443b0c66c4b4ea29c60ace68f670c227922aa4ced45b80f542d |
| work/rack-branding/Logo_Custom_Post_Labels.png | 80278 | a5d35ff653afaa0bc7d20738ff99b786b5cf9125fad7a4f91040d5b12a742645 |
| work/rack-branding/Normal_Branding.png | 127140 | f0a3ae8abed7865ecd3608a685697958931580e7406e1c4c852dd08ffdb88e7a |
| work/rack-branding/Post_Labels_Off.png | 80584 | 26484ee5d0258ea49e159e9a8a9d5d053d95e49c950c057468e866bee2086a7d |
| work/rack-branding/Report.md | 4102 | 7f7cfe0ae8652f96099f757899c5973ddc517eb74b0565d927488fd60c908405 |
| work/rack-branding/before-app/app.py | 33006 | aa601703400bdb2f583daaa86785b837b8c5e732a2dea8b20a95efcae27b85a2 |
| work/rack-branding/before-app/assembly_records.py | 10545 | 350d51c9206d5db43d29b9b3075c3cb69d183c6a4d6bc77f939f6ca64299d696 |
| work/rack-branding/before-app/asset-manifest.json | 6111 | 936e87dddf71f14f67acc68059641a564281d2e8bddf316ada8bb70819da7a23 |
| work/rack-branding/before-app/rack-studio.js | 25917 | 7a9d576326e7521210673314e1a57000282ca0d219d80142090a0e70382fece4 |
| work/rack-branding/before-app/workspace.js | 49748 | dca4c58264510ef4edd62ab83a02c8c8a38020116d3a6cf43c9b01ae7c55b9d0 |
| work/rack-branding/extract_logo.py | 1492 | 16a4e3465d8eefe9a8ffc160e4dea9566b998bba05aeeed034fed7a0429538c8 |
| work/rack-branding/fixture-0li3pv2o/library.sqlite3 | 28672 | eb22b03775e9b66b3bdbb74e174ddc8e36b4fc8e1edc3e46a3be14963631932e |
| work/rack-branding/fixture-0li3pv2o/rack-history/4d274e74-5d5c-46fb-82a0-023f1b2cc9ea.json | 399 | dd2e7920afee3a4f3eddd25df38fb5f016868b215f0190f038c8e684e21edc01 |
| work/rack-branding/fixture-0li3pv2o/rack-history/814b0610-fa71-440f-aa73-d43a9c9f20f2.json | 327 | 55a52533a5cd9bd0dc9acb9838dbb2e5e4010da5581b76eaebbb17a031fd1e22 |
| work/rack-branding/fixture-0li3pv2o/rack-history/c81445d0-8988-41ee-a511-8eb8eb9314c1.json | 398 | fac8ed1b04915a9362df05b2eff1bda54ce66b7d9e0e6a323b5946099aa4940d |
| work/rack-branding/fixture-0li3pv2o/rack-history/cf29af92-ab4f-452b-bcbf-58c7fe3d8da2.json | 398 | 62145b05123222583983bc5aad55999c3bcfa365c347ed1bba1213b7d3752008 |
| work/rack-branding/fixture-0li3pv2o/rack-workspace.json | 2504 | c50bd7f9cc447a2c1bd98bb21fd8379756e5dc365a576cd0b3e965c454793ddf |
| work/rack-branding/http.log | 17431 | d6db03a63c0f4190d3543491e5106372cc6bdffbf025728460a57e396d818ec5 |
| work/rack-branding/preview_server.py | 1098 | 25d4e932e70e64782f8887a4e3f93eff9e41fa5cda73b762346a568f25733391 |
| work/rack-branding/register_assets.py | 747 | b24b71cf959b22a306144059354b31dec5f847f6f2d0e3adb958939d669f6f7b |
| work/rack-branding/server.stderr.log | 3319 | 12def8510d33bb57c0ade286b3daa10ff184d0738d7e3d56a840229735b83ce2 |
| work/rack-branding/server.stdout.log | 125 | ac82f41376ff4a57787f491712d9925a7baed86000383357eab942ab893d68c1 |
| work/rack-branding/test_branding.cjs | 2161 | 97869f969d2b29f6bc48b818dbe0e75a126bb150e3807617410d14a1d975e02b |
| work/rack-branding/test_branding.py | 2227 | 5b01f6bc18cf87a64f7bb9b4a72f760342ccfff3e64b877b16e25724ca5dadfc |
| work/rack-geometry-recovery/Historical_Provenance.json | 920 | 8b9e1101dcc5f80281dc06b11aedb3cd02e06730f9f6bb968c739113263490e2 |
| work/rack-geometry-recovery/Preservation_Report.json | 779 | 741746a9a46c4007357fa1475fa5bf581c4c7e5e13e83bd05aaed0938f47b800 |
| work/rack-geometry-recovery/Protected_Data_Before.json | 2781 | dd56935b3b92e1c7e8609aa3f4ff0c62824c9c74a714f1536414c1111214ad35 |
| work/rack-geometry-recovery/Recovery_Report.md | 10356 | dfc0339c7209c5c09c09d0c52f3c4a658ccec411011a6a3d792edbc3808a7808 |
| work/rack-geometry-recovery/Reference_Inspection.json | 94425 | 0a2c97998df768f97353e994e02eb143110e372dc739d15287fb8b84cd80e3f7 |
| work/rack-geometry-recovery/Source_Manifest.json | 1334 | 422c1fc246052df04176a1d58caef4e2a8ab54461f3708759850570b5097464d |
| work/rack-geometry-recovery/Verification.json | 4641 | 7bfb73cb7a919b9ff47b2fe9ab2b9c02b39532716818180433c67060d42b87c2 |
| work/rack-geometry-recovery/before-app/app.py | 27529 | 807d4cb57e6ac1dcc4bc455eda25d07a16501febdbc7100ee5c2b55be559726d |
| work/rack-geometry-recovery/before-app/index.html | 28522 | 63983ff45427d82daed5d7a088eda5fd7d0a865d0fec2018f18739305d2f1bc6 |
| work/rack-geometry-recovery/before-app/workspace.css | 13316 | b6730766c9c3185ab30a4c8d5d106d004f9e9c33d5d46dd59a55ae018f4e47b9 |
| work/rack-geometry-recovery/before-app/workspace.js | 28136 | 37995129724205aff94386d6407b2beb69e1981e0e413fb068292e3f994728bf |
| work/rack-geometry-recovery/historical-creator/BETA_HARDENING_SIGMA.md | 1146 | f390d1dc45058d7d64f8414bb85877cb69187d31aab7e5450815209c92c0226c |
| work/rack-geometry-recovery/historical-creator/manufacturer_reference/structural_reference.json | 30690 | b25ac4971fe6631ba61d82c111a9527078933746912a912b8ed58f3dc2d551ae |
| work/rack-geometry-recovery/inspect_references.py | 9823 | ec5b5d920c3ac0b8f2eef5e0ea6e6c1f7c8e5a28c163a4f261e25ce87188d441 |
| work/rack-geometry-recovery/original_index_script_2.js | 213684 | 722ca95d6385957bbef17dc10ca91e80e82c62619b3394886a5d54d4233f7ff3 |
| work/rack-geometry-recovery/original_lab-rax-assembler-code-only_script_2.js | 213684 | 722ca95d6385957bbef17dc10ca91e80e82c62619b3394886a5d54d4233f7ff3 |
| work/rack-geometry-recovery/pictures/reference_0_0.webp | 60524 | 8c058f31823fcf8e00678e7f6a8d069284ad69d93a84bf43dbf40eac4035aa7b |
| work/rack-geometry-recovery/pictures/reference_0_1.webp | 127306 | 256d41a3041864229d72224da23119820372861204c12aef6dc72e2007277c4b |
| work/rack-geometry-recovery/pictures/reference_0_2.webp | 117798 | 61de108914c478bf6444fe72ec4bff435d8c3c6cc3b3565b5eee06e9cde411b2 |
| work/rack-geometry-recovery/pictures/reference_1_0.webp | 97522 | 12798038ec8e595e6b3f3f328dfc3ec4cacefc2e4013dfae5d934b57c94d4850 |
| work/rack-geometry-recovery/pictures/reference_1_1.webp | 130830 | b71de893e736f0e8d42eeff2e4ab60956a13248137c320844f5eb04b23ef893d |
| work/rack-geometry-recovery/pictures/reference_1_2.webp | 183492 | d7c81d67c3fca5d5bf6b18029f1dcc0c6c9242548cc637d5793bad8836a6913d |
| work/rack-geometry-recovery/pictures/reference_1_3.webp | 178334 | 70ba484410cf7d66dc44659eefa5584e12cbbfdd3c7ec83aa4e4850e3965bc13 |
| work/rack-geometry-recovery/pictures/reference_1_4.webp | 171964 | 8eb68e9ed8ea360a7d343b9f0dbc10e8a9c67d114ca5b8d4534021595ca7407f |
| work/rack-geometry-recovery/pictures/reference_1_5.webp | 158606 | 3b1d083f18093ccbc9303c4972d5b3409a79c8882b3bfbb63a2c78356711186f |
| work/rack-geometry-recovery/pictures/reference_1_6.webp | 138244 | 2af4a84e2566e37c92550397c69b1c1c06b4d8a48de0a104ab6025397745512c |
| work/rack-geometry-recovery/pictures/reference_2_0.webp | 182520 | eaf3ef9804c36ecd1e3447f88d14b7362a59e4fedc865df357fddc7fd9c8b7da |
| work/rack-geometry-recovery/pictures/reference_2_1.webp | 62806 | 2c22f4e80907e6bfbc16362cf43df01a7ed73d37fda93035466a820bb5d81b65 |
| work/rack-geometry-recovery/pictures/reference_2_2.webp | 76806 | 58e28a82ba59d5d5e05573b022424e056b14b13ec52caec2049290bf68461e52 |
| work/rack-geometry-recovery/pictures/reference_2_3.webp | 50466 | 308960c2d32b983661632ea532825f7f1339308f3c7188552927e4cddf7b15fb |
| work/rack-geometry-recovery/pictures/reference_2_4.webp | 111760 | e4eb30c0bec2ffa07b6588e61884e5d70c26343dfa507897f862e02b2f8ec57a |
| work/rack-geometry-recovery/pictures/reference_2_5.webp | 51600 | 380d378fcab1ffb3b3a2506dc08527c3d8b8734ec54f0c425da8716c871f4f7f |
| work/rack-geometry-recovery/prepare_local_reference.py | 3486 | 13513c4370ada86d308866acd8ef379491114fa7a4f38d30eccff220004f1370 |
| work/rack-geometry-recovery/sources/1U+Support+Extension.3mf | 1229976 | 26a9e3321e951f319c77450b79cfa5fd946abadaaf041fbc9343b37adcc756a8 |
| work/rack-geometry-recovery/sources/5U+Lab+Rax+X2D.3mf | 3250025 | 0372934444785bd36a6edd3f265fdd8a9c9cb27fd125df8eae49d7840d459ef6 |
| work/rack-geometry-recovery/sources/Lab+Rax+1-5U+Posts+&+Panels.3mf | 1575265 | 64e4eb982ce70d426777f55b133988a8d94eccbe9b067f9ceaef9b490afb01aa |
| work/rack-geometry-recovery/sources/index.html | 2213962 | 0400d9d26ef322fb193d73cc805e731f23231fb03b175171af88c5109cc1533b |
| work/rack-geometry-recovery/sources/lab-rax-assembler-code-only.html | 249831 | 842f6d8048fc7fdd23db3db52452151c8776969d1ce6066fa9b82555da5ed879 |
| work/rack-geometry-recovery/test_reference_ui.cjs | 3957 | a7522701e85eb7654e87fd4ed68856ca27b9ad05eb7a97bc27e32d9c2befc1da |
| work/rack-scene/After_State_Manifest.json | 1175 | f7388f913a02224f265f85e61ffcaacf3af0048073c6cdddd9f6d724ef2591f3 |
| work/rack-scene/GUI_History_Evidence.json | 7102 | e8be1597fed75828445a885c8500708ebef93abf23292b153d3bd6eb28250f91 |
| work/rack-scene/Normal_Use_Activation.json | 405 | 4bd492e58a70b7bff7678e93348f7920bf58146e7fc363d1b33eef419d8de2d0 |
| work/rack-scene/Normal_Use_Saved_Rack.png | 98462 | d22aaf7cb5c6a47566a50b9d117f1f93fdee96769aa573977d9327c2fb9495f0 |
| work/rack-scene/Protected_Data_Before.json | 1027 | f706d1aa5beb402a1a923df3c92b4b1ef47c514a62407202bc6e6807bf3738a3 |
| work/rack-scene/README.md | 342 | b5f38d319fd020813a13f1d40b4e5f76684a1e70e590dfd14092ad253375c5c1 |
| work/rack-scene/Rack_Mesh_Preview.png | 75619 | 4c41a108b34c7434b5a63edac33d8c1214626cc79e4e27a43d955598d3877455 |
| work/rack-scene/Report.md | 5940 | 60963ee20897063688e5ff36f6af8f81df52805b6ff3d29f19f1edb5b4d774c8 |
| work/rack-scene/Verification.json | 1485 | 0e9b9e7e48330ecd98cc4a82174eb5a34addaee62bc0e4147614806daaf345b3 |
| work/rack-scene/after-state/AGENTS.md | 5322 | 57c6e7091f017f8e6033b80e6ad37cbbd3ffe7fe0254c13fd6c8abe6f445ef19 |
| work/rack-scene/after-state/HANDOFF.md | 13008 | 691843dcc23917c6dc90eaf1a7e8fd4a844205704dd69358d224b58308fa2a64 |
| work/rack-scene/after-state/PROJECT.md | 5985 | f1a37aa1977fc2de064e9328fbf1b67e6fd779b010add65854e141638dedf7d6 |
| work/rack-scene/after-state/outputs/Mechanical_Design_App/index.html | 29833 | f44342b7d1aac3c596cdaa9a1c2a8a95a08b7cd5516a04343e1a9491c3c2ee28 |
| work/rack-scene/after-state/outputs/Mechanical_Design_App/rack-references/asset-manifest.json | 5494 | 566c31d91a5d336f19f4a9b53f131fc944db01d74be9521594d03d0f3ac79f20 |
| work/rack-scene/after-state/outputs/Mechanical_Design_App/rack-references/rack-scene.js | 7970 | 414214bcbf3f1f40ff7a6be0791741ec721cb3d9585cc4d148b1c68f7ff1c7d2 |
| work/rack-scene/after-state/outputs/Mechanical_Design_App/workspace.css | 14445 | 523272e481889185ebeeea2eb75df531a27dc6c88004ede3bc24e12d337473ed |
| work/rack-scene/after-state/outputs/Mechanical_Design_App/workspace.js | 27895 | b81ad216e2282e0a3844c56fd128bd4535b69944f0538f65c9f1d37847a2f467 |
| work/rack-scene/before-app/index.html | 29779 | 288ef9fed077b4351cede5d9960c56c218d324da727480dbe70b6dc38e4f7fa4 |
| work/rack-scene/before-app/workspace.css | 14445 | 523272e481889185ebeeea2eb75df531a27dc6c88004ede3bc24e12d337473ed |
| work/rack-scene/before-app/workspace.js | 28136 | 37995129724205aff94386d6407b2beb69e1981e0e413fb068292e3f994728bf |
| work/rack-scene/before-guides/AGENTS.md | 5084 | 48c98b418319d723e28f671e8d4ce981376a4629e9424015684abfe1c4923326 |
| work/rack-scene/before-guides/HANDOFF.md | 11961 | 2ebd930c4e511be41630c397b8d6c28afaa84f28fd2b8ee6eb1d966f10a40dc9 |
| work/rack-scene/before-guides/PROJECT.md | 5813 | 0b8f8aec055c3c6aa6ba7e4ab0f6f32f41f51208778cb9dd5b0dbeaf82ece6be |
| work/rack-scene/preview_server.py | 938 | b50b521d744b300482d1b82e05fd03d41e68424d09bab6eca4abb87cf783e6a1 |
| work/rack-scene/server.stderr.log | 2860 | 32c5ecb9b5167e23498717e4b5c25fea66166a87429cd5c8ee21f285e8ce2a80 |
| work/rack-scene/server.stdout.log | 58 | aa82a471bffbcd4869fde79af3cbe2778dd7599c981e0112faec4c3eb44b9586 |
| work/rack-scene/test_scene.cjs | 2029 | 26bee2e9f8039dba3c33151afe98169eb650ce81a8b414cda8a4ee6fb08b31c7 |
| work/rack-scene/visual-check-3h7kthpg/library.sqlite3 | 28672 | eb22b03775e9b66b3bdbb74e174ddc8e36b4fc8e1edc3e46a3be14963631932e |
| work/rack-scene/visual-check-3h7kthpg/rack-workspace.json | 300 | 3da3fccb16940eda9cd820240b9555a22f4cce2f1eaaa6fb7d507a9920e6ced4 |
| work/rack-scene/visual-check-4bhvm8v1/artwork/1eeb1edbdbf419e32046475331ad0cce38c43a896007087d11713089426c5084.png | 2217 | 1eeb1edbdbf419e32046475331ad0cce38c43a896007087d11713089426c5084 |
| work/rack-scene/visual-check-4bhvm8v1/library.sqlite3 | 28672 | eb22b03775e9b66b3bdbb74e174ddc8e36b4fc8e1edc3e46a3be14963631932e |
| work/rack-scene/visual-check-4bhvm8v1/rack-history/2f793b05-3bd5-4fd7-85ff-ce878b06b4a4.json | 5059 | 5b99009f4c197963dbdb498bef3991d5c20e39815c8a7f940f2225c3cc976656 |
| work/rack-scene/visual-check-4bhvm8v1/rack-history/4f01d2cc-7885-4cbb-aef0-9ee2702b557e.json | 4747 | 368d41fed5c9eea9119f4ba34d8a8f854627c65be838ec0429e4e73f245b980e |
| work/rack-scene/visual-check-4bhvm8v1/rack-history/afdf8144-b95e-4949-882c-2aa3916b8275.json | 325 | d7dc8973562fb0896b4b2b1b9ae2af486f6a88493b4dda00b84aaa3568258418 |
| work/rack-scene/visual-check-4bhvm8v1/rack-history/e3456b10-590c-4626-bdea-7f4e0a28c50b.json | 2431 | d22e1c948c04f5ea32b462cbcad008504ddb96772c4ae92ae5b8649f3e52e810 |
| work/rack-scene/visual-check-4bhvm8v1/rack-history/e7c806e3-fbe9-4be8-9a03-32e49d9aaff0.json | 5059 | f4a8c7ea957ec1319ad353b1e15c5122dd7a854facd2609c579f23018a65e198 |
| work/rack-scene/visual-check-4bhvm8v1/rack-workspace.json | 7158 | b4f4d1908abc3306637634e8c62d385e189096a270afafdfe41158dcf8462ff6 |
| work/rack-scene/visual-check-cdiaueel/library.sqlite3 | 28672 | eb22b03775e9b66b3bdbb74e174ddc8e36b4fc8e1edc3e46a3be14963631932e |
| work/rack-scene/visual-check-cdiaueel/rack-history/571dd054-4868-4b18-9494-6390d119c989.json | 765 | 4d25a4d6a422f70d1abb5ef3e3beecf90a853d8a4981894af72618e0b3c7cb35 |
| work/rack-scene/visual-check-cdiaueel/rack-history/852e0fd7-38e0-4506-b835-708e9d620528.json | 543 | 21396cf2a26fc205664dae3bae298ee24682ddeba252610c110abf6a8ebb2b2b |
| work/rack-scene/visual-check-cdiaueel/rack-history/8616f703-6108-4df1-8cea-585959d1bb01.json | 543 | 8abb5ccadc72c9920e43193d9b3eab67524e5313fddbf7f130ca9854db6b9d08 |
| work/rack-scene/visual-check-cdiaueel/rack-history/d72a95fb-59a1-40d2-a802-487395717dd1.json | 300 | 850a8bc3c4635249c5a43dbb307a51743032f0bab0ea207aff6405f9e306facc |
| work/rack-scene/visual-check-cdiaueel/rack-workspace.json | 762 | f10cd3b33832c10ecc5417313dc58e3c783f02810cd32ad918411acedf9e5005 |
| work/rack-scene/visual-check-o6bh5dvy/artwork/1eeb1edbdbf419e32046475331ad0cce38c43a896007087d11713089426c5084.png | 2217 | 1eeb1edbdbf419e32046475331ad0cce38c43a896007087d11713089426c5084 |
| work/rack-scene/visual-check-o6bh5dvy/library.sqlite3 | 28672 | eb22b03775e9b66b3bdbb74e174ddc8e36b4fc8e1edc3e46a3be14963631932e |
| work/rack-scene/visual-check-o6bh5dvy/rack-history/79192a00-48ee-4f34-bb16-23539c203ce8.json | 6760 | 7f3dd62d2804894fc2a5ec78477afd5292899ba780fe8de40f6dd140a6e302bc |
| work/rack-scene/visual-check-o6bh5dvy/rack-history/79807f4e-9ccd-442f-91f8-99aa9452883d.json | 4661 | 9bde840e5e7699cfe9093122da5bc9740d14319f734b7077859e1d1b6500b2ea |
| work/rack-scene/visual-check-o6bh5dvy/rack-history/8b0909d4-eaac-49d3-be67-1f73bdf2015c.json | 2431 | 830edca5e5a735cb239fa530cd4d887f3c09a1fc12a625353d6b80e086b325ae |
| work/rack-scene/visual-check-o6bh5dvy/rack-history/954cb9ce-22bf-4a55-ab03-4910876ac742.json | 7161 | 7e67f40d2705378cdb79cb882578cd6c9539e22eec83a51ff14fce0e357e9699 |
| work/rack-scene/visual-check-o6bh5dvy/rack-history/c37cdb3b-9505-4358-8973-70eaa86e5277.json | 7264 | 02aa8b3bffe7760490a1138ccb83bceabc3d3f865ade8d0d7ec8d591e6be434c |
| work/rack-scene/visual-check-o6bh5dvy/rack-history/c5b88364-1421-48f7-984c-fc6fd3108704.json | 325 | 677b4b7c07e9ffc0822be1261f4c03564fb79749276436c15c88a9f46ceade02 |
| work/rack-scene/visual-check-o6bh5dvy/rack-history/e1ff8714-e673-4af1-b8ff-52cdaffcbe66.json | 7264 | cdd93ecaeff79e935b91572b194dbda257ee9001c33911d8b0241e07ceb1ebcd |
| work/rack-scene/visual-check-o6bh5dvy/rack-workspace.json | 7316 | af3f37514cdb3d13dd699ee02f5493454fae1a02f4bacc5c508fc344b26434f6 |
| work/render-studio/GPU_Checks.txt | 654 | bce805177172d596e4bd45ecdc488ae98410fd4efec5074935f16a0307a0f23f |
| work/render-studio/HTTP_Checks.json | 1517 | 0408f46c9c851000c88adad10783b092e2cbaa906ef5c5359d19ff11725ba8f7 |
| work/render-studio/Hardware_Detail.jpg | 62720 | 3954a90cbfaaa8d3ad3ac7bd59f08d68def3027412b5fbe5ef678a9141763095 |
| work/render-studio/Report.md | 7019 | d6fed129348bc7920141db898864e9166396a683c0a9b22a3c17d2ea94fc6291 |
| work/render-studio/Studio_Render.jpg | 94888 | c0af4643214a5ed522d7323f94a964f123a9a9a7d0718295964d9bd710b7f674 |
| work/render-studio/Workspace_Render.jpg | 86696 | a4b0e6e48317f036f62778f763812547cfd15c76f6378841d8d9aed20eb0869a |
| work/render-studio/acceptance-vsqzrl6w/artwork/e8740124844fe91e7f8d5240c27977eddc52b2080f437bbb0be587e3e3c59fb0.png | 877 | e8740124844fe91e7f8d5240c27977eddc52b2080f437bbb0be587e3e3c59fb0 |
| work/render-studio/acceptance-vsqzrl6w/library.sqlite3 | 28672 | eb22b03775e9b66b3bdbb74e174ddc8e36b4fc8e1edc3e46a3be14963631932e |
| work/render-studio/acceptance-vsqzrl6w/rack-history/821d228c-5e7a-4bb2-a9ed-e8876d7acf75.json | 1351 | f52d2bc87a7d0e3b56881c3c85ef300e064f6f4d457f8a78caf20e725988bc96 |
| work/render-studio/acceptance-vsqzrl6w/rack-history/c502b3e4-ee4d-4fed-abb6-8154cdf4106a.json | 2464 | d36da12d0ef7bc5fe6e2faf7f92afc1cf7e58c5bf6c5ef87b4d8f1e94e2427f4 |
| work/render-studio/acceptance-vsqzrl6w/rack-workspace.json | 2779 | 4b5a886874333dfb07f2ef42671b3dc759524a1bbc494a68b4cedb61e8e1cf53 |
| work/render-studio/acceptance-y4diwimh/library.sqlite3 | 28672 | eb22b03775e9b66b3bdbb74e174ddc8e36b4fc8e1edc3e46a3be14963631932e |
| work/render-studio/acceptance-y4diwimh/rack-workspace.json | 1351 | 2856db27892a4204ac874e96f60c6d6f38be06b718e3205596b18401114e5da4 |
| work/render-studio/before-app/HANDOFF-before-closeout.md | 22065 | ba89deb7b0e0467098d446a56cbd5166fff6b4aee3674ac573d4b135108742d6 |
| work/render-studio/before-app/asset-manifest.json | 6343 | ef3ffc266fc5d63a22fdcbcf4c24899a5b52de98f3ebc1e94f34fe868bf32cef |
| work/render-studio/before-app/index.html | 31717 | 5e90c8156c8fe242917a1ff5b494fd300a499893eed2bed64e750e53bf658efc |
| work/render-studio/before-app/rack-scene.js | 7970 | 414214bcbf3f1f40ff7a6be0791741ec721cb3d9585cc4d148b1c68f7ff1c7d2 |
| work/render-studio/before-app/workspace.js | 39174 | c171069729efae44d97cc8022e58ca76a6da4ffada5e7f329ee93442d9ef3ff3 |
| work/render-studio/finish_workspace.py | 1905 | 163a6abd22c43a45038a2ff2ed87f42c8d62e9c9587c20492851ccd17d88b014 |
| work/render-studio/integrate.py | 2983 | a389331b6991691f36b2f4edaba043efc4971c7b6cec356357fad18d33836fec |
| work/render-studio/preview_server.py | 1471 | 80c7d05c3ee9f7a2f53af590738f6dea35ca01071290b834283d48445c24b750 |
| work/render-studio/recover_hybrid.py | 1845 | f43437e2f54642783552b74edcc54f81f1b8aeed6edd9db458a5f8701f497a8b |
| work/render-studio/refresh_manifest.py | 773 | 21d01b9059d028ba121755c5649d33acb7135159e118d813b7404a56ecef99ca |
| work/render-studio/showcase.html | 11147 | 412852b526c8deda0c4da305ad22c63bef30025ca4b16ef8aa5546c582da5624 |
| work/render-studio/test_assets.py | 2693 | 3dea705b34dd4cf77bc53eba81fcc65faab9309b4045ad0f4c3146b4bab70b34 |
| work/render-studio/test_studio.cjs | 4066 | a2f68f87b60bfa342993b2d5b9edfe3e4ef7ec4b02ac833ea7e6a838fb4100a2 |
| work/render-studio/verify_runtime.py | 1347 | b80587c6cea37bc8dcefdc402463fbc2c623a4dd1f3ca6f8d14cc35492e7af65 |
| work/startup-reliability/Browser_Checks.json | 25769 | 57ef46dd0465a0bf2fc0d08c38efd0557599b0ef1dcb15aa04abe3f9ccee7091 |
| work/startup-reliability/Normal_Startup_Verified.png | 106046 | 63e426997437e39db308766f581cdc31560269c17cfc82a68d84b410df72520b |
| work/startup-reliability/Report.md | 3584 | d7357f5106b69375d901fda2211eb102e915ac41637d5b3a3a619656f18fbfc1 |
| work/startup-reliability/Verified_Startup.png | 74827 | 46a7a9dc50b01f211b33009145024a18e835591bc8d7faaad0e252e5b868f2dd |
| work/startup-reliability/before-app/app.py | 32400 | c19b36a3a59e3c0023b64a375898b39c5726a84eb87ba005e492361b3d74da34 |
| work/startup-reliability/before-app/index.html | 31904 | 65657eebce320805db5eefb89223e3f3a8063fcbdc2738b3214195999b7f5547 |
| work/startup-reliability/diagnostic_server.py | 2914 | 94e174512de58ef73b8227ad18ee4c1b9795669abaf44f74294807bc47bab624 |
| work/startup-reliability/fixture-8sibra32/library.sqlite3 | 28672 | eb22b03775e9b66b3bdbb74e174ddc8e36b4fc8e1edc3e46a3be14963631932e |
| work/startup-reliability/fixture-8sibra32/rack-workspace.json | 335 | 90835ff24439b25ba3b858f152841c533dd5f03bf34306467691a289688e3f5c |
| work/startup-reliability/fixture-9e81z4yf/library.sqlite3 | 28672 | eb22b03775e9b66b3bdbb74e174ddc8e36b4fc8e1edc3e46a3be14963631932e |
| work/startup-reliability/fixture-9e81z4yf/rack-workspace.json | 335 | 10374d6d3340dbf050a15a3c12a438f95d96573d79e9a3a506dd5da12ac6924b |
| work/startup-reliability/fixture-flmnqasn/library.sqlite3 | 28672 | eb22b03775e9b66b3bdbb74e174ddc8e36b4fc8e1edc3e46a3be14963631932e |
| work/startup-reliability/fixture-flmnqasn/rack-workspace.json | 335 | f62f27a77ad743f487aa2a9f5c729e8f2b2bef2e2cae33c955b89aa09637c55b |
| work/startup-reliability/fixture-ldx680bo/library.sqlite3 | 28672 | eb22b03775e9b66b3bdbb74e174ddc8e36b4fc8e1edc3e46a3be14963631932e |
| work/startup-reliability/fixture-ldx680bo/rack-workspace.json | 335 | 0eb0b582fc28ef04cbc6bb855c89d0dbe495fca09180ccfe00809ba56df1a85f |
| work/startup-reliability/http.log | 191401 | c3691ef470d0aa5994499b58a3753254842956f4b8a780887916a65c0541d530 |
| work/startup-reliability/server.stderr.log | 3222 | 423108cde9b3e0101296fa916440d0d21384d7421c017e44660bcddc5ae10623 |
| work/startup-reliability/server.stdout.log | 125 | ac82f41376ff4a57787f491712d9925a7baed86000383357eab942ab893d68c1 |
| work/startup-reliability/test_startup.py | 4602 | 8c05b02ed19ad4d708bad1306502e99020ec8fee6b6dd7f32d3c698e51644516 |
| work/startup-repair/Data_Before.json | 1027 | f706d1aa5beb402a1a923df3c92b4b1ef47c514a62407202bc6e6807bf3738a3 |
| work/startup-repair/Repair_Summary.md | 401 | 51b2e53546a0b358b0b9126596d0db0e744ab20d997f6355b1cc77dfca017ec7 |
| work/startup-repair/Verification.json | 1225 | 4003b4cdb770f0dea54053a1183866c1add586292d75c9711c23f5ba6d9bf4f0 |
| work/startup-repair/before-index.html | 28564 | e23c49d371731cca09c589ca3eb03093618e4fbdd4b3a84244fa869e22087bdf |
| work/startup-repair/before-start.bat | 132 | 569bc3faea21f6b383b7c54f00651ac70295ce2c54e3a950fc4070e50b8bbcf1 |
| work/startup-repair/index-after.html | 29779 | 288ef9fed077b4351cede5d9960c56c218d324da727480dbe70b6dc38e4f7fa4 |
| work/startup-repair/server.stderr.log | 4564 | b8d3923cfd4435805990d221acfe4fdac3694b4edbeb82b2feff4d61e219c0c0 |
| work/startup-repair/server.stdout.log | 125 | ac82f41376ff4a57787f491712d9925a7baed86000383357eab942ab893d68c1 |
| work/workflow-audit/After_State_Manifest.json | 2281 | ae8fc5cc76777d94bfa0f3284bfdd0009c9c328e33e652f2ed447893931a86fd |
| work/workflow-audit/Allocation_Controls.png | 81310 | c2aeb397f0c4482254fe2a890ecef80e5128921e8e9967a084fa29bb13e911e7 |
| work/workflow-audit/Protected_Data_Before.json | 1139 | 89519801a29aec88c4ab609f88041e3d31a6990738c34558d85ebb6cb3010ea8 |
| work/workflow-audit/Report.md | 6165 | f905ad18d3d97ea35264e9f16a68eb48c4698c98ee54fa6a8ccfc1690dabeec7 |
| work/workflow-audit/Verification.json | 1533 | 95590c4b723d6b8336c69227ce0e289a315fc12ca23c14944b138dc25ea26939 |
| work/workflow-audit/after-state/HANDOFF.md | 14349 | e3caac2a832e10dece9756da7b2da97b6dfad38d85139db04f4e3937146f9cca |
| work/workflow-audit/after-state/PROJECT.md | 6330 | 3afd6a21e181c79132963d3ac0ca6810ffc3329a727ddb114b372691413e8372 |
| work/workflow-audit/after-state/data/normal-use/library.sqlite3 | 28672 | fdc694c09c2eaf099a3f2262bd03360b42746ecbf30571d263c6351319dc3bfd |
| work/workflow-audit/after-state/data/normal-use/rack-workspace.json | 311 | e2b6f55acfc6e84300cb761981d2ef2eb0fbf22548ea6ae9b1e4ad7b2589b53f |
| work/workflow-audit/after-state/data/normal-use/revisions/ebd6af3164685923c661c7965badd932d98ed6c1da9bfc51742fe934f6a68a78/assembly.json | 310514 | 7c1eab70129e10a7cfdfd5fad23054b4ae2d8db340268ed38e7381c632fba3b1 |
| work/workflow-audit/after-state/data/normal-use/revisions/ebd6af3164685923c661c7965badd932d98ed6c1da9bfc51742fe934f6a68a78/faceplate.stl | 204080 | 1c1512d35979ad8821f07851c5a15ef8306f5f4800d6efb39ce6eb52a64e9906 |
| work/workflow-audit/after-state/data/normal-use/revisions/ebd6af3164685923c661c7965badd932d98ed6c1da9bfc51742fe934f6a68a78/pi4_proposed.scad | 3512 | e673df53fd2d33ccb5f19494a6ff6f9965e2c05389ad8d606cc33787921cab50 |
| work/workflow-audit/after-state/data/normal-use/revisions/ebd6af3164685923c661c7965badd932d98ed6c1da9bfc51742fe934f6a68a78/revision.json | 5648 | 96b123d39c86b0a646544270984a1fa6886f47bea410e2b069c709cc53958fb3 |
| work/workflow-audit/after-state/data/normal-use/revisions/ebd6af3164685923c661c7965badd932d98ed6c1da9bfc51742fe934f6a68a78/tray.stl | 1709434 | 6ca66dca84d4abd4f1b9f5f56dca152b84dabc581dbb5f38d4a577e0ce875d04 |
| work/workflow-audit/after-state/outputs/Mechanical_Design_App/index.html | 29888 | 8c9adb7a270109a3a5cdde79c95ac36420817d324e7fa9fb9d4499a61fd6153b |
| work/workflow-audit/after-state/outputs/Mechanical_Design_App/rack-references/asset-manifest.json | 5697 | 035508d3a046467516218293dab659e4637ac80980eeb77e99fd9564e4afb912 |
| work/workflow-audit/after-state/outputs/Mechanical_Design_App/rack-references/rack-layout.js | 1737 | 15ee6ff1533c49ffee49cac7a66d8e30278ffaad30ba42f94eed936e1e76c5e4 |
| work/workflow-audit/after-state/outputs/Mechanical_Design_App/workspace.js | 30812 | 1a6efcdc1133e2e9318e2e73410c2b123f0d7fddce4a6f611c207b99756b1d90 |
| work/workflow-audit/before-app/index.html | 29833 | f44342b7d1aac3c596cdaa9a1c2a8a95a08b7cd5516a04343e1a9491c3c2ee28 |
| work/workflow-audit/before-app/rack_workspace.py | 5174 | 4f51105a8030ef60fe642f68808a9e70ea72c6ab82fc715733642751003a0cc9 |
| work/workflow-audit/before-app/workspace.css | 14445 | 523272e481889185ebeeea2eb75df531a27dc6c88004ede3bc24e12d337473ed |
| work/workflow-audit/before-app/workspace.js | 27895 | b81ad216e2282e0a3844c56fd128bd4535b69944f0538f65c9f1d37847a2f467 |
| work/workflow-audit/server.stderr.log | 9082 | c0351cb9cdcaa870e75e52d02620a344f463644380dc3f0175439c7ab1cab250 |
| work/workflow-audit/server.stdout.log | 58 | aa82a471bffbcd4869fde79af3cbe2778dd7599c981e0112faec4c3eb44b9586 |
| work/workflow-audit/test_layout_actions.cjs | 1172 | f3f9d7a56db1a5cf13b37ba80427eb7e574a6eba293fa67393bddbf6cfe2e279 |

### Changed since earlier manifest

| Path | Earlier SHA-256 | Checkpoint SHA-256 |
| --- | --- | --- |
| AGENTS.md | 48c98b418319d723e28f671e8d4ce981376a4629e9424015684abfe1c4923326 | 672bef13f690debab88a1ec63844214f3c2a386af7766da20d79af03ffa996a7 |
| HANDOFF.md | 75c7528c849ae5b7ca534d7c24f771fe4dedf62399d3c815a12655b1c4083816 | 1dc6e7fc7a2ea1263fb07ae655553a21abd150dd01799ca02d321e2fb3b3e923 |
| PROJECT.md | 1d10c4952c60cd26ac2c9c244890dd0dc59cdef18f68a2303f3ac0c1c2eed734 | c5e76a66f80cfeda7af4c5370bfac62a06653ad6383ec794032016aa679f3401 |
| outputs/Mechanical_Design_App/__pycache__/app.cpython-310.pyc | 2c8cef35d4b4329d52525dfdb3b629b83ea09add79303797b494fa5b0049b3cd | e41e4752e3ef0fc1a9fd5111cf8d2ca028b4076793d4375c2fce6e58c6b24379 |
| outputs/Mechanical_Design_App/app.py | 807d4cb57e6ac1dcc4bc455eda25d07a16501febdbc7100ee5c2b55be559726d | 2c2abe8d3ae00160eff542e3456a1c431fa662e33160efd9ed8f0144ac32053e |
| outputs/Mechanical_Design_App/faceplate_mounting.json | 9d056b5e459a81f6375417d02ee4b50996b4edfe3de6d389a05ecda37adb56fb | ccd36dc258033fed8d41263d40e656e8f7ac8f9d868f69d00c50f1ec6e95adf7 |
| outputs/Mechanical_Design_App/index.html | 63983ff45427d82daed5d7a088eda5fd7d0a865d0fec2018f18739305d2f1bc6 | 51c015f7e9fe82be46706fb1afc2a21e58f1f89e40c882b1ede26343a83c4b1f |
| outputs/Mechanical_Design_App/rack_workspace.py | 4f51105a8030ef60fe642f68808a9e70ea72c6ab82fc715733642751003a0cc9 | a565c2217bb6a31eb59f7e7069820612cbe205745c12412ef2ac0f46855209da |
| outputs/Mechanical_Design_App/viewer.js | 34b90db810a0ee11d463231ee814c957c013e3cc30112cb30042e3db0222f46f | fe12b8b73915490bf47233eff8aa798bce0f6eab49220ab0814fba200674f87f |
| outputs/Mechanical_Design_App/workspace.css | b6730766c9c3185ab30a4c8d5d106d004f9e9c33d5d46dd59a55ae018f4e47b9 | 0cc5281b2dcd84cd08e928148931e57198e33afa26bb87c57ed839539ed7fd8e |
| outputs/Mechanical_Design_App/workspace.js | 37995129724205aff94386d6407b2beb69e1981e0e413fb068292e3f994728bf | 1f2723d7dafb19e245e2ba24e2f851a6f7bcb1053a35eff4720ae04b229b80f0 |
| work/gui-restoration/Restoration_Report.md | 9b1e0d8f5917e9f2bf37234172b5bad3c9f21d5b9880701a4b3f125462e2ac8b | 3ecfb99b16319c6a12fd9c6c6bc3645bbb2131ce452cba51912c31eec9048369 |
| work/test_viewer_v08.cjs | d1f641afa1ec89a40406dc00362502cf5fa64c7f2e917b127bdff8b8b6d6c1ad | b89764b8175e0483a3087fe45cb8caac2f63f63f65d2e71fd918e3439c405808 |

### Missing at earlier path

None.
