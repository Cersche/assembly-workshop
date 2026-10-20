// Offline orthographic inspection view. Painter sorting is not a collision engine.
async function initAssemblyViewer(){
  const canvas=document.getElementById('assemblyCanvas'),ctx=canvas.getContext('2d');
  const status=document.getElementById('assemblyStatus');
  if(!ctx){status.textContent='Canvas rendering is unavailable in this browser.';return}
  let model;try{const response=await fetch('/api/assembly');if(!response.ok)throw Error('Assembly load failed');model=await response.json()}catch(e){status.textContent=e.message;return}
  let yaw=.55,pitch=.65,zoom=1,focus=[0,39.5,21],pending=false,drag=null;
  const colors={tray:[77,142,110],faceplate:[78,117,163]};
  function schedule(){if(!pending){pending=true;requestAnimationFrame(draw)}}
  function draw(){
    pending=false;const w=canvas.clientWidth||800,h=420,dpr=window.devicePixelRatio||1;
    if(canvas.width!==Math.round(w*dpr)||canvas.height!==Math.round(h*dpr)){canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr)}
    ctx.setTransform(dpr,0,0,dpr,0,0);ctx.fillStyle='#f0f4f0';ctx.fillRect(0,0,w,h);
    const cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch),scale=Math.min(w/290,h/150)*zoom;
    function transform(v){const x=v[0]-focus[0],y=v[1]-focus[1],z=v[2]-focus[2],u=cy*x-sy*y,d=sy*x+cy*y;return [u,cp*z-sp*d,sp*z+cp*d]}
    const faces=[];
    for(const part of model.parts){if(!document.getElementById('show-'+part.id).checked)continue;const vs=part.vertices.map(transform);
      for(const ids of part.triangles){const a=vs[ids[0]],b=vs[ids[1]],c=vs[ids[2]];
        const u=b.map((v,k)=>v-a[k]),v=c.map((v,k)=>v-a[k]);const n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];
        const norm=Math.hypot(...n)||1,shade=.52+.48*Math.abs((n[0]*.2+n[1]*.5+n[2]*.84)/norm);
        faces.push({points:[a,b,c],depth:(a[2]+b[2]+c[2])/3,color:colors[part.id].map(v=>Math.round(v*shade))})}}
    faces.sort((a,b)=>a.depth-b.depth);
    for(const f of faces){ctx.beginPath();f.points.forEach((p,i)=>{const x=w/2+p[0]*scale,y=h/2-p[1]*scale;i?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.closePath();ctx.fillStyle=`rgb(${f.color.join(',')})`;ctx.fill()}
    ctx.fillStyle='#324e40';ctx.font='12px system-ui';ctx.fillText('Model units: mm · '+model.revision,14,h-15);
    status.textContent=faces.length.toLocaleString()+' visible triangles · '+(focus[0]===40?'Right joint focus':'Full assembly')+'. Reference view; no geometry edits.';
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
  new ResizeObserver(schedule).observe(canvas);schedule();
}
initAssemblyViewer();
