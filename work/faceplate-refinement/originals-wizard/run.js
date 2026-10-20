// Rerunnable JavaScript checks for the app's pure modules. Node built-ins only; reads no user data,
// starts no server, writes nothing. Run: node js-tests/run.js  (or run_js_tests.ps1 to locate node).
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const APP = path.resolve(__dirname, '..');
const REF = path.join(APP, 'rack-references');

test('every app script parses', () => {
  const files = [...fs.readdirSync(APP).filter(f => f.endsWith('.js')).map(f => path.join(APP, f)),
                 ...fs.readdirSync(REF).filter(f => f.endsWith('.js')).map(f => path.join(REF, f))];
  assert.ok(files.length >= 9);
  for (const file of files) {
    assert.doesNotThrow(() => new vm.Script(fs.readFileSync(file, 'utf8'), { filename: file }), file);
  }
});

test('every script index.html loads from /rack-references/ is in the asset manifest', () => {
  const html = fs.readFileSync(path.join(APP, 'index.html'), 'utf8');
  const manifest = JSON.parse(fs.readFileSync(path.join(REF, 'asset-manifest.json'), 'utf8'));
  const urls = new Set(manifest.map(e => e.url));
  for (const [, src] of html.matchAll(/<script src="(\/rack-references\/[^"]+)"/g)) {
    assert.ok(urls.has(src), `${src} missing from asset-manifest.json (would 404)`);
  }
});

const layout = require(path.join(REF, 'rack-layout.js'));
const rack = () => ({ id: 'r1', slots: 5, placements: [
  { id: 'a', slot: 1, span: 1, fit: 'UNKNOWN' }, { id: 'b', slot: 3, span: 2, fit: 'UNKNOWN' }] });

test('RackLayout.checkRange rejects out-of-range and overlapping ranges', () => {
  const r = rack();
  assert.throws(() => layout.checkRange(r, 0, 1), /whole slot range/);
  assert.throws(() => layout.checkRange(r, 5, 2), /whole slot range/);
  assert.throws(() => layout.checkRange(r, 1.5, 1), /whole slot range/);
  assert.throws(() => layout.checkRange(r, 2, 2), /overlaps/);
  assert.doesNotThrow(() => layout.checkRange(r, 2, 1));
  assert.doesNotThrow(() => layout.checkRange(r, 3, 3 - 1, 'b'));
});

test('RackLayout.change moves an allocation and resets fit to UNKNOWN', () => {
  const r = rack(); r.placements[0].fit = 'PASS';
  const updated = layout.change(r, 'a', 2, 1);
  assert.equal(updated.slot, 2); assert.equal(updated.fit, 'UNKNOWN');
  assert.throws(() => layout.change(r, 'missing', 1, 1), /no longer available/);
});

test('RackLayout.release and restore round-trip; restore keeps fit UNKNOWN', () => {
  const r = rack();
  const record = layout.release(r, 'b');
  assert.equal(r.placements.length, 1);
  const item = layout.restore(r, { ...record, item: { ...record.item, fit: 'PASS' } });
  assert.equal(item.fit, 'UNKNOWN');
  assert.deepEqual(r.placements.map(p => p.id), ['a', 'b']);
  assert.throws(() => layout.restore(r, record), /already present/);
  assert.throws(() => layout.restore({ ...rack(), id: 'other' }, record), /original rack/);
});

const catalog = require(path.join(APP, 'catalog.js'));
const parts = [
  { id: 's', revision: 1, kind: 'screw', diameter: 3, pitch: 0.5, length: 8, material: 'A2 stainless steel' },
  { id: 's', revision: 2, kind: 'screw', diameter: 3, pitch: 0.5, length: 10, material: 'A2 stainless steel' },
  { id: 'i', revision: 1, kind: 'heatset', diameter: 3, pitch: 0.5, length: 4.3, material: null },
];

test('WorkshopCatalog.filter: latest revision, kind, exact diameter, unknown material, length bounds', () => {
  assert.deepEqual(catalog.filter(parts, { latest: true }).map(p => `${p.id}${p.revision}`), ['s2', 'i1']);
  assert.equal(catalog.filter(parts, { kind: 'heatset' }).length, 1);
  assert.equal(catalog.filter(parts, { diameter: '2.5' }).length, 0);
  assert.deepEqual(catalog.filter(parts, { material: catalog.unknown }).map(p => p.id), ['i']);
  assert.deepEqual(catalog.filter(parts, { min_length: '9' }).map(p => p.revision), [2]);
  assert.equal(catalog.filter(parts, { q: 'HEATSET' }).length, 1);
});

test('WorkshopCatalog.changes lists changed fields with their effect', () => {
  assert.deepEqual(catalog.changes(parts[0], null), []);
  const diff = catalog.changes(parts[0], parts[1]);
  assert.deepEqual(diff.map(d => d.field).sort(), ['length', 'revision']);
  assert.equal(diff.find(d => d.field === 'length').effect, 'Screw reach or insert pocket depth');
});

const scene = require(path.join(REF, 'rack-scene.js'));

test('LabRaxScene.frame stacks posts in levels of at most 5U that sum to the rack height', () => {
  for (const slots of [1, 5, 6, 10, 12]) {
    const f = scene.frame(slots);
    assert.equal(f.levels.reduce((a, b) => a + b, 0), slots);
    assert.ok(f.levels.every(u => u >= 1 && u <= 5));
    assert.equal(f.manufacturing, false);
    assert.match(f.pose_status, /UNKNOWN/);
    assert.equal(f.parts.filter(p => p.key.startsWith('post')).length, 4 * f.levels.length);
  }
  assert.throws(() => scene.frame(0), /Unsupported/);
  assert.throws(() => scene.frame(49), /Unsupported/);
});

const clearance = require(path.join(APP, 'clearance.js'));
const nominal = { slots: 5, width_mm: 208, depth_mm: 240, pitch_mm: 44.45 };
const eq = (spec, span = 1) => ({ span, spec: { dev_w: 85, dev_d: 56, dev_h: 20, standoff: 6, device_mount: 'inserts', ...spec } });

test('WorkshopClearance.screen grades height, width and depth against nominal rack numbers', () => {
  const ok = clearance.screen(nominal, { equipment: 'eq-1', span: 1 }, eq({}));
  assert.equal(ok.level, 'ok');
  assert.deepEqual(ok.checks.map(c => c.level), ['ok', 'ok', 'ok']);
  assert.match(ok.note, /UNKNOWN/);
  // 10 floor + 6 standoff + 26 = 42 of 44.45 -> under the 3 mm height threshold.
  assert.equal(clearance.screen(nominal, { equipment: 'eq-1', span: 1 }, eq({ dev_h: 26 })).checks[0].level, 'tight');
  assert.equal(clearance.screen(nominal, { equipment: 'eq-1', span: 1 }, eq({ dev_h: 40 })).level, 'over');
  // Straps skip the standoff.
  assert.equal(clearance.screen(nominal, { equipment: 'eq-1', span: 1 }, eq({ dev_h: 30, device_mount: 'straps' })).checks[0].level, 'ok');
  assert.equal(clearance.screen(nominal, { equipment: 'eq-1', span: 1 }, eq({ dev_w: 195 })).checks[1].level, 'over');
  assert.equal(clearance.screen(nominal, { equipment: 'eq-1', span: 1 }, eq({ dev_d: 220 })).checks[2].level, 'tight');
});

test('WorkshopClearance.screen keeps unspecified rack numbers UNKNOWN and flags span mismatch', () => {
  const r = clearance.screen({ ...nominal, width_mm: null }, { equipment: 'eq-1', span: 1 }, eq({}, 2));
  assert.equal(r.checks[1].level, 'unknown');
  assert.equal(r.checks.at(-1).name, 'span');
  assert.equal(r.level, 'over');
  assert.equal(clearance.screen(nominal, { equipment: 'pi4', span: 1 }, null).level, 'reference');
  assert.equal(clearance.screen(nominal, { equipment: 'eq-x', span: 1 }, null).level, 'unknown');
});

globalThis.LabRaxScene = scene;
const studio = require(path.join(REF, 'rack-studio.js'));

test('LabRaxStudio.artworkRect stays inside the 216 x 34 mm faceplate field', () => {
  for (const art of [{}, { x: 0, y: 0, scale: 1 }, { x: 1, y: 1, scale: 0.05 }, null]) {
    for (const aspect of [0.5, 1, 4, 10]) {
      const [x, z, w, h] = studio.artworkRect(art, aspect);
      assert.ok(w > 0 && h > 0);
      assert.ok(Math.abs(x) <= (216 - w) / 2 + 1e-9, `x ${x} for ${JSON.stringify(art)} @${aspect}`);
      assert.ok(Math.abs(w / h - aspect) < 1e-9);
    }
  }
});
