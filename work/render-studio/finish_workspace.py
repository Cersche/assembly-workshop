"""Apply small renderer-only workspace changes. Never reads/writes user data."""
from pathlib import Path

path=Path(__file__).resolve().parents[2]/'outputs/Mechanical_Design_App/workspace.js'
s=path.read_text(encoding='utf-8')
s=s.replace('<button id="resetRackView" class="subtle">Perspective</button>', '<button id="resetRackView" class="subtle">Perspective</button><button id="renderQuality" class="subtle" aria-pressed="true" title="Toggle contact shading and cast shadows">Studio quality</button>')
s=s.replace('let showRackPanels=false, perspectiveCamera=true;', 'let showRackPanels=false, perspectiveCamera=true, studioQuality=true;')
start=s.index('    // Ground grid is a viewport guide')
end=s.index('    try {',start)
s=s[:start]+s[end:]
s=s.replace('    ctx.drawImage(sceneRenderer.draw', '    sceneRenderer.shadows=studioQuality&&sceneRenderer.shadowSupported;sceneRenderer.ambientOcclusion=studioQuality;\n    ctx.drawImage(sceneRenderer.draw')
start=s.index('  rackCanvas.onpointerup=')
end=s.index('rackCanvas.onpointercancel=',start)
s=s[:start]+'''  rackCanvas.onpointerup=e=>{
    if(drag&&!drag.moved){const rect=rackCanvas.getBoundingClientRect(),slot=sceneRenderer?.pick(e.clientX-rect.left,e.clientY-rect.top);if(slot)selectSlot(slot);}
    drag=null;
  };'''+s[end:]
s=s.replace("  byId('toggleRackPanels').onclick=", "  byId('renderQuality').onclick=()=>{studioQuality=!studioQuality;byId('renderQuality').setAttribute('aria-pressed',String(studioQuality));byId('renderQuality').textContent=studioQuality?'Studio quality':'Fast preview';drawSoon();};\n  byId('toggleRackPanels').onclick=")
s=s.replace("rackCanvas.dataset.triangles=String(scene.parts.reduce((n,p)=>n+sourceMeshes[p.key].triangles.length,0));", "rackCanvas.dataset.triangles=String(sceneRenderer.stats?.triangles||0);rackCanvas.dataset.quality=studioQuality?'studio':'fast';")
path.write_text(s,encoding='utf-8')
