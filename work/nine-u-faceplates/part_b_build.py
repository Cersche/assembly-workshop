"""Task 40 Part B: U6 Pi 4 + Hue tray variant with the Pi's USB/Ethernet facing the FRONT.
Reads Brian's saved Hue+Pi item (read-only), writes only to the scratch data dir given as argv[2].
Usage: python part_b_build.py <equipment-library.json> <scratch-dir> [--render]
PROPOSED - UNVALIDATED. Fit, cable bend space and strength UNKNOWN.
"""
import copy, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'outputs' / 'Mechanical_Design_App'))
import equipment, mesh_study  # noqa: E402

lib = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8-sig'))
item = next(i for i in lib if i['name'].startswith('Philips Hue Bridge'))
spec = copy.deepcopy(item['spec'])
spec['name'] = 'Hue Bridge + Pi 4 (USB front) PROPOSED'
# Pi turned 270 degrees puts its USB/Ethernet end at the FRONT and USB-C/HDMI/audio on its left side (app port model,
# cable-ports.js). Pi stays on the right (as saved), the Hue moves 6 mm left so an 10 mm gap opens beside the Pi's HDMI
# side: the right-angle micro-HDMI plug exits into that gap and the cable runs back along it (tray rear is open).
# (Pi on the left was tried: no clear left screw-joint spot exists behind a 56 mm opening cluster.)
spec['dev_off_x'] = -36.0
sec = spec['second']
sec['dev_off_x'] = 46.0
sec['dev_rot'] = 270
OPEN = lambda i, label, typ, x, z, w, h, r: dict(id=i, label=label, type=typ, x=x, z=z, w=w, h=h, r=r)
# Pi connector positions from the app's own port model at this offset/rotation: usb2 x27, usb3 x45, ethernet x63.7.
sec['ports'] = [
    OPEN('front-1', 'USB 2.0 stack', 'usb-a', 27.0, 25.4, 13.5, 17, 1),
    OPEN('front-2', 'USB 3.0 stack', 'usb-a', 45.0, 25.4, 13.5, 17, 1),
    OPEN('front-3', 'Ethernet', 'rj45', 63.7, 24.4, 17, 14, 1),
    # Slot under the USB 2.0 stack for a down-angled USB-A plug's cable (plug size ~17 x 8 mm is an ASSUMPTION).
    OPEN('front-4', 'USB cable slot', 'other', 27.0, 10.4, 12, 9, 2.5),
]
cleaned = equipment.clean(spec)
print('clean OK; joint_x:', cleaned.get('joint_x'), 'ports:', [(p['id'], p['x'], p['z'], p['w'], p['h']) for p in cleaned['ports']])
Path(sys.argv[2]).mkdir(parents=True, exist_ok=True)
(Path(sys.argv[2]) / 'spec.json').write_text(json.dumps(spec, indent=1), encoding='utf-8')
if '--render' in sys.argv:
    out = equipment.render(spec, Path(sys.argv[2]))
    for f in sorted(out.iterdir()):
        if f.suffix == '.stl':
            t = mesh_study.load_mesh(f)
            print(f.name, len(t), 'tris', 'open edges', mesh_study.open_edges(t) if hasattr(mesh_study, 'open_edges') else '?',
                  'bodies', len(mesh_study.bodies(t)), 'bbox', mesh_study.bbox(t))
