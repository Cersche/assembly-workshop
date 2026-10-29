"""Independent numeric/section acceptance of all seven Revision 2 items."""
import json
import random
import subprocess
import sys
from measure import ROOT,HERE,mesh_info,volume,section,crossing_intervals
from rail_trial import dist,simplify
REV=HERE/'revision2'
EXE='C:/Program Files/OpenSCAD/openscad.exe'

def z_intervals(sec,x):
    hits=[]
    for l in sec['loops']:
        p=l['points']
        for a,b in zip(p,p[1:]+p[:1]):
            if (a[0]<x)!=(b[0]<x):hits.append(a[1]+(x-a[0])*(b[1]-a[1])/(b[0]-a[0]))
    hits=sorted(set(round(z,5) for z in hits))
    return list(zip(hits[::2],hits[1::2]))

def gap(intervals):
    if any(a<22.225<b for a,b in intervals):return None
    lower=[b for a,b in intervals if b<22.225];upper=[a for a,b in intervals if a>22.225]
    return [max(lower),min(upper)] if lower and upper else None

def intersection(name,files,other):
    path=REV/(name+'.scad')
    body=lambda items:'union(){'+''.join('import('+json.dumps(str(f).replace('\\','/'))+');' for f in items)+'}'
    path.write_text('intersection(){'+body(files)+body(other)+'}',encoding='utf-8')
    p=subprocess.run([EXE,'-o',str(REV/(name+'.stl')),str(path)],capture_output=True,text=True,timeout=300,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    (REV/(name+'.log')).write_text(p.stdout+p.stderr,encoding='utf-8')
    return dict(empty='top level object is empty' in p.stderr.lower(),returncode=p.returncode)

def main():
    spec=json.loads((REV/'spec.json').read_text(encoding='utf-8'))
    names=['faceplate','rail_l','rail_r']+[f'pipe_{i}' for i in range(1,6)]+[f'vector_{i}' for i in range(1,10)]
    meshes={};parts={}
    for n in names:
        v,t,info=mesh_info(REV/(n+'.stl'));info['volume']=volume(v,t)
        meshes[n]=(v,t);parts[n]=info
    refs={n:mesh_info(ROOT/f'outputs/CM1000_M6_2026-10-28/CM6A_{n}.stl')[:2] for n in ['faceplate','rail_l','rail_r']}
    rng=random.Random(44)
    stations=sorted(set([4.01,5,6,7,8,9,9.5,10,11,12,13,14,15,15.9,16.1,19.9,20.1,64.68,66.9,71.99,72.01,92.3,97.39,117.7,125.123,136,137,137.5]+list(range(20,138,5))+[rng.uniform(4.01,137.6) for _ in range(20)]))
    rows=[];boundary_rows=[]
    for y in stations:
        name='faceplate' if y<16 else 'rail_l'
        sa=section(*refs[name],1,y)
        bv,bt=meshes[name]
        sb=section([[x+127,yy+4,z] for x,yy,z in bv],bt,1,y)
        def edges(sec):return [(a,b) for l in sec['loops'] for a,b in zip(l['points'],l['points'][1:]+l['points'][:1]) if a!=b]
        for src,target,label in [(sa,edges(sb),'A to B'),(sb,edges(sa),'B to A')]:
            worst_boundary=(0,None)
            for l in src['loops']:
                for p in simplify(l['points'],.005):
                    if not(20.7<=p[0]<=35.03 and 2.51<=p[1]<=41.94):continue
                    error=min(dist(p,a,b) for a,b in target)
                    if error>worst_boundary[0]:worst_boundary=error,p
            boundary_rows.append(dict(y_A=y,direction=label,error=worst_boundary[0],point=worst_boundary[1]))
        for x in [20.75,21,21.5,22.6,24,26,30,34,35,40,80,127]:
            # Direct triangle rays avoid ambiguous section graph pairing at exact loft stations.
            a=gap(crossing_intervals(*refs[name],2,[x,y,0]));b=gap(crossing_intervals(bv,bt,2,[x-127,y-4,0]))
            if a:
                rows.append(dict(side='left/centre',y=y,x=x,reference=a,candidate=b,error=max(abs(a[i]-b[i]) for i in [0,1]) if b else None,missing=b is None))
        name_r='faceplate' if y<16 else 'rail_r'
        rv,rt=meshes[name_r]
        for x in [233.25,233,232.5,231.4,230,228,224,220,219]:
            a=gap(crossing_intervals(*refs[name_r],2,[x,y,0]));b=gap(crossing_intervals(rv,rt,2,[x-127,y-4,0]))
            if a:rows.append(dict(side='right',y=y,x=x,reference=a,candidate=b,error=max(abs(a[i]-b[i]) for i in [0,1]) if b else None,missing=b is None))
    finite=[r for r in rows if r['error'] is not None]
    worst=max(finite,key=lambda r:r['error'])
    # Window boundaries at independent positions through each rail width.
    windows={}
    for side,xs in [('l',[17,18,20,22.6,26,30,34]),('r',[237,236,234,231.4,228,224,220])]:
        av,at=refs['rail_'+side];bv,bt=meshes['rail_'+side]
        bv=[[x+127,y+4,z] for x,y,z in bv]
        comparison=[]
        for x in xs:
            a=section(av,at,0,x);b=section(bv,bt,0,x)
            ae=[(u,v) for l in a['loops'] for u,v in zip(l['points'],l['points'][1:]+l['points'][:1]) if u!=v]
            be=[(u,v) for l in b['loops'] for u,v in zip(l['points'],l['points'][1:]+l['points'][:1]) if u!=v]
            for lo,hi in [(20,67),(71.9,92.4),(97.3,117.8)]:
                for bottom,top in [(2.5,17),(27.4,41.9)]:
                    worst_error=0;witness=None
                    for src,target,direction in [(a,be,'A to B'),(b,ae,'B to A')]:
                        for l in src['loops']:
                            for p in simplify(l['points'],.005):
                                if not(lo<=p[0]<=hi and bottom<=p[1]<=top):continue
                                error=min(dist(p,u,v) for u,v in target)
                                if error>worst_error:worst_error=error;witness=dict(point=p,direction=direction)
                    comparison.append(dict(x=x,y_range=[lo,hi],z_range=[bottom,top],error=worst_error,witness=witness))
        windows[side]=comparison
    probes={}
    for side,x in [('l',18),('r',236)]:
        v,t=meshes['rail_'+side]
        zints=crossing_intervals(v,t,2,[x-127,26,0])
        yints=crossing_intervals(v,t,1,[x-127,0,8.6])
        probes[side]=dict(bay_z=zints,bay_y_A=[[a+4,b+4] for a,b in yints],
                          floor=zints[0][1]-zints[0][0],top=zints[-1][1]-zints[-1][0])
        # Floor/top grid includes the previously thin rounded inner margin.
        grid=[]
        for yy in [20.001,25,30,40,50,60,64.68,66.8]:
            sec=section(v,t,1,yy-4)
            for xx in [16.768,17,18,20,22.6,26,30,34,34.9,35.02]:
                xa=xx if side=='l' else 254-xx
                ints=z_intervals(sec,xa-127)
                if ints:grid.append(dict(x_A=xa,y_A=yy,floor=ints[0][1]-ints[0][0],top=ints[-1][1]-ints[-1][0]))
        probes[side]['floor_top_grid']=grid
        probes[side]['grid_min_floor']=min(r['floor'] for r in grid)
        probes[side]['grid_min_top']=min(r['top'] for r in grid)
        holes=[]
        for z in [8.6,35.85]:
            holes.append(dict(x_A=22.6 if side=='l' else 231.4,z=z,
                              x_material=crossing_intervals(v,t,0,[-104.4 if side=='l' else 104.4,14,z]),
                              z_material=crossing_intervals(v,t,2,[-104.4 if side=='l' else 104.4,14,0])))
        probes[side]['joint_probes']=holes
    av,at=refs['rail_l'];bv,bt=meshes['rail_l']
    slots={}
    for label,v,t,x in [('reference',av,at,18),('candidate',[[x+127,y+4,z] for x,y,z in bv],bt,18)]:
        sec=section(v,t,0,x)
        choices=[l['points'] for l in sec['loops'] if min(z for yy,z in l['points'])>18 and max(z for yy,z in l['points'])<27]
        pts=max(choices,key=len)
        lo=[min(p[k] for p in pts) for k in [0,1]];hi=[max(p[k] for p in pts) for k in [0,1]]
        slots[label]=dict(bounds=[lo,hi],centre=[(a+b)/2 for a,b in zip(lo,hi)],size=[b-a for a,b in zip(lo,hi)])
    colours={}
    measured=json.loads((HERE/'sections.json').read_text(encoding='utf-8'))
    for i,n in enumerate(names[3:]):
        refn=i+4 if i<5 else [9,10,11,12,13,14,15,2,3][i-5]
        a=measured[f'colour_{refn}']['bounds'];b=parts[n]['bounds']
        b=[[p[0]+127,p[1]+4,p[2]] for p in b]
        err=max(abs(a[j][k]-b[j][k]) for j in [0,1] for k in ([0,2] if i>=5 else [0,1,2]))
        colours[n]=dict(reference_bounds=a,candidate_bounds_A=b,bounds_error=err)
    result=dict(parts=parts,retention_slot=slots,pocket=dict(stations=stations,seed=44,random_count=20,samples=rows,worst=worst,missing_count=sum(r['missing'] for r in rows),boundary_samples=boundary_rows,worst_boundary=max(boundary_rows,key=lambda r:r['error']),
                        every_shape_change_certified=False),windows=windows,bays=probes,colours=colours,
                structural_intersection=intersection('structure-intersection',[REV/'faceplate.stl'],[REV/'rail_l.stl',REV/'rail_r.stl']),
                colour_intersection=intersection('colour-intersection',[REV/'faceplate.stl'],[REV/(n+'.stl') for n in names[3:]]))
    for side in ['l','r']:
        av,at=refs['rail_'+side];a=volume(av,at);b=parts['rail_'+side]['volume']
        parts['rail_'+side].update(reference_volume=a,volume_error_percent=100*(b/a-1))
    (REV/'audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('pocket worst',worst,'missing',result['pocket']['missing_count'],flush=True)
    print('windows', {s:max(r['error'] for r in rows) for s,rows in windows.items()},flush=True)
    print('bays', {s:{k:v for k,v in p.items() if k in ('bay_z','bay_y_A','grid_min_floor','grid_min_top')} for s,p in probes.items()},flush=True)
    print('intersections',result['structural_intersection'],result['colour_intersection'],flush=True)

if __name__=='__main__':main()
