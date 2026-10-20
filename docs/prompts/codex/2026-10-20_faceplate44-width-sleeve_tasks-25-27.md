# Codex prompt · 2026-10-20 · 44.4 mm faceplate, width limit, sleeve mount (tasks 25-27)

Paste this into Codex (once, in one Codex session):

```
Do these three tasks in order, following the standing rules in work/codex-tasks/README.md:
1. work/codex-tasks/25-faceplate-44-standard.md
2. work/codex-tasks/26-tray-width-hard-limit.md
3. work/codex-tasks/27-sleeve-flush-front.md
Finish each task's REPORT file and get run_checks.ps1 passing before starting the next. If a task's checks fail and you can't fix them inside its "May change" list, write its report and stop; don't start the later tasks. After task 27's report, stop.
```

What it does:
- makes the 44.4 mm faceplate (coupon-proven) the standard and fixes the 1.225 mm slot offset;
- blocks trays wider than the rack opening and suggests Rotate 90°;
- adds a "Sleeve" mount with a flush front window that also works on rear-post support (OptiPlex test case).
