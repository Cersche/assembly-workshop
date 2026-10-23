"""Multi-color faceplate artwork: one STL per filament color for wizard-made faceplates (equipment_tray.scad).

This opt-in "Print in color" export is the only path from artwork to STL; the normal
tray/faceplate STLs never contain artwork (see AGENTS.md). The saved local preview image is
placed exactly as the rack view places it (same window, same opening-avoidance), reduced to a
few colors on a 0.4 mm grid, thin features are cleaned up, cells near openings and rack holes
are left as plain faceplate, and each color becomes a body of merged rectangles that OpenSCAD
extrudes. The slot's own faceplate gets a matching pocket (inlay) or is left unchanged
(emboss). All files share the faceplate origin, so a slicer can load them together and assign
one filament per file.

PROPOSED — UNVALIDATED. Printed color result, fit, strength and filament behavior
remain UNKNOWN. No printer, slicer or material integration.
"""
from collections import Counter, deque
import hashlib
import io
import json
import math
from pathlib import Path
import struct
import subprocess
import tempfile
import threading
import zipfile
import zlib

import assembly_records
import equipment
import mesh_revision
import port_openings

CELL = 0.4                     # grid pitch, mm
MIN_FEATURE = 0.8              # features thinner than this are merged into a neighbor
DEPTH = 0.6                    # inlay depth / emboss height, mm
STYLES = ('inlay', 'emboss')
# Generic faceplate (equipment_tray.scad): 252 mm wide, 4 mm thick, front face at Y = -4, 44.45 mm pitch per U.
FRONT_Y, PLATE_W = -4.0, 252.0
RACK_PITCH, PLATE_GAP = port_openings.RACK_PITCH, port_openings.PLATE_GAP
SIDE_MARGIN, EDGE_MARGIN = 18.0, 4.0   # image window margins: rack-studio.js artworkWindow()
OPENING_GAP = 2.0                      # clearance kept around openings: rack-studio.js clearWindow()
KS_BLOCK_W, KS_BLOCK_H, KS_BLOCK_DZ = 21.0, 33.5, 1.75   # golden keystone block (ks_box_cut), centre above plate centre
SLEEVE_JOINT_D = 3.4                   # m3_clear holes through the plate for a sleeve screw joint
HOLE_X, HOLE_DZ, SLOT_LEN, SLOT_D = 118.2625, 15.902, 10.0, 7.0   # four-corner rack slots per U
EDGE_KEEP = 1.0                        # color stays this far inside the plate outline and every hole (SCAD clip)
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


# ---------------------------------------------------------------- faceplate front
def slot_spec(data_dir, placement):
    """Cleaned equipment spec for a slot allocation ({'equipment', 'tray', 'second'}), as Place on tray builds it."""
    if not isinstance(placement, dict) or not str(placement.get('equipment') or '').startswith('eq-'):
        raise ValueError('Print in color needs equipment from the library in this slot.')
    request = {'item': placement['equipment'], 'tray': placement.get('tray')}
    second = placement.get('second')
    if isinstance(second, dict) and second.get('equipment'):
        request['second'] = {'item': second['equipment'], 'tray': second.get('tray')}
    return equipment.allocation_request(data_dir, request)


def openings(s):
    """Front openings {x, z, w, h} (X from centre, Z from the slot bottom), as equipment-wizard.js openings() lists them."""
    grow = float(s.get('bezel_size', 1)) if s.get('bezel', 'none') != 'none' else 0.0
    out = []
    win = port_openings.front_window(s)
    if win:
        out.append({'x': win['x'], 'z': (win['bottom'] + win['top']) / 2, 'w': win['width'] + 2 * grow, 'h': win['height'] + 2 * grow})
    sleeve = port_openings.sleeve(s)
    if sleeve and s.get('joint') == 'screw':
        out += [{'x': x, 'z': z, 'w': SLEEVE_JOINT_D, 'h': SLEEVE_JOINT_D} for x in sleeve['joints'] for z in sleeve['joint_z']]
    centre = s['u'] * RACK_PITCH / 2
    out += [{'x': float(x), 'z': centre + KS_BLOCK_DZ, 'w': KS_BLOCK_W, 'h': KS_BLOCK_H} for x in s.get('keystones') or []]
    out += [{'x': p['x'], 'z': p['z'], 'w': p['w'] + 2 * grow, 'h': p['h'] + 2 * grow} for p in s.get('ports') or []]
    return out


def plate(s):
    """Image window and keep-out areas of a wizard faceplate front (same numbers as the rack view)."""
    u = s['u']
    bottom, plate_h = PLATE_GAP / 2, u * RACK_PITCH - PLATE_GAP
    slots = [{'x': x, 'z': i * RACK_PITCH + RACK_PITCH / 2 + dz, 'w': SLOT_LEN, 'h': SLOT_D}
             for i in range(u) for dz in (-HOLE_DZ, HOLE_DZ) for x in (-HOLE_X, HOLE_X)]
    holes = openings(s)
    return {'u': u, 'height_mm': plate_h, 'bottom': bottom, 'openings': holes, 'keep_out': holes + slots,
            'window': {'w': max(1.0, PLATE_W - 2 * SIDE_MARGIN), 'h': max(1.0, plate_h - 2 * EDGE_MARGIN), 'z': bottom + plate_h / 2}}


def clear_window(win, obstacles, aspect=1.0, gap=OPENING_GAP):
    """Largest part of the window clear of openings (+ gap) for this image aspect. Port of rack-studio.js clearWindow()."""
    cx = win.get('x', 0)
    L, R, B, T, eps = cx - win['w'] / 2, cx + win['w'] / 2, win['z'] - win['h'] / 2, win['z'] + win['h'] / 2, 1e-6
    obs = [(o['x'] - o['w'] / 2 - gap, o['x'] + o['w'] / 2 + gap, o['z'] - o['h'] / 2 - gap, o['z'] + o['h'] / 2 + gap) for o in obstacles]
    obs = [o for o in obs if o[1] > L and o[0] < R and o[3] > B and o[2] < T]
    if not obs:
        return win
    xs = sorted(set(min(R, max(L, x)) for x in [L, R] + [v for o in obs for v in o[:2]]))
    best, score = None, -1
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            x0, x1 = xs[i], xs[j]
            spans = sorted(([o[2], o[3]] for o in obs if o[1] > x0 + eps and o[0] < x1 - eps), key=lambda a: a[0])
            z = B
            for b, t in spans + [[T, T]]:
                if b > z + eps:
                    h = min(b, T) - z
                    width = min(x1 - x0, h * aspect)
                    s = width * width / aspect - 1e-6 * math.hypot((x0 + x1) / 2 - cx, z + h / 2 - win['z'])
                    if s > score:
                        score, best = s, {'x': (x0 + x1) / 2, 'z': z + h / 2, 'w': x1 - x0, 'h': h}
                z = max(z, t)
                if z >= T:
                    break
    return best or win


def layout(clean, width, height, front):
    """Image rectangle on the faceplate front, mm. Mirrors rack-studio.js artworkRect() with the opening-clear window."""
    ratio = width / height
    win = clear_window(front['window'], front['openings'], ratio)
    w = min(win['w'], win['h'] * ratio) * max(.05, clean['scale'])
    h = w / ratio
    cx = win.get('x', 0) + (clean['x'] - .5) * (win['w'] - w)
    cz = win['z'] + (.5 - clean['y']) * (win['h'] - h)
    return cx - w / 2, cz + h / 2, w, h   # left X, top Z, width, height


def keep_clear(cells, nx, nz, left, top, cw, ch, front):
    """Leave cells within the gap of any opening or rack slot, or near the plate edge, as plain faceplate."""
    boxes = [(o['x'] - o['w'] / 2 - OPENING_GAP, o['x'] + o['w'] / 2 + OPENING_GAP,
              o['z'] - o['h'] / 2 - OPENING_GAP, o['z'] + o['h'] / 2 + OPENING_GAP) for o in front['keep_out']]
    lo, hi = front['bottom'] + EDGE_KEEP, front['bottom'] + front['height_mm'] - EDGE_KEEP
    edge = PLATE_W / 2 - EDGE_KEEP
    cleared = 0
    for j in range(nz):
        z1 = top - j * ch
        z0 = z1 - ch
        for i in range(nx):
            k = j * nx + i
            if cells[k] is None:
                continue
            x0 = left + i * cw
            x1 = x0 + cw
            if x0 < -edge or x1 > edge or z0 < lo or z1 > hi or any(x1 > b[0] and x0 < b[1] and z1 > b[2] and z0 < b[3] for b in boxes):
                cells[k] = None
                cleared += 1
    return cleared


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


_DECODED = {}   # sha256 -> decoded image; artwork files are immutable, so this never goes stale


def decoded(data_dir, identity):
    if identity not in _DECODED:
        if len(_DECODED) >= 4:
            _DECODED.pop(next(iter(_DECODED)))
        _DECODED[identity] = decode_png(assembly_records.artwork(data_dir, identity))
    return _DECODED[identity]


def reduce(art, data_dir, s, faceplate_color='#4e75a3'):
    """Image + settings + the slot's cleaned equipment spec -> grid labels, palette, stats and warnings (no files written).

    Index 0 is always the faceplate itself (transparent image area and everything
    outside the image). The image is reduced to count - 1 colors; a color given the
    same filament as the base is merged into the faceplate."""
    clean, fil = settings(art)
    width, height, rgba = decoded(data_dir, clean['sha256'])
    front = plate(s)
    left, top, w, h = layout(clean, width, height, front)
    nx, nz = max(1, round(w / CELL)), max(1, round(h / CELL))
    cw, ch = w / nx, h / nz
    cells = sample(width, height, rgba, nx, nz)
    kept_clear = keep_clear(cells, nx, nz, left, top, cw, ch, front)
    count = fil['count']
    centers = kmeans(cells, count - 1)
    raw = [None if c is None else min(range(len(centers)), key=lambda i: dist(c, centers[i])) for c in cells]
    sizes = Counter(raw)
    order = sorted(range(len(centers)), key=lambda i: (-sizes[i], i))
    index = {ci: n + 1 for n, ci in enumerate(order)}
    auto = [None] + [centers[i] for i in order]
    labels = [0 if r is None else index[r] for r in raw]
    colors = list(fil.get('colors') or [])
    palette = []
    for n, c in enumerate(auto):
        if n < len(colors) and colors[n]:
            palette.append(colors[n])
        elif c is None:
            palette.append(None)   # base: use the faceplate color
        else:
            palette.append('#%02x%02x%02x' % tuple(round(v) for v in c))
    base_hex = (palette[0] or faceplate_color).lower()
    # Same filament color twice = merged into one body; the base color merges into the faceplate.
    merge = {}
    for n, hexv in enumerate(palette):
        merge[n] = 0 if n == 0 or hexv.lower() == base_hex else next(
            (m for m in range(1, n) if palette[m].lower() == hexv.lower()), n)
    labels = [merge[v] for v in labels]
    labels, changed, still_thin = clean_thin(labels, nx, nz)
    total_islands, small_islands = islands(labels, nx, nz)
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
    if kept_clear:
        warnings.append(f'{kept_clear} image cells near openings, rack holes or the plate edge stay plain faceplate.')
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
    return {'settings': {'count': count, 'style': fil['style']}, 'clean': clean, 'grid': [nx, nz], 'spec': s, 'plate': front,
            'cell_mm': [cw, ch], 'origin': [left, top], 'size_mm': [round(w, 2), round(h, 2)],
            'labels': labels, 'palette': palette, 'base_hex': base_hex, 'merge': merge, 'bodies': bodies,
            'rect_total': rect_total, 'warnings': warnings}


def preview(art, data_dir, s, faceplate_color='#4e75a3'):
    r = reduce(art, data_dir, s, faceplate_color)
    nx, nz = r['grid']
    base = hexrgb(r['base_hex'])
    shown = [hexrgb(c) if c else base for c in r['palette']]
    rgb = bytearray()
    for v in r['labels']:
        rgb += bytes(shown[v])
    import base64
    return {'preview_png': 'data:image/png;base64,' + base64.b64encode(encode_png(nx, nz, rgb)).decode('ascii'),
            'palette': r['palette'], 'base_hex': r['base_hex'], 'base_is_faceplate': r['palette'][0] is None,
            'merged': [n for n, m in r['merge'].items() if m != n],
            'bodies': [{k: b[k] for k in ('index', 'color', 'area_mm2', 'volume_mm3', 'grams_estimate')} | {'rectangles': len(b['rects'])}
                       for b in r['bodies']],
            'size_mm': r['size_mm'], 'origin_mm': [round(v, 3) for v in r['origin']], 'u': r['plate']['u'],
            'grid': r['grid'], 'style': r['settings']['style'], 'count': r['settings']['count'],
            'depth_mm': DEPTH, 'warnings': r['warnings'], 'filaments': FILAMENTS, 'limitations': LIMITS,
            'exportable': bool(r['bodies']) and r['rect_total'] <= MAX_RECTS}


# ---------------------------------------------------------------- geometry
# Appended to the slot's equipment source (used via `use <faceplate_source.scad>`), so these modules see its variables.
# color_base(): the printed faceplate part, or the one-piece faceplate + tray for a single printed piece joint.
# color_clip(): keeps color EDGE_KEEP inside the plate outline and every through-hole (slots, ports, windows).
SOURCE_HELPERS = f"""
// ---- Print in color helpers (faceplate_color.py). PROPOSED — UNVALIDATED.
module color_base(){{if(joint=="single")union(){{faceplate();translate([tray_x,-0.01,tray_z])cube([tray_w,0.02+0.01,tray_t]);tray();if(rear_support)rear_bracket();}}else faceplate();}}
module color_clip(){{intersection(){{children();offset(delta=-{EDGE_KEEP})plate2d();}}}}
"""


def faceplate_source(s):
    return equipment.source(s) + SOURCE_HELPERS


def scad(r):
    left, top = r['origin']
    cw, ch = r['cell_mm']
    lines = ['// Multi-color faceplate artwork. PROPOSED — UNVALIDATED. Generated; do not edit.',
             'use <faceplate_source.scad>', 'part="base";', f'depth={DEPTH};', f'front_y={FRONT_Y};']
    names = []
    for b in r['bodies']:
        name = 'color_%d' % b['index']
        names.append(name)
        lines.append(f'module {name}(){{color_clip()union(){{')
        for x0, y0, x1, y1 in b['rects']:
            lines.append(f' translate([{left + x0 * cw:.4f},{top - y1 * ch:.4f}])square([{(x1 - x0) * cw:.4f},{(y1 - y0) * ch:.4f}]);')
        lines.append('}}')
    lines.append('module art_all(){union(){' + ''.join(n + '();' for n in names) + '}}')
    # 2D X = rack X, 2D Y = height Z; rotate([90,0,0]) extrudes toward -Y.
    if r['settings']['style'] == 'inlay':
        lines.append('if(part=="base")difference(){color_base();translate([0,front_y+depth,0])rotate([90,0,0])linear_extrude(height=depth+0.1)art_all();}')
        for n in names:
            lines.append(f'if(part=="{n}")translate([0,front_y+depth,0])rotate([90,0,0])linear_extrude(height=depth){n}();')
    else:
        lines.append('if(part=="base")color_base();')
        for n in names:
            lines.append(f'if(part=="{n}")translate([0,front_y,0])rotate([90,0,0])linear_extrude(height=depth){n}();')
    return '\n'.join(lines) + '\n', names


def export_identity(r, faceplate_source, art_source):
    """Cache key. The README and revision.json name each file's color, so colors are part of it
    (v1 keyed geometry only and could return a cached zip listing old colors)."""
    named = json.dumps({'base': r['base_hex'], 'bodies': [[b['index'], b['color']] for b in r['bodies']],
                        'image': r['clean']['name']}, sort_keys=True)
    return hashlib.sha256(('faceplate-color-v3\n' + faceplate_source + '\n' + art_source + '\n' + named).encode('utf-8')).hexdigest()


def export(art, s, metadata, data_dir, faceplate_color='#4e75a3'):
    """Render base + one body per color for the slot's cleaned equipment spec; returns a zip. Cached immutably by content."""
    r = reduce(art, data_dir, s, faceplate_color)
    if not r['bodies']:
        raise ValueError('Only the base color remains; there is nothing to export in a second color.')
    if r['rect_total'] > MAX_RECTS:
        raise ValueError(r['warnings'][-1])
    art_source, names = scad(r)
    base_hex = r['base_hex']
    source = faceplate_source(s)
    identity = export_identity(r, source, art_source)
    final = Path(data_dir) / 'faceplate-color-revisions' / identity
    with LOCK:
        if not final.exists():
            final.parent.mkdir(parents=True, exist_ok=True)
            exe = mesh_revision.compiler()
            with tempfile.TemporaryDirectory(dir=final.parent, prefix='render-') as temp:
                folder = Path(temp)
                (folder / 'faceplate_colors.scad').write_text(art_source, encoding='utf-8', newline='\n')
                files, logs, meshes, nudges = [], {}, {}, {}
                for part in ['base'] + names:
                    out = folder / (part + '.stl')
                    # Same OpenSCAD 2021 sliver repair as equipment.render(): retry the base with the plate nudged;
                    # color bodies then use the base's nudge, so their outline clip matches its pocket.
                    for nudge in ((0, 0.011, 0.023, 0.037, 0.051) if part == 'base' else (nudges['base'],)):
                        (folder / 'faceplate_source.scad').write_text(source + (f'nudge={nudge};\n' if nudge else ''), encoding='utf-8', newline='\n')
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
                        try:
                            mesh = mesh_revision.read_mesh(out, part)
                            break
                        except ValueError:
                            if nudge == 0.051 or part != 'base':
                                raise
                    nudges[part] = nudge
                    meshes[part] = {'signed_volume_mm3': round(mesh['signed_volume_mm3'], 3), 'bounds': mesh['bounds']}
                    files.append(part + '.stl')
                # The zip's source is the exact one rendered (with a nudge line only when the repair was needed).
                (folder / 'faceplate_source.scad').write_text(source + (f"nudge={nudges['base']};\n" if nudges['base'] else ''), encoding='utf-8', newline='\n')
                bodies = [{k: b[k] for k in ('index', 'color', 'area_mm2', 'volume_mm3', 'grams_estimate')} | {'file': 'color_%d.stl' % b['index']}
                          for b in r['bodies']]
                report = {'id': identity, 'status': 'PROPOSED — UNVALIDATED', 'style': r['settings']['style'],
                          'depth_mm': DEPTH, 'grid_mm': [round(v, 4) for v in r['cell_mm']],
                          'min_feature_mm': MIN_FEATURE, 'image': {k: r['clean'][k] for k in ('sha256', 'name', 'x', 'y', 'scale')},
                          'image_size_mm': r['size_mm'], 'image_origin_mm': [round(v, 4) for v in r['origin']],
                          'faceplate': {'template': 'equipment_tray.scad', 'u': s['u'], 'front_y_mm': FRONT_Y,
                                        'equipment_source_sha256': hashlib.sha256(equipment.source(s).encode('utf-8')).hexdigest(),
                                        'plate_height_mm': round(r['plate']['height_mm'], 4), 'joint': s['joint'],
                                        'keep_clear_mm': {'openings_and_rack_holes': OPENING_GAP, 'plate_outline_clip': EDGE_KEEP}},
                          'nudge_mm': nudges,
                          'base': {'file': 'base.stl', 'color': base_hex, 'note': 'The faceplate itself (with the tray for a single printed piece), printed in the base filament.'},
                          'bodies': bodies, 'warnings': r['warnings'], 'mesh': meshes, 'faceplate_revision': metadata,
                          'limitations': LIMITS, 'logs': logs,
                          'sha256': {f: hashlib.sha256((folder / f).read_bytes()).hexdigest() for f in files}}
                (folder / 'revision.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
                readme = ['Multi-color faceplate (PROPOSED — UNVALIDATED)', '',
                          'Load ALL .stl files together into your slicer as ONE multi-part object',
                          '(keep their positions; they share the same origin), then assign a filament to each:', '',
                          f'  base.stl     -> {base_hex}  (faceplate{" + tray, one piece" if s["joint"] == "single" else ""})']
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
