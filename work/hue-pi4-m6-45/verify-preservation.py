from pathlib import Path
import hashlib,json,subprocess,re,difflib
R=Path('D:/Projects/assembly-workshop'); O=R/'outputs/Hue_Pi4_M6_2026-10-28'; W=R/'work/hue-pi4-m6-45'
before=json.loads((W/'protected-before.json').read_text(encoding='utf-8'))
after={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in before}
assert before==after
(W/'protected-after.json').write_text(json.dumps(after,indent=2),encoding='utf-8')
base=(R/'outputs/Hue_Pi4_WideLane_2026-10-24/ext.scad').read_text(encoding='utf-8')
source=(O/'src/HP4-M6-A.scad').read_text(encoding='utf-8')
# Compare unchanged source outside the explicitly allowed joint modules / ID call sites.
def remove_module(text,name):
    start=text.index('module '+name+'('); brace=text.index('{',start);depth=1;i=brace+1
    while depth:
        depth+=(text[i]=='{')-(text[i]=='}');i+=1
    return text[:start]+text[i:]
a=base;b=re.sub(r'\n// @m6-begin\n.*?// @m6-end\n','',source,flags=re.S)
b=b.split('\n// HP4-M6-A identification only:')[0]+'\n'
b=b.replace('   hp4_plate_id();\n','').replace('  hp4_tray_id();\n','')
b=b.replace('slot_clear=0.3; boss_d=14; m3_clear=6.6; joint_pilot=7.6;  // HP4-M6-A: rack M6 insert bore and clearance',
            'slot_clear=0.3; boss_d=9; m3_clear=3.4; joint_pilot=4.0;  // 4.0 = the printed, well-fitting Pi4 trial')
for name in ['plate_joint_add','plate_joint_cut','tray_joint_add','tray_joint_cut']:
    a=remove_module(a,name);b=remove_module(b,name)
assert a.strip()==b.strip(), 'Changes outside allowed joint/ID regions'
(W/'source.diff').write_text(''.join(difflib.unified_diff(base.splitlines(True),source.splitlines(True),fromfile='baseline/ext.scad',tofile='src/HP4-M6-A.scad')),encoding='utf-8')
status=subprocess.run(['git','status','--short'],cwd=R,capture_output=True,text=True,check=True).stdout
(W/'git-status-after.txt').write_text(status,encoding='utf-8')
assert not any(p in status for p in ('outputs/Hue_Pi4_WideLane_2026-10-24/','outputs/CM1000','outputs/TL-SG108E','data/normal-use/','outputs/Mechanical_Design_App/'))
print('PASS: protected SHA-256 unchanged:',len(before),'files; source scope passed; protected git status clean')
subprocess.run(['python',str(R/'tools/mesh_viewer.py'),str(O/'HP4-M6-A_tray.stl'),str(O/'HP4-M6-A_faceplate.stl'),'--as-is','-o',str(R/'work/mesh-viewer/HP4-M6-A_assembled.html'),'-t','HP4-M6-A assembled — pending contact-check decision'],check=True)
subprocess.run(['python',str(R/'tools/mesh_viewer.py'),str(R/'outputs/Hue_Pi4_WideLane_2026-10-24/HuePi4_widelane_tray.stl'),str(R/'outputs/Hue_Pi4_WideLane_2026-10-24/HuePi4_widelane_faceplate.stl'),'-o',str(R/'work/mesh-viewer/HP4-M6-A_baseline.html'),'-t','Immutable Hue + Pi 4 wide-lane baseline'],check=True)
