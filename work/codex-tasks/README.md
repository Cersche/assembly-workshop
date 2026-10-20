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
