"""Local mechanical design beta. Python standard library only."""

import argparse
import copy
import assembly_records
from urllib.parse import urlsplit, parse_qs

import csv

import io

import json

import math

from pathlib import Path

import secrets

import sqlite3

import zipfile

import mesh_revision
import equipment
import rack_stl

import faceplate_mounting
import faceplate_color
import catalog_packs
import catalog_evidence
import rack_workspace
import rack_references

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

    add('Nominal screw-head surface screening', 'unknown', 'No geometry-specific surface screen is available for this assembly.')
    add('Physical and spatial checks', 'unknown', 'Driver/installation-tool envelopes, insertion path, containment, material, strength and printed fit remain unestablished. A nominal screw-head surface screen is reported separately.')

    return {'status': 'fail' if any(c['status'] == 'fail' for c in checks) else 'incomplete', 'checks': checks, 'access_assessment': [{'name':'Installation and service access','status':'unknown','required':'Equipment-specific tool, cable and motion envelopes.','limit':'Nominal hardware dimensions do not establish access or fit.'}]}





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





class Store:

    def __init__(self, path):

        self.path = path

        with self.connect() as db:

            db.execute('CREATE TABLE IF NOT EXISTS parts (id TEXT, revision INTEGER, body TEXT NOT NULL, PRIMARY KEY(id,revision))')

            db.execute('CREATE TABLE IF NOT EXISTS projects (id TEXT PRIMARY KEY, body TEXT NOT NULL)')

            if not db.execute('SELECT 1 FROM projects LIMIT 1').fetchone():
                project = {'id':'workshop-default','name':'Untitled assembly','units':'mm',
                           'selections':{},'inputs':positive_inputs({}),'notes':'Fit and strength UNKNOWN.'}
                db.execute('INSERT INTO projects VALUES (?,?)',(project['id'],json.dumps(project)))



    def connect(self):

        return sqlite3.connect(self.path)



    def parts(self):

        with self.connect() as db:

            return [json.loads(r[0]) for r in db.execute('SELECT body FROM parts ORDER BY id,revision DESC')]



    def project(self):

        with self.connect() as db:

            return json.loads(db.execute('SELECT body FROM projects ORDER BY rowid LIMIT 1').fetchone()[0])



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



    def draft(self, payload, project=None):

        project = copy.deepcopy(self.project() if project is None else project)

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





class WorkshopHTTPServer(ThreadingHTTPServer):
    # Browsers can open a burst of script/API/mesh connections on startup or
    # reload. The standard library's five-connection backlog drops some of
    # those connections on Windows before a handler ever sees the request.
    request_queue_size = 64


def make_handler(store, token):

    class Handler(BaseHTTPRequestHandler):

        def send(self, value, status=200, mime='application/json'):

            data = value if isinstance(value, bytes) else json.dumps(value).encode() if mime == 'application/json' else value.encode()

            self.send_response(status)

            self.send_header('Content-Type', mime + '; charset=utf-8')

            self.send_header('Content-Length', str(len(data)))

            self.send_header('X-Content-Type-Options', 'nosniff')

            self.send_header('Cache-Control', 'no-store')

            try:
                self.end_headers()
                self.wfile.write(data)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                # Navigation/reload cancelled this response. Do not try to send
                # a second error response or misreport an asset-integrity error.
                return



        def valid_host(self):

            return self.headers.get('Host') in [f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}']



        def selected_store(self):
            query = parse_qs(urlsplit(getattr(self, 'raw_request_path', self.path)).query)
            if self.headers.get('X-Assembly-Id') and query.get('assembly') and self.headers['X-Assembly-Id'] != query['assembly'][0]:
                raise ValueError('Conflicting assembly context.')
            identity = self.headers.get('X-Assembly-Id') or (query.get('assembly') or [None])[0]
            if not identity and self.command == 'POST' and self.path in ('/api/save','/api/build','/api/design'):
                document = rack_workspace.read(Path(store.path).parent, seed_project=store.project())
                if any(r['placements'] for r in document['racks']):
                    raise ValueError('Open this slot in the updated studio before editing or exporting its independent assembly. The legacy hardware project is preserved.')
            return assembly_records.InstanceStore(store, identity, self.headers.get('X-Workspace-Generation')) if identity else store

        def do_GET(self):
            self.raw_request_path = self.path
            self.path = urlsplit(self.path).path
            try:
                return self.get_request()
            except (ValueError, OSError, KeyError, TypeError, AttributeError) as exc:
                return self.send({'error': str(exc)}, 400)

        def get_request(self):

            if not self.valid_host():

                return self.send({'error': 'Invalid host'}, 403)

            if self.path == '/':

                # Keep studio styling in the document so a failed secondary CSS load
                # cannot strand the hybrid GUI. workspace.css remains canonical.
                html = (ROOT / 'index.html').read_text(encoding='utf-8').replace('__TOKEN__', token)
                css = (ROOT / 'workspace.css').read_text(encoding='utf-8')
                html = html.replace('<link rel="stylesheet" href="/workspace.css?v=render-hybrid-1">',
                                    '<style id="studio-workspace-css">' + css + '</style>')
                return self.send(html, mime='text/html')

            if self.path == '/api/state':

                return self.send(self.selected_store().state())

            if self.path == '/api/workspace-capabilities':
                return self.send({'version': 2, 'independent_assemblies': True, 'studio_save_version': 1, 'appearance': True, 'artwork': 'preview-only', 'faceplate_colors': 1, 'save_history': 1})

            if self.path.startswith('/api/artwork/') and self.path.endswith('.png'):
                return self.send(assembly_records.artwork(Path(store.path).parent, self.path[len('/api/artwork/'):-4]), mime='image/png')

            if self.path == '/api/rack-workspace':
                try:
                    return self.send(rack_workspace.read(Path(store.path).parent, seed_project=store.project()))
                except (OSError, ValueError, TypeError, AttributeError) as exc:
                    return self.send({'error': 'Rack document could not be read: ' + str(exc)}, 400)

            # Read-only save history: list earlier saved layouts / build an unsaved restore draft.
            if self.path == '/api/rack-history':
                return self.send(rack_workspace.list_history(Path(store.path).parent, seed_project=store.project()))

            if self.path == '/api/rack-history/restore':
                query = parse_qs(urlsplit(self.raw_request_path).query)
                return self.send(rack_workspace.restore_rack(Path(store.path).parent, (query.get('generation') or [''])[0],
                                                             (query.get('rack') or [''])[0], seed_project=store.project()))

            if self.path.startswith('/rack-references/'):
                try:
                    reference = rack_references.asset(self.path)
                    if reference is None:
                        return self.send({'error': 'Reference not found.'}, 404)
                    return self.send(reference[0], mime=reference[1])
                except (OSError, ValueError, KeyError) as exc:
                    return self.send({'error': 'Local reference unavailable: ' + str(exc)}, 409)

            if self.path == '/api/equipment-library':
                return self.send(equipment.library(Path(store.path).parent))

            if self.path == '/api/equipment-template-status':
                data_dir = Path(store.path).parent
                return self.send({item['id']: equipment.template_status(data_dir, item)
                                  for item in equipment.library(data_dir)})

            if self.path.startswith('/api/equipment-mesh/') and self.path.endswith('.stl'):
                identity, _, part = self.path[len('/api/equipment-mesh/'):-4].partition('/')
                return self.send(equipment.mesh_file(Path(store.path).parent, identity, part), mime='model/stl')

            if self.path in ('/rack-studio.js', '/assembly-studio.js', '/workspace.js', '/workspace.css', '/rack-reference.js', '/equipment-wizard.js', '/tray-placement.js', '/render-quality.js'):
                name = self.path[1:]
                return self.send((ROOT / name).read_text(encoding='utf-8'),
                                 mime='text/javascript' if name.endswith('.js') else 'text/css')

            if self.path == '/api/catalog-packs':
                return self.send(catalog_packs.inventory())

            if self.path in ('/catalog.js', '/clearance.js', '/port-openings.js', '/cable-ports.js', '/cable-routes.js', '/cable-view.js', '/cable-suggest.js', '/cable-sheet.js', '/cable-sheet-view.js', '/cable-inventory.js'):
                return self.send((ROOT / self.path[1:]).read_text(encoding='utf-8'), mime='text/javascript')

            if self.path == '/api/project':

                return self.send(self.selected_store().project())

            if self.path == '/api/geometry':

                return self.send(joint_geometry(self.selected_store().project()))

            if self.path == '/api/assembly':
                return self.send({'units':'mm','revision':'No assembly selected','parts':[]})

            if self.path == '/viewer.js':

                return self.send((ROOT / 'viewer.js').read_text(encoding='utf-8'), mime='text/javascript')

            if self.path == '/api/bom':

                stream = io.StringIO(newline='')

                writer = csv.writer(stream)

                writer.writerow(['project', 'category', 'id', 'revision', 'part_number', 'name', 'quantity', 'verification', 'source'])

                project = self.selected_store().project()
                for kind, p in project['selections'].items():

                    row = [project['id'], kind, p['id'], p['revision'], p.get('part_number', ''), p['name'], 2, p['verification'], p['source']]

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

                if self.path == '/api/studio-save':
                    return self.send(assembly_records.save_workspace(store,payload))

                if self.path == '/api/rack-workspace':
                    try:
                        return self.send(rack_workspace.save(Path(store.path).parent, payload, seed_project=store.project(), canonical_project=lambda value: store.draft(value, project=value)))
                    except OSError:
                        return self.send({'error': 'Rack layout could not be saved. Keep this page open; your draft is still available.'}, 400)

                if self.path == '/api/artwork':
                    return self.send(assembly_records.save_artwork(Path(store.path).parent, payload))

                if self.path == '/api/faceplate-colors/preview':
                    # Draft settings are fine here: nothing is written.
                    return self.send(faceplate_color.preview(payload.get('artwork'), Path(store.path).parent,
                                                             payload.get('faceplate') or '#4e75a3'))

                if self.path == '/api/faceplate-colors/export':
                    # Exports use the SAVED slot assembly only (drafts never leak into files).
                    selected = self.selected_store()
                    if not isinstance(selected, assembly_records.InstanceStore):
                        raise ValueError('Open the slot assembly before exporting its color faceplate.')
                    if payload.get('assembly') != selected.identity:
                        raise ValueError('The open assembly is not the slot you are exporting. Select that slot and try again.')
                    _, placement = assembly_records.find(selected.document(), selected.identity)
                    raise ValueError('Print in color is not available for this faceplate yet. Saved artwork remains a preview.')

                if self.path == '/api/import':

                    store.import_parts(payload)

                    return self.send(store.state())

                if self.path == '/api/save':

                    return self.send(self.selected_store().save(payload))

                if self.path == '/api/preview':

                    return self.send(joint_geometry(self.selected_store().draft(payload)))

                if self.path in ('/api/design', '/api/build'):
                    raise ValueError('Use Place on tray for this assembly’s proposed geometry.')

                if self.path == '/api/equipment-library':
                    return self.send(equipment.save_item(payload, Path(store.path).parent))

                if self.path == '/api/equipment-rebuild-copy':
                    if not isinstance(payload, dict):
                        raise ValueError('Rebuild request must be an object.')
                    return self.send(equipment.rebuild_copy(Path(store.path).parent, payload.get('id'), payload.get('expected_build')))

                if self.path == '/api/equipment-library-delete':
                    data_dir = Path(store.path).parent
                    document = rack_workspace.read(data_dir, seed_project=store.project())
                    in_use = {p['equipment'] for r in document['racks'] for p in r['placements']}
                    return self.send(equipment.delete_item(payload.get('id'), data_dir, in_use))

                if self.path == '/api/equipment-preview':
                    data_dir = Path(store.path).parent
                    # A slot's Place on tray window sends {item, tray}; the wizard sends a whole spec.
                    spec = equipment.allocation_request(data_dir, payload) if isinstance(payload, dict) and 'item' in payload else payload
                    return self.send(equipment.preview(spec, data_dir))

                if self.path == '/api/equipment-placement-mesh':
                    # Rack view: reuse an existing exact render of a slot's tray settings; never renders.
                    return self.send(equipment.cached_allocation_render(Path(store.path).parent, payload))

                if self.path == '/api/equipment-placement-check':
                    return self.send(equipment.check_allocation(Path(store.path).parent, payload))

                if self.path == '/api/rack-stl':
                    return self.send(rack_stl.export(payload), mime='application/zip')

                if self.path == '/api/step-to-stl':
                    return self.send(equipment.step_to_stl(payload), mime='model/stl')

                if self.path == '/api/scad-to-stl':
                    return self.send(equipment.scad_to_stl(payload), mime='model/stl')

                if self.path == '/api/equipment-build':
                    data_dir = Path(store.path).parent
                    spec = equipment.allocation_request(data_dir, payload) if isinstance(payload, dict) and 'item' in payload else payload
                    return self.send(equipment.build(spec, data_dir), mime='application/zip')

                if self.path == '/api/build-bundle':

                    bundle = mesh_revision.bundle(payload.get('id'), Path(store.path).parent)
                    project = self.selected_store().project()
                    if project.get('instance_id'):
                        with zipfile.ZipFile(io.BytesIO(bundle)) as archive:
                            binding = json.loads(archive.read('revision.json')).get('assembly_instance')
                        expected = {'id': project['instance_id'], 'revision': project['instance_revision'], 'project_sha256': assembly_records.fingerprint(project)}
                        if binding != expected:
                            raise ValueError('This mesh revision belongs to another assembly or older hardware snapshot. Generate the selected assembly revision explicitly.')
                    return self.send(bundle, mime='application/zip')

                if self.path == '/api/check':

                    project = self.selected_store().project()

                    return self.send(evaluate(project['selections'].get('screw'), project['selections'].get('heatset'), project['inputs']))

                return self.send({'error': 'Not found'}, 404)

            except (ValueError, KeyError, TypeError, AttributeError, OSError) as e:

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

    server = WorkshopHTTPServer(('127.0.0.1', args.port), make_handler(store, secrets.token_hex(24)))

    print(f'Open http://127.0.0.1:{server.server_port} in your browser. Ctrl+C stops the app.', flush=True)

    try:

        server.serve_forever()

    except KeyboardInterrupt:

        pass

    finally:

        server.server_close()

