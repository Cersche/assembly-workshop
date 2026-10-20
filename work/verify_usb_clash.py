exec(open('work/analyze_pi.py').read().split('rs=[]')[0])
root=find(next(v for v in par if 33.98<v[0]-44<34 and 14.99<69-v[2]<15 and v[1]<.27))
ids=[i for i,t in enumerate(ts) if find(t[0])==root]
new=bytearray(80)+struct.pack('<I',len(ids))
for i in ids:
 rec=bytearray(b[84+50*i:134+50*i])
 nx,ny,nz=struct.unpack_from('<3f',rec);struct.pack_into('<3f',rec,0,nx,-nz,ny)
 for j in range(3):
  x,y,z=struct.unpack_from('<3f',rec,12+12*j);struct.pack_into('<3f',rec,12+12*j,x-44,69-z,y+13.900009155273438)
 new+=rec
Path('work/usb_candidate.stl').write_bytes(new)
Path('work/usb_collision.scad').write_text('intersection(){import("usb_candidate.stl"); translate([33,0,0]) hull(){translate([0,9,9.7])cube([2,2,0.5]);translate([0,9,16])cube([2,2,0.5]);translate([0,20,9.7])cube([2,2,0.5]);}}')
import subprocess
r=subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o','work/usb_collision.stl','work/usb_collision.scad'],capture_output=True,text=True)
Path('work/usb_collision.log').write_text(r.stderr);print(r.stderr)
