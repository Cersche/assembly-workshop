"""Compare regression sources and protected bytes against task-43 pre-edit evidence."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'outputs/Mechanical_Design_App'))
import equipment as eq

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

cases = json.loads((HERE/'legacy-before.json').read_text(encoding='utf-8'))
results = []
for case in cases:
    after = sha(eq.source(eq.clean(case['spec'])).encode('utf-8'))
    results.append(dict(label=case['label'],before=case['sha256'],after=after,identical=case['sha256']==after))
protected = json.loads((HERE/'protected-before.json').read_text(encoding='utf-8'))
files = [dict(path=name,before=before,after=sha((ROOT/name).read_bytes()),
              identical=before==sha((ROOT/name).read_bytes())) for name,before in protected.items()]
historical = [c for c in files if Path(c['path']).as_posix() not in ('outputs/Mechanical_Design_App/equipment.py','outputs/Mechanical_Design_App/equipment_tray.scad')]
result = dict(source_cases=results,protected_files=files,
              all_sources_identical=all(c['identical'] for c in results),
              all_protected_identical=all(c['identical'] for c in historical))
(HERE/'preservation-results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if isinstance(v,bool)}))
if not result['all_sources_identical'] or not result['all_protected_identical']:
    raise SystemExit(1)
