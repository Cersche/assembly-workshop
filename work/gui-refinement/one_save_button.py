from pathlib import Path
p=Path('outputs/Mechanical_Design_App/workspace.js');s=p.read_text(encoding='utf-8')
s=s.replace("button(persistedAssemblyIds.has(placement.assembly.id)?'Open assembly':'Save & open assembly',()=>openAssembly(placement,true),'primary')","button('Open assembly',()=>openAssembly(placement),'primary')")
s=s.replace("    appendReleaseUndo(host,rack);\n  }\n  function editAllocation", "    if(placement&&!persistedAssemblyIds.has(placement.assembly.id)){host.querySelector('button.primary').disabled=true;host.append(paragraph('Use Save to keep this allocation before opening its hardware editor.'));}\n    appendReleaseUndo(host,rack);\n  }\n  function editAllocation")
s=s.replace('async function openAssembly(placement,saveFirst=false){','async function openAssembly(placement){')
a=s.index('    if(!persistedAssemblyIds.has(placement.assembly.id)){');b=s.index('    openingAssembly=true;',a)
s=s[:a]+"    if(!persistedAssemblyIds.has(placement.assembly.id)){notify('Use Save to keep this allocation before opening its hardware editor.',true);return;}\n"+s[b:]
p.write_text(s,encoding='utf-8')
