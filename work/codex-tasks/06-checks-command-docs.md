# 06 — Document the working checks command

**Goal:** task 01 found `run_checks.ps1` fails with a plain `-File` call because Windows blocks scripts. The working command is `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1` (process-only; changes no system setting).

**Do:** update every place that tells someone how to run the checks (PROJECT.md, HANDOFF.md, ROADMAP.md, outputs/Mechanical_Design_App/README.md) to use that exact command, and update the test counts to 52 Python + 47 JS. Change only those lines.

**May change:** those four files, only the lines about running checks and test counts (archive copies first).

**Done when:** the report lists each line changed (before → after), then runs the command once and records the totals.
