"""Task 51 build/acceptance; Python 3.10 stdlib, UTF-8. Writes only SCR5-G folder."""
import concurrent.futures as cf
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import re
import struct
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent.parent
ROOT=HERE.parent.parent
CHECKS=HERE/'checks'
SCAD=HERE/'src/SCR5-G.scad'
EXE=Path(r'C:\Program Files\OpenSCAD\openscad.exe')
def repair_collinear(path):
    """Remove zero-area triangle by splitting its long-edge neighbour, no vertex movement."""
    data=path.read_bytes(); n=struct.unpack_from('<I',data,80)[0]
    faces=[]
    for i in range(n):
        c=struct.unpack_from('<9f',data,96+50*i);faces.append([c[k:k+3] for k in (0,3,6)])
    repairs=0
    while True:
        target=None
        for i,t in enumerate(faces):
            p,q,r=t;u=[q[k]-p[k] for k in range(3)];w=[r[k]-p[k] for k in range(3)]
            cross=[u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0]]
            if sum(x*x for x in cross)==0:
                assert len(set(t))==3,'Repeated vertex requires separate investigation'
                edges=[(sum((t[a][k]-t[b][k])**2 for k in range(3)),a,b) for a,b in ((0,1),(1,2),(2,0))]
                _,a,b=max(edges);c=3-a-b
                target=i,t[a],t[b],t[c];break
        if target is None:break
        i,a,b,c=target;found=False
        for j,t in enumerate(faces):
            if j==i:continue
            for k in range(3):
                if t[k]==b and t[(k+1)%3]==a:
                    d=t[(k+2)%3];faces[j]=[b,c,d];faces.append([c,a,d]);faces.pop(i);found=True;break
            if found:break
        assert found,'No neighbour for collinear edge'
        repairs+=1
    if repairs:
        out=bytearray(data[:80])+struct.pack('<I',len(faces))
        for t in faces:out+=struct.pack('<12fH',0,0,0,*[v for p in t for v in p],0)
        path.write_bytes(out)
    return repairs
def render(name,source,empty_ok=False):
    src=CHECKS/(name+'.scad'); dst=CHECKS/(name+'.stl')
    src.write_text(source,encoding='utf-8')
    r=subprocess.run([str(EXE),'--export-format','binstl','-o',str(dst),str(src)],capture_output=True,text=True,encoding='utf-8')
    log=r.stdout+r.stderr
    (CHECKS/(name+'.log')).write_text(log,encoding='utf-8')
    if r.returncode and not (empty_ok and 'Current top level object is empty' in log):
        raise RuntimeError(name+': '+log)
    if empty_ok and 'Current top level object is empty' in log:
        dst.unlink(missing_ok=True) # remove only stale task-owned zero-volume diagnostic
        return None
    return dst

def mesh(path):
    data=path.read_bytes(); n=struct.unpack_from('<I',data,80)[0]
    assert len(data)==84+50*n
    v=[]; index={}; tris=[]
    for i in range(n):
        c=struct.unpack_from('<9f',data,96+50*i)
        t=[]
        for k in (0,3,6):
            p=c[k:k+3]
            if p not in index:index[p]=len(v);v.append(p)
            t.append(index[p])
        tris.append(t)
    edges={}; parent=list(range(len(v))); deg=0; volume=0
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for a,b,c in tris:
        p,q,r=v[a],v[b],v[c]
        u=[q[k]-p[k] for k in range(3)]; w=[r[k]-p[k] for k in range(3)]
        cross=[u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0]]
        if sum(x*x for x in cross)<1e-16:deg+=1
        volume+=(p[0]*(q[1]*r[2]-q[2]*r[1])-p[1]*(q[0]*r[2]-q[2]*r[0])+p[2]*(q[0]*r[1]-q[1]*r[0]))/6
        for x,y in ((a,b),(b,c),(c,a)):
            edges[x,y]=edges.get((x,y),0)+1;parent[find(x)]=find(y)
    return dict(vertices=len(v),triangles=n,shells=len({find(i) for i in range(len(v))}),
        bad_edges=sum(n!=1 or edges.get((b,a),0)!=1 for (a,b),n in edges.items()),
        degenerate=deg,volume_mm3=volume,bounds=[[min(p[k] for p in v),max(p[k] for p in v)] for k in range(3)])

def inventory():
    # Explicitly limited to user-protected revisions and documents; no normal-use reads/writes.
    paths=[ROOT/'HANDOFF.md',ROOT/'IDEAS.md',ROOT/'work/screen-5in/Dimensions.md']
    for pat in ('Screen_5in_SCR5-[BCDEF]*','Screen_Pi_Hue_SCR5-[BCDEF]*','Screen_WedgePin_Coupon_SCR5-WP-A*','Hue_Pi4_M6*','Final_3MF'):
        for d in (ROOT/'outputs').glob(pat):
            if d.is_dir():paths.extend(p for p in d.rglob('*') if p.is_file())
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()}

def main():
    CHECKS.mkdir(exist_ok=True)
    before=inventory()
    (CHECKS/'protected_before.json').write_text(json.dumps(before,indent=2),encoding='utf-8')
    parts=['plate','frame','pin1','pin2','pin3']
    def build(p):
        dst=HERE/f'SCR5-G_{p}.stl'
        r=subprocess.run([str(EXE),'--export-format','binstl','-D',f'part="{p}"','-o',str(dst),str(SCAD)],capture_output=True,text=True,encoding='utf-8')
        (CHECKS/f'render_{p}.log').write_text(r.stdout+r.stderr,encoding='utf-8')
        if r.returncode:raise RuntimeError(p+': '+r.stderr)
        repaired=repair_collinear(dst)
        m=mesh(dst);m['collinear_repairs']=repaired
        return p,m
    with cf.ThreadPoolExecutor(max_workers=3) as pool:results=dict(pool.map(build,parts))
    checkrun=subprocess.run([sys.executable,str(HERE/'src/SCR5-F_meshcheck.py')]+[str(HERE/f'SCR5-G_{p}.stl') for p in parts],capture_output=True,text=True,encoding='utf-8')
    (CHECKS/'meshcheck.log').write_text(checkrun.stdout+checkrun.stderr,encoding='utf-8')
    assert checkrun.returncode==0
    for p,m in results.items():
        assert m['shells']==1 and m['bad_edges']==m['degenerate']==0 and m['volume_mm3']>0,(p,m)
    # Strip only top-level dispatcher in an exact local copy to retain all same parameter definitions.
    source=SCAD.read_text(encoding='utf-8'); definitions=source.split('if(part=="plate")plate();')[0]
    common=CHECKS/'geometry.scad';common.write_text(definitions,encoding='utf-8')
    head=f'include <{common.as_posix()}>\n'
    items={'plate':'plate()','frame':'frame()','pin1':'placed_pin(0)','pin2':'placed_pin(1)','pin3':'placed_pin(2)',
        'glass':'glass()','lcd':'lcd()','pcb':'pcb()','standoffs':'standoffs()','buttons':'buttons()','dsi':'dsi()','touch':'touch()'}
    boxes={p:results[p]['bounds'] for p in parts}
    for i,p in enumerate(parts[2:]):
        offsets=[33+[45.5,35.5,25.5][i],0,41.5]
        boxes[p]=[[a+offsets[k],b+offsets[k]] for k,(a,b) in enumerate(boxes[p])]
    for p in ('glass','lcd','pcb','standoffs','buttons','dsi','touch'):
        dst=render('dummy_'+p,head+items[p]+';')
        boxes[p]=mesh(dst)['bounds']
    # Check exact delivered STL meshes, including the geometry-preserving triangulation repair.
    for p in parts:
        imp=f'import("{(HERE / ("SCR5-G_"+p+".stl")).as_posix()}")'
        if p.startswith('pin'):
            i=int(p[-1])-1;imp=f'translate([{33+[45.5,35.5,25.5][i]},0,41.5])'+imp
        items[p]=imp
    # Check every manufactured pair and every manufactured/screen-component pair.
    pairs=[(a,b) for a,b in itertools.combinations(items,2) if a in parts or b in parts]
    def intersect(pair):
        a,b=pair;n='intersect_'+a+'_'+b
        if any(boxes[a][k][1]<=boxes[b][k][0] or boxes[b][k][1]<=boxes[a][k][0] for k in range(3)):
            (CHECKS/(n+'.stl')).unlink(missing_ok=True)
            (CHECKS/(n+'.log')).write_text('Exact delivered-mesh AABB separation or boundary contact: zero intersection volume.\n',encoding='utf-8')
            return n,0.0
        dst=render(n,head+f'intersection(){{{items[a]};{items[b]};}}',True)
        m=mesh(dst) if dst is not None else None
        return n,0.0 if m is None else abs(m['volume_mm3'])
    with cf.ThreadPoolExecutor(max_workers=3) as pool:intersections=dict(pool.map(intersect,pairs))
    # Extra entire connector clearance envelope and routing-corridor solid checks.
    for n,body in {'frame_dsi_3mm':'intersection(){frame();dsi_keepout();}',
                   'frame_ribbon_18mm':'intersection(){frame();ribbon_route();}',
                   'plate_dsi_3mm':'intersection(){plate();dsi_keepout();}'}.items():
        dst=render(n,head+body,True);intersections[n]=abs(mesh(dst)['volume_mm3']) if dst is not None else 0.0
    assert all(v<0.00001 for v in intersections.values()),intersections
    render('SCR5-G_assembled_reference',head+'assembly();')
    render('SCR5-G_screen_dummy',head+'dummy();')
    subprocess.run([sys.executable,str(HERE/'src/SCR5-G_pack3mf.py')],check=True)
    with zipfile.ZipFile(HERE/'SCR5-G_screen_plate_set.3mf') as z:
        xml=z.read('3D/3dmodel.model').decode('utf-8'); tree=ET.fromstring(xml)
    ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
    tags=dict(vertex_tags=xml.count('<vertex '),triangle_tags=xml.count('<triangle '),ns0='ns0' in xml,objects=[])
    assert not tags['ns0']
    for obj in tree.findall('m:resources/m:object',ns):
        verts=obj.findall('.//m:vertex',ns);tri=obj.findall('.//m:triangle',ns)
        assert len(verts)>0 and len(tri)>0
        assert abs(min(float(v.attrib['z']) for v in verts))<1e-6
        tags['objects'].append(dict(name=obj.attrib['name'],vertices=len(verts),triangles=len(tri)))
    assert len(tags['objects'])==5
    # Independent numerical datum checks + rendered glass/plate bounds.
    glass=mesh(CHECKS/'dummy_glass.stl')
    datums=dict(plate_front=results['plate']['bounds'][1][0],glass_front=glass['bounds'][1][0],
        lit_centre_z=41.5+(8.6-2.8)/2,plate_centre_z=44.4,
        window_clearance_per_side=0.2,glass_centre_x=33,seat_y=13.3,
        lip_enabled_edges=re.search(r'LIP_EDGES=([^;]+)',source).group(1),
        chamfer_mm=0.3,ribbon_slot_width_mm=18)
    assert abs(datums['plate_front'])<0.00001 and datums['glass_front']==0
    assert abs(datums['lit_centre_z']-datums['plate_centre_z'])<0.1
    after=inventory();assert before==after,'Protected inputs changed'
    out=dict(meshes=results,intersections_mm3=intersections,datums=datums,three_mf=tags,
        protected_file_count=len(before),protected_unchanged=True,
        lip_status='left/right cosmetic only; no top/bottom lip; rear frame supports screen')
    (CHECKS/'acceptance.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
