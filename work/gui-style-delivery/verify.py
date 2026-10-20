"""Read-only data preservation and document stylesheet regression check."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / 'outputs/Mechanical_Design_App'
sys.path.insert(0, str(APP))
import app

record = Path(__file__).with_name('data-before.json')
files = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
         for folder in ('data/normal-use', 'outputs/Mechanical_Design_App/data')
         for p in (ROOT / folder).rglob('*') if p.is_file()}
if '--snapshot' in sys.argv:
    record.write_text(json.dumps(files, indent=2), encoding='utf-8')
    print('Preserved data fingerprints:', len(files))
else:
    assert files == json.loads(record.read_text(encoding='utf-8')), 'User data changed'
    class ForbiddenStore:
        def __getattribute__(self, name):
            raise AssertionError('GUI delivery touched user store')
    handler_type = app.make_handler(ForbiddenStore(), 'test-token')
    handler = handler_type.__new__(handler_type)
    handler.path = '/'
    handler.valid_host = lambda: True
    responses = []
    handler.send = lambda value, status=200, mime='application/json': responses.append((value, status, mime))
    handler.do_GET()
    html, status, mime = responses[0]
    css = (APP / 'workspace.css').read_text(encoding='utf-8')
    assert status == 200 and mime == 'text/html'
    assert html.count('<style id="studio-workspace-css">') == 1
    assert '<style id="studio-workspace-css">' + css + '</style>' in html
    assert '<link rel="stylesheet" href="/workspace.css' not in html
    assert 'grid-template-columns' in css and 'library-section' in css
    assert hashlib.sha256((APP / 'rack-references/rack-scene.js').read_bytes()).hexdigest() == '414214bcbf3f1f40ff7a6be0791741ec721cb3d9585cc4d148b1c68f7ff1c7d2'
    print('PASS: canonical CSS in root document; no store access; rack lock intact;', len(files), 'data files unchanged')
