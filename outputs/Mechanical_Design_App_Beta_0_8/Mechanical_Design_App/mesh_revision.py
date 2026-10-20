"""Render constrained Pi4 proposals with the user's local OpenSCAD CLI."""
from collections import Counter
import hashlib
import io
import json
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
    # OpenSCAD's default STL export is ASCII. Reject other encodings explicitly.
    vertices = [tuple(map(float, v)) for v in re.findall(
        rb'vertex\s+([-\d.eE+]+)\s+([-\d.eE+]+)\s+([-\d.eE+]+)', raw)]
    if not vertices or len(vertices) % 3:
        raise ValueError('Invalid ASCII STL output for ' + name)
    edges = Counter(tuple(sorted((vertices[i+j], vertices[i+(j+1)%3])))
                    for i in range(0, len(vertices), 3) for j in range(3))
    if set(edges.values()) != {2}:
        raise ValueError('Rendered mesh has open or non-manifold edges: ' + name)
    unique, indices = {}, []
    for vertex in vertices:
        if vertex not in unique:
            unique[vertex] = len(unique)
        indices.append(unique[vertex])
    return {'id': name, 'vertices': list(unique),
            'triangles': [indices[i:i+3] for i in range(0, len(indices), 3)],
            'source_sha256': hashlib.sha256(raw).hexdigest(),
            'bounds': [[min(v[k] for v in vertices) for k in range(3)],
                       [max(v[k] for v in vertices) for k in range(3)]]}


def compiler():
    candidates = [os.environ.get('OPENSCAD_EXE'), shutil.which('openscad'),
                  'C:/Program Files/OpenSCAD/openscad.exe']
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(Path(candidate).resolve())
    raise ValueError('OpenSCAD is needed for mesh generation. Install it or set OPENSCAD_EXE to its executable. Source-only export remains available.')


def build(source, metadata, data_dir):
    identity = hashlib.sha256(('pi4-mesh-v1\n' + source + json.dumps(metadata, sort_keys=True)).encode()).hexdigest()
    root = Path(data_dir) / 'revisions'
    final = root / identity
    with LOCK:
        if (final / 'assembly.json').is_file():
            return {'id': identity, 'assembly': json.loads((final / 'assembly.json').read_text()), 'cached': True}
        executable = compiler()
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root, prefix='render-') as temp:
            folder = Path(temp)
            src = folder / 'pi4_proposed.scad'
            src.write_text(source, encoding='utf-8', newline='\n')
            parts, logs = [], {}
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
                parts.append(read_mesh(folder / (name+'.stl'), name))
            report = dict(metadata, mesh_build={'id': identity, 'compiler': executable,
                          'checks': 'Both STL meshes have exactly two triangles at every edge.', 'logs': logs},
                          mesh_limits='Mesh closure and successful rendering are not collision, strength or physical fit validation.')
            report['limitations'] = [line for line in metadata['limitations']
                                     if 'viewer still displays' not in line]
            report['limitations'].append('This package contains the generated proposal; the viewer can switch between it and baseline v2.')
            assembly = {'units': 'mm', 'revision': 'PROPOSED pilot '+str(metadata['changed_parameter']['insert_pilot'])+' mm · '+identity[:8],
                        'parts': parts, 'proposal_id': identity, 'status': 'PROPOSED — UNVALIDATED'}
            (folder / 'assembly.json').write_text(json.dumps(assembly, separators=(',', ':')))
            (folder / 'revision.json').write_text(json.dumps(report, indent=2))
            # Immutable cache entry: every packaged mesh comes from this exact source.
            folder.rename(final)
    return {'id': identity, 'assembly': assembly, 'cached': False}


def bundle(identity, data_dir):
    if not isinstance(identity, str) or not re.fullmatch('[0-9a-f]{64}', identity):
        raise ValueError('Invalid revision identifier.')
    folder = Path(data_dir) / 'revisions' / identity
    if not (folder / 'assembly.json').is_file():
        raise ValueError('Build this revision before downloading it.')
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name in ['pi4_proposed.scad', 'tray.stl', 'faceplate.stl', 'revision.json', 'assembly.json']:
            archive.write(folder / name, name)
    return stream.getvalue()
