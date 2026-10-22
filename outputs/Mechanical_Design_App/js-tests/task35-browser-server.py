from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
ROOT=Path('D:/Projects/assembly-workshop')
APP=ROOT/'outputs/Mechanical_Design_App'
class Handler(SimpleHTTPRequestHandler):
    def translate_path(self,path):
        from urllib.parse import unquote,urlsplit
        name=unquote(urlsplit(path).path).lstrip('/')
        base=APP
        if name.startswith('before/'):
            base=ROOT/'docs/archive/codex/2026-10-22/task35'
            name=name[len('before/'):]
        target=(base/name).resolve()
        if not target.is_relative_to(base.resolve()) or any(x in target.parts for x in ['data','normal-use']):
            return str(APP/'js-tests/no-such-file')
        return str(target)
ThreadingHTTPServer(('127.0.0.1',8836),Handler).serve_forever()
