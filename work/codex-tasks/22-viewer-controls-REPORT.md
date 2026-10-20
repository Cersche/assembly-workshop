# Task 22 viewer controls — interrupted implementation report

2026-10-20. **INCOMPLETE — concurrent edits detected. Do not treat this working tree as ready for browser acceptance.** No commit or push was made, per the explicit task standing rules. No server was started/stopped, browser controlled, user data edited, geometry built, or export run.

## Why work stopped

During implementation, equipment-wizard.js was changed externally from this session's `ViewerControls.attach` / `presets` API to `ViewerControls.attachViewerControls` / `PRESETS`. The latter API is not exported by this session's viewer-controls.js. A separate `docs/archive/codex/2026-10-20/task-22-viewer-controls/` directory appeared alongside this session's `task-22/` archive. IDEAS.md also gained an unrelated entry externally. This is evidence of overlapping editing, contrary to the one-session-at-a-time rule. I stopped source edits rather than overwrite or reconcile another active session's work. Hashes below are observations at report creation, not a stable final deliverable.

## Work applied by this session

- Added viewer-controls.js: shared input, four-pixel drag threshold, left orbit, right/middle pan, cursor-anchored zoom, pointer cancellation, touch pinch, preset buttons, scoped keyboard presets and fit. Rebinding does not stack listeners.
- Wired rack view to shared GPU projection/picking/label transforms and retained left-click selection/port placement and right-click port connection. Original rack buttons reset pan. Wiring-sheet camera snapshots preserve pan.
- Wired mesh viewer, including software offsets and a local renderer adapter in viewer.js. The adapter duplicates the existing assembly renderer preparation to insert a camera transform without modifying assembly-studio.js outside the allowed list. A future permitted camera hook would avoid this duplication. Missing controls produce an explicit status message while allowing the model to render.
- Initially wired the wizard painter (also used by Place on tray) and its CSS-pixel pan. That binding was subsequently replaced externally with the incompatible API described above. The 2D placement drag and floor-first sorting were not changed by this session.
- Added script loading and manifest entries/hashes, six shared-control tests, and registration in run.js. Later source changes require another manifest refresh after reconciliation.
- Did not update the viewer-controls IDEAS line because concurrent edits were discovered first. Optional painter clipping improvements were not attempted.

## Bambu reference

The wiki page https://wiki.bambulab.com/en/software/bambu-studio/3d-scene-operations could not be fetched (402). Instead inspected the official source for the in-app shortcut list:
https://raw.githubusercontent.com/bambulab/BambuStudio/master/src/slic3r/GUI/KBShortcutsDialog.cpp (lines 206–234): left mouse rotates, right mouse pans, wheel zooms; Ctrl+0 default, Ctrl+1 top, Ctrl+2 bottom, Ctrl+3 front, Ctrl+4 behind, Ctrl+5 left, Ctrl+6 right, Ctrl+7 isometric; Z fits scene/selection. Official release notes https://github.com/bambulab/BambuStudio/releases describe wheel zoom centered on the pointer by default. These were current upstream sources, not a locally inspected installed Bambu version.

Differences: plain 0–7 aliases in addition to Ctrl+0–7, scoped to hovered/focused canvases and ignored while typing; middle-drag pan as requested (not separately listed in the inspected shortcut list); fit targets the viewer scene, not selected geometry; projection zoom rather than camera dolly. No modifier-based object editing. Browser verification of orientation, pinch, zoom, picking, and existing view buttons remains pending.

## Verification and commands actually run

- Read AGENTS.md, PROJECT.md, HANDOFF.md, ROADMAP.md, task README and specification; targeted Get-Content/rg source inspection and git status/diff checks only.
- `git pull`: initially failed opening .git/FETCH_HEAD (sandbox permission); escalated retry returned “Already up to date.”
- Byte copies via PowerShell Copy-Item into docs/archive/codex/2026-10-20/task-22/, preserving path structure, before this session edited existing files.
- Python 3.10 stdlib inline editing/hashing commands and apply_patch; UTF-8, no installations.
- Required check command: `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1`.
- Baseline: exit 0, RESULT all checks passed. Output was truncated by the tool, so the baseline's individual totals were not retained as a separate log.
- First post-edit run: 114 Python tests, OK with one render test skipped; 172 JS tests, 169 passed / 3 failed. Two old viewer-startup fixtures do not load the new dependency; one rack-BOM source-extraction fixture failed due to CRLF conversion. Restored LF and made missing-controls degradation explicit. Six new shared-input tests passed. No test files outside the allowed new-test/run.js scope were changed.
- A subsequent attempted patch (wizard fit and an additional renderer test) failed its context check after external edits were detected; neither addition was applied.
- Final read-only check run at interruption: subprocess exit 1. Summary follows. Passing tests would not resolve the incompatible wizard API or establish browser acceptance.

```text
Ran 114 tests in 3.901s
OK (skipped=1)
ℹ tests 35
ℹ pass 34
ℹ fail 1
ℹ skipped 0
ℹ tests 26
ℹ pass 26
ℹ fail 0
ℹ skipped 0
ℹ tests 17
ℹ pass 17
ℹ fail 0
ℹ skipped 0
ℹ tests 9
ℹ pass 9
ℹ fail 0
ℹ skipped 0
ℹ tests 4
ℹ pass 4
ℹ fail 0
ℹ skipped 0
ℹ tests 9
ℹ pass 9
ℹ fail 0
ℹ skipped 0
ℹ tests 5
ℹ pass 5
ℹ fail 0
ℹ skipped 0
ℹ tests 19
ℹ pass 19
ℹ fail 0
ℹ skipped 0
ℹ tests 21
ℹ pass 21
ℹ fail 0
ℹ skipped 0
ℹ tests 11
ℹ pass 11
ℹ fail 0
ℹ skipped 0
ℹ tests 9
ℹ pass 9
ℹ fail 0
ℹ skipped 0
ℹ tests 7
ℹ pass 7
ℹ fail 0
ℹ skipped 0
RESULT: FAILED or incomplete
```

## SHA-256 (raw bytes)

Before hashes are from this session's byte archives. After hashes include any overlapping external edits present at report creation. Manifest hashes separately normalize CRLF to LF.

| File | Before | At report creation |
| --- | --- | --- |
| `outputs\Mechanical_Design_App\viewer-controls.js` | `NEW` | `5a54ce48c5b0b22f972b65b4990448f90a822c455fbd8003dfa7697a2be067ed` |
| `outputs\Mechanical_Design_App\workspace.js` | `b726126399f7f17b8a554b71d171c741ffb36fe26911f70a7734b06283169234` | `02f6543b23f9da8d622fbedc5389745b0472c4e565112d170fb346f0f955b41d` |
| `outputs\Mechanical_Design_App\viewer.js` | `0778667599b39a3ea6761e82a9cd8a54239782f7880213b162ad6eac86f637fb` | `aae1dfe7bdd022fc68f33166c5c76018ddaf3be32e39db395219c92ec8ff8440` |
| `outputs\Mechanical_Design_App\equipment-wizard.js` | `dca0332e8651dd54f5d4e03f4e6e9ea56e305bc1d3e70c971e67253cdbfb01ee` | `2b09b4a3b2878186481467aad5105f48d71e36d98d70effb417603b6c64508c6` |
| `outputs\Mechanical_Design_App\index.html` | `fa8b33406ab66d89541addcfb40d93fbf15b9778c3dab42ed86720bbd61e5ca1` | `aa2fb36da147339922232cadf8f67c72e77c276b2e1531bcdfe02ae15b4f1a76` |
| `outputs\Mechanical_Design_App\asset-manifest.json` | `8bd0e566cad97a512e0089e6626bde84067c7499b26374b114ec28f18d8a273b` | `1948a4dc975c9f5934c39ea9618d530486fc399dfab034698ebc7f07e867d1e2` |
| `outputs\Mechanical_Design_App\js-tests\viewer-controls.js` | `NEW` | `e097b06845be2d256422bc70c425f07804be9ce7c113824d5bcafcc5980838ba` |
| `outputs\Mechanical_Design_App\js-tests\run.js` | `4be0681c267a0bcd88dca6de9bca167974ff937b4eda6a7b580a2fc98c26097c` | `a1d3bb22cd6f21c67d4fa88c2d3014b2320ce68eb920a9f5517095480625351d` |
| `IDEAS.md` | `cad1fbbdbb0c86bde528a785106ab632cb8c8e7030211054f03dc65c1cbe6342` | `0fd5b4fa820be8a7beceec54b1ef1a8492f4b7d2c49ee609b233004713326f7e` |

## Remaining work

Establish which session owns task 22, reconcile the controls API and all call sites, review the local assembly adapter, finish IDEAS status, regenerate changed asset hashes, and rerun the complete checks. Then Claude can browser-check on disposable data. Do not use the mixed working tree as a completed implementation. Physical fit/strength remain UNKNOWN. No changes to HANDOFF.md, commits or pushes were made because this specific task authorizes only its May change list and says to write the report then stop.
