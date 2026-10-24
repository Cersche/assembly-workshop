from pathlib import Path
import sys,json,hashlib,shutil
root=Path(r'D:\Projects\assembly-workshop'); app=root/'outputs/Mechanical_Design_App'
out=root/'work/wall-device-42';out.mkdir(exist_ok=False)
sys.path.insert(0,str(app));import equipment as eq
shutil.copy2(root/'data/normal-use/equipment-library.json',out/'library-readonly-copy.json')
fixtures=[]
for i in json.loads((app/'equipment-examples.json').read_text(encoding='utf-8')):
 fixtures.append((f"example:{i['name']}",i['spec']))
for i in json.loads((out/'library-readonly-copy.json').read_text(encoding='utf-8')):
 fixtures.append((f"library:{i['name']}",i['spec']))
for p in sorted((root/'outputs').glob('Physical_Test_Coupons*/*spec*.json')):
 fixtures.append((p.stem,json.loads(p.read_text(encoding='utf-8'))))
base=dict(name='legacy sleeve',dev_w=120,dev_d=100,dev_h=25,device_mount='sleeve',joint='screw',u=1)
fixtures.extend([('plain sleeve',base),('flat',dict(base,device_mount='flat'))])
pi=json.loads((app/'equipment-examples.json').read_text(encoding='utf-8'))[0]['spec']
fixtures.append(('pair',dict(pi,dev_off_x=-45,keystones=[],ports=[],second=dict(pi,dev_off_x=45,keystones=[],ports=[]))))
records=[]
for label,spec in fixtures:
 s=eq.clean(spec);src=eq.source(s)
 records.append(dict(label=label,spec=spec,before=hashlib.sha256(src.encode('utf-8')).hexdigest()))
(out/'legacy-before.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
files=['equipment.py','equipment_tray.scad','port_openings.py','port-openings.js','clearance.js','cable-ports.js','tray-placement.js','equipment-wizard.js','tray-pair.js','asset-manifest.json','run_checks.ps1']
(out/'before-files').mkdir()
for f in files:shutil.copy2(app/f,out/'before-files'/f)
print('Captured',len(records),'legacy sources;',len(json.loads((out/'library-readonly-copy.json').read_text(encoding='utf-8'))),'library items; seven coupon specs.')
