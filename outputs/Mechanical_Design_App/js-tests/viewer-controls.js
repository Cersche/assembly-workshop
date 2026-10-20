'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const C=require('../viewer-controls.js');
test('viewer button actions and strict four pixel threshold',()=>{
  assert.deepEqual([0,1,2,3].map(C.action),['orbit','pan','pan',null]);
  assert.equal(C.moved({x:0,y:0},{x:4,y:0}),false);
  assert.equal(C.moved({x:0,y:0},{x:3,y:3}),true);
});
test('cursor anchor is invariant across zoom and existing pan',()=>{
  for(const z of [.5,1,2.5,10]){
    const old={zoom:1.3,panX:34,panY:-17},x=-120,y=93,next=C.zoomAt(old,z,x,y);
    assert.ok(Math.abs((x-old.panX)/old.zoom*z+next.panX-x)<1e-10);
    assert.ok(Math.abs((y-old.panY)/old.zoom*z+next.panY-y)<1e-10);
  }
});
test('GPU projection, projected labels and inverse picking agree',()=>{
  const base={matrix:[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
    project:p=>[100+p[0]*100,50-p[1]*50,p[2]],ray:(x,y)=>[x,y]};
  const v={zoom:2,panX:13,panY:-8},out=C.camera(base,200,100,v);
  const p=[.2,.3,.5],q=out.project(p);
  assert.ok(Math.abs(q[0]-(out.matrix[0]*p[0]+out.matrix[12]+1)*100)<1e-5);
  assert.ok(Math.abs(q[1]-(1-out.matrix[5]*p[1]-out.matrix[13])*50)<1e-5);
  assert.deepEqual(out.ray(q[0],q[1]),base.project(p).slice(0,2));
});
function harness(){
  class Target{
    constructor(){this.listeners={};this.style={};this.children=[];}
    addEventListener(k,fn){(this.listeners[k]??=[]).push(fn);}
    emit(k,data={}){const e={pointerId:1,button:0,clientX:100,clientY:100,key:'',preventDefault(){this.prevented=true;},...data};for(const fn of this.listeners[k]||[])fn(e);return e;}
    setAttribute(){} appendChild(c){this.children.push(c);} after(c){this.bar=c;}
    focus(){doc.activeElement=this;}setPointerCapture(){}hasPointerCapture(){return true;}releasePointerCapture(){}
    getBoundingClientRect(){return {left:0,top:0,width:400,height:300};}
  }
  const doc=new Target(),cv=new Target();cv.ownerDocument=doc;
  doc.createElement=()=>new Target();doc.querySelectorAll=()=>[cv];
  let view={yaw:0,pitch:0,zoom:1,panX:0,panY:0},clicks=0,right=0,orbits=0;
  const options={getView:()=>view,setView:v=>view=v,redraw:()=>{},presets:C.presets,
    onClick:()=>clicks++,onRightClick:()=>right++,onOrbit:()=>orbits++};
  C.attach(cv,options);
  return {cv,doc,options,view:()=>view,counts:()=>[clicks,right,orbits]};
}
test('subthreshold clicks, pan versus orbit, and cancel retain selection semantics',()=>{
  const h=harness(),c=h.cv;
  c.emit('pointerdown');c.emit('pointermove',{clientX:103});c.emit('pointerup',{clientX:103});
  assert.deepEqual(h.counts(),[1,0,0]);assert.equal(h.view().yaw,0);
  c.emit('pointerdown',{button:2});c.emit('pointermove',{clientX:120});c.emit('pointerup',{button:2,clientX:120});
  assert.equal(h.view().panX,20);assert.deepEqual(h.counts(),[1,0,0]);
  c.emit('pointerdown');c.emit('pointermove',{clientY:110});c.emit('pointercancel');c.emit('pointerup');
  assert.equal(h.view().pitch,.08);assert.deepEqual(h.counts(),[1,0,1]);
  c.emit('pointerdown',{button:2});c.emit('pointerup',{button:2});
  assert.deepEqual(h.counts(),[1,1,1]);assert.equal(c.emit('contextmenu').prevented,true);
});
test('shortcuts are scoped, do not consume typing/undo, and rebinding is idempotent',()=>{
  const h=harness(),d=h.doc,c=h.cv;
  d.emit('keydown',{key:'1'});assert.equal(h.view().pitch,0);
  c.emit('pointerenter');
  d.emit('keydown',{key:'1',target:{closest:()=>true}});assert.equal(h.view().pitch,0);
  d.emit('keydown',{key:'1',ctrlKey:true});assert.equal(h.view().pitch,Math.PI/2);
  assert.equal(d.emit('keydown',{key:'z',ctrlKey:true}).prevented,undefined);
  C.attach(c,h.options);assert.equal(c.listeners.pointerdown.length,1);
  c.emit('wheel',{deltaY:-100,deltaMode:0});assert.ok(h.view().zoom>1);
  d.emit('keydown',{key:'z'});assert.equal(h.view().zoom,1);assert.equal(h.view().panX,0);
  assert.equal(c.bar.children.length,4);
});
test('pinch zooms and never emits a click after either finger lifts',()=>{
  const h=harness(),c=h.cv;
  c.emit('pointerdown',{pointerId:1,clientX:100});
  c.emit('pointerdown',{pointerId:2,clientX:200});
  c.emit('pointermove',{pointerId:2,clientX:250});
  assert.equal(h.view().zoom,1.5);
  c.emit('pointerup',{pointerId:2,clientX:250});c.emit('pointerup',{pointerId:1});
  assert.deepEqual(h.counts(),[0,0,0]);
});
