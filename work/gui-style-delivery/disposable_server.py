"""Fresh test data; deliberately deny external CSS to prove self-contained styling."""
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'outputs/Mechanical_Design_App'))
import app
import rack_workspace

with tempfile.TemporaryDirectory(prefix='browser-fixture-', dir=Path(__file__).parent) as folder:
    data = Path(folder)
    store = app.Store(data / 'library.sqlite3')
    store.load_starter()
    rack_workspace.save(data, {'version': 1, 'generation': None, 'racks': [
        {'id': 'css-test', 'name': 'CSS persistence · disposable', 'slots': 5,
         'width_mm': None, 'depth_mm': None, 'pitch_mm': None, 'placements': []}
    ]}, seed_project=store.project())
    base = app.make_handler(store, 'css-persistence-disposable')
    class Handler(base):
        def log_message(self, fmt, *args):
            with Path(__file__).with_name('browser-http.log').open('a', encoding='utf-8') as log:
                log.write((fmt % args) + '\n')

        def do_GET(self):
            if self.path.split('?')[0] == '/workspace.css':
                return self.send('Stylesheet deliberately unavailable for regression test', 503, 'text/plain')
            return super().do_GET()
    server = app.ThreadingHTTPServer(('127.0.0.1', 8769), Handler)
    print('Disposable CSS failure test on 8769', flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()
