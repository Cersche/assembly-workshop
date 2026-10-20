from pathlib import Path
import sys,tempfile,json,hashlib
sys.path.insert(0,'outputs/Mechanical_Design_App')
import mesh_revision as m
out=Path('outputs/Phase7_Digital_Acceptance')
for name in ['mesh_revision.py','index.html','README.md']:
    dst=out/('before_'+name)
    assert not dst.exists()
    dst.write_bytes((Path('outputs/Mechanical_Design_App')/name).read_bytes())
with tempfile.TemporaryDirectory() as d:
    root=Path(d)
    p=root/'duplicate.stl'
    tri='facet normal 0 0 1\nouter loop\nvertex 0 0 0\nvertex 1 0 0\nvertex 0 1 0\nendloop\nendfacet\n'
    p.write_text('solid bad\n'+tri+tri+'endsolid bad\n')
    result=m.read_mesh(p,'duplicate')
    source='invalid cached source'
    meta={'limitations':[]}
    identity=hashlib.sha256(('pi4-mesh-v1\n'+source+json.dumps(meta,sort_keys=True)).encode()).hexdigest()
    folder=root/'revisions'/identity;folder.mkdir(parents=True)
    (folder/'assembly.json').write_text('{"parts":[],"units":"mm"}')
    cached=m.build(source,meta,root)
    report={'duplicate_coplanar_faces_accepted':len(result['triangles'])==2,'incomplete_cache_accepted':cached['cached'],'disposition':'Confirmed; fix mesh checks and cache/export validation without altering old entries'}
    (out/'Reproduced_Issues.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))
