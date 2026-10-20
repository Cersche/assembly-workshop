from pathlib import Path
import json,hashlib,difflib
root=Path.cwd();out=root/'outputs/Phase7_Digital_Acceptance';app=root/'outputs/Mechanical_Design_App'
# Freeze a readable code/doc change record without staging or committing untracked assets.
patch=[]
for name in ['mesh_revision.py','index.html','README.md','hardware-records.md']:
    before=(out/('before_'+name)).read_text(encoding='utf-8').splitlines(True)
    after=(app/name).read_text(encoding='utf-8').splitlines(True)
    patch.extend(difflib.unified_diff(before,after,fromfile='before/'+name,tofile='after/'+name))
(out/'Changes.patch').write_text(''.join(patch),encoding='utf-8')
report=json.loads((out/'Digital_Integration.json').read_text(encoding='utf-8'))
revision=Path(report['cache_path'])
processing=json.loads((revision/'revision.json').read_text(encoding='utf-8'))['mesh_processing']
(out/'Export_Processing.json').write_text(json.dumps(processing,indent=2),encoding='utf-8')
for name in ['HANDOFF.md','PROJECT.md']:
    p=root/name
    (out/('before_final_'+name)).write_bytes(p.read_bytes())
    s=p.read_text(encoding='utf-8')
    s+='''\n## Phase 7 points 2–6 — 2026-10-18\n\nCompleted digital acceptance WITH LIMITATIONS; see outputs/Phase7_Digital_Acceptance/Report.md.46 Python tests PASS, one preexisting mounting-specific test deferred; Node behavioral/syntax and9 localhost endpoints PASS. Fresh supported M3 trial render, source/STL/viewer integrity, cache reuse, corrupted-export rejection and pin preservation verified in new disposable data. Protected baseline/reference/mounting files and35 old-cache files unchanged. No desktop/physical work or release packaging occurred.\n\nNew renders use pi4-mesh-v2-triangulation1, strict mesh checks and artifact integrity manifests. Exact collinear export-face repair preserves existing coordinates/surface; raw/output hashes and processing trace are recorded. Old immutable caches are retained; legacy downloads lacking the new manifest require explicit regeneration into a separate new entry. Physical fit/strength and unsupported hardware dimensions remain UNKNOWN. Printer/slicer integration is outside scope. Mounting remains tabled. Report to Brian before point7; physical work requires separate direction and printing approval.\n'''
    p.write_text(s,encoding='utf-8')
status=root/'outputs/Phase7_Start/Status.md'
status.write_text(status.read_text(encoding='utf-8')+'\n## Subsequent milestone\n\nPhase7 points2–6 completed with limitations. Current acceptance: ../Phase7_Digital_Acceptance/Report.md. Earlier preparation entries remain historical; printer/material selection does not block software acceptance. Physical work has not started.\n',encoding='utf-8')
manifest={}
for p in [app/n for n in ['mesh_revision.py','index.html','README.md','hardware-records.md','test_mesh_integrity.py','test_phase7_workflow.cjs']]+list(out.glob('*.json'))+list(out.glob('*.md')):
    manifest[str(p.relative_to(root))]=hashlib.sha256(p.read_bytes()).hexdigest()
(out/'Acceptance_File_Hashes.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
assert all(hashlib.sha256((app/f).read_bytes()).hexdigest()==h for f,h in report['protected_hashes'].items())
print('Acceptance report, processing evidence, change patch, file hashes and durable handoffs saved. Protected hashes unchanged.')
