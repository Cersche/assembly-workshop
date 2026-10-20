# Task 24 — wizard tray default mount report

Completed 2026-10-20. Implementation and automated checks complete; browser review remains for Claude. Fit and strength remain UNKNOWN.

## Changes

- Ports → Save now offers **Tray default mount**, using all five existing MOUNTS labels. New items still start with inserts; editing keeps the saved mount. Nothing switches mounts automatically.
- Save checks for no-hole inserts/pegs before sending a request, with the requested pointer to another tray default mount. The same guidance appears above the selector. A no-hole flat device reaches Save; backend clean() accepts it.
- Mount changes recompute U through LabRaxPortOpenings.autoU(spec) for a new item unless U was explicitly entered. The current wizard has no U input; the shared field handler tracks an explicit U input if used. Editing an existing item conservatively treats its saved U as explicit, since its provenance is unknown, and keeps it on mount changes. Reset clears that flag. Existing model-import auto-U behavior remains unchanged.
- Existing front-opening Z values remain untouched. The Ports note displays deviceLift(spec) and explicitly asks users to check their entered heights against the current lift. The step-1 flat hint points to the Ports tray default mount and per-slot Place on tray.
- Updated both changed frontend asset hashes using CRLF → LF normalization. Edited text files were written as UTF-8 with LF.
- Added four JavaScript regression tests using actual wizard closures with in-memory DOM/fetch fixtures, registered in js-tests/run.js, plus one Python clean() regression.

## Verification and commands run

- `git pull`: initial sandbox attempt failed opening .git/FETCH_HEAD (permission denied); approved elevated retry returned **Already up to date**.
- Read AGENTS.md, PROJECT.md, HANDOFF.md, ROADMAP.md, task README/spec and relevant source/tests with Get-Content and rg. Two attempted test-file reads used nonexistent paths; located the actual test files and continued. Initial `git status --short` was clean.
- Before editing: `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1` — exit 0, **119 Python tests (118 passed, 1 skipped), 176 JavaScript passed**.
- Archived the five existing files listed below byte-for-byte with Python 3.10 shutil.copyfile before editing. Applied targeted UTF-8 edits using Python 3.10 standard library and apply_patch; no packages installed.
- First after-change run of the same checks — exit 1: new Python fixture omitted required joint; an existing extracted-import JS fixture did not define the new U flag. Added joint='screw' to the fixture and retained the original model-import behavior, keeping the U guard scoped to mount changes.
- Final run of the same checks — exit 0, **120 Python tests (119 passed, 1 skipped), 180 JavaScript passed**. The skip is the opt-in OpenSCAD keystone render test. JS suite totals: 43 + 26 + 17 + 9 + 4 + 9 + 5 + 19 + 21 + 11 + 9 + 7 = 180.
- `git diff --stat`, targeted `git diff`, `git diff --check`, and `git status --short`: changes limited to allowed files and required archives; no whitespace errors. Git reported its normal LF-to-CRLF future-checkout warnings.
- SHA-256 calculated from actual file bytes with Python hashlib for the table below. Archive hashes supply the before values. Asset-manifest hashes separately normalize CRLF to LF as required.

No server started/stopped, no desktop session, no live user-data access, no renders or STL exports. Save was mocked in JS; this does not establish a real render/save or browser acceptance result.

## Files and SHA-256

Paths below are relative to outputs/Mechanical_Design_App/. Before copies are under docs/archive/codex/2026-10-20/task24/ with matching relative paths. The new test has no before copy.

| File | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `equipment-wizard.js` | `08baa1202dd18f1201e400428c9b4d3218b329ded372162f2ce42a71dce7b947` | `87695b32b719db7999494ecd76c05c9b41d77d020046aff2232bdb9388fce06d` |
| `port-openings.js` | `0a1436e9cc7d23d7459c602ba9dd0c724a0fe1e924cce782805752e153463b92` | `0a68b93f05732d0f7d1028f45c0fdff8c171f90a7e49aa94f6e7819b7ccdb845` |
| `asset-manifest.json` | `7d0e3e7a25645b24c4f92a1e5ab72123b266250e71f9e732d65ed5c8807682ff` | `5ff8980f3babd2bef080927dbf0c1fcbf0f04f3d3e3e7f1ca812d0069aad8a16` |
| `test_port_openings.py` | `4fd272442d496781781a8f06c4898db74520ba059894efe6a861a855c9f39ff6` | `a2278165c823ce26929e710cd749a70446a4c62ae31d6309a113a5856aff97cc` |
| `js-tests/run.js` | `08f09edd9a7e7973434997d7127c9572de129a75e79ad946087e91786c1eedfd` | `a2df72dd0c0f5fbdc858d3f583f8e49612a5c52deb0a45d11214d5b467e3a24a` |
| `js-tests/wizard-mount-default.js` | `NEW` | `97e046ec01e20ead8f8ed3092f2d834009eee1b5bc7af6ca9c48a05fc01702a2` |

The required new report is work/codex-tasks/24-wizard-mount-default-REPORT.md (no before file; no self-referential hash).

## Assumptions and remaining review

Saved U is preserved conservatively when changing an older item's default mount; new-item U is automatic on mount selection. No new U editor was added. Browser layout and real Save/render remain unverified and are left for Claude's review as the task requests. No other open implementation questions.

Followed the explicit task instruction to write this report and stop: no HANDOFF edit, commit, or push, despite the general session-end synchronization guidance. No changes outside the allowed implementation/test files and mandatory archive/report artifacts.
