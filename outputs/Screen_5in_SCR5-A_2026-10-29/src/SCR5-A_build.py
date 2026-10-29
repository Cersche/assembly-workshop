"""SCR5-A explicit concept build/check/pack, Python 3.10 standard library only.

Run --review to create clearly unapproved review files. --final checks the
hardware/registration gates BEFORE any rendering or file replacement.
No repair, welding, rounding or tolerance-based vertex merging is performed.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parents[1]
CHECKS = HERE / 'checks'
SOURCE = HERE / 'src/SCR5-A.scad'
OPENSCAD = Path('C:/Program Files/OpenSCAD/openscad.exe')
CORE = 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
NAMES = ['SCR5-A plate', 'SCR5-A rear frame']


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def bounds(v):
    return [[min(p[k] for p in v), max(p[k] for p in v)] for k in range(3)]


def read_stl(path):
    data = path.read_bytes()
    count = struct.unpack_from('<I', data, 80)[0]
    assert len(data) == 84 + 50*count, 'Require binary STL, exact float32 coordinates'
    verts, tris, lookup = [], [], {}
    for i in range(count):
        c = struct.unpack_from('<9f', data, 96+50*i)
        tri = []
        for k in range(0, 9, 3):
            p = tuple(c[k:k+3])
            if p not in lookup:
                lookup[p] = len(verts)
                verts.append(p)
            tri.append(lookup[p])
        tris.append(tuple(tri))
    return verts, tris


def mesh_check(mesh):
    v, t = mesh
    assert all(math.isfinite(c) for p in v for c in p)
    edges, directed, adj = defaultdict(list), Counter(), defaultdict(set)
    degenerate = []
    volume = 0
    for i, tri in enumerate(t):
        assert len(set(tri)) == 3 and all(0 <= a < len(v) for a in tri)
        a, b, c = (v[k] for k in tri)
        area = cross(sub(b, a), sub(c, a))
        if dot(area, area) == 0:
            degenerate.append(i)
        volume += dot(a, cross(b, c))/6
        for a, b in zip(tri, tri[1:]+tri[:1]):
            edges[tuple(sorted((a, b)))].append(i)
            directed[(a, b)] += 1
    bad = [e for e, faces in edges.items() if len(faces) != 2]
    winding = [e for e in edges if directed[e] != 1 or directed[e[::-1]] != 1]
    for faces in edges.values():
        for a in faces:
            adj[a].update(faces)
    todo, shells = set(range(len(t))), 0
    while todo:
        shells += 1
        stack = [todo.pop()]
        while stack:
            for n in adj[stack.pop()]:
                if n in todo:
                    todo.remove(n)
                    stack.append(n)
    return {'vertices': len(v), 'triangles': len(t), 'edges': len(edges),
            'bounds': bounds(v), 'shells': shells, 'bad_edges': len(bad),
            'inconsistent_winding_edges': len(winding), 'degenerate_faces': degenerate,
            'signed_volume_mm3': volume,
            'pass': shells == 1 and not bad and not winding and not degenerate and volume > 0}


def parameter_checks(doc):
    p = doc['values']
    p['pcb_front_y'] = p['seat_y']+p['glass_t']+p['glass_pcb_gap']
    p['frame_front_y'] = p['pcb_front_y']-p['frame_t']-p['bearing_h']
    # Offsets, deliberately zero bearing offset, and explicit coordinate arrays
    # may be zero/negative. All dimensional scalars must be finite positive.
    offsets = {'pcb_reg_x','pcb_reg_z','active_offset_x','active_offset_z',
               'bearing_h','ribbon_x','buttons_x','id_x','seat_y'}
    for k, value in p.items():
        vals = value if isinstance(value, list) else [value]
        assert all(isinstance(v, (int,float)) and math.isfinite(v) for v in vals), k
        if k not in offsets and not isinstance(value, list):
            assert value > 0, k
    assert p['bearing_h'] >= 0
    assert p['seat_y'] >= 0
    assert 0 < p['aperture_r'] < min(p['glass_w']-p['lip_left']-p['lip_right'], p['glass_h']-p['lip_top']-p['lip_bottom'])/2
    assert p['frame_inner_w'] < p['frame_outer_w'] and p['frame_inner_h'] < p['frame_outer_h']
    assert p['insert_pilot'] < p['insert_od'] + 2*p['boss_wall']
    assert p['screw_clearance'] > 2.5
    assert p['insert_leadin'] < p['insert_seat_depth'] < p['frame_t']
    assert p['insert_length'] <= p['insert_seat_depth']
    assert p['id_depth'] < p['frame_t']
    assert p['pcb_front_y'] == p['frame_front_y']+p['frame_t']+p['bearing_h']
    assert p['frame_front_y'] > p['seat_y']+p['glass_t']
    assert p['pcb_front_y']+p['pcb_t'] <= p['seat_y']+p['total_depth']
    assert p['ribbon_cut_y'] > p['pcb_front_y']+p['pcb_t']
    assert p['buttons_y'] > p['pcb_front_y']+p['pcb_t']
    stack = p['pcb_t']+p['bearing_h']
    engagement = p['screw_length']-stack
    limits = [stack+p['minimum_engagement'], stack+p['insert_length']-p['tip_clearance']]
    assert limits[0] <= p['screw_length'] <= limits[1], 'Screw length outside conditional range'
    cx = max(p['glass_w']/2+max(p['glass_clear_left'],p['glass_clear_right']), abs(p['pcb_reg_x'])+p['pcb_w']/2+p['pcb_clear_x'])
    ch = max(p['glass_h']/2+max(p['glass_clear_top'],p['glass_clear_bottom']), abs(p['pcb_reg_z'])+p['pcb_h']/2+p['pcb_clear_z'])
    assert cx+p['pocket_wall'] < 104
    assert ch+p['pocket_wall'] < p['plate_h']/2
    assert p['frame_outer_w']/2+p['frame_clearance'] <= cx
    assert p['frame_outer_h']/2+p['frame_clearance'] <= ch
    assert p['clip_x']+p['clip_t']/2 <= cx
    clip_retraction=p['clip_hook']+p['clip_deflection_clearance']
    clip_inboard=p['clip_x']-p['clip_t']/2-clip_retraction
    assert clip_inboard > max(p['glass_w']/2,abs(p['pcb_reg_x'])+p['pcb_w']/2), 'Clips cannot retract through screen outline'
    assert p['clip_window_y'] <= p['clip_end_y'] <= p['clip_window_y']+p['clip_window_depth']
    assert p['clip_window_y']+p['clip_window_depth'] < p['pocket_depth']
    assert p['frame_front_y'] < p['clip_window_y']
    br = p['insert_od']/2+p['boss_wall']
    # Signed front-projection separation, using entire active rectangle.
    # A behind-glass interposer overlap is NOT proof of optical obstruction,
    # nor can its transparency/position be silently certified from this model.
    active = [p['active_offset_x']-p['active_w']/2-p['active_keepout'],
              p['active_offset_x']+p['active_w']/2+p['active_keepout'],
              p['centre_z']+p['active_offset_z']-p['active_h']/2-p['active_keepout'],
              p['centre_z']+p['active_offset_z']+p['active_h']/2+p['active_keepout']]
    bosses = []
    for x in [-p['hole_dx']/2,p['hole_dx']/2]:
        for z in [p['centre_z']-p['hole_dz']/2,p['centre_z']+p['hole_dz']/2]:
            x += p['pcb_reg_x']; z += p['pcb_reg_z']
            dx=max(active[0]-x,0,x-active[1]); dz=max(active[2]-z,0,z-active[3])
            bosses.append({'axis':[x,z], 'radius':br, 'signed_projection_gap':math.hypot(dx,dz)-br})
    aperture = [-p['glass_w']/2+p['lip_left'],p['glass_w']/2-p['lip_right'],
                p['centre_z']-p['glass_h']/2+p['lip_bottom'],p['centre_z']+p['glass_h']/2-p['lip_top']]
    def rr_inside(x,z):
        r=p['aperture_r']; midx=(aperture[0]+aperture[1])/2; midz=(aperture[2]+aperture[3])/2
        dx=max(abs(x-midx)-(aperture[1]-aperture[0])/2+r,0)
        dz=max(abs(z-midz)-(aperture[3]-aperture[2])/2+r,0)
        return dx*dx+dz*dz <= r*r
    active_corners = all(rr_inside(x,z) for x in active[:2] for z in active[2:])
    return {'status':'CONDITIONAL concept arithmetic; not measured hardware',
            'screw_stack_mm':stack,'screw_length_range_mm':limits,'selected_screw_length_mm':p['screw_length'],
            'nominal_engagement_mm':engagement,'insert_front_tip_gap_mm':p['insert_length']-engagement,
            'pilot_floor_mm':p['frame_t']-p['insert_seat_depth'],
            'engraving_remaining_wall_mm':p['frame_t']-p['id_depth'],
            'cavity_half_xz':[cx,ch],'active_keepout_xz':active,'aperture_xz':aperture,
            'centred_assumed_active_corners_inside_rounded_aperture':active_corners,
            'boss_projection':bosses,
            'glass_to_frame_front_gap_mm':p['frame_front_y']-(p['seat_y']+p['glass_t']),
            'required_assumed_glass_to_pcb_gap_mm':p['pcb_front_y']-(p['seat_y']+p['glass_t']),
            'clip_nominal_retraction_mm':clip_retraction,
            'retracted_clip_to_pcb_edge_mm':clip_inboard-(abs(p['pcb_reg_x'])+p['pcb_w']/2),
            'blockers':['Unverified '+k for k,v in doc['unknown_measurements'].items() if v is None] +
                       ['Bosses overlap active keepout in projection; behind-glass placement and registration require review'],
            'front_projection_clearance_verified':False,
            'glass_insertion':'Nominal rear-loaded subassembly fits cavity; interposer preassembly access and clip deflection UNKNOWN',
            'component_clearance':'Only provisional touch/FPC boxes; actual full-board component clearance UNKNOWN',
            'retention':'Four frame hooks engage pocket windows; clip strain, insertion, release and screen pressure UNKNOWN'}


def render(part, target):
    command = [str(OPENSCAD),'--export-format','binstl','-o',str(target),'-D',f'part="{part}"',str(SOURCE)]
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace')
    log = result.stdout + result.stderr
    (CHECKS/(part+'.log')).write_text(log,encoding='utf-8')
    if result.returncode or 'ERROR:' in log:
        raise RuntimeError(log)
    return log


def pack(meshes, gap):
    ET.register_namespace('',CORE)
    root=ET.Element('{'+CORE+'}model',{'unit':'millimeter','xml:lang':'en-US'})
    ET.SubElement(root,'metadata',{'name':'Title'}).text='SCR5-A INCOMPLETE CONCEPT REVIEW ONLY'
    res=ET.SubElement(root,'resources'); build=ET.SubElement(root,'build')
    layouts=[]; next_x=0
    for i,(v,t) in enumerate(meshes,1):
        # Right-handed rotation (x,y,z)->(x,-z,y). Front face rests on bed.
        rot=[(x,-z,y) for x,y,z in v]; b=bounds(rot)
        shift=(next_x-b[0][0],-b[1][0],-b[2][0])
        placed=[tuple(p[k]+shift[k] for k in range(3)) for p in rot]
        obj=ET.SubElement(res,'object',{'id':str(i),'type':'model','name':NAMES[i-1]})
        mesh=ET.SubElement(obj,'mesh'); vs=ET.SubElement(mesh,'vertices'); ts=ET.SubElement(mesh,'triangles')
        for x,y,z in placed:
            ET.SubElement(vs,'vertex',{'x':repr(x),'y':repr(y),'z':repr(z)})
        for a,b_,c in t:
            ET.SubElement(ts,'triangle',{'v1':str(a),'v2':str(b_),'v3':str(c)})
        ET.SubElement(build,'item',{'objectid':str(i)})
        layouts.append({'rotation':'(x,y,z) -> (x,-z,y)','translation_after_rotation':shift,'bounds':bounds(placed)})
        next_x=bounds(placed)[0][1]+gap
    path=HERE/'SCR5-A_screen_plate_and_frame.3mf'
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml','<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels','<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr('3D/3dmodel.model',ET.tostring(root,encoding='utf-8',xml_declaration=True))
    dump(CHECKS/'placement.json',layouts)
    return path


def reopen(path, originals):
    # Independent fresh ZIP/XML traversal, independent of writing tree.
    with zipfile.ZipFile(path) as z:
        assert set(z.namelist()) == {'[Content_Types].xml','_rels/.rels','3D/3dmodel.model'}
        rel=ET.fromstring(z.read('_rels/.rels'))
        assert len(rel)==1 and rel[0].get('Target')=='/3D/3dmodel.model'
        assert rel[0].get('Type')=='http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel'
        ct=ET.fromstring(z.read('[Content_Types].xml'))
        assert {c.get('Extension'):c.get('ContentType') for c in ct} == {'rels':'application/vnd.openxmlformats-package.relationships+xml','model':'application/vnd.ms-package.3dmanufacturing-3dmodel+xml'}
        raw=z.read('3D/3dmodel.model')
    assert b'<vertex ' in raw and b'<triangle ' in raw and b'ns0:' not in raw
    q=lambda s:'{'+CORE+'}'+s
    root=ET.fromstring(raw); assert root.get('unit')=='millimeter'
    objects=root.findall('./'+q('resources')+'/'+q('object'))
    items=root.findall('./'+q('build')+'/'+q('item'))
    assert len(objects)==len(items)==2
    result=[]; boxes=[]
    for i,(obj,item,(ov,ot)) in enumerate(zip(objects,items,originals),1):
        assert obj.get('name')==NAMES[i-1] and obj.get('id')==item.get('objectid')==str(i)
        assert item.get('transform') is None and obj.find(q('components')) is None
        v=[tuple(float(e.get(k)) for k in ('x','y','z')) for e in obj.findall('./'+q('mesh')+'/'+q('vertices')+'/'+q('vertex'))]
        t=[tuple(int(e.get(k)) for k in ('v1','v2','v3')) for e in obj.findall('./'+q('mesh')+'/'+q('triangles')+'/'+q('triangle'))]
        assert len(v)==len(ov) and t==ot
        assert all(math.isfinite(c) for p in v for c in p)
        b=bounds(v); assert b[2][0]==0
        # Recover rigid shift from first vertex, verify every coordinate and
        # every triangle index exactly (no scaling / tolerance-based matching).
        transformed=[(x,-zz,y) for x,y,zz in ov]
        shift=sub(v[0],transformed[0])
        assert all(a==tuple(c[k]+shift[k] for k in range(3)) for a,c in zip(v,transformed))
        checked=mesh_check((v,t)); assert checked['pass'],checked
        boxes.append(b); result.append({'name':obj.get('name'),**checked,'triangle_equivalence':'exact indexed triangles after rigid rotation and translation'})
    actual_gap=boxes[1][0][0]-boxes[0][0][1]; assert actual_gap>0
    return {'objects':result,'positive_gap_mm':actual_gap,'plain_tags':True,'relationships':'pass','slicer_load':'NOT TESTED'}


def preserved():
    base=json.loads((CHECKS/'baseline.json').read_text(encoding='utf-8'))
    changed=[]
    for name, old in base['sha256'].items():
        if name=='HANDOFF.md':
            continue
        if not (ROOT/name).is_file() or sha(ROOT/name)!=old:
            changed.append(name)
    assert not changed, changed
    return {'protected_files_compared':len(base['sha256'])-1,'changed':changed,'handoff':'excluded: authorized update','scope':base['roots']}


def viewers(files):
    out=ROOT/'work/mesh-viewer'
    out.mkdir(exist_ok=True)
    commands=[
        [*files,'-o',str(out/'SCR5-A-review.html'),'-t','SCR5-A — INCOMPLETE concept: separate STLs and print 3MF'],
        [str(HERE/'SCR5-A_plate.stl'),str(HERE/'SCR5-A_frame.stl'),'--as-is','-o',str(out/'SCR5-A-assembled.html'),'-t','SCR5-A — assembled common datums; no screen hardware proof'],
        [str(HERE/'SCR5-A_screen_plate_and_frame.3mf'),'-o',str(out/'SCR5-A-print.html'),'-t','SCR5-A — 3MF load proof; REVIEW ONLY']]
    for args in commands:
        subprocess.run([sys.executable,str(ROOT/'tools/mesh_viewer.py'),*args],check=True)
    return {'pages':[str(out/name) for name in ('SCR5-A-review.html','SCR5-A-assembled.html','SCR5-A-print.html')],
            'load':'mesh_viewer.py successfully parsed both STL files and final review 3MF',
            'private_artifact':'pending in Claude; no SendUserFile or private Artifact tool available on this host',
            'visual_gui_review':'not performed; no desktop control authorized'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--review',action='store_true')
    group.add_argument('--final',action='store_true')
    group.add_argument('--check-only',action='store_true')
    args=parser.parse_args()
    doc=json.loads((HERE/'SCR5-A_parameters.json').read_text(encoding='utf-8'))
    conditions=parameter_checks(doc)
    if args.final:
        raise SystemExit('FINAL EXPORT BLOCKED: '+ '; '.join(conditions['blockers']))
    dump(CHECKS/'acceptance.json',{'status':'CHECKS IN PROGRESS; no validated export; final hardware export blocked'})
    dump(CHECKS/'conditional-clearance.json',conditions)
    p=doc['values']
    render_inputs=[SOURCE,HERE/'SCR5-A_parameters.json',HERE/'src/SCR5-A_config.scad']
    if args.check_only:
        recorded=json.loads((CHECKS/'render-inputs.json').read_text(encoding='utf-8'))
        assert all(recorded[f.relative_to(HERE).as_posix()]==sha(f) for f in render_inputs), 'Render inputs changed; explicit --review rebuild required'
    if not args.check_only:
        assert OPENSCAD.name.lower()=='openscad.exe' and OPENSCAD.is_file()
        (HERE/'src/SCR5-A_config.scad').write_text('// Generated, mm; concept assumptions, not measurements.\n'+
            '\n'.join(k+'='+json.dumps(v)+';' for k,v in p.items())+'\n',encoding='utf-8')
        for part in ('plate','frame'):
            print('Rendering',part,flush=True)
            render(part,HERE/f'SCR5-A_{part}.stl')
        dump(CHECKS/'render-inputs.json',{f.relative_to(HERE).as_posix():sha(f) for f in render_inputs})
        version=subprocess.run([str(OPENSCAD),'--version'],capture_output=True,text=True,encoding='utf-8',errors='replace')
        dump(CHECKS/'build-context.json',{'python':sys.version,'openscad':version.stdout+version.stderr,
            'renderer':str(OPENSCAD),'format':'binary STL float32, no post-render repair',
            'font':'Liberation Sans Bold via OpenSCAD font lookup; exact glyph geometry is recorded in mesh hashes',
            'invocation':'python src/SCR5-A_build.py --review','automatic_build':False})
    meshes=[read_stl(HERE/f'SCR5-A_{part}.stl') for part in ('plate','frame')]
    topology={name:mesh_check(mesh) for name,mesh in zip(NAMES,meshes)}
    dump(CHECKS/'topology.json',topology)
    for name,result in topology.items():
        assert result['pass'], (name,result)
    b=topology[NAMES[0]]['bounds']
    expected=[[-126,126],[-4,20],[0.05,88.85]]
    assert all(abs(x-y)<1e-5 for a,c in zip(b,expected) for x,y in zip(a,c))
    spec=importlib.util.spec_from_file_location('scr5_geometry',HERE/'src/SCR5-A_geometry_checks.py')
    geo=importlib.util.module_from_spec(spec);spec.loader.exec_module(geo)
    focused=geo.run(sys.modules[__name__],doc,meshes,not args.check_only)
    dump(CHECKS/'geometry.json',focused)
    packpath=pack(meshes,p['print_gap']) if not args.check_only else HERE/'SCR5-A_screen_plate_and_frame.3mf'
    roundtrip=reopen(packpath,meshes)
    dump(CHECKS/'3mf-roundtrip.json',roundtrip)
    pages=viewers([str(HERE/'SCR5-A_plate.stl'),str(HERE/'SCR5-A_frame.stl'),str(packpath)])
    spec=importlib.util.spec_from_file_location('scr5_review',HERE/'src/SCR5-A_review.py')
    review=importlib.util.module_from_spec(spec);spec.loader.exec_module(review)
    review.make(sys.modules[__name__])
    gate=subprocess.run([sys.executable,str(Path(__file__)),'--final'],capture_output=True,text=True,encoding='utf-8')
    assert gate.returncode != 0 and 'FINAL EXPORT BLOCKED' in gate.stderr
    (CHECKS/'final-gate.log').write_text(gate.stdout+gate.stderr,encoding='utf-8')
    dump(CHECKS/'viewers.json',pages)
    dump(CHECKS/'preservation.json',preserved())
    hashfiles=list((HERE/'src').glob('*.py'))+list((HERE/'src').glob('*.scad'))+list(HERE.glob('*.stl'))+list((HERE/'checks').glob('*.stl'))+[HERE/'SCR5-A_parameters.json',packpath]
    dump(CHECKS/'hashes.json',{f.relative_to(HERE).as_posix():sha(f) for f in hashfiles})
    dump(CHECKS/'acceptance.json',{'status':'INCOMPLETE REVIEW ONLY; final export blocked',
        'topology':'pass', 'plate_bounds':b, '3mf':'independent roundtrip pass',
        'hardware':'BLOCKED: see conditional-clearance.json',
        'physical':'NOT PRINTED; fit/retention/access/ribbon reach/strength UNKNOWN',
        'self_intersection':'numerical triangle screen pass; see self-intersection.json for scope',
        'assembly_intersection':focused['assembly'],
        'slots_and_engraving':'measured from parsed meshes; see geometry.json',
        'private_artifact':'private Artifact publishing pending in Claude'})
    print(json.dumps({'topology':topology,'3mf_gap':roundtrip['positive_gap_mm'],'status':'INCOMPLETE REVIEW ONLY'},indent=2))


if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        dump(CHECKS/'acceptance.json',{'status':'FAILED CHECKS — review files incomplete/stale; no validated export','error':str(exc),'final':'BLOCKED'})
        raise
