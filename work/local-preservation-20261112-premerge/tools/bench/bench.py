"""Workshop Bench: local, read-mostly project notebook. Python 3.10 stdlib only."""
import argparse
import copy
import datetime as dt
import hashlib
from functools import lru_cache
import html
import json
import os
from pathlib import Path
import re
import secrets
import stat
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlsplit, parse_qs, quote

STATUSES = ('idea', 'measuring', 'draft', 'printing', 'report-due', 'done', 'parked')
PROJECTS = 'work/bench/projects.json'
FIT = 'docs/Fit_Findings.md'
WORKFLOW = 'work/workbench/Workflow_Log.md'
WRITABLE = (PROJECTS, FIT, WORKFLOW)
STATIC = Path(__file__).resolve().parent / 'static'
RESULTS = ('Fits', 'Too tight', 'Too loose', 'Failed', 'Other')


class Problem(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(root, name):
    """No aliases, alternate streams, backslashes, encoded paths or symlink hops."""
    if not isinstance(name, str) or not name or any(c in name for c in '\\:%\x00'):
        raise Problem('That path is not allowed.', 403)
    parts = name.split('/')
    if any(p in ('', '.', '..') or p.endswith((' ', '.')) for p in parts):
        raise Problem('That path is not allowed.', 403)
    root = Path(root).absolute()
    path = root
    for part in parts:
        path = path / part
        try:
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                raise Problem('Linked paths are not allowed.', 403)
        except FileNotFoundError:
            pass
    if not path.is_relative_to(root):
        raise Problem('That path is outside the repository.', 403)
    return path


@lru_cache(maxsize=256)
def revision_pattern(prefix):
    suffix = r'(?:-[A-Z0-9]+)+'
    if re.search(r'\d$', prefix):
        suffix = r'(?:[A-Z](?:[0-9]+)?(?:-[A-Z0-9]+)*|(?:-[A-Z0-9]+)+)'
    return re.compile(r'(?<![A-Za-z0-9])' + re.escape(prefix) + suffix + r'(?![A-Z0-9]|-[A-Z0-9])')


def revision_ids(text, prefixes):
    found = set()
    for prefix in sorted(prefixes, key=len, reverse=True):
        found.update(revision_pattern(prefix).findall(text))
    return sorted(found)


def has_id(text, revision):
    return bool(re.search(r'(?<![A-Za-z0-9-])' + re.escape(revision) + r'(?![A-Za-z0-9-])', text))


def guess_fit(lines):
    text = ' '.join(lines).lower()
    if re.search(r'too tight|too loose|did not fit|would not|\bfailed\b|no driver|not fit|does not fit', text):
        return 'problem'
    if re.search(r'\bfits?\b|good fit|perfect|fitment great|hold well enough|seats with ports flush', text):
        # Negative and unprinted statements must never become a positive fit.
        if not re.search(r'not printed|unprinted|fit unknown|not reported', text):
            return 'fit'
        if re.search(r'\bfits\b|good fit|perfect|fitment great', text):
            return 'fit'
    if re.search(r'\bprinting\b', text) and not re.search(r'not printing|before printing', text):
        return 'printing'
    return 'not printed'


def inline(text, link=None):
    """Render a small, escaped subset. File links need an allowlisted resolver."""
    tokens = re.split(r'(`[^`\n]+`|\[[^\]\n]+\]\([^\)\n]+\))', text)
    out = []
    for token in tokens:
        if token.startswith('`') and token.endswith('`'):
            out.append('<code>' + html.escape(token[1:-1]) + '</code>')
        else:
            m = re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)', token)
            if m:
                label, url = m.groups()
                href = url if re.match(r'https?://[^\s<>"\x00-\x20]+$', url, re.I) else (link(url) if link else None)
                if href:
                    out.append('<a rel="noopener noreferrer" target="_blank" href="' + html.escape(href, quote=True) + '">' + html.escape(label) + '</a>')
                else:
                    out.append(html.escape(label + ' (' + url + ')'))
            else:
                escaped = html.escape(token)
                out.append(re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', escaped))
    return ''.join(out)


def markdown(text, link=None):
    lines = text.splitlines()
    out, i = [], 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = lines[i].strip().strip('|').split('|')
                if not all(re.fullmatch(r'\s*:?-+:?\s*', c) for c in cells):
                    rows.append(cells)
                i += 1
            out.append('<div class="table-scroll" tabindex="0"><table>')
            for n, cells in enumerate(rows):
                tag = 'th' if n == 0 else 'td'
                out.append('<tr>' + ''.join('<' + tag + '>' + inline(c.strip(), link) + '</' + tag + '>' for c in cells) + '</tr>')
            out.append('</table></div>')
            continue
        heading = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading:
            level = min(6, len(heading[1]) + 1)
            out.append(f'<h{level}>' + inline(heading[2], link) + f'</h{level}>')
        elif re.match(r'^[-*] ', line):
            out.append('<ul>')
            while i < len(lines) and re.match(r'^[-*] ', lines[i].strip()):
                out.append('<li>' + inline(lines[i].strip()[2:], link) + '</li>')
                i += 1
            out.append('</ul>')
            continue
        elif line:
            out.append('<p>' + inline(line, link) + '</p>')
        i += 1
    return '\n'.join(out)


def workflow_section(text, title):
    if not title:
        return ''
    chunks, keep = [], False
    for line in text.splitlines():
        if line.startswith('## '):
            keep = line[3:].strip() in (title, title + ' (continued)')
        if keep:
            chunks.append(line)
    return '\n'.join(chunks)


def append_bytes(old, text):
    newline = b'\r\n' if b'\r\n' in old else b'\n'
    addition = text.replace('\r\n', '\n').replace('\r', '\n').encode('utf-8').replace(b'\n', newline)
    return old + (b'' if not old or old.endswith(b'\n') else newline) + addition.rstrip(b'\r\n') + newline


def natural(value):
    return tuple((1, int(x)) if x.isdigit() else (0, x) for x in re.split(r'(\d+)', value))


class Bench:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.lock = threading.RLock()
        self.token = secrets.token_urlsafe(32)
        self.cache = None
        self.allowed_text = set()

    def read(self, name, optional=False):
        path = safe_path(self.root, name)
        if optional and not path.exists():
            return b''
        if not path.is_file():
            raise Problem('File is missing: ' + name, 404)
        return path.read_bytes()

    def hashes(self):
        return {name: digest(self.read(name, True)) for name in WRITABLE}

    def data(self):
        try:
            data = json.loads(self.read(PROJECTS).decode('utf-8'))
            if data['version'] != 1 or not isinstance(data['projects'], list):
                raise ValueError()
            ids, prefixes = set(), set()
            for p in data['projects']:
                if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', p['id']) or p['id'] in ids:
                    raise ValueError()
                if p['status'] not in STATUSES or not isinstance(p['title'], str):
                    raise ValueError()
                dt.date.fromisoformat(p['updated'])
                ids.add(p['id'])
                for prefix in p['prefixes']:
                    if not re.fullmatch(r'[A-Z][A-Z0-9]*', prefix) or prefix in prefixes:
                        raise ValueError()
                    prefixes.add(prefix)
                for key in ('sources', 'device_cards'):
                    for name in p.get(key, []):
                        safe_path(self.root, name)
            return data
        except (ValueError, KeyError, TypeError, UnicodeError):
            raise Problem('projects.json is invalid. Restore it from a reviewed backup.', 500)

    def refresh(self):
        with self.lock:
            started = time.perf_counter()
            data = self.data()
            projects = copy.deepcopy(data['projects'])
            all_prefixes = [x for p in projects for x in p['prefixes']]
            owners = {prefix: p['id'] for p in projects for prefix in p['prefixes']}
            revisions = {p['id']: {} for p in projects}
            texts = {}
            errors = []
            self.allowed_text = {FIT, WORKFLOW, 'HANDOFF.md', 'outputs/Final_3MF/README.md'}

            def read_text(name):
                try:
                    text = self.read(name, True).decode('utf-8')
                    self.allowed_text.add(name)
                    texts[name] = text
                    return text
                except (Problem, OSError, UnicodeError) as exc:
                    errors.append(name + ': ' + str(exc))
                    return ''

            handoff = read_text('HANDOFF.md')
            fit = read_text(FIT)
            workflow = read_text(WORKFLOW)
            final = read_text('outputs/Final_3MF/README.md')

            def register(text, name=None, kind=None, folder=None):
                for revision in revision_ids(text, all_prefixes):
                    matches = [prefix for prefix in all_prefixes if revision_ids(revision, [prefix]) == [revision]]
                    if not matches:
                        continue
                    owner = owners[max(matches, key=len)]
                    r = revisions[owner].setdefault(revision, {'id': revision, 'date': '', 'date_source': 'not recorded', 'folders': [], 'three_mf': [], 'viewers': [], 'mentions': []})
                    if name:
                        dates = re.findall(r'20\d{2}-\d{2}-\d{2}', name)
                        try:
                            date = dates[-1] if dates else dt.datetime.fromtimestamp(safe_path(self.root, name).stat().st_mtime).date().isoformat()
                        except OSError:
                            date = ''
                        if dates:
                            r['date'] = max(r['date'] if r['date_source'] == 'folder name' else '', date)
                            r['date_source'] = 'folder name'
                        elif r['date_source'] != 'folder name':
                            r['date'] = max(r['date'], date)
                            r['date_source'] = 'file time'
                        if kind and name not in r[kind]:
                            r[kind].append(name)
                    if folder and folder not in r['folders']:
                        r['folders'].append(folder)

            # Bounded metadata walk: no mesh contents, app data, frozen sources or caches.
            output_root = safe_path(self.root, 'outputs')
            if output_root.exists():
                for base, dirs, files in os.walk(output_root, followlinks=False):
                    dirs[:] = [d for d in dirs if not d.startswith(('Mechanical_Design_App', 'Phase', 'Session_', '.')) and d.lower() not in ('src', 'stl', 'checks', 'data', 'revisions', 'cache', '__pycache__') and not (Path(base) / d).is_symlink()]
                    folder = Path(base).relative_to(self.root).as_posix()
                    folder_ids = revision_ids(Path(base).name, all_prefixes)
                    if folder_ids and ('README.md' in files or 'release_report.md' in files):
                        register(' '.join(folder_ids), folder, folder=folder)
                    for file in files:
                        name = folder + '/' + file
                        if file in ('README.md', 'release_report.md'):
                            content = read_text(name)
                            # README references are evidence, not a release association.
                            register(content)
                            if file == 'release_report.md':
                                declared = [content.split('\n', 1)[0]]
                                declared.extend(line for line in content.splitlines() if re.search(r': ID \S+ is on the mesh', line))
                                register('\n'.join(declared), name, folder=folder)
                        elif file.lower().endswith('.3mf'):
                            try:
                                safe_path(self.root, name)
                                register(file, name, 'three_mf', folder if 'README.md' in files else None)
                            except Problem as exc:
                                errors.append(name + ': ' + str(exc))
            viewers = safe_path(self.root, 'work/mesh-viewer')
            if viewers.exists():
                for path in viewers.glob('*.html'):
                    try:
                        name = path.relative_to(self.root).as_posix()
                        safe_path(self.root, name)
                        register(path.name, name, 'viewers')
                    except Problem as exc:
                        errors.append(str(exc))
            register(handoff)
            register(fit)
            register(final)

            # Map Final_3MF table's first ID(s) to its source-folder column.
            for line in final.splitlines():
                if line.startswith('|'):
                    cells = line.strip('|').split('|')
                    if len(cells) >= 3:
                        folder = 'outputs/' + cells[-1].strip().strip('`')
                        try:
                            if safe_path(self.root, folder).is_dir():
                                register(cells[0], folder, folder=folder)
                        except Problem:
                            pass

            fit_lines = [line for line in fit.splitlines() if line.strip() and not re.match(r'^\|\s*[-:]', line)]
            notices = [line for line in (final + '\n' + handoff).splitlines() if re.search(r'superseded|do not print|dropped|scratched|rejected|replaces|replaced by', line, re.I)]
            attention = []
            for p in projects:
                p['cards'], p['unknowns'] = [], []
                for name in p.get('device_cards', []):
                    content = read_text(name)
                    p['cards'].append({'path': name, 'html': self.render(content, name), 'missing': not content})
                    p['unknowns'].extend({'source': name, 'text': line} for line in content.splitlines() if line.strip().startswith('|') and re.search(r'\bUNKNOWN\b', line, re.I))
                for r in revisions[p['id']].values():
                    r['fit_lines'] = [line for line in fit_lines if has_id(line, r['id'])]
                    # Keep all mentions visible; use only the subject ID for guessing.
                    primary = [line for line in r['fit_lines'] if revision_ids_in_order(line, all_prefixes)[:1] == [r['id']]]
                    r['status'] = guess_fit(primary)
                    r['status_is_guess'] = True
                    r['warnings'] = [line for line in notices if has_id(line, r['id'])]
                    r['readmes'] = [f + '/README.md' for f in r['folders'] if f + '/README.md' in self.allowed_text]
                    r['reports'] = [f + '/release_report.md' for f in r['folders'] if f + '/release_report.md' in self.allowed_text]
                    r['released'] = bool(r['folders'])
                    if r['released'] and not primary:
                        attention.append({'project': p['id'], 'text': r['id'] + ': released with no direct fit report'})
                p['revisions'] = sorted(revisions[p['id']].values(), key=lambda r: (r['date'], natural(r['id'])), reverse=True)
                newest = next((r for r in p['revisions'] if r['readmes']), None)
                if newest:
                    for name in newest['readmes']:
                        p['unknowns'].extend({'source': name, 'text': line} for line in texts.get(name, '').splitlines() if re.search(r'\bUNKNOWN\b', line, re.I))
                p['workflow_html'] = self.render(workflow_section(workflow, p.get('workflow_log')), WORKFLOW)
                p['step'] = {'idea': 'Measure', 'measuring': 'Measure', 'draft': 'Draft', 'printing': 'Print', 'report-due': 'Report'}.get(p['status'], p['status'])
                if p['status'] == 'report-due':
                    attention.append({'project': p['id'], 'text': p['title'] + ': report due'})
                if p['status'] == 'printing' and (dt.date.today() - dt.date.fromisoformat(p['updated'])).days > 3:
                    attention.append({'project': p['id'], 'text': p['title'] + ': printing for more than 3 days'})
                if p['status'] == 'draft' and p['unknowns']:
                    attention.append({'project': p['id'], 'text': p['title'] + ': linked device/README UNKNOWNs; dependencies need review'})
            self.cache = {'projects': projects, 'attention': attention, 'errors': errors, 'hashes': self.hashes(), 'statuses': STATUSES, 'token': self.token, 'scan_seconds': round(time.perf_counter() - started, 6)}
            return self.cache

    def snapshot(self):
        with self.lock:
            return self.cache if self.cache is not None else self.refresh()

    def render(self, text, source):
        def link(url):
            # Normalize relative markdown links, then enforce the read allowlist.
            if ':' in url or '\\' in url or url.startswith('/'):
                return None
            candidate = (self.root / source).parent / url
            try:
                name = candidate.resolve().relative_to(self.root).as_posix()
                safe_path(self.root, name)
                if name in self.allowed_text:
                    return '/text?path=' + quote(name, safe='')
            except (ValueError, Problem):
                pass
            return None
        return markdown(text, link)

    def check_hashes(self, supplied, names):
        if not isinstance(supplied, dict):
            raise Problem('Reload the page before saving: file hashes are required.', 409)
        for name in names:
            if supplied.get(name) != digest(self.read(name, True)):
                raise Problem(name + ' changed. Refresh and review your draft before saving again.', 409)

    def replace(self, changes, hashes):
        """Stage every file and backup before replacement; rollback on caught I/O errors.

        Each replacement is atomic. No portable filesystem can atomically commit three
        files; power loss between replacements requires reviewing the .bak copies.
        """
        if not set(changes) <= set(WRITABLE):
            raise Problem('Write target is not allowed.', 403)
        self.check_hashes(hashes, changes)
        staged, originals, done = {}, {}, []
        try:
            for name, content in changes.items():
                path = safe_path(self.root, name)
                backup = safe_path(self.root, name + '.bak')
                if not path.is_file() or path.stat().st_nlink != 1:
                    raise Problem('Missing or linked write target: ' + name, 409)
                if backup.exists() and (not backup.is_file() or backup.stat().st_nlink != 1):
                    raise Problem('Backup is not a regular file: ' + name, 409)
                originals[name] = path.read_bytes()
                for target, payload in ((path, content), (backup, originals[name])):
                    fd, temp = tempfile.mkstemp(prefix='.' + path.name + '-', suffix='.tmp', dir=path.parent)
                    staged[str(target)] = temp
                    with os.fdopen(fd, 'wb') as stream:
                        stream.write(payload)
                        stream.flush()
                        os.fsync(stream.fileno())
            self.check_hashes(hashes, changes)
            for name in changes:
                path = safe_path(self.root, name)
                backup = safe_path(self.root, name + '.bak')
                os.replace(staged[str(backup)], backup)
            for name in changes:
                path = safe_path(self.root, name)
                os.replace(staged[str(path)], path)
                done.append(name)
        except OSError as exc:
            # .bak is retained, including if rollback itself fails.
            for name in reversed(done):
                path = safe_path(self.root, name)
                fd, temp = tempfile.mkstemp(prefix='.bench-rollback-', suffix='.tmp', dir=path.parent)
                staged['rollback:' + name] = temp
                with os.fdopen(fd, 'wb') as stream:
                    stream.write(originals[name])
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temp, path)
            raise Problem('Save failed; review the files and their .bak copies. ' + str(exc), 500)
        finally:
            for temp in staged.values():
                try:
                    os.unlink(temp)
                except FileNotFoundError:
                    pass
        self.cache = None

    def update(self, project_id, body):
        with self.lock:
            reject_keys(body, {'hashes', 'status', 'notes'})
            data = self.data()
            p = next((p for p in data['projects'] if p['id'] == project_id), None)
            if p is None:
                raise Problem('Unknown project.', 404)
            if not {'status', 'notes'} & body.keys():
                raise Problem('Supply a status or notes.')
            if 'status' in body:
                if body['status'] not in STATUSES:
                    raise Problem('Choose a valid project status.')
                p['status'] = body['status']
            if 'notes' in body:
                p['notes'] = clean_text(body['notes'], 'Notes', 12000, multiline=True)
            p['updated'] = dt.date.today().isoformat()
            self.replace({PROJECTS: json_bytes(data)}, body.get('hashes'))
            return p

    def create(self, body):
        with self.lock:
            reject_keys(body, {'hashes', 'id', 'title', 'prefixes', 'device_cards', 'sources'})
            title = clean_text(body.get('title'), 'Title', 160, required=True)
            project_id = body.get('id') or re.sub('[^a-z0-9]+', '-', title.lower()).strip('-')
            if not isinstance(project_id, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', project_id) or len(project_id) > 80:
                raise Problem('Use a short project ID of lowercase letters, digits and hyphens.')
            data = self.data()
            if any(p['id'] == project_id for p in data['projects']):
                raise Problem('That project ID already exists.')
            prefixes = body.get('prefixes')
            if not isinstance(prefixes, list) or not 1 <= len(prefixes) <= 20 or any(not isinstance(p, str) or not re.fullmatch('[A-Z][A-Z0-9]{1,15}', p) for p in prefixes):
                raise Problem('Supply 1–20 uppercase revision prefixes, 2–16 letters/digits each.')
            used = {x for p in data['projects'] for x in p['prefixes']}
            if len(set(prefixes)) != len(prefixes) or used.intersection(prefixes):
                raise Problem('A revision prefix is already in use.')
            # Compact CM6A-style IDs make overlapping prefixes ambiguous.
            if any(a != b and (a.startswith(b) or b.startswith(a)) for a in prefixes for b in used | set(prefixes)):
                raise Problem('Revision prefixes must not overlap existing prefixes.')
            p = {'id': project_id, 'title': title, 'prefixes': prefixes, 'status': 'idea', 'notes': '', 'updated': dt.date.today().isoformat(), 'workflow_log': ''}
            for key in ('device_cards', 'sources'):
                values = body.get(key, [])
                if not isinstance(values, list) or len(values) > 30:
                    raise Problem(key + ' must be a list of at most 30 paths.')
                for name in values:
                    path = safe_path(self.root, name)
                    if not path.is_file():
                        raise Problem('File does not exist: ' + name)
                    if key == 'device_cards' and (not name.startswith('docs/devices/') or path.suffix != '.md'):
                        raise Problem('Device cards must be markdown in docs/devices/.')
                    if key == 'sources' and not name.startswith(('work/', 'outputs/')):
                        raise Problem('Sources must be inside work/ or outputs/.')
                p[key] = values
            data['projects'].append(p)
            self.replace({PROJECTS: json_bytes(data)}, body.get('hashes'))
            return p

    def fit_preview(self, body):
        reject_keys(body, {'hashes', 'revision', 'result', 'where', 'walls', 'infill', 'notes'})
        revision = clean_text(body.get('revision'), 'Revision', 80, required=True)
        data = self.snapshot()
        p = next((p for p in data['projects'] if any(r['id'] == revision for r in p['revisions'])), None)
        if not p:
            raise Problem('Unknown revision. Select a discovered revision belonging to a project.')
        if body.get('result') not in RESULTS:
            raise Problem('Choose Fits, Too tight, Too loose, Failed or Other.')
        where = clean_text(body.get('where', ''), 'Where', 2000)
        notes = clean_text(body.get('notes', ''), 'Extra notes', 4000)
        walls = clean_text(body.get('walls', ''), 'Walls', 3)
        infill = clean_text(body.get('infill', ''), 'Infill', 6).rstrip('%')
        if walls and (not walls.isdecimal() or not 1 <= int(walls) <= 100):
            raise Problem('Walls must be a whole number from 1 to 100, or blank for UNKNOWN.')
        if infill and (not re.fullmatch(r'\d+(?:\.\d+)?', infill) or not 0 <= float(infill) <= 100):
            raise Problem('Infill must be 0–100 percent, or blank for UNKNOWN.')
        def sentence(value):
            return escape_markdown(value.rstrip('. ')) + '. ' if value else ''
        text = f'- {dt.date.today().isoformat()} {revision} (Brian, via Workshop Bench): {body["result"]}. '
        text += sentence(where) + (walls or 'UNKNOWN') + ' walls, ' + (infill + '%' if infill else 'UNKNOWN') + ' infill. '
        text += sentence(notes) + 'Strength UNKNOWN.'
        return {'project': p['id'], 'text': text}

    def report(self, body):
        with self.lock:
            self.check_hashes(body.get('hashes'), WRITABLE)
            preview = self.fit_preview(body)
            data = self.data()
            p = next(p for p in data['projects'] if p['id'] == preview['project'])
            changes = {FIT: append_bytes(self.read(FIT), preview['text'])}
            workflow = self.read(WORKFLOW).decode('utf-8')
            if workflow_section(workflow, p.get('workflow_log')):
                continuation = '\n## ' + p['workflow_log'] + ' (continued)\n\n| Date | Step | What happened | Friction | App idea |\n| --- | --- | --- | --- | --- |\n'
                continuation += '| ' + dt.date.today().isoformat() + ' | Report | ' + preview['text'][2:].replace('|', '&#124;') + ' | | |'
                changes[WORKFLOW] = append_bytes(self.read(WORKFLOW), continuation)
            p['status'], p['updated'] = 'draft', dt.date.today().isoformat()
            changes[PROJECTS] = json_bytes(data)
            self.replace(changes, body['hashes'])
            return preview


def revision_ids_in_order(text, prefixes):
    ids = revision_ids(text, prefixes)
    return sorted(ids, key=lambda value: text.find(value))


def clean_text(value, label, maximum, required=False, multiline=False):
    if not isinstance(value, str) or len(value) > maximum:
        raise Problem(f'{label} must be text, at most {maximum} characters.')
    if any(ord(c) < 32 and (not multiline or c not in '\n\r\t') for c in value):
        raise Problem(label + ' contains a control character or newline.')
    value = value.strip()
    if required and not value:
        raise Problem(label + ' is required.')
    return value


def escape_markdown(value):
    return html.escape(value, quote=False).replace('|', '&#124;').replace('`', '&#96;').replace('[', '&#91;').replace(']', '&#93;').replace('*', '&#42;')


def reject_keys(body, allowed):
    if not isinstance(body, dict) or set(body) - allowed:
        raise Problem('Unexpected fields in request.')


def json_bytes(data):
    return (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def send(self, code, payload, content_type='application/json; charset=utf-8', viewer=False):
        raw = json_bytes(payload) if content_type.startswith('application/json') else payload
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(raw)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        policy = "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data: blob:; connect-src 'self'; frame-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'self'"
        if viewer:
            policy = "sandbox allow-scripts; default-src 'none'; script-src 'unsafe-inline' 'unsafe-eval'; style-src 'unsafe-inline'; img-src data: blob:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'self'"
        self.send_header('Content-Security-Policy', policy)
        self.end_headers()
        self.wfile.write(raw)

    def dispatch(self):
        app = self.server.bench
        expected_host = '127.0.0.1:' + str(self.server.server_port)
        if self.headers.get('Host') != expected_host:
            raise Problem('Use the 127.0.0.1 address shown by Workshop Bench.', 403)
        origin = self.headers.get('Origin')
        if origin and origin != 'http://' + expected_host:
            raise Problem('Requests from other pages are not allowed.', 403)
        raw = self.path
        split = urlsplit(raw)
        if '\\' in split.path or '%' in unquote(split.path) or re.search(r'%(?:2e|2f|5c|00|3a)', split.path, re.I):
            raise Problem('Encoded paths are not allowed.', 403)
        if split.scheme or split.netloc:
            raise Problem('Absolute paths are not allowed.', 403)
        route = unquote(split.path)
        if '..' in route.split('/') or '\\' in route or ':' in route:
            raise Problem('That path is not allowed.', 403)
        if self.command == 'GET':
            data = app.snapshot()
            if route in ('/api/projects', '/api/state'):
                return self.send(200, data)
            if route == '/api/health':
                return self.send(200, {'ok': True, 'bind': self.server.server_address[0]})
            if route.startswith('/api/projects/'):
                p = next((p for p in data['projects'] if p['id'] == route[len('/api/projects/'):]), None)
                if not p:
                    raise Problem('Unknown project.', 404)
                return self.send(200, {'project': p, 'hashes': data['hashes'], 'token': app.token})
            if route == '/text':
                names = parse_qs(split.query).get('path', [])
                if len(names) != 1 or names[0] not in app.allowed_text:
                    raise Problem('This file is not a Bench document.', 403)
                content = app.read(names[0])
                return self.send(200, content, 'text/plain; charset=utf-8')
            if route.startswith('/viewer/'):
                name = route[len('/viewer/'):]
                if '/' in name or not name.endswith('.html'):
                    raise Problem('Only viewer HTML pages can be shown.', 403)
                return self.send(200, app.read('work/mesh-viewer/' + name), 'text/html; charset=utf-8', viewer=True)
            name = 'index.html' if route == '/' else route.removeprefix('/static/')
            if route != '/' and not route.startswith('/static/'):
                raise Problem('Page not found.', 404)
            if name not in ('index.html', 'bench.css', 'bench.js'):
                raise Problem('File not found.', 404)
            path = safe_path(STATIC, name)
            types = {'.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript'}
            return self.send(200, path.read_bytes(), types[path.suffix] + '; charset=utf-8')
        if self.command not in ('POST', 'PATCH'):
            raise Problem('Method not allowed.', 405)
        if self.headers.get('X-Bench-Token') != app.token:
            raise Problem('Reload Workshop Bench before saving.', 403)
        if self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
            raise Problem('Send JSON with Content-Type application/json.', 415)
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 65536:
                raise Problem('Request must be between 1 and 65536 bytes.', 413)
            body = json.loads(self.rfile.read(size).decode('utf-8'))
        except (ValueError, UnicodeError):
            raise Problem('Request is not valid UTF-8 JSON.')
        if not isinstance(body, dict):
            raise Problem('Request must be a JSON object.')
        if self.command == 'POST' and route == '/api/refresh':
            reject_keys(body, set())
            return self.send(200, app.refresh())
        if self.command == 'POST' and route == '/api/projects':
            return self.send(201, app.create(body))
        if self.command == 'PATCH' and route.startswith('/api/projects/'):
            return self.send(200, app.update(route[len('/api/projects/'):], body))
        if self.command == 'POST' and route == '/api/fit-report/preview':
            return self.send(200, app.fit_preview(body))
        if self.command == 'POST' and route == '/api/fit-report':
            return self.send(200, app.report(body))
        raise Problem('API route not found.', 404)

    def handle_request(self):
        try:
            self.dispatch()
        except Problem as exc:
            self.send(exc.status, {'error': str(exc)})
        except (OSError, UnicodeError, ValueError) as exc:
            self.send(500, {'error': 'Could not read or save a Bench file: ' + str(exc)})

    do_GET = do_POST = do_PATCH = do_DELETE = do_PUT = handle_request


def make_server(root, port=8720):
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    server.daemon_threads = True
    server.bench = Bench(root)
    return server


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--port', type=int, default=8720)
    args = parser.parse_args()
    server = make_server(args.root, args.port)
    print(f'Workshop Bench: http://127.0.0.1:{server.server_port} (root: {server.bench.root})', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
