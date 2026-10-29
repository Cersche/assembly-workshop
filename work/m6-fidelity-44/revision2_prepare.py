"""Explicit read-only measurement to numeric polygons, then a new disposable spec."""
import json
import math
import shutil
from measure import ROOT,HERE,mesh_info,section
from rail_trial import simplify

REV=HERE/'revision2'
REV.mkdir(exist_ok=True)
report=ROOT/'work/codex-tasks/44-cm6b-fidelity-REPORT.md'
if not (REV/'first-run-report.md').exists():shutil.copyfile(report,REV/'first-run-report.md')
out=ROOT/'outputs/CM1000_M6_generated_2026-10-28'
if not (REV/'task43-delivery').exists():shutil.copytree(out,REV/'task43-delivery')

def contour(loop,n=256):
    p=simplify(loop,.008)
    area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))
    if area<0:p.reverse()
    # Stable outer-wall/bottom anchor, independent of STL facet ordering.
    left=sum(x for x,z in p)/len(p)<127
    outer=min(x for x,z in p) if left else max(x for x,z in p)
    k=min(range(len(p)),key=lambda i:(p[i][0]-outer)**2+(p[i][1]-1.6)**2)
    p=p[k:]+p[:k]
    edges=list(zip(p,p[1:]+p[:1]));lengths=[math.dist(a,b) for a,b in edges]
    total=sum(lengths);res=[];j=0;offset=0
    for i in range(n):
        target=total*i/n
        while offset+lengths[j]<target:offset+=lengths[j];j+=1
        a,b=edges[j];t=(target-offset)/lengths[j]
        res.append([round(a[0]+t*(b[0]-a[0])-127,6),round(a[1]+t*(b[1]-a[1]),6)])
    return res

def convert(poly,kind):
    return [[round(a-(127 if kind=='xz' else 4),6),round(b,6)] for a,b in poly]

def main():
    spec=json.loads((out/'CM6B_spec.json').read_text(encoding='utf-8'))
    spec.update(m6_rail_len=121.62,m6_bay_h=14.36,m6_bay_d=46.91,
                m6_edge_radius=0,m6_retention_slot=[64.786,22.987,16.0274,6.5024,0])
    # Bay datum shifts +.005 in Z so exact 14.36 opening keeps >=2.5 at both outer faces.
    # Joint centres themselves are unchanged.
    profiles=[];masks=[];stubs=[[],[]]
    fv,ft,_=mesh_info(ROOT/'outputs/CM1000_M6_2026-10-28/CM6A_faceplate.stl')
    for side,(name,x) in enumerate([('l',18),('r',236)]):
        v,t,_=mesh_info(ROOT/f'outputs/CM1000_M6_2026-10-28/CM6A_rail_{name}.stl')
        base=section(v,t,1,125.123)
        profiles.append(convert(simplify(max(base['loops'],key=lambda l:len(l['points']))['points'],.008),'xz'))
        mask=section(v,t,0,x)
        # Outer side silhouette contains the three upper/lower openings; retention hole cut independently.
        def area(l):
            p=l['points'];return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1])))
        ordered=sorted(mask['loops'],key=area,reverse=True)
        masks.append([convert(simplify(l['points'],.008),'yz') for l in ordered
                      if not (side==0 and 19<min(z for yy,z in l['points'])<20 and 26<max(z for yy,z in l['points'])<27)])
        for y in [4.001]+[4.25+i*.25 for i in range(47)]+[15.999]:
            loops=section(fv,ft,1,y)['loops']
            # Trace the pocket boundary with vertical rays through numeric section contours.
            # Deliberately omit the reference's centre bridge: only the two equipment stubs
            # belong to this split-rail adapter. This remaining difference is measured later.
            lower=[];upper=[]
            for i in range(81):
                xx=20.702+(35.0293-20.702)*i/80
                xa=xx if side==0 else 254-xx
                hits=[]
                for l in loops:
                    p=l['points']
                    for a,b in zip(p,p[1:]+p[:1]):
                        if (a[0]<xa)!=(b[0]<xa):
                            hits.append(a[1]+(xa-a[0])*(b[1]-a[1])/(b[0]-a[0]))
                below=[z for z in hits if z<22.225];above=[z for z in hits if z>22.225]
                lo=max(below) if below else .025
                hi=min(above) if above else 44.425
                lower.append([xx,lo]);upper.append([xx,hi])
            p=[[16.767,.025],[35.0293,.025]]+list(reversed(lower))+upper+[[35.0293,44.425],[16.767,44.425]]
            if side:p=[[254-xx,z] for xx,z in reversed(p)]
            stubs[side].append([round(y-4,6),convert(p,'xz')])
        stubs[side][0][0]=-.01;stubs[side][-1][0]=12
    spec.update(m6_rail_profiles=profiles,m6_side_windows=masks,m6_stub_sections=stubs)
    # Uniform central bridge measured at X_A=40. Kept as a numeric side-outline extrusion;
    # the two end lofts cover the varying side blends and overlap the bridge by 0.0293 mm.
    bridge=section(fv,ft,0,40)
    def bridge_area(l):
        p=l['points'];return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1])))
    spec['m6_nose_bridge']=[[-92,92],[convert(simplify(l['points'],.003),'yz') for l in sorted(bridge['loops'],key=bridge_area,reverse=True)]]
    data=json.loads((HERE/'sections.json').read_text(encoding='utf-8'))
    spec['m6_light_pipes']=[]
    spec['m6_vectors']=[]
    for n in range(4,9):
        lo,hi=data[f'colour_{n}']['bounds']
        spec['m6_light_pipes'].append([round((lo[0]+hi[0])/2-127,6),round((lo[2]+hi[2])/2,6),8,8.72])
    for n in list(range(9,16))+[2,3]:
        sec=data[f'colour_{n}']['sections'][1]
        spec['m6_vectors'].append([.2,[convert(simplify(l['points'],.01),'xz') for l in sec['loops']]])
    (REV/'spec.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
    print('prepared',len(stubs[0]),'stub sections per side,',len(spec['m6_vectors']),'vector objects')

if __name__=='__main__':main()
