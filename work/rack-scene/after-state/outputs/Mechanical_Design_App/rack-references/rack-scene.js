// Full-coordinate source meshes, recovered visual poses. No manufacturing adapter.
(function(root){
  'use strict';
  const U=44.45,PX=125.98,DEPTH=240;
  const I=[1,0,0,0,1,0,0,0,1],RX=[1,0,0,0,-1,0,0,0,-1],RY=[-1,0,0,0,1,0,0,0,-1],RZ=[-1,0,0,0,-1,0,0,0,1],R90=[0,-1,0,1,0,0,0,0,1];
  const sources={post1:[0,'1'],post2:[0,'9'],post3:[0,'17'],post4:[0,'24'],post5:[0,'31'],panel1:[0,'6'],panel2:[0,'14'],panel3:[0,'22'],panel4:[0,'29'],panel5:[0,'36'],beam_bottom:[1,'20'],beam_top_front:[1,'23'],beam_top_rear:[1,'18'],side_rail:[1,'28'],panel_bottom:[1,'13'],panel_top:[1,'11'],foot:[1,'6'],handle:[1,'25'],extension:[2,'1']};
  function apply(R,t,v){return [R[0]*v[0]+R[1]*v[1]+R[2]*v[2]+t[0],R[3]*v[0]+R[4]*v[1]+R[5]*v[2]+t[1],R[6]*v[0]+R[7]*v[1]+R[8]*v[2]+t[2]];}
  function frame(slots,panels=false){
    if(!Number.isInteger(slots)||slots<1||slots>48)throw Error('Unsupported rack preview slot count.');
    const parts=[],levels=[];let remaining=slots;
    while(remaining){const u=Math.min(5,remaining);levels.push(u);remaining-=u;}
    const add=(key,R,t,kind='frame')=>parts.push({key,R:R.slice(),t,kind,source:sources[key]});
    add('beam_bottom',I,[0,27.425,-7.575]);add('beam_bottom',RZ,[0,DEPTH-27.425,-7.575]);
    add('side_rail',RX,[-PX,120,-17.5]);add('side_rail',RY,[PX,120,-17.5]);add('panel_bottom',I,[0,120,-31.5],'panel');
    for(const x of [-124.73,124.73])for(const y of [55,185])add('foot',I,[x,y,-41],'foot');
    let z=0;
    for(const u of levels){const middle=z+u*U/2;
      for(const [R,x,y] of [[I,-PX,17.5],[RY,PX,17.5],[RX,-PX,DEPTH-17.5],[RZ,PX,DEPTH-17.5]])add('post'+u,R,[x,y,middle]);
      if(panels){add('panel'+u,R90,[-138.48,120,middle],'side');add('panel'+u,R90,[138.48,120,middle],'side');}z+=u*U;
    }
    const dz=(slots-5)*U;
    add('beam_top_front',I,[0,27.425,229.825+dz]);add('beam_top_rear',RZ,[0,DEPTH-27.425,229.825+dz]);
    add('side_rail',I,[-PX,120,239.75+dz]);add('side_rail',RZ,[PX,120,239.75+dz]);add('panel_top',I,[0,120,253.75+dz],'panel');
    add('handle',I,[-124.789,120,276+dz]);add('handle',RZ,[124.789,120,276+dz]);
    return {slots,parts,levels,pitch:U,manufacturing:false,pose_status:'Recovered visual placement; assembled fit UNKNOWN'};
  }
  function bounds(scene,meshes){const lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];
    for(const part of scene.parts)for(const v of meshes[part.key].vertices){const p=apply(part.R,part.t,v);for(let k=0;k<3;k++){lo[k]=Math.min(lo[k],p[k]);hi[k]=Math.max(hi[k],p[k]);}}
    return {lo,hi};
  }
  function camera(box,yaw,pitch,width,height,zoom=1){
    const center=box.lo.map((v,k)=>(v+box.hi[k])/2),sy=Math.sin(yaw),cy=Math.cos(yaw),sp=Math.sin(pitch),cp=Math.cos(pitch);
    const rotate=v=>{const x=v[0]-center[0],y=v[1]-center[1],z=v[2]-center[2],d=sy*x+cy*y;return [cy*x-sy*y,cp*z+sp*d,sp*z-cp*d];};
    const corners=[];for(const x of [box.lo[0],box.hi[0]])for(const y of [box.lo[1],box.hi[1]])for(const z of [box.lo[2],box.hi[2]])corners.push(rotate([x,y,z]));
    const limits=[0,1,2].map(k=>[Math.min(...corners.map(p=>p[k])),Math.max(...corners.map(p=>p[k]))]);
    const ox=(limits[0][0]+limits[0][1])/2,oy=(limits[1][0]+limits[1][1])/2;
    const scale=Math.min((width-105)/(limits[0][1]-limits[0][0]||1),(height-65)/(limits[1][1]-limits[1][0]||1))*zoom;
    const sx=2*scale/width,sz=2*scale/height,range=Math.max(1,...corners.map(p=>Math.abs(p[2])))*2;
    const matrix=new Float32Array([cy*sx,sp*sy*sz,cp*sy/range,0,-sy*sx,sp*cy*sz,cp*cy/range,0,0,cp*sz,-sp/range,0,
      -(cy*center[0]-sy*center[1]+ox)*sx,-(sp*sy*center[0]+sp*cy*center[1]+cp*center[2]+oy)*sz,-(cp*sy*center[0]+cp*cy*center[1]-sp*center[2])/range,1]);
    return {matrix,scale,project:v=>{const p=rotate(v);return [width/2+(p[0]-ox)*scale,height/2-(p[1]-oy)*scale,p[2]];}};
  }
  async function load(fetcher){
    const catalogResponse=await fetcher('/rack-references/catalog.json');if(!catalogResponse.ok)throw Error('Rack source catalog unavailable.');
    const catalog=await catalogResponse.json(),meshes={};
    await Promise.all(Object.entries(sources).filter(([key])=>key!=='extension').map(async([key,[ref,id]])=>{
      const component=catalog.references[ref].components.find(c=>c.id===id);const response=await fetcher(component.url);if(!response.ok)throw Error('Rack component unavailable: '+component.name);meshes[key]=await response.json();
    }));return meshes;
  }
  class Renderer{
    constructor(){
      this.canvas=document.createElement('canvas');const gl=this.gl=this.canvas.getContext('webgl',{alpha:true,antialias:true,preserveDrawingBuffer:true,premultipliedAlpha:false});
      if(!gl)throw Error('WebGL is unavailable; enable graphics acceleration for the source-mesh rack preview.');
      const shader=(type,source)=>{const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(s));return s;};
      const program=this.program=gl.createProgram();
      gl.attachShader(program,shader(gl.VERTEX_SHADER,'attribute vec3 aPosition; attribute vec3 aNormal; uniform mat4 uModel; uniform mat4 uCamera; varying vec3 normal; void main(){normal=mat3(uModel)*aNormal; gl_Position=uCamera*uModel*vec4(aPosition,1.0);}'));
      gl.attachShader(program,shader(gl.FRAGMENT_SHADER,'precision mediump float; varying vec3 normal; uniform vec3 uColor; void main(){vec3 n=normalize(normal); float light=0.48+0.52*abs(dot(n,normalize(vec3(0.4,-0.65,0.8)))); gl_FragColor=vec4(uColor*light,1.0);}'));
      gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(program));
      this.position=gl.getAttribLocation(program,'aPosition');this.normal=gl.getAttribLocation(program,'aNormal');this.model=gl.getUniformLocation(program,'uModel');this.camera=gl.getUniformLocation(program,'uCamera');this.color=gl.getUniformLocation(program,'uColor');this.buffers=new Map();
    }
    upload(key,mesh){
      if(this.buffers.has(key))return this.buffers.get(key);
      const gl=this.gl,data=new Float32Array(mesh.triangles.length*18);let offset=0;
      for(const t of mesh.triangles){const a=mesh.vertices[t[0]],b=mesh.vertices[t[1]],c=mesh.vertices[t[2]],u=b.map((v,k)=>v-a[k]),v=c.map((x,k)=>x-a[k]),n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]],len=Math.hypot(...n)||1;for(const p of [a,b,c]){data.set(p,offset);data.set(n.map(x=>x/len),offset+3);offset+=6;}}
      const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,data,gl.STATIC_DRAW);const item={buffer,count:mesh.triangles.length*3};this.buffers.set(key,item);return item;
    }
    draw(scene,meshes,view,width,height){
      const gl=this.gl;this.canvas.width=width;this.canvas.height=height;gl.viewport(0,0,width,height);gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);gl.enable(gl.DEPTH_TEST);gl.depthFunc(gl.LEQUAL);gl.disable(gl.CULL_FACE);gl.useProgram(this.program);gl.uniformMatrix4fv(this.camera,false,view.matrix);
      for(const part of scene.parts){const item=this.upload(part.key,meshes[part.key]),R=part.R,t=part.t;
        gl.bindBuffer(gl.ARRAY_BUFFER,item.buffer);gl.enableVertexAttribArray(this.position);gl.enableVertexAttribArray(this.normal);gl.vertexAttribPointer(this.position,3,gl.FLOAT,false,24,0);gl.vertexAttribPointer(this.normal,3,gl.FLOAT,false,24,12);
        gl.uniformMatrix4fv(this.model,false,new Float32Array([R[0],R[3],R[6],0,R[1],R[4],R[7],0,R[2],R[5],R[8],0,...t,1]));
        gl.uniform3fv(this.color,part.kind==='panel'?[.39,.48,.47]:part.kind==='side'?[.30,.37,.40]:part.kind==='foot'?[.24,.28,.32]:[.48,.53,.60]);gl.drawArrays(gl.TRIANGLES,0,item.count);
      }
      return this.canvas;
    }
  }
  const api={U,frame,bounds,camera,apply,load,Renderer,sources};if(typeof module!=='undefined'&&module.exports)module.exports=api;root.LabRaxScene=api;
})(typeof window==='undefined'?globalThis:window);
