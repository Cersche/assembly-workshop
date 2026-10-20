from pathlib import Path
root=Path.cwd(); app=root/'outputs/Mechanical_Design_App';out=root/'outputs/Phase7_Digital_Acceptance'
readme=app/'README.md'
s=readme.read_text(encoding='utf-8')
notice='''> Current status — 2026-10-18: Phase 6 is closed with limitations. Phase 7 digital STL/export acceptance is in progress; printer/slicer integration is outside scope. See `../../outputs/Phase7_Digital_Acceptance/Report.md` for the resulting acceptance record. Older phase/count descriptions below are historical. Physical fit and strength remain UNKNOWN.

## Phase 7 artifact integrity

New renders use the separate `pi4-mesh-v2` identity namespace and include `integrity.json` with SHA-256 values for source, STLs, viewer geometry and revision report. The report binds the exact source/configuration; cache reuse and rendered downloads revalidate the files and viewer/STL correspondence. Mesh checks cover finite coordinates, nondegenerate unique triangles, two incident triangles per edge, consistent winding and positive signed volume. These bounded checks do not establish absence of self-intersections, vertex manifoldness, complete clearance, strength or physical fit.

Older immutable cache entries are preserved without modification. Entries lacking the new manifest cannot be downloaded through the new integrity-checked endpoint; explicitly generate the current configuration to create a separate v2 entry. Corrupted v2 entries are blocked rather than silently repaired or overwritten. Preserve a damaged entry and use a new data directory to regenerate the same configuration if needed.

STL coordinates follow the project's millimeter convention and remain in assembly orientation. STL does not encode a unit; retain millimeter scale when importing into other software. No printer profile or print-bed orientation is prescribed. The generated revision download is an app feature; acceptance checks inspect it in memory and do not constitute release packaging.

'''
s=s.replace('# Assembly Workshop — beta 0.8\n\n','# Assembly Workshop — beta 0.8\n\n'+notice,1)
readme.write_text(s,encoding='utf-8')
p=app/'hardware-records.md'
old=p.read_text(encoding='utf-8');(out/'before_hardware-records.md').write_text(old,encoding='utf-8')
p.write_text(old+'''\n## Phase 7 audit note — 2026-10-18\n\nCurrent software scope is STL delivery, without printer/slicer integration. Phase 6 is closed with limitations; historical pending-acceptance statements above are superseded by phase6-closeout.md. McMaster's standard-profile row for 94459A140 labels 5.7 mm as installed length and 4 mm as For Max. Hole Dia. The stored length must not be promoted into usable threaded depth, a certified OD, wall minimum or a printed-pilot recommendation. Original immutable records remain unchanged. See ../../outputs/Phase7_Digital_Acceptance/Hardware_Source_Review.md for source applicability and retained UNKNOWNs.\n''',encoding='utf-8')
