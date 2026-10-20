// Actual page closures in isolated VM fixtures. Node built-ins only; no server/data/builds.
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const APP = path.resolve(__dirname, '..');
const read = name => fs.readFileSync(path.join(APP, name), 'utf8');
const workspace = read('workspace.js');
// Deliberately fail if anchors move: do not silently test a copied implementation.
function section(source, start, end) {
  const a = source.indexOf(start), b = source.indexOf(end, a + start.length);
  assert.ok(a >= 0 && b > a && source.indexOf(start, a + 1) < 0, `Unique source anchors: ${start}`);
  return source.slice(a, b);
}
const saveSource = section(workspace, '  async function saveWorkshop(){', '  // Save history:');
const statusSource = section(workspace, '  function updateSaveStatus()', '  function button(');
const clone = x => JSON.parse(JSON.stringify(x));
function elements() {
  const map = new Map();
  const get = id => {
    if (!map.has(id)) map.set(id, { hidden: true, open: false, checked: true, disabled: false,
      textContent: '', value: '', dataset: {}, children: [],
      append(...items) { this.children.push(...items); }, replaceChildren(...items) { this.children = items; } });
    return map.get(id);
  };
  return get;
}
function saver() {
  const get = elements(), requests = [], notices = [];
  const draft = { generation: 1, racks: [{ id: 'rack', name: 'Draft rack', placements: [
    { id: 'slot', assembly: { id: 'assembly', name: 'Pi', revision: 1, project: { pilot: 4 } } }] }] };
  const box = vm.createContext({ window: { workshopContext: { id: 'assembly', generation: 1 }, addEventListener() {} },
    byId: get, initial: draft, requests, notices, drawSoon() {}, render() {}, clearBuild() {}, renderReplacement() {},
    notify: (...args) => notices.push(args), hardware: { inputs: { pilot: 4 }, instance_revision: 1 },
    state: { project: { instance_revision: 1 } },
    api: async (route, body) => {
      requests.push({ route, body: clone(body) });
      return box.respond(body);
    } });
  box.respond = body => {
    const saved = clone(body.workspace); saved.generation++;
    saved.racks[0].placements[0].assembly.revision++;
    saved.racks[0].placements[0].assembly.project = clone(body.assembly.inputs);
    return saved;
  };
  vm.runInContext(`let capable=true, openingAssembly=false, savingLayout=false, artworkPending=0;
    let documentState=initial, layoutDirty=false, dirty=false, persistedAssemblyIds=new Set();
    const active=()=>documentState.racks[0]; const payload=()=>JSON.parse(JSON.stringify(hardware));
    ${statusSource}\n${saveSource}
    globalThis.inspect=()=>({documentState,layoutDirty,dirty,savingLayout,pins:[...persistedAssemblyIds]});`, box);
  return { box, get, requests, notices, run: code => vm.runInContext(code, box) };
}

test('page Save: layout/hardware dirty status enables Save without persistence', () => {
  const h = saver(); h.run('updateSaveStatus()');
  assert.equal(h.get('saveLayout').disabled, true);
  h.run('markChanged()');
  assert.equal(h.get('layoutSaveStatus').textContent, 'Unsaved changes');
  assert.equal(h.get('saveLayout').disabled, false);
  assert.throws(() => h.box.window.assertWorkshopSaved(), /Use Save/);
  h.run('layoutDirty=false;dirty=true;updateSaveStatus()');
  assert.equal(h.get('saveLayout').disabled, false);
  assert.equal(h.requests.length, 0);
});

test('page Save: one atomic request commits layout, appearance and hardware then clears dirty state', async () => {
  const h = saver();
  h.run('markChanged();dirty=true;documentState.racks[0].appearance={frame:"#123456"}');
  await h.get('saveLayout').onclick();
  assert.equal(h.requests.length, 1); const req = h.requests[0];
  assert.equal(req.route, 'studio-save'); assert.equal(req.body.assembly.id, 'assembly');
  assert.equal(req.body.assembly.inputs.pilot, 4);
  assert.equal(req.body.workspace.racks[0].appearance.frame, '#123456');
  const st = h.box.inspect();
  assert.equal(st.layoutDirty, false); assert.equal(st.dirty, false); assert.equal(st.savingLayout, false);
  assert.equal(st.documentState.generation, 2); assert.equal(h.box.state.project.instance_revision, 2);
  assert.deepEqual(Array.from(st.pins), ['assembly']);
  assert.equal(h.get('saveLayout').disabled, true);
  assert.doesNotThrow(() => h.box.window.assertWorkshopSaved());
});

test('page Save: rejected request keeps draft and hardware, reports error and permits retry', async () => {
  const h = saver(); h.run('markChanged();dirty=true');
  const before = clone(h.box.inspect().documentState);
  h.box.respond = () => { throw Error('Fixture stale generation'); };
  await h.get('saveLayout').onclick();
  assert.deepEqual(clone(h.box.inspect().documentState), before);
  assert.equal(h.box.inspect().dirty, true); assert.equal(h.box.inspect().layoutDirty, true);
  assert.equal(h.box.inspect().savingLayout, false); assert.equal(h.get('saveLayout').disabled, false);
  assert.deepEqual(h.notices.at(-1), ['Fixture stale generation', true]);
  assert.equal(h.box.hardware.inputs.pilot, 4); assert.equal(h.box.state.project.instance_revision, 1);
});

test('page Save: edits during in-flight Save remain dirty and double Save is rejected', async () => {
  const h = saver(); h.run('markChanged();dirty=true');
  const respond = h.box.respond; let finish;
  h.box.respond = body => new Promise(resolve => { finish = () => resolve(respond(body)); });
  const pending = h.box.window.saveWorkshop();
  assert.equal(h.get('saveLayout').disabled, true);
  await assert.rejects(h.box.window.saveWorkshop(), /Wait for the current operation/);
  assert.throws(() => h.box.window.assertWorkshopSaved(), /Use Save/);
  h.run('documentState.racks[0].name="Newer draft";hardware.inputs.pilot=3.9;markChanged()');
  finish(); await pending;
  const st = h.box.inspect();
  assert.equal(st.documentState.racks[0].name, 'Newer draft'); assert.equal(st.documentState.generation, 2);
  assert.equal(h.box.hardware.inputs.pilot, 3.9); assert.equal(st.dirty, true); assert.equal(st.layoutDirty, true);
  assert.equal(h.requests.length, 1); assert.equal(h.get('saveLayout').disabled, false);
});

for (const [setup, message] of [
  ['capable=false', /Restart/], ['openingAssembly=true', /Wait/], ['artworkPending=1', /image preview/],
  ['byId("mountWizard").hidden=false', /Apply or cancel/], ['byId("rackDialog").open=true', /Apply or cancel/],
]) test(`page Save: precondition ${setup} blocks writes`, async () => {
  const h = saver(); h.run(setup); await assert.rejects(h.box.window.saveWorkshop(), message);
  assert.equal(h.requests.length, 0); assert.equal(h.box.inspect().savingLayout, false);
});

// Run the real inline handlers with the installed workspace guard; disable only its unrelated auto-refresh.
function page(h) {
  const html = read('index.html').replace(/\r\n/g, '\n');
  let inline = section(html, '<script>\n', '</script>').slice('<script>\n'.length);
  const boot = 'safe(async()=>{await refresh();await loadPacks()});';
  assert.ok(inline.includes(boot)); inline = inline.replace(boot, '');
  const calls = [], notices = [], get = elements();
  const box = vm.createContext({ window: h.box.window, document: { getElementById: get,
    createElement: () => ({ click() {} }), createElementNS: () => ({}) },
    WorkshopCatalog: require(path.join(APP, 'catalog.js')), Option: class {},
    CustomEvent: class {}, setTimeout() {}, clearTimeout() {}, URL: { createObjectURL: () => 'fixture:blob' },
    fetch: async url => { calls.push(url); return { ok: true, blob: async () => ({}) }; },
    calls, notices });
  box.window.dispatchEvent = () => {};
  vm.runInContext(inline, box);
  vm.runInContext(`api=async(route)=>{calls.push(route);return {checks:[],status:'unknown'}};
    preview=async()=>{};message=(...args)=>notices.push(args);payload=()=>({inputs:{pilot:4}});`, box);
  return { box, get, calls, notices };
}
for (const id of ['check', 'bom', 'project', 'designExport', 'buildRevision']) {
  test(`page ${id}: dirty guard blocks action without silently saving`, async () => {
    const h = saver(); const p = page(h); h.run('markChanged();dirty=true');
    await p.get(id).onclick();
    assert.equal(h.requests.length, 0); assert.equal(p.calls.length, 0);
    assert.match(p.notices.at(-1)[0], /Use Save/);
    assert.equal(h.box.inspect().layoutDirty, true); assert.equal(h.box.inspect().dirty, true);
  });
}
test('page checks and BOM: clean actions use saved state without issuing Save', async () => {
  const h = saver(), p = page(h);
  await p.get('check').onclick(); await p.get('bom').onclick();
  assert.deepEqual(p.calls, ['check', '/api/bom?assembly=assembly']); assert.equal(h.requests.length, 0);
  assert.ok(p.notices.every(n => !n[1]));
});

async function viewer(mode = 'ok', studioMode = 'missing') {
  const get = elements(), frames = [], calls = [], events = new Map(); let painted = 0;
  const canvas = get('assemblyCanvas'); canvas.clientWidth = 32;
  const ctx = { setTransform() {}, fillRect() {}, fillText() {}, drawImage() {},
    createImageData: (w, h) => ({ data: new Uint8ClampedArray(w * h * 4) }), putImageData() { painted++; } };
  canvas.getContext = () => mode === 'no-canvas' ? null : ctx;
  const mesh = { id: 'tray', vertices: [[0, 0, 0], [5, 0, 0], [0, 5, 5]], triangles: [[0, 1, 2]] };
  const window = { addEventListener: (type, fn) => events.set(type, fn) };
  if (studioMode === 'throws') window.LabRaxAssembly = { AssemblyRenderer: class { constructor() { throw Error('Fixture WebGL unavailable'); } } };
  const box = vm.createContext({ window, document: { getElementById: get },
    requestAnimationFrame: fn => frames.push(fn), ResizeObserver: class { observe() {} },
    fetch: async url => {
      calls.push(url);
      if (mode === 'network' && url === '/api/assembly') throw Error('Fixture network failure');
      if (mode === 'bad-json' && url === '/api/assembly') return { ok: true, json: async () => { throw Error('Fixture invalid JSON'); } };
      if (mode === 'missing' && url === '/api/assembly') return { ok: false };
      if (url === '/api/assembly') return { ok: true, json: async () => ({ revision: 'Fixture only', parts: [mesh] }) };
      throw Error('Unexpected fixture URL: ' + url);
    } });
  const source = read('viewer.js');
  assert.ok(source.trimEnd().endsWith('initAssemblyViewer();'));
  // Capture the existing startup promise so rejections cannot escape the test.
  vm.runInContext(source.replace(/initAssemblyViewer\(\);\s*$/, 'globalThis.ready=initAssemblyViewer();'), box);
  await box.ready;
  while (frames.length) frames.shift()();
  return { get, calls, events, painted };
}
test('viewer startup: actual script loads, binds events and paints its first frame', async () => {
  const h = await viewer();
  assert.deepEqual(h.calls, ['/api/assembly']);
  assert.equal(h.painted, 1); assert.equal(h.get('assemblyCanvas').dataset.renderer, 'software');
  assert.match(h.get('assemblyStatus').textContent, /Fixture only/);
  assert.ok(h.events.has('assembly-model')); assert.equal(typeof h.get('assemblyReset').onclick, 'function');
});
for (const [mode, message] of [['missing', /Assembly load failed/], ['network', /Fixture network failure/],
  ['bad-json', /Fixture invalid JSON/], ['no-canvas', /Canvas rendering is unavailable/]]) {
  test(`viewer startup: ${mode} reports error without drawing or unhandled rejection`, async () => {
    const h = await viewer(mode); assert.equal(h.painted, 0);
    assert.match(h.get('assemblyStatus').textContent, message);
    assert.equal(h.calls.length, mode === 'no-canvas' ? 0 : 1);
  });
}
test('viewer startup: failed studio renderer falls back with a visible reason', async () => {
  const h = await viewer('ok', 'throws'); assert.equal(h.painted, 1);
  assert.equal(h.get('assemblyCanvas').dataset.renderer, 'software');
  assert.match(h.get('assemblyStatus').textContent, /Software fallback: Fixture WebGL unavailable/);
});

const rackBoot = section(workspace, '  try{sceneRenderer=new LabRaxStudio.Renderer();', "  byId('frontRackView').onclick=");
async function rackStartup(mode) {
  let draws = 0, previews = 0;
  const box = vm.createContext({ window: {}, sourceMeshes: null, sourceError: null, sceneRenderer: null,
    sceneCacheKey: 'old', drawSoon: () => draws++, drawPreviewSoon: () => previews++,
    LabRaxStudio: { Renderer: class { constructor() { if (mode === 'renderer') throw Error('Fixture renderer failed'); } } },
    LabRaxScene: { load: async () => { if (mode === 'required') throw Error('Rack component unavailable: fixture'); return { post: {} }; } },
    fetch: async url => { if (mode === 'optional-network') throw Error('Fixture optional asset failed');
      return { ok: mode !== 'optional-404', json: async () => ({ fixture: url }) }; } });
  vm.runInContext(rackBoot, box);
  // Production boot intentionally does not expose a promise. Drain its finite fixture microtasks.
  await new Promise(resolve => setImmediate(resolve));
  return { box, draws, previews };
}
test('rack viewer startup: required and optional meshes load then schedule both views', async () => {
  const h = await rackStartup('ok');
  assert.ok(h.box.sourceMeshes.post); assert.ok(h.box.sourceMeshes.extension); assert.ok(h.box.sourceMeshes.cable_guide);
  assert.equal(h.box.sourceError, null); assert.equal(h.draws, 1); assert.equal(h.previews, 1);
});
for (const mode of ['optional-404', 'optional-network']) test(`rack viewer startup: ${mode} keeps required meshes usable`, async () => {
  const h = await rackStartup(mode); assert.ok(h.box.sourceMeshes.post);
  assert.equal(h.box.sourceMeshes.extension, undefined); assert.equal(h.box.sourceMeshes.cable_guide, undefined);
  assert.equal(h.box.sourceError, null); assert.equal(h.draws, 1); assert.equal(h.previews, 1);
});
for (const mode of ['required', 'renderer']) test(`rack viewer startup: ${mode} failure retains diagnostic`, async () => {
  const h = await rackStartup(mode); assert.equal(h.box.sourceMeshes, null);
  assert.match(h.box.sourceError, mode === 'required' ? /Rack component unavailable/ : /Fixture renderer failed/);
  assert.equal(h.previews, 0);
  if (mode === 'required') assert.equal(h.draws, 1);
});
