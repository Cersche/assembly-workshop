"""Complete the staged GUI reconstruction, then carry over only the new renderer integration."""
from pathlib import Path
import hashlib
import json

root=Path(__file__).resolve().parents[2]
stage=root/'work/gui-render-repair/stage/outputs/Mechanical_Design_App'
app=root/'outputs/Mechanical_Design_App'
p=stage/'workspace.js';s=p.read_text(encoding='utf-8')
# Restore the save-race fixes covered by the preserved final acceptance harness.
s=s.replace("    const snapshot=JSON.stringify(documentState),identity=window.workshopContext?.id,hardware=identity?payload():null;\n    try{", "    try{\n      const snapshot=JSON.stringify(documentState),identity=window.workshopContext?.id,hardware=identity?payload():null;")
s=s.replace("      const newerLayout=JSON.stringify(documentState)!==snapshot,newerHardware=hardware&&JSON.stringify(payload())!==JSON.stringify(hardware);", "      const newerLayout=JSON.stringify(documentState)!==snapshot;\n      let newerHardware=false;\n      if(hardware){try{newerHardware=JSON.stringify(payload())!==JSON.stringify(hardware);}catch(e){newerHardware=true;}}")
s=s.replace('        renderReplacement();',"        renderReplacement();if(typeof preview==='function'&&typeof safe==='function')safe(preview);")
# Current user-defined coordinate convention: Slot 01 is at the top.
s=s.replace('for(let s=rack.slots;s>=1;s--)','for(let s=1;s<=rack.slots;s++)')
old=s.index('  // Actual source components in recovered visual poses')
end=s.index('  Promise.all([api(\'workspace-capabilities\')',old)
renderer=(app/'workspace.js').read_text(encoding='utf-8')
ra=renderer.index('  // Actual source components in recovered visual poses')
rb=renderer.index("  api('rack-workspace')",ra)
s=s[:old]+renderer[ra:rb]+s[end:]
s=s.replace('<button id="resetRackView" class="subtle">Perspective</button>','<button id="resetRackView" class="subtle">Perspective</button><button id="renderQuality" class="subtle" aria-pressed="true" title="Toggle contact shading and cast shadows">Studio quality</button>')
# The current renderer must redraw while appearance drafts change.
s=s.replace("function markChanged(){layoutDirty=true;updateSaveStatus();}","function markChanged(){layoutDirty=true;updateSaveStatus();drawSoon();}")
p.write_text(s,encoding='utf-8')
p=stage/'index.html';s=p.read_text(encoding='utf-8')
s=s.replace('href="/workspace.css?v=4"','href="/workspace.css?v=render-hybrid-1"')
s=s.replace('<script src="/rack-references/rack-layout.js">','<script src="/rack-references/rack-studio.js"></script><script src="/rack-references/rack-layout.js">')
p.write_text(s,encoding='utf-8')
print('Staged hybrid GUI + current renderer. Live sources and user data are not changed.')
