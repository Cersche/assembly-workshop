'use strict';
// Real workspace closures, in-memory fixtures only. No server, user data or export.
const test=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const APP=path.resolve(__dirname,'..'),source=fs.readFileSync(path.join(APP,'workspace.js'),'utf8');
function section(start,end){const a=source.indexOf(start),b=source.indexOf(end,a+start.length);assert.ok(a>=0&&b>a);return source.slice(a,b);}
const plain=x=>JSON.parse(JSON.stringify(x));
function harness(){
  const nodes=new Map(),get=id=>{if(!nodes.has(id))nodes.set(id,{value:0,open:false,children:[],append(...x){this.children.push(...x);},replaceChildren(){this.children=[];}});return nodes.get(id);};
  const box=vm.createContext({LabRaxScene:require(path.join(APP,'rack-references/rack-scene.js')),
    byId:get,paragraph:text=>text,documentState:{racks:[]},editingId:null,editingRack:null,
    sourceMeshes:{extension:{}},rackGuides:()=>[],drawPreviewSoon(){},markChanged(){},drawSoon(){},renderProperties(){},notify(){},sceneCacheKey:''});
  vm.runInContext(source.match(/  const POSTS = 4, HOLES_PER_U = 3;/)[0]+'\n'+
    section('  const stackHeight=','  // Rack frame STL export:')+'\n'+
    section('  function setSlots(','  function drawPreviewSoon(')+'\n'+
    section('  function moveExtension(','  function drawSoon(')+
    '\nglobalThis.counts=rackCounts;globalThis.frame=rackFrame;globalThis.setHeight=setSlots;globalThis.bom=renderBom;globalThis.move=moveExtension;',box);
  return {box,get};
}
const examples=[
  ['5U default',{slots:5},{5:4},0,60,{5:2}],
  ['5U custom',{slots:5,post_levels:{left:[1,3],right:[5]}},{1:2,3:2,5:2},1,54,{1:1,3:1,5:1}],
  ['9U default',{slots:9},{3:4,5:4},2,96,{3:2,5:2}],
  ['9U custom',{slots:9,post_levels:{left:[3,5],right:[4,4]}},{3:2,4:4,5:2},2,96,{3:1,4:2,5:1}],
  ['14U default',{slots:14},{2:4,5:8},4,144,{2:2,5:4}],
  ['14U custom',{slots:14,post_levels:{left:[2,5,5],right:[4,4,4]}},{2:2,4:6,5:4},4,144,{2:1,4:3,5:2}],
];
for(const [label,rack,posts,ext,hardware,panels] of examples)test('rack BOM worked example: '+label,()=>{
  const {box}=harness(),before=JSON.stringify(rack),c=plain(box.counts(rack,true));
  assert.deepEqual(c.posts,posts);assert.equal(c.extensions,ext);assert.equal(c.hardware_allowance,hardware);assert.deepEqual(c.panels,panels);
  assert.equal(JSON.stringify(rack),before);
});
test('rack BOM missing side defaults only the missing stack; 1U has no joints',()=>{
  const {box}=harness();const c=plain(box.counts({slots:5,post_levels:{left:[1,3]}}));
  assert.deepEqual(c.stacks,{left:[1,3],right:[5]});assert.equal(c.hardware_allowance,54);
  assert.deepEqual(plain(box.counts({slots:1})).posts,{1:4});
});
test('rack BOM rejects explicitly invalid stacks and heights without fabricated parts',()=>{
  const {box}=harness();
  for(const level of [null,[],{extra:[5]},{left:[]},{left:[0,4]},{left:[6]},{left:[2.5,1.5]},{left:['5']},{left:[true]},{left:[4]},{left:null},{left:'5'}]){
    const c=plain(box.counts({slots:5,post_levels:level}));assert.match(c.error,/Invalid post/);assert.equal(c.parts,undefined);
  }
  for(const slots of [0,49,2.5,'5',null])assert.ok(box.counts({slots}).error);
});
test('rack BOM locked and unlocked stacks count identically',()=>{
  const {box}=harness(),rack=examples[3][1];assert.deepEqual(plain(box.counts({...rack,layout_locked:true},true)),plain(box.counts({...rack,layout_locked:false},true)));
});
test('rack BOM side panels toggle only segmented panels, never top/bottom',()=>{
  const {box}=harness(),on=plain(box.counts(examples[5][1],true)),off=plain(box.counts(examples[5][1],false));
  assert.deepEqual(off.panels,{});assert.equal(off.parts.panel_top,1);assert.equal(off.parts.panel_bottom,1);
  for(const [key,n] of Object.entries(off.parts))assert.equal(on.parts[key],n);
  assert.equal(off.parts.panel2,undefined);assert.equal(on.parts.panel2,1);
});
test('rack BOM ignores cable guides, ports and artwork',()=>{
  const {box}=harness(),rack={slots:9,cabling:{guides:[{id:'guide'}],ports:[{}]},appearance:{artwork:{sha256:'fixture'}}};
  assert.deepEqual(plain(box.counts(rack,true)),plain(box.counts({slots:9},true)));
});
test('rack BOM agrees with real rackFrame source placements and all fixed parts',()=>{
  const {box}=harness();
  for(const [,rack] of examples)for(const panels of [false,true]){
    const actual={};for(const p of box.frame(rack.slots,panels,rack).parts)actual[p.key]=(actual[p.key]||0)+1;
    assert.deepEqual(actual,plain(box.counts(rack,panels).parts));
  }
});
test('rack BOM requires extensions independently of missing preview assets',()=>{
  const {box}=harness();box.sourceMeshes={};const rack=examples[5][1];
  assert.equal(box.counts(rack).parts.extension,4);
  assert.equal(box.frame(rack.slots,false,rack).parts.filter(p=>p.key==='extension').length,0);
  assert.throws(()=>box.frame(5,false,{slots:5,post_levels:{left:[4]}}),/Invalid post/);
});
test('rack setup height edits retain chosen saved stacks only at unchanged height, clamp at 14U and do not mutate',()=>{
  const {box,get}=harness(),rack={...plain(examples[1][1]),id:'rack',layout_locked:true};
  const before=JSON.stringify(rack);box.documentState.racks=[rack];box.editingId='rack';
  box.setHeight(5);assert.deepEqual(plain(box.editingRack.post_levels),rack.post_levels);
  box.setHeight(9);assert.equal(box.editingRack.post_levels,undefined);assert.equal(box.editingRack.layout_locked,undefined);
  box.setHeight(50);assert.equal(box.editingRack.slots,14);assert.equal(get('rackSlots').value,14);
  box.setHeight(5);assert.deepEqual(plain(box.editingRack.post_levels),rack.post_levels);
  assert.equal(JSON.stringify(rack),before);
});
test('rack BOM shows explicit allowances/UNKNOWNs and invalid layout error',()=>{
  const {box,get}=harness();box.bom(examples[1][1]);
  assert.ok(get('rackBom').children.includes('Full-hole hardware allowance; installed quantity UNKNOWN'));
  assert.ok(get('rackBom').children.includes('Extension and other frame/side-panel fastener quantities: UNKNOWN'));
  box.bom({slots:5,post_levels:{left:[4]}});assert.equal(get('rackBom').children.length,1);assert.match(get('rackBom').children[0],/Invalid post/);
});
test('moving a support refreshes a visible editing BOM; locked layout stays unchanged',()=>{
  const {box,get}=harness(),rack={...plain(examples[3][1]),id:'rack'};box.active=()=>rack;box.editingId='rack';get('rackDialog').open=true;
  box.move('left',0,1);assert.deepEqual(plain(rack.post_levels.left),[4,4]);
  assert.deepEqual(plain(box.editingRack.post_levels.left),[4,4]);assert.ok(get('rackBom').children.includes('8 × 4U post segment'));
  rack.layout_locked=true;box.move('left',0,-1);assert.deepEqual(plain(rack.post_levels.left),[4,4]);
});
test('multi-U plate across a support extension warns (never blocks); 1U and clear spans stay quiet',()=>{
  const {box}=harness();
  vm.runInContext("const uNum=(rack,slot)=>rack.slots-slot+1,uPad=n=>'U'+String(n).padStart(2,'0'),uText=(rack,slot,span=1)=>span>1?uPad(uNum(rack,slot+span-1))+'–'+uPad(uNum(rack,slot)):uPad(uNum(rack,slot));"+section('  // Slots taken by a 1U support extension','  function guideLabel(').replace(/  window\.extensionJointWarning=.*\r?\n/,'')+'\nglobalThis.jw=jointWarning;',box);
  // 10U, posts 5U + extension + 4U on both sides: the extension is slot 5.
  const rack={slots:10,post_levels:{left:[5,4],right:[5,4]}};
  assert.match(box.jw(rack,4,2),/crosses the 1U support extension at U06 \(both sides\).*UNKNOWN.*Warning only/);
  assert.equal(box.jw(rack,5,1),null);
  assert.equal(box.jw(rack,6,3),null);
  assert.equal(box.jw(rack,1,4),null);
  assert.match(box.jw({slots:10,post_levels:{left:[5,4],right:[4,5]}},5,2),/U06 \(left side\) and U05 \(right side\)/);
  assert.equal(box.jw(null,4,2),null);
});
