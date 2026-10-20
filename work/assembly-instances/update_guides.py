from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=root/'AGENTS.md';s=p.read_text(encoding='utf-8').replace('Pi4 remains the only manufacturing geometry adapter and hardware pins remain shared.', 'Pi4 remains the only manufacturing geometry adapter. Each saved slot allocation now has independent assembly hardware pins/inputs/revisions; the legacy project is preserved and copied once for new assemblies. Appearance and local image assets are preview-only. Preserve rack-history/ and artwork/ with the rack document.')
p.write_text(s,encoding='utf-8')
p=root/'PROJECT.md';s=p.read_text(encoding='utf-8').replace('Arbitrary equipment/CAD manipulation and independent per-slot hardware projects are not implemented. Pi4 placements share the existing hardware project.', 'Saved Pi4 placements now own independent hardware snapshots, inputs and revisions. Arbitrary equipment/CAD manipulation remains unimplemented. Colors and local faceplate images are preview-only; image-to-STL work is deferred by Brian.')
s=s.replace('workflow audit added', 'workflow audit added')
s=s.replace('Workflow audit added draft-only', 'Independent assemblies, preview colors/images and slot context menus were subsequently implemented and tested; see `work/assembly-instances/Report.md`. Two interactive GUI concepts (Focused studio / Canvas-first) await Brian’s refinement choice. Preserve artwork/ with rack documents/history.\n\nWorkflow audit added draft-only')
p.write_text(s,encoding='utf-8')
p=root/'HANDOFF.md';s=p.read_text(encoding='utf-8').replace('Only the existing Pi4 geometry adapter works. Slot allocations reference a **shared Pi4 hardware project**, not independent per-slot pins or revisions.', 'Only the existing Pi4 geometry adapter works. Saved slot allocations now own independent assembly hardware snapshots, inputs and revisions. The legacy Pi4 SQLite project remains preserved; new instances copy it once. See the latest independent-assemblies note below, which supersedes earlier shared-project statements.')
s=s.replace('Remaining highest-priority gap is independent per-slot assembly records/pins, followed by', 'That audit’s independent per-slot gap is now closed by the subsequent work below. Remaining priorities include')
s+='''

## Independent assemblies, colors, artwork and GUI options — 2026-10-18

Brian requested closing the per-slot hardware gap, colors, local faceplate images and two streamlined GUI choices. He explicitly selected **preview first; STL artwork later**. Implemented/verified details: `work/assembly-instances/Report.md`, `Verification.json`, before-app/before-guides safety copies and screenshots there.

Each saved Pi4 allocation now contains a stable independent assembly ID, hardware snapshot, inputs and revision in rack workspace v2. A new allocation copies legacy pins once. Save layout & open assembly is explicit; hardware saves are scoped, stale writes/wrong-instance bundles blocked. V1 reads normalize in memory only; explicit save preserves the prior v1 file in rack-history. Legacy SQLite project, immutable part revisions and mesh caches remain intact. Generic layout saves cannot overwrite instance hardware. Draft switching is guarded; saved release undo restores the latest hardware snapshot.

Rack/source-component colors and equipment-reference/tray/faceplate colors are visual-only. Local PNG/JPEG/WebP chooser stores a bounded PNG under data/artwork by SHA256; image size/position are saved with appearance. Faceplate front triangles receive depth-tested artwork without filling mounting openings. Save layout preserves appearance. STL files have no colors or image geometry. Preserve **artwork/** with rack-workspace.json, rack-history/, library.sqlite3 and revisions/.

Ellipsis and right-click slot actions are implemented in the existing studio. Broader redesign remains unchosen: interactive **Focused studio** (compact tree + contextual inspector) and **Canvas-first** (slot rail + selection dock) concepts are supplied for Brian's refinement. These are new concepts grounded in the recovered direction, not recovered old screenshots. Recommended: Focused studio.

31 Python checks and targeted Node suites PASS; disposable8767 browser checks verified isolation, draft guards, reload persistence, rack component colors, Pi reference color and faceplate artwork. No build/source export or tabled mechanical tests ran. All7 normal-use file hashes unchanged, SQLite integrity ok and protected baseline unchanged. No normal-use acceptance writes. Old PID28892 was verified/restarted; **normal server PID19424** now runs existing-library on8765 with0 starter imports. A clean normal-use tab was inspected read-only and shows the real five-slot rack/zero allocations. The older unconfirmed slot5 wizard was not present in the current browser inventory; no older page was refreshed or altered.

Remaining: installed-equipment transforms and rack clearance/interface evidence, explicit source component/stack editing, additional geometry adapters, recovery UI, eventual image-to-STL artwork and rack-frame manufacturing support. Physical UNKNOWNs/rights restrictions remain; Phase7 closed with limitations, mounting tabled and niche research parked. No automatic render, print, purchases, remote upload, release packaging, publishing, deployment or push.
'''
p.write_text(s,encoding='utf-8')
p=root/'work/gui-restoration/Restoration_Report.md';s=p.read_text(encoding='utf-8')
s+='''

## Subsequent independent-instance and appearance work — 2026-10-18

The earlier shared-project limitation is superseded: saved Pi4 allocations now own independent hardware/inputs/revisions, with legacy project preserved. Actual source-mesh rack previews, preview colors/local faceplate artwork and slot context menus are implemented. Brian chose preview-only artwork for now. See `../assembly-instances/Report.md` for scope, verified checks and two proposed GUI directions awaiting refinement. This does not implement arbitrary equipment/CAD, installed rack clearance, image geometry in STL or a rack-frame generator. Earlier restoration/recovery notes remain historical evidence.
'''
p.write_text(s,encoding='utf-8')
