const fs=require('fs'),path=require('path'),assert=require('assert');
const folder=path.resolve('outputs/Mechanical_Design_App/rack-references');
const S=require(path.join(folder,'rack-scene.js')),catalog=JSON.parse(fs.readFileSync(path.join(folder,'catalog.json'),'utf8'));
const meshes={};for(const [key,[r,id]] of Object.entries(S.sources)){const component=catalog.references[r].components.find(c=>c.id===id);meshes[key]=JSON.parse(fs.readFileSync(path.join(folder,path.basename(component.url)),'utf8'));}
for(const slots of [1,3,5,6,8,9,48])for(const panels of [false,true]){
 const scene=S.frame(slots,panels),bounds=S.bounds(scene,meshes);
 assert.equal(scene.manufacturing,false);assert.equal(scene.levels.reduce((a,b)=>a+b,0),slots);
 assert(scene.parts.every(p=>p.source&&meshes[p.key]));assert.equal(scene.parts.filter(p=>p.key.startsWith('post')).length,4*scene.levels.length);
 // Source meshes are instanced by rigid rotations only, never scaled to rack dimensions.
 for(const p of scene.parts){for(let row=0;row<3;row++)for(let col=0;col<3;col++){let dot=0;for(let k=0;k<3;k++)dot+=p.R[row*3+k]*p.R[col*3+k];assert.equal(dot,row===col?1:0);}}
 for(const [yaw,pitch] of [[-.48,.24],[0,0],[1.1,.8]]){
  const camera=S.camera(bounds,yaw,pitch,800,550);for(const part of scene.parts)for(const v of meshes[part.key].vertices){const p=S.apply(part.R,part.t,v),screen=camera.project(p);assert(screen.every(Number.isFinite));assert(screen[0]>=0&&screen[0]<=800);assert(screen[1]>=0&&screen[1]<=550);
   const m=camera.matrix,clip=[m[0]*p[0]+m[4]*p[1]+m[8]*p[2]+m[12],m[1]*p[0]+m[5]*p[1]+m[9]*p[2]+m[13]];assert(Math.abs((clip[0]+1)*400-screen[0])<.001);assert(Math.abs((1-clip[1])*275-screen[1])<.001);
  }
 }
}
const five=S.frame(5);assert.equal(five.parts.length,20);assert.equal(S.frame(5,true).parts.length,22);
for(const invalid of [0,49,2.5,NaN])assert.throws(()=>S.frame(invalid));
console.log('PASS rigid source instances, 1–48-slot stacks, no export capability, camera/overlay alignment and complete framing.');
