# Assembly Workshop — handoff (2026-10-18)

## Goal
Build a local mechanical-design app that selects real hardware, generates matching joints, and checks assemblies before printing. The Lab Rax Raspberry Pi 4 tray/faceplate is the first beta validation project; later expand the sourced screw/heat-set insert library across M1–M8. Original Claude-app recovery was waived; the beta specification is the baseline.

## Workspace and session rules
- Root: `C:/Users/brian/Documents/Codex/2026-10-17/referenced-chatgpt-conversation-this-is-an`.
- Read this file and AGENTS.md first, then only listed/relevant files; do not scan the whole repo. AGENTS.md was absent at root and checked ancestor directories.
- Local development is approved. Preserve existing `data/`. Ask before each fresh desktop-control session and before printing. No purchasing. No agents unless explicitly requested by user/applicable instructions.
- Work in bounded milestones; update this file after finished steps or decisions. User wants efficient context use and fresh-session handoffs.
- Git repository exists on `master`; before this handoff commit there were no commits. Only HANDOFF.md is to be committed; outputs/, work/ and result.json are untracked and excluded.

## Done so far
**Four phases complete; Phase 5 of 7 is next.**
- Runnable app: `outputs/Mechanical_Design_App/`:
  - `app.py`: standard-library HTTP service, SQLite catalog, immutable hardware revisions, pinned project selections, imports, dimensional rules, BOM/project exports, draft geometry and constrained SCAD/mesh endpoints.
  - `index.html`: offline UI, roadmap, selection/check/export/generation/comparison controls.
  - `viewer.js`: canvas orbit/zoom/top/joint focus, part visibility, nominal hardware envelopes, baseline/proposal switching.
  - `mesh_revision.py`: OpenSCAD rendering, ASCII STL edge-closure checks, hashed immutable build cache and matching ZIPs.
  - `starter-hardware.json`: three sourced Accu M3 screws (6/8/10 mm), three partial McMaster M3 inserts (3.4/4.3/5.7 mm).
  - `assembly.json`: clearance-v2 tray (10,340 triangles) and faceplate (1,220), original mm coordinates/hashes. `pi4_baseline.scad` preserves source.
  - Supporting files: `test_app.py`, `README.md`, `hardware-records.md`, `start.bat`.
- Latest app release: `outputs/Mechanical_Design_App_Beta_0_8.zip`; spec: `outputs/Mechanical_Design_App_Beta_Spec.md`.
- Mechanical baseline: `outputs/Lab_Rax_Pi4_Assembly_Beta_Clearance_v2/` (start with its README); package: `outputs/Lab_Rax_Pi4_Clearance_v2.zip`.
- Baseline gussets restored and crests lowered another 1 mm after detailed Pi mesh exposed ~0.05 mm USB-metal interference. Prior targeted solid/triangle checks support 0.5 mm vertical clearance at four gussets; nominal joint/PCB checks passed. Physical testing remains undone.
- Verification rerun: 13 Python tests PASS, both frontend JS syntax checks PASS, viewer mock PASS, integration/cache/ZIP consistency PASS. No known failing automated tests.
- Phase 4 live browser acceptance completed 2026-10-18: saved/check trial, generated meshes, visually switched baseline/proposal labels, exercised joint focus/full assembly visibility, downloaded/verified matching ZIP, tested input-change invalidation and cached regeneration.
- Actual browser download (outside this repo): `C:/Users/brian/Documents/Codex/2026-10-17/i-m-continuing-work-from-a-2/outputs/pi4-rendered-revision-ebd6af31.zip`. Verified ZIP integrity, exact generated source, pilot-only change, pinned hardware, retained unknowns, matching report/assembly build ID and both STL SHA-256 hashes. Logs: tray 21.759 s, faceplate 1.604 s.

## In progress — exact state
- **Phase 5 of 7: full Pi4 validation. Not started.** Stopped at the accepted Phase 4 milestone; no app code or release packages changed this session.
- Chrome local app: `http://127.0.0.1:8765/`, Guest window titled `Assembly Workshop · Hardware beta - Google Chrome`. Last window ID 2568462 is historical; rediscover handles.
- Saved selections: Accu `SSCF-M3-8-A2` r1 and McMaster `94459A140` (5.7 mm) r1. Inputs: pilot 4, stack 3.3, pocket 8, boss diameter 9, minimum engagement 3, bottom allowance 0.5 mm.
- Checks: six PASS, six UNKNOWN, zero FAIL. Unknowns: usable thread engagement, bottom clearance, installation hole recommendation, boss wall, source completeness, physical/spatial checks.
- Current generated proposal active, generation controls in view, download/proposal enabled. Build ID: `ebd6af3164685923c661c7965badd932d98ed6c1da9bfc51742fe934f6a68a78`.
- Pilot 4 -> 3.9 -> 4 disabled old proposal/download and returned canvas to baseline. Restoring 4 did not revive stale controls. Saved/check restored inputs; generation explicitly reused matching cached render and re-enabled controls.

## Next steps
1. Read spec, baseline README and current app README. Follow only exact Pi asset/validation-script paths referenced there; do not inventory the repo.
2. Establish the detailed Pi reference mesh/source, hashes, units and transform into baseline coordinates. Inspect existing targeted validation evidence and non-manifold limitations.
3. Define Phase 5 acceptance checks: actual Pi placement, component/gusset/PCB clearances, joint alignment and relevant access checks. Keep unresolved evidence marked unknown.
4. Integrate the actual Pi reference into the app viewer and implement defensible assembly checks; preserve baseline, saved data and immutable build identity. Request fresh permission before desktop testing.
5. Fix stale UI wording when making the next scoped app change; run appropriate tests and browser acceptance, then update release/package docs without overwriting user data.
6. Resolve insert OD, usable depth, installation recommendation, minimum wall and material before physical joint coupon/full prototype. Phase 6 is sourced M1–M8 expansion; Phase 7 is physical testing/sign-off. Never print without approval.

## Decisions made
- Roadmap: 1 foundation, 2 starter library, 3 selections/rules/exports, 4 geometry integration COMPLETE; 5 full Pi4 validation NEXT; 6 library expansion; 7 physical beta sign-off. Report Phase X of 7, not invented percentages.
- Python 3.10+ standard library + SQLite + offline loopback browser UI; no external JS dependencies. Local OpenSCAD generates meshes.
- Unknown stays unknown; no fabricated standard-part dimensions. Supplier maximum hole diameter is not a printed-hole recommendation. The 4 mm pilot is a trial, not approved physical fit.
- Pi4 adapter changes only `insert_pilot` (3–4.2 mm), supports M3x0.5 joint hardware and requires stack 3.3/pocket 8/boss 9. Failed checks block export; unknowns allow clearly labeled PROPOSED — UNVALIDATED output.
- Preserve baseline. Draft generation does not save selections; save/check are explicit. Packages match exact immutable build IDs; edits invalidate view/download state.
- Hardware envelopes are nominal without threads/knurls, not collision solids. Unknown insert OD is shown with dashed axes through parts.
- Joint axes: X=+/-40, Z=21, along Y; ear rear bearing Y=11.3, screw points -Y, insert entrance Y=11.3-stack (default 8). PCB underside Z=16, hole pitch 58x49. Pi mounting hardware is separate from assembly M3 screws.

## Known issues / fragile points
- No Pi reference in viewer yet; no complete collision, strength, driver-access, rack-fit or physical-fit validation. Full M1–M8 catalog/hardware CAD absent.
- Whole-Pi CGAL check failed on non-manifold reference edges. Empty output after conversion errors is INCONCLUSIVE, never a clearance pass. Use documented targeted/triangle evidence appropriately.
- UI wording debt: pilot notice always says 4.2 mm; subtitle/footer claim manufacturing editing pending/no geometry modification; build-status still says Showing PROPOSED after baseline switch although canvas label switches correctly; triangle-status calls generated view a reference/no edits. README/release roadmap still says Phase 4 pending; not revised in this handoff-only task.
- Painter-sorted triangles can show surface-order artifacts. Mesh closure alone does not establish assembly fit.
- Active browser install/data path has not been established. Earlier empty selections may reflect a different extracted install; do not assume data loss or overwrite data.
- OpenSCAD `.exe` works; `.com` launcher is broken. ASCII STL only. Builds cache under active app `data/revisions/`. Integration script may reuse `work/v08-build`; its latest rerun was cached, while browser download includes render logs.
- Windows automation: allow ~400 ms after actions before snapshots; offscreen clicks fail, native dropdown keyboard navigation works. Save As indexes failed and coordinate focus was inconsistent; Brian saved manually. Recovered 'no monitor found for window' by rediscovering/activating Chrome. Do not reuse indexes/handles or bypass browser policy blocks.
- Existing reminder `finish-pi4-tray-fit-test`: every two days at 6 PM Pacific until physical testing complete; do not duplicate.

## How to run / test
Run PowerShell from repo root. Python/Node/Git use explicit paths because node/git are not on PATH.

```powershell
# Run (or use outputs/Mechanical_Design_App/start.bat); preserve existing data/.
& 'C:/Program Files/Python310/python.exe' outputs/Mechanical_Design_App/app.py
# Open http://127.0.0.1:8765/ ; Ctrl+C stops server. Avoid starting a duplicate.

& 'C:/Program Files/Python310/python.exe' -m unittest discover -s outputs/Mechanical_Design_App -v
& 'C:/Program Files/Python310/python.exe' work/extract_frontend.py
& 'C:/Users/brian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe' --check work/app_frontend_check.js
& 'C:/Users/brian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe' --check outputs/Mechanical_Design_App/viewer.js
& 'C:/Users/brian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe' work/test_viewer_v08.cjs
& 'C:/Program Files/Python310/python.exe' work/validate_v08.py
# Above integration checks render/cache/closed meshes/matching ZIP, without desktop/printing.

# Release packaging ONLY when a release update is intended: rewrites README and ZIP.
& 'C:/Program Files/Python310/python.exe' work/pack_v08.py
```

OpenSCAD: `C:/Program Files/OpenSCAD/openscad.exe`.
Git: `C:/Users/brian/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe`.
Computer-use skill: `C:/Users/brian/.codex/plugins/cache/openai-bundled/computer-use/26.1013.40934/skills/computer-use/SKILL.md`; read it and required docs before UI work. Use `mcp__node_repl__js` + `@oai/sky`, observe/act once/refresh. No terminal UI automation. Ask fresh desktop permission after session transition.

Git identity decision: use repository-local author roci <roci@example.invalid> for this and future commits here until Brian requests a change; placeholder email avoids recording a personal address.
