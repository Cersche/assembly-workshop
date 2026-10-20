// Rack-first workspace. Slot allocations are planning records, not certified fit.
(function(){
  'use strict';
  const byId=id=>document.getElementById(id);
  const oldMain=document.querySelector('main.shell');
  const inspector=byId('screw').closest('.card');
  const hardwareCard=byId('parts').closest('.card');
  const packCard=byId('catalogPack').closest('.card');
  const importCard=byId('json').closest('.card');
  const assemblyCard=byId('assemblyCanvas').closest('.card');
  const reviewCard=byId('checks').closest('.card');
  const axialCard=byId('jointSvg').closest('.card');
  const roadmap=document.querySelector('[aria-label="Beta roadmap"]');
  const message=byId('message');
  const shell=document.createElement('div');shell.id='studio';
  shell.innerHTML=`
    <header class="studio-header"><button id="homeStudio" class="brand" aria-label="Project dashboard"><span class="brand-mark">AW</span><span>Assembly Workshop<small>LAB RAX STUDIO</small></span></button><span class="header-divider"></span><span id="projectTitle">Your rack workspace</span><span id="layoutSaveStatus" role="status">No rack selected</span><button id="saveLayout" class="primary">Save</button><button id="shortcutHelp" class="icon-button" aria-label="Keyboard shortcuts">?</button></header>
    <nav class="studio-nav" aria-label="Workspace"><span class="local-label"><i></i> LOCAL WORKSPACE</span><div class="stage-tabs"><button data-stage="rack" aria-pressed="true">01 <span>Rack</span></button><button data-stage="assemble" aria-pressed="false">02 <span>Assemble</span></button><button data-stage="review" aria-pressed="false">03 <span>Review</span></button><button data-stage="prepare" aria-pressed="false">04 <span>Prepare</span></button></div><div class="studio-view-actions"><button id="configureRack" class="subtle">Rack settings</button><button id="toggleInspector" class="subtle" aria-expanded="true" aria-controls="studioInspector">Hide inspector</button></div></nav>
    <div class="studio-columns"><aside class="studio-left"><details id="racksSection" class="library-section" open><summary>Racks & slots</summary><div class="panel-heading"><span>PROJECT</span><button id="newRack" class="subtle" aria-label="New rack">＋</button></div><label class="sr-only" for="rackChoice">Rack layout</label><select id="rackChoice"></select><div id="explorerPane"><div id="rackTree"></div><p class="sidebar-hint">Select a slot to place equipment.<br>Slot 1 starts at the top.</p></div></details><details id="equipmentSection" class="library-section"><summary>Equipment</summary><div id="equipmentPane"><p class="section-eyebrow">SUPPORTED EQUIPMENT</p><button id="pi4Card" class="equipment-card"><svg viewBox="0 0 220 125" aria-hidden="true"><path d="M24 53 145 22 199 59 77 94Z" fill="#46977c"/><path d="M24 53v10l53 40V94m0 0 122-35v10L77 103" fill="#246c58"/><path d="m72 48 46-12 30 20-47 13Z" fill="#233637"/><path d="m150 33 17-4 26 18-16 5Zm-22 9 17-4 26 18-16 5Z" fill="#aab8c0"/><path d="m31 48 20-5 10 7-20 5Z" fill="#d0b662"/></svg><strong>Raspberry Pi 4</strong><span>Tray + faceplate · supported baseline</span><small>Choose a slot, then create an assembly →</small></button><div class="empty-library">More equipment<br><small>Additional geometry adapters are not yet supported.</small></div></div></details><details id="hardwareSection" class="library-section hardware-drawer"><summary>Hardware</summary><div id="hardwarePane"></div></details></aside>
    <main class="studio-center"><div class="viewport-heading"><div><p class="section-eyebrow" id="contextEyebrow">RACK DESIGN</p><h1 id="contextTitle">Build your workspace</h1></div><span id="contextBadge" class="studio-badge">Layout planning</span></div><section id="rackView"><div class="rack-toolbar"><span id="rackDimensions">Dimensions not configured</span><button id="frontRackView" class="subtle">Front</button><button id="toggleRackPanels" class="subtle" aria-pressed="false">Side panels</button><button id="resetRackView" class="subtle">Perspective</button><button id="renderQuality" class="subtle" aria-pressed="true" title="Toggle contact shading and cast shadows">Studio quality</button></div><canvas id="rackCanvas" tabindex="0" aria-label="Lab Rax source meshes. Drag to orbit, scroll to zoom; select a slot in Explorer."></canvas><div class="viewport-caption"><span><i class="axis-x">X</i> <i class="axis-y">Y</i> <i class="axis-z">Z</i> Drag to orbit · scroll to zoom · select a slot</span><span id="rackScale">Schematic · not manufacturing geometry</span></div></section><div id="assemblyView" hidden></div><div class="context-strip"><span id="selectionSummary">No slot selected</span><button id="backToRack" class="subtle">View rack</button></div><section id="reviewView" hidden><div class="section-heading"><h2>Design review</h2><span class="studio-badge">Evidence and limits</span></div><div id="rackReview"></div><div id="jointReview"></div></section><section id="prepareView" hidden><div class="section-heading"><h2>Prepare & export</h2><span class="studio-badge">STL delivery</span></div><p class="notice">The current geometry adapter exports the Pi4 assembly in its documented assembly coordinates. Rack frames, slot positions and other equipment are layout context and are not included in these STLs. Physical rack fit and strength remain UNKNOWN.</p><div id="exportTools"></div></section><div id="workspaceMessage" role="status" aria-live="polite"></div></main>
    <aside class="studio-right" id="studioInspector"><div class="panel-heading">INSPECTOR <span id="propertiesContext">Rack layout</span></div><div class="inspector-tabs" role="tablist" aria-label="Inspector"><button id="tabSetup" role="tab" aria-selected="true" aria-controls="panelSetup">Setup</button><button id="tabHardware" role="tab" aria-selected="false" aria-controls="panelHardware">Hardware</button><button id="tabAppearance" role="tab" aria-selected="false" aria-controls="panelAppearance">Appearance</button></div><section id="panelSetup" role="tabpanel" aria-labelledby="tabSetup"><div id="slotProperties"></div><div id="mountWizard" hidden></div><details class="reference-drawer"><summary>Project status & limitations</summary><div id="roadmapPane"></div></details></section><section id="panelHardware" role="tabpanel" aria-labelledby="tabHardware" hidden><p id="hardwareEmpty" class="muted">Select an allocated slot and open its assembly to edit hardware.</p><div id="jointProperties"><p class="notice">Independent hardware project. Installed fit and strength remain UNKNOWN.</p><div id="jointControls"></div></div></section><section id="panelAppearance" role="tabpanel" aria-labelledby="tabAppearance" hidden><div id="appearanceProperties"></div></section></aside></div>
    <footer class="studio-footer"><span id="workspaceFooter">Local rack layout · no cloud connection required</span><span>Millimeters · physical fit UNKNOWN</span></footer>
    <dialog id="rackDialog"><form id="rackForm"><div class="dialog-heading"><span class="section-eyebrow">RACK SETUP</span><button type="button" id="closeRackDialog" class="subtle" aria-label="Close rack setup">✕</button></div><h2 id="rackDialogTitle">Create your rack</h2><p class="muted">Define the slot layout, then select a slot to create an assembly. Dimensions are optional until you have a verified rack reference.</p><label for="rackName">Project / rack name</label><input id="rackName" maxlength="100" required placeholder="My Lab Rax"><div class="fields"><div><label for="rackSlots">Number of slots</label><input id="rackSlots" type="number" min="1" max="48" step="1" required></div><div><label for="rackPitch">Slot pitch (mm)</label><input id="rackPitch" type="number" min="0.001" max="10000" step="any" placeholder="Unknown"></div><div><label for="rackWidth">Clear internal width (mm)</label><input id="rackWidth" type="number" min="0.001" max="10000" step="any" placeholder="Unknown"></div><div><label for="rackDepth">Usable depth (mm)</label><input id="rackDepth" type="number" min="0.001" max="10000" step="any" placeholder="Unknown"></div></div><p class="notice">Entered dimensions are user-supplied layout references. The preview uses the supplied rack parts at recovered visual placements. Entered dimensions do not resize those meshes. Assembled clearances, fit and strength remain UNKNOWN.</p><p id="rackFormError" class="fail" role="alert"></p><div class="dialog-actions"><button type="button" id="cancelRackDialog" class="secondary">Cancel</button><button class="primary" type="submit">Apply rack layout</button></div></form></dialog>
    <dialog id="dashboardDialog"><div class="dialog-heading"><span class="section-eyebrow">YOUR WORKSHOP</span><button id="closeDashboard" class="subtle" aria-label="Close dashboard">✕</button></div><h2>Start with the rack.<br>Make room for your ideas.</h2><p class="muted">Plan the space, place your equipment, then work on the assembly.</p><div class="dashboard-grid"><div><h3>Start a project</h3><button id="dashboardNew" class="template-card"><span class="template-icon">▥</span><strong>Custom Lab Rax layout</strong><small>Choose slots and reference dimensions</small></button></div><div><h3>Recent local layouts</h3><div id="recentRacks"></div></div></div><p class="notice">Your existing Pi4 library, saved hardware selections and immutable meshes remain available. A rack layout is saved separately from that project.</p></dialog>
    <dialog id="shortcutsDialog"><div class="dialog-heading"><h2>Keyboard shortcuts</h2><button id="closeShortcuts" class="subtle" aria-label="Close keyboard shortcuts">✕</button></div><label for="shortcutSearch">Find a shortcut</label><input id="shortcutSearch" placeholder="Search commands"><div id="shortcutList"></div></dialog>`;
  document.body.prepend(shell);
  byId('hardwarePane').append(hardwareCard,packCard,importCard);
  byId('assemblyView').append(assemblyCard);
  byId('jointReview').append(axialCard,reviewCard);
  byId('roadmapPane').append(roadmap);
  // Keep existing handler elements and IDs; move export groups rather than reimplementing them.
  const firstHeading=Array.from(inspector.querySelectorAll('h3')).find(e=>e.textContent==='Generate proposed meshes');
  if(firstHeading){let node=firstHeading;while(node){const next=node.nextSibling;byId('exportTools').append(node);node=next;}}
  byId('jointControls').append(inspector);
  byId('workspaceMessage').append(message);
  oldMain.remove();for(const header of Array.from(document.body.children))if(header.tagName==='HEADER')header.remove();

  let documentState={version:2,generation:null,racks:[]},activeId=null,selectedSlot=null,stage='rack',layoutDirty=false,editingId=null,savingLayout=false,lastReleased=null;
  let capable=false,legacyTemplate=null,persistedAssemblyIds=new Set(),openingAssembly=false,artworkRequests=new Map();
  window.workshopContext=null;
  let inspectorTab='Setup',inspectorCollapsed=false,artworkPending=0;
  let yaw=-.48,pitch=.24,zoom=1,drag=null,clickRegions=[],pending=false;
  let sourceMeshes=null,sourceError=null,sceneRenderer=null,sceneCache=null,sceneCacheKey='';
  const rackCanvas=byId('rackCanvas'),rackContext=rackCanvas.getContext('2d');
  const active=()=>documentState.racks.find(r=>r.id===activeId);
  const assigned=(rack,slot)=>rack?.placements.find(p=>slot>=p.slot&&slot<p.slot+p.span);
  const uid=()=>crypto.randomUUID();
  function notify(value,error=false){byId('workspaceMessage').classList.toggle('workspace-error',error);byId('message').textContent=value;}
  function updateSaveStatus(){byId('layoutSaveStatus').textContent=(layoutDirty||dirty)?'Unsaved changes':active()?'Saved locally':'No rack selected';byId('saveLayout').disabled=!capable||savingLayout||!(layoutDirty||dirty);}
  function markChanged(){layoutDirty=true;updateSaveStatus();drawSoon();}
  window.addEventListener('workshop-dirty',updateSaveStatus);
  function button(label,fn,cls=''){const e=document.createElement('button');e.type='button';e.textContent=label;e.className=cls;e.onclick=fn;return e;}
  function paragraph(value,cls='muted'){const e=document.createElement('p');e.textContent=value;e.className=cls;return e;}
  function setStage(next){if(next==='assemble'&&!window.workshopContext){const p=assigned(active(),selectedSlot);if(p){openAssembly(p);return;}notify('Select an allocated slot and open its saved assembly first.');next='rack';}stage=next;byId('jointProperties').open=stage==='assemble';shell.dataset.stage=stage;document.querySelector('.studio-center').scrollTop=0;for(const e of document.querySelectorAll('[data-stage]'))e.setAttribute('aria-pressed',String(e.dataset.stage===stage));byId('rackView').hidden=stage==='assemble';byId('assemblyView').hidden=stage!=='assemble';byId('reviewView').hidden=stage!=='review';byId('prepareView').hidden=stage!=='prepare';byId('contextEyebrow').textContent=stage==='assemble'?'PI4 ASSEMBLY INSPECTION':'RACK DESIGN';byId('contextTitle').textContent=active()?.name||'Build your workspace';byId('contextBadge').textContent=stage==='assemble'?'Supported reference geometry':'Source mesh preview';byId('jointProperties').hidden=!window.workshopContext;byId('exportTools').hidden=!window.workshopContext;byId('jointReview').hidden=!window.workshopContext;if(stage==='assemble'){window.dispatchEvent(new Event('resize'));}drawSoon();renderReview();}
  function selectSlot(slot){if(selectedSlot===slot)return;if(!leaveAssembly())return;selectedSlot=slot;byId('mountWizard').hidden=true;inspectorTab='Setup';setStage('rack');renderTree();renderProperties();drawSoon();}
  function renderTree(){const rack=active(),tree=byId('rackTree');tree.replaceChildren();if(!rack){tree.append(paragraph('Create a rack to begin.'));return;}tree.append(paragraph(rack.slots+' SLOTS · '+rack.placements.length+(rack.placements.length===1?' ASSEMBLY':' ASSEMBLIES'),'section-eyebrow'));for(let s=1;s<=rack.slots;s++){const item=assigned(rack,s);const row=button('',()=>selectSlot(s),'slot-row'+(s===selectedSlot?' selected':''));row.setAttribute('aria-label','Slot '+s+(item?' · Raspberry Pi 4':' · Empty'));row.setAttribute('aria-pressed',String(s===selectedSlot));const number=document.createElement('span');number.className='slot-number';number.textContent=String(s).padStart(2,'0');const content=document.createElement('span');const title=document.createElement('strong');title.textContent=item?'Raspberry Pi 4':'Empty slot';content.append(title);const sub=document.createElement('small');sub.textContent=item?'Fit UNKNOWN':'Available';content.append(sub);const dot=document.createElement('i');dot.className=item?'occupied-dot':'empty-dot';row.append(number,content,dot);const wrap=document.createElement('div');wrap.className='slot-item';const more=button('⋯',()=>{selectSlot(s);showSlotMenu(s,more);},'slot-more');more.setAttribute('aria-label','More actions for slot '+s);row.oncontextmenu=e=>{e.preventDefault();selectSlot(s);showSlotMenu(s,more);};row.onkeydown=e=>{if(e.key==='ContextMenu'||(e.shiftKey&&e.key==='F10')){e.preventDefault();selectSlot(s);showSlotMenu(s,more);}};wrap.append(row,more);tree.append(wrap);}}
  function syncInspector(){
    byId('studioInspector').hidden=inspectorCollapsed;shell.classList.toggle('inspector-collapsed',inspectorCollapsed);
    byId('toggleInspector').setAttribute('aria-expanded',String(!inspectorCollapsed));byId('toggleInspector').textContent=inspectorCollapsed?'Show inspector':'Hide inspector';
    for(const name of ['Setup','Hardware','Appearance']){byId('tab'+name).setAttribute('aria-selected',String(inspectorTab===name));byId('panel'+name).hidden=inspectorTab!==name;}
    byId('hardwareEmpty').hidden=!!window.workshopContext;
    byId('tabHardware').disabled=!assigned(active(),selectedSlot);
  }
  function showInspector(name){inspectorCollapsed=false;inspectorTab=name;syncInspector();window.dispatchEvent(new Event('resize'));}
  byId('toggleInspector').onclick=()=>{inspectorCollapsed=!inspectorCollapsed;syncInspector();window.dispatchEvent(new Event('resize'));};
  for(const name of ['Setup','Hardware','Appearance']){
    const tab=byId('tab'+name);tab.onclick=async()=>{
      if(name==='Hardware'&&!window.workshopContext){const p=assigned(active(),selectedSlot);if(p){await openAssembly(p);if(!window.workshopContext)return;}}
      showInspector(name);
    };
    tab.onkeydown=e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();const tabs=['Setup','Hardware','Appearance'].map(n=>byId('tab'+n)).filter(t=>!t.disabled),i=tabs.indexOf(tab),next=e.key==='Home'?tabs[0]:e.key==='End'?tabs.at(-1):tabs[(i+(e.key==='ArrowLeft'?-1:1)+tabs.length)%tabs.length];next.focus();next.click();};
  }
  byId('save').hidden=true;byId('check').textContent='Check saved joint';

  function newAssembly(){
    if(!capable||!legacyTemplate)throw Error('Wait for the independent assembly workspace to load.');
    const id='asm-'+uid(),name='Raspberry Pi 4',project=JSON.parse(JSON.stringify(legacyTemplate));
    project.id=id;project.name=name;
    return {id,name,revision:1,project,appearance:{},fit:'UNKNOWN'};
  }
  function clearBuild(){
    previewRevision++;clearTimeout(previewTimer);generatedBuild=null;
    byId('viewProposal').disabled=byId('downloadBuild').disabled=true;
    byId('buildStatus').textContent='No generated mesh selected for this assembly.';
    byId('checks').replaceChildren();byId('resultSummary').textContent='Run checks for this saved assembly.';
    window.assemblyHardware=null;window.dispatchEvent(new CustomEvent('assembly-hardware',{detail:null}));
    window.dispatchEvent(new CustomEvent('assembly-model',{detail:null}));
  }
  function leaveAssembly(){
    if(openingAssembly||savingLayout||projectBusy){notify('Wait for the current operation to finish.',true);return false;}
    if(window.workshopContext&&dirty){notify('Save the current assembly hardware draft before changing selection.',true);return false;}
    window.workshopContext=null;clearBuild();
    byId('jointProperties').hidden=true;byId('exportTools').hidden=true;byId('jointReview').hidden=true;
    return true;
  }
  async function openAssembly(placement){
    if(!capable||openingAssembly)return;
    if(window.workshopContext?.id===placement.assembly.id){setStage('assemble');return;}
    if(!leaveAssembly())return;
    if(!persistedAssemblyIds.has(placement.assembly.id)){notify('Use Save to keep this allocation before opening its hardware editor.',true);return;}
    openingAssembly=true;byId('jointControls').inert=true;
    window.workshopContext={id:placement.assembly.id,generation:documentState.generation};
    try{clearBuild();await refresh();dirty=false;byId('dirty').textContent='Saved independent assembly · hardware pins retained.';setStage('assemble');renderProperties();applyAssemblyAppearance(placement);showInspector('Hardware');}
    catch(e){window.workshopContext=null;setStage('rack');notify(e.message,true);}
    finally{openingAssembly=false;byId('jointControls').inert=false;}
  }
  window.addEventListener('assembly-project-saved',e=>{
    const project=e.detail;byId('assemblyProjectName').textContent=project.name+' · revision '+project.instance_revision;
    for(const rack of documentState.racks)for(const p of rack.placements)if(p.assembly.id===project.instance_id){
      const clean=JSON.parse(JSON.stringify(project));delete clean.instance_id;delete clean.instance_revision;delete clean.workspace_generation;
      p.assembly.project=clean;p.assembly.revision=project.instance_revision;
    }
    documentState.generation=project.workspace_generation;
    if(window.workshopContext?.id===project.instance_id)window.workshopContext.generation=project.workspace_generation;
    renderTree();renderProperties();
  });
  function releasePlacement(placement){
    if(!leaveAssembly())return;
    lastReleased=RackLayout.release(active(),placement.id);selectedSlot=placement.slot;
    byId('mountWizard').hidden=true;markChanged();setStage('rack');render();
    notify('Allocation released in the draft. Undo restores its independent hardware and appearance. Save to keep the release; prior saved records remain in local history.');
  }
  const slotMenu=document.createElement('div');slotMenu.id='slotMenu';slotMenu.hidden=true;slotMenu.setAttribute('role','menu');shell.append(slotMenu);
  function closeSlotMenu(){slotMenu.hidden=true;}
  function showSlotMenu(slot,anchor){
    if(selectedSlot!==slot)return;
    const p=assigned(active(),slot);slotMenu.replaceChildren();
    const action=(label,fn)=>{const b=button(label,()=>{closeSlotMenu();fn();});b.setAttribute('role','menuitem');slotMenu.append(b);};
    if(p){action('Open assembly',()=>openAssembly(p));action('Edit slot allocation',()=>editAllocation(p));action('Colors & faceplate image',()=>showInspector('Appearance'));action('Release slots',()=>releasePlacement(p));}
    else action('Create assembly',startWizard);
    action('Rack colors',()=>{showInspector('Appearance');byId('rackAppearance').open=true;byId('rackAppearance').scrollIntoView({block:'nearest'});});
    anchor=byId('rackTree').querySelector('[aria-label="More actions for slot '+slot+'"]')||anchor;const box=anchor.getBoundingClientRect();slotMenu.style.left=Math.max(8,Math.min(innerWidth-238,box.right))+'px';slotMenu.style.top=Math.max(8,Math.min(innerHeight-240,box.top))+'px';slotMenu.hidden=false;slotMenu.querySelector('button')?.focus();
  }
  document.addEventListener('pointerdown',e=>{if(!slotMenu.contains(e.target)&&!e.target.closest('.slot-more'))closeSlotMenu();});
  document.addEventListener('keydown',e=>{if(slotMenu.hidden)return;const items=Array.from(slotMenu.querySelectorAll('button')),i=items.indexOf(document.activeElement);if(e.key==='Escape'){closeSlotMenu();byId('rackTree').querySelector('[aria-label="More actions for slot '+selectedSlot+'"]')?.focus();}else if(['ArrowDown','ArrowUp','Home','End'].includes(e.key)){e.preventDefault();items[e.key==='Home'?0:e.key==='End'?items.length-1:(i+(e.key==='ArrowUp'?-1:1)+items.length)%items.length]?.focus();}});
  function applyAssemblyAppearance(p){if(window.workshopContext?.id!==p?.assembly.id)return;window.assemblyAppearance=p?.assembly.appearance||{};window.dispatchEvent(new CustomEvent('assembly-appearance',{detail:window.assemblyAppearance}));}
  const colorPresets=[['Graphite','#28313c'],['Silver','#9daab8'],['Ivory','#e6e4db'],['Blue','#325a8e'],['Green','#4d8e6e'],['Copper','#ba7245'],['Gold','#d09b55'],['Red','#b95d5d']];
  function colorField(host,label,value,onChange){
    const group=document.createElement('fieldset');group.className='color-group';const legend=document.createElement('legend');legend.textContent=label;group.append(legend);
    const row=document.createElement('div');row.className='color-field';const hex=document.createElement('span');hex.textContent=value;
    const input=document.createElement('input');input.type='color';input.value=value;input.setAttribute('aria-label',label+' custom color');
    const set=v=>{input.value=v;hex.textContent=v;onChange(v);};input.oninput=()=>set(input.value);row.append(hex,input);group.append(row);
    const swatches=document.createElement('div');swatches.className='color-swatches';
    for(const [name,color] of colorPresets){const b=button('',()=>set(color));b.style.background=color;b.setAttribute('aria-label',label+': '+name);b.title=name;swatches.append(b);}group.append(swatches);host.append(group);
  }
  function renderAppearance(){
    const host=byId('appearanceProperties'),rack=active();if(!host)return;host.replaceChildren();if(!rack||!capable)return;
    rack.appearance ||= {};
    const details=document.createElement('details');details.id='rackAppearance';const summary=document.createElement('summary');summary.textContent='Rack colors';details.append(summary);
    colorField(details,'Whole rack',rack.appearance.color||'#7a8799',v=>{rack.appearance.color=v;markChanged();drawSoon();});
    const label=document.createElement('label');label.textContent='Component override';label.htmlFor='rackColorComponent';const select=document.createElement('select');select.id='rackColorComponent';
    for(const [key,title] of [['post1','1U posts'],['post2','2U posts'],['post3','3U posts'],['post4','4U posts'],['post5','5U posts'],['beam_bottom','Bottom beams'],['beam_top_front','Top front beam'],['beam_top_rear','Top rear beam'],['side_rail','Side rails'],['panel_top','Top panel'],['panel_bottom','Bottom panel'],['panel1','1U side panels'],['panel2','2U side panels'],['panel3','3U side panels'],['panel4','4U side panels'],['panel5','5U side panels'],['foot','Feet'],['handle','Handles']])select.append(new Option(title,key));
    const component=document.createElement('div');const update=()=>{component.replaceChildren();colorField(component,'Component color',rack.appearance.components?.[select.value]||rack.appearance.color||'#7a8799',v=>{rack.appearance.components ||= {};rack.appearance.components[select.value]=v;markChanged();drawSoon();});};select.onchange=update;details.append(label,select,component);update();
    details.append(button('Reset rack colors',()=>{rack.appearance={};markChanged();renderAppearance();drawSoon();},'secondary'));host.append(details);
    const p=assigned(rack,selectedSlot);if(!p)return;p.assembly.appearance ||= {};
    const artDetails=document.createElement('details');artDetails.open=true;artDetails.id='assemblyAppearance';const sum=document.createElement('summary');sum.textContent='Equipment colors & faceplate image';artDetails.append(sum);
    for(const [key,title,defaultColor] of [['equipment','Equipment (Pi reference)','#5b8545'],['tray','Tray','#4d8e6e'],['faceplate','Faceplate','#4e75a3']])colorField(artDetails,title,p.assembly.appearance[key]||defaultColor,v=>{p.assembly.appearance[key]=v;markChanged();applyAssemblyAppearance(p);});
    const fileLabel=document.createElement('label');fileLabel.textContent='Local faceplate image';fileLabel.htmlFor='faceplateImage';const file=document.createElement('input');file.id='faceplateImage';file.type='file';file.accept='image/png,image/jpeg,image/webp';file.onchange=()=>loadArtwork(file,p);artDetails.append(fileLabel,file);
    const art=p.assembly.appearance.artwork;
    if(art){artDetails.append(paragraph(art.name+' · preview only'),button('Fit & center image',()=>{Object.assign(art,{x:.5,y:.5,scale:1});markChanged();applyAssemblyAppearance(p);renderAppearance();},'secondary'),button('Center image',()=>{Object.assign(art,{x:.5,y:.5});markChanged();applyAssemblyAppearance(p);renderAppearance();},'secondary'));for(const [key,title,min,max] of [['x','Image horizontal position',0,1],['y','Image vertical position',0,1],['scale','Image size',.05,1]]){const label=document.createElement('label');label.textContent=title;const input=document.createElement('input');input.type='range';input.min=min;input.max=max;input.step=.01;input.value=art[key];input.setAttribute('aria-label',title);input.oninput=()=>{art[key]=Number(input.value);markChanged();applyAssemblyAppearance(p);};label.append(input);artDetails.append(label);}artDetails.append(button('Remove image',()=>{delete p.assembly.appearance.artwork;markChanged();applyAssemblyAppearance(p);renderAppearance();byId('assemblyAppearance').open=true;},'secondary'));}
    artDetails.append(button('View faceplate front',async()=>{await openAssembly(p);if(window.workshopContext?.id===p.assembly.id)window.dispatchEvent(new Event('assembly-faceplate-front'));},'secondary'),paragraph('Colors and images are visual previews. Save to keep them. STL files have no color or artwork.','notice'));host.append(artDetails);
  }
  async function loadArtwork(input,p){
    const file=input.files[0];if(!file)return;input.disabled=true;artworkPending++;
    const identity=p.assembly.id,request=(artworkRequests.get(identity)||0)+1;artworkRequests.set(identity,request);
    try{
      if(!['image/png','image/jpeg','image/webp'].includes(file.type)||file.size>10*1024*1024)throw Error('Choose a PNG, JPEG or WebP up to 10 MB.');
      const bitmap=await createImageBitmap(file);if(bitmap.width*bitmap.height>40_000_000){bitmap.close();throw Error('Choose an image up to 40 megapixels.');}
      const canvas=document.createElement('canvas');let url;
      for(const limit of [512,256]){const ratio=Math.min(1,limit/Math.max(bitmap.width,bitmap.height));canvas.width=Math.max(1,Math.round(bitmap.width*ratio));canvas.height=Math.max(1,Math.round(bitmap.height*ratio));canvas.getContext('2d').drawImage(bitmap,0,0,canvas.width,canvas.height);url=canvas.toDataURL('image/png');if(url.length<690000)break;}bitmap.close();
      const asset=await api('artwork',{data_url:url});
      if(artworkRequests.get(identity)!==request)return;
      p=documentState.racks.flatMap(r=>r.placements).find(item=>item.assembly.id===p.assembly.id);if(!p)throw Error('The allocation was released. Choose an existing assembly.');
      p.assembly.appearance.artwork={sha256:asset.sha256,name:file.name.slice(0,120),mode:'preview-only',x:.5,y:.5,scale:.65};markChanged();applyAssemblyAppearance(p);renderAppearance();if(byId('assemblyAppearance'))byId('assemblyAppearance').open=true;notify('Local faceplate preview image prepared. Save to keep its placement. STL geometry is unchanged.');
    }catch(e){notify(e.message,true);}finally{input.disabled=false;artworkPending--;}
  }

  function appendReleaseUndo(host,rack){
    if(lastReleased?.rackId!==rack.id)return;
    host.append(button('Undo slot release',()=>{try{const item=RackLayout.restore(rack,lastReleased);lastReleased=null;selectedSlot=item.slot;markChanged();render();notify('Slot allocation restored in the draft. Save to keep it.');}catch(e){notify('Cannot restore allocation: '+e.message,true);}},'secondary'));
  }
  function renderProperties(){
    const rack=active(),host=byId('slotProperties');host.replaceChildren();renderAppearance();byId('jointProperties').open=stage==='assemble';syncInspector();
    byId('selectionSummary').textContent=rack?rack.name+(selectedSlot?' / Slot '+selectedSlot:' / Rack'):'No rack selected';
    if(!rack){host.append(paragraph('Create a rack layout to define your workspace.'),button('Create rack',()=>openRackDialog(false),'primary'));return;}
    byId('propertiesContext').textContent=selectedSlot?'Slot '+selectedSlot:'Rack layout';host.append(paragraph('CURRENT SELECTION','section-eyebrow'));
    const title=document.createElement('h2');title.textContent=selectedSlot?'Slot '+String(selectedSlot).padStart(2,'0'):rack.name;host.append(title);
    if(!selectedSlot){host.append(paragraph(rack.slots+' slots · '+rack.placements.length+' assigned assemblies'),button('Edit rack settings',()=>openRackDialog(true),'secondary'));appendReleaseUndo(host,rack);return;}
    const placement=assigned(rack,selectedSlot);
    if(placement){host.append(paragraph('Raspberry Pi 4 · slots '+placement.slot+'–'+(placement.slot+placement.span-1)),paragraph('Reference allocation. Installed fit, service access and load capacity are UNKNOWN.'),button('Open assembly',()=>openAssembly(placement),'primary'),button('Slot actions ⋯',e=>showSlotMenu(selectedSlot,e.currentTarget),'secondary'));}
    else{host.append(paragraph('An open slot in your rack. Choose equipment to begin a guided assembly.'),button('Create assembly',startWizard,'primary'));}
    if(placement&&!persistedAssemblyIds.has(placement.assembly.id)){host.querySelector('button.primary').disabled=true;host.append(paragraph('Use Save to keep this allocation before opening its hardware editor.'));}
    appendReleaseUndo(host,rack);
  }
  function editAllocation(placement){
    showInspector('Setup');
    const rack=active(),wizard=byId('mountWizard');wizard.hidden=false;wizard.replaceChildren();wizard.append(paragraph('EDIT SLOT ALLOCATION','section-eyebrow'));
    for(const [id,label,value] of [['allocationStart','Starting slot',placement.slot],['allocationSpan','Number of slots to reserve',placement.span]]){const caption=document.createElement('label');caption.htmlFor=id;caption.textContent=label;const input=document.createElement('input');input.id=id;input.type='number';input.min='1';input.max=String(rack.slots);input.step='1';input.value=String(value);wizard.append(caption,input);}
    wizard.append(paragraph('This edits the logical reservation. It does not move or resize manufacturing meshes or verify rack fit. The independent assembly record is retained.','notice'));
    const error=paragraph('','fail');error.setAttribute('role','alert');wizard.append(error,button('Apply allocation',()=>{try{const current=active();if(current?.id!==rack.id)throw Error('Select the original rack before applying this allocation.');const item=RackLayout.change(current,placement.id,Number(byId('allocationStart').value),Number(byId('allocationSpan').value));selectedSlot=item.slot;wizard.hidden=true;markChanged();setStage('rack');render();notify('Slot allocation updated in the draft. Save to keep it.');}catch(e){error.textContent=e.message;}},'primary'),button('Cancel',()=>{wizard.hidden=true;},'secondary'));
  }
  function startWizard(){if(!capable){notify('Wait for the updated workspace to load.',true);return;}showInspector('Setup');const rack=active();if(!rack||!selectedSlot){notify('Select an empty rack slot first.');return;}if(assigned(rack,selectedSlot)){notify('This slot already has an assembly. Select an empty slot.');return;}const wizard=byId('mountWizard');wizard.hidden=false;wizard.replaceChildren();wizard.append(paragraph('CREATE ASSEMBLY · SLOT '+selectedSlot,'section-eyebrow'));const h=document.createElement('h2');h.textContent='Make space for a Pi4';wizard.append(h,paragraph('1 · Equipment'),paragraph('Raspberry Pi 4 · documented tray and faceplate baseline.'),paragraph('2 · Slot allocation'));const label=document.createElement('label');label.htmlFor='allocationSpan';label.textContent='Number of slots to reserve';const input=document.createElement('input');input.id='allocationSpan';input.type='number';input.min='1';input.max=String(rack.slots-selectedSlot+1);input.step='1';input.value='1';wizard.append(label,input,paragraph('3 · Review'),paragraph('This creates an independent assembly, copying the current legacy hardware pins once. Save before opening its editor. It does not build meshes or confirm rack fit.','notice'));const error=paragraph('','fail');error.setAttribute('role','alert');wizard.append(error,button('Confirm slot allocation',()=>{const span=Number(input.value);if(!Number.isInteger(span)||span<1||selectedSlot+span-1>rack.slots){error.textContent='Choose a whole slot count within the rack.';return;}const current=active();if(current?.id!==rack.id){error.textContent='Select the original rack before confirming.';return;}for(let s=selectedSlot;s<selectedSlot+span;s++)if(assigned(current,s)){error.textContent='That allocation overlaps another assembly.';return;}current.placements.push({assembly:newAssembly(),id:uid(),equipment:'pi4',slot:selectedSlot,span,geometry:'pi4-clearance-v2-reference',fit:'UNKNOWN'});markChanged();wizard.hidden=true;renderTree();setStage('rack');renderProperties();notify('Slot allocation added to the draft layout. Save to keep it. No meshes were generated.');},'primary'),button('Cancel',()=>{wizard.hidden=true;},'secondary'));}
  function renderReview(){const rack=active(),host=byId('rackReview');host.replaceChildren();host.append(paragraph('UNKNOWN · Rack installation and strength','review-unknown'));if(!rack){host.append(paragraph('No rack layout selected.'));return;}const missing=['width_mm','depth_mm','pitch_mm'].filter(k=>rack[k]===null);host.append(paragraph(missing.length?'UNKNOWN · '+missing.map(k=>({width_mm:'internal width',depth_mm:'usable depth',pitch_mm:'slot pitch'}[k])).join(', ')+' not specified.':'USER-SUPPLIED · Layout dimensions recorded; physical fit is not verified.'));host.append(paragraph('Slot allocations do not overlap. This is logical occupancy only; component geometry and tool/cable clearance are not screened against the rack.'));for(const p of rack.placements)host.append(paragraph('Pi4 · slots '+p.slot+'–'+(p.slot+p.span-1)+' · supported reference assembly; rack fit UNKNOWN.'));}
  function render(){const rack=active();byId('rackChoice').replaceChildren();if(!documentState.racks.length)byId('rackChoice').append(new Option('No rack layout yet',''));for(const r of documentState.racks)byId('rackChoice').append(new Option(r.name,r.id));byId('rackChoice').value=activeId||'';byId('projectTitle').textContent=rack?.name||'Your rack workspace';byId('layoutSaveStatus').textContent=layoutDirty?'Layout changes · unsaved':rack?'Layout saved locally':'No rack selected';updateSaveStatus();byId('rackDimensions').textContent=rack?(rack.width_mm===null?'Width unknown':rack.width_mm+' mm wide')+' · '+(rack.depth_mm===null?'Depth unknown':rack.depth_mm+' mm deep')+' · '+rack.slots+' slots':'Dimensions not configured';byId('rackScale').textContent='Supplied rack meshes · visual placement';renderTree();renderProperties();renderReview();setStage(stage);}
  function openRackDialog(edit){if(!leaveAssembly())return;editingId=edit?activeId:null;const rack=edit?active():null;byId('rackDialogTitle').textContent=edit?'Rack settings':'Create your rack';byId('rackName').value=rack?.name||'My Lab Rax';byId('rackSlots').value=rack?.slots||5;byId('rackWidth').value=rack?.width_mm??'';byId('rackDepth').value=rack?.depth_mm??'';byId('rackPitch').value=rack?.pitch_mm??'';byId('rackFormError').textContent='';byId('rackDialog').showModal();}
  byId('rackForm').onsubmit=e=>{e.preventDefault();const number=id=>byId(id).value.trim()===''?null:Number(byId(id).value);const old=documentState.racks.find(r=>r.id===editingId);const next={id:old?.id||uid(),name:byId('rackName').value.trim(),slots:Number(byId('rackSlots').value),width_mm:number('rackWidth'),depth_mm:number('rackDepth'),pitch_mm:number('rackPitch'),appearance:old?.appearance||{},placements:old?.placements||[]};if(next.placements.some(p=>p.slot+p.span-1>next.slots)){byId('rackFormError').textContent='Existing assemblies extend beyond this slot count. Keep enough slots for them.';return;}if(!next.name||!Number.isInteger(next.slots)||next.slots<1||next.slots>48||['width_mm','depth_mm','pitch_mm'].some(k=>next[k]!==null&&(!Number.isFinite(next[k])||next[k]<=0||next[k]>10000))){byId('rackFormError').textContent='Check the rack name, slot count and positive dimensions.';return;}if(documentState.racks.length>=50&&!old){byId('rackFormError').textContent='This workspace supports up to 50 rack layouts.';return;}if(old)documentState.racks[documentState.racks.indexOf(old)]=next;else documentState.racks.push(next);activeId=next.id;selectedSlot=null;markChanged();byId('rackDialog').close();stage='rack';render();notify('Rack layout updated in the draft. Save to keep it.');};
  async function saveWorkshop(){
    if(!capable)throw Error('Restart the local app server to enable this version of Save.');
    if(openingAssembly||savingLayout)throw Error('Wait for the current operation to finish.');
    if(artworkPending)throw Error('Wait for the image preview to finish preparing, then Save.');
    if(!byId('mountWizard').hidden||byId('rackDialog').open)throw Error('Apply or cancel the open rack or allocation editor before saving.');
    savingLayout=true;updateSaveStatus();
    try{
      const snapshot=JSON.stringify(documentState),identity=window.workshopContext?.id,hardware=identity?payload():null;
      const saved=await api('studio-save',{workspace:documentState,assembly:hardware?{...hardware,id:identity}:null});
      const newerLayout=JSON.stringify(documentState)!==snapshot;
      let newerHardware=false;
      if(hardware){try{newerHardware=JSON.stringify(payload())!==JSON.stringify(hardware);}catch(e){newerHardware=true;}}
      if(!newerLayout){documentState=saved;layoutDirty=false;}
      else{
        documentState.generation=saved.generation;
        for(const local of documentState.racks.flatMap(r=>r.placements)){
          const committed=saved.racks.flatMap(r=>r.placements).find(p=>p.assembly.id===local.assembly.id);
          if(committed){local.assembly.project=committed.assembly.project;local.assembly.revision=committed.assembly.revision;}
        }
        layoutDirty=true;
      }
      persistedAssemblyIds=new Set(saved.racks.flatMap(r=>r.placements.map(p=>p.assembly.id)));
      if(identity&&window.workshopContext?.id===identity){
        const record=saved.racks.flatMap(r=>r.placements).find(p=>p.assembly.id===identity)?.assembly;
        if(!record)throw Error('The current assembly was removed; reload before editing it.');
        if(record.revision!==state.project.instance_revision)clearBuild();
        state.project={...record.project,instance_id:record.id,instance_revision:record.revision,workspace_generation:saved.generation};
        window.workshopContext.generation=saved.generation;dirty=!!newerHardware;
        byId('assemblyProjectName').textContent=record.name+' · revision '+record.revision;
        byId('dirty').textContent=dirty?'Saved earlier hardware inputs; newer edits remain unsaved.':'Saved locally · independent hardware pins retained.';
        renderReplacement();if(typeof preview==='function'&&typeof safe==='function')safe(preview);
      }
      render();notify(layoutDirty||dirty?'Saved the submitted changes. Newer edits remain unsaved.':'Saved rack, hardware and appearance locally.');
      return saved;
    }finally{savingLayout=false;updateSaveStatus();}
  }
  window.saveWorkshop=saveWorkshop;
  window.assertWorkshopSaved=()=>{if(layoutDirty||dirty||savingLayout||artworkPending)throw Error('Use Save to keep pending changes before checking or exporting.');};
  byId('saveLayout').onclick=async()=>{try{await saveWorkshop();}catch(e){notify(e.message,true);}};

  byId('rackChoice').onchange=e=>{if(!leaveAssembly()){e.target.value=activeId;return;}activeId=e.target.value;selectedSlot=null;stage='rack';byId('mountWizard').hidden=true;render();};
  for(const e of document.querySelectorAll('[data-stage]'))e.onclick=()=>{setStage(e.dataset.stage);renderProperties();};
  byId('newRack').onclick=()=>openRackDialog(false);byId('configureRack').onclick=()=>openRackDialog(!!active());byId('backToRack').onclick=()=>{setStage('rack');renderProperties();};
  byId('closeRackDialog').onclick=byId('cancelRackDialog').onclick=()=>byId('rackDialog').close();
  function libraryTab(which){byId(which==='equipment'?'equipmentSection':'racksSection').open=true;}
  byId('pi4Card').onclick=startWizard;
  function dashboard(){const list=byId('recentRacks');list.replaceChildren();if(!documentState.racks.length)list.append(paragraph('Your saved layouts will appear here.'));for(const rack of documentState.racks)list.append(button(rack.name+' · '+rack.slots+' slots',()=>{if(!leaveAssembly())return;activeId=rack.id;selectedSlot=null;stage='rack';byId('dashboardDialog').close();render();},'recent-rack'));byId('dashboardDialog').showModal();}
  byId('homeStudio').onclick=dashboard;byId('closeDashboard').onclick=()=>byId('dashboardDialog').close();byId('dashboardNew').onclick=()=>{byId('dashboardDialog').close();openRackDialog(false);};
  const shortcuts=[['Orbit rack','Drag in the rack viewport'],['Orbit assembly','Arrow keys while the assembly viewport is focused'],['Save rack layout','Ctrl / ⌘ + S'],['Cancel dialog','Escape'],['Inspect a slot','Select a slot in Assembly Explorer']];
  function renderShortcuts(){const list=byId('shortcutList');list.replaceChildren();for(const [name,key] of shortcuts)if((name+' '+key).toLowerCase().includes(byId('shortcutSearch').value.toLowerCase()))list.append(paragraph(name+' — '+key));}
  byId('shortcutHelp').onclick=()=>{renderShortcuts();byId('shortcutsDialog').showModal();};byId('shortcutSearch').oninput=renderShortcuts;byId('closeShortcuts').onclick=()=>byId('shortcutsDialog').close();
  window.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){e.preventDefault();if(layoutDirty||dirty)byId('saveLayout').click();}});
  window.addEventListener('beforeunload',e=>{if(layoutDirty||dirty){e.preventDefault();e.returnValue='';}});

  // Actual source components in recovered visual poses, isolated from STL export.
  let showRackPanels=false, perspectiveCamera=true, studioQuality=true;
  function drawSoon(){if(!pending){pending=true;requestAnimationFrame(drawRack);}}
  function drawRack(){
    pending=false;if(byId('rackView').hidden||!rackContext)return;
    const w=Math.max(280,rackCanvas.clientWidth),h=Math.max(350,rackCanvas.clientHeight),dpr=Math.min(window.devicePixelRatio||1,2);
    rackCanvas.width=Math.round(w*dpr);rackCanvas.height=Math.round(h*dpr);
    const ctx=rackContext;ctx.setTransform(dpr,0,0,dpr,0,0);ctx.fillStyle='#151c26';ctx.fillRect(0,0,w,h);clickRegions=[];
    const rack=active();
    if(!rack||!sourceMeshes||!sceneRenderer){ctx.fillStyle='#aab9cb';ctx.font='15px system-ui';ctx.textAlign='center';ctx.fillText(!rack?'Create a rack layout to begin':sourceError||'Loading your Lab Rax enclosure meshes…',w/2,h/2);return;}
    const key=rack.slots+':'+showRackPanels;
    if(sceneCacheKey!==key){const scene=LabRaxScene.frame(rack.slots,showRackPanels);sceneCache={scene,box:LabRaxScene.bounds(scene,sourceMeshes)};sceneCacheKey=key;}
    const {scene,box}=sceneCache,view=LabRaxStudio.camera(box,yaw,pitch,w,h,zoom,perspectiveCamera),project=view.project;
    try {
    if(sceneRenderer.restoreRequired){sceneRenderer.dispose();sceneRenderer=new LabRaxStudio.Renderer();sceneRenderer.invalidated=drawSoon;}
    sceneRenderer.shadows=studioQuality&&sceneRenderer.shadowSupported;sceneRenderer.ambientOcclusion=studioQuality;
    ctx.drawImage(sceneRenderer.draw(scene,sourceMeshes,view,Math.round(w*dpr),Math.round(h*dpr),rack,selectedSlot),0,0,w,h);
    } catch(e) {sourceError=e.message;ctx.fillStyle='#efb6a5';ctx.fillText(sourceError,24,36);return;}
    for(let slot=1;slot<=rack.slots;slot++){
      const z=(rack.slots-slot)*LabRaxScene.U,points=[[-104,-3,z+1],[104,-3,z+1],[104,-3,z+LabRaxScene.U-1],[-104,-3,z+LabRaxScene.U-1]].map(project),selected=slot===selectedSlot,placement=assigned(rack,slot);
      clickRegions.push({slot,p:points});
      const label=project([-154,-3,z+LabRaxScene.U/2]);ctx.textAlign='right';ctx.fillStyle=selected?'#a2ceff':placement?'#81cfb5':'#8fa5bf';ctx.font='11px ui-monospace,monospace';ctx.fillText('U'+String(slot).padStart(2,'0'),label[0],label[1]+4);
    }
    ctx.textAlign='left';rackCanvas.dataset.preview='source-mesh';rackCanvas.dataset.parts=String(scene.parts.length);rackCanvas.dataset.triangles=String(sceneRenderer.stats?.triangles||0);rackCanvas.dataset.quality=studioQuality?'studio':'fast';
    byId('rackScale').textContent=(perspectiveCamera?'Perspective':'Orthographic')+' · depth-tested · '+(sceneRenderer.stats?.triangles||0).toLocaleString()+' triangles';
  }
  try{sceneRenderer=new LabRaxStudio.Renderer();sceneRenderer.invalidated=drawSoon;LabRaxScene.load(fetch).then(meshes=>{sourceMeshes=meshes;drawSoon();}).catch(e=>{sourceError=e.message;drawSoon();});}catch(e){sourceError=e.message;}
  byId('frontRackView').onclick=()=>{perspectiveCamera=false;yaw=0;pitch=0;zoom=1;drawSoon();};
  byId('renderQuality').onclick=()=>{studioQuality=!studioQuality;byId('renderQuality').setAttribute('aria-pressed',String(studioQuality));byId('renderQuality').textContent=studioQuality?'Studio quality':'Fast preview';drawSoon();};
  byId('toggleRackPanels').onclick=()=>{showRackPanels=!showRackPanels;byId('toggleRackPanels').setAttribute('aria-pressed',String(showRackPanels));drawSoon();};
  rackCanvas.addEventListener('wheel',e=>{e.preventDefault();zoom=Math.max(.5,Math.min(2.5,zoom*Math.exp(-e.deltaY*.001)));drawSoon();},{passive:false});
  rackCanvas.onpointerdown=e=>{drag={x:e.clientX,y:e.clientY,startX:e.clientX,startY:e.clientY,moved:false};rackCanvas.setPointerCapture(e.pointerId);};
  rackCanvas.onpointermove=e=>{if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;drag.moved=drag.moved||Math.hypot(e.clientX-drag.startX,e.clientY-drag.startY)>4;yaw+=dx*.006;pitch=Math.max(-1.1,Math.min(1.1,pitch+dy*.006));drag.x=e.clientX;drag.y=e.clientY;drawSoon();};
  rackCanvas.onpointerup=e=>{
    if(drag&&!drag.moved){const rect=rackCanvas.getBoundingClientRect(),slot=sceneRenderer?.pick(e.clientX-rect.left,e.clientY-rect.top);if(slot)selectSlot(slot);}
    drag=null;
  };rackCanvas.onpointercancel=()=>{drag=null;};
  rackCanvas.onkeydown=e=>{if(e.key==='ArrowLeft')yaw-=.12;else if(e.key==='ArrowRight')yaw+=.12;else if(e.key==='ArrowUp')pitch=Math.min(1.1,pitch+.12);else if(e.key==='ArrowDown')pitch=Math.max(-1.1,pitch-.12);else return;e.preventDefault();drawSoon();};
  byId('resetRackView').onclick=()=>{perspectiveCamera=true;yaw=-.48;pitch=.24;zoom=1;drawSoon();};new ResizeObserver(drawSoon).observe(rackCanvas);
  Promise.all([api('workspace-capabilities'),api('rack-workspace'),api('project')]).then(([caps,data,template])=>{if(!caps.independent_assemblies||caps.version!==2||caps.studio_save_version!==1)throw Error('Restart the app server to enable this updated interface.');capable=true;legacyTemplate=template;documentState=data;persistedAssemblyIds=new Set(data.racks.flatMap(r=>r.placements.map(p=>p.assembly.id)));activeId=data.racks[0]?.id||null;render();if(!activeId)dashboard();}).catch(e=>{notify('Rack layouts unavailable: '+e.message,true);byId('saveLayout').disabled=true;});
})();
