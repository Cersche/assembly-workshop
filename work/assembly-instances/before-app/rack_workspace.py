"""Separate rack-layout documents; never migrates hardware pins or cached meshes."""
import json
import math
import os
from pathlib import Path
import tempfile
import threading
import uuid

_lock = threading.Lock()


def validate(value):
    if not isinstance(value, dict) or value.get('version') != 1:
        raise ValueError('Unsupported rack workspace version.')
    racks = value.get('racks')
    if not isinstance(racks, list) or len(racks) > 50:
        raise ValueError('Use up to 50 rack layouts.')
    ids = set()
    clean = {'version': 1, 'racks': []}
    for rack in racks:
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
        result = {'id': identity, 'name': name.strip(), 'slots': slots}
        for key in ('width_mm', 'depth_mm', 'pitch_mm'):
            number = rack.get(key)
            if number is not None and (type(number) not in (int, float) or not math.isfinite(number) or not 0 < number <= 10000):
                raise ValueError('Rack dimensions must be positive millimeters, or unknown.')
            result[key] = number
        placements = rack.get('placements', [])
        if not isinstance(placements, list) or len(placements) > slots:
            raise ValueError('Invalid slot assignments.')
        occupied = set()
        placement_ids = set()
        result['placements'] = []
        for item in placements:
            start, span = item.get('slot'), item.get('span')
            if type(start) is not int or type(span) is not int or start < 1 or span < 1 or start + span - 1 > slots:
                raise ValueError('Assembly extends outside the rack slots.')
            allocation = set(range(start, start + span))
            if occupied & allocation:
                raise ValueError('Slot allocations overlap. Choose an empty slot range.')
            occupied.update(allocation)
            if item.get('equipment') != 'pi4':
                raise ValueError('Only the documented Raspberry Pi 4 assembly is supported currently.')
            item_id = item.get('id')
            if not isinstance(item_id, str) or not item_id or len(item_id) > 80 or item_id in placement_ids:
                raise ValueError('Assembly identities must be unique within a rack.')
            placement_ids.add(item_id)
            result['placements'].append({'id': item_id, 'equipment': 'pi4', 'slot': start, 'span': span,
                                         'geometry': 'pi4-clearance-v2-reference', 'fit': 'UNKNOWN'})
        clean['racks'].append(result)
    return clean


def read(data_dir):
    path = Path(data_dir) / 'rack-workspace.json'
    if not path.exists():
        return {'version': 1, 'generation': None, 'racks': []}
    value = json.loads(path.read_text(encoding='utf-8'))
    try:
        uuid.UUID(value['generation'])
    except (KeyError, ValueError, TypeError, AttributeError) as exc:
        raise ValueError('Invalid rack document generation; preserve the file for recovery.') from exc
    return dict(validate(value), generation=value.get('generation'))


def save(data_dir, value):
    clean = validate(value)
    path = Path(data_dir) / 'rack-workspace.json'
    with _lock:
        previous = read(data_dir)
        if value.get('generation') != previous['generation']:
            raise ValueError('Rack layout changed in another session. Reload before saving.')
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
