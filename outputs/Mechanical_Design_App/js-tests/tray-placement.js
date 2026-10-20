'use strict';
// Place on tray window: pure placement logic, the workspace "Apply to draft" hook, and static wiring checks.
// In-memory fixtures only. No server, user data, rendering or export.
const test=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const APP=path.resolve(__dirname,'..'),T=require(path.join(APP,'tray-placement.js'));
const RackLayout=require(path.join(APP,'rack-references','rack-layout.js'));
const read=f=>fs.readFileSync(path.join(APP,f),'utf8');
const SPEC={name:'Box',dev_w:85,dev_d:56,dev_h:20,hole_d:2.7,holes:[[3.5,3.5],[61.5,49.5]],standoff:5,insert_pilot:3.2,board_t:1.6,
  device_mount:'inserts',joint:'screw',keystones:[-100],rear_support:false,u:1};

test('values: slot tray wins, then the library spec, then template defaults',()=>{
  const v=T.values(SPEC,{dev_off_x:-4,keystones:[90]});
  assert.equal(v.dev_off_x,-4);assert.equal(v.standoff,5);assert.deepEqual(v.keystones,[90]);
  const older=T.values({dev_w:50,dev_d:50,dev_h:10},null);
  assert.deepEqual([older.dev_off_y,older.dev_rot,older.device_mount,older.u,older.joint],[0,0,'inserts',1,'screw']);
  v.keystones.push(1);assert.deepEqual(SPEC.keystones,[-100]);
});
test('diff keeps only choices that differ from the library item',()=>{
  assert.deepEqual(T.diff(SPEC,T.values(SPEC,{})),{});
  const v=T.values(SPEC,{});v.dev_off_x=3;v.keystones=[-100];v.u=2;
  assert.deepEqual(T.diff(SPEC,v),{dev_off_x:3,u:2});
  assert.deepEqual(T.diff(SPEC,T.values(SPEC,{standoff:5})),{});
});
test('layout and hole positions follow equipment_tray.scad (rotation swaps width and depth)',()=>{
  const L=T.layout(SPEC,T.values(SPEC,{dev_off_x:10,dev_off_y:4,dev_rot:90}));
  assert.deepEqual([L.fp_w,L.fp_d,L.tray_w,L.dev_x,L.dev_y],[56,85,2*(10+28+8),10-28,16]);
  // dp() at 90°: [x,y] -> [dev_d-y, x]
  assert.deepEqual(T.holes(SPEC,T.values(SPEC,{dev_rot:90,dev_off_x:10,dev_off_y:4}))[0],[-18+56-3.5,16+3.5]);
  assert.deepEqual(T.holes(SPEC,T.values(SPEC,{}))[1],[-42.5+61.5,12+49.5]);
});
test('SCAD assert errors show as plain messages',()=>{
  const msg=t=>T.problems(SPEC,T.values(SPEC,t)).join(' ');
  assert.equal(msg({}),'');
  assert.match(msg({dev_off_x:70}),/This tray is 241 mm wide.*allows 204 mm/);
  assert.match(msg({dev_off_y:-13}),/moved into the faceplate/);
  assert.match(msg({rear_support:true,dev_off_y:180}),/past the rear posts/);
  assert.match(msg({dev_rot:45}),/Rotation must be 0, 90, 180 or 270/);
  assert.match(T.problems({...SPEC,dev_w:220,dev_d:60},T.values({...SPEC,dev_w:220},{})).join(' '),/This tray is 236 mm wide.*Rotate 90°/);
  assert.equal(T.problems({...SPEC,dev_w:220,dev_d:60},T.values(SPEC,{dev_rot:90})).length,0);
  assert.match(msg({standoff:30}),/taller than 1U/);
  assert.match(msg({keystones:[-60]}),/collar would hit the tray/);
  assert.match(T.problems({...SPEC,holes:[]},T.values(SPEC,{})).join(' '),/need mounting holes/);
  assert.equal(T.problems({...SPEC,holes:[]},T.values(SPEC,{device_mount:'straps'})).length,0);
});
test('snap rounds to whole millimetres; live sketch is whole triangles',()=>{
  assert.deepEqual([T.snap(2.4),T.snap(-2.6),T.snap(7.5)],[2,-3,8]);
  const sets=T.schematic(SPEC,T.values(SPEC,{}));
  assert.ok(sets.length>=3);for(const s of sets)assert.equal(s.v.length%9,0);
  assert.equal(sets[2].alpha,0.55); // translucent device box
});

function applyHarness(rack){
  const src=read('workspace.js'),a=src.indexOf('  window.applyTrayPlacement=function'),b=src.indexOf('\n  };',a)+5;assert.ok(a>0&&b>a);
  const ctx=vm.createContext({window:{},RackLayout,active:()=>rack,selectedSlot:null,changed:0,rendered:0,note:''});
  vm.runInContext('function markChanged(){changed++;}function render(){rendered++;}function notify(t){note=t;}\n'+src.slice(a,b),ctx);
  return ctx;
}
test('Apply to draft changes only the rack draft and the slot span when U changes',()=>{
  const rack={id:'r1',slots:5,placements:[{id:'a',equipment:'eq-0123456789ab',slot:1,span:1},{id:'b',equipment:'eq-000000000004',slot:4,span:1}]};
  const ctx=applyHarness(rack);
  ctx.window.applyTrayPlacement('r1','a',{dev_off_x:5},null);
  assert.deepEqual(rack.placements[0].tray,{dev_off_x:5});assert.equal(ctx.changed,1);assert.match(ctx.note,/Save to keep it/);
  ctx.window.applyTrayPlacement('r1','a',{u:2},2);
  assert.equal(rack.placements[0].span,2);assert.deepEqual(rack.placements[0].tray,{u:2});assert.equal(rack.placements[0].fit,'UNKNOWN');
  ctx.window.applyTrayPlacement('r1','a',{},null);assert.equal('tray' in rack.placements[0],false);
  assert.throws(()=>ctx.window.applyTrayPlacement('r1','a',{u:4},4),/overlaps/);
  assert.throws(()=>ctx.window.applyTrayPlacement('other','a',{},null),/original rack/);
  assert.equal(rack.placements[0].span,2);
});
test('wiring: window opens on place/edit, blocks while a problem shows, never saves',()=>{
  const ws=read('workspace.js'),tp=read('tray-placement.js'),html=read('index.html'),wiz=read('equipment-wizard.js');
  assert.ok(html.indexOf('/equipment-wizard.js')<html.indexOf('/tray-placement.js'));
  assert.ok(ws.includes('window.openTrayPlacement?.(rack.id,placement)'));
  assert.ok(ws.includes("window.openTrayPlacement(active()?.id,placement)"));
  assert.ok(tp.includes("'Fit, retention, strength: UNKNOWN'"));
  assert.ok(tp.includes("for(const id of['tpApply','tpExport'])")&&tp.includes('.disabled=!!list.length'));
  for(const p of['/api/rack-workspace','/api/studio-save','/api/equipment-library\','])assert.ok(!tp.includes(p),p);
  for(const k of['Snap','Centre','Left/right offset','Front gap','Standoff','Height (rack units)','Keystones','Rear support','Apply to draft'])assert.ok(tp.includes(k),k);
  assert.ok(wiz.includes('window.EquipmentPainter='));
  assert.ok(!wiz.includes('function trayChoices')&&!wiz.includes('Tray choices (temporary'));
});
test('rack view draws each slot\'s own tray: exact render if one exists, else a box sketch; never renders (2026-10-19)',()=>{
  const ws=read('workspace.js'),wiz=read('equipment-wizard.js'),tp=read('tray-placement.js'),app=read('app.py');
  assert.ok(!/Placement not rendered yet|trayNotRendered/.test(ws));
  assert.match(ws,/EquipmentRackView\?\.status\(placement\)==='sketch'/);
  const patch=wiz.slice(wiz.indexOf('const placed=new Map()'),wiz.indexOf('function open()'));
  // Lookup only: the rack view never asks for a preview render or an STL build.
  assert.ok(patch.includes("'/api/equipment-placement-mesh'")&&!/equipment-preview|equipment-build/.test(patch));
  assert.ok(patch.includes('const got=partsFor(a);')&&patch.includes('T.rackSketch(it.spec,a.tray)'));
  assert.match(patch,/frontFace\(mesh,got\.spec\)/); // images and outline use the slot's openings
  assert.ok(app.includes("'/api/equipment-placement-mesh'")&&app.includes('equipment.cached_allocation_render('));
  assert.equal((tp.match(/window\.EquipmentRackView\?\.refresh\(\)/g)||[]).length,2); // after exact preview and after build
  // Mesh arrival really redraws the rack, and a sketch -> exact switch refreshes the inspector note.
  assert.ok(ws.includes("window.addEventListener('resize',drawSoon);window.addEventListener('equipment-rack-view',()=>{drawSoon();renderProperties();});"));
  assert.ok(wiz.includes("new Event('equipment-rack-view')"));
});
const bounds=flat=>{const lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];
  for(let i=0;i<flat.length;i+=3)for(let k=0;k<3;k++){lo[k]=Math.min(lo[k],flat[i+k]);hi[k]=Math.max(hi[k],flat[i+k]);}return [lo,hi];};
test('rackSketch follows the slot tray settings in equipment_tray.scad coordinates',()=>{
  const lib=T.rackSketch(SPEC,{});
  assert.deepEqual(Object.keys(lib).sort(),['faceplate','openings','tray']);
  assert.deepEqual(bounds(lib.faceplate),[[-126,-4,0.025],[126,0,44.45-0.025]]);  // 1U plate
  assert.deepEqual(bounds(lib.tray)[0].slice(0,2),[-(85/2+8),0]);           // tray_w = 2*(fp_w/2+margin)
  assert.equal(bounds(lib.tray)[1][1],12+56+8);                             // tray_d = front_gap+fp_d+margin
  const h=44.45/2;
  assert.deepEqual(bounds(lib.openings),[[-107.4,-4.2,h-8.3],[-92.6,0.2,h+8.3]]); // keystone at -100 (14.8 x 16.6)
  const moved=T.rackSketch(SPEC,{dev_off_x:-20,dev_off_y:15,dev_rot:90,u:2,keystones:[],rear_support:true});
  assert.equal(bounds(moved.faceplate)[1][2],0.025+(2*44.45-0.05));
  assert.equal(moved.openings,undefined);
  assert.equal(bounds(moved.tray)[0][0],-(20+56/2+8));                      // rotated: fp_w = dev_d
  assert.equal(bounds(moved.tray)[1][1],240);                               // rear support: tray to the rear posts
  assert.deepEqual(bounds(moved.rear_bracket),[[-126,240,0.025],[126,244,0.025+(2*44.45-0.05)]]);
  const ported=T.rackSketch({...SPEC,keystones:[],ports:[{x:10,z:20,w:15,h:8,r:1}]},null);
  assert.deepEqual(bounds(ported.openings),[[2.5,-4.2,16],[17.5,0.2,24]]);
  for(const flat of Object.values(moved))assert.equal(flat.length%9,0);     // whole triangles
});

test('204 mm hard width budget includes margin and offsets, with explicit rotate advice',()=>{
  const s={...SPEC,keystones:[],dev_w:194.5,dev_d:182.5,dev_h:38.8,device_mount:'flat'};
  assert.match(T.widthProblem(s),/210.5.*204.*208.*2 mm each side.*Rotate 90°/);
  assert.deepEqual(T.problems(s,T.values(s,{dev_rot:90})),[]);
  assert.equal(T.layout(s,T.values(s,{dev_rot:90})).tray_w,198.5);
  assert.equal(T.widthProblem({...s,dev_w:188}),'');
  assert.match(T.widthProblem({...s,dev_w:188.1}),/204.1/);
  assert.match(T.widthProblem({...s,dev_w:188},T.values(s,{dev_off_x:.1})),/204.2/);
});


test('rear cable openings preserve saved defaults and roundtrip explicit choices',()=>{
  const old={...SPEC,rear_support:true};
  const v=T.values(old,null);
  assert.equal(v.rear_openings,false);
  assert.deepEqual(T.diff(old,v),{});
  v.rear_openings=true;
  assert.deepEqual(T.diff(old,v),{rear_openings:true});
  assert.equal(T.values(old,{rear_openings:true}).rear_openings,true);
  assert.equal(T.values({...old,rear_openings:true},{rear_openings:false}).rear_openings,false);
  const ui=read('tray-placement.js');
  assert.ok(ui.includes("if(rs.checked)v.rear_openings=true"));
  assert.ok(ui.includes("...(v.rear_support?[h('label'"));
  assert.ok(ui.includes('Cable openings in the rear bracket'));
  assert.ok(ui.includes('this box sketch does not show the cutouts'));
});
