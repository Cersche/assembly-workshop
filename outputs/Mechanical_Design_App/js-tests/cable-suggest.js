'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),vm=require('node:vm'),cp=require('node:child_process'),path=require('node:path');
const S=require('../cable-suggest.js'),C=require('../cable-routes.js'),P=require('../cable-ports.js');
const port=(allocation,p)=>({allocation,port:p});
function fixture(){
  const ctx={ports:P,cables:C,newId:()=> 'new-guide',library:[{id:'wizard',name:'Switch',spec:{u:1,dev_d:80,
    ports:[{id:'front-left',x:-40,z:20,type:'rj45'}],rear_ports:[
      {id:'rear-left',x:-40,z:20,type:'rj45'},{id:'rear-right',x:40,z:20,type:'iec'},
      {id:'usb',x:0,z:20,type:'usb-c',label:'USB data'}],keystones:[0]}}]};
  const rack={slots:6,placements:[{id:'pi',equipment:'pi4',slot:1,span:1},
    {id:'w1',equipment:'wizard',slot:2,span:1},{id:'w2',equipment:'wizard',slot:5,span:1}],
    cabling:{guides:[],exits:[],endpoints:[{id:'desk',kind:'desk',name:'Desk'}],cables:[]}};
  const c={id:'c1',number:'C1',type:'rj45',service_loop_m:0.15,from:port('w1','rear-left'),to:port('w2','rear-left'),
    route:{mode:'manual',guides:[],exit:null}};
  rack.cabling.cables.push(c);return {rack,ctx,c};
}
function guide(rack,post,slot){const g={id:post+slot,kind:'labrax-cable-guide',post,slot};rack.cabling.guides.push(g);return g.id;}
function exit(rack,id,position='bottom-rear',slot=6){rack.cabling.exits.push({id,position,slot});return id;}
const rule=(rack,ctx,name)=>S.suggestions(rack,ctx).filter(s=>s.rule===name);
const one=(f,name)=>{const items=rule(f.rack,f.ctx,name);assert.equal(items.length,1,name);return items[0];};
function shape(rack){
  // Run the real Python save-schema validator against JSON on stdin; no files or user data.
  const script='import json,sys; import rack_workspace; r=json.load(sys.stdin); rack_workspace._cabling(r["cabling"],r["slots"],{p["id"]:p["span"] for p in r["placements"]}); print("valid")';
  const result=cp.spawnSync('C:/Program Files/Python310/python.exe',['-B','-c',script],
    {cwd:path.resolve(__dirname,'..'),input:JSON.stringify(rack),encoding:'utf8'});
  assert.equal(result.status,0,result.stderr||String(result.error));assert.match(result.stdout,/valid/);
}
test('exact API and standalone browser global without DOM, window or fetch',()=>{
  assert.deepEqual(Object.keys(S).sort(),['RULES','BEND_FACTOR','carries','powerPost','dataPost','suggestions','applySuggestion','ignore','unignore','pruneIgnored'].sort());
  assert.deepEqual(Object.keys(S.RULES),['power-post','missing-guide','one-exit','top-exit','keystone','service-loop','short-run','bend','crowded','one-ended','unused-ports','adapter']);
  assert.deepEqual(S.BEND_FACTOR,{rj45:4,other:10});
  const sandbox={};vm.runInNewContext(fs.readFileSync(require.resolve('../cable-suggest.js'),'utf8'),sandbox);
  assert.deepEqual(Object.keys(sandbox),['LabRaxCableSuggest']);
});
test('carries defaults, USB label/id at either end, overrides and post settings',()=>{
  const {rack,ctx,c}=fixture();
  for(const type of Object.keys(C.TYPE_STYLE)){c.type=type;assert.equal(S.carries(rack,c,ctx),['iec','dc-barrel'].includes(type)?'power':'data');}
  c.type='usb-c';c.from=port('pi','usb-c-power');assert.equal(S.carries(rack,c,ctx),'power');
  c.from=port('w1','usb');c.to=port('w2','usb');assert.equal(S.carries(rack,c,ctx),'data');
  ctx.library[0].spec.rear_ports[2].label='POWER input';assert.equal(S.carries(rack,c,ctx),'power');
  c.carries='data';assert.equal(S.carries(rack,c,ctx),'data');c.carries='power';c.type='rj45';assert.equal(S.carries(rack,c,ctx),'power');
  delete c.carries;ctx.library[0].spec.rear_ports[2].label='USB';c.type='usb-c';c.to=port('pi','usb-c-power');assert.equal(S.carries(rack,c,ctx),'power');
  assert.equal(S.powerPost(rack),'RR');assert.equal(S.dataPost(rack),'RL');rack.cabling.settings={power_post:'RL'};
  assert.equal(S.powerPost(rack),'RL');assert.equal(S.dataPost(rack),'RR');
});
test('power-post wrong rear side, crossing, reverse interval, front exclusion and no target',()=>{
  const f=fixture(),{rack,ctx,c}=f;c.type='iec';c.route.guides=[guide(rack,'RL',2),guide(rack,'RL',5)];
  let s=one(f,'power-post');assert.equal(s.apply,null);assert.match(s.detail,/Add a guide on RR first/);
  guide(rack,'RR',1);guide(rack,'RR',3);guide(rack,'RR',4);guide(rack,'RR',6);
  s=one(f,'power-post');assert.deepEqual(s.apply,{kind:'move-post',cable:'c1',guides:['RR3','RR4']});
  [c.from,c.to]=[c.to,c.from];assert.deepEqual(one(f,'power-post').apply.guides,['RR4','RR3']);
  c.route.guides.push('RR3');assert.match(one(f,'power-post').detail,/crosses between the rear posts/);
  c.route.guides=['RR3'];assert.equal(rule(rack,ctx,'power-post').length,0);
  c.route.guides=[guide(rack,'FL',3),'RL2'];assert.equal(rule(rack,ctx,'power-post').length,0);
  c.route.guides=[];assert.equal(rule(rack,ctx,'power-post').length,0);
});
test('missing-guide merges cables, rounds midpoint, skips occupied spots, short gaps and multiple posts',()=>{
  const f=fixture(),{rack,ctx,c}=f;
  rack.cabling.cables.push({...structuredClone(c),id:'c2',number:'C2',from:port('w1','ks-1-rear'),to:port('w2','ks-1-rear')});
  // Keystone X=0 would choose RR; make this cable explicitly follow RL.
  rack.cabling.cables[1].route.guides=[guide(rack,'RL',2)];
  let s=one(f,'missing-guide');assert.equal(s.id,'missing-guide:RL:4');assert.deepEqual(s.involves.cables,['c1','c2']);
  assert.match(s.title,/RL U04/);guide(rack,'RL',4);assert.equal(rule(rack,ctx,'missing-guide').length,0);
  rack.cabling.guides=[];rack.cabling.cables=[c];c.route.guides=[guide(rack,'RL',2),guide(rack,'RR',3)];
  assert.equal(rule(rack,ctx,'missing-guide').length,0);c.route.guides=[];rack.placements[2].slot=4;
  assert.equal(rule(rack,ctx,'missing-guide').length,0);
});
test('missing-guide uses anchors, front/mean-X post, exit slots and absent endpoint fallback',()=>{
  const f=fixture(),{rack,ctx,c}=f;c.from=port('w1','front-left');c.to=port('w2','front-left');assert.equal(one(f,'missing-guide').apply.post,'FL');
  c.from=port('w1','rear-right');c.to=port('w2','rear-right');assert.equal(one(f,'missing-guide').apply.post,'RR');
  c.to={endpoint:'desk'};assert.equal(rule(rack,ctx,'missing-guide').length,0);
  c.route.exit=exit(rack,'bottom');assert.equal(one(f,'missing-guide').apply.slot,4);
  [c.from,c.to]=[c.to,c.from];assert.equal(one(f,'missing-guide').apply.slot,4);
  c.from=null;c.to=null;assert.equal(rule(rack,ctx,'missing-guide').length,0);
  c.from=port('w1','rear-left');c.to=port('w2','rear-left');rack.placements[1].span=2;
  assert.equal(rule(rack,ctx,'missing-guide').length,0);
});
function exitFixture(){
  const f=fixture(),{rack,c}=f;
  exit(rack,'top','top-rear',1);exit(rack,'left','left',3);exit(rack,'bottom');
  c.to={endpoint:'desk'};c.route.exit='top';
  for(const [i,e] of ['top','bottom','left'].entries())rack.cabling.cables.push({
    ...structuredClone(c),id:'c'+(i+2),number:'C'+(i+2),from:null,route:{mode:'manual',guides:[],exit:e}});
  return f;
}
test('one-exit prefers non-top even with fewer users; ties follow exit order; all-top fallback',()=>{
  const f=exitFixture(),{rack,ctx}=f;let s=one(f,'one-exit');assert.equal(s.apply.exit,'left');assert.deepEqual(s.apply.cables,['c1','c2','c3']);
  rack.cabling.cables[1].route.exit='bottom';assert.equal(one(f,'one-exit').apply.exit,'bottom');
  rack.cabling.exits=rack.cabling.exits.filter(e=>e.id!=='left');rack.cabling.cables.pop();
  rack.cabling.exits[1].position='top-rear';assert.equal(one(f,'one-exit').apply.exit,'bottom');
  rack.cabling.cables.forEach(c=>c.route.exit='top');assert.equal(rule(rack,ctx,'one-exit').length,0);
  rack.cabling.cables.forEach(c=>c.to=null);assert.equal(rule(rack,ctx,'one-exit').length,0);
});
test('top-exit most-used alternative, first unused alternative, no alternative and unused top',()=>{
  const f=exitFixture(),{rack,ctx}=f;assert.equal(one(f,'top-exit').apply.exit,'left');
  rack.cabling.cables[1].route.exit='bottom';assert.equal(one(f,'top-exit').apply.exit,'bottom');
  rack.cabling.cables[1].to=port('w2','rear-right');assert.equal(one(f,'top-exit').apply.exit,'bottom');
  rack.cabling.cables=[rack.cabling.cables[0]];assert.equal(one(f,'top-exit').apply.exit,'left');
  rack.cabling.exits=rack.cabling.exits.slice(0,1);assert.equal(one(f,'top-exit').apply,null);
  rack.cabling.cables=[];assert.equal(rule(rack,ctx,'top-exit').length,0);
});
test('keystone and service-loop positive and negative rules',()=>{
  const f=fixture(),{rack,ctx,c}=f;assert.equal(rule(rack,ctx,'keystone').length,0);
  c.unplug_often=true;assert.equal(one(f,'keystone').apply,null);
  c.to=port('w2','ks-1-rear');assert.equal(rule(rack,ctx,'keystone').length,0);
  c.to=port('w2','rear-left');c.from=port('w1','ks-1-front');assert.equal(rule(rack,ctx,'keystone').length,0);
  c.service_loop_m=0;assert.equal(one(f,'service-loop').apply,null);
  delete c.service_loop_m;rack.cabling.settings={service_loop_m:0};one(f,'service-loop');
  delete rack.cabling.settings;assert.equal(rule(rack,ctx,'service-loop').length,0);
  c.service_loop_m=0;c.from=null;c.to={endpoint:'desk'};assert.equal(rule(rack,ctx,'service-loop').length,0);
});
test('short-run strictly less than U, with two known port anchors and guides',()=>{
  const f=fixture(),{rack,ctx,c}=f;c.route.guides=[guide(rack,'RL',2)];rack.placements[2].slot=2;
  assert.equal(one(f,'short-run').apply.kind,'drop-guides');rack.placements[2].slot=3;
  assert.equal(rule(rack,ctx,'short-run').length,0);rack.placements[2].slot=2;c.to={endpoint:'desk'};
  assert.equal(rule(rack,ctx,'short-run').length,0);c.to=port('w2','gone');assert.equal(rule(rack,ctx,'short-run').length,0);
  c.to=port('w2','rear-left');c.route.guides=[];assert.equal(rule(rack,ctx,'short-run').length,0);
});
test('bend right-angle math, tight guide mapping, straight line, threshold and generic factor',()=>{
  const f=fixture(),{rack,ctx,c}=f;c.route.guides=[guide(rack,'RL',3)];
  let points=[[0,0,0],[20,0,0],[20,20,0]];ctx.cables={...C,path:()=>points};
  let s=one(f,'bend');assert.equal(s.level,'guidance');assert.match(s.detail,/1 tight turn; tightest radius 10 mm/);
  assert.match(s.detail,/Nominal sizes, guidance only/);assert.deepEqual(s.involves.guides,['RL3']);assert.equal(s.apply,null);
  points=[[0,0,0],[100,0,0],[100,100,0]];assert.equal(rule(rack,ctx,'bend').length,0);
  c.type='iec';assert.match(one(f,'bend').detail,/generic rule of thumb/);
  points=[[0,0,0],[20,0,0],[40,0,0]];assert.equal(rule(rack,ctx,'bend').length,0);
  points=[[0,0,0],[0,0,0],[20,0,0]];assert.equal(rule(rack,ctx,'bend').length,0);
  points=[[0,0,0],[20,0,0],[0,0,0]];assert.match(one(f,'bend').detail,/radius 0 mm/);
});
test('crowded uses user threshold and UNKNOWN, one-ended and aggregated unused ports',()=>{
  const f=fixture(),{rack,ctx,c}=f;c.route.guides=[guide(rack,'RL',3)];rack.cabling.settings={guide_warn_above:1};
  assert.equal(rule(rack,ctx,'crowded').length,0);rack.cabling.cables.push({...structuredClone(c),id:'c2',number:'C2',from:null,to:null});
  let s=one(f,'crowded');assert.match(s.detail,/2 cables exceeds your setting of 1. Capacity is UNKNOWN/);assert.deepEqual(s.involves.cables,['c1','c2']);
  assert.equal(one(f,'one-ended').id,'one-ended:c2');rack.cabling.cables.pop();assert.equal(rule(rack,ctx,'one-ended').length,0);
  let unused=rule(rack,ctx,'unused-ports');assert.equal(unused.length,3);assert.match(unused.find(s=>s.id.endsWith(':w1')).title,/Switch \(U\d\d\): 5 of 6 ports unused/);
  rack.placements[1].assembly={name:'Named'};assert.match(rule(rack,ctx,'unused-ports').find(s=>s.id.endsWith(':w1')).title,/Named \(U\d\d\):/);
  ctx.cables={...C,portInUse:()=> 'occupied'};assert.equal(rule(rack,ctx,'unused-ports').length,0);
});
test('move-post and drop-guides apply keep exits, make manual and pass real Python validation',()=>{
  const f=fixture(),{rack,ctx,c}=f;c.type='iec';c.route.guides=[guide(rack,'RL',3)];guide(rack,'RR',3);
  c.route.exit=exit(rack,'bottom');const outsideBefore=JSON.stringify({slots:rack.slots,placements:rack.placements});
  assert.equal(S.applySuggestion(rack,one(f,'power-post'),ctx).ok,true);
  assert.deepEqual(rack.cabling.cables[0].route,{mode:'manual',guides:['RR3'],exit:'bottom'});shape(rack);
  rack.placements[2].slot=2;assert.equal(S.applySuggestion(rack,one(f,'short-run'),ctx).ok,true);
  assert.deepEqual(rack.cabling.cables[0].route,{mode:'manual',guides:[],exit:'bottom'});shape(rack);
  rack.placements[2].slot=5;assert.equal(JSON.stringify({slots:rack.slots,placements:rack.placements}),outsideBefore);
});
test('add-guide applies to auto routes, leaves manual guides alone, validates, refuses occupied spot',()=>{
  const f=fixture(),{rack,ctx,c}=f;c.route.mode='auto';const s=one(f,'missing-guide');
  rack.cabling.cables.push({...structuredClone(c),id:'c2',number:'C2',from:port('w1','front-left'),to:port('w2','front-left'),route:{mode:'manual',guides:[],exit:null}});
  assert.equal(S.applySuggestion(rack,s,ctx).ok,true);assert.equal(rack.cabling.guides[0].id,'new-guide');
  assert.deepEqual(rack.cabling.cables[0].route.guides,['new-guide']);assert.deepEqual(rack.cabling.cables[1].route.guides,[]);shape(rack);
  const before=JSON.stringify(rack);assert.equal(S.applySuggestion(rack,s,ctx).ok,false);assert.equal(JSON.stringify(rack),before);
  const f2=fixture();delete f2.ctx.newId;assert.equal(S.applySuggestion(f2.rack,one(f2,'missing-guide'),f2.ctx).ok,true);
  assert.match(f2.rack.cabling.guides[0].id,/^guide-[0-9a-f]{12}$/);shape(f2.rack);
});
test('set-exit apply keeps guides and passes real schema for one-exit and top-exit',()=>{
  for(const name of ['one-exit','top-exit']){
    const f=exitFixture(),{rack,ctx}=f;rack.cabling.cables[0].route.guides=[guide(rack,'RL',3)];
    const s=one(f,name);assert.equal(S.applySuggestion(rack,s,ctx).ok,true);
    for(const id of s.apply.cables){const c=rack.cabling.cables.find(c=>c.id===id);assert.equal(c.route.mode,'manual');assert.equal(c.route.exit,s.apply.exit);}
    assert.deepEqual(rack.cabling.cables[0].route.guides,['RL3']);shape(rack);
  }
});
test('every apply kind refuses stale involved cable, guide and exit without mutation',()=>{
  for(const kind of ['move-post','add-guide','set-exit','drop-guides'])for(const key of ['cables','guides','exits']){
    const f=fixture(),{rack,ctx,c}=f;const g=guide(rack,'RL',3),e=exit(rack,'bottom');
    const apply={kind,cable:c.id,cables:[c.id],guides:[g],exit:e,post:'RR',slot:4};
    const s={apply,involves:{cables:[c.id],guides:[g],exits:[e],ports:[]}};
    rack.cabling[key]=[];const before=JSON.stringify(rack);
    assert.equal(S.applySuggestion(rack,s,ctx).ok,false,kind+' '+key);assert.equal(JSON.stringify(rack),before);
  }
});
test('apply refuses stale action targets/retained routes, duplicate ids and invalid spots; upkeep failure is atomic',()=>{
  const f=fixture(),{rack,ctx,c}=f;
  const s=one(f,'missing-guide');guide(rack,'RR',1);ctx.newId=()=> 'RR1';
  const before=JSON.stringify(rack);assert.equal(S.applySuggestion(rack,s,ctx).ok,false);assert.equal(JSON.stringify(rack),before);
  for(const apply of [{kind:'move-post',cable:'gone',guides:[]},{kind:'set-exit',cables:['c1'],exit:'gone'},
    {kind:'add-guide',post:'XX',slot:3},{kind:'add-guide',post:'RR',slot:7},{kind:'add-guide',post:'RR',slot:1.5},
    {kind:'move-post',cable:'c1',guides:['RR1','RR1']},{kind:'unknown'}]){
    assert.equal(S.applySuggestion(rack,{apply},ctx).ok,false);assert.equal(JSON.stringify(rack),before);
  }
  c.route.guides=['gone'];const stale=JSON.stringify(rack);
  assert.equal(S.applySuggestion(rack,{apply:{kind:'drop-guides',cable:c.id}},ctx).ok,false);assert.equal(JSON.stringify(rack),stale);
  c.route.guides=[];ctx.newId=()=> 'fresh';ctx.cables={...C,upkeep:()=>{throw Error('test failure');}};
  const prior=JSON.stringify(rack);assert.equal(S.applySuggestion(rack,s,ctx).ok,false);assert.equal(JSON.stringify(rack),prior);
});
test('signatures stable, 8-hex, change for every specified involved field',()=>{
  const f=fixture(),{rack,ctx,c}=f;c.unplug_often=true;c.route.guides=[guide(rack,'RL',3)];c.route.exit=exit(rack,'bottom');
  const baseline=one(f,'keystone').sig;assert.match(baseline,/^[0-9a-f]{8}$/);assert.equal(one(f,'keystone').sig,baseline);
  const mutations=[r=>r.cabling.cables[0].from=port('pi','ethernet'),r=>r.cabling.cables[0].to=null,
    r=>r.cabling.cables[0].type='iec',r=>r.cabling.cables[0].carries='power',r=>r.cabling.cables[0].route.mode='auto',
    r=>r.cabling.cables[0].service_loop_m=0,r=>r.cabling.guides[0].post='RR',r=>r.cabling.guides[0].slot=4,
    r=>r.cabling.exits[0].position='left',r=>r.cabling.exits[0].slot=5];
  for(const mutate of mutations){const other=structuredClone(rack);mutate(other);assert.notEqual(rule(other,ctx,'keystone')[0].sig,baseline);}
  c.from=null;let sig=one(f,'one-ended').sig;c.unplug_often=false;assert.notEqual(one(f,'one-ended').sig,sig);
  const copy=structuredClone(rack);copy.cabling.cables[0].note='not involved';assert.equal(rule(copy,ctx,'one-ended')[0].sig,one(f,'one-ended').sig);
});
test('ignore includes matching sig only, unignore cleans empty key, pruning changes/disappearance',()=>{
  const f=fixture(),{rack,ctx,c}=f;c.unplug_often=true;const s=one(f,'keystone');S.ignore(rack,s);
  assert.equal(rule(rack,ctx,'keystone').length,0);assert.equal(S.suggestions(rack,ctx,{includeIgnored:true}).find(x=>x.id===s.id).ignored,true);
  assert.equal(S.pruneIgnored(rack,ctx),0);S.unignore(rack,s.id);assert.ok(!('ignored_suggestions' in rack.cabling.settings));
  S.ignore(rack,s);c.service_loop_m=0;assert.equal(one(f,'keystone').ignored,false);assert.equal(S.pruneIgnored(rack,ctx),1);
  assert.ok(!('ignored_suggestions' in rack.cabling.settings));S.ignore(rack,one(f,'keystone'));c.unplug_often=false;
  assert.equal(S.pruneIgnored(rack,ctx),1);assert.equal(S.pruneIgnored({},ctx),0);S.unignore({},'missing');
});
test('ignore replaces and caps at 500 dropping oldest; saved shape accepted',()=>{
  const {rack}=fixture();for(let i=0;i<501;i++)S.ignore(rack,{id:'rule:'+i,sig:'01234567'});
  assert.equal(rack.cabling.settings.ignored_suggestions.length,500);assert.equal(rack.cabling.settings.ignored_suggestions[0].id,'rule:1');
  S.ignore(rack,{id:'rule:1',sig:'abcdef12'});assert.equal(rack.cabling.settings.ignored_suggestions.length,500);
  assert.deepEqual(rack.cabling.settings.ignored_suggestions.at(-1),{id:'rule:1',sig:'abcdef12'});shape(rack);
});
test('suggestion shapes, rule/subject sorting, idempotence and no input mutation',()=>{
  const f=exitFixture(),{rack,ctx}=f;rack.cabling.cables[0].unplug_often=true;
  const before=JSON.stringify(rack),a=S.suggestions(rack,ctx),b=S.suggestions(rack,ctx);
  assert.deepEqual(a,b);assert.equal(JSON.stringify(rack),before);
  const order=Object.keys(S.RULES);for(let i=0;i<a.length;i++){
    const s=a[i];assert.deepEqual(Object.keys(s).sort(),['id','rule','level','title','detail','involves','apply','applyLabel','sig','ignored'].sort());
    assert.deepEqual(Object.keys(s.involves),['cables','guides','ports','exits']);
    assert.ok(s.id.startsWith(s.rule+':'));assert.equal(s.ignored,false);
    if(i)assert.ok(order.indexOf(a[i-1].rule)<order.indexOf(s.rule)||(a[i-1].rule===s.rule&&a[i-1].id<=s.id));
  }
  assert.deepEqual(S.suggestions({slots:6},ctx),[]);assert.equal(S.applySuggestion(rack,{apply:null},ctx).ok,false);
});

test('adapter advice is info only, exact, ignorable and pruned when resolved',()=>{
  const f=fixture(),{rack,ctx,c}=f;
  rack.cabling.ports=[{allocation:'w2',port:'rear-left',type:'usb-a'}];
  const before=structuredClone({rack,library:ctx.library}),s=one(f,'adapter');
  assert.equal(S.RULES.adapter,'Plan an adapter cable');assert.equal(s.title,'C1 needs an adapter cable');
  assert.equal(s.detail,'One end is RJ45 (Ethernet), the other USB-A. Plan an adapter cable or adapter; its fit is UNKNOWN.');
  assert.equal(s.level,'info');assert.equal(s.apply,null);assert.equal(s.applyLabel,null);
  assert.deepEqual(s.involves,{cables:['c1'],guides:[],ports:['w1/rear-left','w2/rear-left'],exits:[]});
  assert.equal(S.applySuggestion(rack,s,ctx).ok,false);assert.deepEqual({rack,library:ctx.library},before);
  S.ignore(rack,s);assert.equal(rule(rack,ctx,'adapter').length,0);assert.equal(S.pruneIgnored(rack,ctx),0);
  rack.cabling.ports[0].type='rj45';assert.equal(S.pruneIgnored(rack,ctx),1);assert.equal(rule(rack,ctx,'adapter').length,0);
  for(const end of [null,{endpoint:'desk'},port('w2','removed')]){c.to=end;assert.equal(rule(rack,ctx,'adapter').length,0);}
});
