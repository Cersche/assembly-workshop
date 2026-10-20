"""Shared mesh checks and local OpenSCAD discovery for equipment geometry."""
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
    try:
        return _normalize_collinear_faces(path, longest_first=False)
    except ValueError:
        # 2026-10-19: OpenSCAD can stack two zero-area faces on one edge (seen with moved tray screw joints). In file
        # order the inner one may come first and has no real neighbor; repairing the longest one first resolves the
        # stack with the same exact split. Only tried when the original order fails, so earlier results are unchanged.
        return _normalize_collinear_faces(path, longest_first=True)


def _normalize_collinear_faces(path, longest_first):
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
        empty=[i for i,f in enumerate(faces) if normal(f)==(0,0,0)]
        if not empty:break
        span=lambda f:max(sum((f[j][k]-f[i][k])**2 for k in range(3)) for i,j in ((0,1),(1,2),(2,0)))
        index=max(empty,key=lambda i:span(faces[i])) if longest_first else empty[0]
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


def compiler():
    candidates = [os.environ.get('OPENSCAD_EXE'), shutil.which('openscad'),
                  'C:/Program Files/OpenSCAD/openscad.exe']
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(Path(candidate).resolve())
    raise ValueError('OpenSCAD is needed for mesh generation. Install it or set OPENSCAD_EXE to its executable. Source-only export remains available.')



def bundle(identity, data_dir):
    if not isinstance(identity, str) or not re.fullmatch('[0-9a-f]{64}', identity):
        raise ValueError('Invalid revision identifier.')
    raise ValueError('This historical revision is preserved. Use Place on tray to build a new library revision.')
