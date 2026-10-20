from pathlib import Path
import sys,json,threading,urllib.request,urllib.error,tempfile
sys.dont_write_bytecode=True
root=Path.cwd();sys.path.insert(0,str(root/'outputs/Mechanical_Design_App'))
import app
with tempfile.TemporaryDirectory(prefix='aw-rack-http-',dir=root/'work/gui-restoration') as tmp:
    store=app.Store(Path(tmp)/'library.sqlite3');store.load_starter();before=store.state()
    server=app.ThreadingHTTPServer(('127.0.0.1',0),app.make_handler(store,'test-token'))
    worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
    base='http://127.0.0.1:'+str(server.server_port)
    def call(path,data=None,token='test-token'):
        req=urllib.request.Request(base+path,data=None if data is None else json.dumps(data).encode('utf-8'),headers={'Content-Type':'application/json','X-App-Token':token})
        with urllib.request.urlopen(req,timeout=10) as result:return result.status,result.read()
    try:
        for path in ['/','/workspace.css','/workspace.js','/api/rack-workspace','/api/state','/api/assembly']:
            assert call(path)[0]==200
        value={'version':1,'generation':None,'racks':[{'id':'rack','name':'Custom rack','slots':5,'width_mm':None,'depth_mm':None,'pitch_mm':None,'placements':[{'id':'pi','equipment':'pi4','slot':2,'span':2}]}]}
        saved=json.loads(call('/api/rack-workspace',value)[1]);assert saved['racks'][0]['placements'][0]['fit']=='UNKNOWN'
        assert json.loads(call('/api/rack-workspace')[1])==saved
        try:call('/api/rack-workspace',value)
        except urllib.error.HTTPError as e:assert e.code==400
        else:raise AssertionError('Stale write accepted')
        try:call('/api/rack-workspace',saved,token='wrong')
        except urllib.error.HTTPError as e:assert e.code==403
        else:raise AssertionError('Invalid token accepted')
        assert store.state()==before
        (root/'work/gui-restoration/HTTP_Checks.json').write_text(json.dumps({'static_and_api_gets':'PASS','rack_save_reload':'PASS','stale_save_blocked':'PASS','invalid_token_blocked':'PASS','hardware_rows_and_project_unchanged':'PASS','renders':0},indent=2),encoding='utf-8')
        print('PASS: GUI assets, API save/reload, stale write and token guards; hardware state unchanged; no builds.')
    finally:server.shutdown();server.server_close();worker.join()
