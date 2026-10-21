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

import cable_ports
import port_openings
import mesh_revision

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / 'equipment_tray.scad'
MOUNTS = ('inserts', 'pegs', 'clips', 'straps', 'flat', 'sleeve')
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
PLACEMENT_KEYS = ('dev_off_x', 'dev_off_y', 'dev_rot', 'device_mount', 'standoff', 'insert_pilot', 'board_t',
                  'joint', 'keystones', 'rear_support', 'rear_openings', 'rear_style', 'u', 'front_position', 'front_setback', 'bezel', 'bezel_size')


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
    for key in PLACEMENT_KEYS:
        if key not in value:
            continue
        v = value[key]
        if key == 'keystones':
            if not isinstance(v, list) or len(v) > 12 or any(type(x) not in (int, float) or isinstance(x, bool) for x in v):
                raise ValueError('Keystones must be a list of positions.')
            v = list(v)
        elif key in ('rear_support', 'rear_openings'):
            if type(v) is not bool:
                raise ValueError('Rear support must be true or false.')
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
    return {'ok': True, 'u': s['u']}


RACK_PITCH, PLATE_GAP, LEGACY_SLOT_OFFSET = port_openings.RACK_PITCH, port_openings.PLATE_GAP, port_openings.LEGACY_SLOT_OFFSET

RACK_INNER_W, SIDE_CLEAR = 208, 2  # PROPOSED nominal opening and clearance per side
MAX_TRAY = RACK_INNER_W - 2 * SIDE_CLEAR
FRONT_GAP, MARGIN = 12, 8  # mirror front_gap / margin in equipment_tray.scad


def floor_z(spec):
    return 0.5 if spec.get('device_mount') in ('flat', 'sleeve') else 7 + LEGACY_SLOT_OFFSET


def device_lift(spec):
    feet = port_openings.foot_height(spec)
    return floor_z(spec) + 3 + (0 if spec.get('device_mount') in ('straps', 'flat', 'sleeve') else float(spec.get('standoff', 6))) - feet  # case on the floor top; feet hang in their pockets


def needed_height(spec):
    mount = spec.get('device_mount')
    extra = (float(spec.get('board_t', 1.6)) + (1.6 if mount == 'pegs' else 2.5)) if mount in ('pegs', 'clips') else 0
    return max(device_lift(spec) + max(float(spec['dev_h']), extra),
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


def validate_foot_pockets(spec, tray_w):
    pockets=foot_pockets(spec)
    if not pockets:return
    fp_w,fp_d=(spec['dev_d'],spec['dev_w']) if spec.get('dev_rot',0) in (90,270) else (spec['dev_w'],spec['dev_d'])
    dev_x=-fp_w/2+float(spec.get('dev_off_x',0));dev_y=port_openings.device_y(spec)
    def overlap(p,x0,x1,y0,y1):return p['x0']<x1 and p['x1']>x0 and p['y0']<y1 and p['y1']>y0
    if spec.get('joint','screw')=='screw':
        jx=min(40,tray_w/2-12)
        if any(overlap(p,x-9,x+9,0,11.3) for p in pockets for x in (-jx,jx)):
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
            if overlap(p,left,right,0,8):raise ValueError('A foot pocket would cut into the floor strip under the sleeve window; move or remove that foot.')


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
    jx = min(40, abs(s.get('dev_off_x', 0)) + width/2 + 8 - 12)
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
        fp_d = s['dev_w'] if s.get('dev_rot') in (90,270) else s['dev_d']
        device_rear = (port_openings.device_y(s))+fp_d
        clear_depth = 240-device_rear-REAR_RETENTION_REACH.get(s['device_mount'],0)-REAR_LIP_CLEAR
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


def template_source(spec):
    # New builds always use the current slot-bottom template; saved revisions remain immutable.
    text = TEMPLATE.read_text(encoding='utf-8')
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
        plan=port_openings.bezel_plan(spec)
        shapes=[[p['x'],p['z'],p['w'],p['h'],p['r'],p['size']] for p in plan['openings'] if p['size']>0]
        code='\n// Front-edge bezel only: ports and case window. 8 rounded steps; 2 mm web.\n'
        code+='bezel_shapes='+json.dumps(shapes)+';\nbezel_rounded='+('true' if spec['bezel']=='rounded' else 'false')+';\n'
        code+=BEZEL_SCAD
        code+='\n'+'\n'.join('// '+n for n in plan['notes'])+'\n'
        text=text.replace('   plate_joint_cut();','   plate_joint_cut();bezel_cuts();')+code
    return text


BEZEL_SCAD = r"""
function bezel_out(b,t)=bezel_rounded?b-sqrt(max(0,b*b-(b-t)*(b-t))):b-t;
module bezel_slice(p,t){translate([p[0],-4+t,p[1]])rotate([90,0,0])linear_extrude(height=0.02)offset(delta=bezel_out(p[5],t))rrect(p[2],p[3],p[4]);}
module bezel_cuts(){for(p=bezel_shapes)let(n=bezel_rounded?8:1)for(i=[0:n-1])hull(){bezel_slice(p,p[5]*i/n);bezel_slice(p,p[5]*(i+1)/n);}}
"""


def clean(spec):
    if not isinstance(spec, dict):
        raise ValueError('Equipment spec must be an object.')
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
    win = port_openings.sleeve(s)
    border = max(MARGIN, port_openings.SLEEVE_SIDE + port_openings.SLEEVE_WALL) if win else MARGIN
    tray_width = 2 * (abs(s['dev_off_x']) + fp_w / 2 + border)
    if tray_width > MAX_TRAY:
        hint = ' Too wide this way round; it fits if you press Rotate 90°.' if 2 * abs(s['dev_off_x']) + fp_d + 2 * border <= MAX_TRAY else ''
        raise ValueError(f'This tray is {tray_width:g} mm wide but the rack opening allows {MAX_TRAY:g} mm ({RACK_INNER_W:g} mm minus {SIDE_CLEAR:g} mm each side). Move the device less far sideways.' + hint)
    validate_foot_pockets(s, tray_width)
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
    tray_half = abs(s['dev_off_x']) + fp_w / 2 + MARGIN
    if any(abs(x) - 9.9 < tray_half + 0.5 for x in s['keystones']):
        raise ValueError(f'A keystone collar would hit the tray; keep keystones at least {tray_half + 10.4:g} mm from centre.')
    s['ports'] = []
    input_ports, dropped_ports, window_errors = port_openings.sleeve_ports((spec.get('ports') or [])[:20], s) if port_openings.front_window(s) else ((spec.get('ports') or [])[:20], [], [])
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
    if win and s['joint'] == 'screw':
        for p in s['ports']:
            if any(abs(p['x']-x) < port_openings.SLEEVE_WALL/2+p['w']/2 and p['z']+p['h']/2 > win['bottom'] and p['z']-p['h']/2 < win['top'] for x in win['joints']):
                raise ValueError('A front opening overlaps a sleeve wall joint; move or remove it.')
    if s['joint'] == 'screw' and not win:
        placed = port_openings.joint_positions(s['ports'], s['keystones'], tray_half)
        if placed['problem']:
            raise ValueError(placed['problem'])
        if placed['moved']:
            s['joint_x'] = placed['joints']
    ids = [p['id'] for p in s['ports'] + s['rear_ports']]
    if len(ids) != len(set(ids)):
        raise ValueError('Each port needs its own id.')
    if 'planning_ports' in spec:
        s['planning_ports'] = cable_ports.planning_ports(spec['planning_ports'], s['u'])
    return s


def source(s):
    def lit(v):
        return json.dumps(v)
    over = {k: s[k] for k in ('dev_w', 'dev_d', 'dev_h', 'hole_d', 'standoff', 'insert_pilot', 'board_t', 'u',
                              'holes', 'keystones', 'device_mount', 'joint', 'rear_support', 'coupon')}
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
    over['ports'] = [[p['x'], p['z'], p['w'], p['h'], p['r']] for p in s['ports']]
    # Export quality: only a non-standard level overrides the template's $fn=48 (last assignment wins in OpenSCAD).
    if s.get('quality', DEFAULT_QUALITY) != DEFAULT_QUALITY:
        over['$fn'] = EXPORT_QUALITY[s['quality']]
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
    return stream.getvalue()


def preview(spec, data_dir):
    """Render (or reuse) the parts and return ids so the wizard can fetch meshes for its 3D view."""
    final = render(spec, data_dir)
    report = json.loads((final / 'revision.json').read_text(encoding='utf-8'))
    return {'id': report['id'], 'parts': report['parts']}


def render(spec, data_dir):
    s = clean(spec)
    src = source(s)
    parts = ['combined'] if s['joint'] == 'single' else ['tray', 'faceplate'] + (['rear_bracket'] if s['rear_support'] else [])
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
                (folder / 'revision.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
                folder.rename(final)
    return final
