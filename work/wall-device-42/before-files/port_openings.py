"""Pure front-opening planning. Physical fit and strength remain UNKNOWN."""
from copy import deepcopy
import math

RACK_PITCH, PLATE_GAP, LEGACY_SLOT_OFFSET = 44.45, 0.05, 1.225


# PROPOSED sleeve defaults, independent of third-party geometry.
SLEEVE_SIDE, SLEEVE_TOP, SLEEVE_WALL = 0.5, 0.3, 6
SLEEVE_LIP_W, SLEEVE_LIP_T, SLEEVE_BAND = 10, 1.5, 1.5
SLEEVE_STOP_T, SLEEVE_STOP_H = 4, 6
HIDDEN_TOP = 22.5   # tray_z 0.5 + 3 + 19: top of the joint upright
HIDDEN_GAP, HIDDEN_HALF = 2, 9   # opt-in hidden_joint (Task 41): joint block half-width and gap beyond the sleeve wall
FOOT_CLEARANCE, FOOT_EXTRA_DEPTH, FOOT_MIN_FLOOR = 0.5, 0.3, 0.8
FOOT_LIP_T = 3.0


def foot_height(spec):
    return max([0.0] + [float(f.get('h', 0)) for f in spec.get('feet', [])]) if spec.get('device_mount') in ('flat', 'sleeve') else 0.0


def case_height(spec):
    return max(0.0, float(spec.get('dev_h', 0)) - foot_height(spec))


def pocket_depth(spec):
    return foot_height(spec) + FOOT_EXTRA_DEPTH


def sleeve(spec):
    if spec.get('device_mount') != 'sleeve':
        return None
    turned = spec.get('dev_rot', 0) in (90, 270)
    w, d = (float(spec['dev_d']), float(spec['dev_w'])) if turned else (float(spec['dev_w']), float(spec['dev_d']))
    x, bottom = float(spec.get('dev_off_x', 0)), 3.5  # case rests on the floor top
    half = w / 2 + SLEEVE_SIDE
    top = bottom + case_height(spec) + SLEEVE_TOP
    lip_t = FOOT_LIP_T if foot_height(spec) else SLEEVE_LIP_T
    lip = lip_t if top + lip_t <= float(spec.get('u', 1)) * RACK_PITCH else 0
    out = dict(x=x, half=half, bottom=bottom, top=top, width=half*2,
               height=top-bottom, outside=w+2*(SLEEVE_SIDE+SLEEVE_WALL),
               lip=lip, rear=-4+d, stop_end=-4+d+SLEEVE_STOP_T,
               joints=[x-half-SLEEVE_WALL/2, x+half+SLEEVE_WALL/2],
               joint_z=[bottom+3, top-3])
    if spec.get('hidden_joint') is True:
        # Hidden joint: no screw holes through the plate; the tongue/boss joint sits outside the walls.
        reach = half+SLEEVE_WALL+HIDDEN_GAP+HIDDEN_HALF
        out.update(joints=[x-reach, x+reach], joint_z=[], hidden=True,
                   outside=w+2*(SLEEVE_SIDE+SLEEVE_WALL+HIDDEN_GAP+2*HIDDEN_HALF))
    return out


def sleeve_ports(ports, spec):
    win = front_window(spec)
    if not win:
        return list(ports or []), [], []
    kept, dropped, errors = [], [], []
    for p in ports or []:
        try:
            x, z, width, height = (float(p[k]) for k in ('x', 'z', 'w', 'h'))
        except (KeyError, TypeError, ValueError):
            raise ValueError('Enter valid sleeve front-opening dimensions.')
        if not all(math.isfinite(v) for v in (x,z,width,height)) or width < 1 or height < 1:
            raise ValueError('Enter valid sleeve front-opening dimensions.')
        x0, x1 = x-width/2, x+width/2
        z0, z1 = z-height/2, z+height/2
        inside = x0 >= win['x']-win['half'] and x1 <= win['x']+win['half'] and z0 >= win['bottom'] and z1 <= win['top']
        overlap = x1 > win['x']-win['half'] and x0 < win['x']+win['half'] and z1 > win['bottom'] and z0 < win['top']
        if inside:
            dropped.append(p)
        elif overlap:
            errors.append('A front opening crosses the sleeve window edge; move or remove it.')
        else:
            kept.append(p)
    return kept, dropped, errors

DEFAULT_SIZES = {
    'rj45': {'w': 17, 'h': 14, 'r': 1}, 'usb-a': {'w': 15, 'h': 8, 'r': 1},
    'usb-c': {'w': 12, 'h': 7, 'r': 3}, 'hdmi': {'w': 17, 'h': 8, 'r': 1},
    'micro-hdmi': {'w': 11, 'h': 7, 'r': 2}, 'dc-barrel': {'w': 11, 'h': 11, 'r': 5.5},
    'iec': {'w': 28, 'h': 20, 'r': 1}, 'other': {'w': 15, 'h': 8, 'r': 1}}
SIZE_NOTE = 'Starting size for this connector type: a guess, not a measured size. Edit it to match your device.'


def default_size(type=None):
    return dict(DEFAULT_SIZES.get(type, DEFAULT_SIZES['other']))


def lift(spec):
    return (0.5 + 3 - (7 + LEGACY_SLOT_OFFSET + 3) - foot_height(spec) if spec.get('device_mount') in ('flat', 'sleeve') else
            0 if spec.get('device_mount') == 'straps' else float(spec.get('standoff', 6)))


def front_openings(lib_spec, tray=None):
    eff = dict(lib_spec)
    eff.update({k: v for k, v in (tray or {}).items() if k in ('dev_off_x', 'dev_rot', 'device_mount', 'standoff')})
    rotation = float(eff.get('dev_rot') or 0)
    follows = rotation == 0
    dx = float(eff.get('dev_off_x') or 0) - float(lib_spec.get('dev_off_x') or 0) if follows else 0
    dz = round(lift(eff) - lift(lib_spec), 3) if follows else 0
    ports = deepcopy(lib_spec.get('ports') or [])
    if follows:
        for p in ports:
            p.update(x=round(float(p['x']) + dx, 3), z=round(float(p['z']) + dz, 3))
    face = 'rear' if rotation == 180 else 'side'
    message = (f'The device is turned {rotation:g}°, so its front ports now face the {face} of the tray. '
               'The front openings no longer line up with them. The faceplate STL keeps the openings where they were entered '
               'in the library (not moved). Check them, or remove them in Edit library item.') if not follows and ports else None
    return dict(ports=ports, dx=dx, dz=dz, follows=follows, rotation=rotation, message=message)


# Tray screw joint behind the faceplate (equipment_tray.scad tray_joint_add/plate_joint_add): block, tongue, boss and
# post fill X = joint ± 9 mm up to Z = 29 mm. An opening there would be blocked by it (and an edge touching the screw
# hole cannot be rendered cleanly). Brian, 2026-10-19: block such openings. 1 mm clearance is kept around the zone.
JOINT_HALF, JOINT_TOP, JOINT_CLEAR = 9, 29 + LEGACY_SLOT_OFFSET, 1


def problems(ports, u, keystones, joints=()):
    out = []
    plate_h = u * RACK_PITCH - PLATE_GAP
    for i, p in enumerate(ports or []):
        values = [p.get(k) for k in ('x', 'z', 'w', 'h')]
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in values):
            continue
        x, z, w, h = values
        label = p.get('label') or f'Port {i + 1}'
        if abs(x) + w / 2 > 126:
            out.append(f'{label} opening would run past the faceplate edge. Move the device back toward the centre or edit the port.')
        elif z - h / 2 < PLATE_GAP / 2 + 2 or z + h / 2 > PLATE_GAP / 2 + plate_h - 2:
            out.append(f'{label} opening would run off the top or bottom of the faceplate. Change the standoff or faceplate height, or edit the port.')
        else:
            for n, k in enumerate(keystones or []):
                if abs(x - k) < 10.5 + w / 2 and z - h / 2 < u * RACK_PITCH / 2 + 18.5 and z + h / 2 > u * RACK_PITCH / 2 - 15:
                    out.append(f'{label} opening would cut into keystone {n + 1} (at X = {k:g} mm). Move the device or the keystone.')
                    break
            else:
                for j in joints or ():
                    if abs(x - j) < JOINT_HALF + JOINT_CLEAR + w / 2 and z - h / 2 < JOINT_TOP + JOINT_CLEAR:
                        out.append(f'{label} opening sits in front of the tray screw joint at X = {j:g} mm; the cable would hit it. '
                                   'Move the device sideways or edit the port.')
                        break
    return out


# Brian, 2026-10-19 (option 3): each tray screw joint sits where it clears the front openings and keystones. The default
# spot (equipment_tray.scad: X = ±min(40, tray_w/2 - 12)) is kept whenever it is clear, so existing designs build the
# same; otherwise the nearest clear spot, in 0.5 mm steps, between 10 mm from centre and tray_w/2 - 12, is used for that
# side. Keystones keep the existing 16 mm joint distance. No clear spot -> a plain problem (blocks the build).
KEYSTONE_JOINT_GAP, JOINT_STEP, JOINT_MIN = 16, 0.5, 10


def _joint_clear(x, ports, keystones):
    for p in ports or []:
        values = [p.get(k) for k in ('x', 'z', 'w', 'h')]
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in values):
            continue
        px, z, w, h = values
        if abs(px - x) < JOINT_HALF + JOINT_CLEAR + w / 2 and z - h / 2 < JOINT_TOP + JOINT_CLEAR:
            return False
    return all(abs(k - x) >= KEYSTONE_JOINT_GAP for k in keystones or [])


def joint_positions(ports, keystones, tray_half):
    """-> {'joints': [left, right] (None where no spot is clear), 'default': d, 'moved': bool, 'problem': str|None}"""
    default = min(40, tray_half - 12)
    lo, hi = min(default, JOINT_MIN), tray_half - 12
    mags = [round(lo + i * JOINT_STEP, 3) for i in range(int(round((hi - lo) / JOINT_STEP)) + 1)]
    mags = sorted(set(mags + [default]), key=lambda m: (abs(m - default), -m))
    joints = []
    for sign in (-1, 1):
        joints.append(next((sign * m for m in mags if _joint_clear(sign * m, ports, keystones)), None))
    missing = [side for side, j in zip(('left', 'right'), joints) if j is None]
    problem = None
    if missing:
        problem = (f'The {" and ".join(missing)} tray screw joint{"s" if len(missing) > 1 else ""} cannot be placed clear of '
                   'the openings and keystones anywhere on the tray. Move the device or an opening, or choose the single '
                   'printed piece joint.')
    return {'joints': joints, 'default': default, 'moved': joints != [-default, default], 'problem': problem}


# Position measured from front Y=-4; unchanged defaults never add source text.
FRONT_POSITIONS = ('today', 'flush', 'setback')
BEZELS = ('none', 'chamfer', 'rounded')
SETBACK_MIN, SETBACK_MAX = 0, 100
BEZEL_MIN, BEZEL_MAX, BEZEL_DEFAULT, BEZEL_STEPS = .5, 1.5, 1., 8
BEZEL_WEB = 2.0  # >= existing problems() top/bottom allowance (2 mm)


def device_y(spec):
    mode=spec.get('front_position','today')
    if mode=='flush':return -4.0
    if mode=='setback':return -4.0+float(spec.get('front_setback',16))
    return -4.0 if spec.get('device_mount')=='sleeve' else 12.0+float(spec.get('dev_off_y',0))


def front_window(s):
    existing=sleeve(s)
    if existing:return existing
    if s.get('front_position','today')=='today' or device_y(s)>0:return None
    w=float(s['dev_d'] if s.get('dev_rot',0) in (90,270) else s['dev_w'])
    bottom=11.225+(0 if s.get('device_mount')=='straps' else float(s.get('standoff',6)))
    if s.get('device_mount')=='flat':bottom=3.5
    half=w/2+SLEEVE_SIDE;top=bottom+case_height(s)+SLEEVE_TOP
    return dict(x=float(s.get('dev_off_x',0)),half=half,bottom=bottom,top=top,width=half*2,height=top-bottom)


def position_problems(s):
    if s.get('front_position','today')=='today':return []
    y=device_y(s);out=[]
    if s.get('device_mount')=='sleeve' and abs(y+4)>1e-9:
        out.append('Sleeve set back is not supported: its front wall joints and strap slots assume a flush case. Choose As today or Flush with faceplate, or change the mount.')
    joint=y<11.5 and s.get('device_mount')!='sleeve' and s.get('joint')!='single'
    flat=s.get('device_mount')=='flat' and y<6.2
    if joint and flat:
        out.append('Flush or a set back under 15.5 mm is too close for the front screw joint and the flat corner stops. Set back at least 15.5 mm or choose Sleeve.')
    elif joint:
        out.append('Flush or a set back under 15.5 mm needs the Sleeve mount or a single printed piece joint; the front screw joint would hit the case.')
    elif flat:
        out.append('Flat corner stops need a front gap of at least 6.2 mm. Set back at least 10.2 mm or choose Sleeve.')
    if s.get('device_mount')=='clips' and y<1:
        out.append('Clip support ledges need a front gap of at least 1 mm. Set back at least 5 mm or choose Sleeve.')
    win=front_window(s)
    if win and (win['bottom']-PLATE_GAP/2<SLEEVE_BAND or s['u']*RACK_PITCH-PLATE_GAP/2-win['top']<SLEEVE_BAND):
        out.append('The front window needs 1.5 mm bands above and below; choose more rack units or lower the device.')
    if y<0 and s.get('device_mount') in ('inserts','pegs'):
        for x,hy in s.get('holes',[]):
            # Conservative all-rotation footprint check, 5 mm standoff/floor margin.
            rot=s.get('dev_rot',0);qy=x if rot==90 else s['dev_d']-hy if rot==180 else s['dev_w']-x if rot==270 else hy
            if y+qy<5:out.append('A front standoff would extend past the tray floor. Move the mounting hole back, increase Set back or choose Sleeve.');break
    return out


def bezel_plan(s):
    if s.get('bezel','none')=='none':return dict(openings=[],notes=[])
    ports,_,_=sleeve_ports(s.get('ports',[]),s)
    shapes=[dict(x=p['x'],z=p['z'],w=p['w'],h=p['h'],r=p.get('r',0),label=p.get('label') or 'Port '+str(i+1)) for i,p in enumerate(ports)]
    win=front_window(s)
    if win:shapes.append(dict(x=win['x'],z=(win['bottom']+win['top'])/2,w=win['width'],h=win['height'],r=0,label='Front window'))
    def rect(p):return (p['x']-p['w']/2,p['x']+p['w']/2,p['z']-p['h']/2,p['z']+p['h']/2)
    def gap(a,b):return max(a[0]-b[1],b[0]-a[1],a[2]-b[3],b[2]-a[3])
    obstacles=[]
    for i in range(s['u']):
        for x in (-118.2625,118.2625):
            for dz in (-15.902,15.902):
                z=i*RACK_PITCH+RACK_PITCH/2+dz;obstacles.append((x-5,x+5,z-3.5,z+3.5))
    for x in s.get('keystones',[]):obstacles.append((x-10.5,x+10.5,s['u']*RACK_PITCH/2-15,s['u']*RACK_PITCH/2+18.5))
    sw=sleeve(s)
    if sw and s.get('joint')=='screw':
        for x in sw['joints']:
            for z in sw['joint_z']:obstacles.append((x-1.7,x+1.7,z-1.7,z+1.7))
    requested=float(s.get('bezel_size',BEZEL_DEFAULT));out=[];notes=[]
    for i,p in enumerate(shapes):
        a=rect(p);available=min(requested,a[0]+126-BEZEL_WEB,126-a[1]-BEZEL_WEB,a[2]-PLATE_GAP/2-BEZEL_WEB,s['u']*RACK_PITCH-PLATE_GAP/2-a[3]-BEZEL_WEB)
        for o in obstacles:available=min(available,gap(a,o)-BEZEL_WEB)
        for j,q in enumerate(shapes):
            if j!=i:available=min(available,(gap(a,rect(q))-BEZEL_WEB)/2)
        size=max(0,math.floor((available+1e-9)*1000)/1000)
        if size<requested-1e-6:notes.append(p['label']+' bezel '+('omitted' if size==0 else 'reduced to '+str(size)+' mm')+' to keep a 2 mm web; existing openings are unchanged.')
        out.append(dict(p,size=size))
    return dict(openings=out,notes=notes)
