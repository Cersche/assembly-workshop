exec(open('work/check_v2_triangles.py').read().split('results={}')[0])
import math
regions={}
for cx in [-40,40]:regions['ear_'+str(cx)]=[((1,0,0),cx+7),((-1,0,0),7-cx),((0,1,0),11.3),((0,-1,0),-8.3),((0,0,1),29),((0,0,-1),-10)]
for cx in [-40.5,17.5]:
 for cy in [16.5,65.5]:
  planes=[((0,0,1),15.999),((0,0,-1),-10)]
  for i in range(48):
   a=(i+.5)*2*math.pi/48;nx,ny=math.cos(a),math.sin(a);planes.append(((nx,ny,0),nx*cx+ny*cy+3.5*math.cos(math.pi/48)))
  regions[f'standoff_{cx}_{cy}']=planes
results={}
for name,planes in regions.items():
 hits=[]
 for i,t in enumerate(ts):
  if any(all(sum(x*y for x,y in zip(a,v))>lim for v in t) for a,lim in planes):continue
  poly=t
  for a,lim in planes:
   poly=clip(poly,a,lim-.00001)
   if not poly:break
  if poly:hits.append(i)
 results[name]=len(hits)
print(results);Path('work/v2_other_triangle_checks.json').write_text(json.dumps(results,indent=2));assert not any(results.values())
