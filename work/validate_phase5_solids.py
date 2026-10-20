"""Reproduce bounded baseline solid checks in work/, never rewrite mechanical assets."""
from pathlib import Path
import hashlib,json,subprocess,sys
sys.path.insert(0,str(Path('outputs/Mechanical_Design_App').resolve()))
from mesh_revision import compiler
from pi_validation import solid_result
root=Path('outputs/Mechanical_Design_App'); folder=Path('work/phase5-solid-checks');folder.mkdir(exist_ok=True)
raw=(root/'pi4_baseline.scad').read_bytes(); source=raw.decode('utf-8');body=source.split('if(part=="faceplate")')[0]
expressions={
 'tray_faceplate':'intersection(){tray();translate([0,-0.001,0])faceplate();}',
 'nominal_pcb':'intersection(){tray();translate([-44,13,16.001])cube([85,56,1.6]);}',
 'positive_joint_clash':'intersection(){tray();translate([0,0.4,0])faceplate();}'
}
report={'schema':1,'source_sha256':hashlib.sha256(raw).hexdigest(),'compiler':compiler(),'results':{}}
for name,expression in expressions.items():
 src=folder/(name+'.scad');dst=folder/(name+'.stl');src.write_text(body+expression,encoding='utf-8')
 r=subprocess.run([compiler(),'-o',str(dst),str(src)],capture_output=True,text=True,timeout=180,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
 log=r.stderr;empty='Current top level object is empty.' in log
 state=solid_result(log,empty,r.returncode)
 report['results'][name]={'returncode':r.returncode,'empty':empty,'log':log,'expression':expression,'status':state,'test_source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'result_mesh_sha256':hashlib.sha256(dst.read_bytes()).hexdigest() if dst.exists() else None}
 print(name,state,flush=True)
 assert state==('fail' if name=='positive_joint_clash' else 'pass'),log
(root/'joint_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(folder/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Pinned solid evidence recorded; mechanical baseline unchanged.')
