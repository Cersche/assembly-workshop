from pathlib import Path
import sys,json,sqlite3,hashlib,threading,urllib.request,subprocess,tempfile
sys.dont_write_bytecode=True
root=Path(__file__).resolve().parents[2]; appdir=root/'outputs/Mechanical_Design_App'; sys.path.insert(0,str(appdir))
import app,mesh_revision
p=Path(__file__).with_name('Setup.json'); report=json.loads(p.read_text(encoding='utf-8')); dst=Path(report['normal_use']); src=Path(report['source'])
def hashes(path):
    return {str(f.relative_to(path)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(path.rglob('*')) if f.is_file()}
def rows(path):
    with sqlite3.connect((path/'library.sqlite3').as_uri()+'?mode=ro',uri=True) as db:
        assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        return {t:db.execute('SELECT * FROM '+t+' ORDER BY 1,2').fetchall() for t in ('parts','projects')}
before=rows(src); store=app.Store(dst/'library.sqlite3'); state=store.state()
assert len(state['parts'])==6 and rows(dst)==before
server=app.ThreadingHTTPServer(('127.0.0.1',0),app.make_handler(store,'local-check')); thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start(); checks={}
try:
    for endpoint in ('/','/api/state','/api/project'):
        with urllib.request.urlopen('http://127.0.0.1:'+str(server.server_port)+endpoint,timeout=10) as response:
            body=response.read(); checks[endpoint]=response.status
            if endpoint=='/api/project': assert json.loads(body)==state['project']
finally:
    server.shutdown(); server.server_close(); thread.join()
legacy=[]
for folder in (dst/'revisions').iterdir():
    if folder.is_dir():
        try: mesh_revision.checked_revision(folder,folder.name)
        except ValueError as exc:
            assert not (folder/'integrity.json').exists(),str(exc)
            legacy.append({'id':folder.name,'status':'Preserved; download blocked because legacy integrity manifest is absent.','detail':str(exc)})
with tempfile.TemporaryDirectory(prefix='aw-startup-') as tmp:
    missing=Path(tmp)/'missing'; result=subprocess.run([sys.executable,'-B',str(appdir/'app.py'),'--existing-library','--data',str(missing)],capture_output=True,text=True,encoding='utf-8')
    assert result.returncode==2 and not missing.exists()
assert rows(dst)==before and hashes(src)==report['source_hashes']==hashes(dst)
report.update({'sqlite_integrity':'ok','current_app_store_and_state':'PASS','localhost_get_checks':checks,'all_database_rows_and_pins_unchanged':True,'all_source_and_copy_file_hashes_unchanged':True,'legacy_caches':legacy,'missing_library_startup_guard':'PASS: exit 2; no directory created','automatic_imports':False,'builds_regenerated':False})
p.write_text(json.dumps(report,indent=2),encoding='utf-8'); print('PASS: compatibility, HTTP, pins, all six file hashes, missing-library guard. Legacy caches:',len(legacy))
