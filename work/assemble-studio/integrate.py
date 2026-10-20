"""Connect the exact inspection meshes to studio rendering; no data writes or builds."""
from pathlib import Path
import hashlib
import json
root=Path(__file__).resolve().parents[2]
app=root/'outputs/Mechanical_Design_App'
p=app/'viewer.js';s=p.read_text(encoding='utf-8')
def replace(old,new):
    global s
    assert s.count(old)==1,old[:90]
    s=s.replace(old,new)
replace("  let selectedPart=null,pickBuffer=null,pickParts=[];", """  let selectedPart=null,pickBuffer=null,pickParts=[],hardwareMeshes=null;
  let studioRenderer=null,studioUnavailable='';
  function createStudioRenderer(){
    try{if(window.LabRaxAssembly){studioRenderer=new window.LabRaxAssembly.AssemblyRenderer();studioRenderer.invalidated=schedule;studioUnavailable='';}}
    catch(e){studioUnavailable=e.message;studioRenderer=null;}
  }
  createStudioRenderer();""")
replace("window.addEventListener('assembly-hardware',e=>{hardware=e.detail;schedule()});", "window.addEventListener('assembly-hardware',e=>{hardware=e.detail;hardwareMeshes=null;schedule()});")
replace("function transform(v){const p=camera(v);return [p[0]-centerX,p[1]-centerY,p[2]]}", "let studioView=null;\n    function transform(v){if(studioView){const p=studioView.project(v);return [p[0]-w/2,h/2-p[1],p[2]];}const p=camera(v);return [p[0]-centerX,p[1]-centerY,p[2]]}")
replace("if(showHardware&&hardware)parts.push(...hardware.hardware_envelopes.map(cylinder));", "if(showHardware&&hardware){if(!hardwareMeshes)hardwareMeshes=hardware.hardware_envelopes.map(cylinder);parts.push(...hardwareMeshes);}")
replace("    for(const part of parts){const vs=part.vertices.map(transform);", """    let usedStudio=false,renderedTriangles=0;
    if(studioRenderer){
      try{
        if(studioRenderer.restoreRequired){studioRenderer.dispose();createStudioRenderer();}
        const result=studioRenderer.render({parts,fullParts:model.parts,yaw,pitch,zoom,focus,frontMode,appearance,selectedPart,width:w,height:h,dpr});
        studioView=result.view;scale=1;ctx.drawImage(result.canvas,0,0,w,h);renderedTriangles=result.triangles;usedStudio=true;
      }catch(e){studioUnavailable=e.message;if(!studioRenderer?.lost){studioRenderer?.dispose();studioRenderer=null;}}
    }
    if(!usedStudio){
    for(const part of parts){const vs=part.vertices.map(transform);""")
replace("    ctx.putImageData(frame,0,0);", "    ctx.putImageData(frame,0,0);renderedTriangles=faces.length;\n    }")
replace("    canvas.dataset.artwork=texture?'preview-only':'none';", "    canvas.dataset.renderer=usedStudio?'webgl':'software';\n    canvas.dataset.artwork=texture?'preview-only':'none';")
replace("status.textContent=faces.length.toLocaleString()+' visible triangles", "status.textContent=renderedTriangles.toLocaleString()+' visible triangles")
replace("    status.textContent+=(selectedPart?", "    status.textContent+=usedStudio?' · Studio lighting / shadows / contact shading.':studioUnavailable?' · Software fallback: '+studioUnavailable+'.':'';\n    status.textContent+=(selectedPart?")
replace("canvas.onpointerup=e=>{if(drag&&!drag.moved&&pickBuffer){const rect=canvas.getBoundingClientRect(),x=Math.floor((e.clientX-rect.left)*canvas.width/rect.width),y=Math.floor((e.clientY-rect.top)*canvas.height/rect.height);selectedPart=x>=0&&x<canvas.width&&y>=0&&y<canvas.height?pickParts[pickBuffer[y*canvas.width+x]]||null:null;schedule();}drag=null};", """canvas.onpointerup=e=>{if(drag&&!drag.moved){const rect=canvas.getBoundingClientRect();
    if(canvas.dataset.renderer==='webgl')selectedPart=studioRenderer.pickPart((e.clientX-rect.left)*wRatio(rect),(e.clientY-rect.top)*420/rect.height);
    else if(pickBuffer){const x=Math.floor((e.clientX-rect.left)*canvas.width/rect.width),y=Math.floor((e.clientY-rect.top)*canvas.height/rect.height);selectedPart=x>=0&&x<canvas.width&&y>=0&&y<canvas.height?pickParts[pickBuffer[y*canvas.width+x]]||null:null;}
    schedule();}drag=null};
  function wRatio(rect){return (canvas.clientWidth||800)/rect.width;}""")
p.write_text(s,encoding='utf-8')
p=app/'index.html';s=p.read_text(encoding='utf-8')
old='<script src="/rack-references/rack-studio.js"></script>'
assert s.count(old)==1
s=s.replace(old,old+'<script src="/rack-references/assembly-studio.js"></script>')
p.write_text(s,encoding='utf-8')
manifest=app/'rack-references/asset-manifest.json'
entries=json.loads(manifest.read_text(encoding='utf-8'))
for name in ['rack-studio.js','assembly-studio.js']:
    entry=next((e for e in entries if e['file']==name),None)
    if entry is None:entry={'url':'/rack-references/'+name,'file':name,'mime':'text/javascript'};entries.append(entry)
    entry['sha256']=hashlib.sha256((app/'rack-references'/name).read_bytes()).hexdigest()
manifest.write_text(json.dumps(entries,indent=2)+'\n',encoding='utf-8')
data=root/'data/normal-use'
(Path(__file__).parent/'Data_Before.json').write_text(json.dumps({str(p.relative_to(data)):hashlib.sha256(p.read_bytes()).hexdigest() for p in data.rglob('*') if p.is_file()},indent=2),encoding='utf-8')
print('Studio inspection integration complete. No user data or manufacturing meshes changed.')
