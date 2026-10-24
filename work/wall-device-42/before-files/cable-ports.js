// Cable-planning ports (cable management Step 2). Planning data only: no geometry, STL or hardware pins.
// Frame: X from the rack centre, Y depth from the faceplate rear face (plate front is negative Y), Z above the
// equipment's base in the rack view. Connector fit, cable access and rear clearance stay UNKNOWN.
(function(root){
  'use strict';
  const PITCH=44.45;
  // Connector types: label, marker colour (data / USB / video / power families) and nominal face outline (mm).
  const TYPES={
    rj45:{label:'RJ45 (Ethernet)',color:'#3fb6ff'},
    'usb-a':{label:'USB-A',color:'#6f8cff'},
    'usb-c':{label:'USB-C',color:'#b08cff'},
    hdmi:{label:'HDMI',color:'#ffb347'},
    'micro-hdmi':{label:'Micro-HDMI',color:'#ffb347'},
    'dc-barrel':{label:'DC barrel',color:'#ff6b6b'},
    iec:{label:'IEC power inlet',color:'#ff6b6b'},
    keystone:{label:'Keystone (pass-through)',color:'#5fe0b8'},
    other:{label:'Other',color:'#c3ccd6'}};
  const FACES={front:'Front',rear:'Rear'};
  // Direction the connector opening points: row-major rotation about Z (world = R·local, as the renderer applies it)
  // that turns the marker's outward −Y onto that direction. Rotations only, never mirrors.
  const POINTS={front:[1,0,0,0,1,0,0,0,1],rear:[-1,0,0,0,-1,0,0,0,1],right:[0,-1,0,1,0,0,0,0,1],left:[0,1,0,-1,0,0,0,0,1]};
  const POINT_LABELS={front:'toward the front (−Y)',rear:'toward the rear (+Y)',right:'toward the rack’s right side (+X)',left:'toward the rack’s left side (−X)'};
  // equipment_tray.scad: plate front at Y = −plate_t (4), device front at front_gap (12) + dev_off_y, keystone opening
  // centred on the plate, device base lifted by the standoff (none for straps).
  const WIZ={plateT:4,frontGap:12};
  const lift=s=>PO().deviceLift(s);
  // Rear port of the device (X from the device centre, Z from the plate bottom at the library standoff) -> this slot's
  // tray: offset, rotation (equipment_tray.scad dp()) and standoff change. Returns position and pointing direction.
  function rearPort(lib,s,p){
    const w=+s.dev_w||0,d=+s.dev_d||0,rot=+s.dev_rot||0,turned=rot===90||rot===270,fpW=turned?d:w;
    const px=+p.x+w/2,q=rot===90?[0,px]:rot===180?[w-px,0]:rot===270?[d,w-px]:[px,d];
    return {x:-fpW/2+(+s.dev_off_x||0)+q[0],y:(s.device_mount==='sleeve'?-WIZ.plateT:WIZ.frontGap+(+s.dev_off_y||0))+q[1],z:+p.z+lift(s)-lift(lib),
      points:rot===90?'left':rot===180?'front':rot===270?'right':'rear'};
  }
  // spec = library item spec; tray = this slot's placement.tray (its keys win, as equipment.allocation_spec()).
  // Front openings follow the device's offset and standoff (port-openings.js, Brian 2026-10-19); a turned device keeps
  // them where they were entered, as its faceplate STL does.
  function PO(){if(root.LabRaxPortOpenings)return root.LabRaxPortOpenings;
    if(typeof module!=='undefined'&&typeof require==='function'){try{return require('./port-openings.js');}catch(e){}}return null;}
  function wizardPorts(spec,tray){
    if(!spec)return [];const P=PO(),s=spec.faceplate_only?P.faceplateSpec(tray?.faceplate):{...spec,...(tray||{})},out=[],plateCenter=(+s.u||1)*PITCH/2;
    (P&&tray?P.frontOpenings(spec,tray).ports:s.ports||[]).forEach((p,i)=>out.push({id:p.id||'front-'+(i+1),label:p.label||'Port '+(i+1),type:TYPES[p.type]?p.type:'other',face:'front',x:+p.x,y:-WIZ.plateT,z:+p.z,points:'front',opening:true}));
    (s.rear_ports||[]).forEach((p,i)=>out.push({id:p.id||'rear-'+(i+1),label:p.label||'Rear port '+(i+1),type:TYPES[p.type]?p.type:'other',face:'rear',...rearPort(spec,s,p)}));
    // Keystones are pass-through ports: one front face and one rear face, paired by passThrough.
    (s.keystones||[]).forEach((position,i)=>{const id='ks-'+(i+1),x=Array.isArray(position)?position[0]:position,z=Array.isArray(position)&&position.length>1?position[1]:plateCenter;
      out.push({id:id+'-front',label:'Keystone '+(i+1)+' · front',type:'keystone',face:'front',x:+x,y:-WIZ.plateT,z,points:'front',passThrough:id+'-rear'});
      out.push({id:id+'-rear',label:'Keystone '+(i+1)+' · rear',type:'keystone',face:'rear',x:+x,y:0,z,points:'rear',passThrough:id+'-front'});});
    for(const p of spec.planning_ports||[]){
      const angle=(+s.dev_rot||0)*Math.PI/180,dx=p.x-(+spec.dev_off_x||0),dy=p.y-((spec.device_mount==='sleeve'?-WIZ.plateT:12+(+spec.dev_off_y||0))+spec.dev_d/2);
      out.push({...p,x:(+s.dev_off_x||0)+dx*Math.cos(angle)-dy*Math.sin(angle),
        y:(s.device_mount==='sleeve'?-WIZ.plateT:12+(+s.dev_off_y||0))+(s.dev_rot===90||s.dev_rot===270?s.dev_w:s.dev_d)/2+dx*Math.sin(angle)+dy*Math.cos(angle),
        z:p.z+lift(s)-lift(spec),points:['front','right','rear','left'][(['front','right','rear','left'].indexOf(p.points||'front')+(+s.dev_rot||0)/90)%4],opening:false});
    }
    return out.filter(p=>[p.x,p.y,p.z].every(Number.isFinite));
  }
  // Two devices on one tray (Brian, 2026-10-20): the second device's ports join the slot's list with a "d2-" id and its
  // name on the label; keystones belong to the shared faceplate and come from the first device only.
  function secondPorts(placement,library){
    const s=placement?.second,it=s&&(library||root.equipmentLibraryItems?.()||[]).find(i=>i.id===s.equipment);if(!it)return [];
    const shared={};for(const k of ['u','joint','rear_support'])if(placement.tray&&k in placement.tray)shared[k]=placement.tray[k];
    const name=it.display_name||it.name||'Device 2';
    return wizardPorts({...it.spec,keystones:[]},{...shared,...(s.tray||{}),keystones:[]}).map(p=>({...p,id:'d2-'+p.id,label:name+' · '+p.label,device:2}));
  }
  function basePorts(placement,item,library){
    return item?[...wizardPorts(item.spec,placement?.tray),...secondPorts(placement,library)].map(p=>({...p,source:'wizard',note:p.type==='keystone'?'Keystone pass-through from the wizard. Rear marker sits on the plate rear face; the jack body depth is UNKNOWN.':p.face==='front'?'Faceplate opening from the wizard Ports step.':(placement?.tray?'Rear port from the wizard Ports step (no opening), moved with this slot’s tray placement.':'Rear port from the wizard Ports step (no opening). Position as entered.')})):null;
  }
  // All equipment uses the allocation bottom as its rack-view base.
  function baseZ(rack,placement){return (rack.slots-(placement.slot+placement.span-1))*PITCH;}
  const overridesFor=(rack,placement)=>(rack?.cabling?.ports||[]).filter(o=>o.allocation===placement.id);
  // Effective ports of one placement: preset or wizard ports, then the saved per-rack edits (mesh-click positions,
  // label/type/face changes) and custom ports. Key = allocation id / port id, stable while the slot moves.
  function portsFor(rack,placement,item){
    const base=basePorts(placement,item);if(base===null)return [];const edits=overridesFor(rack,placement),out=[];
    for(const p of base){const o=edits.find(e=>e.port===p.id&&!e.custom)||{};const tuned=['x','y','z'].some(k=>k in o);
      out.push({...p,...pick(o),tuned,edited:Object.keys(pick(o)).length>0,key:placement.id+'/'+p.id,allocation:placement.id});}
    for(const o of edits)if(o.custom)out.push({points:o.face||'front',y:o.face==='rear'?60:-4,...pick(o),id:o.port,custom:true,source:'custom',note:'Custom port added in this rack. Position as set.',key:placement.id+'/'+o.port,allocation:placement.id});
    for(const p of out)if(!p.points)p.points=p.face||'front';
    return out;
  }
  function pick(o){const r={};for(const k of ['label','type','face','x','y','z'])if(k in o)r[k]=o[k];return r;}
  // Write one edit into rack.cabling.ports (draft only). changes=null removes the entry (reset / remove custom).
  function setOverride(rack,allocation,port,changes,custom=false){
    const list=(rack.cabling?.ports||[]).filter(o=>!(o.allocation===allocation&&o.port===port));
    if(changes){const old=(rack.cabling?.ports||[]).find(o=>o.allocation===allocation&&o.port===port)||{};const next={...old,...changes,allocation,port};if(custom)next.custom=true;
      for(const k of ['x','y','z'])if(k in next)next[k]=Math.round(next[k]*100)/100;list.push(next);}
    if(list.length)rack.cabling={...(rack.cabling||{}),ports:list};
    else if(rack.cabling){const {ports,...rest}=rack.cabling;if(Object.keys(rest).length)rack.cabling=rest;else delete rack.cabling;}
    return list;
  }
  // Keep only edits whose allocation still exists (a released slot's edits are dropped at Save).
  function prune(rack){if(!rack?.cabling?.ports)return rack;const ids=new Set(rack.placements.map(p=>p.id)),ports=rack.cabling.ports.filter(o=>ids.has(o.allocation));
    const cabling={...rack.cabling,ports};if(!ports.length)delete cabling.ports;const next={...rack};if(Object.keys(cabling).length)next.cabling=cabling;else delete next.cabling;return next;}
  function newPortId(rack,allocation){let id;do id='custom-'+Math.random().toString(36).slice(2,8);while((rack.cabling?.ports||[]).some(o=>o.allocation===allocation&&o.port===id));return id;}
  // Scene parts for the rack renderer: one connector-shaped marker per port (mesh key 'port-<type>').
  function markerParts(rack,placements,library,selectedKey){
    const parts=[];
    for(const placement of placements){const item=(library||[]).find(i=>i.id===placement.equipment),z0=baseZ(rack,placement);
      for(const p of portsFor(rack,placement,item))parts.push({key:'port-'+(TYPES[p.type]?p.type:'other'),R:POINTS[p.points]||POINTS.front,t:[p.x,p.y,z0+p.z],kind:'port',port:p.key,tint:TYPES[p.type]?.color||TYPES.other.color,selected:p.key===selectedKey});}
    return parts;
  }
  // Point on the device mesh (scene coordinates) -> port position relative to that allocation.
  // Clamped to the ranges cable_ports.py accepts, so a stray hit can't make the rack unsaveable.
  const clamp=(v,lo,hi)=>Math.min(hi,Math.max(lo,v));
  function positionFromHit(rack,placement,point){return {x:clamp(point[0],-150,150),y:clamp(point[1],-40,280),z:clamp(point[2]-baseZ(rack,placement),-10,placement.span*PITCH+10)};}
  // Connector-face markers: outline in X–Z, 2.5 mm deep toward −Y (outward); the socket opening is a real hole.
  function markerMeshes(S){
    const ring=(x,z,r,n=28)=>Array.from({length:n},(_,i)=>[x+r*Math.cos(i*Math.PI*2/n),z+r*Math.sin(i*Math.PI*2/n)]);
    const rect=(w,h,x=0,z=0)=>[[x-w/2,z-h/2],[x+w/2,z-h/2],[x+w/2,z+h/2],[x-w/2,z+h/2]];
    const rr=(w,h,r)=>S.rounded(-w/2,w/2,-h/2,h/2,r,6);
    const rj45=[[-3,-4.5],[3,-4.5],[3,-3],[5.8,-3],[5.8,4.5],[-5.8,4.5],[-5.8,-3],[-3,-3]];
    const shapes={
      rj45:[rr(16,13.5,1),rj45],
      'usb-a':[rr(14.5,7,.8),rect(12.5,5),rect(11,1.8,0,.9)],
      'usb-c':[rr(10.5,4.6,2.3),rr(8.6,2.8,1.4),rect(6.4,.7)],
      hdmi:[rr(17,7,1),[[-7,-.6],[-5.3,-2.25],[5.3,-2.25],[7,-.6],[7,2.25],[-7,2.25]]],
      'micro-hdmi':[rr(8,4.4,.8),[[-3.2,-.2],[-2.3,-1.2],[2.3,-1.2],[3.2,-.2],[3.2,1.2],[-3.2,1.2]]],
      'dc-barrel':[ring(0,0,4.5,32),ring(0,0,3.1,32),ring(0,0,1,16)],
      iec:[rr(31,24,2),[[-12,-8],[12,-8],[12,4],[8,8],[-8,8],[-12,4]],rect(1.6,5,-7,-1.5),rect(1.6,5,7,-1.5),rect(5,1.6,0,4.5)],
      keystone:[rr(16.5,18,.6),rj45],
      other:[ring(0,0,4,24),ring(0,0,2,20)]};
    const out={};
    for(const [type,[outer,...holes]] of Object.entries(shapes)){const m=new S.Mesh();S.slab(m,outer,holes,-2.5,0,(x,z,y)=>[x,y,z]);out['port-'+type]=m;}
    return out;
  }
  const api={TYPES,FACES,POINTS,POINT_LABELS,wizardPorts,basePorts,baseZ,portsFor,setOverride,prune,newPortId,markerParts,positionFromHit,markerMeshes};
  root.LabRaxPorts=api;if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(typeof window==='undefined'?globalThis:window);
