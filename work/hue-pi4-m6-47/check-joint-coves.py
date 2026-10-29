from pathlib import Path
import math,re,json,itertools
R=Path('D:/Projects/assembly-workshop');O=R/'outputs/Hue_Pi4_M6-B_2026-10-28';W=R/'work/hue-pi4-m6-47'
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def pointtri(p,a,b,c):
 ab=sub(b,a);ac=sub(c,a);ap=sub(p,a);d1=dot(ab,ap);d2=dot(ac,ap)
 if d1<=0 and d2<=0:return dot(ap,ap)
 bp=sub(p,b);d3=dot(ab,bp);d4=dot(ac,bp)
 if d3>=0 and d4<=d3:return dot(bp,bp)
 vc=d1*d4-d3*d2
 if vc<=0 and d1>=0 and d3<=0:
  q=add(a,mul(ab,d1/(d1-d3)));return dot(sub(p,q),sub(p,q))
 cp=sub(p,c);d5=dot(ab,cp);d6=dot(ac,cp)
 if d6>=0 and d5<=d6:return dot(cp,cp)
 vb=d5*d2-d1*d6
 if vb<=0 and d2>=0 and d6<=0:
  q=add(a,mul(ac,d2/(d2-d6)));return dot(sub(p,q),sub(p,q))
 va=d3*d6-d5*d4
 if va<=0 and d4-d3>=0 and d5-d6>=0:
  q=add(b,mul(sub(c,b),(d4-d3)/((d4-d3)+(d5-d6))));return dot(sub(p,q),sub(p,q))
 den=va+vb+vc
 if den==0:return min(dot(ap,ap),dot(bp,bp),dot(cp,cp))
 q=add(a,add(mul(ab,vb/den),mul(ac,vc/den)));return dot(sub(p,q),sub(p,q))
def segseg(p1,q1,p2,q2):
 d1=sub(q1,p1);d2=sub(q2,p2);r=sub(p1,p2);a=dot(d1,d1);e=dot(d2,d2);f=dot(d2,r)
 clamp=lambda v:max(0,min(1,v))
 if a==0 and e==0:return dot(r,r)
 if a==0:s=0;t=clamp(f/e)
 else:
  c=dot(d1,r)
  if e==0:t=0;s=clamp(-c/a)
  else:
   b=dot(d1,d2);den=a*e-b*b;s=clamp((b*f-c*e)/den) if den>0 else 0;t=(b*s+f)/e
   if t<0:t=0;s=clamp(-c/a)
   elif t>1:t=1;s=clamp((b-c)/a)
 v=sub(add(p1,mul(d1,s)),add(p2,mul(d2,t)));return dot(v,v)
def boxtri(box):
 lo,hi=box;result=[]
 for axis in range(3):
  other=[i for i in range(3) if i!=axis]
  for side in range(2):
   pts=[]
   for j,k in [(0,0),(1,0),(1,1),(0,1)]:
    p=list(lo);p[axis]=box[side][axis];p[other[0]]=box[j][other[0]];p[other[1]]=box[k][other[1]];pts.append(tuple(p))
   result.extend([(pts[0],pts[1],pts[2]),(pts[0],pts[2],pts[3])])
 return result
def tritri(a,b):
 d=min([pointtri(p,*b) for p in a]+[pointtri(p,*a) for p in b])
 for i in range(3):
  for j in range(3):d=min(d,segseg(a[i],a[(i+1)%3],b[j],b[(j+1)%3]))
 return d
v=[tuple(map(float,m)) for m in re.findall(r'\bvertex\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)',(O/'checks/lane-joint.stl').read_text(encoding='utf-8'))];ts=[v[i:i+3] for i in range(0,len(v),3)]
# Disjoint-by-X cases: exact surface distance to conservative device/port boxes.
pi=[[-102,0,17.225],[-46,85,38.825]]
ports=[[[x-w/2,-4,z-h/2],[x+w/2,0,z+h/2]] for x,z,w,h in [(-93,26.8,15,17.5),(-75,26.8,15,17.5),(-56.3,25.6,17.5,15)]]
def distance(mesh,box):return math.sqrt(min(tritri(t,b) for t in mesh for b in boxtri(box)))
a=json.loads((O/'checks/clearance.json').read_text(encoding='utf-8'))
for j in a['joints']:
 x=j['x'];delta=x+29.5;mesh=[[add(p,(delta,0,0)) for p in t] for t in ts]
 d=j['gap_lower_bounds_mm'];d['pi_footprint']=distance(mesh,pi);d['pi_openings']=min(distance(mesh,p) for p in ports)
 # Full joint includes 4 mm coves beyond each tab side. Use full envelope for other positive separations.
 full=[[x-14,0,11.215],[x+14,14.3,42.225]]
 def gap(b):return math.sqrt(sum(max(0,full[0][i]-b[1][i],b[0][i]-full[1][i])**2 for i in range(3)))
 d['cradle_posts']=gap(a['cradle']['bounds']);d['tie_slots']=min(gap([[t,96,8.125],[t+3,108,11.325]]) for t in [-42.5,-19.5]);d['keystone_rear']=gap([[82.6,0,7.225],[102.4,6.31999,40.725]])
 j['conservative_envelope']=full;j['smallest_guaranteed_gap_mm']=min(d.values());print(x,d)
a['method']='All lengths mm. Positive Euclidean AABB separations are conservative lower bounds, not exact closest mesh distances. Full M6 joint includes low 4 mm coves beyond nominal tab +/-10. Pi/port bounds use triangle-to-box distances from a rendered full joint; rounded ports are inside their boxes. Keystone uses Y>0 rear envelope. Cradle read/cut/rendered in place.'
a['lane_joint_detail']={'nominal_tab_x':[-39.5,-19.5],'tab_to_pi_x_gap_mm':6.5,'full_cove_x':[-43.5,-15.5],'cove_projected_x_gap_mm':2.5,'cove_top_z_mm':15.215,'pi_bottom_z_mm':17.225,'full_joint_to_pi_box_minimum_mm':a['joints'][0]['gap_lower_bounds_mm']['pi_footprint'],'distance_algorithm':'minimum vertex-to-triangle and edge-to-edge distances on disjoint triangle surfaces; no coordinate rounding'}
assert a['joints'][0]['gap_lower_bounds_mm']['pi_footprint']>=5
assert all(j['smallest_guaranteed_gap_mm']>0 for j in a['joints'])
for p in [O/'checks/clearance.json',W/'clearance.json']:p.write_text(json.dumps(a,indent=2),encoding='utf-8')
p=O/'checks/acceptance.json';acc=json.loads(p.read_text(encoding='utf-8'));acc['clearance']=a;p.write_text(json.dumps(acc,indent=2),encoding='utf-8')
