from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sqlite3
r=Path(__file__).resolve().parents[2];f=Path(__file__).parent
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
before=json.loads((f/'Protected_Data_Before.json').read_text(encoding='utf-8'))
authorized=json.loads((f/'After_Authorized_Draft_Save.json').read_text(encoding='utf-8'))
hardware={name:digest(r/name)==value for name,value in before.items() if not name.endswith('rack-workspace.json') and 'rack-history' not in name and 'artwork' not in name}
after_authorized={name:digest(r/name)==value for name,value in authorized.items()}
baseline={name:digest(r/'outputs/Mechanical_Design_App'/name)==digest(r/'work/gui-restoration/before-app'/name) for name in ['pi4_baseline.scad','assembly.json','pi_reference.json','faceplate_mounting.py']}
db=sqlite3.connect((r/'data/normal-use/library.sqlite3').as_uri()+'?mode=ro',uri=True);integrity=db.execute('pragma integrity_check').fetchone()[0];db.close()
value={'time_utc':datetime.now(timezone.utc).isoformat(),'user_choices':'1C 2C 3A 4A 5A 6A 7A 8A','hardware_cache_unchanged':hardware,'all_files_match_authorized_save':after_authorized,'protected_baseline_unchanged':baseline,'sqlite_integrity':integrity,
 'python_tests':37,'node_suites':['atomic Save serialization and newer-draft retention, including invalid newer input','viewer appearance initialization replay','existing viewer controls','catalog handlers','Phase7 handlers','project context and depth-tested artwork'],
 'browser_checks':['collapsible inspector restores contextual actions','collapsible rack/equipment/hardware sections','Setup/Hardware/Appearance tabs','header Save commits hardware and colors together','new allocation requires explicit Save before opening','saved instance isolation after second allocation','local image fit/center and front preview','immediate post-reload artwork restores correctly','desktop layout and no console warnings/errors'],
 'normal_activation':{'user_authorization':'1, followed by explicit Save current draft and refresh reply','saved_user_draft':True,'rack':'My Lab Rax, 5 slots, 0 allocations','pid':25160,'port':8765,'starter_imports':0,'data':'data/normal-use','actual_source_mesh_colors':'retained from user draft'},
 'manufacturing_builds_exports':0,'limits':['preview-only colors/artwork','Pi4-only geometry adapter','rack planning/source preview, no rack STL generator','physical fit/strength/clearances UNKNOWN','Phase7 closed with limitations; mounting and niche research parked']}
(f/'Verification.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert all(hardware.values()) and all(after_authorized.values()) and all(baseline.values()) and integrity=='ok'
print(json.dumps({'protected_hardware_cache_files':len(hardware),'authorized_saved_files_unchanged_after_restart':len(after_authorized),'baseline':baseline,'sqlite':integrity}))
