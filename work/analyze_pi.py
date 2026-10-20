import struct,json
from pathlib import Path
b=Path('work/pi_reference.stl').read_bytes();n=struct.unpack_from('<I',b,80)[0]
ts=[[struct.unpack_from('<3f',b,84+50*i+12+12*j) for j in range(3)] for i in range(n)]
par={}
def find(v):
 par.setdefault(v,v)
 while par[v]!=v:par[v]=par[par[v]];v=par[v]
 return v
for t in ts:
 a=find(t[0])
 for v in t[1:]:par[find(v)]=a
cs={}
for v in par:cs.setdefault(find(v),[]).append(v)
rs=[]
for vs in sorted(cs.values(),key=len,reverse=True):
 rs.append({'vertices':len(vs),'bounds':[[min(v[k] for v in vs) for k in range(3)],[max(v[k] for v in vs) for k in range(3)]]})
Path('work/pi_components.json').write_text(json.dumps(rs,indent=2));print(json.dumps(rs[:12],indent=2))
