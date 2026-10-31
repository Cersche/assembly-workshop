"""Move the screen + Pi + Hue unit to U6-U5 and the drive tray to U3 (Brian, 2026-10-29).

Usage: python apply_move_screen_u6u5.py <data-dir>     (use a disposable copy first; normal-use only with Brian's OK)

Layout after: U9 CM1000, U8 TL-SG108E, U7 keystone panel, U6-U5 SCR5-F (app placeholder item), U4 empty,
U3 drive tray, U2 empty (cooling), U1 OptiPlex. Assembly names get their current U labels.
rack_workspace.save() writes the previous document to rack-history/ first.
Stored slot numbers count from the top; U = slots - slot + 1.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'outputs' / 'Mechanical_Design_App'))
import app, rack_workspace  # noqa: E402

data = Path(sys.argv[1])
store = app.Store(data / 'library.sqlite3')
seed = store.project()
doc = rack_workspace.read(data, seed)
rack = doc['racks'][0]
SLOTS = rack['slots']
slot_for_u = lambda u: SLOTS - u + 1
by_id = {p['id']: p for p in rack['placements']}
screen, drive = by_id['u4-u3-scr5e'], by_id['u2-90c95fdb9fce']
screen.update(slot=slot_for_u(6), span=2)
screen['assembly']['name'] = 'Screen + Pi + Hue SCR5-F (U6-U5)'
drive['slot'] = slot_for_u(3)
drive['assembly']['name'] = 'Drive tray (3.5" HDD + 2.5" SSD) (U3)'
out = rack_workspace.save(data, doc, seed_project=seed, allow_project_changes=True,
                          canonical_project=lambda p: store.draft(p, project=p))
r = out['racks'][0]
print(sorted((SLOTS - p['slot'] - p['span'] + 2, SLOTS - p['slot'] + 1, p['assembly']['name']) for p in r['placements']))
