"""Validate cable planning data. No geometry or physical approval is implied."""
import math
import re

from cable_ports import PORT_ID, PORT_TYPES

EXIT_POSITIONS = ('bottom-rear', 'top-rear', 'left', 'right')
ENDPOINT_KINDS = ('wall-outlet', 'ups', 'modem', 'wall-jack', 'desk', 'other-rack', 'other')


def _object(value, keys, name):
    if not isinstance(value, dict) or set(value) - set(keys):
        raise ValueError(f'{name} must be an object with known fields.')


def _text(value, maximum, name, minimum=1):
    if not isinstance(value, str) or not minimum <= len(value.strip()) <= maximum:
        raise ValueError(f'{name} must be text, {minimum} to {maximum} characters.')
    return value.strip()


def _number(value, name):
    if type(value) not in (int, float) or not 0 <= value <= 2 or not math.isfinite(value):
        raise ValueError(f'{name} must be a finite number between 0 and 2 metres.')
    return value


def _entries(value, name, maximum):
    entries = value.get(name, [])
    if not isinstance(entries, list) or len(entries) > maximum:
        raise ValueError(f'Cable {name} must be a list of at most {maximum} entries.')
    return entries


def _identity(item, seen, name):
    identity = item.get('id')
    if not isinstance(identity, str) or not identity or len(identity) > 80:
        raise ValueError(f'{name} id must be non-empty text, up to 80 characters.')
    if identity in seen:
        raise ValueError(f'{name} ids must be unique.')
    seen.add(identity)
    return identity


def validate(value, slots, allocations, guide_ids):
    """Return only supplied Step 3 keys, keeping legacy cabling documents unchanged."""
    _object(value, ('guides', 'ports', 'exits', 'endpoints', 'cables', 'settings'), 'Cable management data')
    result, exit_ids, endpoint_ids, cable_ids = {}, set(), set(), set()
    exits, endpoints, cables, spots, numbers, used_ports = [], [], [], set(), set(), set()
    for item in _entries(value, 'exits', 32):
        _object(item, ('id', 'position', 'slot'), 'Cable exit')
        identity = _identity(item, exit_ids, 'Cable exit')
        position, slot = item.get('position'), item.get('slot')
        if position not in EXIT_POSITIONS:
            raise ValueError('A cable exit position is bottom-rear, top-rear, left or right.')
        if type(slot) is not int or not 1 <= slot <= slots:
            raise ValueError('A cable exit slot must be an integer inside the rack slots.')
        if (position, slot) in spots:
            raise ValueError('A cable exit already occupies that position and slot.')
        spots.add((position, slot))
        exits.append({'id': identity, 'position': position, 'slot': slot})
    for item in _entries(value, 'endpoints', 50):
        _object(item, ('id', 'kind', 'name'), 'Outside endpoint')
        identity = _identity(item, endpoint_ids, 'Outside endpoint')
        if item.get('kind') not in ENDPOINT_KINDS:
            raise ValueError('Unknown outside endpoint kind.')
        endpoints.append({'id': identity, 'kind': item['kind'], 'name': _text(item.get('name'), 60, 'Endpoint name')})

    def end(value):
        if value is None:
            return None
        _object(value, ('allocation', 'port', 'endpoint'), 'Cable end')
        if set(value) == {'endpoint'}:
            if not isinstance(value['endpoint'], str) or value['endpoint'] not in endpoint_ids:
                raise ValueError('A cable refers to an unknown outside endpoint.')
            return dict(value)
        if set(value) != {'allocation', 'port'}:
            raise ValueError('A cable end needs allocation and port, or endpoint.')
        allocation, port = value['allocation'], value['port']
        if not isinstance(allocation, str) or allocation not in allocations:
            raise ValueError('A cable refers to equipment that is not in this rack.')
        if not isinstance(port, str) or not PORT_ID.fullmatch(port):
            raise ValueError('Cable port ids use lowercase letters, digits and dashes (up to 40).')
        key = (allocation, port)
        if key in used_ports:
            raise ValueError('A port can be used by only one cable end.')
        used_ports.add(key)
        return dict(value)

    for item in _entries(value, 'cables', 200):
        _object(item, ('id', 'number', 'type', 'color', 'service_loop_m', 'from', 'to',
                       'face_assumed', 'route', 'route_changed', 'note', 'carries', 'unplug_often'), 'Cable')
        identity = _identity(item, cable_ids, 'Cable')
        number = _text(item.get('number'), 12, 'Cable number')
        if number in numbers:
            raise ValueError('Cable numbers must be unique.')
        numbers.add(number)
        if item.get('type') not in PORT_TYPES:
            raise ValueError('Unknown cable connector type.')
        if 'from' not in item or 'to' not in item:
            raise ValueError('A cable needs from and to ends (null is unconnected).')
        start, finish = end(item['from']), end(item['to'])
        if start is not None and start == finish:
            raise ValueError('A cable must not connect an end to itself.')
        route = item.get('route')
        _object(route, ('mode', 'guides', 'exit'), 'Cable route')
        if route.get('mode') not in ('auto', 'manual'):
            raise ValueError('Cable route mode is auto or manual.')
        guides = route.get('guides')
        if not isinstance(guides, list) or len(guides) > 48:
            raise ValueError('A cable route needs a list of at most 48 guides.')
        seen = set()
        for guide in guides:
            if not isinstance(guide, str) or guide not in guide_ids:
                raise ValueError('A cable route refers to an unknown guide.')
            if guide in seen:
                raise ValueError('A cable route must not repeat a guide.')
            seen.add(guide)
        if 'exit' not in route:
            raise ValueError('A cable route needs an exit id or null.')
        exit_id = route['exit']
        if exit_id is not None and (not isinstance(exit_id, str) or exit_id not in exit_ids):
            raise ValueError('A cable route refers to an unknown exit.')
        out = {'id': identity, 'number': number, 'type': item['type'],
               'service_loop_m': _number(item.get('service_loop_m'), 'Cable service loop'),
               'from': start, 'to': finish,
               'route': {'mode': route['mode'], 'guides': list(guides), 'exit': exit_id}}
        if 'color' in item:
            if not isinstance(item['color'], str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', item['color']):
                raise ValueError('Cable colour must be a six-digit hex colour (#rrggbb).')
            out['color'] = item['color'].lower()
        if 'face_assumed' in item:
            if item['face_assumed'] != 'rear':
                raise ValueError('An assumed cable face must be rear.')
            out['face_assumed'] = 'rear'
        if 'route_changed' in item:
            if type(item['route_changed']) is not bool:
                raise ValueError('Cable route changed must be true or false.')
            out['route_changed'] = item['route_changed']
        if 'note' in item:
            if not isinstance(item['note'], str) or len(item['note']) > 200:
                raise ValueError('Cable note must be text, up to 200 characters.')
            out['note'] = item['note']
        if 'carries' in item:
            if item['carries'] not in ('power', 'data'):
                raise ValueError('Cable carries is power or data.')
            out['carries'] = item['carries']
        if 'unplug_often' in item:
            if type(item['unplug_often']) is not bool:
                raise ValueError('Cable unplugged often must be true or false.')
            out['unplug_often'] = item['unplug_often']
        cables.append(out)
    for key, cleaned in (('exits', exits), ('endpoints', endpoints), ('cables', cables)):
        if key in value:
            result[key] = cleaned
    if 'settings' in value:
        settings = value['settings']
        _object(settings, ('guide_warn_above', 'service_loop_m', 'power_post', 'ignored_suggestions'), 'Cable settings')
        threshold = settings.get('guide_warn_above', 6)
        if type(threshold) is not int or not 1 <= threshold <= 50:
            raise ValueError('Guide warning setting must be an integer between 1 and 50.')
        result['settings'] = {'guide_warn_above': threshold,
                              'service_loop_m': _number(settings.get('service_loop_m', 0.15), 'Default service loop')}
        if 'power_post' in settings:
            if settings['power_post'] not in ('RR', 'RL'):
                raise ValueError('The power post is RR or RL.')
            result['settings']['power_post'] = settings['power_post']
        if 'ignored_suggestions' in settings:
            entries = settings['ignored_suggestions']
            if not isinstance(entries, list) or len(entries) > 500:
                raise ValueError('Ignored suggestions are a list of at most 500 {id, sig} entries.')
            cleaned, ids = [], set()
            for entry in entries:
                if not isinstance(entry, dict) or set(entry) != {'id', 'sig'}:
                    raise ValueError('Each ignored suggestion needs exactly id and sig.')
                for key, maximum in (('id', 120), ('sig', 32)):
                    if not isinstance(entry[key], str) or not 1 <= len(entry[key]) <= maximum:
                        raise ValueError(f'Ignored suggestion {key} must be non-empty text, up to {maximum} characters.')
                if entry['id'] in ids:
                    raise ValueError('Ignored suggestion ids must be unique.')
                ids.add(entry['id'])
                cleaned.append(dict(entry))
            result['settings']['ignored_suggestions'] = cleaned
    return result
