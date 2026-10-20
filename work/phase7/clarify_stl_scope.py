from pathlib import Path
root=Path.cwd()
a=root/'AGENTS.md'
s=a.read_text(encoding='utf-8')
s+='''
## STL delivery scope — Brian, 2026-10-18

The app delivers STL files. Do not require or build integration for the end user's printer, slicer, filament profiles or machine setup. Printer/material identification is not an app-readiness or Phase 7 software-completion gate. Prioritize supported geometry, exact source/mesh matching, traceable hardware, export integrity and explicit validation limits. Any later optional physical validation applies only to its documented specimens/material/process; it does not certify arbitrary printers or materials. Do not ask for printer details to continue software development. Unsupported printed fit and strength remain UNKNOWN. Physical fitting remains late Phase 7 and requires Brian's direction; printing is not authorized.
'''
a.write_text(s,encoding='utf-8')
clarification='''
## Scope clarification — Brian, 2026-10-18

STL output is sufficient for the end user's printing workflow. Printer/slicer/material-profile integration is outside the current app scope. Lack of a selected printer/material does not block Phase 7 software work. Earlier printer/process planning gates apply only if a separately authorized, bounded physical validation is later undertaken; they are not requirements to configure the end user's machine.

Continue Phase 7 with: (1) traceable hardware and honest dimensional UNKNOWNs, (2) supported geometry and source-to-STL identity, (3) existing mesh integrity and export safeguards, (4) artifact/revision traceability and reproducible digital acceptance, and (5) clear remaining physical-validation limits. Hardware actually owned and installation tools matter only when making claims about a specific installation or planning later physical work; they do not block auditing the recorded software configuration. Existing agreed geometry remains unchanged. Do not revisit the tabled mounting matter. No printing, physical tests or release packaging are authorized.
'''
for name in ['PROJECT.md','docs/phase7-readiness/Readiness_Plan.md','outputs/Phase7_Start/Status.md']:
    p=root/name
    s=p.read_text(encoding='utf-8')
    if name.endswith('Status.md'):
        s=s.replace('Physical readiness is NOT established; no physical work has begun.','Physical readiness is NOT established; no physical work has begun. Printer configuration is outside app scope and is not a software-readiness blocker.')
        s=s.replace('| Material/process | UNKNOWN | Printer/material/process identification |','| Optional physical specimen material/process | DEFERRED | Only relevant to separately authorized physical validation; not an app gate |')
    p.write_text(s+clarification,encoding='utf-8')
p=root/'outputs/Phase7_Start/Configuration_Snapshot.json'
# Preserve the entry snapshot unchanged; scope corrections live in a new record.
import json
record=dict(date='2026-10-18',source='Brian explicit clarification',deliverable='STL files',printer_integration='OUT_OF_SCOPE',printer_selection_blocks_software=False,material_profile_integration='OUT_OF_SCOPE',entry_snapshot='Configuration_Snapshot.json retained as historical entry evidence',physical_fit='UNKNOWN',strength='UNKNOWN',physical_tests='NOT_STARTED',next_work='Digital STL/source/revision integrity and supported-geometry/export acceptance')
(root/'outputs/Phase7_Start/Scope_Clarification.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print('Updated persistent guidance, project guide, Phase 7 plan/status; original entry snapshot preserved.')
