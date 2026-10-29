"""STL section evidence and final digital assertions. No rendering or user-data access."""
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(ROOT/'outputs/Mechanical_Design_App'))
from measure_reference import mesh_info,crossing_intervals
import m6_rails
import equipment as eq

def section(vs,ts,y):
    segments=[]
    for t in ts:
        tri=[vs[i] for i in t]
        pts=[]
        for a,b in zip(tri,tri[1:]+tri[:1]):
            if (a[1]<y<b[1]) or (b[1]<y<a[1]):
                q=(y-a[1])/(b[1]-a[1])
                pts.append([a[0]+q*(b[0]-a[0]),a[2]+q*(b[2]-a[2])])
        if len(pts)==2:segments.append(pts)
    return segments

def pilot_min_wall(vs,ts,y,centres):
    segs=section(vs,ts,y)
    holes=[]
    for c in centres:
        # Subdivided triangle-plane segments lie within the 48-sided bore polygon.
        hs=[s for s in segs if all(3.78<math.dist(p,c)<3.81 for p in s)]
        if not hs:raise ValueError('No pilot section found')
        holes.extend(hs)
    outer=[s for s in segs if s not in holes]
    return min(min([m6_rails.distance(p,*b) for p in a]+[m6_rails.distance(p,*a) for p in b]) for a in holes for b in outer)

results={}
paths={
 'CM6A':dict(faceplate=ROOT/'outputs/CM1000_M6_2026-10-28/CM6A_faceplate.stl',
             rail_l=ROOT/'outputs/CM1000_M6_2026-10-28/CM6A_rail_l.stl',rail_r=ROOT/'outputs/CM1000_M6_2026-10-28/CM6A_rail_r.stl'),
 'CM6B':dict(faceplate=ROOT/'outputs/CM1000_M6_generated_2026-10-28/CM6B_faceplate_with_stubs.stl',
             rail_l=ROOT/'outputs/CM1000_M6_generated_2026-10-28/CM6B_rail_left.stl',rail_r=ROOT/'outputs/CM1000_M6_generated_2026-10-28/CM6B_rail_right.stl')}
for label,parts in paths.items():
    a=label=='CM6A'
    ox=127 if a else 0
    centres=[[ox+x,z] for x in [-104.4,104.4] for z in [8.6,35.85]]
    result={}
    for name,path in parts.items():
        vs,ts,info=mesh_info(path)
        info['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        if name=='faceplate':
            y=12 if a else 8
            info['pilot_section_y']=y
            info['min_pilot_wall_in_section_mm']=pilot_min_wall(vs,ts,y,centres)
            info['pilot_diameter_sections']=[crossing_intervals(vs,ts,2,[ox-104.4,y,0]),crossing_intervals(vs,ts,0,[0,y,8.6])]
            info['blind_end_y']=crossing_intervals(vs,ts,1,[ox-104.4,0,8.6])
            info['plate_thickness_ray']=crossing_intervals(vs,ts,1,[ox-60,0,10])
            # Exactly two disconnected gaps on each of the two rack-slot rows; no centre row gap.
            rows=[6.323,38.127] if not a else [6.325,38.125]
            info['rack_slot_rows']={str(z):crossing_intervals(vs,ts,0,[0,1.5 if a else -2,z]) for z in rows}
            info['rack_slot_midrow']=crossing_intervals(vs,ts,0,[0,1.5 if a else -2,22.225])
        else:
            x=18 if a else -109
            if name=='rail_r':x=254-x if a else -x
            info['bay_outerwall_x']=x
            info['bay_height_section']=crossing_intervals(vs,ts,2,[x,30,0])
            info['bay_depth_section']=crossing_intervals(vs,ts,1,[x,0,8.6])
            cx=(22.6 if name=='rail_l' else 231.4) if a else (-104.4 if name=='rail_l' else 104.4)
            info['clearance_section']=crossing_intervals(vs,ts,0,[0,18 if a else 14,8.6])
            info['floor_top_non_bay']=crossing_intervals(vs,ts,2,[cx,80,0])
        if not a:
            # Glyph floor triangles at exact 0.5 mm below the nominal top (STL coordinate precision).
            glyph=[vs[i] for tri in ts if all(abs(vs[j][2]-43.925)<.0001 for j in tri) for i in tri]
            info['id_depth_mm']=round(44.425-min(p[2] for p in glyph),6) if glyph else None
            info['id_floor_vertices']=len(glyph)
        result[name]=info
    results[label]=result
spec=json.loads((HERE/'cm6b-spec.json').read_text(encoding='utf-8'))
current=eq.source(eq.clean(spec)).encode('utf-8')
stored=(ROOT/'outputs/CM1000_M6_generated_2026-10-28/CM6B_source.scad').read_bytes()
checks=dict(source_matches=hashlib.sha256(current).hexdigest()==hashlib.sha256(stored).hexdigest(),
            closed_single_parts=all(p['closed'] and p['components']==1 for p in results['CM6B'].values()),
            all_ids_half_mm=all(abs(p['id_depth_mm']-.5)<.0001 for p in results['CM6B'].values()),
            min_pilot_wall_at_least_2=results['CM6B']['faceplate']['min_pilot_wall_in_section_mm']>=2-1e-5,
            empty_intersection=json.loads((HERE/'cm6b-measurements.json').read_text(encoding='utf-8'))['intersection']['empty'])
results['checks']=checks
(HERE/'acceptance-measurements.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(checks,indent=2))
for label in ['CM6A','CM6B']:
    print(label,'min section pilot wall',results[label]['faceplate']['min_pilot_wall_in_section_mm'])
    for name in ['rail_l','rail_r']:
        print(name,'bay Z',results[label][name]['bay_height_section'],'bay Y',results[label][name]['bay_depth_section'])
if not all(checks.values()):raise SystemExit(1)
