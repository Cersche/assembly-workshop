from pathlib import Path
import json,hashlib
app=Path(r'D:\Projects\assembly-workshop\outputs\Mechanical_Design_App')
p=app/'equipment_tray.scad';t=p.read_text(encoding='utf-8').replace('len(search([side],wall_open))>0','len([for(o=wall_open)if(o==side)o])>0').replace('len(search([s],wall_open))>0','len([for(o=wall_open)if(o==s)o])>0');p.write_text(t,encoding='utf-8',newline='\n')
print('SCAD membership fixed')
