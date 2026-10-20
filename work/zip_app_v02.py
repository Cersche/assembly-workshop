from pathlib import Path
import zipfile,json
root=Path('outputs/Mechanical_Design_App')
assert len(json.loads((root/'starter-hardware.json').read_text()))==6
assert 'button.onclick=()=>{' in (root/'index.html').read_text(encoding='utf-8')
with zipfile.ZipFile('outputs/Mechanical_Design_App_Beta_0_2.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in root.iterdir():
  if p.is_file():z.write(p,Path(root.name)/p.name)
with zipfile.ZipFile('outputs/Mechanical_Design_App_Beta_0_2.zip') as z:
 assert z.testzip() is None
 print('Validated beta 0.2 package:',len(z.namelist()),'files')
