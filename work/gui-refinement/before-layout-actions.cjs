const assert=require('assert'),fs=require('fs'),vm=require('vm');
const A=require('../../outputs/Mechanical_Design_App/rack-references/rack-layout.js');
const p=(id,slot,span=1)=>({id,equipment:'pi4',slot,span,fit:'UNKNOWN',geometry:'pi4-clearance-v2-reference'});
const rack={id:'r',slots:5,placements:[p('one',1),p('two',2,2)]};
const before=JSON.stringify(rack);assert.throws(()=>A.change(rack,'two',1,2),/overlaps/);assert.equal(JSON.stringify(rack),before);
assert.throws(()=>A.change(rack,'two',5,2),/within/);assert.equal(JSON.stringify(rack),before);
A.change(rack,'two',4,2);assert.equal(rack.placements[1].slot,4);
const record=A.release(rack,'two');assert.equal(rack.placements.length,1);A.restore(rack,record);assert.equal(rack.placements[1].slot,4);
A.release(rack,'two');rack.slots=3;assert.throws(()=>A.restore(rack,record),/within/);assert.equal(rack.placements.length,1);
rack.slots=5;rack.placements.push(p('other',5));assert.throws(()=>A.restore(rack,record),/overlaps/);assert.equal(rack.placements.length,2);
// Exercise the actual workspace save handler against a controllable asynchronous API.
const source=fs.readFileSync('outputs/Mechanical_Design_App/workspace.js','utf8');
const save=source.slice(source.indexOf("byId('saveLayout').onclick=async()=>"),source.indexOf("\n  byId('rackChoice')"));
const mark=source.slice(source.indexOf('function markChanged()'),source.indexOf('  function button('));
const elements={saveLayout:{},mountWizard:{hidden:true},rackDialog:{open:false},layoutSaveStatus:{}};
const messages=[],resolves=[];
const box={byId:id=>elements[id],notify:m=>messages.push(m),render(){},api:async()=>new Promise(resolve=>resolves.push(resolve))};
vm.createContext(box);vm.runInContext("let capable=true,openingAssembly=false,projectBusy=false,persistedAssemblyIds=new Set();let window={};let documentState={version:2,generation:null,racks:[]},layoutDirty=true,savingLayout=false;"+mark+save,box);
(async()=>{
 const first=elements.saveLayout.onclick();assert.equal(resolves.length,1);
 vm.runInContext("documentState.racks.push({id:'new draft',placements:[]});markChanged();",box);assert.equal(elements.saveLayout.disabled,true);
 await elements.saveLayout.onclick();assert.equal(resolves.length,1);
 resolves[0]({version:1,generation:'g1',racks:[]});await first;
 assert.equal(vm.runInContext('documentState.generation',box),'g1');assert.equal(vm.runInContext('documentState.racks.length',box),1);assert.equal(vm.runInContext('layoutDirty',box),true);assert.equal(elements.saveLayout.disabled,false);
 elements.mountWizard.hidden=false;await elements.saveLayout.onclick();assert.equal(resolves.length,1);assert.match(messages.at(-1),/Apply or cancel/);elements.mountWizard.hidden=true;
 const second=elements.saveLayout.onclick();resolves[1]({version:1,generation:'g2',racks:[{id:'new draft',placements:[]}]});await second;assert.equal(vm.runInContext('layoutDirty',box),false);assert.equal(elements.saveLayout.disabled,true);
 console.log('PASS allocation move/resize/release/undo guards; actual save handler serializes requests and preserves newer edits.');
})().catch(e=>{console.error(e);process.exitCode=1;});
