'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),vm=require('node:vm');
const C=require('../cable-routes.js'),P=require('../cable-ports.js');
const U=44.45;
function fixture(){
  const ctx={ports:P,library:[{id:'wizard',spec:{u:1,dev_d:80,
    ports:[{id:'front-left',x:-40,z:20,type:'rj45'}],
    rear_ports:[{id:'rear-left',x:-40,z:20,type:'rj45'},{id:'rear-right',x:40,z:20,type:'iec'}],keystones:[0]}}]};
  const rack={slots:6,placements:[{id:'pi',equipment:'pi4',slot:1,span:1},
    {id:'w1',equipment:'wizard',slot:2,span:1},{id:'w2',equipment:'wizard',slot:5,span:1}],
    cabling:{guides:[],exits:[],endpoints:[{id:'desk',kind:'desk',name:'Desk'}],cables:[]}};
  for(const post of ['FL','FR','RL','RR'])for(let slot=1;slot<=6;slot++)rack.cabling.guides.push({id:post+slot,post,slot});
  return {rack,ctx};
}
const port=(allocation,p)=>({allocation,port:p});
function cable(from=port('w1','rear-left'),to=port('w2','rear-left')){
  return {id:'c1',number:'C1',type:'rj45',service_loop_m:0.15,from,to,route:{mode:'auto',guides:[],exit:null}};
}
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-9,`${a} != ${b}`);

test('exact API exports and browser load without window/DOM/fetch',()=>{
  assert.deepEqual(Object.keys(C).sort(),['EXIT_POSITIONS','ENDPOINT_KINDS','TYPE_STYLE','cableColor','endAnchor','endFace','autoRoute','path','estimate','linkedCable','portInUse','nextNumber','guideLoad','crowded','upkeep','warnings','connectorMismatch'].sort());
  const sandbox={};vm.runInNewContext(fs.readFileSync(require.resolve('../cable-routes.js'),'utf8'),sandbox);
  assert.deepEqual(Object.keys(sandbox),['LabRaxCables']);
  for(const [type,style] of Object.entries(C.TYPE_STYLE))assert.equal(style.color,P.TYPES[type].color);
  assert.deepEqual(Object.values(C.TYPE_STYLE).map(s=>s.diameter_mm),[6,4.5,4,7,5,3.5,8,6,4]);
  assert.equal(C.cableColor({type:'iec'}),'#ff6b6b');
  assert.equal(C.cableColor({type:'rj45',color:'#010203'}),'#010203');
});
test('port anchors use actual Pi and generic wizard data, pointing offsets and base Z',()=>{
  const {rack,ctx}=fixture();
  const a=C.endAnchor(rack,port('pi','ethernet'),ctx);near(a[0],52.2);near(a[1],58.75);near(a[2],5*U+24.4);
  assert.deepEqual(C.endAnchor(rack,port('w1','rear-left'),ctx),[-40,100,4*U+20]);
  assert.deepEqual(C.endAnchor(rack,port('w1','front-left'),ctx),[-40,-12,4*U+20]);
  for(const end of [null,{endpoint:'desk'},port('gone','x'),port('w1','gone')])assert.equal(C.endAnchor(rack,end,ctx),null);
  const left={ports:{portsFor:()=>[{id:'p',x:10,y:20,z:30,points:'left'}],baseZ:()=>40},library:[]};
  assert.deepEqual(C.endAnchor(rack,port('pi','p'),left),[2,20,70]);
});
test('end faces keep UNKNOWN separate from rear fallback',()=>{
  const {rack,ctx}=fixture();
  assert.equal(C.endFace(rack,port('pi','ethernet'),ctx),null);
  assert.equal(C.endFace(rack,port('w1','front-left'),ctx),'front');
  assert.equal(C.endFace(rack,port('w1','rear-left'),ctx),'rear');
  assert.equal(C.endFace(rack,{endpoint:'desk'},ctx),'rear');
  assert.equal(C.endFace(rack,null,ctx),null);
});
test('auto routing chooses one post and orders guides from from to to',()=>{
  const {rack,ctx}=fixture(),c=cable();
  assert.deepEqual(C.autoRoute(rack,c,ctx),{guides:['RL2','RL3','RL4','RL5'],exit:null});
  [c.from,c.to]=[c.to,c.from];assert.deepEqual(C.autoRoute(rack,c,ctx).guides,['RL5','RL4','RL3','RL2']);
  c.from=port('w1','front-left');c.to=port('w2','front-left');assert.deepEqual(C.autoRoute(rack,c,ctx).guides,['FL2','FL3','FL4','FL5']);
  c.to=port('w2','rear-left');assert.ok(C.autoRoute(rack,c,ctx).guides.every(id=>id.startsWith('RL')));
  c.from=port('w1','rear-right');c.to=port('w2','rear-right');assert.deepEqual(C.autoRoute(rack,c,ctx).guides,['RR2','RR3','RR4','RR5']);
  c.from=port('pi','ethernet');assert.deepEqual(C.autoRoute(rack,c,ctx).guides,['RR1','RR2','RR3','RR4','RR5']);
});
test('multi-U endpoint slots come from anchor Z, not allocation start',()=>{
  const {rack,ctx}=fixture();rack.placements[1].span=2;
  const c=cable();assert.deepEqual(C.autoRoute(rack,c,ctx).guides,['RL3','RL4','RL5']);
});
test('exit selection preserves an existing choice and otherwise scores nearest route point',()=>{
  const {rack,ctx}=fixture(),c=cable(port('w1','rear-left'),{endpoint:'desk'});
  rack.cabling.exits=[{id:'right',position:'right',slot:2},{id:'left',position:'left',slot:2}];
  assert.deepEqual(C.autoRoute(rack,c,ctx),{guides:['RL2'],exit:'left'});
  c.route.exit='right';assert.equal(C.autoRoute(rack,c,ctx).exit,'right');
  c.route.exit='gone';assert.equal(C.autoRoute(rack,c,ctx).exit,'left');
  rack.cabling.exits=[];assert.deepEqual(C.autoRoute(rack,c,ctx),{guides:['RL2'],exit:null});
  c.to=port('w2','rear-left');c.route.exit='left';assert.equal(C.autoRoute(rack,c,ctx).exit,null);
});
test('endpoint exit slot determines guide interval in either end direction',()=>{
  const {rack,ctx}=fixture(),c=cable(port('w1','rear-left'),{endpoint:'desk'});
  rack.cabling.exits=[{id:'bottom',position:'bottom-rear',slot:6}];
  assert.deepEqual(C.autoRoute(rack,c,ctx),{guides:['RL2','RL3','RL4','RL5','RL6'],exit:'bottom'});
  [c.from,c.to]=[c.to,c.from];assert.deepEqual(C.autoRoute(rack,c,ctx).guides,['RL6','RL5','RL4','RL3','RL2']);
});
test('path preserves specified point order, manual order and all scene anchor coordinates',()=>{
  const {rack,ctx}=fixture(),c=cable();
  rack.cabling.exits=[{id:'bottom',position:'bottom-rear',slot:6},{id:'top',position:'top-rear',slot:1},
    {id:'left',position:'left',slot:3},{id:'right',position:'right',slot:4}];
  c.route={mode:'manual',guides:['FR3','RL2'],exit:'bottom'};
  assert.deepEqual(C.path(rack,c,ctx),[[-40,100,4*U+20],[118.26,-14,3*U+U/2],[-118.26,254,4*U+U/2],[0,250,-10],[-40,100,U+20]]);
  c.from=null;c.to={endpoint:'desk'};c.route.guides=[];
  for(const [id,point] of [['bottom',[0,250,-10]],['top',[0,250,6*U+10]],['left',[-140,220,3*U+U/2]],['right',[140,220,2*U+U/2]]]){
    c.route.exit=id;assert.deepEqual(C.path(rack,c,ctx),[point]);
  }
});
test('length is straight segments plus service loops per connected port, rounded up',()=>{
  const {rack,ctx}=fixture(),c=cable();
  let e=C.estimate(rack,c,ctx);near(e.route_mm,3*U);assert.equal(e.length_m,0.5);assert.equal(e.complete,true);assert.equal(e.to_exit,false);
  c.service_loop_m=0;assert.equal(C.estimate(rack,c,ctx).length_m,0.2);
  delete c.service_loop_m;rack.cabling.settings={service_loop_m:0.2};assert.equal(C.estimate(rack,c,ctx).length_m,0.6);
  delete rack.cabling.settings;assert.equal(C.estimate(rack,c,ctx).length_m,0.5);
  c.to={endpoint:'desk'};e=C.estimate(rack,c,ctx);assert.deepEqual(e,{route_mm:0,length_m:0.2,to_exit:true,complete:true});
  c.from=null;assert.deepEqual(C.estimate(rack,c,ctx),{route_mm:0,length_m:0,to_exit:true,complete:false});
  c.to=null;assert.equal(C.estimate(rack,c,ctx).complete,false);
});
test('rounding handles exact tenths and a value truly above a tenth',()=>{
  const {rack,ctx}=fixture(),c=cable();c.to=c.from;c.service_loop_m=0.15;
  assert.equal(C.estimate(rack,c,ctx).length_m,0.3);
  c.service_loop_m=0.1500001;assert.equal(C.estimate(rack,c,ctx).length_m,0.4);
});
test('keystone pair lookup, port occupancy and lowest unused cable number',()=>{
  const {rack,ctx}=fixture(),rear=cable(port('pi','ethernet'),port('w1','ks-1-rear'));
  const front={...cable(port('w1','ks-1-front'),{endpoint:'desk'}),id:'c3',number:'C3'};
  rack.cabling.cables=[rear,front];
  assert.equal(C.linkedCable(rack,rear,ctx),'c3');assert.equal(C.linkedCable(rack,front,ctx),'c1');
  assert.equal(C.portInUse(rack,'w1','ks-1-front'),'c3');assert.equal(C.portInUse(rack,'w1','ks-1-front','c3'),null);
  assert.equal(C.portInUse(rack,'w2','ks-1-front'),null);assert.equal(C.nextNumber(rack),'C2');
  front.from=port('w2','ks-1-front');assert.equal(C.linkedCable(rack,rear,ctx),null);
});
test('guide load counts cables once and crowding is strictly above user setting',()=>{
  const {rack}=fixture();
  rack.cabling.cables=Array.from({length:7},(_,i)=>({...cable(),id:'c'+i,route:{mode:'manual',guides:['RL2','RL2'],exit:null}}));
  assert.deepEqual(C.guideLoad(rack),{RL2:7});assert.deepEqual(C.crowded(rack),['RL2']);
  rack.cabling.settings={guide_warn_above:7};assert.deepEqual(C.crowded(rack),[]);
  rack.cabling.cables[0].route.guides=['__proto__'];assert.equal(C.guideLoad(rack).__proto__,1);
});
test('manual upkeep drops missing references, retains order and is idempotent',()=>{
  const {rack,ctx}=fixture(),c=cable();c.route={mode:'manual',guides:['RL4','gone','RL2'],exit:'gone'};rack.cabling.cables=[c];
  assert.equal(C.upkeep(rack,ctx),rack.cabling.cables);
  assert.deepEqual(c.route,{mode:'manual',guides:['RL4','RL2'],exit:null});assert.equal(c.route_changed,true);
  const saved=JSON.stringify(rack);C.upkeep(rack,ctx);assert.equal(JSON.stringify(rack),saved);
});
test('manual moved guide is retained and marked until acknowledged',()=>{
  const {rack,ctx}=fixture(),c=cable();c.route={mode:'manual',guides:['RL2'],exit:null};rack.cabling.cables=[c];
  C.upkeep(rack,ctx);assert.equal(c.route_changed,undefined);
  rack.cabling.guides.find(g=>g.id==='RL2').post='RR';C.upkeep(rack,ctx);
  assert.equal(c.route_changed,true);assert.deepEqual(c.route.guides,['RL2']);
  delete c.route_changed;C.upkeep(rack,ctx);assert.equal(c.route_changed,undefined);
});
test('automatic upkeep follows equipment movement and removed guides',()=>{
  const {rack,ctx}=fixture(),c=cable();rack.cabling.cables=[c];C.upkeep(rack,ctx);
  rack.placements[1].slot=3;rack.cabling.guides=rack.cabling.guides.filter(g=>g.id!=='RL4');C.upkeep(rack,ctx);
  assert.deepEqual(c.route,{mode:'auto',guides:['RL3','RL5'],exit:null});
  const saved=JSON.stringify(rack);C.upkeep(rack,ctx);assert.equal(JSON.stringify(rack),saved);
});
test('upkeep disconnects removed allocations, ports and outside endpoints without deleting cables',()=>{
  for(const scenario of ['allocation','port','endpoint']){
    const {rack,ctx}=fixture(),c=cable(port('w1','rear-left'),{endpoint:'desk'});rack.cabling.cables=[c];
    if(scenario==='allocation')rack.placements=rack.placements.filter(p=>p.id!=='w1');
    if(scenario==='port')ctx.library[0].spec.rear_ports=[];
    if(scenario==='endpoint')rack.cabling.endpoints=[];
    C.upkeep(rack,ctx);assert.equal(c[scenario==='endpoint'?'to':'from'],null);assert.equal(rack.cabling.cables.length,1);
    const saved=JSON.stringify(rack);C.upkeep(rack,ctx);assert.equal(JSON.stringify(rack),saved);
  }
});
test('warnings include unconnected, missing exit, UNKNOWN face, route changed and crowding',()=>{
  const {rack,ctx}=fixture(),c=cable(port('pi','ethernet'),{endpoint:'desk'});c.route_changed=true;c.route.guides=['RR1'];
  rack.cabling.cables=[c,{...c,id:'c2'}];rack.cabling.settings={guide_warn_above:1};
  let warnings=C.warnings(rack,c,ctx);assert.equal(warnings.length,4);
  for(const text of ['no exit','face UNKNOWN','route changed','crowding'])assert.ok(warnings.some(s=>s.includes(text)));
  c.from=null;assert.ok(C.warnings(rack,c,ctx).some(s=>s.includes('Unconnected')));
  const clean=cable();rack.cabling.cables=[clean];assert.deepEqual(C.warnings(rack,clean,ctx),[]);
});
test('read-only helpers never modify rack or cable fixtures',()=>{
  const {rack,ctx}=fixture(),c=cable();rack.cabling.cables=[c];const saved=JSON.stringify(rack);
  C.autoRoute(rack,c,ctx);C.path(rack,c,ctx);C.estimate(rack,c,ctx);C.warnings(rack,c,ctx);C.linkedCable(rack,c,ctx);C.guideLoad(rack);
  assert.equal(JSON.stringify(rack),saved);
});

test('connector mismatches respect saved overrides and never mutate inputs',()=>{
  const {rack,ctx}=fixture(),c=cable();
  rack.cabling.ports=[{allocation:'w2',port:'rear-left',type:'usb-a'}];
  let before=structuredClone({rack,c,library:ctx.library});
  assert.deepEqual(C.connectorMismatch(rack,c,ctx),{from:'rj45',to:'usb-a',text:'Needs an adapter cable: RJ45 (Ethernet) to USB-A.'});
  c.route_changed=true;before=structuredClone({rack,c,library:ctx.library});
  assert.deepEqual(C.warnings(rack,c,ctx),['Cable route changed.','Needs an adapter cable: RJ45 (Ethernet) to USB-A.']);
  assert.deepEqual({rack,c,library:ctx.library},before);
  [c.from,c.to]=[c.to,c.from];assert.equal(C.connectorMismatch(rack,c,ctx).text,'Needs an adapter cable: USB-A to RJ45 (Ethernet).');
  [c.from,c.to]=[c.to,c.from];
  for(const type of ['rj45','keystone','other']){rack.cabling.ports[0].type=type;assert.equal(C.connectorMismatch(rack,c,ctx),null);}
  rack.cabling.ports=[];delete ctx.library[0].spec.rear_ports[0].type;assert.equal(C.connectorMismatch(rack,c,ctx),null);
  for(const end of [null,{endpoint:'desk'},port('w2','gone'),port('removed','rear-left')]){c.to=end;assert.equal(C.connectorMismatch(rack,c,ctx),null);}
});
