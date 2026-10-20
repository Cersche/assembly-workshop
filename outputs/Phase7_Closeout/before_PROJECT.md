# Assembly Workshop — project home and operating guide

Updated 2026-10-18. Verified from files, conversation history, Git status, app CLI and project-management inventory. This is the current project entry point; HANDOFF.md remains the historical Phase 6 handoff.

## Purpose and technology

Local mechanical-design app for traceable hardware selection, constrained joint generation and bounded assembly checks before printing. First beta: Lab Rax Raspberry Pi 4 tray/faceplate. Backend: Python 3.10+ standard-library HTTP server and SQLite. Frontend: HTML/JavaScript and canvas viewer. OpenSCAD CLI renders supported proposals; no pip/npm installation is needed for runtime. Node runs development checks.

## Locations and preservation

Recommended primary project folder (existing Git root): `C:/Users/brian/Documents/Codex/2026-10-17/Assembly Workshop`. The original repository folder was successfully renamed to Assembly Workshop on 2026-10-18; all original file hashes matched immediately after the rename. The prior copy is retained separately as Assembly Workshop - preserved copy.

- Current app: `outputs/Mechanical_Design_App/`; entry `app.py`, launcher `start.bat`.
- Protected baseline: app `pi4_baseline.scad`, `assembly.json`, `pi_reference.json` and manifest; original deliverables `outputs/Lab_Rax_Pi4_Assembly_Beta_Clearance_v2/`.
- Catalog: app `starter-hardware.json`, `catalog-packs/` (seven optional packs and manifests); closeout `catalog-packs/phase6-closeout.md`.
- Tests: app `test_*.py`, `test_catalog_workflow.cjs`; root `work/extract_frontend.py` and `work/test_viewer_v08.cjs`.
- Historical app versions and research/evidence stay under outputs/ and work/. Do not replace them with the current app.
- Phase 6 full closeout: `C:/Users/brian/Documents/Codex/2026-10-18/continue-assembly-workshop-from-c-users-2/outputs/Phase6_Closeout/`.
- Phase 7 preparation originals: `C:/Users/brian/Documents/Codex/2026-10-18/yaml-continue-assembly-workshop-from-c/outputs/Phase7_Readiness/`. Matching copies are in `docs/phase7-readiness/` here, so new project chats can find them without switching roots.
- Organization records and local preservation copy: `C:/Users/brian/Documents/Codex/2026-10-18/yaml-continue-assembly-workshop-from-c/outputs/Project_Organization`. The pre-documentation copy includes the entire original workspace, including .git, outputs/, work/ and result.json, plus Phase 6 closeout and Phase 7 preparation. See preservation_manifest.json for per-file source/copy hashes. This is a local safety copy, not a release or an off-machine backup.

Git HEAD was `9b44e5c`; before organization only HANDOFF.md was tracked and outputs/, work/, result.json were untracked. No commit, push or deletion was performed. The original repository folder was subsequently renamed to Assembly Workshop at Brian's request. The earlier copy remains as Assembly Workshop - preserved copy. Newly created guidance is also not automatically committed. Keep both working files and preservation copy.

## Project and conversation state

A local project named Assembly Workshop exists (ID 23bbc12a-5bb0-42a8-8c3f-a060bf2d0ea0). Its primary path was verified through list_projects as C:/Users/brian/Documents/Codex/2026-10-17/Assembly Workshop on 2026-10-18. Current chat 01a14e5b-bc7c-78b2-94b5-0ccbf997c2e7 belongs to the project. This existing chat retains its separate Documents/ChatGPT/Assembly Workshop cwd; run app commands with the canonical project root explicitly.

Conversation history remains in the existing app chats; this documentation is not a full transcript export. Relevant earlier chats: Inspect Lab Rax assembly (`01a14d3a-8a2c-7783-a892-260be252db8c`), Validate Phase 5 readiness (`01a14e09-c589-75f3-900a-6c6e2244f73f`, Phase 6 closeout workspace), and the current chat. Preserve them; none was deleted, archived, forked or replaced. Other historical chats remain in the sidebar. Membership can be organized after the project exists.

## Run and check

From the primary folder in PowerShell:

```powershell
$py='C:/Program Files/Python310/python.exe'
$node='C:/Users/brian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
& $py outputs/Mechanical_Design_App/app.py --port 8767 --data work/NEW-disposable-sandbox
# Choose a NEW directory each time. Ctrl+C stops it.
```

App URL is http://127.0.0.1:8767. Opening/controlling the browser requires separate desktop approval. The default launcher runs port 8765 with app-relative `data/library.sqlite3`; starting it can create data/load starter records. No default data/ directory was present beside the current app during inspection. Active data elsewhere and ports 8765/8766 were not identified as belonging to this app; do not infer their location or overwrite them. Before a normal restart, confirm which existing data directory Brian intends to use. SQLite stores pinned project selections; generated immutable meshes live beneath the chosen data directory's revisions/.

```powershell
& $py -m unittest discover -s outputs/Mechanical_Design_App -v
& $node outputs/Mechanical_Design_App/test_catalog_workflow.cjs
& $node --check outputs/Mechanical_Design_App/catalog.js
& $node --check outputs/Mechanical_Design_App/viewer.js
& $py work/extract_frontend.py
& $node --check work/app_frontend_check.js
& $node work/test_viewer_v08.cjs
```

OpenSCAD path: `C:/Program Files/OpenSCAD/openscad.exe`, overridable with OPENSCAD_EXE. Python and OpenSCAD executable files were confirmed present. Node path is machine-specific. Do not generate builds merely to check startup.

## Features and limits

Implemented: immutable hardware revisions and project pins; atomic JSON imports; source/field evidence; filters and replacement comparisons; explicit verified optional packs; constrained M3 joint rules; BOM/project/source exports; baseline/reference/proposal viewer; matching immutable OpenSCAD builds and evidence. Seven packs plus starter give 34 identities / 38 revisions; 14/14 screw and 12/14 insert families are represented, not exhaustive. M4.5/M7 insert evidence remains awaiting_source.

Phase 6 is closed WITH LIMITATIONS. Phase 7 planning/checks/register are prepared; physical work has not started. Whole-Pi non-manifold conversion, containment/global clearance, actual installation/tool/Pi/cable/rack access and physical fit/strength remain UNKNOWN. Exact selected insert usable depth, wall/process evidence and actual hardware/material remain unresolved. PEM source policy is a project decision with retained disagreement, not a manufacturer erratum. Supplier drawings/CAD are link-only; redistribution rights and upstream Pi provenance remain unresolved. Axial segments are metadata, not arbitrary geometry support.

Documentation discrepancy: app README/hardware-records retain historical Phase 5/6 counts and in-progress passages alongside their newer closeout note. Use this guide plus the explicit closeout for status. They were preserved unchanged during organization.

## Path/dependency assessment and next steps

App assets use Path(__file__).parent and start.bat changes to its own directory. Relative --data paths and work verification scripts depend on the invoking working directory. Renderer/Python/Node paths and historical handoff evidence references include absolute machine paths. Moving only the app or making its subfolder the project root would disconnect root-level evidence/instructions and root-relative checks. Keeping the Git root primary avoids those changes. The original complete Git root has now been renamed successfully; relative layout is unchanged. Historical evidence and the preservation manifest retain original paths as provenance.

Next: continue Phase 7 from outputs/Phase7_Start/Status.md; confirm intended live data location without repinning; continue Phase 7 evidence gathering from docs/phase7-readiness. Agree actual hardware/material/process, tools/envelopes, measurements and acceptance criteria before later authorized specimens. Physical fitting remains late Phase 7. Follow AGENTS.md for all boundaries.

## Scope clarification — Brian, 2026-10-18

STL output is sufficient for the end user's printing workflow. Printer/slicer/material-profile integration is outside the current app scope. Lack of a selected printer/material does not block Phase 7 software work. Earlier printer/process planning gates apply only if a separately authorized, bounded physical validation is later undertaken; they are not requirements to configure the end user's machine.

Continue Phase 7 with: (1) traceable hardware and honest dimensional UNKNOWNs, (2) supported geometry and source-to-STL identity, (3) existing mesh integrity and export safeguards, (4) artifact/revision traceability and reproducible digital acceptance, and (5) clear remaining physical-validation limits. Hardware actually owned and installation tools matter only when making claims about a specific installation or planning later physical work; they do not block auditing the recorded software configuration. Existing agreed geometry remains unchanged. Do not revisit the tabled mounting matter. No printing, physical tests or release packaging are authorized.

## Phase 7 points 2–6 — 2026-10-18

Completed digital acceptance WITH LIMITATIONS; see outputs/Phase7_Digital_Acceptance/Report.md.46 Python tests PASS, one preexisting mounting-specific test deferred; Node behavioral/syntax and9 localhost endpoints PASS. Fresh supported M3 trial render, source/STL/viewer integrity, cache reuse, corrupted-export rejection and pin preservation verified in new disposable data. Protected baseline/reference/mounting files and35 old-cache files unchanged. No desktop/physical work or release packaging occurred.

New renders use pi4-mesh-v2-triangulation1, strict mesh checks and artifact integrity manifests. Exact collinear export-face repair preserves existing coordinates/surface; raw/output hashes and processing trace are recorded. Old immutable caches are retained; legacy downloads lacking the new manifest require explicit regeneration into a separate new entry. Physical fit/strength and unsupported hardware dimensions remain UNKNOWN. Printer/slicer integration is outside scope. Mounting remains tabled. Report to Brian before point7; physical work requires separate direction and printing approval.

## User-provided physical observation — 2026-10-18

Brian reports “Fitment is fantastic” and supplies three photographs of the printed parts, including assembled positioning. Evidence: outputs/Phase7_Physical_Observations/2026-10-18/Observation.md and Observation.json. This is a positive qualitative fit report for the shown specimen; the exact STL revision is not identified. Strength/retention, hardware installation, Pi-board and rack/service fit remain unestablished by these photos. Earlier no-physical-work statements describe the state before this user report. No further printing/testing is authorized; mounting remains tabled. Remaining niche insert research is parked at Brian's direction; retain documented UNKNOWNs.

### Recovered earlier test-fit delivery
The requested pre-Phase6 test-fit files were located in chat Validate Phase 5 readiness (01a14dde-e57e-7063-b72b-f9e4a0dbce49). Initial pair: the prior workspace outputs/Pi4_Test_Fit_Parts; later explicit replacement pair: outputs/Pi4_Four_Corner_Test_Fit, build bbbe12450805205dfcb2be26f02d707bd53c3030e21970631539be2d3cd27937. File hashes verified against saved manifests/assembly. This supplies historical provenance for Brian's reported specimen, without attributing it to the later Phase7 digital build. See outputs/Phase7_Physical_Observations/2026-10-18/Recovered_Test_File_Provenance.json. No new tests or mounting reassessment.
