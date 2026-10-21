const test=require('node:test'),assert=require('node:assert/strict');
const E=require('../equipment-wizard.js'),TP=require('../tray-placement.js');
test('touching plug cylinders merge transitively into one editable union question',()=>{
  const segment=(x,y0,y1,r)=>{const v=[],n=24,tri=(...p)=>v.push(...p.flat());for(let i=0;i<n;i++){const point=(j,y)=>[x+r*Math.cos(j*2*Math.PI/n),y,15+r*Math.sin(j*2*Math.PI/n)],a=point(i,y0),b=point(i+1,y0),A=point(i,y1),B=point(i+1,y1);tri(a,A,b);tri(b,A,B);tri([x,y0,15],a,b);tri([x,y1,15],B,A);}return v;};
  const v=[...cube(0,0,0,100,100,30),...segment(50,100,110,4),...segment(50,110.4,120,3),...segment(50,120,135,2)];
  const [mn,mx]=bounds(v),d=E.findProtrusions(v,mn,mx);assert.equal(E.PROTRUSION.mergeToleranceMM,.5);assert.equal(d.items.length,1);
  const p=d.items[0];assert.deepEqual([p.face,p.x,p.y,p.z,p.w,p.d,p.h,p.method],['back',46,100,11,8,35,8,'separate bodies']);
  p.answer='space';p.d=40;assert.equal(E.importFrame(d).zones[0].d,40);
  for(const gap of [.5,.51,20]){const mesh=[...cube(0,0,0,100,100,30),...segment(30,100,110,4),...segment(30,110+gap,125,3)],b=bounds(mesh);assert.equal(E.findProtrusions(mesh,...b).items.length,gap<=.5?1:2);}
  const far=[...cube(0,0,0,100,100,30),...segment(20,100,135,4),...segment(80,100,135,4)];assert.equal(E.findProtrusions(far,...bounds(far)).items.length,2);
});

test('flat front-position message appears once with the newer advice',()=>{
  for(const front_position of ['flush','setback','today']){const s={dev_w:85,dev_d:100,dev_h:20,device_mount:'flat',joint:'single',front_position,front_setback:6,dev_off_y:-10},messages=TP.problems(s,TP.values(s)).filter(x=>x.includes('Flat corner stops'));
    assert.equal(messages.length,1);if(front_position!=='today')assert.match(messages[0],/Set back at least 10.2 mm or choose Sleeve/);
  }
});

test('merge stays on one face and does not bridge through empty union-box corners',()=>{
  const side=[...cube(0,0,0,100,100,30),...cube(-10,-10,10,0,0,18)],d=E.findProtrusions(side,...bounds(side));
  assert.deepEqual(d.items.map(p=>p.face).sort(),['front','left']);
  const mesh=[...cube(0,0,0,100,100,30),...cube(10,100,10,20,130,14),...cube(20.4,100,10,60,105,14),...cube(50,120,10,55,125,14)];
  assert.equal(E.findProtrusions(mesh,...bounds(mesh)).items.length,2);
});

test('band warning measures 2.1 mm, names merged windows and joint cuts without blocking',()=>{
  const s={name:'Disposable band fixture',dev_w:158,dev_d:101.1,dev_h:26.5,device_mount:'flat',joint:'screw',rear_support:true,rear_style:'reinforced',front_position:'setback',front_setback:70,u:1,holes:[],protrusions:[{face:'back',x:5,y:101.1,z:9.4,w:9,d:140,h:9.5,keep_clear:true}]},v=TP.values(s),original=JSON.stringify(s);
  assert.equal(TP.keepClearBands(s,v)[0].band,2.1);assert.match(TP.warnings(s,v).join(' '),/it joins a style window and leaves a 2.1 mm band to the next style window \(the Reinforced style normally keeps 5 mm\)/);assert.deepEqual(TP.problems(s,v),[]);assert.equal(JSON.stringify(s),original);
  s.protrusions[0]={...s.protrusions[0],x:36.5,w:5,z:9,h:4};assert.match(TP.warnings(s,v).join(' '),/cuts the joint boss and joint pilot/);assert.deepEqual(TP.problems(s,v),[]);
});

test('band and style cut geometry mirror Python across styles mounts U rotations and moved joints',()=>{
  const {spawnSync}=require('node:child_process'),path=require('node:path'),fixtures=[];
  for(const device_mount of ['flat','sleeve','inserts'])for(const rear_style of ['solid','open','reinforced','slots','vents'])for(const u of [1,2,5])for(const dev_rot of [0,90,180,270]){
    const p=dev_rot===0?{x:5,y:100,w:9,d:140}:dev_rot===90?{x:100,y:5,w:140,d:9}:dev_rot===180?{x:5,y:-140,w:9,d:140}:{x:-140,y:5,w:140,d:9};
    fixtures.push({name:'Disposable parity',dev_w:85,dev_d:100,dev_h:20,device_mount,joint:'screw',rear_support:true,rear_style,u,dev_rot,holes:[[20,20]],protrusions:[{...p,z:5,h:10,face:'back',keep_clear:true}]});
  }
  fixtures.push({...fixtures[0],ports:[{x:-38,z:26,w:10,h:10,r:1}],rear_style:'reinforced'});
  const code="import sys,json,equipment as E; result=[]\nfor raw in json.load(sys.stdin):\n s=E.clean(raw); g=E.rear_geometry(s); result.append(dict(spec=s,bands=E.keep_clear_bands(s),windows=g['windows'],holes=g['holes']))\nprint(json.dumps(result))";
  const run=spawnSync('C:/Program Files/Python310/python.exe',['-B','-c',code],{cwd:path.resolve(__dirname,'..'),input:JSON.stringify(fixtures),encoding:'utf8',maxBuffer:5e6});assert.equal(run.status,0,run.stderr);
  const close=(a,b)=>{if(typeof a==='number'&&typeof b==='number')assert.ok(Math.abs(a-b)<1e-6,`${a} != ${b}`);else if(Array.isArray(a)){assert.equal(a.length,b.length);a.forEach((x,i)=>close(x,b[i]));}else if(a&&typeof a==='object'){assert.deepEqual(Object.keys(a).sort(),Object.keys(b).sort());for(const k in a)close(a[k],b[k]);}else assert.equal(a,b);};
  for(const r of JSON.parse(run.stdout)){const v=TP.values(r.spec),g=TP.rearCutGeometry(r.spec,v);close(g.windows,r.windows);close(g.holes,r.holes);close(TP.keepClearBands(r.spec,v),r.bands);}
});
function cube(x0,y0,z0,x1,y1,z1){const p=[[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]],v=[];for(const f of [[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]])for(const i of f)v.push(...p[i]);return v;}
function cylinder(fused=false){let v=cube(0,0,0,100,100,30);if(fused)v.splice(8*9,2*9);const angles=[...Array.from({length:32},(_,i)=>2*Math.PI*i/32),...[[50,15],[-50,15],[-50,-15],[50,-15]].map(([x,z])=>(Math.atan2(z,x)+2*Math.PI)%(2*Math.PI))].sort((a,b)=>a-b),N=angles.length,c=[50,100,15],tri=(...p)=>v.push(...p.flat());for(let i=0;i<N;i++){const angle=i=>angles[i%N],point=i=>[50+4*Math.cos(angle(i)),100,15+4*Math.sin(angle(i))],a=point(i),b=point(i+1),A=[a[0],135,a[2]],B=[b[0],135,b[2]];tri(a,A,b);tri(b,A,B);tri([50,135,15],B,A);if(!fused)tri(c,a,b);else{const edge=p=>{const t=Math.min(50/Math.abs(p[0]-50),15/Math.abs(p[2]-15));return [50+(p[0]-50)*t,100,15+(p[2]-15)*t];};const q=edge(a),r=edge(b);tri(a,b,q);tri(q,b,r);}}return v;}
function bounds(v){const mn=[Infinity,Infinity,Infinity],mx=[-Infinity,-Infinity,-Infinity];v.forEach((x,i)=>{mn[i%3]=Math.min(mn[i%3],x);mx[i%3]=Math.max(mx[i%3],x);});return [mn,mx];}
for(const fused of [false,true])test('back cylinder '+(fused?'fused':'separate'),()=>{const v=cylinder(fused),[mn,mx]=bounds(v),d=E.findProtrusions(v,mn,mx);assert.equal(d.items.length,1);const p=d.items[0];assert.equal(p.face,'back');assert.equal(p.method,fused?'fused':'separate body');assert.ok(Math.abs(p.d-35)<.51);assert.ok(Math.abs(p.w-8)<.1);assert.ok(Math.abs(d.caseMax[1]-100)<.51);});
test('feet excluded; sub-2mm bumps and internal solids excluded',()=>{let v=cube(0,0,0,100,100,30);for(const x of [10,80])for(const y of [10,80])v.push(...cube(x,y,-3,x+5,y+5,0));v.push(...cube(40,100,10,45,101.9,15),...cube(20,20,5,25,25,10));const [mn,mx]=bounds(v),f=E.findFeet(v,mn,mx);assert.equal(E.findProtrusions(v,mn,mx,f).items.length,0);});
test('left plug answers keep the case origin and mandatory unanswered guard',()=>{const v=[...cube(0,0,0,100,100,30),...cube(-20,40,10,0,48,18)],[mn,mx]=bounds(v),d=E.findProtrusions(v,mn,mx);assert.equal(d.items[0].face,'left');assert.equal(E.protrusionsAnswered(d.items),false);for(const answer of ['case','space','omit']){d.items[0].answer=answer;const f=E.importFrame(d);assert.equal(E.protrusionsAnswered(d.items),true);assert.equal(f.mx[0]-f.mn[0],answer==='case'?120:100);assert.equal(10-f.mn[0],answer==='case'?30:10);assert.equal(f.zones.length,answer==='space'?1:0);if(f.zones.length)assert.equal(f.zones[0].x,-20);}});
test('front and bottom plug origin stays stable for holes feet and ports',()=>{for(const axis of [1,2]){const a=[40,40,10],b=[48,48,18];a[axis]=-10;b[axis]=0;const v=[...cube(0,0,0,100,100,30),...cube(...a,...b)],[mn,mx]=bounds(v),d=E.findProtrusions(v,mn,mx);assert.equal(d.items.length,1);d.items[0].answer='space';const f=E.importFrame(d);assert.equal(f.mn[axis],0);assert.equal(12-f.mn[axis],12);}});
test('warnings rotate zones and include real bend-space limits',()=>{const s={dev_w:100,dev_d:100,dev_h:20,u:1,device_mount:'sleeve',joint:'single',protrusions:[{x:-20,y:-10,z:30,w:10,d:20,h:30,face:'front',keep_clear:true}]};const msg=TP.warnings(s,TP.values(s)).join(' ');for(const re of [/faceplate/,/sleeve wall/,/above/,/extra bend space/])assert.match(msg,re);});
test('screening performance 50k triangles',()=>{const base=cylinder(),v=[];while(v.length/9<50000)v.push(...base.slice(0,Math.min(base.length,450000-v.length)));const [mn,mx]=bounds(v),start=performance.now();E.findProtrusions(v,mn,mx);const ms=performance.now()-start;console.log(`protrusions: 50k triangles ${ms.toFixed(1)} ms`);assert.ok(ms<10000);});

test('unflagged short bumps and large separate case bodies remain in the size',()=>{for(const extra of [cube(40,100,10,45,101.9,15),cube(0,100,0,100,120,30)]){const v=[...cube(0,0,0,100,100,30),...extra],[mn,mx]=bounds(v),d=E.findProtrusions(v,mn,mx);assert.equal(d.items.length,0);assert.deepEqual(E.importFrame(d).mx,mx);}});
test('actual wizard frame sync rebases holes feet and both port lists for left front bottom',()=>{const fs=require('node:fs'),vm=require('node:vm'),src=fs.readFileSync(require.resolve('../equipment-wizard.js'),'utf8'),code=src.slice(src.indexOf('  function syncImportFrame(){'),src.indexOf('  function findHoles('));for(const axis of [0,1,2]){const origin=[0,0,0];origin[axis]=-20;const item={x:0,y:0,z:0,w:8,d:8,h:8,answer:'omit'};item[['x','y','z'][axis]]=-20;const box={protrusionDetection:{caseMin:[0,0,0],caseMax:[100,100,30],items:[item]},importOrigin:origin,importFrame:E.importFrame,spec:{dev_w:axis===0?120:100,dev_d:axis===1?120:100,dev_h:axis===2?50:30,holes:[[10-origin[0],15-origin[1]]],ports:[{x:axis===0?0:-10,z:axis===2?30:10}],rear_ports:[{x:axis===0?0:-10,z:axis===2?30:10}]},found:[{x:10-origin[0],y:15-origin[1]}],foundFeet:[{x:20-origin[0],y:30-origin[1],w:4,d:4,h:2,keep:true}],foundPorts:[{cx:40-origin[0],cz:10-origin[2]}],uExplicit:true};vm.runInNewContext(code+'syncImportFrame()',box);assert.equal(box.spec.holes[0][0],10);assert.equal(box.spec.holes[0][1],15);assert.equal(box.spec.feet[0].x,20);assert.equal(box.spec.feet[0].y,30);assert.equal(box.foundPorts[0].cx,40);assert.equal(box.foundPorts[0].cz,10);for(const p of [...box.spec.ports,...box.spec.rear_ports]){assert.equal(p.x,-10);assert.equal(p.z,10);}}});

test('flush flat with a screw joint gives one front-gap message (Claude review 34)',()=>{
  const s={dev_w:85,dev_d:100,dev_h:20,device_mount:'flat',joint:'screw',front_position:'flush'},p=TP.problems(s,TP.values(s));
  assert.equal(p.filter(x=>/front screw joint|corner stops/.test(x)).length,1);assert.ok(p.some(x=>x.includes('Set back at least 15.5 mm or choose Sleeve')));
});
