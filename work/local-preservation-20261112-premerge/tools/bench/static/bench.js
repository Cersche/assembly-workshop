'use strict';
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let state, selected, revision, dirty = false, preview = null, newHashes = null;
function message(text, error = false) { $('#message').textContent = text; $('#message').className = error ? 'error' : ''; }
async function api(path, method = 'GET', body) {
  const response = await fetch(path, {method, headers: method === 'GET' ? {} : {'Content-Type':'application/json','X-Bench-Token':state?.token || ''}, body:body === undefined ? undefined : JSON.stringify(body)});
  const value = await response.json();
  if (!response.ok) throw new Error(value.error || `Request failed (${response.status}).`);
  return value;
}
const options = (values, value) => values.map(v => `<option value="${esc(v)}" ${v === value ? 'selected' : ''}>${esc(v)}</option>`).join('');
function drawList() {
  const term = $('#search').value.trim().toLowerCase(), filter = $('#filter').value;
  const shown = state.projects.filter(p => (!filter || p.status === filter) && [p.title,...p.prefixes,...p.revisions.map(r => r.id)].some(t => t.toLowerCase().includes(term)));
  $('#project-count').textContent = `${shown.length} of ${state.projects.length} projects`;
  $('#projects').innerHTML = shown.map(p => `<button class="project" data-project="${esc(p.id)}" aria-current="${p.id === selected}"><strong>${esc(p.title)}</strong><span>${esc(p.status)} · ${p.revisions.length} revisions</span></button>`).join('') || '<p>No projects match. Try another search or status.</p>';
  $('#attention-count').textContent = state.attention.length;
  $('#attention-list').innerHTML = state.attention.map(a => `<button data-project="${esc(a.project)}">${esc(a.text)}</button>`).join('') || '<p>No attention items found.</p>';
}
function docLink(path, label) { return `<a href="/text?path=${encodeURIComponent(path)}" target="_blank" rel="noopener">${esc(label || path)}</a>`; }
function project() { return state.projects.find(p => p.id === selected); }
function drawProject() {
  const p = project(); if (!p) return;
  revision = p.revisions.some(r => r.id === revision) ? revision : p.revisions[0]?.id;
  const warnings = state.errors.length ? `<details><summary class="warning">${state.errors.length} files could not be read</summary><ul>${state.errors.map(e => `<li>${esc(e)}</li>`).join('')}</ul></details>` : '';
  $('#main').innerHTML = `<div class="heading"><div><p class="eyebrow">${esc(p.prefixes.join(' / ') || 'NO REVISION PREFIX YET')}</p><h2>${esc(p.title)}</h2></div><span class="badge">${esc(p.status)}</span></div>
    <ol class="step-strip" aria-label="Project workflow">${['Measure','Draft','Print','Report'].map(s => `<li class="${p.step === s ? 'current' : ''}" ${p.step === s ? 'aria-current="step"' : ''}>${s}</li>`).join('')}</ol>
    ${['done','parked'].includes(p.status) ? `<p>Project ${esc(p.status)}. This is an organizational label, not physical approval.</p>` : ''}${warnings}
    <div class="columns"><div><section aria-label="3D view"><div class="heading"><h3>3D view</h3><span id="view-id" class="muted"></span></div><div id="viewer"></div><p class="small muted">Local preview only. No geometry changes or exports.</p></section>
    <section><h3>Revisions · newest first</h3><p class="small muted">Dates use folder dates, otherwise file times. Statuses are guesses from the matching fit text.</p><p class="small">Printed fit applies to that specimen only. Strength UNKNOWN.</p><div class="revisions">${p.revisions.map(r => `<article class="revision ${r.id === revision ? 'selected' : ''}"><div class="heading"><button data-revision="${esc(r.id)}" aria-pressed="${r.id === revision}">${esc(r.id)}</button><span class="badge ${r.status === 'fit' ? 'fit' : r.status === 'problem' ? 'problem' : ''}">${esc(r.status)} (guess)</span></div><p class="small muted">${esc(r.date || 'Date not recorded')} · ${r.released ? 'Release folder found' : 'No release folder'}</p>
    ${r.readmes.map(f => docLink(f, 'README')).join(' · ')} ${r.reports.map(f => docLink(f, 'Release report')).join(' · ')}
    <details><summary>Files and evidence</summary><p>3MF: ${r.three_mf.length ? r.three_mf.map(f => `<code>${esc(f)}</code>`).join('<br>') : 'None found'}</p><p>Viewer: ${r.viewers.length ? r.viewers.map(esc).join('<br>') : 'None found'}</p><p class="small muted">File locations only; Bench does not copy or download print files.</p>
    <ul>${r.fit_lines.map(l => `<li>${esc(l)}</li>`).join('') || '<li>No fit line names this exact ID.</li>'}</ul></details>
    ${r.warnings.length ? `<details><summary class="warning">Historical warning / supersession mentions (${r.warnings.length})</summary><p class="small">Mentions may describe another revision or a replacement. Read the source wording.</p><ul>${r.warnings.map(l => `<li>${esc(l)}</li>`).join('')}</ul></details>` : ''}</article>`).join('') || '<p>No revisions discovered for these prefixes yet.</p>'}</div></section></div>
    <div><section><h3>Project notes</h3><form id="project-form"><label for="status">Status</label><select id="status">${options(state.statuses,p.status)}</select><label for="notes">Notes</label><textarea id="notes" maxlength="12000">${esc(p.notes)}</textarea><p class="small muted">Updated ${esc(p.updated)}. Changes stay here until Save.</p><button class="primary" type="submit">Save status and notes</button></form><details><summary>Sources</summary>${p.sources.length ? `<ul>${p.sources.map(f => `<li><code>${esc(f)}</code></li>`).join('')}</ul>` : '<p>No source path recorded.</p>'}</details></section>
    <section><h3>Device cards</h3>${p.cards.map(c => `<details><summary>${esc(c.path.split('/').pop())}</summary><div class="document">${c.missing ? '<p>Device card is missing.</p>' : c.html}</div>${docLink(c.path, 'Read source')}</details>`).join('') || '<p>No device card linked yet.</p>'}</section>
    <section><h3>Still unknown</h3><ul class="unknown-list">${p.unknowns.map(u => `<li>${esc(u.text)}<br><span class="small">${docLink(u.source)}</span></li>`).join('') || '<li>No explicit UNKNOWN rows or newest README lines found. This does not establish fit or strength.</li>'}</ul></section></div></div>
    <section><h3>Fit report</h3><p>Report a printed specimen by the ID on the part. Review the exact log entry before saving.</p><form id="fit-form"><div class="form-row"><div><label for="fit-id">Revision ID</label><input id="fit-id" name="revision" required value="${esc(revision || '')}" list="revision-ids"><datalist id="revision-ids">${options(p.revisions.map(r => r.id))}</datalist></div><div><label for="fit-result">Result</label><select id="fit-result" name="result">${options(['Fits','Too tight','Too loose','Failed','Other'],'Fits')}</select></div></div>
    <label for="fit-where">Where was it tight or loose? What worked?</label><input id="fit-where" name="where" maxlength="2000"><div class="form-row"><div><label for="fit-walls">Walls (blank = UNKNOWN)</label><input id="fit-walls" name="walls" inputmode="numeric" maxlength="3"></div><div><label for="fit-infill">Infill % (blank = UNKNOWN)</label><input id="fit-infill" name="infill" inputmode="decimal" maxlength="6"></div></div><label for="fit-notes">Extra notes</label><input id="fit-notes" name="notes" maxlength="4000"><p class="small muted">Saving appends to the fit log and, when linked, the workflow log; the project moves to draft.</p><button type="submit">Preview exact entry</button><div id="fit-preview"></div></form></section>
    <section><h3>Workflow log</h3><div class="document">${p.workflow_html || '<p>No workflow section linked to this project.</p>'}</div></section>`;
  drawViewer();
  $('#project-form').addEventListener('input', () => { dirty = true; });
  $('#project-form').addEventListener('submit', saveProject);
  $('#fit-form').addEventListener('input', () => {dirty = true; preview = null; $('#fit-preview').replaceChildren();});
  $('#fit-form').addEventListener('submit', previewFit);
}
function drawViewer() {
  const r = project().revisions.find(r => r.id === revision);
  $('#view-id').textContent = revision || 'No revision';
  $('#viewer').innerHTML = r?.viewers.length ? `<label for="viewer-choice">Viewer page</label><select id="viewer-choice">${r.viewers.map(v => `<option value="${esc(v)}">${esc(v.split('/').pop())}</option>`).join('')}</select><iframe title="${esc(revision)} 3D preview" sandbox="allow-scripts" loading="lazy" src="/viewer/${encodeURIComponent(r.viewers[0].split('/').pop())}"></iframe>` : `<p class="empty">${revision ? `No viewer page for ${esc(revision)} yet` : 'No revision or viewer page yet'}</p>`;
  $('#viewer-choice')?.addEventListener('change', e => {$('#viewer iframe').src = '/viewer/' + encodeURIComponent(e.target.value.split('/').pop());});
}
function mayLeave() { return !dirty || window.confirm('Discard the unsaved changes on this project?'); }
async function load(rescan = false, preserve = false) {
  const data = await api(rescan ? '/api/refresh' : '/api/state', rescan ? 'POST' : 'GET', rescan ? {} : undefined);
  state = data; selected ||= state.projects[0]?.id;
  drawList(); if (!preserve) {dirty = false; preview = null; drawProject();}
  message(`Loaded ${state.projects.length} projects. Metadata scan ${(state.scan_seconds*1000).toFixed(0)} ms.`);
}
async function saveProject(e) {
  e.preventDefault(); const button = e.submitter; button.disabled = true;
  try {await api('/api/projects/'+selected,'PATCH',{status:$('#status').value,notes:$('#notes').value,hashes:state.hashes}); await load(); message('Status and notes saved.');}
  catch(err){message(err.message,true);} finally{button.disabled=false;}
}
async function previewFit(e) {
  e.preventDefault(); const body = Object.fromEntries(new FormData(e.target));
  try {const response = await api('/api/fit-report/preview','POST',body); preview = {...body,hashes:{...state.hashes}}; $('#fit-preview').innerHTML = `<pre>${esc(response.text)}</pre><button type="button" id="save-fit" class="primary">Save this fit report</button>`; $('#save-fit').addEventListener('click',saveFit);}
  catch(err){message(err.message,true);}
}
async function saveFit(e) {
  if(!preview)return; e.target.disabled=true;
  try {await api('/api/fit-report','POST',preview); await load(); message('Fit report saved. Project moved to draft.');}
  catch(err){message(err.message,true);e.target.disabled=false;}
}
document.addEventListener('click', e => {
  const p = e.target.closest('[data-project]'), r = e.target.closest('[data-revision]');
  if(p && mayLeave()){selected=p.dataset.project;revision=null;dirty=false;preview=null;drawList();drawProject();}
  if(r && mayLeave()){revision=r.dataset.revision;dirty=false;preview=null;drawProject();}
});
$('#search').addEventListener('input',drawList);
$('#filter').addEventListener('change',()=>{try{localStorage.setItem('bench.status',$('#filter').value);}catch{}drawList();});
$('#refresh').addEventListener('click',async()=>{if(!mayLeave())return;try{await load(true);}catch(err){message(err.message,true);}});
$('#new-project').addEventListener('click',()=>{newHashes={...state.hashes};$('#new-error').textContent='';$('#new-dialog').showModal();});
$('#close-new').addEventListener('click',()=>$('#new-dialog').close());
$('#new-form').addEventListener('submit',async e=>{
  e.preventDefault();const body=Object.fromEntries(new FormData(e.target));body.prefixes=body.prefixes.split(',').map(s=>s.trim()).filter(Boolean);
  for(const key of ['device_cards','sources'])body[key]=body[key].split(/\r?\n/).map(s=>s.trim()).filter(Boolean);
  body.hashes=newHashes;e.submitter.disabled=true;
  try{if(!mayLeave())return;const p=await api('/api/projects','POST',body);selected=p.id;revision=null;$('#new-dialog').close();e.target.reset();await load();message('Project created.');}
  catch(err){$('#new-error').textContent=err.message;}finally{e.submitter.disabled=false;}
});
window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue='';}});
(async()=>{try{state=await api('/api/state');$('#filter').innerHTML='<option value="">All statuses</option>'+options(state.statuses);try{$('#filter').value=localStorage.getItem('bench.status')||'';}catch{}selected=state.projects[0]?.id;drawList();drawProject();message(`Loaded ${state.projects.length} projects. Metadata scan ${(state.scan_seconds*1000).toFixed(0)} ms.`);}catch(err){message(err.message,true);$('#projects').innerHTML='<p>Projects could not be loaded. Use Refresh to try again.</p>';}})();
