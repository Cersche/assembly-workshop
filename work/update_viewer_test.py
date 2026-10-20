from pathlib import Path
p=Path('work/test_viewer.cjs');s=p.read_text().replace('let fills=0;','let fills=0;const listeners={};')
s=s.replace('const ctx={','const ctx={setLineDash(){},stroke(){},')
s=s.replace("'show-faceplate']","'show-faceplate','show-hardware','hardwareStatus']")
s=s.replace('window:{devicePixelRatio:1}','window:{devicePixelRatio:1,addEventListener:(name,fn)=>listeners[name]=fn}')
s=s.replace("assert(fills>=11560);", "assert(fills>=11560);listeners['assembly-hardware']({detail:{hardware_envelopes:[{kind:'screw',x:40,z:21,y0:1.3,y1:11.3,diameter:3}],hardware_guides:[{x:40,z:21,y0:3.7,y1:8}]}});assert(elements.assemblyStatus.textContent.includes('11,656'));assert(elements.hardwareStatus.textContent.includes('1 hardware envelopes'));elements['show-hardware'].checked=false;elements['show-hardware'].onchange();")
s=s.replace('initial draw, finite coordinates, joint focus, visibility, top and reset.','hardware event rendering, finite coordinates, joint focus, visibility, top and reset.')
Path('work/test_viewer_v06.cjs').write_text(s)
