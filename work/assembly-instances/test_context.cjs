const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync('outputs/Mechanical_Design_App/index.html','utf8');
const script=html.split('<script>')[1].split('</script>')[0].replace('safe(async()=>{await refresh();await loadPacks()});','');
const elements={},events=[],calls=[];
function el(){return {value:'',checked:true,disabled:false,children:[],append(...n){this.children.push(...n)},replaceChildren(...n){this.children=n},setAttribute(){}};}
const box={document:{getElementById:id=>elements[id]||(elements[id]=el()),createElement:el,createElementNS:el},window:{workshopContext:null,addEventListener(){},dispatchEvent:e=>events.push(e)},CustomEvent:class{constructor(type,args){Object.assign(this,{type,detail:args?.detail});}},WorkshopCatalog:require('../../outputs/Mechanical_Design_App/catalog.js'),URL,Option:class{},setTimeout(){},clearTimeout(){}};
vm.createContext(box);vm.runInContext(script,box);
box.fetch=async(url,options)=>{calls.push({url,options});return {ok:true,json:async()=>({})};};
(async()=>{
 box.window.workshopContext={id:'asm-slot-a',generation:'g1'};
 await vm.runInContext("api('preview',{inputs:{pilot:4}})",box);
 assert.equal(calls.at(-1).options.headers['X-Assembly-Id'],'asm-slot-a');assert.equal(calls.at(-1).options.headers['X-Workspace-Generation'],'g1');
 await vm.runInContext("api('rack-workspace',{version:2})",box);assert(!('X-Assembly-Id' in calls.at(-1).options.headers));
 assert.equal(vm.runInContext("projectUrl('bom')",box),'/api/bom?assembly=asm-slot-a');
 let resolve;const pendingState=new Promise(r=>resolve=r);box.fetch=async()=>({ok:true,json:()=>pendingState});
 const refresh=vm.runInContext('refresh()',box);await Promise.resolve();box.window.workshopContext={id:'asm-slot-b',generation:'g1'};resolve({project:{id:'asm-slot-a'}});await refresh;
 assert.equal(vm.runInContext('state',box),undefined,'Stale state must not open another slot project.');
 vm.runInContext("state={project:{instance_id:'asm-slot-b',instance_revision:1,selections:{},inputs:{pilot:4}},parts:[]};renderReplacement=()=>{};payload=()=>({instance_revision:state.project.instance_revision,inputs:{pilot:__pilot},selections:{}});dirty=true;",box);
 box.__pilot=4;let saveResolve;const pendingSave=new Promise(r=>saveResolve=r);box.fetch=async()=>({ok:true,json:()=>pendingSave});
 const save=vm.runInContext('save()',box);await Promise.resolve();box.__pilot=3.9;
 saveResolve({name:'Pi4',instance_id:'asm-slot-b',instance_revision:2,workspace_generation:'g2',selections:{},inputs:{pilot:4}});await save;
 assert.equal(vm.runInContext('dirty',box),true,'A newer draft survives an earlier save.');assert.match(elements.dirty.textContent,/newer hardware edits/);assert.equal(events.at(-1).detail.instance_revision,2);
 console.log('PASS scoped headers/BOM, layout scope separation, stale project response rejection, and draft edits made during save.');
 // Pixel-level preview art respects the original mesh coverage and depth buffer.
 const source=fs.readFileSync('outputs/Mechanical_Design_App/viewer.js','utf8').split('async function initAssemblyViewer')[0];const raster={};vm.createContext(raster);vm.runInContext(source,raster);
 const texture={width:1,height:1,data:new Uint8ClampedArray([255,0,0,255])};
 const face={points:[[-4,-4,1],[4,-4,1],[0,4,1]],color:[50,60,70],texture,uv:[[.2,.2],[.2,.2],[.2,.2]]};
 const front={points:[[-1,-1,2],[1,-1,2],[0,1,2]],color:[0,255,0]};
 const output={data:new Uint8ClampedArray(10*10*4)};raster.rasterizeAssemblyFaces([face,front],10,10,1,output);
 const pixel=(x,y)=>Array.from(output.data.slice((y*10+x)*4,(y*10+x)*4+3));
 assert.deepEqual(pixel(0,0),[21,28,38]);assert.deepEqual(pixel(5,7),[255,0,0]);assert.deepEqual(pixel(4,5),[0,255,0]);
 console.log('PASS artwork paints only mesh pixels and remains occluded by nearer geometry.');
})().catch(e=>{console.error(e);process.exitCode=1;});
