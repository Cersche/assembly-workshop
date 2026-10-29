"""Task 43 pre-edit evidence. Reads user library bytes only; tests use this new copy."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
APP = ROOT / 'outputs/Mechanical_Design_App'
sys.path.insert(0, str(APP))
import equipment as eq
from test_tray_pair import A, B

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def main():
    copy = HERE / 'library-readonly-copy.json'
    if not copy.exists():
        copy.write_bytes((ROOT / 'data/normal-use/equipment-library.json').read_bytes())
    if (HERE / 'legacy-before.json').exists():
        raise SystemExit('Baseline already captured; refusing to overwrite.')
    cases = []
    for label, path in [('example', APP / 'equipment-examples.json'), ('library-copy', copy)]:
        for i, item in enumerate(json.loads(path.read_text(encoding='utf-8'))):
            cases.append((f'{label}-{i}-{item["name"]}', item['spec']))
    hdt = json.loads((ROOT / 'outputs/Hard_Drive_Tray_2026-10-25/revision.json').read_text(encoding='utf-8'))['spec']
    cases += [('HDT-M6-A', dict(hdt, m6_joint=True)),
              ('flat', dict(name='Flat regression', dev_w=120, dev_d=80, dev_h=25, device_mount='flat', standoff=0, joint='screw')),
              ('sleeve', dict(name='Sleeve regression', dev_w=120, dev_d=100, dev_h=25, device_mount='sleeve', standoff=0, joint='screw')),
              ('two-device-pair', dict(A, ports=[], dev_off_x=-45, second=dict(B, ports=[], dev_off_x=50)))]
    results = []
    for label, spec in cases:
        try:
            source = eq.source(eq.clean(spec))
            results.append(dict(label=label, spec=spec, sha256=sha(source.encode('utf-8'))))
        except ValueError as exc:
            results.append(dict(label=label, spec=spec, error=str(exc)))
    (HERE / 'legacy-before.json').write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
    protected = [ROOT / 'HANDOFF.md']
    for folder in ['outputs/CM1000_M6_2026-10-28', 'outputs/STL_Deliveries/2026-10-16_CM1000_bracket',
                   'outputs/Hard_Drive_Tray_M6_2026-10-28', 'outputs/TL-SG108E_M6_2026-10-28']:
        protected.extend(p for p in (ROOT / folder).rglob('*') if p.is_file())
    protected += [APP / 'equipment.py', APP / 'equipment_tray.scad']
    (HERE / 'protected-before.json').write_text(json.dumps({str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in protected}, indent=2), encoding='utf-8')
    print(json.dumps({'cases':len(results), 'errors':[r for r in results if 'error' in r], 'protected_files':len(protected)}, indent=2))

if __name__ == '__main__':
    main()
