'use strict';
// Library wizard is Device -> Holes -> Ports (equipment facts). Tray choices moved to the Place on tray window
// (tray-placement.js); new items keep the template defaults so they place and build as before. Static source checks only.
const test=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path');
const src=fs.readFileSync(path.join(__dirname,'..','equipment-wizard.js'),'utf8');
test('wizard has three fact steps',()=>{assert.ok(src.includes("STEPS=['Device','Holes','Ports']"));});
test('tray choices keep their defaults but are no longer edited in the wizard',()=>{
  for(const k of ["standoff:6","insert_pilot:3.2","board_t:1.6","device_mount:'inserts'","joint:'screw'","u:1","keystones:[]"])assert.ok(src.includes(k),k);
  for(const k of ['function trayChoices','function keystoneBar','Tray choices (temporary'])assert.ok(!src.includes(k),k);
  assert.ok(src.includes('Place on tray window'));
});
test('save, preview and build buttons remain on the last step',()=>{
  const fin=src.slice(src.indexOf('function finish'));
  for(const k of ['/api/equipment-build','/api/equipment-library','Show 3D preview'])assert.ok(fin.includes(k),k);
});
test('last-step summary counts front openings and rear ports separately',()=>{
  const a=src.indexOf('  const count=(n,one'),b=src.indexOf('  function body(){');assert.ok(a>=0&&b>a);
  const summary=new Function('MOUNTS','JOINTS',src.slice(a,b)+';return summary;')({inserts:'Heat-set inserts + screws'},{screw:'Screw joint'});
  const spec={name:'Box',dev_w:120,dev_d:80,dev_h:25,u:1,device_mount:'inserts',joint:'screw',holes:[[1,1],[2,2]],ports:[{}],rear_ports:[{}],keystones:[]};
  assert.equal(summary(spec),'Box: 120 × 80 × 25 mm, 2 holes, 1 front opening, 1 rear port. Tray defaults for new slots: 1U, Heat-set inserts + screws, Screw joint, 0 keystones.');
  assert.ok(summary({...spec,rear_ports:undefined}).includes('0 rear ports'));
});
test('last-step summary counts feet and leaves them out when there are none',()=>{
  const a=src.indexOf('  const count=(n,one'),b=src.indexOf('  function body(){');
  const summary=new Function('MOUNTS','JOINTS',src.slice(a,b)+';return summary;')({inserts:'Heat-set inserts + screws'},{screw:'Screw joint'});
  const spec={name:'Box',dev_w:120,dev_d:80,dev_h:25,u:1,device_mount:'inserts',joint:'screw',holes:[],ports:[],rear_ports:[],keystones:[]};
  const f={x:0,y:0,w:2,d:2,h:1};
  assert.ok(summary({...spec,feet:[f,f,f,f]}).includes('0 holes, 4 feet, 0 front openings'));
  assert.ok(summary({...spec,feet:[f]}).includes('0 holes, 1 foot, 0 front openings'));
  assert.ok(!/feet|foot/.test(summary({...spec,feet:[]})));
  assert.ok(!/feet|foot/.test(summary(spec)));
});
