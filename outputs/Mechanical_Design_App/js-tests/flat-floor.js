'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const P=require('../port-openings.js'),T=require('../tray-placement.js'),C=require('../cable-ports.js');
const spec={dev_w:182.5,dev_d:194.5,dev_h:38.8,device_mount:'inserts',standoff:6,u:2,holes:[[3,3]],ports:[],rear_ports:[]};
test('height rule and auto-U use the actual floor and only real standoffs',()=>{
  for(const [device_mount,lift] of [['inserts',17.225],['pegs',17.225],['clips',17.225],['straps',11.225],['flat',3.5]]){
    const s={...spec,device_mount,dev_h:44.45-lift};
    assert.ok(Math.abs(P.deviceLift(s)-lift)<1e-9);assert.equal(P.autoU(s),1);
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
  const box={spec:{...spec},window:{LabRaxPortOpenings:P},transformed:()=>[0,0,0,182.5,194.5,38.8],findHoles:()=>[],findPorts:()=>[],findProtrusions:()=>({items:[]}),syncImportFrame:()=>{}};
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
  assert.equal(P.frontOpenings(s,tray).ports[0].z,8.275);
  const ports=C.wizardPorts(s,tray);
  for(const id of ['front-1','rear-1','custom'])assert.ok(Math.abs(ports.find(p=>p.id===id).z-8.275)<1e-9);
  assert.equal(s.ports[0].z,22);
  assert.equal(P.frontOpenings(s,{...tray,dev_rot:90}).ports[0].z,22);
});

test('slot-bottom standard: 1U/2U bounds, rack holes, preserved non-flat rack heights',()=>{
  for(const [u,top] of [[1,44.425],[2,88.875]]){
    const v=T.values(spec,{u,device_mount:'flat'}),verts=T.rackSketch(spec,v).faceplate;
    const zs=verts.filter((_,i)=>i%3===2),xs=verts.filter((_,i)=>i%3===0);
    assert.ok(Math.abs(Math.min(...zs)-0.025)<1e-9);
    assert.ok(Math.abs(Math.max(...zs)-top)<1e-9);
    assert.equal(Math.min(...xs),-126);assert.equal(Math.max(...xs),126);
  }
  assert.ok(Math.abs(P.RACK_PITCH/2-15.902-6.323)<1e-9);
  assert.ok(Math.abs(P.RACK_PITCH/2+15.902-38.127)<1e-9);
  for(const mount of ['inserts','pegs','clips','straps']){
    assert.equal(P.floorZ({device_mount:mount}),7+1.225);
    const oldLift=mount==='straps'?10:16;
    assert.ok(Math.abs(P.deviceLift({device_mount:mount})-(oldLift+1.225))<1e-9);
    assert.ok(T.problems({...spec,dev_h:44.45-oldLift},T.values(spec,{device_mount:mount,u:1})).some(x=>x.includes('taller')));
  }
  const scad=fs.readFileSync(path.join(__dirname,'../equipment_tray.scad'),'utf8');
  assert.match(scad,/plate_center=u\*rack_pitch\/2/);
  assert.ok(scad.includes('plate_center+sz*(plate_h/2-plate_r)'));
  assert.ok(scad.includes('i*rack_pitch+rack_pitch/2+dz'));
});

test('sleeve sketch contains a real window and walls/lips/stop in the shared coordinate frame',()=>{
  const s={...spec,device_mount:'sleeve',u:1,holes:[]},v=T.values(s),w=P.sleeve(s);
  assert.deepEqual(T.problems(s,v),[]);assert.equal(T.layout(s,v).dev_y,-4);
  assert.equal(T.layout(s,v).tray_w,198.5);assert.equal(w.lip,1.5);
  assert.deepEqual(T.joints(s,v).joints,[-94.75,94.75]);
  const mesh=T.rackSketch(s),zs=mesh.tray.filter((_,i)=>i%3===2);
  assert.ok(Math.abs(Math.max(...zs)-44.1)<1e-9);
  // Four rectangular plate bands: no front triangle covers the centre of the window.
  const front=[];for(let i=0;i<mesh.faceplate.length;i+=9){const q=mesh.faceplate.slice(i,i+9);if([q[1],q[4],q[7]].every(y=>y===-4))front.push(q);}
  for(const q of front){const xs=[q[0],q[3],q[6]],zs=[q[2],q[5],q[8]];
    assert.ok(Math.max(...xs)<=-w.half||Math.min(...xs)>=w.half||Math.max(...zs)<=w.bottom||Math.min(...zs)>=w.top);}
  const ported={...s,ports:[{x:0,z:20,w:17,h:14,r:1}]};
  assert.ok(T.warnings(ported,T.values(ported)).some(x=>x.includes('omitted')));
  assert.equal(T.rackSketch(ported).openings,undefined);
  const rear=C.wizardPorts({...s,rear_ports:[{id:'rear',x:0,z:20}]}).find(p=>p.id==='rear');
  assert.equal(rear.y,190.5);
});
