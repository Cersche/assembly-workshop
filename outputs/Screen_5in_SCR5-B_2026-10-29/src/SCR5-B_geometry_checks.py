"""Focused mesh measurements and intersection screening; standard library.

Topology always uses exact parsed coordinates in the builder. This supplementary
triangle intersection screen uses 1e-9 mm predicate tolerance, never moves vertices.
"""
import copy
import math
from pathlib import Path
import subprocess


def y_hits(mesh, x, z):
    """Intersections of line (x,Y,z) with triangles, in original coordinates."""
    v,t=mesh; result=[]
    for tri in t:
        a,b,c=(v[k] for k in tri)
        den=(b[2]-c[2])*(a[0]-c[0])+(c[0]-b[0])*(a[2]-c[2])
        if den==0:
            continue
        u=((b[2]-c[2])*(x-c[0])+(c[0]-b[0])*(z-c[2]))/den
        w=((c[2]-a[2])*(x-c[0])+(a[0]-c[0])*(z-c[2]))/den
        if u>=-1e-10 and w>=-1e-10 and u+w<=1+1e-10:
            result.append(u*a[1]+w*b[1]+(1-u-w)*c[1])
    return sorted(set(result))


def strict_triangle_screen(b, mesh):
    """Sweep AABBs; detect coplanar area overlap and transverse crossings.

    Incident edge pairs are excluded: they have their intended exact shared edge
    and are already checked for closure and winding. Vertex-only pairs are tested.
    This is a numerical digital screen, not an exact-arithmetic solid proof.
    """
    v,t=mesh; eps=1e-9
    tris=[tuple(v[k] for k in tri) for tri in t]
    boxes=[b.bounds(tri) for tri in tris]
    normals=[b.cross(b.sub(tri[1],tri[0]),b.sub(tri[2],tri[0])) for tri in tris]
    order=sorted(range(len(t)),key=lambda i:boxes[i][0][0])
    candidates=0; coplanar=0; bad=[]; active=[]

    def segment_triangle(p,q,tri):
        e1=b.sub(tri[1],tri[0]);e2=b.sub(tri[2],tri[0]);d=b.sub(q,p)
        h=b.cross(d,e2); det=b.dot(e1,h)
        if abs(det)<1e-14:
            return None
        s=b.sub(p,tri[0]);u=b.dot(s,h)/det
        qq=b.cross(s,e1);w=b.dot(d,qq)/det;tt=b.dot(e2,qq)/det
        if -eps<=u<=1+eps and -eps<=w and u+w<=1+eps and -eps<=tt<=1+eps:
            return tuple(p[k]+tt*d[k] for k in range(3))
        return None

    def area_overlap(a,c,n):
        drop=max(range(3),key=lambda k:abs(n[k]));axes=[k for k in range(3) if k!=drop]
        aa=[tuple(p[k] for k in axes) for p in a];cc=[tuple(p[k] for k in axes) for p in c]
        orient=lambda p,q,r:(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
        sign=1 if orient(*cc)>0 else -1
        poly=aa
        for u,w in zip(cc,cc[1:]+cc[:1]):
            result=[]
            if not poly:
                break
            for p,q in zip(poly,poly[1:]+poly[:1]):
                dp=sign*orient(u,w,p);dq=sign*orient(u,w,q)
                pin=dp>=0; qin=dq>=0
                if pin:
                    result.append(p)
                if pin!=qin:
                    ratio=dp/(dp-dq)
                    result.append(tuple(p[k]+ratio*(q[k]-p[k]) for k in range(2)))
            poly=result
        # Translate before shoelace to avoid subtracting large nearly equal areas.
        if len(poly)<3:
            return False
        poly=[tuple(p[k]-poly[0][k] for k in range(2)) for p in poly]
        area=abs(sum(p[0]*q[1]-p[1]*q[0] for p,q in zip(poly,poly[1:]+poly[:1])))/2
        return area>1e-10

    for i in order:
        bb=boxes[i]; active=[j for j in active if boxes[j][0][1]>=bb[0][0]]
        for j in active:
            bc=boxes[j]
            if any(bb[k][1]<bc[k][0] or bc[k][1]<bb[k][0] for k in (1,2)):
                continue
            shared=set(t[i])&set(t[j])
            if len(shared)>=2:
                continue
            candidates+=1
            n=normals[i];norm=math.sqrt(b.dot(n,n))
            distances=[b.dot(n,b.sub(p,tris[i][0]))/norm for p in tris[j]]
            if min(distances)>eps or max(distances)<-eps:
                continue
            if all(abs(d)<eps for d in distances):
                coplanar+=1
                if area_overlap(tris[i],tris[j],n):
                    bad.append([j,i,'coplanar area overlap'])
            else:
                allowed=[v[k] for k in shared]
                for a,c in ((tris[i],tris[j]),(tris[j],tris[i])):
                    for p,q in zip(a,a[1:]+a[:1]):
                        hit=segment_triangle(p,q,c)
                        if hit is not None and not any(max(abs(x-y) for x,y in zip(hit,sv))<eps for sv in allowed):
                            bad.append([j,i,'nonincident crossing'])
                            break
                    if bad and bad[-1][:2]==[j,i]:
                        break
        active.append(i)
    return {'candidate_nonedge_pairs':candidates,'coplanar_pairs':coplanar,
            'intersections':bad,'pass':not bad,'predicate_tolerance_mm':eps,
            'scope':'AABB sweep, incident edges excluded; coplanar overlap and transverse segment/triangle screen; not exact-arithmetic certification'}


def run(b, doc, meshes, render_probes=True):
    p=doc['values'];plate,frame=meshes
    slots=[]
    for x in (-p['slot_x'],p['slot_x']):
        for z in p['slot_z']:
            free=[(x,z),(x-4.9,z),(x+4.9,z),(x,z-3.4),(x,z+3.4)]
            solid=[(x-5.1,z),(x+5.1,z),(x,z-3.6),(x,z+3.6)]
            assert all(not y_hits(plate,xx,zz) for xx,zz in free)
            assert all(y_hits(plate,xx,zz) for xx,zz in solid)
            verts=[v for v in plate[0] if abs(v[0]-x)<=5.0001 and abs(v[2]-z)<=3.5001]
            measured=b.bounds(verts)
            assert abs(measured[0][1]-measured[0][0]-10)<2e-5
            assert abs(measured[2][1]-measured[2][0]-7)<2e-5
            slots.append({'centre_xz':[x,z],'parsed_boundary_bounds':measured,'horizontal_10x7':True,'through_at_five_interior_rays':True})
    # Verify no front-facing opaque plate at centred assumed active corners.
    aperture_verts=[v for v in plate[0] if v[1]==-p['plate_t'] and abs(v[0])<60 and 8<v[2]<81]
    aperture_bounds=b.bounds(aperture_verts)
    assert abs(aperture_bounds[0][1]-aperture_bounds[0][0]-(p['glass_w']-p['lip_left']-p['lip_right']))<2e-5
    assert abs(aperture_bounds[2][1]-aperture_bounds[2][0]-(p['glass_h']-p['lip_top']-p['lip_bottom']))<2e-5
    assert abs(sum(aperture_bounds[0])/2-(p['lip_left']-p['lip_right'])/2)<2e-5
    assert abs(sum(aperture_bounds[2])/2-(p['centre_z']+(p['lip_bottom']-p['lip_top'])/2))<2e-5
    active=b.parameter_checks(doc)['active_keepout_xz']
    for x in active[:2]:
        for z in active[2:]:
            assert not [y for y in y_hits(plate,x,z) if -4.001<=y<=0.001]
    # Compare exact source mesh slot boundary vertices, before tolerant bounds.
    old_path=b.ROOT/'outputs/Screen_5in_SCR5-A_2026-10-29/SCR5-A_plate.stl'
    old=b.read_stl(old_path)
    assert b.bounds(old[0])==b.bounds(plate[0]),'SCR5-A plate bounds changed'
    for slot in slots:
        x,z=slot['centre_xz']
        select=lambda m:{v for v in m[0] if abs(v[0]-x)<=5.0001 and abs(v[2]-z)<=3.5001}
        assert select(old)==select(plate), 'SCR5-A slot boundary changed'
    # Exact parsed pilot floors and open frame through holes.
    pilots=[]
    for x in (-p['boss_x'],p['boss_x']):
        for z in p['boss_z']:
            hits=y_hits(plate,x,z)
            # A ray on a triangle seam can return duplicate floating-point
            # interpolants. Check all values against the two planes; no mesh welding.
            assert hits and abs(hits[0]+4)<1e-6 and abs(hits[-1]-(p['boss_end_y']-p['insert_seat_depth']))<2e-5
            assert all(abs(y+4)<1e-6 or abs(y-(p['boss_end_y']-p['insert_seat_depth']))<2e-5 for y in hits)
            assert not y_hits(frame,x,z)
            pilots.append({'axis_xz':[x,z],'plate_material_hits_y':hits,'frame_through_hole':'open'})
    noid=b.CHECKS/'SCR5-B_frame-unengraved-probe.stl'
    if render_probes: b.render('no_id',noid)
    noidmesh=b.read_stl(noid); assert b.mesh_check(noidmesh)['pass']
    removed=b.mesh_check(noidmesh)['signed_volume_mm3']-b.mesh_check(frame)['signed_volume_mm3']
    assert removed>1
    floor_y=p['frame_front_y']+p['frame_t']-p['id_depth']
    floor=[v for v in frame[0] if abs(v[1]-floor_y)<1e-6 and abs(v[0]-p['id_x'])<12 and abs(v[2]-p['id_z'])<3]
    assert len(floor)>20
    probes={}
    for name in ('plate_frame_intersection','plate_screen_intersection','frame_screen_intersection','unintended','intended','seating_clearance'):
        target=b.CHECKS/('SCR5-B_'+name+'.stl');logfile=b.CHECKS/(name+'.log')
        if render_probes:
            # Empty OpenSCAD outputs must not leave a stale nonempty probe.
            if target.exists():target.unlink()
            proc=subprocess.run([str(b.OPENSCAD),'--export-format','binstl','-o',str(target),'-D',f'part="{name}"',str(b.SOURCE)],capture_output=True,text=True,encoding='utf-8',errors='replace')
            log=proc.stdout+proc.stderr;logfile.write_text(log,encoding='utf-8')
            assert proc.returncode in (0,1) and 'ERROR:' not in log,log
        else: log=logfile.read_text(encoding='utf-8')
        if target.exists():
            mesh=b.read_stl(target); result=b.mesh_check(mesh)
            probes[name]={'volume_mm3':result['signed_volume_mm3'],'bounds':result['bounds'],'triangles':len(mesh[1])}
            if name in ('plate_frame_intersection','plate_screen_intersection'):
                assert abs(result['signed_volume_mm3'])<1e-7,probes[name]
                expected_y=p['frame_front_y'] if name=='plate_frame_intersection' else p['seat_y']
                assert all(abs(v[1]-expected_y)<1e-6 for v in mesh[0]), 'Only intended bearing planes permitted'
            elif name in ('unintended','seating_clearance'):
                raise AssertionError('Expected empty solid intersection: '+name)
            else:
                pad_front=p['total_depth']-p['preload']
                assert result['signed_volume_mm3']>0
                # Every point of the contact solid must be inside an intended pad prism.
                assert all(any(abs(v[0]-x)<=p['pad_w']/2+1e-5 and abs(v[2]-z)<=p['pad_h']/2+1e-5 and pad_front-1e-5<=v[1]<=p['total_depth']+1e-5 for x in (-p['pad_x'],p['pad_x']) for z in (p['centre_z']-p['pad_z_offset'],p['centre_z']+p['pad_z_offset'])) for v in mesh[0])
        else:
            assert 'Current top level object is empty' in log,log
            assert name not in ('frame_screen_intersection','intended')
            probes[name]={'volume_mm3':0,'result':'empty CGAL intersection'}
    assert abs(probes['frame_screen_intersection']['volume_mm3']-probes['intended']['volume_mm3'])<1e-7
    expected_pad_volume=4*(p['pad_w']*p['pad_h']-(4-math.pi)*p['pad_r']**2)*p['preload']
    assert abs(probes['intended']['volume_mm3']-expected_pad_volume)<.02
    selfcheck={name:strict_triangle_screen(b,m) for name,m in zip(b.NAMES,meshes)}
    b.dump(b.CHECKS/'self-intersection.json',selfcheck)
    assert all(c['pass'] for c in selfcheck.values()),'Self-intersection screen failed'
    keepouts={}
    for key in ('touch_keepout','fpc_keepout'):
        k=p[key];box=[[k[i],k[i]+k[i+3]] for i in range(3)]
        candidates=sum(all(tb[i][0]<box[i][1] and box[i][0]<tb[i][1] for i in range(3)) for tb in (b.bounds([frame[0][j] for j in tri]) for tri in frame[1]))
        assert candidates==0,'Provisional component box may touch frame: '+key
        keepouts[key]={'box':box,'overlapping_triangle_aabbs':candidates,'provenance':'provisional only; actual component clearance UNKNOWN'}
    if render_probes:b.render('screen',b.CHECKS/'SCR5-B_nominal-screen-envelope.stl')
    invalid={'long_screw':('screw_length',9),'short_screw':('screw_length',5),'deep_seat':('insert_seat_depth',21),'zero_pilot':('insert_pilot',0),'nan_clearance':('pcb_clear_x',float('nan')),'window_covers_active':('aperture_r',20),'through_id':('id_depth',5),'boss_hits_screen':('boss_x',63),'excess_preload':('preload',13),'pad_off_pcb':('pad_x',61),'access_hits_pad':('ribbon_z',80),'negative_radius':('frame_inner_r',-1),'square_pcb_blocked':('pocket_half_x',60.8),'boss_unanchored':('boss_x',62.5),'button_hits_pad':('buttons_z',70)}
    rejected=[]
    for case,(key,value) in invalid.items():
        test=copy.deepcopy(doc);test['values'][key]=value
        try:b.parameter_checks(test)
        except AssertionError:rejected.append(case)
        else:raise AssertionError('Invalid configuration accepted: '+case)
    return {'slots':slots,'scr5_a_slot_boundary_vertices':'exact equality, all eight; original read only','scr5_a_plate_bounds':'exact parsed equality','measured_aperture_bounds':aperture_bounds,'pilot_axes':pilots,
        'assembly':probes,'nominal_preload_contact_mm3':probes['intended']['volume_mm3'],'analytic_pad_contact_mm3':expected_pad_volume,
        'engraving':{'source_text':'SCR5-B','removed_volume_mm3':removed,'floor_vertices':len(floor),'remaining_wall_mm':p['frame_t']-p['id_depth']},
        'provisional_component_keepouts':keepouts,'invalid_configurations_rejected':rejected,
        'conditional':['Square outline rear insertion passes with frame removed; no screen disassembly required','12.6 total-depth box is an envelope, not actual PCB contact surface','Actual component-free contact lands, button/finger approach, preload and retention UNKNOWN','Active registration UNKNOWN; centred assumed rectangle and 0.25 keepout pass','Numerical self-intersection screen only; no exact-arithmetic certification or slicer test']}
