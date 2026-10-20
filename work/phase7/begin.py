from pathlib import Path
import json,hashlib,sys
root=Path.cwd()
app=root/'outputs/Mechanical_Design_App'
out=root/'outputs/Phase7_Start'
assert not (out/'Configuration_Snapshot.json').exists(),'Do not overwrite a prior snapshot'
sys.path.insert(0,str(app))
import catalog_evidence,catalog_packs
from app import evaluate,positive_inputs
records=json.loads((app/'starter-hardware.json').read_text(encoding='utf-8'))
selected=[next(p for p in records if p['id']==i and p['revision']==1) for i in ('accu-sscf-m3-8-a2','mcmaster-94459a140')]
manifest=json.loads((app/'pi_reference_manifest.json').read_text(encoding='utf-8'))
checks=[]
for f,key in [('pi4_baseline.scad','baseline_source_sha256'),('assembly.json','baseline_assembly_sha256'),('pi_reference.json','sha256')]:
    actual=hashlib.sha256((app/f).read_bytes()).hexdigest()
    assert actual==manifest[key]
    checks.append(dict(file=f,sha256=actual,status='PASS'))
packs=catalog_packs.inventory()['packs']
assert len(packs)==7 and all(p['available'] for p in packs)
inputs=positive_inputs({'pilot':4})
trial=evaluate(selected[0],selected[1],inputs)
snapshot=dict(schema=1,date='2026-10-18',phase='7 — nonphysical preparation started',project_home=str(root),project_id='23bbc12a-5bb0-42a8-8c3f-a060bf2d0ea0',scope='Local recorded candidate audit; not active data or actual hardware confirmation',protected_hashes=checks,candidate_records=selected,candidate_record_status='Historical disposable trial only; NOT newly selected or saved',resolved_trial_inputs=inputs,inputs_status='Digital trial inputs/defaults, not measurements or approved physical criteria',audit=[catalog_evidence.inspect(p) for p in selected],trial_rule_report=trial,actual_configuration={k:'UNKNOWN' for k in ['board_revision','rack_environment','accessories','printer','material','slicer_process','hardware_in_hand','heat_tool_tip','driver_envelope','measurement_instruments','loads','temperature_requirements','torque_retention_cycle_criteria','live_user_data_path']},physical_testing='NOT_STARTED',physical_approval=False,geometry_generated=False)
(out/'Configuration_Snapshot.json').write_text(json.dumps(snapshot,indent=2,ensure_ascii=False),encoding='utf-8')
(out/'Entry_Checks.json').write_text(json.dumps(dict(protected_files=checks,pack_hashes='7 PASS',candidate_rule_status=trial['status'],candidate_checks=trial['checks'],limits='No physical validation or fresh browser/build claim'),indent=2),encoding='utf-8')
(out/'HANDOFF_before_Phase7.md').write_bytes((root/'HANDOFF.md').read_bytes())
handoff=(root/'HANDOFF.md').read_text(encoding='utf-8')
handoff=handoff.replace('Phase7 NOT STARTED.','Phase7 nonphysical preparation STARTED; see outputs/Phase7_Start/Status.md and docs/phase7-readiness/Readiness_Plan.md. Physical work NOT STARTED.')
handoff=handoff.replace('Phase6 closed at Brian\'s explicit instruction; next is Phase7 planning.','Phase6 closed at Brian\'s explicit instruction; Phase7 nonphysical configuration/evidence preparation has begun.')
handoff=handoff.replace('Root AGENTS.md absent; check again.','Root AGENTS.md now exists and contains persistent development guidance.')
(root/'HANDOFF.md').write_text(handoff,encoding='utf-8')
p=(root/'PROJECT.md').read_text(encoding='utf-8')
a=p.index('A local project named Assembly Workshop now exists')
b=p.index('\n\nConversation history',a)
p=p[:a]+'''A local project named Assembly Workshop exists (ID 23bbc12a-5bb0-42a8-8c3f-a060bf2d0ea0). Its primary path was verified through list_projects as C:/Users/brian/Documents/Codex/2026-10-17/Assembly Workshop on 2026-10-18. Current chat 01a14e5b-bc7c-78b2-94b5-0ccbf997c2e7 belongs to the project. This existing chat retains its separate Documents/ChatGPT/Assembly Workshop cwd; run app commands with the canonical project root explicitly.''' +p[b:]
p=p.replace('Next: set the renamed Git root as the existing Assembly Workshop project\'s primary folder and verify its path through list_projects;','Next: continue Phase 7 from outputs/Phase7_Start/Status.md;')
(root/'PROJECT.md').write_text(p,encoding='utf-8')
print(json.dumps(dict(protected_hashes='3 PASS',packs='7 PASS',candidate_rule_status=trial['status'],trial_inputs=inputs,candidate_checks=trial['checks']),indent=2))
