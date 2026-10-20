"""Update assembly-view interaction guidance; preserve normal data fingerprints."""
from pathlib import Path
import hashlib
import json
root=Path(__file__).resolve().parents[2]
p=root/'outputs/Mechanical_Design_App/index.html'
s=p.read_text(encoding='utf-8')
old='Actual clearance-v2 tray and faceplate meshes in their assembly coordinates. Drag to rotate, or focus the view and use the arrow keys.'
new='Actual clearance-v2 tray and faceplate meshes in their assembly coordinates. Click a part to highlight it; click empty space or press Escape to clear. Drag to rotate, or use the arrow keys.'
assert s.count(old)==1
s=s.replace(old,new)
p.write_text(s,encoding='utf-8')
data=root/'data/normal-use'
(Path(__file__).parent/'Data_Before.json').write_text(json.dumps({str(p.relative_to(data)):hashlib.sha256(p.read_bytes()).hexdigest() for p in data.rglob('*') if p.is_file()},indent=2),encoding='utf-8')
