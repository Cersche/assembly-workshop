"""Disposable browser acceptance; never opens normal-use data or builds meshes."""
from pathlib import Path
import sys
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'outputs/Mechanical_Design_App'))
import app
import rack_workspace

with tempfile.TemporaryDirectory(prefix='visual-check-',dir=Path(__file__).resolve().parent) as folder:
    data=Path(folder)
    store=app.Store(data/'library.sqlite3')
    store.load_starter()
    rack_workspace.save(data,{'version':1,'generation':None,'racks':[{'id':'visual-check','name':'Lab Rax · mesh preview','slots':5,'width_mm':None,'depth_mm':None,'pitch_mm':None,'placements':[]}]})
    server=app.ThreadingHTTPServer(('127.0.0.1',8767),app.make_handler(store,'disposable-visual-check'))
    print('Disposable source-mesh preview at http://127.0.0.1:8767/',flush=True)
    try:server.serve_forever()
    finally:server.server_close()
