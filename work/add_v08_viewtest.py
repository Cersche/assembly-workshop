from pathlib import Path
p=Path('work/test_viewer_v061.cjs');s=p.read_text();s=s.replace("console.log('Viewer logic passed:","const proposed=JSON.parse(fs.readFileSync(root+'assembly.json','utf8'));proposed.parts=proposed.parts.filter(p=>p.id==='tray');listeners['assembly-model']({detail:proposed});assert(elements.assemblyStatus.textContent.includes('10,340'));listeners['assembly-model']({detail:null});assert(elements.assemblyStatus.textContent.includes('11,560'));console.log('Viewer logic passed: model switching,")
Path('work/test_viewer_v08.cjs').write_text(s)
