# Codex task 55 — Workshop Bench: five features Brian asked for

Brian picked these on 2026-11-08 (Claude session). Claude plans and reviews; Codex builds. Build them in this order, each one complete with tests before the next, so Claude can check and commit them one at a time.

Read first: AGENTS.md, `tools/bench/README.md`, `work/codex-tasks/54-workshop-bench-app.md` (original spec; all its limits still apply), `tools/bench/bench.py`, `tools/bench/static/*`, `tools/bench/test_bench.py`, and `tools/mesh_viewer_template.html` lines 226-252 (the viewer's part list).

## Limits that do not change

- Python 3.10 standard library only; plain HTML/CSS/JS, no CDN, no packages, no build step. Server binds 127.0.0.1 only.
- The app still writes only `work/bench/projects.json`, `docs/Fit_Findings.md` and `work/workbench/Workflow_Log.md`, atomically with `.bak`, markdown append-only, hash preconditions and 409 on stale files (the page rescans and keeps typed text). No new write targets.
- No subprocess, git, rendering, releasing or network client code. Viewer pages and 3MFs on disk are never modified, copied or exported.
- Keep every existing feature and test working. Keep the existing look (dark UI, current layout); add to it, don't redesign it.
- Every user-visible label in plain English.

## Feature 1 — Solo a part in 3D

Under the 3D viewer, a row of part buttons: `All parts` followed by one button per part in the viewer page. Clicking a part shows only that part in the 3D view and re-zooms to fit it. `All parts` shows the whole set again and re-zooms. The pressed button is highlighted (`aria-pressed`). Switching to another viewer page or revision resets to `All parts`. With 0 or 1 parts, hide the row.

How (the iframe is sandboxed, opaque origin, so the parent cannot touch its DOM):

- When serving `GET /viewer/<file>.html`, the server inserts a small **inline** bridge script into the **response only**, just before the last `</body>` (or at the end if there is none). The file on disk is not changed. Keep the bridge source in `tools/bench/static/viewer-bridge.js` and read it from the installation's `static/` (not from `--root`). It must work under the existing viewer CSP (`script-src 'unsafe-inline' 'unsafe-eval'`, `connect-src 'none'`); do not loosen that policy. Do not serve `viewer-bridge.js` as a separate route unless needed.
- The bridge, after the page has built its list, reads the part names from `#parts label.part .name` (213 of the 214 pages in `work/mesh-viewer/` have that list; the generator is `tools/mesh_viewer_template.html`) and sends `{bench: "parts", names: [...]}` to `parent` with `postMessage`, only when `parent !== window`.
- It listens for `{bench: "solo", name: <string or null>}` messages, accepted only when `event.source === parent`. For each part row it sets the checkbox to `name === null || rowName === name`, fires a `change` event on it (that is how the page updates its own `visible` flags), then clicks `#reset` so the page re-frames to the visible parts (`frame()` already fits visible parts only). Unknown names do nothing.
- On load it also applies `location.hash` of the form `#solo=<URI-encoded name>` (used by feature 2's new-tab link).
- A page without the part list must not break: the bridge sends `names: []` and the page keeps working as before.
- Parent side (`bench.js`): accept a message only when `event.source` is the current viewer iframe's `contentWindow` and the data has exactly that shape (array of strings, at most 200 names, each at most 200 chars). Escape names when building buttons. Send solo messages with `postMessage(msg, "*")` (the frame's origin is `null`; the content is not sensitive).

Tests: the served viewer contains the bridge exactly once and before `</body>`; the file's bytes on disk are unchanged; the viewer CSP header is unchanged; a page with no `</body>` still gets the script; path safety for `/viewer/` unchanged. Browser check on a temp root with a real multi-part page copied from `work/mesh-viewer/` (e.g. `TF-D.html`): buttons appear, a part solos and zooms, All parts restores.

## Feature 2 — Open 3D in a new tab

Beside the viewer chooser, an `Open 3D in new tab` link: `href="/viewer/<file>.html"` plus `#solo=<name>` when a part is soloed, `target="_blank" rel="noopener"`. It follows the chooser and the solo choice. The new tab is still served with the sandbox CSP. Hide it when there is no viewer page.

Tests: browser check that the link follows the chooser and the solo name, and that the new tab opens with only that part shown. Server test: `/viewer/<file>.html` served standalone (no Referer) still carries the sandbox CSP and the bridge.

## Feature 3 — Edit job details

An `Edit details` button on the project panel opens a form like New project, prefilled: title, revision prefixes, device cards, source files, workflow log section. The project ID is shown but cannot be changed. `Save details` and `Cancel`. Unsaved edits get the same leave-page / switch-project warning as notes.

Server: extend `PATCH /api/projects/<id>` to also accept `title`, `prefixes`, `device_cards`, `sources`, `workflow_log` (still accepts `status`, `notes`, `hashes`; still rejects unknown keys and an empty change).

- Move the create-time validation of title, prefixes, device cards and sources into shared helpers and use them for both create and edit (same messages, same limits).
- Prefix checks on edit: duplicates and overlap are checked against **other** projects only; the project's own current prefixes are allowed.
- `workflow_log`: empty, or the exact title of an existing `## ` section in `work/workbench/Workflow_Log.md` (a `(continued)` section counts as the same title). Otherwise 400 with a plain message.
- Set `updated` to today; one atomic write of `projects.json`; rescan so the new prefixes and files show at once.

Tests: each field edits; ID cannot change (an `id` key is rejected); own prefixes accepted; another project's prefix or an overlapping prefix rejected; missing file, wrong folder and non-markdown card rejected; bad workflow section rejected; stale hash gives 409 and changes nothing; create still behaves exactly as before.

## Feature 4 — Quick status buttons

On the project panel, one or two one-click buttons for the next step, depending on current status:

| Status now | Buttons |
|---|---|
| idea, measuring | `Start draft` → draft |
| draft | `I'm printing it` → printing |
| printing | `Printed, report due` → report-due |
| report-due | `Write fit report` (opens the fit report form for this job's newest release; no status change), `Mark done` → done |
| done, parked | `Reopen as draft` → draft |

Each status button saves immediately with the existing `PATCH` (status only) and shows the saved state. While the notes or details box has unsaved edits, the status buttons are disabled with the hint `Save or cancel your edits first`; they never save typed notes by accident. A 409 behaves like the other saves (rescan, keep typed text, say so). The existing dropdown + Save stays.

Tests: server side is the existing PATCH; add tests that status-only PATCH leaves notes and details untouched. Browser check of each button on a temp root.

## Feature 5 — Print queue view

A `Print queue` view the user can switch to from the project list (a toggle or tab above the list; remember the choice like the status filter, only when browser storage works). It lists jobs with status `printing` or `report-due`, oldest `updated` first: job title, status, newest release ID (or `no release found`), and `N days` since updated, with printing over 3 days marked overdue (same rule as the attention list). Clicking a row opens that project. Empty queue: `Nothing printing or waiting for a fit report.`

Server: add `queue` to `/api/state` (computed in the scan, read-only): list of `{id, title, status, latest, days, overdue}` in that order.

Tests: ordering, the two statuses only, days and overdue flags (use a fixed date in the test the way the existing printing-overdue test does), `latest` null when there is no release.

## Acceptance (all required, report the output)

1. `python -m unittest tools/bench/test_bench.py -v` passes **three runs in a row** (the HTTP tests used to be flaky on Windows). New tests for every feature above.
2. No writes to the real repo during acceptance: exercise everything on a temp copy with `--root <temp>` on a port in 8700-8899 other than 8720 (Brian's copy may be running on 8720; do not stop it). Show `git status --short` and the SHA-256 of `work/bench/projects.json`, `docs/Fit_Findings.md`, `work/workbench/Workflow_Log.md` and `work/mesh-viewer/TF-D.html` before and after: unchanged.
3. Browser click-through on the temp root at 1280 and 375 wide: each feature works, no console errors. Screenshots into `work/codex-tasks/55-screens/`.
4. Update `tools/bench/README.md` (Use, HTTP API, the served-only bridge script and why the disk file is untouched).

## Do not

- Touch anything outside `tools/bench/` except the report, the screenshots folder and (only if truly needed) nothing else. Do not edit `tools/mesh_viewer.py`, `tools/mesh_viewer_template.html`, any viewer page, `work/bench/projects.json`, outputs/, data/, lib/, the rack app or any SCAD.
- Commit or push. Claude reviews and commits each feature.

## Report

Write `work/codex-tasks/55-bench-five-features-REPORT.md`: files changed per feature, test output (all three runs), acceptance hashes before/after, screenshots list, anything you could not check, and decisions Brian or Claude should confirm.
