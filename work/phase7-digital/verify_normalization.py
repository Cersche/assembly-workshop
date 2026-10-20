from pathlib import Path
import sys,shutil,json
sys.path.insert(0,'outputs/Mechanical_Design_App')
import mesh_revision as m
root=Path('work/phase7-digital/render-diagnostics')
p=root/'tray-normalized.stl';shutil.copy2(root/'tray-asciistl.stl',p)
processing=m.normalize_collinear_faces(p);mesh=m.read_mesh(p,'tray')
print(json.dumps({'processing':processing,'triangles':len(mesh['triangles']),'bounds':mesh['bounds'],'signed_volume_mm3':mesh['signed_volume_mm3']},indent=2))
