// Pure opening planning. Physical fit and strength remain UNKNOWN.
(function(root){
  'use strict';
  const DEFAULT_SIZES={'rj45':{w:17,h:14,r:1},'usb-a':{w:15,h:8,r:1},'usb-c':{w:12,h:7,r:3},hdmi:{w:17,h:8,r:1},'micro-hdmi':{w:11,h:7,r:2},'dc-barrel':{w:11,h:11,r:5.5},iec:{w:28,h:20,r:1},other:{w:15,h:8,r:1}};
  const SIZE_NOTE='Starting size for this connector type: a guess, not a measured size. Edit it to match your device.';
  function defaultSize(type){return {...(Object.prototype.hasOwnProperty.call(DEFAULT_SIZES,type)?DEFAULT_SIZES[type]:DEFAULT_SIZES.other)};}
  // Shared height rule for the wizard, placement sketches and cable markers; mirrors equipment.py.
  const floorZ=spec=>spec.device_mount==='flat'?0.5:7;
  const usesStandoffs=spec=>!['straps','flat'].includes(spec.device_mount);
  const deviceLift=spec=>floorZ(spec)+3+(usesStandoffs(spec)?+(spec.standoff===undefined?6:spec.standoff):0);
  const neededHeight=spec=>deviceLift(spec)+ +spec.dev_h;
  const autoU=spec=>Math.min(5,Math.max(1,Math.ceil(neededHeight(spec)/44.45)));
  function flatHint(spec){
    const flat={...spec,device_mount:'flat'},u=Math.ceil(neededHeight(flat)/44.45);
    return u>=1&&u<=5&&u<Math.ceil(neededHeight(spec)/44.45)?`Fits ${u}U if it sits flat (no standoffs): ${Math.round(neededHeight(flat)*100)/100} mm needed / ${u*44.45} mm available. Choose 'Sits flat' under Mounting in Place on tray.`:'';
  }
  // Historical public lift is relative to the old floor top (10 mm); differences include the new floor.
  function lift(spec){return deviceLift(spec)-10;}
  function frontOpenings(libSpec,tray){
    const eff={...libSpec};
    for(const k of ['dev_off_x','dev_rot','device_mount','standoff'])if(tray&&k in tray)eff[k]=tray[k];
    const rotation=+(eff.dev_rot||0),follows=rotation===0;
    const dx=follows?+(eff.dev_off_x||0)-+(libSpec.dev_off_x||0):0,dz=follows?lift(eff)-lift(libSpec):0;
    const ports=(libSpec.ports||[]).map(p=>follows?{...p,x:Math.round((+p.x+dx)*1000)/1000,z:Math.round((+p.z+dz)*1000)/1000}:{...p});
    const face=rotation===180?'rear':'side';
    const message=!follows&&ports.length?`The device is turned ${rotation}°, so its front ports now face the ${face} of the tray. The front openings no longer line up with them. The faceplate STL keeps the openings where they were entered in the library (not moved). Check them, or remove them in Edit library item.`:null;
    return {ports,dx,dz,follows,rotation,message};
  }
  // Tray screw joint behind the faceplate (equipment_tray.scad): block, tongue, boss and post fill X = joint ± 9 mm up to
  // Z = 29 mm; an opening there would be blocked (Brian, 2026-10-19). 1 mm clearance. Same rule as port_openings.py.
  const JOINT_HALF=9,JOINT_TOP=29,JOINT_CLEAR=1;
  function problems(ports,u,keystones,joints){
    const out=[],plate_h=u*44.45-2.45;
    (ports||[]).forEach((p,i)=>{
      const {x,z,w,h}=p,label=p.label||'Port '+(i+1);
      if(![x,z,w,h].every(Number.isFinite))return;
      if(Math.abs(x)+w/2>126)out.push(`${label} opening would run past the faceplate edge. Move the device back toward the centre or edit the port.`);
      else if(z-h/2<2||z+h/2>plate_h-2)out.push(`${label} opening would run off the top or bottom of the faceplate. Change the standoff or faceplate height, or edit the port.`);
      else {const n=(keystones||[]).findIndex(k=>Math.abs(x-k)<10.5+w/2&&z-h/2<plate_h/2+18.5&&z+h/2>plate_h/2-15);
        if(n>=0)out.push(`${label} opening would cut into keystone ${n+1} (at X = ${keystones[n]} mm). Move the device or the keystone.`);
        else{const j=(joints||[]).find(j=>Math.abs(x-j)<JOINT_HALF+JOINT_CLEAR+w/2&&z-h/2<JOINT_TOP+JOINT_CLEAR);
          if(j!==undefined)out.push(`${label} opening sits in front of the tray screw joint at X = ${j} mm; the cable would hit it. Move the device sideways or edit the port.`);}}
    });
    return out;
  }
  // Brian, 2026-10-19 (option 3): each tray screw joint sits where it clears the openings and keystones; the default
  // spot (±min(40, tray_w/2 − 12)) is kept when clear, else the nearest clear spot (0.5 mm steps, 10 mm … tray_w/2 − 12)
  // for that side. Same rule as port_openings.joint_positions().
  const KEYSTONE_JOINT_GAP=16,JOINT_STEP=0.5,JOINT_MIN=10;
  function jointClear(x,ports,keystones){
    for(const p of ports||[]){const {x:px,z,w,h}=p;if(![px,z,w,h].every(Number.isFinite))continue;
      if(Math.abs(px-x)<JOINT_HALF+JOINT_CLEAR+w/2&&z-h/2<JOINT_TOP+JOINT_CLEAR)return false;}
    return (keystones||[]).every(k=>Math.abs(k-x)>=KEYSTONE_JOINT_GAP);
  }
  const r3=x=>Math.round(x*1000)/1000;
  function jointPositions(ports,keystones,trayHalf){
    const def=Math.min(40,trayHalf-12),lo=Math.min(def,JOINT_MIN),hi=trayHalf-12,n=Math.round((hi-lo)/JOINT_STEP);
    const mags=[...new Set([...Array.from({length:Math.max(0,n+1)},(_,i)=>r3(lo+i*JOINT_STEP)),def])].sort((a,b)=>Math.abs(a-def)-Math.abs(b-def)||b-a);
    const joints=[-1,1].map(sign=>{const m=mags.find(m=>jointClear(sign*m,ports,keystones));return m===undefined?null:sign*m;});
    const missing=['left','right'].filter((_,i)=>joints[i]===null);
    const problem=missing.length?`The ${missing.join(' and ')} tray screw joint${missing.length>1?'s':''} cannot be placed clear of the openings and keystones anywhere on the tray. Move the device or an opening, or choose the single printed piece joint.`:null;
    return {joints,default:def,moved:joints[0]!==-def||joints[1]!==def,problem};
  }
  const api={floorZ,usesStandoffs,deviceLift,neededHeight,autoU,flatHint,DEFAULT_SIZES,SIZE_NOTE,JOINT_HALF,JOINT_TOP,JOINT_CLEAR,jointPositions,defaultSize,lift,frontOpenings,problems};
  root.LabRaxPortOpenings=api;if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(globalThis);
