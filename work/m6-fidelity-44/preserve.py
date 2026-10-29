"""Re-prove task-43 preservation without writing to task-43 evidence."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OLD = ROOT/'work/m6-rails-43'
sys.path.insert(0, str(ROOT/'outputs/Mechanical_Design_App'))
import equipment as eq


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


if sys.argv[1:] == ['snapshot']:
    names = json.loads((OLD/'protected-before.json').read_text(encoding='utf-8'))
    names.update({str(p.relative_to(ROOT)).replace('\\', '/'): None
                  for p in (ROOT/'outputs/CM1000_M6_generated_2026-10-28').rglob('*') if p.is_file()})
    (HERE/'starting-hashes.json').write_text(json.dumps({n:sha(ROOT/n) for n in names}, indent=2), encoding='utf-8')
    source = (OLD/'verify_hdt.py').read_text(encoding='utf-8').replace("(HERE/'legacy-before.json')", "(ROOT/'work/m6-rails-43/legacy-before.json')")
    (HERE/'verify_hdt.py').write_text(source, encoding='utf-8')
else:
    cases = json.loads((OLD/'legacy-before.json').read_text(encoding='utf-8'))
    rows = []
    for c in cases:
        digest = hashlib.sha256(eq.source(eq.clean(c['spec'])).encode('utf-8')).hexdigest()
        rows.append(dict(label=c['label'], before=c['sha256'], after=digest, identical=digest==c['sha256']))
    baseline = json.loads((HERE/'starting-hashes.json').read_text(encoding='utf-8'))
    files = [dict(path=n, before=h, after=sha(ROOT/n), identical=h==sha(ROOT/n)) for n,h in baseline.items()]
    protected = [r for r in files if r['path'] not in ('outputs/Mechanical_Design_App/equipment.py', 'outputs/Mechanical_Design_App/equipment_tray.scad') and not r['path'].startswith('outputs/CM1000_M6_generated_2026-10-28/')]
    result = dict(source_cases=rows, files=files, all_14_identical=len(rows)==14 and all(r['identical'] for r in rows), protected_identical=all(r['identical'] for r in protected))
    (HERE/'preservation.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print({k:v for k,v in result.items() if isinstance(v,bool)})
    if not result['all_14_identical'] or not result['protected_identical']:
        raise SystemExit(1)
