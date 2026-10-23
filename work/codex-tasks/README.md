# Codex task queue

Brian hands Codex one file from here: "Do work/codex-tasks/<task>.md". Claude writes specs and reviews results.

## Standing rules (apply to every task)

- Read AGENTS.md, PROJECT.md, HANDOFF.md, ROADMAP.md first. They override any task file.
- No deletions, git clean/reset/checkout, commits, pushes, installs, subagents, printing, uploads or exports.
- Never touch data/normal-use or other user data. Tests use new temporary data only.
- Never start bare `python app.py`; never stop/restart the live server on 8765 unless the task says so.
- Python 3.10 stdlib, UTF-8. Physical fit/strength stays UNKNOWN. No phase numbers in new docs.
- Before editing an EXISTING file, save a byte-for-byte copy to docs/archive/codex/<date>/ (new files need no copy).
- Stay inside the task's "May change" list. If something else seems to need changing, write it in the report instead.
- Finish by writing work/codex-tasks/<task>-REPORT.md: files changed (with before/after SHA-256), commands actually run with results, assumptions, open questions. Then stop.

## Queue

| Task | Status |
| --- | --- |
| [01-run-checks-baseline](01-run-checks-baseline.md) | done, reviewed by Claude |
| [02-readme-refresh](02-readme-refresh.md) | done, reviewed by Claude |
| [03-page-logic-tests](03-page-logic-tests.md) | done, reviewed by Claude (52 Py + 47 JS pass) |
| [04-bom-follows-segments](04-bom-follows-segments.md) | done (plan reviewed and approved by Claude) |
| [05-library-resave-proposal](05-library-resave-proposal.md) | done (Brian chose recommendations 2026-10-19) |
| [06-checks-command-docs](06-checks-command-docs.md) | done, checked by Claude |
| [07-bom-implementation](07-bom-implementation.md) | done, reviewed by Claude (hashes match; note: workspace.js converted to CRLF) |
| [08-library-rebuild-copy](08-library-rebuild-copy.md) | done, reviewed by Claude (67 Py + 72 JS pass; equipment-wizard.js converted to CRLF) |
| [09-cable-schema](09-cable-schema.md) | done (71 Python + 94 JS pass; see task report) |
| [10-cable-routes-logic](10-cable-routes-logic.md) | done (exact API; 71 Python + 94 JS pass; see task report) |
| [11-cable-suggest-schema](11-cable-suggest-schema.md) | done, reviewed by Claude (73 Py + 114 JS pass) |
| [12-cable-suggest-logic](12-cable-suggest-logic.md) | done, reviewed by Claude (exact API; wording tweaked at integration) |
| [13-cable-sheet-logic](13-cable-sheet-logic.md) | done, reviewed by Claude (exact API; 73 Py + 137 JS pass after integration) |
| [14-cable-inventory-logic](14-cable-inventory-logic.md) | done, reviewed by Claude; Review card integrated (defaults PROPOSED, Brian to confirm [Parts_Order_Decisions](../cable-management/Parts_Order_Decisions.md)) |
| [15-docs-refresh-wizard-placement](15-docs-refresh-wizard-placement.md) | done, reviewed by Claude (95 Py + 152 JS pass) |
| [16-keystone-render-sweep](16-keystone-render-sweep.md) | done, reviewed by Claude (22 pass, 2 out-of-range skips, 0 fail) |
| [17-docs-rack-view-placement](17-docs-rack-view-placement.md) | done, reviewed by Claude |
| [18-placement-render-sweep](18-placement-render-sweep.md) | done, reviewed by Claude (24 pass / 2 fail: opening in front of a screw joint; fixed by moving joints) |
| [19-front-openings-logic](19-front-openings-logic.md) | done, reviewed by Claude (integrated; 110 Py + 163 JS pass) |
| [20-adapter-cable-warning](20-adapter-cable-warning.md) | done, reviewed by Claude (integrated; shown in Review/sheet/parts order) |
| [21-pi4-deep-clean](21-pi4-deep-clean.md) | done, reviewed by Claude (113 Py + 166 JS pass; 117 → 11 Pi lines) |
| [22-viewer-controls](22-viewer-controls.md) | done, reviewed by Claude (ran twice in parallel by mistake; Claude reconciled the wizard API, served viewer-controls.js in app.py, fixed hints; checks pass, browser-checked) |
| [23-flat-device-low-floor](23-flat-device-low-floor.md) | done, reviewed by Claude (119 Py + 176 JS pass; OptiPlex STEP browser-checked: 2U default + flat hint, Sits flat = 1U, joint and front opening OK in exact preview) |
| [24-wizard-mount-default](24-wizard-mount-default.md) | done, reviewed by Claude (120 Py + 180 JS pass; OptiPlex STEP saved with 0 holes as 1U Sits flat in the browser) |
| [25-faceplate-44-standard](25-faceplate-44-standard.md) | done, reviewed by Claude (44.4 plate, Z=0 = slot bottom; exact render: plate Z 0.02-44.42, slots 6.32/38.13) |
| [26-tray-width-hard-limit](26-tray-width-hard-limit.md) | done, reviewed by Claude (204 mm hard limit + rotate hint; Claude de-duplicated the step-1 message and fixed the stale 230 mm sketch label) |
| [27-sleeve-flush-front](27-sleeve-flush-front.md) | done, reviewed by Claude (127 Py + 183 JS pass; OptiPlex STEP sleeve on rear support exact-rendered: closed meshes, window 183.5 x 39.1, 6 mm walls, 1.5 mm lips) |
| [28-foot-pockets](28-foot-pockets.md) | done, reviewed by Claude (fixed case-in-floor bug; OptiPlex STEP: 4 feet 2.8 mm found, sleeve band 1.8 → 4.6 mm, exact render closed) |
| [29-rear-bracket-cable-openings](29-rear-bracket-cable-openings.md) | done, reviewed by Claude (139 Py + all JS pass; legacy source byte-identical; OptiPlex + 2U inserts brackets render closed, openings measured = report; SLV-D coupon made from it) |
| [30-rear-bracket-styles](30-rear-bracket-styles.md) | done, reviewed by Claude (142 Py + all JS pass; all 5 styles render closed; follow-ups: outer lips block flat printing, vents sparse) |
| [31-rear-bracket-lips-and-vents](31-rear-bracket-lips-and-vents.md) | done, reviewed by Claude (145 Py + all JS pass; outer face flat, lips clash-free, vents 62 holes ~51 % open) |
| [32-protrusion-detection](32-protrusion-detection.md) | done, reviewed by Claude (155 Py + 204 JS pass; real SG108 STEP: plug found, 3 questions, size from case, keep-clear zone cuts the rear bracket; Claude fixed an over-cut on Slots/Vents) |
| [33-front-position-and-bezel](33-front-position-and-bezel.md) | done, reviewed by Claude (exact renders closed; chamfer 45°, rounded 8-step, 2 mm webs held; keystones/slots untouched; defaults byte-identical) |
| [34-protrusion-polish](34-protrusion-polish.md) | done, reviewed by Claude (159 Py + 210 JS pass; real SG108 STEP: 1 back question, warning says 2.1 mm band vs 5 mm; front-gap messages merged to one; no geometry change) |
| [35-webgl-small-viewers](35-webgl-small-viewers.md) | done, reviewed 2026-10-22: WebGL for the wizard / Place on tray preview, 2D painter kept as fallback, 16 ms budget |
| [38-faceplate-only-slot](38-faceplate-only-slot.md) | done, reviewed by Claude 2026-10-22 (183 Py + 234 JS pass; hashes match; 10-keystone reference rebuilt exactly; browser click-through NOT yet done) |
