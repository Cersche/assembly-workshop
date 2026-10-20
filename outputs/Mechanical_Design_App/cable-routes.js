// Cable planning only: lengths are estimates; physical fit and capacity are UNKNOWN.
(function(root){
  'use strict';
  const U=44.45;
  const EXIT_POSITIONS={'bottom-rear':'Bottom rear','top-rear':'Top rear',left:'Left side',right:'Right side'};
  const ENDPOINT_KINDS={'wall-outlet':'Wall outlet',ups:'UPS',modem:'Modem / ONT','wall-jack':'Wall jack',desk:'Desk','other-rack':'Another rack',other:'Other'};
  const TYPE_STYLE={
    rj45:{color:'#3fb6ff',diameter_mm:6},'usb-a':{color:'#6f8cff',diameter_mm:4.5},
    'usb-c':{color:'#b08cff',diameter_mm:4},hdmi:{color:'#ffb347',diameter_mm:7},
    'micro-hdmi':{color:'#ffb347',diameter_mm:5},'dc-barrel':{color:'#ff6b6b',diameter_mm:3.5},
    iec:{color:'#ff6b6b',diameter_mm:8},keystone:{color:'#5fe0b8',diameter_mm:6},other:{color:'#c3ccd6',diameter_mm:4}};
  const list=(rack,key)=>rack.cabling?.[key]||[];
  const outside=end=>!!end&&typeof end.endpoint==='string';
  const zmid=(rack,slot)=>(rack.slots-slot)*U+U/2;
  const slotAt=(rack,point)=>Math.max(1,Math.min(rack.slots,rack.slots-Math.floor(point[2]/U)));
  const guideAnchor=(rack,g)=>[g.post.endsWith('L')?-118.26:118.26,g.post.startsWith('R')?254:-14,zmid(rack,g.slot)];
  function exitAnchor(rack,e){
    if(e.position==='bottom-rear')return [0,250,-10];
    if(e.position==='top-rear')return [0,250,rack.slots*U+10];
    return [e.position==='left'?-140:140,220,zmid(rack,e.slot)];
  }
  const distance=(a,b)=>Math.hypot(...a.map((v,i)=>v-b[i]));
  function portInfo(rack,end,ctx){
    if(!end||outside(end)||!ctx?.ports)return null;
    const placement=(rack.placements||[]).find(p=>p.id===end.allocation);
    if(!placement)return null;
    const item=(ctx.library||[]).find(i=>i.id===placement.equipment);
    const port=(ctx.ports.portsFor(rack,placement,item)||[]).find(p=>p.id===end.port);
    return port?{placement,port}:null;
  }
  function connectorMismatch(rack,cable,ctx){
    const from=portInfo(rack,cable.from,ctx)?.port.type,to=portInfo(rack,cable.to,ctx)?.port.type;
    if(!from||!to||[from,to].some(t=>t==='keystone'||t==='other')||from===to)return null;
    const labelA=ctx.ports.TYPES[from]?.label||from,labelB=ctx.ports.TYPES[to]?.label||to;
    return {from,to,text:'Needs an adapter cable: '+labelA+' to '+labelB+'.'};
  }
  function cableColor(cable){return cable.color||(TYPE_STYLE[cable.type]||TYPE_STYLE.other).color;}
  function endAnchor(rack,end,ctx){
    const info=portInfo(rack,end,ctx);if(!info)return null;
    const p=info.port,offset={front:[0,-8],rear:[0,8],right:[8,0],left:[-8,0]}[p.points||p.face||'rear'];
    return [p.x+(offset?.[0]||0),p.y+(offset?.[1]||0),ctx.ports.baseZ(rack,info.placement)+p.z];
  }
  function endFace(rack,end,ctx){
    if(outside(end))return 'rear';
    const face=portInfo(rack,end,ctx)?.port.face;
    return face==='front'||face==='rear'?face:null;
  }
  function autoRoute(rack,cable,ctx){
    const a=endAnchor(rack,cable.from,ctx),b=endAnchor(rack,cable.to,ctx),known=[a,b].filter(Boolean);
    const front=!outside(cable.from)&&!outside(cable.to)&&endFace(rack,cable.from,ctx)==='front'&&endFace(rack,cable.to,ctx)==='front';
    const mean=known.length?known.reduce((sum,p)=>sum+p[0],0)/known.length:0;
    const post=(front?'F':'R')+(mean<0?'L':'R');
    function guidesFor(exit){
      const sa=a?slotAt(rack,a):outside(cable.from)&&exit?exit.slot:b?slotAt(rack,b):exit?.slot;
      const sb=b?slotAt(rack,b):outside(cable.to)&&exit?exit.slot:a?slotAt(rack,a):exit?.slot;
      if(sa==null||sb==null)return [];
      return list(rack,'guides').filter(g=>g.post===post&&g.slot>=Math.min(sa,sb)&&g.slot<=Math.max(sa,sb))
        .slice().sort((x,y)=>(sa<=sb?1:-1)*(x.slot-y.slot));
    }
    let exit=null;
    if(outside(cable.from)||outside(cable.to)){
      exit=list(rack,'exits').find(e=>e.id===cable.route?.exit)||null;
      if(!exit){
        // Score each candidate with the guides it would use, avoiding iteration/oscillation.
        let best=Infinity;
        for(const candidate of list(rack,'exits')){
          const guides=guidesFor(candidate);
          const last=guides.length?guideAnchor(rack,guides[guides.length-1]):b||a;
          const score=last?distance(last,exitAnchor(rack,candidate)):0;
          if(score<best){best=score;exit=candidate;}
        }
      }
    }
    return {guides:guidesFor(exit).map(g=>g.id),exit:exit?.id||null};
  }
  function path(rack,cable,ctx){
    const route=cable.route||autoRoute(rack,cable,ctx),points=[];
    const from=endAnchor(rack,cable.from,ctx);if(from)points.push(from);
    for(const id of route.guides||[]){const g=list(rack,'guides').find(g=>g.id===id);if(g)points.push(guideAnchor(rack,g));}
    const exit=list(rack,'exits').find(e=>e.id===route.exit);if(exit)points.push(exitAnchor(rack,exit));
    const to=endAnchor(rack,cable.to,ctx);if(to)points.push(to);
    return points;
  }
  function estimate(rack,cable,ctx){
    const points=path(rack,cable,ctx);
    const route_mm=points.slice(1).reduce((sum,p,i)=>sum+distance(points[i],p),0);
    const loop=cable.service_loop_m??rack.cabling?.settings?.service_loop_m??0.15;
    const count=[cable.from,cable.to].filter(e=>e&&!outside(e)).length;
    const metres=route_mm/1000+loop*count;
    // Suppress only floating-point noise at exact tenth-metre boundaries.
    const length_m=Math.max(0,Math.ceil(metres*10-Number.EPSILON*Math.max(1,metres*10)*4)/10);
    return {route_mm,length_m,to_exit:outside(cable.from)||outside(cable.to),complete:cable.from!=null&&cable.to!=null};
  }
  function portInUse(rack,allocation,port,exceptCableId){
    return list(rack,'cables').find(c=>c.id!==exceptCableId&&[c.from,c.to].some(e=>e?.allocation===allocation&&e?.port===port))?.id||null;
  }
  function linkedCable(rack,cable,ctx){
    for(const end of [cable.from,cable.to]){
      const info=portInfo(rack,end,ctx);
      if(info?.port.passThrough){const id=portInUse(rack,end.allocation,info.port.passThrough,cable.id);if(id)return id;}
    }
    return null;
  }
  function nextNumber(rack){const used=new Set(list(rack,'cables').map(c=>c.number));let n=1;while(used.has('C'+n))n++;return 'C'+n;}
  function guideLoad(rack){
    const counts={};
    for(const cable of list(rack,'cables'))for(const id of new Set(cable.route?.guides||[])){
      Object.defineProperty(counts,id,{value:(Object.hasOwn(counts,id)?counts[id]:0)+1,writable:true,enumerable:true,configurable:true});
    }
    return counts;
  }
  function crowded(rack){const limit=rack.cabling?.settings?.guide_warn_above??6;return Object.entries(guideLoad(rack)).filter(([,n])=>n>limit).map(([id])=>id);}
  // In-memory observations detect moved manual guide anchors without adding stored schema fields.
  // The first upkeep establishes the baseline; an already-moved loaded document has no prior positions.
  const previousGuides=new WeakMap();
  function upkeep(rack,ctx){
    const guides=new Map(list(rack,'guides').map(g=>[g.id,JSON.stringify(guideAnchor(rack,g))]));
    const before=previousGuides.get(rack);
    const exits=new Set(list(rack,'exits').map(e=>e.id)),endpoints=new Set(list(rack,'endpoints').map(e=>e.id));
    for(const cable of list(rack,'cables')){
      for(const key of ['from','to']){const end=cable[key];if(end&&(outside(end)?!endpoints.has(end.endpoint):!portInfo(rack,end,ctx)))cable[key]=null;}
      if(cable.route?.mode!=='manual')cable.route={mode:'auto',...autoRoute(rack,cable,ctx)};
      else{
        const old=cable.route.guides||[],kept=old.filter(id=>guides.has(id));
        const removedExit=cable.route.exit!=null&&!exits.has(cable.route.exit);
        const moved=kept.some(id=>before?.has(id)&&before.get(id)!==guides.get(id));
        if(kept.length!==old.length||removedExit||moved)cable.route_changed=true;
        cable.route.guides=kept;if(removedExit)cable.route.exit=null;
      }
    }
    previousGuides.set(rack,guides);
    return list(rack,'cables');
  }
  function warnings(rack,cable,ctx){
    const out=[];
    if(cable.from==null||cable.to==null)out.push('Unconnected cable end.');
    if((outside(cable.from)||outside(cable.to))&&!list(rack,'exits').length)out.push('Outside endpoint has no exit in this rack.');
    if([cable.from,cable.to].some(e=>e&&!outside(e)&&endFace(rack,e,ctx)===null))out.push('Port face UNKNOWN; routing uses the rear by default.');
    if(cable.route_changed)out.push('Cable route changed.');
    const busy=new Set(crowded(rack));
    if((cable.route?.guides||[]).some(id=>busy.has(id)))out.push('Guide over the crowding setting; capacity UNKNOWN.');
    const mismatch=connectorMismatch(rack,cable,ctx);if(mismatch)out.push(mismatch.text);
    return out;
  }
  const api={EXIT_POSITIONS,ENDPOINT_KINDS,TYPE_STYLE,cableColor,endAnchor,endFace,autoRoute,path,estimate,linkedCable,portInUse,nextNumber,guideLoad,crowded,upkeep,warnings,connectorMismatch};
  root.LabRaxCables=api;if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(globalThis);
