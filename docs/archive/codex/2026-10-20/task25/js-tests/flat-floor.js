'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const P=require('../port-openings.js'),T=require('../tray-placement.js'),C=require('../cable-ports.js');
const spec={dev_w:182.5,dev_d:194.5,dev_h:38.8,device_mount:'inserts',standoff:6,u:2,holes:[[3,3]],ports:[],rear_ports:[]};
test('height rule and auto-U use the actual floor and only real standoffs',()=>{
  for(const [device_mount,lift] of [['inserts',16],['pegs',16],['clips',16],['straps',10],['flat',3.5]]){
    const s={...spec,device_mount,dev_h:44.45-lift};
    assert.equal(P.deviceLift(s),lift);assert.equal(P.autoU(s),1);
    assert.equal(P.autoU({...s,dev_h:s.dev_h+0.001}),2);
  }
  assert.equal(P.autoU(spec),2);assert.equal(P.autoU({...spec,device_mount:'flat'}),1);
  assert.match(P.flatHint(spec),/Fits 1U.*42.3 mm needed \/ 44.45 mm available/);
  assert.equal(P.flatHint({...spec,device_mount:'flat'}),'');
  assert.equal(P.flatHint({...spec,dev_h:10}),'');
});
test('wizard import actually uses shared auto-U and shows the flat hint without changing mount',()=>{
  const src=fs.readFileSync(path.join(__dirname,'../equipment-wizard.js'),'utf8');
  const apply=src.slice(src.indexOf('  function applyImport(){'),src.indexOf('  function topView(){'));
  const box={spec:{...spec},window:{LabRaxPortOpenings:P},transformed:()=>[0,0,0,182.5,194.5,38.8],findHoles:()=>[],findPorts:()=>[]};
  vm.runInNewContext(apply+';applyImport();',box);
  assert.equal(box.spec.u,2);assert.equal(box.spec.device_mount,'inserts');
  box.spec.device_mount='flat';vm.runInNewContext('applyImport()',box);assert.equal(box.spec.u,1);
  assert.match(src,/const hint=window.LabRaxPortOpenings.flatHint\(spec\);if\(hint\)imp.push/);
});
test('flat placement fits 1U, sketch floor and device agree, joints remain guarded',()=>{
  const s={...spec,holes:[]},v=T.values(s,{device_mount:'flat',u:1});
  assert.deepEqual(T.problems(s,v),[]);
  assert.equal(T.layout(s,v).lift,3.5);
  const sets=T.schematic(s,v),zs=a=>a.filter((_,i)=>i%3===2);
  assert.equal(Math.min(...zs(sets[1].v)),0.5);
  assert.equal(Math.min(...zs(sets[2].v)),3.5);
  assert.ok(T.problems(s,{...v,device_mount:'inserts'}).some(x=>x.includes('taller')));
  assert.ok(T.problems(s,{...v,dev_off_y:-1}).some(x=>x.includes('front screw joint')));
  assert.ok(T.problems(s,{...v,joint:'single',dev_off_y:-6}).some(x=>x.includes('corner stops')));
  assert.deepEqual(T.problems(s,{...v,joint:'single',dev_off_y:-5.8}),[]);
});
test('front, rear and custom cable ports track the lower floor and preserve library input',()=>{
  const s={...spec,ports:[{id:'front-1',x:0,z:22,w:8,h:6,r:1}],
    rear_ports:[{id:'rear-1',x:0,z:22}],planning_ports:[{id:'custom',x:0,y:30,z:22,points:'front'}]};
  const tray={device_mount:'flat',standoff:30,u:1};
  assert.equal(P.frontOpenings(s,tray).ports[0].z,9.5);
  const ports=C.wizardPorts(s,tray);
  for(const id of ['front-1','rear-1','custom'])assert.equal(ports.find(p=>p.id===id).z,9.5);
  assert.equal(s.ports[0].z,22);
  assert.equal(P.frontOpenings(s,{...tray,dev_rot:90}).ports[0].z,22);
});
