'use strict';
// Exercise the wizard's real closures with an in-memory DOM and mocked Save.
const test=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const src=fs.readFileSync(path.join(__dirname,'..','equipment-wizard.js'),'utf8');
const P=require('../port-openings.js');
function fixture(){
  const posts=[];
  const node=(tag)=>({tag,children:[],value:'',textContent:'',
    setAttribute(k,v){this[k]=v;},append(...kids){this.children.push(...kids);}});
  const box=vm.createContext({window:{LabRaxPortOpenings:P,TrayPlacement:require('../tray-placement.js')},document:{createElement:node,getElementById:()=>null},
    setTimeout:()=>{},token:'test',fetch:async(url,options)=>{posts.push({url,spec:JSON.parse(options.body)});return {ok:true,json:async()=>({id:'fixture',name:'Box'})};}});
  const end=src.indexOf('  let items=[];');
  assert.ok(end>0);
  const edit=src.match(/  function editItem\(it\)\{[^\n]+/)[0];
  vm.runInContext(src.slice(0,end)+`
    ${edit}
    render=()=>{};open=()=>reset();
    async function loadLibrary(){}
    reset();
    globalThis.api={reset,finish,body,field,editItem,current:()=>spec};
  })();`,box);
  const all=n=>[n,...(n.children||[]).flatMap(c=>typeof c==='object'?all(c):[c])];
  const finish=()=>box.api.finish();
  const choose=value=>{const select=finish().flatMap(all).find(n=>n.tag==='select');select.value=value;select.onchange();};
  return {api:box.api,posts,finish,choose,all};
}
test('wizard mount selector retains inserts default and explicitly selects all mount choices',()=>{
  const f=fixture();assert.equal(f.api.current().device_mount,'inserts');
  for(const mount of ['pegs','clips','straps','flat','sleeve','inserts']){
    f.choose(mount);assert.equal(f.api.current().device_mount,mount);
  }
});
test('wizard Save blocks no-hole inserts and pegs with pointer; flat reaches Save unchanged',async()=>{
  const f=fixture();
  for(const mount of ['inserts','pegs','flat']){
    f.choose(mount);
    const nodes=f.finish().flatMap(f.all),save=nodes.find(n=>n.tag==='button'&&n.children.includes('Save to equipment library'));
    await save.onclick();
    if(mount!=='flat'){
      assert.equal(f.posts.length,0);
      assert.ok(nodes.some(n=>n.textContent?.includes('Problem: Add at least one mounting hole for inserts or pegs, or choose another tray default mount below (e.g. Sits flat).')));
    }
  }
  assert.equal(f.posts.length,1);assert.equal(f.posts[0].url,'/api/equipment-library');
  assert.equal(f.posts[0].spec.device_mount,'flat');assert.deepEqual(f.posts[0].spec.holes,[]);
});
test('mount changes use shared autoU, retain entered port Z, and protect typed or saved U',()=>{
  const f=fixture(),s=f.api.current();s.dev_h=36;s.ports=[{z:24}];
  f.choose('inserts');assert.equal(s.u,2);
  f.choose('flat');assert.equal(s.u,1);assert.equal(s.ports[0].z,24);
  const input=f.api.field('U','u').children.find(n=>n.tag==='input');
  input.value='4';input.oninput();f.choose('inserts');assert.equal(s.u,4);
  const saved={...s,u:3,device_mount:'straps'};
  f.api.editItem({id:'old',spec:saved});assert.equal(f.api.current().device_mount,'straps');
  f.choose('flat');assert.equal(f.api.current().u,3);
  assert.equal(saved.device_mount,'straps');
  f.api.reset();f.api.current().dev_h=36;f.choose('flat');assert.equal(f.api.current().u,1);
});
test('flat hint points to Ports and wizard note uses current device lift without moving heights',()=>{
  assert.match(P.flatHint({device_mount:'inserts',dev_h:36,standoff:6}),/tray default mount on the Ports step/);
  const f=fixture();f.choose('flat');
  assert.ok(src.includes("'Current device lift is '+window.LabRaxPortOpenings.deviceLift(spec)"));
  assert.ok(src.includes('Entered opening heights stay as entered'));
  assert.equal(P.deviceLift(f.api.current()),3.5);
});
