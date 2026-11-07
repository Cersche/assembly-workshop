# Task 54: Workshop Bench, a local app for organizing part projects

**Brian (2026-11-06):** build Workshop Bench from the approved mockup. A project is a **job** (such as "Cable span bracket" or "CM1000 lights"), linked to a device card when there is one. Version 1 shows everything, lets Brian set a project's status and notes, and saves fit reports. **It never runs releases, renders, git or anything else**: releasing stays a chat step with Claude. Brian wants this done thoroughly: be exhaustive in research, tests and checks.

Mockup (look and flow to follow): https://claude.ai/artifact/T1cst7qAqkqus6LSnB8ACC. If you can't open it, the layout is: header; left list of projects; main area with a Measure → Draft → Print → Report step strip, a 3D view, revisions newest first (ID, status, note), a device card table, a "Still unknown" list and a fit report form. Dark palette from the rack app: background #111720, panels #1a2330, lines #2a3544, text #dbe4f0, muted #a9b8cc, accent #67a8ff, fit #70ceb1, problem #ff9d9d, unknown/pending #e6be77. Status is always written in words too, never color alone.

## Read first
AGENTS.md, HANDOFF.md (all of it), PROJECT.md, `.claude/skills/new-part/SKILL.md`, `docs/Fit_Findings.md`, `work/workbench/Workflow_Log.md`, every file in `docs/devices/`, `outputs/Final_3MF/README.md`, and `git log --since=2026-10-20 --format="%ad %s" --date=short`.

## Files to create
- `tools/bench/bench.py`: the server. **Python 3.10 standard library only** (`http.server`, `json`, `pathlib`, `re`, `html`...). Binds `127.0.0.1` only, default port **8720**, `--root` (default: the repo root) and `--port` flags. UTF-8 everywhere.
- `tools/bench/static/index.html`, `bench.css`, `bench.js`: plain HTML/CSS/JS, no CDN, no build step, no frameworks, works offline.
- `tools/bench/start.bat`: starts it on 8720 and opens the browser.
- `tools/bench/README.md`: what it reads, what it writes, how to start it, limits.
- `work/bench/projects.json`: the only new data file (see Seed).
- `tools/bench/test_bench.py`: unittest suite (see Tests).
- Add a `.claude/launch.json` entry named `Workshop Bench` (python `tools/bench/bench.py --port 8720`, port 8720). Keep every existing entry byte for byte.
- One short paragraph in PROJECT.md under the release-script paragraphs, linking `tools/bench/README.md`.

## Data model: `work/bench/projects.json`
```json
{"version": 1, "projects": [
  {"id": "csb", "title": "Cable span bracket", "prefixes": ["CSB"], "status": "printing",
   "device_cards": ["docs/devices/lab-rax-4u-post.md"], "sources": ["work/cable-span-bracket/span_bracket.scad"],
   "workflow_log": "Cable management bracket (front to rear posts)", "notes": "", "updated": "2026-11-06"}
]}
```
Statuses, in order: `idea`, `measuring`, `draft`, `printing`, `report-due`, `done`, `parked`. The step strip maps idea/measuring → Measure, draft → Draft, printing → Print, report-due → Report, and done/parked are shown as labels.

## Everything else is discovered from the repo, read-only
- **Revisions:** every revision ID matching a project prefix (`^PREFIX(-[A-Z0-9]+)+` and forms like `CM6A`, `SCR5-H10`, `SG8-M6-F`; write the regex carefully and test it against every real ID listed in HANDOFF). Look in `outputs/*/` folder names, `outputs/Final_3MF/*.3mf`, `outputs/Chunky_Revisions/`, `work/mesh-viewer/*.html` and `release_report.md` files. Per revision show: has release folder (link to its README and release_report.md), has 3MF, has viewer page, the date (from the folder name or file time), and **printed fit results**: every row or bullet in `docs/Fit_Findings.md` that names the ID as a whole token (CM1P-T1 must not match CM1P-T10). Revision status: fit/problem/not printed/printing, worked out from the fit lines ("fits", "good fit", "perfect" → fit; "too tight", "too loose", "did not fit", "would not" → problem; no line → not printed). Show the matched line text so Brian can judge; mark the status as a guess.
- **Superseded / do-not-print:** if `outputs/Final_3MF/README.md` or HANDOFF marks a revision superseded, dropped or do not print, show that.
- **Device card:** render the markdown read-only (headings, paragraphs, lists, pipe tables, inline code, links). Escape everything first; never insert raw HTML from a file.
- **Still unknown:** list every device-card row whose status is UNKNOWN, plus lines in the project's newest README containing "UNKNOWN".
- **Workflow log:** show the project's section of `work/workbench/Workflow_Log.md` as a table.
- **3D view:** an iframe showing the chosen revision's viewer page from `work/mesh-viewer/`, served only from that folder. No viewer page → say so plainly.
- **Attention list** at the top of the project list: projects in `report-due`, projects in `printing` for more than 3 days, revisions released with no fit line, device cards with UNKNOWN rows that a draft depends on.
- **Search and filter:** a search box (project title, prefix, revision ID) and a status filter. Filter choice remembered in localStorage (try/catch).

## Writes (the only three)
1. **Status and notes:** `PATCH /api/projects/<id>` with `status` and/or `notes` updates `projects.json` and sets `updated`.
2. **New project:** `POST /api/projects` with title, prefixes, optional device cards and sources. Reject duplicate ids and prefixes.
3. **Fit report:** `POST /api/fit-report` with revision ID, result (Fits / Too tight / Too loose / Failed / Other), where (free text), walls, infill, extra notes. It **appends** one bullet to the end of `docs/Fit_Findings.md` in the existing style:
   `- 2026-11-06 CSB-A (Brian, via Workshop Bench): Fits. <where>. 2 walls, 10% infill. Strength UNKNOWN.`
   It also appends a row to the project's section in `Workflow_Log.md` if there is one (step `Report`). Then it sets the project to `draft`. The form needs the revision ID (prefilled from the selected revision; refuse an ID that belongs to no project) and shows the exact text before saving.

Every write: rejects bad input with a clear message; atomic (write a temp file in the same folder, then `os.replace`); keeps a copy of the previous file as `<name>.bak` beside it before replacing; never removes or rewrites existing text in the markdown files (append only, preserving the file's line endings and a final newline); refuses with 409 if the file changed since the page loaded it (send a hash or mtime with the page data).

## Hard limits
- Never write anything outside `work/bench/projects.json`(+ .bak), `docs/Fit_Findings.md`(+ .bak) and `work/workbench/Workflow_Log.md`(+ .bak).
- Serve files only from `tools/bench/static/`, `work/mesh-viewer/`, and the markdown/text files the API reads. Block path traversal (`..`, absolute paths, drive letters, encoded forms, symlinks out of the repo).
- No subprocess, no git, no OpenSCAD, no network, no installs, no third-party packages.
- Don't touch `outputs/`, `data/`, `lib/`, `outputs/Mechanical_Design_App/`, any SCAD, any tool except the new `tools/bench/`. Don't commit or push; Claude reviews and commits.
- Licensed meshes: the viewer pages are local and uncommitted. Bench never copies or exports them.
- Keep UNKNOWNs visible; never show a part as approved or strong. The page says "Printed fit applies to that specimen only. Strength UNKNOWN." near fit results.

## Seed `projects.json`
Research HANDOFF, git log, outputs/ and work/ and create one project per active job. At least these (confirm prefixes, sources, cards and the latest revision from the files):
| id | title | prefixes | starting status |
| --- | --- | --- | --- |
| csb | Cable span bracket | CSB | printing |
| mrt | MoCA rack tray | MRT | draft |
| fan | Rack top for a 200 mm fan | TFE, TRE, TSR, TFG | draft |
| opx | OptiPlex rear channels | OPX, SLV | draft |
| scr5 | Screen, Pi and Hue | SCR5 | draft |
| er6 | ER605 router bracket | ER6 | draft |
| cm1000 | CM1000 modem bracket and lights | CM1P, CM6 | draft |
| psb | Power strip bracket | PSB | draft |
| rx5 | MoCA receiver box | RX4, RX5 | draft |
| chs | Chess clock switch | CHS | idea |
| wmb | Flat wire bracket | WMB | idea |
| sg8 | TL-SG108E switch tray | SG8 | done |
| hdt | Drive tray | HDT | done |
| phx | Post hex anti-warp concept | PHX | parked |
Add any other job you find. Put what you inferred in `notes`, starting with "Seeded by Codex, check:".

## UI requirements
- Follow the mockup. Left list stacks above the main area below 760 px wide; no horizontal page scroll at 375 px.
- Real `<button>`, `<label>`, `<input>`; full keyboard use; visible focus; touch targets at least 44 px; text contrast at least 4.5:1.
- Light mode too, via `prefers-color-scheme`, with the same tokens on `:root`.
- Loads in under 1 second on the real repo; repo scan cached in memory, with a Refresh button that rescans.
- Error and empty states written in plain words ("No viewer page for CSB-B yet").

## Tests (`python -m unittest tools/bench/test_bench.py`)
Build a disposable fake repo in a temp folder per test; never touch the real repo's files in tests. At least:
1. Revision ID regex: every ID listed in HANDOFF.md and in outputs/Final_3MF/ is found exactly once for its project; CM1P-T1 vs CM1P-T10 and SCR5-H vs SCR5-H10 don't cross-match; non-IDs (`M6`, `U5`, `FP44`) are not revisions of any project.
2. Fit status guessing on each phrase family, with mixed lines ("fits, but rails a tad short").
3. Each write: success; exact appended text; line endings kept (CRLF and LF fixtures); `.bak` written; temp file cleaned; 409 on a stale hash; bad status, unknown project, unknown revision, empty title, duplicate prefix all rejected; nothing else in the temp repo changed (hash every file before and after).
4. Path traversal: `..`, `%2e%2e`, absolute, `C:\`, backslashes, symlink out of root, a static file outside the allowed folders: all 403/404.
5. Markdown rendering escapes `<script>`, `onerror=`, `javascript:` links.
6. Server binds 127.0.0.1 only.
7. API smoke test on a full copy of the real `docs/`, `work/bench`, `work/workbench`, `outputs/Final_3MF/README.md` and folder listing (copied into temp; outputs/ STLs not needed): every seeded project loads, every revision has a status, timing printed.
Aim for 60+ tests. All must pass.

## Acceptance checks (run them all, paste results in the report)
1. `python -m unittest tools/bench/test_bench.py -v`
2. `python tools/bench/bench.py --port 8720` against the real repo, then with Python's `urllib`: GET every API route; GET each project; time the first and second load.
3. Before and after step 2, `git status --porcelain` and SHA-256 of `docs/Fit_Findings.md` and `work/workbench/Workflow_Log.md`: **unchanged** (no writes on the real repo during acceptance).
4. Exercise each write against a temp copy only (`--root <temp>`), and show the diff of each file it changed.
5. `python -m unittest tools/test_release_part.py tools/test_workshop_lib.py` still pass (you changed nothing there).
6. If you can drive a browser, click through every screen at 1280 and 375 wide and save screenshots to `work/codex-tasks/54-screens/`; if not, say so.

## Report
`work/codex-tasks/54-workshop-bench-app-REPORT.md`: files created, each seeded project with what you inferred and how sure you are, the revision count per project, every ID the regex could not place, all acceptance output, timings, known gaps, and anything you were unsure about. List decisions you made that Brian or Claude should confirm.
