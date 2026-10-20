# Keystone render sweep report

Date: 2026-10-19 (Brian local time). Task 16; investigation only.

## Result

22 PASS, 2 SKIP, 0 FAIL across 24 requested cases.
Every returned part was checked with mesh_revision.read_mesh(); nudge_mm below is from revision.json. Fit, retention and strength remain UNKNOWN. No code or mesh checks changed.

## Coverage

Base spec: `{"name": "Sweep", "dev_w": 100, "dev_d": 80, "dev_h": 20, "device_mount": "inserts", "joint": "screw", "holes": [[10, 10]]}`. Device height stayed 20 mm; clean() required no increase. Each accepted case used its own fresh directory and equipment.render(spec, temp_dir). No existing cache was reused.

| Case | U | Quality | Joint | Keystone X mm | Result | nudge_mm per part | Error |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | standard | screw | [-105] | SKIP | {} | Keystone X must be between -102 and 102 mm. |
| 2 | 1 | standard | screw | [-100] | PASS | {"tray": 0, "faceplate": 0} |  |
| 3 | 1 | standard | screw | [-90] | PASS | {"tray": 0, "faceplate": 0} |  |
| 4 | 1 | standard | screw | [-80] | PASS | {"tray": 0, "faceplate": 0} |  |
| 5 | 1 | standard | screw | [-75] | PASS | {"tray": 0, "faceplate": 0} |  |
| 6 | 1 | standard | screw | [75] | PASS | {"tray": 0, "faceplate": 0} |  |
| 7 | 1 | standard | screw | [80] | PASS | {"tray": 0, "faceplate": 0} |  |
| 8 | 1 | standard | screw | [90] | PASS | {"tray": 0, "faceplate": 0} |  |
| 9 | 1 | standard | screw | [100] | PASS | {"tray": 0, "faceplate": 0} |  |
| 10 | 1 | standard | screw | [105] | SKIP | {} | Keystone X must be between -102 and 102 mm. |
| 11 | 2 | standard | screw | [-100, 100] | PASS | {"tray": 0, "faceplate": 0} |  |
| 12 | 3 | standard | screw | [-90, 95] | PASS | {"tray": 0, "faceplate": 0} |  |
| 13 | 1 | draft | screw | [-75] | PASS | {"tray": 0, "faceplate": 0} |  |
| 14 | 1 | fine | screw | [100] | PASS | {"tray": 0, "faceplate": 0} |  |
| 15 | 2 | draft | screw | [-75] | PASS | {"tray": 0, "faceplate": 0} |  |
| 16 | 2 | fine | screw | [100] | PASS | {"tray": 0, "faceplate": 0} |  |
| 17 | 3 | draft | screw | [-75] | PASS | {"tray": 0, "faceplate": 0} |  |
| 18 | 3 | fine | screw | [100] | PASS | {"tray": 0, "faceplate": 0} |  |
| 19 | 5 | draft | screw | [-75] | PASS | {"tray": 0, "faceplate": 0} |  |
| 20 | 5 | fine | screw | [100] | PASS | {"tray": 0, "faceplate": 0} |  |
| 21 | 1 | draft | single | [75] | PASS | {"combined": 0} |  |
| 22 | 1 | fine | single | [75] | PASS | {"combined": 0} |  |
| 23 | 2 | draft | single | [75] | PASS | {"combined": 0} |  |
| 24 | 2 | fine | single | [75] | PASS | {"combined": 0} |  |

The requested -105 and +105 mm positions are rejected by clean(): the accepted range is -102 to +102 mm (PLATE_HALF 126 minus 24). They were skipped without bypassing validation.

## Commands actually run and results

- Get-Content read AGENTS.md, PROJECT.md, HANDOFF.md, ROADMAP.md, queue README, both task specs, Wizard_Fixes_Report.md and relevant source/docs. rg inspected render/clean/read_mesh, cached placement lookup, rack sketch and inspector code. Get-Command python resolved C:/Program Files/Python310/python.exe; both report files were absent.
- Initial PowerShell here-string piped to `python -B -u -` began the same 24-case sweep in sandbox temporary data. Case 1 was rejected as expected; case 2 reached a folder rename and failed with WinError 5 Access is denied (no captured mesh-check failure). The process was interrupted with Ctrl+C, exit 1. This was an environment failure, not evidence against geometry; subsequent partial work in that attempt is not counted here.
- Re-ran the investigation with approved escalation using a PowerShell here-string piped to `python -B -u -`. All 24 results above are from this rerun. Renderer: `C:\Program Files\OpenSCAD\openscad.exe`. No runner file was written.
- From outputs/Mechanical_Design_App, ran `python -B -m unittest test_keystone_mesh -v` with AW_RENDER_TESTS=1 and TMP/TEMP set to the new scratch directory. Exit 0.

```text
test_keystone_faceplates_pass_the_mesh_check_without_nudge (test_keystone_mesh.KeystoneRenderTests) ... ok
test_block_is_clipped_by_the_same_box_as_the_plate_opening (test_keystone_mesh.StaticKeystoneTests) ... ok
test_golden_table_and_tightness_unchanged (test_keystone_mesh.StaticKeystoneTests) ... ok
test_plate_flush_depths_land_on_the_2d_grid (test_keystone_mesh.StaticKeystoneTests) ... ok

----------------------------------------------------------------------
Ran 4 tests in 22.501s

OK
```

Both the interrupted scratch directory and the completed sweep directory were removed/confirmed absent: True. Completed sweep path: `C:\Users\brian\AppData\Local\Temp\aw-task16-hi4bycc7`. Cleanup targeted only newly created diagnostic data.

## Files and SHA-256

New persistent file: work/codex-tasks/16-keystone-render-sweep-REPORT.md; before: absent. Its final hash is verified externally after writing (a self-hash cannot be embedded). No other persistent file was changed. Inspected source hashes before / after:

- `outputs/Mechanical_Design_App/equipment.py`: `fdb69c38b82339773167255aeb8e860fa11cde22078fed1c1709f52867ce9cf9` / `fdb69c38b82339773167255aeb8e860fa11cde22078fed1c1709f52867ce9cf9`.
- `outputs/Mechanical_Design_App/equipment_tray.scad`: `4c98aa5ba251a87edf641276f71a022f09b273633fec2421c5f63606c903f5fa` / `4c98aa5ba251a87edf641276f71a022f09b273633fec2421c5f63606c903f5fa`.
- `outputs/Mechanical_Design_App/mesh_revision.py`: `a569e208d9ad2be574d9f7c22fba8125e4df9daf70a6bd690792f6fb95832962` / `a569e208d9ad2be574d9f7c22fba8125e4df9daf70a6bd690792f6fb95832962`.
- `outputs/Mechanical_Design_App/test_keystone_mesh.py`: `5ed17018bef865dcd8ea3b17fc0b1ac3e0eae176e5c7dc546d5e893008d74d41` / `5ed17018bef865dcd8ea3b17fc0b1ac3e0eae176e5c7dc546d5e893008d74d41`.

## Assumptions and open questions

Task 16 explicitly authorizes disposable diagnostic renders and temporary-folder cleanup. No bundles or delivery exports were made. No user data, live server, desktop session, physical test, print, commit, push, install or upload was used. This selected sweep covers each requested value, not every combination. No missing user decision blocked this investigation.

No final failing case required bad-edge diagnostics.
