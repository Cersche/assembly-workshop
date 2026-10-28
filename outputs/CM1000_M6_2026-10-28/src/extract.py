import zipfile,re,sys,struct,xml.etree.ElementTree as ET
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
def load(path,tag):
    z=zipfile.ZipFile(path)
    cfg=z.read('Metadata/model_settings.config').decode()
    names={}
    for m in re.finditer(r'<part id="(\d+)" subtype="(\w+)">\s*<metadata key="name" value="([^"]*)"',cfg): names[m.group(1)]=(m.group(2),m.group(3))
    root=ET.fromstring(z.read('3D/Objects/object_1.model'))
    for o in root.iter('{%s}object'%ns['m']):
        oid=o.get('id')
        vs=[(float(v.get('x')),float(v.get('y')),float(v.get('z'))) for v in o.iter('{%s}vertex'%ns['m'])]
        ts=[(int(t.get('v1')),int(t.get('v2')),int(t.get('v3'))) for t in o.iter('{%s}triangle'%ns['m'])]
        st,nm=names.get(oid,('?','?'))
        mn=[min(v[i] for v in vs) for i in range(3)];mx=[max(v[i] for v in vs) for i in range(3)]
        print(tag,oid,st,nm,len(ts),'min',[round(a,2) for a in mn],'max',[round(a,2) for a in mx])
        fn=f'{tag}_{oid}_{st}.stl'
        with open(fn,'w') as f:
            f.write('solid a\n')
            for a,b,c in ts:
                f.write('facet normal 0 0 0\nouter loop\n')
                for i in (a,b,c): f.write('vertex %f %f %f\n'%vs[i])
                f.write('endloop\nendfacet\n')
            f.write('endsolid a\n')
import os; os.makedirs('orig',exist_ok=True); os.chdir('orig')
for p,t in [('fp','CM1000_LabRax_faceplate'),('rl','CM1000_LabRax_rails_v2')]:
    load('D:/Projects/assembly-workshop/outputs/STL_Deliveries/2026-10-16_CM1000_bracket/'+t+'.3mf',p)
