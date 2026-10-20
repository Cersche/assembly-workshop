// Read-only individual creator components; never manufacturing export inputs.
(function(){
  'use strict';
  const $=id=>document.getElementById(id),toolbar=document.querySelector('.rack-toolbar');
  if(!toolbar)return;
  const launch=document.createElement('button');launch.id='openRackReferences';launch.className='tb-more';launch.textContent='Parts catalog';launch.title='Browse the original Lab Rax part models';const heading=document.querySelector('.viewport-heading');if(heading)heading.insertBefore(launch,$('contextBadge'));else toolbar.append(launch);
  const dialog=document.createElement('dialog');dialog.id='rackReferenceDialog';dialog.setAttribute('aria-labelledby','rackReferenceTitle');
  dialog.innerHTML=`<div class="dialog-heading"><span class="section-eyebrow">RACK BUILDER · SOURCE REFERENCES</span><button id="closeRackReferences" class="subtle" aria-label="Close Lab Rax references">✕</button></div>
    <h2 id="rackReferenceTitle">Lab Rax frame & components</h2><p class="muted">Inspect the supplied creator parts and visual references while planning your rack. Dimensions below are source mesh observations. Rack layout dimensions are edited separately.</p>
    <p id="rackReferenceStatus" role="status">Loading local references…</p><div id="rackReferenceContent" hidden><div id="rackReferenceTabs" class="reference-tabs" role="tablist" aria-label="Reference file"></div>
    <div class="reference-grid"><figure><img id="rackReferencePhoto" alt="Creator reference from the supplied 3MF"><figcaption id="rackReferenceCaption"></figcaption></figure><div><label for="rackReferenceComponent">Inspect a component</label><select id="rackReferenceComponent"></select><canvas id="rackReferenceCanvas" tabindex="0" aria-label="Individual source component; drag or use arrow keys to orbit"></canvas><p class="muted">Drag or use arrow keys to orbit · individual component, unassembled</p><p id="rackReferenceDimensions"></p><p id="rackReferenceMember" class="muted"></p></div></div>
    <p id="rackReferenceM6" class="notice"></p><details><summary>Source & validation limits</summary><p id="rackReferenceProvenance"></p><p class="notice">Assembly transforms, clearances, usable depth, insert specification, physical fit and strength remain UNKNOWN. This reference viewer does not add rack-frame STL export or change the saved assembly hardware. Source assets stay local; redistribution rights remain unresolved.</p></details></div>`;
  document.body.append(dialog);
  let catalog=null,reference=null,mesh=null,yaw=-.5,pitch=.3,drag=null,request=0;
  const canvas=$('rackReferenceCanvas'),ctx=canvas.getContext('2d');
  const status=message=>{$('rackReferenceStatus').textContent=message;};
  async function json(url){const response=await fetch(url);if(!response.ok)throw new Error('Local reference unavailable ('+response.status+'). Restart the app with start.bat after a source update.');return response.json();}
  async function selectComponent(){
    const current=++request;mesh=null;draw();
    const component=reference.components.find(c=>c.id===$('rackReferenceComponent').value);
    $('rackReferenceDimensions').textContent=component.extent_mm.map(v=>v.toFixed(3)).join(' × ')+' mm · local X × Y × Z bounds · '+component.triangles.toLocaleString()+' triangles';
    $('rackReferenceMember').textContent=component.source_member+' / object '+component.id;status('Loading source component…');
    try{const loaded=await json(component.url);if(current!==request)return;mesh=loaded;yaw=-.5;pitch=.3;draw();status('Source component reference · assembled fit UNKNOWN');}catch(e){if(current===request)status(e.message);}
  }
  function selectReference(value){
    reference=value;for(const tab of $('rackReferenceTabs').children)tab.setAttribute('aria-selected',String(tab.dataset.reference===value.id));
    $('rackReferencePhoto').src=value.pictures[0].url;$('rackReferencePhoto').alt=value.title+' · embedded creator reference image';$('rackReferenceCaption').textContent=value.title+' · '+value.designer;
    const choices=$('rackReferenceComponent');choices.replaceChildren();for(const c of value.components){const option=document.createElement('option');option.value=c.id;option.textContent=c.name;choices.append(option);}
    $('rackReferenceProvenance').textContent=value.source_file+' · SHA-256 '+value.source_sha256+' · license metadata: '+value.license_metadata+'. Full source coordinates retained; no rescaling or quantization.';selectComponent();
  }
  launch.onclick=async()=>{dialog.showModal();if(catalog){draw();return;}try{catalog=await json('/rack-references/catalog.json');$('rackReferenceM6').textContent=catalog.m6_note;const tabs=$('rackReferenceTabs');tabs.replaceChildren();for(const ref of catalog.references){const b=document.createElement('button');b.type='button';b.setAttribute('role','tab');b.dataset.reference=ref.id;b.textContent=ref.title;b.onclick=()=>selectReference(ref);tabs.append(b);}$('rackReferenceContent').hidden=false;selectReference(catalog.references[0]);}catch(e){catalog=null;status(e.message);}};
  $('closeRackReferences').onclick=()=>dialog.close();$('rackReferenceComponent').onchange=selectComponent;
  function draw(){
    if(!dialog.open||!ctx)return;
    const w=Math.max(240,canvas.clientWidth),h=330,dpr=Math.min(window.devicePixelRatio||1,2);canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);ctx.fillStyle='#111923';ctx.fillRect(0,0,w,h);if(!mesh)return;
    const lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];for(const v of mesh.vertices)for(let k=0;k<3;k++){lo[k]=Math.min(lo[k],v[k]);hi[k]=Math.max(hi[k],v[k]);}
    const center=lo.map((v,k)=>(v+hi[k])/2),sy=Math.sin(yaw),cy=Math.cos(yaw),sp=Math.sin(pitch),cp=Math.cos(pitch);
    const points=mesh.vertices.map(v=>{const x=v[0]-center[0],y=v[1]-center[1],z=v[2]-center[2],u=cy*x-sy*y,d=sy*x+cy*y;return [u,cp*z-sp*d,sp*z+cp*d];});
    const bounds=[Infinity,-Infinity,Infinity,-Infinity];for(const p of points){bounds[0]=Math.min(bounds[0],p[0]);bounds[1]=Math.max(bounds[1],p[0]);bounds[2]=Math.min(bounds[2],p[1]);bounds[3]=Math.max(bounds[3],p[1]);}
    const scale=Math.min((w-44)/(bounds[1]-bounds[0]||1),(h-44)/(bounds[3]-bounds[2]||1)),ox=(bounds[0]+bounds[1])/2,oy=(bounds[2]+bounds[3])/2;
    const faces=mesh.triangles.map(t=>({t,d:t.reduce((s,i)=>s+points[i][2],0)/3})).sort((a,b)=>a.d-b.d);
    for(const {t} of faces){const a=points[t[0]],b=points[t[1]],c=points[t[2]],u=b.map((v,k)=>v-a[k]),v=c.map((x,k)=>x-a[k]),n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]],length=Math.hypot(...n)||1,light=.35+.65*Math.abs((n[0]*.25+n[1]*.45+n[2]*.85)/length);ctx.fillStyle='rgb('+[112,151,191].map(x=>Math.round(x*light)).join(',')+')';ctx.beginPath();t.forEach((i,k)=>{const p=points[i],x=w/2+(p[0]-ox)*scale,y=h/2-(p[1]-oy)*scale;k?ctx.lineTo(x,y):ctx.moveTo(x,y);});ctx.closePath();ctx.fill();}
  }
  canvas.onpointerdown=e=>{drag=[e.clientX,e.clientY];canvas.setPointerCapture(e.pointerId);};canvas.onpointermove=e=>{if(!drag)return;yaw+=(e.clientX-drag[0])*.008;pitch+=(e.clientY-drag[1])*.008;drag=[e.clientX,e.clientY];draw();};canvas.onpointerup=canvas.onpointercancel=()=>{drag=null;};
  canvas.onkeydown=e=>{if(e.key==='ArrowLeft')yaw-=.12;else if(e.key==='ArrowRight')yaw+=.12;else if(e.key==='ArrowUp')pitch+=.12;else if(e.key==='ArrowDown')pitch-=.12;else return;e.preventDefault();draw();};new ResizeObserver(draw).observe(canvas);
})();
