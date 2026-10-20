from pathlib import Path
p=Path('work/phase7-digital/accept.py')
s=p.read_text(encoding='utf-8').replace("data=root/'work/phase7-digital/acceptance-data'","from uuid import uuid4\ndata=root/'work/phase7-digital'/('acceptance-data-'+uuid4().hex[:8])")
s=s.replace("assert all(store.import_parts(p['records'])==0 for p in packs)","before_import=store.parts()\nfor pack in packs:store.import_parts(pack['records'])\nassert store.parts()==before_import and store.project()==saved")
p.write_text(s,encoding='utf-8')
