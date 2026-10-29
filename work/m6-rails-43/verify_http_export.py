"""Explicit final HTTP export acceptance against task-43 disposable server only."""
import hashlib
import io
import json
from pathlib import Path
import re
import urllib.request
import zipfile
import xml.etree.ElementTree as ET

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
base='http://127.0.0.1:8819'
page=urllib.request.urlopen(base,timeout=15).read().decode('utf-8')
token=re.search(r"const token='([^']+)'",page).group(1)
spec=json.loads((HERE/'cm6b-spec.json').read_text(encoding='utf-8'))
req=urllib.request.Request(base+'/api/equipment-build',data=json.dumps(spec).encode('utf-8'),headers={'Content-Type':'application/json','X-App-Token':token},method='POST')
raw=urllib.request.urlopen(req,timeout=180).read()
(HERE/'final-http-export.zip').write_bytes(raw)
with zipfile.ZipFile(io.BytesIO(raw)) as z:
    trace=json.loads(z.read('export.json'))
    report=json.loads(z.read('revision.json'))
    matches={}
    names=dict(faceplate='CM6B_faceplate_with_stubs',rail_l='CM6B_rail_left',rail_r='CM6B_rail_right')
    for part,stem in names.items():
        matches[part]=z.read(part+'.stl')==(ROOT/'outputs/CM1000_M6_generated_2026-10-28'/(stem+'.stl')).read_bytes()
    mf=next(n for n in z.namelist() if n.endswith('.3mf'))
    with zipfile.ZipFile(io.BytesIO(z.read(mf))) as three:
        model=ET.fromstring(three.read('3D/3dmodel.model'))
    ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
    result=dict(parts=report['parts'],all_stls_match_delivery=all(matches.values()),matches=matches,
                source_matches=z.read('equipment.scad')==(ROOT/'outputs/CM1000_M6_generated_2026-10-28/CM6B_source.scad').read_bytes(),
                source_sha256=trace['source_sha256'],objects_in_3mf=len(model.findall('m:resources/m:object',ns)))
(HERE/'final-http-export-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
assert result['all_stls_match_delivery'] and result['source_matches'] and result['objects_in_3mf']==3
