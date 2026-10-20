"""Render constrained Pi4 proposals with the user's local OpenSCAD CLI."""
from collections import Counter
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import threading
import zipfile

LOCK = threading.Lock()


def read_mesh(path, name):
    raw = path.read_bytes()
    matches = re.findall(rb'^\s*vertex\s+([^\r\n]+)', raw, re.M)
    try:
        vertices = [tuple(map(float, line.split())) for line in matches]
    except ValueError as exc:
        raise ValueError('Invalid ASCII STL coordinates for ' + name) from exc
    if (not raw.lstrip().startswith(b'solid') or b'endsolid' not in raw
            or not vertices or len(vertices) % 3
            or len(re.findall(rb'^\s*facet\s+normal\b', raw, re.M)) != len(vertices) // 3
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


def normalize_collinear_faces(path):
    """Retriangulate only exact zero-area faces with a strict interior vertex.

    Remove the empty triangle and split its unique long-edge neighbor at the
    existing middle vertex. No coordinate is added or moved; all surface area
    and winding belong to the same original neighboring triangle.
    """
    raw = path.read_bytes()
    vertices = [tuple(map(float, line.split())) for line in
                re.findall(rb'^\s*vertex\s+([^\r\n]+)', raw, re.M)]
    if (not vertices or len(vertices)%3 or any(len(v)!=3 or not all(math.isfinite(x) for x in v) for v in vertices)):
        raise ValueError('Cannot normalize malformed STL.')
    faces = [vertices[i:i+3] for i in range(0,len(vertices),3)]
    def normal(face):
        a,b,c=face;u=[b[k]-a[k] for k in range(3)];v=[c[k]-a[k] for k in range(3)]
        return (u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
    repairs=[]
    while True:
        index=next((i for i,f in enumerate(faces) if normal(f)==(0,0,0)),None)
        if index is None:break
        face=faces[index]
        if len(set(face))!=3:raise ValueError('Repeated-vertex STL face cannot be normalized safely.')
        a,b=max(((face[i],face[j]) for i,j in ((0,1),(1,2),(2,0))),key=lambda pair:sum((pair[1][k]-pair[0][k])**2 for k in range(3)))
        middle=next(v for v in face if v!=a and v!=b)
        if sum((middle[k]-a[k])*(middle[k]-b[k]) for k in range(3))>=0:
            raise ValueError('Collinear vertex is not strictly inside the edge.')
        neighbors=[(i,j) for i,f in enumerate(faces) if i!=index for j in range(3)
                   if {f[j],f[(j+1)%3]}=={a,b}]
        if len(neighbors)!=1:raise ValueError('Collinear face has no unique edge neighbor.')
        neighbor,j=neighbors[0];f=faces[neighbor];x,y,z=f[j],f[(j+1)%3],f[(j+2)%3]
        split=[[x,middle,z],[middle,y,z]];old_normal=normal(f)
        if any(sum(n[k]*old_normal[k] for k in range(3))<=0 for n in map(normal,split)):
            raise ValueError('Collinear repair would change face orientation.')
        repairs.append({'long_edge':[a,b],'existing_middle_vertex':middle})
        faces=[f for i,f in enumerate(faces) if i not in (index,neighbor)]+split
    if repairs:
        lines=['solid normalized_export']
        for face in faces:
            n=normal(face);length=math.sqrt(sum(x*x for x in n))
            lines+=['facet normal '+' '.join(format(x/length,'.17g') for x in n),'outer loop']
            lines+=['vertex '+' '.join(format(x,'.17g') for x in vertex) for vertex in face]
            lines+=['endloop','endfacet']
        path.write_text('\n'.join(lines+['endsolid normalized_export','']),encoding='ascii',newline='\n')
    return {'method':'exact-collinear-neighbor-split-v1','renderer_sha256':hashlib.sha256(raw).hexdigest(),
            'output_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'repairs':repairs,
            'scope':'Export triangulation only. Existing coordinates and neighboring surface preserved; no dimensions changed.'}


ARTIFACTS = ('pi4_proposed.scad', 'tray.stl', 'faceplate.stl', 'revision.json', 'assembly.json')


def revision_identity(source, metadata):
    return hashlib.sha256(('pi4-mesh-v2-triangulation1\n' + source + json.dumps(metadata, sort_keys=True)).encode()).hexdigest()


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
            if report['mesh_processing'][name]['output_sha256'] != integrity['sha256'][name+'.stl']:
                raise ValueError('Processing/STL hash mismatch: ' + name)
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


def compiler():
    candidates = [os.environ.get('OPENSCAD_EXE'), shutil.which('openscad'),
                  'C:/Program Files/OpenSCAD/openscad.exe']
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(Path(candidate).resolve())
    raise ValueError('OpenSCAD is needed for mesh generation. Install it or set OPENSCAD_EXE to its executable. Source-only export remains available.')


def build(source, metadata, data_dir):
    identity = revision_identity(source, metadata)
    root = Path(data_dir) / 'revisions'
    final = root / identity
    with LOCK:
        if final.exists():
            return {'id': identity, 'assembly': checked_revision(final, identity, source, metadata), 'cached': True}
        executable = compiler()
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root, prefix='render-') as temp:
            folder = Path(temp)
            src = folder / 'pi4_proposed.scad'
            src.write_text(source, encoding='utf-8', newline='\n')
            parts, logs, processing = [], {}, {}
            for name in ['tray', 'faceplate']:
                try:
                    result = subprocess.run([executable, '-o', str(folder / (name+'.stl')),
                                             '-D', f'part="{name}"', str(src)],
                                            capture_output=True, text=True, timeout=180,
                                            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
                except (OSError, subprocess.TimeoutExpired) as exc:
                    raise ValueError('Mesh rendering failed or timed out: ' + str(exc)) from exc
                logs[name] = result.stderr
                if result.returncode or 'ERROR:' in result.stderr:
                    raise ValueError('OpenSCAD failed for ' + name + ': ' + result.stderr[-1600:])
                processing[name] = normalize_collinear_faces(folder / (name+'.stl'))
                parts.append(read_mesh(folder / (name+'.stl'), name))
            report = dict(metadata, build_inputs=metadata, mesh_processing=processing, mesh_build={'id': identity, 'compiler': executable,
                          'checks': 'Finite, nondegenerate, unique STL triangles; closed edges, consistent winding and positive signed volume.', 'logs': logs},
                          mesh_limits='Mesh closure and successful rendering are not collision, strength or physical fit validation.')
            report['limitations'] = [line for line in metadata['limitations']
                                     if 'viewer still displays' not in line]
            report['limitations'].append('This package contains the generated proposal; the viewer can switch between it and baseline v2.')
            assembly = {'units': 'mm', 'revision': 'PROPOSED pilot '+str(metadata['changed_parameter']['insert_pilot'])+' mm'+(' · 4 corner mounts' if metadata.get('mounting_layout') else '')+' · '+identity[:8],
                        'parts': parts, 'proposal_id': identity, 'status': 'PROPOSED — UNVALIDATED'}
            (folder / 'assembly.json').write_text(json.dumps(assembly, separators=(',', ':')), encoding='utf-8')
            (folder / 'revision.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
            integrity = {'schema': 1, 'id': identity, 'sha256': {
                name: hashlib.sha256((folder/name).read_bytes()).hexdigest() for name in ARTIFACTS}}
            (folder/'integrity.json').write_text(json.dumps(integrity, indent=2), encoding='utf-8')
            checked_revision(folder, identity, source, metadata)
            # Immutable cache entry: every packaged mesh comes from this exact source.
            folder.rename(final)
    return {'id': identity, 'assembly': assembly, 'cached': False}


def bundle(identity, data_dir):
    if not isinstance(identity, str) or not re.fullmatch('[0-9a-f]{64}', identity):
        raise ValueError('Invalid revision identifier.')
    folder = Path(data_dir) / 'revisions' / identity
    if not (folder / 'assembly.json').is_file():
        raise ValueError('Build this revision before downloading it.')
    checked_revision(folder, identity)
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name in (*ARTIFACTS, 'integrity.json'):
            archive.write(folder / name, name)
    return stream.getvalue()
