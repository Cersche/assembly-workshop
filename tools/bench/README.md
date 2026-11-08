# Workshop Bench

A local notebook for part **jobs**, with revision evidence, device cards, project status, notes and printed fit reports. Python 3.10 standard library; plain HTML/CSS/JavaScript, no CDN, packages, build step or internet requirement.

## Start

Double-click `tools/bench/start.bat`, or from the repository root:

```text
python -B tools/bench/bench.py --port 8720
```

Open http://127.0.0.1:8720/ . The server binds only 127.0.0.1; there is no option for a public interface. Close the server console or press Ctrl+C to stop. If the port is occupied, stop the old Bench process rather than running two writers. The batch launcher opens a browser and starts Python; **the application launches no program except File Explorer for Open folder** (below).

For disposable testing:

```text
python -B tools/bench/bench.py --root C:\path\to\temporary-copy --port 8720
python -m unittest tools/bench/test_bench.py -v
```

`--root` controls all project data and discovered files. Static assets always come from this installation's `static/`. Tests build a fresh temporary fake repository per test. Set `PYTHONDONTWRITEBYTECODE=1` when verifying that the real repository remains unchanged.

## Use

Pick a project; search titles, prefixes or revision IDs and filter by project status. The status filter is remembered when browser storage is available. Project status is an organizational choice, separate from guessed revision fit. Edit status/notes and explicitly Save. New project requires a unique ID and nonoverlapping uppercase revision prefixes; device cards and source paths are optional existing repository-relative files.

Select a revision for its local viewer. Below multi-part viewers, choose a part to solo and re-frame it, or All parts to restore the set. Changing viewer/revision resets to All parts. Open 3D in new tab follows the selected viewer and solo choice through an encoded `#solo=` fragment; the standalone page keeps the same sandbox policy.

Edit details opens the job title, prefixes, device cards, sources and workflow section. The ID is fixed. Save details sends only the fields you changed and validates them with the same rules as New project (so an unchanged path that has since moved does not block a title fix); workflow must name an existing level-two section (without the continuation suffix), or be blank. Cancel discards details edits. Unsaved forms warn before navigation and survive stale saves. Saving one form preserves unsaved text in other forms.

Quick next-step buttons save status immediately through the existing PATCH. Notes and details edits disable them with Save or cancel your edits first. Cancel notes and status edits restores the last loaded values. Write fit report selects the newest released revision without changing status; with no release it leaves the revision blank and explains why.

Print queue above the project list shows printing and report-due jobs oldest updated first, with newest release ID, elapsed days and overdue printing after three days. Search/status filtering is disabled while the complete queue is shown. The view choice is remembered when browser storage works.

Select a revision for its local viewer. Missing viewers are reported plainly. File locations for 3MFs are shown as text, not downloaded or copied. **Open folder** beside a 3MF opens File Explorer with that file selected (Windows only). Source markdown opens as plain text. Device cards render an escaped subset: headings, paragraphs, lists, pipe tables, inline code, bold and safe links.

Fit report: select a discovered exact revision ID, choose a result, describe the location and optionally record walls/infill and notes. Blank process fields remain UNKNOWN. Preview shows the exact bullet. Save appends it to Fit_Findings, appends a workflow continuation when a matching section exists, and moves the owning project to draft. Project/revision navigation warns before discarding unsaved edits.

## Reads and discovery

- `work/bench/projects.json` is the sole project catalog; this seed contains 21 jobs. Every inferred decision starts `Seeded by Codex, check:`.
- `HANDOFF.md`, `docs/Fit_Findings.md`, `work/workbench/Workflow_Log.md`, linked `docs/devices/*.md`, and output README/release reports are read as UTF-8.
- Output folder names and 3MF filenames are scanned, including Final_3MF and Chunky_Revisions. Mesh contents are never opened. The walk skips app trees, historical Phase/Session trees, frozen `src`, mesh `stl`, `checks`, `data`, revision and cache folders.
- `work/mesh-viewer/*.html` filenames are indexed; a chosen existing page is served in place. Pages are not copied or exported. Sandboxed frames allow their scripts but deny parent-page access and network connections.
- Explicit IDs in metadata are discovered even when only mentioned in a handoff. Such entries have no release unless associated with a real folder/3MF or an ID declaration in a release report. Component IDs remain distinct; shorthand ranges and historical file-name aliases may require human interpretation.
- Dates prefer dated folder names, otherwise file modification time. Undated mentions sort last. Imported file times do not establish design chronology. Newest README means newest discovered dated release; it is not a claim that the design is current.
- Fit lines use whole-token matching. Every matching line stays visible; only lines where the ID is the first revision named drive the guess, to avoid assigning an old revision's fit to its replacement. Conservative phrase matching is imperfect; read the evidence. Historical supersession/do-not-print mentions are shown verbatim as warnings, not automatic approval/release decisions.
- Attention includes overdue printing (updated more than three days ago), report-due projects, releases without direct fit lines, and draft jobs with linked UNKNOWNs. UNKNOWN dependency warnings are conservative: the app does not infer a CAD dependency graph.

The scan is cached in memory. Refresh explicitly rescans; GETs never save. External edits cause a 409 on the next save, even if the cached page is older. Refresh and review before retrying. A file with corrupt project JSON is an error, never silently reset.

## Exactly three runtime write targets

1. `work/bench/projects.json` — project creation or status/notes changes; updated date set on explicit save.
2. `docs/Fit_Findings.md` — append only.
3. `work/workbench/Workflow_Log.md` — append only, when the project has an existing section.

Each target gets its previous bytes in `<filename>.bak`. Writes stage temporary files **in the same directory**, flush/fsync and replace with `os.replace`; temporary files are cleaned after success/failure. A process-wide lock serializes writes and hash preconditions are checked before staging and again before commit. Symlink/reparse and hardlinked write targets/backups are refused. Only the three exact targets and their backups may be replaced.

Existing markdown bytes are never rewritten. LF/CRLF style is retained for additions, with a final newline. A report for a section in the middle of Workflow_Log adds an identically titled `(continued)` section at EOF; the UI merges its display. This resolves the spec's section-placement/append-only conflict without moving existing text.

**Atomicity limit:** each file replacement is atomic. Three separate filesystem paths cannot form a portable all-or-nothing transaction without a separate journal (not authorized here). All inputs and all hashes are checked before writing; files/backups are staged first; caught I/O failures trigger rollback. A power loss or an external editor racing the final hash check can still leave a partial multi-file update. Review the `.bak` copies before retrying; there is no background recovery writer or silent repair. Run one Bench instance per data root.

## HTTP API

GET `/api/health`, `/api/state`, `/api/projects`, `/api/projects/<id>`. State includes projects, discovered evidence, attention, `queue` (read-only `{id, title, status, latest, days, overdue}` entries; `latest` is null without a release), file hashes, a per-process write token and scan timing.

PATCH `/api/projects/<id>` accepts one or more of `status`, `notes`, `title`, `prefixes`, `device_cards`, `sources`, `workflow_log`, plus `hashes`. Unknown fields (including `id`) and empty changes are rejected. Own prefixes are allowed; other jobs and overlaps remain protected. Successful writes invalidate the cached scan; the next state request rescans immediately. Only projects.json and its backup change for details/status edits.

POST `/api/refresh` with `{}`; POST `/api/open-folder` with `{"path": <3MF path>}`; POST `/api/projects`; PATCH `/api/projects/<id>`; POST `/api/fit-report/preview`; POST `/api/fit-report`.

Mutations require `Content-Type: application/json`, `X-Bench-Token` from state and `hashes` from the loaded page (refresh/preview do not write and need no hashes). Maximum body 64 KiB. Only the exact loopback Host and, if present, same Origin are accepted; no CORS. Fit report checks all three hashes before changing anything. Errors return a clear JSON `error`; stale content returns 409.

Static GETs: `/`, `/static/bench.css`, `/static/bench.js`; viewer GET `/viewer/<filename>.html`; allowlisted text GET `/text?path=<repository-relative-path>`. Arbitrary files, meshes, SCAD, traversal, absolute/drive paths, alternate streams and symlink hops cannot be served. The one program launch is `explorer /select,"<file>"` for Open folder (Brian, 2026-11-08): only for a 3MF path Bench itself discovered and that still exists, only with the write token, and the app never waits on or reads from it. There are no other subprocess calls and no git, rendering, release, installation, purchase, publishing or network-client functions.

Printed fit applies to that specimen only. **Strength UNKNOWN.** No file presence, mesh closure, project status or guessed label establishes physical approval.

## Served viewer bridge

`static/viewer-bridge.js` is read from this installation, even with `--root`. The server inserts it inline once before the last closing body tag (or appends when absent) in the response only. No viewer file on disk is rewritten, and there is no separate bridge URL. The existing sandbox CSP is unchanged, including `connect-src 'none'` and no same-origin permission.

After load, the bridge reads the viewer's part labels and posts names to its parent. Bench accepts only the current iframe window and an exact two-field payload with at most 200 string names of at most 200 characters. Names are escaped for display. Solo messages target the opaque-origin frame with `*`; the bridge only accepts its parent, changes the existing checkboxes, fires change, then clicks the viewer's reset control to fit visible parts. Unknown names do nothing. Missing lists and malformed hash fragments are harmless. The hash also works in standalone tabs.

Task 55 verification logs are in `task55-feature*-tests.txt` and `task55-run-*.txt`; they are operator evidence, never read by the application. Runtime remains Python standard library and plain JS only.

The task-55 operator harness `task55-browser-acceptance.cjs` uses the already bundled Playwright and Chrome for disposable-root browser acceptance at 1280 and 375 pixels. It is never imported or served by Bench, installs nothing, and adds no application runtime dependency. Brian authorized in-memory `window.confirm` overrides for Cancel/Discard plus a dismissing native-dialog backup; the harness records those simulated paths separately. Deliberate stale-save tests produce expected HTTP 409 browser resource logs; unexpected console/script errors fail acceptance. Screenshots and the full results are linked in the task report.
