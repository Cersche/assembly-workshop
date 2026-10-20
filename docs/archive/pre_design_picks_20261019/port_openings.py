"""Pure front-opening planning. Physical fit and strength remain UNKNOWN."""
from copy import deepcopy
import math

DEFAULT_SIZES = {
    'rj45': {'w': 17, 'h': 14, 'r': 1}, 'usb-a': {'w': 15, 'h': 8, 'r': 1},
    'usb-c': {'w': 12, 'h': 7, 'r': 3}, 'hdmi': {'w': 17, 'h': 8, 'r': 1},
    'micro-hdmi': {'w': 11, 'h': 7, 'r': 2}, 'dc-barrel': {'w': 11, 'h': 11, 'r': 5.5},
    'iec': {'w': 28, 'h': 20, 'r': 1}, 'other': {'w': 15, 'h': 8, 'r': 1}}
SIZE_NOTE = 'Starting size for this connector type: a guess, not a measured size. Edit it to match your device.'


def default_size(type=None):
    return dict(DEFAULT_SIZES.get(type, DEFAULT_SIZES['other']))


def lift(spec):
    return 0 if spec.get('device_mount', 'inserts') == 'straps' else float(spec.get('standoff', 6))


def front_openings(lib_spec, tray=None):
    eff = dict(lib_spec)
    eff.update({k: v for k, v in (tray or {}).items() if k in ('dev_off_x', 'dev_rot', 'device_mount', 'standoff')})
    rotation = float(eff.get('dev_rot') or 0)
    follows = rotation == 0
    dx = float(eff.get('dev_off_x') or 0) - float(lib_spec.get('dev_off_x') or 0) if follows else 0
    dz = lift(eff) - lift(lib_spec) if follows else 0
    ports = deepcopy(lib_spec.get('ports') or [])
    if follows:
        for p in ports:
            p.update(x=round(float(p['x']) + dx, 3), z=round(float(p['z']) + dz, 3))
    face = 'rear' if rotation == 180 else 'side'
    message = (f'The device is turned {rotation:g}°, so its front ports now face the {face} of the tray. '
               'The front openings no longer line up with them. The faceplate STL keeps the openings where they were entered '
               'in the library (not moved). Check them, or remove them in Edit library item.') if not follows and ports else None
    return dict(ports=ports, dx=dx, dz=dz, follows=follows, rotation=rotation, message=message)


def problems(ports, u, keystones):
    out = []
    plate_h = u * 44.45 - 2.45
    for i, p in enumerate(ports or []):
        values = [p.get(k) for k in ('x', 'z', 'w', 'h')]
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in values):
            continue
        x, z, w, h = values
        label = p.get('label') or f'Port {i + 1}'
        if abs(x) + w / 2 > 126:
            out.append(f'{label} opening would run past the faceplate edge. Move the device back toward the centre or edit the port.')
        elif z - h / 2 < 2 or z + h / 2 > plate_h - 2:
            out.append(f'{label} opening would run off the top or bottom of the faceplate. Change the standoff or faceplate height, or edit the port.')
        else:
            for n, k in enumerate(keystones or []):
                if abs(x - k) < 10.5 + w / 2 and z - h / 2 < plate_h / 2 + 18.5 and z + h / 2 > plate_h / 2 - 15:
                    out.append(f'{label} opening would cut into keystone {n + 1} (at X = {k:g} mm). Move the device or the keystone.')
                    break
    return out
