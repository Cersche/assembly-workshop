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
    <nav class="studio-nav" aria-label="Workspace"><span class="local-label"><i></i> LOCAL WORKSPACE</span><div class="stage-tabs"><button data-stage="rack" aria-pressed="true">01 <span>Rack</span></button><button data-stage="assemble" aria-pressed="false">02 <span>Assemble</span></button><button data-stage="review" aria-pressed="false">03 <span>Review</span></button><button data-stage="prepare" aria-pressed="false">04 <span>Prepare</span></button></div><div class="studio-view-actions"><button id="configureRack" class="subtle">Rack settings</button><button id="rackHistory" class="subtle" hidden>History</button><button id="toggleInspector" class="subtle" aria-expanded="true" aria-controls="studioInspector">Hide inspector</button></div></nav>
    <div class="studio-columns"><aside class="studio-left"><details id="racksSection" class="library-section" open><summary>Racks & slots</summary><div class="panel-heading"><span>PROJECT</span><button id="newRack" class="subtle" aria-label="New rack">＋</button></div><label class="sr-only" for="rackChoice">Rack layout</label><select id="rackChoice"></select><div id="explorerPane"><div id="rackTree"></div><p class="sidebar-hint">Select a slot to place equipment.<br>Slot 1 starts at the top.</p></div></details><details id="equipmentSection" class="library-section"><summary>Equipment</summary><div id="equipmentPane"><p class="section-eyebrow">SUPPORTED EQUIPMENT</p><button id="pi4Card" class="equipment-card"><svg viewBox="0 0 220 125" aria-hidden="true"><path d="M24 53 145 22 199 59 77 94Z" fill="#46977c"/><path d="M24 53v10l53 40V94m0 0 122-35v10L77 103" fill="#246c58"/><path d="m72 48 46-12 30 20-47 13Z" fill="#233637"/><path d="m150 33 17-4 26 18-16 5Zm-22 9 17-4 26 18-16 5Z" fill="#aab8c0"/><path d="m31 48 20-5 10 7-20 5Z" fill="#d0b662"/></svg><strong>Raspberry Pi 4</strong><span>Tray + faceplate · supported baseline</span><small>Choose a slot, then create an assembly →</small></button></div></details><details id="hardwareSection" class="library-section hardware-drawer"><summary>Hardware</summary><div id="hardwarePane"></div></details></aside>
    <main class="studio-center"><div class="viewport-heading"><div><p class="section-eyebrow" id="contextEyebrow">RACK DESIGN</p><h1 id="contextTitle">Build your workspace</h1></div><span id="contextBadge" class="studio-badge">Layout planning</span></div><section id="rackView"><div class="rack-toolbar"><span id="rackDimensions" class="tb-summary">No rack yet</span><span class="tb-group" role="group" aria-label="Camera"><span class="tb-label">View</span><button id="resetRackView" class="tb-seg" aria-pressed="true" title="Angled 3D view you can orbit">3D</button><button id="frontRackView" class="tb-seg" aria-pressed="false" title="Straight-on front view">Front</button></span><span class="tb-group" role="group" aria-label="Show"><span class="tb-label">Show</span><button id="toggleRackPanels" class="tb-toggle" aria-pressed="false">Side panels</button><button id="toggleRearLabels" class="tb-toggle" aria-pressed="false">Back labels</button></span><span class="tb-group"><button id="renderQuality" class="tb-toggle" aria-pressed="true" title="Soft shadows and shading. Turn off if the view feels slow.">Shadows</button></span></div><canvas id="rackCanvas" tabindex="0" aria-label="Lab Rax source meshes. Drag to orbit, scroll to zoom; select a slot in Explorer."></canvas><div class="viewport-caption"><span><i class="axis-x">X</i> <i class="axis-y">Y</i> <i class="axis-z">Z</i> Drag to orbit · scroll to zoom · select a slot</span><span id="rackScale">Schematic · not manufacturing geometry</span></div></section><div id="assemblyView" hidden></div><div class="context-strip"><span id="selectionSummary">No slot selected</span><button id="backToRack" class="subtle">View rack</button></div><section id="reviewView" hidden><div class="section-heading"><h2>Design review</h2><span class="studio-badge">Evidence and limits</span></div><div id="rackReview"></div><div id="jointReview"></div></section><section id="prepareView" hidden><div class="section-heading"><h2>Prepare & export</h2><span class="studio-badge">STL delivery</span></div><p class="notice">The current geometry adapter exports the Pi4 assembly in its documented assembly coordinates. Rack frames, slot positions and other equipment are layout context and are not included in these STLs. Physical rack fit and strength remain UNKNOWN.</p><div id="exportTools"></div></section><div id="workspaceMessage" role="status" aria-live="polite"></div></main>
    <aside class="studio-right" id="studioInspector"><div class="panel-heading">INSPECTOR <span id="propertiesContext">Rack layout</span></div><div class="inspector-tabs" role="tablist" aria-label="Inspector"><button id="tabSetup" role="tab" aria-selected="true" aria-controls="panelSetup">Setup</button><button id="tabHardware" role="tab" aria-selected="false" aria-controls="panelHardware">Hardware</button><button id="tabAppearance" role="tab" aria-selected="false" aria-controls="panelAppearance">Appearance</button></div><section id="panelSetup" role="tabpanel" aria-labelledby="tabSetup"><div id="slotProperties"></div><div id="mountWizard" hidden></div><details class="reference-drawer"><summary>Project status & limitations</summary><div id="roadmapPane"></div></details></section><section id="panelHardware" role="tabpanel" aria-labelledby="tabHardware" hidden><p id="hardwareEmpty" class="muted">Select an allocated slot and open its assembly to edit hardware.</p><div id="jointProperties"><p class="notice">Independent hardware project. Installed fit and strength remain UNKNOWN.</p><div id="jointControls"></div></div></section><section id="panelAppearance" role="tabpanel" aria-labelledby="tabAppearance" hidden><div id="appearanceProperties"></div></section></aside></div>
    <footer class="studio-footer"><span id="workspaceFooter">Local rack layout · no cloud connection required</span><span>Millimeters · physical fit UNKNOWN</span></footer>
    <dialog id="rackDialog" style="max-width: 640px; width: 95%;">
      <form id="rackForm">
        <div class="dialog-heading"><span class="section-eyebrow">MODULAR RACK CONFIGURATION</span><button type="button" id="closeRackDialog" class="subtle" aria-label="Close rack setup">✕</button></div>
        <h2 id="rackDialogTitle">Modular Post Stacking</h2>
        <p class="muted">Configure vertical capacity (1U to 14U) by composing post segments and support extensions.</p>
        <label for="rackName">Project / rack name</label>
        <input id="rackName" maxlength="100" required placeholder="My Lab Rax">
        <div style="margin: 14px 0;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <label for="rackSlots" style="font-weight:600;">Total Vertical Capacity</label>
            <span id="slotCountDisplay" style="font-weight:700; color:#55a6ff; font-size:16px;">5U</span>
          </div>
          <input id="rackSlots" type="range" min="1" max="14" step="1" value="5" style="width:100%; margin:8px 0;">
          <p class="section-eyebrow" style="margin-top:10px;">POST SEGMENTS TRAY</p>
          <div id="postPiecesTray" style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:8px;">
            <button type="button" class="subtle piece-chip" data-u="1">+ 1U Post</button>
            <button type="button" class="subtle piece-chip" data-u="2">+ 2U Post</button>
            <button type="button" class="subtle piece-chip" data-u="3">+ 3U Post</button>
            <button type="button" class="subtle piece-chip" data-u="4">+ 4U Post</button>
            <button type="button" class="subtle piece-chip" data-u="5">+ 5U Post</button>
            <button type="button" class="subtle piece-chip" data-u="1" title="1U Support Extension">+ 1U Support Extension</button>
          </div>
          <canvas id="rackPreviewCanvas" aria-label="Frame preview. Drop post segments here." style="width:100%; height:260px; display:block; border:1px dashed #3a4a5e; border-radius:6px;"></canvas>
          <p class="section-eyebrow" style="margin-top:10px;">BILL OF MATERIALS</p>
          <div id="rackBom" class="muted" style="font-size:13px;"></div>
        </div>
        <div id="rackFormError" class="fail" role="alert"></div>
        <div class="dialog-actions">
          <button type="button" id="cancelRackDialog" class="secondary">Cancel</button>
          <button class="primary" type="submit">Apply modular layout</button>
        </div>
      </form>
    </dialog>
    <dialog id="dashboardDialog"><div class="dialog-heading"><span class="section-eyebrow">YOUR WORKSHOP</span><button id="closeDashboard" class="subtle" aria-label="Close dashboard">✕</button></div><h2>Start with the rack.<br>Make room for your ideas.</h2><p class="muted">Plan the space, place your equipment, then work on the assembly.</p><div class="dashboard-grid"><div><h3>Start a project</h3><button id="dashboardNew" class="template-card"><span class="template-icon">▥</span><strong>Custom Lab Rax layout</strong><small>Choose slots and reference dimensions</small></button></div><div><h3>Recent local layouts</h3><div id="recentRacks"></div></div></div><p class="notice">Your existing Pi4 library, saved hardware selections and immutable meshes remain available. A rack layout is saved separately from that project.</p></dialog>
    <dialog id="shortcutsDialog"><div class="dialog-heading"><h2>Keyboard shortcuts</h2><button id="closeShortcuts" class="subtle" aria-label="Close keyboard shortcuts">✕</button></div><label for="shortcutSearch">Find a shortcut</label><input id="shortcutSearch" placeholder="Search commands"><div id="shortcutList"></div></dialog>`;
  document.body.prepend(shell);
  const paintStyle=document.createElement('style');paintStyle.textContent=`
    .paint-themes{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
    .paint-theme{display:flex;align-items:center;gap:6px;font-size:12px;padding:5px 9px;border-radius:999px}
    .paint-theme::before{content:'';width:14px;height:14px;border-radius:50%;background:linear-gradient(135deg,var(--body) 60%,var(--logo) 60%);box-shadow:0 0 0 1px #0006}
    .paint-list{display:grid;gap:4px;margin-bottom:10px}
    .paint-item{background:transparent;border:1px solid #2c3a4b;color:inherit;display:grid;grid-template-columns:18px 1fr auto;align-items:center;gap:8px;text-align:left;padding:7px 9px;border-radius:6px}
    .paint-item i{width:18px;height:18px;border-radius:4px;box-shadow:0 0 0 1px #0007}
    .paint-item small{opacity:.6;font-size:11px}
    .paint-item.active{outline:2px solid #55a6ff}
    .rack-toolbar{justify-content:flex-start;flex-wrap:wrap;gap:14px;padding:8px 12px}
    .tb-summary{font-size:13px;font-weight:600;color:#dce8f7;margin-right:auto}
    .tb-group{display:flex;align-items:center;gap:4px}
    .tb-label{font-size:10px;letter-spacing:1px;text-transform:uppercase;color:#7189a8;margin-right:4px}
    .tb-seg,.tb-toggle,.tb-more{font-size:12px;padding:5px 11px;border-radius:6px;background:#202d3e;border:1px solid #2f3f55;color:#b9c9de}
    .tb-seg[aria-pressed=true]{background:#2f5f99;border-color:#4f86c9;color:#fff}
    .tb-toggle::before{content:'';display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;background:#3a4a60;vertical-align:1px}
    .tb-toggle[aria-pressed=true]{color:#e6f0fc}.tb-toggle[aria-pressed=true]::before{background:#6fd3a5}
    .tb-more{background:transparent;margin-left:auto}`;
  document.head.append(paintStyle);
  // Sidebar Hardware library: shared catalog only; per-slot choices live in the inspector's Hardware tab.
  byId('hardwareSection').querySelector('summary').textContent='Hardware library';
  const hwHint=document.createElement('p');hwHint.className='sidebar-hint';
  hwHint.textContent='Shared parts list. Each slot’s own hardware choices are in the inspector’s Hardware tab.';
  const addParts=document.createElement('details');addParts.className='hw-add';
  addParts.innerHTML='<summary>Add or import parts</summary>';addParts.append(packCard,importCard);
  byId('hardwarePane').append(hwHint,hardwareCard,addParts);
  {const cov=byId('coverage'),toggle=document.createElement('button');toggle.type='button';toggle.className='secondary hw-cov-toggle';toggle.hidden=true;
    cov.after(toggle);let showAll=false;
    const tidy=()=>{let empty=0;
      for(const s of cov.children){const m=s.textContent.match(/^(\S+) · (\d+) S \/ (\d+) I$/);
        if(m)s.textContent=`${m[1]} · ${m[2]} screw${m[2]==='1'?'':'s'} / ${m[3]} insert${m[3]==='1'?'':'s'}`;
        const isEmpty=/· 0 screws \/ 0 inserts$/.test(s.textContent);s.classList.toggle('cov-empty',isEmpty);empty+=isEmpty;}
      cov.classList.toggle('show-all',showAll);toggle.hidden=!empty;
      toggle.textContent=showAll?'Hide empty sizes':`${empty} size${empty===1?'':'s'} awaiting parts`;};
    toggle.onclick=()=>{showAll=!showAll;tidy();};
    new MutationObserver(tidy).observe(cov,{childList:true});tidy();}
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
  function setStage(next){if(next==='assemble'&&!window.workshopContext){const p=assigned(active(),selectedSlot);if(p){openAssembly(p);return;}notify('Select an allocated slot and open its saved assembly first.');next='rack';}stage=next;byId('jointProperties').open=stage==='assemble';shell.dataset.stage=stage;document.querySelector('.studio-center').scrollTop=0;for(const e of document.querySelectorAll('[data-stage]'))e.setAttribute('aria-pressed',String(e.dataset.stage===stage));byId('rackView').hidden=stage==='assemble';byId('assemblyView').hidden=stage!=='assemble';byId('reviewView').hidden=stage!=='review';byId('prepareView').hidden=stage!=='prepare';byId('contextEyebrow').textContent=stage==='assemble'?'PI4 ASSEMBLY INSPECTION':'RACK DESIGN';byId('contextTitle').textContent=active()?.name||'Build your workspace';byId('contextBadge').textContent=stage==='assemble'?'Pi 4 assembly':'Rack preview';byId('jointProperties').hidden=!window.workshopContext;byId('exportTools').hidden=!window.workshopContext;byId('jointReview').hidden=!window.workshopContext;if(stage==='assemble'){window.dispatchEvent(new Event('resize'));}drawSoon();renderReview();}
  function selectSlot(slot){if(selectedSlot===slot)return;if(!leaveAssembly())return;selectedSlot=slot;byId('mountWizard').hidden=true;inspectorTab='Setup';setStage('rack');renderTree();renderProperties();drawSoon();}
  function renderTree(){const rack=active(),tree=byId('rackTree');tree.replaceChildren();if(!rack){tree.append(paragraph('Create a rack to begin.'));return;}tree.append(paragraph(rack.slots+' SLOTS · '+rack.placements.length+(rack.placements.length===1?' ASSEMBLY':' ASSEMBLIES'),'section-eyebrow'));for(let s=1;s<=rack.slots;s++){const item=assigned(rack,s);const row=button('',()=>selectSlot(s),'slot-row'+(s===selectedSlot?' selected':''));row.setAttribute('aria-label','Slot '+s+(item?' · '+(item.assembly?.name||'Raspberry Pi 4'):' · Empty'));row.setAttribute('aria-pressed',String(s===selectedSlot));const number=document.createElement('span');number.className='slot-number';number.textContent=String(s).padStart(2,'0');const content=document.createElement('span');const title=document.createElement('strong');title.textContent=item?(item.assembly?.name||'Raspberry Pi 4'):'Empty slot';content.append(title);const sub=document.createElement('small');sub.textContent=item?'Fit UNKNOWN':'Available';content.append(sub);const dot=document.createElement('i');dot.className=item?'occupied-dot':'empty-dot';row.append(number,content,dot);const wrap=document.createElement('div');wrap.className='slot-item';const more=button('⋯',()=>{selectSlot(s);showSlotMenu(s,more);},'slot-more');more.setAttribute('aria-label','More actions for slot '+s);row.oncontextmenu=e=>{e.preventDefault();selectSlot(s);showSlotMenu(s,more);};row.onkeydown=e=>{if(e.key==='ContextMenu'||(e.shiftKey&&e.key==='F10')){e.preventDefault();selectSlot(s);showSlotMenu(s,more);}};wrap.append(row,more);tree.append(wrap);}}
  function syncInspector(){
    byId('studioInspector').hidden=inspectorCollapsed;shell.classList.toggle('inspector-collapsed',inspectorCollapsed);
    byId('toggleInspector').setAttribute('aria-expanded',String(!inspectorCollapsed));byId('toggleInspector').textContent=inspectorCollapsed?'Show inspector':'Hide inspector';
    for(const name of ['Setup','Hardware','Appearance']){byId('tab'+name).setAttribute('aria-selected',String(inspectorTab===name));byId('panel'+name).hidden=inspectorTab!==name;}
    byId('hardwareEmpty').hidden=!!window.workshopContext;
    byId('tabHardware').disabled=!assigned(active(),selectedSlot);
  }
  function showInspector(name){inspectorCollapsed=false;inspectorTab=name;syncInspector();window.dispatchEvent(new Event('resize'));drawSoon();}
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
    // Wizard-made equipment has its own editor (equipment-wizard.js), not the Pi4 hardware editor.
    if(String(placement.equipment).startsWith('eq-')&&window.openCustomEquipment){window.openCustomEquipment(placement);return;}
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
    for(const [name,color] of colorPresets){const b=button('',()=>set(color));b.style.background=color;b.setAttribute('aria-label',label+': '+name);b.title=name;swatches.append(b);}group.append(swatches);
    // Recent custom colors: a per-browser convenience (not saved with the rack), newest first.
    const recent=document.createElement('div');recent.className='color-swatches color-recent';
    const showRecent=()=>{recent.replaceChildren();const colors=recentColors();recent.hidden=!colors.length;if(!colors.length)return;
      const tag=document.createElement('span');tag.className='color-recent-label';tag.textContent='Recent';recent.append(tag);
      for(const color of colors){const b=button('',()=>set(color));b.style.background=color;b.setAttribute('aria-label',label+': recent '+color);b.title=color;recent.append(b);}};
    // Refresh every visible field's Recent row; fields removed by a re-render drop their listener.
    const refresh=()=>{if(!group.isConnected){window.removeEventListener('recent-colors',refresh);return;}showRecent();};
    window.addEventListener('recent-colors',refresh);
    input.onchange=()=>{rememberColor(input.value);window.dispatchEvent(new Event('recent-colors'));};showRecent();group.append(recent);host.append(group);
  }
  const RECENT_KEY='assembly-workshop-recent-colors';
  function recentColors(){try{const v=JSON.parse(localStorage.getItem(RECENT_KEY)||'[]');return Array.isArray(v)?v.filter(c=>/^#[0-9a-f]{6}$/i.test(c)).slice(0,6):[];}catch(e){return [];}}
  function rememberColor(color){
    color=String(color).toLowerCase();if(!/^#[0-9a-f]{6}$/.test(color)||colorPresets.some(([,c])=>c===color))return;
    try{localStorage.setItem(RECENT_KEY,JSON.stringify([color,...recentColors().filter(c=>c.toLowerCase()!==color)].slice(0,6)));}catch(e){}
  }
  // ---- Click-to-paint rack appearance ----
  // Paint groups map clickable mesh keys to the saved appearance.components keys (logo → appearance.logo_color).
  const paintGroups=[
    ['posts','Posts',['post1','post2','post3','post4','post5']],['extension','Support extensions',['extension']],
    ['beams','Beams',['beam_bottom','beam_top_front','beam_top_rear']],['rails','Side rails',['side_rail']],
    ['panels','Top & bottom panels',['panel_top','panel_bottom']],['sidepanels','Side panels',['panel1','panel2','panel3','panel4','panel5']],
    ['foot','Feet',['foot']],['handle','Handles',['handle']],['logo','Lab Rax logo',[]]];
  const rackThemes=[['Lab Rax','#8b9aa8','#a6e22e'],['Stealth','#2a2f36','#a6e22e'],['Arctic','#e6e8ec','#2f6fd1'],['Workshop orange','#d9822b','#1c1f24'],['Forest','#3f6b4f','#e6e4db']];
  let paintGroup='posts';
  const groupOfKey=key=>key==='beam_top_front-logo'?'logo':key==='beam_top_front-body'?'beams':paintGroups.find(g=>g[2].includes(key))?.[0];
  function groupColor(rack,id){const a=rack.appearance||{};if(id==='logo')return a.logo_color||'#a6e22e';const keys=paintGroups.find(g=>g[0]===id)[2];return keys.map(k=>a.components?.[k]).find(Boolean)||a.color||'#8b9aa8';}
  function setGroupColor(rack,id,v){rack.appearance ||= {};const a=rack.appearance;if(id==='logo')a.logo_color=v;else{a.components ||= {};for(const k of paintGroups.find(g=>g[0]===id)[2])if(v)a.components[k]=v;else delete a.components[k];if(!Object.keys(a.components).length)delete a.components;}markChanged();drawSoon();}
  function renderRackPaint(host,rack){
    const inBuild=new Set(rackFrame(rack.slots,true,rack).parts.map(p=>p.key));
    const groups=paintGroups.filter(g=>g[0]==='logo'||g[2].some(k=>inBuild.has(k)));
    if(!groups.some(g=>g[0]===paintGroup))paintGroup=groups[0][0];
    host.append(paragraph('Click any part of the rack in the 3D view to pick it, then choose a color.','muted'));
    // Themes: one click sets the whole rack + logo and clears per-part overrides.
    host.append(paragraph('THEMES','section-eyebrow'));const themes=document.createElement('div');themes.className='paint-themes';
    for(const [name,body,logo] of rackThemes){const b=button(name,()=>{rack.appearance={...rack.appearance,color:body,logo_color:logo};delete rack.appearance.components;markChanged();drawSoon();renderAppearance();},'paint-theme');b.style.setProperty('--body',body);b.style.setProperty('--logo',logo);themes.append(b);}
    host.append(themes);
    colorField(host,'Whole rack',rack.appearance.color||'#8b9aa8',v=>{rack.appearance.color=v;markChanged();drawSoon();renderPaintList();});
    host.append(paragraph('PARTS','section-eyebrow'));const list=document.createElement('div');list.className='paint-list';host.append(list);
    const editor=document.createElement('div');host.append(editor);
    function renderPaintList(){
      list.replaceChildren();
      for(const [id,title,keys] of groups){const custom=id==='logo'?!!rack.appearance.logo_color:keys.some(k=>rack.appearance.components?.[k]);
        const b=button('',()=>{paintGroup=id;renderPaintList();renderEditor();drawSoon();},'paint-item'+(id===paintGroup?' active':''));
        const sw=document.createElement('i');sw.style.background=groupColor(rack,id);const name=document.createElement('span');name.textContent=title;const tag=document.createElement('small');tag.textContent=custom?'custom':'rack color';
        b.append(sw,name,tag);b.setAttribute('aria-pressed',String(id===paintGroup));list.append(b);}
    }
    function renderEditor(){
      editor.replaceChildren();const title=groups.find(g=>g[0]===paintGroup)[1];
      colorField(editor,title,groupColor(rack,paintGroup),v=>{setGroupColor(rack,paintGroup,v);renderPaintList();});
      editor.append(button(paintGroup==='logo'?'Use default lime':'Use whole-rack color',()=>{if(paintGroup==='logo'){delete rack.appearance.logo_color;markChanged();drawSoon();}else setGroupColor(rack,paintGroup,null);renderPaintList();renderEditor();},'secondary'));
    }
    window.selectPaintGroup=id=>{if(!groups.some(g=>g[0]===id))return;paintGroup=id;renderPaintList();renderEditor();drawSoon();editor.scrollIntoView({block:'nearest'});};
    renderPaintList();renderEditor();
    host.append(button('Reset all rack colors',()=>{rack.appearance={};markChanged();renderAppearance();drawSoon();},'secondary'));
  }
  // Ray-pick the rack part under (x,y) using the renderer's last pick state (same maths as LabRaxStudio.pick).
  function pickRackPart(x,y){
    const st=sceneRenderer?.pickState;if(!st)return null;const ray=st.view.ray(x,y);let best=Infinity,hit=null,logoAt=Infinity;
    const sub=(a,b)=>[a[0]-b[0],a[1]-b[1],a[2]-b[2]],cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
    for(const o of st.objects){if(!groupOfKey(o.key))continue;const R=o.R,q=sub(ray.origin,o.t),rot=v=>[R[0]*v[0]+R[3]*v[1]+R[6]*v[2],R[1]*v[0]+R[4]*v[1]+R[7]*v[2],R[2]*v[0]+R[5]*v[1]+R[8]*v[2]],org=rot(q),dir=rot(ray.direction);
      for(const t of o.mesh.triangles){const a=o.mesh.vertices[t[0]],e1=sub(o.mesh.vertices[t[1]],a),e2=sub(o.mesh.vertices[t[2]],a),p=cross(dir,e2),det=dot(e1,p);if(Math.abs(det)<1e-8)continue;const s=sub(org,a),u=dot(s,p)/det;if(u<0||u>1)continue;const qq=cross(s,e1),v=dot(dir,qq)/det;if(v<0||u+v>1)continue;const d=dot(e2,qq)/det;if(d>0&&d<best){best=d;hit=o;}if(d>0&&o.key==='beam_top_front-logo')logoAt=Math.min(logoAt,d);}}
    // The logo is painted flush with the beam, so a near-tie goes to the logo.
    if(logoAt<best+2)return 'logo';
    return hit?groupOfKey(hit.key):null;
  }
  function renderAppearance(){
    const host=byId('appearanceProperties'),rack=active();if(!host)return;host.replaceChildren();if(!rack||!capable)return;
    rack.appearance ||= {};
    const details=document.createElement('details');details.id='rackAppearance';const summary=document.createElement('summary');summary.textContent='Rack colors';details.append(summary);
    // Colors wait until the post stack / support extension positions are locked in (Setup tab).
    details.open=true;
    if(!rack.layout_locked)details.append(paragraph('Lock in the support extension positions and post segments on the Setup tab before choosing colors.','notice'),button('Go to Setup',()=>showInspector('Setup'),'secondary'));
    else renderRackPaint(details,rack);
    host.append(details);
    const p=assigned(rack,selectedSlot);if(!p)return;p.assembly.appearance ||= {};
    const artDetails=document.createElement('details');artDetails.open=true;artDetails.id='assemblyAppearance';const sum=document.createElement('summary');sum.textContent='Equipment colors & faceplate image';artDetails.append(sum);
    for(const [key,title,defaultColor] of [['equipment','Equipment (Pi reference)','#5b8545'],['tray','Tray','#4d8e6e'],['faceplate','Faceplate','#4e75a3']])colorField(artDetails,title,p.assembly.appearance[key]||defaultColor,v=>{p.assembly.appearance[key]=v;markChanged();applyAssemblyAppearance(p);});
    const fileLabel=document.createElement('label');fileLabel.textContent='Local faceplate image';fileLabel.htmlFor='faceplateImage';const file=document.createElement('input');file.id='faceplateImage';file.type='file';file.accept='image/png,image/jpeg,image/webp';file.onchange=()=>loadArtwork(file,p);artDetails.append(fileLabel,file);
    const art=p.assembly.appearance.artwork;
    if(art){artDetails.append(paragraph(art.name+' · preview only'),button('Fit & center image',()=>{Object.assign(art,{x:.5,y:.5,scale:1});markChanged();applyAssemblyAppearance(p);renderAppearance();},'secondary'),button('Center image',()=>{Object.assign(art,{x:.5,y:.5});markChanged();applyAssemblyAppearance(p);renderAppearance();},'secondary'));for(const [key,title,min,max] of [['x','Image horizontal position',0,1],['y','Image vertical position',0,1],['scale','Image size',.05,1]]){const label=document.createElement('label');label.textContent=title;const input=document.createElement('input');input.type='range';input.min=min;input.max=max;input.step=.01;input.value=art[key];input.setAttribute('aria-label',title);input.oninput=()=>{art[key]=Number(input.value);markChanged();applyAssemblyAppearance(p);};label.append(input);artDetails.append(label);}artDetails.append(button('Remove image',()=>{delete p.assembly.appearance.artwork;markChanged();applyAssemblyAppearance(p);renderAppearance();byId('assemblyAppearance').open=true;},'secondary'));}
    artDetails.append(button('View faceplate front',async()=>{await openAssembly(p);if(window.workshopContext?.id===p.assembly.id)window.dispatchEvent(new Event('assembly-faceplate-front'));},'secondary'),paragraph('Colors and images are visual previews. Save to keep them. The normal STL files have no color or artwork; use "Print in color" below for multi-color files.','notice'));host.append(artDetails);
    if(art)renderFilament(host,p,art);
  }
  // Multi-color faceplate: one STL per filament color (faceplate_color.py). Pi4 faceplate only.
  const filamentPreviews=new Map();let filamentTimer=null;
  function renderFilament(host,p,art){
    const box=document.createElement('details');box.id='filamentColors';box.open=filamentPreviews.has(p.assembly.id);
    const sum=document.createElement('summary');sum.textContent='Print in color (multi-material)';box.append(sum);
    const fil=art.filament||{count:4,style:'inlay',colors:[]};
    const setFil=change=>{art.filament=Object.assign({count:fil.count,style:fil.style,colors:fil.colors||[]},change);markChanged();clearTimeout(filamentTimer);filamentTimer=setTimeout(()=>preview(true),250);};
    box.append(paragraph('Turns the image into a few filament colors and exports one STL per color. Load them all together in your slicer and give each file its own filament. Printed result, fit and strength stay UNKNOWN.','muted'));
    const styleLabel=document.createElement('label');styleLabel.textContent='Style';const style=document.createElement('select');
    for(const [v,t] of [['inlay','Inlay: flush with the face, 0.6 mm deep (print face down)'],['emboss','Raised: 0.6 mm above the face']]){const o=new Option(t,v);o.selected=fil.style===v;style.append(o);}
    style.onchange=()=>setFil({style:style.value});styleLabel.append(style);
    const countLabel=document.createElement('label');countLabel.textContent='Number of filament colors (including the faceplate color)';const count=document.createElement('select');
    for(let n=2;n<=8;n++){const o=new Option(String(n),n);o.selected=fil.count===n;count.append(o);}
    count.onchange=()=>setFil({count:Number(count.value),colors:[]});countLabel.append(count);
    const out=document.createElement('div');out.className='filament-preview';
    box.append(styleLabel,countLabel,button('Preview colors',()=>preview(false),'secondary'),out);
    const exportButton=button('Export color STLs (.zip)',async()=>{
      try{
        if(window.assertWorkshopSaved)window.assertWorkshopSaved();
        if(window.workshopContext?.id!==p.assembly.id)await openAssembly(p);
        exportButton.disabled=true;notify('Building color STLs… this can take a minute for detailed images.');
        const response=await fetch('/api/faceplate-colors/export',{method:'POST',headers:{...projectHeaders(),'Content-Type':'application/json','X-App-Token':token},body:'{}'});
        if(!response.ok){const e=await response.json();throw Error(e.error);}
        const url=URL.createObjectURL(await response.blob()),a=document.createElement('a');a.href=url;a.download='faceplate-colors-'+p.assembly.id.slice(4,12)+'.zip';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
        notify('Color STLs exported (PROPOSED — UNVALIDATED). See README.txt in the zip for which file gets which filament.');
      }catch(e){notify(e.message,true);}finally{exportButton.disabled=false;}
    });
    box.append(exportButton,paragraph('Export uses the saved settings: Save first. Images stay on this computer.','muted'));host.append(box);
    function show(r){
      out.replaceChildren();
      const img=document.createElement('img');img.src=r.preview_png;img.alt='Color preview of the faceplate image';img.style.cssText='width:100%;image-rendering:pixelated;border:1px solid #445;border-radius:4px;';out.append(img);
      out.append(paragraph(`${r.size_mm[0]} × ${r.size_mm[1]} mm on the faceplate front · ${r.style}, ${r.depth_mm} mm`,'muted'));
      r.palette.forEach((hex,i)=>{
        const body=r.bodies.find(b=>b.index===i),merged=r.merged.includes(i);
        const title=i===0?'Faceplate (base) color':'Color '+i+(merged?' — merged':body?` — ${body.area_mm2} mm², ~${body.grams_estimate} g`:' — removed in clean-up');
        const value=hex||(p.assembly.appearance.faceplate||'#4e75a3');
        const row=document.createElement('div');row.className='color-field';
        const label=document.createElement('span');label.textContent=title;
        const pick=document.createElement('input');pick.type='color';pick.value=value;pick.setAttribute('aria-label',title+' color');
        const named=document.createElement('select');named.setAttribute('aria-label',title+' filament');named.append(new Option('Filament…',''));
        for(const [n,h] of r.filaments)named.append(new Option(n,h));
        const set=v=>{const colors=r.palette.map((c,k)=>c||(k===0?(p.assembly.appearance.faceplate||'#4e75a3'):'#808080'));colors[i]=v;setFil({colors});};
        pick.onchange=()=>set(pick.value);named.onchange=()=>{if(named.value)set(named.value);};
        row.append(label,pick,named);out.append(row);
      });
      out.append(paragraph('Tip: give two colors the same filament to merge them.','muted'));
      for(const w of r.warnings)out.append(paragraph(w,'notice'));
      if(!r.exportable)out.append(paragraph('Not exportable yet — see the notes above.','workspace-error'));
    }
    async function preview(quiet){
      try{const r=await api('faceplate-colors/preview',{artwork:art,faceplate:p.assembly.appearance.faceplate});filamentPreviews.set(p.assembly.id,r);if(box.isConnected){box.open=true;show(r);}}
      catch(e){if(!quiet)notify(e.message,true);else out.replaceChildren(paragraph(e.message,'workspace-error'));}
    }
    if(filamentPreviews.has(p.assembly.id))preview(true);
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
    if(!selectedSlot){host.append(paragraph(rack.slots+' slots · '+rack.placements.length+' assigned assemblies'),button('Edit rack settings',()=>openRackDialog(true),'secondary'));appendExtensionControls(host,rack);appendRackStlExport(host,rack);appendReleaseUndo(host,rack);return;}
    const placement=assigned(rack,selectedSlot);
    if(placement){host.append(paragraph((placement.assembly?.name||'Raspberry Pi 4')+' · slots '+placement.slot+'–'+(placement.slot+placement.span-1)),paragraph('Reference allocation. Installed fit, service access and load capacity are UNKNOWN.'),button(String(placement.equipment).startsWith('eq-')?'Edit equipment':'Open assembly',()=>openAssembly(placement),'primary'),button('Slot actions ⋯',e=>showSlotMenu(selectedSlot,e.currentTarget),'secondary'));}
    else{host.append(paragraph('An open slot in your rack. Choose equipment to begin a guided assembly.'),button('Create assembly',startWizard,'primary'));}
    if(placement&&!String(placement.equipment).startsWith('eq-')&&!persistedAssemblyIds.has(placement.assembly.id)){host.querySelector('button.primary').disabled=true;host.append(paragraph('Use Save to keep this allocation before opening its hardware editor.'));}
    appendReleaseUndo(host,rack);
  }
  function editAllocation(placement){
    showInspector('Setup');
    const rack=active(),wizard=byId('mountWizard');wizard.hidden=false;wizard.replaceChildren();wizard.append(paragraph('EDIT SLOT ALLOCATION','section-eyebrow'));
    for(const [id,label,value] of [['allocationStart','Starting slot',placement.slot],['allocationSpan','Number of slots to reserve',placement.span]]){const caption=document.createElement('label');caption.htmlFor=id;caption.textContent=label;const input=document.createElement('input');input.id=id;input.type='number';input.min='1';input.max=String(rack.slots);input.step='1';input.value=String(value);wizard.append(caption,input);}
    wizard.append(paragraph('This edits the logical reservation. It does not move or resize manufacturing meshes or verify rack fit. The independent assembly record is retained.','notice'));
    const error=paragraph('','fail');error.setAttribute('role','alert');wizard.append(error,button('Apply allocation',()=>{try{const current=active();if(current?.id!==rack.id)throw Error('Select the original rack before applying this allocation.');const item=RackLayout.change(current,placement.id,Number(byId('allocationStart').value),Number(byId('allocationSpan').value));selectedSlot=item.slot;wizard.hidden=true;markChanged();setStage('rack');render();notify('Slot allocation updated in the draft. Save to keep it.');}catch(e){error.textContent=e.message;}},'primary'),button('Cancel',()=>{wizard.hidden=true;},'secondary'));
  }
  // Place a wizard-made library item (equipment-wizard.js) into the selected empty slot.
  window.placeLibraryEquipment=function(item){
    if(!capable){notify('Wait for the updated workspace to load.',true);return false;}
    const rack=active();if(!rack||!selectedSlot){notify('Select an empty rack slot first, then click the equipment.',true);return false;}
    const span=item.span||1;if(selectedSlot+span-1>rack.slots){notify(item.name+' needs '+span+' slots; not enough room below slot '+selectedSlot+'.',true);return false;}
    for(let s=selectedSlot;s<selectedSlot+span;s++)if(assigned(rack,s)){notify('That allocation overlaps another assembly.',true);return false;}
    const assembly=newAssembly();assembly.name=item.name;assembly.project.name=item.name;
    rack.placements.push({assembly,id:uid(),equipment:item.id,slot:selectedSlot,span,geometry:'equipment-library',fit:'UNKNOWN'});
    markChanged();renderTree();setStage('rack');renderProperties();
    notify(item.name+' placed in the draft layout. Save to keep it. Rack fit is UNKNOWN.');return true;
  };
  function startWizard(){if(!capable){notify('Wait for the updated workspace to load.',true);return;}showInspector('Setup');const rack=active();if(!rack||!selectedSlot){notify('Select an empty rack slot first.');return;}if(assigned(rack,selectedSlot)){notify('This slot already has an assembly. Select an empty slot.');return;}const wizard=byId('mountWizard');wizard.hidden=false;wizard.replaceChildren();wizard.append(paragraph('CREATE ASSEMBLY · SLOT '+selectedSlot,'section-eyebrow'));const h=document.createElement('h2');h.textContent='Make space for a Pi4';wizard.append(h,paragraph('1 · Equipment'),paragraph('Raspberry Pi 4 · documented tray and faceplate baseline.'),paragraph('2 · Slot allocation'));const label=document.createElement('label');label.htmlFor='allocationSpan';label.textContent='Number of slots to reserve';const input=document.createElement('input');input.id='allocationSpan';input.type='number';input.min='1';input.max=String(rack.slots-selectedSlot+1);input.step='1';input.value='1';wizard.append(label,input,paragraph('3 · Review'),paragraph('This creates an independent assembly, copying the current legacy hardware pins once. Save before opening its editor. It does not build meshes or confirm rack fit.','notice'));const error=paragraph('','fail');error.setAttribute('role','alert');wizard.append(error,button('Confirm slot allocation',()=>{const span=Number(input.value);if(!Number.isInteger(span)||span<1||selectedSlot+span-1>rack.slots){error.textContent='Choose a whole slot count within the rack.';return;}const current=active();if(current?.id!==rack.id){error.textContent='Select the original rack before confirming.';return;}for(let s=selectedSlot;s<selectedSlot+span;s++)if(assigned(current,s)){error.textContent='That allocation overlaps another assembly.';return;}current.placements.push({assembly:newAssembly(),id:uid(),equipment:'pi4',slot:selectedSlot,span,geometry:'pi4-clearance-v2-reference',fit:'UNKNOWN'});markChanged();wizard.hidden=true;renderTree();setStage('rack');renderProperties();notify('Slot allocation added to the draft layout. Save to keep it. No meshes were generated.');},'primary'),button('Cancel',()=>{wizard.hidden=true;},'secondary'));}
  function renderReview(){const rack=active(),host=byId('rackReview');host.replaceChildren();host.append(paragraph('UNKNOWN · Rack installation and strength','review-unknown'));if(!rack){host.append(paragraph('No rack layout selected.'));return;}const missing=['width_mm','depth_mm','pitch_mm'].filter(k=>rack[k]===null);host.append(paragraph(missing.length?'UNKNOWN · '+missing.map(k=>({width_mm:'internal width',depth_mm:'usable depth',pitch_mm:'slot pitch'}[k])).join(', ')+' not specified.':'USER-SUPPLIED · Layout dimensions recorded; physical fit is not verified.'));host.append(paragraph('Slot allocations do not overlap. Wizard equipment is envelope-screened against the nominal rack numbers below; this is not a fit check. Cable and tool clearance are not screened.'));
    const library=window.equipmentLibraryItems?.()||[],screen=window.WorkshopClearance?.screen,labels={ok:'SCREENED OK',tight:'TIGHT',over:'OVER',unknown:'UNKNOWN',reference:'REFERENCE'};
    for(const p of rack.placements){
      const where=(p.assembly?.name||'Pi4')+' · slots '+p.slot+'–'+(p.slot+p.span-1);
      if(!screen){host.append(paragraph(where+' · screening unavailable; rack fit UNKNOWN.'));continue;}
      const r=screen(rack,p,library.find(i=>i.id===p.equipment));
      const box=document.createElement('div');box.className='clearance-result clearance-'+r.level;
      const head=document.createElement('strong');head.textContent=labels[r.level]+' · '+where;box.append(head);
      for(const c of r.checks)box.append(paragraph((c.level==='ok'?'✓ ':c.level==='unknown'?'? ':'⚠ ')+c.text,'clearance-check clearance-'+c.level));
      box.append(paragraph(r.note));host.append(box);
    }}
  function render(){const rack=active();byId('rackChoice').replaceChildren();if(!documentState.racks.length)byId('rackChoice').append(new Option('No rack layout yet',''));for(const r of documentState.racks)byId('rackChoice').append(new Option(r.name,r.id));byId('rackChoice').value=activeId||'';byId('projectTitle').textContent=rack?.name||'Your rack workspace';byId('layoutSaveStatus').textContent=layoutDirty?'Layout changes · unsaved':rack?'Layout saved locally':'No rack selected';updateSaveStatus();byId('rackDimensions').textContent=rack?rack.slots+'U rack · '+(rack.width_mm??208)+' × '+(rack.depth_mm??240)+' mm':'No rack yet';byId('rackScale').textContent='Supplied rack meshes · visual placement';renderTree();renderProperties();renderReview();setStage(stage);}
  function openRackDialog(edit){
    if(!leaveAssembly())return;
    editingId=edit?activeId:null;
    const rack=edit?active():null;
    byId('rackDialogTitle').textContent=edit?'Modular Post Stacking Settings':'Modular Post Stacking';
    byId('rackName').value=rack?.name||'My Lab Rax';
    setSlots(rack?.slots || 5);
    byId('rackSlots').oninput = e => setSlots(e.target.value);
    for(const chip of document.querySelectorAll('.piece-chip')){
      chip.draggable = true;
      chip.onclick = () => setSlots(Number(byId('rackSlots').value) + Number(chip.dataset.u));
      chip.ondragstart = e => { e.dataTransfer.setData('text/plain', chip.dataset.u); e.dataTransfer.effectAllowed = 'copy'; };
    }
    const drop = byId('rackPreviewCanvas');
    drop.ondragover = e => { e.preventDefault(); drop.style.borderColor = '#55a6ff'; };
    drop.ondragleave = () => { drop.style.borderColor = '#3a4a5e'; };
    drop.ondrop = e => { e.preventDefault(); drop.style.borderColor = '#3a4a5e'; const u = Number(e.dataTransfer.getData('text/plain')); if(u) setSlots(Number(byId('rackSlots').value) + u); };
    byId('rackFormError').textContent='';
    byId('rackDialog').showModal();
    drawPreviewSoon();
  }
  // Dialog-only preview: separate renderer so the main viewport's cache is untouched.
  const POSTS = 4, HOLES_PER_U = 3;
  let previewRenderer = null, previewPending = false;
  function setSlots(n){
    const slots = Math.min(14, Math.max(1, Math.round(Number(n)) || 1));
    byId('rackSlots').value = slots;
    byId('slotCountDisplay').textContent = slots + 'U';
    renderBom(slots);
    drawPreviewSoon();
  }
  function renderBom(slots){
    // Same default stack the 3D view uses: posts plus one 1U support extension per side at each joint.
    const levels = defaultLevels(slots), pieces = {}, postU = levels.reduce((a, b) => a + b, 0), joints = levels.length - 1;
    for(const u of levels) pieces[u] = (pieces[u] || 0) + 1;
    const holes = postU * HOLES_PER_U * POSTS, host = byId('rackBom');
    host.replaceChildren();
    for(const u of Object.keys(pieces).sort((a, b) => b - a)) host.append(paragraph(pieces[u] * POSTS + ' × ' + u + 'U post segment (' + pieces[u] + ' per post × ' + POSTS + ' posts)'));
    if(joints) host.append(paragraph(joints * 2 + ' × 1U support extension (' + joints + ' per side × 2 sides)'));
    host.append(paragraph(holes + ' × M6 DIN 7380 buttonhead bolt'), paragraph(holes + ' × M6 brass heat-set insert'), paragraph(HOLES_PER_U + ' holes per U per post · ' + postU * HOLES_PER_U + ' per post (extension mounting hardware not counted)'));
  }
  function drawPreviewSoon(){ if(!previewPending){ previewPending = true; requestAnimationFrame(drawRackPreview); } }
  function drawRackPreview(){
    previewPending = false;
    const c = byId('rackPreviewCanvas');
    if(!byId('rackDialog').open || !c) return;
    const w = c.clientWidth || 280, h = c.clientHeight || 260, dpr = Math.min(window.devicePixelRatio || 1, 2);
    c.width = Math.round(w * dpr); c.height = Math.round(h * dpr);
    const ctx = c.getContext('2d'); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = '#151c26'; ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#aab9cb'; ctx.font = '13px system-ui';
    if(!sourceMeshes){ ctx.fillText(sourceError || 'Loading frame meshes…', 12, 22); return; }
    try{
      if(!previewRenderer || previewRenderer.restoreRequired){ previewRenderer?.dispose(); previewRenderer = new LabRaxStudio.Renderer(); previewRenderer.invalidated = drawPreviewSoon; }
      previewRenderer.shadows = false; previewRenderer.ambientOcclusion = false;
      const slots = Number(byId('rackSlots').value), scene = rackFrame(slots, false), box = LabRaxScene.bounds(scene, sourceMeshes);
      const view = LabRaxStudio.camera(box, -.5, .3, w, h, 1, true);
      ctx.drawImage(previewRenderer.draw(scene, sourceMeshes, view, c.width, c.height, {slots, placements: []}, null), 0, 0, w, h);
    }catch(e){ ctx.fillStyle = '#efb6a5'; ctx.fillText(e.message, 12, 22); }
  }
  byId('rackDialog').addEventListener('close', () => { previewRenderer?.dispose(); previewRenderer = null; });
  byId('rackForm').onsubmit=e=>{
    e.preventDefault();
    const old=documentState.racks.find(r=>r.id===editingId);
    const slots = Number(byId('rackSlots').value);
    const next={
      id:old?.id||uid(),
      name:byId('rackName').value.trim()||'My Lab Rax',
      slots: slots,
      width_mm: 208.0,
      depth_mm: 240.0,
      pitch_mm: 44.45,
      appearance:old?.appearance||{},
      placements:old?.placements||[]
    };
    // Height unchanged keeps the post layout (and its lock); a new height must be re-locked.
    if(old&&old.slots===slots){if(old.post_levels)next.post_levels=old.post_levels;if(old.layout_locked)next.layout_locked=true;}
    if(next.placements.some(p=>p.slot+p.span-1>next.slots)){
      byId('rackFormError').textContent='Existing assemblies extend beyond ' + next.slots + 'U. Keep enough slots or release them first.';
      return;
    }
    if(old) documentState.racks[documentState.racks.indexOf(old)]=next;
    else documentState.racks.push(next);
    activeId=next.id; selectedSlot=null; markChanged();
    byId('rackDialog').close(); stage='rack'; render();
    notify('Modular rack layout updated in draft. Save to keep it.');
  };
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

  // Save history: earlier saved layouts (rack-history/) restore into the draft only; Save keeps them.
  async function getJson(path){const r=await fetch('/api/'+path);const out=await r.json();if(!r.ok)throw Error(out.error||'Request failed');return out;}
  async function openHistory(){
    const rack=active();if(!rack){notify('Select a rack first.',true);return;}
    let dialog=byId('historyDialog');
    if(!dialog){dialog=document.createElement('dialog');dialog.id='historyDialog';dialog.className='history-dialog';document.body.append(dialog);}
    const list=document.createElement('div');list.className='history-list';list.append(paragraph('Loading saved versions…'));
    const close=button('✕',()=>dialog.close(),'subtle');close.setAttribute('aria-label','Close history');
    const heading=document.createElement('div');heading.className='dialog-heading';
    const eyebrow=document.createElement('span');eyebrow.className='section-eyebrow';eyebrow.textContent='SAVE HISTORY · '+rack.name.toUpperCase();heading.append(eyebrow,close);
    dialog.replaceChildren(heading,paragraph('Each entry is this rack as it was before a later Save. Restoring puts it in your draft only: nothing changes on disk until you click Save, and reloading discards it. Assemblies keep their latest saved hardware. Fit stays UNKNOWN.'),list);
    dialog.showModal();
    try{
      const entries=(await getJson('rack-history')).filter(e=>e.unreadable||e.racks.some(r=>r.id===rack.id));
      list.replaceChildren();
      if(!entries.length){list.append(paragraph('No earlier saved versions of this rack yet. Each Save keeps the previous version here.'));return;}
      for(const entry of entries){
        const row=document.createElement('div');row.className='history-entry';
        const when=new Date(entry.replaced_ns/1e6).toLocaleString();
        if(entry.unreadable){row.append(paragraph('Replaced '+when+' · could not be read (preserved on disk).'));list.append(row);continue;}
        const r=entry.racks.find(x=>x.id===rack.id);
        const title=document.createElement('strong');title.textContent='Replaced '+when;
        const detail=paragraph(r.name+' · '+r.slots+' slots · '+(r.allocations.length?r.allocations.map(a=>'slot '+a.slot+(a.span>1?'–'+(a.slot+a.span-1):'')+': '+a.name).join(', '):'no assemblies'));
        row.append(title,detail,button('Restore as draft',()=>restoreVersion(entry.generation,rack.id,when),'secondary'));
        list.append(row);
      }
    }catch(e){list.replaceChildren(paragraph('Could not load history: '+e.message,'workspace-error'));}
  }
  async function restoreVersion(generation,rackId,when){
    if(!leaveAssembly())return;
    if((layoutDirty||dirty)&&!confirm('Replace your unsaved changes to this rack with the version replaced '+when+'?'))return;
    try{
      const restored=await getJson('rack-history/restore?generation='+encodeURIComponent(generation)+'&rack='+encodeURIComponent(rackId));
      const index=documentState.racks.findIndex(r=>r.id===rackId);
      if(index<0)documentState.racks.push(restored);else documentState.racks[index]=restored;
      activeId=restored.id;selectedSlot=null;stage='rack';markChanged();render();byId('historyDialog').close();
      notify('Restored the version replaced '+when+' as an unsaved draft. Click Save to keep it, or reload to discard it.');
    }catch(e){notify('Restore failed: '+e.message,true);}
  }
  byId('rackHistory').onclick=openHistory;
  window.addEventListener('equipment-library',()=>renderReview());
  window.activeRackNumbers=()=>{const r=active();return r?{width_mm:r.width_mm,depth_mm:r.depth_mm,pitch_mm:r.pitch_mm}:null;};

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
  let showRackPanels=false, perspectiveCamera=true, studioQuality=true, showRearLabels=false;
  // Post stack, bottom-up U sizes. Each joint between posts is a 1U support extension that takes up
  // its own unit of height, so posts + (joints × 1U) = rack slots. e.g. 9U = 3U post + 1U ext + 5U post.
  const stackHeight=levels=>levels.reduce((a,b)=>a+b,0)+levels.length-1;
  function defaultLevels(slots){
    // Fewest posts that fit; every post gets 1U, then fill from the top post down to 5U (short post ends up at the bottom).
    const n=Math.ceil((slots+1)/6),out=Array(n).fill(1);let left=slots-(n-1)-n;
    for(let i=n-1;i>=0&&left>0;i--){const add=Math.min(4,left);out[i]+=add;left-=add;}
    return out;
  }
  function sideLevels(rack,side){const s=rack?.post_levels?.[side];return Array.isArray(s)&&s.length&&stackHeight(s)===rack.slots?s:defaultLevels(rack?.slots||1);}
  // Frame with per-side post stacks plus a 1U support extension at every joint (rack-scene.js leaves it out).
  function rackFrame(slots,panels,rack){
    const scene=LabRaxScene.frame(slots,panels),U=LabRaxScene.U,PX=125.98,DEPTH=240;
    const I=[1,0,0,0,1,0,0,0,1],RX=[1,0,0,0,-1,0,0,0,-1],RY=[-1,0,0,0,1,0,0,0,-1],RZ=[-1,0,0,0,-1,0,0,0,1],R90=[0,-1,0,1,0,0,0,0,1];
    scene.parts=scene.parts.filter(p=>!/^post\d$/.test(p.key)&&p.kind!=='side');
    const sides={left:[[I,-PX,17.5],[RX,-PX,DEPTH-17.5]],right:[[RY,PX,17.5],[RZ,PX,DEPTH-17.5]]};
    for(const side of ['left','right']){
      const levels=rack?sideLevels(rack,side):defaultLevels(slots),x=side==='left'?-PX:PX;let z=0;
      levels.forEach((u,i)=>{const middle=z+u*U/2;
        for(const [R,px,py] of sides[side])scene.parts.push({key:'post'+u,R,t:[px,py,middle],kind:'frame'});
        if(panels)scene.parts.push({key:'panel'+u,R:R90,t:[side==='left'?-138.48:138.48,120,middle],kind:'side'});
        z+=u*U;
        // The extension fills the next 1U; its end tabs reach into the pockets of the posts either side.
        if(i<levels.length-1){if(sourceMeshes?.extension)scene.parts.push({key:'extension',R:side==='left'?I:RY,t:[x,120,z+U/2],kind:'frame',source:[2,'1']});z+=U;}
      });
    }
    return scene;
  }
  // Rack frame STL export: count every frame part this layout uses and ask the server for the source meshes.
  const RACK_PART_SOURCES={post1:[0,'1'],post2:[0,'9'],post3:[0,'17'],post4:[0,'24'],post5:[0,'31'],panel1:[0,'6'],panel2:[0,'14'],panel3:[0,'22'],panel4:[0,'29'],panel5:[0,'36'],beam_bottom:[1,'20'],beam_top_front:[1,'23'],beam_top_rear:[1,'18'],side_rail:[1,'28'],panel_bottom:[1,'13'],panel_top:[1,'11'],foot:[1,'6'],handle:[1,'25'],extension:[2,'1']};
  async function downloadRackStl(rack,panels){
    const counts={};for(const p of rackFrame(rack.slots,panels,rack).parts)if(RACK_PART_SOURCES[p.key])counts[p.key]=(counts[p.key]||0)+1;
    if(!counts.extension){const joints=sideLevels(rack,'left').length-1+sideLevels(rack,'right').length-1;if(joints>0)counts.extension=joints;}
    const parts=Object.entries(counts).map(([key,count])=>({ref:RACK_PART_SOURCES[key][0],id:RACK_PART_SOURCES[key][1],count,label:key}));
    const r=await fetch('/api/rack-stl',{method:'POST',headers:{'Content-Type':'application/json','X-App-Token':token},body:JSON.stringify({rack:rack.name,parts})});
    if(!r.ok)throw Error((await r.json()).error||'Rack STL export failed');
    const url=URL.createObjectURL(await r.blob()),a=document.createElement('a');a.href=url;a.download=(rack.name||'lab-rax').replace(/[^\w-]+/g,'_')+'-frame-stl.zip';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  function appendRackStlExport(host,rack){
    host.append(paragraph('PRINT THE RACK','section-eyebrow'),paragraph('Download STL files for every frame part this layout uses, with a parts list showing how many of each to print. These are the original Lab Rax designer’s parts, for your own use only.'));
    const panels=document.createElement('label');const cb=document.createElement('input');cb.type='checkbox';cb.checked=true;panels.append(cb,' Include side panels');host.append(panels);
    host.append(button('Download rack frame STLs',()=>downloadRackStl(rack,cb.checked).then(()=>notify('Rack frame STLs downloaded. Fit and strength remain UNKNOWN.')).catch(e=>notify(e.message,true)),'secondary'));
  }
  function appendExtensionControls(host,rack){
    const locked=!!rack.layout_locked;
    host.append(paragraph('POST LAYOUT','section-eyebrow'),paragraph(locked?'Locked · post segments and support extensions are fixed. Colors are unlocked.':'Set the support extensions, then lock the layout to choose colors.',locked?'':'notice'));
    host.append(button(locked?'Unlock post layout':'Lock in post layout',()=>{rack.layout_locked=!locked;markChanged();renderProperties();renderAppearance();},locked?'secondary':'primary'));
    for(const side of ['left','right']){
      const levels=sideLevels(rack,side);if(levels.length<2)continue;
      host.append(paragraph((side==='left'?'LEFT':'RIGHT')+' SUPPORT EXTENSION','section-eyebrow'),paragraph('Stack (top → bottom): '+[...levels].reverse().map(u=>u+'U post').join(' + 1U extension + ')));
      for(let j=0;j<levels.length-1;j++){
        const row=document.createElement('div');row.style.cssText='display:flex;gap:6px;align-items:center;margin-bottom:6px';
        const label=document.createElement('span');label.textContent='Extension '+(levels.length-1>1?j+1+' ':'')+'· at U'+String(rack.slots-levels.slice(0,j+1).reduce((a,b)=>a+b,0)-j).padStart(2,'0');label.style.flex='1';
        const up=button('▲ Up',()=>moveExtension(side,j,1),'secondary'),down=button('▼ Down',()=>moveExtension(side,j,-1),'secondary');up.disabled=down.disabled=locked;
        row.append(label,up,down);host.append(row);
      }
    }
  }
  // Move the support extension at joint j on one side by ±1U (the segments either side grow/shrink).
  function moveExtension(side,j,dir){
    const rack=active();if(!rack||rack.layout_locked)return;const levels=[...sideLevels(rack,side)];
    const below=levels[j]+dir,above=levels[j+1]-dir;
    if(below<1||below>5||above<1||above>5){notify('A post segment must stay between 1U and 5U.',true);return;}
    levels[j]=below;levels[j+1]=above;rack.post_levels={left:sideLevels(rack,'left'),right:sideLevels(rack,'right'),[side]:levels};
    sceneCacheKey='';markChanged();drawSoon();renderProperties();
  }
  function drawSoon(){if(!pending){pending=true;requestAnimationFrame(drawRack);}}
  function drawRack(){
    pending=false;if(byId('rackView').hidden||!rackContext)return;
    const w=Math.max(280,rackCanvas.clientWidth),h=Math.max(350,rackCanvas.clientHeight),dpr=Math.min(window.devicePixelRatio||1,2);
    rackCanvas.width=Math.round(w*dpr);rackCanvas.height=Math.round(h*dpr);
    const ctx=rackContext;ctx.setTransform(dpr,0,0,dpr,0,0);ctx.fillStyle='#151c26';ctx.fillRect(0,0,w,h);clickRegions=[];
    const rack=active();
    if(!rack||!sourceMeshes||!sceneRenderer){ctx.fillStyle='#aab9cb';ctx.font='15px system-ui';ctx.textAlign='center';ctx.fillText(!rack?'Create a rack layout to begin':sourceError||'Loading your Lab Rax enclosure meshes…',w/2,h/2);return;}
    const key=rack.slots+':'+showRackPanels+':'+sideLevels(rack,'left')+'|'+sideLevels(rack,'right')+':'+!!sourceMeshes.extension;
    if(sceneCacheKey!==key){const scene=rackFrame(rack.slots,showRackPanels,rack);sceneCache={scene,box:LabRaxScene.bounds(scene,sourceMeshes)};sceneCacheKey=key;}
    // Highlight the paint group being edited (renderer copies part.selected into its uSelected tint).
    const paintKeys=inspectorTab==='Appearance'&&rack.layout_locked?(paintGroup==='logo'?['beam_top_front']:paintGroups.find(g=>g[0]===paintGroup)?.[2]||[]):[];
    for(const p of sceneCache.scene.parts)p.selected=paintKeys.includes(p.key);
    const {scene,box}=sceneCache,view=LabRaxStudio.camera(box,yaw,pitch,w,h,zoom,perspectiveCamera),project=view.project;
    try {
    if(sceneRenderer.restoreRequired){sceneRenderer.dispose();sceneRenderer=new LabRaxStudio.Renderer();sceneRenderer.invalidated=drawSoon;}
    sceneRenderer.shadows=studioQuality&&sceneRenderer.shadowSupported;sceneRenderer.ambientOcclusion=studioQuality;
    ctx.drawImage(sceneRenderer.draw(scene,sourceMeshes,view,Math.round(w*dpr),Math.round(h*dpr),rack,selectedSlot),0,0,w,h);
    } catch(e) {sourceError=e.message;ctx.fillStyle='#efb6a5';ctx.fillText(sourceError,24,36);return;}
    for(let slot=1;slot<=rack.slots;slot++){
      const z=(rack.slots-slot)*LabRaxScene.U,points=[[-104,-3,z+1],[104,-3,z+1],[104,-3,z+LabRaxScene.U-1],[-104,-3,z+LabRaxScene.U-1]].map(project),selected=slot===selectedSlot,placement=assigned(rack,slot);
      clickRegions.push({slot,p:points});
      // "Printed" on each post face: centred on the unit's top post hole (EIA 6.35/22.225/38.1; 36.902 is the faceplate slot, not the hole), outboard of the faceplate (|X| > 125.5).
      // Front left/right always; rear posts only when toggled. Rear text runs along -X so it reads correctly from behind.
      const rearY=box.hi[1]-(-3.2-box.lo[1]),faces=[[-133,-3.2,1],[133,-3.2,1]];
      if(showRearLabels)faces.push([133,rearY,-1],[-133,rearY,-1]);
      for(const [fx,fy,dir] of faces){
        const at=[fx,fy,z+38.1],o=project(at),ax=project([at[0]+dir,at[1],at[2]]),az=project([at[0],at[1],at[2]+1]);
        // Skip when this post face is turned away from the camera.
        if((ax[0]-o[0])*(az[1]-o[1])-(ax[1]-o[1])*(az[0]-o[0])>=0)continue;
        ctx.save();ctx.transform(ax[0]-o[0],ax[1]-o[1],o[0]-az[0],o[1]-az[1],o[0],o[1]);
        // Alphabetic baseline + half cap height (~0.7em) centres the glyphs on the hole.
        ctx.textAlign='center';ctx.textBaseline='alphabetic';ctx.font='700 5px ui-monospace,monospace';ctx.fillStyle=selected?'#1f6fd1':placement?'#1d7a5c':'#3a4654';ctx.globalAlpha=.85;
        ctx.fillText('U'+String(slot).padStart(2,'0'),0,1.75);ctx.restore();
      }
    }
    ctx.textAlign='left';rackCanvas.dataset.preview='source-mesh';rackCanvas.dataset.parts=String(scene.parts.length);rackCanvas.dataset.triangles=String(sceneRenderer.stats?.triangles||0);rackCanvas.dataset.quality=studioQuality?'studio':'fast';
    byId('rackScale').textContent=(perspectiveCamera?'Perspective':'Orthographic')+' · depth-tested · '+(sceneRenderer.stats?.triangles||0).toLocaleString()+' triangles';
  }
  try{sceneRenderer=new LabRaxStudio.Renderer();sceneRenderer.invalidated=drawSoon;LabRaxScene.load(fetch).then(async meshes=>{
    // LabRaxScene.load skips the support extension; fetch it here so rackFrame() can place it.
    try{const r=await fetch('/rack-references/component_2_1.json');if(r.ok)meshes.extension=await r.json();}catch(e){}
    sourceMeshes=meshes;sceneCacheKey='';drawSoon();drawPreviewSoon();}).catch(e=>{sourceError=e.message;drawSoon();});}catch(e){sourceError=e.message;}
  byId('frontRackView').onclick=()=>{perspectiveCamera=false;yaw=0;pitch=0;zoom=1;setViewButtons(true);drawSoon();};
  byId('renderQuality').onclick=()=>{studioQuality=!studioQuality;byId('renderQuality').setAttribute('aria-pressed',String(studioQuality));drawSoon();};
  byId('toggleRearLabels').onclick=()=>{showRearLabels=!showRearLabels;byId('toggleRearLabels').setAttribute('aria-pressed',String(showRearLabels));drawSoon();};
  byId('toggleRackPanels').onclick=()=>{showRackPanels=!showRackPanels;byId('toggleRackPanels').setAttribute('aria-pressed',String(showRackPanels));drawSoon();};
  rackCanvas.addEventListener('wheel',e=>{e.preventDefault();zoom=Math.max(.5,Math.min(2.5,zoom*Math.exp(-e.deltaY*.001)));drawSoon();},{passive:false});
  rackCanvas.onpointerdown=e=>{drag={x:e.clientX,y:e.clientY,startX:e.clientX,startY:e.clientY,moved:false};rackCanvas.setPointerCapture(e.pointerId);};
  rackCanvas.onpointermove=e=>{if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;drag.moved=drag.moved||Math.hypot(e.clientX-drag.startX,e.clientY-drag.startY)>4;if(drag.moved&&!perspectiveCamera){perspectiveCamera=true;setViewButtons(false);}yaw+=dx*.006;pitch=Math.max(-1.1,Math.min(1.1,pitch+dy*.006));drag.x=e.clientX;drag.y=e.clientY;drawSoon();};
  rackCanvas.onpointerup=e=>{
    // In the Appearance tab (layout locked) a click picks a part to paint instead of a slot.
    if(drag&&!drag.moved&&inspectorTab==='Appearance'&&active()?.layout_locked){const rect=rackCanvas.getBoundingClientRect(),group=pickRackPart(e.clientX-rect.left,e.clientY-rect.top);if(group)window.selectPaintGroup?.(group);drag=null;return;}
    if(drag&&!drag.moved){const rect=rackCanvas.getBoundingClientRect(),slot=sceneRenderer?.pick(e.clientX-rect.left,e.clientY-rect.top);if(slot)selectSlot(slot);}
    drag=null;
  };rackCanvas.onpointercancel=()=>{drag=null;};
  rackCanvas.onkeydown=e=>{if(e.key==='ArrowLeft')yaw-=.12;else if(e.key==='ArrowRight')yaw+=.12;else if(e.key==='ArrowUp')pitch=Math.min(1.1,pitch+.12);else if(e.key==='ArrowDown')pitch=Math.max(-1.1,pitch-.12);else return;e.preventDefault();drawSoon();};
  const setViewButtons=front=>{byId('frontRackView').setAttribute('aria-pressed',String(front));byId('resetRackView').setAttribute('aria-pressed',String(!front));};
  byId('resetRackView').onclick=()=>{perspectiveCamera=true;yaw=-.48;pitch=.24;zoom=1;setViewButtons(false);drawSoon();};new ResizeObserver(drawSoon).observe(rackCanvas);
  Promise.all([api('workspace-capabilities'),api('rack-workspace'),api('project')]).then(([caps,data,template])=>{if(!caps.independent_assemblies||caps.version!==2||caps.studio_save_version!==1)throw Error('Restart the app server to enable this updated interface.');capable=true;byId('rackHistory').hidden=!caps.save_history;legacyTemplate=template;documentState=data;persistedAssemblyIds=new Set(data.racks.flatMap(r=>r.placements.map(p=>p.assembly.id)));activeId=data.racks[0]?.id||null;render();if(!activeId)dashboard();}).catch(e=>{notify('Rack layouts unavailable: '+e.message,true);byId('saveLayout').disabled=true;});
})();
