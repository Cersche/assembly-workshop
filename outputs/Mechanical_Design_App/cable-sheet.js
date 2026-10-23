// Read-only planning documents. The caller supplies the saved rack and save time.
(function(root){
  'use strict';
  const LIMITS='Lengths are planning estimates. Guide capacity, cable fit, bend tolerance and strength are UNKNOWN.';
  const CSV_COLUMNS=['Number','From','To','Type','Carries','Colour','Route','Exit','Length estimate (m)','Service loop (m)','Linked to','Warnings','Note'];
  const pad=n=>String(n).padStart(2,'0');
  // U counts from the bottom; stored slots count from the top.
  const uNo=(rack,slot)=>rack.slots-slot+1;
  const uOf=(rack,p)=>p.span>1?pad(uNo(rack,p.slot+p.span-1))+'–U'+pad(uNo(rack,p.slot)):pad(uNo(rack,p.slot));
  const list=(rack,key)=>rack.cabling?.[key]||[];
  const outside=end=>typeof end?.endpoint==='string';
  const portEnd=end=>end&&typeof end.allocation==='string'&&typeof end.port==='string';
  const keystone=port=>port?.type==='keystone'?/^ks-(\d+)-(front|rear)$/.exec(port.id):null;
  const typeName=(cable,ctx)=>ctx.ports.TYPES[cable.type]?.label||cable.type;
  function info(rack,end,ctx){
    const placement=(rack.placements||[]).find(p=>p.id===end?.allocation);
    const item=(ctx.library||[]).find(i=>i.id===placement?.equipment);
    return {placement,name:placement?.assembly?.name||item?.name||'Equipment',
      port:placement?(ctx.ports.portsFor(rack,placement,item)||[]).find(p=>p.id===end.port):undefined};
  }
  function sortCables(rack){
    return list(rack,'cables').slice().sort((a,b)=>String(a.number).localeCompare(String(b.number),undefined,{numeric:true})||String(a.id).localeCompare(String(b.id)));
  }
  function endName(rack,end,ctx){
    if(end==null)return 'Unconnected';
    if(outside(end)){const e=list(rack,'endpoints').find(e=>e.id===end.endpoint);return e?e.name+' (outside)':'Removed endpoint';}
    const {placement,name,port}=info(rack,end,ctx);
    if(!placement)return 'Removed equipment';
    if(!port)return name+' · removed port';
    const face=ctx.cables.endFace(rack,end,ctx);
    return name+' · '+port.label+' (U'+uOf(rack,placement)+(keystone(port)?'':face==='front'||face==='rear'?' '+face:', face UNKNOWN')+')';
  }
  function shortName(rack,end,ctx){
    if(end==null)return 'unconnected';
    if(outside(end))return list(rack,'endpoints').find(e=>e.id===end.endpoint)?.name??'removed';
    const {placement,name,port}=info(rack,end,ctx),ks=keystone(port);
    return !placement||!port?'removed':ks?'K'+ks[1]:name;
  }
  function faceOf(rack,cable,ctx){
    return [cable.from,cable.to].every(e=>portEnd(e)&&ctx.cables.endFace(rack,e,ctx)==='front')?'front':'rear';
  }
  function schedule(rack,ctx){
    return sortCables(rack).map(cable=>{
      const estimate=ctx.cables.estimate(rack,cable,ctx),length_m=estimate.complete?estimate.length_m:null;
      const guides=(cable.route?.guides||[]).map(id=>list(rack,'guides').find(g=>g.id===id)).filter(Boolean);
      const exit=list(rack,'exits').find(e=>e.id===cable.route?.exit);
      const linkedId=ctx.cables.linkedCable(rack,cable,ctx),other=list(rack,'cables').find(c=>c.id===linkedId);
      // Match the paired end when both ends of this cable are keystones.
      const linkedEnd=other&&[cable.from,cable.to].find(end=>{
        if(!portEnd(end))return false;
        const p=info(rack,end,ctx).port;
        return keystone(p)&&[other.from,other.to].some(e=>e?.allocation===end.allocation&&e?.port===p.passThrough);
      });
      return {id:cable.id,number:cable.number,face:faceOf(rack,cable,ctx),
        from:endName(rack,cable.from,ctx),to:endName(rack,cable.to,ctx),type:typeName(cable,ctx),
        carries:ctx.suggest?ctx.suggest.carries(rack,cable,ctx):(cable.carries||''),colour:ctx.cables.cableColor(cable),
        route:(guides.map(g=>g.post+' U'+pad(uNo(rack,g.slot))).join(' → ')||'direct')+(cable.route?.mode==='manual'?' (manual)':''),
        exit:exit?ctx.cables.EXIT_POSITIONS[exit.position]+(['left','right'].includes(exit.position)?' U'+pad(uNo(rack,exit.slot)):''):'',
        length_m,to_exit:estimate.to_exit,length:length_m===null?'':length_m.toFixed(1)+(estimate.to_exit?' to exit':''),
        service_loop_m:cable.service_loop_m??rack.cabling?.settings?.service_loop_m??0.15,
        linked:other?other.number+' via '+shortName(rack,linkedEnd||[cable.from,cable.to].find(e=>portEnd(e)&&keystone(info(rack,e,ctx).port)),ctx):'',
        warnings:ctx.cables.warnings(rack,cable,ctx),note:cable.note||''};
    });
  }
  function csvField(value){
    let text=String(value);
    if(/^[=+\-@\t\r]/.test(text))text="'"+text;
    return /[,"\r\n]|^ | $/.test(text)?'"'+text.replace(/"/g,'""')+'"':text;
  }
  function csv(rack,ctx,meta={}){
    const rows=[[`# ${rack.name||'Rack'} cable schedule · saved ${meta.savedAt||'time unknown'} · lengths are planning estimates; fit and capacity UNKNOWN`],CSV_COLUMNS];
    for(const r of schedule(rack,ctx))rows.push([r.number,r.from,r.to,r.type,r.carries,r.colour,r.route,r.exit,r.length,String(r.service_loop_m),r.linked,r.warnings.join(' '),r.note]);
    return '\uFEFF'+rows.map(row=>row.map(csvField).join(',')+'\r\n').join('');
  }
  function detail(rack,end,ctx){
    if(outside(end))return list(rack,'endpoints').find(e=>e.id===end.endpoint)?.name??'removed';
    const {port,name}=info(rack,end,ctx),ks=keystone(port);
    return !port?'removed':ks?'K'+ks[1]+' '+ks[2]:name+' '+port.label;
  }
  function labels(rack,ctx){
    return sortCables(rack).flatMap(cable=>['from','to'].filter(end=>cable[end]!=null).map(end=>({
      cable:cable.id,number:cable.number,end,
      text:cable.number+' · '+shortName(rack,cable[end],ctx)+' → '+shortName(rack,cable[end==='from'?'to':'from'],ctx),
      sub:typeName(cable,ctx)+' · this end: '+detail(rack,cable[end],ctx)})));
  }
  function notes(rack,ctx){
    return sortCables(rack).flatMap(cable=>ctx.cables.warnings(rack,cable,ctx).map(text=>({number:cable.number,text})));
  }
  const api={LIMITS,CSV_COLUMNS,sortCables,endName,shortName,faceOf,schedule,csv,labels,notes};
  root.LabRaxCableSheet=api;if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(globalThis);
