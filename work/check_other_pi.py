exec(open('work/check_gusset_pi.py').read().split('hits=[]')[0])
import math
for name,fn in [
 ('PCB standoffs',lambda x,y,z:10.001<z<15.999 and any(1.401<math.hypot(x-cx,y-cy)<3.499 for cx in [-40.5,17.5] for cy in [16.5,65.5])),
 ('screw ears',lambda x,y,z:8.301<y<11.299 and 10.001<z<28.999 and any(abs(x-cx)<6.999 and math.hypot(x-cx,z-21)>1.701 for cx in [-40,40])),
 ('socket rails',lambda x,y,z:0.001<y<7.999 and 10.001<z<14.999 and any(abs(x-cx)<8.999 for cx in [-40,40])),
 ('faceplate',lambda x,y,z:-2.999<y<-.001 and 0<z<42)]:
 h=[p for p in pts if fn(*p)];print(name,len(h),h[:2])
