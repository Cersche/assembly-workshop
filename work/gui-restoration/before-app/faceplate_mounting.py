"""Four-corner default sourced from the user-supplied 1U faceplate."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
LEGACY_SLOTS='for(x=[-118.2625,118.2625])translate([x,-plate_t-0.1,plate_h/2+1.9722])rotate([-90,0,0])linear_extrude(height=plate_t+0.2) capsule2d();'

def profile():
    return json.loads((ROOT/'faceplate_mounting.json').read_text(encoding='utf-8'))

def apply_default(source):
    p=profile()
    if source.count(LEGACY_SLOTS)!=1:
        raise ValueError('Faceplate source does not match the supported mounting adapter.')
    zs=','.join(format(z,'.10g') for z in p['centers_z_mm'])
    replacement='for(x=[-118.2625,118.2625], z=['+zs+'])translate([x,-plate_t-0.1,z])rotate([-90,0,0])linear_extrude(height=plate_t+0.2) capsule2d();'
    return source.replace('// 1U creator slots, vertical center +1.9722 relative to source midpoint','// Four outer-corner slots: user-supplied 1U reference centers; prior baseline retained separately.').replace(LEGACY_SLOTS,replacement)
