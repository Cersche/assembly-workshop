"""Cable-planning port data (cable management Step 2). Planning data only: no geometry, STL or hardware pins.

Port positions are in the equipment frame the rack view uses: X from the rack centre, Y depth from the
faceplate rear face (front face of a plate is negative Y), Z above the allocation's bottom. Connector fit,
cable access and clearance remain UNKNOWN.
"""
import math
import re

PORT_TYPES = ('rj45', 'usb-a', 'usb-c', 'hdmi', 'micro-hdmi', 'dc-barrel', 'iec', 'keystone', 'other')
FACES = ('front', 'rear')
PITCH = 44.45
PORT_ID = re.compile(r'[a-z0-9][a-z0-9-]{0,39}')
MAX_PER_ALLOCATION = 64


def _number(value, name, lo, hi):
    if type(value) not in (int, float) or not math.isfinite(value) or not lo <= value <= hi:
        raise ValueError(f'Port {name} must be a number between {lo:g} and {hi:g} mm.')
    return round(float(value), 3)


def _label(value):
    if not isinstance(value, str) or len(value) > 40:
        raise ValueError('Port labels are text, up to 40 characters.')
    return value.strip()


def overrides(value, allocations):
    """Per-placement port edits in rack.cabling.ports: position fine-tuning (mesh click), label/type changes
    and custom ports. allocations maps placement id -> span in U. Returns the cleaned list."""
    if not isinstance(value, list):
        raise ValueError('Cable ports must be a list.')
    seen, counts, clean = set(), {}, []
    for item in value:
        if not isinstance(item, dict) or set(item) - {'allocation', 'port', 'label', 'type', 'face', 'x', 'y', 'z', 'custom'}:
            raise ValueError('Each cable port entry must be an object with known fields.')
        allocation, port = item.get('allocation'), item.get('port')
        if allocation not in allocations:
            raise ValueError('A cable port refers to equipment that is not in this rack.')
        if not isinstance(port, str) or not PORT_ID.fullmatch(port):
            raise ValueError('Port ids use lowercase letters, digits and dashes (up to 40).')
        if (allocation, port) in seen:
            raise ValueError(f'Port {port} is listed twice for the same equipment.')
        seen.add((allocation, port))
        counts[allocation] = counts.get(allocation, 0) + 1
        if counts[allocation] > MAX_PER_ALLOCATION:
            raise ValueError(f'Use at most {MAX_PER_ALLOCATION} port entries per equipment item.')
        custom = item.get('custom', False)
        if type(custom) is not bool:
            raise ValueError('Custom port flag must be true or false.')
        if custom and not all(k in item for k in ('label', 'type', 'face', 'x', 'z')):
            raise ValueError('A custom port needs a label, type, face and position.')
        out = {'allocation': allocation, 'port': port}
        if custom:
            out['custom'] = True
        if 'label' in item:
            out['label'] = _label(item['label'])
        if 'type' in item:
            if item['type'] not in PORT_TYPES:
                raise ValueError('Unknown port connector type.')
            out['type'] = item['type']
        if 'face' in item:
            if item['face'] not in FACES:
                raise ValueError('A port face is front or rear.')
            out['face'] = item['face']
        height = allocations[allocation] * PITCH
        for key, lo, hi in (('x', -150, 150), ('y', -40, 280), ('z', -10, height + 10)):
            if key in item:
                out[key] = _number(item[key], key.upper(), lo, hi)
        if len(out) == 2:
            raise ValueError('A port entry must change something.')
        clean.append(out)
    return clean


def port_type(value, default='other'):
    if value is None:
        return default
    if value not in PORT_TYPES:
        raise ValueError('Unknown port connector type.')
    return value
