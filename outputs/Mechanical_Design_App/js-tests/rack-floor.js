// Preview only; source meshes read in place, no user data or geometry builds.
'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const S=require('../rack-studio.js'),scene=require('../rack-references/rack-scene.js');
const I=[1,0,0,0,1,0,0,0,1];
function meshes(){return Object.fromEntries(Object.entries(scene.sources).map(([key,[ref,id]])=>[key,JSON.parse(fs.readFileSync(path.join(__dirname,'../rack-references',`component_${ref}_${id}.json`),'utf8'))]));}
function objects(frame,ms){return frame.parts.map(p=>({...p,mesh:ms[p.key]}));}
test('rack floor helper follows the lowest finite part bound and falls back for no parts',()=>{
  assert.equal(S.floorTop([]),-42);
  assert.equal(S.floorTop([{lo:[0,0,Infinity]}]),-42);
  assert.equal(S.floorTop([{lo:[0,0,-47]},{lo:[0,0,0]}]),-47.65);
  assert.equal(S.floorTop([{lo:[0,0,12]}]),11.35);
  assert.equal(S.floorTop([{lo:[0,0,0]}]),-.65);
});
test('world bounds follow rotations and translations, ignore empty meshes and unused vertices',()=>{
  const mesh=new S.Mesh();mesh.tri([1,2,3],[4,5,6],[-2,0,1]);mesh.vertices.push([0,0,-999]);
  const cache=new WeakMap(),o={mesh,R:I,t:[0,0,10]};
  assert.deepEqual(S.partBounds([o],cache),[{lo:[-2,0,11],hi:[4,5,16]}]);
  o.t=[0,0,-10];assert.equal(S.floorTop(S.partBounds([o],cache)),-9.65);
  o.R=[1,0,0,0,0,-1,0,1,0];assert.deepEqual(S.partBounds([o],cache),[{lo:[-2,-6,-10],hi:[4,-1,-5]}]);
  assert.deepEqual(S.partBounds([{mesh:new S.Mesh(),R:I,t:[0,0,-100]}]),[]);
});
test('real rack feet never fall below the floor at several heights, with panels and without feet',()=>{
  const ms=meshes();
  for(const slots of [1,5,9,14])for(const panels of [false,true]){
    const frame=scene.frame(slots,panels),before=JSON.stringify(frame),drawn=objects(frame,ms),z=S.floorTop(S.partBounds(drawn));
    assert.equal(z,-47.65);
    for(const o of drawn.filter(o=>o.kind==='foot'))for(const v of o.mesh.vertices){const world=scene.apply(o.R,o.t,v);assert.ok(world[2]>=z);}
    assert.equal(S.floorTop(S.partBounds(drawn.filter(o=>o.kind!=='foot'))),-35.6500031);
    assert.equal(JSON.stringify(frame),before,'floor calculation must not move parts');
  }
});
test('renderer updates floor placement and depth/shadow caches as feet and scene height change',()=>{
  globalThis.LabRaxScene=scene;
  const ms=meshes(),r=Object.create(S.Renderer.prototype),floor=new S.Mesh();floor.box(-900,900,-700,900,-1,0);
  Object.assign(r,{canvas:{width:800,height:600},geometry:{floor},boundsCache:new WeakMap(),shadows:true,ambientOcclusion:true,program:{},depthProgram:{}});
  r.gl=new Proxy({},{get:(_,name)=>typeof name==='string'&&/^[A-Z_]+$/.test(name)?0:()=>{}});
  let current=[],submitted=[];r.objects=()=>current;r.loc=()=>0;r.sceneDepthTarget=()=>({ready:true,width:800,height:600});r.submit=(p,os)=>submitted.push({p,os:os.slice()});
  const frame=scene.frame(5),view=S.camera(scene.bounds(frame,ms),.4,.1,800,600),rack={placements:[]};
  function draw(f,feet){current=objects(f,ms).filter(o=>feet||o.kind!=='foot');submitted=[];r.draw(f,ms,view,800,600,rack);return submitted.findLast(s=>s.p===r.program).os.find(o=>o.kind==='floor');}
  assert.equal(draw(frame,true).t[2],-47.65);const key=r.shadowKey,depth=r.depthKey;
  assert.equal(draw(frame,false).t[2],-35.6500031);assert.notEqual(r.shadowKey,key);assert.notEqual(r.depthKey,depth);
  assert.equal(draw(scene.frame(9),true).t[2],-47.65);
  current=[];submitted=[];r.draw({slots:0,parts:[]},ms,view,800,600,rack);
  const fallback=submitted.findLast(s=>s.p===r.program).os.find(o=>o.kind==='floor');assert.equal(fallback.t[2],-42);
  assert.deepEqual([Math.min(...floor.vertices.map(v=>v[0])),Math.max(...floor.vertices.map(v=>v[0])),Math.min(...floor.vertices.map(v=>v[1])),Math.max(...floor.vertices.map(v=>v[1]))],[-900,900,-700,900]);
});
