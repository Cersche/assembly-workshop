const test=require('node:test'),assert=require('node:assert/strict'),P=require('../port-openings.js');
const spec={ports:[{id:'lan',label:'LAN',type:'rj45',x:0,z:20,w:17,h:14,r:1}],standoff:6};
test('opening movement fixtures and input preservation',()=>{
  const fixtures=[[undefined,0,0],[null,0,0],[{},0,0],[{dev_off_x:11},11,0],[{standoff:10},0,4],[{device_mount:'straps'},0,-6],[{ports:[],u:5,dev_off_y:100},0,0]];
  for(const [tray,dx,dz] of fixtures){const before=structuredClone({spec,tray}),r=P.frontOpenings(spec,tray);
    assert.deepEqual(r,{ports:[{...spec.ports[0],x:dx,z:20+dz}],dx,dz,follows:true,rotation:0,message:null});assert.deepEqual({spec,tray},before);}
  assert.equal(P.frontOpenings({...spec,dev_off_x:5},{dev_off_x:5}).dx,0);
  assert.equal(P.lift({}),6);assert.equal(P.lift({device_mount:'straps',standoff:10}),0);
  assert.equal(P.frontOpenings({...spec,ports:[{x:0.1234,z:20.1234}]},{}).ports[0].x,0.123);
});
test('turned openings stay as entered with exact warning',()=>{
  for(const rotation of [90,180,270]){const tray={dev_rot:rotation,dev_off_x:11,standoff:10},before=structuredClone({spec,tray}),r=P.frontOpenings(spec,tray);
    assert.deepEqual(r,{ports:spec.ports,dx:0,dz:0,follows:false,rotation,message:`The device is turned ${rotation}°, so its front ports now face the ${rotation===180?'rear':'side'} of the tray. The front openings no longer line up with them. The faceplate STL keeps the openings where they were entered in the library (not moved). Check them, or remove them in Edit library item.`});
    assert.notEqual(r.ports[0],spec.ports[0]);assert.equal(P.frontOpenings({},tray).message,null);assert.deepEqual({spec,tray},before);}
});
test('starting sizes are editable copies',()=>{
  const sizes={'rj45':[17,14,1],'usb-a':[15,8,1],'usb-c':[12,7,3],hdmi:[17,8,1],'micro-hdmi':[11,7,2],'dc-barrel':[11,11,5.5],iec:[28,20,1],other:[15,8,1]};
  for(const [type,[w,h,r]] of Object.entries(sizes))assert.deepEqual(P.defaultSize(type),{w,h,r});
  for(const type of [undefined,'unknown','toString'])assert.deepEqual(P.defaultSize(type),sizes.other&&{w:15,h:8,r:1});
  const size=P.defaultSize('rj45');size.w=999;assert.equal(P.DEFAULT_SIZES.rj45.w,17);
  assert.equal(P.SIZE_NOTE,'Starting size for this connector type: a guess, not a measured size. Edit it to match your device.');
});
test('opening bounds, priority, keystone and finite fixtures',()=>{
  const base={x:0,z:20,w:10,h:8};
  const edge='Port 1 opening would run past the faceplate edge. Move the device back toward the centre or edit the port.';
  const vertical='Port 1 opening would run off the top or bottom of the faceplate. Change the standoff or faceplate height, or edit the port.';
  for(const [patch,ks,expected] of [[{x:125,z:0},[125],[edge]],[{z:5},[],[vertical]],[{z:39},[],[vertical]],[{x:60},[60],['Port 1 opening would cut into keystone 1 (at X = 60 mm). Move the device or the keystone.']],[{x:-60},[72.5,-60],['Port 1 opening would cut into keystone 2 (at X = -60 mm). Move the device or the keystone.']],[{x:72.5},[72.5],['Port 1 opening would cut into keystone 1 (at X = 72.5 mm). Move the device or the keystone.']],[{x:75.5},[60],[]],[{x:121,z:6.025},[],[]]]){
    const ports=[{...base,...patch}],before=structuredClone({ports,ks});assert.deepEqual(P.problems(ports,1,ks),expected);assert.deepEqual({ports,ks},before);}
  for(const key of ['x','z','w','h'])for(const v of [NaN,Infinity,-Infinity])assert.deepEqual(P.problems([{...base,[key]:v}],1,[]),[]);
  assert.equal(P.problems([{...base,label:'LAN',x:125},{...base,z:0}],1,[])[0].startsWith('LAN opening'),true);
  assert.equal(P.problems([{...base,x:125},{...base,z:0}],1,[]).length,2);
  const joint='Port 1 opening sits in front of the tray screw joint at X = -40 mm; the cable would hit it. Move the device sideways or edit the port.';
  assert.deepEqual(P.problems([{...base,x:-30,z:15,w:16,h:14}],1,[],[-40,40]),[joint]);
  assert.deepEqual(P.problems([{...base,x:-58,z:15,w:16,h:14}],1,[],[-40,40]),[]);
  assert.deepEqual(P.problems([{...base,x:-57.9,z:15,w:16,h:14}],1,[],[-40,40]),[joint]);
  assert.deepEqual(P.problems([{...base,x:-40,z:38,w:10,h:6}],2,[],[-40,40]),[]);
  assert.deepEqual(P.problems([{...base,x:-30,z:15,w:16,h:14}],1,[]),[]);
});
test('joint positions: default kept when clear, nearest clear spot per side, else a plain problem (Brian, 2026-10-19)',()=>{
  const lan=[{x:-30,z:15,w:16,h:14}],before=structuredClone(lan);
  assert.deepEqual(P.jointPositions([],[],68),{joints:[-40,40],default:40,moved:false,problem:null});
  assert.equal(P.jointPositions([{x:-40,z:38,w:10,h:6}],[],68).moved,false);
  assert.deepEqual(P.jointPositions(lan,[],68).joints,[-48,40]);
  assert.deepEqual(P.jointPositions(lan,[],50.5).joints,[-12,38.5]);
  assert.deepEqual(P.jointPositions([{x:-40,z:15,w:16,h:14},{x:-58,z:15,w:16,h:14}],[],68).joints,[-22,40]);
  assert.deepEqual(P.jointPositions([],[-50],68).joints,[-34,40]);
  const r=P.jointPositions([{x:0,z:15,w:200,h:14}],[],68);
  assert.deepEqual(r.joints,[null,null]);
  assert.equal(r.problem,'The left and right tray screw joints cannot be placed clear of the openings and keystones anywhere on the tray. Move the device or an opening, or choose the single printed piece joint.');
  assert.ok(P.jointPositions([{x:-30,z:15,w:90,h:14}],[],68).problem.startsWith('The left tray screw joint cannot'));
  assert.deepEqual(lan,before);
});
