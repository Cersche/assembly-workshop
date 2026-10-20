// Pure opening planning. Physical fit and strength remain UNKNOWN.
(function(root){
  'use strict';
  const DEFAULT_SIZES={'rj45':{w:17,h:14,r:1},'usb-a':{w:15,h:8,r:1},'usb-c':{w:12,h:7,r:3},hdmi:{w:17,h:8,r:1},'micro-hdmi':{w:11,h:7,r:2},'dc-barrel':{w:11,h:11,r:5.5},iec:{w:28,h:20,r:1},other:{w:15,h:8,r:1}};
  const SIZE_NOTE='Starting size for this connector type: a guess, not a measured size. Edit it to match your device.';
  function defaultSize(type){return {...(Object.prototype.hasOwnProperty.call(DEFAULT_SIZES,type)?DEFAULT_SIZES[type]:DEFAULT_SIZES.other)};}
  function lift(spec){return spec.device_mount==='straps'?0:+(spec.standoff===undefined?6:spec.standoff);}
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
  function problems(ports,u,keystones){
    const out=[],plate_h=u*44.45-2.45;
    (ports||[]).forEach((p,i)=>{
      const {x,z,w,h}=p,label=p.label||'Port '+(i+1);
      if(![x,z,w,h].every(Number.isFinite))return;
      if(Math.abs(x)+w/2>126)out.push(`${label} opening would run past the faceplate edge. Move the device back toward the centre or edit the port.`);
      else if(z-h/2<2||z+h/2>plate_h-2)out.push(`${label} opening would run off the top or bottom of the faceplate. Change the standoff or faceplate height, or edit the port.`);
      else {const n=(keystones||[]).findIndex(k=>Math.abs(x-k)<10.5+w/2&&z-h/2<plate_h/2+18.5&&z+h/2>plate_h/2-15);
        if(n>=0)out.push(`${label} opening would cut into keystone ${n+1} (at X = ${keystones[n]} mm). Move the device or the keystone.`);}
    });
    return out;
  }
  const api={DEFAULT_SIZES,SIZE_NOTE,defaultSize,lift,frontOpenings,problems};
  root.LabRaxPortOpenings=api;if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(globalThis);
