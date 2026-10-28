// Analytical only: no render, server, user data or export.
'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const T=require('../tray-placement.js');
const raw=JSON.parse(fs.readFileSync(path.join(__dirname,'../../../outputs/Physical_Test_Coupons_2026-10-20_SLV-B/SLV-B_spec.json'),'utf8'));
const choices={sleeve_top:.8,feet_style:'grooves',rear_floor_opening:true,insert_bosses:true};
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-9,`${a} != ${b}`);
test('sleeve v2 OptiPlex dimensions, floor, dip ramps and boss widths',()=>{
 const v=T.values(raw,choices),s={...raw,...v},w=T.sleeveGeometry(s),tracks=T.footGrooves(raw,v);
 assert.deepEqual(T.problems(raw,v),[]);close(w.height,37.3);close(w.top,40.8);close(v.u*44.45-.025-w.top,3.625);assert.equal(w.lip,3);
 assert.deepEqual(w.joints,[-95.75,95.75]);close(T.layout(raw,v).tray_w,201.521456708);
 assert.deepEqual(tracks.map(t=>[t.x0,t.x1]),[[-76.75,-70.75],[71.25,76.25]]);
 for(const t of tracks){close(t.depth,2.3);close(t.bottom,1.2);assert.equal(t.floor_bottom,0);assert.ok(t.bottom-t.floor_bottom>=.8);assert.equal(t.y0,-4);close(t.y1,165.8);
  for(const p of t.dips){close(p.ramp,1.3);close(p.ramp,p.cut_depth-t.depth);}}
 assert.equal(Math.abs(w.joints[0])-T.V2.pilotR-w.half,2);close(T.V2.bossR*Math.cos(Math.PI/T.V2.bossFacets)-T.V2.pilotR,3);
 assert.match(T.widthProblem(raw,{...v,dev_off_x:2}),/204/);
});
test('sleeve v2 cable rectangle clears stop, walls, grooves and conservative joints',()=>{
 const v=T.values(raw,choices),q=T.rearFloorGeometry(raw,v),w=T.sleeveGeometry({...raw,...v});
 assert.deepEqual(q,{x0:-28,x1:28,y0:198.5,y1:225.7,r:2});assert.ok(q.y0-w.stop_end>=4);assert.ok(240-T.V2.jointReach-q.y1>=3-1e-9);assert.ok(40-T.V2.jointHalf-q.x1>=3);assert.ok(w.half-q.x1>=5);
 for(const t of T.footGrooves(raw,v))assert.ok(t.y1<q.y0);
});
test('sleeve v2 defaults and explicit draft round trip',()=>{
 assert.deepEqual(T.diff(raw,T.values(raw)),{});assert.deepEqual(T.diff(raw,T.values(raw,choices)),choices);
 for(const name of ['SLV-B','SLV-D','SLV-E']){const day=name==='SLV-E'?'2026-10-21':'2026-10-20',s=JSON.parse(fs.readFileSync(path.join(__dirname,`../../../outputs/Physical_Test_Coupons_${day}_${name}/${name}_spec.json`),'utf8'));assert.deepEqual(T.diff(s,T.values(s)),{});assert.equal(T.sleeveGeometry(s).height,36.3);}
});
test('sleeve v2 blocks invalid dimensions and unsupported combinations',()=>{
 for(const bad of [{sleeve_top:.2},{sleeve_top:2.1},{sleeve_top:true},{sleeve_top:NaN},{feet_style:'bad'},{rear_floor_opening:1},{insert_bosses:'yes'},{rear_support:false},{joint:'single',rear_support:false,rear_floor_opening:false}])assert.ok(T.problems(raw,T.values(raw,{...choices,...bad})).length,JSON.stringify(bad));
 const tall={...raw,feet:raw.feet.map(f=>({...f,h:3.3}))};assert.match(T.problems(tall,T.values(tall,choices)).join(' '),/too tall for grooves/);
 const deep={...raw,dev_w:220,dev_d:182.5};assert.match(T.problems(deep,T.values(deep,{...choices,dev_rot:90})).join(' '),/Not enough floor/);
 assert.match(T.problems({...raw,feet:[]},T.values(raw,choices)).join(' '),/need/);
});
test('sleeve v2 control labels and source hooks are wired without persistence',()=>{
 const ui=fs.readFileSync(path.join(__dirname,'../tray-placement.js'),'utf8');for(const label of ['Top play (mm)','Feet:','Grooves','Cable opening in floor','Stronger insert bosses'])assert.ok(ui.includes(label),label);
 const scad=fs.readFileSync(path.join(__dirname,'../equipment_tray.scad'),'utf8');assert.doesNotMatch(scad,/if\(sleeve&&feet_style=="grooves"\)sleeve_v2_cut\(\);/);assert.match(scad,/module device_features_cut\(\)\{\r?\n sleeve_v2_cut\(\);/);assert.match(scad,/sl_joints=.*sl_pilot_offset/);
});

// Task 41: opt-in hidden faceplate screws (analytical only; fit and strength UNKNOWN).
const hidden={name:'HJ',dev_w:120,dev_d:100,dev_h:30,u:1,device_mount:'sleeve',joint:'screw',rear_support:false,dev_rot:0,holes:[],ports:[],keystones:[]};
test('hidden joint moves the screws outside the sleeve walls and removes the plate holes',()=>{
 const off=T.values(hidden),on=T.values(hidden,{hidden_joint:true}),w=T.sleeveGeometry({...hidden,...on});
 assert.equal(off.hidden_joint,false);assert.deepEqual(T.diff(hidden,on),{hidden_joint:true});assert.deepEqual(T.problems(hidden,on),[]);
 assert.deepEqual(w.joints,[-77.5,77.5]);assert.deepEqual(w.joint_z,[]);assert.equal(w.hidden,true);close(w.outside,173);close(T.layout(hidden,on).tray_w,173);
 assert.deepEqual(T.sleeveGeometry({...hidden,...off}).joint_z.length,2);close(T.layout(hidden,off).tray_w,T.layout(hidden,T.values(hidden,{hidden_joint:false})).tray_w);
 assert.deepEqual(require('../port-openings.js').sleeve({...hidden,hidden_joint:true}).joint_z,[]);
});
test('hidden joint limits: width, combinations, openings in front of the joint',()=>{
 const wide={...hidden,dev_w:160};assert.match(T.widthProblem(wide,T.values(wide,{hidden_joint:true})),/204[\s\S]*hidden screw joint/);
 close(T.layout({...hidden,dev_w:150},T.values({...hidden,dev_w:150},{hidden_joint:true})).tray_w,203);assert.equal(T.widthProblem({...hidden,dev_w:150},T.values({...hidden,dev_w:150},{hidden_joint:true})),'');
 assert.match(T.problems(hidden,T.values(hidden,{hidden_joint:true,insert_bosses:true})).join(' '),/cannot be combined/);
 const flat={...hidden,device_mount:'inserts',holes:[[5,5]]};assert.match(T.problems(flat,T.values(flat,{hidden_joint:true})).join(' '),/need a sleeve/);
 assert.ok(T.problems(hidden,T.values(hidden,{hidden_joint:'yes'})).length);
 const low={...hidden,ports:[{x:77.5,z:12,w:8,h:5,r:1,label:'P'}]},high={...hidden,ports:[{x:77.5,z:30,w:8,h:5,r:1,label:'P'}]};
 assert.match(T.problems(low,T.values(low,{hidden_joint:true})).join(' '),/hidden screw joint/);assert.deepEqual(T.problems(high,T.values(high,{hidden_joint:true})),[]);
});
test('hidden joint control and template hooks exist',()=>{
 const ui=fs.readFileSync(path.join(__dirname,'../tray-placement.js'),'utf8');assert.ok(ui.includes('Hidden screws'));
 const scad=fs.readFileSync(path.join(__dirname,'../equipment_tray.scad'),'utf8');for(const hook of ['hidden_joint=false;','function jon(r)','function jxs(r)','if(jon(rear))','&&!hidden_joint)for(x=sl_joints'])assert.ok(scad.includes(hook),hook);
});

// M6 bracket hardware (Brian, 2026-10-28; HDT-M6-A): opt-in switch, analytical only.
test('M6 hardware switch: default off, saved only when on, limits',()=>{
 const flat={name:'M6',dev_w:150,dev_d:120,dev_h:30,u:1,device_mount:'flat',joint:'screw',rear_support:false,dev_rot:0,holes:[],ports:[],keystones:[]};
 const off=T.values(flat),on=T.values(flat,{m6_joint:true});
 assert.equal(off.m6_joint,false);assert.deepEqual(T.diff(flat,on),{m6_joint:true});assert.deepEqual(T.problems(flat,on),[]);
 assert.match(T.problems(hidden,T.values(hidden,{m6_joint:true})).join(' '),/M6 hardware needs a screw joint/);
 assert.match(T.problems(flat,T.values(flat,{m6_joint:true,dev_off_y:-3})).join(' '),/15\.5 mm/);
});
