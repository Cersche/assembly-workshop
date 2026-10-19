# Local link and path check — after approved organization

Static existence inspection only. No app/browser/HTTP/test/build/export action. Scope: root Markdown files, all docs/**/*.md and immediate work/*/Report.md. Markdown targets are checked relative to their document. Code-span/plain path candidates also use explicit app/reference/data/source contexts. Anchors, external URLs and HTTP route patterns are not filesystem targets. Preserved archived root docs keep their original link context; literal broken relocated Markdown links are listed, not rewritten. Inline shorthand/examples are separated from broken targets. This report contains no active link destinations and is excluded from scanning its own generated result. No protected file was edited.

Inspected 32 documents; 1966 existing reference records; 20 broken/missing historical-path records; 41 unresolved shorthand/example candidates; 9 dynamic patterns. Existing-reference totals are grouped by source to keep the report readable. These checks establish existence only, not that a command is safe or a feature works.

## Broken local links and missing historical paths

| Source file:line | Reference | Kind | Proposed fix |
| --- | --- | --- | --- |
| docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:120 | outputs/Physical_Test_Kit_2026-10-18/ | inline | Historical original path; retained destination: outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/ (exists). Use archive index; do not change protected sources. |
| docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:120 | outputs/Physical_Test_Kit_2026-10-18/ | plain path | Historical original path; retained destination: outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/ (exists). Use archive index; do not change protected sources. |
| docs/archive/handoffs/START_HERE_20261018.md:3 | AGENTS.md | markdown | Archived root-context Markdown link. Original target exists; use archive index or resolve from original root. Preserve archived bytes. |
| docs/archive/handoffs/START_HERE_20261018.md:3 | PROJECT.md | markdown | Archived root-context Markdown link. Original target exists; use archive index or resolve from original root. Preserve archived bytes. |
| docs/archive/handoffs/START_HERE_20261018.md:3 | HANDOFF.md | markdown | Archived root-context Markdown link. Original target exists; use archive index or resolve from original root. Preserve archived bytes. |
| docs/archive/handoffs/START_HERE_20261018.md:30 | work/gui-refinement/Report.md | markdown | Archived root-context Markdown link. Original target exists; use archive index or resolve from original root. Preserve archived bytes. |
| docs/archive/handoffs/START_HERE_20261018.md:30 | work/gui-refinement/Verification.json | markdown | Archived root-context Markdown link. Original target exists; use archive index or resolve from original root. Preserve archived bytes. |
| docs/archive/handoffs/START_HERE_20261018.md:30 | work/gui-refinement/Decisions.json | markdown | Archived root-context Markdown link. Original target exists; use archive index or resolve from original root. Preserve archived bytes. |
| docs/archive/handoffs/START_HERE_20261018.md:32 | work/gui-refinement/After_Authorized_Draft_Save.json | markdown | Archived root-context Markdown link. Original target exists; use archive index or resolve from original root. Preserve archived bytes. |
| docs/archive/handoffs/START_HERE_20261018.md:75 | work/gui-refinement/Report.md | markdown | Archived root-context Markdown link. Original target exists; use archive index or resolve from original root. Preserve archived bytes. |
| docs/archive/handoffs/START_HERE_20261018.md:75 | work/assembly-instances/Report.md | markdown | Archived root-context Markdown link. Original target exists; use archive index or resolve from original root. Preserve archived bytes. |
| docs/archive/handoffs/START_HERE_20261018.md:75 | work/rack-scene/Report.md | markdown | Archived root-context Markdown link. Original target exists; use archive index or resolve from original root. Preserve archived bytes. |
| docs/archive/handoffs/START_HERE_20261018.md:75 | work/rack-geometry-recovery/Recovery_Report.md | markdown | Archived root-context Markdown link. Original target exists; use archive index or resolve from original root. Preserve archived bytes. |
| docs/archive/handoffs/START_HERE_20261018.md:75 | outputs/Phase7_Closeout/Closeout_Report.md | markdown | Archived root-context Markdown link. Original target exists; use archive index or resolve from original root. Preserve archived bytes. |
| docs/archive/handoffs/START_HERE_20261018.md:75 | work/gui-restoration/Recovered_GUI_Decisions.json | markdown | Archived root-context Markdown link. Original target exists; use archive index or resolve from original root. Preserve archived bytes. |
| docs/housekeeping/Audit.md:29 | patch_dialog.py | inline | Historical original path; retained destination: docs/archive/scripts/patch_dialog.py (exists). Use archive index; do not change protected sources. |
| docs/housekeeping/Audit.md:142 | patch_dialog.py | inline | Historical original path; retained destination: docs/archive/scripts/patch_dialog.py (exists). Use archive index; do not change protected sources. |
| docs/housekeeping/Audit.md:191 | outputs/Physical_Test_Kit_2026-10-18/ | inline | Historical original path; retained destination: outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/ (exists). Use archive index; do not change protected sources. |
| docs/housekeeping/Audit.md:191 | outputs/Physical_Test_Kit_2026-10-18/ | plain path | Historical original path; retained destination: outputs/SUPERSEDED_Physical_Test_Kit_2026-10-18_old_2hole/ (exists). Use archive index; do not change protected sources. |
| docs/housekeeping/Audit.md:212 | patch_dialog.py | inline | Historical original path; retained destination: docs/archive/scripts/patch_dialog.py (exists). Use archive index; do not change protected sources. |

## Unresolved shorthand, examples and proposed paths

These are not asserted broken. No file was created merely to satisfy an old proposal/path example.

| Source | Candidate | Interpretation |
| --- | --- | --- |
| AGENTS.md:28 | data/history | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:55 | generic_tray.scad | Historical proposal name; implemented template is outputs/Mechanical_Design_App/equipment_tray.scad. Do not create this old proposal. |
| docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:70 | data/equipment-library.json | Runtime-created or example filename; absence is not a broken documentation link. |
| docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:120 | __source.scad | Runtime-created or example filename; absence is not a broken documentation link. |
| docs/archive/handoffs/PROJECT_pre_housekeeping_20261018.md:16 | outputs/work | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/archive/README.md:3 | outputs/work | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:9 | work/output | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:66 | Pi4_fit_inspection.md | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:66 | Pi4_fit_review_REFERENCE_ONLY.3mf | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:127 | docs/archive/phase7-readiness/ | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:153 | app_v04.py | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:153 | app_v05.py | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:153 | app_v06.py | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:153 | app_v061.py | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:153 | app_v07.py | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:153 | app_v08.py | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:154 | pack_v04.py | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:154 | pack_v05.py | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:154 | pack_v06.py | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:154 | pack_v061.py | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:154 | pack_v07.py | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:154 | pack_v08.py | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:155 | test_viewer_v06.cjs | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:155 | test_viewer_v061.cjs | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:155 | test_viewer_v08.cjs | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:156 | joint_collision.stl | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:157 | pcb_collision.stl | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:158 | usb_collision.scad | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:158 | usb_collision.stl | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:172 | work/gui-restoration/Restoration_Report | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:181 | data/sources | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:208 | docs/archive/phase7-readiness/Readiness_Plan.md | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:208 | Verification_Report.md | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:208 | Evidence_Register.csv | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:208 | docs/phase7-readiness/README.md | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Audit.md:216 | outputs/work | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/housekeeping/Code_Map.md:61 | data/cache | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| docs/phase7-readiness/Readiness_Plan.md:7 | outputs/work | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| HANDOFF.md:34 | outputs/work/data | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| PROJECT.md:31 | outputs/work | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |
| work/assembly-instances/Report.md:11 | data/artwork/ | Unresolved prose/path candidate, shorthand or historical proposed destination; not asserted broken. Confirm context. |

## Dynamic patterns

| Source | Pattern | Disposition |
| --- | --- | --- |
| docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:54 | revisions/<sha256>/ | Dynamic/example pattern; not an absent literal file |
| docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:66 | data/equipment-revisions/<sha>/ | Dynamic/example pattern; not an absent literal file |
| docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:89 | C:\Program Files\FreeCAD* | Dynamic/example pattern; not an absent literal file |
| docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md:125 | rack-references/component_<ref>_<id>.json | Dynamic/example pattern; not an absent literal file |
| docs/housekeeping/Audit.md:168 | outputs/Phase7_Closeout/{Closeout_Report.md,Final_Checks.json,Next_Chat_Prompt.md,Preservation_Report.json} | Dynamic/example pattern; not an absent literal file |
| docs/housekeeping/Audit.md:169 | outputs/Session_Handoff_20261018/{Final_Checks.json,Next_Chat_Prompt.md,Preservation_Report.json} | Dynamic/example pattern; not an absent literal file |
| docs/housekeeping/Audit.md:170 | work/gui-restoration/{HTTP_Checks.json,Recovered_GUI_Decisions.json,Restoration_Report.md,Verification.json} | Dynamic/example pattern; not an absent literal file |
| docs/housekeeping/Audit.md:192 | .../referenced-chatgpt-conversation-this-is-an | Dynamic/example pattern; not an absent literal file |
| docs/housekeeping/Audit.md:199 | work/*/Report.md | Dynamic/example pattern; not an absent literal file |

## Existing reference counts by source

| Document | Existing reference records |
| --- | --- |
| AGENTS.md | 6 |
| GEMINI_HANDOFF.md | 9 |
| HANDOFF.md | 32 |
| PROJECT.md | 28 |
| START_HERE.md | 9 |
| docs/archive/README.md | 36 |
| docs/archive/handoffs/GEMINI_HANDOFF_20261018.md | 33 |
| docs/archive/handoffs/HANDOFF_pre_housekeeping_20261018.md | 36 |
| docs/archive/handoffs/PROJECT_pre_housekeeping_20261018.md | 38 |
| docs/archive/handoffs/START_HERE_20261018.md | 38 |
| docs/housekeeping/Audit.md | 273 |
| docs/housekeeping/Backup_Manifest_Summary.md | 493 |
| docs/housekeeping/Changes.md | 334 |
| docs/housekeeping/Code_Map.md | 214 |
| docs/housekeeping/Data_Locations.md | 37 |
| docs/housekeeping/Decision_Log.md | 135 |
| docs/housekeeping/Open_Unknowns.md | 163 |
| docs/phase7-readiness/Verification_Report.md | 2 |
| work/assemble-studio/Report.md | 7 |
| work/assembly-instances/Report.md | 5 |
| work/gui-refinement/Report.md | 2 |
| work/gui-render-repair/Report.md | 5 |
| work/gui-style-delivery/Report.md | 3 |
| work/rack-branding/Report.md | 1 |
| work/rack-scene/Report.md | 4 |
| work/render-studio/Report.md | 17 |
| work/startup-reliability/Report.md | 4 |
| work/workflow-audit/Report.md | 2 |

Current root entry documents: no missing local Markdown links found. Archived relative links remain intentionally byte-preserved and are mapped by docs/archive/README.md. Historical Phase 1 Audit references to patch_dialog.py and old kit paths now have retained destinations recorded above.

## Plain absolute-path follow-up

Also examined Windows absolute paths written as plain prose (not just links/code spans). 8 literal candidates exist; 13 candidates contain surrounding prose, wildcard/example syntax or remain context-dependent and are not asserted broken. The following additional missing historical workspace reference is confirmed:

| Source file:line | Absolute path | Proposed fix |
| --- | --- | --- |
| docs/phase7-readiness/Verification_Report.md:3 | C:/Users/brian/Documents/Codex/2026-10-17/referenced-chatgpt-conversation-this-is-an | Historical former workspace is absent. Current canonical root is C:/Users/brian/Documents/Codex/2026-10-17/Assembly Workshop. Preserve historical record. |
