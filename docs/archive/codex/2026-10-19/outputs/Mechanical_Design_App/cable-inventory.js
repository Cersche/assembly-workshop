// Planning inventory. The caller supplies the saved rack; no persistence or geometry.
(function(root){
  'use strict';
  const LIMITS='Lengths are planning estimates. Jack type, guide capacity, cable fit and strength are UNKNOWN. No prices or purchases.';
  const STOCK_LENGTHS_M=[0.15,0.3,0.5,1,1.5,2,3,5];
  const CSV_COLUMNS=['Section','Item','Quantity','Buy or print','Cables','Notes'];
  const list=(rack,key)=>rack.cabling?.[key]||[];
  function stockLength(m){return Number.isFinite(m)?STOCK_LENGTHS_M.find(n=>n>=m)??null:null;}
  function items(rack,ctx){
    const placements=rack.placements||[],groups=new Map();
    const ports=p=>ctx.ports.portsFor(rack,p,(ctx.library||[]).find(i=>i.id===p.equipment))||[];
    function exists(end){
      if(!end)return false;
      if(typeof end.endpoint==='string')return list(rack,'endpoints').some(e=>e.id===end.endpoint);
      const p=placements.find(p=>p.id===end.allocation);
      return !!p&&ports(p).some(p=>p.id===end.port);
    }
    const sorted=list(rack,'cables').slice().sort((a,b)=>String(a.number).localeCompare(String(b.number),undefined,{numeric:true})||String(a.id).localeCompare(String(b.id)));
    for(const cable of sorted){
      const estimate=ctx.cables.estimate(rack,cable,ctx),stock=stockLength(estimate.length_m),type=cable.type||'';
      const key='cable:'+type+':'+(stock??'custom'),label=ctx.ports.TYPES[type]?.label||type||'Unknown type';
      if(!groups.has(key))groups.set(key,{label,stock,max:estimate.length_m,row:{section:'cables',key,item:'',quantity:0,source:'buy',cables:[],notes:[]}});
      const g=groups.get(key);g.max=Math.max(g.max,estimate.length_m);g.row.quantity++;g.row.cables.push(cable.number);
      if((estimate.complete===false||!exists(cable.from)||!exists(cable.to))&&!g.row.notes.length)g.row.notes.push('check: incomplete');
    }
    const rows=[...groups.values()].sort((a,b)=>a.label.localeCompare(b.label)||(a.stock??Infinity)-(b.stock??Infinity)||a.row.key.localeCompare(b.row.key)).map(g=>{
      g.row.item=g.label+' · '+(g.stock===null?'custom length (≥ '+g.max+' m)':g.stock+' m');return g.row;
    });
    const quantity=placements.reduce((n,p)=>n+new Set(ports(p).filter(p=>p.type==='keystone').map(p=>/^ks-(\d+)-(front|rear)$/.exec(p.id)).filter(Boolean).map(m=>m[1])).size,0);
    if(quantity)rows.push({section:'keystones',key:'keystones',item:'Keystone jack',quantity,source:'buy',cables:[],notes:['Jack type UNKNOWN']});
    if(list(rack,'guides').length)rows.push({section:'guides',key:'guides',item:'Lab Rax Cable Guide',quantity:list(rack,'guides').length,source:'print',cables:[],notes:['Local model only; not in PRINT THE RACK; never redistributed']});
    return rows;
  }
  function csvField(value){
    let text=String(value);if(/^[=+\-@\t\r]/.test(text))text="'"+text;
    return '"'+text.replace(/"/g,'""')+'"';
  }
  function csv(rack,ctx,meta={}){
    const rows=[CSV_COLUMNS,...items(rack,ctx).map(r=>[r.section,r.item,r.quantity,r.source,r.cables.join(' '),r.notes.join('; ')])];
    rows.push(['','','','','',LIMITS]);
    if(meta.savedAt)rows.push(['','','','','','Saved '+meta.savedAt]);
    return '\uFEFF'+rows.map(r=>r.map(csvField).join(',')+'\r\n').join('');
  }
  const api={LIMITS,STOCK_LENGTHS_M,CSV_COLUMNS,stockLength,items,csv};
  root.LabRaxCableInventory=api;if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(globalThis);
