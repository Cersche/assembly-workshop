from pathlib import Path
import zipfile
root=Path('outputs/Mechanical_Design_App')
with zipfile.ZipFile('outputs/Mechanical_Design_App_Beta_0_1.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in root.iterdir():
  if p.is_file():z.write(p,Path(root.name)/p.name)
with zipfile.ZipFile('outputs/Mechanical_Design_App_Beta_0_1.zip') as z:
 assert z.testzip() is None
 print('Validated package:',len(z.namelist()),'files')
