"""Narrow source integration; no application data or manufacturing builds."""
from pathlib import Path
import json
import hashlib

root=Path(__file__).resolve().parents[2]/'outputs/Mechanical_Design_App'
path=root/'workspace.js'
s=path.read_text(encoding='utf-8')
start=s.index('                                                            // Track B:')
end=s.index("      const label=project",start)
s=s[:start]+s[end:]
s=s.replace('let showRackPanels=false;', 'let showRackPanels=false, perspectiveCamera=true;')
s=s.replace('view=LabRaxScene.camera(box,yaw,pitch,w,h,zoom)', 'view=LabRaxStudio.camera(box,yaw,pitch,w,h,zoom,perspectiveCamera)')
s=s.replace('sceneRenderer.draw(scene,sourceMeshes,view,Math.round(w*dpr),Math.round(h*dpr))','sceneRenderer.draw(scene,sourceMeshes,view,Math.round(w*dpr),Math.round(h*dpr),rack)')
s=s.replace("    ctx.drawImage(sceneRenderer.draw", "    try {\n    if(sceneRenderer.restoreRequired){sceneRenderer.dispose();sceneRenderer=new LabRaxStudio.Renderer();sceneRenderer.invalidated=drawSoon;}\n    ctx.drawImage(sceneRenderer.draw")
s=s.replace(')),0,0,w,h);\n    for(let slot', ')),0,0,w,h);\n    } catch(e) {sourceError=e.message;ctx.fillStyle=\'#efb6a5\';ctx.fillText(sourceError,24,36);return;}\n    for(let slot')
# draw call ends in rack), not a second closing parenthesis.
s=s.replace('),rack),0,0,w,h);\n    for(let slot', '),rack),0,0,w,h);\n    } catch(e) {sourceError=e.message;ctx.fillStyle=\'#efb6a5\';ctx.fillText(sourceError,24,36);return;}\n    for(let slot')
s=s.replace("byId('rackScale').textContent='Supplied meshes · placement / fit unverified';", "byId('rackScale').textContent=(perspectiveCamera?'Perspective':'Orthographic')+' · depth-tested · '+(sceneRenderer.stats?.triangles||0).toLocaleString()+' triangles';")
s=s.replace('sceneRenderer=new LabRaxScene.Renderer();', 'sceneRenderer=new LabRaxStudio.Renderer();sceneRenderer.invalidated=drawSoon;')
s=s.replace("onclick=()=>{yaw=0;pitch=0;zoom=1;drawSoon();}", "onclick=()=>{perspectiveCamera=false;yaw=0;pitch=0;zoom=1;drawSoon();}")
s=s.replace("onclick=()=>{yaw=-.48;pitch=.24;zoom=1;drawSoon();}", "onclick=()=>{perspectiveCamera=true;yaw=-.48;pitch=.24;zoom=1;drawSoon();}")
path.write_text(s,encoding='utf-8')
path=root/'index.html'
s=path.read_text(encoding='utf-8').replace('<script src="/rack-references/rack-layout.js">','<script src="/rack-references/rack-studio.js"></script><script src="/rack-references/rack-layout.js">')
path.write_text(s,encoding='utf-8')
manifest=root/'rack-references/asset-manifest.json'
entries=json.loads(manifest.read_text(encoding='utf-8'))
name='rack-studio.js'
entries=[e for e in entries if e['file']!=name]
entries.append({'url':'/rack-references/'+name,'file':name,'mime':'text/javascript','sha256':hashlib.sha256((root/'rack-references'/name).read_bytes()).hexdigest()})
manifest.write_text(json.dumps(entries,indent=2)+'\n',encoding='utf-8')
print('Integrated preview renderer; original rack-scene.js unchanged.')
