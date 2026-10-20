"""Fresh startup fixture and DOM-backed script diagnostics; no active data."""
from pathlib import Path
import re
import sys
import tempfile
import traceback
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'outputs/Mechanical_Design_App'))
import app
import rack_workspace

def log(text):
    with (HERE / 'http.log').open('a', encoding='utf-8') as stream:
        stream.write(datetime.now(timezone.utc).isoformat() + ' ' + text + '\n')

with tempfile.TemporaryDirectory(prefix='fixture-', dir=HERE) as folder:
    data = Path(folder)
    store = app.Store(data / 'library.sqlite3')
    store.load_starter()
    rack_workspace.save(data, {'version': 1, 'generation': None, 'racks': [
        {'id': 'startup-test', 'name': 'Startup reliability · disposable', 'slots': 5,
         'width_mm': None, 'depth_mm': None, 'pitch_mm': None, 'placements': []}
    ]}, seed_project=store.project())
    base = app.make_handler(store, 'startup-disposable')
    class Handler(base):
        def log_message(self, fmt, *args):
            log(fmt % args)

        def send(self, value, status=200, mime='application/json'):
            if mime == 'text/html':
                diagnostic = '''<script>
function recordStartupError(text){
 let box=document.getElementById('startup-diagnostics');
 if(!box){box=document.createElement('pre');box.id='startup-diagnostics';box.style='position:fixed;bottom:0;z-index:999;background:#000;color:#fff;font-size:10px';document.documentElement.append(box);}
 box.textContent += '\\n'+text;
}
window.addEventListener('error', function(e){
 recordStartupError('ERROR: '+(e.message||e.target.src||e.target.href||'resource')+' '+(e.filename||'')+':'+(e.lineno||''));
},true);
window.addEventListener('unhandledrejection', function(e){
 recordStartupError('REJECTION: '+String(e.reason));
});
</script>'''
                value = value.replace('<title>', diagnostic + '<title>', 1)
                value = value.replace('<body>', '<body><pre id="startup-diagnostics" style="position:fixed;bottom:0;z-index:999;background:#000;color:#fff;font-size:10px;max-height:90px;overflow:auto">Startup diagnostics</pre>', 1)
                value = re.sub(r'<script src="([^"]+)">', lambda m: '<script src="' + m[1] + '" onload="this.dataset.loaded=\'yes\'" onerror="this.dataset.loaded=\'failed\'">', value)
            return super().send(value, status, mime)

    class Server(app.WorkshopHTTPServer):
        request_queue_size = 5 if '--small-queue' in sys.argv else app.WorkshopHTTPServer.request_queue_size
        def handle_error(self, request, client_address):
            log(traceback.format_exc())
    server = Server(('127.0.0.1', 8770), Handler)
    print('Disposable startup diagnostics on 8770', flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()
