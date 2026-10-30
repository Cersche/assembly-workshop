"""Put the SCR5-E 2U screen + Pi 4 + Hue unit into the saved 9U rack (Brian, 2026-10-29).

Usage: python apply_scr5e.py <data-dir>     (use a disposable copy first; normal-use only with Brian's OK)

Adds a faceplate-only library placeholder for SCR5-E (screen aperture at X +33, Pi USB/Ethernet
openings, golden-keystone position) and places it at U4-U3. U5 is freed (SCR5-E houses the Pi and
Hue), so the old Pi 4 + Hue placement there is removed. The real part is outputs/Screen_Pi_Hue_SCR5-E_2026-10-29/;
the app item is a placeholder faceplate only. rack_workspace.save() writes the previous document to rack-history/ first.
Stored slot numbers count from the top; U = slots - slot + 1.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'outputs' / 'Mechanical_Design_App'))
import app, equipment, rack_workspace  # noqa: E402

NAME = 'Screen 5in + Pi 4 + Hue 2U (SCR5-E, placeholder)'
data = Path(sys.argv[1])
library = equipment.library(data)
item = next((i for i in library if i['name'] == NAME), None)
if item is None:
    spec = dict(next(i for i in library if i['id'] == 'eq-6cee544dd821')['spec'])  # 7in placeholder as template
    spec.update(u=2, ports=[
        # SCR5-B aperture: glass 120.7 x 77.2 + 0.5 clearance each side, minus 3 mm lips; screen centre X +33
        {'x': 33.0, 'z': 44.45, 'w': 115.7, 'h': 72.2, 'r': 4.0, 'label': 'Screen', 'type': 'other', 'id': 'front-1'},
        {'x': -93.0, 'z': 26.8, 'w': 15.0, 'h': 17.5, 'r': 1.0, 'label': 'Pi USB', 'type': 'usb-a', 'id': 'front-2'},
        {'x': -75.0, 'z': 26.8, 'w': 15.0, 'h': 17.5, 'r': 1.0, 'label': 'Pi USB', 'type': 'usb-a', 'id': 'front-3'},
        {'x': -56.3, 'z': 25.6, 'w': 17.5, 'h': 15.0, 'r': 1.0, 'label': 'Pi Ethernet', 'type': 'rj45', 'id': 'front-4'}],
        keystones=[[-92.5, 66.0]])
    spec['display_name'] = NAME
    item = equipment.save_item(spec, data)
store = app.Store(data / 'library.sqlite3')
seed = store.project()
doc = rack_workspace.read(data, seed)
rack = doc['racks'][0]
SLOTS = rack['slots']
slot_for_u = lambda u: SLOTS - u + 1
keep = [p for p in rack['placements'] if p['slot'] not in (slot_for_u(5), slot_for_u(4), slot_for_u(3))]
rack['placements'] = keep + [{'id': 'u4-u3-scr5e', 'equipment': item['id'], 'slot': slot_for_u(4), 'span': 2,
                              'assembly': {'name': 'Screen + Pi + Hue SCR5-E (U4-U3)'}}]
out = rack_workspace.save(data, doc, seed_project=seed, allow_project_changes=True,
                          canonical_project=lambda p: store.draft(p, project=p))
r = out['racks'][0]
print(item['id'], item['build'][:12], item['parts'])
print(sorted((SLOTS - p['slot'] + 1, p['span'], p['assembly']['name']) for p in r['placements']))
