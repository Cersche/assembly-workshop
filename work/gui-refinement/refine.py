from pathlib import Path
p=Path('outputs/Mechanical_Design_App/workspace.js');s=p.read_text(encoding='utf-8')
def swap(a,b):
    global s
    if a not in s: raise RuntimeError('Missing marker: '+a[:90])
    s=s.replace(a,b)
swap('>Save layout</button>','>Save</button>')
swap('<button id="configureRack" class="subtle">Rack settings</button>', '<div class="studio-view-actions"><button id="configureRack" class="subtle">Rack settings</button><button id="toggleInspector" class="subtle" aria-expanded="true" aria-controls="studioInspector">Hide inspector</button></div>')
swap('<aside class="studio-left"><div class="panel-heading">','<aside class="studio-left"><details id="racksSection" class="library-section" open><summary>Racks & slots</summary><div class="panel-heading">')
start=s.index('<div class="sidebar-tabs"');end=s.index('<div id="explorerPane">',start)
s=s[:start]+s[end:]
swap('<div id="equipmentPane" hidden>','</details><details id="equipmentSection" class="library-section"><summary>Equipment</summary><div id="equipmentPane">')
swap('</div><details class="hardware-drawer"><summary>Hardware library <span>↗</span></summary>', '</div></details><details id="hardwareSection" class="library-section hardware-drawer"><summary>Hardware</summary>')
start=s.index('<aside class="studio-right">');end=s.index('</aside></div>',start)+len('</aside>')
s=s[:start]+'''<aside class="studio-right" id="studioInspector"><div class="panel-heading">INSPECTOR <span id="propertiesContext">Rack layout</span></div><div class="inspector-tabs" role="tablist" aria-label="Inspector"><button id="tabSetup" role="tab" aria-selected="true" aria-controls="panelSetup">Setup</button><button id="tabHardware" role="tab" aria-selected="false" aria-controls="panelHardware">Hardware</button><button id="tabAppearance" role="tab" aria-selected="false" aria-controls="panelAppearance">Appearance</button></div><section id="panelSetup" role="tabpanel" aria-labelledby="tabSetup"><div id="slotProperties"></div><div id="mountWizard" hidden></div><details class="reference-drawer"><summary>Project status & limitations</summary><div id="roadmapPane"></div></details></section><section id="panelHardware" role="tabpanel" aria-labelledby="tabHardware" hidden><p id="hardwareEmpty" class="muted">Select an allocated slot and open its assembly to edit hardware.</p><div id="jointProperties"><p class="notice">Independent hardware project. Installed fit and strength remain UNKNOWN.</p><div id="jointControls"></div></div></section><section id="panelAppearance" role="tabpanel" aria-labelledby="tabAppearance" hidden><div id="appearanceProperties"></div></section></aside>'''+s[end:]
swap('  let yaw=-.48',"  let inspectorTab='Setup',inspectorCollapsed=false,artworkPending=0;\n  let yaw=-.48")
a=s.index('  function markChanged()');b=s.index('  function button(',a)
s=s[:a]+'''  function updateSaveStatus(){byId('layoutSaveStatus').textContent=(layoutDirty||dirty)?'Unsaved changes':active()?'Saved locally':'No rack selected';byId('saveLayout').disabled=!capable||savingLayout||!(layoutDirty||dirty);}
  function markChanged(){layoutDirty=true;updateSaveStatus();}
  window.addEventListener('workshop-dirty',updateSaveStatus);
'''+s[b:]
swap("function selectSlot(slot){if(!leaveAssembly())return;", "function selectSlot(slot){if(selectedSlot===slot)return;if(!leaveAssembly())return;")
swap("selectedSlot=slot;byId('mountWizard').hidden=true;", "selectedSlot=slot;byId('mountWizard').hidden=true;inspectorTab='Setup';")
swap("async function openAssembly(placement){", "async function openAssembly(placement,saveFirst=false){")
swap("      await byId('saveLayout').onclick();\n      if(!persistedAssemblyIds.has(placement.assembly.id))return;", "      if(!saveFirst){notify('Save this new allocation before opening its hardware editor.',true);return;}\n      try{await saveWorkshop();}catch(e){notify(e.message,true);return;}\n      if(!persistedAssemblyIds.has(placement.assembly.id))return;")
swap("applyAssemblyAppearance(placement);}", "applyAssemblyAppearance(placement);showInspector('Hardware');}")
swap("action('Edit slot allocation',()=>editAllocation(p));action('Colors & faceplate image',()=>{byId('appearanceProperties').scrollIntoView({block:'nearest'});byId('assemblyAppearance').open=true;});", "action('Edit slot allocation',()=>editAllocation(p));action('Colors & faceplate image',()=>showInspector('Appearance'));")
swap("action('Rack colors',()=>{byId('rackAppearance').open=true;", "action('Rack colors',()=>{showInspector('Appearance');byId('rackAppearance').open=true;")
swap("function editAllocation(placement){", "function editAllocation(placement){\n    showInspector('Setup');")
swap("const rack=active();if(!rack||!selectedSlot)", "showInspector('Setup');const rack=active();if(!rack||!selectedSlot)")
swap("renderAppearance();byId('jointProperties').open=stage==='assemble';", "renderAppearance();byId('jointProperties').open=stage==='assemble';syncInspector();")
swap("'Save layout & open assembly',()=>openAssembly(placement)", "'Save & open assembly',()=>openAssembly(placement,true)")
swap("button('Edit slot allocation',()=>editAllocation(placement),'secondary'),button('Release slots',()=>releasePlacement(placement),'secondary')", "button('Slot actions ⋯',e=>showSlotMenu(selectedSlot,e.currentTarget),'secondary')")
swap("appendReleaseUndo(host,rack);host.append(paragraph('Dimensions and slot assignments describe a layout, not a verified physical rack.'));", "appendReleaseUndo(host,rack);")
swap("byId('saveLayout').disabled=savingLayout||!layoutDirty;", "updateSaveStatus();")
start=s.index("  byId('saveLayout').onclick=async()=>");end=s.index("\n  byId('rackChoice')",start)
s=s[:start]+Path('work/gui-refinement/save_controller.txt').read_text(encoding='utf-8')+s[end:]
start=s.index('  function libraryTab(');end=s.index('  function dashboard()',start)
s=s[:start]+'''  function libraryTab(which){byId(which==='equipment'?'equipmentSection':'racksSection').open=true;}
  byId('pi4Card').onclick=startWizard;
'''+s[end:]
swap("if(layoutDirty)byId('saveLayout').click();", "if(layoutDirty||dirty)byId('saveLayout').click();")
swap("caps.version!==2", "caps.version!==2||caps.studio_save_version!==1")
swap("const file=input.files[0];if(!file)return;input.disabled=true;", "const file=input.files[0];if(!file)return;input.disabled=true;artworkPending++;")
swap("finally{input.disabled=false;}", "finally{input.disabled=false;artworkPending--;}")
start=s.index('  function colorField(');end=s.index('  function renderAppearance()',start)
s=s[:start]+'''  const colorPresets=[['Graphite','#28313c'],['Silver','#9daab8'],['Ivory','#e6e4db'],['Blue','#325a8e'],['Green','#4d8e6e'],['Copper','#ba7245'],['Gold','#d09b55'],['Red','#b95d5d']];
  function colorField(host,label,value,onChange){
    const group=document.createElement('fieldset');group.className='color-group';const legend=document.createElement('legend');legend.textContent=label;group.append(legend);
    const row=document.createElement('div');row.className='color-field';const hex=document.createElement('span');hex.textContent=value;
    const input=document.createElement('input');input.type='color';input.value=value;input.setAttribute('aria-label',label+' custom color');
    const set=v=>{input.value=v;hex.textContent=v;onChange(v);};input.oninput=()=>set(input.value);row.append(hex,input);group.append(row);
    const swatches=document.createElement('div');swatches.className='color-swatches';
    for(const [name,color] of colorPresets){const b=button('',()=>set(color));b.style.background=color;b.setAttribute('aria-label',label+': '+name);b.title=name;swatches.append(b);}group.append(swatches);host.append(group);
  }
'''+s[end:]
swap("const artDetails=document.createElement('details');artDetails.id='assemblyAppearance';", "const artDetails=document.createElement('details');artDetails.open=true;artDetails.id='assemblyAppearance';")
swap("const art=p.assembly.appearance.artwork;", "const art=p.assembly.appearance.artwork;")
swap("if(art){artDetails.append(paragraph(art.name+' · preview only'));", "if(art){artDetails.append(paragraph(art.name+' · preview only'),button('Fit & center image',()=>{Object.assign(art,{x:.5,y:.5,scale:1});markChanged();applyAssemblyAppearance(p);renderAppearance();},'secondary'),button('Center image',()=>{Object.assign(art,{x:.5,y:.5});markChanged();applyAssemblyAppearance(p);renderAppearance();},'secondary'));")
# Existing copy is updated for the single explicit Save action.
s=s.replace('Save layout','Save').replace('save layout','save')
marker=s.index('  function newAssembly()')
s=s[:marker]+Path('work/gui-refinement/inspector_controller.txt').read_text(encoding='utf-8')+'\n'+s[marker:]
p.write_text(s,encoding='utf-8')
p=Path('outputs/Mechanical_Design_App/index.html');s=p.read_text(encoding='utf-8')
s=s.replace("['rack-workspace','workspace-capabilities','artwork']", "['rack-workspace','workspace-capabilities','artwork','studio-save']")
s=s.replace("async function save(){const draft=", "async function save(){if(window.saveWorkshop)return window.saveWorkshop();const draft=")
s=s.replace("$('dirty').textContent='Unsaved changes. Exports save your selections first.';", "$('dirty').textContent='Unsaved hardware changes. Use Save to keep them.';window.dispatchEvent(new Event('workshop-dirty'));")
s=s.replace("{await save();const r=await api('check'", "{if(window.assertWorkshopSaved)window.assertWorkshopSaved();else await save();const r=await api('check'")
s=s.replace("async function download(path,name){await save();", "async function download(path,name){if(window.assertWorkshopSaved)window.assertWorkshopSaved();else await save();")
s=s.replace("$('designExport').onclick=()=>safe(async()=>{const response=", "$('designExport').onclick=()=>safe(async()=>{if(window.assertWorkshopSaved)window.assertWorkshopSaved();const response=")
s=s.replace("$('buildRevision').onclick=()=>safe(async()=>{if(window.workshopContext", "$('buildRevision').onclick=()=>safe(async()=>{if(window.assertWorkshopSaved)window.assertWorkshopSaved();if(window.workshopContext")
s=s.replace('/workspace.css?v=2','/workspace.css?v=3')
p.write_text(s,encoding='utf-8')
