"""Refresh the one edited front-end asset using the manifest's LF hashing contract."""
import json
import hashlib
from pathlib import Path
app=Path(__file__).resolve().parents[2]/'outputs/Mechanical_Design_App'
p=app/'asset-manifest.json'
data=json.loads(p.read_text(encoding='utf-8'))
for row in data:
    if row['file']=='tray-placement.js':row['sha256']=hashlib.sha256((app/row['file']).read_text(encoding='utf-8').encode('utf-8')).hexdigest()
p.write_text(json.dumps(data,indent=1)+'\n',encoding='utf-8',newline='\n')
