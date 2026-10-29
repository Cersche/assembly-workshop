from pathlib import Path
import sys,json,hashlib,zipfile,importlib.util
r=Path.cwd();w=r/'work/cm6b-46';sys.path[:0]=[str(r/'tools'),str(r/'outputs/Mechanical_Design_App')]
from mesh_viewer import read_stl
import print_layout as new
zipfile.time.localtime=lambda *args:(2026,10,28,12,0,0,2,301,-1)
spec=importlib.util.spec_from_file_location('oldpacker',w/'before-print_layout.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
result={}
def triangles(p):
 v,t=read_stl(p);return sorted(tuple(sorted(v[i] for i in q)) for q in t)
for label in ['HDT-M6-A','flat']:
 before=w/'before';after=w/'after';parts={p:(before/(label+'-'+p+'.stl')).read_text(encoding='utf-8') for p in ['faceplate','tray']}
 old3=old.layout_3mf(parts);new3=new.layout_3mf(parts);oldstl=old.layout(parts);newstl=new.layout(parts)
 assert old3==new3 and oldstl==newstl
 for stage,m in [('old',old),('new',new)]:
  (w/(label+'-'+stage+'.3mf')).write_bytes(m.layout_3mf(parts));(w/(label+'-'+stage+'-layout.stl')).write_text(m.layout(parts),encoding='utf-8')
 same={p:triangles(before/(label+'-'+p+'.stl'))==triangles(after/(label+'-'+p+'.stl')) for p in ['faceplate','tray']};assert all(same.values()),same
 result[label]=dict(same_input_3mf_byte_identical=True,same_input_layout_stl_byte_identical=True,source_byte_identical=(before/(label+'.scad')).read_bytes()==(after/(label+'.scad')).read_bytes(),fresh_render_triangle_identical=same,fresh_raw_STL_bytes_equal={p:(before/(label+'-'+p+'.stl')).read_bytes()==(after/(label+'-'+p+'.stl')).read_bytes() for p in ['faceplate','tray']},packer_output_sha256=dict(model3mf=hashlib.sha256(old3).hexdigest(),layout_stl=hashlib.sha256(oldstl.encode('utf-8')).hexdigest()))
result['HDT_triangle_identical']={p:triangles(w/'after'/('HDT-M6-A-'+p+'.stl'))==triangles(r/'work/m6-fidelity-44/revision2/hdt-regression'/('reference-without-id-'+p+'.stl')) for p in ['faceplate','tray']};assert all(result['HDT_triangle_identical'].values())
result['ZIP_clock']='Fixed 2026-10-28 12:00:00 for both packers; ZIP timestamps otherwise encode run time.'
(w/'regression-proof.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
