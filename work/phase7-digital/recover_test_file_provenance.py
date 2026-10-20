from pathlib import Path
import hashlib,json
root=Path.cwd();out=root/'outputs/Phase7_Physical_Observations/2026-10-18'
base=Path(r'C:/Users/brian/Documents/Codex/2026-10-18/continue-assembly-workshop-from-c-users/outputs')
original=base/'Pi4_Test_Fit_Parts';replacement=base/'Pi4_Four_Corner_Test_Fit'
manifest=json.loads((original/'test_fit_manifest.json').read_text(encoding='utf-8'))
verified=[]
for part in manifest['parts']:
    path=original/part['file'];actual=hashlib.sha256(path.read_bytes()).hexdigest();assert actual==part['sha256']
    verified.append({'path':str(path),'sha256':actual,'original_manifest_matches':True})
assembly=json.loads((replacement/'assembly.json').read_text(encoding='utf-8'))
updated=[]
for filename,part_id in [('Pi4_Tray_Clearance_v2_TEST_FIT.stl','tray'),('Pi4_Faceplate_FOUR_CORNER_Pilot4mm_TRIAL.stl','faceplate')]:
    path=replacement/filename;actual=hashlib.sha256(path.read_bytes()).hexdigest()
    part=next(p for p in assembly['parts'] if p['id']==part_id);assert actual==part['source_sha256']
    updated.append({'path':str(path),'sha256':actual,'saved_assembly_hash_matches':True})
record={'chat_title':'Validate Phase 5 readiness','chat_id':'01a14dde-e57e-7063-b72b-f9e4a0dbce49','request_turn':'01a14dff-bfa0-7b81-995c-b07c352effef','user_request':"Great. We're going to handoff to a new session for phase 6. before we do that, please provide me with the stl that you wanted me to print out and test fit.",'original_delivery':verified,'original_build_id':manifest['build_id'],'later_explicit_replacement':updated,'replacement_build_id':'bbbe12450805205dfcb2be26f02d707bd53c3030e21970631539be2d3cd27937','provenance':'Recovered exact supplied test-fit files and later replacement from earlier chat and verified saved hashes. Full tray, not a separate small coupon.','photo_link_scope':'User points to these earlier supplied test-fit parts. File delivery is verified; a photo cannot independently recover the printed STL hash. Do not associate this print with the later Phase7 digital acceptance build.','mounting':'Historical file identification only; matter not reopened or reassessed.'}
(out/'Recovered_Test_File_Provenance.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
p=out/'Observation.json';observation=json.loads(p.read_text(encoding='utf-8'))
observation['exact_stl_revision']='Earlier supplied test-fit pair recovered from chat; later replacement build bbbe12450805205dfcb2be26f02d707bd53c3030e21970631539be2d3cd27937 is the documented replacement. Direct print-file hash not provided.'
observation['file_provenance']='Recovered_Test_File_Provenance.json'
p.write_text(json.dumps(observation,indent=2),encoding='utf-8')
p=out/'Observation.md';s=p.read_text(encoding='utf-8');s+='''\n## Earlier chat and file provenance recovered\n\nThe pre-Phase6 request and supplied STLs were found in “Validate Phase 5 readiness” (01a14dde-e57e-7063-b72b-f9e4a0dbce49). The initial full tray and trial faceplate are in the earlier chat outputs/Pi4_Test_Fit_Parts. That same chat later explicitly supplied a replacement faceplate and unchanged matching tray in outputs/Pi4_Four_Corner_Test_Fit, build bbbe12450805205dfcb2be26f02d707bd53c3030e21970631539be2d3cd27937. Both sets' STL hashes match their stored evidence. This recovers delivery provenance without making Brian locate the files again. These parts predate the Phase7 acceptance build; photos do not independently prove file hashes. No mounting reassessment or geometry change occurred. See Recovered_Test_File_Provenance.json.\n''';p.write_text(s,encoding='utf-8')
for name in ['HANDOFF.md','PROJECT.md']:
    p=root/name;s=p.read_text(encoding='utf-8');s+='''\n### Recovered earlier test-fit delivery\nThe requested pre-Phase6 test-fit files were located in chat Validate Phase 5 readiness (01a14dde-e57e-7063-b72b-f9e4a0dbce49). Initial pair: the prior workspace outputs/Pi4_Test_Fit_Parts; later explicit replacement pair: outputs/Pi4_Four_Corner_Test_Fit, build bbbe12450805205dfcb2be26f02d707bd53c3030e21970631539be2d3cd27937. File hashes verified against saved manifests/assembly. This supplies historical provenance for Brian's reported specimen, without attributing it to the later Phase7 digital build. See outputs/Phase7_Physical_Observations/2026-10-18/Recovered_Test_File_Provenance.json. No new tests or mounting reassessment.\n''';p.write_text(s,encoding='utf-8')
print('Recovered initial and replacement test-fit files; all 4 STL hashes match saved evidence. Photo record and handoffs updated.')
