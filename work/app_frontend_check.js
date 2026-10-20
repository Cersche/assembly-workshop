

const token='__TOKEN__';let state;let dirty=false;let previewTimer;let previewRevision=0;let generatedBuild=null;

const $=id=>document.getElementById(id);

const labels={stack:'Stack to insert entrance (mm)',pocket:'Available pocket depth (mm)',boss_diameter:'Boss diameter (mm)',pilot:'Installation pilot (mm)',minimum_engagement:'Minimum engagement target (mm)',bottom_allowance:'Bottom clearance target (mm)'};

function text(tag,value,cls){const e=document.createElement(tag);e.textContent=value;if(cls)e.className=cls;return e}

function message(value,error=false){$('message').textContent=value;$('message').className=error?'fail':'pass'}

async function api(path,body){const response=await fetch('/api/'+path,body===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json','X-App-Token':token},body:JSON.stringify(body)});const data=await response.json();if(!response.ok)throw Error(data.error||'Request failed');return data}

function markDirty(){dirty=true;generatedBuild=null;$('downloadBuild').disabled=true;$('viewProposal').disabled=true;$('buildStatus').textContent='Inputs changed. Generate the revised meshes again.';window.dispatchEvent(new CustomEvent('assembly-model',{detail:null}));window.assemblyHardware=null;window.dispatchEvent(new CustomEvent('assembly-hardware',{detail:null}));$('dirty').textContent='Unsaved changes. Exports save your selections first.';$('resultSummary').textContent='Inputs changed. Run the checks again.';$('checks').replaceChildren();$('jointSvg').replaceChildren();$('geometryText').textContent='Updating draft preview…';previewRevision++;clearTimeout(previewTimer);previewTimer=setTimeout(()=>preview().catch(e=>{$('geometryText').textContent=e.message}),180)}

function renderParts(){const ps=WorkshopCatalog.filter(state.parts,filterCriteria());$('parts').replaceChildren();for(const p of ps){const row=document.createElement('tr');row.append(text('td',p.name+' · r'+p.revision),text('td',`M${p.diameter} × ${p.pitch}`),text('td',p.verification));const cell=document.createElement('td'),button=text('button','Inspect','secondary');button.onclick=()=>{$('partDetails').textContent=JSON.stringify(p,null,2);const a=$('sourceLink');a.hidden=true;try{const u=new URL(p.source);if(['https:','http:'].includes(u.protocol)){a.href=u.href;a.hidden=false}}catch(e){}};cell.append(button);row.append(cell);$('parts').append(row)}$('empty').textContent=ps.length?'':'No matching parts. Import documented hardware or try the labeled custom examples.'}

const filterFields=['diameter','pitch','min_length','max_length','head_style','material','installation_method'];let packInventory=[];
function filterCriteria(){const c={q:$('search').value,kind:$('kind').value,latest:$('filter-latest').checked};for(const k of filterFields)c[k]=$('filter-'+k).value;return c}
function populateFilters(){for(const k of ['head_style','material','installation_method']){const e=$('filter-'+k),old=e.value;const values=[...new Set(state.parts.map(p=>p[k]).filter(v=>typeof v==='string'&&v))].sort();e.replaceChildren(new Option('All',''),new Option('Unrecorded / unknown',WorkshopCatalog.unknown));for(const v of values)e.append(new Option(v,v));e.value=[...e.options].some(o=>o.value===old)?old:''}}
function renderReplacement(){const host=$('replacementChanges');host.replaceChildren();for(const kind of ['screw','heatset']){const selected=state.parts.find(p=>p.id+'|'+p.revision===$(kind).value),saved=state.project.selections[kind];host.append(text('h4',kind==='screw'?'Joint screw':'Heat-set insert'));if(!selected){host.append(text('p',saved?'Draft selection cleared; saved pin remains until Save.':'No hardware selected.'));continue}const changes=WorkshopCatalog.changes(saved,selected);if(!changes.length){host.append(text('p','Matches saved selection.'));continue}const table=document.createElement('table'),head=document.createElement('tr');for(const t of ['Field','Saved','Draft','Review'])head.append(text('th',t));table.append(head);for(const c of changes){const row=document.createElement('tr');for(const v of [c.field,c.before===null?'unknown':JSON.stringify(c.before),c.after===null?'unknown':JSON.stringify(c.after),c.effect])row.append(text('td',v));table.append(row)}host.append(table)}}
async function loadPacks(){const data=await api('catalog-packs');packInventory=data.packs;$('catalogPack').replaceChildren(...packInventory.map(p=>new Option(p.id+(p.available?' · '+p.records.length+' records':' · unavailable'),p.id)));$('sourceGaps').textContent=data.gaps.error?'Gap evidence unavailable: '+data.gaps.error:(data.gaps.gaps||[]).map(g=>'M'+g.size+' '+g.kind+' · '+g.state+': '+g.finding).join('\n');updatePackStatus()}
function updatePackStatus(){const p=packInventory.find(p=>p.id===$('catalogPack').value);$('importPack').disabled=!p?.available;$('packStatus').textContent=p?.available?'SHA-256 verified. '+p.records.length+' records ready for explicit import. No models bundled.':p?.error||'No local pack available.'}

function render(){state.coverage.forEach(c=>$('coverage').append(text('span',`M${c.size} · ${c.screws} S / ${c.heatsets} I`)));$('count').textContent=state.parts.length+' part revisions';for(const kind of ['screw','heatset']){const selected=state.project.selections[kind];$(kind).replaceChildren(new Option('Choose a part…',''));state.parts.filter(p=>p.kind===kind).forEach(p=>$(kind).append(new Option(p.name+' · r'+p.revision,p.id+'|'+p.revision)));if(selected)$(kind).value=selected.id+'|'+selected.revision}for(const [key,label] of Object.entries(labels)){const div=document.createElement('div'),l=text('label',label),input=document.createElement('input');input.id=key;input.type='number';input.min=0;input.step='any';input.value=state.project.inputs[key];l.htmlFor=key;input.oninput=markDirty;div.append(l,input);$('inputs').append(div)}populateFilters();renderParts();renderReplacement();preview().catch(e=>{$('geometryText').textContent=e.message})}

async function refresh(){state=await api('state');$('coverage').replaceChildren();$('inputs').replaceChildren();render()}

function payload(){const selections={};for(const kind of ['screw','heatset']){const val=$(kind).value;if(val){const p=state.parts.find(p=>p.id+'|'+p.revision===val);selections[kind]={id:p.id,revision:p.revision}}}const inputs={};for(const key of Object.keys(labels)){if($(key).value.trim()==='')throw Error('Fill every joint dimension.');inputs[key]=Number($(key).value)}return {selections,inputs}}

async function save(){state.project=await api('save',payload());dirty=false;$('dirty').textContent='Saved locally. Part revisions are pinned.';renderReplacement()}

async function safe(fn){try{await fn()}catch(e){message(e.message,true)}}

$('search').oninput=renderParts;$('kind').onchange=renderParts;['screw','heatset'].forEach(k=>$(k).onchange=()=>{markDirty();renderReplacement()});for(const k of filterFields)$('filter-'+k).oninput=renderParts;$('filter-latest').onchange=renderParts;
$('clearFilters').onclick=()=>{for(const k of filterFields)$('filter-'+k).value='';$('search').value='';$('kind').value='';$('filter-latest').checked=true;renderParts()};
$('catalogPack').onchange=updatePackStatus;
$('importPack').onclick=()=>safe(async()=>{if(dirty)throw Error('Save your project changes before importing a pack.');const p=packInventory.find(p=>p.id===$('catalogPack').value);if(!p?.available)throw Error('Choose a verified available pack.');await api('import',p.records);await refresh();message(p.id+' imported. Saved selections were preserved.');});

$('save').onclick=()=>safe(async()=>{await save();message('Project saved locally.')});

$('check').onclick=()=>safe(async()=>{await save();const r=await api('check',{});$('resultSummary').textContent=r.status==='fail'?'A dimensional check failed. Review the details below.':'Dimensional review incomplete: resolve the unknowns below.';$('checks').replaceChildren();for(const c of r.checks){const d=text('div','','check');d.append(text('strong',c.status.toUpperCase()+' · '+c.name,c.status),text('p',c.detail));$('checks').append(d)}await preview();message('Checks completed for the saved project.')});

$('import').onclick=()=>safe(async()=>{if(dirty)throw Error('Save your project changes before importing parts.');await api('import',JSON.parse($('json').value));await refresh();message('Hardware records imported. Existing project selections were preserved.')});

$('file').onchange=()=>safe(async()=>{if($('file').files[0])$('json').value=await $('file').files[0].text()});

$('example').onclick=()=>{$('json').value=JSON.stringify([

{id:'example-m3-screw',revision:1,name:'EXAMPLE ONLY · M3 × 6 screw',kind:'screw',diameter:3,pitch:.5,length:6,threaded_length:6,length_convention:'under_head',verification:'custom',source:'Fictional workflow example; replace with actual hardware.'},

{id:'example-m3-insert',revision:1,name:'EXAMPLE ONLY · M3 insert',kind:'heatset',diameter:3,pitch:.5,length:5,outside_diameter:4.6,hole_diameter:4.2,hole_profile:'straight',usable_depth:4.5,min_wall:2,end_type:'open',verification:'custom',source:'Fictional workflow example; not manufacturer guidance.'}

],null,2);message('Custom examples shown. Review, then import them if you want to try the workflow.')};

async function download(path,name){await save();const response=await fetch('/api/'+path);if(!response.ok)throw Error('Export failed');const blob=await response.blob();const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}



function showModel(assembly){window.dispatchEvent(new CustomEvent('assembly-model',{detail:assembly}))}

$('viewBaseline').onclick=()=>{showModel(null);$('buildStatus').textContent='Showing baseline clearance v2.'};

$('viewProposal').onclick=()=>{if(generatedBuild){showModel(generatedBuild.assembly);$('buildStatus').textContent='Showing '+generatedBuild.assembly.revision}};

$('buildRevision').onclick=()=>safe(async()=>{const draft=payload(),snapshot=JSON.stringify(draft);$('buildRevision').disabled=true;$('buildStatus').textContent='Rendering tray and faceplate with OpenSCAD…';try{const result=await api('build',draft);if(JSON.stringify(payload())!==snapshot){$('buildStatus').textContent='Render completed for older inputs. Generate again for current inputs.';return}generatedBuild=result;$('viewProposal').disabled=false;$('downloadBuild').disabled=false;showModel(result.assembly);$('buildStatus').textContent=`Showing ${result.assembly.revision}. Both meshes passed STL integrity checks. Scale: millimeters. Physical fit remains unvalidated.${result.cached?' Reused matching cached render.':''}`;}catch(e){$('buildStatus').textContent=e.message;throw e}finally{$('buildRevision').disabled=false}});

$('downloadBuild').onclick=()=>safe(async()=>{if(!generatedBuild)throw Error('Generate the current revision first.');const response=await fetch('/api/build-bundle',{method:'POST',headers:{'Content-Type':'application/json','X-App-Token':token},body:JSON.stringify({id:generatedBuild.id})});if(!response.ok){const e=await response.json();throw Error(e.error)}const url=URL.createObjectURL(await response.blob()),a=document.createElement('a');a.href=url;a.download='pi4-rendered-revision-'+generatedBuild.id.slice(0,8)+'.zip';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)});



$('designExport').onclick=()=>safe(async()=>{const response=await fetch('/api/design',{method:'POST',headers:{'Content-Type':'application/json','X-App-Token':token},body:JSON.stringify(payload())});if(!response.ok){const error=await response.json();$('designStatus').textContent=error.error;throw Error(error.error)}const url=URL.createObjectURL(await response.blob()),a=document.createElement('a');a.href=url;a.download='pi4-proposed-joint.zip';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);$('designStatus').textContent='Exported an unvalidated proposal and hardware/check report. Baseline files and saved selections were not changed.'});

$('bom').onclick=()=>safe(()=>download('bom','pi4-beta-bom.csv'));$('project').onclick=()=>safe(()=>download('project','pi4-beta-project.json'));



async function preview(){const revision=++previewRevision;const g=await api('preview',payload());if(revision!==previewRevision)return;window.assemblyHardware=g;window.dispatchEvent(new CustomEvent('assembly-hardware',{detail:g}));const svg=$('jointSvg');svg.replaceChildren();const max=Math.max(g.bore_end,g.screw_tip||0,g.insert_end||0,1);const x=v=>30+450*v/max;function el(tag,attrs,label){const e=document.createElementNS('http://www.w3.org/2000/svg',tag);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,v);if(label!==undefined)e.textContent=label;svg.append(e)}function bar(a,b,y,color,label){el('rect',{x:x(a),y,width:Math.max(1,x(b)-x(a)),height:14,fill:color,rx:3});el('text',{x:30,y:y-6,'font-size':12,fill:'#334c40'},label)}bar(g.insert_entrance,g.bore_end,105,'#d7e4dc','Modeled bore');if(g.insert_end!==null)bar(g.insert_entrance,g.insert_end,65,'#ca9d43','Insert body length');if(g.screw_tip!==null)bar(0,g.screw_tip,25,'#3b7565','Screw under-head length');for(const v of [0,g.insert_entrance,g.bore_end]){el('line',{x1:x(v),x2:x(v),y1:120,y2:130,stroke:'#6b8076'});el('text',{x:x(v),y:148,'text-anchor':'middle','font-size':11},v.toFixed(2))}$('geometryText').textContent=g.screw_tip===null?'Select an under-head-length screw to calculate reach. Preview uses current inputs; save to persist them.':`Reach ${g.reach.toFixed(2)} mm · tip beyond insert body ${g.tip_beyond_insert===null?'unknown':g.tip_beyond_insert.toFixed(2)+' mm'} · modeled bore-end gap ${g.tip_to_bore_end.toFixed(2)} mm. ${dirty?'Draft preview — unsaved changes.':'Saved project dimensions.'}`}

$('geometryDownload').onclick=()=>safe(()=>download('geometry','pi4-joint-geometry.json'));



window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue=''}});safe(async()=>{await refresh();await loadPacks()});

