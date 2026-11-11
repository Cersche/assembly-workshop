"""Rack frame STL export: the original Lab Rax source meshes (rack-references) for the parts a rack needs.

Local, personal use only: these are the designer's meshes (archive metadata BY-NC-SA); no redistribution.
Assembled fit, strength and print settings remain UNKNOWN.
"""

import hashlib
import io
import json
import re
import struct
import zipfile

import rack_references

NOTICE = ('Lab Rax rack frame parts, exported from the original designer\'s meshes (mklements).\n'
          'Source-specific archive license metadata is recorded in source-manifest.json; it is not redistribution clearance.\n'
          'For your own personal printing only. Do not share or sell these files.\n'
          'Counts come from the Assembly Workshop rack layout. Assembled fit, strength and print settings are UNKNOWN.\n')


def checked_asset(url):
    result = rack_references.asset(url)
    if result is None:
        raise ValueError('Unknown rack source asset.')
    return result[0]


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
    catalog_data = checked_asset('/rack-references/catalog.json')
    catalog = json.loads(catalog_data)
    parts = payload.get('parts') if isinstance(payload, dict) else None
    if not isinstance(parts, list) or not parts or len(parts) > 40:
        raise ValueError('No rack parts to export.')
    name = re.sub(r'[^\w -]+', '', str(payload.get('rack') or 'Lab Rax'))[:40] or 'Lab Rax'
    stream, lines = io.BytesIO(), [f'Parts list for {name}', '']
    manifest = {'version': 1, 'rack': name, 'unit': 'millimeter',
                'geometry': 'Unscaled source components in local coordinates; not assembled poses.',
                'validation': 'Source integrity only; assembled fit, strength and usable depth UNKNOWN.',
                'catalog_sha256': rack_references.digest(catalog_data, 'application/json'), 'parts': []}
    seen, filenames = set(), set()
    with zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED) as z:
        for part in parts:
            if not isinstance(part, dict):
                raise ValueError('Invalid rack part.')
            ref, ident, count = str(part.get('ref')), str(part.get('id')), part.get('count')
            if type(count) is not int or not 1 <= count <= 200:
                raise ValueError('Invalid part count.')
            reference = next((r for r in catalog['references'] if r['id'] == ref), None)
            component = next((c for c in reference['components'] if c['id'] == ident), None) if reference else None
            if component is None or (ref, ident) in seen:
                raise ValueError('Unknown rack part.')
            seen.add((ref, ident))
            mesh_data = checked_asset(component['url'])
            mesh = json.loads(mesh_data)
            title = re.sub(r'\.stl$', '', component['name'], flags=re.I)
            label = str(part.get('label') or '')[:40]
            filename = f'{count}x {title}.stl'
            if filename in filenames or '/' in filename or '\\' in filename:
                raise ValueError('Ambiguous rack part filename.')
            filenames.add(filename)
            stl = stl_bytes(mesh, title)
            z.writestr(filename, stl)
            manifest['parts'].append({'file': filename, 'count': count,
                'source_file': reference['source_file'], 'source_sha256': reference['source_sha256'],
                'license_metadata': reference['license_metadata'], 'source_member': component['source_member'],
                'object_id': ident, 'unit': component['unit'],
                'mesh_sha256': rack_references.digest(mesh_data, 'application/json'),
                'stl_sha256': hashlib.sha256(stl).hexdigest()})
            lines.append(f'{count} x {title}' + (f'  ({label})' if label else '') + f'  -> {filename}')
        lines += ['', NOTICE]
        z.writestr('parts-list.txt', '\n'.join(lines))
        z.writestr('source-manifest.json', json.dumps(manifest, indent=2, ensure_ascii=False))
    return stream.getvalue()
