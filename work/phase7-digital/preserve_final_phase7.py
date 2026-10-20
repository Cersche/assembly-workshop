from pathlib import Path
import shutil,hashlib,json
root=Path.cwd().resolve();out=root/'outputs/Phase7_Closeout'
backup=Path(r'C:/Users/brian/Documents/Codex/2026-10-18/yaml-continue-assembly-workshop-from-c/outputs/Phase7_Final_Preservation_20261018').resolve()
assert root not in backup.parents and backup not in root.parents
assert not backup.exists(),'Never overwrite a preservation snapshot'
manifest=[]
for src in sorted(root.rglob('*')):
    if not src.is_file():continue
    relative=src.relative_to(root);dst=backup/relative
    dst.parent.mkdir(parents=True,exist_ok=True)
    before=hashlib.sha256(src.read_bytes()).hexdigest()
    shutil.copy2(src,dst)
    copied=hashlib.sha256(dst.read_bytes()).hexdigest();after=hashlib.sha256(src.read_bytes()).hexdigest()
    assert before==copied==after,str(relative)
    manifest.append(dict(file=relative.as_posix(),bytes=src.stat().st_size,sha256=before))
# Keep an additional local copy of the externally delivered earlier STL sources.
provenance=json.loads((root/'outputs/Phase7_Physical_Observations/2026-10-18/Recovered_Test_File_Provenance.json').read_text(encoding='utf-8'))
external=[]
for index,item in enumerate(provenance['original_delivery']+provenance['later_explicit_replacement']):
    src=Path(item['path']);dst=backup/'earlier_test_fit_stls'/str(index+1)/src.name;dst.parent.mkdir(parents=True)
    shutil.copy2(src,dst);assert hashlib.sha256(dst.read_bytes()).hexdigest()==item['sha256']
    external.append(dict(source=str(src),copy=str(dst),sha256=item['sha256']))
(backup/'Snapshot_Manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
report=dict(date='2026-10-18',source=str(root),snapshot=str(backup),files=len(manifest),bytes=sum(x['bytes'] for x in manifest),all_source_copy_hashes_match=True,external_test_stls=external,includes='Entire project at snapshot time, including .git, untracked app/work/outputs/evidence, photos and any workspace data',scope='Local raw preservation copy; not a release package or off-machine backup',git_timing='Snapshot .git precedes the final handoff commit; latest working docs/source are included. The local handoff commit is separate and contains guidance only.',manifest=str(backup/'Snapshot_Manifest.json'))
(out/'Preservation_Report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
shutil.copy2(out/'Preservation_Report.json',backup/'outputs/Phase7_Closeout/Preservation_Report.json')
print(json.dumps({k:report[k] for k in ['snapshot','files','bytes','all_source_copy_hashes_match']}))
