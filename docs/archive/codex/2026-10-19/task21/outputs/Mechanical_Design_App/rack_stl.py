"""Rack frame STL export: the original Lab Rax source meshes (rack-references) for the parts a rack needs.

Local, personal use only: these are the designer's meshes (archive metadata BY-NC-SA); no redistribution.
Assembled fit, strength and print settings remain UNKNOWN.
"""

import io
import json
import re
import struct
import zipfile
from pathlib import Path

REFS = Path(__file__).resolve().parent / 'rack-references'
NOTICE = ('Lab Rax rack frame parts, exported from the original designer\'s meshes (mklements, archive license metadata BY-NC-SA).\n'
          'For your own personal printing only. Do not share or sell these files.\n'
          'Counts come from the Assembly Workshop rack layout. Assembled fit, strength and print settings are UNKNOWN.\n')


def stl_bytes(mesh, name):
    v, tris = mesh['vertices'], mesh['triangles']
    out = [struct.pack('<80sI', name.encode('ascii', 'replace')[:80], len(tris))]
    for a, b, c in tris:
        p, q, r = v[a], v[b], v[c]
        u = [q[i] - p[i] for i in range(3)]
        w = [r[i] - p[i] for i in range(3)]
        n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
        length = sum(x * x for x in n) ** 0.5 or 1
        out.append(struct.pack('<12fH', *[x / length for x in n], *p, *q, *r, 0))
    return b''.join(out)


def export(payload):
    catalog = json.loads((REFS / 'catalog.json').read_text(encoding='utf-8'))
    parts = payload.get('parts') if isinstance(payload, dict) else None
    if not isinstance(parts, list) or not parts or len(parts) > 40:
        raise ValueError('No rack parts to export.')
    name = re.sub(r'[^\w -]+', '', str(payload.get('rack') or 'Lab Rax'))[:40] or 'Lab Rax'
    stream, lines = io.BytesIO(), [f'Parts list for {name}', '']
    with zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED) as z:
        for part in parts:
            ref, ident, count = str(part.get('ref')), str(part.get('id')), part.get('count')
            if type(count) is not int or not 1 <= count <= 200:
                raise ValueError('Invalid part count.')
            try:
                component = next(c for c in catalog['references'][int(ref)]['components'] if c['id'] == ident)
            except (ValueError, IndexError, StopIteration):
                raise ValueError('Unknown rack part.')
            mesh = json.loads((REFS / f'component_{ref}_{ident}.json').read_text(encoding='utf-8'))
            title = re.sub(r'\.stl$', '', component['name'], flags=re.I)
            label = str(part.get('label') or '')[:40]
            filename = f'{count}x {title}.stl'
            z.writestr(filename, stl_bytes(mesh, title))
            lines.append(f'{count} x {title}' + (f'  ({label})' if label else '') + f'  -> {filename}')
        lines += ['', NOTICE]
        z.writestr('parts-list.txt', '\n'.join(lines))
    return stream.getvalue()
