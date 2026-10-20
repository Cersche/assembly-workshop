'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert');
global.LabRaxScene=require(path.resolve('outputs/Mechanical_Design_App/rack-references/rack-scene.js'));
global.LabRaxStudio=require(path.resolve('outputs/Mechanical_Design_App/rack-references/rack-studio.js'));
const A=require(path.resolve('outputs/Mechanical_Design_App/rack-references/assembly-studio.js'));
const model=JSON.parse(fs.readFileSync('outputs/Mechanical_Design_App/assembly.json','utf8')),copy=JSON.stringify(model);
const objects=model.parts.map(mesh=>({mesh,box:A.bounds([mesh]),partId:mesh.id}));
assert.equal(A.hitTest(objects,{origin:[-80,-100,21],direction:[0,1,0]}),'faceplate');
assert.equal(A.hitTest(objects,{origin:[0,45,100],direction:[0,0,-1]}),'tray');
assert.equal(A.hitTest(objects,{origin:[300,-100,21],direction:[0,1,0]}),null);
const box=A.bounds(model.parts);for(const mode of [true,false]){const raw=LabRaxStudio.camera(box,-.55,.65,800,420,1,mode),view=A.fitInspectionView(raw,raw,model.parts,800,420),m=view.matrix;for(const p of [box.lo,box.hi,[0,0,21]]){
  const screen=view.project(p),clip=[0,1,2,3].map(i=>m[i]*p[0]+m[i+4]*p[1]+m[i+8]*p[2]+m[i+12]);assert(screen.every(Number.isFinite));assert(Math.abs((clip[0]/clip[3]+1)*400-screen[0])<.001);assert(Math.abs((1-clip[1]/clip[3])*210-screen[1])<.001);
}}
assert.equal(JSON.stringify(model),copy);
console.log('PASS exact-mesh bounds, frontmost faceplate/tray picking, background clearing, both camera modes and unchanged source data.');
