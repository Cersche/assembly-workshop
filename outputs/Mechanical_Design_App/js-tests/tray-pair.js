'use strict';
// Two devices on one tray (Brian, 2026-10-20): pair checks, rack sketch, cable ports, screening and window wiring.
// In-memory fixtures only. No server, user data, rendering or export.
const test=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const APP=path.resolve(__dirname,'..');
require(path.join(APP,'port-openings.js'));
const T=require(path.join(APP,'tray-placement.js')),P=require(path.join(APP,'tray-pair.js'));
const C=require(path.join(APP,'cable-ports.js')),S=require(path.join(APP,'clearance.js'));
const read=f=>fs.readFileSync(path.join(APP,f),'utf8');
const A={name:'Router',dev_w:80,dev_d:60,dev_h:20,device_mount:'inserts',joint:'screw',holes:[[5,5],[75,55]],standoff:6,u:1,
  ports:[{id:'lan',label:'LAN',x:0,z:20,w:16,h:14}],rear_ports:[{id:'pwr',label:'Power',x:0,z:15}]};
const B={name:'Switch',dev_w:70,dev_d:50,dev_h:25,device_mount:'straps',joint:'screw',u:1,ports:[{id:'usb',label:'USB',x:0,z:20,w:14,h:8}]};
const LIB=[{id:'eq-0000000000a1',name:'Router',spec:A},{id:'eq-0000000000b2',name:'Switch',spec:B}];

test('second-device values and diff keep only its own keys',()=>{
  const v2=P.values(B,{dev_off_x:50,u:3});
  assert.deepEqual(Object.keys(v2).sort(),[...P.SECOND_KEYS].sort());
  assert.equal(v2.device_mount,'straps');
  assert.deepEqual(P.diff(B,{...v2}),{dev_off_x:50});
});
test('pair layout spans both devices and stays centred',()=>{
  const L=P.layout(A,T.values(A,{dev_off_x:-45}),B,P.values(B,{dev_off_x:50}));
  assert.equal(L.tray_w,186);assert.equal(L.second.dev_x,15);
  assert.deepEqual(P.problems(A,T.values(A,{dev_off_x:-45}),B,P.values(B,{dev_off_x:50})),[]);
  assert.match(P.problems(A,T.values(A,{}),B,P.values(B,{})).join(' '),/overlapping; they need at least 5\.5 mm/);
});
test('rack sketch draws the wider tray and both devices’ openings',()=>{
  const one=T.rackSketch(A,{}),two=T.rackSketch(A,{dev_off_x:-45},{spec:B,tray:{dev_off_x:50}});
  const xs=v=>v.filter((_,i)=>i%3===0);
  assert.equal(Math.max(...xs(two.tray)),93);assert.ok(Math.max(...xs(one.tray))<93);
  assert.equal(two.openings.length,one.openings.length*2);
});
test('cable planner lists the second device’s ports with d2- ids and its name',()=>{
  const placement={id:'a',slot:1,span:1,equipment:LIB[0].id,tray:{dev_off_x:-45},second:{equipment:LIB[1].id,tray:{dev_off_x:50}}};
  const ports=C.basePorts(placement,LIB[0],LIB);
  const two=ports.find(p=>p.id==='d2-usb');
  assert.ok(two);assert.equal(two.label,'Switch · USB');assert.equal(two.x,50);
  assert.ok(ports.find(p=>p.id==='lan'));
  assert.equal(C.basePorts({...placement,second:undefined},LIB[0],LIB).length,ports.length-1);
});
test('screening uses the shared tray width',()=>{
  globalThis.equipmentLibraryItems=()=>LIB;
  try{
    const rack={width_mm:190,depth_mm:240,pitch_mm:44.45};
    const placement={slot:1,span:1,equipment:LIB[0].id,tray:{dev_off_x:-45},second:{equipment:LIB[1].id,tray:{dev_off_x:50}}};
    const width=S.screen(rack,placement,LIB[0]).checks.find(c=>c.name==='width');
    assert.equal(width.needed,186);
  }finally{delete globalThis.equipmentLibraryItems;}
});
test('window, workspace and rack view are wired for a second device',()=>{
  const tp=read('tray-placement.js'),ws=read('workspace.js'),wiz=read('equipment-wizard.js');
  assert.match(tp,/class:'tp-tabs',role:'tablist'/);
  assert.match(tp,/\+ Add a second device…/);
  assert.match(tp,/r\.second=s2/);
  assert.match(ws,/applyTrayPlacement=function\(rackId,placementId,tray,newSpan,second\)/);
  assert.match(ws,/if\(second\)placement\.second=second;else delete placement\.second;/);
  assert.match(wiz,/second:\{item:a\.second\.equipment,tray:a\.second\.tray\}/);
});
