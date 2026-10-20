# Rack-view placement documentation report

Date: 2026-10-19 (Brian local time). Task 17, completed after task 16.

## Changes

Updated only the stale rack-view paragraph in outputs/Mechanical_Design_App/README.md and the ending of the equipment wizard paragraph in hardware-records.md. Both now describe library build / existing exact render / box sketch behavior, the lookup-only route, sketch details, inspector note and keystone mesh fix. Fit, retention and strength remain UNKNOWN. Every byte outside the two paragraph replacements is unchanged; existing scope limits and UNKNOWNs were preserved.

## Sources confirmed

- work/equipment-wizard-options/Wizard_Fixes_Report.md records the keystone fix and current rack-view behavior.
- equipment.py: allocation_spec() merges slot tray choices; cached_allocation_render() checks existing revision.json files for standard/draft/fine quality and never calls render(). app.py routes /api/equipment-placement-mesh to that lookup.
- equipment-wizard.js: partsFor() selects the library build when no slot tray settings exist, an available exact render otherwise, or rackSketch(). Refresh is wired after explicit preview/build.
- tray-placement.js: schematic()/rackSketch() reflect plate U height, tray size/offset/rotation and rear bracket, with dark keystone/port opening blocks. workspace.js identifies the sketch with TRAY_SKETCH/traySketch().
- Task 16: 22 accepted sweep cases passed with zero nudges; two out-of-range cases skipped; four keystone tests passed. This is digital evidence, not physical approval.

## Commands actually run and results

- Get-Content and rg read the task sources, relevant Python/JS code and both documents. No desktop/browser session was started.
- Initial PowerShell here-string piped to `python -B -` archived and edited README.md successfully, then failed while printing its Unicode diff to the cp1252 console (UnicodeEncodeError for the arrow character). hardware-records.md and this report had not yet been written. The archived README bytes and edited file remained intact.
- Continued with a UTF-8 stdout configuration using another PowerShell here-string piped to `python -B -`. Archived hardware-records.md byte-for-byte before editing, made its single replacement, verified both files and wrote this report. Exit 0 if this report is present.
- Verification: each document has exactly one changed paragraph; reconstructing the current bytes from its archive by that one replacement matches exactly. The obsolete note is absent and the new text includes the lookup-only behavior, sketch and UNKNOWN limits. SHA-256 values are below. No unrelated document wording changed.
- No new tests were needed for these documentation edits. No full-suite rerun, server access/restart, render, export, user-data access, install, commit, push or upload was performed for task 17. Task 16 renders/tests are recorded in its own report.

## Files and SHA-256

| File | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| `outputs/Mechanical_Design_App/README.md` | `6f25c6da372e17f3021b00fa7466c07e47872dbb9872eda5b5928b743ff16f16` | `df14a30a7123bd621eb31a7e85e3726e16a951a6d1bd3e9a3a9ea663594d8647` |
| `docs/archive/codex/2026-10-19/task17/README.md` | absent | `6f25c6da372e17f3021b00fa7466c07e47872dbb9872eda5b5928b743ff16f16` |
| `outputs/Mechanical_Design_App/hardware-records.md` | `b1bc7da88cc5640c5374b13a327f1ad33bc1705864f0709c4119c9a2d38e3dd8` | `9470c7b4b3290261e41c8d3df04d9422426d74a367b7047da5b47f7a739827cb` |
| `docs/archive/codex/2026-10-19/task17/hardware-records.md` | absent | `b1bc7da88cc5640c5374b13a327f1ad33bc1705864f0709c4119c9a2d38e3dd8` |

New report: work/codex-tasks/17-docs-rack-view-placement-REPORT.md (before: absent). Its SHA-256 is checked after writing; no self-referential hash is embedded. Task 16 report was read only; its SHA-256 is 4fe25f03d912a0d219420db85301d227932670fd96ded907515df4c9f095e463.

## Assumptions and open questions

The task authorizes the required archive copies in addition to its two document edits and report. Static source confirmation is sufficient for this documentation task; no new browser acceptance run is claimed. Existing unrelated test counts and historical physical-scope wording were retained because only the specified sentences were in scope. No blocking questions or further changes are proposed. Both requested reports are written; stopping as requested.
