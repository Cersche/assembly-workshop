"""Reconstruct the selected GUI in staging from its preserved sources; no data access."""
from pathlib import Path
import hashlib
import json
import os
import runpy
import shutil

root=Path(__file__).resolve().parents[2]
repair=root/'work/gui-render-repair'
repair.mkdir(exist_ok=True)
app=root/'outputs/Mechanical_Design_App'
before=repair/'before-app'
before.mkdir(exist_ok=True)
for name in ['index.html','workspace.js','workspace.css','app.py','viewer.js']:
    if not (before/name).exists(): shutil.copy2(app/name,before/name)
data=root/'data/normal-use'
hashes={str(p.relative_to(data)):hashlib.sha256(p.read_bytes()).hexdigest() for p in data.rglob('*') if p.is_file()}
(repair/'Data_Before.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
stage=repair/'stage'
target=stage/'outputs/Mechanical_Design_App'
target.mkdir(parents=True,exist_ok=True)
resources=stage/'work/gui-refinement'
resources.mkdir(parents=True,exist_ok=True)
for name in ['workspace.js','index.html','viewer.js']:
    shutil.copy2(root/'work/gui-refinement/before-app'/name,target/name)
for name in ['save_controller.txt','inspector_controller.txt']:
    shutil.copy2(root/'work/gui-refinement'/name,resources/name)
os.chdir(stage)
for script in ['refine.py','one_save_button.py','compact_slots.py','fix_event.py','appearance_startup.py','asset_version.py']:
    runpy.run_path(str(root/'work/gui-refinement'/script),run_name='__main__')
os.chdir(root)
expected=json.loads((root/'work/gui-refinement/After_State_Manifest.json').read_text(encoding='utf-8'))
for name in ['workspace.js','index.html','viewer.js']:
    current=hashlib.sha256((target/name).read_bytes()).hexdigest()
    previous=next(e['sha256'] for e in expected if e['path'].endswith('\\'+name))
    print(name,len((target/name).read_bytes()),'matches recorded final:',current==previous)
