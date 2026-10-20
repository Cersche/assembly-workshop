"""Finish the recovered UI text and verify protected data/assets are unchanged."""
from pathlib import Path
import hashlib
import json

root=Path(__file__).resolve().parents[2]
app=root/'outputs/Mechanical_Design_App'
p=app/'workspace.js'
s=p.read_text(encoding='utf-8').replace('Slot 1 starts at the bottom.','Slot 1 starts at the top.')
p.write_text(s,encoding='utf-8')
before=json.loads((Path(__file__).parent/'Data_Before.json').read_text(encoding='utf-8'))
data=root/'data/normal-use'
now={str(p.relative_to(data)):hashlib.sha256(p.read_bytes()).hexdigest() for p in data.rglob('*') if p.is_file()}
assert now==before,'User data changed during repair; inspect before proceeding.'
print('PASS all',len(before),'normal-use data file hashes unchanged.')
