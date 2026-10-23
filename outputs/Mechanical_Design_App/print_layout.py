"""One print-ready 3MF holding every part of an equipment build, each a separate body flat on the bed.

Brian, 2026-10-22: every STL export also gets one 3MF with all parts laid out side by side, each its own
object in the slicer (a multi-body STL loads as one object in Bambu Studio, so STL is not used for this).
Parts are only moved/rotated, never changed: the tray keeps its orientation, the faceplate lies
front face down 10 mm in front of it, a rear bracket goes 10 mm behind it, everything on Z=0.
Fit and strength stay UNKNOWN; no slicer/printer settings are implied.
"""
from pathlib import Path

GAP = 10.0


def facets(text):
    tris, cur = [], []
    for line in text.splitlines():
        p = line.split()
        if p[:1] == ['vertex']:
            cur.append(tuple(map(float, p[1:4])))
            if len(cur) == 3:
                tris.append(cur); cur = []
    return tris


def move(tris, f):
    return [[f(v) for v in t] for t in tris]


def bounds(tris):
    vs = [v for t in tris for v in t]
    return [min(v[i] for v in vs) for i in range(3)], [max(v[i] for v in vs) for i in range(3)]


def stl(bodies):
    out = []
    for name, tris in bodies:
        out.append(f'solid {name}')
        for a, b, c in tris:
            u = [b[i] - a[i] for i in range(3)]; w = [c[i] - a[i] for i in range(3)]
            n = [u[1]*w[2]-u[2]*w[1], u[2]*w[0]-u[0]*w[2], u[0]*w[1]-u[1]*w[0]]
            m = sum(x*x for x in n) ** 0.5 or 1
            out.append('facet normal %g %g %g\nouter loop' % tuple(x/m for x in n))
            out += ['vertex %.6f %.6f %.6f' % v for v in (a, b, c)]
            out.append('endloop\nendfacet')
        out.append(f'endsolid {name}')
    return '\n'.join(out) + '\n'


def layout(parts):
    """parts: {name: ascii STL text} -> ascii STL text with one solid per part, flat on Z=0."""
    return stl(place(parts))


def layout_3mf(parts):
    """Same layout as a 3MF: slicers (e.g. Bambu Studio) open each part as its own object; STL can't do that."""
    import io, zipfile
    objs, items = [], []
    for i, (name, tris) in enumerate(place(parts), 1):
        idx, verts = {}, []
        def vid(v):
            if v not in idx:
                idx[v] = len(verts); verts.append(v)
            return idx[v]
        faces = [tuple(vid(v) for v in t) for t in tris]
        objs.append(f'<object id="{i}" name="{name}" type="model"><mesh><vertices>'
                    + ''.join('<vertex x="%.6f" y="%.6f" z="%.6f"/>' % v for v in verts) + '</vertices><triangles>'
                    + ''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in faces) + '</triangles></mesh></object>')
        items.append(f'<item objectid="{i}"/>')
    model = ('<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources>'
             + ''.join(objs) + '</resources><build>' + ''.join(items) + '</build></model>')
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                   '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr('3D/3dmodel.model', model)
    return buf.getvalue()


def place(parts):
    placed = []
    for name in ('tray', 'combined', 'faceplate', 'rear_bracket'):
        if name not in parts:
            continue
        tris = facets(parts[name])
        if name == 'faceplate':
            tris = move(tris, lambda v: (v[0], -v[2], v[1]))  # +90 deg about X: front face (Y=-4) onto the bed
        lo, hi = bounds(tris)
        if placed:
            plo, phi = bounds([t for _, b in placed for t in b])
            dy = (plo[1] - GAP - hi[1]) if name == 'faceplate' else (phi[1] + GAP - lo[1])
        else:
            dy = 0
        placed.append((name, move(tris, lambda v, dy=dy, z=lo[2]: (v[0], v[1] + dy, v[2] - z))))
    if not placed:
        raise ValueError('No parts to lay out.')
    return placed


if __name__ == '__main__':
    import sys
    *ins, out = sys.argv[1:]
    parts = {Path(p).stem: Path(p).read_text(encoding='utf-8') for p in ins}
    if out.lower().endswith('.3mf'):
        Path(out).write_bytes(layout_3mf(parts))
    else:
        Path(out).write_text(layout(parts), encoding='utf-8')
