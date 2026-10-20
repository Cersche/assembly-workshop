// Offline orthographic inspection view. Depth testing is visual only, not a collision engine.
function rasterizeAssemblyFaces(faces,width,height,scale,output){
  const depth=new Float64Array(width*height);depth.fill(-Infinity);
  const pixels=output.data;
  for(let i=0;i<pixels.length;i+=4){pixels[i]=240;pixels[i+1]=244;pixels[i+2]=240;pixels[i+3]=255}
  for(const face of faces){
    const [a,b,c]=face.points.map(p=>[width/2+p[0]*scale,height/2-p[1]*scale,p[2]]);
    const area=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1]);
    if(Math.abs(area)<1e-10)continue;
    const x0=Math.max(0,Math.ceil(Math.min(a[0],b[0],c[0])-.5)),x1=Math.min(width-1,Math.floor(Math.max(a[0],b[0],c[0])-.5));
    const y0=Math.max(0,Math.ceil(Math.min(a[1],b[1],c[1])-.5)),y1=Math.min(height-1,Math.floor(Math.max(a[1],b[1],c[1])-.5));
    for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){
      const u=((b[1]-c[1])*(x+.5-c[0])+(c[0]-b[0])*(y+.5-c[1]))/area;
      const v=((c[1]-a[1])*(x+.5-c[0])+(a[0]-c[0])*(y+.5-c[1]))/area;
      const t=1-u-v;if(u< -1e-9||v< -1e-9||t< -1e-9)continue;
      const z=u*a[2]+v*b[2]+t*c[2],index=y*width+x;
      if(z<=depth[index])continue;
      depth[index]=z;const offset=index*4;
      pixels[offset]=face.color[0];pixels[offset+1]=face.color[1];pixels[offset+2]=face.color[2];
    }
  }
  return output;
}


async function initAssemblyViewer(){

  const canvas=document.getElementById('assemblyCanvas'),ctx=canvas.getContext('2d');

  const status=document.getElementById('assemblyStatus');

  if(!ctx){status.textContent='Canvas rendering is unavailable in this browser.';return}

  let model;try{const response=await fetch('/api/assembly');if(!response.ok)throw Error('Assembly load failed');model=await response.json()}catch(e){status.textContent=e.message;return}

  const baseline=model;

  let pi=null;

  try{const r=await fetch('/api/pi-reference');if(!r.ok)throw Error('Pi reference unavailable');pi=await r.json()}catch(e){document.getElementById('piStatus').textContent=e.message}

  try{const r=await fetch('/api/assembly-checks'),report=await r.json();document.getElementById('piStatus').textContent=report.checks.map(c=>c.status.toUpperCase()+' · '+c.name+': '+c.detail).concat((report.access_assessment||[]).map(a=>'UNKNOWN · '+a.name+': '+a.required+' '+a.limit)).join('\n')}catch(e){document.getElementById('piStatus').textContent=e.message}

  window.addEventListener('assembly-model',e=>{model=e.detail||baseline;schedule()});

  let yaw=.55,pitch=.65,zoom=1,focus=[0,39.5,21],pending=false,drag=null;

  const colors={tray:[77,142,110],faceplate:[78,117,163],screw:[179,86,57],screw_head:[179,86,57],insert:[195,152,52],pi_reference:[91,133,69]};

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

    const cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch);
    let scale=Math.min(w/290,h/150)*zoom,centerX=0,centerY=0;

    function camera(v){const x=v[0]-focus[0],y=v[1]-focus[1],z=v[2]-focus[2],u=cy*x-sy*y,d=sy*x+cy*y;return [u,cp*z-sp*d,sp*z+cp*d]}

    // Fit the full model with a margin; visibility toggles do not shift the camera.
    if(focus[0]!==40){
      let minX=Infinity,maxX=-Infinity,minY=Infinity,maxY=-Infinity;
      for(const part of model.parts)for(const v of part.vertices){const p=camera(v);minX=Math.min(minX,p[0]);maxX=Math.max(maxX,p[0]);minY=Math.min(minY,p[1]);maxY=Math.max(maxY,p[1])}
      if(Number.isFinite(minX)){centerX=(minX+maxX)/2;centerY=(minY+maxY)/2;scale=Math.min(w*.88/Math.max(maxX-minX,1),(h-50)*.88/Math.max(maxY-minY,1))*zoom}
    }
    function transform(v){const p=camera(v);return [p[0]-centerX,p[1]-centerY,p[2]]}

    const faces=[];

    const showHardware=document.getElementById('show-hardware').checked;

    const parts=model.parts.filter(p=>document.getElementById('show-'+p.id).checked);

    if(pi&&document.getElementById('show-pi_reference').checked)parts.push(pi);

    if(showHardware&&hardware)parts.push(...hardware.hardware_envelopes.map(cylinder));

    for(const part of parts){const vs=part.vertices.map(transform);

      for(const ids of part.triangles){const a=vs[ids[0]],b=vs[ids[1]],c=vs[ids[2]];

        const u=b.map((v,k)=>v-a[k]),v=c.map((v,k)=>v-a[k]);const n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];

        const norm=Math.hypot(...n)||1,shade=.52+.48*Math.abs((n[0]*.2+n[1]*.5+n[2]*.84)/norm);

        faces.push({points:[a,b,c],depth:(a[2]+b[2]+c[2])/3,color:colors[part.id].map(v=>Math.round(v*shade))})}}

    // Interpolate depth at each pixel so crossing triangles occlude correctly.
    const frame=ctx.createImageData(canvas.width,canvas.height);
    rasterizeAssemblyFaces(faces,canvas.width,canvas.height,scale*dpr,frame);
    ctx.putImageData(frame,0,0);

    if(showHardware&&hardware){ctx.strokeStyle='#b37e0f';ctx.setLineDash([5,4]);ctx.lineWidth=2;

      for(const g of hardware.hardware_guides){const a=transform([g.x,g.y0,g.z]),b=transform([g.x,g.y1,g.z]);ctx.beginPath();ctx.moveTo(w/2+a[0]*scale,h/2-a[1]*scale);ctx.lineTo(w/2+b[0]*scale,h/2-b[1]*scale);ctx.stroke()}

      ctx.setLineDash([]);

    }

    ctx.fillStyle='#324e40';ctx.font='12px system-ui';ctx.fillText('Model units: mm · '+model.revision,14,h-15);

    status.textContent=faces.length.toLocaleString()+' visible triangles · '+(focus[0]===40?'Right joint focus':'Full assembly')+'. '+model.revision+' · Pi is reference only; surface screening is not physical fit validation.';

    document.getElementById('hardwareStatus').textContent=showHardware&&hardware?`${hardware.hardware_envelopes.length} hardware envelopes; ${hardware.hardware_guides.length} dashed insert axes (outside diameter unknown). Axes are drawn through parts for visibility.`:'Hardware references hidden or no selection.';

  }

  canvas.onpointerdown=e=>{drag=[e.clientX,e.clientY];canvas.setPointerCapture(e.pointerId)};

  canvas.onpointermove=e=>{if(!drag)return;yaw+=(e.clientX-drag[0])*.008;pitch=Math.max(-1.5,Math.min(1.5,pitch+(e.clientY-drag[1])*.008));drag=[e.clientX,e.clientY];schedule()};

  canvas.onpointerup=canvas.onpointercancel=()=>{drag=null};

  canvas.onkeydown=e=>{if(e.key==='ArrowLeft')yaw-=.12;else if(e.key==='ArrowRight')yaw+=.12;else if(e.key==='ArrowUp')pitch=Math.min(1.5,pitch+.12);else if(e.key==='ArrowDown')pitch=Math.max(-1.5,pitch-.12);else return;e.preventDefault();schedule()};

  document.getElementById('assemblyZoom').oninput=e=>{zoom=Number(e.target.value);schedule()};

  document.getElementById('assemblyReset').onclick=()=>{yaw=.55;pitch=.65;focus=[0,39.5,21];zoom=1;document.getElementById('assemblyZoom').value=1;document.getElementById('show-tray').checked=true;document.getElementById('show-faceplate').checked=true;schedule()};

  document.getElementById('assemblyTop').onclick=()=>{yaw=0;pitch=Math.PI/2;schedule()};

  document.getElementById('assemblyJoint').onclick=()=>{focus=[40,8,21];yaw=.45;pitch=.45;zoom=2.5;document.getElementById('assemblyZoom').value=2.5;document.getElementById('show-tray').checked=true;document.getElementById('show-faceplate').checked=false;document.getElementById('show-hardware').checked=true;schedule()};

  for(const part of model.parts)document.getElementById('show-'+part.id).onchange=schedule;

  document.getElementById('show-hardware').onchange=schedule;

  document.getElementById('show-pi_reference').onchange=schedule;

  new ResizeObserver(schedule).observe(canvas);schedule();

}

initAssemblyViewer();

