from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
root=Path(__file__).resolve().parents[2];folder=Path(__file__).parent
paths=['app.py','rack_workspace.py','assembly_records.py','workspace.js','workspace.css','index.html','viewer.js','test_assembly_records.py','rack-references/rack-scene.js','rack-references/asset-manifest.json']
manifest=[]
for name in paths:
    path=root/'outputs/Mechanical_Design_App'/name
    manifest.append({'path':str(path.relative_to(root)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
for name in ('AGENTS.md','PROJECT.md','HANDOFF.md','work/assembly-instances/Report.md'):
    path=root/name;manifest.append({'path':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
prototype=Path('C:/Users/brian/.codex/visualizations/2026/10/18/01a14f51-2a90-7a30-8627-77653e78e987/rack-studio-options.html')
copy=folder/'rack-studio-options.html';copy.write_bytes(prototype.read_bytes())
manifest.append({'path':str(copy.relative_to(root)),'sha256':hashlib.sha256(copy.read_bytes()).hexdigest()})
(folder/'After_State_Manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
stamp=datetime.now(timezone.utc).isoformat()
memory='''

## Independent assemblies, preview appearance and GUI options — STAMP

Brian asked to close the independent per-slot hardware gap, add rack/equipment/component colors, local faceplate images and two streamlined GUI options. He explicitly chose preview first; STL artwork later. Implemented stable instance IDs/hardware snapshots/inputs/revisions in rack workspace v2; new records copy legacy pins once. Legacy SQLite project stays unchanged. V1 read normalization is in memory only; explicit saves retain history. Scoped state/preview/check/BOM/project/export identities, stale generation/revision guards, wrong-instance bundle rejection, old-client protection, guarded switching and release undo. No render/source export ran and mechanical adapter/baseline stayed unchanged.

Whole-rack colors plus overrides per source component type; equipment color for optional detailed Pi reference and tray/faceplate colors. Local PNG/JPEG/WebP chooser produces bounded content-hashed PNGs in data/artwork; saved appearance holds position/size. Front-only depth-tested texturing and faceplate-front view preserve openings. Colors/artwork are preview-only and excluded from hardware/STL identity. Save layout persists appearance; preserve artwork/ with workspace/history/library/revisions. Ellipsis/right-click/keyboard slot menu implemented in existing studio. Larger redesign unchosen: inline interactive Focused studio (recommended compact tree + contextual inspector) and Canvas-first (slot rail + bottom selection dock) are concepts for Brian to refine. Do not silently choose/apply a redesign or image-to-STL work.

31 targeted Python checks and Node context/pixel/viewer/catalog/Phase7/reference/scene/allocation checks PASS. Disposable8767 browser verified two instances stay isolated, hardware draft switching guard, color/image persistence/reload, actual source-post overrides, detailed equipment-reference color and faceplate front artwork; no console warnings/errors. GUI options checked at1024 and320 widths, no horizontal overflow. All7 normal-use file hashes unchanged, SQLite integrity ok, protected SCAD/assembly/Pi/mounting baseline unchanged. Evidence/safety copies/manifests/screenshots: work/assembly-instances/. HANDOFF/PROJECT/AGENTS updated.

Verified/restarted normal old PID28892 to new PID19424, existing-library data/normal-use port8765,6 revisions/0 starter imports. New normal tab inspected read-only: My Lab Rax5 slots/0 allocations; real saved v1 JSON unchanged. Earlier unconfirmed slot5 wizard was not accessible in this browser session; no older tab saved/refreshed/cancelled. New normal tab retained. Temporary test/GUI tabs and servers cleaned up after checks; normal server stays running. No CAD build/export, physical work, remote upload, release, publishing or push. Phase7 stays CLOSED WITH LIMITATIONS; mounting tabled, niche research parked. Still missing installed-equipment transforms/clearances, exact interfaces, explicit stack editor, other adapters, history UI, STL artwork and rack-frame manufacturing. Physical fit/strength/usable depth/M6 specification remain UNKNOWN.
'''.replace('STAMP',stamp)
(folder/'Memory_Append.md').write_text(memory,encoding='utf-8')
print('Preserved final source hashes and prepared automation-memory append.')
