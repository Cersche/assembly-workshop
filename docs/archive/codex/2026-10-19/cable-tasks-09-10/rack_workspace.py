"""Separate rack-layout documents; never migrates hardware pins or cached meshes."""
import json
import assembly_records
import cable_ports
import math
import os
from pathlib import Path
import re
import tempfile
import threading
import uuid

_lock = threading.Lock()


GUIDE_POSTS = ('FL', 'FR', 'RL', 'RR')


def _cabling(value, slots, allocations=None):
    """Optional cable-management planning data. Guides are preview placements; ports are planning data
    (cable_ports.overrides). Fit, strength, capacity and cable access UNKNOWN."""
    if value is None:
        return None
    if not isinstance(value, dict) or set(value) - {'guides', 'ports'}:
        raise ValueError('Invalid cable management data.')
    guides = value.get('guides', [])
    if not isinstance(guides, list) or len(guides) > 4 * slots:
        raise ValueError('Use at most one cable guide per post per U.')
    ids, spots, clean = set(), set(), []
    for guide in guides:
        if not isinstance(guide, dict): raise ValueError('Each cable guide must be an object.')
        identity, post, slot = guide.get('id'), guide.get('post'), guide.get('slot')
        if not isinstance(identity, str) or not identity or len(identity) > 80 or identity in ids:
            raise ValueError('Cable guide identities must be unique.')
        if guide.get('kind', 'labrax-cable-guide') != 'labrax-cable-guide':
            raise ValueError('Unknown cable guide type.')
        if post not in GUIDE_POSTS:
            raise ValueError('A cable guide goes on post FL, FR, RL or RR.')
        if type(slot) is not int or not 1 <= slot <= slots:
            raise ValueError('A cable guide must sit inside the rack slots.')
        if (post, slot) in spots:
            raise ValueError(f'Post {post} already has a cable guide at U{slot}.')
        ids.add(identity)
        spots.add((post, slot))
        clean.append({'id': identity, 'kind': 'labrax-cable-guide', 'post': post, 'slot': slot})
    result = {'guides': clean}
    if 'ports' in value:
        result['ports'] = cable_ports.overrides(value['ports'], allocations or {})
    return result


def validate(value, seed_project=None):
    if not isinstance(value, dict) or value.get('version') not in (1, 2):
        raise ValueError('Unsupported rack workspace version.')
    racks = value.get('racks')
    if not isinstance(racks, list) or len(racks) > 50:
        raise ValueError('Use up to 50 rack layouts.')
    ids = set()
    assembly_ids = set()
    clean = {'version': 2, 'racks': []}
    for rack in racks:
        if not isinstance(rack, dict): raise ValueError('Each rack must be an object.')
        identity = rack.get('id')
        if not isinstance(identity, str) or not identity or len(identity) > 80 or identity in ids:
            raise ValueError('Rack identities must be unique.')
        ids.add(identity)
        name = rack.get('name', '')
        if not isinstance(name, str) or not name.strip() or len(name) > 100:
            raise ValueError('Give the rack a name, up to 100 characters.')
        slots = rack.get('slots')
        if type(slots) is not int or not 1 <= slots <= 48:
            raise ValueError('Rack layouts support 1–48 slots.')
        result = {'id': identity, 'name': name.strip(), 'slots': slots, 'appearance': assembly_records.appearance(rack.get('appearance'), rack=True)}
        for key in ('width_mm', 'depth_mm', 'pitch_mm'):
            number = rack.get(key)
            if number is not None and (type(number) not in (int, float) or not math.isfinite(number) or not 0 < number <= 10000):
                raise ValueError('Rack dimensions must be positive millimeters, or unknown.')
            result[key] = number
        # Optional per-side post segment stack (bottom-up U sizes), set by moving the support extension.
        levels = rack.get('post_levels')
        if levels is not None:
            if not isinstance(levels, dict) or set(levels) - {'left', 'right'}:
                raise ValueError('Invalid post segment layout.')
            for side, stack in levels.items():
                # Each joint is a 1U support extension, so posts + joints = slots.
                if not isinstance(stack, list) or not stack or not all(type(u) is int and 1 <= u <= 5 for u in stack) or sum(stack) + len(stack) - 1 != slots:
                    raise ValueError('Post segments (1–5U) plus 1U support extensions must add up to the rack height.')
            result['post_levels'] = {side: list(stack) for side, stack in levels.items()}
        locked = rack.get('layout_locked')
        if locked is not None:
            if type(locked) is not bool:
                raise ValueError('Layout lock must be true or false.')
            result['layout_locked'] = locked
        placements = rack.get('placements', [])
        if not isinstance(placements, list) or len(placements) > slots:
            raise ValueError('Invalid slot assignments.')
        occupied = set()
        placement_ids = set()
        result['placements'] = []
        for item in placements:
            if not isinstance(item, dict): raise ValueError('Each allocation must be an object.')
            start, span = item.get('slot'), item.get('span')
            if type(start) is not int or type(span) is not int or start < 1 or span < 1 or start + span - 1 > slots:
                raise ValueError('Assembly extends outside the rack slots.')
            allocation = set(range(start, start + span))
            if occupied & allocation:
                raise ValueError('Slot allocations overlap. Choose an empty slot range.')
            occupied.update(allocation)
            equipment = item.get('equipment')
            if equipment != 'pi4' and not (isinstance(equipment, str) and re.fullmatch('eq-[0-9a-f]{12}', equipment)):
                raise ValueError('Unknown equipment type in a slot allocation.')
            item_id = item.get('id')
            if not isinstance(item_id, str) or not item_id or len(item_id) > 80 or item_id in placement_ids:
                raise ValueError('Assembly identities must be unique within a rack.')
            placement_ids.add(item_id)
            record = assembly_records.normalize(item.get('assembly'), identity, item_id, seed_project)
            if record['id'] in assembly_ids: raise ValueError('Assembly identities must be unique across the workspace.')
            assembly_ids.add(record['id'])
            result['placements'].append({'assembly': record, 'id': item_id, 'equipment': equipment, 'slot': start, 'span': span,
                                         'geometry': 'pi4-clearance-v2-reference' if equipment == 'pi4' else 'equipment-library', 'fit': 'UNKNOWN'})
        # Ports refer to placements by id, so cabling is checked after them.
        cabling = _cabling(rack.get('cabling'), slots, {p['id']: p['span'] for p in result['placements']})
        if cabling is not None:
            result['cabling'] = cabling
        clean['racks'].append(result)
    return clean


def read(data_dir, seed_project=None):
    path = Path(data_dir) / 'rack-workspace.json'
    if not path.exists():
        return {'version': 2, 'generation': None, 'racks': []}
    value = json.loads(path.read_text(encoding='utf-8'))
    try:
        uuid.UUID(value['generation'])
    except (KeyError, ValueError, TypeError, AttributeError) as exc:
        raise ValueError('Invalid rack document generation; preserve the file for recovery.') from exc
    return dict(validate(value, seed_project), generation=value.get('generation'))


def _latest_history_record(data_dir, identity, seed_project=None):
    """Most recent saved hardware record for an assembly id across rack-history/, or None."""
    history = Path(data_dir) / 'rack-history'
    if not history.exists(): return None
    for snapshot in sorted(history.glob('*.json'), key=lambda p:p.stat().st_mtime_ns, reverse=True):
        historic = validate(json.loads(snapshot.read_text(encoding='utf-8')), seed_project)
        for r in historic['racks']:
            for p in r['placements']:
                if p['assembly']['id'] == identity: return p['assembly']
    return None


def _history_path(data_dir, generation):
    try:
        name = str(uuid.UUID(generation))
    except (ValueError, TypeError, AttributeError) as exc:
        raise ValueError('Unknown saved version.') from exc
    path = Path(data_dir) / 'rack-history' / (name + '.json')
    if not path.is_file():
        raise ValueError('Unknown saved version.')
    return path


def list_history(data_dir, seed_project=None):
    """Read-only summaries of earlier saved layouts in rack-history/, newest first. Never modifies history."""
    history = Path(data_dir) / 'rack-history'
    if not history.exists(): return []
    entries = []
    for snapshot in sorted(history.glob('*.json'), key=lambda p:p.stat().st_mtime_ns, reverse=True):
        try:
            uuid.UUID(snapshot.stem)
        except ValueError:
            continue
        entry = {'generation': snapshot.stem, 'replaced_ns': snapshot.stat().st_mtime_ns}
        try:
            value = validate(json.loads(snapshot.read_text(encoding='utf-8')), seed_project)
            entry['racks'] = [{'id': r['id'], 'name': r['name'], 'slots': r['slots'],
                               'allocations': [{'slot': p['slot'], 'span': p['span'], 'name': p['assembly']['name']} for p in r['placements']]}
                              for r in value['racks']]
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
            entry['unreadable'] = str(exc)[:200]
        entries.append(entry)
    return entries


def restore_rack(data_dir, generation, rack_id, seed_project=None):
    """Build an unsaved draft of one rack from an earlier saved version. Nothing is written.
    Each assembly keeps its newest saved hardware (current document, else latest history) so Save's
    revision checks hold; layout, slots, post segments and appearance come from the earlier version."""
    snapshot = validate(json.loads(_history_path(data_dir, generation).read_text(encoding='utf-8')), seed_project)
    rack = next((r for r in snapshot['racks'] if r['id'] == rack_id), None)
    if rack is None:
        raise ValueError('That rack is not in the selected saved version.')
    current = read(data_dir, seed_project)
    records = {p['assembly']['id']: p['assembly'] for r in current['racks'] for p in r['placements']}
    elsewhere = {p['assembly']['id'] for r in current['racks'] if r['id'] != rack_id for p in r['placements']}
    for placement in rack['placements']:
        identity = placement['assembly']['id']
        if identity in elsewhere:
            raise ValueError(f"“{placement['assembly']['name']}” now belongs to another rack; release it there first.")
        newest = records.get(identity) or _latest_history_record(data_dir, identity, seed_project)
        if newest is not None:
            placement['assembly'] = newest
    return rack


def save(data_dir, value, seed_project=None, allow_project_changes=False, canonical_project=None):
    clean = validate(value, seed_project)
    path = Path(data_dir) / 'rack-workspace.json'
    with _lock:
        previous = read(data_dir, seed_project)
        if value.get('generation') != previous['generation']:
            raise ValueError('Rack layout changed in another session. Reload before saving.')
        if path.exists():
            stored_version = json.loads(path.read_text(encoding='utf-8')).get('version')
            if stored_version == 2 and value.get('version') != 2:
                raise ValueError('This workspace now has independent assemblies. Reload the updated app; old clients cannot overwrite it.')
        old_records = {p['assembly']['id']: p['assembly'] for r in previous['racks'] for p in r['placements']}
        # A session undo can restore a released, previously saved assembly. It must
        # restore the most recent hardware snapshot, never invent an older revision.
        released_record = lambda identity: _latest_history_record(path.parent, identity, seed_project)
        for rack in clean['racks']:
            for placement in rack['placements']:
                record = placement['assembly'];old = old_records.get(record['id'])
                if old and not allow_project_changes and (record['revision'] != old['revision'] or record['project'] != old['project']):
                    raise ValueError('Assembly hardware changed. Reload or save it through its independent editor first.')
                if not old:
                    released = released_record(record['id'])
                    if released and (record['revision'] != released['revision'] or record['project'] != released['project']):
                        raise ValueError('Restore the most recent saved assembly hardware snapshot.')
                    if not released and record['revision'] != 1:
                        raise ValueError('New assemblies start at revision 1.')
                if canonical_project is not None:
                    project = canonical_project(record['project'])
                    record['project'] = assembly_records.project_snapshot(project, record['id'], record['name'])
        clean['generation'] = str(uuid.uuid4())
        path.parent.mkdir(parents=True, exist_ok=True)
        # Preserve each prior saved layout as an immutable recovery document.
        if path.exists():
            history = path.parent / 'rack-history'
            history.mkdir(exist_ok=True)
            backup_path = history / (str(uuid.UUID(previous['generation'])) + '.json')
            previous_text = path.read_text(encoding='utf-8')
            if backup_path.exists():
                if backup_path.read_text(encoding='utf-8') != previous_text:
                    raise ValueError('Recovery history differs; preserve it and resolve before saving.')
            else:
                with backup_path.open('x', encoding='utf-8') as backup:
                    backup.write(previous_text)
        temp_name = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as stream:
                temp_name = stream.name
                json.dump(clean, stream, ensure_ascii=False, indent=2)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp_name, path)
        finally:
            if temp_name and Path(temp_name).exists():
                Path(temp_name).unlink()
    return clean
