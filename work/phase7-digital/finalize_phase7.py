from pathlib import Path
import json,hashlib
root=Path.cwd();out=root/'outputs/Phase7_Closeout'
assert not (out/'Closeout_Report.md').exists(),'Do not overwrite final closeout'
for relative in ['outputs/Mechanical_Design_App/index.html','outputs/Mechanical_Design_App/README.md','HANDOFF.md','PROJECT.md','AGENTS.md']:
    p=root/relative;target=out/('before_final_'+p.name)
    if not target.exists():target.write_bytes(p.read_bytes())
p=root/'outputs/Mechanical_Design_App/index.html';s=p.read_text(encoding='utf-8')
s=s.replace('PHASE 7 OF 7 · DIGITAL VALIDATION','PHASE 7 OF 7 · CLOSED WITH LIMITATIONS')
s=s.replace('6 of 7 phases complete; Phase 7 is in progress.','7 of 7 phases complete, with documented limitations. Brian reports positive fit of the earlier printed test specimen; strength and installation approval remain unknown.')
s=s.replace('In progress — Digital STL/export acceptance; optional physical validation later with separate authorization','Complete with limitations — Digital STL/export acceptance and user-confirmed specimen fit; strength/installation remain unknown')
p.write_text(s,encoding='utf-8')
p=root/'outputs/Mechanical_Design_App/README.md';s=p.read_text(encoding='utf-8')
a=s.index('> Current status');b=s.index('\n\n',a)
s=s[:a]+'> Current status — 2026-10-18: Phase 7 CLOSED WITH LIMITATIONS at Brian\'s direction; all seven milestones are complete within their documented scopes. Digital acceptance passed; Brian confirms positive qualitative fit of the earlier supplied printed tray/faceplate. Strength, retention, installation and unestablished access/whole-solid claims remain UNKNOWN. Printer/slicer integration is outside scope. See `../Phase7_Closeout/Closeout_Report.md`. Older phase/count descriptions below are historical.'+s[b:]
p.write_text(s,encoding='utf-8')
review=(out/'Closeout_Review.md').read_text(encoding='utf-8')
final=review.replace('# Phase 7 closeout review — ready with limitations','# Phase 7 — CLOSED WITH LIMITATIONS')
final=final.replace('2026-10-18. Status: READY FOR CLOSEOUT REVIEW WITH LIMITATIONS. This preparation does not mark Phase 7 closed or authorize a release. Brian has reviewed the digital result and now confirms positive real-world fit for the earlier supplied specimen.', '2026-10-18. Status: CLOSED WITH LIMITATIONS. Brian directed: “lets close out, and prepare for the new chat.” This closes the agreed milestone; it does not authorize a release, new physical work or blanket physical certification. Brian has reviewed the digital result and confirms positive real-world fit for the earlier supplied specimen.')
final=final.replace('8. Disposition: acceptance evidence consolidated and ready for Brian\'s closeout review.', '8. Disposition: acceptance evidence consolidated; Brian authorized closeout. Phase7 is CLOSED WITH LIMITATIONS.')
final=final.replace('## Proposed work after closeout','## Next development work')
final+='''\n## Final organization and preservation\n\nProject home: C:/Users/brian/Documents/Codex/2026-10-17/Assembly Workshop. App: outputs/Mechanical_Design_App/. The project primary folder and current chat membership were verified earlier. Existing conversations and original test files remain intact. A final local safety copy is recorded in Preservation_Report.json once completed; it preserves untracked app/source/assets/work/evidence. This is a local backup, not a release archive or off-machine backup. The small local handoff commit records guidance and closeout files only; Git alone still does not contain the complete app.\n\nDocumented default data paths checked read-only: current app, Beta0.8 and Beta0.7 data/library.sqlite3 were absent. This does not prove no user database exists elsewhere; normal-use data selection remains the first next-chat task. No active user database was migrated or initialized. The acceptance databases in work/ are disposable.\n\nFinal changes after digital acceptance are roadmap/status text only in index.html/README and handoff guidance. No core geometry/rule/mesh implementation changed. Targeted JavaScript handler/syntax checks are recorded in Final_Checks.json; no new render or physical test is required for the status change. Earlier acceptance artifacts/hashes remain historical; final hashes identify the status-updated files.\n'''
(out/'Closeout_Report.md').write_text(final,encoding='utf-8')
p=root/'HANDOFF.md';s=p.read_text(encoding='utf-8')
s=s.replace('Phase7 digital points2–6 accepted WITH LIMITATIONS; Brian now confirms positive qualitative physical fit for the earlier supplied printed tray/faceplate. Point8 closeout review prepared, not yet marked closed. See outputs/Phase7_Closeout/Closeout_Review.md.', 'Phase7 CLOSED WITH LIMITATIONS at Brian\'s explicit direction. Digital points2–6 accepted; Brian confirms positive qualitative physical fit for the earlier supplied printed tray/faceplate. All seven milestones complete within their stated scopes. See outputs/Phase7_Closeout/Closeout_Report.md.')
s=s.replace('1. Present closeout review to Brian. No new tests/rendering are needed solely for documentation changes.','1. Phase7 is closed; do not reopen it or start a new numbered phase by default. Read outputs/Phase7_Closeout/Next_Chat_Prompt.md. Establish the intended normal-use app/data directory next; current/Beta0.8/Beta0.7 default database paths were absent on read-only inspection.')
s=s.replace('2. After closeout direction, establish intended normal-use app/data path without overwriting existing data or mistaking disposable acceptance data for the user\'s library.', '2. Preserve existing user data and pins; do not mistake disposable acceptance data for the user\'s library. Do not create a new default database as a substitute for locating existing work.')
s+='''\n## Final preservation and next-chat preparation\n\nSee outputs/Phase7_Closeout/Preservation_Report.json for the complete local safety copy and manifest. App/assets/work remain largely untracked: the handoff commit is not an app backup. Prepared next-chat prompt: outputs/Phase7_Closeout/Next_Chat_Prompt.md. No release packaging, printing, desktop control, publishing, deployment or push occurred during closeout. Static app roadmap/README now reflect Phase7 closed with limitations; final targeted checks recorded beside the closeout.\n''';p.write_text(s,encoding='utf-8')
p=root/'AGENTS.md';s=p.read_text(encoding='utf-8').replace('outputs/Phase7_Closeout/Closeout_Review.md','outputs/Phase7_Closeout/Closeout_Report.md')
s=s.replace('Phase 7 digital acceptance is complete with limitations; Brian confirms qualitative fit of the earlier supplied specimen, and closeout review is ready.', 'Phase 7 is CLOSED WITH LIMITATIONS at Brian\'s explicit direction. Digital acceptance passed and Brian confirms qualitative fit of the earlier supplied specimen.')
s=s.replace('Phase7 closeout review is prepared;','Phase7 is closed with limitations;')
p.write_text(s,encoding='utf-8')
p=root/'PROJECT.md';s=p.read_text(encoding='utf-8')
s='''> FINAL CURRENT STATUS — 2026-10-18: Phase7 CLOSED WITH LIMITATIONS at Brian's direction. All seven milestones complete within documented scope. See outputs/Phase7_Closeout/Closeout_Report.md and HANDOFF.md; older milestone passages below are historical. Continue with normal-use app/data identification, not more niche insert research or printer integration.\n\n'''+s
p.write_text(s,encoding='utf-8')
prompt='''Continue Assembly Workshop in its existing local project:
C:/Users/brian/Documents/Codex/2026-10-17/Assembly Workshop

Read AGENTS.md, HANDOFF.md and PROJECT.md first, then outputs/Phase7_Closeout/Closeout_Report.md. Inspect only relevant referenced files; do not scan the whole repository.

Phase7 is CLOSED WITH LIMITATIONS. Digital acceptance:46 Python tests PASS, one mounting-specific test intentionally deferred, Node behavioral/syntax checks and9 localhost endpoints PASS. Brian confirms positive qualitative fit of the earlier supplied printed tray/faceplate; three photos and recovered delivery provenance are saved. Do not misattribute the physical result to the later Phase7 digital build or turn it into strength/installation certification.

Next: establish the intended normal-use app/data directory without overwriting existing data or initializing an empty replacement library. The current app and Beta0.8/Beta0.7 documented default database paths were absent; acceptance databases in work/ are disposable. Use relevant prior records and narrowly scoped read-only inspection. Then address actual-use workflow issues within the existing STL-delivery scope. Do not start another numbered phase, render or package by default.

Preserve outputs/,work/,user data,immutable revisions/cache,project pins and mechanical baseline. Most assets remain untracked: the handoff commit is not a full app backup. The complete local preservation copy/manifest is recorded in outputs/Phase7_Closeout/Preservation_Report.json. No git clean/reset or deletion. New mesh cache identity is pi4-mesh-v2-triangulation1; old entries are preserved; downloads without integrity manifests require explicit regeneration into a separate new entry.

STLs are the deliverable. Printer/slicer integration is outside scope. Further niche McMaster insert research is parked. Four-corner mounting remains TABLED until I explicitly raise it. Keep unsupported dimensions, strength, retention, installation and unestablished access claims UNKNOWN. Ask before every fresh desktop-control session. No subagents, printing, purchases, uploads, release packaging, publishing, deployment or pushes unless separately authorized. Preserve this conversation and all prior evidence.
'''
(out/'Next_Chat_Prompt.md').write_text(prompt,encoding='utf-8')
print('Phase7 formally closed with limitations; app status, durable guidance and next-chat prompt updated. No implementation changes.')
