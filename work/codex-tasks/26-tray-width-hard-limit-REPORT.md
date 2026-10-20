# Task 26 report — 2026-10-20

Implemented a 204 mm hard tray-width limit including the 8 mm border and sideways offsets. RACK_INNER_W=208 and SIDE_CLEAR=2 are PROPOSED defaults; MAX_TRAY is derived. They live once in equipment.py (Python), tray-placement.js (JS), equipment_tray.scad (SCAD). Wizard uses TrayPlacement.widthProblem for import warnings, Save/preview/export guards and the saved-item warning. Rotation is suggested only when the rotated footprint with its offset fits; never applied automatically. Raw equipment dimensions retain their existing input ranges so a wide device can be rotated; the effective tray envelope is the hard manufacturing limit.

Tests: 194.5-wide OptiPlex rejected (210.5 mm tray) with rotation hint; 90° rotation passes (198.5 mm tray); 188+16=204 passes; 204.1 and offset-induced 204.2 fail; generic 85×56 example passes. Existing data remains readable and untouched; over-wide builds are rejected by clean(). Frontend manifest hashes updated with LF normalization.

Commands: targeted Get-Content/rg inspection; Python stdlib archival/edit/hash scripts; run_checks.ps1 baseline was task 25's final passing run immediately before these edits. Three task-26 check runs: first exposed old error-text expectations and missing test-harness dependency; corrected within allowed tests; second and final pass. Final: 121 Python (one pre-existing render skip), all JS pass. Log: docs/archive/codex/2026-10-20/task26/checks-final-2.txt. No renders, exports, live-server changes, user-data writes or desktop control. One attempted test-file read found no file; used the actual wizard-mount-default.js harness.

Open questions/limits: 208 mm nominal opening and 2 mm side clearance are proposed; physical fit/strength UNKNOWN. Browser verification remains for Claude. No automatic rotation or rewriting of saved items. No commits/pushes under the task queue's explicit standing restriction.

Byte-for-byte originals: docs/archive/codex/2026-10-20/task26/.

| File | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `outputs/Mechanical_Design_App/asset-manifest.json` | fba3064e70feda6782dee7a073100e584a02243b2a8dcc140100a6704b7f39bf | 3ea95d5650ef2fb56ddff3c4ab1d1e9fcb9f7b79cad034766d18b66cd1aa1c86 |
| `outputs/Mechanical_Design_App/equipment-wizard.js` | f059c4ce4f2b00a01228b924b04feb480086654f0762e3b41fdc10d641864bd8 | fbe1ebd176e169c3e599896e43dd35973376a6754c6af9a6187049d274b34fe4 |
| `outputs/Mechanical_Design_App/equipment.py` | 5269150cbfeb07d7ecc31355cfdb6659242fbd58f7571f1d730e6ce17c0c93a3 | 845e39067004642bfaa96f5da644ea5488edcf57907a0267e35bedfd049bda8a |
| `outputs/Mechanical_Design_App/equipment_tray.scad` | 9a94a9d5c18d14f9af610eb2118b4ba163dd7d7000d1563b16087a728bd964d3 | 5cc525ad6edd0b15e7ab172f5df701f3b9bbbe9683d93b898b968f21eb989e42 |
| `outputs/Mechanical_Design_App/js-tests/tray-placement.js` | 0bae9a7687224439913c8196887a4d8df648db284b9d84897684927f2064fbde | 1acfaa016ed7976433c333411cba052296b3aafc12d272f3cf0669c1131d0cd4 |
| `outputs/Mechanical_Design_App/js-tests/wizard-mount-default.js` | 97e046ec01e20ead8f8ed3092f2d834009eee1b5bc7af6ca9c48a05fc01702a2 | fd6561729fa9d3aa9234bb37d07d3cb0b7f6dae8ce7806f5a4bac00775cb44e0 |
| `outputs/Mechanical_Design_App/test_tray_placement.py` | 9e2d21ba397e122ee9bd892f9f5c64ba102b9003e28b4f57b5bdffe1e0688699 | 4767bdd0f9bad486becf56f80d4ffc8edff53e41ca50d3462f952d1ee5966d6b |
| `outputs/Mechanical_Design_App/tray-placement.js` | 9f2ae9bf66fe8452785687524fdec7900bea65e1b5206bb0d3236cb778890055 | ade4bf4069652188d6cff18157f58c23a564177f8d2498c2d645fcd83c94aa74 |
