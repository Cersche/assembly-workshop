'use strict';
// Wiring sheet drawing and printable pages (cable-sheet-view.js). Uses the real cable modules; cable-sheet.js
// (Codex task 13) is used when present, otherwise a minimal stand-in with the same frozen API.
const test=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const V=require('../cable-sheet-view.js'),P=require('../cable-ports.js'),C=require('../cable-routes.js'),SG=require('../cable-suggest.js');
const sheetFile=path.join(__dirname,'..','cable-sheet.js');
const S=fs.existsSync(sheetFile)?require(sheetFile):{
  LIMITS:'Lengths are planning estimates. Guide capacity, cable fit, bend tolerance and strength are UNKNOWN.',
  sortCables:rack=>[...(rack.cabling?.cables||[])].sort((a,b)=>String(a.number).localeCompare(String(b.number),undefined,{numeric:true})||String(a.id).localeCompare(String(b.id))),
  faceOf:(rack,c,ctx)=>c.from?.allocation&&c.to?.allocation&&C.endFace(rack,c.from,ctx)==='front'&&C.endFace(rack,c.to,ctx)==='front'?'front':'rear',
  notes:(rack,ctx)=>S.sortCables(rack).flatMap(c=>C.warnings(rack,c,ctx).map(text=>({number:c.number,text})))};
function fixture(){
  const ctx={ports:P,cables:C,suggest:SG,sheet:S,library:[{id:'wizard',name:'Wizard box',spec:{u:1,dev_d:80,
    ports:[{id:'front-left',x:-40,z:20,type:'rj45'}],
    rear_ports:[{id:'rear-left',x:-40,z:20,type:'rj45'},{id:'rear-right',x:40,z:20,type:'iec'}],keystones:[0]}}]};
  const rack={name:'Lab <"Rax"> & co',slots:6,placements:[{id:'pi',equipment:'pi4',slot:1,span:1,assembly:{name:'Raspberry Pi 4'}},
    {id:'w1',equipment:'wizard',slot:2,span:1,assembly:{name:'Patch & keystones'}},{id:'w2',equipment:'wizard',slot:5,span:2}],
    cabling:{guides:[{id:'g1',post:'RR',slot:3},{id:'g2',post:'RL',slot:4},{id:'g3',post:'FL',slot:2}],
      exits:[{id:'x1',position:'bottom-rear',slot:6}],endpoints:[{id:'wall',kind:'wall-outlet',name:'Office wall outlet'},{id:'unused',kind:'desk',name:'Desk'}],
      cables:[
        {id:'a',number:'C10',type:'iec',service_loop_m:0.15,from:{allocation:'w2',port:'rear-right'},to:{endpoint:'wall'},route:{mode:'auto',guides:['g1'],exit:'x1'}},
        {id:'b',number:'C2',type:'rj45',service_loop_m:0.15,from:{allocation:'w1',port:'rear-left'},to:{allocation:'w2',port:'rear-left'},route:{mode:'auto',guides:['g2'],exit:null}},
        {id:'c',number:'C3',type:'rj45',service_loop_m:0.15,from:{allocation:'w1',port:'front-left'},to:{allocation:'w2',port:'front-left'},route:{mode:'auto',guides:['g3'],exit:null}},
        {id:'d',number:'C4',type:'rj45',service_loop_m:0.15,from:{endpoint:'wall'},to:null,route:{mode:'auto',guides:[],exit:'x1'}}]}};
  return {rack,ctx};
}
const count=(s,re)=>(s.match(re)||[]).length;

test('exact exports; loads in a bare context without window or DOM',()=>{
  assert.deepEqual(Object.keys(V).sort(),['COLORS','PAPER','cablePoints','labelsPage','safeName','sheetPage','sheetSvg'].sort());
  const sandbox={};vm.runInNewContext(fs.readFileSync(require.resolve('../cable-sheet-view.js'),'utf8'),sandbox);
  assert.deepEqual(Object.keys(sandbox),['LabRaxCableSheetView']);
  assert.deepEqual(Object.keys(V.PAPER),['letter','a4']);
  assert.equal(V.safeName('My Lab Rax / 2'),'My_Lab_Rax_2');assert.equal(V.safeName(''),'lab-rax');
});
test('cable points: endpoint ends run out of the exit, in drawing order',()=>{
  const {rack,ctx}=fixture(),[a,,,d]=rack.cabling.cables;
  const pa=V.cablePoints(rack,a,ctx);assert.equal(pa.exit.id,'x1');assert.equal(pa.endpoint,'wall');
  assert.equal(pa.points.length,3);assert.deepEqual(pa.points[2],[0,-10]);
  const pd=V.cablePoints(rack,d,ctx);assert.deepEqual(pd.points,[[0,-10]]);
});
test('sheet SVG: well-formed text, both faces, escaped names, tags, exits, endpoints and notes',()=>{
  const {rack,ctx}=fixture(),before=JSON.stringify(rack),svg=V.sheetSvg(rack,ctx,{stamp:'version 1a2b3c4d · made 2026-10-19 21:00'});
  assert.equal(JSON.stringify(rack),before,'no mutation');
  assert.match(svg,/^<svg xmlns="http:\/\/www.w3.org\/2000\/svg" viewBox="0 0 1000 700"/);assert.ok(svg.endsWith('</svg>'));
  assert.ok(!/[<>&"]Rax/.test(svg.replace(/&lt;|&gt;|&amp;|&quot;/g,'')),'rack name is escaped');
  assert.match(svg,/Lab &lt;&quot;Rax&quot;&gt; &amp; co · wiring sheet/);
  assert.match(svg,/>Front</);assert.match(svg,/>Rear \(seen from behind\)</);
  for(const n of ['C2','C3','C4','C10'])assert.match(svg,new RegExp('>'+n+'<'));
  assert.match(svg,/Exit · Bottom rear/);assert.match(svg,/Office wall outlet · C4, C10/);assert.ok(!/>Desk/.test(svg),'unused endpoint not drawn');
  assert.match(svg,/C4 · Unconnected cable end\./);assert.match(svg,/strength are UNKNOWN\./);
  assert.equal(count(svg,/<rect x="[\d.-]+" y="[\d.-]+" width="12" height="8" rx="2"/g),4,'two rear guides, one front guide and the legend mark');
  assert.equal(count(svg,/fill="none" stroke="#378add" stroke-width="2.4"/g),1,'front cable drawn as a patch');
  assert.equal(count(svg,/fill="none" stroke="#d85a30" stroke-width="2.4"/g),1,'IEC drawn as power');
  for(const tag of ['text','rect','g','svg','path','defs','marker'])assert.equal(count(svg,new RegExp('<'+tag+'[ >]','g')),count(svg,new RegExp('</'+tag+'>|<'+tag+'[^>]*/>','g')),tag+' balanced');
  assert.ok(!/NaN|undefined/.test(svg));
});
test('rear elevation is mirrored; tall racks shrink to fit; empty rack still draws',()=>{
  const {rack,ctx}=fixture(),svg=V.sheetSvg(rack,ctx,{});
  const posts=[...svg.matchAll(/<text x="([\d.]+)" y="[\d.]+" text-anchor="middle" font-size="9" fill="[^"]+">(F|R)(L|R)</g)].map(m=>[m[2]+m[3],+m[1]]);
  const at=k=>posts.find(p=>p[0]===k)[1];assert.ok(at('FL')<at('FR'));assert.ok(at('RL')>at('RR'),'rear is seen from behind');
  const tall={...rack,slots:42,placements:[]};const t=V.sheetSvg(tall,ctx,{});assert.ok(!/NaN/.test(t));
  const ys=[...t.matchAll(/ y="([\d.]+)"/g)].map(m=>+m[1]);assert.ok(Math.max(...ys)<=700);
  const empty=V.sheetSvg({name:'Empty',slots:3,placements:[]},ctx,{});assert.match(empty,/No open cable warnings\./);assert.match(empty,/0 cables/);
});
test('many warnings are cut to whole notes with a pointer to the CSV',()=>{
  const {rack,ctx}=fixture();
  for(let i=0;i<40;i++)rack.cabling.cables.push({id:'u'+i,number:'C'+(20+i),type:'rj45',service_loop_m:0.15,from:null,to:null,route:{mode:'manual',guides:[],exit:null},route_changed:true});
  const svg=V.sheetSvg(rack,ctx,{});assert.match(svg,/\+ \d+ more: see the Warnings column in the schedule CSV\./);
  const ys=[...svg.matchAll(/<text x="70\d" y="([\d.]+)"/g)].map(m=>+m[1]);assert.ok(Math.max(...ys)<640,'notes stay inside the box');
});
test('printable pages: paper size, orientation, 3D page only when given, labels grid and escaping',()=>{
  const {rack,ctx}=fixture(),svg=V.sheetSvg(rack,ctx,{});
  const page=V.sheetPage({svg,title:'Sheet <1>',paper:'a4'});
  assert.match(page,/^<!doctype html>/);assert.match(page,/@page\{size:A4 landscape;margin:10mm\}/);assert.match(page,/<title>Sheet &lt;1&gt;<\/title>/);
  assert.equal(count(page,/<div class="page">/g),1);assert.ok(!/3D views/.test(page));assert.match(page,/window\.print\(\)/);
  assert.ok(!/<svg[^>]* width="1000"/.test(page),'svg scales to the page');
  const with3d=V.sheetPage({svg,title:'x',paper:'letter',images:[{label:'Front',src:'data:image/png;base64,AA'},{label:'Rear',src:'data:image/png;base64,BB'}]});
  assert.match(with3d,/@page\{size:letter landscape/);assert.equal(count(with3d,/<div class="page">/g),2);assert.equal(count(with3d,/<img /g),2);assert.match(with3d,/3D views · Cables mode/);
  const labels=V.labelsPage({labels:[{text:'C7 · K1 → Modem',sub:'RJ45 (Ethernet) · this end: K1 rear'},{text:'C7 · <b>',sub:'x'}],title:'L',paper:'letter',heading:'Rack · labels'});
  assert.match(labels,/@page\{size:letter portrait/);assert.equal(count(labels,/<div class="label">/g),2);assert.match(labels,/C7 · K1 → Modem/);assert.match(labels,/C7 · &lt;b&gt;/);
  assert.match(V.labelsPage({labels:[],title:'L'}),/No connected cable ends to label yet\./);
});
test('top and side exits: endpoint arrows go round the outside of the rack, bottom exits point straight down',()=>{
  const {rack,ctx}=fixture();
  rack.cabling.exits.push({id:'x2',position:'top-rear',slot:1});
  rack.cabling.cables[0].route={mode:'manual',guides:['g1'],exit:'x2'};
  const svg=V.sheetSvg(rack,ctx,{}),arrows=[...svg.matchAll(/<path d="(M[^"]+)" fill="none" stroke="#5f6b78" stroke-width="0.9"/g)].map(m=>m[1]);
  assert.equal(arrows.length,2,'one arrow per exit serving the endpoint');
  assert.ok(arrows.some(d=>(d.match(/ L/g)||[]).length===3),'top exit goes round');
  assert.ok(arrows.some(d=>(d.match(/ L/g)||[]).length===1),'bottom exit goes straight');
  const xs=arrows.flatMap(d=>[...d.matchAll(/[ML]([\d.]+) /g)].map(m=>+m[1]));assert.ok(Math.max(...xs)<690,'stays left of the legend column');
});
