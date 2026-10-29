from pathlib import Path
import hashlib, json, re, subprocess, difflib

ROOT = Path('D:/Projects/assembly-workshop')
OUT = ROOT/'outputs/Hue_Pi4_M6_2026-10-28'
WORK = ROOT/'work/hue-pi4-m6-45'

def protected():
    paths = [ROOT/'outputs/Hue_Pi4_WideLane_2026-10-24', ROOT/'data/normal-use']
    paths += list((ROOT/'outputs').glob('CM1000*')) + list((ROOT/'outputs').glob('TL-SG108E*'))
    paths += [ROOT/'outputs/Mechanical_Design_App/equipment.py', ROOT/'outputs/Mechanical_Design_App/equipment_tray.scad', ROOT/'tools/plate_layout_stl.py', ROOT/'outputs/Mechanical_Design_App/print_layout.py']
    result = {}
    for p in paths:
        for f in ([p] if p.is_file() else sorted(p.rglob('*'))):
            if f.is_file(): result[f.relative_to(ROOT).as_posix()] = hashlib.sha256(f.read_bytes()).hexdigest()
    return result

assert not OUT.exists(), 'Do not overwrite existing revision'
WORK.mkdir(parents=True, exist_ok=False)
(WORK/'protected-before.json').write_text(json.dumps(protected(), indent=2), encoding='utf-8')
status = subprocess.run(['git','status','--short'],cwd=ROOT,capture_output=True,text=True,check=True).stdout
(WORK/'git-status-before.txt').write_text(status,encoding='utf-8')
src = OUT/'src'; src.mkdir(parents=True)
base = (ROOT/'outputs/Hue_Pi4_WideLane_2026-10-24/ext.scad').read_text(encoding='utf-8')
text = base
def replace(old,new):
    global text
    assert text.count(old)==1, (old, text.count(old))
    text=text.replace(old,new)

replace('slot_clear=0.3; boss_d=9; m3_clear=3.4; joint_pilot=4.0;  // 4.0 = the printed, well-fitting Pi4 trial',
        'slot_clear=0.3; boss_d=14; m3_clear=6.6; joint_pilot=7.6;  // HP4-M6-A: rack M6 insert bore and clearance')
generator=(ROOT/'outputs/Mechanical_Design_App/equipment_tray.scad').read_text(encoding='utf-8')
block=re.search(r'// @m6-begin\n.*?// @m6-end',generator,re.S).group()
block=block.replace('function jzx(x)=abs(x)<jo-1?[32]:[16,32];  // screw heights above tray_z',
                    'function jzx(x)=[24];  // HP4-M6-A: one screw at Z=32.225; boss top 39.225, tab top 42.225')
block=re.sub(r' // edge stiffening walls.*?\n}\nmodule m6_tray_joint_cut',
             ' // HP4-M6-A: edge walls omitted to preserve the keystone gap and wide cable lane.\n}\nmodule m6_tray_joint_cut',block,flags=re.S)
block=block.replace('translate([tray_x,-1,0])cube([tray_w,tray_d+2,60]);',
                    'translate([tray_x0,-1,0])cube([tray_x1-tray_x0,tray_d+2,60]);  // unchanged asymmetric floor bounds')
replace('\nmodule capsule2d', '\n'+block+'\n\nmodule capsule2d')
replace('for(x=joint_x)translate([x,0,tray_z+14])', 'for(x=joint_x,zz=jzx(x))translate([x,0,tray_z+zz])')
replace('for(x=joint_x)translate([x,-0.1,tray_z+14])', 'for(x=joint_x,zz=jzx(x))translate([x,-0.1,tray_z+zz])')
old=re.search(r'  for\(x=joint_x\) translate\(\[x-9.*?\n }\n}',text,re.S).group()[:-5]
# Replace just the three legacy tab/brace statements, retaining the enclosing joint guard.
start=text.index('  for(x=joint_x) translate([x-9')
end=text.index('\n }\n}',start)
text=text[:start]+'  m6_tray_joint_add();'+text[end:]
replace('  for(x=joint_x)translate([x,11.4,tray_z+14])rotate([90,0,0])cylinder(d=m3_clear,h=12);', '  m6_tray_joint_cut();')
replace('   plate_joint_cut();','   plate_joint_cut();\n   hp4_plate_id();')
replace('  lane_tie_cut();', '  lane_tie_cut();\n  hp4_tray_id();')
text+='''
// HP4-M6-A identification only: 0.6 mm engraved, away from functional features.
module hp4_plate_id(){translate([-35,0.01,8])rotate([90,0,0])linear_extrude(0.61)
 text("HP4-M6-A",size=4,font="Liberation Sans:style=Bold",halign="center");}
module hp4_tray_id(){translate([-35,119,floor_top-0.6])linear_extrude(0.61)
 text("HP4-M6-A",size=4,font="Liberation Sans:style=Bold",halign="center");}
'''
(src/'HP4-M6-A.scad').write_text(text,encoding='utf-8')
(WORK/'source.diff').write_text(''.join(difflib.unified_diff(base.splitlines(True),text.splitlines(True),fromfile='baseline/ext.scad',tofile='src/HP4-M6-A.scad')),encoding='utf-8')
print('Created source and preservation snapshot:',len(protected()),'protected files')
