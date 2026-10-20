from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sqlite3
root=Path(__file__).resolve().parents[2];folder=Path(__file__).parent
before=json.loads((folder/'Protected_Data_Before.json').read_text(encoding='utf-8'))
same={name:hashlib.sha256((root/name).read_bytes()).hexdigest()==digest for name,digest in before.items()}
baseline={}
for name in ('pi4_baseline.scad','assembly.json','pi_reference.json','faceplate_mounting.py'):
    current=root/'outputs/Mechanical_Design_App'/name;old=root/'work/gui-restoration/before-app'/name
    if old.exists():baseline[name]=hashlib.sha256(current.read_bytes()).hexdigest()==hashlib.sha256(old.read_bytes()).hexdigest()
db=sqlite3.connect((root/'data/normal-use/library.sqlite3').as_uri()+'?mode=ro',uri=True)
integrity=db.execute('pragma integrity_check').fetchone()[0];db.close()
result={'time_utc':datetime.now(timezone.utc).isoformat(),'normal_use_files_unchanged':same,'mechanical_baseline_unchanged':baseline,'sqlite_integrity':integrity,
        'python_checks':{'rack_documents':7,'exact_source_reference':3,'independent_assemblies':10,'existing_non_mounting_app':11},
        'node_checks':['context headers and stale responses','save preserves newer hardware drafts','depth-tested texture coverage','catalog handlers','Phase7 handlers','viewer controls','viewer depth','rack scene','21-component reference UI','allocation actions and serialized saves'],
        'browser_disposable_checks':['create/save/open two independent assemblies','slot A pins and pilot do not change slot B','save/reload retains faceplate colors and image','front image visible without covering mounting openings','whole rack color and source-component override survive reload','right-click and ellipsis slot menu','unsaved hardware blocks switching slots'],
        'normal_use':{'url':'http://127.0.0.1:8765/','pid':19424,'existing_library':True,'read_only_inspection':'five slots, zero allocations; normal data not saved or migrated','previous_tab':'not available in current browser session; no older tab reloaded, saved or cancelled'},
        'limits':['GUI options are concepts, not an applied redesign','Pi4 is the only manufacturing adapter','image preview only; no STL artwork or colors','no installed equipment transforms or rack-frame STL','fit/strength/interfaces remain UNKNOWN'],
        'manufacturing_builds_exports':0}
(folder/'Verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert all(same.values()) and all(baseline.values()) and integrity=='ok'
print(json.dumps({'normal_files':len(same),'all_unchanged':all(same.values()),'baseline':baseline,'sqlite':integrity}))
