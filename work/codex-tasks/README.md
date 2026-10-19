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
| [01-run-checks-baseline](01-run-checks-baseline.md) | ready |
| [02-readme-refresh](02-readme-refresh.md) | ready |
| [03-page-logic-tests](03-page-logic-tests.md) | ready (after 01) |
