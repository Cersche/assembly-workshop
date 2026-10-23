// Advice for an unsaved cable plan. Real fit, capacity and bend tolerance remain UNKNOWN.
(function(root){
  'use strict';
  const U=44.45;
  const RULES={
    'power-post':'Separate power and data','missing-guide':'Add a support guide',
    'one-exit':'Use one exit','top-exit':'Keep the top clear','keystone':'Use a keystone',
    'service-loop':'Leave a service loop','short-run':'Simplify a short run',
    bend:'Tight bend guidance',crowded:'Guide crowding','one-ended':'Connect the other end',
    'unused-ports':'Unused ports',adapter:'Plan an adapter cable'};
  const BEND_FACTOR={rj45:4,other:10};
  const list=(rack,key)=>rack.cabling?.[key]||[];
  const outside=end=>typeof end?.endpoint==='string';
  const portEnd=end=>end&&typeof end.allocation==='string'&&typeof end.port==='string';
  const unique=values=>[...new Set(values)];
  const portKeys=c=>[c.from,c.to].filter(portEnd).map(e=>e.allocation+'/'+e.port);
  const powerPost=rack=>rack.cabling?.settings?.power_post||'RR';
  const dataPost=rack=>powerPost(rack)==='RR'?'RL':'RR';
  const label=(g,rack)=>g.post+' U'+String(rack.slots-g.slot+1).padStart(2,'0');
  function portsFor(rack,placement,ctx){
    return ctx.ports.portsFor(rack,placement,(ctx.library||[]).find(i=>i.id===placement.equipment))||[];
  }
  function portInfo(rack,end,ctx){
    const placement=portEnd(end)&&(rack.placements||[]).find(p=>p.id===end.allocation);
    return placement?portsFor(rack,placement,ctx).find(p=>p.id===end.port):null;
  }
  function carries(rack,cable,ctx){
    if(cable.carries==='power'||cable.carries==='data')return cable.carries;
    if(['iec','dc-barrel'].includes(cable.type))return 'power';
    if(cable.type==='usb-c'&&[cable.from,cable.to].some(e=>{
      const p=portInfo(rack,e,ctx);return p&&(/power/i.test(p.label)||/power/i.test(p.id));
    }))return 'power';
    return 'data';
  }
  function endSlots(rack,c,ctx){
    const slot=end=>{const p=ctx.cables.endAnchor(rack,end,ctx);return p?Math.max(1,Math.min(rack.slots,rack.slots-Math.floor(p[2]/U))):null;};
    const a=slot(c.from),b=slot(c.to),exit=list(rack,'exits').find(e=>e.id===c.route?.exit);
    return [outside(c.from)?exit?.slot??b:a,outside(c.to)?exit?.slot??a:b];
  }
  function cablePost(rack,c,gs,ctx){
    const posts=unique(gs.map(g=>g.post));
    if(posts.length)return posts.length===1?posts[0]:null;
    const front=[c.from,c.to].every(e=>portEnd(e)&&ctx.cables.endFace(rack,e,ctx)==='front');
    const anchors=[c.from,c.to].map(e=>ctx.cables.endAnchor(rack,e,ctx)).filter(Boolean);
    const mean=anchors.length?anchors.reduce((sum,p)=>sum+p[0],0)/anchors.length:0;
    return (front?'F':'R')+(mean<0?'L':'R');
  }
  function signature(rack,involves){
    const select=(key,ids,fields)=>ids.map(id=>{
      const value=list(rack,key).find(v=>v.id===id);
      return value?fields.map(k=>value[k]):null;
    });
    const state=[select('cables',involves.cables,['from','to','type','carries','route','service_loop_m','unplug_often']),
      select('guides',involves.guides,['post','slot']),select('exits',involves.exits,['position','slot']),involves.ports];
    // FNV-1a over the UTF-8 bytes of JSON, including non-ASCII endpoint names/ids.
    let hash=0x811c9dc5;
    for(const ch of unescape(encodeURIComponent(JSON.stringify(state))))hash=Math.imul(hash^ch.charCodeAt(0),0x01000193)>>>0;
    return hash.toString(16).padStart(8,'0');
  }
  function suggestions(rack,ctx,{includeIgnored=false}={}){
    const result=[],cables=list(rack,'cables'),guides=list(rack,'guides'),exits=list(rack,'exits');
    const guideMap=new Map(guides.map(g=>[g.id,g]));
    function add(rule,subject,title,detail,involves={},apply=null,applyLabel=null,level='suggest'){
      involves=Object.fromEntries(['cables','guides','ports','exits'].map(k=>[k,unique(involves[k]||[]).sort()]));
      const id=rule+':'+subject,sig=signature(rack,involves);
      const ignored=(rack.cabling?.settings?.ignored_suggestions||[]).some(v=>v.id===id&&v.sig===sig);
      if(includeIgnored||!ignored)result.push({id,rule,level,title,detail,involves,apply,applyLabel,sig,ignored});
    }
    const missing=new Map();
    for(const c of cables){
      const mismatch=ctx.cables.connectorMismatch(rack,c,ctx);
      if(mismatch){
        const labelA=ctx.ports.TYPES[mismatch.from]?.label||mismatch.from,labelB=ctx.ports.TYPES[mismatch.to]?.label||mismatch.to;
        add('adapter',c.id,c.number+' needs an adapter cable','One end is '+labelA+', the other '+labelB+'. Plan an adapter cable or adapter; its fit is UNKNOWN.',{cables:[c.id],ports:portKeys(c)},null,null,'info');
      }
      const gs=(c.route?.guides||[]).map(id=>guideMap.get(id)).filter(Boolean),[a,b]=endSlots(rack,c,ctx);
      const involved={cables:[c.id],guides:gs.map(g=>g.id),ports:portKeys(c),exits:c.route?.exit?[c.route.exit]:[]};
      const target=carries(rack,c,ctx)==='power'?powerPost(rack):dataPost(rack);
      if(gs.length&&gs.every(g=>g.post==='RL'||g.post==='RR')&&gs.some(g=>g.post!==target)){
        const selected=a==null||b==null?[]:guides.filter(g=>g.post===target&&g.slot>=Math.min(a,b)&&g.slot<=Math.max(a,b))
          .sort((x,y)=>(a<=b?1:-1)*(x.slot-y.slot)).map(g=>g.id);
        const cross=unique(gs.map(g=>g.post)).length>1;
        add('power-post',c.id,'Move '+c.number+' to '+target,
          (cross?'This cable crosses between the rear posts. ':(carries(rack,c,ctx)==='power'?'Power':'Data')+' belongs on '+target+'. ')+
          (selected.length?'Use the guides on '+target+'.':'Add a guide on '+target+' first.'),
          {...involved,guides:unique([...involved.guides,...selected])},
          selected.length?{kind:'move-post',cable:c.id,guides:selected}:null,selected.length?'Move to '+target:null);
      }
      const post=cablePost(rack,c,gs,ctx),supports=[a,...gs.map(g=>g.slot),b].filter(s=>s!=null);
      if(post)for(let i=1;i<supports.length;i++)if(Math.abs(supports[i]-supports[i-1])>2){
        const slot=Math.round((supports[i]+supports[i-1])/2),key=post+':'+slot;
        if(guides.some(g=>g.post===post&&g.slot===slot))continue;
        if(!missing.has(key))missing.set(key,{post,slot,cables:[],guides:[],ports:[],exits:[]});
        const entry=missing.get(key);for(const k of ['cables','guides','ports','exits'])entry[k].push(...involved[k]);
      }
      if(c.unplug_often===true&&![c.from,c.to].some(e=>portInfo(rack,e,ctx)?.type==='keystone'))
        add('keystone',c.id,'Consider a keystone for '+c.number,'A pass-through may help when this cable is unplugged often. Fit is UNKNOWN.',involved);
      if((c.service_loop_m??rack.cabling?.settings?.service_loop_m??0.15)===0&&[c.from,c.to].some(portEnd))
        add('service-loop',c.id,'Leave a service loop for '+c.number,'Allow extra cable for access; the required length is UNKNOWN.',involved);
      const anchors=[c.from,c.to].map(e=>portEnd(e)?ctx.cables.endAnchor(rack,e,ctx):null);
      // Suppress subtraction noise when port heights are exactly one U apart.
      const heightNoise=anchors.every(Boolean)?Number.EPSILON*Math.max(U,...anchors.map(p=>Math.abs(p[2])))*4:0;
      if(anchors.every(Boolean)&&Math.abs(anchors[0][2]-anchors[1][2])<U-heightNoise&&gs.length)
        add('short-run',c.id,'Simplify '+c.number,'The port ends are less than one U apart in height.',involved,{kind:'drop-guides',cable:c.id},'Drop guides');
      const points=ctx.cables.path(rack,c,ctx),tight=[],bendGuides=[];
      const factor=c.type==='rj45'?BEND_FACTOR.rj45:BEND_FACTOR.other;
      const diameter=(ctx.cables.TYPE_STYLE[c.type]||ctx.cables.TYPE_STYLE.other).diameter_mm;
      const firstGuide=ctx.cables.endAnchor(rack,c.from,ctx)?1:0;
      for(let i=1;i<points.length-1;i++){
        const incoming=points[i].map((n,j)=>n-points[i-1][j]),outgoing=points[i+1].map((n,j)=>n-points[i][j]);
        const la=Math.hypot(...incoming),lb=Math.hypot(...outgoing);
        if(!la||!lb)continue; // A repeated point has no defined turn angle.
        const cosine=Math.max(-1,Math.min(1,incoming.reduce((s,n,j)=>s+n*outgoing[j],0)/(la*lb)));
        const angle=Math.acos(cosine);if(angle<=1e-12)continue;
        const radius=Math.min(la,lb)/2/Math.tan(angle/2);
        if(radius<factor*diameter){tight.push(radius);const g=gs[i-firstGuide];if(g)bendGuides.push(g.id);}
      }
      if(tight.length)add('bend',c.id,'Tight turns in '+c.number,
        tight.length+' tight turn'+(tight.length===1?'':'s')+'; tightest radius '+Math.round(Math.min(...tight))+' mm. Nominal sizes, guidance only; '+
        (c.type==='rj45'?'4 × diameter.':'10 × diameter is a generic rule of thumb.')+' Real bend tolerance is UNKNOWN.',
        {...involved,guides:bendGuides},null,null,'guidance');
      if(c.from==null||c.to==null)add('one-ended',c.id,'Connect the other end of '+c.number,'This cable has an unconnected end.',involved);
    }
    for(const [key,m] of missing)add('missing-guide',key,'Add a guide at '+label(m,rack),
      'The planned run spans more than two U between supports. Guide fit is UNKNOWN.',m,{kind:'add-guide',post:m.post,slot:m.slot},'Add guide');
    const used=cables.filter(c=>c.route?.exit&&[c.from,c.to].some(outside));
    const count=e=>used.filter(c=>c.route.exit===e.id).length;
    const mostUsed=items=>items.slice().sort((a,b)=>count(b)-count(a))[0];
    const usedExits=exits.filter(e=>count(e)>0);
    if(usedExits.length>1){
      const target=mostUsed(usedExits.filter(e=>e.position!=='top-rear'))||mostUsed(usedExits);
      const moving=used.filter(c=>c.route.exit!==target.id);
      add('one-exit','all','Use one cabinet exit','Bring outside runs together at the '+((ctx.cables.EXIT_POSITIONS||{})[target.position]||target.position).toLowerCase()+' exit (U'+String(rack.slots-target.slot+1).padStart(2,'0')+').',
        {cables:used.map(c=>c.id),exits:usedExits.map(e=>e.id),ports:used.flatMap(portKeys)},
        {kind:'set-exit',cables:moving.map(c=>c.id),exit:target.id},'Use this exit');
    }
    for(const e of exits.filter(e=>e.position==='top-rear')){
      const users=cables.filter(c=>c.route?.exit===e.id);if(!users.length)continue;
      const alternatives=exits.filter(x=>x.position!=='top-rear');
      const allCount=id=>cables.filter(c=>c.route?.exit===id).length;
      const target=alternatives.slice().sort((a,b)=>allCount(b.id)-allCount(a.id))[0];
      add('top-exit',e.id,'Keep the top fan panel clear','Move these runs away from the top fan panel'+(target?'.':'; add another exit first.'),
        {cables:users.map(c=>c.id),exits:[e.id,...(target?[target.id]:[])],ports:users.flatMap(portKeys)},
        target?{kind:'set-exit',cables:users.map(c=>c.id),exit:target.id}:null,target?'Use another exit':null);
    }
    const load=ctx.cables.guideLoad(rack);
    for(const id of ctx.cables.crowded(rack)){
      const g=guideMap.get(id);if(!g)continue;
      add('crowded',id,'Crowding at '+label(g,rack),load[id]+' cables exceeds your setting of '+(rack.cabling?.settings?.guide_warn_above??6)+'. Capacity is UNKNOWN.',
        {guides:[id],cables:cables.filter(c=>c.route?.guides?.includes(id)).map(c=>c.id)});
    }
    for(const placement of rack.placements||[]){
      const ports=portsFor(rack,placement,ctx),unused=ports.filter(p=>!ctx.cables.portInUse(rack,placement.id,p.id));
      if(!unused.length)continue;
      const item=(ctx.library||[]).find(i=>i.id===placement.equipment),name=(placement.assembly?.name||item?.name||'Equipment')+' (U'+String(rack.slots-(placement.slot+(placement.span||1)-1)+1).padStart(2,'0')+((placement.span||1)>1?'–U'+String(rack.slots-placement.slot+1).padStart(2,'0'):'')+')';
      add('unused-ports',placement.id,name+': '+unused.length+' of '+ports.length+' ports unused','These ports have no planned cable.',
        {ports:unused.map(p=>p.key)},null,null,'info');
    }
    const order=Object.keys(RULES);
    return result.sort((a,b)=>order.indexOf(a.rule)-order.indexOf(b.rule)||(a.id<b.id?-1:a.id>b.id?1:0));
  }
  function applySuggestion(rack,suggestion,ctx){
    const action=suggestion?.apply,fail=message=>({ok:false,message});
    if(!action||!['move-post','add-guide','set-exit','drop-guides'].includes(action.kind))return fail('This suggestion has no supported action.');
    const refs={cables:[...(suggestion.involves?.cables||[])],guides:[...(suggestion.involves?.guides||[])],exits:[...(suggestion.involves?.exits||[])]};
    if(action.cable)refs.cables.push(action.cable);
    if(action.cables)refs.cables.push(...action.cables);
    if(action.guides)refs.guides.push(...action.guides);
    if(action.exit)refs.exits.push(action.exit);
    for(const key of Object.keys(refs))if(refs[key].some(id=>!list(rack,key).some(v=>v.id===id)))return fail('The cable plan changed; refresh the suggestions.');
    // Also check references retained by the action before upkeep can silently drop them.
    for(const c of list(rack,'cables').filter(c=>refs.cables.includes(c.id))){
      if((c.route?.guides||[]).some(id=>!list(rack,'guides').some(g=>g.id===id))||
        (c.route?.exit!=null&&!list(rack,'exits').some(e=>e.id===c.route.exit)))return fail('The cable route changed; refresh the suggestions.');
    }
    let newGuide;
    if(action.kind==='add-guide'){
      if(!['FL','FR','RL','RR'].includes(action.post)||!Number.isInteger(action.slot)||action.slot<1||action.slot>rack.slots)return fail('Choose a post and slot inside this rack.');
      if(list(rack,'guides').some(g=>g.post===action.post&&g.slot===action.slot))return fail('A guide already occupies that post and slot.');
      const id=ctx.newId?.()||'guide-'+Array.from({length:12},()=>Math.floor(Math.random()*16).toString(16)).join('');
      if(typeof id!=='string'||!id.length||id.length>80||list(rack,'guides').some(g=>g.id===id))return fail('The new guide needs a unique id.');
      newGuide={id,kind:'labrax-cable-guide',post:action.post,slot:action.slot};
    }else if(action.kind==='move-post'){
      if(!action.cable||!Array.isArray(action.guides)||action.guides.length>48||new Set(action.guides).size!==action.guides.length)return fail('Choose a cable and a route without repeated guides.');
    }else if(action.kind==='set-exit'){
      if(!action.exit||!Array.isArray(action.cables)||!action.cables.length)return fail('Choose cables and an exit.');
    }else if(!action.cable)return fail('Choose a cable.');
    // Stage the edit so a failed upkeep cannot leave half an applied action in the draft.
    const staged={...rack,cabling:JSON.parse(JSON.stringify(rack.cabling||{}))};
    if(newGuide)(staged.cabling.guides??=[]).push(newGuide);
    else for(const c of list(staged,'cables')){
      if(action.kind==='set-exit'&&action.cables.includes(c.id))c.route={mode:'manual',guides:[...(c.route?.guides||[])],exit:action.exit};
      if(c.id===action.cable)c.route={mode:'manual',guides:action.kind==='move-post'?[...action.guides]:[],exit:c.route?.exit??null};
    }
    const previous=rack.cabling;
    rack.cabling=staged.cabling;
    try{ctx.cables.upkeep(rack,ctx);}catch(error){
      if(previous===undefined)delete rack.cabling;else rack.cabling=previous;
      return fail('Could not update the cable plan: '+error.message);
    }
    return {ok:true,message:'Applied to the unsaved cable plan.'};
  }
  function ignore(rack,suggestion){
    const settings=((rack.cabling??={}).settings??={});
    settings.ignored_suggestions=[...(settings.ignored_suggestions||[]).filter(e=>e.id!==suggestion.id),{id:suggestion.id,sig:suggestion.sig}].slice(-500);
  }
  function unignore(rack,id){
    const settings=rack.cabling?.settings;if(!settings?.ignored_suggestions)return;
    settings.ignored_suggestions=settings.ignored_suggestions.filter(e=>e.id!==id);
    if(!settings.ignored_suggestions.length)delete settings.ignored_suggestions;
  }
  function pruneIgnored(rack,ctx){
    const settings=rack.cabling?.settings;if(!settings?.ignored_suggestions)return 0;
    const current=new Map(suggestions(rack,ctx,{includeIgnored:true}).map(s=>[s.id,s.sig]));
    const before=settings.ignored_suggestions.length;
    settings.ignored_suggestions=settings.ignored_suggestions.filter(e=>current.get(e.id)===e.sig);
    const removed=before-settings.ignored_suggestions.length;
    if(!settings.ignored_suggestions.length)delete settings.ignored_suggestions;
    return removed;
  }
  const api={RULES,BEND_FACTOR,carries,powerPost,dataPost,suggestions,applySuggestion,ignore,unignore,pruneIgnored};
  root.LabRaxCableSuggest=api;if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(globalThis);
