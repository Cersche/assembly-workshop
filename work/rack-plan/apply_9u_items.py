"""Add the rest of the 9U plan to a data folder's equipment library and place it (Brian, 2026-10-23: "do it all").

Usage: python apply_9u_items.py <data-dir>     (disposable copy first; normal-use only with Brian's OK)

Saves each item through equipment.save_item (the wizard's own save path) and places it through rack_workspace.save,
which writes the previous rack document to rack-history/ first. Keeps the existing Pi 4 + Hue placement at U6.
Real designs: OptiPlex (SLV-B sleeve spec, sleeve_top 0.8), drive tray (3.5" + 2.5"), TL-SG108E (app spec only;
the printable part is the hand-patched STL delivery 2026-10-23_TL-SG108E_flush). Placeholders: modem, keystone
panel, 3U screen plate. Stored slot numbers count from the top; U = slots - slot + 1. Fit/strength UNKNOWN.
"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'outputs' / 'Mechanical_Design_App'))
import app, equipment, rack_workspace  # noqa: E402

data = Path(sys.argv[1])
optiplex = json.loads((ROOT / 'outputs/Physical_Test_Coupons_2026-10-20_SLV-B/SLV-B_spec.json').read_text(encoding='utf-8'))
optiplex.update(name='Dell OptiPlex Micro 7010 (sleeve)', sleeve_top=0.8)
SPECS = {
    1: optiplex,
    2: dict(name='Drive tray (3.5" HDD + 2.5" SSD)', drives=[['3.5', -89.725, 0], ['2.5', 19.875, 0]]),
    3: dict(name='7" touch screen plate (placeholder)', faceplate_only=True, layout='custom', u=3,
            ports=[dict(x=0, z=66.675, w=155, h=86, r=2, label='Screen', type='other')]),
    7: dict(name='Keystone panel, 10 (3 USB, 4 LAN, 3 blank)', faceplate_only=True, layout='keystones', u=1, count=10, rows=1),
    8: dict(name='TP-Link TL-SG108E', dev_w=158, dev_d=100, dev_h=25, u=1, device_mount='sleeve', joint='screw',
            rear_support=False, dev_rot=0, dev_off_x=-15, dev_off_y=0, holes=[], ports=[], rear_ports=[], keystones=[88],
            tray_follow=True, sleeve_top=0.85, labels=[{'text': 'UPLINK', 'x': 88, 'z': 3.8, 'size': 4.5}]),
    # Netgear CM1000 in its 3-piece bracket (faceplate + rails v2, outputs/STL_Deliveries/2026-10-16_CM1000_bracket).
    # Finished meshes can't be a wizard item, so the app shows a 1U plate standing in for the bracket.
    9: dict(name='Netgear CM1000 (bracket: faceplate + rails v2)', faceplate_only=True, layout='blank', u=1),
}
store = app.Store(data / 'library.sqlite3')
seed = store.project()
doc = rack_workspace.read(data, seed)
rack = doc['racks'][0]
assert rack['slots'] == 9, rack['slots']
existing = {i['name']: i for i in equipment.library(data)}
placements = [p for p in rack['placements'] if p['slot'] == 9 - 6 + 1]   # keep U6 Pi + Hue
for u, spec in SPECS.items():
    item = existing.get(spec['name']) or equipment.save_item(dict(spec, display_name=spec['name']), data)
    span = item['span']
    placements.append({'id': f'u{u}-{item["id"][3:]}', 'equipment': item['id'], 'slot': 9 - (u + span - 1) + 1, 'span': span,
                       'assembly': {'name': f'{spec["name"]} (U{u}' + (f'–U{u+span-1})' if span > 1 else ')')}})
    print('item', item['id'], item['name'], 'span', span)
rack['placements'] = placements
out = rack_workspace.save(data, doc, seed_project=seed, allow_project_changes=True,
                          canonical_project=lambda p: store.draft(p, project=p))
for p in sorted(out['racks'][0]['placements'], key=lambda p: p['slot']):
    print('slot', p['slot'], 'span', p['span'], p['assembly']['name'])
