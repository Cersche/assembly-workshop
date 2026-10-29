from pathlib import Path
import hashlib,json,subprocess
R=Path('D:/Projects/assembly-workshop');W=R/'work/hue-pi4-m6-47';O=R/'outputs/Hue_Pi4_M6-B_2026-10-28'
before=json.loads((W/'protected-before.json').read_text(encoding='utf-8'))
paths=[R/'tools',R/'data/normal-use',R/'outputs/Final_3MF',R/'outputs/Mechanical_Design_App/equipment.py',R/'outputs/Mechanical_Design_App/equipment_tray.scad',R/'outputs/Mechanical_Design_App/print_layout.py']
for pat in ['Hue_Pi4*','CM1000*','TL-SG108E*','Hard_Drive*','OptiPlex*','Physical_Test_Coupons*','STL_Deliveries']:
 paths.extend(p for p in (R/'outputs').glob(pat) if p!=O)
paths.append(Path('C:/Users/brian/Downloads/Swanky Rottis.stl'))
files=set()
for p in paths:
 if p.is_file():files.add(p)
 elif p.is_dir():files.update(f for f in p.rglob('*') if f.is_file())
after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
(W/'protected-after.json').write_text(json.dumps(after,indent=2),encoding='utf-8')
changed=[p for p in before.keys()&after.keys() if before[p]!=after[p]];missing=sorted(before.keys()-after.keys());added=sorted(after.keys()-before.keys())
result={'files_before':len(before),'files_after':len(after),'changed':changed,'missing':missing,'added':added};(W/'preservation-result.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result))
assert before==after
status=subprocess.run(['git','status','--short'],cwd=R,capture_output=True,text=True,check=True).stdout
(W/'git-status-after.txt').write_text(status,encoding='utf-8');old=(W/'git-status-before.txt').read_text(encoding='utf-8').splitlines()
new=[s for s in status.splitlines() if s not in old]
allowed=['HANDOFF.md','work/codex-tasks/47-hue-pi4-m6-b-REPORT.md','work/hue-pi4-m6-47/','outputs/Hue_Pi4_M6-B_2026-10-28/']
assert all(any(line[3:].startswith(p) for p in allowed) for line in new),new
assert all(line in status.splitlines() for line in old),'Pre-existing status entry disappeared'
print('New status entries:',new)
p=R/'work/codex-tasks/47-hue-pi4-m6-b-REPORT.md';s=p.read_text(encoding='utf-8').replace('Python 3.10.11','Python 3.10.4');p.write_text(s,encoding='utf-8')
# Preserve an output digest manifest for the exact source/mesh/package delivered.
manifest={p.relative_to(O).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(O.rglob('*')) if p.is_file()}
(W/'output-sha256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Output files:',len(manifest))
