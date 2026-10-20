// Studio rendering of the exact inspection meshes. No geometry generation/export.
(function(root){
  'use strict';
  const I=[1,0,0,0,1,0,0,0,1],S=root.LabRaxStudio;
  const sub=(a,b)=>a.map((v,i)=>v-b[i]),dot=(a,b)=>a.reduce((sum,v,i)=>sum+v*b[i],0);
  const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
  function bounds(meshes){const lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];for(const m of meshes)for(const p of m.vertices)for(let i=0;i<3;i++){lo[i]=Math.min(lo[i],p[i]);hi[i]=Math.max(hi[i],p[i]);}return {lo,hi};}
  function color(hex,fallback){return /^#[0-9a-f]{6}$/i.test(hex||'')?[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255):fallback;}
  function fitInspectionView(view,baseView,parts,width,height){
    // Frame the real mesh silhouette rather than the empty corners of its 3D box.
    let left=Infinity,right=-Infinity,top=Infinity,bottom=-Infinity;
    for(const part of parts)for(const p of part.vertices){const q=baseView.project(p);left=Math.min(left,q[0]);right=Math.max(right,q[0]);top=Math.min(top,q[1]);bottom=Math.max(bottom,q[1]);}
    const cx=(left+right)/2,cy=(top+bottom)/2,factor=Math.min(width*.88/Math.max(right-left,1),(height-60)*.88/Math.max(bottom-top,1));
    const nx=2*cx/width-1,ny=1-2*cy/height,m=new Float32Array(view.matrix),old=view.matrix,project=view.project,ray=view.ray;
    for(let i=0;i<4;i++){m[i*4]=(old[i*4]-nx*old[i*4+3])*factor;m[i*4+1]=(old[i*4+1]-ny*old[i*4+3])*factor;}
    return {...view,matrix:m,project:p=>{const q=project(p);return [width/2+(q[0]-cx)*factor,height/2+(q[1]-cy)*factor,q[2]];},ray:(x,y)=>ray(cx+(x-width/2)/factor,cy+(y-height/2)/factor)};
  }
  function hitTest(objects,ray){
    let best=Infinity,hit=null;
    for(const object of objects){
      const box=object.box;let near=0,far=best;
      for(let i=0;i<3;i++){if(Math.abs(ray.direction[i])<1e-10){if(ray.origin[i]<box.lo[i]||ray.origin[i]>box.hi[i])far=-1;}else{const a=(box.lo[i]-ray.origin[i])/ray.direction[i],b=(box.hi[i]-ray.origin[i])/ray.direction[i];near=Math.max(near,Math.min(a,b));far=Math.min(far,Math.max(a,b));}}
      if(far<near)continue;
      for(const ids of object.mesh.triangles){const [a,b,c]=ids.map(i=>object.mesh.vertices[i]),e1=sub(b,a),e2=sub(c,a),p=cross(ray.direction,e2),det=dot(e1,p);if(Math.abs(det)<1e-9)continue;const s=sub(ray.origin,a),u=dot(s,p)/det;if(u<0||u>1)continue;const q=cross(s,e1),v=dot(ray.direction,q)/det;if(v<0||u+v>1)continue;const d=dot(e2,q)/det;if(d>0&&d<best){best=d;hit=object;}}
    }
    return hit?.partId||null;
  }
  class AssemblyRenderer extends S.Renderer{
    constructor(){super();this.meshKeys=new WeakMap();this.meshBoxes=new WeakMap();this.sequence=0;this.modelParts=null;this.currentObjects=[];}
    key(mesh){if(!this.meshKeys.has(mesh))this.meshKeys.set(mesh,'assembly-'+(++this.sequence));return this.meshKeys.get(mesh);}
    box(mesh){if(!this.meshBoxes.has(mesh))this.meshBoxes.set(mesh,bounds([mesh]));return this.meshBoxes.get(mesh);}
    objects(){return this.currentObjects.slice();}
    render({parts,fullParts,yaw,pitch,zoom,focus,frontMode,appearance,selectedPart,width,height,dpr}){
      if(this.modelParts!==fullParts){
        for(const [key,item] of this.buffers)if(key.startsWith('assembly-')||key==='studio-floor'){this.gl.deleteBuffer(item.buffer);this.buffers.delete(key);}
        this.modelParts=fullParts;this.fullBox=bounds(fullParts);this.shadowKey='';this.depthKey='';
        const z=this.fullBox.lo[2]-.65,floor=new S.Mesh();floor.box(-900,900,-700,900,z-1,z);this.geometry.floor=floor;
        const span=Math.max(this.fullBox.hi[0]-this.fullBox.lo[0],this.fullBox.hi[1]-this.fullBox.lo[1],1);this.floorParams=[(this.fullBox.lo[0]+this.fullBox.hi[0])/2,(this.fullBox.lo[1]+this.fullBox.hi[1])/2,span*.2,span*.75];
      }
      const scene={slots:0,parts:fullParts.map(mesh=>({key:this.key(mesh),R:I,t:[0,0,0]}))},meshes={};for(const mesh of fullParts)meshes[this.key(mesh)]=mesh;
      this.currentObjects=parts.map(mesh=>{
        const id=mesh.id,box=this.box(mesh),brass=id==='insert',steel=id==='screw'||id==='screw_head',plane=id==='tray'?1:0;
        const rgb=id==='tray'?color(appearance.tray,[77/255,142/255,110/255]):id==='faceplate'?color(appearance.faceplate,[78/255,117/255,163/255]):id==='pi_reference'?color(appearance.equipment,[91/255,133/255,69/255]):brass?[.78,.60,.27]:[.19,.21,.25];
        const other=plane?1:2;
        return {key:this.key(mesh),mesh,box,partId:id,R:I,t:[0,0,0],kind:id,color:rgb,metal:brass?.82:steel?.72:0,rough:brass?.28:steel?.3:.43,selected:id===selectedPart,art:id==='faceplate'?appearance.artwork:null,selectionRect:[(box.lo[0]+box.hi[0])/2,(box.lo[other]+box.hi[other])/2,(box.hi[0]-box.lo[0])/2,(box.hi[other]-box.lo[other])/2],selectionRadius:0,selectionPlane:plane};
      });
      const active=new Set([...scene.parts.map(p=>p.key),...this.currentObjects.map(p=>p.key)]);
      for(const [key,item] of this.buffers)if(key.startsWith('assembly-')&&!active.has(key)){this.gl.deleteBuffer(item.buffer);this.buffers.delete(key);}
      let box=this.fullBox;
      if(focus[0]===40){const half=box.lo.map((v,i)=>(box.hi[i]-v)/2);box={lo:focus.map((v,i)=>v-half[i]),hi:focus.map((v,i)=>v+half[i])};}
      let view=S.camera(box,frontMode?0:yaw,frontMode?0:pitch,width,height,zoom,!frontMode);
      if(focus[0]!==40)view=fitInspectionView(view,S.camera(box,frontMode?0:yaw,frontMode?0:pitch,width,height,1,!frontMode),fullParts,width,height);
      // The key records visibility too, so hidden parts stop casting shadows immediately.
      const cacheState={placements:[{id:this.currentObjects.map(o=>o.key).join(','),slot:0}]};
      const canvas=super.draw(scene,meshes,view,Math.round(width*dpr),Math.round(height*dpr),cacheState);
      this.view=view;
      return {canvas,view,triangles:parts.reduce((sum,p)=>sum+p.triangles.length,0)};
    }
    pickPart(x,y){return this.view?hitTest(this.currentObjects,this.view.ray(x,y)):null;}
  }
  root.LabRaxAssembly={AssemblyRenderer,bounds,hitTest,fitInspectionView};
  if(typeof module!=='undefined'&&module.exports)module.exports=root.LabRaxAssembly;
})(typeof window==='undefined'?globalThis:window);
