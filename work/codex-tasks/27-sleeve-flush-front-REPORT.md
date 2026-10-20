# Task 27 report — 2026-10-20

Implemented `sleeve` in the wizard and Place on tray, with a fixed flush front, low floor, two full-depth side walls, conditional top lips, rear stop, strap slots/access, side-wall screw joints and optional rear-post support. Single-piece sleeve is supported; single-piece plus rear support remains rejected. All new geometry is PROPOSED; fit, retention and strength remain UNKNOWN.

## Parameters and provenance

Only work/optiplex-bracket-study/Report.md was read. No third-party bracket file was opened, copied or redistributed. The study's measured 201 mm outside / 9 mm walls / 0.25 mm side clearance / 3.7 mm floor-roof / 15.5 mm ledges were context, not copied geometry or our defaults.

Defaults are named in port_openings.py (Python), SLEEVE in port-openings.js (JS), and sl_* in equipment_tray.scad (SCAD):

| Parameter | Value | Source/choice |
| --- | --- | --- |
| Side clearance | 0.5 mm per side | Task's proposed default |
| Top clearance | 0.3 mm | Task's proposed default |
| Wall | 6 mm | Chosen: leaves nominal 1 mm either side of a 4 mm pilot; physical adequacy UNKNOWN |
| Inward lip width | 10 mm, limited to half the window on narrow devices | Task's approximate target |
| Lip thickness | 1.5 mm minimum | Task's proposed minimum |
| Plate bands | 1.5 mm minimum | Task's proposed minimum |
| Rear-stop thickness/height | 4 mm / min(6 mm, device height) | Chosen low bar |
| Floor bottom/thickness | 0.5 / 3 mm | Existing flat floor after task 25 |
| Front | Y=-4 mm | Existing 4 mm plate front; sleeve front gap fixed |
| Pilot/clearance bores | 4.0 / 3.4 mm | Existing M3 joint dimensions retained |

The lip is present only if its top stays within the U budget. Otherwise a walls-only note is available. With the current equal 1.5 mm minimum band/lip values, any window passing the band check also has room for that minimum lip; thus the OptiPlex has lips, and an overly tall window is rejected rather than silently losing its required band.

## OptiPlex reference calculation

182.5 mm across × 194.5 deep × 38.8 high (feet included in the supplied envelope; no assumption about removing feet):

- Overall tray width 198.5 mm, sleeve outside width 195.5 mm, both ≤204 mm; wall 6 mm.
- Device bottom 3.5 mm, top 42.3 mm. Window 183.5 ×39.1 mm, X ±91.75, Z 3.5–42.6.
- Lower plate band 3.475 mm; upper 1.825 mm. Lip from Z 42.6 to 44.1 (1.5 mm thick); 10 mm inward.
- Device front Y=-4; device rear/rear-stop front Y=190.5. Stop ends Y=194.5. The device stops at the flush position with no added longitudinal clearance.
- Rear-post support floor reaches Y=240; stop clearance to the posts is 45.5 mm, exceeding the required 11.5 mm rear-joint exclusion. Walls stop at the device rear; the stop is behind it.
- Front joint axes X ±94.75, Z 6.5 and 39.6. Each plate clearance hole is outside the window; matching 4 mm pilots extend 8 mm into the front of the side walls. No front-centre tongue/boss obstructs the window. Existing rear tongue/boss/riser geometry is retained, with the flat-style short gusset.

The floor supports the device; walls constrain lateral movement; top lips constrain lift; the rear stop fixes insertion depth. There is no positive forward latch: optional straps are the forward-retention provision; retention and strap fit are UNKNOWN. Strap access notches are placed at quarter-depth, aligned with the existing floor slots. Large lightening windows were not added. A new geometric guard rejects sleeves shallower than 72 mm so those strap slots cannot intersect the front 8 mm pilot region. Screw sleeves also require a window at least 10 mm tall; shorter boxes can select single piece. These are geometric guards, not strength approval.

## Openings and previews

Contained front openings are omitted from the generated sleeve cut-outs, with a UI note that the window exposes them; input objects are not mutated. Partially overlapping window openings and openings at the wall joints are rejected. Outside openings remain supported. Existing keystone collar exclusion stays in force. Rack artwork excludes the sleeve window. Cable-port lift and rear/custom marker positions account for the flush front. Sketches contain four actual plate bands around a window plus walls/lips/stop; exact-preview source contains these features. Numeric front/back offsets are ignored for sleeve geometry and normalized to zero when cleaned; the UI states that the front is fixed flush.

## Verification actually performed

- Baseline: task 26 final run_checks.ps1 passed before this task's edits.
- Repeated `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1`: first found two stale SCAD-text assertions; fixed within allowed tests. Subsequent runs passed. Final log: docs/archive/codex/2026-10-20/task27/checks-final-2.txt — **127 Python tests, one pre-existing render skip; all 183 JS tests pass**.
- New tests cover reference sleeve/rear support/rotation/single piece, rejection of single+rear support and tall windows, contained versus intersecting/outside openings, keystone exclusion, joint placement, Python/JS agreement, real sketch-window bounds, rear cable markers, small-depth/height guards, and SCAD parameter agreement.
- One-off isolated Node comparison: all five pre-existing mount rack sketches are byte-identical JSON to task 26's archived baseline. An initial attempt loaded old/new modules into one global context and failed due to global-module contamination; rerun in separate Node processes passed. No application change was needed for that harness issue.
- `git diff --check` passed (only Git line-ending notices); targeted Get-Content/rg reads and Python stdlib backup/edit/hash scripts were used.
- No OpenSCAD render, STL export, live server restart, desktop-control session, print, user-data write, or third-party bracket-file access. The existing opt-in OpenSCAD test remains skipped. Exact rendered mesh closure and visual/browser checks are not established by this run.

## Remaining questions/limits

Claude's browser review with the STEP remains pending. Feet removal is unconfirmed, so the full 38.8 mm height was used. Fastener length, pilot/insert fit in the new wall, loads, strength, cooling and actual retention remain UNKNOWN. The nominal 208 mm opening and 2 mm per-side clearance remain PROPOSED. No physical claim transfers from the third-party bracket or older specimens. No additional work after this report; tasks 25 and 26 reports were completed with passing checks before this task began. No commits/pushes or HANDOFF edits under the explicitly requested task queue restrictions and May change scope.

Byte-for-byte originals are in docs/archive/codex/2026-10-20/task27/. Actual-byte SHA-256 values below; frontend manifest hashes use LF-normalized text.

| File | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `outputs/Mechanical_Design_App/asset-manifest.json` | 3ea95d5650ef2fb56ddff3c4ab1d1e9fcb9f7b79cad034766d18b66cd1aa1c86 | c8f4883b6e730dd0e42d6d8f445e3c73241681bbab19f0a4b47f2358f2870cae |
| `outputs/Mechanical_Design_App/cable-ports.js` | 47c158f76909659dc7b4ac22af5623b6d025b076c39f3d545a9d8a505d6e06fa | 0e0d095b9a61fae4dd865fbd469d19e039b9aad9d4f601a8852c35d9f0329998 |
| `outputs/Mechanical_Design_App/equipment-wizard.js` | fbe1ebd176e169c3e599896e43dd35973376a6754c6af9a6187049d274b34fe4 | 862506aa29ecb99ada7b7f0e703b75244ea74ceefb979d052d03fbb7a9cdc8fd |
| `outputs/Mechanical_Design_App/equipment.py` | 845e39067004642bfaa96f5da644ea5488edcf57907a0267e35bedfd049bda8a | a493f7d50b7fcf9701686e77f3ca3cb182c7e6c6b5305e6ef628e926bf659abd |
| `outputs/Mechanical_Design_App/equipment_tray.scad` | 5cc525ad6edd0b15e7ab172f5df701f3b9bbbe9683d93b898b968f21eb989e42 | 8afba648cd2537814bf375baffad3705c226b00c5a25a19d01cab4ac4b5676ab |
| `outputs/Mechanical_Design_App/js-tests/flat-floor.js` | 73541a9b52d854deabc23bf63d85114c77f43f4acf2cb9edba6459af0afe35a7 | dea65bd652f3a70224211c4022cf6c4f88db88596587b810665938ff424a07a6 |
| `outputs/Mechanical_Design_App/js-tests/wizard-mount-default.js` | fd6561729fa9d3aa9234bb37d07d3cb0b7f6dae8ce7806f5a4bac00775cb44e0 | c58ace3fc29cda99e362e6f19740e907d1afb80714ae42ae43e6a6210449277c |
| `outputs/Mechanical_Design_App/port-openings.js` | 7f45d17cd18222b75d3f23813b2c232b2ec179241acd80c978d3dcc9307ff245 | 5cc93f646299c084382f9c34cc15e67c7a434f4bc1ea1fb04aae06fb5d640c75 |
| `outputs/Mechanical_Design_App/port_openings.py` | b7940267afa880852b60b7e48ca878d1cfda32eef9e904ce159a57e760c5c4ee | f85b75efff62f424b121a7ec3319858c83a31e1c3afed7c3c894481d36148c48 |
| `outputs/Mechanical_Design_App/test_tray_placement.py` | 4767bdd0f9bad486becf56f80d4ffc8edff53e41ca50d3462f952d1ee5966d6b | 350d0932ad6c3508546e0b548fe2fb37475df023a15e2b3f875ade8038fda5b8 |
| `outputs/Mechanical_Design_App/tray-placement.js` | ade4bf4069652188d6cff18157f58c23a564177f8d2498c2d645fcd83c94aa74 | 2763bb91849d12c7ea53948ecd96cb6f2c6a37f9238d75e31ceaafe6b419346e |
