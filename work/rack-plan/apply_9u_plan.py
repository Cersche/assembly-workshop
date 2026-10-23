"""Apply the 9U rack plan (Rack_Plan_9U.html, 2026-10-22) to a data folder through the app's own save path.

Usage: python apply_9u_plan.py <data-dir>     (use a disposable copy first; normal-use only with Brian's OK)

Keeps the rack's id, name and appearance; sets 9 slots (posts 4U + 1U support extension + 4U on both sides),
puts the library item "Philips Hue Bridge + Raspberry Pi 4 (keystone)" at U6 and adds the bottom-rear cable exit.
Other plan items (OptiPlex, drive tray, keystone panel, switch, screen plate) are not in the equipment library yet,
so their slots stay empty. rack_workspace.save() writes the previous document to rack-history/ first.
Stored slot numbers count from the top; U = slots - slot + 1.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'outputs' / 'Mechanical_Design_App'))
import app, rack_workspace  # noqa: E402

data = Path(sys.argv[1])
store = app.Store(data / 'library.sqlite3')
seed = store.project()
doc = rack_workspace.read(data, seed)
library = json.loads((data / 'equipment-library.json').read_text(encoding='utf-8-sig'))
hue = next(i for i in library if i['name'].startswith('Philips Hue Bridge'))
assert hue.get('span', 1) == 1
rack = doc['racks'][0]
SLOTS = 9
rack.update(slots=SLOTS, post_levels={'left': [4, 4], 'right': [4, 4]})
rack['name'] = 'My Lab Rax 9U'
slot_for_u = lambda u: SLOTS - u + 1
rack['placements'] = [{'id': 'u6-pi-hue', 'equipment': hue['id'], 'slot': slot_for_u(6), 'span': 1,
                       'assembly': {'name': 'Pi 4 + Hue tray (U6)'}}]
rack['cabling'] = {'guides': [], 'exits': [{'id': 'exit-bottom-rear', 'position': 'bottom-rear', 'slot': slot_for_u(1)}]}
out = rack_workspace.save(data, doc, seed_project=seed, allow_project_changes=True,
                          canonical_project=lambda p: store.draft(p, project=p))
r = out['racks'][0]
print(r['name'], r['slots'], r['post_levels'], [(p['assembly']['name'], p['slot'], p['span']) for p in r['placements']], r['cabling']['exits'])
