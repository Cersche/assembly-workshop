'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {findFeet}=require('../equipment-wizard.js');
const PO=require('../port-openings.js'),TP=require('../tray-placement.js');
function cube(x0,y0,z0,x1,y1,z1){const p=[[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]],faces=[[0,2,1,0,3,2],[4,5,6,4,6,7],[0,1,5,0,5,4],[1,2,6,1,6,5],[2,3,7,2,7,6],[3,0,4,3,4,7]],v=[];for(const f of faces)for(const i of f)v.push(...p[i]);return v;}
function scene(feet=true){let v=cube(0,0,0,20,20,10);if(feet)for(const [x,y]of[[1,2],[14,3],[4,14],[13,13]])v.push(...cube(x,y,-2,x+4,y+4,0));return v;}
const bounds=v=>{const mn=[Infinity,Infinity,Infinity],mx=[-Infinity,-Infinity,-Infinity];for(let i=0;i<v.length;i++){const a=i%3;mn[a]=Math.min(mn[a],v[i]);mx[a]=Math.max(mx[a],v[i]);}return[mn,mx];};
test('detects four lower feet on separate overlapping bodies and ignores a plain case',()=>{
  const v=scene(),[mn,mx]=bounds(v),feet=findFeet(v,mn,mx);assert.equal(feet.length,4);assert.deepEqual(feet.map(f=>[f.x,f.y,f.w,f.d,f.h]),[[1,2,4,4,2],[14,3,4,4,2],[13,13,4,4,2],[4,14,4,4,2]]);
  const plain=scene(false),[a,b]=bounds(plain);assert.deepEqual(findFeet(plain,a,b),[]);
});
test('orientation and quarter-turn transform foot locations in the device frame',()=>{
  let v=scene(),[mn,mx]=bounds(v);let feet=findFeet(v,mn,mx);assert.deepEqual(feet[0],{x:1,y:2,w:4,d:4,h:2,keep:true});
  const src=scene(),turned=[];for(let i=0;i<src.length;i+=3)turned.push(-src[i+1],src[i],src[i+2]);[mn,mx]=bounds(turned);feet=findFeet(turned,mn,mx);assert.equal(feet.length,4);assert.deepEqual(feet.map(f=>[f.x,f.y]),[[14,1],[2,4],[3,13],[13,14]]);
});
test('50,000 triangle import stays responsive',()=>{
  const base=scene(),v=[];while(v.length/9<50000){const take=Math.min(base.length,50000*9-v.length);v.push(...base.slice(0,take));}const [mn,mx]=bounds(v),start=performance.now(),feet=findFeet(v,mn,mx),elapsed=performance.now()-start;
  assert.equal(feet.length,4);assert.ok(elapsed<10000,`50k triangles took ${elapsed.toFixed(0)} ms`);console.log(`feet detector: 50,000 triangles in ${elapsed.toFixed(1)} ms`);
});
test('flat and sleeve use case height, rotated pockets and unchanged legacy specs',()=>{
  const feet=[{x:20,y:14.5,w:5.5,d:76.5,h:2},{x:169,y:14.5,w:5.5,d:76.5,h:2}],spec={dev_w:194.5,dev_d:182.5,dev_h:38.8,feet,device_mount:'sleeve',dev_rot:90,u:1,joint:'screw',holes:[],ports:[],keystones:[]};
  const win=PO.sleeve(spec);assert.deepEqual([win.bottom,+win.top.toFixed(6),+win.height.toFixed(6),win.lip],[3.5,40.6,37.1,3]);assert.ok(Math.abs(PO.neededHeight(spec)-40.3)<1e-9);  // case rests on the floor top
  assert.equal(TP.footPockets(spec,TP.values(spec))[0].through,true);
  assert.equal(TP.footPockets(spec,TP.values(spec))[0].x0,-0.25);
  assert.match(TP.warnings(spec,TP.values(spec)).join(' '),/pass through the floor/);
  const noFeet={...spec,feet:[]};assert.equal(PO.neededHeight(noFeet),42.3);assert.ok(Math.abs(PO.sleeve(noFeet).top-42.6)<1e-9);assert.equal(PO.sleeve(noFeet).lip,1.5);
});
test('pockets colliding with joints or straps block placement',()=>{
  const base={dev_w:100,dev_d:100,dev_h:20,device_mount:'flat',joint:'screw',holes:[],ports:[],keystones:[],u:1};
  const strap={...base,feet:[{x:-4,y:25,w:5,d:5,h:1}]};assert.match(TP.problems(strap,TP.values(strap)).join(' '),/strap slot/);
  const sleeve={...base,device_mount:'sleeve',feet:[{x:8,y:5,w:2,d:4,h:1}]};assert.match(TP.problems(sleeve,TP.values(sleeve)).join(' '),/screw joint/);
});
