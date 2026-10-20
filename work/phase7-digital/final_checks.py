from pathlib import Path
import subprocess,json,hashlib
root=Path.cwd();out=root/'outputs/Phase7_Closeout';app=root/'outputs/Mechanical_Design_App'
node='C:/Users/brian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
checks=[]
for label,args in [('catalog_handlers',[node,str(app/'test_catalog_workflow.cjs')]),('phase7_handlers',[node,str(app/'test_phase7_workflow.cjs')]),('extract_frontend',['C:/Program Files/Python310/python.exe','-B','work/extract_frontend.py']),('frontend_syntax',[node,'--check','work/app_frontend_check.js']),('app_cli',['C:/Program Files/Python310/python.exe','-B',str(app/'app.py'),'--help'])]:
    r=subprocess.run(args,cwd=root,capture_output=True,text=True,encoding='utf-8')
    (out/(label+'_final.log')).write_text(r.stdout+r.stderr,encoding='utf-8')
    checks.append(dict(check=label,exit_code=r.returncode));assert r.returncode==0,label
before=(out/'before_final_index.html').read_text(encoding='utf-8');after=(app/'index.html').read_text(encoding='utf-8')
assert before.split('<script>')[1]==after.split('<script>')[1],'Unexpected JS implementation change'
manifest=json.loads((root/'outputs/Phase7_Digital_Acceptance/Acceptance_File_Hashes.json').read_text(encoding='utf-8'))
changed=[]
for name,expected in manifest.items():
    actual=hashlib.sha256((root/name).read_bytes()).hexdigest()
    if actual!=expected:changed.append(Path(name).as_posix())
assert set(changed)=={'outputs/Mechanical_Design_App/index.html','outputs/Mechanical_Design_App/README.md'},changed
integration=json.loads((root/'outputs/Phase7_Digital_Acceptance/Digital_Integration.json').read_text(encoding='utf-8'))
for name,expected in integration['protected_hashes'].items():assert hashlib.sha256((app/name).read_bytes()).hexdigest()==expected
result=dict(date='2026-10-18',checks=checks,inline_js_unchanged=True,changed_since_acceptance=changed,change_scope='Static phase/closeout text only',protected_assets='5 hashes PASS',full_python_suite='Prior46 PASS retained; no implementation changed; not repeated',fresh_render=False,desktop=False,physical_test=False,release_packaged=False)
(out/'Final_Checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('Final targeted checks PASS; inline JS unchanged; only roadmap/README differ from digital acceptance files; protected hashes match.')

