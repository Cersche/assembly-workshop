'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const T=require('../tray-placement.js'),P=require('../port-openings.js'),Pair=require('../tray-pair.js'),C=require('../cable-ports.js');
const spec={name:'Wall',dev_w:90.7,dev_d:90.4,dev_h:25.4,device_mount:'wall',joint:'screw',dev_off_y:13,holes:[],ports:[],rear_ports:[],u:1};
test('Wall accepted; floor, ports and placement round trip',()=>{
 const v=T.values(spec);assert.deepEqual(T.problems(spec,v),[]);assert.equal(P.deviceLift({...spec,...v}),11.225);assert.equal(P.lift(spec),0);assert.equal(P.usesStandoffs(spec),false);
 assert.equal(Pair.REACH.wall,2.5);assert.deepEqual(T.diff(spec,v),{});
 const changed={...v,wall_open:['front','right']};assert.deepEqual(T.diff(spec,changed),{wall_open:['front','right']});
 assert.deepEqual(Pair.diff(spec,Pair.values(spec,{wall_open:['left']})),{wall_open:['left']});
 const ports=C.wizardPorts({...spec,rear_ports:[{id:'r',x:0,z:20}]},{standoff:29});assert.equal(ports[0].z,20);
});
test('Wall rejects missing cable access and unknown sides',()=>{
 for(const wall_open of [[],['back'],'rear',null])assert(T.problems(spec,T.values(spec,{wall_open})).some(x=>x.includes('Open sides')));
 assert(T.problems({...spec,dev_h:2},T.values(spec)).some(x=>x.includes('taller than 2')));
});
test('Wall clash and rotated preview geometry',()=>{
 for(const dev_rot of [0,90,180,270]){
  const v=T.values(spec,{dev_rot,dev_off_y:1});assert(T.problems(spec,v).includes(T.WALL_MESSAGE));
  v.dev_off_y=13;assert.deepEqual(T.problems(spec,v),[]);const q=T.wallBoxes(spec,v);assert.equal(q.length,9);assert.deepEqual([...new Set(q.map(q=>q[4]))].sort((a,b)=>a-b),[4,12]);
  const wall=T.schematic(spec,v)[1].v,strap=T.schematic(spec,{...v,device_mount:'straps'})[1].v;assert(wall.length>strap.length);
 }
 const small={...spec,dev_w:20,dev_d:20,dev_h:5};assert.equal(T.wallBoxes(small,T.values(small)).length,3);
});
test('Two-device wall, own open sides, floor and mixed mount rules',()=>{
 const a={...spec,dev_w:60,dev_d:70,dev_h:20,dev_off_x:-40},b={...a,dev_off_x:40},v=T.values(a),v2=Pair.values(b,{wall_open:['front','left']});
 assert.deepEqual(Pair.problems(a,v,b,v2),[]);assert.deepEqual(Pair.merged(v,v2).wall_open,['front','left']);
 assert.deepEqual(Pair.problems(a,v,b,{...v2,device_mount:'straps'}),[]);
 assert(Pair.problems(a,v,b,{...v2,device_mount:'flat'}).some(x=>x.includes('either both')));
 assert(Pair.schematic(a,v,b,v2)[1].v.length>T.schematic(a,v)[1].v.length);
});
test('Wall side UI is attached to the active device',()=>{
 const fs=require('node:fs'),path=require('node:path'),src=fs.readFileSync(path.join(__dirname,'../tray-placement.js'),'utf8');
 assert(src.includes('Open sides (cables):'));assert(src.includes('dv.wall_open=WALL_SIDES.filter'));assert(src.includes('...wallOpts'));
});

test('Single-piece pair still checks the wall against the faceplate',()=>{
 const a={...spec,dev_w:60,dev_d:70,dev_off_x:-40,joint:'single',dev_off_y:-12},b={...a,dev_off_x:40,dev_off_y:13};
 assert(Pair.problems(a,T.values(a),b,Pair.values(b)).includes(T.WALL_MESSAGE));
});
