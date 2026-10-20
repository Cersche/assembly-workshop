from pathlib import Path
import struct,math,json
exec(Path('work/analyze_pi.py').read_text().split('rs=[]')[0])
board=next(vs for vs in cs.values() if len(vs)==6300)
for x,z in [(3.5,3.5),(61.5,3.5),(3.5,52.5),(61.5,52.5)]:
 r=[math.hypot(v[0]-x,v[2]-z) for v in board];near=[v for v,d in zip(board,r) if abs(d-1.35)<.003]
 print('hole',x,z,'radius1.35 vertices',len(near))
new=bytearray(b)
for i in range(n):
 off=84+50*i
 nx,ny,nz=struct.unpack_from('<3f',b,off);struct.pack_into('<3f',new,off,nx,-nz,ny)
 for j in range(3):
  x,y,z=struct.unpack_from('<3f',b,off+12+12*j)
  struct.pack_into('<3f',new,off+12+12*j,x-44,69-z,y+13.900009155273438)
Path('work/pi_aligned.stl').write_bytes(new)
p=Path('work/package_revision.py').read_text()
p=p.replace("[(1,'faceplate'),(2,'tray')]","[(1,'faceplate'),(2,'tray'),(4,'pi_reference')]")
p=p.replace("raw=(out/(name+'.stl')).read_text()\n    vs=[tuple(map(float,m)) for m in re.findall(r'vertex\\s+([-\\d.e+]+)\\s+([-\\d.e+]+)\\s+([-\\d.e+]+)',raw)]", "if oid==4:\n        vs=[struct.unpack_from('<3f',new,84+50*i+12+12*j) for i in range(n) for j in range(3)]\n    else:\n        raw=(out/(name+'.stl')).read_text()\n        vs=[tuple(map(float,m)) for m in re.findall(r'vertex\\s+([-\\d.e+]+)\\s+([-\\d.e+]+)\\s+([-\\d.e+]+)',raw)]")
p=p.replace('for oid in [1,2]:','for oid in [1,2,4]:').replace("out/'assembly_review.3mf'","root/'work/pi_fit_review.3mf'")
exec(p)
