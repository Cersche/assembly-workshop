"""Read-only HTTP verification; prints no page/session-token contents."""
from pathlib import Path
import hashlib
import json
import urllib.request

ROOT=Path(__file__).resolve().parents[2]
APP=ROOT/'outputs/Mechanical_Design_App'
results=[]
for port in [8765,8767]:
    for route,file in [('/',None),('/rack-references/rack-scene.js','rack-references/rack-scene.js'),('/rack-references/rack-studio.js','rack-references/rack-studio.js'),('/workspace.js','workspace.js')]:
        with urllib.request.urlopen('http://127.0.0.1:'+str(port)+route,timeout=10) as response:
            body=response.read()
            item={'port':port,'route':route,'status':response.status,'sha256':hashlib.sha256(body).hexdigest()}
            if file:
                expected=(APP/file).read_bytes() if route.startswith('/rack-references/') else (APP/file).read_text(encoding='utf-8').encode('utf-8')
                item['matches_disk']=body==expected
                assert item['matches_disk'],route
            else:
                assert b'/rack-references/rack-studio.js' in body
            results.append(item)
destination=Path(__file__).parent/'HTTP_Checks.json'
destination.write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
print('PASS 8 read-only HTTP checks; normal and disposable servers deliver the current matching renderer assets.')
