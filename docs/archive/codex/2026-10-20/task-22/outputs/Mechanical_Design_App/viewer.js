// Local studio inspection with software fallback. Visual depth testing is not a collision engine.
function rasterizeAssemblyFaces(faces,width,height,scale,output,picking){
  const depth=new Float64Array(width*height);depth.fill(-Infinity);
  const pixels=output.data;
  for(let i=0;i<pixels.length;i+=4){pixels[i]=21;pixels[i+1]=28;pixels[i+2]=38;pixels[i+3]=255}
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
      depth[index]=z;if(picking)picking[index]=face.pickId||0;const offset=index*4;
      pixels[offset]=face.color[0];pixels[offset+1]=face.color[1];pixels[offset+2]=face.color[2];
      if(face.texture&&face.uv){
        const uv=[0,1].map(k=>u*face.uv[0][k]+v*face.uv[1][k]+t*face.uv[2][k]);
        if(uv.every(q=>q>=0&&q<1)){
          const image=face.texture,j=(Math.floor(uv[1]*image.height)*image.width+Math.floor(uv[0]*image.width))*4,alpha=image.data[j+3]/255;
          for(let k=0;k<3;k++)pixels[offset+k]=Math.round(pixels[offset+k]*(1-alpha)+image.data[j+k]*alpha*(face.shade||1));
        }
      }
    }
  }
  return output;
}

// Shade only visible pixels belonging to the selected part; preserve occlusion.
function highlightAssemblySelection(output,owners,selected,width,height,radius=2){
  if(!selected)return;
  const pixels=output.data;
  for(let y=0;y<height;y++)for(let x=0;x<width;x++){
    const i=y*width+x;if(owners[i]!==selected)continue;
    const edge=x<radius||y<radius||x+radius>=width||y+radius>=height||
      owners[i-radius]!==selected||owners[i+radius]!==selected||
      owners[i-radius*width]!==selected||owners[i+radius*width]!==selected;
    const target=edge?[89,217,255]:[64,179,255],mix=edge?.95:.2;
    for(let k=0;k<3;k++)pixels[i*4+k]=Math.round(pixels[i*4+k]*(1-mix)+target[k]*mix);
  }
}

async function initAssemblyViewer(){

  const canvas=document.getElementById('assemblyCanvas'),ctx=canvas.getContext('2d');

  const status=document.getElementById('assemblyStatus');

  if(!ctx){status.textContent='Canvas rendering is unavailable in this browser.';return}

  let model;try{const response=await fetch('/api/assembly');if(!response.ok)throw Error('Assembly load failed');model=await response.json()}catch(e){status.textContent=e.message;return}

  const baseline=model;

  window.addEventListener('assembly-model',e=>{model=e.detail||baseline;selectedPart=null;schedule()});

  let yaw=.55,pitch=.65,zoom=1,focus=[0,39.5,21],pending=false,drag=null;
  let frontMode=false,appearance={},texture=null,textureIdentity=null,imageRequest=0;
  let selectedPart=null,pickBuffer=null,pickParts=[],hardwareMeshes=null;
  let studioRenderer=null,studioUnavailable='';
  function createStudioRenderer(){
    try{if(window.LabRaxAssembly){studioRenderer=new window.LabRaxAssembly.AssemblyRenderer();studioRenderer.invalidated=schedule;studioUnavailable='';}}
    catch(e){studioUnavailable=e.message;studioRenderer=null;}
  }
  createStudioRenderer();
  if(studioRenderer)yaw=-.55;
  const partNames={tray:'Tray',faceplate:'Faceplate',screw:'Screw references',screw_head:'Screw-head references',insert:'Insert references'};

  const colors={tray:[77,142,110],faceplate:[78,117,163],screw:[179,86,57],screw_head:[179,86,57],insert:[195,152,52]};
  const baseColors=JSON.parse(JSON.stringify(colors));
  async function updateAppearance(value){
    appearance=value||{};
    for(const [key,id] of [['tray','tray'],['faceplate','faceplate']])colors[id]=/^#[a-f0-9]{6}$/i.test(appearance[key]||'')?[1,3,5].map(i=>parseInt(appearance[key].slice(i,i+2),16)):baseColors[id].slice();
    const identity=appearance.artwork?.sha256;
    if(identity===textureIdentity){schedule();return;}
    const request=++imageRequest;texture=null;textureIdentity=identity;schedule();
    if(!identity)return;
    try{const image=new Image();image.src='/api/artwork/'+identity+'.png';await image.decode();if(request!==imageRequest)return;const surface=document.createElement('canvas');surface.width=image.width;surface.height=image.height;const c=surface.getContext('2d');c.drawImage(image,0,0);texture=c.getImageData(0,0,image.width,image.height);schedule();}
    catch(e){if(request===imageRequest){textureIdentity=null;status.textContent='Faceplate preview image unavailable: '+e.message;}}
  }
  window.addEventListener('assembly-appearance',e=>updateAppearance(e.detail));
  window.addEventListener('assembly-faceplate-front',()=>{frontMode=true;focus=[0,0,21];zoom=1;document.getElementById('assemblyZoom').value=1;document.getElementById('show-faceplate').checked=true;schedule();});

  let hardware=window.assemblyHardware||null;
  if(window.assemblyAppearance)updateAppearance(window.assemblyAppearance);

  function cylinder(e){

    const vertices=[],triangles=[],n=window.RenderQuality?.segments('assembly')||24,r=e.diameter/2;

    for(const y of [e.y0,e.y1])for(let k=0;k<n;k++){const a=k*2*Math.PI/n;vertices.push([e.x+r*Math.cos(a),y,e.z+r*Math.sin(a)])}

    vertices.push([e.x,e.y0,e.z],[e.x,e.y1,e.z]);

    for(let k=0;k<n;k++){const j=(k+1)%n;triangles.push([k,j,n+k],[j,n+j,n+k],[2*n,j,k],[2*n+1,n+k,n+j])}

    return {id:e.kind,vertices,triangles};

  }

  window.addEventListener('assembly-hardware',e=>{hardware=e.detail;hardwareMeshes=null;schedule()});

  function schedule(){if(!pending){pending=true;requestAnimationFrame(draw)}}

  function draw(){

    pending=false;const w=canvas.clientWidth||800,h=420,dpr=window.RenderQuality?window.RenderQuality.pixelRatio('assembly',window.devicePixelRatio||1):window.devicePixelRatio||1;

    if(canvas.width!==Math.round(w*dpr)||canvas.height!==Math.round(h*dpr)){canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr)}

    ctx.setTransform(dpr,0,0,dpr,0,0);ctx.fillStyle='#151c26';ctx.fillRect(0,0,w,h);

    const cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch);
    let scale=Math.min(w/290,h/150)*zoom,centerX=0,centerY=0;

    function camera(v){const x=v[0]-focus[0],y=v[1]-focus[1],z=v[2]-focus[2];if(frontMode)return [x,z,-y];const u=cy*x-sy*y,d=sy*x+cy*y;return [u,cp*z-sp*d,sp*z+cp*d]}

    // Fit the full model with a margin; visibility toggles do not shift the camera.
    if(focus[0]!==40){
      let minX=Infinity,maxX=-Infinity,minY=Infinity,maxY=-Infinity;
      for(const part of model.parts)for(const v of part.vertices){const p=camera(v);minX=Math.min(minX,p[0]);maxX=Math.max(maxX,p[0]);minY=Math.min(minY,p[1]);maxY=Math.max(maxY,p[1])}
      if(Number.isFinite(minX)){centerX=(minX+maxX)/2;centerY=(minY+maxY)/2;scale=Math.min(w*.88/Math.max(maxX-minX,1),(h-50)*.88/Math.max(maxY-minY,1))*zoom}
    }
    let studioView=null;
    function transform(v){if(studioView){const p=studioView.project(v);return [p[0]-w/2,h/2-p[1],p[2]];}const p=camera(v);return [p[0]-centerX,p[1]-centerY,p[2]]}

    const faces=[];

    const showHardware=document.getElementById('show-hardware').checked;

    const parts=model.parts.filter(p=>document.getElementById('show-'+p.id).checked);


    if(showHardware&&hardware){if(!hardwareMeshes)hardwareMeshes=hardware.hardware_envelopes.map(cylinder);parts.push(...hardwareMeshes);}
    if(selectedPart&&!parts.some(p=>p.id===selectedPart))selectedPart=null;
    pickParts=[null,...new Set(parts.map(p=>p.id))];

    let usedStudio=false,renderedTriangles=0;
    if(studioRenderer){
      try{
        if(studioRenderer.restoreRequired){studioRenderer.dispose();createStudioRenderer();}
        const result=studioRenderer.render({parts,fullParts:model.parts,yaw,pitch,zoom,focus,frontMode,appearance,selectedPart,width:w,height:h,dpr});
        studioView=result.view;scale=1;ctx.drawImage(result.canvas,0,0,w,h);renderedTriangles=result.triangles;usedStudio=true;
      }catch(e){studioUnavailable=e.message;if(!studioRenderer?.lost){studioRenderer?.dispose();studioRenderer=null;}}
    }
    if(!usedStudio){
    for(const part of parts){const vs=part.vertices.map(transform);

      for(const ids of part.triangles){const a=vs[ids[0]],b=vs[ids[1]],c=vs[ids[2]];

        const u=b.map((v,k)=>v-a[k]),v=c.map((v,k)=>v-a[k]);const n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];

        const norm=Math.hypot(...n)||1,shade=.52+.48*Math.abs((n[0]*.2+n[1]*.5+n[2]*.84)/norm);

        const face={points:[a,b,c],pickId:pickParts.indexOf(part.id),depth:(a[2]+b[2]+c[2])/3,color:colors[part.id].map(v=>Math.round(v*shade))};
        // Project only onto actual planar front faces: holes and silhouettes stay empty.
        if(texture&&part.id==='faceplate'&&ids.every(i=>Math.abs(part.vertices[i][1]+3)<1e-5)){
          const art=appearance.artwork,availableWidth=216,availableHeight=34,s=Math.max(.05,art.scale),ratio=texture.width/texture.height;
          const imageWidth=Math.min(availableWidth,availableHeight*ratio)*s,imageHeight=imageWidth/ratio;
          const cx=(art.x-.5)*(availableWidth-imageWidth),cz=21+(.5-art.y)*(availableHeight-imageHeight);
          face.texture=texture;face.shade=shade;face.uv=ids.map(i=>[(part.vertices[i][0]-cx)/imageWidth+.5,.5-(part.vertices[i][2]-cz)/imageHeight]);
        }
        faces.push(face)}}

    // Interpolate depth at each pixel so crossing triangles occlude correctly.
    const frame=ctx.createImageData(canvas.width,canvas.height);
    pickBuffer=new Uint16Array(canvas.width*canvas.height);
    rasterizeAssemblyFaces(faces,canvas.width,canvas.height,scale*dpr,frame,pickBuffer);
    highlightAssemblySelection(frame,pickBuffer,pickParts.indexOf(selectedPart),canvas.width,canvas.height,Math.max(1,Math.round(1.5*dpr)));
    ctx.putImageData(frame,0,0);renderedTriangles=faces.length;
    }

    if(showHardware&&hardware){ctx.strokeStyle='#b37e0f';ctx.setLineDash([5,4]);ctx.lineWidth=2;

      for(const g of hardware.hardware_guides){const a=transform([g.x,g.y0,g.z]),b=transform([g.x,g.y1,g.z]);ctx.beginPath();ctx.moveTo(w/2+a[0]*scale,h/2-a[1]*scale);ctx.lineTo(w/2+b[0]*scale,h/2-b[1]*scale);ctx.stroke()}

      ctx.setLineDash([]);

    }

    ctx.fillStyle='#a8bbd3';ctx.font='12px system-ui';ctx.fillText('Model units: mm · '+model.revision,14,h-15);

    canvas.dataset.renderer=usedStudio?'webgl':'software';
    canvas.dataset.artwork=texture?'preview-only':'none';
    canvas.dataset.selectedPart=selectedPart||'none';
    status.textContent=renderedTriangles.toLocaleString()+' visible triangles · '+(frontMode?'Faceplate front':focus[0]===40?'Right joint focus':'Full assembly')+'. '+model.revision+(texture?' · artwork is preview only.':'')+' · Physical fit and strength remain UNKNOWN.';
    status.textContent+=usedStudio?' · Studio lighting / shadows / contact shading.':studioUnavailable?' · Software fallback: '+studioUnavailable+'.':'';
    status.textContent+=(selectedPart?' Selected: '+(partNames[selectedPart]||selectedPart)+'.':' Click a part to select it.');

    document.getElementById('hardwareStatus').textContent=showHardware&&hardware?`${hardware.hardware_envelopes.length} hardware envelopes; ${hardware.hardware_guides.length} dashed insert axes (outside diameter unknown). Axes are drawn through parts for visibility.`:'Hardware references hidden or no selection.';

  }

  canvas.onpointerdown=e=>{drag={x:e.clientX,y:e.clientY,startX:e.clientX,startY:e.clientY,moved:false};canvas.setPointerCapture(e.pointerId)};

  canvas.onpointermove=e=>{if(!drag)return;drag.moved=drag.moved||Math.hypot(e.clientX-drag.startX,e.clientY-drag.startY)>4;if(!drag.moved)return;frontMode=false;yaw+=(e.clientX-drag.x)*.008;pitch=Math.max(-1.5,Math.min(1.5,pitch+(e.clientY-drag.y)*.008));drag.x=e.clientX;drag.y=e.clientY;schedule()};

  canvas.onpointerup=e=>{if(drag&&!drag.moved){const rect=canvas.getBoundingClientRect();
    if(canvas.dataset.renderer==='webgl')selectedPart=studioRenderer.pickPart((e.clientX-rect.left)*wRatio(rect),(e.clientY-rect.top)*420/rect.height);
    else if(pickBuffer){const x=Math.floor((e.clientX-rect.left)*canvas.width/rect.width),y=Math.floor((e.clientY-rect.top)*canvas.height/rect.height);selectedPart=x>=0&&x<canvas.width&&y>=0&&y<canvas.height?pickParts[pickBuffer[y*canvas.width+x]]||null:null;}
    schedule();}drag=null};
  function wRatio(rect){return (canvas.clientWidth||800)/rect.width;}
  canvas.onpointercancel=()=>{drag=null};

  canvas.onkeydown=e=>{if(e.key==='Escape'){selectedPart=null;e.preventDefault();schedule();return;}if(e.key==='ArrowLeft')yaw-=.12;else if(e.key==='ArrowRight')yaw+=.12;else if(e.key==='ArrowUp')pitch=Math.min(1.5,pitch+.12);else if(e.key==='ArrowDown')pitch=Math.max(-1.5,pitch-.12);else return;frontMode=false;e.preventDefault();schedule()};

  document.getElementById('assemblyZoom').oninput=e=>{zoom=Number(e.target.value);schedule()};
  // Preview quality (render-quality.js): drawing resolution and hardware-envelope curve segments; Medium = as before.
  if(window.RenderQuality)document.getElementById('assemblyZoom').after(window.RenderQuality.previewSlider('assembly',()=>{hardwareMeshes=null;schedule();},'rq-assembly'));

  document.getElementById('assemblyReset').onclick=()=>{frontMode=false;yaw=studioRenderer?-.55:.55;pitch=.65;focus=[0,39.5,21];zoom=1;document.getElementById('assemblyZoom').value=1;document.getElementById('show-tray').checked=true;document.getElementById('show-faceplate').checked=true;schedule()};

  document.getElementById('assemblyTop').onclick=()=>{frontMode=false;yaw=0;pitch=Math.PI/2;schedule()};

  document.getElementById('assemblyJoint').onclick=()=>{frontMode=false;focus=[40,8,21];yaw=.45;pitch=.45;zoom=2.5;document.getElementById('assemblyZoom').value=2.5;document.getElementById('show-tray').checked=true;document.getElementById('show-faceplate').checked=false;document.getElementById('show-hardware').checked=true;schedule()};

  for(const part of model.parts)document.getElementById('show-'+part.id).onchange=schedule;

  document.getElementById('show-hardware').onchange=schedule;

  new ResizeObserver(schedule).observe(canvas);schedule();

}

initAssemblyViewer();

