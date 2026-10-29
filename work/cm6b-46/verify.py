"""Task 46 reproducible acceptance checks on new disposable evidence."""
from pathlib import Path
import sys,json,hashlib,zipfile,io,xml.etree.ElementTree as E,importlib.util
R=Path(__file__).resolve().parents[2];W=Path(__file__).resolve().parent
sys.path[:0]=[str(R/'outputs/Mechanical_Design_App'),str(R/'work/m6-rails-43'),str(R/'tools')]
import equipment as eq,print_layout as pl
from measure_reference import mesh_info,crossing_intervals
from mesh_viewer import read_stl
N={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data): (W/name).write_text(json.dumps(data,indent=2),encoding='utf-8')
def tree(blob,parts):
 with zipfile.ZipFile(io.BytesIO(blob)) as z:r=E.fromstring(z.read('3D/3dmodel.model'));entries=z.namelist()
 assert entries==['[Content_Types].xml','_rels/.rels','3D/3dmodel.model']
 assert r.attrib['unit']=='millimeter'
 obs={o.attrib['id']:o for o in r.findall('m:resources/m:object',N)};build=r.findall('m:build/m:item',N);assert len(build)==3
 expected=dict(pl.place(parts));parity=[];parents=[];materials=[]
 for b in build:
  o=obs[b.attrib['objectid']];children=o.findall('m:components/m:component',N);assert children
  parents.append(dict(id=o.attrib['id'],name=o.attrib['name'],parts=[obs[c.attrib['objectid']].attrib['name'] for c in children]))
  for c in children:
   assert 'transform' not in c.attrib
   p=obs[c.attrib['objectid']];name=p.attrib['name'];vs=[tuple(float(v.attrib[k]) for k in ('x','y','z')) for v in p.findall('m:mesh/m:vertices/m:vertex',N)]
   actual=sorted(tuple(sorted(vs[int(t.attrib[k])] for k in ('v1','v2','v3'))) for t in p.findall('m:mesh/m:triangles/m:triangle',N))
   exp=sorted(tuple(sorted(tuple(round(x,6) for x in v) for v in t)) for t in expected[name]);assert actual==exp,name
   parity.append(dict(part=name,triangles=len(actual),positions_equal_to_6dp=True))
   if name.startswith(('pipe_','vector_')):materials.append((p.attrib['pid'],p.attrib['pindex']))
 assert len(parents[0]['parts'])==15 and len(parents[1]['parts'])==len(parents[2]['parts'])==1
 assert len(materials)==len(set(materials))==14
 assert len(r.findall('m:resources/m:basematerials/m:base',N))==15
 return dict(build_items=3,unit='millimeter',object_tree=parents,colour_parts=14,independent_colour_properties=14,mesh_parity=parity,position_error_max_mm=.0000005)
def heights(v,t,x,ys):return [crossing_intervals(v,t,2,[x,y,0])[-1][1] for y in ys]
def main():
 result={};parts={n:(W/(n+'.stl')).read_text(encoding='utf-8') for n in ['faceplate','rail_l','rail_r']+[f'pipe_{i}' for i in range(1,6)]+[f'vector_{i}' for i in range(1,10)]}
 result['parts']={}
 for name in parts:
  _,_,info=mesh_info(W/(name+'.stl'));assert info['closed'] and info['components']==1,(name,info);result['parts'][name]=info
 blob=pl.layout_3mf(parts);(W/'CM6B_rev3.3mf').write_bytes(blob);result['packaging']=tree(blob,parts)
 result['rail_top']={};result['critical_geometry']={}
 for side,x,label in [('l',-104.4,'left'),('r',104.4,'right')]:
  v,t,_=mesh_info(W/('rail_'+side+'.stl'));bv,bt,_=mesh_info(W/f'before-cm6b/CM6B_rail_{label}.stl');av,at,_=mesh_info(R/f'outputs/CM1000_M6_2026-10-28/CM6A_rail_{side}.stl')
  ys=[64.123+i*.5 for i in range(83)];zs=[];old=[]
  for dx in [-3.8,-2.4,2.4,3.8]:zs+=heights(v,t,x+dx,ys);old+=heights(bv,bt,x+dx,ys)
  assert max(zs)-min(zs)<=.001 and max(abs(z-44.425) for z in zs)<=.001
  # Reference top away from its deliberately different/larger ID footprint.
  ax=22.6 if side=='l' else 231.4
  az=heights(av,at,ax,[y+4 for y in ys]);assert max(az)-min(az)<.001
  result['rail_top'][side]=dict(samples=len(zs),region=dict(x_offsets=[-3.8,-2.4,2.4,3.8],y=[ys[0],ys[-1]]),before_z_range=[min(old),max(old)],after_z_range=[min(zs),max(zs)],flatness=max(zs)-min(zs),CM6A_centre_strip_flatness=max(az)-min(az),CM6A_top_z_range=[min(az),max(az)])
  # Compare material intervals on 3 axes away from the changed cosmetic top (>43.9).
  comparisons=[]
  for axis,stations in [(0,[(0,y,z) for y in [12.123,16.123,25.123,40.123,60.123,64.123,70.123,80.123,100.123,120.123,133.123] for z in [1.123,3.123,8.6,16.123,20.123,22.987,27.123,35.85,41.123,43.123]]),
                        (1,[(x+dx,0,z) for dx in [-5,-2,0,2,5] for z in [2.123,8.6,16.123,22.987,27.123,35.85,41.123]]),
                        (2,[(x+dx,y,0) for dx in [-5,-2,0,2,5] for y in [16.123,25.123,40.123,60.123,64.123,70.123,90.123,110.123,133.123]])]:
   for p in stations:
    a=crossing_intervals(bv,bt,axis,p);b=crossing_intervals(v,t,axis,p)
    if axis==2:a=[[lo,min(hi,43.9)] for lo,hi in a if lo<43.9];b=[[lo,min(hi,43.9)] for lo,hi in b if lo<43.9]
    assert len(a)==len(b),(side,axis,p,a,b)
    error=max([abs(q-r) for aa,bb in zip(a,b) for q,r in zip(aa,bb)]+[0]);assert error<=.05,(side,axis,p,error)
    comparisons.append(error)
  result['critical_geometry'][side]=dict(axis_rays=len(comparisons),max_interval_boundary_change_mm=max(comparisons),region_z_below=43.9,old_bounds=mesh_info(W/f'before-cm6b/CM6B_rail_{label}.stl')[2]['bounds'],new_bounds=mesh_info(W/('rail_'+side+'.stl'))[2]['bounds'])
 before=json.loads((W/'before-cm6b/CM6B_spec.json').read_text(encoding='utf-8'));after=json.loads((W/'spec.json').read_text(encoding='utf-8'));before.pop('m6_side_windows');after.pop('m6_side_windows');assert before==after
 bw=json.loads((W/'before-cm6b/CM6B_spec.json').read_text(encoding='utf-8'))['m6_side_windows'];aw=json.loads((W/'spec.json').read_text(encoding='utf-8'))['m6_side_windows'];assert all(a[1:]==b[1:] for a,b in zip(bw,aw))
 def triangles(path):
  vs,ts=read_stl(path);return sorted(tuple(sorted(vs[i] for i in t)) for t in ts)
 labels={'faceplate':'CM6B_faceplate_with_stubs'}
 labels.update({f'pipe_{i}':f'CM6B_light_pipe_{i}' for i in range(1,6)})
 labels.update({f'vector_{i}':f'CM6B_logo_letter_{i}' for i in range(1,8)})
 labels.update({f'vector_{i+7}':f'CM6B_detail_{i}' for i in range(1,3)})
 result['unchanged_part_triangles']={n:triangles(W/(n+'.stl'))==triangles(W/'before-cm6b'/(label+'.stl')) for n,label in labels.items()};assert all(result['unchanged_part_triangles'].values())
 rows=[]
 for c in json.loads((R/'work/m6-rails-43/legacy-before.json').read_text(encoding='utf-8')):
  h=hashlib.sha256(eq.source(eq.clean(c['spec'])).encode('utf-8')).hexdigest();hf=hashlib.sha256(eq.source(eq.clean(dict(c['spec'],m6_rails=False))).encode('utf-8')).hexdigest();assert h==hf==c['sha256'];rows.append(dict(label=c['label'],before=c['sha256'],after=h,explicit_false=hf))
 result['legacy_14']=rows
 protected=json.loads((W/'protected-before.json').read_text(encoding='utf-8'));bad=[n for n,h in protected.items() if sha(R/n)!=h];assert not bad,bad
 result['protected']=dict(files=len(protected),all_unchanged=True)
 write('acceptance.json',result);print('CM6B geometry/packaging, 14 source cases and protected files PASS',flush=True)
if __name__=='__main__':main()
