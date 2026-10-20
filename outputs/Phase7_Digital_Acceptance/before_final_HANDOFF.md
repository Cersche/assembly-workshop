# Assembly Workshop — CURRENT handoff (2026-10-18)

This concise summary replaces the historical handoff. Read it before inspecting relevant files.

## Goal — current
Build a local mechanical-design app that selects traceable hardware, generates matching joints, and checks assemblies before printing. The Lab Rax Raspberry Pi4 tray/faceplate is the first beta project; the M1–M8 catalog supports later designs without inventing dimensions or physical validation.

## Done — current
- Phases1–6 COMPLETE; Phases5/6 closed WITH LIMITATIONS. Phase7 nonphysical preparation STARTED; see outputs/Phase7_Start/Status.md and docs/phase7-readiness/Readiness_Plan.md. Physical work NOT STARTED.
- App: outputs/Mechanical_Design_App/. app.py: stdlib HTTP/SQLite, atomic imports, immutable records/pins, joint rules/exports. index.html/catalog.js: filters, source inspection, explicit pack import and replacement differences. viewer.js/mesh_revision.py: baseline/reference/proposal viewing and immutable matching OpenSCAD builds.
- Phase5: pi_validation.py, pi_reference_manifest.json, pi_reference.json, joint_validation.json. Original baseline9PASS/0FAIL/4UNKNOWN; selected4mm trial7PASS/0FAIL/6UNKNOWN. Digital screening is not physical/whole-solid approval. Preserve pi4_baseline.scad/assembly.json and outputs/Lab_Rax_Pi4_Assembly_Beta_Clearance_v2/.
- Phase6: catalog-packs/phase6-batch1.json through phase6-batch7.json plus manifests; catalog_packs.py checks hashes; catalog_evidence.py audits fields offline and validates axial-segment METADATA. Seven packs+starter yield34identities/38revisions,16screws/18inserts,14/14 screw and12/14 insert families. M4.5/M7 inserts remain awaiting_source, not unavailable.
- PEM batch7 r2 resolves PROJECT source policy: visually inspected SI-9 drawing A=length,E=after-knurlOD,C=pilotmax. Catalog+0.05/-0 intervals equal overlap with product-page+/-0.05:1.75–1.80mm(M1/M1.2),2.15–2.20mm(M1.4/M1.6). Source disagreement/hash retained in installation_evidence_resolution; no manufacturer erratum claimed. r1/pins preserved; usable-depth/generic min_wall/process/physical approval remain UNKNOWN.
- Latest report: app catalog-packs/phase6-closeout.md. Full evidence: C:/Users/brian/Documents/Codex/2026-10-18/continue-assembly-workshop-from-c-users-2/outputs/Phase6_Closeout/ (Closeout_Report.md,PEM_Resolution.json,evidence.json,audit,snapshot,batch7/manifest). Older reports/ZIPs are historical, not Phase6 releases.
- Last verification39PythonPASS; catalog/frontend import-handler checks/JS syntaxPASS;7manifest hashes/3protected baseline-reference hashesPASS. Approved six-pack browser review passed imports27->32->34/source inspection/replacement evidence/pin preservation. Batch7 and static phase text have automated acceptance, no fresh batch7 visual claim.

## In progress — current exact state
No unfinished implementation or running acceptance server. Phase6 closed at Brian's explicit instruction; Phase7 nonphysical configuration/evidence preparation has begun. Active8765/8766 app/data were not updated or inspected during closeout; do not assert current running state. New packs are NOT auto-imported into active data. Disposable accepted trial pins were AccuSSCF-M3-8-A2r1/McMaster94459A140r1, pilot4/stack3.3/pocket8/boss9/minengagement3/bottomallowance0.5mm; not a live-user-state claim.

## Next steps — current
1. Read latest closeout/app README, then only relevant hardware-records.md/catalog evidence/tests. Root AGENTS.md now exists and contains persistent development guidance. No repo scan.
2. Start Phase7 readiness plan: actual material/process/hardware, tool/access envelopes, measurements and fit/retention/torque criteria; do not invent loads/temperatures/print compensation.
3. Resolve selected Pi4 M3 usable-depth/wall/process/access evidence before physical approval. Small PEM parts are not automatic M3 replacements.
4. Prepare reviewable coupon/prototype procedure/artifacts as needed. **Physical test fitting is LATE Phase7 per Brian. Do not test fit or print now.**
5. Conduct late-Phase7 testing when Brian directs, record observations/failures, then evaluate sign-off. Printing needs separate approval; release packaging not authorized.

## Decisions — current
- Preserve user data/, immutable revisions/cache, project pins and mechanical baseline. Explicit import does not repin; draft does not save. Failed checks block proposed export; UNKNOWNs remain explicit.
- Pi4 adapter remains M3x0.5, pilot3–4.2mm, fixed stack3.3/pocket8/boss9. Catalog breadth does not expand geometry support. Axial-segment descriptions are metadata only; non-straight generation/comparison unsupported.
- Conditional manufacturer wall guidance is not generic FDM minwall. OD is nominal after-knurl, not maximum. PEM policy is an explicit project decision, not a corrected supplier publication. Research PDF/render in current-chat work/pem-resolution/, not bundled.
- Supplier CAD/drawings link-only; offline metadata works, integrated offline asset store/viewer unsupported. Do not redistribute supplier/Pi reference assets with unresolved rights.
- **Four-corner mounting matter TABLED until Brian raises it.** Existing faceplate_mounting.py/.json describe proposal default; do not revisit/implement/test it. Historical baseline unchanged.
- Fresh desktop sessions require separate Brian approval; read computer-use skill/required docs first. No purchasing, printing, uploads, release packaging or subagents unless authorized.

## Known issues — current
No known failing tests. Whole-Pi non-manifold CGAL/containment/global clearance, actual tool/install/insertion/cable/rack access, physical fit/strength and upstream Pi provenance remain UNKNOWN. Remaining insert gaps, representative variant breadth, offline CAD/drawing viewer and arbitrary installation geometry are documented beta limits. Old scripts may overwrite evidence or misread CGAL failures; do not rerun blindly. Sky snapshots can lag; rediscover handles. Final dirty-reload warning cancelled, not completed reload. OpenSCAD.exe works; .com launcher broken. Use UTF-8 explicitly; corrected test encoding issue/full rerun PASS.

## Run/test/build — current
PowerShell from repo root. Do not run server against active data for acceptance. These commands are verification guidance, not permission to print/package:

```powershell
$py='C:/Program Files/Python310/python.exe'
$node='C:/Users/brian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
& $py outputs/Mechanical_Design_App/app.py --port 8767 --data work/phase7-sandbox
# NEW disposable folder only; approved browser http://127.0.0.1:8767; Ctrl+C stops.
# Checks in another shell:
& $py -m unittest discover -s outputs/Mechanical_Design_App -v
& $node outputs/Mechanical_Design_App/test_catalog_workflow.cjs
& $node --check outputs/Mechanical_Design_App/catalog.js
& $node --check outputs/Mechanical_Design_App/viewer.js
& $py work/extract_frontend.py
& $node --check work/app_frontend_check.js
& $node work/test_viewer_v08.cjs
& $py -c "import sys; sys.path.insert(0,'outputs/Mechanical_Design_App'); import catalog_packs; p=catalog_packs.inventory()['packs']; assert len(p)==7 and all(x['available'] for x in p); print('7 packs verified')"
```
Build only when justified: renderer C:/Program Files/OpenSCAD/openscad.exe; app Generate & show proposal renders matching meshes into chosen data directory's immutable revisions cache. Desktop approval required. No automatic builds/printing/packages to resume. CLI flags: python app.py --help.

Git identity roci <roci@example.invalid>. Handoff commit contains ONLY HANDOFF.md; outputs/,work/,result.json are untracked local assets, not committed app backups. Do not git clean or assume a clone contains them. Git executable: C:/Users/brian/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe.

---
