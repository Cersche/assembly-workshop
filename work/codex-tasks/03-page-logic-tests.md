# 03 — Automated tests for page-level logic

**Goal:** ROADMAP "Now" item 1. The save controller and viewer startup are only checked by hand today.

**Do:** add JS tests for (a) the explicit atomic Save controller (dirty state, save success, save failure keeps the draft, no silent save on checks/exports) and (b) viewer startup (loads without errors, handles a missing or failed asset gracefully). Follow the style and runner of the existing JS tests that run_checks.ps1 already uses. Add the new tests to run_checks.ps1.

**May change:** new test files, and run_checks.ps1 (to register them).

**Don't:** modify app source to make a test pass. If a test exposes a real bug, mark that test as a known failure and describe the bug in the report.

**Done when:** run_checks.ps1 has been run before and after, with both results in the report, and every new test is listed with what it covers.
