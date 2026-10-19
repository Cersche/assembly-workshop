# Data locations — C4 unresolved, facts only

2026-10-18 inspection. Files were hashed/read in place; each SQLite file and any existing sidecars were copied to a unique external scratch path. Only copies were opened with sqlite3 mode=ro and query_only=ON. No source database connection, schema/data mutation, app request or live-process inspection occurred. No journal/WAL/SHM sidecars were present at the initial checkpoint. Copies matched source hashes at copying; without a coordinated live snapshot this does not guarantee application-level consistency. Disk JSON does not contain unsaved browser drafts. No merge/switch recommendation is made.

| Fact | data/normal-use | outputs/Mechanical_Design_App/data |
| --- | --- | --- |
| File count | 14 | 6 |
| Total bytes | 2320342 | 468391 |
| Database SHA-256 | fdc694c09c2eaf099a3f2262bd03360b42746ecbf30571d263c6351319dc3bfd | eb22b03775e9b66b3bdbb74e174ddc8e36b4fc8e1edc3e46a3be14963631932e |
| DB tables/counts | parts=6; projects=1 | parts=6; projects=1 |
| Rack name | My Lab Rax | My Lab Rax |
| Rack ID | 4e9aa4f8-57a4-446d-97a4-6f8257abb8f3 | 2c9c070f-eb21-4ea4-bdc5-6d7ed9bb776f |
| Slot count | 5 | 5 |
| Allocation count | 2 | 1 |
| Allocation names | Raspberry Pi 4, Raspberry Pi 4 | Raspberry Pi 4 |

The DB hashes differ; equal counts do not establish equal part/project contents. Current JSON histories and immutable cache/artwork coverage differ. Neither observation identifies the live active data path.

## data/normal-use — complete file inventory

| Relative path | Bytes | SHA-256 | Modified UTC |
| --- | --- | --- | --- |
| data/normal-use/artwork/e40e0179e1eeb4a5c98643cba7dbd0f7ed7beb5dac3d18b414a0abfeab3c5582.png | 28616 | e40e0179e1eeb4a5c98643cba7dbd0f7ed7beb5dac3d18b414a0abfeab3c5582 | 2026-10-18T18:52:52.626488+00:00 |
| data/normal-use/library.sqlite3 | 28672 | fdc694c09c2eaf099a3f2262bd03360b42746ecbf30571d263c6351319dc3bfd | 2026-10-18T07:07:16.095463+00:00 |
| data/normal-use/rack-history/14994e90-8fa0-42ae-ace0-6055b7aaf35e.json | 5032 | d6d73e14350ad38729f84f12dbaed374970cd5d5b6230f137f1e2027c37d5a90 | 2026-10-18T20:50:00.336323+00:00 |
| data/normal-use/rack-history/3b04d355-b461-4a86-86d4-3e202e0aff91.json | 4907 | 00990cbc6ac751a41d788a7edb570a9592a4b675fbe89d21176acfc31bb9e92b | 2026-10-18T19:59:30.382914+00:00 |
| data/normal-use/rack-history/45d893fe-b1fa-4a6b-b58d-c8348b709769.json | 4899 | be99e0a711ab90a011ef914d5b37fe28efc759cd50627435819b2652da5a2823 | 2026-10-18T20:50:13.020288+00:00 |
| data/normal-use/rack-history/7eb64862-d443-436f-95c7-6875b041606d.json | 573 | dfaaa9b0f459f079bbcfa834a3bdf16e33d1ad66c13ac98ec641b024014232a3 | 2026-10-18T19:29:57.132528+00:00 |
| data/normal-use/rack-history/aa3ff3ef-24b3-4c78-8b4d-2c39ba12aa34.json | 4899 | 683e34bb377257b120d7fd079e929e0a853a7d987065cfe584e75900b8a1cae1 | 2026-10-18T21:34:02.173853+00:00 |
| data/normal-use/rack-history/ea0d424f-ce11-4f7e-8a10-c676f31e859e.json | 311 | e2b6f55acfc6e84300cb761981d2ef2eb0fbf22548ea6ae9b1e4ad7b2589b53f | 2026-10-18T18:15:23.059148+00:00 |
| data/normal-use/rack-workspace.json | 9245 | accb584350659344602e78cf3864951896958a680805c40c0660b77e671d1847 | 2026-10-19T02:09:00.391813+00:00 |
| data/normal-use/revisions/ebd6af3164685923c661c7965badd932d98ed6c1da9bfc51742fe934f6a68a78/assembly.json | 310514 | 7c1eab70129e10a7cfdfd5fad23054b4ae2d8db340268ed38e7381c632fba3b1 | 2026-10-18T07:07:53.990619+00:00 |
| data/normal-use/revisions/ebd6af3164685923c661c7965badd932d98ed6c1da9bfc51742fe934f6a68a78/faceplate.stl | 204080 | 1c1512d35979ad8821f07851c5a15ef8306f5f4800d6efb39ce6eb52a64e9906 | 2026-10-18T07:07:53.909498+00:00 |
| data/normal-use/revisions/ebd6af3164685923c661c7965badd932d98ed6c1da9bfc51742fe934f6a68a78/pi4_proposed.scad | 3512 | e673df53fd2d33ccb5f19494a6ff6f9965e2c05389ad8d606cc33787921cab50 | 2026-10-18T07:07:27.935031+00:00 |
| data/normal-use/revisions/ebd6af3164685923c661c7965badd932d98ed6c1da9bfc51742fe934f6a68a78/revision.json | 5648 | 96b123d39c86b0a646544270984a1fa6886f47bea410e2b069c709cc53958fb3 | 2026-10-18T07:07:53.990619+00:00 |
| data/normal-use/revisions/ebd6af3164685923c661c7965badd932d98ed6c1da9bfc51742fe934f6a68a78/tray.stl | 1709434 | 6ca66dca84d4abd4f1b9f5f56dca152b84dabc581dbb5f38d4a577e0ce875d04 | 2026-10-18T07:07:51.891955+00:00 |

SQLite scratch copy: C:\Users\brian\AppData\Local\Packages\sandbox.{a74db76a-fac8-4a64-ab03-6b47e878327b}\AC\Temp\assembly-housekeeping-20261018\db-copies\data\normal-use\library.sqlite3

| Table | Rows | Columns | Latest timestamp columns |
| --- | --- | --- | --- |
| parts | 6 | id, revision, body | No timestamp/date/created/updated/modified/time column exists; not inferred from JSON body. |
| projects | 1 | id, body | No timestamp/date/created/updated/modified/time column exists; not inferred from JSON body. |

Saved rack JSON (including history; current document explicitly named):

| JSON path | Version | Generation | Rack name / ID | Slots | Allocations | Allocation names |
| --- | --- | --- | --- | --- | --- | --- |
| data/normal-use/rack-history/14994e90-8fa0-42ae-ace0-6055b7aaf35e.json | 2 | 14994e90-8fa0-42ae-ace0-6055b7aaf35e | My Lab Rax / 4e9aa4f8-57a4-446d-97a4-6f8257abb8f3 | 5 | 1 | Raspberry Pi 4 |
| data/normal-use/rack-history/3b04d355-b461-4a86-86d4-3e202e0aff91.json | 2 | 3b04d355-b461-4a86-86d4-3e202e0aff91 | My Lab Rax / 4e9aa4f8-57a4-446d-97a4-6f8257abb8f3 | 5 | 1 | Raspberry Pi 4 |
| data/normal-use/rack-history/45d893fe-b1fa-4a6b-b58d-c8348b709769.json | 2 | 45d893fe-b1fa-4a6b-b58d-c8348b709769 | My Lab Rax / 4e9aa4f8-57a4-446d-97a4-6f8257abb8f3 | 5 | 1 | Raspberry Pi 4 |
| data/normal-use/rack-history/7eb64862-d443-436f-95c7-6875b041606d.json | 2 | 7eb64862-d443-436f-95c7-6875b041606d | My Lab Rax / 4e9aa4f8-57a4-446d-97a4-6f8257abb8f3 | 5 | 0 |  |
| data/normal-use/rack-history/aa3ff3ef-24b3-4c78-8b4d-2c39ba12aa34.json | 2 | aa3ff3ef-24b3-4c78-8b4d-2c39ba12aa34 | My Lab Rax / 4e9aa4f8-57a4-446d-97a4-6f8257abb8f3 | 5 | 1 | Raspberry Pi 4 |
| data/normal-use/rack-history/ea0d424f-ce11-4f7e-8a10-c676f31e859e.json | 1 | ea0d424f-ce11-4f7e-8a10-c676f31e859e | My Lab Rax / 4e9aa4f8-57a4-446d-97a4-6f8257abb8f3 | 5 | 0 |  |
| data/normal-use/rack-workspace.json | 2 | 6deba0de-fb22-4f48-9568-7ec1818e1504 | My Lab Rax / 4e9aa4f8-57a4-446d-97a4-6f8257abb8f3 | 5 | 2 | Raspberry Pi 4, Raspberry Pi 4 |

## outputs/Mechanical_Design_App/data — complete file inventory

| Relative path | Bytes | SHA-256 | Modified UTC |
| --- | --- | --- | --- |
| outputs/Mechanical_Design_App/data/equipment-revisions/52054080bde21f8567f724692d6a588912e7d423c891d7d18b2327fc9e5379b9/equipment.scad | 5826 | 52054080bde21f8567f724692d6a588912e7d423c891d7d18b2327fc9e5379b9 | 2026-10-19T03:59:51.908193+00:00 |
| outputs/Mechanical_Design_App/data/equipment-revisions/52054080bde21f8567f724692d6a588912e7d423c891d7d18b2327fc9e5379b9/faceplate.stl | 207575 | 0070f137582cad7a6aaf6dfc18119daf4034789f3b37aec111e867d3b02bbc2b | 2026-10-19T03:59:56.973872+00:00 |
| outputs/Mechanical_Design_App/data/equipment-revisions/52054080bde21f8567f724692d6a588912e7d423c891d7d18b2327fc9e5379b9/revision.json | 4876 | f64a8c257d6c8b850b81d081a8da8828527d0b80cf7ca4638d1ce41005a0544c | 2026-10-19T03:59:57.068517+00:00 |
| outputs/Mechanical_Design_App/data/equipment-revisions/52054080bde21f8567f724692d6a588912e7d423c891d7d18b2327fc9e5379b9/tray.stl | 219008 | 68a59cf552918e9782be2129307caf5944b5bbd0bb3d54f8dbde7fb91cf68be9 | 2026-10-19T03:59:54.680019+00:00 |
| outputs/Mechanical_Design_App/data/library.sqlite3 | 28672 | eb22b03775e9b66b3bdbb74e174ddc8e36b4fc8e1edc3e46a3be14963631932e | 2026-10-18T21:42:48.423700+00:00 |
| outputs/Mechanical_Design_App/data/rack-workspace.json | 2434 | 888676fd2a0a78a7e0f7f49e2677427aebf1d903bc36b0d5d0a192ef89f67dc7 | 2026-10-18T21:49:29.301477+00:00 |

SQLite scratch copy: C:\Users\brian\AppData\Local\Packages\sandbox.{a74db76a-fac8-4a64-ab03-6b47e878327b}\AC\Temp\assembly-housekeeping-20261018\db-copies\outputs\Mechanical_Design_App\data\library.sqlite3

| Table | Rows | Columns | Latest timestamp columns |
| --- | --- | --- | --- |
| parts | 6 | id, revision, body | No timestamp/date/created/updated/modified/time column exists; not inferred from JSON body. |
| projects | 1 | id, body | No timestamp/date/created/updated/modified/time column exists; not inferred from JSON body. |

Saved rack JSON (including history; current document explicitly named):

| JSON path | Version | Generation | Rack name / ID | Slots | Allocations | Allocation names |
| --- | --- | --- | --- | --- | --- | --- |
| outputs/Mechanical_Design_App/data/rack-workspace.json | 2 | 95c6c20e-4bb4-4aa6-8779-bc300706980a | My Lab Rax / 2c9c070f-eb21-4ea4-bdc5-6d7ed9bb776f | 5 | 1 | Raspberry Pi 4 |

## Static data-path definitions

- outputs/Mechanical_Design_App/start.bat:3 passes --existing-library --data "%~dp0..\..\data\normal-use" after changing into the app folder (:2).
- outputs/Mechanical_Design_App/app.py:897 defines --data default=ROOT / data; ROOT is defined at app.py:39. This is outputs/Mechanical_Design_App/data.
- work/gui-style-delivery/Report.md:7 and work/startup-reliability/Report.md:21 record later use of app-local data. They are historical reports, not a current listener check.

Brian explicitly leaves C4 unresolved for Claude. No selection, merge, switch or recommendation is made.
