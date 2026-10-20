"""Local mechanical design beta. Python standard library only."""
import argparse
import csv
import io
import json
import math
from pathlib import Path
import secrets
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parent
SIZES = [1, 1.2, 1.4, 1.6, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8]
NUMERIC = {'diameter', 'pitch', 'length', 'head_diameter', 'head_height',
           'outside_diameter', 'hole_diameter', 'usable_depth', 'min_wall',
           'threaded_length'}


def validate_part(part):
    if not isinstance(part, dict):
        raise ValueError('Each part must be a JSON object.')
    required = ['id', 'name', 'kind', 'revision', 'diameter', 'pitch', 'source', 'verification']
    if any(k not in part for k in required):
        raise ValueError('Required fields: ' + ', '.join(required))
    for key in ['id', 'name', 'source']:
        if not isinstance(part[key], str) or not part[key].strip():
            raise ValueError(key + ' must contain text.')
    if part['kind'] not in ['screw', 'heatset']:
        raise ValueError('kind must be screw or heatset.')
    if part['verification'] not in ['custom', 'partial', 'documented']:
        raise ValueError('verification must be custom, partial, or documented.')
    if type(part['revision']) is not int or part['revision'] < 1:
        raise ValueError('revision must be a positive integer.')
    for key in NUMERIC:
        value = part.get(key)
        if value is not None and (type(value) not in [int, float] or not math.isfinite(value) or value <= 0):
            raise ValueError(key + ' must be a finite positive number in millimeters.')
    if part.get('diameter') is None or part.get('pitch') is None:
        raise ValueError('diameter and pitch are required positive numbers.')
    if not 1 <= part['diameter'] <= 8:
        raise ValueError('This catalog supports nominal diameters M1 through M8.')
    if part['verification'] == 'documented' and not part.get('part_number'):
        raise ValueError('Documented parts need an exact part_number.')
    return part


def positive_inputs(inputs):
    defaults = {'stack': 3.3, 'pocket': 8, 'boss_diameter': 9,
                'pilot': 4.2, 'minimum_engagement': 3, 'bottom_allowance': .5}
    result = {}
    for key, default in defaults.items():
        v = inputs.get(key, default)
        if type(v) not in [float, int] or not math.isfinite(v) or v < 0:
            raise ValueError(key + ' must be a finite nonnegative number.')
        result[key] = v
    return result


def evaluate(screw, insert, inputs):
    v = positive_inputs(inputs)
    checks = []
    def add(name, status, detail):
        checks.append({'name': name, 'status': status, 'detail': detail})
    if not screw or not insert:
        add('Hardware selection', 'unknown', 'Choose both a screw and a heat-set insert.')
        return {'status': 'incomplete', 'checks': checks}
    matched = screw['diameter'] == insert['diameter'] and screw['pitch'] == insert['pitch']
    add('Thread compatibility', 'pass' if matched else 'fail',
        f"Screw M{screw['diameter']:g} × {screw['pitch']:g}; insert M{insert['diameter']:g} × {insert['pitch']:g}.")
    length = screw.get('length')
    depth = insert.get('usable_depth')
    if screw.get('length_convention') != 'under_head' or length is None:
        add('Screw reach', 'unknown', 'An under-head length is required; countersunk lengths need a separate adapter.')
    else:
        reach = length - v['stack']
        add('Screw reach', 'pass' if reach >= v['minimum_engagement'] else 'fail',
            f"Reach {reach:.3f} mm; project minimum {v['minimum_engagement']:.3f} mm (user target, not a strength rating).")
        if depth is None:
            add('Usable thread engagement', 'unknown', 'Insert usable thread depth has not been documented.')
        else:
            engagement = max(0, min(depth, reach))
            add('Usable thread engagement', 'pass' if engagement >= v['minimum_engagement'] else 'fail',
                f'Usable engagement {engagement:.3f} mm.')
        if screw.get('threaded_length') is None:
            add('Threaded shank', 'unknown', 'Threaded length is required to exclude unthreaded-shank interference.')
        else:
            add('Threaded shank', 'pass' if screw['threaded_length'] >= reach else 'fail',
                'Conservative check: the entire protruding section must be threaded.')
        if insert.get('end_type') == 'closed' and depth is not None:
            gap = depth - reach
            add('Bottom clearance', 'pass' if gap >= v['bottom_allowance'] else 'fail', f'{gap:.3f} mm to the documented closed end.')
        elif insert.get('end_type') == 'open':
            add('Bottom clearance', 'unknown', 'Open insert: geometry behind it must be checked for screw-tip clearance.')
        else:
            add('Bottom clearance', 'unknown', 'End type and available screw-tip space are not established.')
    for field, name in [('length', 'Insert pocket depth'), ('hole_diameter', 'Installation hole')]:
        value = insert.get(field)
        if value is None:
            add(name, 'unknown', f'Missing insert {field}.')
        elif field == 'length':
            add(name, 'pass' if v['pocket'] >= value else 'fail', f"Pocket {v['pocket']:g} mm; insert {value:g} mm. Melt allowance is still material dependent.")
        elif insert.get('hole_profile') != 'straight':
            add(name, 'unknown', 'Only straight installation holes are supported in this first version.')
        else:
            add(name, 'pass' if abs(v['pilot'] - value) < .0001 else 'fail',
                f"Pilot {v['pilot']:g} mm; recorded recommendation {value:g} mm. Verify with a printed coupon.")
    if insert.get('outside_diameter') and insert.get('min_wall'):
        wall = (v['boss_diameter'] - insert['outside_diameter']) / 2
        add('Boss wall', 'pass' if wall >= insert['min_wall'] else 'fail', f"Radial wall {wall:.3f} mm; recorded minimum {insert['min_wall']:g} mm.")
    else:
        add('Boss wall', 'unknown', 'Insert outside diameter and sourced minimum wall are required.')
    if any(p['verification'] != 'documented' for p in [screw, insert]):
        add('Source completeness', 'unknown', 'A selected part is custom or partially documented.')
    add('Physical and spatial checks', 'unknown', 'Head/driver access, component clearance, material, strength and printed fit require geometry or physical checks.')
    return {'status': 'fail' if any(c['status'] == 'fail' for c in checks) else 'incomplete', 'checks': checks}


class Store:
    def __init__(self, path):
        self.path = path
        with self.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS parts (id TEXT, revision INTEGER, body TEXT NOT NULL, PRIMARY KEY(id,revision))')
            db.execute('CREATE TABLE IF NOT EXISTS projects (id TEXT PRIMARY KEY, body TEXT NOT NULL)')
            project = {'id': 'pi4-beta', 'name': 'Lab Rax · Pi4 beta', 'units': 'mm', 'selections': {},
                       'inputs': positive_inputs({}), 'notes': 'Clearance v2 baseline. Insert pilot is provisional. Physical testing pending.'}
            db.execute('INSERT OR IGNORE INTO projects VALUES (?,?)', ('pi4-beta', json.dumps(project)))

    def connect(self):
        return sqlite3.connect(self.path)

    def parts(self):
        with self.connect() as db:
            return [json.loads(r[0]) for r in db.execute('SELECT body FROM parts ORDER BY id,revision DESC')]

    def project(self):
        with self.connect() as db:
            return json.loads(db.execute('SELECT body FROM projects WHERE id=?', ('pi4-beta',)).fetchone()[0])

    def import_parts(self, items):
        if not isinstance(items, list) or not items or len(items) > 1000:
            raise ValueError('Import an array containing 1–1000 part records.')
        for p in items:
            validate_part(p)
        with self.connect() as db:
            for p in items:
                old = db.execute('SELECT body FROM parts WHERE id=? AND revision=?', (p['id'], p['revision'])).fetchone()
                if old and json.loads(old[0]) != p:
                    raise ValueError('Existing revisions are immutable. Increase the revision number for ' + p['id'])
                db.execute('INSERT OR IGNORE INTO parts VALUES (?,?,?)', (p['id'], p['revision'], json.dumps(p)))

    def save(self, payload):
        project = self.project()
        selections = payload.get('selections', {})
        if not isinstance(selections, dict):
            raise ValueError('Selections must be an object.')
        parts = {(p['id'], p['revision']): p for p in self.parts()}
        pinned = {}
        for kind in ['screw', 'heatset']:
            choice = selections.get(kind)
            if choice:
                p = parts.get((choice.get('id'), choice.get('revision')))
                if not p or p['kind'] != kind:
                    raise ValueError('Invalid ' + kind + ' selection.')
                pinned[kind] = p  # Store the complete immutable snapshot.
        project['selections'] = pinned
        project['inputs'] = positive_inputs(payload.get('inputs', {}))
        with self.connect() as db:
            db.execute('UPDATE projects SET body=? WHERE id=?', (json.dumps(project), project['id']))
        return project

    def state(self):
        parts = self.parts()
        return {'parts': parts, 'project': self.project(), 'coverage': [
            {'size': size, 'screws': sum(p['kind'] == 'screw' and p['diameter'] == size for p in parts),
             'heatsets': sum(p['kind'] == 'heatset' and p['diameter'] == size for p in parts)} for size in SIZES]}


def make_handler(store, token):
    class Handler(BaseHTTPRequestHandler):
        def send(self, value, status=200, mime='application/json'):
            data = json.dumps(value).encode() if mime == 'application/json' else value.encode()
            self.send_response(status)
            self.send_header('Content-Type', mime + '; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(data)

        def valid_host(self):
            return self.headers.get('Host') in [f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}']

        def do_GET(self):
            if not self.valid_host():
                return self.send({'error': 'Invalid host'}, 403)
            if self.path == '/':
                return self.send((ROOT / 'index.html').read_text(encoding='utf-8').replace('__TOKEN__', token), mime='text/html')
            if self.path == '/api/state':
                return self.send(store.state())
            if self.path == '/api/project':
                return self.send(store.project())
            if self.path == '/api/bom':
                stream = io.StringIO(newline='')
                writer = csv.writer(stream)
                writer.writerow(['project', 'category', 'id', 'revision', 'part_number', 'name', 'quantity', 'verification', 'source'])
                for kind, p in store.project()['selections'].items():
                    row = ['pi4-beta', kind, p['id'], p['revision'], p.get('part_number', ''), p['name'], 2, p['verification'], p['source']]
                    writer.writerow(["'" + v if isinstance(v, str) and v.startswith(('=', '+', '-', '@')) else v for v in row])
                return self.send(stream.getvalue(), mime='text/csv')
            return self.send({'error': 'Not found'}, 404)

        def do_POST(self):
            if not self.valid_host() or self.headers.get('X-App-Token') != token:
                return self.send({'error': 'Invalid local session'}, 403)
            try:
                length = int(self.headers.get('Content-Length', '0'))
                if not 0 < length <= 2_000_000:
                    raise ValueError('Request size must be between 1 byte and 2 MB.')
                payload = json.loads(self.rfile.read(length))
                if self.path == '/api/import':
                    store.import_parts(payload)
                    return self.send(store.state())
                if self.path == '/api/save':
                    return self.send(store.save(payload))
                if self.path == '/api/check':
                    project = store.project()
                    return self.send(evaluate(project['selections'].get('screw'), project['selections'].get('heatset'), project['inputs']))
                return self.send({'error': 'Not found'}, 404)
            except (ValueError, KeyError, TypeError, AttributeError) as e:
                return self.send({'error': str(e)}, 400)
    return Handler


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--data', type=Path, default=ROOT / 'data')
    args = parser.parse_args()
    args.data.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(('127.0.0.1', args.port), make_handler(Store(args.data / 'library.sqlite3'), secrets.token_hex(24)))
    print(f'Open http://127.0.0.1:{server.server_port} in your browser. Ctrl+C stops the app.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
