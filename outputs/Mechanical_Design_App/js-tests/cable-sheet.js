'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),vm=require('node:vm');
const S=require('../cable-sheet.js'),P=require('../cable-ports.js'),C=require('../cable-routes.js'),G=require('../cable-suggest.js');
const port=(allocation,p)=>({allocation,port:p});
function fixture(){
  const ctx={ports:P,cables:C,suggest:G,library:[{id:'pi4',name:'Raspberry Pi 4'},
    {id:'wizard',name:'Library box',spec:{u:1,dev_d:80,keystones:[0],
      ports:[{id:'front',label:'USB',type:'usb-a',x:0,z:20}],
      rear_ports:[{id:'rear',label:'Ethernet',type:'rj45',x:-40,z:20},{id:'power',label:'Power',type:'iec',x:40,z:20}]}}]};
  const rack={name:'Rack, "Lab"',slots:6,placements:[{id:'pi',equipment:'pi4',slot:1,span:1},
    {id:'w',equipment:'wizard',slot:2,span:1,assembly:{name:'Box'}},{id:'w2',equipment:'wizard',slot:5,span:1}],
    cabling:{guides:[{id:'g3',post:'RR',slot:3},{id:'g2',post:'RL',slot:2}],
      exits:[{id:'bottom',position:'bottom-rear',slot:6},{id:'left',position:'left',slot:4},{id:'right',position:'right',slot:5}],
      endpoints:[{id:'modem',name:'Modem',kind:'modem'}],cables:[],settings:{service_loop_m:0.2}}};
  rack.cabling.cables=[
    {id:'rear',number:'C10',type:'rj45',from:port('pi','ethernet'),to:port('w','ks-1-rear'),route:{mode:'manual',guides:['g3','gone','g2'],exit:null},note:'Line 1, "quoted"\nLine 2'},
    {id:'front',number:'C2',type:'rj45',from:port('w','ks-1-front'),to:{endpoint:'modem'},route:{mode:'auto',guides:[],exit:'bottom'},service_loop_m:0,color:'#123456'},
    {id:'loose',number:'C3',type:'iec',from:port('w','power'),to:null,route:{mode:'auto',guides:[],exit:null}}];
  return {rack,ctx};
}
// Every module call below is checked independently for rack mutation, including nested values.
function call(name,rack,...args){const before=structuredClone(rack);try{return S[name](rack,...args);}finally{assert.deepEqual(rack,before,name+' mutated rack');}}
test('exact exports, constants and isolated global load without browser APIs or Date',()=>{
  assert.deepEqual(Object.keys(S).sort(),['LIMITS','CSV_COLUMNS','sortCables','endName','shortName','faceOf','schedule','csv','labels','notes'].sort());
  assert.equal(S.LIMITS,'Lengths are planning estimates. Guide capacity, cable fit, bend tolerance and strength are UNKNOWN.');
  assert.deepEqual(S.CSV_COLUMNS,['Number','From','To','Type','Carries','Colour','Route','Exit','Length estimate (m)','Service loop (m)','Linked to','Warnings','Note']);
  const sandbox={Date:undefined};vm.runInNewContext(fs.readFileSync(require.resolve('../cable-sheet.js'),'utf8'),sandbox);
  assert.deepEqual(Object.keys(sandbox),['Date','LabRaxCableSheet']);
  const {rack,ctx}=fixture(),before=structuredClone(rack);
  assert.equal(sandbox.LabRaxCableSheet.csv(rack,ctx,{}),call('csv',rack,ctx,{}));assert.deepEqual(rack,before);
});
test('numeric sorting returns a new array and breaks ties by id',()=>{
  const {rack}=fixture();rack.cabling.cables.push({...rack.cabling.cables[1],id:'aaa'});
  const sorted=call('sortCables',rack);assert.notEqual(sorted,rack.cabling.cables);
  assert.deepEqual(sorted.map(c=>c.id),['aaa','front','loose','rear']);assert.deepEqual(call('sortCables',{}),[]);
});
test('all long and short names, saved overrides and name fallbacks',()=>{
  const {rack,ctx}=fixture();
  const cases=[
    [null,'Unconnected','unconnected'],[{endpoint:'modem'},'Modem (outside)','Modem'],[{endpoint:'gone'},'Removed endpoint','removed'],
    [port('gone','x'),'Removed equipment','removed'],[port('w','gone'),'Box · removed port','removed'],
    [port('pi','ethernet'),'Raspberry Pi 4 · Ethernet (U01, face UNKNOWN)','Raspberry Pi 4'],
    [port('w','rear'),'Box · Ethernet (U02 rear)','Box'],[port('w','front'),'Box · USB (U02 front)','Box'],
    [port('w','ks-1-rear'),'Box · Keystone 1 · rear (U02)','K1'],[port('w','ks-1-front'),'Box · Keystone 1 · front (U02)','K1'],
    [port('w2','front'),'Library box · USB (U05 front)','Library box']];
  for(const [end,long,short] of cases){assert.equal(call('endName',rack,end,ctx),long);assert.equal(call('shortName',rack,end,ctx),short);}
  rack.cabling.ports=[{allocation:'pi',port:'ethernet',face:'rear'}];
  assert.equal(call('endName',rack,port('pi','ethernet'),ctx),'Raspberry Pi 4 · Ethernet (U01 rear)');
  ctx.library[0].name='';assert.equal(call('shortName',rack,port('pi','ethernet'),ctx),'Equipment');
  rack.cabling.ports.push({allocation:'w',port:'front',type:'keystone'});
  assert.equal(call('shortName',rack,port('w','front'),ctx),'Box');
});
test('face selection requires two front ports',()=>{
  const {rack,ctx}=fixture();
  for(const [to,expected] of [[port('w2','front'),'front'],[port('w2','rear'),'rear'],[{endpoint:'modem'},'rear'],[null,'rear'],[port('pi','ethernet'),'rear']])
    assert.equal(call('faceOf',rack,{from:port('w','front'),to},ctx),expected);
});
test('schedule has every field, route order, estimates, warning arrays and reciprocal links',()=>{
  const {rack,ctx}=fixture(),rows=call('schedule',rack,ctx);
  assert.deepEqual(rows[0],{id:'front',number:'C2',face:'rear',from:'Box · Keystone 1 · front (U02)',to:'Modem (outside)',type:'RJ45 (Ethernet)',carries:'data',colour:'#123456',route:'direct',exit:'Bottom rear',length_m:0.4,to_exit:true,length:'0.4 to exit',service_loop_m:0,linked:'C10 via K1',warnings:[],note:''});
  assert.deepEqual(rows[1],{id:'loose',number:'C3',face:'rear',from:'Box · Power (U02 rear)',to:'Unconnected',type:'IEC power inlet',carries:'power',colour:'#ff6b6b',route:'direct',exit:'',length_m:null,to_exit:false,length:'',service_loop_m:0.2,linked:'',warnings:['Unconnected cable end.'],note:''});
  const rear=rows[2];assert.equal(rear.route,'RR U03 → RL U02 (manual)');assert.equal(rear.linked,'C2 via K1');
  assert.equal(rear.length_m,C.estimate(rack,rack.cabling.cables[0],ctx).length_m);
  assert.equal(rear.length,rear.length_m.toFixed(1));assert.equal(rear.note,'Line 1, "quoted"\nLine 2');
  assert.deepEqual(rear.warnings,['Port face UNKNOWN; routing uses the rear by default.']);
  const c=rack.cabling.cables[1];
  for(const [id,label] of [['left','Left side U04'],['right','Right side U05'],['gone','']]){c.route.exit=id;assert.equal(call('schedule',rack,ctx)[0].exit,label);}
  c.route.mode='manual';c.route.guides=['gone'];assert.equal(call('schedule',rack,ctx)[0].route,'direct (manual)');
  delete rack.cabling.settings;assert.equal(call('schedule',rack,ctx)[1].service_loop_m,0.15);
  ctx.cables={...C,linkedCable:()=> 'missing'};assert.equal(call('schedule',rack,ctx)[0].linked,'');
});
test('carries uses optional suggestions and raw type fallback',()=>{
  const {rack,ctx}=fixture();delete ctx.suggest;
  assert.equal(call('schedule',rack,ctx)[0].carries,'');rack.cabling.cables[1].carries='power';
  assert.equal(call('schedule',rack,ctx)[0].carries,'power');rack.cabling.cables[1].type='custom';
  assert.equal(call('schedule',rack,ctx)[0].type,'custom');
});
// Parse quoted records independently so embedded newlines do not inflate the row count.
function parseCSV(text){
  const rows=[];let row=[],field='',quoted=false;
  for(let i=1;i<text.length;i++){
    const ch=text[i];
    if(ch==='"'){if(quoted&&text[i+1]==='"'){field+='"';i++;}else quoted=!quoted;}
    else if(!quoted&&ch===','){row.push(field);field='';}
    else if(!quoted&&ch==='\r'&&text[i+1]==='\n'){row.push(field);rows.push(row);row=[];field='';i++;}
    else field+=ch;
  }
  assert.equal(quoted,false);assert.equal(field,'');assert.deepEqual(row,[]);return rows;
}
test('CSV BOM, CRLF records, metadata quoting, field order and embedded newline',()=>{
  const {rack,ctx}=fixture(),text=call('csv',rack,ctx,{savedAt:'2026-10-19T12:00:00Z'}),rows=parseCSV(text);
  assert.equal(text[0],'\uFEFF');assert.ok(text.endsWith('\r\n'));
  assert.ok(text.startsWith('\uFEFF"# Rack, ""Lab"" cable schedule'));
  assert.deepEqual(rows[0],['# Rack, "Lab" cable schedule · saved 2026-10-19T12:00:00Z · lengths are planning estimates; fit and capacity UNKNOWN']);
  assert.deepEqual(rows[1],S.CSV_COLUMNS);assert.equal(rows.length,5);
  const schedule=call('schedule',rack,ctx);
  schedule.forEach((r,i)=>assert.deepEqual(rows[i+2],[r.number,r.from,r.to,r.type,r.carries,r.colour,r.route,r.exit,r.length,String(r.service_loop_m),r.linked,r.warnings.join(' '),r.note]));
  assert.ok(text.includes('"Line 1, ""quoted""\nLine 2"\r\n'));
  rack.name='';rack.cabling.cables=[];
  const empty=call('csv',rack,ctx);assert.ok(empty.includes('# Rack cable schedule · saved time unknown'));
  assert.equal(empty.replace(/\r\n/g,'').includes('\n'),false);assert.equal(parseCSV(empty).length,2);
});
test('CSV guards formula prefixes before quoting, preserving whitespace',()=>{
  const {rack,ctx}=fixture();rack.cabling.cables=[rack.cabling.cables[0]];
  for(const value of ['=SUM(1,2)','+1','-1','@x','\tx','\rx',' leading','trailing ','quote"x','a\nb']){
    rack.cabling.cables[0].note=value;const text=call('csv',rack,ctx,{});
    assert.equal(parseCSV(text)[2][12],/^[=+\-@\t\r]/.test(value)?"'"+value:value);
    if(value===' leading'||value==='trailing ')assert.ok(text.endsWith('"'+value+'"\r\n'));
  }
});
test('labels include both connected ends in order and keystone face detail',()=>{
  const {rack,ctx}=fixture(),labels=call('labels',rack,ctx);
  assert.equal(labels.length,5);
  assert.deepEqual(labels.slice(0,3),[
    {cable:'front',number:'C2',end:'from',text:'C2 · K1 → Modem',sub:'RJ45 (Ethernet) · this end: K1 front'},
    {cable:'front',number:'C2',end:'to',text:'C2 · Modem → K1',sub:'RJ45 (Ethernet) · this end: Modem'},
    {cable:'loose',number:'C3',end:'from',text:'C3 · Box → unconnected',sub:'IEC power inlet · this end: Box Power'}]);
  assert.equal(labels[4].sub,'RJ45 (Ethernet) · this end: K1 rear');
  for(const end of [port('gone','x'),port('w','gone'),{endpoint:'gone'}]){
    rack.cabling.cables=[{id:'x',number:'C1',type:'other',from:null,to:end}];
    assert.deepEqual(call('labels',rack,ctx),[{cable:'x',number:'C1',end:'to',text:'C1 · removed → unconnected',sub:'Other · this end: removed'}]);
  }
});
test('notes contain each warning in cable order without standing limits',()=>{
  const {rack,ctx}=fixture();rack.cabling.cables[0].route_changed=true;
  assert.deepEqual(call('notes',rack,ctx),[
    {number:'C3',text:'Unconnected cable end.'},
    {number:'C10',text:'Port face UNKNOWN; routing uses the rear by default.'},
    {number:'C10',text:'Cable route changed.'}]);
  assert.deepEqual(call('notes',{},ctx),[]);assert.deepEqual(call('schedule',{},ctx),[]);assert.deepEqual(call('labels',{},ctx),[]);
});

test('adapter warning flows to schedule, CSV warnings column and notes',()=>{
  const {rack,ctx}=fixture();rack.cabling.cables=[{id:'adapter',number:'C1',type:'rj45',from:port('w','rear'),to:port('w2','front'),route:{guides:[],exit:null}}];
  const before=structuredClone(ctx.library),text='Needs an adapter cable: RJ45 (Ethernet) to USB-A.';
  assert.deepEqual(call('schedule',rack,ctx)[0].warnings,[text]);
  assert.deepEqual(call('notes',rack,ctx),[{number:'C1',text}]);
  const csv=call('csv',rack,ctx,{});assert.ok(csv.includes(','+text+',\r\n'));
  assert.deepEqual(ctx.library,before);
  rack.cabling.ports=[{allocation:'w2',port:'front',type:'rj45'}];assert.deepEqual(call('notes',rack,ctx),[]);
});
