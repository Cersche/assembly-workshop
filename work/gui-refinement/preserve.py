from pathlib import Path
import hashlib,json,shutil
r=Path.cwd(); f=r/'work/gui-refinement'; b=f/'before-app';b.mkdir(exist_ok=True)
for name in ('app.py','assembly_records.py','rack_workspace.py','workspace.js','workspace.css','index.html','viewer.js'):
    shutil.copy2(r/'outputs/Mechanical_Design_App'/name,b/name)
for name in ('HANDOFF.md','PROJECT.md','AGENTS.md'): shutil.copy2(r/name,f/('before-'+name))
h={str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (r/'data/normal-use').rglob('*') if p.is_file()}
(f/'Protected_Data_Before.json').write_text(json.dumps(h,indent=2),encoding='utf-8')
(f/'Decisions.json').write_text(json.dumps({'source':'Brian selection 2026-10-18','choices':{'1':'C hybrid, collapsible inspector','2':'C collapsible racks/equipment/hardware, revisit later','3':'A select + ellipsis/right-click','4':'A Setup/Hardware/Appearance tabs','5':'A one explicit Save','6':'A swatches plus custom color','7':'A image fit/center, size, position, remove','8':'A navigation and slot actions first'},'artwork':'preview only; STL later'},indent=2),encoding='utf-8')
