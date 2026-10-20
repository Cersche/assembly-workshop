"""Multi-color faceplate artwork: one STL per filament color (Pi4 faceplate adapter only).

The saved local preview image is reduced to a few colors on a 0.4 mm grid, thin
features are cleaned up, and each color becomes a body of merged rectangles that
OpenSCAD extrudes. The base faceplate gets a matching pocket (inlay) or is left
unchanged (emboss). All files share the faceplate origin, so a slicer can load
them together and assign one filament per file.

PROPOSED — UNVALIDATED. Printed color result, fit, strength and filament behavior
remain UNKNOWN. No printer, slicer or material integration.
"""
from collections import Counter, deque
import hashlib
import io
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import threading
import zipfile
import zlib

import assembly_records
import mesh_revision

CELL = 0.4                     # grid pitch, mm
MIN_FEATURE = 0.8              # features thinner than this are merged into a neighbor
DEPTH = 0.6                    # inlay depth / emboss height, mm
STYLES = ('inlay', 'emboss')
# Same window the 3D preview uses for the image on the Pi4 faceplate front (y = -3).
WINDOW_W, WINDOW_H, WINDOW_Z, FRONT_Y = 216.0, 34.0, 21.0, -3.0
MAX_RECTS = 4000
TINY_ISLAND_CELLS = 6          # about 1 mm²
DENSITY_ESTIMATE = 1.24        # g/cm³, PLA-typical; estimate only
LOCK = threading.Lock()
LIMITS = ['PROPOSED — UNVALIDATED. Printed color result, fit, strength and filament behavior are UNKNOWN.',
          'STL files carry no color: load all files together and assign one filament per file in your slicer.',
          'Mesh closure and successful rendering are not physical approval.',
          'Filament amounts are rough estimates from body volume only (no purge, infill or waste).']

# Generic filament color approximations (not any brand's certified color).
FILAMENTS = [('Black', '#1b1b1b'), ('White', '#f2f2f2'), ('Grey', '#8a8d91'), ('Silver', '#c4c7cc'),
             ('Red', '#c8102e'), ('Orange', '#ff6a13'), ('Yellow', '#ffd100'), ('Green', '#00a651'),
             ('Dark green', '#205c40'), ('Blue', '#0057b8'), ('Light blue', '#6cace4'), ('Navy', '#1f2a44'),
             ('Purple', '#6d3b8f'), ('Pink', '#f4a6c6'), ('Brown', '#6b4423'), ('Beige', '#d9c39a')]


# ---------------------------------------------------------------- PNG (stdlib)
CHANNELS = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}


def decode_png(data):
    """8-bit, non-interlaced PNG -> (width, height, flat RGBA bytearray)."""
    assembly_records.validate_png(data)
    pos, idat, plte, trns = 8, [], b'', b''
    while pos < len(data):
        size = struct.unpack('>I', data[pos:pos + 4])[0]
        kind, body = data[pos + 4:pos + 8], data[pos + 8:pos + 8 + size]
        pos += size + 12
        if kind == b'IHDR':
            width, height, depth, ctype, _, _, interlace = struct.unpack('>IIBBBBB', body)
        elif kind == b'PLTE':
            plte = body
        elif kind == b'tRNS':
            trns = body
        elif kind == b'IDAT':
            idat.append(body)
    if depth != 8 or interlace or ctype not in CHANNELS:
        raise ValueError('Use an 8-bit, non-interlaced PNG (the local image chooser prepares one).')
    ch = CHANNELS[ctype]
    stride = width * ch
    raw = zlib.decompress(b''.join(idat))
    if len(raw) != height * (stride + 1):
        raise ValueError('PNG image data has the wrong size.')
    out, prev = bytearray(), bytearray(stride)
    for y in range(height):
        start = y * (stride + 1)
        f, line = raw[start], bytearray(raw[start + 1:start + 1 + stride])
        if f == 1:
            for i in range(ch, stride):
                line[i] = (line[i] + line[i - ch]) & 255
        elif f == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 255
        elif f == 3:
            for i in range(stride):
                line[i] = (line[i] + ((line[i - ch] if i >= ch else 0) + prev[i]) // 2) & 255
        elif f == 4:
            for i in range(stride):
                a = line[i - ch] if i >= ch else 0
                b, c = prev[i], (prev[i - ch] if i >= ch else 0)
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[i] = (line[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        elif f:
            raise ValueError('Unsupported PNG filter.')
        prev = line
        if ctype == 6:
            out += line
        else:
            for i in range(0, stride, ch):
                if ctype == 2:
                    out += bytes((line[i], line[i + 1], line[i + 2], 255))
                elif ctype == 0:
                    out += bytes((line[i],) * 3 + (255,))
                elif ctype == 4:
                    out += bytes((line[i],) * 3 + (line[i + 1],))
                else:
                    k = line[i]
                    if 3 * k + 2 >= len(plte):
                        raise ValueError('PNG palette index out of range.')
                    out += plte[3 * k:3 * k + 3] + bytes((trns[k] if k < len(trns) else 255,))
    return width, height, out


def encode_png(width, height, rgb):
    rows = b''.join(b'\x00' + bytes(rgb[y * width * 3:(y + 1) * width * 3]) for y in range(height))

    def chunk(kind, body):
        return struct.pack('>I', len(body)) + kind + body + struct.pack('>I', zlib.crc32(kind + body) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(rows, 9)) + chunk(b'IEND', b''))


# ---------------------------------------------------------------- settings
def hexrgb(value):
    return tuple(int(value[i:i + 2], 16) for i in (1, 3, 5))


def settings(art):
    """Validated artwork placement + filament settings (defaults filled in)."""
    if not isinstance(art, dict):
        raise ValueError('Add a faceplate image on the Appearance tab first.')
    clean = assembly_records.appearance({'artwork': art}).get('artwork')
    if not clean:
        raise ValueError('Add a faceplate image on the Appearance tab first.')
    fil = dict(clean.get('filament') or {})
    fil.setdefault('count', 4)
    fil.setdefault('style', 'inlay')
    return clean, fil


def layout(clean, width, height):
    """Image rectangle on the faceplate front, mm (mirrors viewer.js)."""
    s = max(.05, clean['scale'])
    ratio = width / height
    w = min(WINDOW_W, WINDOW_H * ratio) * s
    h = w / ratio
    cx = (clean['x'] - .5) * (WINDOW_W - w)
    cz = WINDOW_Z + (.5 - clean['y']) * (WINDOW_H - h)
    return cx - w / 2, cz + h / 2, w, h   # left X, top Z, width, height


# ---------------------------------------------------------------- reduction
def sample(width, height, rgba, nx, nz):
    """Average image pixels into nx × nz cells. None = transparent cell."""
    cells = []
    for j in range(nz):
        y0 = j * height // nz
        y1 = max(y0 + 1, (j + 1) * height // nz)
        for i in range(nx):
            x0 = i * width // nx
            x1 = max(x0 + 1, (i + 1) * width // nx)
            r = g = b = a = n = 0
            for y in range(y0, y1):
                base = (y * width + x0) * 4
                for k in range(base, base + (x1 - x0) * 4, 4):
                    al = rgba[k + 3]
                    r += rgba[k] * al
                    g += rgba[k + 1] * al
                    b += rgba[k + 2] * al
                    a += al
                    n += 1
            cells.append(None if a < 128 * n else (r / a, g / a, b / a))
    return cells


def dist(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2


def kmeans(cells, k):
    """Deterministic weighted k-means over 5-bit color buckets."""
    buckets = {}
    for c in cells:
        if c is None:
            continue
        key = (int(c[0]) >> 3, int(c[1]) >> 3, int(c[2]) >> 3)
        s = buckets.setdefault(key, [0.0, 0.0, 0.0, 0])
        s[0] += c[0]; s[1] += c[1]; s[2] += c[2]; s[3] += 1
    points = [((s[0] / s[3], s[1] / s[3], s[2] / s[3]), s[3]) for _, s in sorted(buckets.items())]
    if not points:
        return []
    centers = [max(points, key=lambda p: p[1])[0]]
    while len(centers) < min(k, len(points)):
        centers.append(max(points, key=lambda p: p[1] * min(dist(p[0], c) for c in centers))[0])
    for _ in range(15):
        sums = [[0.0, 0.0, 0.0, 0] for _ in centers]
        for color, weight in points:
            s = sums[min(range(len(centers)), key=lambda i: dist(color, centers[i]))]
            s[0] += color[0] * weight; s[1] += color[1] * weight; s[2] += color[2] * weight; s[3] += weight
        moved = [(s[0] / s[3], s[1] / s[3], s[2] / s[3]) if s[3] else c for s, c in zip(sums, centers)]
        if moved == centers:
            break
        centers = moved
    return centers


def clean_thin(labels, nx, nz, passes=4):
    """Merge cells that are not part of any 2×2 same-color block (features < 0.8 mm).

    Outside the image counts as the base color (0), so edges are handled too.
    Returns (labels, cells changed, cells still thin)."""
    W = nx + 2
    grid = [0] * (W * (nz + 2))
    for j in range(nz):
        grid[(j + 1) * W + 1:(j + 1) * W + 1 + nx] = labels[j * nx:(j + 1) * nx]
    changed, bad = 0, []
    for _ in range(passes):
        ok = bytearray(len(grid))
        for y in range(nz + 1):
            row = y * W
            for x in range(nx + 1):
                k = row + x
                c = grid[k]
                if grid[k + 1] == c and grid[k + W] == c and grid[k + W + 1] == c:
                    ok[k] = ok[k + 1] = ok[k + W] = ok[k + W + 1] = 1
        bad = [(y + 1) * W + x + 1 for y in range(nz) for x in range(nx) if not ok[(y + 1) * W + x + 1]]
        if not bad:
            break
        new = grid[:]
        for k in bad:
            around = [k - W - 1, k - W, k - W + 1, k - 1, k + 1, k + W - 1, k + W, k + W + 1]
            votes = Counter(grid[n] for n in around if ok[n]) or Counter(grid[n] for n in around)
            new[k] = votes.most_common(1)[0][0]
            changed += new[k] != grid[k]
        grid = new
    result = [grid[(j + 1) * W + 1 + i] for j in range(nz) for i in range(nx)]
    return result, changed, len(bad)


def islands(labels, nx, nz):
    seen, small, total = bytearray(len(labels)), 0, 0
    for start, c in enumerate(labels):
        if c == 0 or seen[start]:
            continue
        total += 1
        size, queue = 0, deque([start])
        seen[start] = 1
        while queue:
            k = queue.popleft()
            size += 1
            x, y = k % nx, k // nx
            for n, inside in ((k - 1, x > 0), (k + 1, x < nx - 1), (k - nx, y > 0), (k + nx, y < nz - 1)):
                if inside and not seen[n] and labels[n] == c:
                    seen[n] = 1
                    queue.append(n)
        small += size < TINY_ISLAND_CELLS
    return total, small


def rectangles(labels, nx, nz, label):
    """Greedy merge of equal-span row runs into rectangles: [x0, row0, x1, row1] (exclusive ends)."""
    done, open_ = [], {}
    for y in range(nz + 1):
        runs = []
        if y < nz:
            x = 0
            row = labels[y * nx:(y + 1) * nx]
            while x < nx:
                if row[x] == label:
                    s = x
                    while x < nx and row[x] == label:
                        x += 1
                    runs.append((s, x))
                else:
                    x += 1
        nxt = {}
        for span in runs:
            nxt[span] = open_.pop(span, y)
        for (x0, x1), y0 in open_.items():
            done.append((x0, y0, x1, y))
        open_ = nxt
    return done


def reduce(art, data_dir):
    """Image + settings -> grid labels, palette, stats and warnings (no files written)."""
    clean, fil = settings(art)
    data = assembly_records.artwork(data_dir, clean['sha256'])
    width, height, rgba = decode_png(data)
    left, top, w, h = layout(clean, width, height)
    nx, nz = max(1, round(w / CELL)), max(1, round(h / CELL))
    cells = sample(width, height, rgba, nx, nz)
    count = fil['count']
    transparent = any(c is None for c in cells)
    centers = kmeans(cells, count - 1 if transparent else count)
    raw = [None if c is None else min(range(len(centers)), key=lambda i: dist(c, centers[i])) for c in cells]
    sizes = Counter(raw)
    # Base = the faceplate itself: transparent area, else the largest color.
    order = sorted(range(len(centers)), key=lambda i: (-sizes[i], i))
    shift = 1 if transparent else 0
    index = {ci: n + shift for n, ci in enumerate(order)}
    auto = [None] * shift + [centers[i] for i in order]
    labels = [0 if r is None else index[r] for r in raw]
    colors = list(fil.get('colors') or [])
    palette = []
    for n, c in enumerate(auto):
        if n < len(colors):
            palette.append(colors[n])
        elif c is None:
            palette.append(None)   # base: use the faceplate color
        else:
            palette.append('#%02x%02x%02x' % tuple(round(v) for v in c))
    # Same filament color twice = merged into one body.
    merge = {}
    for n, hexv in enumerate(palette):
        merge[n] = 0 if n == 0 or (hexv and hexv == palette[0]) else next(
            (m for m in range(1, n) if palette[m] == hexv and hexv), n)
    labels = [merge[v] for v in labels]
    labels, changed, still_thin = clean_thin(labels, nx, nz)
    total_islands, small_islands = islands(labels, nx, nz)
    cw, ch = w / nx, h / nz
    counts = Counter(labels)
    bodies = []
    for n in range(1, len(palette)):
        if merge[n] != n or not counts[n]:
            continue
        rects = rectangles(labels, nx, nz, n)
        area = counts[n] * cw * ch
        bodies.append({'index': n, 'color': palette[n], 'rects': rects, 'cells': counts[n],
                       'area_mm2': round(area, 1), 'volume_mm3': round(area * DEPTH, 1),
                       'grams_estimate': round(area * DEPTH / 1000 * DENSITY_ESTIMATE, 2)})
    warnings = []
    if changed:
        warnings.append(f'{changed} cells thinner than {MIN_FEATURE:g} mm were merged into a neighboring color.')
    if still_thin:
        warnings.append(f'{still_thin} cells are still thinner than {MIN_FEATURE:g} mm; simplify the image or use fewer colors.')
    if small_islands:
        warnings.append(f'{small_islands} of {total_islands} color islands are smaller than about 1 mm²; they may not print cleanly.')
    if total_islands > 300:
        warnings.append(f'{total_islands} separate color islands: many tool changes. A simpler image or fewer colors will print faster.')
    rect_total = sum(len(b['rects']) for b in bodies)
    if rect_total > MAX_RECTS:
        warnings.append(f'The design needs {rect_total} rectangles (limit {MAX_RECTS}); simplify the image, reduce colors or reduce its size before export.')
    if not bodies:
        warnings.append('Only the base color remains; there is nothing to print in a second color.')
    return {'settings': {'count': count, 'style': fil['style']}, 'clean': clean, 'grid': [nx, nz],
            'cell_mm': [cw, ch], 'origin': [left, top], 'size_mm': [round(w, 2), round(h, 2)],
            'labels': labels, 'palette': palette, 'merge': merge, 'bodies': bodies,
            'rect_total': rect_total, 'warnings': warnings}


def preview(art, data_dir, faceplate_color='#4e75a3'):
    r = reduce(art, data_dir)
    nx, nz = r['grid']
    base = hexrgb(r['palette'][0] or faceplate_color)
    shown = [hexrgb(c) if c else base for c in r['palette']]
    rgb = bytearray()
    for v in r['labels']:
        rgb += bytes(shown[v])
    import base64
    return {'preview_png': 'data:image/png;base64,' + base64.b64encode(encode_png(nx, nz, rgb)).decode('ascii'),
            'palette': r['palette'], 'base_is_faceplate': r['palette'][0] is None,
            'merged': [n for n, m in r['merge'].items() if m != n],
            'bodies': [{k: b[k] for k in ('index', 'color', 'area_mm2', 'volume_mm3', 'grams_estimate')} | {'rectangles': len(b['rects'])}
                       for b in r['bodies']],
            'size_mm': r['size_mm'], 'grid': r['grid'], 'style': r['settings']['style'], 'count': r['settings']['count'],
            'depth_mm': DEPTH, 'warnings': r['warnings'], 'filaments': FILAMENTS, 'limitations': LIMITS,
            'exportable': bool(r['bodies']) and r['rect_total'] <= MAX_RECTS}


# ---------------------------------------------------------------- geometry
def scad(r):
    left, top = r['origin']
    cw, ch = r['cell_mm']
    lines = ['// Multi-color faceplate artwork. PROPOSED — UNVALIDATED. Generated; do not edit.',
             'use <faceplate_source.scad>', 'part="base";', f'depth={DEPTH};', f'front_y={FRONT_Y};']
    names = []
    for b in r['bodies']:
        name = 'color_%d' % b['index']
        names.append(name)
        lines.append(f'module {name}(){{union(){{')
        for x0, y0, x1, y1 in b['rects']:
            lines.append(f' translate([{left + x0 * cw:.4f},{top - y1 * ch:.4f}])square([{(x1 - x0) * cw:.4f},{(y1 - y0) * ch:.4f}]);')
        lines.append('}}')
    lines.append('module art_all(){union(){' + ''.join(n + '();' for n in names) + '}}')
    # 2D X = rack X, 2D Y = height Z; rotate([90,0,0]) extrudes toward -Y.
    if r['settings']['style'] == 'inlay':
        lines.append('if(part=="base")difference(){faceplate();translate([0,front_y+depth,0])rotate([90,0,0])linear_extrude(height=depth+0.1)art_all();}')
        for n in names:
            lines.append(f'if(part=="{n}")translate([0,front_y+depth,0])rotate([90,0,0])linear_extrude(height=depth){n}();')
    else:
        lines.append('if(part=="base")faceplate();')
        for n in names:
            lines.append(f'if(part=="{n}")translate([0,front_y,0])rotate([90,0,0])linear_extrude(height=depth){n}();')
    return '\n'.join(lines) + '\n', names


def export(art, faceplate_source, metadata, data_dir, faceplate_color='#4e75a3'):
    """Render base + one body per color; returns a zip. Cached immutably by content."""
    r = reduce(art, data_dir)
    if not r['bodies']:
        raise ValueError('Only the base color remains; there is nothing to export in a second color.')
    if r['rect_total'] > MAX_RECTS:
        raise ValueError(r['warnings'][-1])
    art_source, names = scad(r)
    identity = hashlib.sha256(('faceplate-color-v1\n' + faceplate_source + '\n' + art_source).encode('utf-8')).hexdigest()
    final = Path(data_dir) / 'faceplate-color-revisions' / identity
    base_hex = r['palette'][0] or faceplate_color
    with LOCK:
        if not final.exists():
            final.parent.mkdir(parents=True, exist_ok=True)
            exe = mesh_revision.compiler()
            with tempfile.TemporaryDirectory(dir=final.parent, prefix='render-') as temp:
                folder = Path(temp)
                (folder / 'faceplate_source.scad').write_text(faceplate_source, encoding='utf-8', newline='\n')
                (folder / 'faceplate_colors.scad').write_text(art_source, encoding='utf-8', newline='\n')
                files, logs, meshes = [], {}, {}
                for part in ['base'] + names:
                    out = folder / (part + '.stl')
                    try:
                        res = subprocess.run([exe, '-o', str(out), '-D', f'part="{part}"', str(folder / 'faceplate_colors.scad')],
                                             capture_output=True, text=True, timeout=600,
                                             creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
                    except (OSError, subprocess.TimeoutExpired) as exc:
                        raise ValueError('Mesh rendering failed or timed out: ' + str(exc)) from exc
                    logs[part] = res.stderr[-4000:]
                    if res.returncode or 'ERROR:' in res.stderr or not out.exists():
                        raise ValueError('OpenSCAD failed for ' + part + ': ' + res.stderr[-1200:])
                    try:
                        mesh_revision.normalize_collinear_faces(out)
                    except ValueError:
                        pass  # optional tidy-up; read_mesh still enforces a closed, valid mesh
                    mesh = mesh_revision.read_mesh(out, part)
                    meshes[part] = {'signed_volume_mm3': round(mesh['signed_volume_mm3'], 3), 'bounds': mesh['bounds']}
                    files.append(part + '.stl')
                bodies = [{k: b[k] for k in ('index', 'color', 'area_mm2', 'volume_mm3', 'grams_estimate')} | {'file': 'color_%d.stl' % b['index']}
                          for b in r['bodies']]
                report = {'id': identity, 'status': 'PROPOSED — UNVALIDATED', 'style': r['settings']['style'],
                          'depth_mm': DEPTH, 'grid_mm': [round(v, 4) for v in r['cell_mm']],
                          'min_feature_mm': MIN_FEATURE, 'image': {k: r['clean'][k] for k in ('sha256', 'name', 'x', 'y', 'scale')},
                          'image_size_mm': r['size_mm'],
                          'base': {'file': 'base.stl', 'color': base_hex, 'note': 'The faceplate itself, printed in the base filament.'},
                          'bodies': bodies, 'warnings': r['warnings'], 'mesh': meshes, 'faceplate_revision': metadata,
                          'limitations': LIMITS, 'logs': logs,
                          'sha256': {f: hashlib.sha256((folder / f).read_bytes()).hexdigest() for f in files}}
                (folder / 'revision.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
                readme = ['Multi-color faceplate (PROPOSED — UNVALIDATED)', '',
                          'Load ALL .stl files together into your slicer as ONE multi-part object',
                          '(keep their positions; they share the same origin), then assign a filament to each:', '',
                          f'  base.stl     -> {base_hex}  (faceplate)']
                readme += [f"  {b['file']:<12} -> {b['color']}  (~{b['grams_estimate']} g estimate)" for b in bodies]
                readme += ['', f"Style: {r['settings']['style']}, {DEPTH} mm. Print the faceplate front face down for an inlay.",
                           ''] + LIMITS
                (folder / 'README.txt').write_text('\n'.join(readme) + '\n', encoding='utf-8')
                folder.rename(final)
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED) as z:
        report = json.loads((final / 'revision.json').read_text(encoding='utf-8'))
        for name, digest in report['sha256'].items():
            data = (final / name).read_bytes()
            if hashlib.sha256(data).hexdigest() != digest:
                raise ValueError('Cached color export failed its integrity check; preserve it and change a setting to regenerate.')
            z.writestr(name, data)
        for name in ('revision.json', 'README.txt', 'faceplate_colors.scad', 'faceplate_source.scad'):
            z.write(final / name, name)
    return stream.getvalue()
