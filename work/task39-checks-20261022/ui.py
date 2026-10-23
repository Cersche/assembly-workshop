from pathlib import Path
p=Path('outputs/Mechanical_Design_App');f=p/'equipment-wizard.js';t=f.read_text(encoding='utf-8')
insert='''  function drivePreset(){return {name:'Drives (3.5" + 2.5")',dev_w:179.45,dev_d:147,dev_h:29.1,u:1,hole_d:2.7,standoff:0,insert_pilot:3.2,board_t:1.6,device_mount:'flat',joint:'screw',holes:[],feet:[],ports:[],rear_ports:[],keystones:[],drives:[['3.5',-89.725,0],['2.5',19.875,0]],drive_mount:'screws',ssd_h:7};}
  window.driveTrayPreset=drivePreset;
'''
t=t.replace('  function reset(){',insert+'  function reset(){',1)
t=t.replace("    if(step===0){\n",'''    if(spec.drives?.length && step<3){
      const generic=h('button',{type:'button'},'Use generic equipment');generic.onclick=()=>{reset();render();};
      return [h('b',{},'Drives (3.5" + 2.5") — blank 1U faceplate'),
        h('label',{class:'ew-field'},'Drive mounting',select({screws:'Bottom screws (default)',sleeve:'Tool-free sleeve (experimental)'},spec.drive_mount,v=>{spec.drive_mount=v;render();})),
        h('label',{class:'ew-field'},'SSD height',select({'7':'7 mm','9.5':'9.5 mm'},String(spec.ssd_h),v=>{spec.ssd_h=Number(v);render();})),
        h('p',{},spec.drive_mount==='screws'?'Drive hardware: 4 × 6-32 × 1/4 inch + 4 × M3 × 4 mm. Use four of the six HDD holes matching your drive.':'Drive retention hardware: none. Rack/faceplate joint hardware remains required.'),
        h('p',{class:'ew-note'},'195.45 mm tray width; 184 mm depth includes 25 mm behind the HDD for SATA/power. Connectors face rear. Standard-derived positions; 7 mm SSD bottom holes are optional.'),
        h('p',{class:'ew-note ew-warn'},'PROPOSED — UNVALIDATED. Fit, peg retention, tab fatigue, vibration, airflow, strength and usable depth UNKNOWN. Confirm actual holes, screw heads and thread engagement.'),generic];
    }
    if(step===0){
''',1)
t=t.replace("      return [h('label',{class:'ew-field'},'Name',name),...imp,", "      const drives=h('button',{type:'button'},'Drives (3.5\\\" + 2.5\\\")');drives.onclick=()=>{reset();spec=drivePreset();render();};\n      return [drives,h('label',{class:'ew-field'},'Name',name),...imp,")
t=t.replace("h('label',{class:'ew-field'},'Tray default mount',mount)","...(spec.drives?.length?[]:[h('label',{class:'ew-field'},'Tray default mount',mount)])")
f.write_text(t,encoding='utf-8',newline='\n')
