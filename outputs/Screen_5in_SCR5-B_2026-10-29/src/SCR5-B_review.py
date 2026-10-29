"""Generate local review navigation and explicit assumed route evidence."""
import json
import math
from pathlib import Path


def make(b,doc):
    p=doc['values']
    route=[('screen connector, assumed',[p['ribbon_x'],p['seat_y']+p['total_depth']+.5,p['centre_z']+22]),
           ('top-left exit, assumed',[p['ribbon_x'],18,87.5]),
           ('lateral transition, assumed',[-74,25,90]),
           ('U5 floor slot underside',[-74,91,97.125]),
           ('U5 floor slot top',[-74,91,100.125]),
           ('Pi connector, assumed',[-74,81,110.4])]
    lengths=[math.dist(a[1],c[1]) for a,c in zip(route,route[1:])]
    data={'status':'planning assumptions, NOT a checked cable route',
          'coordinate_frame':'screen local; rack global Z=local+88.90; U5 local Z=screen local Z-88.90; common plate rear Y=0',
          'slot_source':'outputs/Hue_Pi4_M6-B_2026-10-28/src/HP4-M6-B.scad dsi_slot_cut; read only, no reference mesh opened',
          'floor_z_derivation':'U5 tray_z=7+1.225=8.225, tray_t=3; screen-local floor 97.125..100.125',
          'slot_x':[-86,-62],'slot_y':[87,95], 'u5_start_screen_local_z':88.90,
          'waypoints':[{'label':name,'xyz':p} for name,p in route],
          'segment_lengths_mm':lengths,'polyline_length_mm':sum(lengths),
          'assumed_extra_connector_insertion_mm':16,'assumed_slack_mm':15,'assumed_bend_reserve_mm':10,
          'illustrative_total_mm':sum(lengths)+41,
          '160mm_reach':'UNKNOWN; illustrative reserved path exceeds 160, coordinates/insertion/bends unmeasured',
          'obstructions':'Actual component obstacles, connector contact orientation, tool/finger access and bend sweeps UNKNOWN'}
    b.dump(b.CHECKS/'ribbon-route.json',data)
    def poly(axes,scale,offset):
        return ' '.join(f'{offset[0]+p[axes[0]]*scale},{offset[1]-p[axes[1]]*scale}' for _,p in route)
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="400" viewBox="0 0 1000 400" role="img" aria-label="Assumed ribbon route: front X Z and side Y Z projections">
<rect width="1000" height="400" fill="#171e29"/><g fill="#e6edf5" font-family="sans-serif" font-size="15">
<text x="24" y="26">ASSUMED ROUTE — reach / bend room UNKNOWN</text>
<text x="24" y="55">Front projection X/Z (left is negative X)</text><text x="525" y="55">Side projection Y/Z (rearward is positive Y)</text>
<text x="24" y="375">No reference mesh, screen hardware or ribbon is included in the manufacturing objects.</text></g>
<g fill="none" stroke-width="2"><path d="M30 310H470 M525 310H960" stroke="#65768d"/>
<path d="M30 135H470 M525 135H960" stroke="#65768d" stroke-dasharray="5 5"/>
<polyline points="{poly((0,2),2.5,(360,360))}" stroke="#ffbd68"/>
<polyline points="{poly((1,2),2.5,(570,360))}" stroke="#ffbd68"/>
</g><g fill="#b8c5d7" font-size="13" font-family="sans-serif"><text x="290" y="130">U5 starts Z=88.90</text>
<text x="545" y="90">Slot Y=87..95, Z=97.125..100.125</text>
<text x="30" y="340">X shifts -52 → -74; Y shifts 13.1 → 91 → 81</text></g></svg>'''
    (b.HERE/'checks/SCR5-B-route.svg').write_text(svg,encoding='utf-8')
    import subprocess,sys
    out=b.ROOT/'work/mesh-viewer';out.mkdir(exist_ok=True)
    plate=b.HERE/'SCR5-B_plate.stl';frame=b.HERE/'SCR5-B_frame.stl';package=b.HERE/'SCR5-B_screen_plate_and_frame.3mf'
    screen=b.CHECKS/'SCR5-B_nominal-screen-envelope.stl'
    old=b.ROOT/'outputs/Screen_5in_SCR5-A_2026-10-29/SCR5-A_plate.stl'
    commands=[([plate,frame,package],'review','Separate parts and final print 3MF',False),
              ([plate,frame,screen],'assembled','Assembly: screen envelope is PREVIEW ONLY',True),
              ([package],'print','Two-object 3MF load proof',False),
              (sorted(b.CHECKS.glob('*.stl')),'probes','All retained contact and engraving probes',False),
              ([old,plate],'preservation','SCR5-A / SCR5-B plate comparison, read-only original',False)]
    for files,name,title,as_is in commands:
        subprocess.run([sys.executable,str(b.ROOT/'tools/mesh_viewer.py'),*[str(f) for f in files],*(['--as-is'] if as_is else []),'-o',str(out/f'SCR5-B-{name}.html'),'-t','SCR5-B — '+title],check=True)
    assembled=(out/'SCR5-B-assembled.html').read_text(encoding='utf-8')
    for label,yaw in [('front','-Math.PI / 2'),('rear','Math.PI / 2')]:
        page=assembled.replace('frame(-Math.PI / 3, 0.55)',f'frame({yaw}, 0)')
        page=page.replace('<button id="front">Front</button>','<button id="front">Front</button><button id="rear">Rear</button>')
        page=page.replace('document.getElementById("front").onclick = () => frame(-Math.PI / 2, 0);','document.getElementById("front").onclick = () => frame(-Math.PI / 2, 0);\ndocument.getElementById("rear").onclick = () => frame(Math.PI / 2, 0);')
        (out/f'SCR5-B-{label}.html').write_text(page,encoding='utf-8')
    hub=f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>SCR5-B review</title>
<style>body{{background:#141923;color:#e2e9f1;font:16px system-ui;margin:24px}}a{{color:#8fcaff}}iframe{{width:100%;height:700px}}nav a{{margin-right:20px}}svg{{max-width:100%}}</style>
<h1>SCR5-B — plate-anchored rear clamp</h1><p>Digital gate PASS. NOT PRINTED. Vendor nominal; fit, preload, retention, contact lands, button access, ribbon reach and strength UNKNOWN. Screen box is a preview envelope; only plate and frame are in the delivery 3MF.</p>
<nav><a href="SCR5-B-front.html" target="mesh">Front</a><a href="SCR5-B-rear.html" target="mesh">Rear</a><a href="SCR5-B-assembled.html" target="mesh">Assembly</a><a href="SCR5-B-review.html" target="mesh">Separate parts</a><a href="SCR5-B-print.html" target="mesh">3MF</a><a href="SCR5-B-probes.html" target="mesh">Checks</a></nav><iframe name="mesh" src="SCR5-B-rear.html" title="Interactive 3D review"></iframe>
<p>Four plate bosses at X ±{p['boss_x']}, Z {p['boss_z']}; screws never enter screen holes. Edge pads at X ±{p['pad_x']}, Z {p['centre_z']-p['pad_z_offset']:.2f}/{p['centre_z']+p['pad_z_offset']:.2f}; preload {p['preload']} mm is a tunable assumption. Remove frame to load screen from rear; no glass/PCB interspace access.</p>
{svg}<p>Illustrative route {sum(lengths):.2f} +41 reserve = {sum(lengths)+41:.2f} mm. 160 mm reach UNKNOWN.</p>
<p>Private Artifact publishing pending in Claude. Local viewer is not publication.</p></html>'''
    (out/'SCR5-B-index.html').write_text(hub,encoding='utf-8')
    b.dump(b.CHECKS/'viewers.json',{'pages':[f'SCR5-B-{name}.html' for name in ('index','review','assembled','front','rear','print','probes','preservation')],'load':'both delivered STLs, final 3MF, all retained probe STLs and original comparison plate parsed by mesh_viewer.py','interactive_visual_review':'not performed; no desktop control session','SendUserFile':'not available in this host','private_artifact':'private Artifact publishing pending in Claude'})
    return data
