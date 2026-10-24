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
import print_layout

import cable_ports
import port_openings
import mesh_revision

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / 'equipment_tray.scad'
MOUNTS = ('wall', 'inserts', 'pegs', 'clips', 'straps', 'flat', 'sleeve')
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
PLACEMENT_KEYS = ('dev_off_x', 'dev_off_y', 'dev_rot', 'device_mount', 'wall_open', 'standoff', 'insert_pilot', 'board_t',
                  'joint', 'keystones', 'rear_support', 'rear_openings', 'rear_style', 'u', 'front_position', 'front_setback', 'bezel', 'bezel_size',
                  'sleeve_top', 'feet_style', 'rear_floor_opening', 'insert_bosses', 'hidden_joint')


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
    if 'faceplate' in value:
        if set(value) != {'faceplate'} or not isinstance(value['faceplate'],dict):
            raise ValueError('Faceplate settings cannot be mixed with tray settings.')
        panel = clean_faceplate(value['faceplate'])
        return {'faceplate': {k:panel[k] for k in ('u','layout','count','rows','keystones','ports') if k in panel}}
    for key in PLACEMENT_KEYS:
        if key not in value:
            continue
        v = value[key]
        if key == 'wall_open':
            v = wall_open(v)
        elif key == 'keystones':
            if not isinstance(v, list) or len(v) > 12 or any(type(x) not in (int, float) or isinstance(x, bool) for x in v):
                raise ValueError('Keystones must be a list of positions.')
            v = list(v)
        elif key in ('rear_support', 'rear_openings', 'rear_floor_opening', 'insert_bosses', 'hidden_joint'):
            if type(v) is not bool:
                raise ValueError('Rear support must be true or false.')
        elif key == 'feet_style':
            if v not in FEET_STYLES: raise ValueError('Feet must be pockets or grooves.')
        elif key == 'sleeve_top':
            if isinstance(v, bool): raise ValueError('Top play must be a number.')
            v = num(v, 'Top play', SLEEVE_TOP_DEFAULT, SLEEVE_TOP_MAX)
        elif key in ('front_position','bezel'):
            if v not in (port_openings.FRONT_POSITIONS if key=='front_position' else port_openings.BEZELS):
                raise ValueError('Invalid '+key+'.')
        elif key in ('front_setback','bezel_size'):
            if isinstance(v,bool):raise ValueError('Invalid '+key+'.')
            v=num(v,key,0 if key=='front_setback' else .5,100 if key=='front_setback' else 1.5)
        elif key == 'rear_style':
            if v not in REAR_STYLES:
                raise ValueError('Invalid rear bracket style.')
        elif key in ('device_mount', 'joint'):
            if not isinstance(v, str) or len(v) > 20:
                raise ValueError('Invalid tray setting: ' + key + '.')
        elif type(v) not in (int, float) or isinstance(v, bool) or not math.isfinite(v):
            raise ValueError('Invalid tray setting: ' + key + '.')
        out[key] = v
    if out.get('rear_support') is False:
        out.pop('rear_style', None)
    return out


# Reserved built-in identity: no library write or device is needed for a panel.
FACEPLATE_ID = 'eq-000000000038'
FACEPLATE_PITCH_CAP = 48.0


def faceplate_item():
    return {'id': FACEPLATE_ID, 'name': 'Faceplate only', 'span': 1,
            'spec': {'faceplate_only': True, 'u': 1, 'ports': [], 'keystones': []},
            'parts': ['faceplate'], 'status': 'PROPOSED — UNVALIDATED'}


def faceplate_spacing(count, rows, u):
    if any(type(v) is not int for v in (count, rows, u)) or not 1 <= u <= 5 or not 1 <= rows <= u:
        raise ValueError('Choose 1–5U and between 1 and U rows.')
    if not 1 <= count <= 10:
        raise ValueError('Maximum 10 keystones per row (minimum 1).')
    pitch = min(FACEPLATE_PITCH_CAP, 193.5 / (count - 1)) if count > 1 else 0
    return [[round((i-(count-1)/2)*pitch, 3), round((r+.5)*44.45, 3)]
            for r in range(rows) for i in range(count)]


def faceplate_check(s):
    boxes = [(x-10.5, x+10.5, z-15, z+18.5) for x,z in s['keystones']]
    ports = [(p['x']-p['w']/2,p['x']+p['w']/2,p['z']-p['h']/2,p['z']+p['h']/2) for p in s['ports']]
    slots = [(x-5,x+5,i*44.45+22.225+dz-3.5,i*44.45+22.225+dz+3.5)
             for i in range(s['u']) for x in (-118.2625,118.2625) for dz in (-15.902,15.902)]
    gap = lambda a,b: max(a[0]-b[1],b[0]-a[1],a[2]-b[3],b[2]-a[3])
    def inside(x,z):
        dx=max(abs(x)-123.5,0);dz=max(2.525-z,z-(s['u']*44.45-2.525),0)
        return dx*dx+dz*dz <= 1.5*1.5+1e-9
    thin = False
    shapes = boxes + ports
    for i,a in enumerate(shapes):
        if not all(inside(x,z) for x in (a[0],a[1]) for z in (a[2],a[3])):
            raise ValueError('Keep every opening/block at least 1 mm inside the plate outline.')
        if any(gap(a,b) <= 0 for b in slots):
            raise ValueError('An opening/block overlaps a rack slot.')
        for b in shapes[:i]:
            g = gap(a,b)
            if g < 0: raise ValueError('Openings/keystone blocks overlap (negative web).')
            if g < 2: thin = True
    return ['thin wall, fit/strength UNKNOWN'] if thin else []


def clean_faceplate(spec):
    u = spec.get('u', 1)
    if type(u) is not int or not 1 <= u <= 5: raise ValueError('Choose a height from 1U to 5U.')
    layout = spec.get('layout', 'blank')
    if layout not in ('blank','keystones','custom'): raise ValueError('Choose Blank, Keystones or Custom openings.')
    s = dict(name='Faceplate only', faceplate_only=True, layout=layout, u=u,
             dev_w=5.0, dev_d=5.0, dev_h=1.0, hole_d=2.7, standoff=0.0, insert_pilot=3.2,
             board_t=1.6, device_mount='straps', joint='none', rear_support=False,
             coupon=[], holes=[], ports=[], rear_ports=[], keystones=[])
    q=spec.get('quality',DEFAULT_QUALITY)
    if q not in EXPORT_QUALITY: raise ValueError('Invalid export quality.')
    if q != DEFAULT_QUALITY:s['quality']=q
    if layout=='keystones':
        count,rows=spec.get('count',1),spec.get('rows',u)
        positions=faceplate_spacing(count,rows,u)
        raw=spec.get('keystones',positions)
        if not isinstance(raw,list) or len(raw)!=count*rows: raise ValueError('Keystone positions must match count × rows.')
        s.update(count=count,rows=rows)
        for point in raw:
            if isinstance(point,(int,float)) and not isinstance(point,bool): point=[point,u*44.45/2]
            if not isinstance(point,list) or len(point) not in (1,2): raise ValueError('Each keystone needs X or [X,Z].')
            s['keystones'].append([num(point[0],'Keystone X',-125,125),num(point[1] if len(point)>1 else u*44.45/2,'Keystone Z',0,u*44.45)])
    if layout=='custom':
        raw=spec.get('ports',[])
        if not isinstance(raw,list) or len(raw)>20: raise ValueError('Maximum 20 custom openings.')
        for i,p in enumerate(raw):
            if not isinstance(p,dict): raise ValueError('Each opening needs X, Z, width and height.')
            s['ports'].append(dict(x=num(p.get('x'),'Opening X',-125,125),z=num(p.get('z'),'Opening Z',0,u*44.45),
                w=num(p.get('w'),'Opening width',1,200),h=num(p.get('h'),'Opening height',1,220),
                r=num(p.get('r',0),'Corner radius',0,50),label=str(p.get('label') or 'Opening '+str(i+1))[:30],
                type=cable_ports.port_type(p.get('type')),id='front-'+str(i+1)))
    faceplate_check(s)
    return s


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
    if ident == FACEPLATE_ID:
        if payload.get('second') is not None: raise ValueError('A faceplate-only slot has no devices.')
        settings = placement_settings(payload.get('tray'))
        return clean_faceplate(dict(settings.get('faceplate',{}), **({'quality':payload['quality']} if 'quality' in payload else {})))
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
    # Optional second device on the same tray: {'item': library id, 'tray': its own SECOND_KEYS}.
    second = payload.get('second')
    if second is not None:
        other = next((i for i in library(data_dir) if i.get('id') == second.get('item')), None) if isinstance(second, dict) else None
        if other is None:
            raise ValueError('The second device is no longer in the library.')
        spec['second'] = allocation_spec(other['spec'], second_settings(second.get('tray')))
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
    return {'ok': True, 'u': s['u'], **({'warnings':faceplate_check(s)} if s.get('faceplate_only') else {})}


RACK_PITCH, PLATE_GAP, LEGACY_SLOT_OFFSET = port_openings.RACK_PITCH, port_openings.PLATE_GAP, port_openings.LEGACY_SLOT_OFFSET

RACK_INNER_W, SIDE_CLEAR = 208, 2  # PROPOSED nominal opening and clearance per side
MAX_TRAY = RACK_INNER_W - 2 * SIDE_CLEAR
FRONT_GAP, MARGIN = 12, 8  # mirror front_gap / margin in equipment_tray.scad



WALL_SIDES = ('front', 'rear', 'left', 'right')
WALL_MESSAGE = 'The wall would hit the faceplate joint; set the device back or move it sideways.'

def wall_open(value):
    if not isinstance(value, list) or not value or any(not isinstance(x, str) or x not in WALL_SIDES for x in value) or len(set(value)) == 4:
        raise ValueError('Open sides must name Front, Rear, Left or Right; leave at least one open and one closed.')
    return [x for x in WALL_SIDES if x in value]

def wall_rectangles(s):
    """Actual wall boxes [x0,y0,x1,y1,height], including returns and finger notches."""
    if s.get('device_mount') != 'wall': return []
    w,d,h = s['dev_w'],s['dev_d'],min(12,s['dev_h']-2)
    result=[]
    for side in WALL_SIDES:
        horizontal=side in ('front','rear'); length=w if horizontal else d
        opened=side in s.get('wall_open',['rear'])
        if opened and length<30: continue
        spans=[(-2.5,9.5,h),(length-9.5,length+2.5,h)] if opened else ([(-2.5,length/2-10,h),(length/2-10,length/2+10,min(4,h)),(length/2+10,length+2.5,h)] if not horizontal and length>=40 else [(-2.5,length+2.5,h)])
        cross=(-2.5,-.5) if side in ('front','left') else ((d+.5,d+2.5) if horizontal else (w+.5,w+2.5))
        for a,b,z in spans:
            q=[a,cross[0],b,cross[1]] if horizontal else [cross[0],a,cross[1],b]
            pts=[]
            for x,y in ((q[0],q[1]),(q[2],q[3])):
                rot=s.get('dev_rot',0)
                p=(d-y,x) if rot==90 else (w-x,d-y) if rot==180 else (y,w-x) if rot==270 else (x,y)
                pts.append(p)
            fx,_,fy,_=footprint(s)
            result.append([fx+min(p[0] for p in pts),fy+min(p[1] for p in pts),fx+max(p[0] for p in pts),fy+max(p[1] for p in pts),z])
    return result

def validate_wall(s, joints=None):
    if s.get('device_mount') != 'wall': return
    if s['dev_h'] <= 2: raise ValueError('A wall needs a device taller than 2 mm.')
    if joints is None:
        half=tray_width(s)/2
        joints=s.get('joint_x',[-min(40,half-12),min(40,half-12)])
    for x0,y0,x1,y1,h in wall_rectangles(s):
        if y0 < 0 or (s['joint']=='screw' and any(x0<x+9 and x1>x-9 and ((y0<11.3 and y1>0) or (y0<22 and y1>9 and any(x0<x+side*6+1 and x1>x+side*6-1 for side in (-1,1)))) for x in joints)):
            raise ValueError(WALL_MESSAGE)


def floor_z(spec):
    return 0.5 if spec.get('device_mount') in ('flat', 'sleeve') else 7 + LEGACY_SLOT_OFFSET


def device_lift(spec):
    feet = port_openings.foot_height(spec)
    return floor_z(spec) + 3 + (0 if spec.get('device_mount') in ('straps', 'wall', 'flat', 'sleeve') else float(spec.get('standoff', 6))) - feet  # case on the floor top; feet hang in their pockets


def needed_height(spec):
    mount = spec.get('device_mount')
    extra = (float(spec.get('board_t', 1.6)) + (1.6 if mount == 'pegs' else 2.5)) if mount in ('pegs', 'clips') else 0
    ride = SL_RIDE if spec.get('feet_style') == 'grooves' else 0
    return max(device_lift(spec) + max(float(spec['dev_h']), extra) + ride,
               floor_z(spec) + 22 if spec.get('joint', 'screw') == 'screw' else 0)


def foot_pockets(spec):
    """Pocket rectangles in tray coordinates, following the SCAD dp() rotation."""
    if spec.get('device_mount') not in ('flat', 'sleeve') or not spec.get('feet'):
        return []
    turned = spec.get('dev_rot', 0) in (90, 270)
    fw, fd = (spec['dev_d'], spec['dev_w']) if turned else (spec['dev_w'], spec['dev_d'])
    dx = -fw/2 + float(spec.get('dev_off_x', 0))
    dy = port_openings.device_y(spec)
    def dp(x, y):
        if spec.get('dev_rot') == 90: return spec['dev_d']-y, x
        if spec.get('dev_rot') == 180: return spec['dev_w']-x, spec['dev_d']-y
        if spec.get('dev_rot') == 270: return y, spec['dev_w']-x
        return x, y
    out=[]
    for f in spec['feet']:
        pts=[dp(f['x'],f['y']),dp(f['x']+f['w'],f['y']),dp(f['x'],f['y']+f['d']),dp(f['x']+f['w'],f['y']+f['d'])]
        x0=dx+min(p[0] for p in pts)-port_openings.FOOT_CLEARANCE;x1=dx+max(p[0] for p in pts)+port_openings.FOOT_CLEARANCE
        y0=dy+min(p[1] for p in pts)-port_openings.FOOT_CLEARANCE;y1=dy+max(p[1] for p in pts)+port_openings.FOOT_CLEARANCE
        out.append({'x0':x0,'x1':x1,'y0':y0,'y1':y1,'depth':f['h']+port_openings.FOOT_EXTRA_DEPTH,'through':f['h']+port_openings.FOOT_EXTRA_DEPTH > 3-port_openings.FOOT_MIN_FLOOR})
    return out


# Sleeve v2 is opt-in. These dimensions are design choices, not physical approval.
SLEEVE_TOP_DEFAULT, SLEEVE_TOP_MAX, SL_RIDE = .3, 2, .5
FEET_STYLES = ('pockets', 'grooves')
TRAY_T, SLOT_BOTTOM, GROOVE_ATTACH, CUT_EPS, FOOT_HEIGHT_TOL = 3, 0, .8, .1, .001
PILOT_RADIUS, INSERT_INSIDE, INSERT_OUTSIDE, INSERT_BOSS_DEPTH = 2, 2, 3, 12
BOSS_FACETS = 48
INSERT_BOSS_R = (PILOT_RADIUS+INSERT_OUTSIDE)/math.cos(math.pi/BOSS_FACETS)
FLOOR_OPEN_W, FLOOR_OPEN_D, FLOOR_OPEN_R, FLOOR_OPEN_MIN = 60, 30, 2, 10
FLOOR_STOP_CLEAR, FLOOR_JOINT_CLEAR, FLOOR_WALL_CLEAR = 4, 3, 5
REAR_FLOOR_JOINT_REACH = 11.3
V2_DEFAULTS = dict(sleeve_top=.3, feet_style='pockets', rear_floor_opening=False, insert_bosses=False, hidden_joint=False)
SLEEVE_HEADER = '// PROPOSED sleeve defaults (mm); independent design, fit and strength UNKNOWN.\n'
# The v2 parameters sit before their first use: OpenSCAD evaluates a variable where it is first assigned.
V2_PARAMS = (
    '// Sleeve v2 options (task 36): defined before first use, because OpenSCAD evaluates a variable where it is first assigned.\n'
    'sleeve_top=0.3; feet_style="pockets"; rear_floor_opening=false; insert_bosses=false;\n'
    'sl_ride=0.5; sl_pilot_inside=2; sl_pilot_radius=2; sl_boss_outside=3; sl_boss_depth=12;\n'
    'sl_pilot_offset=sl_pilot_inside+sl_pilot_radius; sl_boss_fn=48; sl_boss_r=(sl_pilot_radius+sl_boss_outside)/cos(180/sl_boss_fn);\n'
    'foot_tracks=[]; foot_dips=[]; floor_cable_box=[];\n'
    'groove_attach=0.8; v2_eps=0.1; v2_tol=0.000000001; floor_cable_r=2; slot_bottom=0;\n'
    'floor_cable_min=10; floor_stop_clear=4; floor_joint_clear=3; floor_wall_clear=5; rear_floor_joint_half=9; rear_floor_joint_reach=11.3;\n'
)
V2_REPLACEMENTS = {
    SLEEVE_HEADER: SLEEVE_HEADER+V2_PARAMS,
    'sl_top=0.3;': 'sl_top=sleeve_top+(feet_style=="grooves"?sl_ride:0);',
    'max(margin,sl_side+sl_wall)': 'max(margin,sl_side+sl_wall,insert_bosses?sl_side+sl_pilot_offset+sl_boss_r:0)',
    'sl_joints=[dev_off_x-sl_half-sl_wall/2,dev_off_x+sl_half+sl_wall/2];':
        'sl_joints=[dev_off_x-sl_half-(insert_bosses?sl_pilot_offset:sl_wall/2),dev_off_x+sl_half+(insert_bosses?sl_pilot_offset:sl_wall/2)];',
    'module device_features_add(){': 'module device_features_add(){\n sleeve_v2_add();',
    'module device_features_cut(){': 'module device_features_cut(){\n sleeve_v2_cut();',
    'if(foot_h>0&&(device_mount=="flat"||sleeve))for(f=feet)':
        'if(feet_style!="grooves"&&foot_h>0&&(device_mount=="flat"||sleeve))for(f=feet)',
}

# Hidden faceplate joint (Brian, 2026-10-22, task 41): opt-in; the sleeve's faceplate screws leave the plate front and
# the proven tongue/boss/upright joint moves outside the sleeve walls. Pairs are (without, with): specs without
# hidden_joint get the "without" text, so their generated sources stay byte-identical. Fit/strength UNKNOWN.
HJ_REPLACEMENTS = (
    ('rear_floor_joint_half=9; rear_floor_joint_reach=11.3;\n',
     'rear_floor_joint_half=9; rear_floor_joint_reach=11.3;\nhidden_joint=false; hj_gap=2; hj_half=9;\n'),
    ('insert_bosses?sl_side+sl_pilot_offset+sl_boss_r:0)',
     'insert_bosses?sl_side+sl_pilot_offset+sl_boss_r:0,hidden_joint?sl_side+sl_wall+hj_gap+2*hj_half:0)'),
    ('sl_joint_z=[sl_bottom+3,sl_window_top-3];',
     'sl_joint_z=[sl_bottom+3,sl_window_top-3];\n'
     'hj_x=[dev_off_x-sl_half-sl_wall-hj_gap-hj_half,dev_off_x+sl_half+sl_wall+hj_gap+hj_half];  // hidden joint centres (outside the sleeve walls)\n'
     'function jon(r)=joint=="screw"&&(!sleeve||r||hidden_joint);  // is the tongue/boss joint built here?\n'
     'function jxs(r)=(hidden_joint&&!r)?hj_x:joint_x;  // front joint X (the rear bracket keeps joint_x)'),
    ('if(joint=="screw"&&(!sleeve||rear)){\n  for(x=joint_x)translate([x-tongue_w/2', 'if(jon(rear)){\n  for(x=jxs(rear))translate([x-tongue_w/2'),
    ('  for(x=joint_x)translate([x,0,tray_z+14])rotate([-90,0,0])cylinder(d=boss_d', '  for(x=jxs(rear))translate([x,0,tray_z+14])rotate([-90,0,0])cylinder(d=boss_d'),
    ('module plate_joint_cut(rear=false){if(joint=="screw"&&(!sleeve||rear))for(x=joint_x)translate', 'module plate_joint_cut(rear=false){if(jon(rear))for(x=jxs(rear))translate'),
    ('if(sleeve&&joint=="screw")for(x=sl_joints,z=sl_joint_z)', 'if(sleeve&&joint=="screw"&&!hidden_joint)for(x=sl_joints,z=sl_joint_z)'),
    ('if(joint=="screw"&&(!sleeve||rear)){\n  for(x=joint_x) translate([x-9,0,tray_z+tray_t])cube([18,8,5]);\n  for(x=joint_x)translate([x-7,8.3,tray_z+3])cube([14,3,19]);\n  for(x=joint_x) for(side=[-1,1])',
     'if(jon(rear)){\n  for(x=jxs(rear)) translate([x-9,0,tray_z+tray_t])cube([18,8,5]);\n  for(x=jxs(rear))translate([x-7,8.3,tray_z+3])cube([14,3,19]);\n  for(x=jxs(rear)) for(side=[-1,1])'),
    ('if(joint=="screw"&&(!sleeve||rear)){\n  for(x=joint_x)translate([x-(tongue_w+slot_clear)/2', 'if(jon(rear)){\n  for(x=jxs(rear))translate([x-(tongue_w+slot_clear)/2'),
    ('  for(x=joint_x)translate([x,11.4,tray_z+14])', '  for(x=jxs(rear))translate([x,11.4,tray_z+14])'),
    ('// @sleeve-v2-end\n',
     '// @sleeve-v2-end\n'
     'assert(!hidden_joint||(sleeve&&joint=="screw"&&!insert_bosses),"Hidden joint needs a sleeve with a screw joint and no insert bosses");\n'
     'assert(!hidden_joint||max([for(x=hj_x)abs(x)])+hj_half<=118.2625-5-3,"Hidden joint must keep 3 mm from the rack slots");\n'),
)


def window_spec(spec):
    """Adapt the shared opening planner without changing its legacy API or sources."""
    if spec.get('device_mount') != 'sleeve': return spec
    extra = spec.get('sleeve_top', SLEEVE_TOP_DEFAULT)-SLEEVE_TOP_DEFAULT
    if spec.get('feet_style') == 'grooves': extra += SL_RIDE
    return dict(spec, dev_h=spec['dev_h']+extra) if extra else spec


def sleeve_geometry(spec):
    win = port_openings.sleeve(window_spec(spec))
    if win and spec.get('insert_bosses'):
        reach = win['half']+INSERT_INSIDE+PILOT_RADIUS
        win['joints'] = [win['x']-reach, win['x']+reach]
        win['outside'] = 2*(reach+INSERT_BOSS_R)
    return win


def tray_width(spec):
    fw = spec['dev_d'] if spec.get('dev_rot') in (90, 270) else spec['dev_w']
    win = sleeve_geometry(spec)
    half = fw/2 + (max(MARGIN, port_openings.SLEEVE_SIDE+port_openings.SLEEVE_WALL) if win else MARGIN)
    if win and (spec.get('insert_bosses') or win.get('hidden')): half = max(half, win['outside']/2)
    return 2*(abs(spec.get('dev_off_x', 0))+half)


def foot_grooves(spec):
    if spec.get('feet_style') != 'grooves': return []
    pockets = foot_pockets(spec)
    tracks = []
    for p in sorted(pockets, key=lambda q:q['x0']):
        if tracks and p['x0'] <= tracks[-1]['x1']:
            tracks[-1]['x1'] = max(tracks[-1]['x1'], p['x1'])
            tracks[-1]['dips'].append(p)
        else: tracks.append(dict(x0=p['x0'], x1=p['x1'], dips=[p]))
    top = floor_z(spec)+TRAY_T
    for t in tracks:
        heights = [p['depth']-port_openings.FOOT_EXTRA_DEPTH for p in t['dips']]
        if max(heights)-min(heights) > FOOT_HEIGHT_TOL:
            raise ValueError('Feet sharing a groove must have the same height.')
        depth = max(heights)-SL_RIDE
        if depth <= 0: raise ValueError('Feet must be taller than the 0.5 mm groove ride lift.')
        bottom = top-depth
        if bottom-SLOT_BOTTOM < port_openings.FOOT_MIN_FLOOR-1e-9:
            raise ValueError('Feet are too tall for grooves: cannot keep 0.8 mm of floor above the slot bottom.')
        for p in t['dips']:
            p['cut_depth'] = top-SLOT_BOTTOM+CUT_EPS if p['through'] else p['depth']
            p['ramp'] = p['cut_depth']-depth  # rise/run = 1:1, 45 degrees
        ramp = max(p['ramp'] for p in t['dips'])
        t.update(y0=port_openings.device_y(spec), y1=max(p['y1'] for p in t['dips'])+ramp,
                 depth=depth, bottom=bottom, floor_bottom=SLOT_BOTTOM if bottom-floor_z(spec)<port_openings.FOOT_MIN_FLOOR else floor_z(spec), ramp=ramp)
    return tracks


def rear_floor_geometry(spec):
    if not spec.get('rear_floor_opening'): return None
    fw, fd = (spec['dev_d'], spec['dev_w']) if spec.get('dev_rot') in (90,270) else (spec['dev_w'], spec['dev_d'])
    win = sleeve_geometry(spec)
    stop_end = port_openings.device_y(spec)+fd+(port_openings.SLEEVE_STOP_T if win else 6.2 if spec['device_mount']=='flat' else 0)
    width = tray_width(spec)
    jx = min(40, width/2-12)
    # Central rectangle clears both conservative rear tongue/upright/boss envelopes.
    joints = spec.get('joint_x', [-jx, jx])
    half = min(FLOOR_OPEN_W/2, min(abs(x) for x in joints)-REAR_JOINT_HALF-FLOOR_JOINT_CLEAR,
               (win['half']-abs(win['x']) if win else width/2)-FLOOR_WALL_CLEAR)
    y0 = stop_end+FLOOR_STOP_CLEAR
    y1 = min(y0+FLOOR_OPEN_D, 240-REAR_FLOOR_JOINT_REACH-FLOOR_JOINT_CLEAR)
    opening = dict(x0=-half,x1=half,y0=y0,y1=y1,r=FLOOR_OPEN_R)
    if 2*half < FLOOR_OPEN_MIN or y1-y0 < FLOOR_OPEN_MIN:
        raise ValueError('Not enough floor behind the device for the cable opening and its clearances.')
    dx = -fw/2+spec.get('dev_off_x',0); dy=port_openings.device_y(spec)
    obstacles = foot_grooves(spec) if spec.get('feet_style')=='grooves' else foot_pockets(spec)
    obstacles += [dict(x0=x,x1=x+3,y0=y-6,y1=y+6) for x in (dx-5.5,dx+fw+2.5) for y in (dy+fd*.25,dy+fd*.75)]
    if any(_rect_overlap(opening,p) for p in obstacles):
        raise ValueError('Cable opening would overlap a strap slot or foot groove/pocket.')
    return opening


def _rect_overlap(a,b):
    return a['x0']<b['x1'] and a['x1']>b['x0'] and a['y0']<b['y1'] and a['y1']>b['y0']


def validate_foot_pockets(spec, tray_w):
    pockets=foot_pockets(spec)
    if not pockets:return
    fp_w,fp_d=(spec['dev_d'],spec['dev_w']) if spec.get('dev_rot',0) in (90,270) else (spec['dev_w'],spec['dev_d'])
    dev_x=-fp_w/2+float(spec.get('dev_off_x',0));dev_y=port_openings.device_y(spec)
    def overlap(p,x0,x1,y0,y1):return p['x0']<x1 and p['x1']>x0 and p['y0']<y1 and p['y1']>y0
    if spec.get('feet_style') == 'grooves':
        tracks = foot_grooves(spec)
        # Include the ramp tails in all interference checks. The sleeve front floor strip
        # is intentionally grooved; the front screw joints are in the sleeve walls.
        pockets = [dict(p, y0=p['y0']-p['ramp'], y1=p['y1']+p['ramp']) for t in tracks for p in t['dips']] + tracks
    if spec.get('joint','screw')=='screw':
        jx=min(40,tray_w/2-12)
        if not (spec.get('feet_style')=='grooves' and spec.get('device_mount')=='sleeve') and any(overlap(p,x-9,x+9,0,11.3) for p in pockets for x in (-jx,jx)):
            raise ValueError('A foot pocket would cut into a tray screw joint; move or remove that foot.')
        if spec.get('rear_support') and any(overlap(p,x-9,x+9,240-11.3,240) for p in pockets for x in (-jx,jx)):
            raise ValueError('A foot pocket would cut into a rear screw joint; move or remove that foot.')
    for p in pockets:
        for x in (dev_x-5.5,dev_x+fp_w+2.5):
            for y in (dev_y+fp_d*.25,dev_y+fp_d*.75):
                if overlap(p,x,x+3,y-6,y+6):raise ValueError('A foot pocket would cut into a strap slot; move or remove that foot.')
        if spec.get('device_mount')=='sleeve':
            win=port_openings.sleeve(spec);left=win['x']-win['half'];right=win['x']+win['half'];wall=port_openings.SLEEVE_WALL
            if overlap(p,left-wall,left,0,dev_y+fp_d) or overlap(p,right,right+wall,0,dev_y+fp_d):raise ValueError('A foot pocket would cut into a sleeve wall; move or remove that foot.')
            if overlap(p,dev_x,dev_x+fp_w,dev_y+fp_d,dev_y+fp_d+port_openings.SLEEVE_STOP_T):raise ValueError('A foot pocket would cut into the sleeve rear stop; move or remove that foot.')
            if spec.get('feet_style')!='grooves' and overlap(p,left,right,0,8):raise ValueError('A foot pocket would cut into the floor strip under the sleeve window; move or remove that foot.')


# PROPOSED rear bracket dimensions (mm). Physical stiffness/airflow/strength UNKNOWN.
REAR_STYLES = ('solid', 'open', 'reinforced', 'slots', 'vents')
REAR_MARGIN = 6
REAR_BAND = 5
REAR_STRIP = 6
REAR_LIMIT = 96
REAR_MIN = 10
REAR_LIP_T = 2.5
REAR_LIP_DEPTH = 8
REAR_LIP_LIMIT = 100
REAR_EDGE_INSET = 0.5
REAR_VENT_D = 6.5
REAR_VENT_BAR = 2.0
REAR_VENT_PITCH = REAR_VENT_D + REAR_VENT_BAR
REAR_VENT_ROW = REAR_VENT_PITCH * math.sqrt(3)/2
REAR_LIP_CLEAR = 0.5
REAR_JOINT_HALF = 9
REAR_JOINT_TOP = 22
REAR_RETENTION_REACH = {"flat": 6.2, "sleeve": 4, "clips": 1}


def rear_style(spec):
    return spec.get('rear_style', 'open' if spec.get('rear_openings') else 'solid') if spec.get('rear_support') else 'solid'


def keep_clear_boxes(s):
    """Rotate device-local AABBs into rack coordinates; no tray geometry changes."""
    w,d=s['dev_w'],s['dev_d'];rot=s.get('dev_rot',0)
    fw,fd=(d,w) if rot in (90,270) else (w,d)
    dx=-fw/2+s.get('dev_off_x',0);dy=port_openings.device_y(s)
    def point(x,y):
        return (d-y,x) if rot==90 else (w-x,d-y) if rot==180 else (y,w-x) if rot==270 else (x,y)
    out=[]
    for p in s.get('protrusions',[]):
        pts=[point(x,y) for x in (p['x'],p['x']+p['w']) for y in (p['y'],p['y']+p['d'])]
        out.append(dict(x0=dx+min(q[0] for q in pts),x1=dx+max(q[0] for q in pts),y0=dy+min(q[1] for q in pts),y1=dy+max(q[1] for q in pts),z0=device_lift(s)+p['z'],z1=device_lift(s)+p['z']+p['h']))
    return out


def keep_clear_openings(s):
    # Bracket occupies assembled Y=240..244. Full rectangles, never clipped to pretend clearance.
    return [[p['x0']-.5,p['x1']+.5,p['z0']-.5,p['z1']+.5] for p in keep_clear_boxes(s)
            if s.get('rear_support') and p['y0']<244 and p['y1']>=240]


def rear_geometry(s):
    """Analytical cut bounds and lip boxes used directly by the SCAD source; no rendering."""
    style = rear_style(s)
    # Keep-clear zones stay plain rectangles (keep_clear_cut); the rounded style windows would over-cut small ones.
    result = dict(windows=[], holes=[], flanges=[], keep_clear=keep_clear_openings(s))
    if style == 'solid':
        return result
    legacy = style == 'open'
    margin, band, strip, limit = (4, 3.5, 4, 100.2625) if legacy else (REAR_MARGIN, REAR_BAND, REAR_STRIP, REAR_LIMIT)
    floor = .5 if s['device_mount'] in ('flat', 'sleeve') else 8.225
    width = s['dev_d'] if s.get('dev_rot') in (90, 270) else s['dev_w']
    jx = min(40, (pair_tray_half(s) if s.get('second') else abs(s.get('dev_off_x', 0)) + width/2 + 8) - 12)
    left, right = min(s.get('joint_x', [-jx, jx])), max(s.get('joint_x', [-jx, jx]))
    half = 6 + margin
    top = floor + 18.5 + margin
    height = s['u'] * 44.45 - .025
    regions = []
    for i in range(s['u']):
        lo = max(.025, i*44.45) + band
        hi = min(height, (i+1)*44.45) - band
        upper = i*44.45 + top
        split = min(i*44.45+22.225, upper-strip)
        candidates = [[-limit,limit,max(lo,upper),hi], [-limit,left-half,lo,split],
                      [left+half,right-half,lo,split], [right+half,limit,lo,split]]
        if not legacy:
            candidates = [[max(-limit,a),min(limit,b),c,d] for a,b,c,d in candidates]
        valid = [q for q in candidates if q[1]-q[0] >= REAR_MIN and q[3]-q[2] >= REAR_MIN]
        if style in ('open', 'reinforced'):
            result['windows'].extend(valid)
        elif style == 'slots':
            result['windows'].extend(q for q in valid if q == candidates[0] or q == candidates[2])
        else:
            centre = candidates[2]
            if centre in valid:
                result['windows'].append(centre)
            # Use conservative rectangular safe regions; even a complete circle must fit.
            regions.extend(q for q in candidates if q != centre and q[1] > q[0] and q[3] > q[2])
    if style == 'vents':
        radius = REAR_VENT_D/2
        def pack(a,b,c,d):
            rows = math.floor((d-c-REAR_VENT_D)/REAR_VENT_ROW)+1
            if rows <= 0 or b-a < REAR_VENT_D:
                return []
            holes = []
            z0 = (c+d-(rows-1)*REAR_VENT_ROW)/2
            for row in range(rows):
                offset = (row % 2)*REAR_VENT_PITCH/2
                count = math.floor((b-a-REAR_VENT_D-offset)/REAR_VENT_PITCH)+1
                for col in range(max(0,count)):
                    holes.append([a+radius+offset+col*REAR_VENT_PITCH,z0+row*REAR_VENT_ROW])
            return holes
        for a,b,c,d in regions:
            normal = pack(a,b,c,d)
            rotated = [[z,x] for x,z in pack(c,d,a,b)]
            result['holes'].extend(rotated if len(rotated)>len(normal) else normal)
    if style in ('reinforced', 'vents'):
        # Local +Y maps to the tray side, assembled Y 232..240.
        b = height-REAR_EDGE_INSET
        t, depth, edge = REAR_LIP_T, REAR_LIP_DEPTH, REAR_LIP_LIMIT
        clear_depth = min(240-(port_openings.device_y(d)+(d['dev_w'] if d.get('dev_rot') in (90,270) else d['dev_d']))
                          -REAR_RETENTION_REACH.get(d['device_mount'],0)-REAR_LIP_CLEAR for d in tray_devices(s))
        if clear_depth < depth:
            depth = max(0,clear_depth)
            result.setdefault('notes', []).append('Lip depth shortened to clear the device and rear retention envelope by 0.5 mm.')
        result['flanges'] = [[-edge,0,b-t,2*edge,depth,t]] if depth > 0 else []
        for x in (-edge,edge-t):
            bottom = floor+3+REAR_LIP_CLEAR
            # Conservative full joint envelope includes the upright at Y 8.3:
            # its 0.3 gap to an 8 mm lip is too small, so lift that end lip.
            if s['joint'] == 'screw' and any(
                    x < j+REAR_JOINT_HALF+REAR_LIP_CLEAR and
                    x+t > j-REAR_JOINT_HALF-REAR_LIP_CLEAR
                    for j in s.get('joint_x', [-jx,jx])):
                bottom = floor+REAR_JOINT_TOP+REAR_LIP_CLEAR
                result.setdefault('notes', []).append('End lip shortened above the rear joint for 0.5 mm clearance.')
            if bottom < b-t and depth > 0:
                result['flanges'].append([x,0,bottom,t,depth,b-t-bottom])
            else:
                result.setdefault('notes', []).append('End lip omitted: no clear height below the top lip.')
    return result


def keep_clear_bands(s):
    """Nominal 2D gaps at each cut, not a stiffness/strength assessment.

    Rounded windows/capsules/circles use core rectangles plus a radius. Merged
    cutouts have no intervening band and are named separately; measure the
    smallest remaining positive gap to other cuts. Edges and joint collisions
    count as zero. Do not change geometry or saved specs.
    """
    geometry = rear_geometry(s)
    cuts = geometry['keep_clear']
    if not cuts:
        return []
    style = rear_style(s)
    height = s['u']*44.45-.025
    floor = .5 if s['device_mount'] in ('flat', 'sleeve') else 8.225
    width = s['dev_d'] if s.get('dev_rot') in (90,270) else s['dev_w']
    jx = min(40,abs(s.get('dev_off_x',0))+width/2+8-12)
    joints = s.get('joint_x',[-jx,jx]) if s['joint']=='screw' else []
    def gap(q, core, radius=0):
        return max(0,math.hypot(max(core[0]-q[1],q[0]-core[1],0),
                                max(core[2]-q[3],q[2]-core[3],0))-radius)
    obstacles = []
    for a,b,c,d in geometry['windows']:
        obstacles.append(('style window',[a+2,b-2,c+2,d-2],2))
    for x,z in geometry['holes']:
        obstacles.append(('vent hole',[x,x,z,z],REAR_VENT_D/2))
    for i in range(s['u']):
        for x in (-118.2625,118.2625):
            for dz in (-15.902,15.902):
                z=i*44.45+22.225+dz
                obstacles.append(('rack slot',[x-1.5,x+1.5,z,z],3.5))
    out=[]
    for i,q in enumerate(cuts):
        # Rounded outer plate: minimum at a corner of the rectangular cut.
        edge=min(q[0]+126,126-q[1],q[2]-.025,height-q[3])
        for x in (q[0],q[1]):
            for z in (q[2],q[3]):
                dx=max(abs(x)-123.5,0); dz=max(2.525-z,z-(height-2.5),0)
                if dx>0 and dz>0:edge=min(edge,2.5-math.hypot(dx,dz))
        distances=[(max(0,edge),'plate edge')]; merged=[]; collisions=[]
        for name,core,radius in obstacles+[("keep-clear opening",p,0) for j,p in enumerate(cuts) if i!=j]:
            distance=gap(q,core,radius)
            if distance<=1e-9:merged.append(name)
            else:distances.append((distance,name))
        for x in joints:
            for name,radius in (('joint boss',4.5),('joint pilot',2)):
                distance=gap(q,[x,x,floor+14,floor+14],radius)
                distances.append((distance,name))
                if distance<=1e-9:collisions.append(name)
        distance,nearest=min(distances,key=lambda p:p[0])
        out.append(dict(opening=q,band=round(distance,6),nearest=nearest,
                        normal_band=3.5 if style=='open' else 5 if style!='solid' else None,
                        merged=sorted(set(merged)),collisions=sorted(set(collisions))))
    return out


KEYSTONE_Z_REPLACEMENTS = {'for(x=keystones)': 'for(k=keystones)let(x=is_list(k)?k[0]:k,kz=is_list(k)&&len(k)>1?k[1]:plate_center)', 'translate([x-ks_ow/2,-plate_t,plate_center])': 'translate([x-ks_ow/2,-plate_t,kz])', 'translate([x-ks_w/2,-plate_t,plate_center])': 'translate([x-ks_w/2,-plate_t,kz])', 'translate([x,0,plate_center])': 'translate([x,0,kz])', 'translate([x-10.5,-plate_t-1,plate_center-15])': 'translate([x-10.5,-plate_t-1,kz-15])', 'translate([x-10.5,-plate_t-0.01,plate_center-15])': 'translate([x-10.5,-plate_t-0.01,kz-15])'}


def template_source(spec):
    # New builds always use the current slot-bottom template; saved revisions remain immutable.
    text = TEMPLATE.read_text(encoding='utf-8')
    if not (spec.get('device_mount') == 'wall' or (spec.get('second') or {}).get('device_mount') == 'wall'):
        text = re.sub(r'// @wall-begin\n.*?// @wall-end\n\n', '', text, flags=re.S)
        text = text.replace('\n wall_add();', '')
    if not spec.get('drives'):
        text = re.sub(r'// @drives-begin\n.*?// @drives-end\n', '', text, flags=re.S)
        for old, new in DRIVE_REPLACEMENTS.items(): text = text.replace(new, old)
    if not spec.get('faceplate_only'):
        for old,new in KEYSTONE_Z_REPLACEMENTS.items(): text=text.replace(new,old)
    if not spec.get('hidden_joint'):
        for old, new in HJ_REPLACEMENTS: text = text.replace(new, old)
    if not any(k in spec for k in V2_DEFAULTS):
        text = text.split('// @sleeve-v2-begin\n')[0]
        for old, new in V2_REPLACEMENTS.items(): text = text.replace(new, old)
    style = rear_style(spec)
    if style not in ('reinforced', 'slots', 'vents'):
        text = re.sub(r'// @rear-styles-begin\n.*?// @rear-styles-end\n(?:\n)?', '', text, flags=re.S)
    else:
        text = text.replace('if(plain && rear_support && rear_openings)rear_windows2d();',
                            'if(plain && rear_support)rear_style_cuts();')
        text = text.replace('plate_joint_add(true);}', 'plate_joint_add(true);rear_style_flanges();}')
    if style in ('reinforced', 'slots', 'vents'):
        text = text.replace('// @rear-openings-begin\n  if(plain && rear_support)rear_style_cuts();\n// @rear-openings-end',
                            '  if(plain && rear_support)rear_style_cuts();')
    if style != 'open':
        text = re.sub(r'// @rear-openings-begin\n.*?// @rear-openings-end\n(?:\n)?', '', text, flags=re.S)
    cuts=keep_clear_openings(spec)
    if cuts:
        code='\n// User-confirmed keep-clear zones; real cable bend space UNKNOWN.\nmodule keep_clear_cut(){for(q='+json.dumps(cuts)+')translate([q[0],-4.1,q[2]])cube([q[1]-q[0],12.2,q[3]-q[2]]); }\n'
        text=text.replace('plate_joint_cut(true);}}','plate_joint_cut(true);keep_clear_cut();}}')+code
    if spec.get('front_position','today')!='today':
        y=port_openings.device_y(spec)
        text=text.replace('dev_y=sleeve?-plate_t:front_gap+dev_off_y;', 'dev_y='+json.dumps(y)+';')
        if y<0 and spec['device_mount']!='sleeve':
            text=text.replace('assert(sleeve||dev_y>=0,','assert(true,')
        win=port_openings.front_window(spec)
        if win and spec['device_mount']!='sleeve':
            old='if(sleeve)translate([dev_off_x,(sl_bottom+sl_window_top)/2])square([2*sl_half,sl_window_top-sl_bottom],center=true);'
            text=text.replace(old,'translate(['+str(win['x'])+','+str((win['bottom']+win['top'])/2)+'])square(['+str(win['width'])+','+str(round(win['height'],3))+'],center=true);')
    if spec.get('bezel','none')!='none':
        plan=port_openings.bezel_plan(window_spec(spec))
        shapes=[[p['x'],p['z'],p['w'],p['h'],p['r'],p['size']] for p in plan['openings'] if p['size']>0]
        code='\n// Front-edge bezel only: ports and case window. 8 rounded steps; 2 mm web.\n'
        code+='bezel_shapes='+json.dumps(shapes)+';\nbezel_rounded='+('true' if spec['bezel']=='rounded' else 'false')+';\n'
        code+=BEZEL_SCAD
        code+='\n'+'\n'.join('// '+n for n in plan['notes'])+'\n'
        text=text.replace('   plate_joint_cut();','   plate_joint_cut();bezel_cuts();')+code
    if spec.get('labels'):
        text = text.replace('   if(ks_style=="v2")ks_cut(); else ks_box_cut();', '   if(ks_style=="v2")ks_cut(); else ks_box_cut();\n   label_cut();') + LABEL_SCAD
    if spec.get('second'):
        text = second_device_source(text)
    return text


LABEL_SCAD = r"""
// Engraved front-face text [text, x, z centre, size]; 0.6 mm deep. Printed legibility UNKNOWN.
labels=[]; label_depth=0.6;
module label_cut(){for(l=labels)translate([l[1],-plate_t-0.1,l[2]])rotate([90,0,0])mirror([0,0,1])linear_extrude(height=label_depth+0.1)text(l[0],size=l[3],font="Liberation Sans:style=Bold",halign="center",valign="center");}
"""

BEZEL_SCAD = r"""
function bezel_out(b,t)=bezel_rounded?b-sqrt(max(0,b*b-(b-t)*(b-t))):b-t;
module bezel_slice(p,t){translate([p[0],-4+t,p[1]])rotate([90,0,0])linear_extrude(height=0.02)offset(delta=bezel_out(p[5],t))rrect(p[2],p[3],p[4]);}
module bezel_cuts(){for(p=bezel_shapes)let(n=bezel_rounded?8:1)for(i=[0:n-1])hull(){bezel_slice(p,p[5]*i/n);bezel_slice(p,p[5]*(i+1)/n);}}
"""


def clean(spec):
    if not isinstance(spec, dict):
        raise ValueError('Equipment spec must be an object.')
    if 'drives' in spec and spec['drives'] != []:
        return clean_drives(spec)
    if spec.get('faceplate_only') is True:
        return clean_faceplate(spec)
    if spec.get('second') is not None:
        return clean_pair(spec)
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
    if s['device_mount'] == 'wall':
        s['wall_open'] = wall_open(spec.get('wall_open', ['rear']))
    raw_feet = spec.get('feet') or []
    if not isinstance(raw_feet, list) or len(raw_feet) > 32:
        raise ValueError('Feet must be a list of at most 32 footprints.')
    if raw_feet:
        s['feet'] = []
        for f in raw_feet:
            if not isinstance(f, dict):
                raise ValueError('Each foot needs x, y, width, depth and height.')
            w, d = num(f.get('w'), 'Foot width', 2, s['dev_w']), num(f.get('d'), 'Foot depth', 2, s['dev_d'])
            x, y = num(f.get('x'), 'Foot X', 0, s['dev_w']-w), num(f.get('y'), 'Foot Y', 0, s['dev_d']-d)
            h = num(f.get('h'), 'Foot height', 0.3, s['dev_h'])
            s['feet'].append({'x': x, 'y': y, 'w': w, 'd': d, 'h': h})
    choices = placement_settings({k:spec[k] for k in V2_DEFAULTS if k in spec})
    for k, default in V2_DEFAULTS.items():
        if k in choices and choices[k] != default: s[k] = choices[k]
    if 'sleeve_top' in s and s['device_mount'] != 'sleeve':
        raise ValueError('Top play is only available for a sleeve.')
    if s.get('feet_style') == 'grooves' and (s['device_mount'] not in ('flat','sleeve') or not s.get('feet')):
        raise ValueError('Foot grooves need a flat or sleeve mount with feet.')
    if s.get('insert_bosses') and (s['device_mount'] != 'sleeve' or s['joint'] != 'screw'):
        raise ValueError('Stronger insert bosses need a sleeve with a screw joint.')
    if s.get('hidden_joint'):
        if s['device_mount'] != 'sleeve' or s['joint'] != 'screw':
            raise ValueError('Hidden screws need a sleeve with a screw joint.')
        if s.get('insert_bosses'):
            raise ValueError('Hidden screws and stronger insert bosses cannot be combined.')
        if spec.get('tray_follow') is True:
            raise ValueError('Hidden screws and a tray that follows the device cannot be combined.')
    if s.get('rear_floor_opening') and spec.get('rear_support') is not True:
        raise ValueError('Cable opening in floor needs rear support.')
    raw_zones = spec.get('protrusions', [])
    if not isinstance(raw_zones, list) or len(raw_zones)>32:
        raise ValueError('Protrusions must be a list of at most 32 keep-clear zones.')
    if raw_zones:
        s['protrusions']=[]
        for p in raw_zones:
            if not isinstance(p,dict) or p.get('face') not in ('front','back','left','right','top','bottom') or p.get('keep_clear') is not True:
                raise ValueError('Each protrusion needs a face and keep_clear: true.')
            q={'face':p['face'],'keep_clear':True}
            for k in ('x','y','z'):q[k]=num(p.get(k),'Keep-clear '+k,-500,500)
            for k in ('w','d','h'):q[k]=num(p.get(k),'Keep-clear '+k,.1,500)
            s['protrusions'].append(q)
    s['rear_support'] = spec.get('rear_support') is True
    if 'rear_style' in spec and spec['rear_style'] not in REAR_STYLES:
        raise ValueError('Invalid rear bracket style.')
    if s['rear_support'] and 'rear_style' in spec:
        s['rear_style'] = spec['rear_style']
    if s['rear_support'] and 'rear_openings' in spec:
        if not isinstance(spec['rear_openings'], bool):
            raise ValueError('rear_openings must be a boolean.')
        s['rear_openings'] = spec['rear_openings']
    if s['rear_support']:
        if s['joint'] == 'single':
            raise ValueError('Rear-post support needs the screw joint (a 240 mm single print is not offered).')
        if s['dev_d'] > 200:
            raise ValueError('With rear-post support the device can be at most 200 mm deep.')
    mode=spec.get('front_position','today');bezel=spec.get('bezel','none')
    if mode not in port_openings.FRONT_POSITIONS:raise ValueError('Invalid front position.')
    if bezel not in port_openings.BEZELS:raise ValueError('Invalid bezel.')
    if any(isinstance(spec.get(k),bool) for k in ('front_setback','bezel_size')):raise ValueError('Position and bezel sizes must be numbers, not booleans.')
    setback=num(spec.get('front_setback',16),'Set back',0,100)
    bezel_size=num(spec.get('bezel_size',1),'Bezel size',.5,1.5)
    if mode!='today':s['front_position']=mode
    if mode=='setback':s['front_setback']=setback
    if bezel!='none':s.update(bezel=bezel,bezel_size=bezel_size)
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
        if mode=='today' and float(spec.get('dev_off_y', 0) or 0) < -FRONT_GAP:  # equipment_tray.scad assert dev_y>=0
            raise ValueError('The device is moved into the faceplate; the front gap must be at least 0 mm.')
    except (TypeError, ValueError) as exc:
        if 'faceplate' in str(exc):
            raise
    s['dev_off_y'] = num(spec.get('dev_off_y', 0) or 0, 'Front/back offset', -FRONT_GAP, 230) if mode=='today' else port_openings.device_y(s)-FRONT_GAP
    position_errors=port_openings.position_problems(dict(s,holes=spec.get('holes') or []))
    if position_errors:raise ValueError(position_errors[0])
    fp_w, fp_d = (s['dev_d'], s['dev_w']) if s['dev_rot'] in (90, 270) else (s['dev_w'], s['dev_d'])
    win = sleeve_geometry(s)
    border = max(MARGIN, port_openings.SLEEVE_SIDE + port_openings.SLEEVE_WALL) if win else MARGIN
    if win and win.get('hidden'):
        border = port_openings.SLEEVE_SIDE + port_openings.SLEEVE_WALL + port_openings.HIDDEN_GAP + 2 * port_openings.HIDDEN_HALF
    width = tray_width(s)
    if width > MAX_TRAY:
        hint = ' Too wide this way round; it fits if you press Rotate 90°.' if 2 * abs(s['dev_off_x']) + fp_d + 2 * border <= MAX_TRAY else ''
        raise ValueError(f'This tray is {width:g} mm wide but the rack opening allows {MAX_TRAY:g} mm ({RACK_INNER_W:g} mm minus {SIDE_CLEAR:g} mm each side). Move the device less far sideways.' + hint
                         + (' The hidden screw joint adds about 20 mm of tray beside each sleeve wall; turn it off for a wider device.' if win and win.get('hidden') else ''))
    validate_foot_pockets(s, width)
    if not win and s['rear_support'] and FRONT_GAP + s['dev_off_y'] + fp_d + MARGIN > 240:
        raise ValueError('The device is moved past the rear posts; reduce the front/back offset.')
    if s['device_mount'] == 'flat':
        if FRONT_GAP + s['dev_off_y'] < 6.2:
            raise ValueError('Flat corner stops need a front gap of at least 6.2 mm.')
        if s['joint'] == 'screw' and FRONT_GAP + s['dev_off_y'] < 11.5:
            raise ValueError('Flat device must clear the front screw joint (front gap >= 11.5 mm).')
        if not win and s['rear_support'] and FRONT_GAP + s['dev_off_y'] + fp_d > 240 - 11.5:
            raise ValueError('Flat device must clear the rear screw joint (rear gap >= 11.5 mm).')
    if win:
        if fp_d / 4 - 4 - 6 < 8:
            raise ValueError('Sleeve depth must be at least 72 mm to keep strap slots clear of the front joint.')
        if win['bottom'] - PLATE_GAP/2 < port_openings.SLEEVE_BAND or s['u']*RACK_PITCH-PLATE_GAP/2-win['top'] < port_openings.SLEEVE_BAND:
            raise ValueError(f"Too tall for a flush window in {s['u']}U; choose {s['u']+1}U")
        if s['rear_support'] and win['stop_end'] > 240-11.5:
            raise ValueError('Sleeve rear stop and device must clear the rear screw joint by at least 11.5 mm.')
        if s['joint'] == 'screw' and win['height'] < 10:
            raise ValueError('Sleeve screw joint needs a window at least 10 mm tall; choose a single printed piece.')
        s['dev_off_y'] = 0  # Flush front is fixed; old front-gap placement does not move the sleeve.
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
    tray_half = width/2 if s.get('insert_bosses') or s.get('hidden_joint') else abs(s['dev_off_x']) + fp_w / 2 + MARGIN
    # Opt-in (Brian, 2026-10-22): the sleeve tray follows the device sideways instead of staying centred,
    # freeing plate room on the other side (e.g. for a keystone). Fit/strength UNKNOWN.
    if spec.get('tray_follow') is True:
        if s['device_mount'] != 'sleeve' or s['rear_support'] or s.get('insert_bosses') or s.get('hidden_joint') or s.get('feet_style') == 'grooves':
            raise ValueError('Tray follows device needs a sleeve without rear support, insert bosses or foot grooves.')
        if s['dev_off_x']:
            s['tray_follow'] = True
    if s.get('tray_follow'):
        lo, hi = s['dev_off_x'] - width/2 + abs(s['dev_off_x']), s['dev_off_x'] + width/2 - abs(s['dev_off_x'])
        if any(x + 9.9 > lo - 0.5 and x - 9.9 < hi + 0.5 for x in s['keystones']):
            raise ValueError(f'A keystone collar would hit the tray (tray spans {lo:g} to {hi:g} mm); keep keystones 10.4 mm clear of it.')
    elif any(abs(x) - 9.9 < tray_half + 0.5 for x in s['keystones']):
        raise ValueError(f'A keystone collar would hit the tray; keep keystones at least {tray_half + 10.4:g} mm from centre.')
    s['ports'] = []
    input_ports, dropped_ports, window_errors = port_openings.sleeve_ports((spec.get('ports') or [])[:20], window_spec(s)) if port_openings.front_window(s) else ((spec.get('ports') or [])[:20], [], [])
    if window_errors:
        raise ValueError(window_errors[0])
    for p in input_ports:
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
    if win and win.get('hidden'):
        for p in s['ports']:
            if any(abs(p['x']-x) < port_openings.JOINT_HALF+port_openings.JOINT_CLEAR+p['w']/2 and p['z']-p['h']/2 < port_openings.HIDDEN_TOP+port_openings.JOINT_CLEAR for x in win['joints']):
                raise ValueError('A front opening sits in front of the hidden screw joint; move or remove it.')
    elif win and s['joint'] == 'screw':
        for p in s['ports']:
            if any(abs(p['x']-x) < port_openings.SLEEVE_WALL/2+p['w']/2 and p['z']+p['h']/2 > win['bottom'] and p['z']-p['h']/2 < win['top'] for x in win['joints']):
                raise ValueError('A front opening overlaps a sleeve wall joint; move or remove it.')
    if s['joint'] == 'screw' and not win and not spec.get('_pair'):  # a pair places its joints in clean_pair()
        placed = port_openings.joint_positions(s['ports'], s['keystones'], tray_half)
        if placed['problem']:
            raise ValueError(placed['problem'])
        if placed['moved']:
            s['joint_x'] = placed['joints']
    ids = [p['id'] for p in s['ports'] + s['rear_ports']]
    if len(ids) != len(set(ids)):
        raise ValueError('Each port needs its own id.')
    # Engraved faceplate text (Brian, 2026-10-22), 0.6 mm deep into the front face. Readability when printed UNKNOWN.
    raw_labels = spec.get('labels') or []
    if not isinstance(raw_labels, list) or len(raw_labels) > 8:
        raise ValueError('Labels must be a list of at most 8 entries.')
    if raw_labels:
        s['labels'] = []
        for l in raw_labels:
            text = str((l or {}).get('text') or '').strip() if isinstance(l, dict) else ''
            if not re.fullmatch(r'[A-Za-z0-9 .-]{1,16}', text):
                raise ValueError('Label text must be 1-16 letters, digits, spaces, dots or dashes.')
            s['labels'].append({'text': text, 'x': num(l.get('x'), 'Label X', -PLATE_HALF + 3, PLATE_HALF - 3),
                                'z': num(l.get('z'), 'Label Z', 1.5, s['u'] * RACK_PITCH - 1.5),
                                'size': num(l.get('size', 4.5), 'Label size', 3, 10)})
    if 'planning_ports' in spec:
        s['planning_ports'] = cable_ports.planning_ports(spec['planning_ports'], s['u'])
    rear_floor_geometry(s)
    if not spec.get('_pair'): validate_wall(s)
    return s


# Two devices on one tray (Brian, 2026-10-20): "space permitting". The first device keeps the slot's tray settings;
# the second has its own position, rotation and mounting (SECOND_KEYS) and shares everything else (rack units, joint,
# keystones, rear support, bezel). Fit, retention and strength of both stay UNKNOWN.
SECOND_KEYS = ('dev_off_x', 'dev_off_y', 'dev_rot', 'device_mount', 'wall_open', 'standoff', 'insert_pilot', 'board_t')
PAIR_GAP = 4  # PROPOSED minimum gap between the two footprints
# How far each mounting's printed features reach outside the footprint (equipment_tray.scad device_features_*).
PAIR_REACH = {'inserts': 0, 'pegs': 0, 'clips': 2.5, 'straps': 5.5, 'wall': 2.5, 'flat': 6.2}
SECOND_FIELDS = ('name', 'dev_w', 'dev_d', 'dev_h', 'hole_d', 'standoff', 'insert_pilot', 'board_t', 'holes',
                 'device_mount', 'dev_off_x', 'dev_off_y', 'dev_rot', 'feet', 'wall_open')


def second_settings(value):
    """Keep only the second device's own tray keys (placement.second.tray)."""
    return {k: v for k, v in placement_settings(value).items() if k in SECOND_KEYS}


def tray_devices(s):
    """The devices on a cleaned spec's tray, each as a spec dict (the second shares the slot settings)."""
    out = [s]
    if s.get('second'):
        out.append(dict(s, **s['second']))
    return out


def footprint(d):
    """(x0, x1, y0, y1) of a device on the tray: X from the rack centre, Y behind the faceplate rear face."""
    fw, fd = (d['dev_d'], d['dev_w']) if d.get('dev_rot', 0) in (90, 270) else (d['dev_w'], d['dev_d'])
    x0, y0 = float(d.get('dev_off_x', 0)) - fw/2, port_openings.device_y(d)
    return x0, x0 + fw, y0, y0 + fd


def pair_tray_half(s):
    return max(max(abs(f[0]), abs(f[1])) for f in map(footprint, tray_devices(s))) + MARGIN


def pair_problems(a, b):
    """Plain-language problems for two cleaned single-device specs sharing one tray (tray-pair.js mirrors this)."""
    out = []
    if 'sleeve' in (a['device_mount'], b['device_mount']):
        out.append('A sleeve boxes in the whole front, so it cannot share a tray. Choose another mounting, or use one device.')
    if a.get('front_position', 'today') != 'today':
        out.append('With two devices, use the As today front position (Flush and Set back cut a window for one device only).')
    if (a['device_mount'] == 'flat') != (b['device_mount'] == 'flat'):
        out.append('Both devices sit on one tray floor: either both use Sits flat, or neither does.')
    if out:
        return out
    fa, fb = footprint(a), footprint(b)
    need = max(PAIR_GAP, PAIR_REACH.get(a['device_mount'], 0) + PAIR_REACH.get(b['device_mount'], 0))
    apart = max(fb[0] - fa[1], fa[0] - fb[1], fb[2] - fa[3], fa[2] - fb[3])
    if apart < need - 1e-9:
        gap = 'overlapping' if apart < 0 else f'only {round(apart, 1):g} mm apart'
        out.append(f'The two devices are {gap}; they need at least {need:g} mm between them (mounting features included). '
                   'Drag one sideways or behind the other.')
    width = 2 * (max(abs(v) for v in fa[:2] + fb[:2]) + MARGIN)
    if width > MAX_TRAY:
        out.append(f'Together the two devices need a tray {round(width, 1):g} mm wide; the rack opening allows {MAX_TRAY:g} mm. '
                   'Rotate one, move them closer to the centre, or put one behind the other.')
    return out


def opening_clash(ports_a, ports_b, web=2):
    """First pair of front openings (one per device) closer than the 2 mm web, as a sentence; else None."""
    for p in ports_a:
        for q in ports_b:
            if abs(p['x'] - q['x']) - (p['w'] + q['w'])/2 < web and abs(p['z'] - q['z']) - (p['h'] + q['h'])/2 < web:
                return (f"The {p['label'] or 'first device'} and {q['label'] or 'second device'} openings are closer than "
                        f'{web:g} mm on the faceplate. Move one device sideways.')
    return None


def clean_pair(spec):
    if any(s.get('feet_style') == 'grooves' or s.get('rear_floor_opening') for s in (spec, spec.get('second') or {}) if isinstance(s, dict)):
        raise ValueError('Foot grooves and the cable floor opening need a single-device tray.')
    second = spec['second']
    if not isinstance(second, dict):
        raise ValueError('The second device must be an object.')
    first = {k: v for k, v in spec.items() if k != 'second'}
    keystones = first.get('keystones') or []
    s = clean(dict(first, keystones=[], _pair=True))
    d2 = {k: v for k, v in second.items() if (k not in PLACEMENT_KEYS or k in SECOND_KEYS)
          and k not in ('quality', 'coupon', 'planning_ports', 'second')}
    try:
        s2 = clean(dict(d2, keystones=[], u=s['u'], joint=s['joint'], rear_support=s['rear_support'], _pair=True))
    except ValueError as exc:
        raise ValueError(f'Second device: {exc}')
    problems = pair_problems(s, s2)
    if not problems and s['rear_support'] and s2.get('protrusions'):
        problems.append('Rear keep-clear zones of the second device are not supported yet; remove them in its library item or turn off rear support.')
    if problems:
        raise ValueError(problems[0])
    s.pop('joint_x', None)
    s['second'] = {k: s2[k] for k in SECOND_FIELDS if k in s2}
    half = pair_tray_half(s)
    validate_foot_pockets(s, 2 * half)
    validate_foot_pockets(dict(s, **s['second']), 2 * half)
    s['keystones'] = [num(x, 'Keystone X', -PLATE_HALF + 24, PLATE_HALF - 24) for x in keystones][:12]
    xs = sorted(s['keystones'])
    if any(b - a < 21 for a, b in zip(xs, xs[1:])):
        raise ValueError('Keystones must be at least 21 mm apart.')
    if any(abs(x) - 9.9 < half + 0.5 for x in s['keystones']):
        raise ValueError(f'A keystone collar would hit the tray; keep keystones at least {half + 10.4:g} mm from centre.')
    # Second-device ports get a "d2-" id so cable plans can tell the two devices apart.
    ports2 = [dict(p, id=('d2-' + p['id'])[:40]) for p in s2['ports']]
    found = port_openings.problems(s['ports'] + ports2, s['u'], s['keystones'])
    clash = opening_clash(s['ports'], ports2)
    if found or clash:
        raise ValueError(found[0] if found else clash)
    s['ports'] += ports2
    s['rear_ports'] += [dict(p, id=('d2-' + p['id'])[:40]) for p in s2['rear_ports']]
    if s['joint'] == 'screw':
        placed = port_openings.joint_positions(s['ports'], s['keystones'], half)
        if placed['problem']:
            raise ValueError(placed['problem'])
        if placed['moved']:
            s['joint_x'] = placed['joints']
    for device in tray_devices(s):
        validate_wall(device, s.get('joint_x', [-min(40,half-12),min(40,half-12)]))
    ids = [p['id'] for p in s['ports'] + s['rear_ports']]
    if len(ids) != len(set(ids)):
        raise ValueError('Each port needs its own id.')
    return s


# The second device reuses the template's own device features: dp() and the two feature modules are copied with every
# device-specific name renamed, so a one-device source stays byte-identical to older ones.
SECOND_RENAMES = {'dev_x': 'dev2_x', 'dev_y': 'dev2_y', 'fp_w': 'fp2_w', 'fp_d': 'fp2_d', 'dev_w': 'dev2_w', 'dev_d': 'dev2_d',
                  'dev_h': 'dev2_h', 'dev_rot': 'dev2_rot', 'dev_off_x': 'dev2_off_x', 'holes': 'dev2_holes', 'hole_d': 'dev2_hole_d',
                  'standoff': 'dev2_standoff', 'insert_pilot': 'dev2_insert_pilot', 'board_t': 'dev2_board_t',
                  'device_mount': 'dev2_mount', 'feet': 'dev2_feet', 'foot_h': 'dev2_foot_h', 'dp': 'dp2',
                  'wall_open': 'dev2_wall_open', 'wall_h': 'dev2_wall_h', 'wall_spans': 'wall2_spans', 'wall_local': 'wall2_local', 'wall_rects': 'wall2_rects', 'wall_add': 'wall2_add',
                  'device_features_add': 'device2_features_add', 'device_features_cut': 'device2_features_cut'}
SECOND_SCAD = """
// ---- Second device on this tray (Brian, 2026-10-20). PROPOSED; fit, retention and strength UNKNOWN.
// Declared here so the derived values below see them; the wizard overrides at the end replace them in place.
dev2_w=1; dev2_d=1; dev2_h=1; dev2_hole_d=2.7; dev2_standoff=6; dev2_insert_pilot=3.2; dev2_board_t=1.6; dev2_holes=[]; dev2_mount="inserts"; dev2_off_x=0; dev2_off_y=0; dev2_rot=0; dev2_feet=[];
fp2_w=(dev2_rot==90||dev2_rot==270)?dev2_d:dev2_w; fp2_d=(dev2_rot==90||dev2_rot==270)?dev2_w:dev2_d;
dev2_x=-fp2_w/2+dev2_off_x; dev2_y=front_gap+dev2_off_y;
dev2_foot_h=dev2_mount=="flat"?max([0,for(f=dev2_feet)f[4]]):0;
module device2_ghost(){%translate([dev2_x,dev2_y,floor_top+(dev2_mount=="inserts"||dev2_mount=="pegs"||dev2_mount=="clips"?dev2_standoff:0)-dev2_foot_h])cube([fp2_w,fp2_d,dev2_h]);}
"""


def second_device_source(text):
    dp = re.search(r'^function dp\(p\)=.*$', text, flags=re.M).group(0)
    body = re.search(r'^module device_features_add\(\)\{.*?(?=^module tray_joint_add)', text, flags=re.M | re.S).group(0)
    code = dp + '\n' + body
    for old, new in SECOND_RENAMES.items():
        code = re.sub(r'\b' + old + r'\b', new, code)
    for old, new in (('   device_features_add();\n', '   device_features_add();device2_features_add();\n'),
                     ('  device_features_cut();\n }', '  device_features_cut();device2_features_cut();\n }'),
                     ('cube([fp_w,fp_d,dev_h]);}', 'cube([fp_w,fp_d,dev_h]);device2_ghost();}')):
        if text.count(old) != 1:
            raise ValueError('The tray template changed; two-device trays cannot be built from it.')
        text = text.replace(old, new)
    return text + SECOND_SCAD + code


def source(s):
    def lit(v):
        return json.dumps(v)
    over = {k: s[k] for k in ('dev_w', 'dev_d', 'dev_h', 'hole_d', 'standoff', 'insert_pilot', 'board_t', 'u',
                              'holes', 'keystones', 'device_mount', 'joint', 'rear_support', 'coupon')}
    if s.get('device_mount') == 'wall': over['wall_open'] = s['wall_open']
    for key in V2_DEFAULTS:
        if key in s: over[key] = s[key]
    if s.get('feet_style') == 'grooves':
        tracks = foot_grooves(s)
        over['foot_tracks'] = [[t[k] for k in ('x0','x1','y0','y1','depth','floor_bottom')] for t in tracks]
        over['foot_dips'] = [[p[k] for k in ('x0','x1','y0','y1','cut_depth')]+[t['depth'],p['ramp']] for t in tracks for p in t['dips']]
    if s.get('rear_floor_opening'):
        q = rear_floor_geometry(s)
        over['floor_cable_box'] = [q[k] for k in ('x0','x1','y0','y1')]
    style = rear_style(s)
    if style == 'open':
        over['rear_openings'] = True
    elif style in ('reinforced', 'slots', 'vents'):
        geometry = rear_geometry(s)
        over.update(rear_style=style, rear_style_windows=geometry['windows'],
                    rear_style_holes=geometry['holes'], rear_style_lips=geometry['flanges'],
                    rear_style_radius=5 if style == 'slots' or style == 'vents' else 2,
                    rear_vent_d=REAR_VENT_D if style == 'vents' else 6)
    if s.get('feet'):
        over['feet'] = [[f['x'], f['y'], f['w'], f['d'], f['h']] for f in s['feet']]
    # Placement keys are written only when moved/rotated, so default sources stay byte-identical to older ones.
    for k in ('dev_off_x', 'dev_off_y', 'dev_rot', 'joint_x'):
        if s.get(k):
            over[k] = s[k]
    if s.get('tray_follow'):
        w = round(tray_width(s) - 2 * abs(s['dev_off_x']), 4)
        over.update(tray_w=w, tray_x=round(s['dev_off_x'] - w / 2, 4))
    if s.get('labels'):
        over['labels'] = [[l['text'], l['x'], l['z'], l['size']] for l in s['labels']]
    over['ports'] = [[p['x'], p['z'], p['w'], p['h'], p['r']] for p in s['ports']]
    # Export quality: only a non-standard level overrides the template's $fn=48 (last assignment wins in OpenSCAD).
    if s.get('quality', DEFAULT_QUALITY) != DEFAULT_QUALITY:
        over['$fn'] = EXPORT_QUALITY[s['quality']]
    if s.get('second'):
        d2 = s['second']
        over.update(dev2_w=d2['dev_w'], dev2_d=d2['dev_d'], dev2_h=d2['dev_h'], dev2_hole_d=d2['hole_d'],
                    dev2_standoff=d2['standoff'], dev2_insert_pilot=d2['insert_pilot'], dev2_board_t=d2['board_t'],
                    dev2_holes=d2['holes'], dev2_mount=d2['device_mount'], dev2_off_x=d2.get('dev_off_x', 0),
                    dev2_off_y=d2.get('dev_off_y', 0), dev2_rot=d2.get('dev_rot', 0),
                    dev2_feet=[[f['x'], f['y'], f['w'], f['d'], f['h']] for f in d2.get('feet', [])])
        if d2['device_mount'] == 'wall': over['dev2_wall_open'] = d2['wall_open']
        # The tray spans both devices (still centred); the template's own formula only knows the first.
        over['tray_w'] = round(2 * pair_tray_half(s), 4)
        if not s['rear_support']:
            over['tray_d'] = round(max(f[3] for f in map(footprint, tray_devices(s))) + MARGIN, 4)
    if s.get('drives'):
        over.update(drives=s['drives'], drive_mount=s['drive_mount'], ssd_h=s['ssd_h'],
                    tray_w=s['dev_w']+16, tray_d=s['dev_d']+12+25)
    if s.get('faceplate_only'): over['part'] = 'faceplate'
    lines = ['', '// ---- wizard overrides: ' + re.sub(r'[\r\n]', ' ', s['name'])] + [f'{k}={lit(v)};' for k, v in over.items()]
    if style in ('reinforced', 'vents'):
        lines.extend('// '+note for note in dict.fromkeys(geometry.get('notes', [])))
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
        # All parts as separate bodies in one file, flat on the bed (built here; the cached revision stays untouched).
        meshes = {f.stem: f.read_text(encoding='utf-8') for f in final.glob('*.stl')}
        if meshes:
            stem = re.sub(r'[^\w-]+', '_', s['name'] or 'equipment').strip('_') + '_print-layout'
            z.writestr(stem + '.3mf', print_layout.layout_3mf(meshes))  # opens as separate objects in slicers
    return stream.getvalue()


def preview(spec, data_dir):
    """Render (or reuse) the parts and return ids so the wizard can fetch meshes for its 3D view."""
    final = render(spec, data_dir)
    report = json.loads((final / 'revision.json').read_text(encoding='utf-8'))
    return {'id': report['id'], 'parts': report['parts']}


def render(spec, data_dir):
    s = clean(spec)
    src = source(s)
    parts = ['faceplate'] if s.get('faceplate_only') else ['combined'] if s['joint'] == 'single' else ['tray', 'faceplate'] + (['rear_bracket'] if s['rear_support'] else [])
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
                if s.get('drives'): report.update(drive_hardware=drive_hardware(s), limitations=LIMITS+DRIVE_LIMITS)
                (folder / 'revision.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
                folder.rename(final)
    return final


# Drive assembly is an opt-in branch of the generic adapter; empty drives change no source bytes.
DRIVE_REPLACEMENTS = {'   device_features_add();': '   if(len(drives)>0)drive_add();else device_features_add();', '  device_features_cut();': '  if(len(drives)>0)drive_cut();else device_features_cut();'}
DRIVE_LIMITS = ['PROPOSED — UNVALIDATED. Drive fit, vibration, strength, airflow/temperature and usable rack depth UNKNOWN.',
 'Nominal SFF dimensions only; actual drive holes, thread depth, screw heads/torque and cable bend space must be checked. 7 mm SSD bottom holes are optional.']

def clean_drives(spec):
    ds=spec.get('drives')
    if not isinstance(ds,list) or len(ds)!=2 or sorted(str(d[0]) for d in ds if isinstance(d,list) and len(d)==3)!=['2.5','3.5']:
        raise ValueError('Drive tray needs one 3.5 and one 2.5 drive [type,x_off,y_off].')
    mode=spec.get('drive_mount','screws')
    if mode!='screws': raise ValueError('Drives mount with bottom screws (the tool-free sleeve was dropped, Brian 2026-10-22).')
    sh=num(spec.get('ssd_h',7),'SSD height',7,9.5)
    if sh not in (7,9.5): raise ValueError('SSD height must be 7 or 9.5 mm.')
    if spec.get('second') or spec.get('faceplate_only') or spec.get('feet') or spec.get('ports') or spec.get('keystones') or spec.get('rear_support') or spec.get('coupon'):
        raise ValueError('Drive tray requires a blank faceplate, no feet, second item, coupon or rear bracket.')
    if spec.get('u',1)!=1 or spec.get('joint','screw')!='screw' or spec.get('device_mount','flat')!='flat' or spec.get('front_position','today')!='today' or spec.get('bezel','none')!='none' or any(spec.get(k,0) for k in ('dev_rot','dev_off_x','dev_off_y')):
        raise ValueError('Drive tray uses fixed 1U placement, a blank faceplate and the existing screw joint.')
    out=[];boxes=[]
    for typ,x,y in ds:
        x=num(x,'Drive X',-100,100);y=num(y,'Drive Y',0,50)
        w,dep=(101.6,147) if typ=='3.5' else (69.85,100)
        out.append([typ,x,y]);boxes.append((x,x+w,12+y,12+y+dep))
    a,b=boxes
    if max(a[0]-b[1],b[0]-a[1])<8: raise ValueError('Drives need an 8 mm side gap for independent rails/tabs.')
    width=round(2*max(abs(v) for b in boxes for v in b[:2])+16,3)
    depth=max(b[3] for b in boxes)+25
    if width>204: raise ValueError('Drive tray exceeds the 204 mm maximum width.')
    if depth>240: raise ValueError('Drive tray needs 25 mm rear connector space within 240 mm nominal depth.')
    base=dict(name=spec.get('name','Drives (3.5" + 2.5")'),dev_w=width-16,dev_d=depth-37,dev_h=29.1,
              device_mount='flat',joint='screw',standoff=0,holes=[],ports=[],keystones=[],u=1)
    if 'quality' in spec:base['quality']=spec['quality']
    s=clean(base);s.update(drives=out,drive_mount=mode,ssd_h=sh)
    return s

def drive_hardware(s):
    if not s.get('drives') or s.get('drive_mount')!='screws':return []
    return [{'quantity':4,'description':'6-32 x 1/4 inch (drive screws; head/torque UNKNOWN)'},
            {'quantity':4,'description':'M3 x 4 mm (drive screws; head/torque UNKNOWN)'}]
