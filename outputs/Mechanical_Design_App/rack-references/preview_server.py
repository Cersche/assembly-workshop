"""Fresh local appearance fixture; no active data or mesh builds."""
from pathlib import Path
import sys
import tempfile
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'outputs/Mechanical_Design_App'))
import app
import rack_workspace
with tempfile.TemporaryDirectory(prefix='fixture-', dir=Path(__file__).parent) as folder:
    data=Path(folder)
    store=app.Store(data/'library.sqlite3')
    store.load_starter()
    rack_workspace.save(data, {'version':1,'generation':None,'racks':[{'id':'brand-test','name':'Rack branding · disposable','slots':5,'width_mm':None,'depth_mm':None,'pitch_mm':None,'placements':[]}]},seed_project=store.project())
    base=app.make_handler(store,'branding-disposable')
    class Handler(base):
        def log_message(self,fmt,*args):
            with Path(__file__).with_name('http.log').open('a',encoding='utf-8') as f:f.write(fmt % args+'\n')
    server=app.WorkshopHTTPServer(('127.0.0.1',8771),Handler)
    print('Disposable rack branding fixture on8771',flush=True)
    try:server.serve_forever()
    finally:server.server_close()
