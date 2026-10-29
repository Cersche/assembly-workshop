"""Task 46 explicit disposable no-colour before/after regression renders."""
import sys,json,subprocess,importlib.util,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];W=Path(__file__).resolve().parent
sys.path[:0]=[str(R/'outputs/Mechanical_Design_App'),str(R/'tools')]
import zipfile
zipfile.time.localtime=lambda *args:(2026,10,28,12,0,0,2,301,-1)
import equipment as eq
from mesh_viewer import read_stl
stage=sys.argv[1];folder=W/stage;folder.mkdir(exist_ok=True)
specs=json.loads((R/'work/m6-rails-43/legacy-before.json').read_text(encoding='utf-8'))
mod=importlib.util.spec_from_file_location('packer',W/'before-print_layout.py' if stage=='before' else R/'outputs/Mechanical_Design_App/print_layout.py');packer=importlib.util.module_from_spec(mod);mod.loader.exec_module(packer)
result={}
for label in ['HDT-M6-A','flat']:
 spec=next(c['spec'] for c in specs if c['label']==label);src=eq.source(eq.clean(spec));scad=folder/(label+'.scad');scad.write_text(src,encoding='utf-8',newline='\n');parts={}
 for part in ['faceplate','tray']:
  target=folder/(label+'-'+part+'.stl')
  p=subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','--export-format','asciistl','-o',str(target),'-D',f'part="{part}"',str(scad)],capture_output=True,text=True,encoding='utf-8',timeout=600,creationflags=subprocess.CREATE_NO_WINDOW)
  (folder/(label+'-'+part+'.log')).write_text(p.stdout+p.stderr,encoding='utf-8');assert p.returncode==0,p.stderr
  parts[part]=target.read_text(encoding='utf-8');print(stage,label,part,flush=True)
 blob=packer.layout_3mf(parts);(folder/(label+'.3mf')).write_bytes(blob)
 (folder/(label+'-layout.stl')).write_text(packer.layout(parts),encoding='utf-8')
 result[label]={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob(label+'*') if p.suffix in ('.stl','.3mf','.scad')}
(W/(stage+'-regression.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
