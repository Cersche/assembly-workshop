// Local preview renderer. Does not generate manufacturing geometry or modify saved data.
(function(root){
  'use strict';
  const I=[1,0,0,0,1,0,0,0,1], TAU=Math.PI*2;
  const add=(a,b)=>a.map((v,i)=>v+b[i]), sub=(a,b)=>a.map((v,i)=>v-b[i]);
  const dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0);
  const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
  const unit=a=>a.map(v=>v/(Math.hypot(...a)||1));
  function rgb(hex,fallback='#657582'){return /^#[0-9a-f]{6}$/i.test(hex||'')?[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255):rgb(fallback);}
  function artworkRect(art={},aspect=1){
    // Match the existing assembly viewer's saved normalized placement semantics.
    art=art||{};
    const width=Math.min(216,34*aspect)*Math.max(.05,art.scale??.65),height=width/aspect;
    return [((art.x??.5)-.5)*(216-width),21+(.5-(art.y??.5))*(34-height),width,height];
  }
  class Mesh{
    constructor(){this.vertices=[];this.triangles=[];this.normals=[];}
    tri(a,b,c,normals){const k=this.vertices.length,n=unit(cross(sub(b,a),sub(c,a)));this.vertices.push(a,b,c);this.normals.push(...(normals||[n,n,n]));this.triangles.push([k,k+1,k+2]);}
    quad(a,b,c,d){this.tri(a,b,c);this.tri(a,c,d);}
    box(x0,x1,y0,y1,z0,z1){
      const p=[[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]];
      for(const f of [[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]])this.quad(...f.map(i=>p[i]));
    }
  }
  function rounded(x0,x1,z0,z1,r,steps=12){const p=[];for(const [x,z,start] of [[x1-r,z1-r,0],[x0+r,z1-r,90],[x0+r,z0+r,180],[x1-r,z0+r,270]])for(let i=0;i<=steps;i++){const t=(start+i*90/steps)*Math.PI/180;p.push([x+r*Math.cos(t),z+r*Math.sin(t)]);}return p;}
  function circle(x,z,r,steps=40){return Array.from({length:steps},(_,i)=>[x+r*Math.cos(i*TAU/steps),z+r*Math.sin(i*TAU/steps)]);}
  // Exact polygonal scan bands: triangulate material intervals, never paint over holes.
  function slab(mesh,outer,holes,low,high,map){
    const loops=[outer,...holes],cuts=[...new Set(loops.flatMap(p=>p.map(v=>v[1].toFixed(8))))].map(Number).sort((a,b)=>a-b);
    function edgesAt(loop,z){const edges=[];for(let i=0;i<loop.length;i++){const a=loop[i],b=loop[(i+1)%loop.length];if((a[1]<z&&b[1]>z)||(b[1]<z&&a[1]>z))edges.push({x:a[0]+(z-a[1])*(b[0]-a[0])/(b[1]-a[1]),at:q=>a[0]+(q-a[1])*(b[0]-a[0])/(b[1]-a[1])});}return edges.sort((a,b)=>a.x-b.x);}
    for(let i=0;i<cuts.length-1;i++){const a=cuts[i],b=cuts[i+1];if(b-a<1e-7)continue;const mid=(a+b)/2,edges=loops.flatMap(p=>edgesAt(p,mid)).sort((p,q)=>p.x-q.x);
      for(let j=0;j+1<edges.length;j+=2){const l=edges[j],r=edges[j+1],p=[[l.at(a),a],[r.at(a),a],[r.at(b),b],[l.at(b),b]];mesh.quad(...p.map(v=>map(v[0],v[1],low)));mesh.quad(...p.reverse().map(v=>map(v[0],v[1],high)));}
    }
    for(let k=0;k<loops.length;k++){const loop=loops[k];for(let i=0;i<loop.length;i++){const a=loop[i],b=loop[(i+1)%loop.length],v=[map(a[0],a[1],low),map(b[0],b[1],low),map(b[0],b[1],high),map(a[0],a[1],high)];mesh.quad(...(k?v.reverse():v));}}
  }
  // Surface of revolution around Y, with analytic profile normals.
  function lathe(mesh,profile,cx,cz,segments=64,smooth=false){
    for(let j=0;j<profile.length-1;j++){const [r0,y0]=profile[j],[r1,y1]=profile[j+1],dr=r1-r0,dy=y1-y0;
      const normal=(index,t)=>{const a=profile[Math.max(0,index-1)],b=profile[Math.min(profile.length-1,index+1)],dyN=smooth?b[1]-a[1]:dy,drN=smooth?b[0]-a[0]:dr;return unit([dyN*Math.cos(t),-drN,dyN*Math.sin(t)]);};
      for(let i=0;i<segments;i++){const a=i*TAU/segments,b=(i+1)*TAU/segments,p=(r,y,t)=>[cx+r*Math.cos(t),y,cz+r*Math.sin(t)],v=[p(r0,y0,a),p(r0,y0,b),p(r1,y1,b),p(r1,y1,a)];mesh.tri(v[0],v[2],v[1],[normal(j,a),normal(j+1,b),normal(j,b)]);mesh.tri(v[0],v[3],v[2],[normal(j,a),normal(j+1,a),normal(j+1,b)]);}
    }
  }
  function equipment(){
    const tray=new Mesh(),plate=new Mesh(),brass=new Mesh(),bolts=new Mesh(),sockets=new Mesh();
    const standoffs=[[-24.5,30],[33.5,30],[-24.5,88],[33.5,88]],vents=[];
    // Reserve solid floor below each boss rather than cutting a vent into its foot.
    for(let x=-55;x<=55;x+=22)for(let y=25;y<=120;y+=22)if(standoffs.every(([sx,sy])=>Math.hypot(x-sx,y-sy)>7.8))vents.push(circle(x,y,3.8,24));
    slab(tray,[[-88,0],[88,0],[88,140],[-88,140]],vents,2,5,(x,y,z)=>[x,y,z]);
    tray.box(-88,-85,0,140,5,37);tray.box(85,88,0,140,5,37);tray.box(-85,85,137.5,140,5,37);
    for(const [x,y] of standoffs){
      const boss=new Mesh();lathe(boss,[[1.2,0],[3.2,0],[3.2,3],[1.2,3],[1.2,0]],0,0,40);
      // Map local Y axis onto the PCB boss Z axis; preserve smooth normals.
      for(const t of boss.triangles){const ids=[t[0],t[2],t[1]];tray.tri(...ids.map(i=>[x+boss.vertices[i][0],y+boss.vertices[i][2],5+boss.vertices[i][1]]),ids.map(i=>[boss.normals[i][0],boss.normals[i][2],boss.normals[i][1]]));}
    }
    const holes=[];for(const x of [-118.2625,118.2625])for(const z of [5.098,36.902]){
      holes.push(rounded(x-5,x+5,z-3.5,z+3.5,3.5,16));
      lathe(brass,[[1.35,.2],[4,.2],[4,7],[1.35,7],[1.35,.2]],x,z);
      // Subtle knurl facets are visual detail only, not a certified insert model.
      for(let i=0;i<40;i++){const t=i*TAU/40,dx=Math.cos(t),dz=Math.sin(t);brass.box(x+dx*3.87-.12,x+dx*3.87+.12,.6,6.6,z+dz*3.87-.12,z+dz*3.87+.12);}
      lathe(bolts,[[0,8],[3,8],[3,-3],[5.25,-3.5]],x,z);
      const dome=Array.from({length:17},(_,i)=>{const t=i/16*Math.acos(2.65/5.25);return [5.25*Math.cos(t),-3.5-3.242*Math.sin(t)];});
      lathe(bolts,dome,x,z,80,true);
      // Real hex recess: annular crown joins a six-sided socket with a recessed floor.
      const hex=Array.from({length:6},(_,i)=>[x+2.3094*Math.cos(i*TAU/6),z+2.3094*Math.sin(i*TAU/6)]);
      slab(bolts,circle(x,z,2.65,48),[hex],-6.3,-6.05,(a,b,c)=>[a,c,b]);
      for(let i=0;i<6;i++){const a=hex[i],b=hex[(i+1)%6];sockets.quad([a[0],-6.3,a[1]],[b[0],-6.3,b[1]],[b[0],-4.8,b[1]],[a[0],-4.8,a[1]]);sockets.tri([x,-4.8,z],[a[0],-4.8,a[1]],[b[0],-4.8,b[1]]);}
    }
    slab(plate,rounded(-125.5,125.5,.475,43.975,4,16),holes,-3,0,(x,z,y)=>[x,y,z]);
    return {tray,plate,brass,bolts,sockets};
  }
  function camera(box,yaw,pitch,width,height,zoom=1,perspective=true){
    if(!perspective){
      const view=root.LabRaxScene.camera(box,yaw,pitch,width,height,zoom);
      const back=[-Math.cos(pitch)*Math.sin(yaw),-Math.cos(pitch)*Math.cos(yaw),Math.sin(pitch)];
      const right=[Math.cos(yaw),-Math.sin(yaw),0],up=[Math.sin(pitch)*Math.sin(yaw),Math.sin(pitch)*Math.cos(yaw),Math.cos(pitch)];
      const center=box.lo.map((v,i)=>(v+box.hi[i])/2),screen=view.project(center),range=1/Math.hypot(view.matrix[2],view.matrix[6],view.matrix[10]);
      return {...view,ray:(x,y)=>({origin:add(add(add(center,right.map(v=>v*(x-screen[0])/view.scale)),up.map(v=>v*(screen[1]-y)/view.scale)),back.map(v=>v*100000)),direction:back.map(v=>-v)}),eye:add(center,back.map(v=>v*100000)),depthParams:[0,0,range,0],perspective:false};
    }
    const center=box.lo.map((v,i)=>(v+box.hi[i])/2),cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch);
    const right=[cy,-sy,0],up=[sp*sy,sp*cy,cp],back=[-cp*sy,-cp*cy,sp],aspect=width/height,f=1/Math.tan(32*Math.PI/360);
    const corners=[];for(const x of [box.lo[0],box.hi[0]])for(const y of [box.lo[1],box.hi[1]])for(const z of [box.lo[2],box.hi[2]])corners.push(sub([x,y,z],center));
    const radius=Math.max(...corners.map(v=>Math.hypot(...v))),distance=Math.max(...corners.map(v=>dot(v,back)+Math.max(Math.abs(dot(v,right))*f/aspect/.82,Math.abs(dot(v,up))*f/.83)))/zoom;
    const near=Math.max(.5,distance-radius*1.15),far=distance+radius*1.7+100,eye=add(center,back.map(v=>v*distance)),m=new Float32Array(16),A=(far+near)/(far-near),B=-2*far*near/(far-near);
    for(let i=0;i<3;i++){m[i*4]=right[i]*f/aspect;m[i*4+1]=up[i]*f;m[i*4+2]=-A*back[i];m[i*4+3]=-back[i];}
    m[12]=-dot(eye,right)*f/aspect;m[13]=-dot(eye,up)*f;m[14]=A*dot(eye,back)+B;m[15]=dot(eye,back);
    return {matrix:m,eye,depthParams:[A,B,0,1],perspective:true,ray:(x,y)=>({origin:eye,direction:unit(add(add(right.map(v=>v*(2*x/width-1)*aspect/f),up.map(v=>v*(1-2*y/height)/f)),back.map(v=>-v)))}),project:p=>{const v=sub(p,eye),d=-dot(v,back);return [width/2+dot(v,right)*f/aspect/d*width/2,height/2-dot(v,up)*f/d*height/2,d];}};
  }
  const VS=`attribute vec3 aPosition; attribute vec3 aNormal;
    uniform mat4 uModel,uCamera,uLight; varying vec3 vWorld,vNormal; varying vec4 vShadow;
    void main(){vec4 p=uModel*vec4(aPosition,1.);vWorld=p.xyz;vNormal=mat3(uModel)*aNormal;vShadow=uLight*p;gl_Position=uCamera*p;}`;
  const FS=`precision highp float;
    varying vec3 vWorld,vNormal; varying vec4 vShadow;
    uniform vec3 uColor,uEye; uniform float uMetal,uRough,uFloor,uShadowEnabled,uSelected;
    uniform sampler2D uShadow,uArtwork,uSceneDepth; uniform vec4 uArtRect,uDepthParams; uniform float uArtEnabled,uBaseZ,uAOEnabled,uShadowTexel;
    uniform mat4 uCamera;
    float unpackDepth(vec4 q){return dot(q,vec4(1.,1./255.,1./65025.,1./16581375.));}
    float linearDepth(float d){return uDepthParams.w>.5?uDepthParams.y/(d*2.-1.-uDepthParams.x):d*2.*uDepthParams.z;}
    float ambientOcclusion(vec3 n){if(uAOEnabled<.5)return 1.;vec3 tangent=normalize(cross(n,abs(n.z)<.8?vec3(0.,0.,1.):vec3(0.,1.,0.))),bitangent=cross(n,tangent);float occluded=0.;
      for(int i=0;i<12;i++){float k=float(i),angle=k*2.39996,radius=2.+k*.55;vec3 offset=tangent*cos(angle)*.8+bitangent*sin(angle)*.8+n*.6;vec4 clip=uCamera*vec4(vWorld+n*.15+offset*radius,1.);vec3 p=clip.xyz/clip.w*.5+.5;if(p.x>0.&&p.x<1.&&p.y>0.&&p.y<1.&&p.z>0.&&p.z<1.){float sampled=linearDepth(unpackDepth(texture2D(uSceneDepth,p.xy))),expected=linearDepth(p.z),difference=expected-sampled;occluded+=step(.35,difference)*(1.-smoothstep(4.,14.,abs(difference)));}}
      return 1.-occluded/12.*.65;}
    vec3 fresnel(float h,vec3 f){return f+(1.-f)*pow(1.-h,5.);}
    float shadow(vec3 n){if(uShadowEnabled<.5)return 1.;vec3 p=vShadow.xyz/vShadow.w*.5+.5;if(p.x<0.||p.x>1.||p.y<0.||p.y>1.||p.z>1.)return 1.;float s=0.;float bias=max(.0005,.0012*(1.-max(dot(n,normalize(vec3(-.5,-.7,1.))),0.)));for(int x=-1;x<=1;x++)for(int y=-1;y<=1;y++){float d=unpackDepth(texture2D(uShadow,p.xy+vec2(float(x),float(y))*uShadowTexel));s+=p.z-bias>d?.34:1.;}return s/9.;}
    vec3 lamp(vec3 n,vec3 v,vec3 l,vec3 radiance,vec3 base,float rough,float metal){vec3 h=normalize(l+v);float nl=max(dot(n,l),0.),nv=max(dot(n,v),.001),nh=max(dot(n,h),0.),vh=max(dot(v,h),0.);float a=rough*rough,a2=a*a,d=a2/(3.14159*pow(nh*nh*(a2-1.)+1.,2.)+.00001),k=pow(rough+1.,2.)/8.;float g=nl/(nl*(1.-k)+k)*nv/(nv*(1.-k)+k);vec3 F=fresnel(vh,mix(vec3(.04),base,metal));return ((1.-F)*(1.-metal)*base/3.14159+F*d*g/max(4.*nl*nv,.001))*radiance*nl;}
    void main(){vec3 n=normalize(vNormal);if(!gl_FrontFacing)n=-n;vec3 v=normalize(uEye-vWorld),base=pow(uColor,vec3(2.2));
      if(uArtEnabled>.5&&vWorld.y< -2.99&&abs(n.y)>.95){vec2 uv=(vec2(vWorld.x,vWorld.z-uBaseZ)-uArtRect.xy)/uArtRect.zw+.5;if(all(greaterThanEqual(uv,vec2(0.)))&&all(lessThanEqual(uv,vec2(1.)))){vec4 art=texture2D(uArtwork,vec2(uv.x,1.-uv.y));base=mix(base,pow(art.rgb,vec3(2.2)),art.a);}}
      float sh=shadow(n);vec3 c=lamp(n,v,normalize(vec3(-.5,-.7,1.)),vec3(3.6,3.35,3.05)*sh,base,uRough,uMetal);
      c+=lamp(n,v,normalize(vec3(.8,.35,.65)),vec3(1.3,1.65,2.1),base,uRough,uMetal);
      c+=lamp(n,v,normalize(vec3(-.7,.8,.3)),vec3(.65,.8,1.),base,uRough,uMetal);
      float ao=ambientOcclusion(n);vec3 hemi=mix(vec3(.09,.105,.14),vec3(.34,.40,.48),n.z*.5+.5);c+=base*hemi*(1.-uMetal*.65)*ao;c*=mix(.82,1.,ao);
      vec3 r=reflect(-v,n);float softbox=pow(max(0.,dot(r,normalize(vec3(-.3,-.65,.7)))),mix(90.,5.,uRough));c+=fresnel(max(dot(n,v),0.),mix(vec3(.04),base,uMetal))*(.17+softbox*1.2)*(1.-uRough*.6);
      c=pow(vec3(1.)-exp(-c*1.25),vec3(1./2.2));
      // Selection is shaded on the actual plate, so rack posts still occlude it.
      if(uSelected>.5){
        vec2 q=abs(vec2(vWorld.x,vWorld.z-uBaseZ-22.225))-vec2(121.5,17.75);
        float edge=length(max(q,vec2(0.)))+min(max(q.x,q.y),0.)-4.;
        float rim=1.-smoothstep(.8,2.4,abs(edge));
        c=mix(c,vec3(.25,.7,1.),.2);c=mix(c,vec3(.35,.85,1.),rim*.95);
      }
      if(uFloor>.5){float fade=1.-smoothstep(220.,600.,length(vWorld.xy-vec2(0.,120.)));c=mix(vec3(.035,.05,.075),c,fade);}
      gl_FragColor=vec4(c,1.);}`;
  const DEPTH=`precision highp float;void main(){vec4 c=fract(gl_FragCoord.z*vec4(1.,255.,65025.,16581375.));c-=c.yzww*vec4(1./255.,1./255.,1./255.,0.);gl_FragColor=c;}`;
  class Renderer{
    constructor(){
      this.canvas=document.createElement('canvas');const gl=this.gl=this.canvas.getContext('webgl',{alpha:true,antialias:true,preserveDrawingBuffer:true,premultipliedAlpha:false});if(!gl)throw Error('WebGL unavailable. Enable graphics acceleration for the rack preview.');
      this.buffers=new Map();this.textures=new Map();this.geometry=equipment();this.shadowKey='';this.invalidated=()=>{};this.ambientOcclusion=true;
      this.program=this.programFor(VS,FS);this.depthProgram=this.programFor(VS,DEPTH);this.locations=new Map();
      this.shadowSize=Math.min(2048,gl.getParameter(gl.MAX_TEXTURE_SIZE));
      this.shadowTexture=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,this.shadowTexture);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,this.shadowSize,this.shadowSize,0,gl.RGBA,gl.UNSIGNED_BYTE,null);this.textureSettings();gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.NEAREST);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.NEAREST);
      this.shadowFbo=gl.createFramebuffer();gl.bindFramebuffer(gl.FRAMEBUFFER,this.shadowFbo);gl.framebufferTexture2D(gl.FRAMEBUFFER,gl.COLOR_ATTACHMENT0,gl.TEXTURE_2D,this.shadowTexture,0);
      this.shadowDepth=gl.createRenderbuffer();gl.bindRenderbuffer(gl.RENDERBUFFER,this.shadowDepth);gl.renderbufferStorage(gl.RENDERBUFFER,gl.DEPTH_COMPONENT16,this.shadowSize,this.shadowSize);gl.framebufferRenderbuffer(gl.FRAMEBUFFER,gl.DEPTH_ATTACHMENT,gl.RENDERBUFFER,this.shadowDepth);
      this.shadowSupported=this.shadows=gl.checkFramebufferStatus(gl.FRAMEBUFFER)===gl.FRAMEBUFFER_COMPLETE;gl.bindFramebuffer(gl.FRAMEBUFFER,null);
      this.blank=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,this.blank);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,1,1,0,gl.RGBA,gl.UNSIGNED_BYTE,new Uint8Array([255,255,255,0]));this.textureSettings();
      const floor=new Mesh();floor.box(-900,900,-700,900,-43,-42);this.geometry.floor=floor;
      this.canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();this.lost=true;this.invalidated();});
      this.canvas.addEventListener('webglcontextrestored',()=>{this.restoreRequired=true;this.invalidated();});
    }
    textureSettings(){const g=this.gl;g.texParameteri(g.TEXTURE_2D,g.TEXTURE_MIN_FILTER,g.LINEAR);g.texParameteri(g.TEXTURE_2D,g.TEXTURE_MAG_FILTER,g.LINEAR);g.texParameteri(g.TEXTURE_2D,g.TEXTURE_WRAP_S,g.CLAMP_TO_EDGE);g.texParameteri(g.TEXTURE_2D,g.TEXTURE_WRAP_T,g.CLAMP_TO_EDGE);}
    programFor(v,f){const g=this.gl,p=g.createProgram();for(const [type,src] of [[g.VERTEX_SHADER,v],[g.FRAGMENT_SHADER,f]]){const s=g.createShader(type);g.shaderSource(s,src);g.compileShader(s);if(!g.getShaderParameter(s,g.COMPILE_STATUS))throw Error(g.getShaderInfoLog(s));g.attachShader(p,s);g.deleteShader(s);}g.linkProgram(p);if(!g.getProgramParameter(p,g.LINK_STATUS))throw Error(g.getProgramInfoLog(p));return p;}
    loc(p,name){let map=this.locations.get(p);if(!map){map={};this.locations.set(p,map);}if(!(name in map))map[name]=name.startsWith('a')?this.gl.getAttribLocation(p,name):this.gl.getUniformLocation(p,name);return map[name];}
    upload(key,mesh){if(this.buffers.has(key))return this.buffers.get(key);const g=this.gl,d=new Float32Array(mesh.triangles.length*18);let k=0;for(const t of mesh.triangles){const [a,b,c]=t.map(i=>mesh.vertices[i]),n=unit(cross(sub(b,a),sub(c,a)));for(const i of t){d.set(mesh.vertices[i],k);d.set(mesh.normals?mesh.normals[i]:n,k+3);k+=6;}}const buffer=g.createBuffer();g.bindBuffer(g.ARRAY_BUFFER,buffer);g.bufferData(g.ARRAY_BUFFER,d,g.STATIC_DRAW);const item={buffer,count:d.length/6};this.buffers.set(key,item);return item;}
    artwork(art){if(!art?.sha256)return null;if(this.textures.has(art.sha256))return this.textures.get(art.sha256);const item={ready:false,texture:null};this.textures.set(art.sha256,item);const image=new Image();image.onload=()=>{if(this.disposed)return;const g=this.gl;item.texture=g.createTexture();g.bindTexture(g.TEXTURE_2D,item.texture);g.texImage2D(g.TEXTURE_2D,0,g.RGBA,g.RGBA,g.UNSIGNED_BYTE,image);this.textureSettings();item.aspect=image.width/image.height;item.ready=true;this.invalidated();};image.onerror=()=>{item.error=true;};image.src='/api/artwork/'+art.sha256+'.png';return item;}
    sceneDepthTarget(width,height){
      const g=this.gl,w=Math.min(width,1200),h=Math.max(1,Math.round(height*w/width));
      if(this.depthTarget?.width===w&&this.depthTarget?.height===h)return this.depthTarget;
      if(this.depthTarget){g.deleteFramebuffer(this.depthTarget.fbo);g.deleteTexture(this.depthTarget.texture);g.deleteRenderbuffer(this.depthTarget.depth);}
      const texture=g.createTexture();g.bindTexture(g.TEXTURE_2D,texture);g.texImage2D(g.TEXTURE_2D,0,g.RGBA,w,h,0,g.RGBA,g.UNSIGNED_BYTE,null);this.textureSettings();g.texParameteri(g.TEXTURE_2D,g.TEXTURE_MIN_FILTER,g.NEAREST);g.texParameteri(g.TEXTURE_2D,g.TEXTURE_MAG_FILTER,g.NEAREST);
      const fbo=g.createFramebuffer(),depth=g.createRenderbuffer();g.bindFramebuffer(g.FRAMEBUFFER,fbo);g.framebufferTexture2D(g.FRAMEBUFFER,g.COLOR_ATTACHMENT0,g.TEXTURE_2D,texture,0);g.bindRenderbuffer(g.RENDERBUFFER,depth);g.renderbufferStorage(g.RENDERBUFFER,g.DEPTH_COMPONENT16,w,h);g.framebufferRenderbuffer(g.FRAMEBUFFER,g.DEPTH_ATTACHMENT,g.RENDERBUFFER,depth);const ready=g.checkFramebufferStatus(g.FRAMEBUFFER)===g.FRAMEBUFFER_COMPLETE;g.bindFramebuffer(g.FRAMEBUFFER,null);
      this.depthTarget={texture,fbo,depth,width:w,height:h,ready};this.depthKey='';return this.depthTarget;
    }
    objects(scene,meshes,rack,selectedSlot=null){
      const appearance=rack?.appearance||{},objects=scene.parts.map(p=>({...p,mesh:meshes[p.key],color:rgb(appearance.components?.[p.key]||appearance.color,p.kind==='foot'?'#28313d':p.kind==='panel'?'#627a78':'#8b9aa8'),metal:.05,rough:.52}));
      for(const allocation of rack?.placements||[]){const a=allocation.assembly?.appearance||{},z=(rack.slots-allocation.slot)*44.45;for(const [key,color,metal,rough] of [['tray',a.tray||'#4d8e6e',0,.48],['plate',a.faceplate||'#4e75a3',0,.38],['brass','#c89a46',.82,.28],['bolts','#303640',.72,.3],['sockets','#11151c',.2,.65]])objects.push({key:'studio-'+key,mesh:this.geometry[key],R:I,t:[0,0,z],kind:key,slot:allocation.slot,selected:key==='plate'&&selectedSlot>=allocation.slot&&selectedSlot<allocation.slot+allocation.span,color:rgb(color),metal,rough,art:key==='plate'?a.artwork:null});}
      return objects;
    }
    submit(p,objects){
      const g=this.gl;
      for(const o of objects){
        const item=this.upload(o.key,o.mesh),R=o.R,t=o.t;
        g.bindBuffer(g.ARRAY_BUFFER,item.buffer);
        const pos=this.loc(p,'aPosition'),norm=this.loc(p,'aNormal');
        g.enableVertexAttribArray(pos);g.vertexAttribPointer(pos,3,g.FLOAT,false,24,0);
        if(norm>=0){g.enableVertexAttribArray(norm);g.vertexAttribPointer(norm,3,g.FLOAT,false,24,12);}
        g.uniformMatrix4fv(this.loc(p,'uModel'),false,new Float32Array([R[0],R[3],R[6],0,R[1],R[4],R[7],0,R[2],R[5],R[8],0,...t,1]));
        if(p===this.program){
          g.uniform1f(this.loc(p,'uSelected'),o.selected?1:0);g.uniform3fv(this.loc(p,'uColor'),o.color);g.uniform1f(this.loc(p,'uMetal'),o.metal);g.uniform1f(this.loc(p,'uRough'),o.rough);g.uniform1f(this.loc(p,'uFloor'),o.kind==='floor'?1:0);
          const art=this.artwork(o.art);g.activeTexture(g.TEXTURE1);g.bindTexture(g.TEXTURE_2D,art?.ready?art.texture:this.blank);
          g.uniform1f(this.loc(p,'uArtEnabled'),art?.ready?1:0);g.uniform1f(this.loc(p,'uBaseZ'),t[2]);g.uniform4fv(this.loc(p,'uArtRect'),artworkRect(o.art,art?.aspect||1));
        }
        g.drawArrays(g.TRIANGLES,0,item.count);
      }
    }
    draw(scene,meshes,view,width,height,rack,selectedSlot=null){
      if(this.lost)throw Error('Graphics context lost; waiting for recovery.');const g=this.gl;if(this.canvas.width!==width||this.canvas.height!==height){this.canvas.width=width;this.canvas.height=height;}const objects=this.objects(scene,meshes,rack,selectedSlot),box=root.LabRaxScene.bounds(scene,meshes),light=root.LabRaxScene.camera(box,.62,.8,2048,2048,.79).matrix;
      g.enable(g.DEPTH_TEST);g.depthMask(true);g.depthFunc(g.LEQUAL);g.disable(g.CULL_FACE);g.disable(g.BLEND);g.disable(g.DITHER);
      const key=JSON.stringify([scene.slots,scene.parts.map(p=>p.key),rack?.placements.map(p=>[p.id,p.slot])]);
      if(this.shadows&&key!==this.shadowKey){g.bindFramebuffer(g.FRAMEBUFFER,this.shadowFbo);g.viewport(0,0,this.shadowSize,this.shadowSize);g.clearColor(1,1,1,1);g.clear(g.COLOR_BUFFER_BIT|g.DEPTH_BUFFER_BIT);g.enable(g.POLYGON_OFFSET_FILL);g.polygonOffset(2,3);g.useProgram(this.depthProgram);g.uniformMatrix4fv(this.loc(this.depthProgram,'uCamera'),false,light);this.submit(this.depthProgram,objects);g.disable(g.POLYGON_OFFSET_FILL);this.shadowKey=key;}
      objects.push({key:'studio-floor',mesh:this.geometry.floor,R:I,t:[0,0,0],kind:'floor',color:rgb('#1a2330'),metal:.05,rough:.8});
      const depthTarget=this.sceneDepthTarget(width,height),depthKey=key+JSON.stringify(Array.from(view.matrix))+width+':'+height;
      if(this.ambientOcclusion&&depthTarget.ready&&this.depthKey!==depthKey){g.bindFramebuffer(g.FRAMEBUFFER,depthTarget.fbo);g.viewport(0,0,depthTarget.width,depthTarget.height);g.clearColor(1,1,1,1);g.clear(g.COLOR_BUFFER_BIT|g.DEPTH_BUFFER_BIT);g.useProgram(this.depthProgram);g.uniformMatrix4fv(this.loc(this.depthProgram,'uCamera'),false,view.matrix);this.submit(this.depthProgram,objects);this.depthKey=depthKey;}
      g.bindFramebuffer(g.FRAMEBUFFER,null);g.viewport(0,0,width,height);g.clearColor(.035,.05,.075,1);g.clear(g.COLOR_BUFFER_BIT|g.DEPTH_BUFFER_BIT);g.useProgram(this.program);g.uniformMatrix4fv(this.loc(this.program,'uCamera'),false,view.matrix);g.uniformMatrix4fv(this.loc(this.program,'uLight'),false,light);g.uniform3fv(this.loc(this.program,'uEye'),view.eye);g.uniform1f(this.loc(this.program,'uShadowEnabled'),this.shadows?1:0);g.activeTexture(g.TEXTURE0);g.bindTexture(g.TEXTURE_2D,this.shadowTexture);g.uniform1i(this.loc(this.program,'uShadow'),0);g.uniform1i(this.loc(this.program,'uArtwork'),1);
      g.uniform1f(this.loc(this.program,'uShadowTexel'),1/this.shadowSize);g.uniform4fv(this.loc(this.program,'uDepthParams'),view.depthParams);g.uniform1f(this.loc(this.program,'uAOEnabled'),this.ambientOcclusion&&depthTarget.ready?1:0);g.activeTexture(g.TEXTURE2);g.bindTexture(g.TEXTURE_2D,depthTarget.texture);g.uniform1i(this.loc(this.program,'uSceneDepth'),2);this.submit(this.program,objects);
      this.pickState={view,objects:objects.filter(o=>o.kind!=='floor'),rack};
      this.stats={objects:objects.length,triangles:objects.reduce((n,o)=>n+o.mesh.triangles.length,0),shadows:this.shadows,ambientOcclusion:this.ambientOcclusion&&depthTarget.ready,perspective:view.perspective};return this.canvas;
    }
    pick(x,y){
      if(!this.pickState)return null;const {view,objects,rack}=this.pickState,ray=view.ray(x,y);let best=Infinity,hit=null;
      for(const object of objects){const R=object.R,q=sub(ray.origin,object.t),rotate=v=>[R[0]*v[0]+R[3]*v[1]+R[6]*v[2],R[1]*v[0]+R[4]*v[1]+R[7]*v[2],R[2]*v[0]+R[5]*v[1]+R[8]*v[2]],origin=rotate(q),direction=rotate(ray.direction);
        for(const t of object.mesh.triangles){const [a,b,c]=t.map(i=>object.mesh.vertices[i]),e1=sub(b,a),e2=sub(c,a),p=cross(direction,e2),det=dot(e1,p);if(Math.abs(det)<1e-8)continue;const s=sub(origin,a),u=dot(s,p)/det;if(u<0||u>1)continue;const q=cross(s,e1),v=dot(direction,q)/det;if(v<0||u+v>1)continue;const distance=dot(e2,q)/det;if(distance>0&&distance<best){best=distance;hit=object;}}
      }
      const distance=(-3-ray.origin[1])/ray.direction[1],p=add(ray.origin,ray.direction.map(v=>v*distance)),slot=rack? rack.slots-Math.floor(p[2]/44.45):0;
      if(hit?.slot)return hit.slot;
      if(distance>0&&distance<best&&Math.abs(p[0])<=104&&slot>=1&&slot<=rack?.slots)return slot;
      return null;
    }
    dispose(){this.disposed=true;const g=this.gl;for(const {buffer} of this.buffers.values())g.deleteBuffer(buffer);for(const a of this.textures.values())if(a.texture)g.deleteTexture(a.texture);if(this.depthTarget){g.deleteFramebuffer(this.depthTarget.fbo);g.deleteTexture(this.depthTarget.texture);g.deleteRenderbuffer(this.depthTarget.depth);}g.deleteTexture(this.blank);g.deleteTexture(this.shadowTexture);g.deleteFramebuffer(this.shadowFbo);g.deleteRenderbuffer(this.shadowDepth);g.deleteProgram(this.program);g.deleteProgram(this.depthProgram);}
  }
  const api={Renderer,camera,equipment,Mesh,slab,rounded,artworkRect};root.LabRaxStudio=api;if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(typeof window==='undefined'?globalThis:window);
