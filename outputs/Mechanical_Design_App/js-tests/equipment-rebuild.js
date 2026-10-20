'use strict';
// Actual Equipment-list closures in VM; in-memory fetch/DOM fixtures only.
const test=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const src=fs.readFileSync(path.join(__dirname,'..','equipment-wizard.js'),'utf8');
const a=src.indexOf('  let items=[];'),b=src.indexOf('  // Same as rack-studio.js rgb()',a);
assert.ok(a>=0&&b>a);const librarySource=src.slice(a,b);
const clone=x=>JSON.parse(JSON.stringify(x));
function fixture(status='older_source',failure=false){
  const initial={id:'eq-0123456789ab',name:'Router',span:1,spec:{name:'Router',dev_w:85,dev_d:56,dev_h:20},build:'a'.repeat(64),parts:['tray','faceplate']};
  const copy={...clone(initial),id:'eq-ffffffffffff',build:'b'.repeat(64),name:'Router (current template copy)',display_name:'Router (current template copy)'};
  let list=[initial],posts=0,pendingResolve=null;
  const calls=[],events=[],listeners={},nodes=new Map();
  function h(tag,attrs,...children){return {tag,attrs:attrs||{},children,disabled:false,textContent:'',value:attrs?.value,
    replaceChildren(...items){this.children=items;}};}
  const host=h('div');nodes.set('ewLibrary',host);
  const draft={rack:{unsaved:true,placements:[{equipment:initial.id}]},wizard:{name:'Unsaved wizard'}};
  const meshesReady={tray:{fixture:true},faceplate:{fixture:true}};
  const box=vm.createContext({h,token:'fixture-token',initialSpec:clone(draft.wizard),document:{getElementById:id=>nodes.get(id),addEventListener:(name,fn)=>{listeners[name]=fn;}},
    window:{addEventListener:(name,fn)=>{listeners[name]=fn;},dispatchEvent:e=>events.push(e.type)},
    Event:class{constructor(type){this.type=type;}},open(){},render(){},redraw(){},confirm:()=>false,alert(){},
    fetch:async(url,options)=>{
      calls.push({url,options});
      if(url==='/api/equipment-library')return {ok:true,json:async()=>clone(list)};
      if(url==='/api/equipment-template-status')return {ok:true,json:async()=>Object.fromEntries(list.map(it=>[it.id,{status,reason:status==='needs_review'?'The snap-fit tray joint is retired.':'Fixture reason'}]))};
      if(url==='/api/equipment-rebuild-copy'){
        posts++;
        if(failure)return {ok:false,json:async()=>({error:'Fixture render failed'})};
        if(box.hold)await new Promise(resolve=>{pendingResolve=resolve;});
        list=[initial,copy];return {ok:true,json:async()=>({item:copy,reused_build:box.reuse||false})};
      }
      throw Error('Unexpected fixture fetch '+url);
    }});
  vm.runInContext('let spec=initialSpec;\n'+librarySource+'\nglobalThis.load=loadLibrary;globalThis.edit=editItem;globalThis.current=()=>spec;globalThis.parts=partsFor;globalThis.seed=(key,value)=>meshes.set(key,value);',box);
  const flatten=node=>[node,...(node.children||[]).flatMap(c=>typeof c==='object'&&c?flatten(c):[c])];
  const button=()=>flatten(host).find(n=>n?.tag==='button'&&n.children.includes('Rebuild as new item'));
  const allText=()=>flatten(host).map(n=>typeof n==='string'?n:n.textContent||'').join(' ');
  return {box,host,calls,events,listeners,initial,copy,draft,meshesReady,button,allText,
    get posts(){return posts;},release:()=>pendingResolve()};
}
test('equipment list: read-only status on list/focus/open keeps both drafts and grouping',async()=>{
  const h=fixture(),before=clone(h.draft);await h.box.load();
  await h.listeners.focus();await h.listeners.toggle({target:{id:'equipmentSection',open:true}});
  assert.equal(h.posts,0);assert.ok(h.calls.every(c=>!c.options));
  assert.ok(h.allText().includes('Older template/source'));
  assert.ok(h.allText().includes('A newer equipment template is available. The saved build is unchanged. Printed fit and strength remain UNKNOWN.'));
  assert.ok(h.allText().includes('Creates a new library item with the current template. Existing rack placements keep the original. No STL download.'));
  assert.equal(h.button().attrs.class,'ew-chip');assert.deepEqual(h.draft,before);
  assert.deepEqual(clone(h.box.current()),before.wizard);
});
test('equipment list: explicit rebuild posts original identity once and preserves placed item lookup/drafts',async()=>{
  const h=fixture(),before=clone(h.draft);await h.box.load();await h.button().onclick();
  assert.equal(h.posts,1);const post=h.calls.find(c=>c.options);
  assert.equal(post.url,'/api/equipment-rebuild-copy');assert.equal(post.options.method,'POST');
  assert.equal(post.options.headers['X-App-Token'],'fixture-token');
  assert.deepEqual(JSON.parse(post.options.body),{id:h.initial.id,expected_build:h.initial.build});
  assert.ok(h.allText().includes('Created ‘Router (current template copy)’. Existing placements are unchanged. PROPOSED — UNVALIDATED; fit and strength UNKNOWN.'));
  assert.deepEqual(h.draft,before);assert.deepEqual(clone(h.box.current()),before.wizard);
  h.box.seed(h.initial.build,h.meshesReady);h.box.seed(h.copy.build,{tray:{copy:true}});
  assert.equal(h.box.parts(h.initial.id).item.build,h.initial.build);
  assert.equal(h.box.parts(h.copy.id).item.build,h.copy.build);
  assert.equal(h.calls.filter(c=>c.options).length,1);assert.equal(h.button().disabled,false);
});
test('equipment list: double click and focus refresh while rebuilding do not duplicate requests',async()=>{
  const h=fixture();await h.box.load();h.box.hold=true;const old=h.button();const first=old.onclick();
  assert.equal(old.disabled,true);assert.ok(h.allText().includes('Rebuilding a copy…'));
  await old.onclick();await h.listeners.focus();assert.equal(h.button().disabled,true);await h.button().onclick();
  assert.equal(h.posts,1);h.release();await first;assert.equal(h.button().disabled,false);
});
test('equipment list: source match with unknown process offers low-key rebuild and verified-cache wording',async()=>{
  const h=fixture('matches_source_unknown_pipeline');h.box.reuse=true;await h.box.load();
  assert.ok(h.allText().includes('Matches current source; build process unknown'));assert.ok(h.button());
  assert.equal(h.button().attrs.class,'ew-chip');await h.button().onclick();
  assert.ok(h.allText().includes('Created a new item using its verified current-template build. Existing placements are unchanged.'));
});
for(const status of ['needs_review','unknown_evidence','integrity_problem'])test('equipment list: '+status+' has no rebuild and performs no write',async()=>{
  const h=fixture(status);await h.box.load();assert.equal(h.button(),undefined);assert.equal(h.posts,0);
  if(status==='needs_review'){assert.ok(h.allText().includes('Needs review'));assert.ok(h.allText().includes('snap-fit tray joint is retired'));}
});
test('equipment list: rebuild failure keeps drafts and permits retry with exact error text',async()=>{
  const h=fixture('older_source',true);const before=clone(h.draft);await h.box.load();await h.button().onclick();
  assert.equal(h.button().disabled,false);assert.ok(h.allText().includes('Rebuild failed. The original item and your rack draft are unchanged. Fixture render failed'));
  assert.deepEqual(h.draft,before);assert.deepEqual(clone(h.box.current()),before.wizard);
});
test('equipment copy: normal Edit changes separate display name without changing source-producing spec.name',async()=>{
  const h=fixture();await h.box.load();await h.button().onclick();h.box.edit(h.copy);
  assert.equal(h.box.current().name,'Router');assert.equal(h.box.current().display_name,'Router (current template copy)');
  const start=src.indexOf("      const name=h('input'"),end=src.indexOf('\n',start);
  assert.ok(start>=0);const input=vm.runInContext('(()=>{'+src.slice(start,end)+';return name;})()',h.box);
  input.value='Renamed copy';input.oninput();
  assert.equal(h.box.current().display_name,'Renamed copy');assert.equal(h.box.current().name,'Router');
});
