const fs=require('fs'),vm=require('vm'),assert=require('assert');
const root='outputs/Mechanical_Design_App/';const C=require('./catalog.js');
const packs=[1,2,3,4].flatMap(n=>JSON.parse(fs.readFileSync(root+`catalog-packs/phase6-batch${n}.json`)));
const before=JSON.stringify(packs);
assert.equal(C.filter(packs,{head_style:'countersunk',diameter:1}).length,1);
assert.equal(C.filter(packs,{diameter:3.5,kind:'screw'}).length,1);
assert.equal(C.filter(packs,{diameter:3.5,pitch:.6,kind:'heatset',installation_method:'heat or ultrasonic',min_length:7,max_length:8}).length,1);
assert.equal(C.filter(packs,{kind:'screw',material:'A4 stainless steel'}).length,1);
assert.equal(C.filter(packs,{kind:'heatset',head_style:C.unknown}).length,11);
assert.equal(C.filter(packs,{diameter:3.5,pitch:.5}).length,0);
assert.equal(C.filter(packs,{min_length:100}).length,0);
const old=packs[0],newer={...old,revision:2,length:9};
assert.equal(C.filter([old,newer],{latest:true}).length,1);
assert.equal(C.filter([old,newer],{latest:false}).length,2);
const changes=C.changes(old,newer);
assert(changes.some(c=>c.field==='length'&&c.before===8&&c.after===9&&c.effect.includes('reach')));
assert.deepEqual(C.changes(old,{...old}),[]);
assert(C.changes({kind:'heatset'},packs.find(p=>p.kind==='heatset')).some(c=>c.field==='outside_diameter'&&c.before===null));
assert.equal(JSON.stringify(packs),before);
// Exercise actual UI handlers, including the dirty-project import guard and successful explicit import.
const html=fs.readFileSync(root+'index.html','utf8');const source=html.split('<script>')[1].split('</script>')[0].replace('safe(async()=>{await refresh();await loadPacks()});','');
const elements={};function element(){return {value:'',checked:true,children:[],options:[],textContent:'',append(...nodes){this.children.push(...nodes)},replaceChildren(...nodes){this.children=[...nodes];this.options=nodes;this.value=nodes[0]?.value||''},setAttribute(){}}}
const messages=[],calls=[];const box={WorkshopCatalog:C,document:{getElementById:id=>elements[id]||(elements[id]=element()),createElement:element,createElementNS:element},Option:class{constructor(text,value){this.textContent=text;this.value=value}},window:{addEventListener(){},dispatchEvent(){}},CustomEvent:class{},setTimeout(){},clearTimeout(){},URL};vm.createContext(box);vm.runInContext(source,box);
vm.runInContext('api=async(path,body)=>{__calls.push({path,body});return {}};refresh=async()=>{};message=(s,e)=>__messages.push({s,e});',Object.assign(box,{__calls:calls,__messages:messages}));
vm.runInContext('packInventory=[{id:"test-pack",available:true,records:[{id:"test"}]}];dirty=true;',box);elements.catalogPack.value='test-pack';
(async()=>{await elements.importPack.onclick();assert.equal(calls.length,0);assert(messages.at(-1).e);vm.runInContext('dirty=false;',box);await elements.importPack.onclick();assert.equal(calls[0].path,'import');assert.equal(calls[0].body[0].id,'test');vm.runInContext('packInventory[0].available=false;updatePackStatus();',box);assert(elements.importPack.disabled);console.log('Catalog filters, revision search, unknowns, replacement effects and actual explicit-import handlers PASS.');})().catch(e=>{console.error(e);process.exitCode=1});
