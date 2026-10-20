// Equipment wizard: equipment facts only (Device -> Holes -> Ports). Tray choices (position, rotation, mounting,
// standoff, faceplate U/keystones, rear support) are per-slot allocation data, edited in the Place on tray window
// (tray-placement.js). New items keep the template defaults below; older items keep their saved values as defaults.
(function(){
  const PLATE_W=252,STEPS=['Device','Holes','Ports'];
  const MOUNTS={inserts:'Heat-set inserts + screws',pegs:'Printed standoffs / pegs',clips:'Snap-fit clips',straps:'Strap / zip-tie slots',flat:'Sits flat on the tray (PCs, boxes)',sleeve:'Sleeve: boxed in, front flush (PCs, boxes)'};
  const JOINTS={screw:'Screw joint',single:'Single printed piece'};
  let uExplicit=false;
  let spec,step,imported=null,orient=0,turn=0,importMsg='',found=[],foundPorts=[];
  // ---- STL import (phase 2): size from the bounding box, holes from round loops in flat faces.
  function parseStlBuffer(buf){
    const dv=new DataView(buf),n=buf.byteLength>=84?dv.getUint32(80,true):0,out=[];
    if(n&&84+n*50===buf.byteLength){for(let i=0;i<n;i++){const o=84+i*50+12;for(let k=0;k<9;k++)out.push(dv.getFloat32(o+k*4,true));}}
    else{const t=new TextDecoder().decode(buf);for(const m of t.matchAll(/vertex\s+(\S+)\s+(\S+)\s+(\S+)/g))out.push(+m[1],+m[2],+m[3]);}
    if(!out.length||out.length%9||out.some(v=>!isFinite(v)))throw Error('no triangles found');
    return out;
  }
  function transformed(){
    const t=imported.tris,o=[];
    for(let i=0;i<t.length;i+=3){let x=t[i],y=t[i+1],z=t[i+2];
      if(orient===1)[y,z]=[-z,y];else if(orient===2)[x,z]=[-z,x];
      for(let k=0;k<turn;k++)[x,y]=[-y,x];o.push(x,y,z);}
    return o;
  }
  function findHoles(v,minX,minY){
    const R=a=>Math.round(a*1000)/1000,planes=new Map();
    for(let i=0;i<v.length;i+=9){
      const ux=v[i+3]-v[i],uy=v[i+4]-v[i+1],uz=v[i+5]-v[i+2],wx=v[i+6]-v[i],wy=v[i+7]-v[i+1],wz=v[i+8]-v[i+2];
      const nx=uy*wz-uz*wy,ny=uz*wx-ux*wz,nz=ux*wy-uy*wx,len=Math.hypot(nx,ny,nz);
      if(!len||Math.abs(nz)/len<0.99)continue;
      const key=Math.round(v[i+2]*100);if(!planes.has(key))planes.set(key,new Map());const edges=planes.get(key);
      const p=[0,3,6].map(o=>R(v[i+o])+','+R(v[i+o+1]));
      for(const[a,b]of[[p[0],p[1]],[p[1],p[2]],[p[2],p[0]]]){const k=a<b?a+'|'+b:b+'|'+a;edges.set(k,(edges.get(k)||0)+1);}
    }
    const holes=[];
    for(const edges of planes.values()){
      const adj=new Map();for(const[k,c]of edges)if(c===1){const[a,b]=k.split('|');(adj.get(a)||adj.set(a,[]).get(a)).push(b);(adj.get(b)||adj.set(b,[]).get(b)).push(a);}
      const seen=new Set();
      for(const start of adj.keys()){if(seen.has(start))continue;const loop=[];let cur=start,prev=null;
        while(cur&&!seen.has(cur)){seen.add(cur);loop.push(cur.split(',').map(Number));const nxt=(adj.get(cur)||[]).find(q=>q!==prev&&!seen.has(q));prev=cur;cur=nxt;}
        if(loop.length<6)continue;
        const cx=loop.reduce((s,p)=>s+p[0],0)/loop.length,cy=loop.reduce((s,p)=>s+p[1],0)/loop.length,rs=loop.map(p=>Math.hypot(p[0]-cx,p[1]-cy)),r=rs.reduce((a,b)=>a+b,0)/rs.length;
        if(r<0.6||r>4.5||rs.some(q=>Math.abs(q-r)/r>0.1))continue;
        const x=Math.round((cx-minX)*10)/10,y=Math.round((cy-minY)*10)/10,d=Math.round(r*20)/10;
        if(!holes.some(hh=>Math.hypot(hh.x-x,hh.y-y)<0.5))holes.push({x,y,d,keep:true});
      }
    }
    return holes.sort((a,b)=>a.y-b.y||a.x-b.x).slice(0,16);
  }
  // Ports: rasterise the front 6 mm of the model onto an X–Z grid (0.5 mm) and box each separate blob.
  // Thin strips (board edges) and blobs covering most of the front are skipped.
  function findPorts(v,mn,mx){
    const S=0.5,band=6,W=Math.ceil((mx[0]-mn[0])/S)+1,H=Math.ceil((mx[2]-mn[2])/S)+1;if(W*H>4e6)return [];
    const g=new Uint8Array(W*H);
    for(let i=0;i<v.length;i+=9){
      if(Math.min(v[i+1],v[i+4],v[i+7])>mn[1]+band)continue;
      const p=[0,3,6].map(o=>[(v[i+o]-mn[0])/S,(v[i+o+2]-mn[2])/S]);
      const x0=Math.max(0,Math.floor(Math.min(p[0][0],p[1][0],p[2][0]))),x1=Math.min(W-1,Math.ceil(Math.max(p[0][0],p[1][0],p[2][0])));
      const z0=Math.max(0,Math.floor(Math.min(p[0][1],p[1][1],p[2][1]))),z1=Math.min(H-1,Math.ceil(Math.max(p[0][1],p[1][1],p[2][1])));
      const ar=(a,b,c)=>(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]),A=ar(...p);if(Math.abs(A)<1e-9)continue;
      for(let z=z0;z<=z1;z++)for(let x=x0;x<=x1;x++){const q=[x,z],a=ar(p[1],p[2],q)/A,b=ar(p[2],p[0],q)/A,c=1-a-b;if(a>=-.05&&b>=-.05&&c>=-.05)g[z*W+x]=1;}
    }
    // Clear rows filled almost edge to edge (the board itself) so parts sitting on it separate.
    for(let z=0;z<H;z++){let n=0;for(let x=0;x<W;x++)n+=g[z*W+x];if(n>W*0.8)g.fill(0,z*W,z*W+W);}
    const seen=new Uint8Array(W*H),out=[];
    for(let s=0;s<W*H;s++){if(!g[s]||seen[s])continue;let minx=1e9,maxx=-1,minz=1e9,maxz=-1;const st=[s];seen[s]=1;
      while(st.length){const c=st.pop(),x=c%W,z=(c-x)/W;minx=Math.min(minx,x);maxx=Math.max(maxx,x);minz=Math.min(minz,z);maxz=Math.max(maxz,z);
        for(const n of[x>0?c-1:-1,x<W-1?c+1:-1,c-W,c+W])if(n>=0&&n<W*H&&g[n]&&!seen[n]){seen[n]=1;st.push(n);}}
      const w=(maxx-minx+1)*S,h=(maxz-minz+1)*S;
      if(h<2.5||w<2.5||w>(mx[0]-mn[0])*0.9&&h>(mx[2]-mn[2])*0.9)continue;
      out.push({cx:Math.round((minx+maxx+1)/2*S*10)/10,cz:Math.round((minz+maxz+1)/2*S*10)/10,w:Math.round(w*10)/10,h:Math.round(h*10)/10,keep:true});
    }
    return out.sort((a,b)=>a.cx-b.cx).slice(0,12);
  }
  // Device-local port (from its left/bottom) -> faceplate coordinates, with clearance.
  function portOnPlate(p){
    const lift=window.LabRaxPortOpenings.deviceLift(spec),clr=1;
    return {label:'',x:Math.round((p.cx-spec.dev_w/2)*10)/10,z:Math.round((lift+p.cz)*10)/10,w:p.w+2*clr,h:p.h+2*clr,r:1};
  }
  function applyImport(){
    const v=transformed(),mn=[1e9,1e9,1e9],mx=[-1e9,-1e9,-1e9];
    for(let i=0;i<v.length;i++){const a=i%3;if(v[i]<mn[a])mn[a]=v[i];if(v[i]>mx[a])mx[a]=v[i];}
    const r1=a=>Math.round(a*10)/10;spec.dev_w=r1(mx[0]-mn[0]);spec.dev_d=r1(mx[1]-mn[1]);spec.dev_h=r1(mx[2]-mn[2]);
    spec.u=window.LabRaxPortOpenings.autoU(spec);
    found=findHoles(v,mn[0],mn[1]);foundPorts=findPorts(v,mn,mx);
    importMsg='';
  }
  function topView(){
    const svg=document.getElementById('ewTop');if(!svg)return;const W=+spec.dev_w||1,D=+spec.dev_d||1;
    svg.setAttribute('viewBox',`-6 -6 ${W+12} ${D+12}`);
    let s=`<rect x="0" y="0" width="${W}" height="${D}" fill="#2c4a3c" stroke="#6fbf8f" stroke-width=".6"/><text x="${W/2}" y="${D+5}" font-size="4" fill="#9aa" text-anchor="middle">front (faceplate)</text>`;
    for(const p of spec.holes)s+=`<circle cx="${p[0]}" cy="${D-p[1]}" r="${(spec.hole_d||2.7)/2+.4}" fill="#e6c35c"/>`;
    found.forEach((c,i)=>{s+=`<circle cx="${c.x}" cy="${D-c.y}" r="${c.d/2+.6}" fill="none" stroke="${c.keep?'#5cc8ff':'#666'}" stroke-width=".6"/><text x="${c.x+c.d/2+1}" y="${D-c.y+1.5}" font-size="4" fill="#5cc8ff">${i+1}</text>`;});
    svg.innerHTML=s;
  }
  // ---- 3D preview in the wizard: render via /api/equipment-preview, draw with a small canvas painter.
  // Seen from behind and above, so the faceplate does not hide the device.
  let view={yaw:Math.PI+0.6,pitch:0.45,zoom:1.6,sets:[],quality:'wizard'};
  async function show3D(){
    const r=await fetch('/api/equipment-preview',{method:'POST',headers:{'Content-Type':'application/json','X-App-Token':token},body:JSON.stringify(spec)});
    const out=await r.json();if(!r.ok)throw Error(out.error||'Preview failed');
    const sets=[];
    for(const p of out.parts){const t=await (await fetch(`/api/equipment-mesh/${out.id}/${p}.stl`)).text();sets.push({v:parseStlBuffer(new TextEncoder().encode(t).buffer),color:p==='tray'?[77,142,110]:[78,117,163],alpha:1});}
    // Device ghost: imported model if any, else its bounding box, sitting where the tray holds it.
    const lift=window.LabRaxPortOpenings.deviceLift(spec),ox=-spec.dev_w/2,oy=spec.device_mount==='sleeve'?-4:12;let dv=[];
    if(imported){const v=transformed(),mn=[1e9,1e9,1e9];for(let i=0;i<v.length;i++)mn[i%3]=Math.min(mn[i%3],v[i]);for(let i=0;i<v.length;i+=3)dv.push(v[i]-mn[0]+ox,v[i+1]-mn[1]+oy,v[i+2]-mn[2]+lift);}
    else{const[x0,y0,z0,x1,y1,z1]=[ox,oy,lift,ox+ +spec.dev_w,oy+ +spec.dev_d,lift+ +spec.dev_h],c=[[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]];
      for(const f of[[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]])for(const i of f)dv.push(...c[i]);}
    sets.push({v:dv,color:[230,195,92],alpha:0.55});
    view.sets=sets;const cv=document.getElementById('ewView');cv.hidden=false;
    if(!cv.ewBound){cv.ewBound=true;bindView(cv,view,draw3D);}
    draw3D();
  }
  // ---- Step 1 model view: the imported model as oriented now, on a tray floor whose front edge is orange.
  let modelView={yaw:-0.6,pitch:0.45,zoom:1,sets:[],quality:'wizard'};
  function drawModel(){
    const cv=document.getElementById('ewModel');if(!cv||!imported)return;
    const v=transformed(),mn=[1e9,1e9,1e9],mx=[-1e9,-1e9,-1e9];
    for(let i=0;i<v.length;i++){const a=i%3;if(v[i]<mn[a])mn[a]=v[i];if(v[i]>mx[a])mx[a]=v[i];}
    const W=mx[0]-mn[0],D=mx[1]-mn[1],H=mx[2]-mn[2],m=8,dv=new Array(v.length);
    // Front (lowest y) faces the default camera, as in the rack view.
    for(let i=0;i<v.length;i+=3){dv[i]=v[i]-mn[0]-W/2;dv[i+1]=v[i+1]-mn[1];dv[i+2]=v[i+2]-mn[2];}
    const quad=(x0,y0,x1,y1,z)=>[x0,y0,z,x1,y0,z,x1,y1,z,x0,y0,z,x1,y1,z,x0,y1,z];
    modelView.cen=[0,D/2,H/2];modelView.span=Math.max(W,D,H)*1.6+2*m;
    modelView.sets=[{v:quad(-W/2-m,-m,W/2+m,D+m,-0.5),color:[60,70,84],alpha:1,under:true},{v:quad(-W/2-m,-m-6,W/2+m,-m,-0.4),color:[230,140,60],alpha:1,under:true},{v:dv,color:[120,160,210],alpha:1}];
    bindView(cv,modelView,()=>paint(cv,modelView));paint(cv,modelView);
  }
  // One line on what the import found, plus orientation warnings only when something looks off.
  function modelNote(){
    return `${imported.name} · found ${count(found.length,'possible mounting hole')} and ${count(foundPorts.length,'possible front port')}; confirm them on the Holes and Ports steps.`;
  }
  function modelWarn(){
    const w=[];
    if(spec.dev_h>spec.dev_d&&spec.dev_h>spec.dev_w*0.6)w.push('It is taller than it is deep, so it may be standing on its side. Try Y is up or X is up.');
    const width=window.TrayPlacement.widthProblem(spec);if(width)w.push(width);
    return w.join(' ');
  }
  // Small canvas painter, shared with the Place on tray window (tray-placement.js) as window.EquipmentPainter.
  function bindView(cv,view,redraw){
    // Fit and the view buttons go back to the view's starting zoom.
    const z0=view.z0??=view.zoom;
    window.ViewerControls.attach(cv,{getView:()=>view,setView:v=>Object.assign(view,v),redraw,
      fit:()=>{Object.assign(view,{zoom:z0,panX:0,panY:0});redraw();},
      presets:Object.fromEntries(Object.entries(window.ViewerControls.presets).map(([k,v])=>[k,{...v,zoom:z0}]))});
  }
  function draw3D(){const cv=document.getElementById('ewView');if(cv&&!cv.hidden)paint(cv,view);}
  // view.quality names the viewer for the preview-quality slider (render-quality.js); Medium draws as before.
  function paint(cv,view){
    const RQ=window.RenderQuality,q=RQ&&view.quality,dpr=q?RQ.pixelRatio(q,devicePixelRatio):devicePixelRatio,cell=q?RQ.cell(q):0;
    const W=cv.width=cv.clientWidth*dpr,H=cv.height=cv.clientHeight*dpr,ctx=cv.getContext('2d');
    ctx.fillStyle='#121418';ctx.fillRect(0,0,W,H);
    const cy=Math.cos(view.yaw),sy=Math.sin(view.yaw),cp=Math.cos(view.pitch),sp=Math.sin(view.pitch);
    const cen=view.cen||[0,40,25],sc=Math.min(W,H)/(view.span||280)*view.zoom,L=[0.3,-0.5,0.8];
    // Same camera as the rack view (rack-studio.js camera): yaw 0 looks at the front (lowest y), pitch > 0 looks down.
    // Returns screen x, y and depth (larger = farther).
    const P=(x,y,z)=>{x-=cen[0];y-=cen[1];z-=cen[2];return[W/2+(view.panX||0)*dpr+(x*cy-y*sy)*sc,H/2+(view.panY||0)*dpr-(sp*(x*sy+y*cy)+z*cp)*sc,cp*(x*sy+y*cy)-z*sp];};
    const tris=[];
    for(const s of view.sets){const v=cell?RQ.simplify(s.v,cell):s.v;for(let i=0;i<v.length;i+=9){
      const a=P(v[i],v[i+1],v[i+2]),b=P(v[i+3],v[i+4],v[i+5]),c=P(v[i+6],v[i+7],v[i+8]);
      const ux=v[i+3]-v[i],uy=v[i+4]-v[i+1],uz=v[i+5]-v[i+2],wx=v[i+6]-v[i],wy=v[i+7]-v[i+1],wz=v[i+8]-v[i+2];
      let nx=uy*wz-uz*wy,ny=uz*wx-ux*wz,nz=ux*wy-uy*wx;const n=Math.hypot(nx,ny,nz)||1;
      const lit=0.45+0.55*Math.abs((nx*L[0]+ny*L[1]+nz*L[2])/n);
      tris.push([a,b,c,(a[2]+b[2]+c[2])/3,s,lit]);}}
    tris.sort((p,q)=>(q[4].under?1:0)-(p[4].under?1:0)||q[3]-p[3]);  // under: floor sets, always drawn first
    for(const[a,b,c,,s,lit]of tris){ctx.fillStyle=`rgba(${s.color.map(k=>Math.round(k*lit)).join(',')},${s.alpha})`;
      ctx.beginPath();ctx.moveTo(a[0],a[1]);ctx.lineTo(b[0],b[1]);ctx.lineTo(c[0],c[1]);ctx.closePath();ctx.fill();if(s.alpha===1){ctx.strokeStyle=ctx.fillStyle;ctx.stroke();}}
  }
  window.EquipmentPainter={draw:paint,bind:bindView,parseStl:parseStlBuffer};
  function reset(){uExplicit=false;imported=null;importMsg='';found=[];foundPorts=[];orient=0;turn=0;spec={name:'',dev_w:85,dev_d:56,dev_h:20,u:1,hole_d:2.7,standoff:6,insert_pilot:3.2,board_t:1.6,device_mount:'inserts',joint:'screw',holes:[],ports:[],rear_ports:[],keystones:[]};step=0;}
  // Cable-planning port id (cable-ports.js): stable while the port is edited or moves between faces.
  const portId=()=>'p-'+Math.random().toString(36).slice(2,10);
  const PORT_TYPES=()=>Object.fromEntries(Object.entries(window.LabRaxPorts?.TYPES||{other:{label:'Other'}}).map(([k,v])=>[k,v.label]));
  // Starting opening size per connector type (port-openings.js, Brian 2026-10-19): an editable guess, never a measured size.
  // Only ports added by hand in this window get it, and only until W/H/r is edited; saved and model-found ports keep their sizes.
  const autoSize=new WeakSet();
  const startSize=t=>window.LabRaxPortOpenings?.defaultSize(t)||{w:15,h:8,r:1};
  const SIZE_NOTE=()=>window.LabRaxPortOpenings?.SIZE_NOTE||'Starting size: a guess, not a measured size. Edit it to match your device.';
  function select(options,value,onchange){const s=h('select',{});for(const[v,t]of Object.entries(options)){const o=h('option',{value:v},t);if(v===value)o.selected=true;s.append(o);}s.onchange=()=>onchange(s.value);return s;}
  const h=(tag,attrs={},...kids)=>{const e=document.createElement(tag);for(const[k,v]of Object.entries(attrs)){if(k.startsWith('on'))e[k]=v;else e.setAttribute(k,v);}e.append(...kids);return e;};
  function field(label,key,obj=spec,extra={}){
    const input=h('input',{type:'number',step:'0.1',value:obj[key],...extra});
    input.oninput=()=>{if(obj===spec&&key==='u')uExplicit=true;obj[key]=input.value===''?'':Number(input.value);preview();topView();fitWarn();};
    return h('label',{class:'ew-field'},label,input);
  }
  function plateH(){return window.LabRaxPortOpenings.plateHeight(spec.u);}
  // Non-blocking heads-up: width/depth screened against the selected rack (or nominal 208 × 240 mm).
  function fitWarn(){
    const box=document.getElementById('ewFitWarn');if(!box)return;const screen=window.WorkshopClearance?.screen;if(!screen){box.hidden=true;return;}
    const rack=window.activeRackNumbers?.()||{width_mm:208,depth_mm:240,pitch_mm:44.45};
    const r=screen(rack,{equipment:'eq-draft',span:+spec.u||1},{spec});
    const issues=r.checks.filter(c=>(c.name==='width'||c.name==='depth')&&(c.level==='over'||c.level==='tight'));
    const width=window.TrayPlacement.widthProblem(spec);if(width){box.hidden=false;box.textContent=width;return;}
    box.hidden=!issues.length;
    box.textContent=issues.length?'Heads up: '+issues.map(c=>c.text).join(' ')+' You can still continue; this is a screening warning, and fit stays UNKNOWN.':'';
  }
  function preview(){
    const svg=document.getElementById('ewPreview');if(!svg)return;const H=plateH();
    svg.setAttribute('viewBox',`${-PLATE_W/2-2} ${-H-2} ${PLATE_W+4} ${H+4}`);
    let s=`<rect x="${-PLATE_W/2}" y="${-H-window.LabRaxPortOpenings.plateBottom}" width="${PLATE_W}" height="${H}" fill="#3b6f8f" rx="2.5"/>`;
    for(let i=0;i<spec.u;i++)for(const dz of[-15.902,15.902])for(const x of[-118.2625,118.2625])s+=`<rect x="${x-5}" y="${-(i*44.45+44.45/2+dz)-3.5}" width="10" height="7" rx="3.5" fill="#1d1f24"/>`;
    for(const x of spec.keystones)s+=`<rect x="${x-7.4}" y="${-spec.u*44.45/2-8.3}" width="14.8" height="16.6" fill="#1d1f24"/>`;
    const sw=window.LabRaxPortOpenings.sleeve(spec);if(sw)s+=`<rect x="${sw.x-sw.half}" y="${-sw.top}" width="${sw.width}" height="${sw.height}" fill="#1d1f24"/>`;
    for(const p of window.LabRaxPortOpenings.sleevePorts(spec.ports,spec).ports)s+=`<rect x="${p.x-p.w/2}" y="${-p.z-p.h/2}" width="${p.w}" height="${p.h}" rx="${p.r||0}" fill="#1d1f24"/>`;
    for(const fp of foundPorts){const p=portOnPlate(fp);s+=`<rect x="${p.x-p.w/2}" y="${-p.z-p.h/2}" width="${p.w}" height="${p.h}" fill="none" stroke="${fp.keep?'#5cc8ff':'#666'}" stroke-width=".8" stroke-dasharray="2 1"/>`;}
    const tw=Number(spec.dev_w)+16;s+=`<rect x="${-tw/2}" y="${-window.LabRaxPortOpenings.floorZ(spec)-3}" width="${tw}" height="3" fill="#aab" opacity=".6"/>`;
    svg.innerHTML=s;
  }
  // Last-step summary; counts front openings and rear ports separately (rear ports get no opening).
  const count=(n,one)=>n+' '+one+(n===1?'':'s');
  function summary(spec){return `${spec.name||'Equipment'}: ${spec.dev_w} × ${spec.dev_d} × ${spec.dev_h} mm, ${count(spec.holes.length,'hole')}, ${count(spec.ports.length,'front opening')}, ${count((spec.rear_ports||[]).length,'rear port')}. Tray defaults for new slots: ${spec.u}U, ${MOUNTS[spec.device_mount]}, ${JOINTS[spec.joint]}, ${count(spec.keystones.length,'keystone')}.`;}
  function body(){
    if(step===0){
      const name=h('input',{type:'text',value:spec.display_name??spec.name,placeholder:'e.g. Network switch'});name.oninput=()=>{if(spec.display_name!==undefined)spec.display_name=name.value;else spec.name=name.value;};
      const file=h('input',{type:'file',accept:'.stl,.scad,.step,.stp'});
      file.onchange=async()=>{const f=file.files[0];if(!f)return;
        try{let buf;
          if(/\.(scad|step|stp)$/i.test(f.name)){const step=!/\.scad$/i.test(f.name);
            if(f.size>60e6)throw Error(`${f.name} is ${Math.round(f.size/1e6)} MB; models must be 60 MB or smaller.`);importMsg='Rendering '+f.name+(step?' with FreeCAD':' with OpenSCAD')+'… this can take a minute.';render();
            const r=await fetch(step?'/api/step-to-stl':'/api/scad-to-stl',{method:'POST',headers:{'Content-Type':'application/json','X-App-Token':token},body:JSON.stringify({source:await f.text()})});
            if(!r.ok)throw Error((await r.json().catch(()=>({}))).error||(step?'STEP conversion failed':'SCAD render failed'));buf=await r.arrayBuffer();}
          else buf=await f.arrayBuffer();
          imported={name:f.name,tris:parseStlBuffer(buf)};orient=0;turn=0;if(!spec.name)spec.name=f.name.replace(/\.(stl|scad|step|stp)$/i,'');applyImport();}
        catch(e){importMsg='Could not read that file: '+e.message;}render();};
      const imp=[h('div',{class:'ew-row'},h('b',{},'Import a model (STL, SCAD or STEP)'),file)];
      if(imported){
        const o=h('div',{class:'ew-choices'},...['Z is up','Y is up','X is up'].map((t,i)=>{const b=h('button',{type:'button',class:'ew-chip'+(orient===i?' on':'')},t);b.onclick=()=>{orient=i;applyImport();render();};return b;}));
        const r=h('button',{type:'button',class:'ew-chip'},'↻ Rotate 90°');r.onclick=()=>{turn=(turn+1)%4;applyImport();render();};
        imp.push(h('div',{class:'ew-row'},'Orientation:',o,r));
        imp.push(h('canvas',{id:'ewModel',class:'ew-model'}),h('p',{class:'ew-note ew-hint'},'Left-drag turns · right-drag moves · scroll zooms at the cursor · Z fits · orange edge = front (faceplate side)'),h('p',{class:'ew-note'},modelNote()));
        const hint=window.LabRaxPortOpenings.flatHint(spec);if(hint)imp.push(h('p',{class:'ew-note'},hint));
        const warn=modelWarn();if(warn)imp.push(h('p',{class:'ew-note ew-warn'},warn));
      }
      if(importMsg)imp.push(h('p',{class:'ew-note'},importMsg));
      return [h('label',{class:'ew-field'},'Name',name),...imp,
        h('div',{class:'ew-row'},h('b',{},'Size (mm)'),field('Width','dev_w'),field('Depth','dev_d'),field('Height','dev_h')),
        h('p',{class:'ew-note'},window.TrayPlacement.warnings(spec,window.TrayPlacement.values(spec)).join(' ')),h('p',{id:'ewFitWarn',class:'ew-note ew-warn',hidden:''}),
        ...(imported?[]:[h('p',{class:'ew-note'},'Import a model to fill in the size and find mounting holes, or type the measurements. Width is left–right, depth is front–back, all in millimetres. A SCAD file must be self-contained (no include/use).')])];
    }
    if(step===1){
      const rows=spec.holes.map((p,i)=>{const del=h('button',{type:'button',class:'ew-chip'},'Remove');del.onclick=()=>{spec.holes.splice(i,1);render();};
        return h('div',{class:'ew-row'},`Hole ${i+1}`,field('X','0',p),field('Y','1',p),del);});
      const add=h('button',{type:'button',class:'ew-chip'},'+ Add hole');add.onclick=()=>{spec.holes.push([3.5,3.5]);render();};
      const confirmBox=[];
      if(found.length){
        confirmBox.push(h('p',{},`I found ${found.length} possible mounting hole${found.length>1?'s':''} in the model. Tick the real ones, then press “Use ticked holes”.`));
        confirmBox.push(h('div',{class:'ew-row'},...found.map((c,i)=>{const cb=h('input',{type:'checkbox'});cb.checked=c.keep;cb.onchange=()=>{c.keep=cb.checked;topView();};
          return h('label',{class:'ew-chip'},cb,` ${i+1}: X ${c.x} · Y ${c.y} · Ø ${c.d}`);})));
        const use=h('button',{type:'button',class:'primary'},'Use ticked holes');
        use.onclick=()=>{const k=found.filter(c=>c.keep);spec.holes=k.map(c=>[c.x,c.y]);if(k.length){const ds=k.map(c=>c.d).sort((a,b)=>a-b);spec.hole_d=ds[Math.floor(ds.length/2)];}found=[];render();};
        confirmBox.push(use);
      }else if(imported)confirmBox.push(h('p',{class:'ew-note'},'No round holes found in the model. Add them by hand below.'));
      return [h('p',{},'Where are the device’s mounting holes? Leave the list empty if it has none.'),field('Hole diameter (mm)','hole_d'),...confirmBox,
        h('svg',{id:'ewTop',class:'ew-top'}),
        h('p',{class:'ew-note'},'Hole positions are measured from the device’s front-left corner, seen from above (front = faceplate side, at the bottom of the picture).'),...rows,add];
    }
    if(step===2){
      spec.rear_ports=spec.rear_ports||[];
      // Front ports cut a faceplate opening; rear ports are cable-planning only (no opening, so no W/H/r).
      const row=(list,p,i,face)=>{const lab=h('input',{type:'text',value:p.label,placeholder:'USB, HDMI…',style:'width:90px'});lab.oninput=()=>p.label=lab.value;
        if(!p.id)p.id=portId();
        const type=select(PORT_TYPES(),p.type||'other',v=>{p.type=v;if(face==='front'&&autoSize.has(p)){Object.assign(p,startSize(v));render();}});
        const side=select({front:'Front (opening)',rear:'Rear (no opening)'},face,v=>{list.splice(i,1);
          if(v==='rear')spec.rear_ports.push({id:p.id,label:p.label,type:p.type||'other',x:p.x,z:p.z});
          else{const q={id:p.id,label:p.label,type:p.type||'other',x:p.x,z:p.z,...startSize(p.type)};autoSize.add(q);spec.ports.push(q);}render();});
        const del=h('button',{type:'button',class:'ew-chip'},'Remove');del.onclick=()=>{list.splice(i,1);render();};
        const dims=face==='front'?[field('W','w',p),field('H','h',p),field('Corner r','r',p)]:[];
        const guess=face==='front'&&autoSize.has(p)?h('span',{class:'ew-note ew-size-guess'},SIZE_NOTE()):null;
        for(const d of dims)d.querySelector('input').addEventListener('input',()=>{autoSize.delete(p);guess?.remove();});
        if(guess)dims.push(guess);
        return h('div',{class:'ew-row'},lab,h('label',{class:'ew-field'},'Type',type),h('label',{class:'ew-field'},'Face',side),field('X','x',p),field('Z','z',p),...dims,del);};
      const rows=[...spec.ports.map((p,i)=>row(spec.ports,p,i,'front')),...spec.rear_ports.map((p,i)=>row(spec.rear_ports,p,i,'rear'))];
      const add=h('button',{type:'button',class:'ew-chip'},'+ Add port opening');add.onclick=()=>{const q={id:portId(),label:'',type:'other',x:0,z:Math.round(plateH()/2),...startSize('other')};autoSize.add(q);spec.ports.push(q);render();};
      const sugg=[];
      if(foundPorts.length){
        sugg.push(h('p',{},`The model shows ${foundPorts.length} thing${foundPorts.length>1?'s':''} on its front edge that may need an opening (dashed outlines below). Tick the real ports, then press “Use ticked ports”. 1 mm clearance is added on each side.`));
        sugg.push(h('div',{class:'ew-row'},...foundPorts.map((p,i)=>{const cb=h('input',{type:'checkbox'});cb.checked=p.keep;cb.onchange=()=>{p.keep=cb.checked;preview();};
          return h('label',{class:'ew-chip'},cb,` ${i+1}: ${p.w} × ${p.h} mm`);})));
        const use=h('button',{type:'button',class:'primary'},'Use ticked ports');
        use.onclick=()=>{foundPorts.filter(p=>p.keep).forEach((p,i)=>spec.ports.push({...portOnPlate(p),id:portId(),type:'other',label:'Port '+(spec.ports.length+1)}));foundPorts=[];render();};
        sugg.push(use);
      }else if(imported&&!spec.ports.length)sugg.push(h('p',{class:'ew-note'},'Nothing found sticking out at the model’s front. Add openings by hand if needed.'));
      return [h('p',{},'Which ports need an opening in the faceplate? X is from the faceplate centre; Z is height from its bottom edge.'),...sugg,...rows,add,
        h('p',{class:'ew-note'},'Type and Face are cable-planning data for the Cables view. Rear ports get no opening. Keystones become front/rear pass-through port pairs automatically. Connector fit and cable access stay UNKNOWN.'),
        h('p',{class:'ew-note'},'Current device lift is '+window.LabRaxPortOpenings.deviceLift(spec)+' mm above the faceplate bottom. Entered opening heights stay as entered when the tray default mount changes; check them against this lift. In Place on tray, front openings move with the device’s left/right offset and standoff. Position, mounting, standoff, faceplate height, keystones and rear support are chosen per slot in the Place on tray window after you place the item.'),...finish()];
    }
  }
  function mountProblem(){
    return !spec.holes.length&&['inserts','pegs'].includes(spec.device_mount)?'Add at least one mounting hole for inserts or pegs, or choose another tray default mount below (e.g. Sits flat).':'';
  }
  function finish(){
    const mount=select(MOUNTS,spec.device_mount,v=>{spec.device_mount=v;if(!uExplicit)spec.u=window.LabRaxPortOpenings.autoU(spec);render();});
    const go=h('button',{type:'button',class:'primary'},'Generate STL files');
    const status=h('p',{class:'ew-note'},'Fit, strength and rack clearance stay UNKNOWN until a print is tested.');
    go.onclick=async()=>{const problem=window.TrayPlacement.problems(spec,window.TrayPlacement.values(spec)).join(' ');if(problem){status.textContent='Problem: '+problem;return;}go.disabled=true;status.textContent='Rendering with OpenSCAD… this can take a minute.';
      // Export quality goes with this build request only; the spec and the library item never keep it.
      const quality=window.RenderQuality?.exportLevel()||'standard';
      try{const r=await fetch('/api/equipment-build',{method:'POST',headers:{'Content-Type':'application/json','X-App-Token':token},body:JSON.stringify({...spec,quality})});
        if(!r.ok)throw Error((await r.json()).error||'Build failed');
        const url=URL.createObjectURL(await r.blob()),a=document.createElement('a');a.href=url;a.download=(spec.name||'equipment').replace(/[^\w-]+/g,'_')+'-stl.zip';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
        status.textContent=`Done (${window.RenderQuality?.exportNote(quality)||'Standard'}). The zip holds the STL file(s), the .scad source, a report and export.json.`;}
      catch(e){status.textContent='Problem: '+e.message;}finally{go.disabled=false;}};
    const look=h('button',{type:'button'},'Show 3D preview');
    look.onclick=async()=>{const problem=window.TrayPlacement.problems(spec,window.TrayPlacement.values(spec)).join(' ');if(problem){status.textContent='Problem: '+problem;return;}look.disabled=true;status.textContent='Rendering preview with OpenSCAD…';
      try{await show3D();status.textContent='Left-drag turns, right-drag moves, scroll zooms at the cursor, Z fits. Translucent box = the device. Not saved yet.';}
      catch(e){status.textContent='Problem: '+e.message;}finally{look.disabled=false;}};
    const keep=h('button',{type:'button',class:'primary'},'Save to equipment library');
    keep.onclick=async()=>{const problem=mountProblem()||window.TrayPlacement.problems(spec,window.TrayPlacement.values(spec)).join(' ');if(problem){status.textContent='Problem: '+problem;return;}keep.disabled=true;status.textContent='Rendering and saving… this can take a minute.';
      try{const r=await fetch('/api/equipment-library',{method:'POST',headers:{'Content-Type':'application/json','X-App-Token':token},body:JSON.stringify(spec)});
        const item=await r.json();if(!r.ok)throw Error(item.error||'Save failed');spec.id=item.id;await loadLibrary();
        status.textContent='Saved. Close this, select an empty rack slot, then click “'+item.name+'” in the Equipment list to place it; the Place on tray window opens for that slot.';}
      catch(e){status.textContent='Problem: '+e.message;}finally{keep.disabled=false;}};
    setTimeout(fitWarn);
    return [h('h3',{},'Save'),h('p',{class:'ew-note ew-warn'},mountProblem()||window.TrayPlacement.problems(spec,window.TrayPlacement.values(spec)).join(' ')),h('label',{class:'ew-field'},'Tray default mount',mount),h('p',{class:'ew-note'},window.TrayPlacement.warnings(spec,window.TrayPlacement.values(spec)).join(' ')),h('p',{id:'ewFitWarn',class:'ew-note ew-warn',hidden:''}),h('p',{},summary(spec)),h('div',{class:'ew-row'},look,keep,go,window.RenderQuality?.exportSlider()||''),status,h('canvas',{id:'ewView',class:'ew-view',hidden:''}),window.RenderQuality?.previewSlider('wizard',draw3D)||''];
  }
  function render(){
    const d=document.getElementById('equipmentWizard');
    const tabs=h('div',{class:'ew-steps'},...STEPS.map((s,i)=>{const b=h('button',{type:'button',class:'ew-step'+(i===step?' on':'')},`${i+1}. ${s}`);b.onclick=()=>{step=i;render();};return b;}));
    const back=h('button',{type:'button'},'Back'),next=h('button',{type:'button',class:'primary'},'Next'),close=h('button',{type:'button'},'Close');
    back.disabled=step===0;next.hidden=step===STEPS.length-1;back.onclick=()=>{step--;render();};next.onclick=()=>{step++;render();};close.onclick=()=>d.close();
    d.replaceChildren(h('h2',{},spec.id?'Edit equipment':'New equipment'),
      ...(spec.id?[h('p',{class:'ew-note'},'Saving updates this item everywhere it is placed. Changing its rack-unit height does not resize slots already placed.')]:[]),tabs,h('div',{class:'ew-body'},...body()),
      h('p',{class:'ew-note ew-cap'},'Faceplate, seen from the front'),h('svg',{id:'ewPreview',class:'ew-preview'}),h('div',{class:'ew-nav'},close,back,next));
    // innerHTML on an SVG created via createElement needs the SVG namespace
    const old=document.getElementById('ewPreview'),svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.id='ewPreview';svg.setAttribute('class','ew-preview');old.replaceWith(svg);
    const oldTop=document.getElementById('ewTop');if(oldTop){const t=document.createElementNS('http://www.w3.org/2000/svg','svg');t.id='ewTop';t.setAttribute('class','ew-top');oldTop.replaceWith(t);topView();}
    preview();fitWarn();if(step===0)drawModel();
  }
  // ---- Equipment library: list in the Equipment pane, place into slots, real meshes in the rack view.
  let items=[];const meshes=new Map(),rebuilding=new Set();let libraryNotice='';
  async function loadLibrary(){
    let failed=false,statuses={};
    try{const r=await fetch('/api/equipment-library');if(!r.ok)throw Error();items=await r.json();if(!Array.isArray(items))throw Error();}catch(e){items=[];failed=true;}
    if(!failed)try{const r=await fetch('/api/equipment-template-status');if(r.ok)statuses=await r.json();}catch(e){}
    const host=document.getElementById('ewLibrary');if(!host)return;
    const notice=h('p',{class:'ew-note',role:'status'},libraryNotice);
    const empty=failed?h('div',{class:'empty-library'},'Couldn’t load your equipment library.'):
      h('div',{class:'empty-library'},'No custom equipment yet.',h('br'),h('small',{},'Use + New equipment from dimensions; saved items appear here. Fit UNKNOWN.'));
    host.replaceChildren(h('p',{class:'section-eyebrow'},'MY EQUIPMENT'),notice,...(items.length?[]:[empty]),...items.map(it=>{
      const display=it.display_name||it.name;
      const b=h('button',{type:'button',class:'equipment-card ew-item',title:'Select an empty slot, then click to place'},h('b',{},display),h('span',{class:'ew-note'},` ${it.spec.dev_w}×${it.spec.dev_d}×${it.spec.dev_h} mm · ${it.span}U`),
        h('span',{class:'ew-note'},` ${it.status||'PROPOSED — UNVALIDATED'} · Fit UNKNOWN`));
      b.onclick=()=>window.placeLibraryEquipment&&window.placeLibraryEquipment(it);
      const edit=h('button',{type:'button',class:'ew-chip'},'Edit');edit.onclick=()=>editItem(it);
      const del=h('button',{type:'button',class:'ew-chip',title:'Remove from library'},'Delete');
      del.onclick=async()=>{if(!confirm('Delete “'+display+'” from your equipment library?'))return;
        try{const r=await fetch('/api/equipment-library-delete',{method:'POST',headers:{'Content-Type':'application/json','X-App-Token':token},body:JSON.stringify({id:it.id})});
          const out=await r.json();if(!r.ok)throw Error(out.error);await loadLibrary();}catch(e){alert(e.message);}};
      const status=statuses?.[it.id]||{status:'unknown_evidence',reason:'Template status unknown — build evidence unavailable.'};
      const label={older_source:'Older template/source',matches_source_unknown_pipeline:'Up to date: built from the current template',needs_review:'Needs review',unknown_evidence:'Template status unknown — build evidence unavailable.',integrity_problem:'Build integrity problem'}[status.status]||'Template status unknown — build evidence unavailable.';
      const badge=h('span',{class:'ew-note'},label),details=h('p',{class:'ew-note'},status.status==='older_source'?'A newer equipment template is available. The saved build is unchanged. Printed fit and strength remain UNKNOWN.':status.status!=='matches_source_unknown_pipeline'&&status.reason&&status.reason!==label?status.reason:'');
      const extra=[];
      // Brian, 2026-10-19: only an older template offers a rebuild; an item built from the current template has nothing to rebuild.
      if(status.status==='older_source'){
        const key=it.id+'/'+it.build,rebuild=h('button',{type:'button',class:'ew-chip'},'Rebuild as new item');
        rebuild.disabled=rebuilding.has(key);
        rebuild.onclick=async()=>{
          if(rebuilding.has(key))return;rebuilding.add(key);rebuild.disabled=true;
          notice.textContent=libraryNotice='Rebuilding a copy…';
          try{
            const r=await fetch('/api/equipment-rebuild-copy',{method:'POST',headers:{'Content-Type':'application/json','X-App-Token':token},body:JSON.stringify({id:it.id,expected_build:it.build})});
            const out=await r.json();if(!r.ok)throw Error(out.error||'Rebuild failed');
            libraryNotice=out.reused_build?'Created a new item using its verified current-template build. Existing placements are unchanged.':`Created ‘${out.item.display_name||out.item.name}’. Existing placements are unchanged. PROPOSED — UNVALIDATED; fit and strength UNKNOWN.`;
            rebuilding.delete(key);
            await loadLibrary();
          }catch(e){notice.textContent=libraryNotice='Rebuild failed. The original item and your rack draft are unchanged. '+e.message;}
          finally{rebuilding.delete(key);rebuild.disabled=false;}
        };
        extra.push(rebuild,h('p',{class:'ew-note'},'Creates a new library item with the current template. Existing rack placements keep the original. No STL download.'));
      }
      return h('div',{class:'ew-row'},b,edit,del,badge,details,...extra);}));
    window.dispatchEvent(new Event('equipment-library'));redraw();
  }
  window.equipmentLibraryItems=()=>items;
  function editItem(it){open();uExplicit=true;spec=JSON.parse(JSON.stringify({...it.spec,id:it.id,...(it.display_name!==undefined?{display_name:it.display_name}:{})}));render();}
  // Called by workspace.js openAssembly() for eq- placements ("Edit equipment").
  window.openCustomEquipment=async placement=>{
    if(!items.some(i=>i.id===placement.equipment))await loadLibrary();
    const it=items.find(i=>i.id===placement.equipment);
    if(!it){alert('This equipment is no longer in the library.');return;}
    editItem(it);
  };
  // Keep the list fresh: when the Equipment section opens and when the window regains focus.
  document.addEventListener('toggle',e=>{if(e.target.id==='equipmentSection'&&e.target.open)loadLibrary();},true);
  window.addEventListener('focus',()=>loadLibrary());
  function parseStl(text){
    const M=window.LabRaxStudio.Mesh,m=new M(),v=[...text.matchAll(/vertex\s+(\S+)\s+(\S+)\s+(\S+)/g)].map(a=>[+a[1],+a[2],+a[3]]);
    for(let i=0;i+2<v.length;i+=3)m.tri(v[i],v[i+1],v[i+2]);return m;
  }
  // Rack view (Brian 2026-10-19): every slot shows its own effective tray. Without slot tray settings it is the library
  // item's own build. With them (Place on tray), it is an exact render of those settings when one already exists
  // (looked up only, never rendered here: no automatic builds), otherwise a box sketch of the same settings.
  const placed=new Map(); // item build + tray json -> null (looking up) | {id,parts} (exact render) | {sketch:true}
  function meshesOf(id,parts){
    if(!meshes.has(id)){meshes.set(id,null);Promise.all(parts.map(p=>fetch(`/api/equipment-mesh/${id}/${p}.stl`).then(r=>{if(!r.ok)throw Error(r.status);return r.text();}).then(t=>[p,parseStl(t)])))
      .then(list=>{meshes.set(id,Object.fromEntries(list));redraw();if([...placed.values()].some(f=>f&&f.id===id))changed();}).catch(()=>meshes.delete(id));}
    return meshes.get(id);
  }
  const hasTray=a=>!!a?.tray&&typeof a.tray==='object'&&Object.keys(a.tray).length>0;
  // Library spec with the slot's tray choices on top (equipment.allocation_spec; TrayPlacement.values fills defaults).
  // Front openings follow the device's offset and standoff (port-openings.js), as equipment.allocation_spec() cuts them.
  function effectiveSpec(spec,tray){const T=window.TrayPlacement,out=T?{...spec,...T.values(spec,tray)}:{...spec,...tray},P=window.LabRaxPortOpenings;
    if(P&&tray&&spec.ports)out.ports=P.frontOpenings(spec,tray).ports;return out;}
  function lookup(it,a){
    const key=it.build+'|'+JSON.stringify(a.tray);
    if(!placed.has(key)){placed.set(key,null);
      fetch('/api/equipment-placement-mesh',{method:'POST',headers:{'Content-Type':'application/json','X-App-Token':token},body:JSON.stringify({item:it.id,tray:a.tray})})
        .then(r=>r.json()).then(out=>{placed.set(key,out&&out.cached?{id:out.id,parts:out.parts}:{sketch:true});redraw();if(out&&out.cached)changed();})
        .catch(()=>placed.set(key,{sketch:true}));}
    return {key,found:placed.get(key)};
  }
  const sketches=new Map();
  function sketchParts(key,a,it){
    if(sketches.has(key))return sketches.get(key);const T=window.TrayPlacement;if(!T)return null;const M=window.LabRaxStudio.Mesh;
    const mesh=flat=>{const m=new M();for(let i=0;i+8<flat.length;i+=9)m.tri(flat.slice(i,i+3),flat.slice(i+3,i+6),flat.slice(i+6,i+9));return m;};
    const out=Object.fromEntries(Object.entries(T.rackSketch(it.spec,a.tray)).map(([p,flat])=>[p,mesh(flat)]));
    sketches.set(key,out);return out;
  }
  function partsFor(a){
    const it=items.find(i=>i.id===a.equipment);if(!it)return null;
    if(it.build&&!hasTray(a)){const parts=meshesOf(it.build,it.parts);return parts&&{item:it,spec:it.spec,parts,key:it.build,view:'library'};}
    const spec=effectiveSpec(it.spec,a.tray),{key,found}=lookup(it,a);
    if(found&&found.id){const parts=meshesOf(found.id,found.parts);if(parts)return {item:it,spec,parts,key:found.id,view:'exact'};}
    const parts=sketchParts(key,a,it);return parts&&{item:it,spec,parts,key:'sketch-'+hash(key),view:'sketch'};
  }
  function hash(s){let h=2166136261;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619);}return (h>>>0).toString(36);}
  // workspace.js asks what a slot shows ('library' | 'exact' | 'sketch'); tray-placement.js calls refresh() after an
  // exact preview or STL build, so a slot whose settings now have an exact render switches from the sketch to it.
  window.EquipmentRackView={
    status(a){if(!String(a?.equipment).startsWith('eq-'))return null;const it=items.find(i=>i.id===a.equipment);if(!it)return null;if(it.build&&!hasTray(a))return 'library';
      const f=placed.get(it.build+'|'+JSON.stringify(a.tray));return f&&f.id&&meshes.get(f.id)?'exact':'sketch';},
    refresh(){for(const[k,v]of placed)if(!v||v.sketch)placed.delete(k);redraw();}
  };
  // Same as rack-studio.js rgb() (not exported there).
  function rgb(hex,fallback){return /^#[0-9a-f]{6}$/i.test(hex||'')?[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255):rgb(fallback,'#657582');}
  function redraw(){window.dispatchEvent(new Event('resize'));}
  function changed(){window.dispatchEvent(new Event('equipment-rack-view'));}
  // Image window and selection outline from the plate mesh's own front face (lowest-Y vertices): actual width, height and U span.
  const fronts=new WeakMap();
  // Port and keystone openings in the same frame (X from centre, Z above the plate base), as equipment_tray.scad cuts them.
  function openings(spec,z0,plateH){
    const sw=window.LabRaxPortOpenings.sleeve(spec||{});
    return [...(sw?[{x:sw.x,z:(sw.bottom+sw.top)/2,w:sw.width,h:sw.height}]:[]),...(spec?.keystones||[]).map(x=>({x:+x,z:z0+plateH/2,w:14.8,h:16.6})), // ks_w x ks_h
            ...(spec?.ports||[]).map(p=>({x:+p.x,z:+p.z,w:+p.w,h:+p.h}))].filter(o=>[o.x,o.z,o.w,o.h].every(Number.isFinite));
  }
  function frontFace(mesh,spec){
    if(fronts.has(mesh))return fronts.get(mesh);let y0=Infinity;for(const v of mesh.vertices)y0=Math.min(y0,v[1]);
    let x0=Infinity,x1=-Infinity,z0=Infinity,z1=-Infinity;
    for(const v of mesh.vertices)if(v[1]<y0+.01){x0=Math.min(x0,v[0]);x1=Math.max(x1,v[0]);z0=Math.min(z0,v[2]);z1=Math.max(z1,v[2]);}
    // The image keeps clear of openings: artworkRect picks the largest clear part of this window for the image's aspect.
    const S=window.LabRaxStudio,f=x1>x0&&z1>z0?{art:{...S.artworkWindow(x1-x0,z1-z0,z0),openings:openings(spec,z0,z1-z0)},sel:S.selectionRect(x0,x1,z0,z1,2.5)}:null; // 2.5 = plate_r in equipment_tray.scad
    fronts.set(mesh,f);return f;
  }
  function patchRenderer(){
    const R=window.LabRaxStudio?.Renderer;if(!R||R.prototype.ewPatched)return !!R;R.prototype.ewPatched=true;
    const base=R.prototype.objects;
    R.prototype.objects=function(scene,ms,rack,selectedSlot){
      const objects=base.apply(this,arguments);
      for(const a of rack?.placements||[]){
        if(!String(a.equipment).startsWith('eq-'))continue;const got=partsFor(a);if(!got)continue;
        const proto=objects.find(o=>o.slot===a.slot&&o.key==='studio-tray');if(!proto)continue;
        for(let i=objects.length-1;i>=0;i--)if(objects[i].slot===a.slot&&String(objects[i].key).startsWith('studio-'))objects.splice(i,1);
        const ap=a.assembly?.appearance||{},z=(rack.slots-(a.slot+a.span-1))*44.45,sel=selectedSlot>=a.slot&&selectedSlot<a.slot+a.span;
        // Preview only: the image is drawn on the front faceplate; wizard STLs never contain artwork.
        for(const[p,mesh]of Object.entries(got.parts)){const plate=p!=='tray',face=p==='faceplate'?frontFace(mesh,got.spec):null,front=ap.artwork?face?.art:null;
          // The renderer caches GPU buffers by key, so each build/part needs its own key (else an unrelated plate buffer is reused).
          objects.push({...proto,key:`studio-eq-${got.key}-${p}`,mesh,t:[0,0,z],kind:plate?'plate':'tray',selected:p==='faceplate'&&sel,selRect:face?.sel,
            color:p==='openings'?[0.12,0.13,0.15]:rgb(plate?ap.faceplate:ap.tray,plate?'#4e75a3':'#4d8e6e'),art:front?ap.artwork:null,artWindow:front});}
      }
      return objects;
    };
    return true;
  }
  (function waitR(n=0){if(!patchRenderer()&&n<40)setTimeout(()=>waitR(n+1),250);})();
  function open(){reset();let d=document.getElementById('equipmentWizard');if(!d){d=h('dialog',{id:'equipmentWizard',class:'ew-dialog'});document.body.append(d);}render();d.showModal();}
  function mount(){
    const card=document.getElementById('equipmentPane');if(!card||document.getElementById('newEquipmentCard'))return;
    const b=h('button',{id:'newEquipmentCard',type:'button',class:'equipment-card ew-new'},'+ New equipment from dimensions');b.onclick=open;const lib=h('div',{id:'ewLibrary'});card.append(b,lib);loadLibrary();
    document.head.append(h('style',{},`.ew-dialog{width:min(760px,94vw);background:#1f2228;color:#e6e6e6;border:1px solid #444;border-radius:10px;padding:18px}
.ew-dialog::backdrop{background:#0008}.ew-steps{display:flex;gap:4px;flex-wrap:wrap;margin:8px 0}.ew-step,.ew-chip{background:#2b2f37;color:#ddd;border:1px solid #4a4f59;border-radius:14px;padding:4px 10px;cursor:pointer}
.ew-step.on,.ew-chip.on{background:#3d6b52;border-color:#6fbf8f}.ew-body{min-height:170px;display:flex;flex-direction:column;gap:6px}.ew-field{display:inline-flex;gap:6px;align-items:center;margin-right:10px}
.ew-field input{width:80px;background:#15171b;color:#eee;border:1px solid #555;border-radius:4px;padding:3px}.ew-field input[type=text]{width:220px}.ew-row{display:flex;flex-wrap:wrap;align-items:center;gap:6px}
.ew-choices{display:flex;flex-wrap:wrap;gap:6px}.ew-note{color:#9aa;font-size:12px;margin:2px 0}.ew-hint{text-align:center;margin-top:-2px}.ew-cap{margin:10px 0 -6px;text-transform:uppercase;letter-spacing:.06em;font-size:11px}.ew-model{width:100%;height:300px;background:#121418;border-radius:6px;cursor:grab;touch-action:none}.ew-preview{width:100%;height:110px;background:#121418;border-radius:6px;margin:10px 0}
.ew-view{width:100%;height:320px;background:#121418;border-radius:6px;cursor:grab;touch-action:none}
.ew-top{width:100%;max-height:200px;background:#121418;border-radius:6px}.ew-chip input{margin:0 4px 0 0}
.ew-ksbar{display:flex;flex-wrap:wrap;gap:6px;align-items:center}.ew-ksbar input{background:#15171b;color:#eee;border:1px solid #555;border-radius:4px}.ew-nav{display:flex;justify-content:flex-end;gap:8px;margin-top:12px}.ew-new{min-height:48px;margin-top:8px}.ew-warn{color:#e0b56f}`));
  }
  // The equipment pane is built by workspace.js, so retry until #equipmentPane exists.
  let tries=0;(function wait(){mount();if(!document.getElementById('newEquipmentCard')&&tries++<40)setTimeout(wait,250);})();
  window.openEquipmentWizard=open;
})();
