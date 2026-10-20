// Offline orthographic inspection view. Painter sorting is not a collision engine.
async function initAssemblyViewer(){
  const canvas=document.getElementById('assemblyCanvas'),ctx=canvas.getContext('2d');
  const status=document.getElementById('assemblyStatus');
  if(!ctx){status.textContent='Canvas rendering is unavailable in this browser.';return}
  let model;try{const response=await fetch('/api/assembly');if(!response.ok)throw Error('Assembly load failed');model=await response.json()}catch(e){status.textContent=e.message;return}
  let yaw=.55,pitch=.65,zoom=1,focus=[0,39.5,21],pending=false,drag=null;
  const colors={tray:[77,142,110],faceplate:[78,117,163],screw:[179,86,57],screw_head:[179,86,57],insert:[195,152,52]};
  let hardware=window.assemblyHardware||null;
  function cylinder(e){
    const vertices=[],triangles=[],n=24,r=e.diameter/2;
    for(const y of [e.y0,e.y1])for(let k=0;k<n;k++){const a=k*2*Math.PI/n;vertices.push([e.x+r*Math.cos(a),y,e.z+r*Math.sin(a)])}
    vertices.push([e.x,e.y0,e.z],[e.x,e.y1,e.z]);
    for(let k=0;k<n;k++){const j=(k+1)%n;triangles.push([k,j,n+k],[j,n+j,n+k],[2*n,j,k],[2*n+1,n+k,n+j])}
    return {id:e.kind,vertices,triangles};
  }
  window.addEventListener('assembly-hardware',e=>{hardware=e.detail;schedule()});
  function schedule(){if(!pending){pending=true;requestAnimationFrame(draw)}}
  function draw(){
    pending=false;const w=canvas.clientWidth||800,h=420,dpr=window.devicePixelRatio||1;
    if(canvas.width!==Math.round(w*dpr)||canvas.height!==Math.round(h*dpr)){canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr)}
    ctx.setTransform(dpr,0,0,dpr,0,0);ctx.fillStyle='#f0f4f0';ctx.fillRect(0,0,w,h);
    const cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch),scale=Math.min(w/290,h/150)*zoom;
    function transform(v){const x=v[0]-focus[0],y=v[1]-focus[1],z=v[2]-focus[2],u=cy*x-sy*y,d=sy*x+cy*y;return [u,cp*z-sp*d,sp*z+cp*d]}
    const faces=[];
    const showHardware=document.getElementById('show-hardware').checked;
    const parts=model.parts.filter(p=>document.getElementById('show-'+p.id).checked);
    if(showHardware&&hardware)parts.push(...hardware.hardware_envelopes.map(cylinder));
    for(const part of parts){const vs=part.vertices.map(transform);
      for(const ids of part.triangles){const a=vs[ids[0]],b=vs[ids[1]],c=vs[ids[2]];
        const u=b.map((v,k)=>v-a[k]),v=c.map((v,k)=>v-a[k]);const n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];
        const norm=Math.hypot(...n)||1,shade=.52+.48*Math.abs((n[0]*.2+n[1]*.5+n[2]*.84)/norm);
        faces.push({points:[a,b,c],depth:(a[2]+b[2]+c[2])/3,color:colors[part.id].map(v=>Math.round(v*shade))})}}
    faces.sort((a,b)=>a.depth-b.depth);
    for(const f of faces){ctx.beginPath();f.points.forEach((p,i)=>{const x=w/2+p[0]*scale,y=h/2-p[1]*scale;i?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.closePath();ctx.fillStyle=`rgb(${f.color.join(',')})`;ctx.fill()}
    if(showHardware&&hardware){ctx.strokeStyle='#b37e0f';ctx.setLineDash([5,4]);ctx.lineWidth=2;
      for(const g of hardware.hardware_guides){const a=transform([g.x,g.y0,g.z]),b=transform([g.x,g.y1,g.z]);ctx.beginPath();ctx.moveTo(w/2+a[0]*scale,h/2-a[1]*scale);ctx.lineTo(w/2+b[0]*scale,h/2-b[1]*scale);ctx.stroke()}
      ctx.setLineDash([]);
    }
    ctx.fillStyle='#324e40';ctx.font='12px system-ui';ctx.fillText('Model units: mm · '+model.revision,14,h-15);
    status.textContent=faces.length.toLocaleString()+' visible triangles · '+(focus[0]===40?'Right joint focus':'Full assembly')+'. Reference view; no geometry edits.';
    document.getElementById('hardwareStatus').textContent=showHardware&&hardware?`${hardware.hardware_envelopes.length} hardware envelopes; ${hardware.hardware_guides.length} dashed insert axes (outside diameter unknown). Axes are drawn through parts for visibility.`:'Hardware references hidden or no selection.';
  }
  canvas.onpointerdown=e=>{drag=[e.clientX,e.clientY];canvas.setPointerCapture(e.pointerId)};
  canvas.onpointermove=e=>{if(!drag)return;yaw+=(e.clientX-drag[0])*.008;pitch=Math.max(-1.5,Math.min(1.5,pitch+(e.clientY-drag[1])*.008));drag=[e.clientX,e.clientY];schedule()};
  canvas.onpointerup=canvas.onpointercancel=()=>{drag=null};
  canvas.onkeydown=e=>{if(e.key==='ArrowLeft')yaw-=.12;else if(e.key==='ArrowRight')yaw+=.12;else if(e.key==='ArrowUp')pitch=Math.min(1.5,pitch+.12);else if(e.key==='ArrowDown')pitch=Math.max(-1.5,pitch-.12);else return;e.preventDefault();schedule()};
  document.getElementById('assemblyZoom').oninput=e=>{zoom=Number(e.target.value);schedule()};
  document.getElementById('assemblyReset').onclick=()=>{yaw=.55;pitch=.65;focus=[0,39.5,21];zoom=1;document.getElementById('assemblyZoom').value=1;schedule()};
  document.getElementById('assemblyTop').onclick=()=>{yaw=0;pitch=Math.PI/2;schedule()};
  document.getElementById('assemblyJoint').onclick=()=>{focus=[40,8,21];zoom=4;document.getElementById('assemblyZoom').value=4;schedule()};
  for(const part of model.parts)document.getElementById('show-'+part.id).onchange=schedule;
  document.getElementById('show-hardware').onchange=schedule;
  new ResizeObserver(schedule).observe(canvas);schedule();
}
initAssemblyViewer();
