"""Read verified optional metadata packs; importing them is an explicit app action."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'catalog-packs'
PACK_IDS = ('phase6-batch1', 'phase6-batch2', 'phase6-batch3', 'phase6-batch4', 'phase6-batch5', 'phase6-batch6', 'phase6-batch7')


def inventory():
    result = []
    for identity in PACK_IDS:
        try:
            manifest = json.loads((ROOT / (identity + '-manifest.json')).read_text(encoding='utf-8'))
            raw = (ROOT / (identity + '.json')).read_bytes()
            if (manifest['id'] != identity or manifest['file'] != identity + '.json'
                    or hashlib.sha256(raw).hexdigest() != manifest['sha256']):
                raise ValueError('Pack identity/hash mismatch.')
            records = json.loads(raw)
            if not isinstance(records, list) or len(records) != manifest['records']:
                raise ValueError('Pack record count mismatch.')
            result.append(dict(id=identity, available=True, records=records, manifest=manifest))
        except (OSError, ValueError, KeyError, TypeError) as exc:
            result.append(dict(id=identity, available=False, error=str(exc)))
    try:
        gaps = json.loads((ROOT/'source-gaps.json').read_text(encoding='utf-8'))
        if not isinstance(gaps, dict) or not isinstance(gaps.get('gaps'), list):
            raise ValueError('Invalid gap evidence.')
    except (OSError, ValueError, TypeError) as exc:
        gaps = {'gaps': [], 'error': str(exc)}
    return {'packs': result, 'gaps': gaps}
