from pathlib import Path
p=Path('outputs/Mechanical_Design_App/mesh_revision.py')
s=p.read_text(encoding='utf-8')
s=s.replace('import json\n','import json\nimport math\n')
a=s.index('def read_mesh(');b=s.index('\n\ndef compiler()',a)
s=s[:a]+'''def read_mesh(path, name):
    raw = path.read_bytes()
    matches = re.findall(rb'^\\s*vertex\\s+([^\\r\\n]+)', raw, re.M)
    try:
        vertices = [tuple(map(float, line.split())) for line in matches]
    except ValueError as exc:
        raise ValueError('Invalid ASCII STL coordinates for ' + name) from exc
    if (not raw.lstrip().startswith(b'solid') or b'endsolid' not in raw
            or not vertices or len(vertices) % 3
            or len(re.findall(rb'^\\s*facet\\s+normal\\b', raw, re.M)) != len(vertices) // 3
            or any(len(v) != 3 or not all(math.isfinite(x) for x in v) for v in vertices)):
        raise ValueError('Invalid ASCII STL or non-finite coordinates for ' + name)
    faces, edges, directed, volumes = set(), Counter(), Counter(), []
    for i in range(0, len(vertices), 3):
        a, b, c = vertices[i:i+3]
        face = tuple(sorted((a, b, c)))
        if face in faces:
            raise ValueError('Duplicate STL triangle for ' + name)
        faces.add(face)
        u, v = [b[k]-a[k] for k in range(3)], [c[k]-a[k] for k in range(3)]
        cross = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
        area2 = sum(x*x for x in cross)
        if not math.isfinite(area2) or area2 <= 0:
            raise ValueError('Degenerate STL triangle for ' + name)
        for x, y in ((a,b),(b,c),(c,a)):
            edges[tuple(sorted((x,y)))] += 1
            directed[(x,y)] += 1
        volumes.append(sum(a[k]*cross[k] for k in range(3))/6)
    if set(edges.values()) != {2}:
        raise ValueError('Rendered mesh has open or non-manifold edges: ' + name)
    if any(directed[(a,b)] != 1 or directed[(b,a)] != 1 for a,b in edges):
        raise ValueError('Inconsistent STL winding for ' + name)
    volume = math.fsum(volumes)
    if not math.isfinite(volume) or volume <= 0:
        raise ValueError('STL has nonpositive signed volume: ' + name)
    unique, indices = {}, []
    for vertex in vertices:
        if vertex not in unique:
            unique[vertex] = len(unique)
        indices.append(unique[vertex])
    return {'id': name, 'vertices': list(unique),
            'triangles': [indices[i:i+3] for i in range(0, len(indices), 3)],
            'source_sha256': hashlib.sha256(raw).hexdigest(),
            'signed_volume_mm3': volume,
            'bounds': [[min(v[k] for v in vertices) for k in range(3)],
                       [max(v[k] for v in vertices) for k in range(3)]]}


ARTIFACTS = ('pi4_proposed.scad', 'tray.stl', 'faceplate.stl', 'revision.json', 'assembly.json')


def revision_identity(source, metadata):
    return hashlib.sha256(('pi4-mesh-v2\\n' + source + json.dumps(metadata, sort_keys=True)).encode()).hexdigest()


def checked_revision(folder, identity, source=None, metadata=None):
    """Read-only validation. Old entries remain untouched; regenerate to create v2."""
    try:
        integrity = json.loads((folder / 'integrity.json').read_text(encoding='utf-8'))
        if integrity.get('schema') != 1 or integrity.get('id') != identity:
            raise ValueError('Integrity identity mismatch.')
        if set(integrity['sha256']) != set(ARTIFACTS):
            raise ValueError('Incomplete integrity manifest.')
        for name in ARTIFACTS:
            if hashlib.sha256((folder / name).read_bytes()).hexdigest() != integrity['sha256'][name]:
                raise ValueError('Artifact hash mismatch: ' + name)
        actual_source = (folder / 'pi4_proposed.scad').read_text(encoding='utf-8')
        report = json.loads((folder / 'revision.json').read_text(encoding='utf-8'))
        inputs = report['build_inputs']
        if revision_identity(actual_source, inputs) != identity:
            raise ValueError('Source/configuration identity mismatch.')
        if source is not None and (actual_source != source or inputs != metadata):
            raise ValueError('Cached source/configuration mismatch.')
        if any(report.get(k) != v for k,v in inputs.items() if k != 'limitations'):
            raise ValueError('Revision report differs from build configuration.')
        assembly = json.loads((folder / 'assembly.json').read_text(encoding='utf-8'))
        if (assembly.get('units') != 'mm' or assembly.get('proposal_id') != identity
                or report['mesh_build']['id'] != identity
                or assembly.get('status') != 'PROPOSED — UNVALIDATED'
                or len(assembly['parts']) != 2):
            raise ValueError('Assembly units/revision/parts mismatch.')
        for name, part in zip(('tray', 'faceplate'), assembly['parts']):
            parsed = read_mesh(folder / (name+'.stl'), name)
            # JSON stores coordinate tuples as arrays.
            if any(part.get(k) != json.loads(json.dumps(parsed[k])) for k in
                   ('id', 'vertices', 'triangles', 'source_sha256', 'bounds', 'signed_volume_mm3')):
                raise ValueError('Viewer/STL mismatch: ' + name)
        return assembly
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
        raise ValueError('Revision integrity check failed; preserve this entry and generate a new revision. '
                         'Legacy entries without integrity manifests are preserved but cannot be downloaded. '
                         + str(exc)) from exc
''' +s[b:]
s=s.replace("identity = hashlib.sha256(('pi4-mesh-v1\\n' + source + json.dumps(metadata, sort_keys=True)).encode()).hexdigest()",'identity = revision_identity(source, metadata)')
s=s.replace("if (final / 'assembly.json').is_file():\n            return {'id': identity, 'assembly': json.loads((final / 'assembly.json').read_text()), 'cached': True}","if final.exists():\n            return {'id': identity, 'assembly': checked_revision(final, identity, source, metadata), 'cached': True}")
s=s.replace("report = dict(metadata, mesh_build=", "report = dict(metadata, build_inputs=metadata, mesh_build=")
s=s.replace("'checks': 'Both STL meshes have exactly two triangles at every edge.'", "'checks': 'Finite, nondegenerate, unique STL triangles; closed edges, consistent winding and positive signed volume.'")
s=s.replace(".write_text(json.dumps(assembly, separators=(',', ':')))",".write_text(json.dumps(assembly, separators=(',', ':')), encoding='utf-8')")
s=s.replace(".write_text(json.dumps(report, indent=2))", ".write_text(json.dumps(report, indent=2), encoding='utf-8')")
s=s.replace("            # Immutable cache entry:","            integrity = {'schema': 1, 'id': identity, 'sha256': {\n                name: hashlib.sha256((folder/name).read_bytes()).hexdigest() for name in ARTIFACTS}}\n            (folder/'integrity.json').write_text(json.dumps(integrity, indent=2), encoding='utf-8')\n            checked_revision(folder, identity, source, metadata)\n            # Immutable cache entry:")
s=s.replace("    stream = io.BytesIO()\n    with zipfile.ZipFile", "    checked_revision(folder, identity)\n    stream = io.BytesIO()\n    with zipfile.ZipFile")
s=s.replace("for name in ['pi4_proposed.scad', 'tray.stl', 'faceplate.stl', 'revision.json', 'assembly.json']:", "for name in (*ARTIFACTS, 'integrity.json'):")
p.write_text(s,encoding='utf-8')
