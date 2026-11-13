'use strict';
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const editedForms = new Set();
function markEdited(id) { editedForms.add(id); dirty = true; updateQuickButtons(); }
function clearEdits() { editedForms.clear(); dirty = false; }
let quickSaving = false;
function updateQuickButtons() {
  const blocked = editedForms.has('project-form') || editedForms.has('details-form');
  document.querySelectorAll('[data-status], #write-report').forEach(b => b.disabled = blocked || quickSaving);
  if ($('#quick-hint')) $('#quick-hint').textContent = blocked ? 'Save or cancel your edits first' : '';
}
function quickButtons(p) {
  const actions = {
    idea: [['Start draft','draft']], measuring: [['Start draft','draft']],
    draft: [["I'm printing it",'printing']], printing: [['Printed, report due','report-due']],
    'report-due': [['Mark done','done']], done: [['Reopen as draft','draft']], parked: [['Reopen as draft','draft']]
  };
  return `<div class="part-buttons" aria-label="Next step">${p.status === 'report-due' ? '<button type="button" id="write-report">Write fit report</button>' : ''}${actions[p.status].map(([label,status]) => `<button type="button" data-status="${status}">${esc(label)}</button>`).join('')}</div><p id="quick-hint" class="small muted"></p>`;
}
async function quickStatus(status) {
  if (quickSaving || editedForms.has('project-form') || editedForms.has('details-form')) return;
  quickSaving = true; updateQuickButtons();
  try {
    await api('/api/projects/' + selected, 'PATCH', {status, hashes: state.hashes});
    await reloadAfterSave(null); message('Status saved.');
  } catch (err) { await stale(err); }
  finally { quickSaving = false; updateQuickButtons(); }
}
let listView = 'projects';
let state, selected, revision, dirty = false, preview = null, newHashes = null;
document.addEventListener('click', async e => {
  const button = e.target.closest('.open-folder'); if (!button) return;
  button.disabled = true;
  try { await api('/api/open-folder', 'POST', {path: button.dataset.path}); message('Opened the folder in File Explorer.'); }
  catch (err) { message(err.message, true); } finally { button.disabled = false; }
});
function message(text, error = false) { $('#message').textContent = text; $('#message').className = error ? 'error' : ''; }
async function api(path, method = 'GET', body) {
  const response = await fetch(path, {method, headers: method === 'GET' ? {} : {'Content-Type':'application/json','X-Bench-Token':state?.token || ''}, body:body === undefined ? undefined : JSON.stringify(body)});
  const value = await response.json();
  if (!response.ok) {const err = new Error(value.error || `Request failed (${response.status}).`); err.status = response.status; throw err;}
  return value;
}
const options = (values, value) => values.map(v => `<option value="${esc(v)}" ${v === value ? 'selected' : ''}>${esc(v)}</option>`).join('');
function drawList() {
  const term = $('#search').value.trim().toLowerCase(), filter = $('#filter').value;
  const shown = state.projects.filter(p => (!filter || p.status === filter) && [p.title,...p.prefixes,...p.revisions.map(r => r.id)].some(t => t.toLowerCase().includes(term)));
  $('#project-count').textContent = `${shown.length} of ${state.projects.length} projects`;
  $('#projects').innerHTML = shown.map(p => `<button class="project" data-project="${esc(p.id)}" aria-current="${p.id === selected}"><strong>${esc(p.title)}</strong><span>${esc(p.status)} · ${p.revisions.length} revisions</span></button>`).join('') || '<p>No projects match. Try another search or status.</p>';
  $('#list-view').setAttribute('aria-pressed', String(listView === 'projects'));
  $('#queue-view').setAttribute('aria-pressed', String(listView === 'queue'));
  if (listView === 'queue') {
    $('#project-count').textContent = `${state.queue.length} jobs in print queue`;
    $('#projects').innerHTML = state.queue.map(p => `<button class="project" data-project="${esc(p.id)}" aria-current="${p.id === selected}"><strong>${esc(p.title)}</strong><span>${esc(p.status)} · ${esc(p.latest || 'no release found')}</span><span class="${p.overdue ? 'warning' : ''}">${p.days} day${p.days === 1 ? "" : "s"}${p.overdue ? ' · overdue' : ''}</span></button>`).join('') || '<p>Nothing printing or waiting for a fit report.</p>';
  }
  $('#search').disabled = $('#filter').disabled = listView === 'queue';
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
    <details><summary>Files and evidence</summary><p>3MF: ${r.three_mf.length ? r.three_mf.map(f => `<code>${esc(f)}</code> <button type="button" class="open-folder" data-path="${esc(f)}">Open folder</button>`).join('<br>') : 'None found'}</p><p>Viewer: ${r.viewers.length ? r.viewers.map(esc).join('<br>') : 'None found'}</p><p class="small muted">Bench does not copy or download print files; Open folder shows the file in File Explorer.</p>
    <ul>${r.fit_lines.map(l => `<li>${esc(l)}</li>`).join('') || '<li>No fit line names this exact ID.</li>'}</ul></details>
    ${r.warnings.length ? `<details><summary class="warning">Historical warning / supersession mentions (${r.warnings.length})</summary><p class="small">Mentions may describe another revision or a replacement. Read the source wording.</p><ul>${r.warnings.map(l => `<li>${esc(l)}</li>`).join('')}</ul></details>` : ''}</article>`).join('') || '<p>No revisions discovered for these prefixes yet.</p>'}</div></section></div>
    <div><section><div class="heading"><h3>Project notes</h3><button type="button" id="edit-details">Edit details</button></div><form id="details-form" hidden>
    <p>Project ID: <code>${esc(p.id)}</code> (cannot be changed)</p>
    <label for="detail-title">Title</label><input id="detail-title" name="title" required maxlength="160" value="${esc(p.title)}">
    <label for="detail-prefixes">Revision prefixes (comma separated)</label><input id="detail-prefixes" name="prefixes" required value="${esc(p.prefixes.join(', '))}">
    <label for="detail-cards">Device card paths (one per line)</label><textarea id="detail-cards" name="device_cards">${esc(p.device_cards.join('\n'))}</textarea>
    <label for="detail-sources">Source paths (one per line)</label><textarea id="detail-sources" name="sources">${esc(p.sources.join('\n'))}</textarea>
    <label for="detail-workflow">Workflow log section (blank for none)</label><input id="detail-workflow" name="workflow_log" maxlength="300" value="${esc(p.workflow_log)}">
    <div class="actions"><button class="primary" type="submit">Save details</button><button id="cancel-details" type="button">Cancel</button></div></form>${quickButtons(p)}<form id="project-form"><label for="status">Status</label><select id="status">${options(state.statuses,p.status)}</select><label for="notes">Notes</label><textarea id="notes" maxlength="12000">${esc(p.notes)}</textarea><p class="small muted">Updated ${esc(p.updated)}. Changes stay here until Save.</p><button class="primary" type="submit">Save status and notes</button><button type="button" id="cancel-notes">Cancel notes and status edits</button></form><details><summary>Sources</summary>${p.sources.length ? `<ul>${p.sources.map(f => `<li><code>${esc(f)}</code></li>`).join('')}</ul>` : '<p>No source path recorded.</p>'}</details></section>
    <section><h3>Device cards</h3>${p.cards.map(c => `<details><summary>${esc(c.path.split('/').pop())}</summary><div class="document">${c.missing ? '<p>Device card is missing.</p>' : c.html}</div>${docLink(c.path, 'Read source')}</details>`).join('') || '<p>No device card linked yet.</p>'}</section>
    <section><h3>Still unknown</h3><ul class="unknown-list">${p.unknowns.map(u => `<li>${esc(u.text)}<br><span class="small">${docLink(u.source)}</span></li>`).join('') || '<li>No explicit UNKNOWN rows or newest README lines found. This does not establish fit or strength.</li>'}</ul></section></div></div>
    <section><h3>Fit report</h3><p>Report a printed specimen by the ID on the part. Review the exact log entry before saving.</p><form id="fit-form"><div class="form-row"><div><label for="fit-id">Revision ID</label><input id="fit-id" name="revision" required value="${esc(revision || '')}" list="revision-ids"><datalist id="revision-ids">${options(p.revisions.map(r => r.id))}</datalist></div><div><label for="fit-result">Result</label><select id="fit-result" name="result">${options(['Fits','Too tight','Too loose','Failed','Other'],'Fits')}</select></div></div>
    <label for="fit-where">Where was it tight or loose? What worked?</label><input id="fit-where" name="where" maxlength="2000"><div class="form-row"><div><label for="fit-walls">Walls (blank = UNKNOWN)</label><input id="fit-walls" name="walls" inputmode="numeric" maxlength="3"></div><div><label for="fit-infill">Infill % (blank = UNKNOWN)</label><input id="fit-infill" name="infill" inputmode="decimal" maxlength="6"></div></div><label for="fit-notes">Extra notes</label><input id="fit-notes" name="notes" maxlength="4000"><p class="small muted">Saving appends to the fit log and, when linked, the workflow log; the project moves to draft.</p><button type="submit">Preview exact entry</button><div id="fit-preview"></div></form></section>
    <section><h3>Workflow log</h3><div class="document">${p.workflow_html || '<p>No workflow section linked to this project.</p>'}</div></section>`;
  drawViewer();
  document.querySelectorAll('[data-status]').forEach(b => b.addEventListener('click', () => quickStatus(b.dataset.status)));
  $('#write-report')?.addEventListener('click', () => {
    if (editedForms.has('fit-form') && !mayLeave()) return;
    const latest = project().revisions.find(r => r.released);
    $('#fit-form').reset(); $('#fit-id').value = latest?.id || '';
    preview = null; $('#fit-preview').replaceChildren();
    editedForms.delete('fit-form'); dirty = editedForms.size > 0;
    $('#fit-id').scrollIntoView({block: 'center'}); $('#fit-id').focus();
    if (!latest) message('No release found. Choose a discovered revision for the fit report.');
  });
  $('#cancel-notes').addEventListener('click', () => {
    $('#status').value = project().status; $('#notes').value = project().notes;
    editedForms.delete('project-form'); dirty = editedForms.size > 0; updateQuickButtons();
  });
  updateQuickButtons();
  $('#edit-details').addEventListener('click', () => {$('#details-form').hidden = false; $('#detail-title').focus();});
  $('#details-form').addEventListener('input', () => markEdited('details-form'));
  $('#details-form').addEventListener('submit', saveDetails);
  $('#cancel-details').addEventListener('click', () => {
    $('#details-form').reset(); $('#details-form').hidden = true;
    editedForms.delete('details-form'); dirty = editedForms.size > 0; updateQuickButtons();
  });
  $('#project-form').addEventListener('input', () => markEdited('project-form'));
  $('#project-form').addEventListener('submit', saveProject);
  $('#fit-form').addEventListener('input', () => {markEdited('fit-form'); preview = null; $('#fit-preview').replaceChildren();});
  $('#fit-form').addEventListener('submit', previewFit);
}
let soloName = null;
function updateViewerLink() {
  const link = $('#open-viewer'), frame = $('#viewer iframe');
  if (link && frame) link.href = frame.getAttribute('src') + (soloName === null ? '' : '#solo=' + encodeURIComponent(soloName));
}
function resetSolo() {
  soloName = null;
  $('#part-buttons')?.replaceChildren();
  if ($('#part-buttons')) $('#part-buttons').hidden = true;
  updateViewerLink();
}
window.addEventListener('message', event => {
  const frame = $('#viewer iframe'), data = event.data;
  if (!frame || event.source !== frame.contentWindow || !data || typeof data !== 'object' ||
      Object.keys(data).length !== 2 || data.bench !== 'parts' || !Array.isArray(data.names) ||
      data.names.length > 200 || !Array.from(data.names).every(n => typeof n === 'string' && n.length <= 200)) return;
  const bar = $('#part-buttons');
  resetSolo();
  if (data.names.length <= 1) return;
  bar.hidden = false;
  bar.innerHTML = '<button type="button" aria-pressed="true">All parts</button>' +
    data.names.map(n => `<button type="button" aria-pressed="false">${esc(n)}</button>`).join('');
  [...bar.children].forEach((button, index) => button.addEventListener('click', () => {
    soloName = index === 0 ? null : data.names[index - 1];
    [...bar.children].forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    frame.contentWindow.postMessage({bench: 'solo', name: soloName}, '*');
    updateViewerLink();
  }));
});
function drawViewer() {
  soloName = null;
  const r = project().revisions.find(r => r.id === revision);
  $('#view-id').textContent = revision || 'No revision';
  $('#viewer').innerHTML = r?.viewers.length ? `<label for="viewer-choice">Viewer page</label><select id="viewer-choice">${r.viewers.map(v => `<option value="${esc(v)}">${esc(v.split('/').pop())}</option>`).join('')}</select><p><a id="open-viewer" target="_blank" rel="noopener">Open 3D in new tab</a></p><iframe title="${esc(revision)} 3D preview" sandbox="allow-scripts" loading="lazy" src="/viewer/${encodeURIComponent(r.viewers[0].split('/').pop())}"></iframe><div id="part-buttons" class="part-buttons" aria-label="Show parts" hidden></div>` : `<p class="empty">${revision ? `No viewer page for ${esc(revision)} yet` : 'No revision or viewer page yet'}</p>`;
  $('#viewer-choice')?.addEventListener('change', e => {resetSolo();$('#viewer iframe').src = '/viewer/' + encodeURIComponent(e.target.value.split('/').pop());updateViewerLink();});
  updateViewerLink();
}
// A refused save (409) means a file changed on disk: rescan, keep what was typed, and ask for one more Save.
async function stale(err) {
  if (err.status !== 409) {message(err.message, true); return false;}
  try {await load(true, true);} catch (e) {message(e.message, true); return false;}
  message('A Bench file changed on disk since this page loaded. The page is now up to date and your typed changes are kept: check them and press Save again.', true);
  return true;
}
function mayLeave() { return !dirty || window.confirm('Discard the unsaved changes on this project?'); }
async function load(rescan = false, preserve = false) {
  const data = await api(rescan ? '/api/refresh' : '/api/state', rescan ? 'POST' : 'GET', rescan ? {} : undefined);
  state = data; selected ||= state.projects[0]?.id;
  drawList(); if (!preserve) {clearEdits(); preview = null; drawProject();}
  message(`Loaded ${state.projects.length} projects. Metadata scan ${(state.scan_seconds*1000).toFixed(0)} ms.`);
}
async function saveProject(e) {
  e.preventDefault(); const button = e.submitter; button.disabled = true;
  try {await api('/api/projects/'+selected,'PATCH',{status:$('#status').value,notes:$('#notes').value,hashes:state.hashes}); await reloadAfterSave('project-form'); message('Status and notes saved.');}
  catch(err){await stale(err);} finally{button.disabled=false;}
}
// Preserve independent forms when another form saves successfully.
async function reloadAfterSave(saved) {
  const keep = [...editedForms].filter(id => id !== saved).map(id => [id,
    [...document.querySelectorAll('#' + id + ' input, #' + id + ' textarea, #' + id + ' select')].map(el => [el.id, el.value])]);
  await load();
  for (const [id, values] of keep) {
    for (const [field, value] of values) if ($('#' + field)) $('#' + field).value = value;
    if (id === 'details-form') $('#details-form').hidden = false;
    markEdited(id);
  }
}
function detailBody(form) {
  const body = Object.fromEntries(new FormData(form));
  body.prefixes = body.prefixes.split(',').map(s => s.trim()).filter(Boolean);
  for (const key of ['device_cards', 'sources']) body[key] = body[key].split(/\r?\n/).map(s => s.trim()).filter(Boolean);
  return body;
}
async function saveDetails(e) {
  e.preventDefault(); const button = e.submitter; button.disabled = true;
  try {
    // Send only changed fields, so an unchanged path that has since moved can't block a title fix.
    const saved = state.projects.find(p => p.id === selected), body = detailBody(e.target);
    for (const key of Object.keys(body)) if (JSON.stringify(body[key]) === JSON.stringify(saved[key] ?? '')) delete body[key];
    if (!Object.keys(body).length) {
      e.target.hidden = true; editedForms.delete('details-form'); dirty = editedForms.size > 0; updateQuickButtons();
      message('Nothing changed.'); return;
    }
    await api('/api/projects/' + selected, 'PATCH', {...body, hashes: state.hashes});
    await reloadAfterSave('details-form'); message('Job details saved.');
  } catch (err) { await stale(err); } finally { button.disabled = false; }
}
async function previewFit(e) {
  e.preventDefault(); const body = Object.fromEntries(new FormData(e.target));
  try {const response = await api('/api/fit-report/preview','POST',body); preview = {...body,hashes:{...state.hashes}}; $('#fit-preview').innerHTML = `<pre>${esc(response.text)}</pre><button type="button" id="save-fit" class="primary">Save this fit report</button>`; $('#save-fit').addEventListener('click',saveFit);}
  catch(err){message(err.message,true);}
}
async function saveFit(e) {
  if(!preview)return; e.target.disabled=true;
  try {await api('/api/fit-report','POST',preview); await reloadAfterSave('fit-form'); message('Fit report saved. Project moved to draft.');}
  catch(err){if(await stale(err)&&preview)preview.hashes={...state.hashes};e.target.disabled=false;}
}
document.addEventListener('click', e => {
  const p = e.target.closest('[data-project]'), r = e.target.closest('[data-revision]');
  if(p && mayLeave()){selected=p.dataset.project;revision=null;clearEdits();preview=null;drawList();drawProject();}
  if(r && mayLeave()){revision=r.dataset.revision;clearEdits();preview=null;drawProject();}
});
for (const [id, view] of [['list-view','projects'], ['queue-view','queue']]) {
  $('#' + id).addEventListener('click', () => {
    listView = view;
    try {localStorage.setItem('bench.view', view);} catch {}
    drawList();
  });
}
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
(async()=>{try{state=await api('/api/state');$('#filter').innerHTML='<option value="">All statuses</option>'+options(state.statuses);try{$('#filter').value=localStorage.getItem('bench.status')||'';listView=localStorage.getItem('bench.view')==='queue'?'queue':'projects';}catch{}selected=state.projects[0]?.id;drawList();drawProject();message(`Loaded ${state.projects.length} projects. Metadata scan ${(state.scan_seconds*1000).toFixed(0)} ms.`);}catch(err){message(err.message,true);$('#projects').innerHTML='<p>Projects could not be loaded. Use Refresh to try again.</p>';}})();
