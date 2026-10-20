
(()=>{
 const root=document.getElementById('rax-options');
 for(const app of root.querySelectorAll('.rax')){
   let selected=1;const state={face:'#325a8e',tray:'#ba7245'},menu=app.querySelector('.rx-menu'),sheet=app.querySelector('.rx-sheet'),toast=app.querySelector('.rx-toast');
   const slotList=app.querySelector('[data-slot-list]');
   if(slotList)for(let n=5;n>=1;n--){const row=document.createElement('div');row.className='rx-slot';const select=document.createElement('button');select.className='rx-select';select.dataset.slot=n;select.setAttribute('aria-pressed',String(n===1));select.innerHTML='<span class="rx-num">'+String(n).padStart(2,'0')+'</span><span><strong>'+(n===1?'Pi4 assembly':'Empty slot')+'</strong><small>'+(n===1?'Tray + faceplate':'Ready for equipment')+'</small></span>';const more=document.createElement('button');more.className='rx-more';more.textContent='⋯';more.dataset.menu='';more.dataset.forSlot=n;more.setAttribute('aria-label','More actions for slot '+n);row.append(select,more);row.oncontextmenu=e=>{e.preventDefault();choose(n);menu.hidden=false;};slotList.append(row);}
   function choose(n){selected=n;for(const b of app.querySelectorAll('[data-slot]'))b.setAttribute('aria-pressed',String(Number(b.dataset.slot)===n));app.querySelector('[data-slot-heading]').textContent='Slot '+n+(n===1?' · Pi4':' · Empty');app.querySelector('[data-selection]').textContent='Slot '+n+(n===1?' · Raspberry Pi 4':' · Empty slot');const start=app.querySelector('[data-start]');if(start)start.value=n;toast.textContent=n===1?'':'Empty slot selected · use Add equipment.';menu.hidden=true;}
   function view(name){app.querySelector('[data-rack]').hidden=name!=='rack';app.querySelector('[data-face]').hidden=name!=='face';for(const b of app.querySelectorAll('[data-view]'))b.setAttribute('aria-pressed',String(b.dataset.view===name));}
   function pane(name){for(const b of app.querySelectorAll('[data-pane]'))b.setAttribute('aria-selected',String(b.dataset.pane===name));for(const e of app.querySelectorAll('[data-panel]'))e.hidden=e.dataset.panel!==name;}
   function dialog(title,content){sheet.replaceChildren();const h=document.createElement('h3');h.textContent=title;sheet.append(h);const body=document.createElement('div');body.innerHTML=content;sheet.append(body);const actions=document.createElement('div');actions.className='rx-sheet-actions';const close=document.createElement('button');close.textContent='Done';close.onclick=()=>{sheet.hidden=true;toast.textContent='Interface concept · app data unchanged.';};actions.append(close);sheet.append(actions);sheet.hidden=false;}
   app.addEventListener('click',e=>{
     const b=e.target.closest('button');if(!b)return;
     if(b.dataset.slot){choose(Number(b.dataset.slot));return;}
     if('menu' in b.dataset){if(b.dataset.forSlot)choose(Number(b.dataset.forSlot));menu.hidden=!menu.hidden;menu.querySelector('button')?.focus();return;}
     if(b.dataset.view){view(b.dataset.view);return;}
     if(b.dataset.pane){pane(b.dataset.pane);return;}
     const task=b.dataset.task;if(!task)return;menu.hidden=true;
     if(task==='appearance'){pane('appearance');const dock=app.querySelector('[data-dock-panel]');if(dock)dock.hidden=!dock.hidden;return;}
     if(task==='front'||task==='open'){view('face');return;}
     if(task==='image'){app.querySelector('[data-file]').click();return;}
     if(task==='hardware')dialog('Slot '+selected+' · Hardware','<label class="rx-field stack">Joint screw<select aria-label="Joint screw"><option>M3 × 8 · revision 1</option><option>M3 × 6 · revision 1</option></select></label><label class="rx-field stack">Heat-set insert<select aria-label="Heat-set insert"><option>94459A140 · revision 1</option></select></label><p class="rx-limit">Each assembly retains its own immutable part pins. These concept controls do not edit your library.</p>');
     if(task==='add')dialog('Slot '+selected+' · Add equipment','<p>Raspberry Pi 4</p><small>Tray + faceplate · supported geometry adapter</small><p class="rx-limit">The app will guide allocation, hardware and appearance here. More equipment adapters remain unsupported.</p>');
     if(task==='allocate')dialog('Edit slot allocation','<label class="rx-field">Start<input type="number" min="1" max="5" value="'+selected+'" aria-label="Starting slot"></label><label class="rx-field">Reserve<input type="number" min="1" max="5" value="1" aria-label="Reserved slots"></label><small>Logical occupancy · installed fit UNKNOWN</small>');
     if(task==='rack')dialog('Rack settings','<label class="rx-field">Slots<input type="number" min="1" max="48" value="5" aria-label="Number of slots"></label><label class="rx-field">Rack color<input type="color" value="#708298" aria-label="Rack color"></label><label class="rx-field">Posts<input type="color" value="#d09b55" aria-label="Post color"></label><p class="rx-limit">Actual source meshes at recovered visual poses. Dimensions and installed interfaces remain unverified.</p>');
   });
   function paint(){app.style.setProperty('--rx-face',state.face);app.style.setProperty('--rx-tray',state.tray);for(const i of app.querySelectorAll('[data-color]'))i.value=state[i.dataset.color];}
   for(const input of app.querySelectorAll('[data-color]'))input.oninput=()=>{state[input.dataset.color]=input.value;paint();view('face');toast.textContent='Preview colors changed · STL unchanged.';};
   const size=app.querySelector('[data-size]');if(size)size.oninput=()=>{app.querySelector('.rx-plate img').style.height=size.value+'%';view('face');};
   const file=app.querySelector('[data-file]');file.onchange=()=>{const image=file.files[0];if(!image)return;if(!['image/png','image/jpeg','image/webp'].includes(image.type)||image.size>10*1024*1024){toast.textContent='Choose a PNG, JPEG or WebP up to 10 MB.';return;}const reader=new FileReader();reader.onload=()=>{for(const img of app.querySelectorAll('.rx-plate img,.rx-art-thumb'))img.src=reader.result;view('face');toast.textContent='Local artwork preview · no app data changed.';};reader.readAsDataURL(image);};
   app.addEventListener('keydown',e=>{if(e.key==='Escape'){menu.hidden=true;sheet.hidden=true;}});
   paint();
   if(globalThis.Tweak){const tweak=new Tweak({container:app,onChange:paint});tweak.addColorPicker(state,'face',{label:'Faceplate color',reference:'--rx-face'});tweak.addColorPicker(state,'tray',{label:'Tray color',reference:'--rx-tray'});}
 }
})();
