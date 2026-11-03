"""SCR5-H9: recheck the ribbon, export reference dummies for the viewer, pack the 3MF. Stdlib + OpenSCAD."""
import importlib.util,json,re,struct,subprocess,zipfile
from pathlib import Path
HERE=Path(__file__).resolve().parent.parent;C=HERE/'checks'
sp=importlib.util.spec_from_file_location('g',HERE/'src/build_check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
g.HERE=HERE;g.CHECKS=C
src=(HERE/'src/SCR5-H.scad').read_text(encoding='utf-8').split('if(part=="plate")plate();')[0]
src=src.replace('use <SCR5-H_tray.scad>',f'use <{(HERE/"src/SCR5-H_tray.scad").as_posix()}>').replace('use <SCR5-F_hp4lib.scad>',f'use <{(HERE/"src/SCR5-F_hp4lib.scad").as_posix()}>')
(C/'geometry.scad').write_text(src,encoding='utf-8')
head=f'include <{(C/"geometry.scad").as_posix()}>\n'
imp=lambda n:f'import("{(HERE/n).as_posix()}")'
rows=json.loads((C/'pairwise.json').read_text(encoding='utf-8'))
for r in rows:
 if r['b']=='ribbon':
  d=g.render(f'x_{r["a"]}_ribbon',head+f'intersection(){{{imp("SCR5-H9_"+r["a"]+".stl")};ribbon_path();}}',True)
  r['volume_mm3']=0.0 if d is None or d.stat().st_size==84 else round(abs(g.mesh(d)['volume_mm3']),3)
  print(r)
(C/'pairwise.json').write_text(json.dumps(rows,indent=1),encoding='utf-8')
for n,e in dict(pi='h_pi()',hue='h_hue()',fan='h_fan()',screen='dummy()').items():
 g.render('ref_'+n,head+e+';')
def read(p):
 d=p.read_bytes();n=struct.unpack_from('<I',d,80)[0];V={};T=[]
 for i in range(n):
  c=struct.unpack_from('<9f',d,96+50*i);T.append([V.setdefault(c[k:k+3],len(V)) for k in (0,3,6)])
 return list(V),T
ROT={'down_front':lambda x,y,z:(x,-z,y),'down_rear':lambda x,y,z:(x,z,-y),'upright':lambda x,y,z:(x,y,z),'side':lambda x,y,z:(z,y,-x)}
PARTS=[("SCR5-H9 plate","SCR5-H9_plate.stl","down_front"),("SCR5-H8 frame (unchanged)","SCR5-H8_frame.stl","down_rear"),("SCR5-H9 floor","SCR5-H9_floor.stl","upright"),("SCR5-H9 deck","SCR5-H9_deck.stl","upright")]+[(f"SCR5-H8 pin{i} DROP0.45",f"SCR5-H8_pin{i}.stl","side") for i in (1,2,3)]
objs=[];xcur=0
for name,f,rot in PARTS:
 V,T=read(HERE/f);V=[ROT[rot](*v) for v in V]
 mn=[min(v[k] for v in V) for k in range(3)];mx=max(v[0] for v in V)
 dx=xcur-mn[0];V=[(v[0]+dx,v[1]-mn[1],v[2]-mn[2]) for v in V];xcur+=mx-mn[0]+12
 objs.append((name,V,T))
out=['<?xml version="1.0" encoding="UTF-8"?>','<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">','<resources>']
for i,(name,V,T) in enumerate(objs,1):
 out.append(f'<object id="{i}" name="{name}" type="model"><mesh><vertices>')
 out+=[f'<vertex x="{x:.6f}" y="{y:.6f}" z="{z:.6f}"/>' for x,y,z in V]
 out.append('</vertices><triangles>')
 out+=[f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a,b,c in T]
 out.append('</triangles></mesh></object>')
out.append('</resources><build>'+''.join(f'<item objectid="{i}"/>' for i in range(1,len(objs)+1))+'</build></model>')
dst=HERE/'SCR5-H9_screen_pi_hue_set.3mf'
with zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('[Content_Types].xml','<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
 z.writestr('_rels/.rels','<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
 z.writestr('3D/3dmodel.model','\n'.join(out))
m=zipfile.ZipFile(dst).read('3D/3dmodel.model').decode()
print(dst.name,'vertex',m.count('<vertex '),'triangle',m.count('<triangle '),'objects',m.count('<object '),'ns0' in m and 'HAS ns0' or 'no ns0')
