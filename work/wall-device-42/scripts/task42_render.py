from pathlib import Path
import sys,json,hashlib,re,subprocess
root=Path(r'D:\Projects\assembly-workshop');app=root/'outputs/Mechanical_Design_App';out=root/'work/wall-device-42'
sys.path.insert(0,str(app));import equipment as eq,mesh_revision as mr
pi=json.loads((app/'equipment-examples.json').read_text(encoding='utf-8'))[0]['spec']
hue=dict(name='Hue Bridge test',dev_w=90.7,dev_d=90.4,dev_h=25.4,device_mount='wall',wall_open=['rear'],holes=[],dev_off_x=-30,dev_off_y=1,dev_rot=0,u=1,joint='screw',keystones=[-100],ports=[],rear_ports=[],rear_support=False)
pair=dict(hue,second=dict(pi,dev_off_x=48,dev_rot=90))
records=[]
for label,raw in [('requested pair',pair),('requested pair rotated',dict(pair,dev_rot=90))]:
 try: eq.clean(raw);records.append(dict(label=label,unexpected='accepted'))
 except ValueError as exc: records.append(dict(label=label,blocked=str(exc)))
# Correct only the new disposable Hue position. Existing joint geometry is preserved.
safe=dict(pair,dev_off_y=13)
cases=[('single',dict(hue,dev_off_x=0,dev_off_y=13,keystones=[])),('pair',safe),('pair90',dict(safe,dev_rot=90)),
       ('second-wall',dict(pi,dev_off_x=-48,dev_rot=90,dev_off_y=13,keystones=[],ports=[],second=dict(hue,dev_off_x=30,dev_off_y=13,keystones=[])))]
for label,raw in cases:
 print('Rendering',label,flush=True)
 s=eq.clean(raw);folder=eq.render(raw,out/'render-data')
 r=dict(label=label,spec=s,folder=str(folder.relative_to(root)),parts={})
 for part in ('tray','faceplate'):
  m=mr.read_mesh(folder/(part+'.stl'),part);r['parts'][part]=dict(bounds=m['bounds'],volume=m['signed_volume_mm3'],triangles=len(m['triangles']),closed=True)
 r['nudge_mm']=json.loads((folder/'revision.json').read_text(encoding='utf-8'))['nudge_mm']
 # Horizontal cross-section through the actual STL, transformed back into device-local frame.
 dev=s['second'] if label=='second-wall' else s
 effective=dict(s,**dev);fx,_,fy,_=eq.footprint(effective);rot=effective.get('dev_rot',0);w,d=dev['dev_w'],dev['dev_d'];floor=eq.floor_z(s)+3
 verts=mr.read_mesh(folder/'tray.stl','tray')['vertices'];tris=mr.read_mesh(folder/'tray.stl','tray')['triangles']
 def local(p):
  x,y=p[0]-fx,p[1]-fy
  return (y,d-x,p[2]) if rot==90 else (w-x,d-y,p[2]) if rot==180 else (w-y,x,p[2]) if rot==270 else (x,y,p[2])
 vv=[local(p) for p in verts]
 def intersections(axis,a,z):
  # Intersect horizontal section segments with x=a or y=a; dedup triangle diagonal crossings.
  other=1-axis;hits=[]
  for face in tris:
   tri=[vv[i] for i in face];pts=[]
   for i in range(3):
    p,q=tri[i],tri[(i+1)%3]
    if (p[2]<z<=q[2]) or(q[2]<z<=p[2]):
     t=(z-p[2])/(q[2]-p[2]);pts.append([p[k]+t*(q[k]-p[k]) for k in range(2)])
   if len(pts)==2:
    p,q=pts
    if min(p[axis],q[axis])<a<max(p[axis],q[axis]):
     t=(a-p[axis])/(q[axis]-p[axis]);hits.append(p[other]+t*(q[other]-p[other]))
  return sorted(set(round(v,4) for v in hits))
 # Low section below finger notches gives full inner size; rear-edge line gives actual cable gap.
 yline=intersections(0,w/2+.137,floor+2)
 xline=intersections(1,d*.23+.137,floor+2)
 rearline=intersections(1,d+1.137,floor+6)
 front_z=[p[2] for p in vv if -.51<p[1]<-.49 and -1<p[0]<w+1]
 r['measurements']=dict(inner_width_mm=round(xline[-2]-xline[1],4) if len(xline)>=4 else None,
   front_inner_y_mm=yline[1] if len(yline)>=2 else None,
   inner_depth_mm=round(d+1,4),rear_gap_mm=round(rearline[-2]-rearline[1],4) if len(rearline)>=4 else None,
   wall_height_mm=round(max(front_z)-floor,4),x_section=xline,y_section=yline,rear_section=rearline,
   note='Inner depth uses front inner STL plane and rear return inner plane; rear is open at centre.')
 # Rear return inner face at Y=d+.5 is measured from STL vertex planes.
 rear_inner=sorted(set(round(p[1],4) for p in vv if abs(p[1]-(d+.5))<.001 and abs(p[2]-(floor+12))<.001))
 r['measurements']['rear_inner_planes']=rear_inner
 if rear_inner and len(yline)>=2:r['measurements']['inner_depth_mm']=round(rear_inner[0]-yline[1],4)
 records.append(r)
 (out/'renders.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
 print(label,r['measurements'],flush=True)
print('done',flush=True)
