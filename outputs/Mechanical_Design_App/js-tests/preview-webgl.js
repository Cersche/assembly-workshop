'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const S=require('../rack-studio.js');
test('small preview GPU matrix matches the original painter camera within half a pixel',()=>{
  for(const [yaw,pitch,zoom,panX,panY] of [[0,0,1,0,0],[.55,.65,1.2,17,-23],[-1.2,Math.PI/2,.4,-45,80],[Math.PI,-.5,3,5,7]])for(const dpr of [.6,1,1.5,2]){
    const view={yaw,pitch,zoom,panX,panY,cen:[4,36,21],span:280},W=800*dpr,H=500*dpr,cam=S.previewCamera(view,W,H,dpr),m=cam.matrix;
    for(const p of [[0,0,0],[85,56,20],[-120,220,44.4],[10,-30,100]]){
      const [x,y,z]=p.map((n,i)=>n-view.cen[i]),cy=Math.cos(yaw),sy=Math.sin(yaw),cp=Math.cos(pitch),sp=Math.sin(pitch),sc=Math.min(W,H)/280*zoom;
      const expected=[W/2+panX*dpr+(x*cy-y*sy)*sc,H/2+panY*dpr-(sp*(x*sy+y*cy)+z*cp)*sc];
      const clip=[0,1,2].map(k=>m[k]*p[0]+m[4+k]*p[1]+m[8+k]*p[2]+m[12+k]),gpu=[(clip[0]+1)*W/2,(1-clip[1])*H/2];
      gpu.forEach((n,i)=>assert.ok(Math.abs(n-expected[i])<.5));
      assert.ok(Math.abs(clip[2]*100000-cam.project(p)[2])<.01);
    }
  }
});
test('small preview switch, context restore and ten-frame quality budget boundaries',()=>{
  for(const opts of [{available:false},{preference:'canvas'},{lost:true},{forced:true}])assert.equal(S.previewSwitch(opts).renderer,'canvas');
  assert.equal(S.previewSwitch({lost:false}).renderer,'webgl');
  const check=(level,ms,n=10)=>S.previewSwitch({level,times:Array(n).fill(ms)});
  assert.equal(check('high',17,9).level,'high');assert.equal(check('high',16).level,'high');
  assert.equal(check('high',17).level,'medium');assert.equal(check('medium',17).level,'low');
  assert.equal(check('low',33).renderer,'webgl');assert.equal(check('low',33.01).renderer,'canvas');
  assert.equal(S.median([10,1,5,8]),6.5);
});
test('small preview uploads once for camera changes and equal recreated tray arrays',()=>{
  let uploads=0;const R=Object.create(S.PreviewRenderer.prototype);R.buffers=new Map();R.identities=new WeakMap();R.records=[];R.uploads=0;
  R.gl={createBuffer:()=>({}),bindBuffer(){},bufferData(){uploads++;}};
  const a=[0,0,0,1,0,0,0,1,0],first=R.geometryFor(a);
  for(let i=0;i<25;i++)assert.equal(R.geometryFor(a),first);
  assert.equal(R.geometryFor([...a]),first);assert.equal(uploads,1);
  assert.notEqual(R.geometryFor(a,1),first);assert.equal(uploads,2);
  assert.notEqual(R.geometryFor([0,0,0,2,0,0,0,1,0]),first);assert.equal(uploads,3);
});
test('feature edges: cube has twelve, subdivided flat square has four',()=>{
  const m=new S.Mesh();m.box(-1,1,-1,1,-1,1);const v=m.triangles.flatMap(t=>t.flatMap(i=>m.vertices[i]));
  assert.equal(S.featureEdges(v).length/6,12);
  const out=[];for(let x=0;x<2;x++)for(let y=0;y<2;y++)out.push(x,y,0,x+1,y,0,x+1,y+1,0,x,y,0,x+1,y+1,0,x,y+1,0);
  assert.equal(S.featureEdges(out).length/6,4);
});
test('painter coalesces demand frames, stays idle, falls back, disposes and restores',()=>{
  const source=fs.readFileSync(path.join(__dirname,'../equipment-wizard.js'),'utf8');
  const adapter=source.slice(source.indexOf('  const painters=new WeakMap();'),source.indexOf("  if(typeof module!=='undefined'&&module.exports){module.exports={findFeet"));
  let uploads=0,draws=0,canvasDraws=0,disposed=0,observed=0,preference='',now=0;const frames=new Map(),events={},close=[];
  class FakeRenderer{constructor(){this.canvas={addEventListener:(k,f)=>events[k]=f,removeEventListener:(k)=>delete events[k]};this.init();}init(){this.triangles=1;}draw(){draws++;return this.canvas;}dispose(){disposed++;}}
  const box={WeakMap,MutationObserver:class{observe(){observed++;}disconnect(){observed--;}},requestAnimationFrame:f=>{frames.set(++uploads,f);return uploads;},cancelAnimationFrame:id=>frames.delete(id),performance:{now:()=>now++},devicePixelRatio:1,
    window:{LabRaxStudio:{...S,PreviewRenderer:FakeRenderer},localStorage:{getItem:()=>preference}},paint2d:()=>canvasDraws++,document:{createElement:()=>({setAttribute(){},remove(){}})}};
  const dialog={addEventListener:(_,f)=>close.push(f)},cv={closest:()=>dialog,parentNode:dialog,isConnected:true,clientWidth:400,clientHeight:300,dataset:{},after(){},getContext:()=>({drawImage(){}})},view={yaw:0,pitch:0,zoom:1,sets:[{v:[0,0,0,1,0,0,0,1,0]}]};
  vm.runInNewContext(adapter+'\nthis.draw=paint;this.dispose=disposePainter;',box);
  const flush=()=>{const pending=[...frames.values()];frames.clear();pending.forEach(f=>f());};
  box.draw(cv,view);box.draw(cv,view);assert.equal(frames.size,1);flush();assert.equal(draws,1);assert.equal(frames.size,0);
  preference='canvas';box.draw(cv,view);flush();assert.equal(canvasDraws,1);
  preference='';events.webglcontextlost({preventDefault(){}});flush();assert.equal(canvasDraws,2);events.webglcontextrestored();flush();assert.equal(draws,2);
  box.draw(cv,view);close[0]();assert.equal(frames.size,0);assert.equal(disposed,1);assert.equal(observed,0);
});
