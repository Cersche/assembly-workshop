from pathlib import Path
p=Path('outputs/Mechanical_Design_App'); sc=p/'equipment_tray.scad'; py=p/'equipment.py'
text=sc.read_text(encoding='utf-8'); original=text
block='''// @drives-begin
// Task 39: nominal SFF-8301/8201 geometry; PROPOSED — UNVALIDATED.
// Coordinates: tray X, Y offset from front_gap; connectors face +Y.
drives=[]; drive_mount="screws"; ssd_h=7;
function drive_w(d)=d[0]=="3.5"?101.6:69.85;
function drive_d(d)=d[0]=="3.5"?147:100;
function drive_ys(d)=d[0]=="3.5"?[29.52,61.27,105.72]:[9.4,86];
function drive_xs(d)=d[0]=="3.5"?[3.18,98.43]:[4.07,65.79];
function drive_side_y(d)=d[0]=="3.5"?118.5:86;
function drive_side_z(d)=d[0]=="3.5"?6.35:3;
module drive_add(){for(d=drives)let(w=drive_w(d),dep=drive_d(d),sy=drive_side_y(d),sz=drive_side_z(d))translate([d[1],front_gap+d[2],floor_top]){
 for(x=drive_xs(d),y=drive_ys(d))translate([x,y,-0.1])cylinder(d=8,h=3.1);
 if(drive_mount=="sleeve"){
  // Open rear; 0.5 mm side/front play, 2 mm rails. One rear flexing tab per side.
  translate([-2.5,-2.5,-0.1])cube([w+5,2,8.1]);
  for(side=[0,1])let(x=side?w+0.5:-2.5){
   translate([x,-1,-0.1])cube([2,sy-19,3+sz+2.1]);
   translate([x,sy-21,3+sz-2])cube([2,25,4]);
   // Smooth proposed peg, not a threaded fastener. Insertion/fatigue UNKNOWN.
   translate([side?w+2.5:-2.5,sy,3+sz])rotate([0,side?-90:90,0])cylinder(d=2.4,h=3.5,$fn=32);
  }
 }
}}
module drive_cut(){for(d=drives)translate([d[1],front_gap+d[2],tray_z]){
 if(drive_mount=="screws")for(x=drive_xs(d),y=drive_ys(d)){
  translate([x,y,-0.1])cylinder(d=d[0]=="3.5"?3.8:3.4,h=6.2);
  // 6 mm floor+pad stack: nominal penetration 2.85 mm HDD / 1.5 mm SSD.
  translate([x,y,-0.1])cylinder(d=d[0]=="3.5"?7:6,h=d[0]=="3.5"?2.6:3.6);
 }
 if(d[0]=="3.5")for(x=[14:12:86],y=[18:12:126])translate([x-2.5,y-3,-0.1])cube([5,6,tray_t+0.2]);
}}
// @drives-end
'''
text=block+text
replacements={'   device_features_add();':'   if(len(drives)>0)drive_add();else device_features_add();','  device_features_cut();':'  if(len(drives)>0)drive_cut();else device_features_cut();'}
for old,new in replacements.items():
 assert old in text; text=text.replace(old,new)
sc.write_text(text,encoding='utf-8',newline='\n')
t=py.read_text(encoding='utf-8');t=t.replace("    if spec.get('faceplate_only') is True:\n        return clean_faceplate(spec)","    if 'drives' in spec and spec['drives'] != []:\n        return clean_drives(spec)\n    if spec.get('faceplate_only') is True:\n        return clean_faceplate(spec)",1)
t=t.replace("    if not spec.get('faceplate_only'):\n", "    if not spec.get('drives'):\n        text = re.sub(r'// @drives-begin\\n.*?// @drives-end\\n', '', text, flags=re.S)\n        for old, new in DRIVE_REPLACEMENTS.items(): text = text.replace(new, old)\n    if not spec.get('faceplate_only'):\n",1)
t=t.replace("    if s.get('faceplate_only'): over['part'] = 'faceplate'", "    if s.get('drives'):\n        over.update(drives=s['drives'], drive_mount=s['drive_mount'], ssd_h=s['ssd_h'],\n                    tray_w=s['dev_w']+16, tray_d=s['dev_d']+12+25)\n    if s.get('faceplate_only'): over['part'] = 'faceplate'")
t+='''

# Drive assembly is an opt-in branch of the generic adapter; empty drives change no source bytes.
DRIVE_REPLACEMENTS = '''+repr(replacements)+'''
DRIVE_LIMITS = ['PROPOSED — UNVALIDATED. Drive fit, peg retention, tab fatigue, vibration, strength, airflow/temperature and usable rack depth UNKNOWN.',
 'Nominal SFF dimensions only; actual drive holes, thread depth, screw heads/torque and cable bend space must be checked. 7 mm SSD bottom holes are optional.']

def clean_drives(spec):
    ds=spec.get('drives')
    if not isinstance(ds,list) or len(ds)!=2 or sorted(str(d[0]) for d in ds if isinstance(d,list) and len(d)==3)!=['2.5','3.5']:
        raise ValueError('Drive tray needs one 3.5 and one 2.5 drive [type,x_off,y_off].')
    mode=spec.get('drive_mount','screws')
    if mode not in ('screws','sleeve'): raise ValueError('Choose screws or sleeve for drives.')
    sh=num(spec.get('ssd_h',7),'SSD height',7,9.5)
    if sh not in (7,9.5): raise ValueError('SSD height must be 7 or 9.5 mm.')
    if spec.get('second') or spec.get('faceplate_only') or spec.get('feet') or spec.get('ports') or spec.get('keystones') or spec.get('rear_support') or spec.get('coupon'):
        raise ValueError('Drive tray requires a blank faceplate, no feet, second item, coupon or rear bracket.')
    if spec.get('u',1)!=1 or spec.get('joint','screw')!='screw' or spec.get('device_mount','flat')!='flat' or spec.get('front_position','today')!='today' or spec.get('bezel','none')!='none' or any(spec.get(k,0) for k in ('dev_rot','dev_off_x','dev_off_y')):
        raise ValueError('Drive tray uses fixed 1U placement, a blank faceplate and the existing screw joint.')
    out=[];boxes=[]
    for typ,x,y in ds:
        x=num(x,'Drive X',-100,100);y=num(y,'Drive Y',0,50)
        w,dep=(101.6,147) if typ=='3.5' else (69.85,100)
        out.append([typ,x,y]);boxes.append((x,x+w,12+y,12+y+dep))
    a,b=boxes
    if max(a[0]-b[1],b[0]-a[1])<8: raise ValueError('Drives need an 8 mm side gap for independent rails/tabs.')
    width=round(2*max(abs(v) for b in boxes for v in b[:2])+16,3)
    depth=max(b[3] for b in boxes)+25
    if width>204: raise ValueError('Drive tray exceeds the 204 mm maximum width.')
    if depth>240: raise ValueError('Drive tray needs 25 mm rear connector space within 240 mm nominal depth.')
    base=dict(name=spec.get('name','Drives (3.5" + 2.5")'),dev_w=width-16,dev_d=depth-37,dev_h=29.1,
              device_mount='flat',joint='screw',standoff=0,holes=[],ports=[],keystones=[],u=1)
    if 'quality' in spec:base['quality']=spec['quality']
    s=clean(base);s.update(drives=out,drive_mount=mode,ssd_h=sh)
    return s

def drive_hardware(s):
    if not s.get('drives') or s.get('drive_mount')!='screws':return []
    return [{'quantity':4,'description':'6-32 x 1/4 inch (drive screws; head/torque UNKNOWN)'},
            {'quantity':4,'description':'M3 x 4 mm (drive screws; head/torque UNKNOWN)'}]
'''
t=t.replace("'logs': logs}","'logs': logs}\n                if s.get('drives'): report.update(drive_hardware=drive_hardware(s), limitations=LIMITS+DRIVE_LIMITS)")
py.write_text(t,encoding='utf-8',newline='\n')
