// Envelope SCREENING for wizard equipment in a rack slot. Nominal numbers only: it never establishes
// physical fit (which stays UNKNOWN) and never changes geometry, hardware or saved data.
(function(root){
  'use strict';
  const PITCH=44.45;
  // Same stack the wizard uses: 10 mm tray floor + standoff (none for straps) + device height.
  const FLOOR=10,FACE_OFFSET=12,TRAY_SIDES=16,REAR_TRAY=240; // REAR_TRAY = rack_depth in equipment_tray.scad
  // Screening thresholds (assumptions, not tolerances): below these margins a result is "tight".
  const TIGHT={height:3,width:5,depth:10};
  function grade(name,label,needed,available,unit='mm'){
    if(available===null||available===undefined||!Number.isFinite(available))
      return {name,level:'unknown',needed,available:null,text:`${label}: needs ${needed.toFixed(1)} ${unit}; rack value not specified (UNKNOWN).`};
    const margin=available-needed,level=margin<0?'over':margin<TIGHT[name]?'tight':'ok';
    const verb=level==='over'?`exceeds by ${(-margin).toFixed(1)} ${unit}`:`${margin.toFixed(1)} ${unit} spare`;
    return {name,level,needed,available,margin,text:`${label}: ${needed.toFixed(1)} of ${available.toFixed(1)} ${unit} nominal (${verb}).`};
  }
  function screen(rack,placement,item){
    if(!item?.spec)return {level:'unknown',checks:[],note:'Equipment not found in the library; cannot screen. Rack fit UNKNOWN.'};
    // This slot's tray choices (placement.tray, Place on tray window) win over the library values, as in
    // equipment.allocation_spec(). Rotation swaps width and depth; offsets widen the tray and push the device back.
    const tray=placement.tray||{},s={...item.spec,...tray},checks=[];
    const turned=+s.dev_rot===90||+s.dev_rot===270,fpW=turned?+s.dev_d:+s.dev_w,fpD=turned?+s.dev_w:+s.dev_d;
    const lift=FLOOR+(s.device_mount==='straps'?0:(+s.standoff||0));
    checks.push(grade('height',`Height in ${placement.span}U`,lift+(+s.dev_h),placement.span*(rack.pitch_mm||PITCH)));
    checks.push(grade('width','Tray width vs internal width',fpW+TRAY_SIDES+2*Math.abs(+s.dev_off_x||0),rack.width_mm));
    const depth=FACE_OFFSET+(+s.dev_off_y||0)+fpD;
    const depthCheck=grade('depth',s.rear_support?'Rear-support tray depth vs usable depth':'Depth behind faceplate vs usable depth',s.rear_support?Math.max(depth,REAR_TRAY):depth,rack.depth_mm);
    // Brian, 2026-10-19: a rear-support tray reaches the back posts on purpose, so a depth equal to the rack depth is
    // OK (by design), not TIGHT. A device that pushes the tray past the rack depth is still graded normally.
    if(s.rear_support&&depthCheck.level==='tight'&&depth<=REAR_TRAY&&Math.abs(depthCheck.available-REAR_TRAY)<0.5)
      Object.assign(depthCheck,{level:'ok',byDesign:true,text:`Rear-support tray depth: OK (by design). The tray runs to the back posts (${REAR_TRAY.toFixed(1)} of ${depthCheck.available.toFixed(1)} mm nominal).`});
    checks.push(depthCheck);
    const designed='u' in tray?+tray.u:item.span;
    if(designed&&placement.span<designed)checks.push({name:'span',level:'over',text:`Equipment was designed for ${designed}U but the slot allocation is ${placement.span}U.`});
    const order=['over','tight','unknown','ok'],level=order.find(l=>checks.some(c=>c.level===l))||'ok';
    return {level,checks,note:'Screening only, against nominal rack numbers. Printed fit, cables and tool access remain UNKNOWN.'};
  }
  const api={screen,TIGHT,PITCH};root.WorkshopClearance=api;
  if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
