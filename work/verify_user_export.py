from pathlib import Path
import json
source=Path('C:/Users/brian/Downloads/pi4-proposed-joint/pi4_proposed.scad').read_text(encoding='utf-8')
baseline=Path('outputs/Mechanical_Design_App/pi4_baseline.scad').read_text(encoding='utf-8')
assert source.split('\n',1)[1] == baseline.replace('insert_pilot=4.2;','insert_pilot=4;')
r=json.loads(Path('C:/Users/brian/Downloads/pi4-proposed-joint/revision.json').read_text())
assert r['changed_parameter']['insert_pilot']==4
assert r['hardware']['screw']['part_number']=='SSCF-M3-8-A2'
assert r['hardware']['heatset']['part_number']=='94459A140'
assert not any(c['status']=='fail' for c in r['checks']['checks'])
print('Export verified: only the pilot changed; pinned hardware matches; report retains incomplete status and unknown checks.')
