# Parallel sessions — conflict-safe prompts

Two prompts. Paste **Prompt A** into a coordinating session first, listing the work you want done. Every new session it starts (or that you start yourself) gets **Prompt B** with the blanks filled in.

---

## Prompt A — Coordinator (paste once, in the main session)

```
I want to run several sessions in parallel on Assembly Workshop. Before starting any of them, plan them so they cannot conflict. Read AGENTS.md, PROJECT.md and HANDOFF.md first.

The work I want done:
1. <task>
2. <task>
3. <task>

Do this, in order, and show me the result before starting anything:

1. FILE MAP — For each task, list the files and folders it will likely create or edit (code, GUI, API routes, SCAD, docs). Flag every file that appears in more than one task.
2. TRACKED vs UNTRACKED — Run `git ls-files` against those paths. Most of this project (outputs/, work/, data/, revisions, caches) is untracked, so a git worktree will NOT contain it. For each task, say whether a worktree would have what it needs. If not, the task runs in this folder and must be serialized against any other writer of the same files.
3. GROUPING — Put tasks in three buckets:
   - PARALLEL: no shared files, safe to run at the same time
   - SEQUENTIAL: shares files with another task; give the order
   - READ-ONLY: research/review only; always safe in parallel
4. SHARED HOTSPOTS — Name one owner for each of: HANDOFF.md, AGENTS.md, PROJECT.md, the main app/server file, the main GUI file. No other session may edit these; they write their notes to work/<task-slug>/Report.md instead, and I (or the owner) merge them later.
5. RUNTIME ISOLATION — Assign each session that runs the app:
   - its own disposable data folder: work/<task-slug>/test-data/ (never data/normal-use/)
   - its own port (e.g. 8101, 8102, 8103 …)
   No session runs exports, builds, prints, pushes or uploads unless I authorize it.
6. BACKUP CHECK — Remind me to take a fresh backup to D:\Backups before parallel writes begin, and wait for my OK.
7. BRIEFS — For each session, fill in Prompt B from docs/parallel-sessions/Parallel_Session_Prompt.md.

Only after I approve the plan, start the PARALLEL sessions. Start SEQUENTIAL ones only when the session before them has finished and I've reviewed it. When all are done, check each session's actual changes (not just its report), list any overlapping edits, and ask me before merging anything or updating HANDOFF.md.
```

---

## Prompt B — Per-session brief (one per parallel session)

```
You are one of several sessions running in parallel on Assembly Workshop. Read AGENTS.md, PROJECT.md and HANDOFF.md first, and follow them.

TASK: <one-sentence goal>
DONE MEANS: <what finished looks like, and how to check it>

YOUR FILES — you may create or edit only these:
- <path>
- <path>
- work/<task-slug>/  (your notes, report, scratch, test data)

DO NOT EDIT — other sessions own these right now:
- HANDOFF.md, AGENTS.md, PROJECT.md
- <files owned by other sessions>
- data/normal-use/ and outputs/Mechanical_Design_App/data/ (never touch them)

If you find you need to change a file not on YOUR FILES, stop and ask me. Do not work around it, and do not copy the file to edit a duplicate.

RUNTIME:
- If you run the app, use port <port> and data folder work/<task-slug>/test-data/ (create fresh disposable data there).
- Do not start start.bat against normal-use data. Do not run exports, builds, prints, pushes, uploads or old geometry scripts.

REPORTING:
- Write your status and handoff notes to work/<task-slug>/Report.md, not HANDOFF.md.
- Do not commit unless I ask. If I do, commit only YOUR FILES.
- At the end, list every file you changed, what you verified, and what remains UNKNOWN or unverified.
```

---

## Quick checklist (before starting anything in parallel)

- [ ] Each task's file list written down; no file appears under two writers
- [ ] Shared docs (HANDOFF/AGENTS/PROJECT) have one owner
- [ ] Each app-running session has its own port and its own disposable data folder
- [ ] Nothing points at `data/normal-use/`
- [ ] Worktree sessions are confirmed to have the untracked files they need, or they run in this folder, serialized
- [ ] Fresh backup in `D:\Backups`
- [ ] After finishing: review the actual diffs, then merge notes into HANDOFF.md once
