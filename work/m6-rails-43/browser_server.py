"""Task 43 browser acceptance. New scratch DB/library only, no automatic builds."""
import json
from pathlib import Path
import secrets
import shutil
import sys

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'outputs/Mechanical_Design_App'))
import app
import equipment as eq

data=HERE/'browser-data'
data.mkdir(exist_ok=True)
spec=json.loads((HERE/'cm6b-spec.json').read_text(encoding='utf-8'))
src=eq.source(eq.clean(spec))
import hashlib
identity=hashlib.sha256(src.encode('utf-8')).hexdigest()
cache=HERE/'render-data/equipment-revisions'/identity
destination=data/'equipment-revisions'/identity
if not destination.exists():shutil.copytree(cache,destination)
item=dict(id='eq-0000000043b0',name=spec['name'],spec=spec,span=1,build=identity,parts=['faceplate','rail_l','rail_r'],status='PROPOSED — UNVALIDATED')
flat=dict(name='Task 43 switch fixture',dev_w=120,dev_d=80,dev_h=30,device_mount='flat',standoff=0,joint='screw',u=1)
items=[item,dict(id='eq-0000000043b1',name=flat['name'],spec=flat,span=1,parts=['tray','faceplate'],status='PROPOSED — UNVALIDATED')]
(data/'equipment-library.json').write_text(json.dumps(items,indent=2),encoding='utf-8')
store=app.Store(data/'library.sqlite3')
store.load_starter()
server=app.WorkshopHTTPServer(('127.0.0.1',8819),app.make_handler(store,secrets.token_hex(24)))
print('Task 43 NEW disposable data:',data,flush=True)
print('http://127.0.0.1:8819',flush=True)
try:server.serve_forever()
except KeyboardInterrupt:pass
finally:server.server_close()
