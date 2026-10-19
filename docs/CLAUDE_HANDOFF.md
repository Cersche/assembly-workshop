# Claude handoff — working with Brian

For a Claude session on a new account that has none of the old session's memory. Read this after AGENTS.md, PROJECT.md, HANDOFF.md and ROADMAP.md. Written 2026-10-19.

## How Brian likes to work

- Brian is the owner and isn't an engineer. Explain plainly, keep turns efficient (his usage runs low), and give recommendations instead of surveys.
- **One paste-ready prompt per batch.** When handing work to Codex or another tool, combine every queued task into one prompt that runs them in order, with stop/skip conditions built in. No per-task back-and-forth.
- Memes are welcome now and then (text or ASCII, not every turn). Light shade at Codex ("Sam's demon child") is welcome.
- If Brian sends the same message twice in a row, reply **"YOU SURE ABOUT THAT?"** 🤨 first, then ask whether the resend was intentional before redoing work.
- No phase language ("Phase 6/7", milestones, "closed with limitations"). Plans live in ROADMAP.md (Now / Next / Later). Old phase-named folders are preserved history.
- Before deleting, overwriting or restarting anything, check first. Confirm before outward actions (pushes, uploads, printing).

## Setup facts

- **This PC is the only home** for the project, data and running app. The laptop and phone only steer sessions via Remote Control. Don't sync working copies elsewhere or expose the app on the LAN.
- **Official data is `data/normal-use`.** Start the app only via `outputs/Mechanical_Design_App/start.bat` (or the same `--existing-library --data …\data\normal-use` arguments). Before starting, check no other app.py is running. Never run bare `python app.py`.
- **Checks:** `powershell -NoProfile -ExecutionPolicy Bypass -File outputs\Mechanical_Design_App\run_checks.ps1`. 52 Python + 47 JS tests passed on 2026-10-19.
- **Backups:** `D:\Backups\Assembly Workshop` and private `C:\Users\brian\OneDrive\Backups\Assembly Workshop`. One timestamped folder per run, never overwritten. Never share-link the OneDrive copy (creator/Pi assets are personal-use). Rerun with `"C:\Program Files\Python310\python.exe" -B docs\housekeeping\make_backup.py`.
- **git** isn't on PATH. Use `C:\Users\brian\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe` (or Git Bash, if the session has it). Most assets are untracked; git isn't the backup. Commit locally only when Brian agrees; never push.

## Claude + Codex workflow

- The queue is `work/codex-tasks/`. `README.md` holds the standing rules and status table, plus one spec file per task. Claude writes specs and reviews. Codex executes and writes `<task>-REPORT.md`.
- Brian gives Codex one combined prompt for the batch. Then he tells Claude **"review codex tasks"**.
- Reviewing means reading the reports, then checking the real files: hashes vs the report, `git diff`, the files changed after the task started (other sessions may also be editing, so check HANDOFF before blaming Codex), and rerunning the checks. Then update the status table, commit, and write the next batch with one combined prompt.
- Keep design-heavy work (per-instance component editing, wizard detection heuristics, anything touching user data or the live server) for Claude.

## Current state of the queue (2026-10-19)

- Tasks 01–06 are done. Claude reviewed 01–03 and checked 04–06: Codex stayed within its file lists, and task 06 updated the checks command and counts in PROJECT/HANDOFF/ROADMAP/app README.
- **Waiting on Brian:** task 05 (library rebuild proposal) has three open questions at the end of its report: create-a-copy vs update placed items, automatic vs editable name suffix, and labeling of "source matches, build process unknown" items.
- **Possible next:** turn task 04's BOM plan into code and tests (Claude reviews the plan first), and act on Brian's answers to task 05.
