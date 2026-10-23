'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const P=require('../port-openings.js'),T=require('../tray-placement.js'),C=require('../cable-ports.js');
test('faceplate reference spacing, capacity and thin web',()=>{
 assert.deepEqual(P.faceplateSpacing(10,1,1).map(p=>p[0]),[-96.75,-75.25,-53.75,-32.25,-10.75,10.75,32.25,53.75,75.25,96.75]);
 assert.deepEqual(P.faceplateSpacing(1,1,1),[[0,22.225]]);
 assert.throws(()=>P.faceplateSpacing(11,1,1),/Maximum 10/);
 assert.throws(()=>P.faceplateSpacing(1,2,1));
 assert.deepEqual(P.faceplateCheck({layout:'keystones',count:10,rows:1,u:1}),{errors:[],warnings:['thin wall, fit/strength UNKNOWN']});
});
test('two rows have separate port pairs and no tray sketch',()=>{
 const raw={layout:'keystones',count:5,rows:2,u:2},tray={faceplate:raw},spec={faceplate_only:true};
 assert.deepEqual(P.faceplateCheck(raw),{errors:[],warnings:[]});
 const ports=C.wizardPorts(spec,tray);assert.equal(ports.length,20);
 assert.deepEqual([...new Set(ports.map(p=>p.z))],[22.225,66.675]);
 for(const p of ports)assert.equal(ports.find(q=>q.id===p.passThrough).passThrough,p.id);
 const parts=T.rackSketch(spec,tray);assert.deepEqual(Object.keys(parts).sort(),['faceplate','openings']);
});
test('blank and custom panels have no device or hidden cutouts',()=>{
 assert.deepEqual(Object.keys(T.rackSketch({faceplate_only:true},{faceplate:{u:3,layout:'blank'}})),['faceplate']);
 const raw={layout:'custom',u:2,ports:[{x:0,z:40,w:50,h:25,r:2}]};
 assert.deepEqual(P.faceplateCheck(raw),{errors:[],warnings:[]});
 assert.equal(C.wizardPorts({faceplate_only:true},{faceplate:raw})[0].z,40);
 assert.ok(P.faceplateCheck({...raw,ports:[{x:118,z:6.323,w:10,h:7}]}).errors.length);
 assert.ok(P.faceplateCheck({layout:'keystones',u:1,count:2,rows:1,keystones:[[0,22.225],[20,22.225]]}).errors.length);
});
