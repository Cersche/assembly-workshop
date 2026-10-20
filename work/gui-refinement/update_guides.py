from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
r=Path(__file__).resolve().parents[2];f=Path(__file__).parent
p=r/'AGENTS.md';s=p.read_text(encoding='utf-8')
s+='''

## Selected hybrid GUI — Brian, 2026-10-18

Brian chose1C/2C/3A/4A/5A/6A/7A/8A: hybrid with collapsible inspector; collapsible Racks & slots, Equipment and Hardware on the left (2C is provisional for later review); click selects, ellipsis/right-click actions; Setup/Hardware/Appearance tabs; one explicit atomic Save; color presets plus custom picker; local artwork fit/center, size/position/remove; navigation first. These choices supersede the earlier unchosen concepts. Implemented pass and acceptance: work/gui-refinement/Report.md. Drafts remain unsaved until Save; checks/exports do not silently save them. Artwork remains preview-only. Do not silently replace the left grouping before Brian reviews it.
''';p.write_text(s,encoding='utf-8')
p=r/'PROJECT.md';s=p.read_text(encoding='utf-8').replace('Two interactive GUI concepts (Focused studio / Canvas-first) await Brian’s refinement choice.', 'Brian selected the hybrid refinement: collapsible left libraries and inspector, Setup/Hardware/Appearance tabs, shared slot context actions and one explicit atomic Save. See `work/gui-refinement/Report.md`; left grouping is provisional for review.')
p.write_text(s,encoding='utf-8')
p=r/'HANDOFF.md';s=p.read_text(encoding='utf-8')
s+='''

## Chosen hybrid GUI applied and activated — 2026-10-18

Brian selected **1C,2C,3A,4A,5A,6A,7A,8A**. The prior unchosen-concept note is superseded. Implemented: collapsible inspector and compact Racks & slots / Equipment / Hardware sections; click selection with ellipsis/right-click actions; Setup / Hardware / Appearance tabs; header-only explicit Save with Ctrl/Cmd+S; color swatches/custom pickers; local artwork fit/center and existing size/position/remove controls. Left grouping2C is provisional for later review. See `work/gui-refinement/Report.md`, Decisions.json, Verification.json and screenshots.

`/api/studio-save` preflights and atomically commits layout, appearance and open independent hardware draft in one JSON write. Failed hardware/stale generations/tampering reject all submitted project changes. New allocations require explicit header Save before opening; check/export actions require saved drafts. Save receipts preserve newer edits and advance generation/revision even if newer input becomes invalid. Hardware previews refresh after save. Viewer retains/replays appearance when opened before initialization completes, fixing an observed missing-artwork startup race.

The normal tab contained unsaved rack/component colors. Brian explicitly authorized **Save current draft and refresh** (reply1 and structured reply). Saved with the old valid session before restarting, then refreshed the same tab. Actual rack colors are retained; My Lab Rax5 slots/0 allocations. After_Authorized_Draft_Save.json and Authorized_Rack_Draft.json preserve that user action. All8 files match after restart; six library/cache files and four protected baseline files are unchanged. SQLite integrity ok.

**Current normal server PID25160**, --existing-library, data/normal-use, port8765,6 revisions/0 starter imports. Replaces verified old19424; no duplicate normal listener. Refined normal tab retained. Disposable8767 used separate fresh test data, not active user data.37 targeted Python checks PASS plus actual JavaScript Save/race/viewer/catalog/Phase7/context checks. Browser verified collapse/tabs, one combined save, explicit-save-before-open, second-instance isolation, fit/center artwork and immediate reload replay; no console warnings/errors. Narrow viewport override did not affect the background test tab, so narrow visual acceptance is not claimed. No CAD builds/exports/physical work; Phase7 remains closed with limitations, mounting/niche research parked. All rack/fit/strength/rights limitations remain.

Next: Brian's review of the left section grouping and contextual flow. Keep the selected hybrid and actual source-mesh rack; do not fall back to a Pi4-only product form. Preserve workspace/history/artwork/library/cache together.
''';p.write_text(s,encoding='utf-8')
manifest=[]
for name in ('app.py','assembly_records.py','workspace.js','workspace.css','index.html','viewer.js','test_studio_save.py'):
    path=r/'outputs/Mechanical_Design_App'/name;manifest.append({'path':str(path.relative_to(r)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
for name in ('HANDOFF.md','PROJECT.md','AGENTS.md','work/gui-refinement/Report.md','work/gui-refinement/Decisions.json'):
    path=r/name;manifest.append({'path':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(f/'After_State_Manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
stamp=datetime.now(timezone.utc).isoformat()
text='''

## Selected hybrid GUI applied — STAMP

Brian chose1C,2C,3A,4A,5A,6A,7A,8A. Hybrid with collapsible inspector; collapsible Racks & slots/Equipment/Hardware left sections (2C provisional for later review); click selects, ellipsis/right-click actions; Setup/Hardware/Appearance tabs; one explicit atomic header Save; swatches/custom picker; artwork fit/center/size/position/remove; navigation first. Implemented and activated, superseding earlier unchosen concepts. Current source work/gui-refinement/Report.md, Decisions.json, Verification.json, before-app/guides and source hashes/screenshots. Do not silently switch left grouping before Brian reviews it.

New studio-save endpoint preflights layout/appearance/open independent hardware and commits once atomically. Stale/tampered/invalid hardware rejects all. New allocations require Save before Hardware opens; checks/exports do not silently save. Saves retain newer layout/hardware edits, even invalid newer input, and refresh hardware envelopes. Browser exposed a viewer-init appearance race: current appearance is now retained/replayed after startup; delayed-init regression and immediate reload/open browser checks pass. Artwork remains preview-only; no STL art or color metadata.

37 targeted Python checks and JS Save/race/viewer/catalog/Phase7/context suites PASS. New disposable8767 browser verified collapse, tabs, one hardware+color Save, save-before-open, slot isolation, local fit/center art/persistence and startup replay; no console warnings/errors. Narrow viewport overrides did not resize the background tab, so no narrow visual acceptance claim. No rendering/build/source export/manufacturing export/physical work.

Normal tab had unsaved rack colors. Brian replied1 and explicitly Save current draft and refresh. Saved old valid session first, then verified/restarted old19424 to normal PID25160, --existing-library data/normal-use port8765,6 revisions/0 starter imports, and refreshed SAME tab. My Lab Rax5 slots/0 allocations, user component colors retained. After-authorized-save8 files unchanged across restart; original6 library/cache hashes and protected4 baseline hashes unchanged, SQLite ok. New saved rack/history are user data, not test fixtures. Normal tab/server retained; disposable server/tab cleaned up. Preserve workspace/history/artwork/library/cache. Phase7 closed with limitations, mounting tabled, niche research parked; geometry/physical/rights UNKNOWNs remain. Next is Brian's assessment/refinement of the selected hybrid and provisional left grouping, not another source hunt or Pi4-only redesign.
'''.replace('STAMP',stamp)
(f/'Memory_Append.md').write_text(text,encoding='utf-8')
print('Updated selected GUI guidance, source hashes and run-memory summary.')
