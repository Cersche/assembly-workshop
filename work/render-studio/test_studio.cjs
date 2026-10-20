'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert');
const folder=path.resolve('outputs/Mechanical_Design_App/rack-references');
global.LabRaxScene=require(path.join(folder,'rack-scene.js'));
const S=require(path.join(folder,'rack-studio.js')),geometry=S.equipment();
const catalog=JSON.parse(fs.readFileSync(path.join(folder,'catalog.json'),'utf8')),meshes={};
for(const [key,[r,id]] of Object.entries(LabRaxScene.sources)){const c=catalog.references[r].components.find(c=>c.id===id);meshes[key]=JSON.parse(fs.readFileSync(path.join(folder,path.basename(c.url)),'utf8'));}
let projections=0;
for(const slots of [1,5,8,48])for(const panels of [false,true])for(const [yaw,pitch] of [[0,0],[-.48,.24],[1.3,1.1],[2.6,-.9]])for(const perspective of [false,true]){
  const scene=LabRaxScene.frame(slots,panels),box=LabRaxScene.bounds(scene,meshes),v=S.camera(box,yaw,pitch,800,550,1,perspective),m=v.matrix;
  for(const p of [box.lo,box.hi,box.lo.map((x,i)=>(x+box.hi[i])/2),[-118.2625,-3,(slots-1)*44.45+36.902]]){
    const screen=v.project(p),clip=[0,1,2,3].map(i=>m[i]*p[0]+m[i+4]*p[1]+m[i+8]*p[2]+m[i+12]);
    assert(screen.every(Number.isFinite));assert(Math.abs((clip[0]/clip[3]+1)*400-screen[0])<.015);assert(Math.abs((1-clip[1]/clip[3])*275-screen[1])<.015);
    const ray=v.ray(screen[0],screen[1]),delta=p.map((x,i)=>x-ray.origin[i]),distance=delta.reduce((s,x,i)=>s+x*ray.direction[i],0),error=Math.hypot(...delta.map((x,i)=>x-ray.direction[i]*distance));assert(error<.00001);projections++;
  }
}
for(const [name,m] of Object.entries(geometry)){
  assert(m.triangles.length>0,name);assert(m.vertices.flat().every(Number.isFinite));assert(m.normals.flat().every(Number.isFinite));
  assert(m.triangles.every(t=>t.every(i=>Number.isInteger(i)&&i>=0&&i<m.vertices.length)));
}
const extent=(mesh,axis)=>[Math.min(...mesh.vertices.map(v=>v[axis])),Math.max(...mesh.vertices.map(v=>v[axis]))];
assert.deepEqual(extent(geometry.tray,0),[-88,88]);assert.deepEqual(extent(geometry.tray,1),[0,140]);assert.deepEqual(extent(geometry.plate,0),[-125.5,125.5]);assert.deepEqual(extent(geometry.plate,1),[-3,0]);
assert(Math.abs(extent(geometry.plate,2)[1]-extent(geometry.plate,2)[0]-43.5)<1e-6);
function pick(mesh,origin,direction){return S.Renderer.prototype.pick.call({pickState:{view:{ray:()=>({origin,direction})},rack:{slots:5},objects:[{mesh,R:[1,0,0,0,1,0,0,0,1],t:[0,0,0],slot:5}]}},0,0);}
for(const x of [-118.2625,118.2625])for(const z of [5.098,36.902])assert.equal(pick(geometry.plate,[x,-100,z],[0,1,0]),null,'Mounting opening must be an actual hole');
assert.equal(pick(geometry.plate,[0,-100,20],[0,1,0]),5);
for(let x=-55;x<=55;x+=22)for(let y=25;y<=120;y+=22){if(x===33&&(y===25||y===91))continue;assert.equal(pick(geometry.tray,[x,y,100],[0,0,-1]),null,'Vent must be an actual through-hole');}
assert.equal(pick(geometry.tray,[-40,25,100],[0,0,-1]),5);
assert.deepEqual(S.artworkRect({x:.5,y:.5,scale:1},2),[0,21,68,34]);
assert(S.artworkRect(null).every(Number.isFinite));
const left=S.artworkRect({x:0,y:.5,scale:.5},2),right=S.artworkRect({x:1,y:.5,scale:.5},2);
assert.equal(left[0],-right[0]);assert(left[0]<0);assert.equal(left[2],34);
// The front upright must block an allocation behind it, while visible equipment selects.
const post=new S.Mesh(),surface=new S.Mesh();post.box(-5,5,0,10,0,40);surface.box(-20,20,15,20,0,40);
const fake={pickState:{view:{ray:()=>({origin:[0,-100,20],direction:[0,1,0]})},rack:{slots:5},objects:[{mesh:post,R:[1,0,0,0,1,0,0,0,1],t:[0,0,0]},{mesh:surface,R:[1,0,0,0,1,0,0,0,1],t:[0,0,0],slot:5}]}};
assert.equal(S.Renderer.prototype.pick.call(fake,0,0),5); // Empty slot plane is in front of the post.
fake.pickState.view.ray=()=>({origin:[0,12,20],direction:[0,-1,0]});
assert.equal(S.Renderer.prototype.pick.call(fake,0,0),null); // Looking from inside: post hides slot plane and equipment.
console.log(`PASS ${projections} camera/projection/ray comparisons, 1–48-slot stacks, finite meshes, specified extents, four mounting openings, 28 through-vents and surface picking.`);
