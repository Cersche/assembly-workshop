from pathlib import Path
p=Path('outputs/Mechanical_Design_App/mesh_revision.py');s=p.read_text(encoding='utf-8')
i=s.index('\n\nARTIFACTS =')
fn='''

def normalize_collinear_faces(path):
    """Retriangulate only exact zero-area faces with a strict interior vertex.

    Remove the empty triangle and split its unique long-edge neighbor at the
    existing middle vertex. No coordinate is added or moved; all surface area
    and winding belong to the same original neighboring triangle.
    """
    raw = path.read_bytes()
    vertices = [tuple(map(float, line.split())) for line in
                re.findall(rb'^\\s*vertex\\s+([^\\r\\n]+)', raw, re.M)]
    if (not vertices or len(vertices)%3 or any(len(v)!=3 or not all(math.isfinite(x) for x in v) for v in vertices)):
        raise ValueError('Cannot normalize malformed STL.')
    faces = [vertices[i:i+3] for i in range(0,len(vertices),3)]
    def normal(face):
        a,b,c=face;u=[b[k]-a[k] for k in range(3)];v=[c[k]-a[k] for k in range(3)]
        return (u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
    repairs=[]
    while True:
        index=next((i for i,f in enumerate(faces) if normal(f)==(0,0,0)),None)
        if index is None:break
        face=faces[index]
        if len(set(face))!=3:raise ValueError('Repeated-vertex STL face cannot be normalized safely.')
        a,b=max(((face[i],face[j]) for i,j in ((0,1),(1,2),(2,0))),key=lambda pair:sum((pair[1][k]-pair[0][k])**2 for k in range(3)))
        middle=next(v for v in face if v!=a and v!=b)
        if sum((middle[k]-a[k])*(middle[k]-b[k]) for k in range(3))>=0:
            raise ValueError('Collinear vertex is not strictly inside the edge.')
        neighbors=[(i,j) for i,f in enumerate(faces) if i!=index for j in range(3)
                   if {f[j],f[(j+1)%3]}=={a,b}]
        if len(neighbors)!=1:raise ValueError('Collinear face has no unique edge neighbor.')
        neighbor,j=neighbors[0];f=faces[neighbor];x,y,z=f[j],f[(j+1)%3],f[(j+2)%3]
        split=[[x,middle,z],[middle,y,z]];old_normal=normal(f)
        if any(sum(n[k]*old_normal[k] for k in range(3))<=0 for n in map(normal,split)):
            raise ValueError('Collinear repair would change face orientation.')
        repairs.append({'long_edge':[a,b],'existing_middle_vertex':middle})
        faces=[f for i,f in enumerate(faces) if i not in (index,neighbor)]+split
    if repairs:
        lines=['solid normalized_export']
        for face in faces:
            n=normal(face);length=math.sqrt(sum(x*x for x in n))
            lines+=['facet normal '+' '.join(format(x/length,'.17g') for x in n),'outer loop']
            lines+=['vertex '+' '.join(format(x,'.17g') for x in vertex) for vertex in face]
            lines+=['endloop','endfacet']
        path.write_text('\\n'.join(lines+['endsolid normalized_export','']),encoding='ascii',newline='\\n')
    return {'method':'exact-collinear-neighbor-split-v1','renderer_sha256':hashlib.sha256(raw).hexdigest(),
            'output_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'repairs':repairs,
            'scope':'Export triangulation only. Existing coordinates and neighboring surface preserved; no dimensions changed.'}
'''
s=s[:i]+fn+s[i:]
s=s.replace("'pi4-mesh-v2\\n'", "'pi4-mesh-v2-triangulation1\\n'")
s=s.replace('parts, logs = [], {}','parts, logs, processing = [], {}, {}')
s=s.replace("                parts.append(read_mesh(folder / (name+'.stl'), name))","                processing[name] = normalize_collinear_faces(folder / (name+'.stl'))\n                parts.append(read_mesh(folder / (name+'.stl'), name))")
s=s.replace('report = dict(metadata, build_inputs=metadata, mesh_build=', 'report = dict(metadata, build_inputs=metadata, mesh_processing=processing, mesh_build=')
s=s.replace("        for name, part in zip(('tray', 'faceplate'), assembly['parts']):", "        for name, part in zip(('tray', 'faceplate'), assembly['parts']):\n            if report['mesh_processing'][name]['output_sha256'] != integrity['sha256'][name+'.stl']:\n                raise ValueError('Processing/STL hash mismatch: ' + name)")
p.write_text(s,encoding='utf-8')
