"""Local mechanical design beta. Python standard library only."""

import argparse

import csv

import io

import json

import math

from pathlib import Path

import secrets

import sqlite3

import zipfile

import mesh_revision

import pi_validation
import faceplate_mounting
import catalog_packs
import catalog_evidence
import rack_workspace

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer



ROOT = Path(__file__).resolve().parent

SIZES = [1, 1.2, 1.4, 1.6, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8]

NUMERIC = {'diameter', 'pitch', 'length', 'head_diameter', 'head_height',

           'outside_diameter', 'hole_diameter', 'usable_depth', 'min_wall',

           'threaded_length', 'hole_max_diameter'}





def straight_hole_bounds(part):
    """Return explicit supplier bounds; absent tolerance preserves legacy exact checks."""
    tolerance = part.get('hole_diameter_tolerance_mm')
    if tolerance is None:
        return None
    if (not isinstance(tolerance, dict) or set(tolerance) != {'plus', 'minus'}
            or part.get('hole_profile') != 'straight'):
        raise ValueError('hole_diameter_tolerance_mm needs plus/minus values and a straight hole.')
    nominal = part.get('hole_diameter')
    values = [nominal, tolerance['plus'], tolerance['minus']]
    if any(type(v) not in [int, float] or not math.isfinite(v) for v in values):
        raise ValueError('Hole recommendation and tolerances must be finite numbers in millimeters.')
    if nominal <= 0 or tolerance['plus'] < 0 or tolerance['minus'] < 0:
        raise ValueError('Hole recommendation must be positive; tolerances must be nonnegative.')
    lower, upper = nominal - tolerance['minus'], nominal + tolerance['plus']
    if lower <= 0 or not math.isfinite(upper):
        raise ValueError('Hole recommendation bounds must be finite and positive.')
    return lower, upper


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

    straight_hole_bounds(part)
    catalog_evidence.validate_profile(part)
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

            gap = v['pocket'] - reach

            add('Open insert bore envelope', 'pass' if gap >= v['bottom_allowance'] else 'fail',

                f'{gap:.3f} mm from screw tip to the modeled bore end. Assumes the entered pocket is continuous screw-clear space; verify actual geometry.')

            add('Bottom clearance', 'unknown', 'The modeled bore check does not establish the actual insert exit, installation residue or printed clearance.')

        else:

            add('Bottom clearance', 'unknown', 'End type and available screw-tip space are not established.')

    for field, name in [('length', 'Insert pocket depth'), ('hole_diameter', 'Installation hole')]:

        value = insert.get(field)

        if field == 'hole_diameter' and insert.get('hole_max_diameter') is not None:

            maximum = insert['hole_max_diameter']

            add('Maximum installation hole', 'fail' if v['pilot'] > maximum else 'pass',

                f"Pilot {v['pilot']:g} mm; supplier maximum {maximum:g} mm. Being below the maximum alone does not establish printed fit.")

        if value is None:

            add(name, 'unknown', f'Missing insert {field}.')

        elif field == 'length':

            add(name, 'pass' if v['pocket'] >= value else 'fail', f"Pocket {v['pocket']:g} mm; insert {value:g} mm. Melt allowance is still material dependent.")

        elif insert.get('hole_profile') != 'straight':

            add(name, 'unknown', 'Only straight installation holes are supported in this first version.')

        else:

            bounds = straight_hole_bounds(insert)
            if bounds is None:
                add(name, 'pass' if abs(v['pilot'] - value) < .0001 else 'fail',
                    f"Pilot {v['pilot']:g} mm; recorded recommendation {value:g} mm. Verify with a printed coupon.")
            else:
                lower, upper = bounds
                within = lower - 1e-9 <= v['pilot'] <= upper + 1e-9
                add(name, 'pass' if within else 'fail',
                    f"Pilot {v['pilot']:g} mm; sourced hole range {lower:g}–{upper:g} mm. "
                    "Dimensional comparison only; material/process and printed fit require validation.")

    if insert.get('outside_diameter') and insert.get('min_wall'):

        wall = (v['boss_diameter'] - insert['outside_diameter']) / 2

        add('Boss wall', 'pass' if wall >= insert['min_wall'] else 'fail', f"Radial wall {wall:.3f} mm; recorded minimum {insert['min_wall']:g} mm.")

    else:

        add('Boss wall', 'unknown', 'Insert outside diameter and sourced minimum wall are required.')

    if any(p['verification'] != 'documented' for p in [screw, insert]):

        add('Source completeness', 'unknown', 'A selected part is custom or partially documented.')

    head = pi_validation.head_screen(screw)
    add('Nominal screw-head surface screening', head['status'], json.dumps(head))
    add('Physical and spatial checks', 'unknown', 'Driver/installation-tool envelopes, insertion path, containment, material, strength and printed fit remain unestablished. A nominal screw-head surface screen is reported separately.')

    return {'status': 'fail' if any(c['status'] == 'fail' for c in checks) else 'incomplete', 'checks': checks, 'access_assessment': pi_validation.access_assessment(screw, insert)}





def joint_geometry(project):

    """One-dimensional axial model. Never infer missing insert OD or usable thread."""

    v = positive_inputs(project['inputs'])

    s = project['selections'].get('screw', {})

    i = project['selections'].get('heatset', {})

    length = s.get('length') if s.get('length_convention') == 'under_head' else None

    reach = None if length is None else length - v['stack']

    envelopes, guides = [], []

    for x in [-40, 40]:

        bearing_y = 11.3  # rear bearing face of each tray ear, clearance-v2 source

        entrance_y = bearing_y - v['stack']

        if length is not None:

            envelopes.append({'kind': 'screw', 'x': x, 'z': 21, 'y0': bearing_y-length,

                              'y1': bearing_y, 'diameter': s['diameter']})

            if s.get('head_diameter') and s.get('head_height'):

                envelopes.append({'kind': 'screw_head', 'x': x, 'z': 21, 'y0': bearing_y,

                                  'y1': bearing_y+s['head_height'], 'diameter': s['head_diameter']})

        if i.get('length'):

            end_y = entrance_y-i['length']

            if i.get('outside_diameter'):

                envelopes.append({'kind': 'insert', 'x': x, 'z': 21, 'y0': end_y,

                                  'y1': entrance_y, 'diameter': i['outside_diameter']})

            else:

                guides.append({'x': x, 'z': 21, 'y0': end_y, 'y1': entrance_y,

                               'label': 'Insert axis only — outside diameter unknown'})

    return {'units': 'mm', 'axis': 'Depth from screw bearing surface toward faceplate',

            'bearing': 0, 'insert_entrance': v['stack'],

            'insert_end': None if i.get('length') is None else v['stack'] + i['length'],

            'bore_end': v['stack'] + v['pocket'], 'screw_tip': length,

            'reach': reach, 'tip_beyond_insert': None if reach is None or i.get('length') is None else max(0, reach-i['length']),

            'tip_to_bore_end': None if length is None else v['stack']+v['pocket']-length,

            'pilot': v['pilot'], 'supplier_max_pilot': i.get('hole_max_diameter'),

            'insert_outside_diameter': i.get('outside_diameter'), 'usable_thread_depth': i.get('usable_depth'),

            'hardware_envelopes': envelopes, 'hardware_guides': guides,

            'assumptions': ['Continuous bore depth equals the entered available pocket depth.',

                            'Insert entrance equals the entered stack; washers and gaps must be included.',

                            '3D screw bearing faces fixed at X=+/-40, Y=11.3, Z=21; axes point toward -Y.',

                            'Hardware envelopes are nominal reference geometry; no 3D collision or installation access verification.']}





def design_revision(project):

    """Narrow adapter for the known Pi4 source; export a proposal, never alter baseline."""

    v = positive_inputs(project['inputs'])

    screw = project['selections'].get('screw')

    insert = project['selections'].get('heatset')

    if not screw or not insert:

        raise ValueError('Select a screw and insert before exporting a design revision.')

    if screw['diameter'] != 3 or insert['diameter'] != 3 or screw['pitch'] != .5 or insert['pitch'] != .5:

        raise ValueError('The current Pi4 design adapter supports M3 × 0.5 joint hardware only.')

    if any(abs(v[k]-expected) > .0001 for k, expected in [('stack', 3.3), ('pocket', 8), ('boss_diameter', 9)]):

        raise ValueError('This adapter changes only the pilot and fixed four-corner mount layout. Restore stack 3.3, pocket 8 and boss diameter 9 mm; other geometry changes are not implemented.')

    if not 3 <= v['pilot'] <= 4.2:

        raise ValueError('Supported pilot range for this Pi4 adapter is 3–4.2 mm; printed fit still requires testing.')

    result = evaluate(screw, insert, v)

    if result['status'] == 'fail':

        failed = ', '.join(c['name'] for c in result['checks'] if c['status'] == 'fail')

        raise ValueError('Resolve these failed checks before exporting: ' + failed)

    baseline = (ROOT / 'pi4_baseline.scad').read_text(encoding='utf-8')

    marker = 'insert_pilot=4.2;'

    if baseline.count(marker) != 1:

        raise ValueError('Baseline source does not match the supported design adapter.')

    assembly_validation = pi_validation.validate()
    if assembly_validation['status'] == 'fail':
        raise ValueError('Resolve failed assembly checks before exporting a proposal.')
    metadata = {'status': 'PROPOSED — UNVALIDATED', 'baseline': 'Pi4 clearance v2',

                'changed_parameter': {'insert_pilot': v['pilot']},

                'hardware': project['selections'], 'checks': result,

                'assembly_validation': assembly_validation,
                'mounting_layout': faceplate_mounting.profile(),
                'assembly_validation_scope': 'Baseline evidence retained. Four-corner mounting is a new revision; physical rack engagement, wall/strength and installation remain unvalidated.',

                'limitations': ['Insert outside diameter and usable thread depth may remain unknown.',

                                'Supplier maximum hole diameter is not an exact installation target.',

                                'Pi reference is a separate inspection asset, excluded from manufacturing meshes.',

                                'Re-render, check component clearances and print a fit coupon before use.']}

    # Metadata lives beside the source rather than interpolating user text into SCAD.

    source = '// PROPOSED revision. See revision.json for hardware, assumptions and unresolved checks.\n' + faceplate_mounting.apply_default(baseline).replace(marker, f"insert_pilot={v['pilot']:.6g};")

    return source, metadata





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



    def draft(self, payload):

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

        if 'reference' not in project:

            project['reference'] = pi_validation.reference()[1]

        return project



    def save(self, payload):

        project = self.draft(payload)

        with self.connect() as db:

            db.execute('UPDATE projects SET body=? WHERE id=?', (json.dumps(project), project['id']))

        return project



    def state(self):

        parts = self.parts()

        return {'parts': parts, 'project': self.project(), 'coverage': [

            {'size': size, 'screws': sum(p['kind'] == 'screw' and p['diameter'] == size for p in parts),

             'heatsets': sum(p['kind'] == 'heatset' and p['diameter'] == size for p in parts)} for size in SIZES]}



    def load_starter(self, path=ROOT / 'starter-hardware.json'):

        records = json.loads(path.read_text(encoding='utf-8'))

        existing = {(p['id'], p['revision']): p for p in self.parts()}

        missing = [p for p in records if (p['id'], p['revision']) not in existing]

        if missing:

            self.import_parts(missing)

        return len(missing)





def make_handler(store, token):

    class Handler(BaseHTTPRequestHandler):

        def send(self, value, status=200, mime='application/json'):

            data = value if isinstance(value, bytes) else json.dumps(value).encode() if mime == 'application/json' else value.encode()

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

            if self.path == '/api/rack-workspace':
                try:
                    return self.send(rack_workspace.read(Path(store.path).parent))
                except (OSError, ValueError, TypeError, AttributeError) as exc:
                    return self.send({'error': 'Rack document could not be read: ' + str(exc)}, 400)

            if self.path in ('/workspace.js', '/workspace.css'):
                name = self.path[1:]
                return self.send((ROOT / name).read_text(encoding='utf-8'),
                                 mime='text/javascript' if name.endswith('.js') else 'text/css')

            if self.path == '/api/catalog-packs':
                return self.send(catalog_packs.inventory())

            if self.path == '/catalog.js':
                return self.send((ROOT / 'catalog.js').read_text(encoding='utf-8'), mime='text/javascript')

            if self.path == '/api/project':

                return self.send(store.project())

            if self.path == '/api/geometry':

                return self.send(joint_geometry(store.project()))

            if self.path == '/api/pi-reference':

                try:

                    part, manifest = pi_validation.reference()

                    return self.send(dict(part, reference=manifest))

                except (OSError, ValueError) as exc:

                    return self.send({'error': str(exc)}, 400)

            if self.path == '/api/assembly-checks':

                return self.send(pi_validation.validate())

            if self.path == '/api/assembly':

                return self.send(json.loads((ROOT / 'assembly.json').read_text(encoding='utf-8')))

            if self.path == '/viewer.js':

                return self.send((ROOT / 'viewer.js').read_text(encoding='utf-8'), mime='text/javascript')

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

                if self.path == '/api/rack-workspace':
                    try:
                        return self.send(rack_workspace.save(Path(store.path).parent, payload))
                    except OSError:
                        return self.send({'error': 'Rack layout could not be saved. Keep this page open; your draft is still available.'}, 400)

                if self.path == '/api/import':

                    store.import_parts(payload)

                    return self.send(store.state())

                if self.path == '/api/save':

                    return self.send(store.save(payload))

                if self.path == '/api/preview':

                    return self.send(joint_geometry(store.draft(payload)))

                if self.path == '/api/design':

                    source, metadata = design_revision(store.draft(payload))

                    stream = io.BytesIO()

                    with zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED) as archive:

                        archive.writestr('pi4_proposed.scad', source)

                        archive.writestr('revision.json', json.dumps(metadata, indent=2))

                    return self.send(stream.getvalue(), mime='application/zip')

                if self.path == '/api/build':

                    source, metadata = design_revision(store.draft(payload))

                    return self.send(mesh_revision.build(source, metadata, Path(store.path).parent))

                if self.path == '/api/build-bundle':

                    return self.send(mesh_revision.bundle(payload.get('id'), Path(store.path).parent), mime='application/zip')

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

    parser.add_argument('--existing-library', action='store_true',
                        help='Require an existing library and skip automatic starter imports.')

    args = parser.parse_args()

    if args.existing_library and not (args.data / 'library.sqlite3').is_file():
        parser.error('--existing-library requires an existing data/library.sqlite3; no data was created.')

    args.data.mkdir(parents=True, exist_ok=True)

    store = Store(args.data / 'library.sqlite3')

    added = 0 if args.existing_library else store.load_starter()

    print(f'Hardware library: {len(store.parts())} revisions ({added} starter records added).', flush=True)

    server = ThreadingHTTPServer(('127.0.0.1', args.port), make_handler(store, secrets.token_hex(24)))

    print(f'Open http://127.0.0.1:{server.server_port} in your browser. Ctrl+C stops the app.', flush=True)

    try:

        server.serve_forever()

    except KeyboardInterrupt:

        pass

    finally:

        server.server_close()

