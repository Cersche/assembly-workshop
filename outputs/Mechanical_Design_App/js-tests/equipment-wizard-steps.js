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
