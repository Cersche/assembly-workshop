// Pure opening planning. Physical fit and strength remain UNKNOWN.
(function(root){
  'use strict';
  const RACK_PITCH=44.45,PLATE_GAP=0.05,LEGACY_SLOT_OFFSET=1.225;
  const plateHeight=u=>u*RACK_PITCH-PLATE_GAP,plateBottom=PLATE_GAP/2;
  // PROPOSED defaults: independent sleeve, nominal clearances; fit/strength UNKNOWN.
  const SLEEVE=Object.freeze({side:0.5,top:0.3,wall:6,lipW:10,lipT:1.5,band:1.5,stopT:4,stopH:6});
  const FOOT=Object.freeze({clearance:0.5,extraDepth:0.3,minFloor:0.8,lipT:3.0});
  const footHeight=s=>['flat','sleeve'].includes(s.device_mount)?Math.max(0,...(s.feet||[]).map(f=>+f.h||0)):0;
  const pocketDepth=s=>footHeight(s)+FOOT.extraDepth;
  const deviceCaseHeight=s=>Math.max(0,(+s.dev_h||0)-footHeight(s));
  function sleeve(s){if(s.device_mount!=='sleeve')return null;
    const turned=[90,270].includes(+s.dev_rot),w=+(turned?s.dev_d:s.dev_w),d=+(turned?s.dev_w:s.dev_d),x=+(s.dev_off_x||0),bottom=3.5,half=w/2+SLEEVE.side,top=bottom+deviceCaseHeight(s)+SLEEVE.top;
    const lipT=footHeight(s)?FOOT.lipT:SLEEVE.lipT;
    return {x,half,bottom,top,width:half*2,height:top-bottom,outside:w+2*(SLEEVE.side+SLEEVE.wall),lip:top+lipT<=(+s.u||1)*RACK_PITCH?lipT:0,rear:-4+d,stop_end:-4+d+SLEEVE.stopT,joints:[x-half-SLEEVE.wall/2,x+half+SLEEVE.wall/2],joint_z:[bottom+3,top-3]};
  }
  function sleevePorts(ports,s){const w=sleeve(s),kept=[],dropped=[],errors=[];if(!w)return {ports:ports||[],dropped,errors};
    for(const p of ports||[]){const x0=p.x-p.w/2,x1=p.x+p.w/2,z0=p.z-p.h/2,z1=p.z+p.h/2;
      if(x0>=w.x-w.half&&x1<=w.x+w.half&&z0>=w.bottom&&z1<=w.top)dropped.push(p);
      else if(x1>w.x-w.half&&x0<w.x+w.half&&z1>w.bottom&&z0<w.top)errors.push('A front opening crosses the sleeve window edge; move or remove it.');
      else kept.push(p);
    }return {ports:kept,dropped,errors};
  }
  const DEFAULT_SIZES={'rj45':{w:17,h:14,r:1},'usb-a':{w:15,h:8,r:1},'usb-c':{w:12,h:7,r:3},hdmi:{w:17,h:8,r:1},'micro-hdmi':{w:11,h:7,r:2},'dc-barrel':{w:11,h:11,r:5.5},iec:{w:28,h:20,r:1},other:{w:15,h:8,r:1}};
  const SIZE_NOTE='Starting size for this connector type: a guess, not a measured size. Edit it to match your device.';
  function defaultSize(type){return {...(Object.prototype.hasOwnProperty.call(DEFAULT_SIZES,type)?DEFAULT_SIZES[type]:DEFAULT_SIZES.other)};}
  // Shared height rule for the wizard, placement sketches and cable markers; mirrors equipment.py.
  const floorZ=spec=>['flat','sleeve'].includes(spec.device_mount)?0.5:7+LEGACY_SLOT_OFFSET;
  const usesStandoffs=spec=>!['straps','flat','sleeve'].includes(spec.device_mount);
  const deviceLift=spec=>floorZ(spec)+3+(usesStandoffs(spec)?+(spec.standoff===undefined?6:spec.standoff):0)-footHeight(spec);  // case on the floor top; feet hang in their pockets
  const neededHeight=spec=>{const m=spec.device_mount,extra=['pegs','clips'].includes(m)?+(spec.board_t??1.6)+(m==='pegs'?1.6:2.5):0;return Math.max(deviceLift(spec)+Math.max(+spec.dev_h,extra),(spec.joint||'screw')==='screw'?floorZ(spec)+22:0);};
  const autoU=spec=>Math.min(5,Math.max(1,Math.ceil(neededHeight(spec)/RACK_PITCH)));
  function flatHint(spec){
    const flat={...spec,device_mount:'flat'},u=Math.ceil(neededHeight(flat)/RACK_PITCH);
    return u>=1&&u<=5&&u<Math.ceil(neededHeight(spec)/RACK_PITCH)?`Fits ${u}U if it sits flat (no standoffs): ${Math.round(neededHeight(flat)*100)/100} mm needed / ${u*RACK_PITCH} mm available. Choose 'Sits flat' as the tray default mount on the Ports step, or under Mounting in Place on tray per slot.`:'';
  }
  // Historical public lift is relative to the old floor top (10 mm); differences include the new floor.
  function lift(spec){return ['flat','sleeve'].includes(spec.device_mount)?deviceLift(spec)-(7+LEGACY_SLOT_OFFSET+3):spec.device_mount==='straps'?0:+(spec.standoff??6);}
  function frontOpenings(libSpec,tray){
    const eff={...libSpec};
    for(const k of ['dev_off_x','dev_rot','device_mount','standoff'])if(tray&&k in tray)eff[k]=tray[k];
    const rotation=+(eff.dev_rot||0),follows=rotation===0;
    const dx=follows?+(eff.dev_off_x||0)-+(libSpec.dev_off_x||0):0,dz=follows?Math.round((lift(eff)-lift(libSpec))*1000)/1000:0;
    const ports=(libSpec.ports||[]).map(p=>follows?{...p,x:Math.round((+p.x+dx)*1000)/1000,z:Math.round((+p.z+dz)*1000)/1000}:{...p});
    const face=rotation===180?'rear':'side';
    const message=!follows&&ports.length?`The device is turned ${rotation}°, so its front ports now face the ${face} of the tray. The front openings no longer line up with them. The faceplate STL keeps the openings where they were entered in the library (not moved). Check them, or remove them in Edit library item.`:null;
    return {ports,dx,dz,follows,rotation,message};
  }
  // Tray screw joint behind the faceplate (equipment_tray.scad): block, tongue, boss and post fill X = joint ± 9 mm up to
  // Z = 29 mm; an opening there would be blocked (Brian, 2026-10-19). 1 mm clearance. Same rule as port_openings.py.
  const JOINT_HALF=9,JOINT_TOP=29+LEGACY_SLOT_OFFSET,JOINT_CLEAR=1;
  function problems(ports,u,keystones,joints){
    const out=[],plate_h=plateHeight(u);
    (ports||[]).forEach((p,i)=>{
      const {x,z,w,h}=p,label=p.label||'Port '+(i+1);
      if(![x,z,w,h].every(Number.isFinite))return;
      if(Math.abs(x)+w/2>126)out.push(`${label} opening would run past the faceplate edge. Move the device back toward the centre or edit the port.`);
      else if(z-h/2<plateBottom+2||z+h/2>plateBottom+plate_h-2)out.push(`${label} opening would run off the top or bottom of the faceplate. Change the standoff or faceplate height, or edit the port.`);
      else {const n=(keystones||[]).findIndex(k=>Math.abs(x-k)<10.5+w/2&&z-h/2<u*RACK_PITCH/2+18.5&&z+h/2>u*RACK_PITCH/2-15);
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
  const api={SLEEVE,FOOT,footHeight,pocketDepth,deviceCaseHeight,sleeve,sleevePorts,RACK_PITCH,PLATE_GAP,plateBottom,plateHeight,floorZ,usesStandoffs,deviceLift,neededHeight,autoU,flatHint,DEFAULT_SIZES,SIZE_NOTE,JOINT_HALF,JOINT_TOP,JOINT_CLEAR,jointPositions,defaultSize,lift,frontOpenings,problems};
  root.LabRaxPortOpenings=api;if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(globalThis);
