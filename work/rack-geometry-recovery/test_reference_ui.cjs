// Exercise the new reference viewer with local assets and a disposable DOM stub.
// This is handler/canvas validation, not real-browser visual acceptance.
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const app=path.resolve(__dirname,'../../outputs/Mechanical_Design_App');
const elements=new Map(),requests=[],drawPoints=[];
let failNext=false,release=null;
const context={setTransform(){},fillRect(){},beginPath(){},closePath(){},fill(){},moveTo(x,y){assert(Number.isFinite(x)&&Number.isFinite(y));drawPoints.push([x,y]);},lineTo(x,y){assert(Number.isFinite(x)&&Number.isFinite(y));}};
class Element{
 constructor(tag='div'){this.tag=tag;this.children=[];this.dataset={};this.value='';this.hidden=false;this.clientWidth=420;this.open=false;}
 set id(id){this._id=id;elements.set(id,this);}get id(){return this._id;}
 set innerHTML(text){for(const match of text.matchAll(/<([a-z]+)[^>]*\bid="([^"]+)"[^>]*>/g)){const e=new Element(match[1]);e.id=match[2];}}
 append(...items){this.children.push(...items);if(this.tag==='select'&&!this.value)this.value=items[0]?.value||'';}
 replaceChildren(...items){this.children=[];this.value='';this.append(...items);}
 insertBefore(item){this.children.push(item);}setAttribute(name,value){this[name]=value;}
 getContext(){return context;}showModal(){this.open=true;}close(){this.open=false;}setPointerCapture(){}
}
const toolbar=new Element(),body=new Element();
const document={body,getElementById:id=>elements.get(id),querySelector:()=>toolbar,createElement:tag=>new Element(tag)};
async function fetch(url,options){
 requests.push({url,options});assert(!options,'Reference viewer must not mutate data.');
 if(failNext){failNext=false;return {ok:false,status:409};}
 if(release){const pending=release;release=null;await pending;}
 const data=fs.readFileSync(path.join(app,url));return {ok:true,json:async()=>JSON.parse(data)};
}
vm.runInNewContext(fs.readFileSync(path.join(app,'rack-reference.js'),'utf8'),{document,fetch,window:{devicePixelRatio:1},ResizeObserver:class{observe(){}},console});
const settle=async()=>{for(let i=0;i<5;i++)await new Promise(r=>setImmediate(r));};
(async()=>{
 // Integrity/network errors stay visible; retry must recover.
 failNext=true;await elements.get('openRackReferences').onclick();assert.match(elements.get('rackReferenceStatus').textContent,/409/);
 elements.get('closeRackReferences').onclick();await elements.get('openRackReferences').onclick();await settle();
 assert.match(elements.get('rackReferenceM6').textContent,/Brian supplied.*M6.*UNKNOWN/);
 const tabs=elements.get('rackReferenceTabs').children;assert.equal(tabs.length,3);
 let inspected=0;
 for(const tab of tabs){tab.onclick();await settle();const select=elements.get('rackReferenceComponent');for(const option of [...select.children]){select.value=option.value;await select.onchange();assert.match(elements.get('rackReferenceStatus').textContent,/fit UNKNOWN/);assert.match(elements.get('rackReferenceDimensions').textContent,/local X × Y × Z/);inspected++;}}
 assert.equal(inspected,21);assert(drawPoints.length>10000);
 // A late request for the previous component must not replace current selection.
 tabs[0].onclick();await settle();const select=elements.get('rackReferenceComponent');
 let unblock;release=new Promise(r=>{unblock=r;});select.value=select.children[0].value;const slow=select.onchange();
 select.value=select.children[1].value;await select.onchange();const before=elements.get('rackReferenceMember').textContent;unblock();await slow;assert.equal(elements.get('rackReferenceMember').textContent,before);
 console.log(JSON.stringify({status:'PASS',components:inspected,finite_draw_points:drawPoints.length,fetch_requests:requests.length,checks:['integrity failure retry','all source selections','finite projection','stale selection','read-only requests'],browser_visual_acceptance:false}));
})().catch(e=>{console.error(e);process.exitCode=1;});
