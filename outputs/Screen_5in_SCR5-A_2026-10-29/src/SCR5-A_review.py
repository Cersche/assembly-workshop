"""Generate local review navigation and explicit assumed route evidence."""
import json
import math
from pathlib import Path


def make(b):
    route=[('screen connector, assumed',[-52,13.1,66.45]),
           ('top-left exit, assumed',[-52,18,87.5]),
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
    (b.HERE/'checks/SCR5-A-route.svg').write_text(svg,encoding='utf-8')
    out=b.ROOT/'work/mesh-viewer'
    # Local presentation only, derived from the mandated mesh_viewer output.
    assembled=(out/'SCR5-A-assembled.html').read_text(encoding='utf-8')
    for label,yaw in [('front','-Math.PI / 2'),('rear','Math.PI / 2')]:
        page=assembled.replace('frame(-Math.PI / 3, 0.55)',f'frame({yaw}, 0)')
        # Existing tool supplies Front; add a Rear preset without modifying it.
        page=page.replace('<button id="front">Front</button>','<button id="front">Front</button><button id="rear">Rear</button>')
        page=page.replace('document.getElementById("front").onclick = () => frame(-Math.PI / 2, 0);',
                          'document.getElementById("front").onclick = () => frame(-Math.PI / 2, 0);\ndocument.getElementById("rear").onclick = () => frame(Math.PI / 2, 0);')
        (out/f'SCR5-A-{label}.html').write_text(page,encoding='utf-8')
    html=f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>SCR5-A — incomplete concept review</title>
<style>body{{background:#141923;color:#e2e9f1;font:16px system-ui;margin:24px}}a{{color:#8fcaff}}.warning{{border:2px solid #e8a04c;padding:16px}}iframe{{width:100%;height:670px;border:1px solid #5c6b80}}nav a{{margin-right:20px}}img{{max-width:100%}}</style>
<h1>SCR5-A — incomplete concept review</h1><p class="warning">NOT MANUFACTURING READY. Not printed. Vendor dimensions nominal; printed fit, glass retention, access, ribbon reach and strength UNKNOWN. The insert carrier needs an unmeasured glass-to-PCB gap. Plain holes and 4.5 × 2.5 screw heads are unconfirmed assumptions. Final export is blocked. Claude/Brian review required.</p>
<nav><a href="SCR5-A-front.html" target="mesh">Front / assembly</a><a href="SCR5-A-rear.html" target="mesh">Rear / assembly</a><a href="SCR5-A-review.html" target="mesh">Separate STLs + 3MF</a><a href="SCR5-A-print.html" target="mesh">Two-object 3MF</a><a href="SCR5-A-probes.html" target="mesh">Retained probes</a></nav>
<iframe name="mesh" title="Interactive 3D mesh review" src="SCR5-A-front.html"></iframe>
<h2>Ribbon route assumptions</h2>{svg}<p>Polyline {sum(lengths):.2f} mm; +16 connector insertion +15 slack +10 bend reserve = {sum(lengths)+41:.2f} mm. These are illustrative choices, not measured allowances. 160 mm reach UNKNOWN.</p>
<p>Side hooks capture the carrier to the pocket; this is not a frame merely screwed to a loose PCB. Carrier preassembly into the glass/PCB gap and clip deflection remain unverified. Bosses overlap the assumed active keepout in front projection by 1.3045 mm (radial signed gap). No active-area clearance claim.</p>
<p>Private Artifact publishing pending in Claude. Local files are not private Artifact publication. No SendUserFile/private Artifact tool is available in this Codex host.</p></html>'''
    (out/'SCR5-A-index.html').write_text(html,encoding='utf-8')
    return data
