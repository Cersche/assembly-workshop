"""Equipment wizard (phase 1): dimensions -> tray + faceplate STL via OpenSCAD.

Generated parts are PROPOSED and UNVALIDATED; printed fit, strength and rack
clearance remain UNKNOWN. All equipment uses the generic tray adapter.
"""

import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import secrets
import subprocess
import tempfile
import threading
import zipfile

import cable_ports
import port_openings
import mesh_revision

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / 'equipment_tray.scad'
MOUNTS = ('inserts', 'pegs', 'clips', 'straps', 'flat')
JOINTS = ('screw', 'single')
# Snap-fit faceplate-to-tray joint retired by Brian 2026-10-19: the printed coupon was too brittle to carry the tray.
# equipment_tray.scad keeps its geometry as history only; new specs cannot choose it.
PLATE_HALF = 126
LOCK = threading.Lock()
REBUILD_LOCK = threading.Lock()
# Export quality (Brian, 2026-10-19): OpenSCAD curve resolution for equipment_tray.scad STLs. "standard" is the
# template's own $fn=48 and writes nothing extra, so standard sources (and their build ids) stay byte-identical.
# Curve resolution changes the mesh only; fit and strength stay UNKNOWN at every level.
EXPORT_QUALITY = {'draft': 24, 'standard': 48, 'fine': 96}
DEFAULT_QUALITY = 'standard'
LIMITS = ['PROPOSED — UNVALIDATED. Printed fit, strength, rack clearance and keystone retention are UNKNOWN.',
          'Mesh closure and successful rendering are not physical approval.']


def num(value, name, lo, hi):
    try:
        v = float(value)
    except (TypeError, ValueError):
        raise ValueError(name + ' must be a number.')
    if not math.isfinite(v) or v < lo or v > hi:
        raise ValueError(f'{name} must be between {lo} and {hi} mm.')
    return round(v, 3)


def _port_id(port, face, index):
    """Stable cable-planning id for a wizard port; older specs without one fall back to their position."""
    ident = port.get('id')
    if isinstance(ident, str) and cable_ports.PORT_ID.fullmatch(ident) and not ident.startswith('ks-'):
        return ident
    return f'{face}-{index + 1}'


# Option 1 data model (Brian, 2026-10-19): the library item keeps facts about the equipment (name, size,
# model file, holes, ports); these tray choices belong to each slot allocation's "tray" settings. Older
# library specs still carry them, and those values stay the defaults when an allocation has none.
PLACEMENT_KEYS = ('dev_off_x', 'dev_off_y', 'dev_rot', 'device_mount', 'standoff', 'insert_pilot', 'board_t',
                  'joint', 'keystones', 'rear_support', 'u')


def export_quality(s):
    """Traceability record for a cleaned spec: the quality level and the $fn it puts in the source."""
    level = s.get('quality', DEFAULT_QUALITY)
    return {'level': level, '$fn': EXPORT_QUALITY[level]}


def placement_settings(value):
    """Keep only known tray-choice keys from an allocation's settings (full checks happen in clean())."""
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError('Tray settings must be an object.')
    out = {}
    for key in PLACEMENT_KEYS:
        if key not in value:
            continue
        v = value[key]
        if key == 'keystones':
            if not isinstance(v, list) or len(v) > 12 or any(type(x) not in (int, float) or isinstance(x, bool) for x in v):
                raise ValueError('Keystones must be a list of positions.')
            v = list(v)
        elif key == 'rear_support':
            if type(v) is not bool:
                raise ValueError('Rear support must be true or false.')
        elif key in ('device_mount', 'joint'):
            if not isinstance(v, str) or len(v) > 20:
                raise ValueError('Invalid tray setting: ' + key + '.')
        elif type(v) not in (int, float) or isinstance(v, bool) or not math.isfinite(v):
            raise ValueError('Invalid tray setting: ' + key + '.')
        out[key] = v
    return out


def device_facts(spec):
    """The library-item part of a spec: everything except the per-allocation tray choices."""
    return {k: v for k, v in spec.items() if k not in PLACEMENT_KEYS}


def allocation_spec(item_spec, tray=None):
    """Spec for one slot allocation: library values are defaults, the allocation's tray settings win.
    With no tray settings this returns the library spec unchanged, so older items build identically."""
    merged = dict(item_spec)
    settings = placement_settings(tray)
    merged.update(settings)
    # Brian, 2026-10-19: front openings follow the device (left/right offset, standoff); a turned device keeps them
    # where they were entered (port_openings explains this in Place on tray). Library builds are unchanged.
    if settings and item_spec.get('ports'):
        merged['ports'] = port_openings.front_openings(item_spec, settings)['ports']
    return merged


def allocation_request(data_dir, payload):
    """Place on tray window: {'item': library id, 'tray': slot tray settings} -> cleaned spec.
    Equipment facts always come from the saved library item; only the tray choices come from the request."""
    if not isinstance(payload, dict):
        raise ValueError('Placement request must be an object.')
    ident = payload.get('item')
    item = next((i for i in library(data_dir) if i.get('id') == ident), None) if isinstance(ident, str) else None
    if item is None:
        raise ValueError('This equipment is no longer in the library.')
    spec = allocation_spec(item['spec'], payload.get('tray'))
    # Plain-language opening guards (plate edge, top/bottom, keystone block) before clean()'s generic bounds.
    try:  # malformed values are left to clean()'s own messages
        found = port_openings.problems(list(spec.get('ports') or []), int(spec.get('u', 1)), list(spec.get('keystones') or []))
    except (TypeError, ValueError, AttributeError, KeyError):
        found = []
    if found:
        raise ValueError(found[0])
    if 'quality' in payload:  # export quality is a per-export choice, never a saved tray setting
        spec['quality'] = payload['quality']
    return clean(spec)


def cached_allocation_render(data_dir, payload):
    """Rack view: does an exact OpenSCAD render of this slot's settings already exist? Looks only; never renders.
    Standard quality is tried first, then the other export levels. -> {'cached': bool, 'id', 'parts', 'quality'}"""
    for level in [DEFAULT_QUALITY] + [q for q in EXPORT_QUALITY if q != DEFAULT_QUALITY]:
        try:
            s = allocation_request(data_dir, dict(payload, quality=level) if isinstance(payload, dict) else payload)
        except ValueError as exc:
            return {'cached': False, 'error': str(exc)}
        identity = hashlib.sha256(source(s).encode('utf-8')).hexdigest()
        report = Path(data_dir) / 'equipment-revisions' / identity / 'revision.json'
        if report.is_file():
            parts = json.loads(report.read_text(encoding='utf-8')).get('parts', [])
            return {'cached': True, 'id': identity, 'parts': parts, 'quality': level}
    return {'cached': False}


def check_allocation(data_dir, payload):
    """Run the same checks as a build (clean()) without rendering, writing or saving anything."""
    try:
        s = allocation_request(data_dir, payload)
    except ValueError as exc:
        return {'ok': False, 'error': str(exc)}
    return {'ok': True, 'u': s['u']}


RACK_PITCH, PLATE_GAP, LEGACY_SLOT_OFFSET = port_openings.RACK_PITCH, port_openings.PLATE_GAP, port_openings.LEGACY_SLOT_OFFSET

FRONT_GAP, MARGIN = 12, 8  # mirror front_gap / margin in equipment_tray.scad


def floor_z(spec):
    return 0.5 if spec.get('device_mount') == 'flat' else 7 + LEGACY_SLOT_OFFSET


def device_lift(spec):
    return floor_z(spec) + 3 + (0 if spec.get('device_mount') in ('straps', 'flat') else float(spec.get('standoff', 6)))


def needed_height(spec):
    mount = spec.get('device_mount')
    extra = (float(spec.get('board_t', 1.6)) + (1.6 if mount == 'pegs' else 2.5)) if mount in ('pegs', 'clips') else 0
    return max(device_lift(spec) + max(float(spec['dev_h']), extra),
               floor_z(spec) + 22 if spec.get('joint', 'screw') == 'screw' else 0)


def template_source(spec):
    # New builds always use the current slot-bottom template; saved revisions remain immutable.
    return TEMPLATE.read_text(encoding='utf-8')


def clean(spec):
    if not isinstance(spec, dict):
        raise ValueError('Equipment spec must be an object.')
    name = str(spec.get('name') or 'Equipment').strip()[:60] or 'Equipment'
    s = {'name': name,
         'dev_w': num(spec.get('dev_w'), 'Width', 5, 230),
         'dev_d': num(spec.get('dev_d'), 'Depth', 5, 220),
         'dev_h': num(spec.get('dev_h'), 'Height', 1, 300),
         'hole_d': num(spec.get('hole_d', 2.7), 'Hole diameter', 1.5, 8),
         'standoff': num(spec.get('standoff', 6), 'Standoff', 0, 30),
         'insert_pilot': num(spec.get('insert_pilot', 3.2), 'Insert pilot', 1.5, 8),
         'board_t': num(spec.get('board_t', 1.6), 'Board thickness', 0.5, 6),
         'u': int(num(spec.get('u', 1), 'Rack units', 1, 5))}
    s['device_mount'] = spec.get('device_mount') if spec.get('device_mount') in MOUNTS else None
    if spec.get('joint') == 'snap':
        raise ValueError('The snap-fit tray joint is retired (too brittle to hold the tray); use the screw joint.')
    s['joint'] = spec.get('joint') if spec.get('joint') in JOINTS else None
    if not s['device_mount'] or not s['joint']:
        raise ValueError('Choose a device mounting option and a tray joint.')
    s['rear_support'] = spec.get('rear_support') is True
    if s['rear_support']:
        if s['joint'] == 'single':
            raise ValueError('Rear-post support needs the screw joint (a 240 mm single print is not offered).')
        if s['dev_d'] > 200:
            raise ValueError('With rear-post support the device can be at most 200 mm deep.')
    # Placement on the tray (older library items have none of these keys = centred, unrotated).
    try:
        rot = float(spec.get('dev_rot', 0) or 0)
    except (TypeError, ValueError):
        rot = -1
    if rot not in (0, 90, 180, 270):
        raise ValueError('Rotation must be 0, 90, 180 or 270 degrees.')
    s['dev_rot'] = int(rot)
    s['dev_off_x'] = num(spec.get('dev_off_x', 0) or 0, 'Left/right offset', -115, 115)
    try:
        if float(spec.get('dev_off_y', 0) or 0) < -FRONT_GAP:  # equipment_tray.scad assert dev_y>=0
            raise ValueError('The device is moved into the faceplate; the front gap must be at least 0 mm.')
    except (TypeError, ValueError) as exc:
        if 'faceplate' in str(exc):
            raise
    s['dev_off_y'] = num(spec.get('dev_off_y', 0) or 0, 'Front/back offset', -FRONT_GAP, 230)
    fp_w, fp_d = (s['dev_d'], s['dev_w']) if s['dev_rot'] in (90, 270) else (s['dev_w'], s['dev_d'])
    if 2 * (abs(s['dev_off_x']) + fp_w / 2 + MARGIN) > 230:
        raise ValueError('The device is moved off the tray (the tray would be wider than 230 mm); reduce the left/right offset.')
    if s['rear_support'] and FRONT_GAP + s['dev_off_y'] + fp_d + MARGIN > 240:
        raise ValueError('The device is moved past the rear posts; reduce the front/back offset.')
    if s['device_mount'] == 'flat':
        if FRONT_GAP + s['dev_off_y'] < 6.2:
            raise ValueError('Flat corner stops need a front gap of at least 6.2 mm.')
        if s['joint'] == 'screw' and FRONT_GAP + s['dev_off_y'] < 11.5:
            raise ValueError('Flat device must clear the front screw joint (front gap >= 11.5 mm).')
        if s['rear_support'] and FRONT_GAP + s['dev_off_y'] + fp_d > 240 - 11.5:
            raise ValueError('Flat device must clear the rear screw joint (rear gap >= 11.5 mm).')
    q = spec.get('quality', DEFAULT_QUALITY)
    if q not in EXPORT_QUALITY:
        raise ValueError('Export quality must be draft, standard or fine.')
    if q != DEFAULT_QUALITY:  # kept only when not standard, so standard specs stay identical to older ones
        s['quality'] = q
    s['coupon'] = []
    c = spec.get('coupon')
    if c:
        s['coupon'] = [num(c[0], 'Coupon X0', -130, 130), num(c[1], 'Coupon X1', -130, 130), num(c[2], 'Coupon depth', 5, 250)]
    if needed_height(s) > s['u'] * RACK_PITCH:
        raise ValueError('Device is taller than %dU allows; pick more rack units.' % s['u'])
    s['holes'] = [[num(x, 'Hole X', 0, s['dev_w']), num(y, 'Hole Y', 0, s['dev_d'])]
                  for x, y in (spec.get('holes') or [])][:16]
    if s['device_mount'] in ('inserts', 'pegs') and not s['holes']:
        raise ValueError('Add at least one mounting hole for inserts or pegs.')
    plate_h = s['u'] * RACK_PITCH - PLATE_GAP
    s['keystones'] = [num(x, 'Keystone X', -PLATE_HALF + 24, PLATE_HALF - 24) for x in (spec.get('keystones') or [])][:12]
    xs = sorted(s['keystones'])
    if any(b - a < 21 for a, b in zip(xs, xs[1:])):
        raise ValueError('Keystones must be at least 21 mm apart.')
    # Keystone collars (golden SG108 copy and v2 fallback: 19.8 mm wide) reach 10.4 mm behind the plate, so they must clear the tray.
    tray_half = abs(s['dev_off_x']) + fp_w / 2 + MARGIN
    if any(abs(x) - 9.9 < tray_half + 0.5 for x in s['keystones']):
        raise ValueError(f'A keystone collar would hit the tray; keep keystones at least {tray_half + 10.4:g} mm from centre.')
    s['ports'] = []
    for p in (spec.get('ports') or [])[:20]:
        w, h = num(p.get('w'), 'Port width', 1, 200), num(p.get('h'), 'Port height', 1, plate_h - 4)
        s['ports'].append({'label': str(p.get('label') or '')[:30],
                           'x': num(p.get('x'), 'Port X', -PLATE_HALF + w / 2, PLATE_HALF - w / 2),
                           'z': num(p.get('z'), 'Port Z', PLATE_GAP / 2 + h / 2 + 2, PLATE_GAP / 2 + plate_h - h / 2 - 2),
                           'w': w, 'h': h, 'r': num(p.get('r', 0), 'Corner radius', 0, 50),
                           # Connector type is cable-planning data only; source() never passes it to OpenSCAD.
                           'type': cable_ports.port_type(p.get('type')), 'id': _port_id(p, 'front', len(s['ports']))})
    # Rear ports: planning data only (no cut-outs). X from the plate centre, Z from the plate bottom, as for front ports;
    # they sit on the device's rear face. Positions are what the user enters; connector fit and cable access UNKNOWN.
    s['rear_ports'] = []
    for p in (spec.get('rear_ports') or [])[:20]:
        if not isinstance(p, dict):
            raise ValueError('Each rear port must be an object.')
        s['rear_ports'].append({'id': _port_id(p, 'rear', len(s['rear_ports'])),
                                'label': str(p.get('label') or '')[:30], 'type': cable_ports.port_type(p.get('type')),
                                'x': num(p.get('x'), 'Rear port X', -PLATE_HALF, PLATE_HALF),
                                'z': num(p.get('z'), 'Rear port Z', 0, s['u'] * RACK_PITCH)})
    # Brian, 2026-10-19 (option 3): each tray screw joint sits where it clears the openings (an opening in front of it
    # would be blocked, and can fail to render) and keystones (16 mm, as before). joint_x is derived, never taken from
    # input, and kept only when a joint moved, so designs whose default joints were clear build exactly as before.
    if s['joint'] == 'screw':
        placed = port_openings.joint_positions(s['ports'], s['keystones'], tray_half)
        if placed['problem']:
            raise ValueError(placed['problem'])
        if placed['moved']:
            s['joint_x'] = placed['joints']
    ids = [p['id'] for p in s['ports'] + s['rear_ports']]
    if len(ids) != len(set(ids)):
        raise ValueError('Each port needs its own id.')
    if 'planning_ports' in spec:
        s['planning_ports'] = cable_ports.planning_ports(spec['planning_ports'], s['u'])
    return s


def source(s):
    def lit(v):
        return json.dumps(v)
    over = {k: s[k] for k in ('dev_w', 'dev_d', 'dev_h', 'hole_d', 'standoff', 'insert_pilot', 'board_t', 'u',
                              'holes', 'keystones', 'device_mount', 'joint', 'rear_support', 'coupon')}
    # Placement keys are written only when moved/rotated, so default sources stay byte-identical to older ones.
    for k in ('dev_off_x', 'dev_off_y', 'dev_rot', 'joint_x'):
        if s.get(k):
            over[k] = s[k]
    over['ports'] = [[p['x'], p['z'], p['w'], p['h'], p['r']] for p in s['ports']]
    # Export quality: only a non-standard level overrides the template's $fn=48 (last assignment wins in OpenSCAD).
    if s.get('quality', DEFAULT_QUALITY) != DEFAULT_QUALITY:
        over['$fn'] = EXPORT_QUALITY[s['quality']]
    lines = ['', '// ---- wizard overrides: ' + re.sub(r'[\r\n]', ' ', s['name'])] + [f'{k}={lit(v)};' for k, v in over.items()]
    return template_source(s) + '\n'.join(lines) + '\n'


def library(data_dir):
    path = Path(data_dir) / 'equipment-library.json'
    items = json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
    from equipment_examples import example_item
    example = example_item()
    return items if any(i['id'] == example['id'] for i in items) else items + [example]


def template_status(data_dir, item):
    """Read-only source/hash screening. No rendering, writes or physical approval."""
    unknown = {'status': 'unknown_evidence', 'reason': 'Template status unknown — build evidence unavailable.'}
    if not isinstance(item, dict):
        return unknown
    identity = item.get('build')
    if not isinstance(identity, str) or not re.fullmatch('[0-9a-f]{64}', identity):
        return unknown
    try:
        current = source(clean(item.get('spec'))).encode('utf-8')
    except (ValueError, TypeError, KeyError, IndexError) as exc:
        return {'status': 'needs_review', 'reason': str(exc)}
    except OSError:
        return unknown
    root = Path(data_dir) / 'equipment-revisions'
    folder = root / identity
    bad = {'status': 'integrity_problem', 'reason': 'Build integrity problem; saved evidence disagrees.'}
    try:
        if folder.resolve().parent != root.resolve():
            return bad
        if any((folder / name).resolve().parent != folder.resolve() for name in ('equipment.scad', 'revision.json')):
            return bad
        saved_source = (folder / 'equipment.scad').read_bytes()
        report = json.loads((folder / 'revision.json').read_text(encoding='utf-8'))
        if not isinstance(report, dict):
            return unknown
        parts = report.get('parts')
        allowed = {'tray', 'faceplate', 'combined', 'rear_bracket'}
        if (not isinstance(parts, list) or not parts or
                any(not isinstance(p, str) or p not in allowed for p in parts) or len(set(parts)) != len(parts)):
            return unknown
        hashes = report.get('sha256')
        if not isinstance(hashes, dict):
            return unknown
        if (report.get('id') != identity or item.get('parts') != parts or
                hashlib.sha256(saved_source).hexdigest() != identity):
            return bad
        for part in parts:
            filename = part + '.stl'
            expected = hashes.get(filename)
            if not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected):
                return unknown
            asset = folder / filename
            if asset.resolve().parent != folder.resolve():
                return bad
            if hashlib.sha256(asset.read_bytes()).hexdigest() != expected:
                return bad
    except (FileNotFoundError, OSError, ValueError, UnicodeError):
        return unknown
    status = 'matches_source_unknown_pipeline' if saved_source == current else 'older_source'
    return {'status': status, 'reason': ('Matches current source; build process unknown' if status.startswith('matches')
                                       else 'Older template/source — rebuild available. Change details unavailable.')}


def rebuild_copy(data_dir, item_id, expected_build):
    """Explicit create-copy action; serialize duplicate requests in this process only."""
    if not isinstance(item_id, str) or not re.fullmatch('eq-[0-9a-f]{12}', item_id):
        raise ValueError('Equipment not found.')
    if not isinstance(expected_build, str) or not re.fullmatch('[0-9a-f]{64}', expected_build):
        raise ValueError('Invalid expected build.')
    with REBUILD_LOCK:
        items = library(data_dir)
        original = next((i for i in items if i['id'] == item_id), None)
        if original is None:
            raise ValueError('Equipment not found.')
        if original.get('build') != expected_build:
            raise ValueError('This item changed while rebuilding. Reload its library details and try again. Your rack draft is still available.')
        status = template_status(data_dir, original)
        if status['status'] not in ('older_source', 'matches_source_unknown_pipeline'):
            raise ValueError(status['reason'])
        s = clean(original['spec'])
        target = hashlib.sha256(source(s).encode('utf-8')).hexdigest()
        # Same origin and current target: a repeated/double-click request returns its existing copy.
        for item in items:
            if (item.get('rebuilt_from_item') == item_id and item.get('rebuilt_from_build') == expected_build
                    and item.get('build') == target):
                if template_status(data_dir, item)['status'] != 'matches_source_unknown_pipeline':
                    raise ValueError('Build integrity problem; existing copy cannot be reused.')
                return {'item': item, 'reused_build': True, 'already_created': True}
        folder = Path(data_dir) / 'equipment-revisions' / target
        reused = folder.exists()
        if reused:
            try:
                parts = json.loads((folder / 'revision.json').read_text(encoding='utf-8'))['parts']
            except (OSError, ValueError, KeyError, TypeError) as exc:
                raise ValueError('Build integrity problem; target cache cannot be reused.') from exc
            candidate = {'spec': s, 'build': target, 'parts': parts}
            if template_status(data_dir, candidate)['status'] != 'matches_source_unknown_pipeline':
                raise ValueError('Build integrity problem; target cache cannot be reused.')
        # Existing render() preserves old folders and can reuse a verified current-source build.
        rendered = render(s, data_dir)
        report = json.loads((rendered / 'revision.json').read_text(encoding='utf-8'))
        candidate = {'spec': s, 'build': target, 'parts': report['parts']}
        if template_status(data_dir, candidate)['status'] != 'matches_source_unknown_pipeline':
            raise ValueError('Build integrity problem; rebuilt evidence could not be verified.')
        # Recheck after rendering without replacing or repinning any original item/placement.
        items = library(data_dir)
        latest = next((i for i in items if i['id'] == item_id), None)
        if latest != original:
            raise ValueError('This item changed while rebuilding. Reload its library details and try again. Your rack draft is still available.')
        ident = 'eq-' + secrets.token_hex(6)
        while any(i['id'] == ident for i in items):
            ident = 'eq-' + secrets.token_hex(6)
        display = (original.get('display_name') or original['name']) + ' (current template copy)'
        item = {'id': ident, 'name': display, 'display_name': display, 'span': s['u'], 'spec': s,
                'build': target, 'parts': report['parts'], 'status': 'PROPOSED — UNVALIDATED',
                'rebuilt_from_item': item_id, 'rebuilt_from_build': expected_build}
        path = Path(data_dir) / 'equipment-library.json'
        # Append before the closing array bracket, preserving the serialized old entries verbatim.
        raw = path.read_bytes()
        if json.loads(raw) != [i for i in items if not i.get('example')]:
            raise ValueError('Equipment library changed; reload its details and try again.')
        end = len(raw.rstrip()) - 1
        if raw[end:end + 1] != b']':
            raise ValueError('Invalid equipment library.')
        addition = (',\n' if items else '\n') + json.dumps(item, indent=2, ensure_ascii=False) + '\n'
        tmp = path.with_suffix('.rebuild.tmp')
        tmp.write_bytes(raw[:end] + addition.encode('utf-8') + raw[end:])
        tmp.replace(path)
        return {'item': item, 'reused_build': reused, 'already_created': False}


def save_item(spec, data_dir):
    """Build (or reuse) the meshes, then add/replace the item in the library."""
    s = clean(spec)
    zipped = build(s, data_dir)
    with zipfile.ZipFile(io.BytesIO(zipped)) as z:
        report = json.loads(z.read('revision.json'))
    items = library(data_dir)
    ident = spec.get('id') if isinstance(spec.get('id'), str) and re.fullmatch('eq-[0-9a-f]{12}', spec.get('id') or '') else 'eq-' + secrets.token_hex(6)
    item = {'id': ident, 'name': s['name'], 'span': s['u'], 'spec': s, 'build': report['id'], 'parts': report['parts'],
            'status': 'PROPOSED — UNVALIDATED'}
    if isinstance(spec.get('display_name'), str) and spec['display_name'].strip():
        item['display_name'] = spec['display_name'].strip()[:120]
        item['name'] = item['display_name']
    previous = next((i for i in items if i['id'] == ident), {})
    for key in ('rebuilt_from_item', 'rebuilt_from_build'):
        if key in previous:
            item[key] = previous[key]
    items = [i for i in items if i['id'] != ident] + [item]
    path = Path(data_dir) / 'equipment-library.json'
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(items, indent=2), encoding='utf-8')
    tmp.replace(path)
    return item


def delete_item(ident, data_dir, in_use):
    """Remove a library entry; rendered meshes stay in equipment-revisions/ (immutable cache)."""
    if ident in in_use:
        raise ValueError('This equipment is placed in a saved rack slot. Release that slot and Save first.')
    items = library(data_dir)
    if not any(i['id'] == ident for i in items):
        raise ValueError('Equipment not found.')
    path = Path(data_dir) / 'equipment-library.json'
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps([i for i in items if i['id'] != ident], indent=2), encoding='utf-8')
    tmp.replace(path)
    return {'deleted': ident}


def mesh_file(data_dir, identity, part):
    if not re.fullmatch('[0-9a-f]{64}', identity or '') or part not in ('tray', 'faceplate', 'combined', 'rear_bracket'):
        raise ValueError('Invalid equipment mesh request.')
    return (Path(data_dir) / 'equipment-revisions' / identity / (part + '.stl')).read_bytes()


def scad_to_stl(payload):
    """Render an uploaded equipment .scad to ASCII STL for the wizard's import step (nothing is stored)."""
    text = payload.get('source') if isinstance(payload, dict) else None
    if not isinstance(text, str) or not text.strip():
        raise ValueError('The SCAD file is empty.')
    if len(text) > 2_000_000:
        raise ValueError('SCAD file is too large (2 MB limit).')
    with tempfile.TemporaryDirectory(prefix='scad-import-') as temp:
        src, out = Path(temp) / 'model.scad', Path(temp) / 'model.stl'
        src.write_text(text, encoding='utf-8', newline='\n')
        try:
            r = subprocess.run([mesh_revision.compiler(), '--export-format', 'asciistl', '-o', str(out), str(src)],
                               capture_output=True, text=True, timeout=180,
                               creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ValueError('OpenSCAD failed or timed out: ' + str(exc)) from exc
        if r.returncode or 'ERROR:' in r.stderr or not out.exists():
            hint = ' (Files it includes/uses were not uploaded; paste them into one file.)' if re.search(r'\b(include|use)\s*<', text) else ''
            raise ValueError('OpenSCAD could not render this file' + hint + ': ' + r.stderr[-800:])
        return out.read_bytes()


FREECAD_SCRIPT = '''import os, Part, MeshPart
shape = Part.read(os.environ["EW_STEP_IN"])
mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.1, AngularDeflection=0.35)
mesh.write(os.environ["EW_STL_OUT"])
'''


def freecad():
    for base in sorted(Path('C:/Program Files').glob('FreeCAD*'), reverse=True):
        exe = base / 'bin' / 'freecadcmd.exe'
        if exe.exists():
            return str(exe)
    raise ValueError('FreeCAD is not installed, so STEP files cannot be read. Install FreeCAD or import an STL.')


def step_to_stl(payload):
    """Convert an uploaded STEP model to STL via FreeCAD's command-line tool (nothing is stored)."""
    text = payload.get('source') if isinstance(payload, dict) else None
    if not isinstance(text, str) or 'ISO-10303' not in text[:200]:
        raise ValueError('That does not look like a STEP file.')
    if len(text) > 60_000_000:
        raise ValueError('STEP file is too large (60 MB limit).')
    with tempfile.TemporaryDirectory(prefix='step-import-') as temp:
        folder = Path(temp)
        (folder / 'model.step').write_text(text, encoding='utf-8', newline='\n')
        (folder / 'convert.py').write_text(FREECAD_SCRIPT, encoding='utf-8')
        env = dict(os.environ, EW_STEP_IN=str(folder / 'model.step'), EW_STL_OUT=str(folder / 'model.stl'))
        try:
            r = subprocess.run([freecad(), str(folder / 'convert.py')], capture_output=True, text=True, timeout=300, env=env,
                               creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ValueError('FreeCAD failed or timed out: ' + str(exc)) from exc
        out = folder / 'model.stl'
        if not out.exists() or out.stat().st_size < 100:
            raise ValueError('FreeCAD could not convert this STEP file: ' + (r.stderr or r.stdout)[-800:])
        return out.read_bytes()


def build(spec, data_dir):
    final = render(spec, data_dir)
    s = clean(spec)
    # export.json ties this zip's meshes to their source settings, also for builds cached before quality existed.
    trace = {'export_quality': export_quality(s), 'source_sha256': final.name, 'source': 'equipment.scad',
             'status': 'PROPOSED — UNVALIDATED', 'note': 'Curve resolution only; printed fit and strength stay UNKNOWN.'}
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(final.iterdir()):
            z.write(f, f.name)
        z.writestr('export.json', json.dumps(trace, indent=2))
    return stream.getvalue()


def preview(spec, data_dir):
    """Render (or reuse) the parts and return ids so the wizard can fetch meshes for its 3D view."""
    final = render(spec, data_dir)
    report = json.loads((final / 'revision.json').read_text(encoding='utf-8'))
    return {'id': report['id'], 'parts': report['parts']}


def render(spec, data_dir):
    s = clean(spec)
    src = source(s)
    parts = ['combined'] if s['joint'] == 'single' else ['tray', 'faceplate'] + (['rear_bracket'] if s['rear_support'] else [])
    identity = hashlib.sha256(src.encode('utf-8')).hexdigest()
    final = Path(data_dir) / 'equipment-revisions' / identity
    with LOCK:
        if not final.exists():
            final.parent.mkdir(parents=True, exist_ok=True)
            exe = mesh_revision.compiler()
            with tempfile.TemporaryDirectory(dir=final.parent, prefix='render-') as temp:
                folder = Path(temp)
                logs, nudges = {}, {}
                for name in parts:
                    # OpenSCAD 2021 sometimes emits a zero-area sliver; retry with the faceplate's
                    # pocket/corner sizes nudged by a few hundredths of a mm (recorded in the report).
                    for nudge in (0, 0.011, 0.023, 0.037, 0.051):
                        text = src + (f'nudge={nudge};\n' if nudge else '')
                        (folder / 'equipment.scad').write_text(text, encoding='utf-8', newline='\n')
                        try:
                            r = subprocess.run([exe, '-o', str(folder / (name + '.stl')), '-D', f'part="{name}"', str(folder / 'equipment.scad')],
                                               capture_output=True, text=True, timeout=180,
                                               creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
                        except (OSError, subprocess.TimeoutExpired) as exc:
                            raise ValueError('Mesh rendering failed or timed out: ' + str(exc)) from exc
                        logs[name] = r.stderr
                        if s['coupon'] and 'top level object is empty' in r.stderr:
                            break  # test coupon slice doesn't touch this part
                        if r.returncode or 'ERROR:' in r.stderr:
                            raise ValueError('OpenSCAD failed for ' + name + ': ' + r.stderr[-1200:])
                        try:
                            mesh_revision.normalize_collinear_faces(folder / (name + '.stl'))
                        except ValueError:
                            pass  # optional tidy-up; read_mesh below still enforces a closed, valid mesh
                        try:
                            mesh_revision.read_mesh(folder / (name + '.stl'), name)
                            break
                        except ValueError:
                            if nudge == 0.051:
                                raise
                    nudges[name] = nudge
                    if nudge:
                        (folder / (name + '.scad')).write_text(text, encoding='utf-8', newline='\n')
                (folder / 'equipment.scad').write_text(src, encoding='utf-8', newline='\n')
                parts = [n for n in parts if (folder / (n + '.stl')).exists()]
                report = {'nudge_mm': nudges, 'export_quality': export_quality(s), 'status': 'PROPOSED — UNVALIDATED', 'spec': s, 'parts': parts, 'id': identity,
                          'template': 'equipment_tray.scad', 'limitations': LIMITS,
                          'sha256': {n + '.stl': hashlib.sha256((folder / (n + '.stl')).read_bytes()).hexdigest() for n in parts},
                          'logs': logs}
                (folder / 'revision.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
                folder.rename(final)
    return final
