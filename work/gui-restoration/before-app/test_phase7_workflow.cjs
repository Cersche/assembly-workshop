const fs=require('fs'),vm=require('vm'),assert=require('assert');
const root='outputs/Mechanical_Design_App/';
const source=fs.readFileSync(root+'index.html','utf8').split('<script>')[1].split('</script>')[0].replace('safe(async()=>{await refresh();await loadPacks()});','');
function setup(){
  const elements={},events=[],messages=[];
  function element(){return {value:'',checked:true,disabled:false,children:[],textContent:'',append(...x){this.children.push(...x)},replaceChildren(...x){this.children=x},setAttribute(){}}}
  const box={document:{getElementById:id=>elements[id]||(elements[id]=element()),createElement:element,createElementNS:element},window:{addEventListener(){},dispatchEvent:e=>events.push(e)},CustomEvent:class{constructor(type,args){this.type=type;this.detail=args.detail}},WorkshopCatalog:require('./catalog.js'),setTimeout(){},clearTimeout(){},URL,Option:class{constructor(text,value){this.textContent=text;this.value=value}}};
  vm.createContext(box);vm.runInContext(source,box);
  box.__messages=messages;
  vm.runInContext('payload=()=>({inputs:{pilot:__pilot},selections:{screw:{id:"s",revision:1}}});message=(m,e)=>__messages.push({m,e});',box);
  box.__pilot=4;
  return {box,elements,events,messages};
}
(async()=>{
  let {box,elements,events,messages}=setup();
  box.__result={id:'a'.repeat(64),cached:false,assembly:{revision:'PROPOSED trial',units:'mm',parts:[]}};
  vm.runInContext('api=async()=>__result',box);
  await elements.buildRevision.onclick();
  assert.equal(elements.downloadBuild.disabled,false);assert.equal(elements.viewProposal.disabled,false);
  assert(events.some(e=>e.type==='assembly-model'&&e.detail.revision==='PROPOSED trial'));
  assert(elements.buildStatus.textContent.includes('millimeters'));assert(elements.buildStatus.textContent.includes('unvalidated'));
  vm.runInContext('markDirty()',box);
  assert(elements.downloadBuild.disabled);assert(elements.viewProposal.disabled);
  assert(events.some(e=>e.type==='assembly-model'&&e.detail===null));
  await elements.downloadBuild.onclick();assert(messages.at(-1).e);assert(messages.at(-1).m.includes('Generate'));
  let resolve;
  box.__pending=new Promise(r=>resolve=r);vm.runInContext('api=async()=>await __pending',box);
  const pending=elements.buildRevision.onclick();box.__pilot=3.9;vm.runInContext('markDirty()',box);resolve(box.__result);await pending;
  assert(elements.downloadBuild.disabled);assert(elements.buildStatus.textContent.includes('older inputs'));assert.equal(elements.buildRevision.disabled,false);
  vm.runInContext('api=async()=>{throw Error("Fixture failed check")}',box);
  await elements.buildRevision.onclick();assert(elements.buildStatus.textContent.includes('Fixture failed'));assert(elements.downloadBuild.disabled);
  box.__pilot=4;vm.runInContext('api=async()=>__result',box);await elements.buildRevision.onclick();
  box.fetch=async()=>({ok:false,json:async()=>({error:'Revision integrity check failed'})});
  await elements.downloadBuild.onclick();assert(messages.at(-1).m.includes('integrity'));
  const html=fs.readFileSync(root+'index.html','utf8');assert(html.includes('STL itself does not encode units'));assert(html.includes('Printer and slicer configuration is outside'));
  console.log('Phase7 actual frontend handlers PASS: matching build, source labels, invalidation, stale completion, failures, integrity error, units/scope text. No visual browser claim.');
})().catch(e=>{console.error(e);process.exitCode=1});
