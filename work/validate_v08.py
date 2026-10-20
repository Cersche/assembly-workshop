from pathlib import Path
import sys,json,zipfile,io
sys.path.insert(0,str(Path('outputs/Mechanical_Design_App').resolve()))
from app import design_revision
import mesh_revision
parts=json.loads(Path('outputs/Mechanical_Design_App/starter-hardware.json').read_text())
selection={p['kind']:p for p in parts if p.get('part_number') in ['SSCF-M3-8-A2','94459A140']}
source,metadata=design_revision({'inputs':{'pilot':4},'selections':selection})
folder=Path('work/v08-build')
r=mesh_revision.build(source,metadata,folder)
assert len(r['assembly']['parts'])==2
assert mesh_revision.build(source,metadata,folder)['cached']
with zipfile.ZipFile(io.BytesIO(mesh_revision.bundle(r['id'],folder))) as z:
 assert z.testzip() is None
 assert z.read('pi4_proposed.scad').decode()==source
 assert json.loads(z.read('assembly.json'))['proposal_id']==r['id']
 for p in r['assembly']['parts']:
  import hashlib
  assert hashlib.sha256(z.read(p['id']+'.stl')).hexdigest()==p['source_sha256']
print('Real OpenSCAD build, closed meshes, cache and matching ZIP verified.',r['id'])
Path('work/v08-build-result.json').write_text(json.dumps({'id':r['id'],'triangles':{p['id']:len(p['triangles']) for p in r['assembly']['parts']}}))
