'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const I=require('../cable-inventory.js'),P=require('../cable-ports.js'),C=require('../cable-routes.js');
function fixture(){
  const rack={slots:5,placements:[{id:'a',equipment:'box',slot:1,span:1},{id:'b',equipment:'box',slot:2,span:1}],cabling:{guides:[{id:'g'}],endpoints:[{id:'outside'}],cables:[]}};
  const ctx={ports:P,cables:{...C,estimate:(r,c)=>({length_m:c.length,complete:c.complete!==false})},library:[{id:'box',spec:{u:1,dev_d:80,keystones:[0],ports:[{id:'usb',type:'usb-c',x:0,z:10}]}}]};
  const cable=(number,type,length,extra={})=>({id:number,number,type,length,from:{allocation:'a',port:'usb'},to:{endpoint:'outside'},...extra});
  return {rack,ctx,cable};
}
function call(name,rack,...args){const before=structuredClone(rack);try{return I[name](rack,...args);}finally{assert.deepEqual(rack,before);}}
test('frozen API and browser-independent global load',()=>{
  assert.deepEqual(Object.keys(I).sort(),['LIMITS','STOCK_LENGTHS_M','CSV_COLUMNS','stockLength','items','csv'].sort());
  assert.equal(I.LIMITS,'Lengths are planning estimates. Jack type, guide capacity, cable fit and strength are UNKNOWN. No prices or purchases.');
  const sandbox={Date:undefined};vm.runInNewContext(fs.readFileSync(require.resolve('../cable-inventory.js'),'utf8'),sandbox);
  assert.ok(sandbox.LabRaxCableInventory);assert.deepEqual(Object.keys(sandbox),['Date','LabRaxCableInventory']);
});
test('stock boundaries and nonfinite values',()=>{
  assert.deepEqual(I.STOCK_LENGTHS_M,[0.15,0.3,0.5,1,1.5,2,3,5]);
  for(const [m,n] of [[0.15,0.15],[0.16,0.3],[5,5],[5.01,null],[NaN,null],[Infinity,null],[-Infinity,null]])assert.equal(I.stockLength(m),n);
  for(const n of I.STOCK_LENGTHS_M)assert.equal(I.stockLength(n),n);
});
test('groups by type and stock; numeric cable sort and custom maximum',()=>{
  const {rack,ctx,cable}=fixture();rack.cabling.cables=[cable('C10','usb-c',0.16),cable('C2','usb-c',0.3),cable('C3','rj45',1),cable('C5','usb-c',7),cable('C4','usb-c',6),cable('C1','usb-c',0.15)];
  const rows=call('items',rack,ctx);
  assert.deepEqual(rows.slice(0,4).map(r=>[r.key,r.quantity,r.cables]),[['cable:rj45:1',1,['C3']],['cable:usb-c:0.15',1,['C1']],['cable:usb-c:0.3',2,['C2','C10']],['cable:usb-c:custom',2,['C4','C5']]]);
  assert.equal(rows[3].item,'USB-C · custom length (≥ 7 m)');
  assert.deepEqual(rows[0],{section:'cables',key:'cable:rj45:1',item:'RJ45 (Ethernet) · 1 m',quantity:1,source:'buy',cables:['C3'],notes:[]});
});
test('incomplete ends are counted and flagged once even when estimate says complete',()=>{
  const {rack,ctx,cable}=fixture();
  rack.cabling.cables=[cable('C1','usb-c',1,{to:null}),cable('C2','usb-c',1,{from:{allocation:'a',port:'removed'}}),cable('C3','usb-c',1,{to:{endpoint:'removed'}}),cable('C4','usb-c',1,{from:{allocation:'removed',port:'usb'}}),cable('C5','usb-c',1,{complete:false})];
  const row=call('items',rack,ctx)[0];assert.equal(row.quantity,5);assert.deepEqual(row.notes,['check: incomplete']);
});
test('keystone pairs counted once per placement and guides counted separately',()=>{
  const {rack,ctx}=fixture();assert.deepEqual(call('items',rack,ctx),[
    {section:'keystones',key:'keystones',item:'Keystone jack',quantity:2,source:'buy',cables:[],notes:['Jack type UNKNOWN']},
    {section:'guides',key:'guides',item:'Lab Rax Cable Guide',quantity:1,source:'print',cables:[],notes:['Local model only; not in PRINT THE RACK; never redistributed']}]);
  assert.deepEqual(call('items',{},ctx),[]);
});
test('real routing estimate and slot keystone settings',()=>{
  const {rack,ctx,cable}=fixture();ctx.cables=C;rack.cabling.guides=[];rack.placements[1].tray={keystones:[]};
  rack.cabling.cables=[cable('C1','usb-c',99,{to:{allocation:'b',port:'usb'}})];
  const estimate=C.estimate(rack,rack.cabling.cables[0],ctx),rows=call('items',rack,ctx);
  assert.equal(rows[0].key,'cable:usb-c:'+I.stockLength(estimate.length_m));assert.equal(rows[1].quantity,1);
});
test('unknown labels and tie sorting',()=>{
  const {rack,ctx,cable}=fixture();rack.cabling.cables=[cable('C1','zzz',1),cable('C1','',1),{...cable('C1','zzz',1),id:'aaa'}];
  const rows=call('items',rack,ctx);assert.equal(rows[0].item,'Unknown type · 1 m');assert.equal(rows[1].item,'zzz · 1 m');assert.equal(rows[1].quantity,2);
});
test('CSV quotes every field, guards formulas, BOM, CRLF and trailing notes',()=>{
  const {rack,ctx,cable}=fixture();rack.placements=[];rack.cabling.guides=[];
  for(const label of ['=SUM(1,2)','+x','-x','@x','\tx','\rx','quote"x','a\nb']){
    ctx.ports={...P,TYPES:{x:{label}}};rack.cabling.cables=[cable('C2','x',1),cable('C10','x',1)];
    const text=call('csv',rack,ctx,{savedAt:'today'}),guard=/^[=+\-@\t\r]/.test(label)?"'":'';
    assert.ok(text.startsWith('\uFEFF"Section","Item","Quantity","Buy or print","Cables","Notes"\r\n'));
    assert.ok(text.includes('"'+guard+label.replace(/"/g,'""')+' · 1 m"'));
    assert.ok(text.includes('"C2 C10","check: incomplete"\r\n'));
    assert.ok(text.endsWith('"","","","","","'+I.LIMITS+'"\r\n"","","","","","Saved today"\r\n'));
  }
  const empty=call('csv',{},ctx);assert.equal(empty.replace(/\r\n/g,'').includes('\n'),false);assert.equal(empty.split('\r\n').length,3);
});

test('adapter group note is unique and follows incomplete regardless of cable order',()=>{
  for(const incompleteFirst of [false,true]){
    const {rack,ctx,cable}=fixture();
    rack.cabling.ports=[{allocation:'b',port:'usb',type:'rj45'}];
    const adapter=cable(incompleteFirst?'C2':'C1','usb-c',1,{to:{allocation:'b',port:'usb'}}),loose=cable(incompleteFirst?'C1':'C2','usb-c',1,{to:null});
    rack.cabling.cables=[adapter,{...adapter,id:'duplicate',number:'C3'},loose];
    const before=structuredClone(ctx.library),row=call('items',rack,ctx)[0];
    assert.deepEqual(row.notes,['check: incomplete','needs adapter']);assert.equal(row.quantity,3);
    assert.ok(call('csv',rack,ctx).includes('check: incomplete; needs adapter'));assert.deepEqual(ctx.library,before);
    rack.cabling.cables=[adapter,{...adapter,id:'duplicate',number:'C3'}];assert.deepEqual(call('items',rack,ctx)[0].notes,['needs adapter']);
    rack.cabling.ports[0].type='usb-c';assert.deepEqual(call('items',rack,ctx)[0].notes,[]);
  }
});
