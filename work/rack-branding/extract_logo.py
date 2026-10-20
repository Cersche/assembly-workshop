"""Recover original painted face IDs, without changing any source geometry."""
from pathlib import Path
import hashlib
import json
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[2]
assets = ROOT / 'outputs/Mechanical_Design_App/rack-references'
source = ROOT / 'work/rack-geometry-recovery/sources/5U+Lab+Rax+X2D.3mf'
member = '3D/Objects/object_171.model'
with zipfile.ZipFile(source) as archive:
    model = ET.fromstring(archive.read(member))
vertices = [[float(v.attrib[k]) for k in ('x', 'y', 'z')] for v in model.iter() if v.tag.endswith('}vertex')]
triangles = [t for t in model.iter() if t.tag.endswith('}triangle')]
mesh = json.loads((assets / 'component_1_23.json').read_text(encoding='utf-8'))
assert vertices == mesh['vertices']
assert [[int(t.attrib[k]) for k in ('v1', 'v2', 'v3')] for t in triangles] == mesh['triangles']
faces = [i for i, t in enumerate(triangles) if t.get('paint_color') == '8']
assert len(faces) == 448
record = {'source': source.name, 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
          'member': member, 'component': 'component_1_23.json', 'triangle_count': len(triangles),
          'paint_color': '8', 'triangles': faces, 'scope': 'Original source painted logo faces; preview colors only'}
(assets / 'rack-logo-faces.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
print('Exact source/inspection correspondence verified; 448 original painted faces recovered')
