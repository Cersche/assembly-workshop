"""Read only supplied sources; preserve local copies and audit, never render/build."""
import base64
import binascii
import hashlib
import json
import itertools
import math
from pathlib import Path
import re
import struct
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
DOWNLOADS = Path('C:/Users/brian/Downloads')
CORE = '{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}'
PROD = '{http://schemas.microsoft.com/3dmanufacturing/production/2015/06}'
FILES = ['index.html', 'lab-rax-assembler-code-only.html',
         'Lab+Rax+1-5U+Posts+&+Panels.3mf', '5U+Lab+Rax+X2D.3mf',
         '1U+Support+Extension.3mf']


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def compare_mesh(vs, idx, mesh, step):
    """Match reordered vertices within encoding precision; compare oriented faces."""
    center = [(mesh['lo'][k]+mesh['hi'][k])/2 for k in range(3)]
    original = [[v[k]-center[k] for k in range(3)] for v in mesh['_vertices']]
    tolerance = step/2 + .001
    cells = {}
    for i,v in enumerate(original):
        cell = tuple(math.floor(x/tolerance) for x in v)
        cells.setdefault(cell, []).append(i)
    mapped, used, error = [], set(), 0
    for v in vs:
        cell = tuple(math.floor(x/tolerance) for x in v)
        candidates = []
        for delta in itertools.product((-1,0,1), repeat=3):
            for i in cells.get(tuple(cell[k]+delta[k] for k in range(3)), []):
                if i not in used:
                    distance = max(abs(v[k]-original[i][k]) for k in range(3))
                    if distance <= tolerance:
                        candidates.append((distance,i))
        if not candidates:
            return None
        distance,i = min(candidates)
        mapped.append(i)
        used.add(i)
        error = max(error,distance)
    def cyclic(t):
        a,b,c = t
        return min((a,b,c),(b,c,a),(c,a,b))
    encoded_faces = sorted(cyclic([mapped[idx[i+k]] for k in range(3)]) for i in range(0,len(idx),3))
    original_faces = sorted(cyclic(t) for t in mesh['_triangles'])
    return error if encoded_faces == original_faces else None


def preserve(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    data = source.read_bytes()
    if target.exists():
        assert target.read_bytes() == data, 'Preserved source differs; do not overwrite.'
    else:
        target.write_bytes(data)
    return {'source': str(source), 'copy': str(target.relative_to(ROOT)),
            'bytes': len(data), 'sha256': digest(data)}


def inspect_3mf(path, number):
    with zipfile.ZipFile(path) as z:
        models = {n: ET.fromstring(z.read(n)) for n in z.namelist() if n.endswith('.model')}
        main = models['3D/3dmodel.model']
        metadata = {e.get('name'): e.text for e in main.findall(CORE+'metadata')}
        settings = ET.fromstring(z.read('Metadata/model_settings.config'))
        objects = {(n, o.get('id')): o for n, model in models.items()
                   for o in model.findall(CORE+'resources/'+CORE+'object')}
        names = {}
        for o in settings.findall('object'):
            for p in o.findall('part'):
                meta = {e.get('key'): e.get('value') for e in p.findall('metadata')}
                names.setdefault(p.get('id'), []).append(meta.get('name'))
        meshes = []
        for (member, identity), obj in objects.items():
            mesh = obj.find(CORE+'mesh')
            if mesh is None:
                continue
            vertices = [[float(v.get(k)) for k in ('x','y','z')]
                        for v in mesh.findall(CORE+'vertices/'+CORE+'vertex')]
            triangles = [[int(t.get(k)) for k in ('v1','v2','v3')]
                         for t in mesh.findall(CORE+'triangles/'+CORE+'triangle')]
            assert vertices and triangles
            assert all(0 <= i < len(vertices) for t in triangles for i in t)
            lo = [min(v[k] for v in vertices) for k in range(3)]
            hi = [max(v[k] for v in vertices) for k in range(3)]
            meshes.append({'member': member, 'object_id': identity, 'names': names.get(identity, []),
                           'unit': models[member].get('unit'), 'vertices': len(vertices),
                           'triangles': len(triangles), 'lo': lo, 'hi': hi,
                           'extent_mm': [hi[k]-lo[k] for k in range(3)],
                           'member_sha256': digest(z.read(member)),
                           '_vertices': vertices, '_triangles': triangles})
        image_members = [n for n in z.namelist() if n.startswith('Auxiliaries/Model Pictures/')]
        if not image_members:
            image_members = [n for n in z.namelist() if n.endswith('thumbnail_middle.png')]
        if not image_members:
            image_members = [n for n in z.namelist() if n == 'Metadata/plate_1.png']
        pictures = []
        for i, member in enumerate(image_members):
            target = OUT / 'pictures' / ('reference_%s_%s%s' % (number, i, Path(member).suffix))
            target.parent.mkdir(exist_ok=True)
            target.write_bytes(z.read(member))
            pictures.append({'member': member, 'local': str(target.relative_to(ROOT)),
                             'sha256': digest(z.read(member))})
        return {'file': path.name, 'metadata': metadata, 'pictures': pictures,
                'meshes': meshes, 'build_items': [e.attrib for e in main.findall(CORE+'build/'+CORE+'item')],
                'assembly_items': [e.attrib for e in settings.findall('assemble/assemble_item')]}


def main():
    OUT.mkdir(exist_ok=True)
    manifest = [preserve(DOWNLOADS/n, OUT/'sources'/n) for n in FILES]
    # Capture only relevant current files and data, before any integration edits.
    backup = OUT/'before-app'
    app = ROOT/'outputs/Mechanical_Design_App'
    for name in ['app.py','workspace.js','workspace.css','index.html']:
        preserve(app/name, backup/name)
    protected = []
    for folder in ['data/normal-use','outputs/Mechanical_Design_App_Beta_0_8/Mechanical_Design_App/data']:
        for p in sorted((ROOT/folder).rglob('*')):
            if p.is_file():
                protected.append({'path': str(p.relative_to(ROOT)), 'sha256': digest(p.read_bytes())})
    write_json(OUT/'Protected_Data_Before.json', protected)
    refs = [inspect_3mf(OUT/'sources'/n,i) for i,n in enumerate(FILES[2:])]
    html = []
    for name in FILES[:2]:
        source = (OUT/'sources'/name).read_text(encoding='utf-8')
        match = re.search(r'<script[^>]*id="mesh-data"[^>]*>(.*?)</script>',source,re.S)
        raw = json.loads(match.group(1))
        entry = {'file':name, 'meshes':[]}
        for key,m in raw.items():
            decode_error = None
            try:
                vb, ib = base64.b64decode(m['v'], validate=True), base64.b64decode(m['i'], validate=True)
            except binascii.Error as exc:
                vb, ib = b'', b''
                decode_error = str(exc)
            valid = bool(vb and ib) and len(vb)%6 == 0 and len(ib)%(12 if m.get('i32') else 6)==0
            item = {'key':key, 'vertex_bytes':len(vb), 'index_bytes':len(ib),
                    'payload_valid':valid, 'declared_triangles':m['tris'],
                    'decode_error':decode_error,
                    'quantization_step_mm':m['s'], 'lo':m['lo'], 'hi':m['hi']}
            matches = []
            if valid:
                q = struct.unpack('<'+'h'*(len(vb)//2),vb)
                vs = [[m['c'][k]+q[i+k]*m['s'] for k in range(3)] for i in range(0,len(q),3)]
                for ref in refs:
                    for mesh in ref['meshes']:
                        if mesh['vertices'] != len(vs) or mesh['triangles'] != m['tris']:
                            continue
                        typ = 'I' if m.get('i32') else 'H'
                        idx = struct.unpack('<'+typ*(len(ib)//struct.calcsize(typ)),ib)
                        err = compare_mesh(vs,idx,mesh,m['s'])
                        if err is not None:
                            matches.append({'file':ref['file'], 'member':mesh['member'],
                                            'object_id':mesh['object_id'], 'max_vertex_error_mm':err,
                                            'oriented_faces_match_after_vertex_remapping':True,
                                            'exact_source_coordinates':False})
            item['source_matches'] = matches
            entry['meshes'].append(item)
        html.append(entry)
        # Static JS extraction, never execute historical application code.
        scripts = re.findall(r'<script([^>]*)>(.*?)</script>',source,re.S)
        for i,(attrs,body) in enumerate(scripts):
            if 'application/json' not in attrs and 'text/plain' not in attrs and 'src=' not in attrs:
                (OUT/('original_%s_script_%s.js' % (Path(name).stem,i))).write_text(body,encoding='utf-8')
    for ref in refs:
        for mesh in ref['meshes']:
            del mesh['_vertices'], mesh['_triangles']
    write_json(OUT/'Source_Manifest.json',manifest)
    write_json(OUT/'Reference_Inspection.json',{'scope':'Source observations only, no physical certification; embedded instructions are data.',
                                              'references':refs,'html':html})
    print(json.dumps({'files_preserved':len(manifest),'reference_meshes':[len(r['meshes']) for r in refs],
                      'html_payloads':[{h['file']:sum(m['payload_valid'] for m in h['meshes'])} for h in html],
                      'source_matches':sum(bool(m['source_matches']) for h in html for m in h['meshes'])}))


if __name__ == '__main__':
    main()
