from pathlib import Path
import json,hashlib
root=Path(r'D:\Projects\assembly-workshop');app=root/'outputs/Mechanical_Design_App'
def edit(f,fn):
 p=app/f;t=p.read_text(encoding='utf-8');p.write_text(fn(t),encoding='utf-8',newline='\n')
def rep(t,a,b):
 assert a in t,a[:100]
 return t.replace(a,b)
wall_py='''
WALL_SIDES = ('front', 'rear', 'left', 'right')
WALL_MESSAGE = 'The wall would hit the faceplate joint; set the device back or move it sideways.'

def wall_open(value):
    if not isinstance(value, list) or not value or any(not isinstance(x, str) or x not in WALL_SIDES for x in value) or len(set(value)) == 4:
        raise ValueError('Open sides must name Front, Rear, Left or Right; leave at least one open and one closed.')
    return [x for x in WALL_SIDES if x in value]

def wall_rectangles(s):
    """Actual wall boxes [x0,y0,x1,y1,height], including returns and finger notches."""
    if s.get('device_mount') != 'wall': return []
    w,d,h = s['dev_w'],s['dev_d'],min(12,s['dev_h']-2)
    result=[]
    for side in WALL_SIDES:
        horizontal=side in ('front','rear'); length=w if horizontal else d
        opened=side in s.get('wall_open',['rear'])
        if opened and length<30: continue
        spans=[(-2.5,9.5,h),(length-9.5,length+2.5,h)] if opened else ([(-2.5,length/2-10,h),(length/2-10,length/2+10,min(4,h)),(length/2+10,length+2.5,h)] if not horizontal and length>=40 else [(-2.5,length+2.5,h)])
        cross=(-2.5,-.5) if side in ('front','left') else ((d+.5,d+2.5) if horizontal else (w+.5,w+2.5))
        for a,b,z in spans:
            q=[a,cross[0],b,cross[1]] if horizontal else [cross[0],a,cross[1],b]
            pts=[]
            for x,y in ((q[0],q[1]),(q[2],q[3])):
                rot=s.get('dev_rot',0)
                p=(d-y,x) if rot==90 else (w-x,d-y) if rot==180 else (y,w-x) if rot==270 else (x,y)
                pts.append(p)
            fx,_,fy,_=footprint(s)
            result.append([fx+min(p[0] for p in pts),fy+min(p[1] for p in pts),fx+max(p[0] for p in pts),fy+max(p[1] for p in pts),z])
    return result

def validate_wall(s, joints=None):
    if s.get('device_mount') != 'wall': return
    if s['dev_h'] <= 2: raise ValueError('A wall needs a device taller than 2 mm.')
    if joints is None:
        half=tray_width(s)/2
        joints=s.get('joint_x',[-min(40,half-12),min(40,half-12)])
    for x0,y0,x1,y1,h in wall_rectangles(s):
        if y0 < 0 or (s['joint']=='screw' and any(x0<x+9 and x1>x-9 and y0<11.3 and y1>0 for x in joints)):
            raise ValueError(WALL_MESSAGE)

'''
wall_scad='''// @wall-begin
wall_open=["rear"]; wall_clear=0.5; wall_t=2; wall_h=min(12,dev_h-2);
function wall_spans(l,opened,notch)=opened?(l<30?[]:[[-2.5,9.5,wall_h],[l-9.5,l+2.5,wall_h]]):notch&&l>=40?[[-2.5,l/2-10,wall_h],[l/2-10,l/2+10,min(4,wall_h)],[l/2+10,l+2.5,wall_h]]:[[-2.5,l+2.5,wall_h]];
function wall_local()=[for(side=["front","rear","left","right"])let(hz=side=="front"||side=="rear",l=hz?dev_w:dev_d,c=side=="front"||side=="left"?-2.5:(hz?dev_d:dev_w)+.5)for(a=wall_spans(l,len(search([side],wall_open))>0,!hz))hz?[a[0],c,a[1],c+2,a[2]]:[c,a[0],c+2,a[1],a[2]]];
function wall_rects()=[for(q=wall_local())let(a=dp([q[0],q[1]]),b=dp([q[2],q[3]]))[dev_x+min(a[0],b[0]),dev_y+min(a[1],b[1]),dev_x+max(a[0],b[0]),dev_y+max(a[1],b[1]),q[4]]];
module wall_add(){if(device_mount=="wall")for(q=wall_rects())translate([q[0],q[1],floor_top-.01])cube([q[2]-q[0],q[3]-q[1],q[4]+.01]);}
assert(device_mount!="wall"||(is_list(wall_open)&&len(wall_open)>0&&len([for(s=["front","rear","left","right"])if(len(search([s],wall_open))>0)s])<4&&len([for(s=wall_open)if(s!="front"&&s!="rear"&&s!="left"&&s!="right")s])==0),"Open sides must leave at least one open and one closed");
assert(device_mount!="wall"||dev_h>2,"A wall needs a device taller than 2 mm");
assert(device_mount!="wall"||len([for(q=wall_rects())if(q[1]<0||(joint=="screw"&&len([for(x=joint_x)if(q[0]<x+9&&q[2]>x-9&&q[1]<11.3&&q[3]>0)x])>0))q])==0,"The wall would hit the faceplate joint; set the device back or move it sideways.");
// @wall-end
'''
def eqedit(t):
 t=rep(t,"MOUNTS = ('inserts',", "MOUNTS = ('wall', 'inserts',")
 t=t.replace("('straps', 'flat', 'sleeve')","('straps', 'wall', 'flat', 'sleeve')")
 t=rep(t,"'dev_rot', 'device_mount', 'standoff'","'dev_rot', 'device_mount', 'wall_open', 'standoff'")
 t=rep(t,"        if key == 'keystones':","        if key == 'wall_open':\n            v = wall_open(v)\n        elif key == 'keystones':")
 t=rep(t,"def floor_z(spec):",wall_py+'\ndef floor_z(spec):')
 t=rep(t,"    if not spec.get('drives'):","    if not (spec.get('device_mount') == 'wall' or (spec.get('second') or {}).get('device_mount') == 'wall'):\n        text = re.sub(r'// @wall-begin\\n.*?// @wall-end\\n', '', text, flags=re.S)\n        text = text.replace('\\n wall_add();', '')\n    if not spec.get('drives'):")
 t=rep(t,"    raw_feet = spec.get('feet') or []","    if s['device_mount'] == 'wall':\n        s['wall_open'] = wall_open(spec.get('wall_open', ['rear']))\n    raw_feet = spec.get('feet') or []")
 t=rep(t,"    rear_floor_geometry(s)\n    return s","    rear_floor_geometry(s)\n    if not spec.get('_pair'): validate_wall(s)\n    return s")
 t=rep(t,"'straps': 5.5, 'flat': 6.2","'straps': 5.5, 'wall': 2.5, 'flat': 6.2")
 t=rep(t,"'dev_off_y', 'dev_rot', 'feet')","'dev_off_y', 'dev_rot', 'feet', 'wall_open')")
 t=rep(t,"    ids = [p['id'] for p in s['ports'] + s['rear_ports']]\n    if len(ids) != len(set(ids)):\n        raise ValueError('Each port needs its own id.')\n    return s","    for device in tray_devices(s):\n        validate_wall(device, s.get('joint_x', [-min(40,half-12),min(40,half-12)]))\n    ids = [p['id'] for p in s['ports'] + s['rear_ports']]\n    if len(ids) != len(set(ids)):\n        raise ValueError('Each port needs its own id.')\n    return s")
 t=rep(t,"'device_features_add': 'device2_features_add'","'wall_open': 'dev2_wall_open', 'wall_h': 'dev2_wall_h', 'wall_spans': 'wall2_spans', 'wall_local': 'wall2_local', 'wall_rects': 'wall2_rects', 'wall_add': 'wall2_add',\n                  'device_features_add': 'device2_features_add'")
 t=rep(t,"    for key in V2_DEFAULTS:","    if s.get('device_mount') == 'wall': over['wall_open'] = s['wall_open']\n    for key in V2_DEFAULTS:")
 t=rep(t,"        # The tray spans both devices", "        if d2['device_mount'] == 'wall': over['dev2_wall_open'] = d2['wall_open']\n        # The tray spans both devices")
 return t
edit('equipment.py',eqedit)
def scadedit(t):
 t=rep(t,'module device_features_add(){','module device_features_add(){\n wall_add();')
 return rep(t,'module tray_joint_add(rear=false){',wall_scad+'\nmodule tray_joint_add(rear=false){')
edit('equipment_tray.scad',scadedit)
# Floor height mirrors: wall uses straps height, never straps slots.
edit('port_openings.py',lambda t:t.replace("spec.get('device_mount') == 'straps'","spec.get('device_mount') in ('straps','wall')").replace("s.get('device_mount')=='straps'","s.get('device_mount') in ('straps','wall')"))
edit('port-openings.js',lambda t:t.replace("['straps','flat','sleeve']","['straps','wall','flat','sleeve']").replace("spec.device_mount==='straps'","['straps','wall'].includes(spec.device_mount)").replace("s.device_mount==='straps'","['straps','wall'].includes(s.device_mount)"))
edit('clearance.js',lambda t:t.replace("s.device_mount==='straps'","['straps','wall'].includes(s.device_mount)").replace("s2.device_mount==='straps'","['straps','wall'].includes(s2.device_mount)"))
edit('cable-ports.js',lambda t:t.replace('none for straps','none for straps or wall'))
edit('equipment-wizard.js',lambda t:rep(t,"straps:'Strap / zip-tie slots',","straps:'Strap / zip-tie slots',wall:'Thin wall around it (boxes)',"))
wall_js='''
  const WALL_SIDES=['front','rear','left','right'],WALL_MESSAGE='The wall would hit the faceplate joint; set the device back or move it sideways.';
  function wallBoxes(spec,v){
    if(v.device_mount!=='wall')return [];
    const L=layout(spec,v),w=+spec.dev_w,d=+spec.dev_d,h=Math.min(12,+spec.dev_h-2),out=[];
    for(const side of WALL_SIDES){const hz=['front','rear'].includes(side),len=hz?w:d,opened=(v.wall_open||['rear']).includes(side);if(opened&&len<30)continue;
      const spans=opened?[[-2.5,9.5,h],[len-9.5,len+2.5,h]]:!hz&&len>=40?[[-2.5,len/2-10,h],[len/2-10,len/2+10,Math.min(4,h)],[len/2+10,len+2.5,h]]:[[-2.5,len+2.5,h]],c=['front','left'].includes(side)?-2.5:(hz?d:w)+.5;
      for(const [a,b,z] of spans){const q=hz?[a,c,b,c+2]:[c,a,c+2,b],p=dp(spec,v.dev_rot,[q[0],q[1]]),r=dp(spec,v.dev_rot,[q[2],q[3]]);out.push([L.dev_x+Math.min(p[0],r[0]),L.dev_y+Math.min(p[1],r[1]),L.dev_x+Math.max(p[0],r[0]),L.dev_y+Math.max(p[1],r[1]),z]);}
    }return out;
  }
  function wallProblem(spec,v,xs){if(v.device_mount!=='wall')return '';xs=xs||joints(spec,v)?.joints||[];return wallBoxes(spec,v).some(q=>q[1]<0||v.joint==='screw'&&xs.some(x=>q[0]<x+9&&q[2]>x-9&&q[1]<11.3&&q[3]>0))?WALL_MESSAGE:'';}
'''
def trayedit(t):
 t=rep(t,"'dev_rot','device_mount','standoff'","'dev_rot','device_mount','wall_open','standoff'")
 t=rep(t,"device_mount:'inserts',standoff", "device_mount:'inserts',wall_open:['rear'],standoff")
 t=rep(t,"straps:'Strap',","straps:'Strap',wall:'Wall',")
 t=rep(t,'  function footPockets(spec,v)',wall_js+'\n  function footPockets(spec,v)')
 t=rep(t,"    if(!MOUNTS[v.device_mount])", "    if(v.device_mount==='wall'){if(!Array.isArray(v.wall_open)||!v.wall_open.length||v.wall_open.some(s=>!WALL_SIDES.includes(s))||new Set(v.wall_open).size===4)out.push('Open sides must name Front, Rear, Left or Right; leave at least one open and one closed.');if(+spec.dev_h<=2)out.push('A wall needs a device taller than 2 mm.');}\n    if(!MOUNTS[v.device_mount])")
 t=rep(t,'    return out;\n  }\n  // Plain-language warnings',"    const wp=wallProblem(spec,v);if(wp)out.push(wp);\n    return out;\n  }\n  // Plain-language warnings")
 t=rep(t,"    if(v.device_mount==='flat'){\n      const h=", "    if(v.device_mount==='wall')for(const q of wallBoxes(spec,v))posts.push(...box(q[0],q[1],floor,q[2],q[3],floor+q[4]));\n    if(v.device_mount==='flat'){\n      const h=")
 t=rep(t,'const api={V2,','const api={wallBoxes,wallProblem,WALL_MESSAGE,V2,')
 anchor="    const mountOpts=PO().usesStandoffs(dv)?"
 t=rep(t,anchor,"    const wallOpts=dv.device_mount==='wall'?[h('p',{},'Open sides (cables):'),...WALL_SIDES.map(side=>{const input=h('input',{type:'checkbox'});input.checked=(dv.wall_open||['rear']).includes(side);input.onchange=()=>{dv.wall_open=WALL_SIDES.filter(s=>s===side?input.checked:(dv.wall_open||['rear']).includes(s));render();};return h('label',{},input,side[0].toUpperCase()+side.slice(1));}),h('p',{class:'ew-note'},'Device sits on the floor inside a 2 mm wall, open where you tick. Fit and retention UNKNOWN.')]:[];\n"+anchor)
 t=rep(t,"...mountOpts)),","...mountOpts),...wallOpts),")
 return t
edit('tray-placement.js',trayedit)
def pairedit(t):
 t=t.replace("'dev_rot','device_mount','standoff'","'dev_rot','device_mount','wall_open','standoff'").replace('straps:5.5,flat:6.2','straps:5.5,wall:2.5,flat:6.2')
 t=rep(t,"if(j.problem)out.push(j.problem);}","if(j.problem)out.push(j.problem);for(const [sp,v] of [[spec1,v1],[spec2,m]]){const wp=T().wallProblem(sp,v,j.joints);if(wp&&!out.includes(wp))out.push(wp);}}")
 return t
edit('tray-pair.js',pairedit)
# Update served asset hashes (LF normalized, like existing manifest checks).
p=app/'asset-manifest.json';m=json.loads(p.read_text(encoding='utf-8'))
for row in m:
 f=app/row['file']
 if f.exists():row['sha256']=hashlib.sha256(f.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
p.write_text(json.dumps(m,indent=1)+'\n',encoding='utf-8')
print('wall implementation applied')
