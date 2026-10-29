"""Build HP4-M6-B with OpenSCAD.exe, validate exact STL topology, then pack 3MF.

Python 3.10 standard library only. Run from any directory; optional output directory.
The cradle is read in place from Downloads; never copied.
"""
from pathlib import Path
from collections import Counter, defaultdict
import json, os, re, subprocess, sys, tempfile, zipfile
import xml.etree.ElementTree as ET
ET.register_namespace('', 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02')  # plain tags: slicers reject ns0: prefixes

ID = 'HP4-M6-B'
SOURCE = Path(__file__).with_name(ID+'.scad')
ROOT = next(p for p in SOURCE.parents if (p/'tools/plate_layout_stl.py').is_file())
OPENSCAD = Path(os.environ.get('OPENSCAD_EXE', 'C:/Program Files/OpenSCAD/openscad.exe'))

def render_messages(log):
    warnings=[s for s in log.splitlines() if 'WARNING' in s or 'ERROR' in s]
    expected=[s for s in warnings if re.fullmatch(r'WARNING: \w+ was assigned on line \d+ of ".*" but was overwritten in file .*, line \d+',s)]
    assert len(warnings)==len(expected), '\n'.join(warnings)
    return len(expected)

def mesh_check(path):
    # Exact parsed decimal coordinates: no rounding/welding hides tiny sliver edges.
    values = [tuple(map(float,m)) for m in re.findall(r'\bvertex\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)',path.read_text(encoding='utf-8'))]
    assert values and len(values)%3==0, 'Missing or malformed ASCII STL'
    triangles = [tuple(values[i:i+3]) for i in range(0,len(values),3)]
    edges=defaultdict(list); directions=Counter(); degenerates=0
    parent=list(range(len(triangles)))
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def union(a,b): parent[find(a)]=find(b)
    volume=0
    for i,t in enumerate(triangles):
        a,b,c=t
        cross=((b[1]-a[1])*(c[2]-a[2])-(b[2]-a[2])*(c[1]-a[1]),(b[2]-a[2])*(c[0]-a[0])-(b[0]-a[0])*(c[2]-a[2]),(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))
        if sum(v*v for v in cross)==0: degenerates+=1
        volume+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
        for a,b in ((a,b),(b,c),(c,a)):
            key=tuple(sorted((a,b)))
            edges[key].append(i); directions[key]+=1 if a<b else -1
    for adjacent in edges.values():
        for i in adjacent[1:]: union(adjacent[0],i)
    behind=[v for v in values if v[1]>0]
    result=dict(triangles=len(triangles),vertices=len(set(values)),edges=len(edges),
                bad_edges=sum(len(v)!=2 for v in edges.values()),
                inconsistent_edges=sum(v!=0 for v in directions.values()),
                degenerate_triangles=degenerates,shells=len({find(i) for i in parent}),signed_volume_mm3=volume,
                minimum=[min(v[k] for v in values) for k in range(3)],maximum=[max(v[k] for v in values) for k in range(3)],
                behind_plate_x=[min(v[0] for v in behind),max(v[0] for v in behind)])
    assert result['bad_edges']==result['inconsistent_edges']==0,result
    assert result['shells']==1 and volume>0,result
    assert -104<=result['behind_plate_x'][0] and result['behind_plate_x'][1]<=104,result
    return result

def main():
    out=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else SOURCE.parent.parent
    out.mkdir(parents=True,exist_ok=True)
    evidence=out/'checks'; evidence.mkdir(exist_ok=True)
    assert OPENSCAD.name.lower()=='openscad.exe' and OPENSCAD.is_file()
    assert Path('C:/Users/brian/Downloads/Swanky Rottis.stl').is_file()
    clearance=json.loads((evidence/'clearance.json').read_text(encoding='utf-8'))
    assert clearance['passed'], 'Clearance failed: STOP, no build/package'
    results={'clearance':clearance}
    for part in ('tray','faceplate'):
        path=out/f'{ID}_{part}.stl'
        command=[str(OPENSCAD),'--export-format','asciistl','-D',f'part="{part}"','-o',str(path),str(SOURCE)]
        run=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
        (evidence/f'{part}-render.log').write_text(run.stdout+run.stderr,encoding='utf-8')
        assert run.returncode==0,run.stderr
        overwrite_warnings=render_messages(run.stdout+run.stderr)
        results[part]=mesh_check(path)
        results[part]['inherited_assignment_warnings']=overwrite_warnings
        print(part,json.dumps(results[part]),flush=True)
    text=SOURCE.read_text(encoding='utf-8')
    text=text.replace('clip_coupon(){\n if(part=="faceplate")','if(false)clip_coupon(){\n if(part=="faceplate")')
    probe=evidence/'assembled-intersection.scad'
    probe.write_text(text+'\nintersection(){faceplate();tray();}\n',encoding='utf-8')
    run=subprocess.run([str(OPENSCAD),'--export-format','asciistl','-o',str(evidence/'assembled-intersection.stl'),str(probe)],capture_output=True,text=True,encoding='utf-8')
    (evidence/'intersection-render.log').write_text(run.stdout+run.stderr,encoding='utf-8')
    if 'Current top level object is empty.' in run.stderr:
        render_messages(run.stderr)
        results['intersection']='empty (OpenSCAD empty-object exit '+str(run.returncode)+')'
    else:
        # Brian, task 45: intended Y=0 contact is allowed; only overlapping volume fails.
        # Do not round/weld: every exported contact vertex must lie exactly on that plane.
        contact_path=evidence/'assembled-intersection.stl'
        contact=[tuple(map(float,m)) for m in re.findall(r'\bvertex\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)',contact_path.read_text(encoding='utf-8'))]
        assert run.returncode==0 and contact and all(v[1]==0 for v in contact),run.stderr
        allowed='\n'.join(s for s in run.stderr.splitlines() if not s.startswith(('WARNING: Object may not be a valid 2-manifold','EXPORT-WARNING: Exported object may not be a valid 2-manifold')))
        render_messages(allowed)
        results['intersection']='contact only, 0 volume'
        results['contact_triangles']=len(contact)//3
        results['contact_plane']='Y=0 exactly; no rounding'
    # The CLI keys objects by input filename, so stage exact rendered bytes under its expected part names.
    package=out/f'{ID}_Hue_Pi4_M6_set.3mf'
    with tempfile.TemporaryDirectory(prefix=ID+'-layout-') as temp:
        staged=[]
        for part in ('tray','faceplate'):
            path=Path(temp)/(part+'.stl');path.write_bytes((out/f'{ID}_{part}.stl').read_bytes()); staged.append(str(path))
        subprocess.run([sys.executable,str(ROOT/'tools/plate_layout_stl.py'),*staged,str(package)],check=True)
    with zipfile.ZipFile(package) as z: contents={n:z.read(n) for n in z.namelist()}
    ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
    model=ET.fromstring(contents['3D/3dmodel.model'])
    objects=model.findall('m:resources/m:object',ns)
    assert len(objects)==2 and len(model.findall('m:build/m:item',ns))==2
    packed=[]
    for obj in objects:
        part=obj.attrib['name'];obj.set('name',f'{ID} Hue + Pi 4 {part}')
        verts=[tuple(float(v.attrib[k]) for k in ('x','y','z')) for v in obj.findall('m:mesh/m:vertices/m:vertex',ns)]
        faces=obj.findall('m:mesh/m:triangles/m:triangle',ns)
        assert len(faces)==results[part]['triangles']
        assert min(v[2] for v in verts)==0
        packed.append(dict(name=obj.attrib['name'],triangles=len(faces),minimum=[min(v[k] for v in verts) for k in range(3)],maximum=[max(v[k] for v in verts) for k in range(3)]))
    assert packed[1]['maximum'][1]<packed[0]['minimum'][1]
    results['3mf_objects']=packed
    contents['3D/3dmodel.model']=ET.tostring(model,encoding='utf-8',xml_declaration=True)
    with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED) as z:
        for n,data in contents.items():z.writestr(n,data)
    xml=contents['3D/3dmodel.model']
    assert b'<ns0:' not in xml and xml.count(b'<vertex ')==sum(len(o.findall('m:mesh/m:vertices/m:vertex',ns)) for o in objects)
    assert xml.count(b'<triangle ')==sum(p['triangles'] for p in packed)
    results['plain_xml_tags']={'vertices':xml.count(b'<vertex '),'triangles':xml.count(b'<triangle '),'ns0_prefixes':xml.count(b'ns0:')}
    (evidence/'acceptance.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print('PASS: closed single solids, no overlapping volume, bounded rear geometry, two separate print objects.',flush=True)

if __name__=='__main__': main()
