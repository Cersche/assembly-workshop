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
  const roadmap=document.querySelector('[aria-label="Project status"]');
  const message=byId('message');
  const shell=document.createElement('div');shell.id='studio';
  shell.innerHTML=`
    <header class="studio-header"><button id="homeStudio" class="brand" aria-label="Project dashboard"><span class="brand-mark">AW</span><span>Assembly Workshop<small>LAB RAX STUDIO</small></span></button><span class="header-divider"></span><span id="projectTitle">Your rack workspace</span><span id="layoutSaveStatus" role="status">No rack selected</span><button id="saveLayout" class="primary">Save</button><button id="shortcutHelp" class="icon-button" aria-label="Keyboard shortcuts">?</button></header>
    <nav class="studio-nav" aria-label="Workspace"><span class="local-label"><i></i> LOCAL WORKSPACE</span><div class="stage-tabs"><button data-stage="rack" aria-pressed="true">01 <span>Rack</span></button><button data-stage="assemble" aria-pressed="false">02 <span>Assemble</span></button><button data-stage="review" aria-pressed="false">03 <span>Review</span></button><button data-stage="prepare" aria-pressed="false">04 <span>Prepare</span></button></div><div class="studio-view-actions"><button id="configureRack" class="subtle">Rack settings</button><button id="rackHistory" class="subtle" hidden>History</button><button id="toggleInspector" class="subtle" aria-expanded="true" aria-controls="studioInspector">Hide inspector</button></div></nav>
    <div class="studio-columns"><aside class="studio-left"><details id="racksSection" class="library-section" open><summary>Racks & slots</summary><div class="panel-heading"><span>PROJECT</span><button id="newRack" class="subtle" aria-label="New rack">＋</button></div><label class="sr-only" for="rackChoice">Rack layout</label><select id="rackChoice"></select><div id="explorerPane"><div id="rackTree"></div><p class="sidebar-hint">Select a slot to place equipment.<br>Slot 1 starts at the top.</p></div></details><details id="equipmentSection" class="library-section"><summary>Equipment</summary><div id="equipmentPane"></div></details><details id="hardwareSection" class="library-section hardware-drawer"><summary>Hardware</summary><div id="hardwarePane"></div></details></aside>
    <main class="studio-center"><div class="viewport-heading"><div><p class="section-eyebrow" id="contextEyebrow">RACK DESIGN</p><h1 id="contextTitle">Build your workspace</h1></div><span id="contextBadge" class="studio-badge">Layout planning</span></div><section id="rackView"><div class="rack-toolbar"><span id="rackDimensions" class="tb-summary">No rack yet</span><span class="tb-group" role="group" aria-label="Camera"><span class="tb-label">View</span><button id="resetRackView" class="tb-seg" aria-pressed="true" title="Angled 3D view you can orbit">3D</button><button id="frontRackView" class="tb-seg" aria-pressed="false" title="Straight-on front view">Front</button><button id="rearRackView" class="tb-seg" aria-pressed="false" title="Straight-on rear view, looking at the back of the rack">Rear</button></span><span class="tb-group" role="group" aria-label="Show"><span class="tb-label">Show</span><button id="toggleRackPanels" class="tb-toggle" aria-pressed="false">Side panels</button><button id="toggleRearLabels" class="tb-toggle" aria-pressed="false">Back labels</button><button id="toggleCablesView" class="tb-toggle" aria-pressed="false" title="Hide the panels and see through the frame to the equipment, ports and cable guides">Cables</button><button id="toggleCableRuns" class="tb-toggle" aria-pressed="false" title="Show cable runs in the normal views (they always show in Cables mode and the Rear view)">Cable runs</button></span><span class="tb-group"><button id="renderQuality" class="tb-toggle" aria-pressed="true" title="Soft shadows and shading. Turn off if the view feels slow.">Shadows</button></span></div><canvas id="rackCanvas" tabindex="0" aria-label="Lab Rax source meshes. Left-drag orbits, right-drag pans, scroll zooms at the cursor, Z fits; select a slot in Explorer."></canvas><div class="viewport-caption"><span><i class="axis-x">X</i> <i class="axis-y">Y</i> <i class="axis-z">Z</i> Left-drag orbit · right-drag pan · scroll zoom · Z fit · click a slot</span><span id="rackScale">Schematic · not manufacturing geometry</span></div></section><div id="assemblyView" hidden></div><div class="context-strip"><span id="selectionSummary">No slot selected</span><button id="backToRack" class="subtle">View rack</button></div><section id="reviewView" hidden><div class="section-heading"><h2>Design review</h2><span class="studio-badge">Evidence and limits</span></div><div id="rackReview"></div><div id="jointReview"></div></section><section id="prepareView" hidden><div class="section-heading"><h2>Prepare & export</h2><span class="studio-badge">STL delivery</span></div><p class="notice">Use Place on tray to generate this equipment’s proposed tray and faceplate STLs. Rack frames have a separate export. Physical rack fit and strength remain UNKNOWN.</p><div id="exportTools"></div></section><div id="workspaceMessage" role="status" aria-live="polite"></div></main>
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
    <dialog id="dashboardDialog"><div class="dialog-heading"><span class="section-eyebrow">YOUR WORKSHOP</span><button id="closeDashboard" class="subtle" aria-label="Close dashboard">✕</button></div><h2>Start with the rack.<br>Make room for your ideas.</h2><p class="muted">Plan the space, place your equipment, then work on the assembly.</p><div class="dashboard-grid"><div><h3>Start a project</h3><button id="dashboardNew" class="template-card"><span class="template-icon">▥</span><strong>Custom Lab Rax layout</strong><small>Choose slots and reference dimensions</small></button></div><div><h3>Recent local layouts</h3><div id="recentRacks"></div></div></div><p class="notice">Your equipment library, saved hardware selections and immutable meshes remain available. A rack layout is saved separately from that project.</p></dialog>
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
  let capable=false,assemblyTemplate=null,persistedAssemblyIds=new Set(),openingAssembly=false,artworkRequests=new Map();
  window.workshopContext=null;
  let inspectorTab='Setup',inspectorCollapsed=false,artworkPending=0;
  let yaw=-.48,pitch=.24,zoom=1,panX=0,panY=0,clickRegions=[],pending=false;
  let sourceMeshes=null,sourceError=null,sceneRenderer=null,sceneCache=null,sceneCacheKey='';
  const rackCanvas=byId('rackCanvas'),rackContext=rackCanvas.getContext('2d');
  const active=()=>documentState.racks.find(r=>r.id===activeId);
  const assigned=(rack,slot)=>rack?.placements.find(p=>slot>=p.slot&&slot<p.slot+p.span);
  const uid=()=>crypto.randomUUID();
  function notify(value,error=false){byId('undoApply')?.remove();byId('workspaceMessage').classList.toggle('workspace-error',error);byId('message').textContent=value;}
  function updateSaveStatus(){byId('layoutSaveStatus').textContent=(layoutDirty||dirty)?'Unsaved changes':active()?'Saved locally':'No rack selected';byId('saveLayout').disabled=!capable||savingLayout||!(layoutDirty||dirty);window.labRaxSheetState?.();}
  function markChanged(){layoutDirty=true;const rack=active();if(rack)window.labRaxCableUpkeep?.(rack);updateSaveStatus();drawSoon();}
  window.addEventListener('workshop-dirty',updateSaveStatus);
  function button(label,fn,cls=''){const e=document.createElement('button');e.type='button';e.textContent=label;e.className=cls;e.onclick=fn;return e;}
  function paragraph(value,cls='muted'){const e=document.createElement('p');e.textContent=value;e.className=cls;return e;}
  function setStage(next){if(next==='assemble'&&!window.workshopContext){const p=assigned(active(),selectedSlot);if(p){openAssembly(p);return;}notify('Select an allocated slot and open its saved assembly first.');next='rack';}stage=next;byId('jointProperties').open=stage==='assemble';shell.dataset.stage=stage;document.querySelector('.studio-center').scrollTop=0;for(const e of document.querySelectorAll('[data-stage]'))e.setAttribute('aria-pressed',String(e.dataset.stage===stage));byId('rackView').hidden=stage==='assemble';byId('assemblyView').hidden=stage!=='assemble';byId('reviewView').hidden=stage!=='review';byId('prepareView').hidden=stage!=='prepare';byId('contextEyebrow').textContent=stage==='assemble'?'ASSEMBLY INSPECTION':'RACK DESIGN';byId('contextTitle').textContent=active()?.name||'Build your workspace';byId('contextBadge').textContent=stage==='assemble'?'Assembly':'Rack preview';byId('jointProperties').hidden=!window.workshopContext;byId('exportTools').hidden=!window.workshopContext;byId('jointReview').hidden=!window.workshopContext;if(stage==='assemble'){window.dispatchEvent(new Event('resize'));}drawSoon();renderReview();}
  function selectSlot(slot){if(selectedSlot===slot)return;if(!leaveAssembly())return;selectedSlot=slot;selectedGuide=null;selectedPort=null;placingPort=null;clearCableSelection();byId('mountWizard').hidden=true;inspectorTab='Setup';setStage('rack');renderTree();renderProperties();drawSoon();}
  function renderTree(){const rack=active(),tree=byId('rackTree');tree.replaceChildren();if(!rack){tree.append(paragraph('Create a rack to begin.'));return;}tree.append(paragraph(rack.slots+' SLOTS · '+rack.placements.length+(rack.placements.length===1?' ASSEMBLY':' ASSEMBLIES'),'section-eyebrow'));for(let s=1;s<=rack.slots;s++){const item=assigned(rack,s);const row=button('',()=>selectSlot(s),'slot-row'+(s===selectedSlot?' selected':''));row.setAttribute('aria-label','Slot '+s+(item?' · '+(item.assembly?.name||'Untitled assembly'):' · Empty'));row.setAttribute('aria-pressed',String(s===selectedSlot));const number=document.createElement('span');number.className='slot-number';number.textContent=String(s).padStart(2,'0');const content=document.createElement('span');const title=document.createElement('strong');title.textContent=item?(item.assembly?.name||'Untitled assembly'):'Empty slot';content.append(title);const sub=document.createElement('small');sub.textContent=item?'Fit UNKNOWN':'Available';content.append(sub);const dot=document.createElement('i');dot.className=item?'occupied-dot':'empty-dot';row.append(number,content,dot);const wrap=document.createElement('div');wrap.className='slot-item';const more=button('⋯',()=>{selectSlot(s);showSlotMenu(s,more);},'slot-more');more.setAttribute('aria-label','More actions for slot '+s);row.oncontextmenu=e=>{e.preventDefault();selectSlot(s);showSlotMenu(s,more);};row.onkeydown=e=>{if(e.key==='ContextMenu'||(e.shiftKey&&e.key==='F10')){e.preventDefault();selectSlot(s);showSlotMenu(s,more);}};wrap.append(row,more);tree.append(wrap);}}
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
    if(!capable||!assemblyTemplate)throw Error('Wait for the independent assembly workspace to load.');
    const id='asm-'+uid(),name='Untitled assembly',project=JSON.parse(JSON.stringify({units:'mm',selections:assemblyTemplate.selections,inputs:assemblyTemplate.inputs,notes:'Fit and strength UNKNOWN.'}));
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
    // Wizard-made equipment: this slot's tray choices open in the Place on tray window (tray-placement.js);
    // The library item itself is edited from there or from the Equipment list.
    if(String(placement.equipment).startsWith('eq-')){if(window.openTrayPlacement)window.openTrayPlacement(active()?.id,placement);else window.openCustomEquipment?.(placement);return;}
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
    colorField(host,'Whole rack',rack.appearance.color||'#8b9aa8',v=>{rack.appearance.color=v;markChanged();drawSoon();renderPaintList();renderEditor();});
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
    // Two-step reset: the first click arms it for a few seconds (no browser dialog; works on touch).
    let resetTimer=null;const reset=button('Reset all rack colors',()=>{
      if(!resetTimer){reset.textContent='Click again to reset all rack colors';resetTimer=setTimeout(()=>{resetTimer=null;reset.textContent='Reset all rack colors';},4000);return;}
      clearTimeout(resetTimer);rack.appearance={};markChanged();renderAppearance();drawSoon();notify('Rack colors reset in the draft. Save to keep it; History can restore earlier saved colors.');},'secondary');
    host.append(reset);
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
    const hasColorExport=false;
    const artDetails=document.createElement('details');artDetails.open=true;artDetails.id='assemblyAppearance';const sum=document.createElement('summary');sum.textContent=hasColorExport?'Equipment colors & faceplate image':'Tray & faceplate colors & image';artDetails.append(sum);
    const colorKeys=[['tray','Tray','#4d8e6e'],['faceplate','Faceplate','#4e75a3']];if(hasColorExport)colorKeys.unshift(['equipment','Equipment','#5b8545']);
    for(const [key,title,defaultColor] of colorKeys)colorField(artDetails,title,p.assembly.appearance[key]||defaultColor,v=>{p.assembly.appearance[key]=v;markChanged();applyAssemblyAppearance(p);if(key==='faceplate')refreshFilament();});
    const art=p.assembly.appearance.artwork;
    // The native file input always reads "No file chosen" after a re-render, so a button drives a hidden input.
    {const fileLabel=paragraph('Faceplate image','section-eyebrow');const file=document.createElement('input');file.id='faceplateImage';file.type='file';file.accept=ARTWORK_ACCEPT;file.hidden=true;file.onchange=()=>loadArtwork(file,p);
    const choose=button(art?'Replace image…':'Choose image…',()=>file.click(),'secondary');choose.setAttribute('aria-controls','faceplateImage');
    artDetails.append(fileLabel,file,choose,paragraph(hasColorExport?'PNG, JPEG, WebP, GIF, BMP, AVIF or SVG. Vector SVG is drawn sharp at full preview size, which suits Print in color best.':'PNG, JPEG, WebP, GIF, BMP, AVIF or SVG. Shown on this faceplate in the rack view only, in the largest area clear of port and keystone openings; Print in color is not available for this faceplate yet.','muted'));}
    if(art){artDetails.append(paragraph('Current: '+art.name),button('Fit & center image',()=>{Object.assign(art,{x:.5,y:.5,scale:1});markChanged();applyAssemblyAppearance(p);renderAppearance();},'secondary'),button('Center image',()=>{Object.assign(art,{x:.5,y:.5});markChanged();applyAssemblyAppearance(p);renderAppearance();},'secondary'));for(const [key,title,min,max] of [['x','Image horizontal position',0,1],['y','Image vertical position',0,1],['scale','Image size',.05,1]]){const label=document.createElement('label');label.textContent=title;const input=document.createElement('input');input.type='range';input.min=min;input.max=max;input.step=.01;input.value=art[key];input.setAttribute('aria-label',title);input.oninput=()=>{art[key]=Number(input.value);markChanged();applyAssemblyAppearance(p);refreshFilament();};label.append(input);artDetails.append(label);}artDetails.append(button('Remove image',()=>{delete p.assembly.appearance.artwork;filamentPreviews.delete(p.assembly.id);markChanged();applyAssemblyAppearance(p);renderAppearance();byId('assemblyAppearance').open=true;},'secondary'));}
    if(hasColorExport)artDetails.append(button('View faceplate front',async()=>{await openAssembly(p);if(window.workshopContext?.id===p.assembly.id)window.dispatchEvent(new Event('assembly-faceplate-front'));},'secondary'));
    artDetails.append(paragraph(hasColorExport?'Colors and the image are previews. Save to keep them. The normal tray and faceplate STLs never include color or artwork; the opt-in "Print in color" export below is the only artwork-to-STL path.':'Colors and the image are previews in the rack view. Save to keep them. Wizard-made equipment STLs never include color or artwork.','notice'));host.append(artDetails);
    refreshFilament=()=>{};
    if(art&&hasColorExport)renderFilament(host,p,art);
  }
  // Multi-color faceplate: one STL per filament color (faceplate_color.py). Fixed-outline legacy color export, currently unavailable for generic faceplates.
  const filamentPreviews=new Map();let filamentTimer=null,filamentRequest=0,refreshFilament=()=>{};
  function renderFilament(host,p,art){
    const box=document.createElement('details');box.id='filamentColors';box.open=filamentPreviews.has(p.assembly.id);
    const sum=document.createElement('summary');sum.textContent='Print in color (multi-material)';box.append(sum);
    // Always read the live settings: earlier edits replace art.filament, so a value captured at render time goes stale.
    const current=()=>art.filament||{count:4,style:'inlay',colors:[]};
    const later=()=>{clearTimeout(filamentTimer);filamentTimer=setTimeout(()=>preview(true),250);};
    const setFil=change=>{const f=current();art.filament={count:f.count,style:f.style,colors:f.colors||[],...change};markChanged();later();};
    // Image moves, size and faceplate color change the result too; refresh an open preview.
    refreshFilament=()=>{if(filamentPreviews.has(p.assembly.id)&&box.isConnected)later();};
    box.append(paragraph('Turns the image into a few filament colors and exports one STL per color. Load them all together in your slicer and give each file its own filament. Printed result, fit and strength stay UNKNOWN.','muted'));
    const styleLabel=document.createElement('label');styleLabel.textContent='Style';const style=document.createElement('select');
    for(const [v,t] of [['inlay','Inlay: flush with the face, 0.6 mm deep (print face down)'],['emboss','Raised: 0.6 mm above the face']]){const o=new Option(t,v);o.selected=current().style===v;style.append(o);}
    style.onchange=()=>setFil({style:style.value});styleLabel.append(style);
    const countLabel=document.createElement('label');countLabel.textContent='Number of filament colors (including the faceplate color)';const count=document.createElement('select');
    for(let n=2;n<=8;n++){const o=new Option(String(n),n);o.selected=current().count===n;count.append(o);}
    count.onchange=()=>setFil({count:Number(count.value),colors:[]});countLabel.append(count);
    const out=document.createElement('div');out.className='filament-preview';
    box.append(styleLabel,countLabel,button('Preview colors',()=>preview(false),'secondary'),out);
    const exportButton=button('Export color STLs (.zip)',async()=>{
      try{
        if(window.assertWorkshopSaved)window.assertWorkshopSaved();
        if(window.workshopContext?.id!==p.assembly.id)await openAssembly(p);
        // Never fall through to whichever assembly happens to be open.
        if(window.workshopContext?.id!==p.assembly.id)throw Error('Could not open this slot\'s assembly; open it from Setup, then export.');
        exportButton.disabled=true;notify('Building color STLs… this can take a minute for detailed images.');
        const response=await fetch('/api/faceplate-colors/export',{method:'POST',headers:{...projectHeaders(),'Content-Type':'application/json','X-App-Token':token},body:JSON.stringify({assembly:p.assembly.id})});
        if(!response.ok){const e=await response.json();throw Error(e.error);}
        const url=URL.createObjectURL(await response.blob()),a=document.createElement('a');a.href=url;a.download='faceplate-colors-'+p.assembly.id.slice(4,12)+'.zip';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
        notify('Color STLs exported (PROPOSED — UNVALIDATED). See README.txt in the zip for which file gets which filament.');
      }catch(e){notify(e.message,true);}finally{exportButton.disabled=false;}
    });
    box.append(exportButton,paragraph('Export uses the saved settings: Save first. Images stay on this computer.','muted'));host.append(box);
    function show(r){
      out.replaceChildren();
      const img=document.createElement('img');img.src=r.preview_png;img.alt='Color preview of the faceplate image';img.style.cssText='width:100%;image-rendering:pixelated;border:1px solid #445;border-radius:4px;';out.append(img);
      out.append(paragraph(`${r.size_mm[0]} × ${r.size_mm[1]} mm on the faceplate front · ${r.style==='emboss'?'raised':'inlay'}, ${r.depth_mm} mm`,'muted'));
      r.palette.forEach((hex,i)=>{
        const body=r.bodies.find(b=>b.index===i),merged=r.merged.includes(i),chosen=current().colors?.[i];
        const title=i===0?'Faceplate (base) color':'Color '+i+(merged?' — merged':body?` — ${body.area_mm2} mm², ~${body.grams_estimate} g`:' — removed in clean-up');
        const row=document.createElement('div');row.className='color-field';
        const label=document.createElement('span');label.textContent=title+(chosen?'':' · auto');
        const pick=document.createElement('input');pick.type='color';pick.value=i===0?r.base_hex:hex;pick.setAttribute('aria-label',title+' color');
        const named=document.createElement('select');named.setAttribute('aria-label',title+' filament');named.append(new Option('Filament…',''),new Option(i===0?'Faceplate color (auto)':'Image color (auto)','auto'));
        for(const [n,h] of r.filaments)named.append(new Option(n,h));
        // Explicit choices only; untouched entries stay null (= automatic) so other rows are never frozen or overwritten.
        const set=v=>{const colors=Array.from({length:r.palette.length},(_,k)=>current().colors?.[k]??null);colors[i]=v;while(colors.length&&colors.at(-1)===null)colors.pop();setFil({colors});};
        pick.onchange=()=>set(pick.value);named.onchange=()=>{if(named.value)set(named.value==='auto'?null:named.value);};
        row.append(label,pick,named);out.append(row);
      });
      out.append(paragraph('Tip: give two colors the same filament to merge them; give a color the faceplate filament to leave that area as plain faceplate.','muted'));
      for(const w of r.warnings)out.append(paragraph(w,'notice'));
      if(!r.exportable)out.append(paragraph('Not exportable yet — see the notes above.','workspace-error'));
    }
    async function preview(quiet){
      const request=++filamentRequest;
      try{const r=await api('faceplate-colors/preview',{artwork:art,faceplate:p.assembly.appearance.faceplate});if(request!==filamentRequest)return;filamentPreviews.set(p.assembly.id,r);if(box.isConnected){box.open=true;show(r);}}
      catch(e){if(request!==filamentRequest)return;if(!quiet)notify(e.message,true);else out.replaceChildren(paragraph(e.message,'workspace-error'));}
    }
    if(filamentPreviews.has(p.assembly.id))preview(true);
  }
  // Accepted faceplate image formats. Everything is converted locally to one PNG preview (at most 1024 px).
  const ARTWORK_TYPES={png:'image/png',jpg:'image/jpeg',jpeg:'image/jpeg',webp:'image/webp',gif:'image/gif',bmp:'image/bmp',avif:'image/avif',svg:'image/svg+xml'};
  const ARTWORK_ACCEPT=[...new Set(Object.values(ARTWORK_TYPES))].join(',')+',.svg,.avif';
  async function artworkSource(file){
    const ext=(file.name.split('.').pop()||'').toLowerCase(),type=file.type||ARTWORK_TYPES[ext]||'';
    if(!Object.values(ARTWORK_TYPES).includes(type))throw Error('Choose a PNG, JPEG, WebP, GIF, BMP, AVIF or SVG image.');
    if(type==='image/svg+xml'){
      if(file.size>5*1024*1024)throw Error('Choose an SVG up to 5 MB.');
      const doc=new DOMParser().parseFromString(await file.text(),'image/svg+xml'),svg=doc.documentElement;
      if(svg.nodeName!=='svg'||doc.getElementsByTagName('parsererror').length)throw Error('That SVG could not be read.');
      const dim=v=>/%\s*$/.test(v||'')?NaN:parseFloat(v),box=(svg.getAttribute('viewBox')||'').trim().split(/[\s,]+/).map(Number);
      let w=dim(svg.getAttribute('width')),h=dim(svg.getAttribute('height'));
      if(!(w>0&&h>0)&&box.length===4&&box[2]>0&&box[3]>0){w=box[2];h=box[3];}
      if(!(w>0&&h>0))throw Error('That SVG has no width/height or viewBox.');
      if(!svg.hasAttribute('viewBox'))svg.setAttribute('viewBox',`0 0 ${w} ${h}`);
      // Rendered through <img>: scripts and external resources in the SVG never run or load.
      return {vector:true,width:w,height:h,async draw(ctx,cw,ch){svg.setAttribute('width',cw);svg.setAttribute('height',ch);const url=URL.createObjectURL(new Blob([new XMLSerializer().serializeToString(svg)],{type:'image/svg+xml'}));try{const img=new Image();img.src=url;await img.decode();ctx.drawImage(img,0,0,cw,ch);}catch(e){throw Error('That SVG could not be drawn. Save it as plain SVG and try again.');}finally{URL.revokeObjectURL(url);}},close(){}};
    }
    if(file.size>25*1024*1024)throw Error('Choose an image up to 25 MB.');
    let bitmap;try{bitmap=await createImageBitmap(file);}catch(e){throw Error('This browser could not read that image.');}
    if(bitmap.width*bitmap.height>40_000_000){bitmap.close();throw Error('Choose an image up to 40 megapixels.');}
    return {vector:false,width:bitmap.width,height:bitmap.height,draw(ctx,cw,ch){ctx.drawImage(bitmap,0,0,cw,ch);},close(){bitmap.close();}};
  }
  async function loadArtwork(input,p){
    const file=input.files[0];if(!file)return;input.disabled=true;artworkPending++;
    const identity=p.assembly.id,request=(artworkRequests.get(identity)||0)+1;artworkRequests.set(identity,request);
    let source=null;
    try{
      source=await artworkSource(file);
      const canvas=document.createElement('canvas');let url;
      // Largest preview that fits the server's 1.4 MB PNG limit; vectors are drawn at the target size, never upscaled pixels.
      for(const limit of [1024,768,512,256]){const ratio=source.vector?limit/Math.max(source.width,source.height):Math.min(1,limit/Math.max(source.width,source.height));canvas.width=Math.max(1,Math.min(limit,Math.round(source.width*ratio)));canvas.height=Math.max(1,Math.min(limit,Math.round(source.height*ratio)));const ctx=canvas.getContext('2d');ctx.clearRect(0,0,canvas.width,canvas.height);await source.draw(ctx,canvas.width,canvas.height);url=canvas.toDataURL('image/png');if(url.length<=1_860_000)break;}
      if(url.length>1_860_000)throw Error('That image is too detailed to store; try a simpler image.');
      const asset=await api('artwork',{data_url:url});
      if(artworkRequests.get(identity)!==request)return;
      p=documentState.racks.flatMap(r=>r.placements).find(item=>item.assembly.id===p.assembly.id);if(!p)throw Error('The allocation was released. Choose an existing assembly.');
      filamentPreviews.delete(p.assembly.id);
      p.assembly.appearance.artwork={sha256:asset.sha256,name:file.name.slice(0,120),mode:'preview-only',x:.5,y:.5,scale:.65};markChanged();applyAssemblyAppearance(p);renderAppearance();if(byId('assemblyAppearance'))byId('assemblyAppearance').open=true;notify(`Faceplate image prepared (${asset.width} × ${asset.height} px${source.vector?', from vector':''}). Save to keep it. Normal STL geometry is unchanged.`);
    }catch(e){notify(e.message,true);}finally{source?.close();input.disabled=false;artworkPending--;}
  }

  function appendReleaseUndo(host,rack){
    if(lastReleased?.rackId!==rack.id)return;
    host.append(button('Undo slot release',()=>{try{const item=RackLayout.restore(rack,lastReleased);lastReleased=null;selectedSlot=item.slot;markChanged();render();notify('Slot allocation restored in the draft. Save to keep it.');}catch(e){notify('Cannot restore allocation: '+e.message,true);}},'secondary'));
  }
  function renderProperties(){
    const rack=active(),host=byId('slotProperties');host.replaceChildren();renderAppearance();byId('jointProperties').open=stage==='assemble';syncInspector();
    byId('selectionSummary').textContent=rack?rack.name+(selectedSlot?' / Slot '+selectedSlot:' / Rack'):'No rack selected';
    if(!rack){host.append(paragraph('Create a rack layout to define your workspace.'),button('Create rack',()=>openRackDialog(false),'primary'));return;}
    byId('propertiesContext').textContent=selectedSlot?'Slot '+selectedSlot:'Rack layout';appendConnectBox(host,rack);host.append(paragraph('CURRENT SELECTION','section-eyebrow'));
    const title=document.createElement('h2');title.textContent=selectedSlot?'Slot '+String(selectedSlot).padStart(2,'0'):rack.name;host.append(title);
    if(!selectedSlot){host.append(paragraph(rack.slots+' slots · '+rack.placements.length+' assigned assemblies'),button('Edit rack settings',()=>openRackDialog(true),'secondary'));appendExtensionControls(host,rack);appendGuideControls(host,rack);appendCableSetup(host,rack);appendRackStlExport(host,rack);appendReleaseUndo(host,rack);return;}
    const placement=assigned(rack,selectedSlot);
    if(placement){host.append(paragraph((placement.assembly?.name||'Untitled assembly')+' · slots '+placement.slot+'–'+(placement.slot+placement.span-1)),paragraph('Reference allocation. Installed fit, service access and load capacity are UNKNOWN.'),button(String(placement.equipment).startsWith('eq-')?'Place on tray':'Open assembly',()=>openAssembly(placement),'primary'),button('Slot actions ⋯',e=>showSlotMenu(selectedSlot,e.currentTarget),'secondary'));if(traySketch(placement))host.append(paragraph(TRAY_SKETCH,'notice'));const jw=jointWarning(rack,placement.slot,placement.span);if(jw)host.append(paragraph('⚠ '+jw,'notice'));}
    else{host.append(paragraph('An open slot in your rack. Choose equipment to begin a guided assembly.'),button('Create assembly',startWizard,'primary'));}
    if(placement&&!String(placement.equipment).startsWith('eq-')&&!persistedAssemblyIds.has(placement.assembly.id)){host.querySelector('button.primary').disabled=true;host.append(paragraph('Use Save to keep this allocation before opening its hardware editor.'));}
    if(placement)appendPortControls(host,rack,placement);
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
    const span=item.span||1;if(selectedSlot+span-1>rack.slots){notify(item.name+': '+span+'U from slot '+selectedSlot+' doesn’t fit; this rack ends at slot '+rack.slots+'.',true);return false;}
    for(let s=selectedSlot;s<selectedSlot+span;s++)if(assigned(rack,s)){notify('That allocation overlaps another assembly.',true);return false;}
    const assembly=newAssembly();assembly.name=item.name;assembly.project.name=item.name;
    const placement={assembly,id:uid(),equipment:item.id,slot:selectedSlot,span,geometry:'equipment-library',fit:'UNKNOWN',...(span!==item.spec?.u?{tray:{u:span}}:{})};
    rack.placements.push(placement);
    markChanged();renderTree();setStage('rack');renderProperties();
    notify(item.name+' placed in the draft layout with its library tray defaults. Save to keep it. Rack fit is UNKNOWN.');
    window.openTrayPlacement?.(rack.id,placement);return true;
  };
  // Place on tray window "Apply to draft": store this allocation's tray choices (only those differing from the
  // library item) and, when its faceplate height changed, the slot span. Draft only; Save keeps it.
  // Brian 2026-10-19: the rack view shows the library item's mesh; a slot's own tray placement is not rendered
  // automatically. Screening and ports already use the slot's settings, so say which view lags behind.
  // Rack view (equipment-wizard.js EquipmentRackView): a slot with its own tray settings shows an exact render of them when one
  // already exists, else a box sketch of them. Only the sketch gets this note.
  const TRAY_SKETCH='Rack view shows a box sketch of this slot’s tray settings (position, rotation, height, keystones, ports). Place on tray → Render exact preview draws the exact shape here.';
  function traySketch(placement){return window.EquipmentRackView?.status(placement)==='sketch';}
  window.applyTrayPlacement=function(rackId,placementId,tray,newSpan,second){
    const rack=active();if(!rack||rack.id!==rackId)throw Error('Select the original rack before applying this placement.');
    let placement=rack.placements.find(p=>p.id===placementId);if(!placement)throw Error('This allocation is no longer available.');
    if(newSpan&&newSpan!==placement.span)placement=RackLayout.change(rack,placementId,placement.slot,newSpan);
    if(tray&&Object.keys(tray).length)placement.tray=tray;else delete placement.tray;
    if(second)placement.second=second;else delete placement.second; // two devices on one tray (Brian, 2026-10-20)
    selectedSlot=placement.slot;markChanged();render();
    notify('Tray placement applied to the draft. Save to keep it. Fit, retention and strength are UNKNOWN.');
  };
  function startWizard(){
    if(!capable){notify('Wait for the updated workspace to load.',true);return;}
    const rack=active();if(!rack||!selectedSlot||assigned(rack,selectedSlot)){notify('Select an empty rack slot first.');return;}
    showInspector('Setup');const wizard=byId('mountWizard');wizard.hidden=false;wizard.replaceChildren();
    wizard.append(paragraph('CREATE ASSEMBLY · SLOT '+selectedSlot,'section-eyebrow'),paragraph('Choose equipment from My Equipment, then reserve its slot span.'));
    const choice=document.createElement('select'),empty=document.createElement('option');empty.value='';empty.textContent='Choose equipment…';choice.append(empty);
    for(const item of window.equipmentLibraryItems?.()||[]){const o=document.createElement('option');o.value=item.id;o.textContent=item.name;choice.append(o);}
    const input=document.createElement('input');input.id='allocationSpan';input.type='number';input.min='1';input.max=String(rack.slots-selectedSlot+1);input.value='1';
    choice.onchange=()=>{input.value=String((window.equipmentLibraryItems?.()||[]).find(i=>i.id===choice.value)?.span||1);};
    const label=document.createElement('label');label.textContent='Slots to reserve';label.htmlFor=input.id;
    const error=paragraph('','fail');wizard.append(choice,label,input,error,button('Confirm slot allocation',()=>{
      const item=(window.equipmentLibraryItems?.()||[]).find(i=>i.id===choice.value),span=Number(input.value);
      if(!item){error.textContent='Choose an equipment library item.';return;}
      if(active()?.id!==rack.id||!Number.isInteger(span)||span<1||span>5){error.textContent='Choose 1–5 slots in the original rack.';return;}
      if(window.placeLibraryEquipment({...item,span})){const p=assigned(rack,selectedSlot);if(span!==item.span)p.tray={u:span};wizard.hidden=true;}
    },'primary'),button('New equipment…',()=>window.openEquipmentWizard?.(),'secondary'),button('Cancel',()=>{wizard.hidden=true;},'secondary'));
  }
  function renderReview(){const rack=active(),host=byId('rackReview');host.replaceChildren();host.append(paragraph('UNKNOWN · Rack installation and strength','review-unknown'));if(!rack){host.append(paragraph('No rack layout selected.'));return;}const missing=['width_mm','depth_mm','pitch_mm'].filter(k=>rack[k]===null);host.append(paragraph(missing.length?'UNKNOWN · '+missing.map(k=>({width_mm:'internal width',depth_mm:'usable depth',pitch_mm:'slot pitch'}[k])).join(', ')+' not specified.':'USER-SUPPLIED · Layout dimensions recorded; physical fit is not verified.'));host.append(paragraph('Slot allocations do not overlap. Wizard equipment is envelope-screened against the nominal rack numbers below; this is not a fit check. Cable and tool clearance are not screened.'));
    const library=window.equipmentLibraryItems?.()||[],screen=window.WorkshopClearance?.screen,labels={ok:'SCREENED OK',tight:'TIGHT',over:'OVER',unknown:'UNKNOWN',reference:'REFERENCE'};
    for(const p of rack.placements){
      const where=(p.assembly?.name||'Untitled assembly')+' · slots '+p.slot+'–'+(p.slot+p.span-1);
      if(!screen){host.append(paragraph(where+' · screening unavailable; rack fit UNKNOWN.'));continue;}
      const r=screen(rack,p,library.find(i=>i.id===p.equipment));
      const box=document.createElement('div');box.className='clearance-result clearance-'+r.level;
      const head=document.createElement('strong');head.textContent=labels[r.level]+' · '+where;box.append(head);
      for(const c of r.checks)box.append(paragraph((c.level==='ok'?'✓ ':c.level==='unknown'?'? ':'⚠ ')+c.text,'clearance-check clearance-'+c.level));
      const jw=jointWarning(rack,p.slot,p.span);if(jw)box.append(paragraph('⚠ '+jw,'clearance-check clearance-tight'));
      box.append(paragraph(r.note));host.append(box);
    }
    appendCableSuggestions(host,rack);appendWiringSheet(host,rack);appendPartsOrder(host,rack);}
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
  let previewRenderer = null, previewPending = false, editingRack = null;
  function setSlots(n){
    const slots = Math.min(14, Math.max(1, Math.round(Number(n)) || 1));
    byId('rackSlots').value = slots;
    byId('slotCountDisplay').textContent = slots + 'U';
    const original=documentState.racks.find(r=>r.id===editingId);
    editingRack=original?JSON.parse(JSON.stringify(original)):{placements:[]};
    editingRack.slots=slots;
    if(original?.slots!==slots){delete editingRack.post_levels;delete editingRack.layout_locked;}
    renderBom(editingRack);
    drawPreviewSoon();
  }
  function renderBom(rack){
    const counts=rackCounts(rack,false),host=byId('rackBom');host.replaceChildren();
    if(counts.error){host.append(paragraph(counts.error,'fail'));return;}
    for(const u of Object.keys(counts.posts).sort((a,b)=>b-a))host.append(paragraph(counts.posts[u]+' × '+u+'U post segment'));
    if(counts.extensions)host.append(paragraph(counts.extensions+' × 1U support extension'));
    for(const [key,label] of Object.entries({beam_bottom:'bottom beam',beam_top_front:'top front beam',beam_top_rear:'top rear beam',side_rail:'side rail',panel_bottom:'bottom panel',panel_top:'top panel',foot:'foot',handle:'handle'}))host.append(paragraph(counts.parts[key]+' × '+label));
    host.append(paragraph(counts.hardware_allowance+' × M6 DIN 7380 buttonhead bolt'),paragraph(counts.hardware_allowance+' × M6 brass heat-set insert'),paragraph('Full-hole hardware allowance; installed quantity UNKNOWN'),paragraph('Extension and other frame/side-panel fastener quantities: UNKNOWN'),paragraph('Side panels excluded from this setup preview; top and bottom panels included. Fit and strength UNKNOWN.'));
  }
  function drawPreviewSoon(){ if(!previewPending){ previewPending = true; requestAnimationFrame(drawRackPreview); } }
  function drawRackPreview(){
    previewPending = false;
    const c = byId('rackPreviewCanvas');
    if(!byId('rackDialog').open || !c) return;
    const w = c.clientWidth || 280, h = c.clientHeight || 260, dpr = rackPixelRatio();
    c.width = Math.round(w * dpr); c.height = Math.round(h * dpr);
    const ctx = c.getContext('2d'); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = '#151c26'; ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#aab9cb'; ctx.font = '13px system-ui';
    if(!sourceMeshes){ ctx.fillText(sourceError || 'Loading frame meshes…', 12, 22); return; }
    try{
      if(!previewRenderer || previewRenderer.restoreRequired){ previewRenderer?.dispose(); previewRenderer = new LabRaxStudio.Renderer(); previewRenderer.invalidated = drawPreviewSoon; }
      previewRenderer.shadows = false; previewRenderer.ambientOcclusion = false;
      const counts=rackCounts(editingRack,false);if(counts.error)throw Error(counts.error);
      const slots=editingRack.slots,scene=rackFrame(slots,false,editingRack),box=LabRaxScene.bounds(scene,sourceMeshes);
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
    // Cable guides keep their height above the floor (slots count down from the top); any that no longer fit are dropped.
    if(old?.cabling?.guides?.length){const shift=slots-old.slots,guides=old.cabling.guides.map(g=>({...g,slot:g.slot+shift})).filter(g=>g.slot>=1&&g.slot<=slots);next.cabling={...old.cabling,guides};}
    // Exit points move the same way; cables that used a dropped exit are updated by the cable upkeep (route changed).
    if(old?.cabling?.exits?.length){const shift=slots-old.slots,exits=old.cabling.exits.map(x=>({...x,slot:x.slot+shift})).filter(x=>x.slot>=1&&x.slot<=slots);next.cabling={...(next.cabling||old.cabling),exits};}
    else if(old?.cabling&&!next.cabling)next.cabling=old.cabling;
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
      // Port edits of released slots are dropped from what is saved (the draft keeps them for Undo slot release).
      // Decision 14: cable ends on released equipment or removed ports become unconnected before saving.
      for(const r of documentState.racks)window.labRaxCableUpkeep?.(r);
      const workspace=window.LabRaxPorts?{...documentState,racks:documentState.racks.map(LabRaxPorts.prune)}:documentState;
      const saved=await api('studio-save',{workspace,assembly:hardware?{...hardware,id:identity}:null});
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
  window.addEventListener('equipment-library',()=>{renderReview();
    // Wizard ports come from the library spec; refresh the port list once it has loaded (unless the user is typing there).
    const p=selectedSlot&&active()?assigned(active(),selectedSlot):null;if(p&&String(p.equipment).startsWith('eq-')&&!byId('slotProperties').contains(document.activeElement))renderProperties();});
  window.activeRackNumbers=()=>{const r=active();return r?{width_mm:r.width_mm,depth_mm:r.depth_mm,pitch_mm:r.pitch_mm}:null;};

  byId('rackChoice').onchange=e=>{if(!leaveAssembly()){e.target.value=activeId;return;}activeId=e.target.value;selectedSlot=null;stage='rack';byId('mountWizard').hidden=true;render();};
  for(const e of document.querySelectorAll('[data-stage]'))e.onclick=()=>{setStage(e.dataset.stage);renderProperties();};
  byId('newRack').onclick=()=>openRackDialog(false);byId('configureRack').onclick=()=>openRackDialog(!!active());byId('backToRack').onclick=()=>{setStage('rack');renderProperties();};
  byId('closeRackDialog').onclick=byId('cancelRackDialog').onclick=()=>byId('rackDialog').close();
  function libraryTab(which){byId(which==='equipment'?'equipmentSection':'racksSection').open=true;}
  function dashboard(){const list=byId('recentRacks');list.replaceChildren();if(!documentState.racks.length)list.append(paragraph('Your saved layouts will appear here.'));for(const rack of documentState.racks)list.append(button(rack.name+' · '+rack.slots+' slots',()=>{if(!leaveAssembly())return;activeId=rack.id;selectedSlot=null;stage='rack';byId('dashboardDialog').close();render();},'recent-rack'));byId('dashboardDialog').showModal();}
  byId('homeStudio').onclick=dashboard;byId('closeDashboard').onclick=()=>byId('dashboardDialog').close();byId('dashboardNew').onclick=()=>{byId('dashboardDialog').close();openRackDialog(false);};
  const shortcuts=[['Orbit rack','Drag in the rack viewport'],['Orbit assembly','Arrow keys while the assembly viewport is focused'],['Save rack layout','Ctrl / ⌘ + S'],['Cancel dialog','Escape'],['Inspect a slot','Select a slot in Assembly Explorer']];
  function renderShortcuts(){const list=byId('shortcutList');list.replaceChildren();for(const [name,key] of shortcuts)if((name+' '+key).toLowerCase().includes(byId('shortcutSearch').value.toLowerCase()))list.append(paragraph(name+' — '+key));}
  byId('shortcutHelp').onclick=()=>{renderShortcuts();byId('shortcutsDialog').showModal();};byId('shortcutSearch').oninput=renderShortcuts;byId('closeShortcuts').onclick=()=>byId('shortcutsDialog').close();
  window.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){e.preventDefault();if(layoutDirty||dirty)byId('saveLayout').click();}});
  window.addEventListener('beforeunload',e=>{if(layoutDirty||dirty){e.preventDefault();e.returnValue='';}});

  // Actual source components in recovered visual poses, isolated from STL export.
  let showRackPanels=false, perspectiveCamera=true, studioQuality=true, showRearLabels=false, cablesView=false, selectedGuide=null;
  // Cable-planning ports (cable-ports.js): selected port key (allocation id / port id) and the port waiting for a mesh click.
  let selectedPort=null, placingPort=null;
  // Cables (Step 3, cable-routes.js + cable-view.js): selection, Connect mode, the one-time face question, visibility.
  let selectedCable=null, selectedExit=null, connecting=null, facePrompt=null, showCableRuns=false, viewMode='3d';
  // Step 4 suggestions: "Show me" highlight sets, and the one Apply that Undo can take back.
  let showMe=null, lastApply=null;
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
  // Logical counts do not depend on loaded preview meshes. No mutation or persistence.
  function rackCounts(rack,panels=false){
    const error='Invalid post segment layout. Posts (1–5U) plus 1U extensions must add up to the rack height.';
    if(!rack||!Number.isInteger(rack.slots)||rack.slots<1||rack.slots>48)return {error};
    const levels=rack.post_levels;
    if(levels!==undefined&&(!levels||typeof levels!=='object'||Array.isArray(levels)||Object.keys(levels).some(k=>!['left','right'].includes(k))))return {error};
    const stacks={},posts={},sidePanels={},parts={beam_bottom:2,beam_top_front:1,beam_top_rear:1,side_rail:4,panel_bottom:1,panel_top:1,foot:4,handle:2};
    let extensions=0,postUnits=0;
    for(const side of ['left','right']){
      const stack=levels&&Object.hasOwn(levels,side)?levels[side]:defaultLevels(rack.slots);
      if(!Array.isArray(stack)||!stack.length||!stack.every(u=>Number.isInteger(u)&&u>=1&&u<=5)||stackHeight(stack)!==rack.slots)return {error};
      stacks[side]=stack.slice();extensions+=stack.length-1;
      for(const u of stack){posts[u]=(posts[u]||0)+2;postUnits+=2*u;if(panels)sidePanels[u]=(sidePanels[u]||0)+1;}
    }
    for(const [u,n] of Object.entries(posts))parts['post'+u]=n;
    for(const [u,n] of Object.entries(sidePanels))parts['panel'+u]=n;
    if(extensions)parts.extension=extensions;
    return {stacks,posts,extensions,panels:sidePanels,hardware_allowance:postUnits*HOLES_PER_U,parts};
  }
  // Frame with per-side post stacks plus a 1U support extension at every joint (rack-scene.js leaves it out).
  function rackFrame(slots,panels,rack){
    const counts=rackCounts(rack||{slots},panels);if(counts.error)throw Error(counts.error);
    const scene=LabRaxScene.frame(slots,panels),U=LabRaxScene.U,PX=125.98,DEPTH=240;
    const I=[1,0,0,0,1,0,0,0,1],RX=[1,0,0,0,-1,0,0,0,-1],RY=[-1,0,0,0,1,0,0,0,-1],RZ=[-1,0,0,0,-1,0,0,0,1],R90=[0,-1,0,1,0,0,0,0,1];
    scene.parts=scene.parts.filter(p=>!/^post\d$/.test(p.key)&&p.kind!=='side');
    const sides={left:[[I,-PX,17.5],[RX,-PX,DEPTH-17.5]],right:[[RY,PX,17.5],[RZ,PX,DEPTH-17.5]]};
    for(const side of ['left','right']){
      const levels=counts.stacks[side],x=side==='left'?-PX:PX;let z=0;
      levels.forEach((u,i)=>{const middle=z+u*U/2;
        for(const [R,px,py] of sides[side])scene.parts.push({key:'post'+u,R,t:[px,py,middle],kind:'frame'});
        if(panels)scene.parts.push({key:'panel'+u,R:R90,t:[side==='left'?-138.48:138.48,120,middle],kind:'side'});
        z+=u*U;
        // The extension fills the next 1U; its end tabs reach into the pockets of the posts either side.
        if(i<levels.length-1){if(sourceMeshes?.extension)scene.parts.push({key:'extension',R:side==='left'?I:RY,t:[x,120,z+U/2],kind:'frame',source:[2,'1']});z+=U;}
      });
    }
    // Cable guides are preview parts only (kind 'guide'); RACK_PART_SOURCES has no entry for them, so the STL export skips them.
    if(sourceMeshes?.cable_guide)for(const g of rackGuides(rack)){if(g.slot>slots)continue;const pose=LabRaxScene.guidePose(slots,g.post,g.slot);scene.parts.push({key:'cable_guide',...pose,kind:'guide',guide:g.id});}
    return scene;
  }
  // Rack frame STL export: count every frame part this layout uses and ask the server for the source meshes.
  const RACK_PART_SOURCES={post1:[0,'1'],post2:[0,'9'],post3:[0,'17'],post4:[0,'24'],post5:[0,'31'],panel1:[0,'6'],panel2:[0,'14'],panel3:[0,'22'],panel4:[0,'29'],panel5:[0,'36'],beam_bottom:[1,'20'],beam_top_front:[1,'23'],beam_top_rear:[1,'18'],side_rail:[1,'28'],panel_bottom:[1,'13'],panel_top:[1,'11'],foot:[1,'6'],handle:[1,'25'],extension:[2,'1']};
  async function downloadRackStl(rack,panels){
    const result=rackCounts(rack,panels);if(result.error)throw Error(result.error);
    const counts=result.parts;
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
  // Cable guides (Lab Rax Cable Guide, local preview mesh only): one per post per U, kept in rack.cabling.guides.
  // They are planning placements; never part of the rack STL export. Fit, capacity and strength UNKNOWN.
  const GUIDE_POSTS={RL:'Rear left',RR:'Rear right',FL:'Front left',FR:'Front right'};
  const rackGuides=rack=>rack?.cabling?.guides||[];
  // Set one rack.cabling list; an empty list removes only that key (the rest of the cabling block stays).
  function setCablingList(rack,key,list){const c={...(rack.cabling||{})};if(list&&list.length)c[key]=list;else delete c[key];if(Object.keys(c).length)rack.cabling=c;else delete rack.cabling;}
  function setGuides(rack,list){setCablingList(rack,'guides',list);sceneCacheKey='';markChanged();renderProperties();}
  // Slots taken by a 1U support extension on that side; whether the extension has holes there is UNKNOWN.
  function extensionSlots(rack,side){const out=new Set();let z=0;sideLevels(rack,side).forEach((u,i,levels)=>{z+=u;if(i<levels.length-1){out.add(rack.slots-z);z+=1;}});return out;}
  // Brian, 2026-10-19: a multi-U plate may span a support-extension joint; warn, never block. Rack-hole fit there is UNKNOWN.
  function jointWarning(rack,slot,span){
    if(!rack||!(span>1))return null;const hits=new Map();
    for(const side of['left','right'])for(const s of extensionSlots(rack,side))if(s>=slot&&s<slot+span)hits.set(s,[...(hits.get(s)||[]),side]);
    if(!hits.size)return null;const where=[...hits].sort((a,b)=>a[0]-b[0]).map(([s,sides])=>'slot '+s+' ('+(sides.length>1?'both sides':sides[0]+' side')+')').join(' and ');
    return 'This '+span+'U plate crosses the 1U support extension at '+where+'. Its rack holes may land on the extension joint; fit there is UNKNOWN. Warning only: you can still place and save it.';
  }
  window.extensionJointWarning=(slot,span)=>jointWarning(active(),slot,span);
  function guideLabel(g){return g.post+' · U'+String(g.slot).padStart(2,'0');}
  function selectGuide(id){
    if(selectedSlot!==null){if(!leaveAssembly())return;selectedSlot=null;byId('mountWizard').hidden=true;setStage('rack');renderTree();}
    selectedPort=null;placingPort=null;clearCableSelection();selectedGuide=id;showInspector('Setup');renderProperties();drawSoon();
  }
  function moveGuide(rack,g,changes){
    const next={...g,...changes};
    if(next.slot<1||next.slot>rack.slots){notify('A cable guide must stay inside the rack slots.',true);return;}
    if(rackGuides(rack).some(o=>o.id!==g.id&&o.post===next.post&&o.slot===next.slot)){notify(GUIDE_POSTS[next.post]+' post already has a cable guide at U'+String(next.slot).padStart(2,'0')+'.',true);return;}
    setGuides(rack,rackGuides(rack).map(o=>o.id===g.id?next:o));
  }
  function appendGuideControls(host,rack){
    const list=[...rackGuides(rack)].sort((a,b)=>Object.keys(GUIDE_POSTS).indexOf(a.post)-Object.keys(GUIDE_POSTS).indexOf(b.post)||a.slot-b.slot);
    host.append(paragraph('CABLE GUIDES','section-eyebrow'),paragraph('Lab Rax Cable Guide · 1U on a post with 2 × M6 × 10 mm screws (creator’s note). Preview only: not included in the rack STLs. Fit, cable capacity and strength are UNKNOWN.'));
    const selectFrom=(options,value,label)=>{const s=document.createElement('select');s.setAttribute('aria-label',label);for(const [v,text] of options){const o=document.createElement('option');o.value=v;o.textContent=text;s.append(o);}s.value=String(value);return s;};
    const postOptions=Object.entries(GUIDE_POSTS),slotOptions=Array.from({length:rack.slots},(_,i)=>[String(i+1),'U'+String(i+1).padStart(2,'0')]);
    for(const g of list){
      const row=document.createElement('div');row.className='guide-row'+(g.id===selectedGuide?' selected':'');
      const name=button(guideLabel(g),()=>selectGuide(g.id===selectedGuide?null:g.id),'guide-name');name.setAttribute('aria-pressed',String(g.id===selectedGuide));name.title=GUIDE_POSTS[g.post]+' post, slot '+g.slot+'. Select to highlight it in the viewport.';
      const post=selectFrom(postOptions,g.post,'Post');post.onchange=()=>moveGuide(rack,g,{post:post.value});
      const up=button('▲',()=>moveGuide(rack,g,{slot:g.slot-1}),'secondary'),down=button('▼',()=>moveGuide(rack,g,{slot:g.slot+1}),'secondary');up.title='Move up 1U';down.title='Move down 1U';up.disabled=g.slot<=1;down.disabled=g.slot>=rack.slots;
      const remove=button('Remove',()=>{if(selectedGuide===g.id)selectedGuide=null;setGuides(rack,rackGuides(rack).filter(o=>o.id!==g.id));notify('Cable guide removed from the draft. Save to keep the change.');},'subtle');
      row.append(name,post,up,down,remove);host.append(row);
      if(extensionSlots(rack,g.post[1]==='L'?'left':'right').has(g.slot))host.append(paragraph('This U is a 1U support extension on that side. Whether it has mounting holes for the guide is UNKNOWN.','notice'));
    }
    if(!list.length)host.append(paragraph('No cable guides yet. The creator suggests the rear posts, where cables run between equipment.'));
    const add=document.createElement('div');add.className='guide-row';
    const post=selectFrom(postOptions,'RL','Post for the new guide'),slot=selectFrom(slotOptions,1,'Slot for the new guide');
    const firstFree=()=>{const used=new Set(rackGuides(rack).filter(g=>g.post===post.value).map(g=>g.slot));for(let s=1;s<=rack.slots;s++)if(!used.has(s))return s;return null;};
    post.onchange=()=>{const s=firstFree();if(s)slot.value=String(s);};post.onchange();
    const addButton=button('Add cable guide',()=>{
      const g={id:'guide-'+Math.random().toString(16).slice(2,14),kind:'labrax-cable-guide',post:post.value,slot:Number(slot.value)};
      if(rackGuides(rack).some(o=>o.post===g.post&&o.slot===g.slot)){notify(GUIDE_POSTS[g.post]+' post already has a cable guide at U'+String(g.slot).padStart(2,'0')+'.',true);return;}
      selectedGuide=g.id;setGuides(rack,[...rackGuides(rack),g]);notify('Cable guide added to the draft at '+guideLabel(g)+'. Save to keep it.');
    },'secondary');
    add.append(post,slot,addButton);host.append(add);
  }
  // Ports (cable management Step 2): Library planning ports, plus per-rack edits in rack.cabling.ports.
  // Planning data only: no geometry, STL or hardware pins change. Connector fit and cable access are UNKNOWN.
  const libraryItem=placement=>(window.equipmentLibraryItems?.()||[]).find(i=>i.id===placement.equipment);
  function placementOfPort(rack,key){return key?rack?.placements.find(p=>key.startsWith(p.id+'/'))||null:null;}
  function selectPort(key){
    const rack=active(),placement=placementOfPort(rack,key);if(!placement)return;
    if(selectedSlot!==placement.slot){if(!leaveAssembly())return;selectedSlot=placement.slot;selectedGuide=null;byId('mountWizard').hidden=true;setStage('rack');renderTree();}
    selectedPort=key;placingPort=null;clearCableSelection();rackCanvas.classList.remove('placing-port');showInspector('Setup');renderProperties();drawSoon();
  }
  function editPort(rack,placement,port,changes){
    LabRaxPorts.setOverride(rack,placement.id,port.id,changes,!!port.custom);markChanged();renderProperties();
  }
  function armPortPlacement(key){
    placingPort=placingPort===key?null:key;rackCanvas.classList.toggle('placing-port',!!placingPort);renderProperties();
    if(placingPort)notify('Click a point on this equipment in the rack view to set the port position. Click “Cancel placing” to stop.');
  }
  // Mesh click while a port waits for placement: the hit point on that allocation's own mesh becomes the port position.
  function placePortAt(x,y){
    const rack=active(),placement=placementOfPort(rack,placingPort),found=sceneRenderer?.hitTest(x,y);if(!placement)return;
    const hit=found?.hit;
    if(!hit||hit.kind==='port'||hit.slot!==placement.slot||!found.point){notify('Click on this equipment’s tray or faceplate. See-through trays in Cables view can’t be clicked; turn Cables view off to place on them.',true);return;}
    const port=LabRaxPorts.portsFor(rack,placement,libraryItem(placement)).find(p=>p.key===placingPort);if(!port)return;
    const position=LabRaxPorts.positionFromHit(rack,placement,found.point);placingPort=null;rackCanvas.classList.remove('placing-port');
    editPort(rack,placement,port,position);
    notify(`${port.label} moved to X ${position.x.toFixed(1)} · Y ${position.y.toFixed(1)} · Z ${position.z.toFixed(1)} mm in the draft. Save to keep it.`);
  }
  function appendPortControls(host,rack,placement){
    if(!window.LabRaxPorts)return;const P=LabRaxPorts,eq=String(placement.equipment).startsWith('eq-'),item=libraryItem(placement);
    host.append(paragraph('PORTS','section-eyebrow'),paragraph(eq?'From this equipment’s wizard Ports step: front openings, rear ports and keystones (front and rear face each). Planning data only.':'Library ports are planning data only. Cable access and physical fit remain UNKNOWN.'));
    if(eq&&!item){host.append(paragraph('This equipment’s ports load with the equipment library.'));return;}
    const ports=P.portsFor(rack,placement,item),faceText=p=>p.face?P.FACES[p.face]:'Face UNKNOWN';
    if(!ports.length)host.append(paragraph('No ports yet. Add them in the equipment wizard’s Ports step, or add a custom port below.'));
    for(const p of ports){const row=document.createElement('div');row.className='guide-row port-row'+(p.key===selectedPort?' selected':'');
      const name=button(`${p.label} · ${P.TYPES[p.type]?.label||p.type} · ${faceText(p)}${p.tuned?' · moved':''}`,()=>p.key===selectedPort?(selectedPort=null,placingPort=null,renderProperties(),drawSoon()):selectPort(p.key),'guide-name');
      name.setAttribute('aria-pressed',String(p.key===selectedPort));name.style.setProperty('--port-color',P.TYPES[p.type]?.color||'#c3ccd6');row.append(name);host.append(row);}
    const selected=ports.find(p=>p.key===selectedPort);
    if(selected)appendPortPanel(host,rack,placement,selected,ports);
    host.append(button('Add custom port',()=>{const id=P.newPortId(rack,placement.id);P.setOverride(rack,placement.id,id,{label:'Custom port',type:'other',face:'rear',x:0,y:eq?60:70,z:20},true);markChanged();selectPort(placement.id+'/'+id);notify('Custom port added to the draft. Set its position, then Save to keep it.');},'secondary'));
  }
  function appendPortPanel(host,rack,placement,port,ports){
    const P=LabRaxPorts,panel=document.createElement('div');panel.className='port-panel';panel.setAttribute('aria-label','Port');
    const field=(label,control)=>{const l=document.createElement('label');l.className='port-field';l.append(label,control);return l;};
    const options=(list,value)=>{const s=document.createElement('select');for(const [v,text] of list){const o=document.createElement('option');o.value=v;o.textContent=text;s.append(o);}s.value=value;return s;};
    const head=document.createElement('h3');head.textContent='Port · '+port.label;panel.append(paragraph('PORT','section-eyebrow'),head);
    const label=document.createElement('input');label.type='text';label.maxLength=40;label.value=port.label;label.onchange=()=>editPort(rack,placement,port,{label:label.value.trim()||port.label});
    const type=options(Object.entries(P.TYPES).map(([k,t])=>[k,t.label]),port.type);type.onchange=()=>editPort(rack,placement,port,{type:type.value});
    const face=options([...(port.face?[]:[['','UNKNOWN — choose']]),...Object.entries(P.FACES)],port.face||'');face.onchange=()=>{if(face.value)editPort(rack,placement,port,{face:face.value});};
    panel.append(field('Label',label),field('Connector',type),field('Reached from',face));
    const xyz=document.createElement('div');xyz.className='port-xyz';
    for(const k of ['x','y','z']){const input=document.createElement('input');input.type='number';input.step='0.5';input.value=String(Math.round(port[k]*100)/100);input.setAttribute('aria-label',k.toUpperCase()+' (mm)');
      input.onchange=()=>{const v=Number(input.value);if(input.value===''||!Number.isFinite(v)){notify('Enter a number in millimetres.',true);return;}editPort(rack,placement,port,{[k]:v});};xyz.append(field(k.toUpperCase(),input));}
    panel.append(xyz,paragraph('X from the rack centre, Y depth behind the faceplate, Z above this equipment’s base (mm). Points '+(P.POINT_LABELS[port.points]||port.points)+'.'));
    const place=button(placingPort===port.key?'Cancel placing':'Set position by clicking the mesh',()=>armPortPlacement(port.key),placingPort===port.key?'primary':'secondary');
    panel.append(place);appendPortCableRow(panel,rack,placement,port);
    if(port.passThrough){const pair=ports.find(p=>p.id===port.passThrough);if(pair)panel.append(button('Go to the other face: '+pair.label,()=>selectPort(pair.key),'subtle'));}
    if(port.custom)panel.append(button('Remove port',()=>{P.setOverride(rack,placement.id,port.id,null);selectedPort=null;placingPort=null;markChanged();renderProperties();drawSoon();notify('Custom port removed from the draft. Save to keep the change.');},'subtle'));
    else if(port.edited)panel.append(button('Reset to the library values',()=>{P.setOverride(rack,placement.id,port.id,null);markChanged();renderProperties();drawSoon();notify('Port reset in the draft. Save to keep the change.');},'subtle'));
    panel.append(paragraph(port.note||'','muted'),paragraph('Planning data only. Connector fit, plug and cable access, and rear clearance are UNKNOWN.','notice'));
    host.append(panel);
  }
  // ---- Cables, exit points and outside endpoints (cable management Step 3; decisions in work/cable-management/Step3_Decisions.md).
  // Planning data only, kept in rack.cabling and saved only by the explicit Save. Lengths are planning estimates;
  // cable OD, stiffness, guide capacity and rear clearance are UNKNOWN. Nothing here reaches any STL.
  const EXIT_LABELS={'bottom-rear':'Bottom rear','top-rear':'Top rear',left:'Left side',right:'Right side'};
  const cableCtx=()=>({ports:window.LabRaxPorts,library:window.equipmentLibraryItems?.()||[]});
  const rackCables=rack=>rack?.cabling?.cables||[],rackExits=rack=>rack?.cabling?.exits||[],rackEndpoints=rack=>rack?.cabling?.endpoints||[];
  const cableSettings=rack=>({guide_warn_above:6,service_loop_m:.15,...(rack?.cabling?.settings||{})});
  const slotLabel=slot=>'U'+String(slot).padStart(2,'0');
  // Wizard ports come from the library, so upkeep waits until every wizard item in the rack has loaded
  // (otherwise their cable ends would look removed and be disconnected).
  function libraryReady(rack){const lib=window.equipmentLibraryItems?.()||[];return rack.placements.every(p=>!String(p.equipment).startsWith('eq-')||lib.some(i=>i.id===p.equipment));}
  function cableUpkeep(rack){if(window.LabRaxCables&&window.LabRaxPorts&&libraryReady(rack)){if(rackCables(rack).length)LabRaxCables.upkeep(rack,cableCtx());
    // Step 4 decision 12: an ignored suggestion comes back once the cables, guides or exits involved change.
    if(window.LabRaxCableSuggest&&rack.cabling?.settings?.ignored_suggestions)try{LabRaxCableSuggest.pruneIgnored(rack,suggestCtx());}catch(e){console.error(e);}}}
  // Page hook used by markChanged and Save (a no-op where the cable code isn't loaded, e.g. the page-logic tests).
  window.labRaxCableUpkeep=cableUpkeep;
  function setCables(rack,list){setCablingList(rack,'cables',list);markChanged();renderProperties();}
  function cableById(rack,id){return rackCables(rack).find(c=>c.id===id)||null;}
  function updateCable(rack,id,changes,{reroute=false}={}){
    const list=rackCables(rack).map(c=>c.id===id?{...c,...changes}:c),cable=list.find(c=>c.id===id);
    if(cable&&(reroute||cable.route?.mode!=='manual')&&window.LabRaxCables)cable.route={...LabRaxCables.autoRoute({...rack,cabling:{...rack.cabling,cables:list}},cable,cableCtx()),mode:cable.route?.mode==='manual'&&!reroute?'manual':'auto'};
    setCables(rack,list);
  }
  // Plain description of a cable end.
  function endText(rack,end){
    if(!end)return 'Unconnected';
    if(end.endpoint){const e=rackEndpoints(rack).find(x=>x.id===end.endpoint);return e?e.name+' ('+(LabRaxCables?.ENDPOINT_KINDS?.[e.kind]||e.kind)+', outside)':'Removed endpoint';}
    const placement=rack.placements.find(p=>p.id===end.allocation),port=placement&&window.LabRaxPorts?LabRaxPorts.portsFor(rack,placement,libraryItem(placement)).find(p=>p.id===end.port):null;
    return placement?(placement.assembly?.name||'Equipment')+' · '+(port?.label||end.port):'Removed equipment';
  }
  function portOfEnd(rack,end){if(!end?.allocation||!window.LabRaxPorts)return null;const placement=rack.placements.find(p=>p.id===end.allocation);return placement?LabRaxPorts.portsFor(rack,placement,libraryItem(placement)).find(p=>p.id===end.port)||null:null;}
  const sameEnd=(a,b)=>!!a&&!!b&&(a.endpoint?a.endpoint===b.endpoint:a.allocation===b.allocation&&a.port===b.port);
  function clearCableSelection(){selectedCable=null;selectedExit=null;facePrompt=null;}
  function selectCable(id){
    if(selectedSlot!==null){if(!leaveAssembly())return;selectedSlot=null;byId('mountWizard').hidden=true;setStage('rack');renderTree();}
    selectedPort=null;placingPort=null;selectedGuide=null;selectedExit=null;selectedCable=id;if(facePrompt?.cable!==id)facePrompt=null;showInspector('Setup');renderProperties();drawSoon();
  }
  function selectExit(id){
    if(selectedSlot!==null){if(!leaveAssembly())return;selectedSlot=null;byId('mountWizard').hidden=true;setStage('rack');renderTree();}
    selectedPort=null;placingPort=null;selectedGuide=null;selectedCable=null;selectedExit=id;showInspector('Setup');renderProperties();drawSoon();
  }
  // Connect mode (decision 1): start on a port, then click another port or pick an outside endpoint. Esc cancels.
  // With cable+end set it re-attaches that unconnected end instead of making a new cable (decision 14).
  function startConnect(from,opts={}){
    if(!window.LabRaxCables){notify('Cable routing is not available yet in this build.',true);return;}
    const rack=active();if(from&&LabRaxCables.portInUse(rack,from.allocation,from.port,null)){notify('That port already has a cable. Each port takes one cable.',true);return;}
    connecting={from,cable:opts.cable||null,end:opts.end||null};rackCanvas.classList.add('placing-port');renderProperties();drawSoon();
    notify(from?'Connecting: click another port in the rack view, or choose an outside endpoint in the panel. Esc cancels.':'Reattaching: click a port in the rack view, or choose an outside endpoint. Esc cancels.');
  }
  function cancelConnect(){if(!connecting)return;connecting=null;rackCanvas.classList.remove('placing-port');renderProperties();drawSoon();notify('Connect cancelled.');}
  function completeConnect(target){
    const rack=active(),L=window.LabRaxCables;if(!rack||!connecting||!L)return;const {from,cable:reattach,end}=connecting;
    if(target.allocation&&L.portInUse(rack,target.allocation,target.port,reattach)){notify('That port already has a cable. Each port takes one cable.',true);return;}
    if(reattach){const c=cableById(rack,reattach);if(!c){cancelConnect();return;}const other=end==='from'?c.to:c.from;if(sameEnd(other,target)){notify('Pick a different end from the cable’s other end.',true);return;}
      connecting=null;rackCanvas.classList.remove('placing-port');updateCable(rack,reattach,{[end]:target});askFaces(rack,reattach,[target]);selectCable(reattach);notify('Cable end reattached in the draft. Save to keep it.');return;}
    if(sameEnd(from,target)){notify('Pick a different port to connect to.',true);return;}
    // A keystone end alone says nothing about the cable: copy the cable already on the other side of that keystone,
    // else assume RJ45 (the usual keystone jack). Either way it is only a default the Cable panel can change.
    const ends=[from,target],types=ends.map(e=>portOfEnd(rack,e)?.type).filter(Boolean);
    const linkedType=()=>{for(const e of ends){const p=portOfEnd(rack,e);if(p?.type!=='keystone'||!p.passThrough)continue;const id=L.portInUse(rack,e.allocation,p.passThrough,null),t=id&&cableById(rack,id)?.type;if(t&&t!=='keystone')return t;}return null;};
    const type=types.find(t=>t!=='keystone'&&t!=='other')||(types.includes('keystone')?linkedType()||'rj45':types[0]||'other');
    const cable={id:'cable-'+Math.random().toString(36).slice(2,12),number:L.nextNumber(rack),type,service_loop_m:cableSettings(rack).service_loop_m,from,to:target,route:{mode:'auto',guides:[],exit:null},note:''};
    cable.route={...L.autoRoute({...rack,cabling:{...rack.cabling,cables:[...rackCables(rack),cable]}},cable,cableCtx()),mode:'auto'};
    connecting=null;rackCanvas.classList.remove('placing-port');setCables(rack,[...rackCables(rack),cable]);askFaces(rack,cable.id,[from,target]);selectCable(cable.id);
    notify(`Cable ${cable.number} added to the draft. Save to keep it. Length is a planning estimate.`);
  }
  // Decision 11: a port whose face is UNKNOWN is asked about once, when a cable is connected to it.
  function askFaces(rack,cableId,ends){const pending=ends.filter(e=>e?.allocation&&portOfEnd(rack,e)&&!portOfEnd(rack,e).face);facePrompt=pending.length?{cable:cableId,ends:pending}:null;}
  function answerFace(rack,cable,end,face){
    if(face)LabRaxPorts.setOverride(rack,end.allocation,end.port,{face},!!portOfEnd(rack,end)?.custom);
    facePrompt.ends=facePrompt.ends.filter(e=>!sameEnd(e,end));if(!facePrompt.ends.length)facePrompt=null;
    updateCable(rack,cable.id,face?{}:{face_assumed:'rear'});
  }
  function appendConnectBox(host,rack){
    if(!connecting)return;const box=document.createElement('div');box.className='port-panel connect-box';
    box.append(paragraph('CONNECTING','section-eyebrow'),paragraph(connecting.from?'From '+endText(rack,connecting.from)+'. Click another port in the rack view (all ports are shown), or choose an outside endpoint:':'Reattach the unconnected end: click a port in the rack view, or choose an outside endpoint:'));
    const eps=rackEndpoints(rack);
    if(eps.length){const s=document.createElement('select');s.setAttribute('aria-label','Outside endpoint');for(const e of eps){const o=document.createElement('option');o.value=e.id;o.textContent=e.name;s.append(o);}
      box.append(s,button('Connect to this endpoint',()=>completeConnect({endpoint:s.value}),'primary'));}
    else box.append(paragraph('No outside endpoints yet. Add one under Outside endpoints (select the rack, no slot) to run a cable out of the cabinet.','muted'));
    box.append(button('Cancel (Esc)',cancelConnect,'subtle'));host.append(box);
  }
  // Rack-level Setup: exit points, outside endpoints, cable list and settings, and the selected cable's panel.
  function appendCableSetup(host,rack){
    const L=window.LabRaxCables;
    const select=(list,value,label)=>{const s=document.createElement('select');s.setAttribute('aria-label',label);for(const [v,t] of list){const o=document.createElement('option');o.value=v;o.textContent=t;s.append(o);}s.value=String(value);return s;};
    const slotOptions=Array.from({length:rack.slots},(_,i)=>[String(i+1),slotLabel(i+1)]);
    // Exit points (decision 5): grommet markers only, no geometry.
    host.append(paragraph('EXIT POINTS','section-eyebrow'),paragraph('Where cables leave or enter the cabinet. Drawn as a grommet marker only; no hole is added to any STL.'));
    for(const x of rackExits(rack)){const row=document.createElement('div');row.className='guide-row'+(x.id===selectedExit?' selected':'');
      const name=button(EXIT_LABELS[x.position]+' · '+slotLabel(x.slot),()=>x.id===selectedExit?(selectedExit=null,renderProperties(),drawSoon()):selectExit(x.id),'guide-name');name.setAttribute('aria-pressed',String(x.id===selectedExit));
      const pos=select(Object.entries(EXIT_LABELS),x.position,'Exit position'),slot=select(slotOptions,x.slot,'Exit slot');
      const change=ch=>{const next={...x,...ch};if(rackExits(rack).some(o=>o.id!==x.id&&o.position===next.position&&o.slot===next.slot)){notify('There is already an exit there.',true);renderProperties();return;}setCablingList(rack,'exits',rackExits(rack).map(o=>o.id===x.id?next:o));markChanged();renderProperties();};
      pos.onchange=()=>change({position:pos.value});slot.onchange=()=>change({slot:Number(slot.value)});
      row.append(name,pos,slot,button('Remove',()=>{if(selectedExit===x.id)selectedExit=null;setCablingList(rack,'exits',rackExits(rack).filter(o=>o.id!==x.id));markChanged();renderProperties();notify('Exit point removed from the draft. Cables that used it were re-routed or marked “route changed”.');},'subtle'));host.append(row);}
    {const row=document.createElement('div');row.className='guide-row';const pos=select(Object.entries(EXIT_LABELS),'bottom-rear','New exit position'),slot=select(slotOptions,rack.slots,'New exit slot');
      row.append(pos,slot,button('Add exit point',()=>{const x={id:'exit-'+Math.random().toString(36).slice(2,12),position:pos.value,slot:Number(slot.value)};if(rackExits(rack).some(o=>o.position===x.position&&o.slot===x.slot)){notify('There is already an exit there.',true);return;}setCablingList(rack,'exits',[...rackExits(rack),x]);selectedExit=x.id;markChanged();renderProperties();notify('Exit point added to the draft. Save to keep it.');},'secondary'));host.append(row);}
    // Outside endpoints (decision 7): named once per rack, no 3D position.
    const kinds=Object.entries(L?.ENDPOINT_KINDS||{'wall-outlet':'Wall outlet',ups:'UPS',modem:'Modem / ONT','wall-jack':'Wall jack',desk:'Desk','other-rack':'Another rack',other:'Other'});
    host.append(paragraph('OUTSIDE ENDPOINTS','section-eyebrow'),paragraph('Things outside the cabinet that cables run to, such as a wall outlet or a modem. Drawn as a labelled arrow past the exit.'));
    for(const e of rackEndpoints(rack)){const row=document.createElement('div');row.className='guide-row';const kind=select(kinds,e.kind,'Endpoint kind'),name=document.createElement('input');name.type='text';name.maxLength=60;name.value=e.name;name.setAttribute('aria-label','Endpoint name');
      const change=ch=>{setCablingList(rack,'endpoints',rackEndpoints(rack).map(o=>o.id===e.id?{...o,...ch}:o));markChanged();renderProperties();};
      kind.onchange=()=>change({kind:kind.value});name.onchange=()=>{const v=name.value.trim();if(!v){notify('Give the endpoint a name.',true);name.value=e.name;return;}change({name:v});};
      const uses=rackCables(rack).filter(c=>c.from?.endpoint===e.id||c.to?.endpoint===e.id).length;
      row.append(kind,name,button('Remove',()=>{if(uses&&!confirm(`Remove “${e.name}”? ${uses} cable${uses>1?'s':''} will show that end as unconnected.`))return;setCablingList(rack,'endpoints',rackEndpoints(rack).filter(o=>o.id!==e.id));markChanged();renderProperties();},'subtle'));host.append(row);}
    {const row=document.createElement('div');row.className='guide-row';const kind=select(kinds,'wall-outlet','New endpoint kind'),name=document.createElement('input');name.type='text';name.maxLength=60;name.placeholder='e.g. Office wall outlet';name.setAttribute('aria-label','New endpoint name');
      row.append(kind,name,button('Add endpoint',()=>{const v=name.value.trim();if(!v){notify('Give the endpoint a name.',true);return;}setCablingList(rack,'endpoints',[...rackEndpoints(rack),{id:'endpoint-'+Math.random().toString(36).slice(2,12),kind:kind.value,name:v}]);markChanged();renderProperties();notify('Outside endpoint added to the draft. Save to keep it.');},'secondary'));host.append(row);}
    // Cables (decisions 9, 12, 13).
    host.append(paragraph('CABLES','section-eyebrow'),paragraph('Start a cable from a port: select its slot, pick the port, then Connect (or right-click the port in the rack view). Lengths are planning estimates; cable size and guide capacity are UNKNOWN.'));
    if(!L){host.append(paragraph('Cable routing is not available yet in this build.','notice'));return;}
    const settings=cableSettings(rack),setRow=document.createElement('div');setRow.className='guide-row cable-settings';
    const warn=document.createElement('input');warn.type='number';warn.min='1';warn.max='50';warn.step='1';warn.value=String(settings.guide_warn_above);warn.setAttribute('aria-label','Warn above this many cables per guide');
    const loop=document.createElement('input');loop.type='number';loop.min='0';loop.max='2';loop.step='0.05';loop.value=String(settings.service_loop_m);loop.setAttribute('aria-label','Default service loop per end (m)');
    const saveSetting=(k,v,lo,hi,int)=>{if(!Number.isFinite(v)||v<lo||v>hi||(int&&!Number.isInteger(v))){notify(`Use ${int?'a whole number':'a number'} from ${lo} to ${hi}.`,true);renderProperties();return;}rack.cabling={...(rack.cabling||{}),settings:{...settings,[k]:v}};markChanged();renderProperties();};
    warn.onchange=()=>saveSetting('guide_warn_above',Number(warn.value),1,50,true);loop.onchange=()=>saveSetting('service_loop_m',Number(loop.value),0,2,false);
    const lw=document.createElement('label');lw.className='port-field';lw.append('Warn above (cables per guide)',warn);const ll=document.createElement('label');ll.className='port-field';ll.append('Default service loop (m per end)',loop);
    const post=document.createElement('select');post.setAttribute('aria-label','Power post');for(const [v,t] of [['RR','Right rear (RR)'],['RL','Left rear (RL)']]){const o=document.createElement('option');o.value=v;o.textContent=t;post.append(o);}
    post.value=settings.power_post||'RR';post.onchange=()=>{rack.cabling={...(rack.cabling||{}),settings:{...settings,power_post:post.value}};markChanged();renderProperties();};
    const lp=document.createElement('label');lp.className='port-field';lp.append('Power post (data uses the other rear post)',post);
    setRow.append(lw,ll,lp);host.append(setRow,paragraph('The crowding number is your own setting, not a measured guide capacity (UNKNOWN). Going over it warns and blocks nothing.','muted'));
    for(const g of L.crowded(rack)){const guide=rackGuides(rack).find(x=>x.id===g);if(guide)host.append(paragraph(`Guide ${guideLabel(guide)} carries ${L.guideLoad(rack)[g]} cables, above your setting of ${settings.guide_warn_above}.`,'notice'));}
    const ctx=cableCtx(),list=[...rackCables(rack)].sort((a,b)=>String(a.number).localeCompare(String(b.number),undefined,{numeric:true}));
    if(!list.length)host.append(paragraph('No cables yet.'));
    for(const c of list){const row=document.createElement('div');row.className='guide-row cable-row'+(c.id===selectedCable?' selected':'');const est=L.estimate(rack,c,ctx),flag=L.warnings(rack,c,ctx).length?' ⚠':'';
      const name=button(`${c.number} · ${endText(rack,c.from)} → ${endText(rack,c.to)}${est.complete?' · ≈ '+est.length_m.toFixed(1)+' m':''}${flag}`,()=>c.id===selectedCable?(clearCableSelection(),renderProperties(),drawSoon()):selectCable(c.id),'guide-name');
      name.style.setProperty('--port-color',L.cableColor(c));name.setAttribute('aria-pressed',String(c.id===selectedCable));row.append(name);host.append(row);
      if(c.id===selectedCable)appendCablePanel(host,rack,c);}
  }
  function appendCablePanel(host,rack,cable){
    const L=LabRaxCables,ctx=cableCtx(),panel=document.createElement('div');panel.className='port-panel cable-panel';panel.setAttribute('aria-label','Cable');
    const field=(label,control)=>{const l=document.createElement('label');l.className='port-field';l.append(label,control);return l;};
    const head=document.createElement('h3');head.textContent='Cable '+cable.number;panel.append(paragraph('CABLE','section-eyebrow'),head);
    // Decision 11: one-time question for ports whose face is UNKNOWN.
    if(facePrompt?.cable===cable.id)for(const end of facePrompt.ends){const port=portOfEnd(rack,end);if(!port)continue;const ask=document.createElement('div');ask.className='face-prompt';
      ask.append(paragraph(`Which side does this cable reach “${port.label}” from?`),button('Front',()=>answerFace(rack,cable,end,'front'),'secondary'),button('Rear',()=>answerFace(rack,cable,end,'rear'),'secondary'),button('Leave UNKNOWN',()=>answerFace(rack,cable,end,null),'subtle'));panel.append(ask);}
    const number=document.createElement('input');number.type='text';number.maxLength=12;number.value=cable.number;
    number.onchange=()=>{const v=number.value.trim();if(!v||rackCables(rack).some(c=>c.id!==cable.id&&c.number===v)){notify('Cable numbers must be unique and not empty.',true);number.value=cable.number;return;}updateCable(rack,cable.id,{number:v});};
    const type=document.createElement('select');for(const [k,t] of Object.entries(window.LabRaxPorts?.TYPES||{})){const o=document.createElement('option');o.value=k;o.textContent=t.label;type.append(o);}type.value=cable.type;type.onchange=()=>updateCable(rack,cable.id,{type:type.value});
    const color=document.createElement('input');color.type='color';color.value=L.cableColor(cable);color.onchange=()=>updateCable(rack,cable.id,{color:color.value});
    const colorRow=document.createElement('div');colorRow.className='guide-row';colorRow.append(field('Colour',color));if(cable.color)colorRow.append(button('Use type colour',()=>{const {color:_,...rest}=cable;setCables(rack,rackCables(rack).map(c=>c.id===cable.id?rest:c));},'subtle'));
    const loop=document.createElement('input');loop.type='number';loop.min='0';loop.max='2';loop.step='0.05';loop.value=String(cable.service_loop_m??cableSettings(rack).service_loop_m);
    loop.onchange=()=>{const v=Number(loop.value);if(!Number.isFinite(v)||v<0||v>2){notify('Service loop is 0 to 2 m.',true);return;}updateCable(rack,cable.id,{service_loop_m:v});};
    const note=document.createElement('textarea');note.maxLength=200;note.rows=2;note.value=cable.note||'';note.onchange=()=>updateCable(rack,cable.id,{note:note.value.slice(0,200)});
    // Step 4 decisions 1 and 6: what the cable carries (default from its type) and whether it is unplugged often.
    const SG=window.LabRaxCableSuggest,without=key=>{const {[key]:_,...rest}=cable;setCables(rack,rackCables(rack).map(c=>c.id===cable.id?rest:c));};
    const carries=document.createElement('select');{const {carries:_,...plain}=cable,auto=SG?SG.carries(rack,plain,suggestCtx()):null;
      for(const [v,t] of [['','From type'+(auto?' ('+auto+')':'')],['power','Power'],['data','Data']]){const o=document.createElement('option');o.value=v;o.textContent=t;carries.append(o);}}
    carries.value=cable.carries||'';carries.onchange=()=>carries.value?updateCable(rack,cable.id,{carries:carries.value}):without('carries');
    const often=document.createElement('input');often.type='checkbox';often.checked=cable.unplug_often===true;often.onchange=()=>often.checked?updateCable(rack,cable.id,{unplug_often:true}):without('unplug_often');
    const oftenLabel=document.createElement('label');oftenLabel.className='port-field cable-often';oftenLabel.append(often,' Unplugged often');
    panel.append(field('Number',number),field('Type',type),colorRow,field('Carries (power or data)',carries),oftenLabel,field('Service loop (m per end)',loop),field('Note',note));
    // Ends.
    for(const key of ['from','to']){const end=cable[key],row=document.createElement('div');row.className='cable-end';row.append(paragraph((key==='from'?'From: ':'To: ')+endText(rack,end)));
      if(end?.allocation&&rack.placements.some(p=>p.id===end.allocation))row.append(button('Select port',()=>selectPort(end.allocation+'/'+end.port),'subtle'));
      if(end?.endpoint&&rackEndpoints(rack).length>1){const s=document.createElement('select');s.setAttribute('aria-label','Outside endpoint');for(const e of rackEndpoints(rack)){const o=document.createElement('option');o.value=e.id;o.textContent=e.name;s.append(o);}s.value=end.endpoint;s.onchange=()=>updateCable(rack,cable.id,{[key]:{endpoint:s.value}});row.append(s);}
      if(!end)row.append(button('Reattach…',()=>startConnect(null,{cable:cable.id,end:key}),'secondary'));
      panel.append(row);}
    // Route (decisions 3, 4, 6).
    const route=cable.route||{mode:'auto',guides:[],exit:null},manual=route.mode==='manual';
    panel.append(paragraph('ROUTE · '+(manual?'manual (kept as you set it)':'automatic (nearest guides on one post)'),'section-eyebrow'));
    if(cable.route_changed)panel.append(paragraph('Route changed: a guide or exit it used was moved or removed.','notice'),button('OK, I’ve looked',()=>{const {route_changed:_,...rest}=cable;setCables(rack,rackCables(rack).map(c=>c.id===cable.id?rest:c));},'subtle'));
    const setManual=guides=>updateCable(rack,cable.id,{route:{...route,mode:'manual',guides}});
    route.guides.forEach((gid,i)=>{const g=rackGuides(rack).find(x=>x.id===gid);const row=document.createElement('div');row.className='guide-row';
      const up=button('▲',()=>{const a=[...route.guides];[a[i-1],a[i]]=[a[i],a[i-1]];setManual(a);},'secondary'),down=button('▼',()=>{const a=[...route.guides];[a[i+1],a[i]]=[a[i],a[i+1]];setManual(a);},'secondary');up.disabled=i===0;down.disabled=i===route.guides.length-1;
      row.append(paragraph((i+1)+'. Guide '+(g?guideLabel(g):'(removed)')),up,down,button('✕',()=>setManual(route.guides.filter(x=>x!==gid)),'subtle'));panel.append(row);});
    if(!route.guides.length)panel.append(paragraph('No guides on this route.','muted'));
    const spare=rackGuides(rack).filter(g=>!route.guides.includes(g.id));
    if(spare.length){const row=document.createElement('div');row.className='guide-row';const s=document.createElement('select');s.setAttribute('aria-label','Guide to add');for(const g of spare){const o=document.createElement('option');o.value=g.id;o.textContent=guideLabel(g);s.append(o);}
      row.append(s,button('Add guide to route',()=>setManual([...route.guides,s.value]),'secondary'));panel.append(row);}
    if(cable.from?.endpoint||cable.to?.endpoint){const s=document.createElement('select');s.setAttribute('aria-label','Exit point');const none=document.createElement('option');none.value='';none.textContent=rackExits(rack).length?'No exit':'No exit points yet';s.append(none);
      for(const x of rackExits(rack)){const o=document.createElement('option');o.value=x.id;o.textContent=EXIT_LABELS[x.position]+' · '+slotLabel(x.slot);s.append(o);}s.value=route.exit||'';
      s.onchange=()=>updateCable(rack,cable.id,{route:{...route,mode:'manual',exit:s.value||null}});panel.append(field('Leaves through',s));}
    if(manual)panel.append(button('Back to automatic route',()=>updateCable(rack,cable.id,{route:{mode:'auto',guides:[],exit:null}},{reroute:true}),'subtle'));
    // Length estimate (decision 9).
    const est=L.estimate(rack,cable,ctx);
    panel.append(paragraph(est.complete?`Length ≈ ${est.length_m.toFixed(1)} m${est.to_exit?(rackExits(rack).some(x=>x.id===cable.route?.exit)?' to the exit':' to the last guide (no exit yet)'):''} (planning estimate: route ${(est.route_mm/1000).toFixed(2)} m plus service loops, rounded up).`:'Length: not estimated until both ends are connected.'));
    for(const w of L.warnings(rack,cable,ctx))panel.append(paragraph('⚠ '+w,'notice'));
    const linked=L.linkedCable(rack,cable,ctx);if(linked){const other=cableById(rack,linked);if(other)panel.append(button('Linked keystone cable: '+other.number,()=>selectCable(linked),'subtle'));}
    panel.append(button('Delete cable',()=>{if(!confirm('Delete cable '+cable.number+' from the draft?'))return;clearCableSelection();setCables(rack,rackCables(rack).filter(c=>c.id!==cable.id));notify('Cable deleted from the draft. Save to keep the change.');},'subtle'),
      paragraph('Planning data only. Real cable length depends on cable size, stiffness and connector depth, which are UNKNOWN.','muted'));
    host.append(panel);
  }
  // Port panel addition: Connect, or the cable already on the port.
  function appendPortCableRow(host,rack,placement,port){
    if(!window.LabRaxCables)return;const used=LabRaxCables.portInUse(rack,placement.id,port.id,null),cable=used?cableById(rack,used):null;
    if(cable)host.append(button('Cable '+cable.number+' · select',()=>selectCable(cable.id),'secondary'));
    else host.append(button(connecting?'Connecting… (Esc cancels)':'Connect a cable',()=>connecting?cancelConnect():startConnect({allocation:placement.id,port:port.id}),'primary'));
  }
  // ---- Cable suggestions (cable management Step 4; decisions in work/cable-management/Step4_Decisions.md).
  // Advice only: nothing here blocks Save or says a real cable or guide fits. Apply changes only the unsaved draft
  // (never saves) and the last Apply can be undone while the cabling hasn't changed since.
  const suggestCtx=()=>({...cableCtx(),cables:window.LabRaxCables});
  function cableSuggestions(rack,opts){const S=window.LabRaxCableSuggest;if(!S||!window.LabRaxCables||!window.LabRaxPorts||!rack||!libraryReady(rack))return null;
    try{return S.suggestions(rack,suggestCtx(),opts);}catch(e){console.error(e);return null;}}
  function setCablesView(on){cablesView=on;byId('toggleCablesView').setAttribute('aria-pressed',String(cablesView));byId('toggleRackPanels').disabled=cablesView;drawSoon();}
  function startShowMe(s){const inv=s.involves||{},turnedOn=showMe?showMe.turnedOn:!cablesView;
    showMe={id:s.id,title:s.title,cables:new Set(inv.cables||[]),guides:new Set(inv.guides||[]),ports:new Set(inv.ports||[]),exits:new Set(inv.exits||[]),turnedOn};
    if(!cablesView)setCablesView(true);renderReview();drawSoon();rackCanvas.scrollIntoView?.({block:'nearest'});notify('Showing “'+s.title+'” in the rack view. Done or Esc clears it.');}
  function clearShowMe(quiet){if(!showMe)return;const off=showMe.turnedOn;showMe=null;if(off&&cablesView)setCablesView(false);drawSoon();if(!quiet)renderReview();}
  const canUndo=rack=>!!lastApply&&rack?.id===lastApply.rack&&JSON.stringify(rack.cabling||null)===lastApply.after;
  function applyCableSuggestion(rack,s){
    const S=window.LabRaxCableSuggest;if(!S)return;const before=rack.cabling?JSON.parse(JSON.stringify(rack.cabling)):null;
    let r;try{r=S.applySuggestion(rack,s,suggestCtx());}catch(e){console.error(e);r={ok:false,message:''};}
    if(!r.ok){notify(r.message||'That suggestion no longer applies. The list was refreshed.',true);renderReview();return;}
    clearShowMe(true);sceneCacheKey='';markChanged();lastApply={rack:rack.id,before,after:JSON.stringify(rack.cabling||null),label:s.title};render();
    notify('Applied in the draft: '+s.title+'. Not saved; Save to keep it.');const undo=button('Undo',undoApply,'subtle');undo.id='undoApply';byId('message').after(undo);
  }
  function undoApply(){const rack=active();
    if(!canUndo(rack)){lastApply=null;notify('Undo is no longer available: the cabling changed after that Apply.',true);renderReview();return;}
    if(lastApply.before)rack.cabling=lastApply.before;else delete rack.cabling;lastApply=null;sceneCacheKey='';markChanged();render();notify('Apply undone in the draft.');}
  function suggestionRow(rack,s,ignored){
    const S=window.LabRaxCableSuggest,row=document.createElement('div');row.className='suggestion suggestion-'+s.level+(showMe?.id===s.id?' showing':'');
    const head=document.createElement('strong');head.textContent=({suggest:'SUGGESTION',guidance:'GUIDANCE',info:'INFO'}[s.level]||'SUGGESTION')+' · '+s.title;row.append(head,paragraph(s.detail));
    const acts=document.createElement('div'),inv=s.involves||{};acts.className='suggestion-actions';
    if(['cables','guides','ports','exits'].some(k=>inv[k]?.length))acts.append(button(showMe?.id===s.id?'Done':'Show me',()=>showMe?.id===s.id?clearShowMe():startShowMe(s),'secondary'));
    if(!ignored&&s.apply)acts.append(button(s.applyLabel||'Apply',()=>applyCableSuggestion(rack,s),'primary'));
    acts.append(ignored?button('Bring back',()=>{S.unignore(rack,s.id);markChanged();renderReview();notify('Suggestion brought back in the draft. Save to keep that.');},'subtle')
      :button('Ignore',()=>{S.ignore(rack,s);if(showMe?.id===s.id)clearShowMe(true);markChanged();renderReview();notify('Suggestion ignored in the draft. Save to keep that; it comes back if the cables involved change.');},'subtle'));
    row.append(acts);return row;
  }
  function appendCableSuggestions(host,rack){
    // Only drawn in Review; leaving Review clears any Show me highlight.
    if(stage!=='review'){if(showMe)clearShowMe(true);return;}
    const box=document.createElement('div');box.className='cable-suggestions';box.id='cableSuggestions';const head=document.createElement('h3');head.textContent='Cable suggestions';box.append(head);host.append(box);
    if(!window.LabRaxCableSuggest){box.append(paragraph('Cable suggestions are not available in this build yet.','notice'));return;}
    const all=cableSuggestions(rack,{includeIgnored:true});if(all===null){box.append(paragraph('Waiting for the equipment library to load…'));return;}
    const shown=all.filter(s=>!s.ignored),ignored=all.filter(s=>s.ignored);if(shown.length)head.textContent+=' · '+shown.length;
    box.append(paragraph('Advice for the planned cables, guides and exits. Nothing here blocks Save or says a real cable or guide fits: guide capacity, bend tolerance and real cable size are UNKNOWN, and bend figures are generic guidance on nominal sizes. Apply changes only the unsaved draft.','muted'));
    if(canUndo(rack))box.append(button('Undo last Apply: '+lastApply.label,undoApply,'secondary'));
    if(showMe){const on=document.createElement('div');on.className='suggestion-showing';on.append(paragraph('Showing in the rack view: '+showMe.title),button('Done (Esc)',()=>clearShowMe(),'subtle'));box.append(on);}
    if(!shown.length)box.append(paragraph(rackCables(rack).length?'No suggestions right now.':'No cables planned yet. Add cables in Setup (select the rack, no slot) to get routing suggestions.'));
    for(const s of shown)box.append(suggestionRow(rack,s,false));
    if(ignored.length){const d=document.createElement('details'),sum=document.createElement('summary');sum.textContent='Show ignored ('+ignored.length+')';d.append(sum);for(const s of ignored)d.append(suggestionRow(rack,s,true));box.append(d);}
  }
  // ---- Wiring sheet, cable schedule and labels (cable management Step 5; decisions in work/cable-management/Step5_Decisions.md).
  // Made from the SAVED rack only (fetched from the server; "Save first" while the draft has changes). Planning documents:
  // nothing here saves, prints or touches any STL. Lengths are estimates; guide capacity and cable fit are UNKNOWN.
  let sheetPaper='letter',sheet3d=false;
  try{if(localStorage.getItem('labrax-sheet-paper')==='a4')sheetPaper='a4';}catch(e){}
  const sheetUnsaved=()=>layoutDirty||dirty||savingLayout||artworkPending>0;
  const sheetCtx=()=>({...cableCtx(),cables:window.LabRaxCables,suggest:window.LabRaxCableSuggest,sheet:window.LabRaxCableSheet});
  const two=n=>String(n).padStart(2,'0');
  async function savedRackForSheet(){
    if(sheetUnsaved())throw Error('Save first: the wiring sheet is made from the saved rack, so unsaved changes would be missing.');
    const current=active();if(!current)throw Error('Select a rack first.');
    const doc=await api('rack-workspace'),rack=doc.racks.find(r=>r.id===current.id);
    if(!rack)throw Error('This rack has not been saved yet. Save first.');
    if(!libraryReady(rack))throw Error('Wait for the equipment library to finish loading, then try again.');
    const d=new Date(),made=d.getFullYear()+'-'+two(d.getMonth()+1)+'-'+two(d.getDate())+' '+two(d.getHours())+':'+two(d.getMinutes()),version=String(doc.generation||'unknown').slice(0,8);
    return {rack,stamp:'Saved version '+version+' · made '+made,savedAt:'version '+version+' (made '+made+')',base:LabRaxCableSheetView.safeName(rack.name)};
  }
  function downloadUrl(url,name){const a=document.createElement('a');a.href=url;a.download=name;a.click();}
  function downloadText(text,name,type){const url=URL.createObjectURL(new Blob([text],{type}));downloadUrl(url,name);setTimeout(()=>URL.revokeObjectURL(url),1000);}
  // The tab is opened inside the click (before any await) so pop-up blockers allow it; the page is filled in afterwards.
  // If the browser blocks it anyway, the same page downloads as an .html file to open and print.
  function fillTab(tab,html,name){if(!tab){downloadText(html,name,'text/html;charset=utf-8');return false;}const url=URL.createObjectURL(new Blob([html],{type:'text/html'}));tab.location.href=url;setTimeout(()=>URL.revokeObjectURL(url),120000);return true;}
  // Front and rear 3D views in Cables mode, drawn straight into the rack canvas and restored afterwards (decision 5).
  function sheetSnapshots(){
    if(byId('rackView').hidden||!sceneRenderer||!sourceMeshes)throw Error('The 3D views need the rack view on screen. Open it, or untick Include 3D views.');
    const keep={cablesView,perspectiveCamera,yaw,pitch,zoom,panX,panY,showRearLabels,showMe,selectedCable,selectedExit,selectedGuide,selectedPort,viewMode},shots=[];
    try{
      showMe=null;selectedCable=selectedExit=selectedGuide=selectedPort=null;cablesView=true;perspectiveCamera=false;pitch=0;zoom=1;panX=panY=0;
      for(const [label,y,rear] of [['Front',0,false],['Rear',Math.PI,true]]){yaw=y;showRearLabels=rear;viewMode=rear?'rear':'front';drawRack();shots.push({label,src:rackCanvas.toDataURL('image/png')});}
    }finally{({cablesView,perspectiveCamera,yaw,pitch,zoom,panX,panY,showRearLabels,showMe,selectedCable,selectedExit,selectedGuide,selectedPort,viewMode}=keep);sceneCacheKey='';drawSoon();}
    return shots;
  }
  async function runSheet(kind){
    const tab=kind==='page'||kind==='labels'?window.open('','_blank'):null;
    try{
      const S=window.LabRaxCableSheet,V=window.LabRaxCableSheetView,{rack,stamp,savedAt,base}=await savedRackForSheet(),ctx=sheetCtx();
      if(kind==='svg'){downloadText(V.sheetSvg(rack,ctx,{stamp}),base+'-wiring-sheet.svg','image/svg+xml');notify('Wiring sheet SVG downloaded, made from the saved rack. Lengths are planning estimates.');}
      else if(kind==='csv'){downloadText(S.csv(rack,ctx,{savedAt}),base+'-cable-schedule.csv','text/csv;charset=utf-8');notify('Cable schedule CSV downloaded, made from the saved rack. Lengths are planning estimates.');}
      else if(kind==='png'){for(const s of sheetSnapshots())downloadUrl(s.src,base+'-'+s.label.toLowerCase()+'-3d.png');notify('Front and rear 3D views downloaded as PNG. They are previews, not a fit check.');}
      else if(kind==='page'){const images=sheet3d?sheetSnapshots():null;const shown=fillTab(tab,V.sheetPage({svg:V.sheetSvg(rack,ctx,{stamp}),title:(rack.name||'Rack')+' · wiring sheet',paper:sheetPaper,images}),base+'-wiring-sheet.html');notify(shown?'Printable wiring sheet opened in a new tab. Print or save it as PDF from there.':'The browser blocked the new tab, so the printable sheet downloaded as an HTML file. Open it to print or save as PDF.');}
      else if(kind==='labels'){const labels=S.labels(rack,ctx),shown=fillTab(tab,V.labelsPage({labels,title:(rack.name||'Rack')+' · cable labels',paper:sheetPaper,heading:(rack.name||'Rack')+' · cable labels · '+stamp+' · one per cable end · cut along the dashes'}),base+'-cable-labels.html');notify(labels.length+' cable labels '+(shown?'opened in a new tab.':'downloaded as an HTML file (the browser blocked the new tab). Open it to print.'));}
    }catch(e){tab?.close();notify(e.message,true);}
  }
  // Keeps the card's "Save first" state in step with the draft (called from updateSaveStatus).
  function refreshSheetState(){const unsaved=sheetUnsaved();
    for(const box of [byId('wiringSheet'),byId('partsOrder')]){if(!box)continue;box.querySelector('.sheet-save-first').hidden=!unsaved;
      for(const b of box.querySelectorAll('button[data-sheet]'))b.textContent=unsaved?'Save first':b.dataset.label;}}
  // Parts order (cable inventory; PROPOSED defaults in work/cable-management/Parts_Order_Decisions.md): made from the
  // SAVED rack like the wiring sheet. A shopping list only: no prices, links or purchases; lengths are estimates.
  async function runPartsOrder(kind,box){
    try{
      const I=window.LabRaxCableInventory,{rack,savedAt,base}=await savedRackForSheet(),ctx=sheetCtx();
      if(kind==='csv'){downloadText(I.csv(rack,ctx,{savedAt}),base+'-parts-order.csv','text/csv;charset=utf-8');notify('Parts order CSV downloaded, made from the saved rack. Lengths are planning estimates.');return;}
      const rows=I.items(rack,ctx),out=box.querySelector('.parts-table');out.replaceChildren();
      if(!rows.length){out.append(paragraph('Nothing to order yet: no cables, keystones or guides in the saved rack.','muted'));return;}
      const t=document.createElement('table');t.className='parts-order';const hr=t.insertRow();for(const h of ['Item','Qty','Buy or print','Cables','Notes']){const th=document.createElement('th');th.textContent=h;hr.append(th);}
      for(const r of rows){const tr=t.insertRow();for(const v of [r.item,r.quantity,r.source,r.cables.join(' '),r.notes.join('; ')])tr.insertCell().textContent=String(v);}
      out.append(t,paragraph('Made from '+savedAt+'.','muted'));
    }catch(e){notify(e.message,true);}
  }
  function appendPartsOrder(host,rack){
    if(stage!=='review')return;
    const box=document.createElement('div');box.className='cable-suggestions wiring-sheet';box.id='partsOrder';const head=document.createElement('h3');head.textContent='Parts order';box.append(head);host.append(box);
    if(!window.LabRaxCableInventory||!window.LabRaxCableSheetView){box.append(paragraph('The parts order is not available in this build yet.','notice'));return;}
    box.append(paragraph('Cables by type and stock length, keystone jacks and cable guides to print, made from the saved rack. '+LabRaxCableInventory.LIMITS,'muted'));
    box.append(paragraph('Save first: the parts order is made from the saved rack only, so unsaved changes would be missing.','notice sheet-save-first'));
    const acts=document.createElement('div');acts.className='suggestion-actions';
    const act=(label,kind,cls)=>{const b=button(label,()=>runPartsOrder(kind,box),cls);b.dataset.sheet=kind;b.dataset.label=label;return b;};
    const out=document.createElement('div');out.className='parts-table';
    acts.append(act('Show parts list','show','primary'),act('Parts order (CSV)','csv','secondary'));box.append(acts,out);
    refreshSheetState();
  }
  window.labRaxSheetState=refreshSheetState;
  function appendWiringSheet(host,rack){
    if(stage!=='review')return;
    const box=document.createElement('div');box.className='cable-suggestions wiring-sheet';box.id='wiringSheet';const head=document.createElement('h3');head.textContent='Wiring sheet';box.append(head);host.append(box);
    if(!window.LabRaxCableSheet||!window.LabRaxCableSheetView){box.append(paragraph('The wiring sheet is not available in this build yet.','notice'));return;}
    const n=rackCables(rack).length;head.textContent+=' · '+n+' cable'+(n===1?'':'s');
    box.append(paragraph('Front and rear schematic, cable schedule (CSV) and wrap labels, made from the saved rack. Lengths are planning estimates; guide capacity, cable fit and bend tolerance are UNKNOWN. Nothing here saves or changes any STL, and the app never prints: you print or save as PDF from the browser.','muted'));
    const notice=paragraph('Save first: these are made from the saved rack only, so unsaved changes would be missing.','notice sheet-save-first');box.append(notice);
    const opts=document.createElement('div');opts.className='sheet-options';
    const paper=document.createElement('select');paper.setAttribute('aria-label','Paper size');for(const [k,p] of Object.entries(LabRaxCableSheetView.PAPER)){const o=document.createElement('option');o.value=k;o.textContent=p.label;paper.append(o);}
    paper.value=sheetPaper;paper.onchange=()=>{sheetPaper=paper.value;try{localStorage.setItem('labrax-sheet-paper',sheetPaper);}catch(e){}};
    const pl=document.createElement('label');pl.className='port-field';pl.append('Paper',paper);
    const tick=document.createElement('input');tick.type='checkbox';tick.checked=sheet3d;const tl=document.createElement('label');tl.className='sheet-tick';tl.append(tick,' Include 3D views');
    const acts=document.createElement('div');acts.className='suggestion-actions';
    const act=(label,kind,cls)=>{const b=button(label,()=>runSheet(kind),cls);b.dataset.sheet=kind;b.dataset.label=label;return b;};
    const png=act('3D views (PNG)','png','secondary');png.hidden=!sheet3d;
    tick.onchange=()=>{sheet3d=tick.checked;png.hidden=!sheet3d;};
    opts.append(pl,tl);acts.append(act('Open printable sheet','page','primary'),act('Sheet (SVG)','svg','secondary'),act('Schedule (CSV)','csv','secondary'),act('Labels','labels','secondary'),png);
    box.append(opts,acts);if(!n)box.append(paragraph('No cables planned yet: the sheet will show the rack, guides and exits only.','muted'));
    refreshSheetState();
  }
  // Scene parts for cables and exit grommets; cables show in Cables mode, the Rear view, or with "Cable runs" on.
  const GUIDE_X=118.26,PITCH_MM=44.45;
  const zmid=(rack,slot)=>(rack.slots-slot)*PITCH_MM+PITCH_MM/2;
  function exitAnchor(rack,x){return x.position==='bottom-rear'?[0,250,-10]:x.position==='top-rear'?[0,250,rack.slots*PITCH_MM+10]:[x.position==='left'?-140:140,220,zmid(rack,x.slot)];}
  function guideAnchor(rack,g){return [g.post[1]==='L'?-GUIDE_X:GUIDE_X,g.post[0]==='R'?254:-14,zmid(rack,g.slot)];}
  const cablesShown=()=>cablesView||viewMode==='rear'||showCableRuns;
  function cableParts(rack){
    const L=window.LabRaxCables,V=window.LabRaxCableView;if(!L||!V||!sourceMeshes?.['exit-grommet'])return [];const parts=[],ctx=cableCtx(),show=cablesShown();
    for(const x of rackExits(rack))if(show||x.id===selectedExit)parts.push({key:'exit-grommet',R:V.exitRotation(x.position),t:exitAnchor(rack,x),kind:'exit',exit:x.id,selected:showMe?showMe.exits.has(x.id):x.id===selectedExit,dim:!!showMe&&!showMe.exits.has(x.id)});
    if(!show&&!selectedCable)return parts;
    const cables=rackCables(rack),diameter=c=>L.TYPE_STYLE[c.type]?.diameter_mm||4,offsets=V.bundleOffsets(cables.map(c=>({id:c.id,guides:c.route?.guides||[],diameter:diameter(c)})));
    const linked=selectedCable?L.linkedCable(rack,cableById(rack,selectedCable)||{},ctx):null;
    for(const c of cables){
      if(!show&&c.id!==selectedCable&&c.id!==linked)continue;
      const a=L.endAnchor(rack,c.from,ctx),b=L.endAnchor(rack,c.to,ctx),exit=rackExits(rack).find(x=>x.id===c.route?.exit);
      // Guides are stored in from → to order (cable-routes.js autoRoute).
      const guides=(c.route?.guides||[]).map(gid=>{const g=rackGuides(rack).find(x=>x.id===gid);if(!g)return null;const p=guideAnchor(rack,g);p[0]+=offsets[c.id]?.[gid]||0;return p;}).filter(Boolean);
      // A cable to an outside endpoint runs through its exit and a short way past it (the 2D arrow continues from there).
      const out=exit&&(c.from?.endpoint||c.to?.endpoint)?(()=>{const e=exitAnchor(rack,exit),n=V.EXIT_NORMAL[exit.position];return [e,e.map((v,i)=>v+n[i]*40)];})():null;
      const pts=c.from?.endpoint?[...(out?out.slice().reverse():[]),...guides,...(b?[b]:[])]:[...(a?[a]:[]),...guides,...(c.to?.endpoint&&out?out:[]),...(b?[b]:[])];
      if(pts.length<2)continue;const r=diameter(c)/2,path=V.sagPath(pts),mesh=V.tubeMesh(path,r);
      parts.push({key:'cable-'+V.geometryKey(path,r),mesh,R:[1,0,0,0,1,0,0,0,1],t:[0,0,0],kind:'cable',cable:c.id,tint:L.cableColor(c),lit:showMe?showMe.cables.has(c.id):!!selectedCable&&(c.id===selectedCable||c.id===linked),dim:showMe?!showMe.cables.has(c.id):!!selectedCable&&c.id!==selectedCable&&c.id!==linked});
    }
    return parts;
  }
  // 2D overlay: a labelled arrow past each exit for cables that go to an outside endpoint, and cable numbers.
  function drawCableLabels(ctx,rack,project){
    const L=window.LabRaxCables,V=window.LabRaxCableView;if(!L||!V||!(cablesShown()||selectedCable))return;
    for(const c of rackCables(rack)){
      if(!cablesShown()&&c.id!==selectedCable)continue;
      const endpoint=c.from?.endpoint||c.to?.endpoint,exit=rackExits(rack).find(x=>x.id===c.route?.exit),color=L.cableColor(c);
      ctx.save();ctx.font='600 11px system-ui';ctx.fillStyle=color;ctx.strokeStyle=color;ctx.lineWidth=2;
      if(endpoint&&exit){const ep=rackEndpoints(rack).find(e=>e.id===endpoint),n=V.EXIT_NORMAL[exit.position],e=exitAnchor(rack,exit),p0=project(e.map((v,i)=>v+n[i]*40)),p1=project(e.map((v,i)=>v+n[i]*80));
        const ang=Math.atan2(p1[1]-p0[1],p1[0]-p0[0]);ctx.beginPath();ctx.moveTo(p0[0],p0[1]);ctx.lineTo(p1[0],p1[1]);ctx.stroke();
        ctx.beginPath();ctx.moveTo(p1[0],p1[1]);ctx.lineTo(p1[0]-9*Math.cos(ang-.45),p1[1]-9*Math.sin(ang-.45));ctx.lineTo(p1[0]-9*Math.cos(ang+.45),p1[1]-9*Math.sin(ang+.45));ctx.closePath();ctx.fill();
        const text=c.number+' → '+(ep?.name||'outside'),tw=ctx.measureText(text).width,W=rackCanvas.clientWidth,H=rackCanvas.clientHeight;
        // Keep the label inside the view (a bottom exit's arrow can run off the canvas in the front/rear views).
        const tx=Math.min(W-tw/2-6,Math.max(tw/2+6,p1[0]+14*Math.cos(ang))),ty=Math.min(H-8,Math.max(14,p1[1]+14*Math.sin(ang)+4));
        ctx.textAlign='center';ctx.fillStyle='#0d131b';ctx.globalAlpha=.75;ctx.fillRect(tx-tw/2-4,ty-12,tw+8,16);ctx.globalAlpha=1;ctx.fillStyle=color;ctx.fillText(text,tx,ty);}
      else{const a=L.endAnchor(rack,c.from,cableCtx())||L.endAnchor(rack,c.to,cableCtx());if(a){const p=project(a);ctx.textAlign='left';ctx.fillText(c.number,p[0]+6,p[1]-6);}}
      ctx.restore();
    }
  }
  // Move the support extension at joint j on one side by ±1U (the segments either side grow/shrink).
  function moveExtension(side,j,dir){
    const rack=active();if(!rack||rack.layout_locked)return;const levels=[...sideLevels(rack,side)];
    const below=levels[j]+dir,above=levels[j+1]-dir;
    if(below<1||below>5||above<1||above>5){notify('A post segment must stay between 1U and 5U.',true);return;}
    levels[j]=below;levels[j+1]=above;rack.post_levels={left:sideLevels(rack,'left'),right:sideLevels(rack,'right'),[side]:levels};
    sceneCacheKey='';markChanged();drawSoon();renderProperties();
    if(byId('rackDialog').open&&editingId===rack.id){editingRack=JSON.parse(JSON.stringify(rack));renderBom(editingRack);drawPreviewSoon();}
  }
  function drawSoon(){if(!pending){pending=true;requestAnimationFrame(drawRack);}}
  // Preview quality slider (render-quality.js), shared by the rack view and the rack setup preview. Medium = as before.
  function rackPixelRatio(){const base=Math.min(window.devicePixelRatio||1,2);return window.RenderQuality?window.RenderQuality.pixelRatio('rack',base):base;}
  function drawRack(){
    pending=false;if(byId('rackView').hidden||!rackContext)return;
    const w=Math.max(280,rackCanvas.clientWidth),h=Math.max(350,rackCanvas.clientHeight),dpr=rackPixelRatio();
    rackCanvas.width=Math.round(w*dpr);rackCanvas.height=Math.round(h*dpr);
    const ctx=rackContext;ctx.setTransform(dpr,0,0,dpr,0,0);ctx.fillStyle='#151c26';ctx.fillRect(0,0,w,h);clickRegions=[];
    const rack=active();
    if(!rack||!sourceMeshes||!sceneRenderer){ctx.fillStyle='#aab9cb';ctx.font='15px system-ui';ctx.textAlign='center';ctx.fillText(!rack?'Create a rack layout to begin':sourceError||'Loading your Lab Rax enclosure meshes…',w/2,h/2);return;}
    const key=rack.slots+':'+showRackPanels+':'+cablesView+':'+sideLevels(rack,'left')+'|'+sideLevels(rack,'right')+':'+!!sourceMeshes.extension+':'+!!sourceMeshes.cable_guide+':'+JSON.stringify(rackGuides(rack));
    if(sceneCacheKey!==key){
      const scene=rackFrame(rack.slots,showRackPanels&&!cablesView,rack);
      // Cables view: drop the top/bottom panels and see through everything but the posts, guides and equipment.
      if(cablesView){scene.parts=scene.parts.filter(p=>p.kind!=='panel');for(const p of scene.parts)if((p.kind==='frame'&&!/^post\d$/.test(p.key))||p.kind==='foot'){p.ghost=true;p.alpha=.22;}}
      // Frame the camera and post labels on the frame alone, so adding guides never shifts the view.
      sceneCache={scene,box:LabRaxScene.bounds({parts:scene.parts.filter(p=>p.kind!=='guide')},sourceMeshes)};sceneCacheKey=key;
    }
    // Highlight the paint group being edited (renderer copies part.selected into its uSelected tint).
    const paintKeys=inspectorTab==='Appearance'&&rack.layout_locked?(paintGroup==='logo'?['beam_top_front']:paintGroups.find(g=>g[0]===paintGroup)?.[2]||[]):[];
    for(const p of sceneCache.scene.parts){p.selected=p.kind==='guide'?(showMe?showMe.guides.has(p.guide):p.guide===selectedGuide):paintKeys.includes(p.key);p.dim=!!showMe&&p.kind==='guide'&&!showMe.guides.has(p.guide);}
    let {scene,box}=sceneCache;const view=ViewerControls.camera(LabRaxStudio.camera(box,yaw,pitch,w,h,1,perspectiveCamera),w,h,{zoom,panX,panY}),project=view.project;
    // Port markers: every port in Cables view (trays turn see-through), otherwise the selected slot's equipment only.
    sceneRenderer.ghostTrays=cablesView;
    if(window.LabRaxPorts&&sourceMeshes['port-other']){const shown=cablesView||connecting?rack.placements:rack.placements.filter(p=>selectedSlot>=p.slot&&selectedSlot<p.slot+p.span);
      scene={...scene,parts:[...scene.parts,...LabRaxPorts.markerParts(rack,shown,window.equipmentLibraryItems?.()||[],selectedPort).map(p=>showMe?{...p,selected:showMe.ports.has(p.port),dim:!showMe.ports.has(p.port)}:p),...cableParts(rack)]};}
    try {
    if(sceneRenderer.restoreRequired){sceneRenderer.dispose();sceneRenderer=new LabRaxStudio.Renderer();sceneRenderer.invalidated=drawSoon;}
    sceneRenderer.shadows=studioQuality&&sceneRenderer.shadowSupported;sceneRenderer.ambientOcclusion=studioQuality;
    ctx.drawImage(sceneRenderer.draw(scene,sourceMeshes,view,Math.round(w*dpr),Math.round(h*dpr),rack,selectedSlot),0,0,w,h);
    } catch(e) {sourceError=e.message;ctx.fillStyle='#efb6a5';ctx.fillText(sourceError,24,36);return;}
    drawCableLabels(ctx,rack,project);
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
    // Lab Rax Cable Guide (MakerWorld Exclusive License): local preview mesh only, never exported or redistributed.
    try{const r=await fetch('/rack-references/cable_guide.json');if(r.ok)meshes.cable_guide=await r.json();}catch(e){}
    // Connector-shaped port markers, generated locally (planning preview only).
    if(window.LabRaxPorts)Object.assign(meshes,LabRaxPorts.markerMeshes(LabRaxStudio));
    // Exit grommet marker (cable-view.js), preview only.
    if(window.LabRaxCableView)meshes['exit-grommet']=LabRaxCableView.grommetMesh(LabRaxStudio);
    sourceMeshes=meshes;sceneCacheKey='';drawSoon();drawPreviewSoon();}).catch(e=>{sourceError=e.message;drawSoon();});}catch(e){sourceError=e.message;}
  byId('frontRackView').onclick=()=>{perspectiveCamera=false;yaw=0;pitch=0;zoom=1;panX=panY=0;setViewButtons('front');drawSoon();};
  // Straight-on rear view; post labels on the back faces turn on with it so the U numbers read from behind.
  byId('rearRackView').onclick=()=>{perspectiveCamera=false;yaw=Math.PI;pitch=0;zoom=1;panX=panY=0;setViewButtons('rear');showRearLabels=true;byId('toggleRearLabels').setAttribute('aria-pressed','true');drawSoon();};
  byId('toggleCablesView').onclick=()=>{cablesView=!cablesView;byId('toggleCablesView').setAttribute('aria-pressed',String(cablesView));byId('toggleRackPanels').disabled=cablesView;drawSoon();};
  byId('toggleCableRuns').onclick=()=>{showCableRuns=!showCableRuns;byId('toggleCableRuns').setAttribute('aria-pressed',String(showCableRuns));drawSoon();};
  if(window.RenderQuality)byId('renderQuality').after(window.RenderQuality.previewSlider('rack',()=>{drawSoon();drawPreviewSoon();},'rq-rack'));
  byId('renderQuality').onclick=()=>{studioQuality=!studioQuality;byId('renderQuality').setAttribute('aria-pressed',String(studioQuality));drawSoon();};
  byId('toggleRearLabels').onclick=()=>{showRearLabels=!showRearLabels;byId('toggleRearLabels').setAttribute('aria-pressed',String(showRearLabels));drawSoon();};
  byId('toggleRackPanels').onclick=()=>{showRackPanels=!showRackPanels;byId('toggleRackPanels').setAttribute('aria-pressed',String(showRackPanels));drawSoon();};
  // Port markers have a real socket hole, so a click in the middle passes through to the faceplate.
  // When the exact point misses, try a small ring of nearby points so clicking the centre still picks the port.
  function portNear(x,y){
    let key=sceneRenderer?.pickPort(x,y);if(key)return key;
    for(const r of [6,12])for(let i=0;i<8;i++){key=sceneRenderer?.pickPort(x+r*Math.cos(i*Math.PI/4),y+r*Math.sin(i*Math.PI/4));if(key)return key;}
    return null;
  }
  ViewerControls.attach(rackCanvas,{
    getView:()=>({yaw,pitch,zoom,panX,panY}),
    setView:v=>{({yaw,pitch,zoom,panX,panY}=v);},redraw:drawSoon,minZoom:.5,maxZoom:2.5,
    onOrbit:()=>{perspectiveCamera=true;setViewButtons('3d');},
    onPreset:name=>{perspectiveCamera=name==='iso';setViewButtons(name==='front'||name==='rear'?name:'3d');},
    presets:Object.fromEntries(Object.entries(ViewerControls.presets).map(([k,v])=>[k,{...v}])),
    onClick:e=>{
    // In the Appearance tab (layout locked) a click picks a part to paint instead of a slot.
    if(inspectorTab==='Appearance'&&active()?.layout_locked){const rect=rackCanvas.getBoundingClientRect(),group=pickRackPart(e.clientX-rect.left,e.clientY-rect.top);if(group)window.selectPaintGroup?.(group);return;}
    if(placingPort){const rect=rackCanvas.getBoundingClientRect();placePortAt(e.clientX-rect.left,e.clientY-rect.top);return;}
    if(connecting){const rect=rackCanvas.getBoundingClientRect(),key=portNear(e.clientX-rect.left,e.clientY-rect.top),placement=placementOfPort(active(),key);
      if(placement)completeConnect({allocation:placement.id,port:key.slice(placement.id.length+1)});else notify('Click a port marker, or choose an outside endpoint in the panel. Esc cancels.',true);return;}
    const rect=rackCanvas.getBoundingClientRect(),x=e.clientX-rect.left,y=e.clientY-rect.top,hit=sceneRenderer?.hitTest(x,y)?.hit;
    if(hit?.port)selectPort(hit.port);else if(hit?.cable)selectCable(hit.cable);else if(hit?.exit)selectExit(hit.exit);else if(hit?.guide)selectGuide(hit.guide);else{const slot=sceneRenderer?.pick(x,y);if(slot)selectSlot(slot);}
    },onRightClick:e=>{const rect=rackCanvas.getBoundingClientRect(),key=portNear(e.clientX-rect.left,e.clientY-rect.top),rack=active(),placement=placementOfPort(rack,key);if(!placement)return;e.preventDefault();
    if(connecting){completeConnect({allocation:placement.id,port:key.slice(placement.id.length+1)});return;}selectPort(key);startConnect({allocation:placement.id,port:key.slice(placement.id.length+1)});}
  });
  window.addEventListener('keydown',e=>{if(e.key==='Escape'&&showMe&&!connecting&&!placingPort)clearShowMe();});
  window.addEventListener('keydown',e=>{if(e.key==='Escape'&&(connecting||placingPort)){if(connecting)cancelConnect();else{placingPort=null;rackCanvas.classList.remove('placing-port');renderProperties();}}});
  rackCanvas.onkeydown=e=>{if(e.key==='ArrowLeft')yaw-=.12;else if(e.key==='ArrowRight')yaw+=.12;else if(e.key==='ArrowUp')pitch=Math.min(1.1,pitch+.12);else if(e.key==='ArrowDown')pitch=Math.max(-1.1,pitch-.12);else return;e.preventDefault();drawSoon();};
  const setViewButtons=mode=>{viewMode=mode;for(const [id,m] of [['frontRackView','front'],['rearRackView','rear'],['resetRackView','3d']])byId(id).setAttribute('aria-pressed',String(mode===m));};
  byId('resetRackView').onclick=()=>{perspectiveCamera=true;yaw=-.48;pitch=.24;zoom=1;panX=panY=0;setViewButtons('3d');drawSoon();};new ResizeObserver(drawSoon).observe(rackCanvas);
  // equipment-wizard.js asks for a redraw with a 'resize' event when slot meshes arrive, and sends 'equipment-rack-view'
  // when a slot switches between its box sketch and an exact render (the inspector note depends on it).
  window.addEventListener('resize',drawSoon);window.addEventListener('equipment-rack-view',()=>{drawSoon();renderProperties();});
  Promise.all([api('workspace-capabilities'),api('rack-workspace'),api('project')]).then(([caps,data,template])=>{if(!caps.independent_assemblies||caps.version!==2||caps.studio_save_version!==1)throw Error('Restart the app server to enable this updated interface.');capable=true;byId('rackHistory').hidden=!caps.save_history;assemblyTemplate=template;documentState=data;layoutDirty=!!data.migration_pending;persistedAssemblyIds=new Set(data.racks.flatMap(r=>r.placements.map(p=>p.assembly.id)));activeId=data.racks[0]?.id||null;render();if(!activeId)dashboard();}).catch(e=>{notify('Rack layouts unavailable: '+e.message,true);byId('saveLayout').disabled=true;});
})();
