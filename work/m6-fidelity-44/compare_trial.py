"""Independent section-boundary distances for the disposable primitive rail trial."""
import json
from measure import HERE, ROOT, section, mesh_info
from rail_trial import dist, simplify


def edges(s):
    return [(a,b) for l in s['loops'] for a,b in zip(l['points'],l['points'][1:]+l['points'][:1]) if a != b]


def directed(a, b):
    target = edges(b)
    worst = (0,None,None)
    for l in a['loops']:
        for p in simplify(l['points'], .005):
            # IDs are a separate intentional change, outside the window comparison.
            if p[1] > 43.8 or p[1] < .6 or p[0] < 20 or p[0] > 135:
                continue
            d, e = min((dist(p,u,v),(u,v)) for u,v in target)
            if d > worst[0]:
                worst = (d,p,e)
    return dict(distance=worst[0], point=worst[1], nearest_edge=worst[2])


result = {}
for side, xs in [('l',[17,18,20,22.6,26,30,34]), ('r',[237,236,234,231.4,228,224,220])]:
    av,at,_ = mesh_info(ROOT/f'outputs/CM1000_M6_2026-10-28/CM6A_rail_{side}.stl')
    bv,bt,_ = mesh_info(HERE/f'trial-{side}.stl')
    rows = []
    for x in xs:
        a,b = section(av,at,0,x),section(bv,bt,0,x)
        rows.append(dict(x=x, reference_to_trial=directed(a,b), trial_to_reference=directed(b,a)))
    result[side] = rows
    print(side, json.dumps(rows,indent=2))
(HERE/'trial-window-errors.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
