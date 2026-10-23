"""Task 40 Part A: U8 TL-SG108E sleeve tray/faceplate, switch shifted RIGHT by `offset`, no uplink keystone.
Same spec as outputs/STL_Deliveries/2026-10-22_TL-SG108E except dev_off_x, keystones and labels. Writes only to argv[1].
Usage: python part_a_build.py <scratch-dir> [offset_mm=15]      PROPOSED - UNVALIDATED (case size nominal, not measured).
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'outputs' / 'Mechanical_Design_App'))
import equipment, mesh_study  # noqa: E402
off = float(sys.argv[2]) if len(sys.argv) > 2 else 15.0
spec = {"name": "TL-SG108E U8 (aligned to keystone panel)", "dev_w": 158, "dev_d": 101, "dev_h": 25, "u": 1,
        "device_mount": "sleeve", "joint": "screw", "dev_off_x": off, "keystones": [], "tray_follow": True}
c = equipment.clean(spec)
print('clean OK; joint_x', c.get('joint_x'))
Path(sys.argv[1]).mkdir(parents=True, exist_ok=True)
(Path(sys.argv[1]) / 'spec.json').write_text(json.dumps(spec, indent=1), encoding='utf-8')
out = equipment.render(spec, Path(sys.argv[1]))
for f in sorted(out.iterdir()):
    if f.suffix == '.stl':
        t = mesh_study.load_mesh(f)
        print(f.name, len(t), 'tris, open edges', mesh_study.open_edges(t), 'bodies', len(mesh_study.bodies(t)), 'bbox', mesh_study.bbox(t))
