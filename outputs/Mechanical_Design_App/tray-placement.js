// Place on tray window (Option 1, Brian 2026-10-19): the tray choices of ONE slot allocation.
// The library item keeps the equipment facts (size, holes, ports); this window edits placement.tray, whose
// absent keys fall back to the library spec. "Apply to draft" only changes the rack draft; the workspace's
// explicit Save is the only thing that saves it. Fit, retention and strength stay UNKNOWN.
(function(root){
  'use strict';
  // ---- Pure logic (Node-testable). Mirrors equipment.PLACEMENT_KEYS, clean() and equipment_tray.scad asserts.
  const KEYS=['dev_off_x','dev_off_y','dev_rot','device_mount','wall_open','standoff','insert_pilot','board_t','joint','keystones','rear_support','rear_openings','rear_style','u','front_position','front_setback','bezel','bezel_size','sleeve_top','feet_style','rear_floor_opening','insert_bosses','hidden_joint'];
  const DEFAULTS={dev_off_x:0,dev_off_y:0,dev_rot:0,device_mount:'inserts',wall_open:['rear'],standoff:6,insert_pilot:3.2,board_t:1.6,joint:'screw',keystones:[],rear_support:false,rear_openings:false,u:1,front_position:'today',front_setback:16,bezel:'none',bezel_size:1,sleeve_top:.3,feet_style:'pockets',rear_floor_opening:false,insert_bosses:false,hidden_joint:false};
  const FRONT_GAP=12,MARGIN=8,RACK_INNER_W=208,SIDE_CLEAR=2,MAX_TRAY=RACK_INNER_W-2*SIDE_CLEAR,RACK_DEPTH=240,PITCH=44.45,PLATE_HALF=126,PLATE_T=4,TRAY_T=3;
  const MOUNTS={inserts:'Screws + inserts',pegs:'Pegs',clips:'Clips',straps:'Strap',wall:'Wall',flat:'Sits flat on the tray (PCs, boxes)',sleeve:'Sleeve: boxed in, front flush (PCs, boxes)'};
  const REAR_STYLES={solid:['Solid','Plain plate'],open:['Open','Original cable windows'],reinforced:['Reinforced','Wider bands and inner top/end lips; ends shorten to clear rear joints'],slots:['Cable slots','Rounded upper and centre cable slots'],vents:['Vents','Dense round vents, centre cable slot and inner top/end lips; ends shorten to clear rear joints']};
  const rearStyle=v=>v.rear_style||(v.rear_openings?'open':'solid');
  const JOINTS={screw:'Screw joint',single:'Single printed piece'};
  const copy=v=>Array.isArray(v)?v.slice():v;
  // Values shown in the window: the allocation's tray settings win, then the library spec, then template defaults.
  function values(spec,tray){
    const v={};
    for(const k of KEYS)v[k]=copy(tray&&k in tray?tray[k]:spec&&k in spec?spec[k]:DEFAULTS[k]);
    return v;
  }
  // What goes into placement.tray: only the choices that differ from the library item, so an untouched
  // allocation keeps no tray settings and builds exactly as before.
  function diff(spec,v){
    const out={};
    for(const k of KEYS){if(k==='rear_style'&&!v.rear_support)continue;const base=spec&&k in spec?spec[k]:DEFAULTS[k];if(JSON.stringify(base)!==JSON.stringify(v[k]))out[k]=copy(v[k]);}
    return out;
  }
  function layout(spec,v){
    const turned=v.dev_rot===90||v.dev_rot===270,w=+spec.dev_w,d=+spec.dev_d;
    const fp_w=turned?d:w,fp_d=turned?w:d,tray_w=2*(Math.abs(v.dev_off_x)+fp_w/2+(v.device_mount==='sleeve'?Math.max(MARGIN,PO().SLEEVE.side+PO().SLEEVE.wall,v.insert_bosses?PO().SLEEVE.side+V2.pilotOffset+V2.bossR:0,v.hidden_joint?PO().SLEEVE.side+PO().SLEEVE.wall+PO().SLEEVE.hiddenGap+2*PO().SLEEVE.hiddenHalf:0):MARGIN));
    const dev_x=-fp_w/2+v.dev_off_x,dev_y=PO().deviceY({...spec,...v});
    const tray_d=v.rear_support?RACK_DEPTH:dev_y+fp_d+MARGIN;
    const lift=PO().deviceLift({...spec,...v});
    return {fp_w,fp_d,tray_w,tray_d,dev_x,dev_y,lift,plate_h:PO().plateHeight(v.u),jx:Math.min(40,tray_w/2-12)};
  }
  // PROPOSED nominal opening and 2 mm clearance per side; never rotates the device.
  function widthProblem(spec,v=values(spec)){
    const L=layout(spec,v);if(L.tray_w<=MAX_TRAY)return '';
    const hint=2*Math.abs(v.dev_off_x)+L.fp_d+2*(v.device_mount==='sleeve'?Math.max(MARGIN,PO().SLEEVE.side+PO().SLEEVE.wall,v.insert_bosses?PO().SLEEVE.side+V2.pilotOffset+V2.bossR:0,v.hidden_joint?PO().SLEEVE.side+PO().SLEEVE.wall+PO().SLEEVE.hiddenGap+2*PO().SLEEVE.hiddenHalf:0):MARGIN)<=MAX_TRAY?' Too wide this way round; it fits if you press Rotate 90°.':'';
    return `This tray is ${mm(L.tray_w)} mm wide but the rack opening allows ${MAX_TRAY} mm (${RACK_INNER_W} mm minus ${SIDE_CLEAR} mm each side).`+(v.dev_off_x?' Move the device less far sideways.':'')+hint+(v.hidden_joint&&v.device_mount==='sleeve'?' The hidden screw joint adds about 20 mm of tray beside each sleeve wall; turn it off for a wider device.':'');
  }
  // equipment_tray.scad dp(): device-frame point (front-left origin) -> footprint offset after rotation.
  function dp(spec,rot,p){const w=+spec.dev_w,d=+spec.dev_d;
    return rot===90?[d-p[1],p[0]]:rot===180?[w-p[0],d-p[1]]:rot===270?[p[1],w-p[0]]:[p[0],p[1]];}
  function holes(spec,v){const L=layout(spec,v);return (spec.holes||[]).map(p=>{const q=dp(spec,v.dev_rot,p);return [L.dev_x+q[0],L.dev_y+q[1]];});}

  const WALL_SIDES=['front','rear','left','right'],WALL_MESSAGE='The wall would hit the faceplate joint; set the device back or move it sideways.';
  function wallBoxes(spec,v){
    if(v.device_mount!=='wall')return [];
    const L=layout(spec,v),w=+spec.dev_w,d=+spec.dev_d,h=Math.min(12,+spec.dev_h-2),out=[];
    for(const side of WALL_SIDES){const hz=['front','rear'].includes(side),len=hz?w:d,opened=(v.wall_open||['rear']).includes(side);if(opened&&len<30)continue;
      const spans=opened?[[-2.5,9.5,h],[len-9.5,len+2.5,h]]:!hz&&len>=40?[[-2.5,len/2-10,h],[len/2-10,len/2+10,Math.min(4,h)],[len/2+10,len+2.5,h]]:[[-2.5,len+2.5,h]],c=['front','left'].includes(side)?-2.5:(hz?d:w)+.5;
      for(const [a,b,z] of spans){const q=hz?[a,c,b,c+2]:[c,a,c+2,b],p=dp(spec,v.dev_rot,[q[0],q[1]]),r=dp(spec,v.dev_rot,[q[2],q[3]]);out.push([L.dev_x+Math.min(p[0],r[0]),L.dev_y+Math.min(p[1],r[1]),L.dev_x+Math.max(p[0],r[0]),L.dev_y+Math.max(p[1],r[1]),z]);}
    }return out;
  }
  function wallProblem(spec,v,xs){if(v.device_mount!=='wall')return '';xs=xs||joints(spec,v)?.joints||[];return wallBoxes(spec,v).some(q=>q[1]<0||v.joint==='screw'&&xs.some(x=>q[0]<x+9&&q[2]>x-9&&(q[1]<11.3&&q[3]>0||q[1]<22&&q[3]>9&&[-1,1].some(side=>q[0]<x+side*6+1&&q[2]>x+side*6-1))))?WALL_MESSAGE:'';}

  function footPockets(spec,v){if(!['flat','sleeve'].includes(v.device_mount))return [];const L=layout(spec,v),F=PO().FOOT;
    return (spec.feet||[]).map(f=>{const pts=[[f.x,f.y],[f.x+f.w,f.y],[f.x,f.y+f.d],[f.x+f.w,f.y+f.d]].map(p=>dp(spec,v.dev_rot,p));const depth=+f.h+F.extraDepth;
      return {x0:L.dev_x+Math.min(...pts.map(p=>p[0]))-F.clearance,x1:L.dev_x+Math.max(...pts.map(p=>p[0]))+F.clearance,y0:L.dev_y+Math.min(...pts.map(p=>p[1]))-F.clearance,y1:L.dev_y+Math.max(...pts.map(p=>p[1]))+F.clearance,depth,through:depth>TRAY_T-F.minFloor};});}
  // Opt-in sleeve v2 constants mirror equipment.py / equipment_tray.scad.
  const V2={ride:.5,topDefault:.3,topMax:2,pilotOffset:4,pilotR:2,bossR:5/Math.cos(Math.PI/48),bossFacets:48,bossDepth:12,attach:.8,
    openW:60,openD:30,openR:2,openMin:10,stopClear:4,jointClear:3,wallClear:5,jointHalf:9,jointReach:11.3,eps:.1,heightTol:.001};
  function windowSpec(s){if(s.device_mount!=='sleeve')return s;const extra=(s.sleeve_top??V2.topDefault)-V2.topDefault+(s.feet_style==='grooves'?V2.ride:0);return extra?{...s,dev_h:+s.dev_h+extra}:s;}
  function sleeveGeometry(s){const w=PO().sleeve(windowSpec(s));if(w&&s.insert_bosses){const reach=w.half+V2.pilotOffset;w.joints=[w.x-reach,w.x+reach];w.outside=2*(reach+V2.bossR);}return w;}
  function footGrooves(spec,v){if(v.feet_style!=='grooves')return [];const tracks=[],top=PO().floorZ(v)+TRAY_T,F=PO().FOOT;
    for(const p of footPockets(spec,v).sort((a,b)=>a.x0-b.x0)){const t=tracks.at(-1);if(t&&p.x0<=t.x1){t.x1=Math.max(t.x1,p.x1);t.dips.push(p);}else tracks.push({x0:p.x0,x1:p.x1,dips:[p]});}
    for(const t of tracks){const heights=t.dips.map(p=>p.depth-F.extraDepth),depth=Math.max(...heights)-V2.ride,bottom=top-depth;
      if(Math.max(...heights)-Math.min(...heights)>V2.heightTol)throw Error('Feet sharing a groove must have the same height.');
      if(depth<=0)throw Error('Feet must be taller than the 0.5 mm groove ride lift.');
      if(bottom<F.minFloor-1e-9)throw Error('Feet are too tall for grooves: cannot keep 0.8 mm of floor above the slot bottom.');
      for(const p of t.dips){p.cut_depth=p.through?top+V2.eps:p.depth;p.ramp=p.cut_depth-depth;}
      const ramp=Math.max(...t.dips.map(p=>p.ramp));Object.assign(t,{y0:PO().deviceY({...spec,...v}),y1:Math.max(...t.dips.map(p=>p.y1))+ramp,depth,bottom,floor_bottom:bottom-PO().floorZ(v)<F.minFloor?0:PO().floorZ(v),ramp});}
    return tracks;
  }
  function rearFloorGeometry(spec,v){if(!v.rear_floor_opening)return null;const L=layout(spec,v),w=sleeveGeometry({...spec,...v}),stop=L.dev_y+L.fp_d+(w?PO().SLEEVE.stopT:v.device_mount==='flat'?6.2:0),jx=Math.min(40,L.tray_w/2-12),placed=v.device_mount!=='sleeve'?joints(spec,v):null,xs=placed&&!placed.problem?placed.joints:[-jx,jx],half=Math.min(V2.openW/2,Math.min(...xs.map(Math.abs))-V2.jointHalf-V2.jointClear,(w?w.half-Math.abs(w.x):L.tray_w/2)-V2.wallClear),y0=stop+V2.stopClear,y1=Math.min(y0+V2.openD,RACK_DEPTH-V2.jointReach-V2.jointClear),q={x0:-half,x1:half,y0,y1,r:V2.openR};
    if(2*half<V2.openMin||y1-y0<V2.openMin)throw Error('Not enough floor behind the device for the cable opening and its clearances.');
    const obstacles=v.feet_style==='grooves'?footGrooves(spec,v):footPockets(spec,v);
    for(const x of [L.dev_x-5.5,L.dev_x+L.fp_w+2.5])for(const y of [L.dev_y+L.fp_d*.25,L.dev_y+L.fp_d*.75])obstacles.push({x0:x,x1:x+3,y0:y-6,y1:y+6});
    if(obstacles.some(p=>pocketOverlap(q,p.x0,p.x1,p.y0,p.y1)))throw Error('Cable opening would overlap a strap slot or foot groove/pocket.');return q;
  }
  const pocketOverlap=(p,x0,x1,y0,y1)=>p.x0<x1&&p.x1>x0&&p.y0<y1&&p.y1>y0;
  const fin=x=>typeof x==='number'&&Number.isFinite(x);
  // port-openings.js (Brian, 2026-10-19): front openings follow the device; loaded as a page script or, under Node, required.
  function PO(){if(root.LabRaxPortOpenings)return root.LabRaxPortOpenings;
    if(typeof module!=='undefined'&&typeof require==='function'){try{return require('./port-openings.js');}catch(e){}}return null;}
  // This slot's front openings: moved with the offset and standoff, or as entered when the device is turned.
  function openings(spec,v){const P=PO();return P?P.frontOpenings(spec,v):{ports:(spec.ports||[]).map(p=>({...p})),dx:0,dz:0,follows:false,rotation:+v.dev_rot||0,message:null};}
  const mm=x=>Math.round(x*10)/10;
  // Plain-language versions of the SCAD asserts and the build checks. Any message blocks Apply and export.
  function problems(spec,v,pair=false){
    const out=[];
    if(![0,90,180,270].includes(v.dev_rot))return ['Rotation must be 0, 90, 180 or 270 degrees.'];
    if(!fin(v.dev_off_x)||!fin(v.dev_off_y))return ['Enter numbers for the left/right offset and the front gap.'];
    if(!Number.isInteger(v.u)||v.u<1||v.u>5)out.push('Faceplate height must be a whole number of rack units from 1 to 5.');
    if(v.device_mount==='wall'){if(!Array.isArray(v.wall_open)||!v.wall_open.length||v.wall_open.some(s=>!WALL_SIDES.includes(s))||new Set(v.wall_open).size===4)out.push('Open sides must name Front, Rear, Left or Right; leave at least one open and one closed.');if(+spec.dev_h<=2)out.push('A wall needs a device taller than 2 mm.');}
    if(!MOUNTS[v.device_mount])out.push('Choose how the device attaches to the tray.');
    if(!JOINTS[v.joint])out.push('Choose how the tray joins the faceplate.');
    if(!fin(v.standoff)||v.standoff<0||v.standoff>30)out.push('Standoff must be between 0 and 30 mm.');
    if(v.device_mount==='inserts'&&(!fin(v.insert_pilot)||v.insert_pilot<1.5||v.insert_pilot>8))out.push('Insert pilot hole must be between 1.5 and 8 mm.');
    if((v.device_mount==='pegs'||v.device_mount==='clips')&&(!fin(v.board_t)||v.board_t<0.5||v.board_t>6))out.push('Board thickness must be between 0.5 and 6 mm.');
    if(!PO().FRONT_POSITIONS.includes(v.front_position))out.push('Choose a valid front position.');
    if(!PO().BEZELS.includes(v.bezel))out.push('Choose a valid bezel.');
    if(!fin(v.front_setback)||v.front_setback<0||v.front_setback>100)out.push('Set back must be 0 to 100 mm from the front face.');
    if(!fin(v.bezel_size)||v.bezel_size<.5||v.bezel_size>1.5)out.push('Bezel size must be 0.5 to 1.5 mm.');
    if(!fin(v.sleeve_top)||v.sleeve_top<V2.topDefault||v.sleeve_top>V2.topMax)out.push('Top play must be 0.3 to 2 mm.');
    if(!['pockets','grooves'].includes(v.feet_style))out.push('Feet must be pockets or grooves.');
    for(const k of ['rear_floor_opening','insert_bosses','hidden_joint'])if(typeof v[k]!=='boolean')out.push(k+' must be true or false.');
    if(v.sleeve_top!==V2.topDefault&&v.device_mount!=='sleeve')out.push('Top play is only available for a sleeve.');
    if(v.feet_style==='grooves'&&(!['flat','sleeve'].includes(v.device_mount)||!(spec.feet||[]).length))out.push('Foot grooves need a flat or sleeve mount with feet.');
    if(v.insert_bosses&&(v.device_mount!=='sleeve'||v.joint!=='screw'))out.push('Stronger insert bosses need a sleeve with a screw joint.');
    if(v.hidden_joint&&(v.device_mount!=='sleeve'||v.joint!=='screw'))out.push('Hidden screws need a sleeve with a screw joint.');
    if(v.hidden_joint&&v.insert_bosses)out.push('Hidden screws and stronger insert bosses cannot be combined.');
    if(v.rear_floor_opening&&!v.rear_support)out.push('Cable opening in floor needs rear support.');
    if(out.length)return out;
    try{footGrooves(spec,v);rearFloorGeometry(spec,v);}catch(e){return [e.message];}
    out.push(...PO().positionProblems({...spec,...v}));
    const L=layout(spec,v);
    const width=widthProblem(spec,v);if(width)out.push(width);
    if(v.front_position==='today'&&v.device_mount!=='sleeve'&&L.dev_y<0)out.push('The device is moved into the faceplate. The front gap must be at least 0 mm.');
    if(v.dev_off_y>230)out.push('The device is moved too far back. The front gap can be at most 242 mm.');
    if(v.rear_support){
      if(v.joint==='single')out.push('Rear-post support needs the screw joint (a 240 mm single print is not offered).');
      if(+spec.dev_d>200)out.push('With rear-post support the device can be at most 200 mm deep.');
      if(L.dev_y+L.fp_d+MARGIN>RACK_DEPTH)out.push('The device is moved past the rear posts. Reduce the front gap.');
    }
    if(Math.max(PO().neededHeight({...spec,...v}),L.lift+ +spec.dev_h+(v.feet_style==='grooves'?V2.ride:0))>v.u*PITCH)out.push(`The device is taller than ${v.u}U allows. Pick more rack units or a lower standoff.`);
    const tracks=footGrooves(spec,v),pockets=v.feet_style==='grooves'?[...tracks,...tracks.flatMap(t=>t.dips.map(p=>({...p,y0:p.y0-p.ramp,y1:p.y1+p.ramp})))]:footPockets(spec,v);if(pockets.length){const jx=Math.min(40,L.tray_w/2-12);
      if(!(v.feet_style==='grooves'&&v.device_mount==='sleeve')&&v.joint==='screw'&&pockets.some(p=>[-jx,jx].some(x=>pocketOverlap(p,x-9,x+9,0,11.3))))out.push('A foot pocket would cut into a tray screw joint; move or remove that foot.');
      if(v.rear_support&&v.joint==='screw'&&pockets.some(p=>[-jx,jx].some(x=>pocketOverlap(p,x-9,x+9,RACK_DEPTH-11.3,RACK_DEPTH))))out.push('A foot pocket would cut into a rear screw joint; move or remove that foot.');
      for(const p of pockets){for(const x of [L.dev_x-5.5,L.dev_x+L.fp_w+2.5])for(const y of [L.dev_y+L.fp_d*.25,L.dev_y+L.fp_d*.75])if(pocketOverlap(p,x,x+3,y-6,y+6))out.push('A foot pocket would cut into a strap slot; move or remove that foot.');
        if(v.device_mount==='sleeve'){const sw=sleeveGeometry({...spec,...v}),left=sw.x-sw.half,right=sw.x+sw.half;if(pocketOverlap(p,left-PO().SLEEVE.wall,left,0,L.dev_y+L.fp_d)||pocketOverlap(p,right,right+PO().SLEEVE.wall,0,L.dev_y+L.fp_d))out.push('A foot pocket would cut into a sleeve wall; move or remove that foot.');if(pocketOverlap(p,L.dev_x,L.dev_x+L.fp_w,L.dev_y+L.fp_d,L.dev_y+L.fp_d+PO().SLEEVE.stopT))out.push('A foot pocket would cut into the sleeve rear stop; move or remove that foot.');if(v.feet_style!=='grooves'&&pocketOverlap(p,left,right,0,8))out.push('A foot pocket would cut into the floor strip under the sleeve window; move or remove that foot.');}}
    }
    if((v.device_mount==='inserts'||v.device_mount==='pegs')&&!(spec.holes||[]).length)out.push('Screws and pegs need mounting holes. Add them to the library item (Edit library item), or choose clips or a strap.');
    if(v.device_mount==='flat'){
      if(v.front_position==='today'&&L.dev_y<6.2)out.push('Flat corner stops need a front gap of at least 6.2 mm.');
      if(v.front_position==='today'&&v.joint==='screw'&&L.dev_y<11.5)out.push('Flat device must clear the front screw joint (front gap >= 11.5 mm).');
      if(v.rear_support&&L.dev_y+L.fp_d>RACK_DEPTH-11.5)out.push('Flat device must clear the rear screw joint (rear gap >= 11.5 mm).');
    }
    const ks=v.keystones||[];
    if(ks.length>12)out.push('At most 12 keystones fit the faceplate.');
    if(ks.some(x=>!fin(x)||Math.abs(x)>PLATE_HALF-24))out.push(`Keystones must sit within ${PLATE_HALF-24} mm of the faceplate centre.`);
    const xs=ks.slice().sort((a,b)=>a-b);
    if(xs.some((x,i)=>i&&x-xs[i-1]<21))out.push('Keystones must be at least 21 mm apart.');
    const half=L.tray_w/2;
    if(ks.some(x=>Math.abs(x)-9.9<half+0.5))out.push(`A keystone collar would hit the tray; keep keystones at least ${mm(half+10.4)} mm from the centre.`);
    // Openings moved with the device must stay on the plate and clear of keystones (same limits as equipment.py).
    const P=PO();if(P){const raw=openings(spec,v).ports,sw=sleeveGeometry({...spec,...v}),filtered=P.sleevePorts(raw,windowSpec({...spec,...v}));out.push(...filtered.errors);
      if(sw){if(L.fp_d/4-4-6<8)out.push('Sleeve depth must be at least 72 mm to keep strap slots clear of the front joint.');if(sw.bottom-P.plateBottom<P.SLEEVE.band||v.u*PITCH-P.plateBottom-sw.top<P.SLEEVE.band)out.push(`Too tall for a flush window in ${v.u}U; choose ${v.u+1}U`);
        if(v.rear_support&&sw.stop_end>RACK_DEPTH-11.5)out.push('Sleeve rear stop and device must clear the rear screw joint by at least 11.5 mm.');
        if(v.joint==='screw'&&sw.height<10)out.push('Sleeve screw joint needs a window at least 10 mm tall; choose a single printed piece.');
        if(sw.hidden&&filtered.ports.some(p=>sw.joints.some(x=>Math.abs(p.x-x)<P.JOINT_HALF+P.JOINT_CLEAR+p.w/2&&p.z-p.h/2<P.SLEEVE.hiddenTop+P.JOINT_CLEAR)))out.push('A front opening sits in front of the hidden screw joint; move or remove it.');
        if(!sw.hidden&&v.joint==='screw'&&filtered.ports.some(p=>sw.joints.some(x=>Math.abs(p.x-x)<P.SLEEVE.wall/2+p.w/2&&p.z+p.h/2>sw.bottom&&p.z-p.h/2<sw.top)))out.push('A front opening overlaps a sleeve wall joint; move or remove it.');}
      out.push(...P.problems(filtered.ports,v.u,ks));const j=joints(spec,v);if(j&&j.problem)out.push(j.problem);}
    const wp=pair?'':wallProblem(spec,v);if(wp)out.push(wp);
    return out;
  }
  // Plain-language warnings that never block (Brian, 2026-10-19).
  // Screw joints placed clear of the openings and keystones (port-openings.js jointPositions); null for the single piece.
  function joints(spec,v){const P=PO();if(v.joint!=='screw'||!P)return null;const sw=sleeveGeometry({...spec,...v});if(sw)return {joints:sw.joints,moved:false,problem:null};return P.jointPositions(openings(spec,v).ports,v.keystones||[],layout(spec,v).tray_w/2);}
  // Mirrors equipment.rear_geometry cut bounds, without lips or rendering.
  function rearCutGeometry(spec,v){
    const style=rearStyle(v),L=layout(spec,v),width=L.fp_w,jx=Math.min(40,Math.abs(v.dev_off_x)+width/2+8-12),placed=joints(spec,v);
    // Rear joints use joint_x from clean(), which only moves the non-sleeve front joints.
    const xs=v.joint==='screw'&&v.device_mount!=='sleeve'&&placed&&!placed.problem?placed.joints:[-jx,jx];
    const g={windows:[],holes:[],keep_clear:[],joints:v.joint==='screw'?xs:[]};
    for(const p of spec.protrusions||[]){const pts=[[p.x,p.y],[p.x+p.w,p.y],[p.x,p.y+p.d],[p.x+p.w,p.y+p.d]].map(q=>dp(spec,v.dev_rot,q)),y0=L.dev_y+Math.min(...pts.map(q=>q[1])),y1=L.dev_y+Math.max(...pts.map(q=>q[1]));
      if(v.rear_support&&y0<244&&y1>=240)g.keep_clear.push([L.dev_x+Math.min(...pts.map(q=>q[0]))-.5,L.dev_x+Math.max(...pts.map(q=>q[0]))+.5,L.lift+p.z-.5,L.lift+p.z+p.h+.5]);}
    if(!v.rear_support||style==='solid')return g;
    const legacy=style==='open',margin=legacy?4:6,band=legacy?3.5:5,strip=legacy?4:6,limit=legacy?100.2625:96,floor=['flat','sleeve'].includes(v.device_mount)?.5:8.225;
    const left=Math.min(...xs),right=Math.max(...xs),half=6+margin,top=floor+18.5+margin,height=v.u*PITCH-.025,regions=[];
    for(let i=0;i<v.u;i++){const lo=Math.max(.025,i*PITCH)+band,hi=Math.min(height,(i+1)*PITCH)-band,upper=i*PITCH+top,split=Math.min(i*PITCH+22.225,upper-strip);
      let candidates=[[-limit,limit,Math.max(lo,upper),hi],[-limit,left-half,lo,split],[left+half,right-half,lo,split],[right+half,limit,lo,split]];
      if(!legacy)candidates=candidates.map(([a,b,c,d])=>[Math.max(-limit,a),Math.min(limit,b),c,d]);
      const valid=candidates.filter(q=>q[1]-q[0]>=10&&q[3]-q[2]>=10);
      if(['open','reinforced'].includes(style))g.windows.push(...valid);
      else if(style==='slots')g.windows.push(...valid.filter(q=>q===candidates[0]||q===candidates[2]));
      else{if(valid.includes(candidates[2]))g.windows.push(candidates[2]);regions.push(...candidates.filter(q=>q!==candidates[2]&&q[1]>q[0]&&q[3]>q[2]));}
    }
    if(style==='vents'){
      const diameter=6.5,pitch=8.5,rowPitch=pitch*Math.sqrt(3)/2;
      const pack=(a,b,c,d)=>{const rows=Math.floor((d-c-diameter)/rowPitch)+1,out=[];if(rows<=0||b-a<diameter)return out;const z0=(c+d-(rows-1)*rowPitch)/2;
        for(let row=0;row<rows;row++){const offset=row%2*pitch/2,count=Math.floor((b-a-diameter-offset)/pitch)+1;for(let col=0;col<Math.max(0,count);col++)out.push([a+diameter/2+offset+col*pitch,z0+row*rowPitch]);}return out;};
      for(const [a,b,c,d] of regions){const normal=pack(a,b,c,d),rotated=pack(c,d,a,b).map(([z,x])=>[x,z]);g.holes.push(...(rotated.length>normal.length?rotated:normal));}
    }return g;
  }
  // Nominal planar distances: rounded window cores + 2 mm radius, circular vents/bosses,
  // capsule rack slots. Merged cutouts are named separately from remaining positive bands.
  function keepClearBands(spec,v){
    const g=rearCutGeometry(spec,v),style=rearStyle(v),height=v.u*PITCH-.025,floor=['flat','sleeve'].includes(v.device_mount)?.5:8.225;
    const gap=(q,c,r=0)=>Math.max(0,Math.hypot(Math.max(c[0]-q[1],q[0]-c[1],0),Math.max(c[2]-q[3],q[2]-c[3],0))-r),obstacles=[];
    for(const [a,b,c,d] of g.windows)obstacles.push(['style window',[a+2,b-2,c+2,d-2],2]);
    for(const [x,z] of g.holes)obstacles.push(['vent hole',[x,x,z,z],3.25]);
    for(let i=0;i<v.u;i++)for(const x of [-118.2625,118.2625])for(const dz of [-15.902,15.902]){const z=i*PITCH+22.225+dz;obstacles.push(['rack slot',[x-1.5,x+1.5,z,z],3.5]);}
    return g.keep_clear.map((q,i)=>{let edge=Math.min(q[0]+126,126-q[1],q[2]-.025,height-q[3]);
      for(const x of [q[0],q[1]])for(const z of [q[2],q[3]]){const dx=Math.max(Math.abs(x)-123.5,0),dz=Math.max(2.525-z,z-(height-2.5),0);if(dx>0&&dz>0)edge=Math.min(edge,2.5-Math.hypot(dx,dz));}
      const distances=[[Math.max(0,edge),'plate edge']],merged=new Set(),collisions=new Set();
      for(const [name,core,radius] of [...obstacles,...g.keep_clear.flatMap((p,j)=>i===j?[]:[['keep-clear opening',p,0]])]){const distance=gap(q,core,radius);if(distance<=1e-9)merged.add(name);else distances.push([distance,name]);}
      for(const x of g.joints)for(const [name,radius] of [['joint boss',4.5],['joint pilot',2]]){const distance=gap(q,[x,x,floor+14,floor+14],radius);distances.push([distance,name]);if(distance<=1e-9)collisions.add(name);}
      const [distance,nearest]=distances.reduce((a,b)=>b[0]<a[0]?b:a);
      return {opening:q,band:Math.round(distance*1e6)/1e6,nearest,normal_band:style==='open'?3.5:style!=='solid'?5:null,merged:[...merged].sort(),collisions:[...collisions].sort()};
    });
  }
  function warnings(spec,v){const out=[...PO().bezelPlan(windowSpec({...spec,...v,ports:openings(spec,v).ports})).notes];if(v.bezel==='rounded')out.push('Rounded prints best with the front face up; Chamfer prints either way.');const L=layout(spec,v),bands=keepClearBands(spec,v);let rearIndex=0;for(const p of spec.protrusions||[]){const pts=[[p.x,p.y],[p.x+p.w,p.y],[p.x,p.y+p.d],[p.x+p.w,p.y+p.d]].map(q=>dp(spec,v.dev_rot,q)),x0=L.dev_x+Math.min(...pts.map(q=>q[0])),x1=L.dev_x+Math.max(...pts.map(q=>q[0])),y0=L.dev_y+Math.min(...pts.map(q=>q[1])),y1=L.dev_y+Math.max(...pts.map(q=>q[1])),z1=L.lift+p.z+p.h;const hits=[];
      if(y0<0)hits.push('goes through the faceplate; no front opening is cut automatically');
      if(y1>RACK_DEPTH)hits.push('extends past the rack depth');
      if((x0< -104||x1>104)&&((y0<12&&y1>0)||(y0<244&&y1>228)))hits.push('may hit a rack post');
      if(x0< -L.tray_w/2||x1>L.tray_w/2||v.device_mount==='sleeve'&&(x0<L.dev_x-.5||x1>L.dev_x+L.fp_w+.5))hits.push('may hit a tray or sleeve wall');
      if(z1>v.u*PITCH)hits.push('extends above the allocated U');
      if(v.rear_support&&y0<244&&y1>=240){const b=bands[rearIndex++],style=rearStyle(v),normal=b.normal_band===null?'':` (the ${REAR_STYLES[style][0]} style normally keeps ${b.normal_band} mm)`;
        hits.push(`needs a rear bracket opening; ${b.merged.length?`it joins a ${b.merged.join(' and a ')} and `:''}leaves a ${b.band.toFixed(1)} mm band to the ${b.merged.includes(b.nearest)?'next ':''}${b.nearest}${normal}`);
        if(b.collisions.length)hits.push('cuts the '+b.collisions.join(' and '));
      }
      if(hits.length)out.push('Keep-clear zone '+hits.join('; ')+'. Real cables need extra bend space the app cannot know.');
    }const sw=sleeveGeometry({...spec,...v}),through=v.feet_style==='grooves'?0:footPockets(spec,v).filter(p=>p.through).length;if(through)out.push(`${through} foot pocket(s) pass through the floor (a blind cut would leave less than ${PO().FOOT.minFloor} mm).`);if(sw){out.push(`Opening ${mm(sw.height)} mm above the floor; band above ${mm(v.u*PITCH-PO().plateBottom-sw.top)} mm. Fit and strength UNKNOWN.`);out.push('Sleeve front is flush with the plate; choose As today or Flush with faceplate. Front gap is ignored. Fit, retention and strength UNKNOWN.');if(!sw.lip)out.push('No top lips fit this height budget; walls only.');const dropped=PO().sleevePorts(openings(spec,v).ports,windowSpec({...spec,...v})).dropped;if(dropped.length)out.push(`${dropped.length} front opening(s) inside the sleeve window are omitted; the window already exposes them.`);}const m=openings(spec,v).message;if(m)out.push(m);const j=joints(spec,v);
    if(j&&j.moved&&!j.problem)out.push(`The tray screw joints were moved to X = ${j.joints.map(x=>mm(x)).join(' and ')} mm (normally ±${mm(j.default)} mm) to keep them clear of the openings and keystones.`);
    return out;}
  // Centre: left/right offset back to 0 (front gap unchanged). Snap: whole millimetres.
  const snap=x=>Math.round(x);
  // ---- Live 3D preview: simple boxes for the tray, faceplate, standoffs and device (exact meshes on request).
  function box(x0,y0,z0,x1,y1,z1){
    const c=[[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]],v=[];
    for(const f of[[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],[3,0,4],[3,4,7]])for(const i of f)v.push(...c[i]);
    return v;
  }
  function schematic(spec,v){
    const L=layout(spec,v),floor=PO().floorZ(v)+TRAY_T,tray=box(-L.tray_w/2,0,PO().floorZ(v),L.tray_w/2,L.tray_d,floor);
    const posts=[];
    if(v.device_mount==='inserts'||v.device_mount==='pegs')for(const[x,y]of holes(spec,v))posts.push(...box(x-3,y-3,floor,x+3,y+3,floor+ +v.standoff));
    if(v.device_mount==='wall')for(const q of wallBoxes(spec,v))posts.push(...box(q[0],q[1],floor,q[2],q[3],floor+q[4]));
    if(v.device_mount==='flat'){
      const h=Math.min(6,PO().deviceCaseHeight({...spec,...v})),w=Math.min(6,L.fp_w),d=Math.min(6,L.fp_d);
      for(const x of [L.dev_x-6.2,L.dev_x+L.fp_w+0.2])for(const y of [L.dev_y,L.dev_y+L.fp_d-d])posts.push(...box(x,y,floor,x+6,y+d,floor+h));
      for(const x of [L.dev_x,L.dev_x+L.fp_w-w])for(const y of [L.dev_y-6.2,L.dev_y+L.fp_d+0.2])posts.push(...box(x,y,floor,x+w,y+6,floor+h));
    }
    const sw=sleeveGeometry({...spec,...v}),top=PO().plateBottom+L.plate_h;
    let plate=box(-PLATE_HALF,-PLATE_T,PO().plateBottom,PLATE_HALF,0,top);const jacks=[];
    if(sw){const S=PO().SLEEVE,left=sw.x-sw.half,right=sw.x+sw.half;
      plate=[...box(-PLATE_HALF,-PLATE_T,PO().plateBottom,left,0,top),...box(right,-PLATE_T,PO().plateBottom,PLATE_HALF,0,top),...box(left,-PLATE_T,PO().plateBottom,right,0,sw.bottom),...box(left,-PLATE_T,sw.top,right,0,top)];
      posts.push(...box(left-S.wall,0,floor,left,sw.rear,sw.top),...box(right,0,floor,right+S.wall,sw.rear,sw.top));
      if(sw.lip)posts.push(...box(left-S.wall,0,sw.top,left+Math.min(S.lipW,sw.half),sw.rear,sw.top+sw.lip),...box(right-Math.min(S.lipW,sw.half),0,sw.top,right+S.wall,sw.rear,sw.top+sw.lip));
      posts.push(...box(L.dev_x,sw.rear,floor,L.dev_x+L.fp_w,sw.stop_end,floor+Math.min(S.stopH,+spec.dev_h)));
    }
    const fw=PO().frontWindow({...spec,...v});if(fw&&!sw){const left=fw.x-fw.half,right=fw.x+fw.half;plate=[...box(-PLATE_HALF,-PLATE_T,PO().plateBottom,left,0,top),...box(right,-PLATE_T,PO().plateBottom,PLATE_HALF,0,top),...box(left,-PLATE_T,PO().plateBottom,right,0,fw.bottom),...box(left,-PLATE_T,fw.top,right,0,top)];}
    for(const x of v.keystones||[])jacks.push(...box(x-7.4,-PLATE_T-0.2,v.u*PITCH/2-8.3,x+7.4,0.2,v.u*PITCH/2+8.3));
    const pockets=footPockets(spec,v),pocketSketch=[],pz=PO().floorZ(v)+TRAY_T+0.01,border=0.6;for(const p of pockets){pocketSketch.push(...box(p.x0,p.y0,pz,p.x1,p.y0+border,pz+0.08),...box(p.x0,p.y1-border,pz,p.x1,p.y1,pz+0.08),...box(p.x0,p.y0+border,pz,p.x0+border,p.y1-border,pz+0.08),...box(p.x1-border,p.y0+border,pz,p.x1,p.y1-border,pz+0.08));}
    if(v.feet_style==='grooves')try{for(const t of footGrooves(spec,v))pocketSketch.push(...box(t.x0,Math.max(0,t.y0),pz,t.x1,t.y1,pz+.08));}catch(e){}
    if(v.rear_floor_opening)try{const q=rearFloorGeometry(spec,v);pocketSketch.push(...box(q.x0,q.y0,pz,q.x1,q.y1,pz+.08));}catch(e){}
    if(v.hidden_joint&&sw&&sw.hidden){const fz=PO().floorZ(v);for(const x of sw.joints)posts.push(...box(x-9,0,fz+3,x+9,8,fz+8),...box(x-7,8.3,fz+3,x+7,11.3,fz+22),...box(x-4.5,0,fz+14-4.5,x+4.5,8,fz+14+4.5));}  // tongue block, upright and plate boss of the hidden joint
    if(v.insert_bosses&&sw)for(const x of sw.joints)for(const z of sw.joint_z){const inside=sw.x+(x<sw.x?-sw.half:sw.half);posts.push(...box(x<sw.x?x-V2.bossR:inside,0,Math.max(PO().floorZ(v),z-V2.bossR),x<sw.x?inside:x+V2.bossR,V2.bossDepth,Math.min(sw.top+sw.lip,z+V2.bossR)));}
    const sets=[{v:plate,color:[78,117,163],alpha:1},{v:tray.concat(posts),color:[77,142,110],alpha:1},
      ...(pocketSketch.length?[{v:pocketSketch,color:[28,42,36],alpha:1}]:[]),{v:box(L.dev_x,L.dev_y,L.lift,L.dev_x+L.fp_w,L.dev_y+L.fp_d,L.lift+ +spec.dev_h),color:[230,195,92],alpha:0.55,device:true},
      // Orange = the device's front face (same convention as the wizard's model view).
      {v:(()=>{const p=dp(spec,v.dev_rot,[0,-.2]),q=dp(spec,v.dev_rot,[+spec.dev_w,.8]);return box(L.dev_x+Math.min(p[0],q[0]),L.dev_y+Math.min(p[1],q[1]),L.lift,L.dev_x+Math.max(p[0],q[0]),L.dev_y+Math.max(p[1],q[1]),L.lift+ +spec.dev_h);})(),color:[230,140,60],alpha:0.9,device:true}];
    if(jacks.length)sets.push({v:jacks,color:[30,32,36],alpha:1});
    return sets;
  }
  // Rack view sketch of one slot's effective tray (equipment-wizard.js draws it when no exact render exists):
  // flat triangle lists in equipment_tray.scad coordinates, the same frame as the rendered STLs.
  // Openings are dark blocks where the SCAD cuts keystones (ks_w x ks_h = 14.8 x 16.6, centred) and ports.
  function rackSketch(spec,tray,second){
    if(spec.faceplate_only){const s=PO().faceplateSpec(tray?.faceplate),holes=[];
      for(const k of s.keystones){const x=Array.isArray(k)?k[0]:k,z=Array.isArray(k)&&k.length>1?k[1]:s.u*PITCH/2;holes.push(...box(x-7.4,-4.2,z-8.3,x+7.4,.2,z+8.3));}
      for(const p of s.ports)holes.push(...box(p.x-p.w/2,-4.2,p.z-p.h/2,p.x+p.w/2,.2,p.z+p.h/2));
      return {faceplate:box(-126,-4,.025,126,0,s.u*PITCH-.025),...(holes.length?{openings:holes}:{})};
    }

    const v=values(spec,tray),Pr=second&&root.TrayPair,v2=Pr?Pr.values(second.spec,second.tray):null,L=Pr?Pr.layout(spec,v,second.spec,v2):layout(spec,v),
      sets=Pr?Pr.schematic(spec,v,second.spec,v2):schematic(spec,v),out={faceplate:sets[0].v,tray:sets[1].v};
    const holes=[];
    for(const x of v.keystones||[])if(fin(+x))holes.push(...box(x-7.4,-PLATE_T-0.2,v.u*PITCH/2-8.3,x+7.4,0.2,v.u*PITCH/2+8.3));
    for(const p of [...PO().sleevePorts(openings(spec,v).ports,windowSpec({...spec,...v})).ports,...(Pr?Pr.ports2(second.spec,Pr.merged(v,v2)):[])]){const o=[+p.x,+p.z,+p.w,+p.h];if(o.every(fin))holes.push(...box(o[0]-o[2]/2,-PLATE_T-0.2,o[1]-o[3]/2,o[0]+o[2]/2,0.2,o[1]+o[3]/2));}
    if(holes.length)out.openings=holes;
    if(v.rear_support)out.rear_bracket=box(-PLATE_HALF,RACK_DEPTH,PO().plateBottom,PLATE_HALF,RACK_DEPTH+PLATE_T,PO().plateBottom+L.plate_h); // to_rear(): plate mirrored about mid-depth
    return out;
  }
  const api={wallBoxes,wallProblem,WALL_MESSAGE,V2,windowSpec,sleeveGeometry,footGrooves,rearFloorGeometry,RACK_INNER_W,SIDE_CLEAR,MAX_TRAY,widthProblem,KEYS,DEFAULTS,MOUNTS,JOINTS,FRONT_GAP,values,diff,layout,holes,footPockets,openings,joints,rearCutGeometry,keepClearBands,problems,warnings,snap,schematic,box,rackSketch};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;
  root.TrayPlacement=api;
  if(typeof document==='undefined')return;

  // ---- Window (browser only).
  const h=(tag,attrs={},...kids)=>{const e=document.createElement(tag);for(const[k,a]of Object.entries(attrs)){if(k.startsWith('on'))e[k]=a;else if(a!==false&&a!=null)e.setAttribute(k,a===true?'':a);}e.append(...kids);return e;};
  const NS='http://www.w3.org/2000/svg';
  // index.html declares the session token as a top-level const (not a window property).
  const appToken=()=>typeof token!=='undefined'?token:'';
  let state=null; // {placement id, rack id, item, v (working values), prevU, exact (rendered meshes for this json), second: null | {item, v}, tab: 1 | 2}
  const view={yaw:2.5,pitch:0.5,zoom:1.6,sets:[],quality:'placement'}; // seen from behind and above, so the faceplate does not hide the device
  // Two devices (tray-pair.js, Brian 2026-10-20): the first device's own joint placement is replaced by the shared one.
  function current(){if(!state)return null;const own=problems(state.item.spec,state.v,!!state.second);if(!state.second)return own;
    if([state.v,state.second.v,state.second.item.spec].some(s=>s.feet_style==='grooves'||s.rear_floor_opening))own.push('Foot grooves and the cable floor opening need a single-device tray.');return [...new Set([...own.filter(t=>!/screw joints? cannot be placed/.test(t)),...TrayPair.problems(state.item.spec,state.v,state.second.item.spec,state.second.v)])];}
  const pairLayout=()=>state.second?TrayPair.layout(state.item.spec,state.v,state.second.item.spec,state.second.v):layout(state.item.spec,state.v);
  // The device whose position and mounting the window is editing (tab), as spec + full values.
  function editing(){return state.tab===2&&state.second?{spec:state.second.item.spec,v:state.second.v,full:TrayPair.merged(state.v,state.second.v)}:{spec:state.item.spec,v:state.v,full:state.v};}
  function field(label,get,set,attrs={}){
    const input=h('input',{type:'number',step:'1',value:String(get()),...attrs});
    input.oninput=()=>{if(input.value==='')return;set(Number(input.value));update();};
    input.onchange=()=>{input.value=String(get());};
    return h('label',{class:'ew-field'},label,input);
  }
  function chips(options,value,pick){
    return h('div',{class:'ew-choices'},...Object.entries(options).map(([k,t])=>{const b=h('button',{type:'button',class:'ew-chip'+(value===k?' on':''),'aria-pressed':String(value===k)},t);b.onclick=()=>{pick(k);render();};return b;}));
  }
  function topView(){
    const svg=document.getElementById('tpTop');if(!svg)return;const spec=state.item.spec,v=state.v,L=pairLayout();
    const depth=Math.max(L.tray_d,L.dev_y+L.fp_d,L.second?L.second.dev_y+L.second.fp_d:0)+12;
    svg.setAttribute('viewBox',`-132 ${-depth} 264 ${depth+20}`);
    let s=`<rect x="-126" y="0" width="252" height="4" fill="#4e75a3"/><text x="0" y="14" font-size="6" fill="#9aa" text-anchor="middle">faceplate (front)</text>`;
    const over=L.tray_w>MAX_TRAY;
    s+=`<rect x="${-L.tray_w/2}" y="${-L.tray_d}" width="${L.tray_w}" height="${L.tray_d}" fill="#24382f" stroke="${over?'#e07070':'#4d8e6e'}" stroke-width=".8"/>`;
    s+=`<rect x="${-MAX_TRAY/2}" y="${-depth+2}" width="${MAX_TRAY}" height="${depth-2}" fill="none" stroke="#666" stroke-width=".4" stroke-dasharray="3 2"/>`;
    if(v.joint==='screw'){const j=joints(spec,v);for(const x of j?j.joints.filter(x=>x!==null):[-L.jx,L.jx])s+=`<circle cx="${x}" cy="-3.5" r="2" fill="#aab"/>`;}
    for(const x of v.keystones||[])s+=`<rect x="${x-9.9}" y="-10.4" width="19.8" height="10.4" fill="#1d1f24" stroke="#888" stroke-width=".4"/>`;
    // Front-port openings in the faceplate strip (they follow the offset; a turned device leaves them as entered).
    for(const p of PO().sleevePorts(openings(spec,v).ports,windowSpec({...spec,...v})).ports)if([+p.x,+p.w].every(fin))s+=`<rect x="${+p.x-p.w/2}" y="0.6" width="${+p.w}" height="2.8" fill="#1d1f24" stroke="#ff9f43" stroke-width=".4"><title>${String(p.label||'Port').replace(/[<&"]/g,'')} opening</title></rect>`;
    if(state.second){const S2=state.second,m=TrayPair.merged(v,S2.v),L2=L.second,sp=S2.item.spec;
      for(const p of TrayPair.ports2(sp,m))if([+p.x,+p.w].every(fin))s+=`<rect x="${+p.x-p.w/2}" y="0.6" width="${+p.w}" height="2.8" fill="#1d1f24" stroke="#5cb8e6" stroke-width=".4"/>`;
      s+=`<rect id="tpDevice2" x="${L2.dev_x}" y="${-(L2.dev_y+L2.fp_d)}" width="${L2.fp_w}" height="${L2.fp_d}" fill="#6eb4e6" fill-opacity=".35" stroke="#6eb4e6" stroke-width="${state.tab===2?1.6:.8}" style="cursor:grab"/>`;
      const a2=dp(sp,m.dev_rot,[0,0]),b2=dp(sp,m.dev_rot,[+sp.dev_w,0]);
      s+=`<line x1="${L2.dev_x+a2[0]}" y1="${-(L2.dev_y+a2[1])}" x2="${L2.dev_x+b2[0]}" y2="${-(L2.dev_y+b2[1])}" stroke="#ff9f43" stroke-width="2" pointer-events="none"/>`;
      for(const[x,y]of holes(sp,m))s+=`<circle cx="${x}" cy="${-y}" r="${(+sp.hole_d||2.7)/2+.4}" fill="#5cc8ff" pointer-events="none"/>`;
      s+=`<text x="${L2.dev_x+L2.fp_w/2}" y="${-(L2.dev_y+L2.fp_d/2)}" font-size="6" fill="#eee" text-anchor="middle" pointer-events="none">2 · ${m.dev_rot}°</text>`;}
    s+=`<rect id="tpDevice" x="${L.dev_x}" y="${-(L.dev_y+L.fp_d)}" width="${L.fp_w}" height="${L.fp_d}" fill="#e6c35c" fill-opacity=".35" stroke="#e6c35c" stroke-width="${state.second&&state.tab===1?1.6:.8}" style="cursor:grab"/>`;
    const a=dp(spec,v.dev_rot,[0,0]),b=dp(spec,v.dev_rot,[+spec.dev_w,0]);
    s+=`<line x1="${L.dev_x+a[0]}" y1="${-(L.dev_y+a[1])}" x2="${L.dev_x+b[0]}" y2="${-(L.dev_y+b[1])}" stroke="#ff9f43" stroke-width="2" pointer-events="none"/>`;
    for(const[x,y]of holes(spec,v))s+=`<circle cx="${x}" cy="${-y}" r="${(+spec.hole_d||2.7)/2+.4}" fill="#5cc8ff" pointer-events="none"/>`;
    s+=`<text x="${L.dev_x+L.fp_w/2}" y="${-(L.dev_y+L.fp_d/2)}" font-size="6" fill="#eee" text-anchor="middle" pointer-events="none">${state.second?'1 · ':''}${v.dev_rot}°</text>`;
    svg.innerHTML=s;
    // Dragging a device also selects its tab (the tabs are redrawn when the drag ends).
    for(const [id,tab] of [['#tpDevice',1],['#tpDevice2',2]]){const dev=svg.querySelector(id);if(!dev)continue;const dv=tab===2?state.second.v:v;
      dev.onpointerdown=e=>{e.preventDefault();dev.setPointerCapture(e.pointerId);const m=svg.getScreenCTM().inverse(),pt=q=>{const p=svg.createSVGPoint();p.x=q.clientX;p.y=q.clientY;return p.matrixTransform(m);};
        const start=pt(e),x0=dv.dev_off_x,y0=dv.dev_off_y,switched=state.tab!==tab;state.tab=tab;
        dev.onpointermove=ev=>{const p=pt(ev);dv.dev_off_x=Math.max(-150,Math.min(150,snap(x0+p.x-start.x)));if(v.front_position==='today')dv.dev_off_y=Math.max(-40,Math.min(260,snap(y0-(p.y-start.y))));syncFields();update();};
        dev.onpointerup=()=>{dev.onpointermove=null;if(switched)render();};};}
  }
  function syncFields(){
    const x=document.getElementById('tpOffX'),y=document.getElementById('tpGap'),dv=editing().v;
    if(x&&document.activeElement!==x)x.value=String(dv.dev_off_x);
    if(y&&document.activeElement!==y)y.value=String(FRONT_GAP+dv.dev_off_y);
  }
  function draw3D(){
    const cv=document.getElementById('tpView'),P=window.EquipmentPainter;if(!cv||!P)return;
    const key=exactKey();
    const sketch=state.second?TrayPair.schematic(state.item.spec,state.v,state.second.item.spec,state.second.v):schematic(state.item.spec,state.v);
    view.sets=state.exact&&state.exact.key===key?state.exact.sets.concat(sketch.filter(s=>s.device)):sketch;
    const note=document.getElementById('tpViewNote');
    if(note)note.textContent=state.exact&&state.exact.key===key?`Exact OpenSCAD render of these settings at export quality ${exportNote()} (not saved). Translucent box = the device, orange = its front.`:'Live sketch: boxes for the tray, faceplate, standoffs and device (translucent; orange = device front). Left-drag turns, right-drag moves, scroll zooms.';
    if(note&&state.v.rear_support)note.textContent+=' Rear bracket: '+REAR_STYLES[rearStyle(state.v)][0]+'. This box sketch does not show the cutouts or flanges; stiffness/airflow UNKNOWN';
    P.draw(cv,view);
  }
  function update(){
    if(!state)return;topView();draw3D();
    const list=current(),box=document.getElementById('tpProblems');
    box.replaceChildren(...list.map(t=>h('li',{},t)));box.hidden=!list.length;
    for(const id of['tpApply','tpExport'])if(document.getElementById(id))document.getElementById(id).disabled=!!list.length;
    // Warnings never block Apply or export (Brian, 2026-10-19): turned-device front openings, support-extension joint.
    const warn=document.getElementById('tpWarnings');
    if(warn){const ws=warnings(state.item.spec,state.v),jw=window.extensionJointWarning?.(state.slot,state.v.u);if(jw)ws.push(jw);
      warn.replaceChildren(...ws.map(t=>h('li',{},t)));warn.hidden=!ws.length;}
    const L=pairLayout(),sum=document.getElementById('tpSummary');
    if(sum)sum.textContent=`Tray ${mm(L.tray_w)} × ${mm(L.tray_d)} mm · device ${mm(L.fp_w)} × ${mm(L.fp_d)} mm`+(L.second?` and ${mm(L.second.fp_w)} × ${mm(L.second.fp_d)} mm`:'')+` on the tray · ${state.v.u}U faceplate.`;
  }
  function keystones(){
    const v=state.v,x=h('input',{type:'number',step:'1',value:String(v.keystones.length?Math.min(100,v.keystones.at(-1)+25):-100),style:'width:70px','aria-label':'Keystone X position (mm)'});
    const add=h('button',{type:'button',class:'ew-chip'},'+ Add keystone');add.onclick=()=>{v.keystones.push(Number(x.value));render();};
    return h('div',{class:'ew-ksbar'},'Keystones at X ',x,' mm (0 = centre) ',add,
      ...v.keystones.map((k,i)=>{const b=h('button',{type:'button',class:'ew-chip on',title:'Remove'},`⌧ ${k} mm`);b.onclick=()=>{v.keystones.splice(i,1);render();};return b;}));
  }
  async function post(path,body){
    return fetch(path,{method:'POST',headers:{'Content-Type':'application/json','X-App-Token':appToken()},body:JSON.stringify(body)});
  }
  function secondRequest(){return state.second?{item:state.second.item.id,tray:TrayPair.diff(state.second.item.spec,state.second.v)}:null;}
  function request(){const r={item:state.item.id,tray:diff(state.item.spec,state.v)},s2=secondRequest();if(s2)r.second=s2;return r;}
  // Export quality (render-quality.js) goes with exact renders and exports only; it is never a saved tray setting.
  const exportLevel=()=>window.RenderQuality?.exportLevel()||'standard';
  const exportNote=()=>window.RenderQuality?.exportNote(exportLevel())||'Standard';
  function exportRequest(){return {...request(),quality:exportLevel()};}
  const exactKey=()=>JSON.stringify(state.v)+'|'+JSON.stringify(secondRequest())+'|'+exportLevel();
  async function serverCheck(){
    const r=await post('/api/equipment-placement-check',request()),out=await r.json();
    if(!r.ok)throw Error(out.error||'Check failed');if(!out.ok)throw Error(out.error);
  }
  function setStatus(t){const s=document.getElementById('tpStatus');if(s)s.textContent=t;}
  function render(){
    const d=document.getElementById('trayPlacement');if(!d||!state)return;
    const spec=state.item.spec,v=state.v,name=state.item.display_name||state.item.name,E=editing(),dv=E.v,dspec=E.spec;
    const rot=h('div',{class:'ew-choices',role:'group','aria-label':'Rotation'},...[0,90,180,270].map(r=>{const b=h('button',{type:'button',class:'ew-chip'+(dv.dev_rot===r?' on':''),'aria-pressed':String(dv.dev_rot===r)},r+'°');b.onclick=()=>{dv.dev_rot=r;render();};return b;}));
    const centre=h('button',{type:'button',class:'ew-chip'},'Centre');centre.onclick=()=>{dv.dev_off_x=0;syncFields();update();};
    const wallOpts=dv.device_mount==='wall'?[h('p',{},'Open sides (cables):'),h('div',{class:'ew-row'},...WALL_SIDES.map(side=>{const input=h('input',{type:'checkbox'});input.checked=(dv.wall_open||['rear']).includes(side);input.onchange=()=>{dv.wall_open=WALL_SIDES.filter(s=>s===side?input.checked:(dv.wall_open||['rear']).includes(s));render();};return h('label',{class:'ew-chip'},input,' '+side[0].toUpperCase()+side.slice(1));})),h('p',{class:'ew-note'},'Device sits on the floor inside a 2 mm wall, open where you tick. Fit and retention UNKNOWN.')]:[];
    const mountOpts=PO().usesStandoffs(dv)?[field('Standoff (mm)',()=>dv.standoff,x=>dv.standoff=x,{step:'0.5',min:'0',max:'30'})]:[h('p',{class:'ew-note'},dv.device_mount==='sleeve'?'Low floor, side walls, top lips when space permits, rear stop and optional straps. Front flush; fit/retention/strength UNKNOWN.':v.device_mount==='flat'?'Rests on the low floor with corner stops and optional strap slots. Retention UNKNOWN.':'Rests on the tray floor; no standoffs.')];
    if(dv.device_mount==='inserts')mountOpts.push(field('Insert pilot hole (mm)',()=>dv.insert_pilot,x=>dv.insert_pilot=x,{step:'0.1'}));
    if(dv.device_mount==='pegs'||dv.device_mount==='clips')mountOpts.push(field(dv.device_mount==='pegs'?'Board thickness (mm)':'Edge thickness clipped (mm)',()=>dv.board_t,x=>dv.board_t=x,{step:'0.1'}));
    const rs=h('input',{type:'checkbox'});rs.checked=!!v.rear_support;rs.onchange=()=>{v.rear_support=rs.checked;if(rs.checked&&!v.rear_style)v.rear_style='reinforced';if(!rs.checked)delete v.rear_style;render();};
    const toggleV2=(key,label,hint)=>{const c=h('input',{type:'checkbox'});c.checked=v[key];c.onchange=()=>{v[key]=c.checked;update();};return h('label',{class:'ew-chip'},c,' '+label,h('small',{},' '+hint));};
    const sleeveControls=v.device_mount==='sleeve'?[
      field('Top play (mm)',()=>v.sleeve_top,x=>v.sleeve_top=x,{min:'.3',max:'2',step:'.1'}),
      h('div',{class:'ew-row'},'Feet:',chips({pockets:'Pockets',grooves:'Grooves'},v.feet_style,k=>v.feet_style=k)),
      h('p',{class:'ew-note'},'Grooves lift the case 0.5 mm while sliding, then dip at the feet. Fit and retention UNKNOWN.'),
      toggleV2('rear_floor_opening','Cable opening in floor','Needs rear support; cable fit UNKNOWN.'),
      toggleV2('insert_bosses','Stronger insert bosses','Sleeve + screw joint; strength UNKNOWN.'),
      toggleV2('hidden_joint','Hidden screws','Faceplate screws go in from behind, outside the sleeve walls; device up to about 150 mm wide; strength UNKNOWN.')]:[];
    const styles=h('div',{class:'ew-choices',role:'group','aria-label':'Rear bracket'},h('span',{},'Rear bracket:'),...Object.entries(REAR_STYLES).map(([key,[label]])=>{const b=h('button',{type:'button',class:'ew-chip'+(rearStyle(v)===key?' on':''),'aria-pressed':String(rearStyle(v)===key)},label);b.onclick=()=>{v.rear_style=key;render();};return b;}));
    const cv=h('canvas',{id:'tpView',class:'ew-view tp-view'});
    const exact=h('button',{type:'button'},'Render exact preview');
    exact.onclick=async()=>{exact.disabled=true;setStatus('Rendering with OpenSCAD… this can take a minute. Nothing is saved.');
      try{if(current().length)throw Error('Fix the problems listed first.');const key=exactKey(),r=await post('/api/equipment-preview',exportRequest()),out=await r.json();if(!r.ok)throw Error(out.error||'Preview failed');
        const sets=[];for(const p of out.parts){const buf=await (await fetch(`/api/equipment-mesh/${out.id}/${p}.stl`)).arrayBuffer();sets.push({v:window.EquipmentPainter.parseStl(buf),color:p==='tray'?[77,142,110]:[78,117,163],alpha:1});}
        state.exact={key,sets};draw3D();window.EquipmentRackView?.refresh();setStatus('Exact preview ready. Change any value to go back to the live sketch.');}
      catch(e){setStatus('Problem: '+e.message);}finally{exact.disabled=false;}};
    const exp=h('button',{type:'button',id:'tpExport'},'Generate proposed STL files');
    exp.onclick=async()=>{if(current().length){update();return;}exp.disabled=true;setStatus('Checking, then rendering with OpenSCAD…');
      try{await serverCheck();const r=await post('/api/equipment-build',exportRequest());if(!r.ok)throw Error((await r.json()).error||'Build failed');
        const url=URL.createObjectURL(await r.blob()),a=document.createElement('a');a.href=url;a.download=(name||'equipment').replace(/[^\w-]+/g,'_')+'-'+(window.rackUText?window.rackUText(state.slot,state.span).replace('–','-'):'slot-'+state.slot)+'-stl.zip';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);window.EquipmentRackView?.refresh();
        setStatus(`Done (${exportNote()}). PROPOSED — UNVALIDATED STLs for these window values; export.json in the zip records the quality.`+' The rack draft is unchanged until you Apply and Save.');}
      catch(e){setStatus('Problem: '+e.message);}finally{update();}};
    const apply=h('button',{type:'button',id:'tpApply',class:'primary'},'Apply to draft');
    apply.onclick=async()=>{if(current().length){update();return;}apply.disabled=true;setStatus('Checking…');
      try{await serverCheck();if(!window.applyTrayPlacement)throw Error('The workspace is not ready.');const s2=secondRequest();
        window.applyTrayPlacement(state.rack,state.id,diff(spec,v),v.u!==state.prevU?v.u:null,s2&&{equipment:s2.item,...(Object.keys(s2.tray).length?{tray:s2.tray}:{})});d.close();}
      catch(e){setStatus('Problem: '+e.message);update();}};
    const cancel=h('button',{type:'button'},'Cancel');cancel.onclick=()=>d.close();
    const lib=h('button',{type:'button',class:'subtle'},'Edit library item…');lib.onclick=()=>{const id=(state.tab===2&&state.second?state.second.item:state.item).id;d.close();window.openCustomEquipment?.({equipment:id});};
    const offX=field('Left/right offset (mm)',()=>dv.dev_off_x,x=>dv.dev_off_x=x,{id:'tpOffX'});
    const gap=field('Front gap (mm)',()=>FRONT_GAP+dv.dev_off_y,x=>dv.dev_off_y=x-FRONT_GAP,{id:'tpGap',min:'0'});
    // Device tabs (option A, Brian 2026-10-20): Position and Mounting edit the selected device; Faceplate is shared.
    const tab=(n,label)=>{const b=h('button',{type:'button',role:'tab',class:'tp-tab'+(state.tab===n?' on':''),'aria-selected':String(state.tab===n)},label);b.onclick=()=>{state.tab=n;render();};return b;};
    const tabs=h('div',{class:'tp-tabs',role:'tablist','aria-label':'Devices on this tray'},tab(1,(state.second?'1 · ':'')+name));
    if(state.second){const rm=h('button',{type:'button',class:'tp-tab-x',title:'Remove the second device','aria-label':'Remove the second device'},'✕');
      rm.onclick=()=>{state.second=null;state.tab=1;render();};tabs.append(h('span',{class:'tp-tab-pair'},tab(2,'2 · '+(state.second.item.display_name||state.second.item.name)),rm));}
    else{const pick=h('select',{'aria-label':'Second device'},h('option',{value:''},'+ Add a second device…'),...(window.equipmentLibraryItems?.()||[]).map(i=>h('option',{value:i.id},i.display_name||i.name)));
      pick.onchange=()=>{const item=(window.equipmentLibraryItems?.()||[]).find(i=>i.id===pick.value);if(item)addSecond(item);};tabs.append(pick);}

    const position=h('div',{class:'ew-row'},h('span',{},'Front position:'),chips({today:'As today',flush:'Flush with faceplate',setback:'Set back'},v.front_position,k=>{v.front_position=k;}),...(v.front_position==='setback'?[field('Set back (mm)',()=>v.front_setback,x=>v.front_setback=x,{min:'0',max:'100',step:'.1'})]:[]));
    const bezel=h('div',{class:'ew-row'},h('span',{},'Bezel:'),chips({none:'None',chamfer:'Chamfer',rounded:'Rounded'},v.bezel,k=>v.bezel=k),...(v.bezel!=='none'?[field('Bezel size (mm)',()=>v.bezel_size,x=>v.bezel_size=x,{min:'.5',max:'1.5',step:'.1'})]:[]));
    d.replaceChildren(
      h('div',{class:'tp-head'},h('div',{},h('p',{class:'section-eyebrow'},'PLACE ON TRAY · '+(window.rackUText?window.rackUText(state.slot,state.span):'SLOT '+state.slot)),h('h2',{},state.tab===2&&state.second?state.second.item.display_name||state.second.item.name:name)),lib),
      h('p',{class:'ew-note'},`${dspec.dev_w} × ${dspec.dev_d} × ${dspec.dev_h} mm, ${(dspec.holes||[]).length} mounting hole(s). These choices belong to this slot only; the library item is not changed.`),tabs,
      h('div',{class:'tp-grid'},
        h('div',{class:'tp-pane'},h('h3',{},'Top view'),document.createElementNS(NS,'svg'),
          h('p',{class:'ew-note'},(state.second?'Yellow = device 1, blue = device 2; drag either. They need at least '+TrayPair.GAP+' mm between them (more for clips, straps and flat stops). ':'')+'Drag the device (snaps to 1 mm). Orange edge = device front. Blue dots = screw/hole positions. Dashed outline = the '+MAX_TRAY+' mm tray limit (rack opening minus side clearance).'),
          h('h3',{},'Position'+(state.second?' · device '+state.tab:'')),h('div',{class:'ew-row'},offX,centre),...(v.front_position==='today'?[h('div',{class:'ew-row'},gap)]:[]),
          ...(state.tab===1?[position,h('p',{class:'ew-note'},'Flush and Set back are measured from the outside front face. Set back: 0–100 mm. Near the plate, use Sleeve or a single printed piece; flat corner stops need at least 10.2 mm set back.')]:[h('p',{class:'ew-note'},'Both devices use the As today front position. Faceplate height, joint, keystones and rear support are shared by the whole tray.')]),h('div',{class:'ew-row'},'Rotate ',rot),
          h('h3',{},'Mounting'+(state.second?' · device '+state.tab:'')),chips(MOUNTS,dv.device_mount,k=>dv.device_mount=k),h('div',{class:'ew-row'},...mountOpts),...wallOpts),
        h('div',{class:'tp-pane'},h('h3',{},'Live 3D preview'),cv,h('p',{id:'tpViewNote',class:'ew-note'}),h('div',{class:'ew-row'},exact,window.RenderQuality?.previewSlider('placement',draw3D)||''),
          h('h3',{},'Faceplate'),bezel,h('p',{class:'ew-note'},'Bezel softens front opening edges only. Size 0.5–1.5 mm; reduced or omitted to preserve 2 mm webs. Rounded prints best with the front face up; Chamfer prints either way.'),h('div',{class:'ew-row'},field('Height (rack units)',()=>v.u,x=>v.u=x,{min:'1',max:'5'})),keystones(),
          h('p',{},'Tray joint'),chips(JOINTS,v.joint,k=>v.joint=k),
          h('label',{class:'ew-chip'},rs,' Rear support (tray runs to the back posts)'),
          ...sleeveControls,
          ...(v.rear_support?[styles,h('p',{class:'ew-note'},REAR_STYLES[rearStyle(v)][1]+'; stiffness/airflow UNKNOWN')]:[]),
          h('p',{class:'tp-unknown'},'Fit, retention, strength: UNKNOWN'))),
      h('p',{id:'tpSummary',class:'ew-note'}),
      h('ul',{id:'tpProblems',class:'tp-problems',role:'alert'}),
      h('ul',{id:'tpWarnings',class:'tp-warnings',role:'status'}),
      h('p',{id:'tpStatus',class:'ew-note',role:'status'},'Changes stay in this window until you press Apply to draft. Apply changes the rack draft only; use Save to keep it.'),
      h('div',{class:'ew-nav'},exp,window.RenderQuality?.exportSlider(()=>draw3D(),'tp-export-quality')||'',cancel,apply));
    const svg=d.querySelector('.tp-pane svg');svg.id='tpTop';svg.setAttribute('class','tp-top');svg.setAttribute('role','img');svg.setAttribute('aria-label','Top view of the tray and faceplate');
    if(!cv.tpBound){cv.tpBound=true;window.EquipmentPainter?.bind(cv,view,draw3D);}
    update();
  }
  function ensureDialog(){
    let d=document.getElementById('trayPlacement');
    if(!d){d=h('dialog',{id:'trayPlacement',class:'ew-dialog tp-dialog','aria-label':'Place on tray'});document.body.append(d);
      d.addEventListener('close',()=>{window.EquipmentPainter?.dispose(document.getElementById('tpView'));state=null;});
      document.head.append(h('style',{},`.tp-dialog{width:min(1040px,96vw)}.tp-head{display:flex;justify-content:space-between;align-items:flex-start;gap:8px}.tp-head h2{margin:0}
.tp-grid{display:grid;grid-template-columns:1.15fr 1fr;gap:14px}@media(max-width:760px){.tp-grid{grid-template-columns:1fr}}.tp-pane h3{margin:10px 0 4px;font-size:13px;color:#cfd6df}
.tp-top{width:100%;height:300px;background:#121418;border-radius:6px;touch-action:none}.tp-view{height:240px}.tp-unknown{color:#e0b56f;font-weight:600;margin-top:10px}
.tp-tabs{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:8px 0;border-bottom:1px solid #3a3f48;padding-bottom:6px}.tp-tab{background:#2b2f37;color:#ddd;border:1px solid #4a4f59;border-radius:6px 6px 0 0;padding:5px 12px;cursor:pointer}.tp-tab.on{background:#3b6fa8;border-color:#6ea0d8;color:#fff}.tp-tab-pair{display:inline-flex;gap:2px}.tp-tab-x{background:none;border:none;color:#e09a9a;cursor:pointer;font-size:14px}.tp-tabs select{background:#15171b;color:#ddd;border:1px dashed #5a606b;border-radius:6px;padding:4px}
.tp-problems{color:#ff9a9a;margin:6px 0;padding-left:18px}.tp-problems:empty{display:none}.tp-warnings{color:#e0b56f;margin:6px 0;padding-left:18px}.tp-warnings:empty{display:none}`));}
    return d;
  }
  function addSecond(item){
    const v=state.v,v2={...TrayPair.values(item.spec),dev_off_y:v.dev_off_y,dev_rot:0};if(v2.device_mount==='sleeve')v2.device_mount=v.device_mount==='flat'?'flat':'straps';
    const w1=layout(state.item.spec,v).fp_w,w2=layout(item.spec,TrayPair.merged(v,v2)).fp_w,need=Math.max(TrayPair.GAP,(TrayPair.REACH[v.device_mount]||0)+(TrayPair.REACH[v2.device_mount]||0)),total=w1+need+w2;
    v.dev_off_x=snap(-total/2+w1/2);v2.dev_off_x=snap(total/2-w2/2);
    state.second={item,v:v2};state.tab=2;render();
    setStatus('Second device added beside the first; the pair is centred. Drag either one. Apply changes the rack draft only.');
  }
  // Called by workspace.js when a library item is placed in a slot or its slot placement is edited.
  window.openTrayPlacement=async function(rackId,placement){
    let item=(window.equipmentLibraryItems?.()||[]).find(i=>i.id===placement.equipment);
    if(!item)try{item=(await (await fetch('/api/equipment-library')).json()).find(i=>i.id===placement.equipment);}catch(e){}
    if(!item){alert('This equipment is no longer in the library.');return false;}
    const v=values(item.spec,placement.tray);
    let second=null;if(placement.second){const s2=(window.equipmentLibraryItems?.()||[]).find(i=>i.id===placement.second.equipment);
      if(!s2){alert('The second device on this tray is no longer in the library.');return false;}second={item:s2,v:TrayPair.values(s2.spec,placement.second.tray)};}
    // Existing rear-supported items retain their legacy solid/open choice.
    state={rack:rackId,id:placement.id,slot:placement.slot,span:placement.span,item,v,prevU:v.u,exact:null,second,tab:1};
    // Paint again once the dialog is shown: the canvas has no size before that.
    const d=ensureDialog();render();if(!d.open)d.showModal();draw3D();return true;
  };
})(typeof window!=='undefined'?window:globalThis);
