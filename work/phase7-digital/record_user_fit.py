from pathlib import Path
import shutil,hashlib,json
root=Path.cwd();out=root/'outputs/Phase7_Physical_Observations/2026-10-18'
source=Path(r'C:/Users/brian/.codex/codex-remote-attachments/01a14e5b-bc7c-78b2-94b5-0ccbf997c2e7/B62C35CD-7391-40CC-993A-BC907BD6872F')
photos=[]
for i in range(1,4):
    src=source/f'{i}-Photo-{i}.jpg';dst=out/'photos'/f'Photo_{i}.jpg'
    if dst.exists():assert dst.read_bytes()==src.read_bytes(),'Refusing differing evidence overwrite'
    else:shutil.copy2(src,dst)
    photos.append({'file':str(dst.relative_to(root)),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
record={'date':'2026-10-18','specimen_id':'BRIAN-20261018-01','evidence_type':'User-reported qualitative fit with photographs','user_statement':'Fitment is fantastic','reported_result':'POSITIVE_FIT_REPORT_FOR_SHOWN_SPECIMEN','visual_observations':['Separate printed tray and faceplate shown alongside rulers.','Third photo shows tray and faceplate positioned together at the joint.'],'scope':'Record the reported specimen fit; no universal fit or strength approval.','exact_stl_revision':'UNKNOWN — awaiting identification; do not bind to digital acceptance build by appearance','hardware_installed':'UNKNOWN','calibrated_measurements':'NOT PROVIDED; no precise ruler/photo measurements inferred','pi_board_fit':'NOT ESTABLISHED by these photos','retention_torque_strength':'UNKNOWN — no test results supplied','rack_cable_tool_access':'UNKNOWN','mounting_matter':'Remains tabled; photos are not authorization to reopen it','further_physical_work_authorized':False,'photos':photos}
(out/'Observation.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
(out/'Observation.md').write_text('''# User-reported fit observation — 2026-10-18

Specimen: BRIAN-20261018-01. Brian reports: “Fitment is fantastic.” Three supplied photos are preserved with SHA-256 hashes in Observation.json. Separate parts and their assembled positioning are visible. This is positive qualitative evidence for the shown specimen.

Exact STL revision is not yet identified. Do not silently associate this specimen with the later digital acceptance build. No precise dimensions are inferred from the rulers or perspective. Pi-board fit, screw/insert installation, retention/torque, strength and service/rack access are not established by these photos. Mounting remains tabled. No new print or physical test was initiated or authorized by recording this observation.

This supplements, rather than overwrites, the earlier digital acceptance report's historical physical-not-started status. Before a revision-specific physical-fit disposition, identify the printed STL files/revision. No printer/slicer integration information is required.
''',encoding='utf-8')
for name in ['HANDOFF.md','PROJECT.md']:
    p=root/name
    text=p.read_text(encoding='utf-8')
    text+='''\n## User-provided physical observation — 2026-10-18\n\nBrian reports “Fitment is fantastic” and supplies three photographs of the printed parts, including assembled positioning. Evidence: outputs/Phase7_Physical_Observations/2026-10-18/Observation.md and Observation.json. This is a positive qualitative fit report for the shown specimen; the exact STL revision is not identified. Strength/retention, hardware installation, Pi-board and rack/service fit remain unestablished by these photos. Earlier no-physical-work statements describe the state before this user report. No further printing/testing is authorized; mounting remains tabled. Remaining niche insert research is parked at Brian's direction; retain documented UNKNOWNs.\n'''
    p.write_text(text,encoding='utf-8')
print('Preserved 3 original photos with hashes and recorded specimen-specific fit report. No geometry or catalog changes.')
