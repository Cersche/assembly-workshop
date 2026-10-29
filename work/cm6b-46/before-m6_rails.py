"""Opt-in split rails. Nominal digital clearances only; physical fit remains UNKNOWN."""
import math
import re
import m6_fidelity

KEYS = ('m6_rails', 'm6_rail_t', 'm6_joint_x', 'm6_joint_z', 'm6_pocket_profile', 'm6_usable_depth', 'test_id') + m6_fidelity.KEYS
NEEDS = 'Split rails need M6 hardware turned on.'
OPENING = 'A front opening or keystone sits in front of a split-rail stub; move or remove it.'
WIDE = 'The device is too wide for split-rail stubs and rack slot clearance.'
DEPTH = 'The rails are longer than the usable depth; use a shorter device or more usable depth.'
WALL = 'Each M6 pilot needs at least 2 mm of wall to the pocket and plate edge, and clearance from the rack slots.'

def distance(p, a, b):
    dx, dz = b[0]-a[0], b[1]-a[1]
    t = max(0, min(1, ((p[0]-a[0])*dx+(p[1]-a[1])*dz)/(dx*dx+dz*dz)))
    return math.hypot(p[0]-a[0]-t*dx, p[1]-a[1]-t*dz)

def inside(p, poly):
    odd = False
    for a,b in zip(poly, poly[1:]+poly[:1]):
        if (a[1]>p[1]) != (b[1]>p[1]) and p[0] < (b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0]:
            odd = not odd
    return odd

def validate(spec, eq):
    if spec.get('m6_joint') is not True:
        raise ValueError(NEEDS)
    if spec.get('device_mount') != 'flat' or spec.get('joint') != 'screw':
        raise ValueError('Split rails need Sits flat and a screw joint.')
    if spec.get('rear_support') or spec.get('second') or spec.get('_pair') or spec.get('front_position','today') != 'today':
        raise ValueError('Split rails cannot be combined with a rear bracket, a second device or a moved front position.')
    if spec.get('bezel','none') != 'none':
        raise ValueError('Split rails do not yet support a front-edge bezel.')
    if any(spec.get(k) for k in ('dev_off_y','dev_rot','feet','drives','coupon','protrusions','labels')):
        raise ValueError('Split rails need an unrotated device without feet, drives, coupons, keep-clear zones or faceplate labels; front/back offset must be zero.')
    w = eq.num(spec.get('dev_w'), 'Device width', 10, 250)
    d = eq.num(spec.get('dev_d'), 'Device depth', 10, 250)
    h = eq.num(spec.get('dev_h'), 'Device height', 1, 220)
    u = spec.get('u',1)
    if type(u) is not int or not 1 <= u <= 5:
        raise ValueError('Choose a height from 1U to 5U.')
    top = u*44.45-.025
    t = eq.num(spec.get('m6_rail_t',3.3),'Rail thickness',2.5,8)
    usable = eq.num(spec.get('m6_usable_depth',240),'Usable depth',40,300)
    if spec.get('m6_rail_len',d+2) > usable:
        raise ValueError(DEPTH)
    if d+2 < 38:
        raise ValueError('Split rails need at least 38 mm of rail length for the screw access bays.')
    off = eq.num(spec.get('dev_off_x',0),'Left/right offset',-110,110)
    def pair(key, default, lo, hi):
        raw = spec.get(key, default)
        if not isinstance(raw,list) or len(raw)!=2 or any(isinstance(v,bool) for v in raw):
            raise ValueError(key+' must contain two positions in generator coordinates.')
        out = [eq.num(v,key,lo,hi) for v in raw]
        if out[1]<=out[0]:
            raise ValueError(key+' positions must be in increasing order.')
        return out
    # Explicit settings, never inferred from a bounding box (Brian's task-43 correction).
    xs = pair('m6_joint_x',[-65.8,65.8],-125,125)
    zs = pair('m6_joint_z',[8.6,35.825],0,top)
    if xs[1]-xs[0]<24 or any(abs(x)+5.8 > 113.2625-2 for x in xs) or max(abs(off-w/2),abs(off+w/2))+t>111.2625:
        raise ValueError(WIDE)
    raw = spec.get('m6_pocket_profile',[[off-w/2,t+.025],[off+w/2,t+.025],[off+w/2,t+h+.025],[off-w/2,t+h+.025]])
    if not isinstance(raw,list) or not 4<=len(raw)<=32:
        raise ValueError('The split-rail pocket needs 4 to 32 X/Z points.')
    poly = []
    for p in raw:
        if not isinstance(p,list) or len(p)!=2 or any(isinstance(v,bool) for v in p):
            raise ValueError('Each pocket point needs X and Z in millimetres.')
        poly.append([eq.num(p[0],'Pocket X',-110,110),eq.num(p[1],'Pocket Z',2.525,top-2.5)])
    if any(a==b for a,b in zip(poly,poly[1:]+poly[:1])):
        raise ValueError('Pocket points must be distinct.')
    # The pocket is a simple convex or concave polygon. Reject crossings, including collinear contacts.
    edges = list(zip(poly,poly[1:]+poly[:1]))
    def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    for i,(a,b) in enumerate(edges):
        for j,(c,e) in enumerate(edges):
            if j<=i+1 or (i==0 and j==len(edges)-1):continue
            if orient(a,b,c)*orient(a,b,e)<=0 and orient(c,e,a)*orient(c,e,b)<=0:
                if max(min(a[0],b[0]),min(c[0],e[0]))<=min(max(a[0],b[0]),max(c[0],e[0])) and max(min(a[1],b[1]),min(c[1],e[1]))<=min(max(a[1],b[1]),max(c[1],e[1])):
                    raise ValueError('Pocket outline must not cross or touch itself.')
    if max(x for x,z in poly)-min(x for x,z in poly)>w+.001 or max(z for x,z in poly)-min(z for x,z in poly)>h+.001:
        raise ValueError('Pocket profile exceeds the device envelope.')
    if zs[0]-6 < 2.525-1e-9 or top-zs[1]-6 < 2.5-1e-9 or zs[1]-zs[0] < 14:
        raise ValueError('Screw access bays must keep at least 2.5 mm of floor, top and connecting wall.')
    wall = min(distance([x,z],a,b)-3.8 for x in xs for z in zs for a,b in edges)
    if wall < 2-1e-8 or any(inside([x,z],poly) or z-3.8<2.025 or top-z-3.8<2 for x in xs for z in zs):
        raise ValueError(WALL)
    # Full-height stubs may not cover an opening or a golden keystone's whole block.
    for x in xs:
        if any(abs(float(p['x'])+off-x)<float(p['w'])/2+5.8+2 for p in spec.get('ports',[])) or any(abs(k-x)<10.5+5.8+2 for k in spec.get('keystones',[])):
            raise ValueError(OPENING)
    ident = spec.get('test_id','')
    if not isinstance(ident,str) or (ident and not re.fullmatch(r'[A-Za-z0-9-]{1,16}',ident)):
        raise ValueError('Test ID must be at most 16 letters, numbers or hyphens.')
    if ident and (t<3 or max(z for x,z in poly)>top-3):
        raise ValueError('Engraved rail IDs need at least 3 mm of top material before engraving.')
    result = dict(m6_rails=True,m6_joint=True,m6_rail_t=t,m6_joint_x=xs,m6_joint_z=zs,m6_pocket_profile=poly,
                m6_usable_depth=usable,test_id=ident)
    result.update(m6_fidelity.validate(spec,eq))
    return result

def clean(spec, eq):
    settings = validate(spec,eq)
    # Reuse ordinary input and opening validation on a narrow disposable surrogate. The rail-specific
    # shape and rack-slot rules above replace the legacy full-tray width and joint layout rules.
    proxy = dict(spec,m6_rails=False,m6_joint=False,dev_w=min(float(spec['dev_w']),max(10,170-2*abs(float(spec.get('dev_off_x',0))))),standoff=0)
    for key in KEYS:proxy.pop(key,None)
    s = eq.clean(proxy)
    s.update(dev_w=eq.num(spec['dev_w'],'Device width',10,250),dev_off_x=eq.num(spec.get('dev_off_x',0),'Left/right offset',-110,110))
    s.update(settings)
    s.pop('joint_x',None)
    return s

def check_connected(mesh):
    neighbors = {}
    for a,b,c in mesh['triangles']:
        for i,j in ((a,b),(b,c),(c,a)):
            neighbors.setdefault(i,set()).add(j)
            neighbors.setdefault(j,set()).add(i)
    seen = set()
    todo = [next(iter(neighbors))]
    while todo:
        i=todo.pop()
        if i not in seen:
            seen.add(i)
            todo.extend(neighbors[i]-seen)
    if len(seen)!=len(neighbors):
        raise ValueError('Each split-rail part must be one connected closed solid.')
