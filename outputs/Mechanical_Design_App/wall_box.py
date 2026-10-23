"""Wall-mount box (Brian, 2026-10-22; work/wall-box-wizard/Scope.md): spec validation and SCAD source.

PROPOSED - UNVALIDATED. Fit, hinge/latch/snap function, wall-mount load and strength are UNKNOWN until Brian prints and
tests a box. STL only. The keystone geometry is read from equipment_tray.scad (the golden keystone, ks_tight 0.2) so
there is one copy of it; wall_box.scad holds the box shape and the constants mirrored in CONST below.

Spec (JSON object; unknown keys are refused):
  inner: {w, d, h}          inner size in mm (d = depth from the front opening to the back wall)
  wall: 2.5                 1.6..4.0; a parameter, not a wall-thickness recommendation
  corner_radius: 3          0..10, outer radius of the front-to-back edges
  lid_style: screw | hinge | snap
  mount_style: keyhole | tabs | cleat
  vents: [wall, ...]        walls with slot vents; vents step around every cutout and feature automatically
  cutouts: [{wall, u, v, type: keystone | gland (size PG7/PG9) | round (d) | rect (w, h) | preset (preset)}]
  standoffs: [{x, z, height, hole, outer?}]   on the inside of the back wall, x/z from the centre seen from the front
Walls: lid, back, left, right, top, bottom. u is to the right and v up as seen from outside the wall (top/bottom: v
towards the back); 0,0 is the centre of the wall's inner area.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / 'wall_box.scad'
PARTS = HERE / 'wall_box_parts.json'
TRAY = HERE / 'equipment_tray.scad'

WALLS = ('lid', 'back', 'left', 'right', 'top', 'bottom')
LIDS = ('screw', 'hinge', 'snap')
MOUNTS = ('keyhole', 'tabs', 'cleat')
MAX_OUTER = 250.0
MARGIN = 2.0       # every cutout stays this far inside its wall's inner area and from other features
VENT_GAP = 3.0     # vents stay this far from cutouts and features
# Same numbers as wall_box.scad (test_wall_box checks they match).
CONST = {
    'boss_r': 5, 'boss_inset': 4, 'boss_len': 10, 'insert_pilot': 4.0, 'insert_depth': 8.2, 'm3_clear': 3.4,
    'lid_clear': 0.3, 'lip_t': 1.6, 'lip_h': 6, 'snap_y': 4, 'snap_r': 0.6, 'groove_r': 0.8,
    'hinge_r': 4, 'hinge_gap': 0.4, 'hinge_pin': 2.0, 'hinge_segments': 5,
    'latch_w': 18, 'latch_arm': 2, 'latch_reach': 7,
    'key_head': 9, 'key_slot': 4.5, 'key_rise': 9, 'key_from_top': 20, 'key_from_side': 15, 'key_max_x': 60,
    'tab_w': 20, 'tab_len': 16, 'tab_t': 4, 'tab_hole': 4.5,
    'cleat_c': 8, 'cleat_h': 25, 'cleat_hole': 4.5, 'spacer_h': 12,
    'vent_w': 2.5, 'vent_pitch': 5.5, 'vent_inset': 12,
}
KEYSTONE = (21.0, -15.0, 18.5)   # width, v from centre to the block bottom / top (the 21 x 33.5 golden block)
GLANDS = {'PG7': 12.5, 'PG9': 15.2}   # DIN 40430 thread outside diameter = clearance hole
GLAND_NUT_EXTRA = 8.0  # keep-out around a gland hole for its nut/seal; an estimate, check your gland


class WallBoxError(ValueError):
    def __init__(self, problems):
        self.problems = list(problems)
        super().__init__('; '.join(self.problems))


def load_parts():
    return json.loads(PARTS.read_text(encoding='utf-8'))


def _num(value, name, lo, hi, problems):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        problems.append(f'{name} must be a number.')
        return None
    if not lo <= value <= hi:
        problems.append(f'{name} must be between {lo:g} and {hi:g} mm (got {value:g}).')
        return None
    return float(value)


def _keys(obj, allowed, name, problems):
    if not isinstance(obj, dict):
        problems.append(f'{name} must be an object.')
        return False
    extra = sorted(set(obj) - set(allowed))
    if extra:
        problems.append(f'{name} has unknown settings: {", ".join(extra)}.')
    return True


def half(spec, wall):
    i = spec['inner']
    if wall in ('lid', 'back'):
        return i['w'] / 2, i['h'] / 2
    if wall in ('left', 'right'):
        return i['d'] / 2, i['h'] / 2
    return i['w'] / 2, i['d'] / 2


def outer_size(spec):
    """Outer X, Y, Z in mm including lid and wall mounts (the hinge and latch stick out sideways)."""
    t, i, c = spec['wall'], spec['inner'], CONST
    x = i['w'] + 2 * t
    if spec['lid_style'] == 'hinge':
        x += 2 * c['hinge_r'] + c['hinge_gap'] + 1.3 + c['latch_arm']
    y = i['d'] + 2 * t + (c['cleat_c'] if spec['mount_style'] == 'cleat' else 0)
    z = i['h'] + 2 * t + (2 * c['tab_len'] if spec['mount_style'] == 'tabs' else 0)
    return round(x, 4), round(y, 4), round(z, 4)


def footprint(cut):
    """Cutout rectangle (u0, v0, u1, v1) in its wall frame, including what must stay clear around the hole."""
    u, v, kind = cut['u'], cut['v'], cut['type']
    if kind == 'keystone':
        w, b, t = KEYSTONE
        return (u - w / 2, v + b, u + w / 2, v + t)
    if kind == 'gland':
        r = (GLANDS[cut['size']] + GLAND_NUT_EXTRA) / 2
    elif kind == 'round':
        r = cut['d'] / 2
    else:
        return (u - cut['w'] / 2, v - cut['h'] / 2, u + cut['w'] / 2, v + cut['h'] / 2)
    return (u - r, v - r, u + r, v + r)


def features(spec):
    """Keep-out rectangles per wall for the box's own features (bosses, lid lip, hinge, latch, mounts)."""
    c, t, i = CONST, spec['wall'], spec['inner']
    out = {w: [] for w in WALLS}
    hw, hh, hd = i['w'] / 2, i['h'] / 2, i['d'] / 2
    lid, mount = spec['lid_style'], spec['mount_style']
    if lid == 'screw':
        # Boss centres sit boss_inset in from the inner corner (wall frame of the lid/opening).
        cx, cz = hw - c['boss_inset'], hh - c['boss_inset']
        r = c['boss_r']
        for sx in (-1, 1):
            for sz in (-1, 1):
                out['lid'].append((sx * cx - r, sz * cz - r, sx * cx + r, sz * cz + r))
        # Bosses run boss_len back from the opening in each inner corner (2*boss_r across).
        reach, d = c['boss_len'], 2 * r
        for w in ('left', 'right', 'top', 'bottom'):
            front = (hd - reach, hd) if w == 'left' else (-hd, -hd + reach)
            span = hh if w in ('left', 'right') else hw
            for lo, hi in ((-span, -span + d), (span - d, span)):
                out[w].append((front[0], lo, front[1], hi) if w in ('left', 'right') else (lo, front[0], hi, front[1]))
    if lid == 'snap':
        band = c['lid_clear'] + c['lip_t'] + c['snap_r']
        out['lid'] += [(-hw, -hh, hw, -hh + band), (-hw, hh - band, hw, hh), (-hw, -hh, -hw + band, hh), (hw - band, -hh, hw, hh)]
        reach = c['snap_y'] + c['groove_r'] + 1
        out['left'].append((hd - reach, -hh, hd, hh))
        out['right'].append((-hd, -hh, -hd + reach, hh))
        out['top'].append((-hw, -hd, hw, -hd + reach))
        out['bottom'].append((-hw, -hd, hw, -hd + reach))
    if lid == 'hinge':
        out['left'].append((hd - (2 * c['hinge_r'] + c['hinge_gap'] + 0.5), -hh - t, hd, hh + t))
        out['right'].append((-hd, -c['latch_w'] / 2, -hd + c['latch_reach'] + 1, c['latch_w'] / 2))
    if mount == 'keyhole':
        x = min(hw - c['key_from_side'], c['key_max_x'])
        v = hh - c['key_from_top']
        r = c['key_head'] / 2
        for s in (-1, 1):
            out['back'].append((s * x - r, v - r, s * x + r, v + c['key_rise'] + c['key_slot'] / 2))
    if mount == 'cleat':
        out['back'].append((-hw, hh + t - c['cleat_h'], hw, hh))
        out['back'].append((-hw, -hh, hw, -hh - t + spec['corner_radius'] + c['spacer_h']))
    return out


def _overlap(a, b, gap=0.0):
    return a[0] < b[2] + gap and b[0] < a[2] + gap and a[1] < b[3] + gap and b[1] < a[3] + gap


def _resolve_cut(raw, parts, n, problems):
    name = f'Cutout {n}'
    if not _keys(raw, ('wall', 'u', 'v', 'type', 'size', 'd', 'w', 'h', 'preset'), name, problems):
        return None
    cut = dict(raw)
    if cut.get('type') == 'preset':
        preset = parts.get(cut.get('preset'))
        if preset is None:
            problems.append(f'{name}: unknown part preset "{cut.get("preset")}".')
            return None
        if preset.get('kind') != 'cutout' or preset.get('cutout') is None:
            problems.append(f'{name}: {preset.get("name", cut["preset"])} has no known size yet ({preset.get("note", "measure it first")}). '
                            'Its dimensions stay UNKNOWN; add a measured size before using it.')
            return None
        cut = {'wall': cut.get('wall'), 'u': cut.get('u'), 'v': cut.get('v'), **preset['cutout']}
    if cut.get('wall') not in WALLS:
        problems.append(f'{name}: wall must be one of {", ".join(WALLS)}.')
        return None
    kind = cut.get('type')
    need = {'keystone': (), 'gland': ('size',), 'round': ('d',), 'rect': ('w', 'h')}.get(kind)
    if need is None:
        problems.append(f'{name}: type must be keystone, gland, round, rect or preset.')
        return None
    out = {'wall': cut['wall'], 'type': kind}
    for key in ('u', 'v'):
        out[key] = _num(cut.get(key), f'{name} {key}', -MAX_OUTER, MAX_OUTER, problems)
    if kind == 'gland':
        if cut.get('size') not in GLANDS:
            problems.append(f'{name}: gland size must be PG7 or PG9.')
            return None
        out['size'] = cut['size']
    for key in need:
        if key != 'size':
            out[key] = _num(cut.get(key), f'{name} {key}', 1, 200, problems)
    if any(out.get(k) is None for k in ('u', 'v', *[k for k in need if k != 'size'])):
        return None
    return out


def validate(spec):
    """Return a normalised spec or raise WallBoxError with plain-language problems."""
    problems = []
    if not _keys(spec, ('inner', 'wall', 'corner_radius', 'lid_style', 'mount_style', 'vents', 'cutouts', 'standoffs'), 'The box', problems):
        raise WallBoxError(problems)
    inner = spec.get('inner')
    out = {}
    if _keys(inner, ('w', 'd', 'h'), 'inner', problems):
        out['inner'] = {k: _num(inner.get(k), f'Inner {name}', 20, MAX_OUTER, problems)
                        for k, name in (('w', 'width'), ('d', 'depth'), ('h', 'height'))}
    out['wall'] = _num(spec.get('wall', 2.5), 'Wall thickness', 1.6, 4.0, problems)
    out['corner_radius'] = _num(spec.get('corner_radius', 3), 'Corner radius', 0, 10, problems)
    for key, options, default in (('lid_style', LIDS, 'screw'), ('mount_style', MOUNTS, 'keyhole')):
        out[key] = spec.get(key, default)
        if out[key] not in options:
            problems.append(f'{key.replace("_", " ").capitalize()} must be one of {", ".join(options)}.')
    vents = spec.get('vents', [])
    if not isinstance(vents, list) or any(w not in WALLS for w in vents):
        problems.append(f'Vents must be a list of walls ({", ".join(WALLS)}).')
        vents = []
    out['vents'] = [w for w in WALLS if w in vents]
    if problems or any(v is None for v in out.get('inner', {None: None}).values()):
        raise WallBoxError(problems or ['Inner size is incomplete.'])

    t, i, c = out['wall'], out['inner'], CONST
    if out['corner_radius'] > min(i['w'], i['h']) / 2:
        problems.append('Corner radius is too large for this box.')
    size = outer_size(out)
    for axis, value in zip('XYZ', size):
        if value > MAX_OUTER:
            problems.append(f'Outer size {axis} would be {value:g} mm; the limit is {MAX_OUTER:g} mm (mounts and lid included).')
    if out['lid_style'] == 'screw' and i['d'] < c['boss_len'] + 2:
        problems.append(f'A screw lid needs at least {c["boss_len"] + 2} mm inner depth for its insert bosses.')
    if out['lid_style'] == 'snap' and i['d'] < c['lip_h'] + 2:
        problems.append(f'A snap lid needs at least {c["lip_h"] + 2} mm inner depth for its lip.')
    if out['mount_style'] == 'keyhole' and (i['h'] < 2 * c['key_from_top'] + c['key_rise'] or i['w'] < 2 * c['key_from_side'] + c['key_head']):
        problems.append('The box is too small for two keyhole slots; use tabs or a cleat.')
    if out['mount_style'] == 'cleat' and i['h'] + 2 * t < c['cleat_h'] + c['spacer_h'] + 10:
        problems.append('The box is too short for a French cleat; use keyholes or tabs.')
    if out['mount_style'] == 'tabs' and i['w'] + 2 * t < c['tab_w'] + 2 * out['corner_radius']:
        problems.append('The box is too narrow for the mounting tabs.')

    parts = load_parts()
    cuts = []
    raw_cuts = spec.get('cutouts', [])
    if not isinstance(raw_cuts, list):
        problems.append('Cutouts must be a list.')
        raw_cuts = []
    for n, raw in enumerate(raw_cuts, 1):
        cut = _resolve_cut(raw, parts, n, problems)
        if cut:
            cuts.append(cut)
    feats = features(out)
    for n, cut in enumerate(cuts, 1):
        fp = footprint(cut)
        hu, hv = half(out, cut['wall'])
        if fp[0] < -hu + MARGIN or fp[2] > hu - MARGIN or fp[1] < -hv + MARGIN or fp[3] > hv - MARGIN:
            problems.append(f'Cutout {n} ({cut["type"]}) on the {cut["wall"]} must stay {MARGIN:g} mm inside the wall\'s inner area '
                            f'(u ±{hu - MARGIN:g}, v ±{hv - MARGIN:g}).')
        if any(_overlap(fp, f, MARGIN) for f in feats[cut['wall']]):
            problems.append(f'Cutout {n} ({cut["type"]}) on the {cut["wall"]} hits a box feature (lid screws, lip, hinge, latch or wall mount).')
        for m, other in enumerate(cuts[:n - 1], 1):
            if other['wall'] == cut['wall'] and _overlap(fp, footprint(other), MARGIN):
                problems.append(f'Cutouts {m} and {n} on the {cut["wall"]} overlap or are closer than {MARGIN:g} mm.')
    out['cutouts'] = cuts

    stands = []
    raw_st = spec.get('standoffs', [])
    if not isinstance(raw_st, list):
        problems.append('Standoffs must be a list.')
        raw_st = []
    for n, raw in enumerate(raw_st, 1):
        name = f'Standoff {n}'
        if not _keys(raw, ('x', 'z', 'height', 'hole', 'outer'), name, problems):
            continue
        s = {'x': _num(raw.get('x'), f'{name} x', -MAX_OUTER, MAX_OUTER, problems),
             'z': _num(raw.get('z'), f'{name} z', -MAX_OUTER, MAX_OUTER, problems),
             'height': _num(raw.get('height'), f'{name} height', 1, MAX_OUTER, problems),
             'hole': _num(raw.get('hole'), f'{name} hole', 1, 10, problems)}
        if None in s.values():
            continue
        s['outer'] = _num(raw.get('outer', max(s['hole'] + 4, 6)), f'{name} outer', s['hole'] + 2, 20, problems)
        if s['outer'] is None:
            continue
        if s['height'] > i['d'] - 2:
            problems.append(f'{name} is taller than the inner depth allows ({i["d"] - 2:g} mm).')
        r = s['outer'] / 2
        # The back wall frame has u = -x (it is seen from behind).
        fp = (-s['x'] - r, s['z'] - r, -s['x'] + r, s['z'] + r)
        if fp[0] < -i['w'] / 2 + MARGIN or fp[2] > i['w'] / 2 - MARGIN or fp[1] < -i['h'] / 2 + MARGIN or fp[3] > i['h'] / 2 - MARGIN:
            problems.append(f'{name} must stay {MARGIN:g} mm inside the back wall.')
        if any(_overlap(fp, footprint(cut), MARGIN) for cut in cuts if cut['wall'] == 'back') or any(_overlap(fp, f, MARGIN) for f in feats['back']):
            problems.append(f'{name} hits a cutout or wall-mount feature on the back.')
        for m, other in enumerate(stands, 1):
            ro = other['outer'] / 2
            if _overlap(fp, (-other['x'] - ro, other['z'] - ro, -other['x'] + ro, other['z'] + ro)):
                problems.append(f'Standoffs {m} and {n} overlap.')
        s['_fp'] = fp
        stands.append(s)
    out['standoffs'] = stands
    if problems:
        raise WallBoxError(problems)
    return out


def vent_avoid(spec):
    rows = []
    for w in spec['vents']:
        rects = list(features(spec)[w])
        rects += [footprint(c) for c in spec['cutouts'] if c['wall'] == w]
        if w == 'back':
            rects += [s['_fp'] for s in spec['standoffs']]
        rows += [(w, r[0] - VENT_GAP, r[1] - VENT_GAP, r[2] + VENT_GAP, r[3] + VENT_GAP) for r in rects]
    return rows


def _f(x):
    text = f'{float(x):.4f}'.rstrip('0').rstrip('.')
    return '0' if text in ('-0', '') else text


def _s(x):
    return json.dumps(x)


def _keystone_block():
    text = TRAY.read_text(encoding='utf-8')
    tight = re.search(r'^ks_tight=[^;]+;', text, re.M).group(0)
    gold = re.search(r'^KS_GOLD=\[.*?\n\];', text, re.M | re.S).group(0)
    return tight + '\n' + gold


def scad_source(spec, part='all'):
    """Deterministic OpenSCAD source for a validated spec."""
    if part not in ('all', 'body', 'lid', 'cleat'):
        raise WallBoxError(['Part must be all, body, lid or cleat.'])
    if part == 'cleat' and spec['mount_style'] != 'cleat':
        raise WallBoxError(['Only a cleat-mounted box has a cleat rail.'])
    i = spec['inner']
    cuts = []
    for c in spec['cutouts']:
        a = GLANDS[c['size']] if c['type'] == 'gland' else c.get('d', c.get('w', 0))
        b = c.get('h', 0)
        cuts.append(f'[{_s(c["wall"])},{_s(c["type"])},{_f(c["u"])},{_f(c["v"])},{_f(a)},{_f(b)}]')
    stands = [f'[{_f(s["x"])},{_f(s["z"])},{_f(s["height"])},{_f(s["hole"])},{_f(s["outer"])}]' for s in spec['standoffs']]
    avoid = [f'[{_s(r[0])},{",".join(_f(v) for v in r[1:])}]' for r in vent_avoid(spec)]
    params = '\n'.join([
        f'part={_s(part)};',
        f'inner_w={_f(i["w"])}; inner_d={_f(i["d"])}; inner_h={_f(i["h"])};',
        f'wall={_f(spec["wall"])};',
        f'corner_r={_f(spec["corner_radius"])};',
        f'lid_style={_s(spec["lid_style"])};',
        f'mount_style={_s(spec["mount_style"])};',
        f'vents=[{",".join(_s(w) for w in spec["vents"])}];',
        f'cutouts=[{",".join(cuts)}];',
        f'standoffs=[{",".join(stands)}];',
        f'vent_avoid=[{",".join(avoid)}];',
    ])
    text = TEMPLATE.read_text(encoding='utf-8')
    text = re.sub(r'// @@PARAMS@@\n.*?// @@END@@', lambda _: '// @@PARAMS@@\n' + params + '\n// @@END@@', text, count=1, flags=re.S)
    text = re.sub(r'// @@KEYSTONE@@\n.*?// @@END@@', lambda _: '// @@KEYSTONE@@\n' + _keystone_block() + '\n// @@END@@', text, count=1, flags=re.S)
    return text.replace('\r\n', '\n')


def template_constants():
    """Constants as written in wall_box.scad (for the consistency test)."""
    text = TEMPLATE.read_text(encoding='utf-8')
    return {k: float(re.search(rf'\b{k}=([-0-9.]+);', text).group(1)) for k in CONST}


if __name__ == '__main__':
    import sys
    if len(sys.argv) not in (3, 4):
        sys.exit('usage: wall_box.py spec.json out.scad [all|body|lid|cleat]')
    try:
        spec = validate(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')))
    except WallBoxError as error:
        sys.exit('\n'.join(error.problems))
    Path(sys.argv[2]).write_text(scad_source(spec, sys.argv[3] if len(sys.argv) == 4 else 'all'), encoding='utf-8', newline='\n')
