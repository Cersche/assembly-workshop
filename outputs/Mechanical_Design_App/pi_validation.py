"""Bounded surface screening for the pinned Pi reference; never a solid-fit claim."""
import hashlib
import json
import math
from pathlib import Path
from functools import lru_cache
ROOT = Path(__file__).resolve().parent

def reference():
    manifest = json.loads((ROOT/'pi_reference_manifest.json').read_text())
    raw = (ROOT/'pi_reference.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != manifest['sha256'] or manifest['units'] != 'mm':
        raise ValueError('Pi reference hash or units mismatch.')
    return json.loads(raw), manifest

def clip(poly, axis, limit):
    out = []
    for i, p in enumerate(poly):
        q = poly[(i+1)%len(poly)]
        dp = sum(a*b for a,b in zip(axis,p))-limit
        dq = sum(a*b for a,b in zip(axis,q))-limit
        if dp <= 0: out.append(p)
        if dp < 0 < dq or dq < 0 < dp:
            t = dp/(dp-dq)
            out.append(tuple(p[k]+t*(q[k]-p[k]) for k in range(3)))
    return out

def gusset_hits(part, crest_raise=0):
    counts = {}
    vs = part['vertices']
    for cx in [-46,-34,34,46]:
        top = 15.5+crest_raise
        slope = (top-10.2)/11
        planes = [((1,0,0),cx+1),((-1,0,0),1-cx),((0,1,0),22),((0,-1,0),-9),((0,0,-1),-9.7),((0,0,1),top),((0,slope,1),top+slope*11)]
        hits = 0
        for ids in part['triangles']:
            tri = [vs[i] for i in ids]
            if max(v[0] for v in tri)<cx-1 or min(v[0] for v in tri)>cx+1 or min(v[1] for v in tri)>22 or max(v[1] for v in tri)<9 or min(v[2] for v in tri)>top+.5: continue
            poly = [(v[0],v[1],v[2]-.5) for v in tri]
            for a,lim in planes:
                poly=clip(poly,a,lim-.00001)
                if not poly: break
            hits += bool(poly)
        counts[str(cx)] = hits
    return counts

def other_hits(part):
    regions={}
    for cx in [-40,40]:
        regions['ear_'+str(cx)]=[((1,0,0),cx+7),((-1,0,0),7-cx),((0,1,0),11.3),((0,-1,0),-8.3),((0,0,1),29),((0,0,-1),-10)]
    for cx in [-40.5,17.5]:
        for cy in [16.5,65.5]:
            planes=[((0,0,1),15.999),((0,0,-1),-10)]
            for i in range(48):
                a=(i+.5)*2*math.pi/48; nx,ny=math.cos(a),math.sin(a)
                planes.append(((nx,ny,0),nx*cx+ny*cy+3.5*math.cos(math.pi/48)))
            regions[f'standoff_{cx}_{cy}']=planes
    triangles=[[part['vertices'][i] for i in ids] for ids in part['triangles']]
    result={}
    for name,planes in regions.items():
        hits=0
        for tri in triangles:
            if any(all(sum(a*b for a,b in zip(axis,v))>lim for v in tri) for axis,lim in planes): continue
            poly=tri
            for axis,lim in planes:
                poly=clip(poly,axis,lim-.00001)
                if not poly: break
            hits+=bool(poly)
        result[name]=hits
    return result

def pcb_measurements(part):
    """Identify the PCB by connectivity and documented mesh signature, not ring Z."""
    parent = list(range(len(part['vertices'])))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for a, b, c in part['triangles']:
        a = find(a)
        parent[find(b)] = a
        parent[find(c)] = a
    components = {}
    for i, vertex in enumerate(part['vertices']):
        components.setdefault(find(i), []).append(vertex)
    # Signature documented by work/analyze_pi.py and work/align_pi.py.
    candidates = [vs for vs in components.values() if len(vs) == 6300]
    if len(candidates) != 1:
        return {'identified': False, 'reason': 'Expected one documented 6,300-vertex PCB component.'}
    board = candidates[0]
    bounds = [[min(v[k] for v in board) for k in range(3)],
              [max(v[k] for v in board) for k in range(3)]]
    rings = []
    for x in [-40.5, 17.5]:
        for y in [16.5, 65.5]:
            points = [v for v in board if abs(math.hypot(v[0]-x, v[1]-y)-1.35) < .003]
            quadrants = {(v[0] >= x, v[1] >= y) for v in points}
            center = [(min(v[k] for v in points)+max(v[k] for v in points))/2
                      for k in [0, 1]] if points else None
            rings.append({'expected_xy': [x,y], 'measured_xy': center,
                          'vertices': len(points), 'quadrants': len(quadrants),
                          'surface_z_levels': sorted({round(v[2], 5) for v in points})})
    return {'identified': True, 'component_vertices': len(board), 'bounds': bounds,
            'rings': rings, 'underside_gap_to_standoff_mm': bounds[0][2]-16,
            'xy_match': all(r['quadrants'] == 4 and r['vertices'] >= 8 and
                            all(abs(a-b) < .003 for a,b in zip(r['expected_xy'],r['measured_xy']))
                            for r in rings)}


def separation_measurements(part):
    """Coordinate bounds are sufficient only for the separated objects named here."""
    low = [min(v[k] for v in part['vertices']) for k in range(3)]
    return {'pi_min_y': low[1], 'pi_min_z': low[2],
            'faceplate_y_gap_mm': low[1]-8,
            'socket_rail_y_gap_mm': low[1]-8,
            'tray_floor_z_gap_mm': low[2]-10}


def joint_measurements(assembly):
    measurements=[]
    parts={p['id']:p for p in assembly['parts']}
    for name,ys,radius in [('tray',[8.3,11.3],1.7),('faceplate',[8],2.1)]:
        for x in [-40,40]:
            for y in ys:
                points=[v for v in parts[name]['vertices'] if abs(v[1]-y)<.003 and abs(math.hypot(v[0]-x,v[2]-21)-radius)<.003]
                center=[(min(v[k] for v in points)+max(v[k] for v in points))/2 for k in [0,2]] if points else None
                quadrants={(v[0]>=x,v[2]>=21) for v in points}
                measurements.append({'part':name,'section_y':y,'expected_xz':[x,21],
                                     'measured_xz':center,'vertices':len(points),'quadrants':len(quadrants)})
    return {'sections':measurements,'axes_match':all(r['quadrants']==4 and r['vertices']>=8 and
            all(abs(a-b)<.003 for a,b in zip(r['measured_xz'],r['expected_xz'])) for r in measurements),
            'tolerance_mm':.003,
            'nominal_source_clearances_mm':{'tongue_side_each':.15,'tongue_vertical_each':.15,'tongue_tip':.2,'boss_to_ear':.3},
            'limits':'Bore ring centers verify baseline joint axes at X +/-40 Z21 along Y. Nominal clearances follow pinned SCAD dimensions, not as-printed fit or hardware/driver access. Pilot-only proposals preserve these axes.'}


def head_surface_hits(part, x, diameter, height):
    """Bracket a nominal Y-axis cylinder with inscribed/circumscribed 48-gons."""
    radius=diameter/2
    lower,upper=11.301,11.3+height
    if upper <= lower:
        return {'inner':0,'outer':0,'status':'unknown'}
    counts={}
    for kind,apothem in [('inner',radius*math.cos(math.pi/48)),('outer',radius)]:
        planes=[((0,-1,0),-lower),((0,1,0),upper)]
        for i in range(48):
            angle=(i+.5)*2*math.pi/48
            nx,nz=math.cos(angle),math.sin(angle)
            planes.append(((nx,0,nz),nx*x+nz*21+apothem))
        count=0
        for ids in part['triangles']:
            tri=[part['vertices'][i] for i in ids]
            # Enclose the circumscribed polygon for conservative broad-phase screening.
            outer_radius=radius/math.cos(math.pi/48)
            if any(max(v[k] for v in tri)<lo or min(v[k] for v in tri)>hi for k,lo,hi in
                   [(0,x-outer_radius,x+outer_radius),(1,lower,upper),(2,21-outer_radius,21+outer_radius)]):
                continue
            poly=tri
            for axis,limit in planes:
                poly=clip(poly,axis,limit-.00001)
                if not poly:break
            count+=bool(poly)
        counts[kind]=count
    counts['status']='fail' if counts['inner'] else ('pass' if not counts['outer'] else 'unknown')
    return counts


@lru_cache(maxsize=12)
def _head_screen(diameter,height,asset_hash,assembly_hash,source_hash,manifest_hash):
    part,manifest=reference()
    if source_hash!=manifest['baseline_source_sha256'] or assembly_hash!=manifest.get('baseline_assembly_sha256'):
        return {'status':'unknown','detail':'Head screening requires pinned baseline source and meshes.'}
    assembly=json.loads((ROOT/'assembly.json').read_text(encoding='utf-8'))
    measurements=[]
    for x in [-40,40]:
        for target in [part]+assembly['parts']:
            measurements.append(dict(axis_x=x,target=target['id'],**head_surface_hits(target,x,diameter,height)))
    status='fail' if any(m['status']=='fail' for m in measurements) else ('pass' if all(m['status']=='pass' for m in measurements) else 'unknown')
    return {'status':status,'measurements':measurements,'head_diameter_mm':diameter,'head_height_mm':height,
            'method':'head-cylinder-surface-bracket-v1','bearing_contact_exclusion_mm':.001,
            'clipping_epsilon_mm':.00001,'polygon_sides':48,
            'limits':'Nominal head cylinder surface screen against Pi/tray/faceplate; inner intersections FAIL, outer-only intersections UNKNOWN. No outer intersection passes only the surface screen, not containment, tool access, tolerances or physical fit. Ear bearing contact excluded by +0.001 mm Y. Driver/shaft/handle envelope and insertion path remain UNKNOWN.'}


def head_screen(screw):
    diameter,height=screw.get('head_diameter'),screw.get('head_height')
    if any(type(v) not in [int,float] or not math.isfinite(v) or v<=0 for v in [diameter,height]):
        return {'status':'unknown','detail':'Documented head diameter and height are required; no envelope inferred.'}
    if screw.get('diameter')!=3 or screw.get('pitch')!=.5:
        return {'status':'unknown','detail':'This head screen applies only to the pinned M3x0.5 Pi4 joint axes.'}
    try:
        reference()
        return _head_screen(diameter,height,*[hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                    for name in ['pi_reference.json','assembly.json','pi4_baseline.scad','pi_reference_manifest.json']])
    except (OSError,ValueError,KeyError) as exc:
        return {'status':'unknown','detail':str(exc)}


def access_assessment(screw=None, insert=None):
    """Evidence requirements, not invented tool/accessory geometry or a fit pass."""
    screw,insert=screw or {},insert or {}
    return [
        {'name':'Screwdriver approach','status':'unknown',
         'known':{'drive':screw.get('drive'),'bearing_y_mm':11.3,'approach':'from rear (+Y), toward -Y'},
         'required':'Exact driver shaft/bit/handle envelope, usable reach, approach/rotation path, and any surrounding rack geometry.',
         'limit':'Drive size alone does not define the complete tool envelope.'},
        {'name':'Insert installation','status':'unknown',
         'known':{'part_number':insert.get('part_number'),'length_mm':insert.get('length'),'boss_entrance_y_mm':8},
         'required':'Exact insert outside diameter and installation-tip envelope/reach, documented installation procedure, material, and installation sequence.',
         'limit':'Install tool and hot material clearance are not established by the nominal insert length.'},
        {'name':'Pi insertion/removal path','status':'unknown','known':{'final_pose':'pinned reference transform'},
         'required':'Explicit assembly order and motion path, including mounting fasteners and accessories, followed by swept-volume or equivalent path checks.',
         'limit':'A clear final pose does not prove that parts can be inserted or removed.'},
        {'name':'Connector/cable/accessory access','status':'unknown','known':{'bare_board_reference':'included'},
         'required':'Actual cable plug/boot/bend envelopes and intended ports, SD-card service path, heatsink/fan or other accessory geometry.',
         'limit':'Bare-board geometry does not supply connected-cable or accessory envelopes.'},
        {'name':'Rack engagement and physical sign-off','status':'unknown','known':{'rack_fit':'unverified'},
         'required':'Mating rack geometry and installation path; actual hardware/material selection; separately approved coupon/prototype and recorded fit/load results.',
         'limit':'Digital surface screening is not a strength or physical-fit certification.'}
    ]


def solid_result(log, empty, returncode=1):
    """OpenSCAD uses code 1 for a valid empty intersection; require that diagnostic."""
    lower = log.lower()
    if any(word in lower for word in ['error', 'warning', 'not closed', 'unable to', 'failed']):
        return 'unknown'
    if empty and returncode == 1 and 'current top level object is empty.' in lower:
        return 'pass'
    if not empty and returncode == 0:
        return 'fail'
    return 'unknown'


def joint_evidence(source_hash):
    path = ROOT/'joint_validation.json'
    try:
        report = json.loads(path.read_text(encoding='utf-8'))
        if report['source_sha256'] != source_hash or report['schema'] != 1:
            raise ValueError('Joint evidence does not match current baseline source.')
        checks=[]
        for name in ['tray_faceplate', 'nominal_pcb', 'positive_joint_clash']:
            record=report['results'][name]
            state=solid_result(record['log'], record['empty'], record['returncode'])
            expected='fail' if name == 'positive_joint_clash' else 'pass'
            checks.append({'name':name, 'status':'pass' if state == expected else ('unknown' if state == 'unknown' else 'fail'),
                           'actual_intersection_status':state,
                           'expression':record['expression'], 'log_sha256':hashlib.sha256(record['log'].encode()).hexdigest()})
        return {'status':'fail' if any(c['status']=='fail' for c in checks) else ('pass' if all(c['status']=='pass' for c in checks) else 'unknown'),
                'checks':checks,'evidence_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                'limits':'Tray/faceplate seating excluded by translating faceplate -0.001 mm along Y; nominal PCB seating excluded by +0.001 mm Z. Positive regression shifts faceplate +0.4 mm Y. Nominal PCB is not detailed-Pi solid validation.'}
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return {'status':'unknown','detail':str(exc)}


@lru_cache(maxsize=1)
def _validated(asset_hash, source_hash, manifest_hash, evidence_hash, assembly_hash):
    part, manifest = reference()
    checks=[]
    def add(name,status,detail): checks.append(dict(name=name,status=status,detail=detail))
    add('Pinned Pi reference','pass','SHA-256 verified; millimeters; baked assembly transform. Reference only.')
    baseline_ok = source_hash == manifest['baseline_source_sha256']
    add('Supported mechanical baseline','pass' if baseline_ok else 'unknown','Source SHA-256 '+source_hash+'. Screening envelopes apply only to the pinned clearance-v2 source and pilot-only proposals.')
    hits=gusset_hits(part)
    add('Four gussets: vertical surface screening','pass' if baseline_ok and not any(hits.values()) else ('fail' if any(hits.values()) else 'unknown'), 'Triangle clipping after lowering Pi 0.5 mm; inward clipping epsilon 0.00001 mm. Hits: '+json.dumps(hits)+'. Surface screening, not global minimum distance or solid containment.')
    pcb=pcb_measurements(part)
    add('PCB hole XY alignment','pass' if baseline_ok and pcb.get('xy_match') else 'unknown',
        'Connected PCB component; four mounting rings sampled at documented radius 1.35 mm with 0.003 mm radial/center tolerance. Expected pitch 58 x 49 mm. '+json.dumps(pcb.get('rings',[]))+'. This does not approve mounting fasteners.')
    seating = pcb.get('identified') and abs(pcb['underside_gap_to_standoff_mm']) < .003
    add('PCB mounting placement','pass' if baseline_ok and seating else 'unknown',
        'Connected 6,300-vertex PCB component bounds, not inset mounting-ring surfaces. Nominal underside and standoff top Z16; tolerance 0.003 mm. '+json.dumps({k:v for k,v in pcb.items() if k not in ['rings','xy_match']})+'. Ring surfaces at Z16.01001 do not define the PCB underside. Nominal model seating only; printed contact remains unknown.')
    separated=separation_measurements(part)
    add('Pi versus faceplate, socket rails and floor','pass' if baseline_ok and all(separated[k]>0 for k in ['faceplate_y_gap_mm','socket_rail_y_gap_mm','tray_floor_z_gap_mm']) else 'unknown',
        'Axis-aligned separation of complete Pi reference from pinned faceplate/rail Y<=8 and floor Z<=10: '+json.dumps(separated)+'. Bounds separation, not a global minimum-distance calculation.')
    other=other_hits(part)
    add('Ear and standoff surface screening','pass' if baseline_ok and not any(other.values()) else ('fail' if any(other.values()) else 'unknown'),'Convex envelopes, standoff contact excluded by 0.001 mm; inward epsilon 0.00001 mm. Hits: '+json.dumps(other)+'. Surface test excludes containment claims.')
    assembly=json.loads((ROOT/'assembly.json').read_text(encoding='utf-8'))
    alignment=joint_measurements(assembly)
    assembly_ok=assembly_hash==manifest.get('baseline_assembly_sha256')
    add('Baseline joint axis alignment','pass' if baseline_ok and assembly_ok and alignment['axes_match'] else 'unknown',json.dumps(alignment))
    joint=joint_evidence(source_hash)
    add('Tray/faceplate and nominal PCB solid regression',joint['status'],json.dumps(joint))
    add('Whole-Pi solid interference','unknown','Non-manifold reference: CGAL conversion failed in baseline evidence. Empty output after conversion error is inconclusive.')
    add('Other assembly clearances','unknown','Complete Pi is separated from faceplate/floor/rails by bounds; gusset/ear/standoff checks screen triangle surfaces. Whole-object containment, insertion path and accessory geometry remain unestablished.')
    add('Access and physical fit','unknown','Cable/connector envelopes, driver and installation access, rack fit, material, strength and printed tolerances require further evidence/testing.')
    add('Reference provenance','unknown','Upstream source units/provenance and redistribution license remain unresolved. Existing local 3MF explicitly declares millimeters.')
    return {'status':'fail' if any(c['status']=='fail' for c in checks) else 'incomplete','checks':checks,'reference':manifest,'method':'pi4-surface-screen-v2','manufacturing_reference_included':False,'access_assessment':access_assessment()}

def validate():
    try:
        # Rehash on every request so cached evidence cannot hide modified assets.
        reference()
        return _validated(hashlib.sha256((ROOT/'pi_reference.json').read_bytes()).hexdigest(),hashlib.sha256((ROOT/'pi4_baseline.scad').read_bytes()).hexdigest(),hashlib.sha256((ROOT/'pi_reference_manifest.json').read_bytes()).hexdigest(),hashlib.sha256((ROOT/'joint_validation.json').read_bytes()).hexdigest() if (ROOT/'joint_validation.json').exists() else 'missing',hashlib.sha256((ROOT/'assembly.json').read_bytes()).hexdigest())
    except (OSError,ValueError,KeyError) as exc:
        return {'status':'incomplete','checks':[{'name':'Pi reference validation','status':'unknown','detail':str(exc)}]}
