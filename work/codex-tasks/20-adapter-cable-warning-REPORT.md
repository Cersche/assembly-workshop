# Task 20 report — 2026-10-19

Added the single connectorMismatch helper to cable-routes.js. It resolves actual ports (including saved overrides), ignores unknown/other/keystone and outside/removed ends, and appends the exact warning after existing warnings. Cable type and rack inputs are unchanged. Review gets an info-only adapter suggestion, no action, using the existing Ignore/pruneIgnored lifecycle. Inventory groups get one needs adapter note, ordered after check: incomplete even if an incomplete cable is encountered later. Existing sheet code inherits warnings without changes.

Existing files were copied byte-for-byte under docs/archive/codex/2026-10-19/ with original relative paths before editing. Only the permitted three modules and four test files changed. Two existing exact-shape assertions were updated for the explicitly requested new helper export and adapter rule key. No existing fixture or other existing assertion changed.

Commands actually run:

- Get-Content and rg to inspect the permitted cable modules/tests and relevant sheet implementation.
- Copy-Item to create the seven archive copies.
- Python 3.10 -B on stdin to edit the permitted modules/tests and calculate SHA-256/report contents. Task 19 also used apply_patch for its two new modules.
- powershell -NoProfile -ExecutionPolicy Bypass -File outputs/Mechanical_Design_App/run_checks.ps1, with output captured and summarized using Select-String. First task-20 run exposed a mistake in the new CSV assertion (it expected every field quoted); corrected the new assertion to match the existing selective CSV quoting. No product change was needed.
- Diagnostic: set PYTHONUTF8=1 in that command process, then C:/Program Files/Python310/python.exe -B work/gui-refinement/check_python.py. All 109 Python tests completed successfully with one OpenSCAD render test skipped. This includes all three unchanged FrontOpeningsFollowTheDevice integration tests. No source/runner encoding setting was changed.
- Final full run_checks command under its default environment: exit 1. Python: 109 run, 107 passed, 1 failed, 1 skipped. JavaScript: 163 run, 162 passed, 1 failed. Task-20 suites all pass: routes 19, suggestions 21, sheet 11, inventory 9. Task-19 new suites pass: 4 Python and 4 JS.

Remaining full-suite failures (also observed immediately after task 19):

- test_tray_placement.FrontOpeningsFollowTheDevice.test_js_sketch_markers_and_warnings_agree_with_the_build: default Windows subprocess decoding turns the UTF-8 degree sign into U+00C2/U+00B0. UTF-8 diagnostic above confirms it passes with correct decoding. The test file was not edited.
- js-tests/run.js:284, “LabRaxPorts wizard ports follow the slot tray placement”: line 297 still explicitly expects unmoved front opening [10,-4,20]; correct new behavior produces [15,-4,18]. Outside May change; left unchanged and reported for the integration owner.

Assumptions/open questions: known non-generic connector types use ctx.ports.TYPES labels; unrecognized type labels fall back to the raw type. No new decision is needed for the requested logic. Full checks require the integration owner to resolve the two issues above; they are not claimed passed. Adapter fit and all physical fit/strength remain UNKNOWN. Tests use temporary fixtures only; no user data, server control, renders, exports, printing, installs, commits or pushes. Task 18 was neither run nor changed. Work stops with these reports.

| File | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `outputs/Mechanical_Design_App/cable-routes.js` | 429185d2da44e4435308f520c872714f88e38a3347373c153b98a6e7f315a626 | ef5d53c838108e4ec01406d9a2d129f6e280b1ed132e7e7bc0e0a4a433f1fa2f |
| `outputs/Mechanical_Design_App/cable-suggest.js` | 60f52ecff89b52e94c33597bd2bd40519154ec36173d8cb67aa2112d2d82687d | 2478ff4910df2a254fd1f85b1c38d16653f258467cc5cdb5a11d60d6ada0b78c |
| `outputs/Mechanical_Design_App/cable-inventory.js` | a8ceaf908e04e5c7db7caca9fad55f16e8ee5335ffb040116f0d8c0eef563562 | ceb151fa81427250aadc21546c734beb5b4f95d32c5bfecd09d0222f2a938adf |
| `outputs/Mechanical_Design_App/js-tests/cable-routes.js` | 0a6b71f6f5261dd5b4d5b1c0d503db1121e5eb0b5d8864e4b317f18cb5d40753 | af0a53f388c5dbf21328db8f63afed5adc08242e8d39c346809badefa2e26917 |
| `outputs/Mechanical_Design_App/js-tests/cable-suggest.js` | c295d171f62cb0e9828e05344036548cd3f5fcbf4356aa5ff1a7896b597e413f | 3731068628db35030fcee41772c45301647fedb3c1319a6c4b6fa8b4c49c7592 |
| `outputs/Mechanical_Design_App/js-tests/cable-sheet.js` | 9ddbcfead4d0768dbae84cde699f5baa93e593d906cfc25dcbe0e5637808a4d3 | aa73cdc0ff07b29937887b4888227755688bc998eb9565a5412ed60c4dad80e7 |
| `outputs/Mechanical_Design_App/js-tests/cable-inventory.js` | f9e1bf4b3d30ef8f44f2abd371c1f579996cdf40232654bf43d77c6d2e8f7268 | 1c1205070170cfce830cd24f4d037aafa89cf3ff7e65fefb321d5edcad3a16ae |
