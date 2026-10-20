from pathlib import Path
import hashlib,json
r=Path.cwd();f=r/'work/gui-refinement'
manifest={str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (r/'data/normal-use').rglob('*') if p.is_file()}
(f/'After_Authorized_Draft_Save.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(f/'Authorized_Rack_Draft.json').write_bytes((r/'data/normal-use/rack-workspace.json').read_bytes())
