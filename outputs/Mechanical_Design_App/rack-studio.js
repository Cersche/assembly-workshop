// Local preview renderer. Does not generate manufacturing geometry or modify saved data.
(function(root){
  'use strict';
  const I=[1,0,0,0,1,0,0,0,1], TAU=Math.PI*2;
  const add=(a,b)=>a.map((v,i)=>v+b[i]), sub=(a,b)=>a.map((v,i)=>v-b[i]);
  const dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0);
  const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
  const unit=a=>a.map(v=>v/(Math.hypot(...a)||1));
  function rgb(hex,fallback='#657582'){return /^#[0-9a-f]{6}$/i.test(hex||'')?[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255):rgb(fallback);}
  // Brighten (k > 1, toward white) or dim (k < 1, toward black) a linear colour.
  function shade(c,k){return k>=1?c.map(v=>v+(1-v)*(k-1)):c.map(v=>v*k);}
  // Image window on a faceplate front: width, height and centre height (mm above the plate's base Z).
  const DEFAULT_ART_WINDOW={w:216,h:36.4,z:22.225};
  // Generic window for a plate front face of plate_w x plate_h: same 18 mm side and 4 mm top/bottom margins as the default window.
  function artworkWindow(plateW,plateH,bottom=0){return {w:Math.max(1,plateW-36),h:Math.max(1,plateH-8),z:bottom+plateH/2};}
  // Selection outline: [centre x, centre z above base, half width, half height, corner radius] of the plate front.
  const DEFAULT_SELECTION=[0,22.225,125.5,21.75,4];
  function selectionRect(x0,x1,z0,z1,radius){return [(x0+x1)/2,(z0+z1)/2,(x1-x0)/2,(z1-z0)/2,Math.min(radius,(x1-x0)/2,(z1-z0)/2)];}
  // Largest part of the window clear of openings ({x,z,w,h} centres/sizes, same frame as win) plus a gap,
  // scored by how large an image of this aspect can be drawn in it. Returns win itself when nothing is in the way.
  function clearWindow(win,openings,aspect=1,gap=2){
    const cx=win.x||0,L=cx-win.w/2,R=cx+win.w/2,B=win.z-win.h/2,T=win.z+win.h/2,eps=1e-6;
    const obs=(openings||[]).map(o=>({l:o.x-o.w/2-gap,r:o.x+o.w/2+gap,b:o.z-o.h/2-gap,t:o.z+o.h/2+gap})).filter(o=>o.r>L&&o.l<R&&o.t>B&&o.b<T);
    if(!obs.length)return win;
    const xs=[...new Set([L,R,...obs.flatMap(o=>[o.l,o.r])].map(x=>Math.min(R,Math.max(L,x))))].sort((a,b)=>a-b);
    let best=null,score=-1;
    for(let i=0;i<xs.length;i++)for(let j=i+1;j<xs.length;j++){
      const x0=xs[i],x1=xs[j],spans=obs.filter(o=>o.r>x0+eps&&o.l<x1-eps).map(o=>[o.b,o.t]).sort((a,b)=>a[0]-b[0]);
      let z=B;for(const [b,t] of [...spans,[T,T]]){
        if(b>z+eps){const h=Math.min(b,T)-z,width=Math.min(x1-x0,h*aspect),s=width*width/aspect-1e-6*Math.hypot((x0+x1)/2-cx,z+h/2-win.z);
          if(s>score){score=s;best={x:(x0+x1)/2,z:z+h/2,w:x1-x0,h};}}
        z=Math.max(z,t);if(z>=T)break;}
    }
    return best||win;
  }
  function artworkRect(art={},aspect=1,win=DEFAULT_ART_WINDOW){
    // Match the existing assembly viewer's saved normalized placement semantics.
    art=art||{};win=win||DEFAULT_ART_WINDOW;if(win.openings)win=clearWindow(win,win.openings,aspect);
    const width=Math.min(win.w,win.h*aspect)*Math.max(.05,art.scale??.65),height=width/aspect;
    return [(win.x||0)+((art.x??.5)-.5)*(win.w-width),win.z+(.5-(art.y??.5))*(win.h-height),width,height];
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
  // Split the front beam into body + painted logo faces (indices from rack-logo-faces.json).
  function logoMeshes(mesh){const faces=new Set(mesh.logo_faces||[]);for(const f of faces)if(!Number.isInteger(f)||f<0||f>=mesh.triangles.length)throw Error('Logo face index out of range: '+f);const logo=[],body=[];mesh.triangles.forEach((t,i)=>(faces.has(i)?logo:body).push(t));return {logo:{vertices:mesh.vertices,triangles:logo},body:{vertices:mesh.vertices,triangles:body}};}
  function equipment(){return Object.fromEntries(['tray','plate','brass','bolts','sockets'].map(k=>[k,new Mesh()]));}
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
    uniform sampler2D uShadow,uArtwork,uSceneDepth; uniform vec4 uArtRect,uDepthParams,uSelRect; uniform float uArtEnabled,uBaseZ,uAOEnabled,uShadowTexel,uSelRadius,uAlpha;
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
        // uSelRect = plate front centre (x, z above base) and half size; the rim follows its rounded outline at any U height.
        vec2 q=abs(vec2(vWorld.x,vWorld.z-uBaseZ)-uSelRect.xy)-(uSelRect.zw-uSelRadius);
        float edge=length(max(q,vec2(0.)))+min(max(q.x,q.y),0.)-uSelRadius;
        float rim=1.-smoothstep(.8,2.4,abs(edge));
        c=mix(c,vec3(.25,.7,1.),.2);c=mix(c,vec3(.35,.85,1.),rim*.95);
      }
      if(uFloor>.5){float fade=1.-smoothstep(220.,600.,length(vWorld.xy-vec2(0.,120.)));c=mix(vec3(.035,.05,.075),c,fade);}
      gl_FragColor=vec4(c,uAlpha);}`;
  const DEPTH=`precision highp float;void main(){vec4 c=fract(gl_FragCoord.z*vec4(1.,255.,65025.,16581375.));c-=c.yzww*vec4(1./255.,1./255.,1./255.,0.);gl_FragColor=c;}`;
  class Renderer{
    constructor(){
      this.canvas=document.createElement('canvas');const gl=this.gl=this.canvas.getContext('webgl',{alpha:true,antialias:true,preserveDrawingBuffer:true,premultipliedAlpha:false});if(!gl)throw Error('WebGL unavailable. Enable graphics acceleration for the rack preview.');
      this.buffers=new Map();this.textures=new Map();this.geometry=equipment();this.shadowKey='';this.invalidated=()=>{};this.ambientOcclusion=true;
      this.logoFaces=null;if(typeof fetch==='function')fetch('/rack-references/rack-logo-faces.json').then(r=>r.ok?r.json():null).then(d=>{if(d&&Array.isArray(d.triangles)){this.logoFaces=d.triangles;this.invalidated();}}).catch(()=>{});
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
      // Parts may carry their own mesh (cable tubes, built per route); otherwise the key names a loaded mesh.
      const appearance=rack?.appearance||{},objects=scene.parts.map(p=>({...p,mesh:p.mesh||meshes[p.key],color:rgb(appearance.components?.[p.key]||(p.kind==='guide'?null:appearance.color),p.kind==='foot'?'#28313d':p.kind==='panel'?'#627a78':p.kind==='guide'?'#b4d335':'#8b9aa8'),metal:.05,rough:.52,
        // A selected cable guide turns selection blue as a whole (the plate rim outline does not apply to it).
        ...(p.kind==='guide'&&p.selected?{color:rgb('#5fd0ff'),selected:false}:{}),
        // Port markers (cable-ports.js) carry their connector-type tint; a selected port turns selection blue.
        ...(p.kind==='port'?{color:rgb(p.selected?'#5fd0ff':p.tint,'#c3ccd6'),selected:false,metal:.1,rough:.4}:{}),
        // Cables (cable-view.js tubes): type or chosen colour; a selected run is brightened, the rest dimmed while one is selected.
        ...(p.kind==='cable'?{color:shade(rgb(p.tint,'#c3ccd6'),p.lit?1.35:p.dim?.35:1),selected:false,metal:0,rough:.55}:{}),
        // Exit grommets: amber, selection blue.
        ...(p.kind==='exit'?{color:rgb(p.selected?'#5fd0ff':'#d9a441'),selected:false,metal:.1,rough:.45}:{})}));
      // Suggestion "Show me" (cable management Step 4): guides, ports and exits not involved are dimmed like cables.
      for(const o of objects)if(o.dim&&o.kind!=='cable'&&(o.kind==='guide'||o.kind==='port'||o.kind==='exit'))o.color=shade(o.color,.35);
      const beam=meshes.beam_top_front,faces=beam&&(beam.logo_faces||this.logoFaces);
      if(faces){this.logoCache=this.logoCache||new WeakMap();let split=this.logoCache.get(beam);if(!split){split=logoMeshes({...beam,logo_faces:faces});this.logoCache.set(beam,split);}
        for(let i=objects.length-1;i>=0;i--){const o=objects[i];if(o.key!=='beam_top_front')continue;objects.splice(i,1,{...o,key:'beam_top_front-body',mesh:split.body},{...o,key:'beam_top_front-logo',mesh:split.logo,color:rgb(appearance.logo_color,'#a6e22e'),rough:.4});}}
      for(const allocation of rack?.placements||[]){const a=allocation.assembly?.appearance||{},z=(rack.slots-(allocation.slot+allocation.span-1))*44.45;for(const [key,color,metal,rough] of [['tray',a.tray||'#4d8e6e',0,.48],['plate',a.faceplate||'#4e75a3',0,.38],['brass','#c89a46',.82,.28],['bolts','#303640',.72,.3],['sockets','#11151c',.2,.65]])objects.push({key:'studio-'+key,mesh:this.geometry[key],R:I,t:[0,0,z],kind:key,slot:allocation.slot,selected:key==='plate'&&selectedSlot>=allocation.slot&&selectedSlot<allocation.slot+allocation.span,color:rgb(color),metal,rough,art:key==='plate'?a.artwork:null});}
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
          const sel=o.selRect||DEFAULT_SELECTION;g.uniform1f(this.loc(p,'uSelected'),o.selected?1:0);g.uniform4fv(this.loc(p,'uSelRect'),sel.slice(0,4));g.uniform1f(this.loc(p,'uSelRadius'),sel[4]);g.uniform3fv(this.loc(p,'uColor'),o.color);g.uniform1f(this.loc(p,'uMetal'),o.metal);g.uniform1f(this.loc(p,'uRough'),o.rough);g.uniform1f(this.loc(p,'uFloor'),o.kind==='floor'?1:0);g.uniform1f(this.loc(p,'uAlpha'),o.alpha??1);
          const art=this.artwork(o.art);g.activeTexture(g.TEXTURE1);g.bindTexture(g.TEXTURE_2D,art?.ready?art.texture:this.blank);
          g.uniform1f(this.loc(p,'uArtEnabled'),art?.ready?1:0);g.uniform1f(this.loc(p,'uBaseZ'),t[2]);g.uniform4fv(this.loc(p,'uArtRect'),artworkRect(o.art,art?.aspect||1,o.artWindow));
        }
        g.drawArrays(g.TRIANGLES,0,item.count);
      }
    }
    draw(scene,meshes,view,width,height,rack,selectedSlot=null){
      if(this.lost)throw Error('Graphics context lost; waiting for recovery.');const g=this.gl;if(this.canvas.width!==width||this.canvas.height!==height){this.canvas.width=width;this.canvas.height=height;}const objects=this.objects(scene,meshes,rack,selectedSlot),box=root.LabRaxScene.bounds({parts:scene.parts.filter(p=>!p.mesh)},meshes),light=root.LabRaxScene.camera(box,.62,.8,2048,2048,.79).matrix;
      g.enable(g.DEPTH_TEST);g.depthMask(true);g.depthFunc(g.LEQUAL);g.disable(g.CULL_FACE);g.disable(g.BLEND);g.disable(g.DITHER);
      // See-through parts (Cables view) are drawn last, blended, without depth writes; they cast no shadow and are not pickable.
      // ghostTrays (Cables view): equipment trays turn see-through so the port markers inside them show and can be clicked.
      if(this.ghostTrays)for(const o of objects)if(o.kind==='tray'){o.ghost=true;o.alpha=.3;}
      const solid=objects.filter(o=>!o.ghost),ghosts=objects.filter(o=>o.ghost);
      const key=JSON.stringify([scene.slots,solid.map(p=>p.key+p.t),rack?.placements.map(p=>[p.id,p.slot])]);
      if(this.shadows&&key!==this.shadowKey){g.bindFramebuffer(g.FRAMEBUFFER,this.shadowFbo);g.viewport(0,0,this.shadowSize,this.shadowSize);g.clearColor(1,1,1,1);g.clear(g.COLOR_BUFFER_BIT|g.DEPTH_BUFFER_BIT);g.enable(g.POLYGON_OFFSET_FILL);g.polygonOffset(2,3);g.useProgram(this.depthProgram);g.uniformMatrix4fv(this.loc(this.depthProgram,'uCamera'),false,light);this.submit(this.depthProgram,solid);g.disable(g.POLYGON_OFFSET_FILL);this.shadowKey=key;}
      solid.push({key:'studio-floor',mesh:this.geometry.floor,R:I,t:[0,0,0],kind:'floor',color:rgb('#1a2330'),metal:.05,rough:.8});
      const depthTarget=this.sceneDepthTarget(width,height),depthKey=key+JSON.stringify(Array.from(view.matrix))+width+':'+height;
      if(this.ambientOcclusion&&depthTarget.ready&&this.depthKey!==depthKey){g.bindFramebuffer(g.FRAMEBUFFER,depthTarget.fbo);g.viewport(0,0,depthTarget.width,depthTarget.height);g.clearColor(1,1,1,1);g.clear(g.COLOR_BUFFER_BIT|g.DEPTH_BUFFER_BIT);g.useProgram(this.depthProgram);g.uniformMatrix4fv(this.loc(this.depthProgram,'uCamera'),false,view.matrix);this.submit(this.depthProgram,solid);this.depthKey=depthKey;}
      g.bindFramebuffer(g.FRAMEBUFFER,null);g.viewport(0,0,width,height);g.clearColor(.035,.05,.075,1);g.clear(g.COLOR_BUFFER_BIT|g.DEPTH_BUFFER_BIT);g.useProgram(this.program);g.uniformMatrix4fv(this.loc(this.program,'uCamera'),false,view.matrix);g.uniformMatrix4fv(this.loc(this.program,'uLight'),false,light);g.uniform3fv(this.loc(this.program,'uEye'),view.eye);g.uniform1f(this.loc(this.program,'uShadowEnabled'),this.shadows?1:0);g.activeTexture(g.TEXTURE0);g.bindTexture(g.TEXTURE_2D,this.shadowTexture);g.uniform1i(this.loc(this.program,'uShadow'),0);g.uniform1i(this.loc(this.program,'uArtwork'),1);
      g.uniform1f(this.loc(this.program,'uShadowTexel'),1/this.shadowSize);g.uniform4fv(this.loc(this.program,'uDepthParams'),view.depthParams);g.uniform1f(this.loc(this.program,'uAOEnabled'),this.ambientOcclusion&&depthTarget.ready?1:0);g.activeTexture(g.TEXTURE2);g.bindTexture(g.TEXTURE_2D,depthTarget.texture);g.uniform1i(this.loc(this.program,'uSceneDepth'),2);this.submit(this.program,solid);
      if(ghosts.length){g.enable(g.BLEND);g.blendFunc(g.SRC_ALPHA,g.ONE_MINUS_SRC_ALPHA);g.depthMask(false);g.uniform1f(this.loc(this.program,'uAOEnabled'),0);this.submit(this.program,ghosts);g.depthMask(true);g.disable(g.BLEND);}
      this.pickState={view,objects:solid.filter(o=>o.kind!=='floor'),rack};
      const all=[...solid,...ghosts];
      this.stats={objects:all.length,guides:solid.filter(o=>o.kind==='guide').length,ports:solid.filter(o=>o.kind==='port').length,cables:solid.filter(o=>o.kind==='cable').length,exits:solid.filter(o=>o.kind==='exit').length,ghosts:ghosts.length,triangles:all.reduce((n,o)=>n+o.mesh.triangles.length,0),shadows:this.shadows,ambientOcclusion:this.ambientOcclusion&&depthTarget.ready,perspective:view.perspective};return this.canvas;
    }
    // Nearest solid object under the pointer as {hit, best, ray}, or null before the first draw.
    hitTest(x,y){
      if(!this.pickState)return null;const {view,objects}=this.pickState,ray=view.ray(x,y);let best=Infinity,hit=null;
      for(const object of objects){const R=object.R,q=sub(ray.origin,object.t),rotate=v=>[R[0]*v[0]+R[3]*v[1]+R[6]*v[2],R[1]*v[0]+R[4]*v[1]+R[7]*v[2],R[2]*v[0]+R[5]*v[1]+R[8]*v[2]],origin=rotate(q),direction=rotate(ray.direction);
        for(const t of object.mesh.triangles){const [a,b,c]=t.map(i=>object.mesh.vertices[i]),e1=sub(b,a),e2=sub(c,a),p=cross(direction,e2),det=dot(e1,p);if(Math.abs(det)<1e-8)continue;const s=sub(origin,a),u=dot(s,p)/det;if(u<0||u>1)continue;const q=cross(s,e1),v=dot(direction,q)/det;if(v<0||u+v>1)continue;const distance=dot(e2,q)/det;if(distance>0&&distance<best){best=distance;hit=object;}}
      }
      return {hit,best,ray,point:hit?add(ray.origin,ray.direction.map(v=>v*best)):null};
    }
    // Cable guide id when a guide is the nearest thing under the pointer.
    pickGuide(x,y){return this.hitTest(x,y)?.hit?.guide||null;}
    // Port key (allocation id / port id) when a port marker is the nearest thing under the pointer.
    pickPort(x,y){return this.hitTest(x,y)?.hit?.port||null;}
    // Cable id or exit id when a cable tube or exit grommet is the nearest thing under the pointer.
    pickCable(x,y){return this.hitTest(x,y)?.hit?.cable||null;}
    pickExit(x,y){return this.hitTest(x,y)?.hit?.exit||null;}
    pick(x,y){
      const found=this.hitTest(x,y);if(!found)return null;const {hit,best,ray}=found,rack=this.pickState.rack;
      const distance=(-3-ray.origin[1])/ray.direction[1],p=add(ray.origin,ray.direction.map(v=>v*distance)),slot=rack? rack.slots-Math.floor(p[2]/44.45):0;
      if(hit?.slot)return hit.slot;
      if(distance>0&&distance<best&&Math.abs(p[0])<=104&&slot>=1&&slot<=rack?.slots)return slot;
      return null;
    }
    dispose(){this.disposed=true;const g=this.gl;for(const {buffer} of this.buffers.values())g.deleteBuffer(buffer);for(const a of this.textures.values())if(a.texture)g.deleteTexture(a.texture);if(this.depthTarget){g.deleteFramebuffer(this.depthTarget.fbo);g.deleteTexture(this.depthTarget.texture);g.deleteRenderbuffer(this.depthTarget.depth);}g.deleteTexture(this.blank);g.deleteTexture(this.shadowTexture);g.deleteFramebuffer(this.shadowFbo);g.deleteRenderbuffer(this.shadowDepth);g.deleteProgram(this.program);g.deleteProgram(this.depthProgram);}
  }

  // Small orthographic previews share the rack shader, upload, uniform and submit code.
  // Nothing in Renderer.draw or its shaders is changed by this adapter.
  function previewCamera(view,W,H,dpr=1,range=100000){
    const cy=Math.cos(view.yaw),sy=Math.sin(view.yaw),cp=Math.cos(view.pitch),sp=Math.sin(view.pitch),
      right=[cy,-sy,0],up=[sp*sy,sp*cy,cp],depth=[cp*sy,cp*cy,-sp],cen=view.cen||[0,40,25],
      sc=Math.min(W,H)/(view.span||280)*view.zoom,tx=2*(view.panX||0)*dpr/W,ty=-2*(view.panY||0)*dpr/H,m=new Float32Array(16);
    for(let i=0;i<3;i++){m[i*4]=right[i]*sc*2/W;m[i*4+1]=up[i]*sc*2/H;m[i*4+2]=depth[i]/range;}
    m[12]=tx-dot(cen,right)*sc*2/W;m[13]=ty-dot(cen,up)*sc*2/H;m[14]=-dot(cen,depth)/range;m[15]=1;
    return {matrix:m,eye:sub(cen,depth.map(v=>v*range)),depthParams:[0,0,range,0],
      project:p=>{const v=sub(p,cen);return [W/2+(view.panX||0)*dpr+dot(v,right)*sc,H/2+(view.panY||0)*dpr-dot(v,up)*sc,dot(v,depth)];}};
  }
  function featureEdges(v){
    const edges=new Map(),points=new Map(),key=p=>p.map(x=>Math.round(x*1e6)).join(',');
    for(let i=0;i<v.length;i+=9){const p=[v.slice(i,i+3),v.slice(i+3,i+6),v.slice(i+6,i+9)],n=unit(cross(sub(p[1],p[0]),sub(p[2],p[0])));if(!Math.hypot(...n))continue;
      for(let j=0;j<3;j++){const a=key(p[j]),b=key(p[(j+1)%3]);if(a===b)continue;points.set(a,Array.from(p[j]));points.set(b,Array.from(p[(j+1)%3]));const id=[a,b].sort().join('|');let e=edges.get(id);if(!e){e={a,b,n:[]};edges.set(id,e);}e.n.push(n);}}
    const lines=[...edges.values()].filter(e=>e.n.length!==2||dot(e.n[0],e.n[1])<Math.cos(Math.PI/6)-1e-7).map(e=>[e.a,e.b]);
    // Collapse collinear boundary subdivisions; triangulation must not add edge lines.
    const adj=new Map();lines.forEach((e,i)=>e.forEach(p=>{if(!adj.has(p))adj.set(p,new Set());adj.get(p).add(i);}));
    for(const [p,ids] of adj){if(ids.size!==2)continue;const [i,j]=ids,[a,b]=[lines[i],lines[j]];if(!a||!b)continue;const x=a.find(k=>k!==p),y=b.find(k=>k!==p);if(x===y)continue;
      if(dot(unit(sub(points.get(x),points.get(p))),unit(sub(points.get(y),points.get(p))))>-.999999)continue;
      adj.get(x).delete(i);adj.get(y).delete(j);lines[i]=[x,y];lines[j]=null;adj.get(x).add(i);adj.get(y).add(i);ids.clear();}
    return lines.filter(Boolean).flatMap(e=>e.flatMap(p=>points.get(p)));
  }
  const median=a=>{const b=[...a].sort((a,b)=>a-b),n=b.length;return n?(b[(n-1)>>1]+b[n>>1])/2:0;};
  function previewSwitch({available=true,preference='',lost=false,forced=false,level='medium',times=[]}){
    if(!available||preference==='canvas'||lost||forced)return {renderer:'canvas',level};
    const ms=median(times.slice(-10));if(times.length>=10){if(level==='low'&&ms>33)return {renderer:'canvas',level};if(level!=='low'&&ms>16)return {renderer:'webgl',level:level==='high'?'medium':'low'};}
    return {renderer:'webgl',level};
  }
  class PreviewRenderer{
    constructor(){this.canvas=document.createElement('canvas');this.gl=this.canvas.getContext('webgl',{alpha:false,antialias:true,preserveDrawingBuffer:true});if(!this.gl)throw Error('WebGL unavailable');this.init();}
    init(){const g=this.gl;this.buffers=new Map();this.locations=new Map();this.records=[];this.identities=new WeakMap();this.program=this.programFor(VS,FS);
      this.blank=g.createTexture();g.bindTexture(g.TEXTURE_2D,this.blank);g.texImage2D(g.TEXTURE_2D,0,g.RGBA,1,1,0,g.RGBA,g.UNSIGNED_BYTE,new Uint8Array([255,255,255,0]));this.textureSettings();this.uploads=0;}
    artwork(){return null;}
    geometryFor(v,version){
      let r=this.identities.get(v);if(r&&r.version===version&&this.buffers.has(r.key))return r;
      // The tray sketch is recreated by its caller. Reuse equal geometry as well as array identities.
      r=this.records.find(r=>r.version===version&&r.v.length===v.length&&r.v.every((n,i)=>n===v[i]));
      if(!r){const mesh={vertices:[],triangles:[]};let sum=[0,0,0];for(let i=0;i<v.length;i+=3){mesh.vertices.push([v[i],v[i+1],v[i+2]]);for(let k=0;k<3;k++)sum[k]+=v[i+k];if(i%9===0)mesh.triangles.push([i/3,i/3+1,i/3+2]);}
        r={v,version,mesh,radius:mesh.vertices.reduce((n,p)=>Math.max(n,Math.hypot(...p)),0),key:{},center:sum.map(x=>x/(v.length/3||1))};this.records.push(r);this.upload(r.key,mesh);this.uploads++;}
      this.identities.set(v,r);return r;
    }
    draw(sets,view,W,H,dpr,edges=false){
      const g=this.gl;if(this.canvas.width!==W)this.canvas.width=W;if(this.canvas.height!==H)this.canvas.height=H;
      const used=new Set(),objects=sets.map(s=>{const r=this.geometryFor(s.v,s.version);used.add(r);return {key:r.key,mesh:r.mesh,R:I,t:[0,0,0],color:s.color.map(c=>c/255),metal:0,rough:.52,alpha:s.alpha??1,r};});
      for(const r of this.records)if(!used.has(r)){g.deleteBuffer(this.buffers.get(r.key).buffer);this.buffers.delete(r.key);if(r.edgeBuffer)g.deleteBuffer(r.edgeBuffer);this.identities.delete(r.v);}
      this.records=this.records.filter(r=>used.has(r));
      const cen=view.cen||[0,40,25],range=Math.max(1,...this.records.map(r=>r.radius+Math.hypot(...cen)))*2,cam=previewCamera(view,W,H,dpr,range),p=this.program;
      g.bindFramebuffer(g.FRAMEBUFFER,null);g.viewport(0,0,W,H);g.enable(g.DEPTH_TEST);g.depthFunc(g.LEQUAL);g.depthMask(true);g.disable(g.BLEND);g.disable(g.CULL_FACE);g.disable(g.DITHER);g.clearColor(18/255,20/255,24/255,1);g.clear(g.COLOR_BUFFER_BIT|g.DEPTH_BUFFER_BIT);g.useProgram(p);
      g.uniformMatrix4fv(this.loc(p,'uCamera'),false,cam.matrix);g.uniformMatrix4fv(this.loc(p,'uLight'),false,cam.matrix);g.uniform3fv(this.loc(p,'uEye'),cam.eye);g.uniform1f(this.loc(p,'uShadowEnabled'),0);g.uniform1f(this.loc(p,'uAOEnabled'),0);
      for(const [i,name] of ['uShadow','uArtwork','uSceneDepth'].entries()){g.activeTexture(g.TEXTURE0+i);g.bindTexture(g.TEXTURE_2D,this.blank);g.uniform1i(this.loc(p,name),i);}
      g.uniform4fv(this.loc(p,'uDepthParams'),cam.depthParams);
      const solid=objects.filter(o=>o.alpha>=1),ghost=objects.filter(o=>o.alpha<1).sort((a,b)=>cam.project(b.r.center)[2]-cam.project(a.r.center)[2]);
      if(edges){g.enable(g.POLYGON_OFFSET_FILL);g.polygonOffset(1,1);}this.submit(p,solid);g.disable(g.POLYGON_OFFSET_FILL);
      if(edges){for(const o of solid){const r=o.r;if(!r.edgeBuffer){const lines=featureEdges(r.v),data=new Float32Array(lines.length*2);for(let i=0;i<lines.length;i+=3){data.set(lines.slice(i,i+3),i*2);data.set([0,0,1],i*2+3);}r.edgeBuffer=g.createBuffer();r.edgeCount=data.length/6;g.bindBuffer(g.ARRAY_BUFFER,r.edgeBuffer);g.bufferData(g.ARRAY_BUFFER,data,g.STATIC_DRAW);}
          g.bindBuffer(g.ARRAY_BUFFER,r.edgeBuffer);g.vertexAttribPointer(this.loc(p,'aPosition'),3,g.FLOAT,false,24,0);g.vertexAttribPointer(this.loc(p,'aNormal'),3,g.FLOAT,false,24,12);g.uniform3fv(this.loc(p,'uColor'),[.035,.04,.05]);g.drawArrays(g.LINES,0,r.edgeCount);}}
      if(ghost.length){g.enable(g.BLEND);g.blendFunc(g.SRC_ALPHA,g.ONE_MINUS_SRC_ALPHA);g.depthMask(false);this.submit(p,ghost);g.depthMask(true);g.disable(g.BLEND);}
      this.triangles=objects.reduce((n,o)=>n+o.mesh.triangles.length,0);return this.canvas;
    }
    dispose(lose=true){const g=this.gl;for(const b of this.buffers.values())g.deleteBuffer(b.buffer);for(const r of this.records)if(r.edgeBuffer)g.deleteBuffer(r.edgeBuffer);g.deleteProgram(this.program);g.deleteTexture(this.blank);this.records=[];this.buffers.clear();if(lose)g.getExtension('WEBGL_lose_context')?.loseContext();}
  }
  for(const name of ['programFor','loc','textureSettings','upload','submit'])PreviewRenderer.prototype[name]=Renderer.prototype[name];

  const api={Renderer,PreviewRenderer,previewCamera,previewSwitch,featureEdges,median,camera,equipment,logoMeshes,Mesh,slab,rounded,artworkRect,artworkWindow,clearWindow,selectionRect,DEFAULT_SELECTION};root.LabRaxStudio=api;if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(typeof window==='undefined'?globalThis:window);
