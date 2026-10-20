"""Read-only runtime diagnostics. Does not print session tokens or user records."""
import urllib.request
import urllib.error
import json
import hashlib
from pathlib import Path
results=[]
for port in [8765,8767]:
    for route in ['/workspace.css?v=4','/workspace.css','/api/workspace-capabilities']:
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{port}'+route,timeout=8) as response:
                body=response.read();row={'port':port,'route':route,'status':response.status,'mime':response.headers.get('Content-Type'),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
                if route.endswith('capabilities'):row['capabilities']=json.loads(body)
        except urllib.error.HTTPError as e:row={'port':port,'route':route,'status':e.code}
        results.append(row)
Path(__file__).with_name('Runtime_Diagnostics.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
