# Place on tray render sweep report

Date: 2026-10-19 (Brian local time). Task 18; investigation only.

## Result

**24 PASS, 2 FAIL, 4 SKIP across 30 selected cases.** The two FAIL results reproduce the same configuration in independent fresh folders: 1U, straps, 0°, centred, rear support, screw joint, one keystone at −100 mm, draft quality. The faceplate has one edge shared by four triangles. All five built-in nudge attempts fail at that same edge. No source, tests or validation rules were changed.

All **53 returned parts** from successful cases passed a second explicit `mesh_revision.read_mesh()` call: 19 trays, 19 faceplates, 10 rear brackets and 5 combined parts. Every successful part has `nudge_mm = 0`. There are 24 distinct successful sources and one distinct failing configuration (tested twice). Printed fit, retention and strength remain **UNKNOWN**.

## Method and effective inputs

Python: `3.10.4 (tags/v3.10.4:9d38120, Mar 23 2022, 23:13:41) [MSC v.1929 64 bit (AMD64)]`.
Renderer: `C:\Program Files\OpenSCAD\openscad.exe` (OpenSCAD.exe).

Base library spec (task-supplied equipment facts, with explicit library defaults for mounting, joint and standoff):

```json
{
  "name": "Sweep",
  "dev_w": 120,
  "dev_d": 80,
  "dev_h": 25,
  "holes": [
    [
      10,
      10
    ],
    [
      110,
      70
    ]
  ],
  "ports": [
    {
      "x": -30,
      "z": 21,
      "w": 16,
      "h": 14,
      "r": 1
    }
  ],
  "rear_ports": [
    {
      "x": 0,
      "z": 21
    }
  ],
  "device_mount": "inserts",
  "joint": "screw",
  "standoff": 6
}
```

For each case, the listed tray choices were passed through the current `equipment.allocation_spec(base, tray)`, quality was added separately (it is not a PLACEMENT_KEYS field), and `equipment.clean(spec)` ran first. Rejected inputs were recorded as SKIP, without bypassing validation. Accepted cases used `equipment.render(spec, fresh_case_dir)`. Each returned revision's parts were reread using the unchanged mesh checker. Each case had a fresh directory, so existing or other-case caches were never reused.

The current allocation code includes front-opening movement added since the cited end-to-end report: at 0°, X follows the left/right offset and Z follows the change in device lift relative to the library's 6 mm standoff. Straps have zero lift, so their 0° opening is centred at Z = 15 mm. At 90°/180°/270°, openings remain at the entered library coordinates. The effective opening centre is included below; its size/radius stays 16 × 14 / 1 mm. Rear ports are planning data and do not cut geometry. This report tests the current allocation path, rather than silently ignoring its opening transformation.

The runner observed `read_mesh()` failures in memory, counted undirected STL triangle edges, recorded every edge whose count was not two, and re-raised the original error. It did not alter mesh coordinates, checker outcomes, normalization or nudge behavior. The unchanged renderer's normal collinear normalization and retry policy still ran. Failure diagnostics were captured before the renderer cleaned up its failed temporary files.

## Case results

All lengths are mm. RS = rear support. KS = keystone X positions. Opening = effective front-opening centre (X,Z). A failed render returns no revision.json: for cases 13/25, tray passed at nudge 0, faceplate failed at all listed nudges, and the rear bracket was not reached. SKIP means no render or nudge was attempted.

| Case | Mount | Rotation | Offset X,Y | Standoff | RS | U | KS | Joint | Quality | Opening X,Z | Result | nudge_mm by part / error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | inserts | 0° | 0,0 | 3 | no | 1 | [-100] | screw | draft | -30,18 | PASS | {"tray":0,"faceplate":0} |
| 2 | inserts | 90° | -25,20 | 6 | yes | 2 | [100] | screw | fine | -30,21 | PASS | {"tray":0,"faceplate":0,"rear_bracket":0} |
| 3 | inserts | 180° | 25,0 | 12 | no | 2 | [] | screw | draft | -30,21 | PASS | {"tray":0,"faceplate":0} |
| 4 | inserts | 270° | 0,20 | 3 | yes | 1 | [100] | screw | fine | -30,21 | PASS | {"tray":0,"faceplate":0,"rear_bracket":0} |
| 5 | pegs | 0° | -25,0 | 6 | yes | 2 | [] | screw | draft | -55,21 | PASS | {"tray":0,"faceplate":0,"rear_bracket":0} Fresh-folder retry; prior Windows permission error below. |
| 6 | pegs | 90° | 25,20 | 12 | no | 2 | [100] | screw | fine | -30,21 | PASS | {"tray":0,"faceplate":0} |
| 7 | pegs | 180° | 0,0 | 3 | yes | 1 | [-100] | screw | draft | -30,21 | PASS | {"tray":0,"faceplate":0,"rear_bracket":0} |
| 8 | pegs | 270° | -25,20 | 6 | no | 2 | [100] | screw | fine | -30,21 | PASS | {"tray":0,"faceplate":0} |
| 9 | clips | 0° | 25,0 | 12 | no | 2 | [] | screw | draft | -5,27 | PASS | {"tray":0,"faceplate":0} |
| 10 | clips | 90° | 0,20 | 3 | yes | 1 | [100] | screw | fine | -30,21 | PASS | {"tray":0,"faceplate":0,"rear_bracket":0} |
| 11 | clips | 180° | -25,0 | 6 | no | 2 | [] | screw | draft | -30,21 | PASS | {"tray":0,"faceplate":0} |
| 12 | clips | 270° | 25,20 | 12 | yes | 2 | [100] | screw | fine | -30,21 | PASS | {"tray":0,"faceplate":0,"rear_bracket":0} |
| 13 | straps | 0° | 0,0 | 6 (unused lift) | yes | 1 | [-100] | screw | draft | -30,15 | FAIL | tray: 0 (passed); faceplate: 0, 0.011, 0.023, 0.037, 0.051 (all failed); rear_bracket: not attempted. ValueError: Rendered mesh has open or non-manifold edges: faceplate |
| 14 | straps | 90° | -25,20 | 6 (unused lift) | no | 2 | [100] | screw | fine | -30,21 | PASS | {"tray":0,"faceplate":0} |
| 15 | straps | 180° | 25,0 | 6 (unused lift) | yes | 4 | [] | screw | draft | -30,21 | PASS | {"tray":0,"faceplate":0,"rear_bracket":0} |
| 16 | straps | 270° | 0,20 | 6 (unused lift) | no | 1 | [100] | screw | fine | -30,21 | PASS | {"tray":0,"faceplate":0} |
| 17 | clips | 0° | 0,0 | 3 | no | 1 | [-100] | single | draft | -30,18 | PASS | {"combined":0} |
| 18 | clips | 270° | 25,20 | 12 | no | 4 | [100] | single | fine | -30,21 | PASS | {"combined":0} |
| 19 | inserts | 90° | -25,20 | 6 | no | 2 | [-100] | single | fine | -30,21 | PASS | {"combined":0} |
| 20 | pegs | 180° | 0,0 | 12 | no | 2 | [100] | single | draft | -30,21 | PASS | {"combined":0} |
| 21 | straps | 270° | 25,20 | 6 (unused lift) | no | 4 | [-100] | single | fine | -30,21 | PASS | {"combined":0} |
| 22 | inserts | 0° | 0,0 | 3 | yes | 1 | [100] | screw | fine | -30,18 | PASS | {"tray":0,"faceplate":0,"rear_bracket":0} |
| 23 | pegs | 90° | 25,20 | 12 | yes | 4 | [-100] | screw | draft | -30,21 | PASS | {"tray":0,"faceplate":0,"rear_bracket":0} |
| 24 | clips | 180° | -25,20 | 6 | yes | 2 | [] | screw | fine | -30,21 | PASS | {"tray":0,"faceplate":0,"rear_bracket":0} |
| 25 | straps | 0° | 0,0 | 6 (unused lift) | yes | 1 | [-100] | screw | draft | -30,15 | FAIL | tray: 0 (passed); faceplate: 0, 0.011, 0.023, 0.037, 0.051 (all failed); rear_bracket: not attempted. ValueError: Rendered mesh has open or non-manifold edges: faceplate |
| 26 | clips | 90° | 0,20 | 6 | no | 4 | [100] | screw | fine | -30,21 | PASS | {"tray":0,"faceplate":0} |
| 27 | clips | 0° | 0,0 | 6 | yes | 2 | [100] | single | draft | -30,21 | SKIP | Not attempted. Rear-post support needs the screw joint (a 240 mm single print is not offered). |
| 28 | inserts | 270° | 0,20 | 6 | yes | 4 | [-100] | single | fine | -30,21 | SKIP | Not attempted. Rear-post support needs the screw joint (a 240 mm single print is not offered). |
| 29 | inserts | 0° | 0,0 | 12 | no | 1 | [100] | screw | draft | -30,27 | SKIP | Not attempted. Device is taller than 1U allows; pick more rack units. |
| 30 | pegs | 90° | 0,20 | 12 | yes | 1 | [-100] | screw | fine | -30,21 | SKIP | Not attempted. Device is taller than 1U allows; pick more rack units. |

## Coverage and skip wording

- Cases 1–16 exercise every mount × rotation pair. Straps × 0° fails; all other pairs pass after the environment-only retry of case 5.
- Accepted cases cover offsets X = 0, −25, +25 and Y = 0, 20; non-straps standoffs 3, 6, 12; rear support both on and off; and 1U, 2U, 4U.
- One keystone at −100 or +100 is included at every requested U height. Wide unrotated offset trays omit the keystone where the collar guard would reject ±100. No guard was bypassed.
- Draft: 10 PASS, 2 FAIL, 2 SKIP. Fine: 14 PASS, 2 SKIP. Both quality levels therefore have more than four successfully rendered cases.
- Single joint: five combined parts pass, including clips in cases 17/18. Single plus rear support is explicitly attempted in cases 27/28 and rejected by clean(). It is not a supported render combination.
- Cases 27/28: `Rear-post support needs the screw joint (a 240 mm single print is not offered).` **Plain language: yes**; it identifies the incompatible choices and tells the user to use the screw joint.
- Cases 29/30: `Device is taller than 1U allows; pick more rack units.` **Plain language: yes**; it explains the height conflict and remedy. With this 25 mm device, 12 mm standoff and the cleaner's 10 mm allowance total 47 mm, above 44.45 mm.

This is selected coverage, not a full cross product or physical approval. Cases 13 and 25 are recorded as separate fresh-folder attempts of the same effective settings; their agreement establishes repeatability for that failure.

## Mesh failure and bad edges

Cases **13 and 25** fail with the exact error:

```text
ValueError: Rendered mesh has open or non-manifold edges: faceplate
```

For each case, each of the five nudge attempts has exactly the same single bad undirected edge:

| Cases | Part | nudge_mm attempted | Edge endpoint A (X,Y,Z) | Edge endpoint B (X,Y,Z) | Adjacent triangle count |
| --- | --- | --- | --- | --- | --- |
| 13, 25 | faceplate | 0; 0.011; 0.023; 0.037; 0.051 | (−38, −0.0999994, 21) | (−38, 0, 21) | 4 (required: 2) |

No other edges had a count other than two in these failing meshes. The unchanged check correctly prevents a returned completed revision. Tray passed its internal check at zero nudge before the faceplate failure; the rear bracket was not rendered. There is no final nudge_mm revision record for a failed case, so the table reports observed attempts rather than inventing a successful revision.

Observation: the failing effective opening is X = −30, Z = 15, with dimensions 16 × 14, and the defect is at X = −38, Z = 21 near the plate/tray-joint region. Root cause and corrective geometry are **not established** by this investigation. No geometry fixes or extra variations were attempted. A later authorized fix should reproduce this exact allocation, preserve the mesh guard and rerun this case.

## Environment failures and rerun

The initial sandbox attempt hit `PermissionError: [WinError 5] Access is denied` while renaming case 1's rendered directory to its source-identity folder. It was interrupted (exit 1) and is excluded from case totals. This was a file operation failure, not a reported mesh failure.

The sweep was rerun with approved execution outside the sandbox. Case 5 again encountered a transient folder-rename permission error after its mesh checks. Its first attempt had no captured mesh-check failure and no returned revision. Exact recorded error:

```text
PermissionError: [WinError 5] Access is denied: 'C:\\Users\\brian\\Documents\\Codex\\2026-10-17\\Assembly Workshop\\work\\task18-temp-20261019\\case-05\\equipment-revisions\\render-gzvchspb' -> 'C:\\Users\\brian\\Documents\\Codex\\2026-10-17\\Assembly Workshop\\work\\task18-temp-20261019\\case-05\\equipment-revisions\\b85c8840c8c297c0a8b58ff561510f2290ec44a4dc739d6fb04a0873dc15b042'
```

A separately approved rerun of only this environment-failed case, in a fresh `retry-case-05` directory, passed all three parts with zero nudge. The same inputs and unchanged source/checker were used. Both attempts are disclosed; only the completed retry determines case 5's final PASS result. The two geometry failures were not reclassified or hidden.

## Commands actually run and results

All commands ran from the project root. PowerShell reads used explicit UTF-8; Python ran with `-B`, and all diagnostic text/JSON writes used UTF-8. No bytecode caches were created by the runners.

1. `Get-Content -Encoding UTF8` read AGENTS.md, PROJECT.md, HANDOFF.md, ROADMAP.md, work/codex-tasks/README.md and task 18; HANDOFF.md was reread separately because the combined output was truncated. Relevant reads then covered task 16's report, E2E_Acceptance_Report.md, equipment.py, mesh_revision.py, port_openings.py and equipment_tray.scad (with selected ranges where appropriate). No repository-wide file scan was run.
2. `Get-Item 'C:/Program Files/Python310/python.exe','C:/Program Files/OpenSCAD/openscad.exe'` confirmed both executables. `Test-Path work/codex-tasks/18-placement-render-sweep-REPORT.md` returned False before writing; this is a new report.
3. An inline PowerShell here-string piped to `& 'C:/Program Files/Python310/python.exe' -B -u -` began the 30-case sweep in a new sandbox temp directory. Interrupted with Ctrl+C after the folder-rename permission error; exit 1, excluded from totals.
4. Created the previously absent task-specific disposable folder with `New-Item -ItemType Directory`. Wrote only temporary sweep.py/retry.py diagnostic runners there using apply_patch.
5. With approved execution outside the sandbox: `& 'C:/Program Files/Python310/python.exe' -B -u work/task18-temp-20261019/sweep.py`. Exit 0; 350.229 seconds; first totals 23 PASS / 3 FAIL / 4 SKIP (one FAIL was environmental). Exit 0 indicates the investigation runner completed, not that every geometry case passed.
6. A Python `-B -c` read the temporary results.json and printed failing cases and bad-edge coordinates. `Get-Content -Encoding UTF8 .../results.json -Tail 28` inspected interim source hashes. Session output was polled while rendering; no app server or browser was started.
7. With approved execution outside the sandbox: `& 'C:/Program Files/Python310/python.exe' -B -u work/task18-temp-20261019/retry.py`. Exit 0; case 5 passed in 7.36 seconds; final totals **24 PASS / 2 FAIL / 4 SKIP**. This retry changed no runner inputs or application files.
8. `Get-Content -Raw -Encoding UTF8 work/task18-temp-20261019/results.json` read the completed evidence into working memory for this report. Verified all five inspected source SHA-256 values matched before/after, counted 53 successful returned parts and retained the failure coordinates.
9. Cleanup resolved and checked absolute targets first, then used PowerShell `Remove-Item -LiteralPath <exact-new-scratch-path> -Recurse -Force -ErrorAction Stop` on only the two directories listed below. `Test-Path` confirmed both absent; exit 0, `SweepScratchAbsent=true`, `InitialScratchAbsent=true`.
10. apply_patch created this new REPORT only; final `Get-FileHash -Algorithm SHA256` verifies its completed bytes after writing. A self-hash is not embedded inside the report.

Removed scratch paths (including runners, result JSON and rendered meshes):

- `C:/Users/brian/Documents/Codex/2026-10-17/Assembly Workshop/work/task18-temp-20261019`
- `C:/Users/brian/AppData/Local/Packages/sandbox.{40f771f0-7ac0-4779-975a-94501a410134}/AC/Temp/aw-task18-g1dn9qkd`

No application regression suite was run: this task expressly requested a render investigation without code or test edits. No delivery/export bundle was generated. Task 18's specific diagnostic-render and temporary-cleanup instructions were treated as authorization for these disposable operations despite the general no-export/no-deletion standing rules.

## Files and SHA-256

Only new persistent file: `work/codex-tasks/18-placement-render-sweep-REPORT.md`. **Before: absent. After: completed UTF-8 report; SHA-256 verified externally after writing.** A report cannot contain its own final SHA-256. No existing file was edited, so no archive copy was required. Temporary files were removed as recorded above.

| Inspected application file | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| outputs/Mechanical_Design_App/equipment.py | `57e5cc8e1f1937e70b916c95c98ded2f754c33ce5613d078370ee881519029c9` | `57e5cc8e1f1937e70b916c95c98ded2f754c33ce5613d078370ee881519029c9` |
| outputs/Mechanical_Design_App/equipment_tray.scad | `4c98aa5ba251a87edf641276f71a022f09b273633fec2421c5f63606c903f5fa` | `4c98aa5ba251a87edf641276f71a022f09b273633fec2421c5f63606c903f5fa` |
| outputs/Mechanical_Design_App/mesh_revision.py | `a569e208d9ad2be574d9f7c22fba8125e4df9daf70a6bd690792f6fb95832962` | `a569e208d9ad2be574d9f7c22fba8125e4df9daf70a6bd690792f6fb95832962` |
| outputs/Mechanical_Design_App/port_openings.py | `20aa69584d28e4d9296bfa6cf83002e3aa222b98cdb4a0f3fba8402955135c44` | `20aa69584d28e4d9296bfa6cf83002e3aa222b98cdb4a0f3fba8402955135c44` |
| outputs/Mechanical_Design_App/cable_ports.py | `8cbbc5d83bed9fe401f2f9e1fd175d879f6baeaf3fcc4193658223d3fc5f7136` | `8cbbc5d83bed9fe401f2f9e1fd175d879f6baeaf3fcc4193658223d3fc5f7136` |

## Successful source and part evidence

The identifiers below are SHA-256 of generated equipment.scad as reported by the renderer. Each successful part was independently reread; the table records the STL SHA-256 returned by read_mesh(), plus triangle counts. Source identifiers are from revision.json. This is not an additional source/cache integrity audit. The completed report preserves these recorded hashes after temporary meshes are removed.

| Case | Source SHA-256 | Part: STL SHA-256 (triangle count) |
| --- | --- | --- |
| 1 | `a925e1b29261321a0ab9fd6f28f2bf86892a642ff99948109a740282933a2e38` | tray: `7d99e204363d8f1b1954d63fec19907ba992225285b1322bb10f56a05e3280ba` (742); faceplate: `8fee323602cb267ce27fd5444e40013c1052fe5d79a52bb2f8d432540de018ad` (1700) |
| 2 | `f6e66b9a7213a1267b5cec70c14e79c6924694f0f7be82de0915e9a1d3d435c2` | tray: `4269354fc9496f24fcff7e36e751c64850e083c49083cff06a38d5cc942f279a` (3388); faceplate: `293469b7ef115034df3a57d2c911f8e2547bfd71145fe952952c365f102df41a` (6160); rear_bracket: `70734c05b3fa6a5aa12ec33f677bd7bd53cc28f8029aeb32cc4970aa95e84812` (5132) |
| 3 | `ed8280d557b9fa10f022cd5277086d42f73f977baae7c2303c50bc1d0fa6798e` | tray: `47583daefff4b4dcafecd968bc76fbc6a213b84dc15dbb705f298f62560aed69` (740); faceplate: `53f363e4ef70feb2e63d4eae0ba87df1b0f6f3067c02862e288140f37356c14f` (1512) |
| 4 | `1a576cb8542de9cb8459d5e5ca483cfcdff06433b95f50dafd1938ab34c6293c` | tray: `4aa39575684167f216c61781457043decf746844d68ab2dc5d7d0542d6e487d1` (3388); faceplate: `1c1ecd0fa898ab8d929c5c8a719c72ac70e7a7011f96e9648e4b2e579396682b` (4576); rear_bracket: `60ef7777d62a0b54ee5c1a956ab8c0ef46c8a89f2a8b976ac9348f54f44c3cd3` (3548) |
| 5 | `b85c8840c8c297c0a8b58ff561510f2290ec44a4dc739d6fb04a0873dc15b042` | tray: `73ac31aea9256e1f1c4e35e1eb08c4583645ef03bc512cdeb5fae23d5485d5c0` (1180); faceplate: `49fbab2b2e37e383455a398ae8fdebfacbe5a68340230cdaa841268a2a8efac6` (1504); rear_bracket: `01f77e72da4506f0352540e33fba2cae5a233ec48906c2a023fe4f73a188d651` (1388) |
| 6 | `b0fb6c5012e4fd4297a19b1d7580608dd7e67b25597f1d21d3cd5e509a12cc17` | tray: `74e8792cf7cf38702de89c5428d57a00c45f885b38f7408b1d7da603337577a5` (2852); faceplate: `31369ccbc07b257b5ba9ad3be9d3bac9b7f58d0255834403474f590c7c2f0dad` (6160) |
| 7 | `92c03b1a02133ebf96f490149fbab80b8c98f05b4b332e79ac288afa70a68f53` | tray: `1305fdf84c7c5c7dbf99bd0b761b6c8babe9530baaa29275129c412a6597b401` (1180); faceplate: `c49b85e3d88eec6dcd949af8867722a4835cb2ab3225a82d823d1517ca644d7a` (1696); rear_bracket: `8350466d9fed763075695c593fa681aa347023beb7cb759179b4cdf239afda1f` (956) |
| 8 | `eb5544a6f76a1539df69b0beebc7047507dc0ea2fae9946314c96f3c48e59ea7` | tray: `038eec41caab36089cc7c582dc443372452d2fe4e3b50c91f8335b297ce03b00` (2852); faceplate: `059d489fbbffc4ba0f48bde6311fa2ec7ce9e9eb7adc19828e660cbf08c69fd4` (6160) |
| 9 | `5ac922db6aceb092cc39147827f8ba8043c729865db11b9c57194e1ef1ced77d` | tray: `7440b1537449ea4d1d2126645573cf9f4d79ebe6c3cc04f910ce66d965fd21ba` (496); faceplate: `30c15f68b42e56fa01d6dc20ff902dfac115f93057f66c88845840f6861eb05a` (1504) |
| 10 | `ab94f9a453529055ff98cd465ad2885ece8d125888cbacdc0c02c5170fd2a5b4` | tray: `71504af03a268647b357deb0ca74eb90775dfebf778d4d4e943f9c1c86001427` (1984); faceplate: `69ffbf34f099f942c8343d94a0ae64e60cc56309f9f7d5ffb52952dbdbff671e` (4576); rear_bracket: `0a5f375e77dd776477b0e7e9ed4e818529914d3a75fb7e2733f44e0f168b8c60` (3548) |
| 11 | `9a96d95d6ebe981992d17242ada98a51fc2d803cb1e257e2dd32ccfd974ead60` | tray: `5b4d3331c709da24ff41c437006e3fbbb6f77dd9723ddc785942bda66c89f242` (496); faceplate: `5adad6c98bc7b8df4bfbfba3890a3256f6725d7b2355fd4db9ef92f50f5c1690` (1512) |
| 12 | `7bfe516ff1381b884e85933e50d29ee15d1edb6fe8d361eea32ab28b1e01c58e` | tray: `0b8c8b2b604ef723c5734f6f3584f08b990a384d80b6a1b0a10b9044e2fc323f` (1984); faceplate: `e0f99f4017530e9c433f9a91251fd7a6c3089dfb490215b12b605bd358c82834` (6160); rear_bracket: `35c1b28b8988f1f95632ecaac1bfecbf688cd300f9513bba7303d9011fecfaa5` (5132) |
| 14 | `dfbb813673df4c0509cc8b041b83e6fcef0b29a853e489b1db4f930f63dd744b` | tray: `6111358cd817b0fb306d6152eaeb36567f0d9e06bf891a9236f30bc1c2ab34ce` (1012); faceplate: `f58ff5777fb33af799d13bad46f4b73141298ce94ebad1e4669e9f1b4ff451c0` (6160) |
| 15 | `14711eb388a10b6319578a29b9db1b50438cde1969178726d3c71d4372b14a97` | tray: `7fada465a6dbecd830dfd55ee4860556f258683a017d65c4c770929da83c1238` (780); faceplate: `94e37883dadbbb34f552ebd06ce40dc9c4a34461b7447451a4dd497ee4a4caf0` (2376); rear_bracket: `fa3b67e8f19df3f608f03b5eac2e358044ea52bcb9b4abb176219ff5c9fd1aa2` (2252) |
| 16 | `31397d5e8091af65cfb15fb6bc345ef97cf35e960a10569744d608fde02e0a09` | tray: `2e61ea5503f691475016d59705a39704e25b7d0b2eec26e21b247e1307a848dd` (1012); faceplate: `0f9f96729bef8daf4c9768d2e58591eb26330c38c239dd29be5e84168e6b1ce1` (4576) |
| 17 | `36418ec2ad05d62510403a237e40db9c5f1eba1212d7c4232d664d502a499734` | combined: `17b22e81a9cdf0cb988b92120f38499e4ad3e10e4ea79880df2c5a6f8c9bbd04` (1420) |
| 18 | `38633ed05321ff8aea678755b915927309f94c5b2f61e1980c20de5165dcb4a5` | combined: `51edf523e6c25bc6a47d776f64d6c2e8c8d3642da7afcfb379dc5ffb21dd5588` (7900) |
| 19 | `bb678c8969836b76172bd767860a0e68349a70824e561ef74e9de134acc1f198` | combined: `d8467c52c4a9df98133fbf95b1f52bee890cfd1935c1b9635a1c18b0b7287d97` (6136) |
| 20 | `49f0c410e049599eccf7764e0587a78d4ca784d9073cc9f5730278e26a5eb4b8` | combined: `c707dc61f6467c3d7a0af8c51f9b80315b8406733c46e74761f2ec0b2a21774a` (2200) |
| 21 | `39ad67ddbbe490adbb5560e95e1fe64bf7b004e54a14283a2c25ef6f5f8d1c25` | combined: `474470b2ca6e0b2bb9918dee2305a54e1ddb310c0c7969ea88f3e46b08739458` (7848) |
| 22 | `f3e734272cda5b4593a2fe84267870d218a64178e3a8b5d9c86d3c0bedfbd840` | tray: `3f41d53d8cdf23a285927f37db05172c6b121eb1b5848fc5a66cfed9fab362c5` (3390); faceplate: `c04d712419d2669b13e967a8c01b9ae12b2b7df18e441dfe0d5326f35d6e7995` (4580); rear_bracket: `5645d390e62f52d94abcbaeabf59df149c5e769f37c5e9b04aac1b6aaf87b2cc` (3548) |
| 23 | `8c8e1294e0a5ce6285b83de42b98d84daa25f8b1f642afaaaef1b7a4d89cf4d4` | tray: `3faaa04397a04ceeb75d26f9600230d53e3f901475a0847969d8d6940ce5de65` (1180); faceplate: `4c6ecf39c60ad8a843d7838ae237a7cb4a0fa71813152252975d26285f254c4a` (2992); rear_bracket: `910f15b163c37258a7bb8fff7a79f8e832141b191c76825d8c215406e43d092a` (2252) |
| 24 | `c8110603f0a218824628eeaa648e664dcf910b2d51c4c13a0067084606d0538c` | tray: `3b892d5d4954712c8dc920b33731021cea34518ed09b26b3cfad0032555ca157` (1984); faceplate: `cc95b9a52bf2d5a85d3402d523c5a5b70a1e6cad488a5123c9a35a93a19217f7` (5544); rear_bracket: `234d8cece934e7112d57a3f88c927bd27b5fd4754cdad5d7f7413fd8a001e56f` (5132) |
| 26 | `dde0164615d989e2627968b3182b7f47a43c44576722c5b70a9d4ada8e44699d` | tray: `c49886bcf866ad5f3566b6b8bd5fe668a06cee2c3ed3354af5c0945be0b9e6f8` (1064); faceplate: `e405ec8ad51d8b43eed1f89424c217b1ec4a77293cb6be235625f411f561494b` (9328) |

## Assumptions and open questions

- The supplied equipment facts were preserved. Missing library defaults were explicitly filled with inserts/screw/6 mm so allocation_spec could apply the current opening transformation consistently.
- Standoff is held at the library default 6 for straps; the device lift is zero for straps. Standoff coverage 3/6/12 applies to the other mounts.
- Single plus rear support remains rejected as designed; no unsupported combination was forced through.
- The reproducible 1U straps faceplate failure is an open software geometry issue. Its exact cause/fix requires a separate authorized change; this task makes no code changes.
- Source hashes remained unchanged during the investigation. Current allocation opening behavior, rather than the older end-to-end snapshot, defines these effective inputs.
- No user data (including data/normal-use), historical cache, app-local data, saved rack, immutable revision or unsaved draft was used. No live server stop/restart, desktop control, subagent, physical test, print, purchase, install, commit, push, upload, release packaging or publishing occurred.
- Mesh closure is digital evidence only. Physical fit, strength and retention remain UNKNOWN. No missing user decision blocked this investigation.

