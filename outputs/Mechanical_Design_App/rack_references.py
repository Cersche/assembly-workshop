"""Read-only, integrity-checked local reference assets; no CAD/export adapter."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'rack-references'
TEXT_MIMES = ('application/json', 'text/javascript')


def digest(data, mime):
    # Text assets hash with LF endings so Windows (CRLF) and Linux (LF) checkouts pass the same check.
    if mime in TEXT_MIMES:
        data = data.replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()


def asset(url):
    if not url.startswith('/rack-references/'):
        return None
    entries = json.loads((ROOT / 'asset-manifest.json').read_text(encoding='utf-8'))
    entry = next((item for item in entries if item['url'] == url), None)
    if entry is None:
        return None
    # No user-controlled path ever reaches the filesystem.
    name = entry['file']
    if Path(name).name != name or '/' in name or '\\' in name:
        raise ValueError('Invalid local reference manifest.')
    data = (ROOT / name).read_bytes()
    if digest(data, entry['mime']) != entry['sha256']:
        raise ValueError('Local reference integrity check failed.')
    return data, entry['mime']
