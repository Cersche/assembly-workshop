from pathlib import Path
import sys,os,json,hashlib,io,unittest,subprocess,zipfile,shutil,threading
from urllib.request import build_opener,ProxyHandler,Request
from http.server import ThreadingHTTPServer
root=Path.cwd();app=root/'outputs/Mechanical_Design_App';out=root/'outputs/Phase7_Digital_Acceptance'
sys.path.insert(0,str(app))
import mesh_revision as mesh, catalog_packs,catalog_evidence
from app import Store,design_revision,evaluate,make_handler

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(p):return {str(x.relative_to(p)):digest(x) for x in p.rglob('*') if x.is_file()}
def write(name,data): (out/name).write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
# Existing immutable cache contents and protected files must stay untouched.
old_cache=root/'work/v08-build/revisions';old_hashes=inventory(old_cache)
reference=json.loads((app/'pi_reference_manifest.json').read_text(encoding='utf-8'))
protected={f:digest(app/f) for f in ['pi4_baseline.scad','assembly.json','pi_reference.json','faceplate_mounting.py','faceplate_mounting.json']}
for f,k in [('pi4_baseline.scad','baseline_source_sha256'),('assembly.json','baseline_assembly_sha256'),('pi_reference.json','sha256')]: assert protected[f]==reference[k]
# Routine tests apart from the explicitly tabled mounting-specific test.
if '--integration-only' not in sys.argv:
    loader=unittest.TestLoader();suite=loader.discover(str(app))
    def flatten(s):
        for t in s:
            if isinstance(t,unittest.TestSuite):yield from flatten(t)
            else:yield t
    excluded=[];chosen=[]
    for test in flatten(suite):
        if test.id().endswith('test_revision_uses_four_corner_default_and_rejects_failed_or_unsupported_inputs'):excluded.append(test.id())
        else:chosen.append(test)
    with (out/'python_tests.log').open('w',encoding='utf-8') as log:
        result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.TestSuite(chosen))
    write('Test_Summary.json',dict(run=result.testsRun,failures=len(result.failures),errors=len(result.errors),excluded_tabled=excluded))
    assert result.wasSuccessful(),'Python tests failed; inspect python_tests.log'
    print(f'Python: {result.testsRun} PASS; {len(excluded)} existing mounting-specific test deferred.',flush=True)
else:
    summary=json.loads((out/'Test_Summary.json').read_text(encoding='utf-8'));assert summary['failures']==0 and summary['errors']==0
packs=catalog_packs.inventory()['packs'];assert len(packs)==7 and all(p['available'] for p in packs)
from uuid import uuid4
data=root/'work/phase7-digital'/('acceptance-data-'+uuid4().hex[:8])
if data.exists():raise SystemExit('Acceptance data already exists; choose a fresh folder before rerunning integration')
data.mkdir(parents=True)
store=Store(data/'library.sqlite3');store.load_starter()
parts=store.parts();selected={p['kind']:p for p in parts if p.get('part_number') in ['SSCF-M3-8-A2','94459A140']}
payload={'selections':{k:{'id':v['id'],'revision':v['revision']} for k,v in selected.items()},'inputs':{'pilot':4}}
store.save(payload);saved=store.project()
for pack in packs:store.import_parts(pack['records'])
assert store.project()==saved
all_parts=store.parts();assert len(all_parts)==38 and len({p['id'] for p in all_parts})==34
before_import=store.parts()
for pack in packs:store.import_parts(pack['records'])
assert store.parts()==before_import and store.project()==saved
trial=evaluate(selected['screw'],selected['heatset'],{'pilot':4})
counts={s:sum(c['status']==s for c in trial['checks']) for s in ['pass','fail','unknown']}
assert counts=={'pass':7,'fail':0,'unknown':6}
write('Hardware_Audit.json',dict(parts=selected,offline_audit=[catalog_evidence.inspect(p) for p in selected.values()],rule_report=trial,counts=counts,catalog_identities=34,catalog_revisions=38,pack_hashes='7 PASS',saved_pins_preserved=True))
# Exercise only supported joint inputs and known failed/unsupported cases; no mounting-layout assertions.
for bad in [{'pilot':4.2},{'pilot':2.9},{'pilot':4,'stack':3.4},{'pilot':4,'boss_diameter':10}]:
    try:design_revision(dict(selections=selected,inputs=bad))
    except ValueError:pass
    else:raise AssertionError('Unsupported/failed inputs exported: '+str(bad))
bad_selection={k:dict(v) for k,v in selected.items()};bad_selection['screw']['diameter']=4
try:design_revision(dict(selections=bad_selection,inputs={'pilot':4}))
except ValueError:pass
else:raise AssertionError('Unsupported thread exported')
source,meta=design_revision(store.draft(payload))
print('Rendering exact current proposal in disposable cache; no mechanical layout changes or mounting acceptance.',flush=True)
build=mesh.build(source,meta,data);assert not build['cached']
folder=data/'revisions'/build['id'];before=inventory(folder)
again=mesh.build(source,meta,data);assert again['cached'];assert inventory(folder)==before
assert (folder/'pi4_proposed.scad').read_text(encoding='utf-8')==source
assembly=json.loads((folder/'assembly.json').read_text(encoding='utf-8'));assert assembly['units']=='mm'
base=json.loads((app/'assembly.json').read_text(encoding='utf-8'))
measurements=[]
for part in assembly['parts']:
    baseline=next(p for p in base['parts'] if p['id']==part['id'])
    bounds=part['bounds'];assert all(abs(bounds[i][k]-baseline['bounds'][i][k])<0.01 for i in range(2) for k in range(3)),(part['id'],bounds,baseline['bounds'])
    measurements.append(dict(part=part['id'],triangles=len(part['triangles']),bounds_mm=bounds,extent_mm=[bounds[1][k]-bounds[0][k] for k in range(3)],signed_volume_mm3=part['signed_volume_mm3'],stl_sha256=part['source_sha256'],units='mm by source/project convention; STL has no encoded unit',orientation='Untransformed assembly coordinates; no print-bed orientation prescribed'))
# Inspect the existing download pathway in memory only; do not create a release archive.
archive_bytes=mesh.bundle(build['id'],data)
with zipfile.ZipFile(io.BytesIO(archive_bytes)) as z:
    assert z.testzip() is None
    for name in z.namelist():assert z.read(name)==(folder/name).read_bytes()
assert store.project()==saved
# A corrupted copy must fail without changing either good or damaged immutable entries.
corrupt=root/'work/phase7-digital/corrupt-copy';target=corrupt/'revisions'/build['id'];shutil.copytree(folder,target)
(target/'tray.stl').write_bytes((target/'tray.stl').read_bytes()+b'CORRUPTION')
damaged=inventory(target)
try:mesh.bundle(build['id'],corrupt)
except ValueError:pass
else:raise AssertionError('Corrupt export accepted')
assert inventory(target)==damaged and inventory(folder)==before
# Real HTTP handler routes with isolated store, existing build reused and no browser.
server=ThreadingHTTPServer(('127.0.0.1',0),make_handler(store,'phase7-isolated-token'))
thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
url=f'http://127.0.0.1:{server.server_port}';opener=build_opener(ProxyHandler({}));http=[]
try:
    for route in ['/','/api/state','/api/project','/api/catalog-packs','/api/assembly','/catalog.js','/viewer.js']:
        with opener.open(url+route,timeout=30) as r:
            raw=r.read();assert r.status==200 and raw
            if route.startswith('/api/'):json.loads(raw)
            http.append(dict(route=route,status=r.status,bytes=len(raw)))
    def post(route,body):
        request=Request(url+route,data=json.dumps(body).encode(),headers={'Content-Type':'application/json','X-App-Token':'phase7-isolated-token'})
        return opener.open(request,timeout=30)
    with post('/api/build',payload) as r:
        cached=json.load(r);assert cached['cached'] and cached['id']==build['id'];http.append(dict(route='/api/build',status=r.status,cached=True))
    with post('/api/build-bundle',{'id':build['id']}) as r:
        with zipfile.ZipFile(io.BytesIO(r.read())) as z:assert z.testzip() is None
        http.append(dict(route='/api/build-bundle',status=r.status,in_memory_only=True))
finally:
    server.shutdown();server.server_close();thread.join(timeout=10)
assert not thread.is_alive()
assert store.project()==saved
assert all(digest(app/f)==h for f,h in protected.items())
assert inventory(old_cache)==old_hashes
assert inventory(folder)==before
version=subprocess.run([mesh.compiler(),'--version'],capture_output=True,text=True,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
write('Digital_Integration.json',dict(build_id=build['id'],renderer=mesh.compiler(),renderer_version=(version.stdout+version.stderr).strip(),cache_path=str(folder),source_sha256=digest(folder/'pi4_proposed.scad'),measurements=measurements,cache_reuse='PASS',in_memory_export='PASS',corrupt_cache_rejection='PASS',http=http,http_server_stopped=True,store_pins_preserved=True,old_cache_files_preserved=len(old_hashes),protected_hashes=protected,physical_fit='UNKNOWN',strength='UNKNOWN',mounting_layout='TABLED; no new layout assertions or mechanical changes',desktop_session=False,release_packaged=False))
print('Real render, bounds/units, viewer/STL matching, cache reuse, export and HTTP checks PASS; protected files/pins/old cache preserved.',flush=True)
