// Place on tray window (Option 1, Brian 2026-10-19): the tray choices of ONE slot allocation.
// The library item keeps the equipment facts (size, holes, ports); this window edits placement.tray, whose
// absent keys fall back to the library spec. "Apply to draft" only changes the rack draft; the workspace's
// explicit Save is the only thing that saves it. Fit, retention and strength stay UNKNOWN.
(function(root){
  'use strict';
  // ---- Pure logic (Node-testable). Mirrors equipment.PLACEMENT_KEYS, clean() and equipment_tray.scad asserts.
  const KEYS=['dev_off_x','dev_off_y','dev_rot','device_mount','standoff','insert_pilot','board_t','joint','keystones','rear_support','u'];
  const DEFAULTS={dev_off_x:0,dev_off_y:0,dev_rot:0,device_mount:'inserts',standoff:6,insert_pilot:3.2,board_t:1.6,joint:'screw',keystones:[],rear_support:false,u:1};
  const FRONT_GAP=12,MARGIN=8,MAX_TRAY=230,RACK_DEPTH=240,PITCH=44.45,PLATE_HALF=126,PLATE_T=4,TRAY_T=3;
  const MOUNTS={inserts:'Screws + inserts',pegs:'Pegs',clips:'Clips',straps:'Strap',flat:'Sits flat on the tray (PCs, boxes)'};
  const JOINTS={screw:'Screw joint',single:'Single printed piece'};
  const copy=v=>Array.isArray(v)?v.slice():v;
  // Values shown in the window: the allocation's tray settings win, then the library spec, then template defaults.
  function values(spec,tray){
    const v={};
    for(const k of KEYS)v[k]=copy(tray&&k in tray?tray[k]:spec&&k in spec?spec[k]:DEFAULTS[k]);
    return v;
  }
  // What goes into placement.tray: only the choices that differ from the library item, so an untouched
  // allocation keeps no tray settings and builds exactly as before.
  function diff(spec,v){
    const out={};
    for(const k of KEYS){const base=spec&&k in spec?spec[k]:DEFAULTS[k];if(JSON.stringify(base)!==JSON.stringify(v[k]))out[k]=copy(v[k]);}
    return out;
  }
  function layout(spec,v){
    const turned=v.dev_rot===90||v.dev_rot===270,w=+spec.dev_w,d=+spec.dev_d;
    const fp_w=turned?d:w,fp_d=turned?w:d,tray_w=2*(Math.abs(v.dev_off_x)+fp_w/2+MARGIN);
    const dev_x=-fp_w/2+v.dev_off_x,dev_y=FRONT_GAP+v.dev_off_y;
    const tray_d=v.rear_support?RACK_DEPTH:v.dev_off_y+fp_d+FRONT_GAP+MARGIN;
    const lift=PO().deviceLift(v);
    return {fp_w,fp_d,tray_w,tray_d,dev_x,dev_y,lift,plate_h:v.u*PITCH-2.45,jx:Math.min(40,tray_w/2-12)};
  }
  // equipment_tray.scad dp(): device-frame point (front-left origin) -> footprint offset after rotation.
  function dp(spec,rot,p){const w=+spec.dev_w,d=+spec.dev_d;
    return rot===90?[d-p[1],p[0]]:rot===180?[w-p[0],d-p[1]]:rot===270?[p[1],w-p[0]]:[p[0],p[1]];}
  function holes(spec,v){const L=layout(spec,v);return (spec.holes||[]).map(p=>{const q=dp(spec,v.dev_rot,p);return [L.dev_x+q[0],L.dev_y+q[1]];});}
  const fin=x=>typeof x==='number'&&Number.isFinite(x);
  // port-openings.js (Brian, 2026-10-19): front openings follow the device; loaded as a page script or, under Node, required.
  function PO(){if(root.LabRaxPortOpenings)return root.LabRaxPortOpenings;
    if(typeof module!=='undefined'&&typeof require==='function'){try{return require('./port-openings.js');}catch(e){}}return null;}
  // This slot's front openings: moved with the offset and standoff, or as entered when the device is turned.
  function openings(spec,v){const P=PO();return P?P.frontOpenings(spec,v):{ports:(spec.ports||[]).map(p=>({...p})),dx:0,dz:0,follows:false,rotation:+v.dev_rot||0,message:null};}
  const mm=x=>Math.round(x*10)/10;
  // Plain-language versions of the SCAD asserts and the build checks. Any message blocks Apply and export.
  function problems(spec,v){
    const out=[];
    if(![0,90,180,270].includes(v.dev_rot))return ['Rotation must be 0, 90, 180 or 270 degrees.'];
    if(!fin(v.dev_off_x)||!fin(v.dev_off_y))return ['Enter numbers for the left/right offset and the front gap.'];
    if(!Number.isInteger(v.u)||v.u<1||v.u>5)out.push('Faceplate height must be a whole number of rack units from 1 to 5.');
    if(!MOUNTS[v.device_mount])out.push('Choose how the device attaches to the tray.');
    if(!JOINTS[v.joint])out.push('Choose how the tray joins the faceplate.');
    if(!fin(v.standoff)||v.standoff<0||v.standoff>30)out.push('Standoff must be between 0 and 30 mm.');
    if(v.device_mount==='inserts'&&(!fin(v.insert_pilot)||v.insert_pilot<1.5||v.insert_pilot>8))out.push('Insert pilot hole must be between 1.5 and 8 mm.');
    if((v.device_mount==='pegs'||v.device_mount==='clips')&&(!fin(v.board_t)||v.board_t<0.5||v.board_t>6))out.push('Board thickness must be between 0.5 and 6 mm.');
    if(out.length)return out;
    const L=layout(spec,v);
    if(L.fp_w+2*MARGIN>MAX_TRAY)out.push(`The device is too wide for the tray: it needs ${mm(L.fp_w+2*MARGIN)} mm across with the 8 mm border (max ${MAX_TRAY} mm).`+(v.dev_rot%180===0&&+spec.dev_d+2*MARGIN<=MAX_TRAY?' Try rotating it 90°.':''));
    else if(L.tray_w>MAX_TRAY)out.push(`The device is moved off the tray: it would need a ${mm(L.tray_w)} mm wide tray (max ${MAX_TRAY} mm). Move it back toward the centre.`);
    if(L.dev_y<0)out.push('The device is moved into the faceplate. The front gap must be at least 0 mm.');
    if(v.dev_off_y>230)out.push('The device is moved too far back. The front gap can be at most 242 mm.');
    if(v.rear_support){
      if(v.joint==='single')out.push('Rear-post support needs the screw joint (a 240 mm single print is not offered).');
      if(+spec.dev_d>200)out.push('With rear-post support the device can be at most 200 mm deep.');
      if(L.dev_y+L.fp_d+MARGIN>RACK_DEPTH)out.push('The device is moved past the rear posts. Reduce the front gap.');
    }
    if(PO().neededHeight({...spec,...v})>v.u*PITCH)out.push(`The device is taller than ${v.u}U allows. Pick more rack units or a lower standoff.`);
    if((v.device_mount==='inserts'||v.device_mount==='pegs')&&!(spec.holes||[]).length)out.push('Screws and pegs need mounting holes. Add them to the library item (Edit library item), or choose clips or a strap.');
    if(v.device_mount==='flat'){
      if(L.dev_y<6.2)out.push('Flat corner stops need a front gap of at least 6.2 mm.');
      if(v.joint==='screw'&&L.dev_y<11.5)out.push('Flat device must clear the front screw joint (front gap >= 11.5 mm).');
      if(v.rear_support&&L.dev_y+L.fp_d>RACK_DEPTH-11.5)out.push('Flat device must clear the rear screw joint (rear gap >= 11.5 mm).');
    }
    const ks=v.keystones||[];
    if(ks.length>12)out.push('At most 12 keystones fit the faceplate.');
    if(ks.some(x=>!fin(x)||Math.abs(x)>PLATE_HALF-24))out.push(`Keystones must sit within ${PLATE_HALF-24} mm of the faceplate centre.`);
    const xs=ks.slice().sort((a,b)=>a-b);
    if(xs.some((x,i)=>i&&x-xs[i-1]<21))out.push('Keystones must be at least 21 mm apart.');
    const half=L.tray_w/2;
    if(ks.some(x=>Math.abs(x)-9.9<half+0.5))out.push(`A keystone collar would hit the tray; keep keystones at least ${mm(half+10.4)} mm from the centre.`);
    // Openings moved with the device must stay on the plate and clear of keystones (same limits as equipment.py).
    const P=PO();if(P){out.push(...P.problems(openings(spec,v).ports,v.u,ks));const j=joints(spec,v);if(j&&j.problem)out.push(j.problem);}
    return out;
  }
  // Plain-language warnings that never block (Brian, 2026-10-19).
  // Screw joints placed clear of the openings and keystones (port-openings.js jointPositions); null for the single piece.
  function joints(spec,v){const P=PO();if(v.joint!=='screw'||!P)return null;return P.jointPositions(openings(spec,v).ports,v.keystones||[],layout(spec,v).tray_w/2);}
  function warnings(spec,v){const out=[],m=openings(spec,v).message;if(m)out.push(m);const j=joints(spec,v);
    if(j&&j.moved&&!j.problem)out.push(`The tray screw joints were moved to X = ${j.joints.map(x=>mm(x)).join(' and ')} mm (normally ±${mm(j.default)} mm) to keep them clear of the openings and keystones.`);
    return out;}
  // Centre: left/right offset back to 0 (front gap unchanged). Snap: whole millimetres.
  const snap=x=>Math.round(x);
  // ---- Live 3D preview: simple boxes for the tray, faceplate, standoffs and device (exact meshes on request).
  function box(x0,y0,z0,x1,y1,z1){
    const c=[[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]],v=[];
    for(const f of[[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]])for(const i of f)v.push(...c[i]);
    return v;
  }
  function schematic(spec,v){
    const L=layout(spec,v),floor=PO().floorZ(v)+TRAY_T,tray=box(-L.tray_w/2,0,PO().floorZ(v),L.tray_w/2,L.tray_d,floor);
    const posts=[];
    if(v.device_mount==='inserts'||v.device_mount==='pegs')for(const[x,y]of holes(spec,v))posts.push(...box(x-3,y-3,floor,x+3,y+3,floor+ +v.standoff));
    if(v.device_mount==='flat'){
      const h=Math.min(6,+spec.dev_h),w=Math.min(6,L.fp_w),d=Math.min(6,L.fp_d);
      for(const x of [L.dev_x-6.2,L.dev_x+L.fp_w+0.2])for(const y of [L.dev_y,L.dev_y+L.fp_d-d])posts.push(...box(x,y,floor,x+6,y+d,floor+h));
      for(const x of [L.dev_x,L.dev_x+L.fp_w-w])for(const y of [L.dev_y-6.2,L.dev_y+L.fp_d+0.2])posts.push(...box(x,y,floor,x+w,y+6,floor+h));
    }
    const plate=box(-PLATE_HALF,-PLATE_T,0,PLATE_HALF,0,L.plate_h),jacks=[];
    for(const x of v.keystones||[])jacks.push(...box(x-7.4,-PLATE_T-0.2,L.plate_h/2-8.3,x+7.4,0.2,L.plate_h/2+8.3));
    const sets=[{v:plate,color:[78,117,163],alpha:1},{v:tray.concat(posts),color:[77,142,110],alpha:1},
      {v:box(L.dev_x,L.dev_y,L.lift,L.dev_x+L.fp_w,L.dev_y+L.fp_d,L.lift+ +spec.dev_h),color:[230,195,92],alpha:0.55}];
    if(jacks.length)sets.push({v:jacks,color:[30,32,36],alpha:1});
    return sets;
  }
  // Rack view sketch of one slot's effective tray (equipment-wizard.js draws it when no exact render exists):
  // flat triangle lists in equipment_tray.scad coordinates, the same frame as the rendered STLs.
  // Openings are dark blocks where the SCAD cuts keystones (ks_w x ks_h = 14.8 x 16.6, centred) and ports.
  function rackSketch(spec,tray){
    const v=values(spec,tray),L=layout(spec,v),sets=schematic(spec,v),out={faceplate:sets[0].v,tray:sets[1].v};
    const holes=[];
    for(const x of v.keystones||[])if(fin(+x))holes.push(...box(x-7.4,-PLATE_T-0.2,L.plate_h/2-8.3,x+7.4,0.2,L.plate_h/2+8.3));
    for(const p of openings(spec,v).ports){const o=[+p.x,+p.z,+p.w,+p.h];if(o.every(fin))holes.push(...box(o[0]-o[2]/2,-PLATE_T-0.2,o[1]-o[3]/2,o[0]+o[2]/2,0.2,o[1]+o[3]/2));}
    if(holes.length)out.openings=holes;
    if(v.rear_support)out.rear_bracket=box(-PLATE_HALF,RACK_DEPTH,0,PLATE_HALF,RACK_DEPTH+PLATE_T,L.plate_h); // to_rear(): plate mirrored about mid-depth
    return out;
  }
  const api={KEYS,DEFAULTS,MOUNTS,JOINTS,FRONT_GAP,values,diff,layout,holes,openings,joints,problems,warnings,snap,schematic,box,rackSketch};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;
  root.TrayPlacement=api;
  if(typeof document==='undefined')return;

  // ---- Window (browser only).
  const h=(tag,attrs={},...kids)=>{const e=document.createElement(tag);for(const[k,a]of Object.entries(attrs)){if(k.startsWith('on'))e[k]=a;else if(a!==false&&a!=null)e.setAttribute(k,a===true?'':a);}e.append(...kids);return e;};
  const NS='http://www.w3.org/2000/svg';
  // index.html declares the session token as a top-level const (not a window property).
  const appToken=()=>typeof token!=='undefined'?token:'';
  let state=null; // {placement id, rack id, item, v (working values), prevU, exact (rendered meshes for this json)}
  const view={yaw:2.5,pitch:0.5,zoom:1.6,sets:[],quality:'placement'}; // seen from behind and above, so the faceplate does not hide the device
  function current(){return state&&problems(state.item.spec,state.v);}
  function field(label,get,set,attrs={}){
    const input=h('input',{type:'number',step:'1',value:String(get()),...attrs});
    input.oninput=()=>{if(input.value==='')return;set(Number(input.value));update();};
    input.onchange=()=>{input.value=String(get());};
    return h('label',{class:'ew-field'},label,input);
  }
  function chips(options,value,pick){
    return h('div',{class:'ew-choices'},...Object.entries(options).map(([k,t])=>{const b=h('button',{type:'button',class:'ew-chip'+(value===k?' on':''),'aria-pressed':String(value===k)},t);b.onclick=()=>{pick(k);render();};return b;}));
  }
  function topView(){
    const svg=document.getElementById('tpTop');if(!svg)return;const spec=state.item.spec,v=state.v,L=layout(spec,v);
    const depth=Math.max(L.tray_d,L.dev_y+L.fp_d)+12;
    svg.setAttribute('viewBox',`-132 ${-depth} 264 ${depth+20}`);
    let s=`<rect x="-126" y="0" width="252" height="4" fill="#4e75a3"/><text x="0" y="14" font-size="6" fill="#9aa" text-anchor="middle">faceplate (front)</text>`;
    const over=L.tray_w>MAX_TRAY;
    s+=`<rect x="${-L.tray_w/2}" y="${-L.tray_d}" width="${L.tray_w}" height="${L.tray_d}" fill="#24382f" stroke="${over?'#e07070':'#4d8e6e'}" stroke-width=".8"/>`;
    s+=`<rect x="-115" y="${-depth+2}" width="230" height="${depth-2}" fill="none" stroke="#666" stroke-width=".4" stroke-dasharray="3 2"/>`;
    if(v.joint==='screw'){const j=joints(spec,v);for(const x of j?j.joints.filter(x=>x!==null):[-L.jx,L.jx])s+=`<circle cx="${x}" cy="-3.5" r="2" fill="#aab"/>`;}
    for(const x of v.keystones||[])s+=`<rect x="${x-9.9}" y="-10.4" width="19.8" height="10.4" fill="#1d1f24" stroke="#888" stroke-width=".4"/>`;
    // Front-port openings in the faceplate strip (they follow the offset; a turned device leaves them as entered).
    for(const p of openings(spec,v).ports)if([+p.x,+p.w].every(fin))s+=`<rect x="${+p.x-p.w/2}" y="0.6" width="${+p.w}" height="2.8" fill="#1d1f24" stroke="#ff9f43" stroke-width=".4"><title>${String(p.label||'Port').replace(/[<&"]/g,'')} opening</title></rect>`;
    s+=`<rect id="tpDevice" x="${L.dev_x}" y="${-(L.dev_y+L.fp_d)}" width="${L.fp_w}" height="${L.fp_d}" fill="#e6c35c" fill-opacity=".35" stroke="#e6c35c" stroke-width=".8" style="cursor:grab"/>`;
    const a=dp(spec,v.dev_rot,[0,0]),b=dp(spec,v.dev_rot,[+spec.dev_w,0]);
    s+=`<line x1="${L.dev_x+a[0]}" y1="${-(L.dev_y+a[1])}" x2="${L.dev_x+b[0]}" y2="${-(L.dev_y+b[1])}" stroke="#ff9f43" stroke-width="2" pointer-events="none"/>`;
    for(const[x,y]of holes(spec,v))s+=`<circle cx="${x}" cy="${-y}" r="${(+spec.hole_d||2.7)/2+.4}" fill="#5cc8ff" pointer-events="none"/>`;
    s+=`<text x="${L.dev_x+L.fp_w/2}" y="${-(L.dev_y+L.fp_d/2)}" font-size="6" fill="#eee" text-anchor="middle" pointer-events="none">${v.dev_rot}°</text>`;
    svg.innerHTML=s;
    const dev=svg.querySelector('#tpDevice');
    dev.onpointerdown=e=>{e.preventDefault();dev.setPointerCapture(e.pointerId);const m=svg.getScreenCTM().inverse(),pt=q=>{const p=svg.createSVGPoint();p.x=q.clientX;p.y=q.clientY;return p.matrixTransform(m);};
      const start=pt(e),x0=v.dev_off_x,y0=v.dev_off_y;
      dev.onpointermove=ev=>{const p=pt(ev);v.dev_off_x=Math.max(-150,Math.min(150,snap(x0+p.x-start.x)));v.dev_off_y=Math.max(-40,Math.min(260,snap(y0-(p.y-start.y))));syncFields();update();};
      dev.onpointerup=()=>{dev.onpointermove=null;};};
  }
  function syncFields(){
    const x=document.getElementById('tpOffX'),y=document.getElementById('tpGap');
    if(x&&document.activeElement!==x)x.value=String(state.v.dev_off_x);
    if(y&&document.activeElement!==y)y.value=String(FRONT_GAP+state.v.dev_off_y);
  }
  function draw3D(){
    const cv=document.getElementById('tpView'),P=window.EquipmentPainter;if(!cv||!P)return;
    const key=exactKey();
    view.sets=state.exact&&state.exact.key===key?state.exact.sets.concat(schematic(state.item.spec,state.v).slice(2,3)):schematic(state.item.spec,state.v);
    const note=document.getElementById('tpViewNote');
    if(note)note.textContent=state.exact&&state.exact.key===key?`Exact OpenSCAD render of these settings at export quality ${exportNote()} (not saved). Translucent box = the device.`:'Live sketch: boxes for the tray, faceplate, standoffs and device (translucent). Left-drag turns, right-drag moves, scroll zooms.';
    P.draw(cv,view);
  }
  function update(){
    if(!state)return;topView();draw3D();
    const list=current(),box=document.getElementById('tpProblems');
    box.replaceChildren(...list.map(t=>h('li',{},t)));box.hidden=!list.length;
    for(const id of['tpApply','tpExport'])if(document.getElementById(id))document.getElementById(id).disabled=!!list.length;
    // Warnings never block Apply or export (Brian, 2026-10-19): turned-device front openings, support-extension joint.
    const warn=document.getElementById('tpWarnings');
    if(warn){const ws=warnings(state.item.spec,state.v),jw=window.extensionJointWarning?.(state.slot,state.v.u);if(jw)ws.push(jw);
      warn.replaceChildren(...ws.map(t=>h('li',{},t)));warn.hidden=!ws.length;}
    const L=layout(state.item.spec,state.v),sum=document.getElementById('tpSummary');
    if(sum)sum.textContent=`Tray ${mm(L.tray_w)} × ${mm(L.tray_d)} mm · device ${mm(L.fp_w)} × ${mm(L.fp_d)} mm on the tray · ${state.v.u}U faceplate.`;
  }
  function keystones(){
    const v=state.v,x=h('input',{type:'number',step:'1',value:String(v.keystones.length?Math.min(100,v.keystones.at(-1)+25):-100),style:'width:70px','aria-label':'Keystone X position (mm)'});
    const add=h('button',{type:'button',class:'ew-chip'},'+ Add keystone');add.onclick=()=>{v.keystones.push(Number(x.value));render();};
    return h('div',{class:'ew-ksbar'},'Keystones at X ',x,' mm (0 = centre) ',add,
      ...v.keystones.map((k,i)=>{const b=h('button',{type:'button',class:'ew-chip on',title:'Remove'},`⌧ ${k} mm`);b.onclick=()=>{v.keystones.splice(i,1);render();};return b;}));
  }
  async function post(path,body){
    return fetch(path,{method:'POST',headers:{'Content-Type':'application/json','X-App-Token':appToken()},body:JSON.stringify(body)});
  }
  function request(){return {item:state.item.id,tray:diff(state.item.spec,state.v)};}
  // Export quality (render-quality.js) goes with exact renders and exports only; it is never a saved tray setting.
  const exportLevel=()=>window.RenderQuality?.exportLevel()||'standard';
  const exportNote=()=>window.RenderQuality?.exportNote(exportLevel())||'Standard';
  function exportRequest(){return {...request(),quality:exportLevel()};}
  const exactKey=()=>JSON.stringify(state.v)+'|'+exportLevel();
  async function serverCheck(){
    const r=await post('/api/equipment-placement-check',request()),out=await r.json();
    if(!r.ok)throw Error(out.error||'Check failed');if(!out.ok)throw Error(out.error);
  }
  function setStatus(t){const s=document.getElementById('tpStatus');if(s)s.textContent=t;}
  function render(){
    const d=document.getElementById('trayPlacement');if(!d||!state)return;
    const spec=state.item.spec,v=state.v,name=state.item.display_name||state.item.name;
    const rot=h('div',{class:'ew-choices',role:'group','aria-label':'Rotation'},...[0,90,180,270].map(r=>{const b=h('button',{type:'button',class:'ew-chip'+(v.dev_rot===r?' on':''),'aria-pressed':String(v.dev_rot===r)},r+'°');b.onclick=()=>{v.dev_rot=r;render();};return b;}));
    const centre=h('button',{type:'button',class:'ew-chip'},'Centre');centre.onclick=()=>{v.dev_off_x=0;syncFields();update();};
    const mountOpts=PO().usesStandoffs(v)?[field('Standoff (mm)',()=>v.standoff,x=>v.standoff=x,{step:'0.5',min:'0',max:'30'})]:[h('p',{class:'ew-note'},v.device_mount==='flat'?'Rests on the low floor with corner stops and optional strap slots. Retention UNKNOWN.':'Rests on the tray floor; no standoffs.')];
    if(v.device_mount==='inserts')mountOpts.push(field('Insert pilot hole (mm)',()=>v.insert_pilot,x=>v.insert_pilot=x,{step:'0.1'}));
    if(v.device_mount==='pegs'||v.device_mount==='clips')mountOpts.push(field(v.device_mount==='pegs'?'Board thickness (mm)':'Edge thickness clipped (mm)',()=>v.board_t,x=>v.board_t=x,{step:'0.1'}));
    const rs=h('input',{type:'checkbox'});rs.checked=!!v.rear_support;rs.onchange=()=>{v.rear_support=rs.checked;render();};
    const cv=h('canvas',{id:'tpView',class:'ew-view tp-view'});
    const exact=h('button',{type:'button'},'Render exact preview');
    exact.onclick=async()=>{exact.disabled=true;setStatus('Rendering with OpenSCAD… this can take a minute. Nothing is saved.');
      try{if(current().length)throw Error('Fix the problems listed first.');const key=exactKey(),r=await post('/api/equipment-preview',exportRequest()),out=await r.json();if(!r.ok)throw Error(out.error||'Preview failed');
        const sets=[];for(const p of out.parts){const buf=await (await fetch(`/api/equipment-mesh/${out.id}/${p}.stl`)).arrayBuffer();sets.push({v:window.EquipmentPainter.parseStl(buf),color:p==='tray'?[77,142,110]:[78,117,163],alpha:1});}
        state.exact={key,sets};draw3D();window.EquipmentRackView?.refresh();setStatus('Exact preview ready. Change any value to go back to the live sketch.');}
      catch(e){setStatus('Problem: '+e.message);}finally{exact.disabled=false;}};
    const exp=h('button',{type:'button',id:'tpExport'},'Generate proposed STL files');
    exp.onclick=async()=>{if(current().length){update();return;}exp.disabled=true;setStatus('Checking, then rendering with OpenSCAD…');
      try{await serverCheck();const r=await post('/api/equipment-build',exportRequest());if(!r.ok)throw Error((await r.json()).error||'Build failed');
        const url=URL.createObjectURL(await r.blob()),a=document.createElement('a');a.href=url;a.download=(name||'equipment').replace(/[^\w-]+/g,'_')+'-slot-'+state.slot+'-stl.zip';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);window.EquipmentRackView?.refresh();
        setStatus(`Done (${exportNote()}). PROPOSED — UNVALIDATED STLs for these window values; export.json in the zip records the quality.`+' The rack draft is unchanged until you Apply and Save.');}
      catch(e){setStatus('Problem: '+e.message);}finally{update();}};
    const apply=h('button',{type:'button',id:'tpApply',class:'primary'},'Apply to draft');
    apply.onclick=async()=>{if(current().length){update();return;}apply.disabled=true;setStatus('Checking…');
      try{await serverCheck();if(!window.applyTrayPlacement)throw Error('The workspace is not ready.');
        window.applyTrayPlacement(state.rack,state.id,diff(spec,v),v.u!==state.prevU?v.u:null);d.close();}
      catch(e){setStatus('Problem: '+e.message);update();}};
    const cancel=h('button',{type:'button'},'Cancel');cancel.onclick=()=>d.close();
    const lib=h('button',{type:'button',class:'subtle'},'Edit library item…');lib.onclick=()=>{d.close();window.openCustomEquipment?.({equipment:state.item.id});};
    const offX=field('Left/right offset (mm)',()=>v.dev_off_x,x=>v.dev_off_x=x,{id:'tpOffX'});
    const gap=field('Front gap (mm)',()=>FRONT_GAP+v.dev_off_y,x=>v.dev_off_y=x-FRONT_GAP,{id:'tpGap',min:'0'});
    d.replaceChildren(
      h('div',{class:'tp-head'},h('div',{},h('p',{class:'section-eyebrow'},'PLACE ON TRAY · SLOT '+state.slot+(state.span>1?'–'+(state.slot+state.span-1):'')),h('h2',{},name)),lib),
      h('p',{class:'ew-note'},`${spec.dev_w} × ${spec.dev_d} × ${spec.dev_h} mm, ${(spec.holes||[]).length} mounting hole(s). These choices belong to this slot only; the library item is not changed.`),
      h('div',{class:'tp-grid'},
        h('div',{class:'tp-pane'},h('h3',{},'Top view'),document.createElementNS(NS,'svg'),
          h('p',{class:'ew-note'},'Drag the device (snaps to 1 mm). Orange edge = device front. Blue dots = screw/hole positions. Dashed outline = the 230 mm tray limit.'),
          h('h3',{},'Position'),h('div',{class:'ew-row'},offX,centre),h('div',{class:'ew-row'},gap),h('div',{class:'ew-row'},'Rotate ',rot),
          h('h3',{},'Mounting'),chips(MOUNTS,v.device_mount,k=>v.device_mount=k),h('div',{class:'ew-row'},...mountOpts)),
        h('div',{class:'tp-pane'},h('h3',{},'Live 3D preview'),cv,h('p',{id:'tpViewNote',class:'ew-note'}),h('div',{class:'ew-row'},exact,window.RenderQuality?.previewSlider('placement',draw3D)||''),
          h('h3',{},'Faceplate'),h('div',{class:'ew-row'},field('Height (rack units)',()=>v.u,x=>v.u=x,{min:'1',max:'5'})),keystones(),
          h('p',{},'Tray joint'),chips(JOINTS,v.joint,k=>v.joint=k),
          h('label',{class:'ew-chip'},rs,' Rear support (tray runs to the back posts)'),
          h('p',{class:'tp-unknown'},'Fit, retention, strength: UNKNOWN'))),
      h('p',{id:'tpSummary',class:'ew-note'}),
      h('ul',{id:'tpProblems',class:'tp-problems',role:'alert'}),
      h('ul',{id:'tpWarnings',class:'tp-warnings',role:'status'}),
      h('p',{id:'tpStatus',class:'ew-note',role:'status'},'Changes stay in this window until you press Apply to draft. Apply changes the rack draft only; use Save to keep it.'),
      h('div',{class:'ew-nav'},exp,window.RenderQuality?.exportSlider(()=>draw3D(),'tp-export-quality')||'',cancel,apply));
    const svg=d.querySelector('.tp-pane svg');svg.id='tpTop';svg.setAttribute('class','tp-top');svg.setAttribute('role','img');svg.setAttribute('aria-label','Top view of the tray and faceplate');
    if(!cv.tpBound){cv.tpBound=true;window.EquipmentPainter?.bind(cv,view,draw3D);}
    update();
  }
  function ensureDialog(){
    let d=document.getElementById('trayPlacement');
    if(!d){d=h('dialog',{id:'trayPlacement',class:'ew-dialog tp-dialog','aria-label':'Place on tray'});document.body.append(d);
      d.addEventListener('close',()=>{state=null;});
      document.head.append(h('style',{},`.tp-dialog{width:min(1040px,96vw)}.tp-head{display:flex;justify-content:space-between;align-items:flex-start;gap:8px}.tp-head h2{margin:0}
.tp-grid{display:grid;grid-template-columns:1.15fr 1fr;gap:14px}@media(max-width:760px){.tp-grid{grid-template-columns:1fr}}.tp-pane h3{margin:10px 0 4px;font-size:13px;color:#cfd6df}
.tp-top{width:100%;height:300px;background:#121418;border-radius:6px;touch-action:none}.tp-view{height:240px}.tp-unknown{color:#e0b56f;font-weight:600;margin-top:10px}
.tp-problems{color:#ff9a9a;margin:6px 0;padding-left:18px}.tp-problems:empty{display:none}.tp-warnings{color:#e0b56f;margin:6px 0;padding-left:18px}.tp-warnings:empty{display:none}`));}
    return d;
  }
  // Called by workspace.js when a library item is placed in a slot or its slot placement is edited.
  window.openTrayPlacement=async function(rackId,placement){
    let item=(window.equipmentLibraryItems?.()||[]).find(i=>i.id===placement.equipment);
    if(!item)try{item=(await (await fetch('/api/equipment-library')).json()).find(i=>i.id===placement.equipment);}catch(e){}
    if(!item){alert('This equipment is no longer in the library.');return false;}
    const v=values(item.spec,placement.tray);
    state={rack:rackId,id:placement.id,slot:placement.slot,span:placement.span,item,v,prevU:v.u,exact:null};
    // Paint again once the dialog is shown: the canvas has no size before that.
    const d=ensureDialog();render();if(!d.open)d.showModal();draw3D();return true;
  };
})(typeof window!=='undefined'?window:globalThis);
