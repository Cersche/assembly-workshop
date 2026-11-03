"""SCR5-H11 build and checks: renders plate, floor, deck; frame and pins are H8's, unchanged. Stdlib + OpenSCAD."""
import concurrent.futures as cf,importlib.util,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent.parent;C=HERE/'checks';C.mkdir(exist_ok=True)
sp=importlib.util.spec_from_file_location('g',HERE/'src/build_check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
g.HERE=HERE;g.CHECKS=C
SCAD=HERE/'src/SCR5-H.scad'
def build(p):
 dst=HERE/f'SCR5-H11_{p}.stl'
 r=subprocess.run([str(g.EXE),'--export-format','binstl','-D',f'part="{p}"','-o',str(dst),str(SCAD)],capture_output=True,text=True,encoding='utf-8')
 (C/f'render_{p}.log').write_text(r.stdout+r.stderr,encoding='utf-8')
 if r.returncode or 'ERROR:' in r.stderr:raise RuntimeError(p+': '+r.stderr[-800:])
 fixed=g.repair_collinear(dst);m=g.mesh(dst);m['collinear_repairs']=fixed
 return p,m
with cf.ThreadPoolExecutor(3) as x:meshes=dict(x.map(build,['plate','floor','deck','fanmount']))
meshes['frame']=g.mesh(HERE/'SCR5-H8_frame.stl')
(C/'meshes.json').write_text(json.dumps(meshes,indent=1),encoding='utf-8')
for k,m in meshes.items():print(k,{q:m[q] for q in ('shells','bad_edges','degenerate','volume_mm3','bounds')},flush=True)
src=SCAD.read_text(encoding='utf-8').split('if(part=="plate")plate();')[0]
src=src.replace('use <SCR5-H_tray.scad>',f'use <{(HERE/"src/SCR5-H_tray.scad").as_posix()}>').replace('use <SCR5-F_hp4lib.scad>',f'use <{(HERE/"src/SCR5-F_hp4lib.scad").as_posix()}>')
(C/'geometry.scad').write_text(src,encoding='utf-8')
head=f'include <{(C/"geometry.scad").as_posix()}>\n'
imp=lambda n:f'import("{(HERE/n).as_posix()}")'
P=dict(plate=imp('SCR5-H11_plate.stl'),floor=imp('SCR5-H11_floor.stl'),deck=imp('SCR5-H11_deck.stl'),frame=imp('SCR5-H8_frame.stl'),fanmount=imp('SCR5-H11_fanmount.stl'),
 pi='h_pi()',hue='h_hue()',fan='h_fan()',ribbon='ribbon_path()',heads='screw_heads()',dummy='dummy()',m6='h_joint_tools()',ks='ks_path()',post='translate([0,4,0])import("'+(HERE.parent.parent/'work/rack-post-hex/assembled/post_left.stl').as_posix()+'")')
PAIRS=[('floor','plate'),('deck','plate'),('floor','deck'),('floor','frame'),('deck','frame'),('plate','frame'),('floor','pi'),('deck','pi'),('plate','pi'),('floor','hue'),('deck','hue'),('floor','fan'),('deck','fan'),('plate','fan'),('pi','fan'),('floor','ribbon'),('deck','ribbon'),('plate','ribbon'),('floor','dummy'),('deck','dummy'),('floor','heads'),('deck','heads'),('deck','m6'),('hue','m6'),('plate','ks'),('floor','ks'),('deck','ks'),('plate','post'),('floor','post'),('deck','post'),('fan','post'),('fanmount','floor'),('fanmount','deck'),('fanmount','plate'),('fanmount','fan'),('fanmount','pi'),('fanmount','hue'),('fanmount','post')]
def inter(ab):
 a,b=ab;d=g.render(f'x_{a}_{b}',head+f'intersection(){{{P[a]};{P[b]};}}',True)
 v=0.0 if d is None or d.stat().st_size==84 else abs(g.mesh(d)['volume_mm3'])
 return dict(a=a,b=b,volume_mm3=round(v,3))
with cf.ThreadPoolExecutor(3) as x:rows=list(x.map(inter,PAIRS))
(C/'pairwise.json').write_text(json.dumps(rows,indent=1),encoding='utf-8')
for r in rows:print(r,flush=True)
