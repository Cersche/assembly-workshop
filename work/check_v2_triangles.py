import struct,json
from pathlib import Path
b=Path('work/pi_aligned.stl').read_bytes();n=struct.unpack_from('<I',b,80)[0]
ts=[[struct.unpack_from('<3f',b,84+50*i+12+12*j) for j in range(3)] for i in range(n)]
def clip(poly,a,lim):
 out=[]
 for i,p in enumerate(poly):
  q=poly[(i+1)%len(poly)];dp=sum(x*y for x,y in zip(a,p))-lim;dq=sum(x*y for x,y in zip(a,q))-lim
  if dp<=0:out.append(p)
  if (dp<0<dq) or (dq<0<dp):
   t=dp/(dp-dq);out.append(tuple(p[k]+t*(q[k]-p[k]) for k in range(3)))
 return out
results={}
for cx in [-46,-34,34,46]:
 planes=[((1,0,0),cx+1),((-1,0,0),1-cx),((0,1,0),22),((0,-1,0),-9),((0,0,-1),-9.7),((0,0,1),15.5),((0,5.3/11,1),20.8)]
 hits=[]
 for i,t in enumerate(ts):
  if max(v[0] for v in t)<cx-1 or min(v[0] for v in t)>cx+1 or min(v[1] for v in t)>22 or max(v[1] for v in t)<9 or min(v[2] for v in t)>16:continue
  poly=[(v[0],v[1],v[2]-.5) for v in t]
  for a,lim in planes:
   poly=clip(poly,a,lim-.00001)
   if not poly:break
  if poly:hits.append(i)
 results[str(cx)]={'triangle_intersections_after_pi_lowered_0_5mm':len(hits)}
print(json.dumps(results,indent=2));Path('work/v2_gusset_triangle_checks.json').write_text(json.dumps(results,indent=2));assert all(v['triangle_intersections_after_pi_lowered_0_5mm']==0 for v in results.values())
