from pathlib import Path
import json,hashlib
root=Path.cwd();out=root/'outputs/Phase7_Closeout';digital=root/'outputs/Phase7_Digital_Acceptance';physical=root/'outputs/Phase7_Physical_Observations/2026-10-18'
for name in ['HANDOFF.md','AGENTS.md','PROJECT.md']:
    target=out/('before_'+name)
    assert not target.exists(),'Do not overwrite existing closeout preparation'
    target.write_bytes((root/name).read_bytes())
manifest=json.loads((digital/'Acceptance_File_Hashes.json').read_text(encoding='utf-8'))
verified=[]
for relative,expected in manifest.items():
    p=root/relative;actual=hashlib.sha256(p.read_bytes()).hexdigest();assert actual==expected,relative
    verified.append(relative)
observation=json.loads((physical/'Observation.json').read_text(encoding='utf-8'))
for photo in observation['photos']:
    assert hashlib.sha256((root/photo['file']).read_bytes()).hexdigest()==photo['sha256']
provenance=json.loads((physical/'Recovered_Test_File_Provenance.json').read_text(encoding='utf-8'))
for artifact in provenance['original_delivery']+provenance['later_explicit_replacement']:
    assert hashlib.sha256(Path(artifact['path']).read_bytes()).hexdigest()==artifact['sha256']
integration=json.loads((digital/'Digital_Integration.json').read_text(encoding='utf-8'))
for name,expected in integration['protected_hashes'].items():
    assert hashlib.sha256((root/'outputs/Mechanical_Design_App'/name).read_bytes()).hexdigest()==expected
confirmation={'date':'2026-10-18','specimen_id':observation['specimen_id'],'user_confirmation':"we've now got physical confirmation that your hard work translates well into the real world",'reported_fit':'CONFIRMED_BY_BRIAN_FOR_EARLIER_TEST_FIT_SPECIMEN','basis':['Original statement: Fitment is fantastic','Three supplied photographs','Earlier supplied test-fit files and subsequent replacement recovered and hash-verified','Brian acknowledged recovered provenance and physical confirmation'],'linkage':'User-confirmed context and recovered delivery history; not a forensic hash of a printed object','physical_result_scope':'Qualitative fit of the earlier supplied printed tray/faceplate specimen','excluded_claims':['Generalized fit across printers/materials','Later Phase7 integrity build physically tested','Pi electronics/board fit unless separately reported','Screw/insert installation, torque, retention or strength','Rack/cable/tool access approval','Reopening the tabled mounting matter'],'new_physical_work_authorized':False}
(physical/'User_Confirmation.json').write_text(json.dumps(confirmation,indent=2),encoding='utf-8')
validation={'date':'2026-10-18','prior_digital_acceptance_files_hash_verified':len(verified),'photos_hash_verified':3,'earlier_test_stls_hash_verified':4,'protected_assets_hash_verified':5,'new_tests_or_renders':False,'code_changes':False,'status':'Evidence consistent; ready for Phase7 closeout review WITH LIMITATIONS'}
(out/'Evidence_Check.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
(out/'Closeout_Review.md').write_text('''# Phase 7 closeout review — ready with limitations

2026-10-18. Status: READY FOR CLOSEOUT REVIEW WITH LIMITATIONS. This preparation does not mark Phase 7 closed or authorize a release. Brian has reviewed the digital result and now confirms positive real-world fit for the earlier supplied specimen.

## Results by agreed point

1. Scope/baseline: STL delivery; no end-user printer/slicer integration. Original mechanical/reference baseline remains intact.
2. Hardware/rules: audited with unresolved dimensions explicit. Remaining niche McMaster research parked at Brian's direction. Later drawing is retained as reference evidence; no catalog/pin changes were inferred from it.
3. STL generation: digital integrity checks and real isolated rendering passed; exact collinear export triangulation repair preserves original coordinates/surface. No mechanical source change.
4. Revision/export behavior: source/configuration/artifact integrity, cache reuse, input invalidation, corrupt-export blocking and pin preservation passed. Legacy cache entries remain preserved; new integrity-checked downloads require explicit regeneration.
5. Workflow: source and automated-handler review passed within stated scope. No fresh visual browser acceptance is claimed.
6. Digital acceptance:46 Python tests passed, one mounting-specific test intentionally deferred; catalog/frontend/viewer behavioral and syntax checks plus9 localhost endpoints passed. See ../Phase7_Digital_Acceptance/Report.md. This closeout preparation rechecked evidence hashes rather than repeating tests or rendering unchanged code.
7. Physical observation: Brian reports “Fitment is fantastic,” supplies three photos, and explicitly acknowledges physical confirmation following recovery of the earlier test-fit delivery. Record POSITIVE QUALITATIVE FIT FOR THE SHOWN EARLIER TRAY/FACEPLATE SPECIMEN. The supplied replacement build is bbbe12450805205dfcb2be26f02d707bd53c3030e21970631539be2d3cd27937. Delivery context and hashes establish file provenance; they do not measure the printed object's file hash. Do not assign this physical result to the later Phase7 digital build7c639ef2… .
8. Disposition: acceptance evidence consolidated and ready for Brian's closeout review. No further source hunting or printer setup is required to finish the agreed software scope. Release packaging/publication remains a separate decision.

## Retained limitations

Physical strength, torque/retention, screw/insert installation, exact usable thread depth and applicable wall guidance remain UNKNOWN. Reference OD/length are not certified tolerance bounds. Pi-board seating, rack/cable/tool/service access and mounting-layout acceptance are not established by these photos. Complete-Pi solid conversion/containment/global clearance and reference-asset rights remain limited or unresolved. The mounting matter remains tabled. No blanket fit or production certification follows from one positive specimen report.

## Preserved evidence

- ../Phase7_Digital_Acceptance/Report.md, Test_Summary.json, Digital_Integration.json and associated logs/hashes.
- ../Phase7_Physical_Observations/2026-10-18/Observation.md, User_Confirmation.json, Recovered_Test_File_Provenance.json and three original photos.
- ../Phase7_Hardware_Evidence/94459A140_Drawing_Review.json; no further niche-part investigation scheduled.
- Evidence_Check.json records fresh consistency checks. Existing app source, immutable records/cache, project pins, original STLs and supplier/Pi evidence remain preserved.

## Proposed work after closeout

1. Establish the intended normal-use app/data directory without replacing or repinning an existing database. Prior acceptance data is disposable, not the user's library.
2. If Brian wants a normal-use visual walkthrough, obtain fresh desktop-session approval first. Review selecting hardware, generating/viewing a clearly labeled revision and obtaining its matching STLs, keeping UNKNOWNs visible.
3. Maintain a short issue list from actual use. Prioritize repeatable workflow defects and useful STL-delivery improvements. Do not expand geometry scope, revisit mounting, add printer integration or resume niche insert research without a new reason/request.
4. Consider release preparation only under separate authorization, with unresolved third-party asset rights respected. No packaging/publishing/deployment/push is part of this review.
''',encoding='utf-8')
# Replace the accumulated current handoff, preserving its full previous content above.
(root/'HANDOFF.md').write_text('''# Assembly Workshop — current handoff (2026-10-18)

Read AGENTS.md and PROJECT.md, then only referenced relevant files. Canonical project home: C:/Users/brian/Documents/Codex/2026-10-17/Assembly Workshop. The earlier generated folder was successfully renamed; previous copy and all assets retained.

## Goal and status

Local Python-standard-library/SQLite + HTML/JavaScript mechanical design app. Traceable hardware, constrained Pi4 M3 joint proposals, viewer and matching STLs. Printer/slicer integration is OUT OF SCOPE. Phases1–6 closed with limitations. Phase7 digital points2–6 accepted WITH LIMITATIONS; Brian now confirms positive qualitative physical fit for the earlier supplied printed tray/faceplate. Point8 closeout review prepared, not yet marked closed. See outputs/Phase7_Closeout/Closeout_Review.md.

## Current evidence

- App: outputs/Mechanical_Design_App/. Digital acceptance: outputs/Phase7_Digital_Acceptance/Report.md (46PythonPASS; one mounting-specific test deferred; JS behavior/syntax and9localhost endpointsPASS). New pi4-mesh-v2-triangulation1 cache uses strict mesh checks, bounded exact-collinear export retriangulation and per-artifact integrity manifests. Old caches stay untouched; legacy downloads lacking manifests require explicit new generation.
- Physical: outputs/Phase7_Physical_Observations/2026-10-18/. Brian: “Fitment is fantastic”;3photos, recovered prior chat/file provenance, User_Confirmation.json. Earlier replacement build bbbe12450805205dfcb2be26f02d707bd53c3030e21970631539be2d3cd27937. Do not claim the later digital build was physically tested. No precise photo/ruler measurements inferred.
- Hardware:7packs+starter,34identities/38revisions.14/14screw and12/14insert families; M4.5/M7 inserts awaiting_source. Phase6 closeout: app catalog-packs/phase6-closeout.md. Full prior evidence remains at C:/Users/brian/Documents/Codex/2026-10-18/continue-assembly-workshop-from-c-users-2/outputs/Phase6_Closeout/.
- McMaster94459A140 drawing reference evidence: outputs/Phase7_Hardware_Evidence/94459A140_Drawing_Review.json. Brian parked further niche insert research. Keep missing tolerances/usable-depth/wall and installation claims UNKNOWN; do not infer dimensions or revise pins.
- Protected pi4_baseline.scad, assembly.json, pi_reference.json and mounting files unchanged. Rechecked evidence/photo/earlier-STL/protected hashes in outputs/Phase7_Closeout/Evidence_Check.json. Prior handoff saved there as before_HANDOFF.md.

## Next steps

1. Present closeout review to Brian. No new tests/rendering are needed solely for documentation changes.
2. After closeout direction, establish intended normal-use app/data path without overwriting existing data or mistaking disposable acceptance data for the user's library.
3. Fresh desktop sessions require Brian's permission. Any later workflow review, release preparation or further physical work is separately scoped. No print/purchase/release package/publish/deploy/push authorized.

## Decisions and limitations

Preserve all outputs/,work/,user data,immutable hardware revisions/cache and project pins. Most app/evidence assets are untracked; Git alone is not a backup. Draft does not save; explicit imports do not repin; failures block proposed export; UNKNOWNs remain explicit. M3x0.5 adapter/pilot3–4.2/fixed stack3.3,pocket8,boss9 retained. Four-corner mounting matter remains TABLED until Brian raises it; supplied-photo/file identification is not reopening it. Strength/retention/torque, installation approval, Pi-board/rack/cable/tool access and whole-Pi containment/global clearance remain UNKNOWN or unestablished. Supplier/Pi reference rights unresolved; no redistribution. Exact supplier/project source policy stays distinct from manufacturer corrections. No subagents unless authorized.

## Run/check

From canonical project root, Python C:/Program Files/Python310/python.exe; Node C:/Users/brian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe. App: python outputs/Mechanical_Design_App/app.py --port8767 --data work/NEW-disposable-folder (use actual separated CLI arguments --port 8767; --data points to a NEW folder). Ctrl+C stops it. Normal default launcher uses app-relative data/ and port8765; intended active data location is not yet established. No running acceptance server remains from digital tests.

Routine Python discovery includes the tabled mounting-specific test; for current acceptance scope use work/phase7-digital/accept.py filtering and inspect its fresh-data behavior before running. It renders and uses disposable data, so don't rerun by default. Existing Node tests: app test_catalog_workflow.cjs, test_phase7_workflow.cjs; work/test_viewer_v08.cjs; JS syntax checks and work/extract_frontend.py. OpenSCAD.exe C:/Program Files/OpenSCAD/openscad.exe (not broken .com launcher). User-authorized rendering only. No automatic builds or historical evidence regeneration.
''',encoding='utf-8')
a=root/'AGENTS.md';s=a.read_text(encoding='utf-8').replace('HANDOFF.md contains the Phase 6 closeout; PROJECT.md and docs/phase7-readiness record the subsequent preparation.','HANDOFF.md contains current Phase7 status; outputs/Phase7_Closeout/Closeout_Review.md consolidates digital acceptance and Brian\'s reported specimen fit. Historical planning remains in docs/phase7-readiness.')
s=s.replace('Phase 6 is closed WITH LIMITATIONS. Phase 7 is in preparation.','Phase 6 is closed WITH LIMITATIONS. Phase 7 digital acceptance is complete with limitations; Brian confirms qualitative fit of the earlier supplied specimen, and closeout review is ready.')
s+='''\n## Confirmed specimen and parked research — 2026-10-18\n\nBrian confirms positive physical fit of the earlier supplied tray/faceplate specimen; preserve that report/photos/provenance without repeatedly asking him to identify already recovered files. This is specimen-specific qualitative evidence, not general strength/installation approval or a physical test of the later digital build. Remaining niche insert research is parked at Brian's direction; do not resume by default. Phase7 closeout review is prepared; do not silently mark every physical UNKNOWN passed. Further printing/testing remains separately authorized.\n''';a.write_text(s,encoding='utf-8')
p=root/'PROJECT.md';s=p.read_text(encoding='utf-8');s='''> Current milestone — 2026-10-18: Phase7 digital acceptance complete with limitations; Brian confirms positive qualitative fit of the earlier supplied specimen. Point8 closeout review is ready at outputs/Phase7_Closeout/Closeout_Review.md. Older status passages below are historical; HANDOFF.md is the concise current state. Further niche insert research is parked.\n\n'''+s;p.write_text(s,encoding='utf-8')
print(json.dumps(validation))
