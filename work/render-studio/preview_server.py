"""Disposable renderer acceptance server; never opens active user data."""
from pathlib import Path
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
APP=ROOT/'outputs/Mechanical_Design_App'
sys.path.insert(0,str(APP))
import app
import rack_workspace

with tempfile.TemporaryDirectory(prefix='acceptance-',dir=Path(__file__).resolve().parent) as folder:
    data=Path(folder)
    store=app.Store(data/'library.sqlite3')
    store.load_starter()
    rack_workspace.save(data,{'version':1,'generation':None,'racks':[{'id':'render-check','name':'Render Studio · disposable acceptance','slots':5,'width_mm':None,'depth_mm':None,'pitch_mm':44.45,'placements':[{'id':'render-pi','slot':3,'span':1,'equipment':'pi4'}]}]},seed_project=store.project())
    base=app.make_handler(store,'render-studio-disposable')
    class Handler(base):
        def do_GET(self):
            if self.path=='/render-showcase':
                return self.send((Path(__file__).parent/'showcase.html').read_text(encoding='utf-8'),mime='text/html')
            if self.path=='/render-checks.js':
                return self.send((Path(__file__).parent/'gpu-checks.js').read_text(encoding='utf-8'),mime='text/javascript')
            return super().do_GET()
    server=app.ThreadingHTTPServer(('127.0.0.1',8767),Handler)
    print('Disposable render acceptance: http://127.0.0.1:8767/render-showcase',flush=True)
    try: server.serve_forever()
    finally: server.server_close()
