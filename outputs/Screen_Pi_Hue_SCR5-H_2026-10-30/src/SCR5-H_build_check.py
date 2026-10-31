"""SCR5-H reproducible build/check runner. Python 3.10 stdlib; writes only this output folder."""
import concurrent.futures as cf
import csv,hashlib,importlib.util,itertools,json,math,re,subprocess,sys,zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent.parent
ROOT=HERE.parent.parent
CHECKS=HERE/'checks'
spec=importlib.util.spec_from_file_location('g_check',HERE/'src/build_check.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
g.HERE=HERE;g.ROOT=ROOT;g.CHECKS=CHECKS
SCAD=HERE/'src/SCR5-H.scad'
PARTS=['plate','frame','floor','deck','pin1','pin2','pin3']

def build(p):
 dst=HERE/f'SCR5-H_{p}.stl'
 r=subprocess.run([str(g.EXE),'--export-format','binstl','-D',f'part="{p}"','-o',str(dst),str(SCAD)],capture_output=True,text=True,encoding='utf-8')
 (CHECKS/f'render_{p}.log').write_text(r.stdout+r.stderr,encoding='utf-8')
 if r.returncode or 'ERROR:' in r.stderr:raise RuntimeError(p+': '+r.stderr)
 repaired=g.repair_collinear(dst);m=g.mesh(dst);m['collinear_repairs']=repaired
 assert m['shells']==1 and m['bad_edges']==m['degenerate']==0 and m['volume_mm3']>0,(p,m)
 return p,m

def main():
 with cf.ThreadPoolExecutor(max_workers=3) as pool:meshes=dict(pool.map(build,PARTS))
 (CHECKS/'meshes.json').write_text(json.dumps(meshes,indent=2),encoding='utf-8')
 source=SCAD.read_text(encoding='utf-8').split('if(part=="plate")plate();')[0]
 common=CHECKS/'geometry.scad';common.write_text(source.replace('use <SCR5-H_tray.scad>',f'use <{(HERE/"src/SCR5-H_tray.scad").as_posix()}>').replace('use <SCR5-F_hp4lib.scad>',f'use <{(HERE/"src/SCR5-F_hp4lib.scad").as_posix()}>'),encoding='utf-8')
 head=f'include <{common.as_posix()}>\n'
 items={}
 for p in PARTS:
  expr=f'import("{(HERE/f"SCR5-H_{p}.stl").as_posix()}")'
  if p.startswith('pin'):expr=f'translate([{33+[45.5,35.5,25.5][int(p[-1])-1]},0,41.5])'+expr
  items[p]=expr
 items.update({p:p+'()' for p in ('glass','lcd','pcb','standoffs','buttons','dsi','touch')})
 items.update(pi_dsi='pi_dsi()',pi='h_pi()',hue='h_hue()',fan='h_fan()',leaves='leaves()',dsi_keepout='dsi_keepout()',ribbon_corridor='ribbon_route()',screw_heads='screw_heads()',screw_drivers='screw_drivers()',m6_drivers='h_joint_tools()',ribbon_path='ribbon_path()')
 items.update({f'pin_stroke{i+1}':f'pin_stroke({i})' for i in range(3)})
 boxes={}
 def render_item(item):
  name,expr=item
  dst=g.render('dummy_'+name,head+expr+';')
  return name,g.mesh(dst)['bounds']
 with cf.ThreadPoolExecutor(max_workers=3) as pool:boxes=dict(pool.map(render_item,items.items()))
 def intersect(pair):
  a,b=pair;name='intersect_'+a+'_'+b
  if any(boxes[a][k][1]<=boxes[b][k][0] or boxes[b][k][1]<=boxes[a][k][0] for k in range(3)):
   (CHECKS/(name+'.stl')).unlink(missing_ok=True)
   method='AABB separation/contact';volume=0.0
  else:
   dst=g.render(name,head+f'intersection(){{{items[a]};{items[b]};}}',True)
   volume=0.0 if dst is None or dst.stat().st_size==84 else abs(g.mesh(dst)['volume_mm3']);method='OpenSCAD CGAL'
  return dict(a=a,b=b,volume_mm3=volume,method=method)
 with cf.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(intersect,itertools.combinations(items,2)))
 (CHECKS/'pairwise_intersections.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
 with (CHECKS/'pairwise_intersections.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=['a','b','volume_mm3','method']);w.writeheader();w.writerows(rows)
 hard=[]
 keepouts=['frame','glass','lcd','pcb','standoffs','buttons','dsi','touch','leaves','dsi_keepout','screw_heads','screw_drivers','pin_stroke1','pin_stroke2','pin_stroke3']
 for row in rows:
  a,b=row['a'],row['b']
  if (a in ('floor','deck') and b in keepouts) or (b in ('floor','deck') and a in keepouts):hard.append(row)
 hard_pass=all(r['volume_mm3']<1e-5 for r in hard)
 # Finalizer checks the changed diagnostics, mesh roundtrip and strict export gate.
 sys.exit(subprocess.run([sys.executable,str(HERE/'src/SCR5-H_finalize.py')]).returncode)
if __name__=='__main__':main()
