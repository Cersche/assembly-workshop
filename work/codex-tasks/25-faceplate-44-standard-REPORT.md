# Task 25 report — 2026-10-20

Implemented the 44.4 mm 1U standard with slot-bottom Z=0. New 1U bounds are X ±126, Z 0.025–44.425; 2U Z 0.025–88.875. Hole centres are 6.323/38.127 per U. No saved data or revisions were rewritten.

Constants: SCAD rack_pitch=44.45, plate_gap=0.05, legacy_slot_offset=1.225; Python RACK_PITCH/PLATE_GAP/LEGACY_SLOT_OFFSET in port_openings.py, imported by equipment.py; JS counterparts and plateHeight/plateBottom in port-openings.js, consumed by placement/wizard. Keystone centres use the full slot centre; golden profile/table and tightness are unchanged.

Floor and joint changes: equipment_tray.scad, equipment.py and port-openings.js now use non-flat floor 7 → 8.225 (old true rack height 8.225 → 8.225), floor top 10 → 11.225, default device base 16 → 17.225 for inserts/pegs/clips, straps 10 → 11.225. Flat floor remains 0.5 in source, correcting true rack height 1.725 → 0.5; device base 4.725 → 3.5. SCAD tongue, boss, riser, strap slots and rear joints inherit tray_z: non-flat tongue 10.5 → 11.725, boss centre 21 → 22.225, riser top 29 → 30.225; these preserve their true rack heights. Flat counterparts remain 4/14.5/22.5 in the new frame. Opening joint exclusion uses the conservative non-flat top 30.225. Height checks include peg/clip protrusions and screw risers. Port bounds include the 0.025 bottom gap.

Removed the entire task-23 template_source compatibility rewrite: all new generated sources now use the current template, including non-flat mounts. Archived sources and immutable saved meshes remain unchanged. Unified Python opening lift rules and removed the now-redundant equipment.py correction. Updated sketches, artwork placement, slot-span placement and keystone markers. rack-scene.js and workspace.js already use slot-centred placements and needed no changes.

Verification: session-start git pull reported already up to date (first sandbox attempt denied FETCH_HEAD; approved retry passed). run_checks.ps1 ran before editing (pass), after edits (initial stale boundary/hash fixture failures), after fixes (pass), and after new regression coverage (pass: 120 Python, one pre-existing render skip; all JS pass). Final output: docs/archive/codex/2026-10-20/task25/checks-final.txt. Commands also included targeted Get-Content/rg reads, git status --short, and Python stdlib editing/hash scripts. One initial PowerShell brace-list search had a parse error and was rerun with explicit paths. Tests use disposable data; no OpenSCAD renders, STL exports, server restart or desktop control.

Limits/open questions: actual STL bounding boxes were not rendered (source formulas and sketch bounds checked). Claude browser verification remains pending. faceplate_mounting.json remains historical evidence mentioning 42 mm; faceplate_color.py remains unchanged and unavailable for generic equipment. Its legacy geometry remains reachable only through the guarded legacy path, not wizard faceplates. Physical fit applies only to Brian's coupons; other fit and strength remain UNKNOWN. Existing unrelated working-tree changes were preserved. No commits/pushes under this task queue's explicit standing restriction.

Byte-for-byte originals are under docs/archive/codex/2026-10-20/task25/. SHA-256 below is over actual file bytes (manifest hashes separately use LF-normalized source).

| File | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `outputs/Mechanical_Design_App/asset-manifest.json` | 5ff8980f3babd2bef080927dbf0c1fcbf0f04f3d3e3e7f1ca812d0069aad8a16 | fba3064e70feda6782dee7a073100e584a02243b2a8dcc140100a6704b7f39bf |
| `outputs/Mechanical_Design_App/cable-ports.js` | 1df78e24bba2b7929ddc77c1322a37c47fa111a1d5173bdf0f3050618adf5632 | 47c158f76909659dc7b4ac22af5623b6d025b076c39f3d545a9d8a505d6e06fa |
| `outputs/Mechanical_Design_App/equipment-wizard.js` | 87695b32b719db7999494ecd76c05c9b41d77d020046aff2232bdb9388fce06d | f059c4ce4f2b00a01228b924b04feb480086654f0762e3b41fdc10d641864bd8 |
| `outputs/Mechanical_Design_App/equipment.py` | cc722910da57641a6da6ef67ea9f95548ae885207549992ec3376151eaf81210 | 5269150cbfeb07d7ecc31355cfdb6659242fbd58f7571f1d730e6ce17c0c93a3 |
| `outputs/Mechanical_Design_App/equipment_tray.scad` | a51f4a6d4fcd586c4e1d63db84ff6c8662277ab06775a90ad5b5e5e411f11c77 | 9a94a9d5c18d14f9af610eb2118b4ba163dd7d7000d1563b16087a728bd964d3 |
| `outputs/Mechanical_Design_App/js-tests/flat-floor.js` | 07d52fd198da37b4350f79e2ef2702f1113951959e316a4f0eff88328ab95228 | 73541a9b52d854deabc23bf63d85114c77f43f4acf2cb9edba6459af0afe35a7 |
| `outputs/Mechanical_Design_App/js-tests/port-openings.js` | 4ab3556f8f7e10a5a2b42f230e598d127470d5fb40d3205d4b4ed4cfb1b4a39c | a9e59c6a871fd8a63de4045e2e173bbce83a2b68924838ad4d35677bc2e9803b |
| `outputs/Mechanical_Design_App/js-tests/run.js` | a2df72dd0c0f5fbdc858d3f583f8e49612a5c52deb0a45d11214d5b467e3a24a | b0d1c0ec60f8ec34f7448890e9a8b4d2e8f965089774ec12bd347dd49397759f |
| `outputs/Mechanical_Design_App/js-tests/tray-placement.js` | e1b806b13b1e2e453dde5905f48832cb7ff6d5892a85183194bed1ccc45717e1 | 0bae9a7687224439913c8196887a4d8df648db284b9d84897684927f2064fbde |
| `outputs/Mechanical_Design_App/port-openings.js` | 0a68b93f05732d0f7d1028f45c0fdff8c171f90a7e49aa94f6e7819b7ccdb845 | 7f45d17cd18222b75d3f23813b2c232b2ec179241acd80c978d3dcc9307ff245 |
| `outputs/Mechanical_Design_App/port_openings.py` | bc0a82e5d850ab6a79452d5f24c8aa834e3ae46a37faac12d1a685614301f276 | b7940267afa880852b60b7e48ca878d1cfda32eef9e904ce159a57e760c5c4ee |
| `outputs/Mechanical_Design_App/rack-studio.js` | ab296315ab0ae9ce168983187dc06981754608eda5817d094fa32f27c92df74a | 060060b7698d7d836d2dccedac8c06dfce015128b35c635ad00f04a43fbe3e4f |
| `outputs/Mechanical_Design_App/test_keystone_mesh.py` | 5ed17018bef865dcd8ea3b17fc0b1ac3e0eae176e5c7dc546d5e893008d74d41 | 89889dba05aa7ab86488af47f57f7a5f935bf3c28f3c10bfd8b20b90ad3ae46d |
| `outputs/Mechanical_Design_App/test_tray_placement.py` | be1f4e8b14ceb6a520c74464b6578476b6ccad1c050ac009552ae61339271821 | 9e2d21ba397e122ee9bd892f9f5c64ba102b9003e28b4f57b5bdffe1e0688699 |
| `outputs/Mechanical_Design_App/tray-placement.js` | e7df6306a0638f78d79fd54a8a2236d6151bc34fd5d1bf7ba1144cad255888fa | 9f2ae9bf66fe8452785687524fdec7900bea65e1b5206bb0d3236cb778890055 |
| `outputs/Mechanical_Design_App/viewer.js` | aae1dfe7bdd022fc68f33166c5c76018ddaf3be32e39db395219c92ec8ff8440 | 7f3844b306744f930c74b502f9004a430555a6de1a8883ea6ff6ac279c2e0e16 |
