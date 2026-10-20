from pathlib import Path
import hashlib,json
root=Path('outputs/Mechanical_Design_App')
p=root/'index.html';s=p.read_text(encoding='utf-8')
s=s.replace('<h2 style="margin-top:12px">Lab Rax · Pi4 beta</h2>','<h2 id="assemblyProjectName" style="margin-top:12px">Lab Rax · Pi4 beta</h2>')
s=s.replace('let generatedBuild=null;','let generatedBuild=null;let projectBusy=false;')
s=s.replace("async function safe(fn){try{await fn()}catch(e){message(e.message,true)}}", "async function safe(fn){if(projectBusy)return;projectBusy=true;try{await fn()}catch(e){message(e.message,true)}finally{projectBusy=false}}")
# Protect an edit made while a save is in flight, and preserve matching mesh identity.
start=s.index('async function save(){');end=s.index('\n',start)
s=s[:start]+"async function save(){const draft=payload(),snapshot=JSON.stringify(draft),saved=await api('save',draft);state.project=saved;if(JSON.stringify({...payload(),instance_revision:draft.instance_revision})===snapshot){dirty=false;$('dirty').textContent='Saved locally. Part revisions are pinned.';}else{$('dirty').textContent='Saved earlier inputs; newer hardware edits remain unsaved.';}generatedBuild=null;$('downloadBuild').disabled=true;$('viewProposal').disabled=true;renderReplacement();if(saved.instance_id)window.dispatchEvent(new CustomEvent('assembly-project-saved',{detail:saved}))}"+s[end:]
p.write_text(s,encoding='utf-8')
p=root/'workspace.js';s=p.read_text(encoding='utf-8').replace('if(openingAssembly||savingLayout){','if(openingAssembly||savingLayout||projectBusy){')
s=s.replace("const box=anchor.getBoundingClientRect();", "anchor=byId('rackTree').querySelector('[aria-label=\"More actions for slot '+slot+'\"]')||anchor;const box=anchor.getBoundingClientRect();")
# Selecting a new rack or slot cannot discard an open hardware draft or ongoing save.
s=s.replace("function startWizard(){const rack=active();", "function startWizard(){if(!capable){notify('Wait for the updated workspace to load.',true);return;}const rack=active();")
# Keep private artwork previews scoped to the currently opened instance.
s=s.replace("function applyAssemblyAppearance(p){window.dispatchEvent", "function applyAssemblyAppearance(p){if(window.workshopContext?.id!==p?.assembly.id)return;window.dispatchEvent")
p.write_text(s,encoding='utf-8')
p=root/'rack-references/asset-manifest.json';items=json.loads(p.read_text(encoding='utf-8'))
for item in items:
    if item['file']=='rack-scene.js': item['sha256']=hashlib.sha256((root/'rack-references/rack-scene.js').read_bytes()).hexdigest()
p.write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
