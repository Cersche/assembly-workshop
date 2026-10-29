"""Preservation proof using normalized paths; generated delivery intentionally replaceable."""
import json
import hashlib
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'outputs/Mechanical_Design_App'))
import equipment as eq
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for c in json.loads((ROOT/'work/m6-rails-43/legacy-before.json').read_text(encoding='utf-8')):
    h=hashlib.sha256(eq.source(eq.clean(c['spec'])).encode('utf-8')).hexdigest()
    hf=hashlib.sha256(eq.source(eq.clean(dict(c['spec'],m6_rails=False))).encode('utf-8')).hexdigest()
    rows.append(dict(label=c['label'],before=c['sha256'],after=h,explicit_false=hf,identical=h==hf==c['sha256']))
files=[]
for n,h in json.loads((HERE/'starting-hashes.json').read_text(encoding='utf-8')).items():
    n=n.replace('\\','/')
    if n in ('outputs/Mechanical_Design_App/equipment.py','outputs/Mechanical_Design_App/equipment_tray.scad') or n.startswith('outputs/CM1000_M6_generated_2026-10-28/'):continue
    after=sha(ROOT/n)
    files.append(dict(path=n,before=h,after=after,identical=h==after))
result=dict(source_cases=rows,protected_files=files,all_14_identical=len(rows)==14 and all(r['identical'] for r in rows),protected_identical=all(r['identical'] for r in files))
(HERE/'revision2/preservation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('legacy',result['all_14_identical'],'protected',result['protected_identical'],len(files))
if not result['all_14_identical'] or not result['protected_identical']:raise SystemExit(1)
