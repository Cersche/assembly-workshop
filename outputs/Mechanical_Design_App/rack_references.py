"""Read-only, integrity-checked local reference assets; no CAD/export adapter."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'rack-references'


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
    if hashlib.sha256(data).hexdigest() != entry['sha256']:
        raise ValueError('Local reference integrity check failed.')
    return data, entry['mime']
