// Two devices on one tray (Brian, 2026-10-20: "space permitting"). Mirrors equipment.py clean_pair()/pair_problems().
// The first device keeps the slot's tray settings; the second (placement.second = {equipment, tray}) has its own
// position, rotation and mounting (SECOND_KEYS) and shares the rest. Fit, retention and strength stay UNKNOWN.
(function(root){
  'use strict';
  const SECOND_KEYS=['dev_off_x','dev_off_y','dev_rot','device_mount','wall_open','standoff','insert_pilot','board_t'];
  const GAP=4,MARGIN=8,WEB=2; // PROPOSED gap between footprints; equipment_tray.scad margin; 2 mm faceplate web
  // How far each mounting's printed features reach outside the footprint (equipment_tray.scad device_features_*).
  const REACH={inserts:0,pegs:0,clips:2.5,straps:5.5,wall:2.5,flat:6.2};
  function T(){if(root.TrayPlacement)return root.TrayPlacement;if(typeof require==='function')return require('./tray-placement.js');return null;}
  function PO(){if(root.LabRaxPortOpenings)return root.LabRaxPortOpenings;if(typeof require==='function')return require('./port-openings.js');return null;}
  const mm=x=>Math.round(x*10)/10;
  // Values shown for the second device: its own keys (slot tray, then its library item, then defaults).
  function values(spec2,tray2){const all=T().values(spec2,tray2),out={};for(const k of SECOND_KEYS)out[k]=all[k];return out;}
  // What goes into placement.second.tray: only own keys that differ from the second library item.
  function diff(spec2,v2){const d=T().diff(spec2,{...T().values(spec2),...v2}),out={};for(const k of SECOND_KEYS)if(k in d)out[k]=d[k];return out;}
  // The second device as a full value set: the slot's shared settings with its own keys on top.
  function merged(v1,v2){return {...v1,...v2,keystones:[],front_position:'today',bezel:'none'};}
  function footprint(spec,v){const L=T().layout(spec,v);return [L.dev_x,L.dev_x+L.fp_w,L.dev_y,L.dev_y+L.fp_d];}
  function half(spec1,v1,spec2,v2){return Math.max(...[...footprint(spec1,v1).slice(0,2),...footprint(spec2,merged(v1,v2)).slice(0,2)].map(Math.abs))+MARGIN;}
  function layout(spec1,v1,spec2,v2){const L=T().layout(spec1,v1);if(!spec2)return L;const m=merged(v1,v2),L2=T().layout(spec2,m),w=2*half(spec1,v1,spec2,v2);
    return {...L,tray_w:w,tray_d:v1.rear_support?L.tray_d:Math.max(L.tray_d,L2.tray_d),jx:Math.min(40,w/2-12),second:L2};}
  function ports2(spec2,m){return T().openings(spec2,m).ports.map(p=>({...p,id:'d2-'+(p.id||'')}));}
  // Plain-language problems that come from sharing the tray. Any message blocks Apply and export.
  function problems(spec1,v1,spec2,v2){
    const out=[],m=merged(v1,v2);
    if([v1.device_mount,m.device_mount].includes('sleeve'))out.push('A sleeve boxes in the whole front, so it cannot share a tray. Choose another mounting, or use one device.');
    if(v1.front_position!=='today')out.push('With two devices, use the As today front position (Flush and Set back cut a window for one device only).');
    if((v1.device_mount==='flat')!==(m.device_mount==='flat'))out.push('Both devices sit on one tray floor: either both use Sits flat, or neither does.');
    if(out.length)return out;
    out.push(...T().problems(spec2,m,true).filter(t=>!/tray is .* mm wide|screw joints? cannot be placed/.test(t)).map(t=>'Second device: '+t));
    const a=footprint(spec1,v1),b=footprint(spec2,m),need=Math.max(GAP,(REACH[v1.device_mount]||0)+(REACH[m.device_mount]||0));
    const apart=Math.max(b[0]-a[1],a[0]-b[1],b[2]-a[3],a[2]-b[3]);
    if(apart<need-1e-9)out.push(`The two devices are ${apart<0?'overlapping':'only '+mm(apart)+' mm apart'}; they need at least ${need} mm between them (mounting features included). Drag one sideways or behind the other.`);
    const H=half(spec1,v1,spec2,v2);
    if(2*H>T().MAX_TRAY)out.push(`Together the two devices need a tray ${mm(2*H)} mm wide; the rack opening allows ${T().MAX_TRAY} mm. Rotate one, move them closer to the centre, or put one behind the other.`);
    if(v1.rear_support&&(spec2.protrusions||[]).length)out.push('Rear keep-clear zones of the second device are not supported yet; remove them in its library item or turn off rear support.');
    const ks=v1.keystones||[];
    if(ks.some(x=>Math.abs(x)-9.9<H+0.5))out.push(`A keystone collar would hit the tray; keep keystones at least ${mm(H+10.4)} mm from the centre.`);
    const p1=T().openings(spec1,v1).ports,p2=ports2(spec2,m);
    out.push(...PO().problems(p2,v1.u,ks));
    clash:for(const p of p1)for(const q of p2)if(Math.abs(p.x-q.x)-(p.w+q.w)/2<WEB&&Math.abs(p.z-q.z)-(p.h+q.h)/2<WEB){out.push(`The ${p.label||'first device'} and ${q.label||'second device'} openings are closer than ${WEB} mm on the faceplate. Move one device sideways.`);break clash;}
    const j=v1.joint==='screw'?PO().jointPositions([...p1,...p2],ks,H):null;if(j?.problem)out.push(j.problem);
    for(const [sp,v] of [[spec1,v1],[spec2,m]]){const wp=T().wallProblem(sp,v,j?.joints||[]);if(wp&&!out.includes(wp))out.push(wp);}
    return out;
  }
  // Live sketch with both devices: device 1's sets, the tray box widened to span both, device 2's posts and boxes added.
  // schematic() puts the tray box (12 triangles = 108 numbers) first in set 1, followed by the posts.
  function schematic(spec1,v1,spec2,v2){
    const S=T().schematic(spec1,v1);if(!spec2)return S;const m=merged(v1,v2),S2=T().schematic(spec2,m),L=layout(spec1,v1,spec2,v2),z0=PO().floorZ(v1);
    S[1]={...S[1],v:[...T().box(-L.tray_w/2,0,z0,L.tray_w/2,L.tray_d,z0+3),...S[1].v.slice(108),...S2[1].v.slice(108)]};
    const extra=S2.filter((s,i)=>i>1&&s.device).map(s=>({...s,color:[110,180,230],second:true}));
    return [...S,...extra];
  }
  const api={SECOND_KEYS,GAP,REACH,values,diff,merged,footprint,layout,ports2,problems,schematic};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;
  root.TrayPair=api;
})(typeof window!=='undefined'?window:globalThis);
