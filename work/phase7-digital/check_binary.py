from pathlib import Path
import struct,collections,json
raw=Path('work/phase7-digital/render-diagnostics/tray-binstl.stl').read_bytes();n=struct.unpack_from('<I',raw,80)[0];deg=[];edges=collections.Counter();points=[]
for i in range(n):
 row=struct.unpack_from('<12fH',raw,84+50*i);a,b,c=[tuple(row[j:j+3]) for j in (3,6,9)];u=[b[k]-a[k] for k in range(3)];v=[c[k]-a[k] for k in range(3)];cross=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]);
 if sum(x*x for x in cross)==0:deg.append(dict(triangle=i,vertices=[a,b,c]))
 for x,y in ((a,b),(b,c),(c,a)):edges[tuple(sorted((x,y)))]+=1
print(json.dumps({'binary_triangles':n,'degenerate':deg[:5],'edge_incidence':dict(collections.Counter(edges.values()))},indent=2))
