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
  assert.throws(() => layout.checkRange(r, 5, 2), /^Error: 2U from slot 5 doesn’t fit; this rack ends at slot 5\.$/);
  assert.throws(() => layout.checkRange(r, 6, 1), /Slot 6 doesn’t exist; this rack ends at slot 5/);
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

test('LabRaxScene.guidePose puts the cable guide plate flat on the post face at the slot hole pair', () => {
  const guide = JSON.parse(fs.readFileSync(path.join(REF, 'cable_guide.json'), 'utf8'));
  assert.equal(guide.vertices.length, 352);
  assert.equal(guide.triangles.length, 708);
  for (const slots of [1, 5, 9]) {
    for (const post of scene.GUIDE_POSTS) {
      for (const slot of [1, slots]) {
        const { R, t } = scene.guidePose(slots, post, slot), world = guide.vertices.map(v => scene.apply(R, t, v));
        assert.equal(Math.abs(R[0] * (R[4] * R[8] - R[5] * R[7]) - R[1] * (R[3] * R[8] - R[5] * R[6]) + R[2] * (R[3] * R[7] - R[4] * R[6])), 1);
        const ys = world.map(p => p[1]), zs = world.map(p => p[2]), xs = world.map(p => p[0]);
        // Plate on the post face (front posts y = 0, rear posts y = 240), loops pointing away from the rack.
        if (post[0] === 'R') { assert.ok(Math.abs(Math.min(...ys) - 240) < 1e-6); assert.ok(Math.max(...ys) > 260); }
        else { assert.ok(Math.abs(Math.max(...ys)) < 1e-6); assert.ok(Math.min(...ys) < -20); }
        // 1U tall, centred on the slot; centred on the faceplate hole column of that side.
        const mid = (slots - slot) * scene.U + scene.U / 2;
        assert.ok(Math.abs(Math.min(...zs) - (mid - 22)) < 1e-6 && Math.abs(Math.max(...zs) - (mid + 22)) < 1e-6);
        assert.ok(Math.abs((Math.min(...xs) + Math.max(...xs)) / 2 - (post[1] === 'L' ? -118.2625 : 118.2625)) < 1e-4);
      }
    }
  }
  assert.throws(() => scene.guidePose(5, 'XL', 1), /post FL/);
  assert.throws(() => scene.guidePose(5, 'RL', 6), /inside the rack/);
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
  assert.equal(clearance.screen(nominal, { equipment: 'eq-000000000004', span: 1 }, null).level, 'unknown');
  assert.equal(clearance.screen(nominal, { equipment: 'eq-x', span: 1 }, null).level, 'unknown');
});

globalThis.LabRaxScene = scene;
test('WorkshopClearance.screen uses the slot tray placement (offset, rotation, standoff, rear support, U)', () => {
  const at = (tray, span = 1, item = eq({})) => clearance.screen(nominal, { equipment: 'eq-1', span, tray }, item);
  assert.deepEqual(at(undefined).checks, at({}).checks);
  // 85 + 16 + 2 x 50 = 201 of 208 -> 7 mm spare (ok); 2 x 53 -> 2 mm spare (tight).
  assert.equal(at({ dev_off_x: 50 }).checks[1].needed, 201);
  assert.equal(at({ dev_off_x: -53 }).checks[1].level, 'tight');
  // Rotated 90: 56 wide, 85 deep.
  assert.deepEqual(at({ dev_rot: 90 }).checks.slice(1).map(c => c.needed), [56 + 16, 12 + 85]);
  assert.equal(at({ dev_off_y: 175 }).checks[2].level, 'over');
  assert.equal(at({ rear_support: true }).checks[2].needed, 240);
  assert.match(at({ rear_support: true }).checks[2].text, /Rear-support/);
  // Rear support runs to the back posts by design: 240 of 240 mm reads OK (by design), not TIGHT (Brian, 2026-10-19).
  assert.equal(at({ rear_support: true }).checks[2].level, 'ok');
  assert.equal(at({ rear_support: true }).checks[2].byDesign, true);
  assert.match(at({ rear_support: true }).checks[2].text, /OK \(by design\)/);
  assert.equal(clearance.screen({ ...nominal, depth_mm: 238 }, { equipment: 'eq-1', span: 1, tray: { rear_support: true } }, eq({})).checks[2].level, 'over');
  assert.equal(clearance.screen({ ...nominal, depth_mm: 245 }, { equipment: 'eq-1', span: 1, tray: { rear_support: true } }, eq({})).checks[2].level, 'tight');
  // A taller standoff only for this slot.
  assert.equal(at({ standoff: 20 }).checks[0].level, 'over');
  assert.equal(at({ standoff: 20, device_mount: 'straps' }).checks[0].level, 'ok');
  // Designed U follows the slot's tray u (the library item says 1U).
  assert.equal(at({ u: 2 }, 1).checks.at(-1).name, 'span');
  assert.equal(at({ u: 2 }, 2).level, 'ok');
  assert.equal(at({ u: 1 }, 1, eq({}, 2)).level, 'ok');
});

const studio = require(path.join(APP, 'rack-studio.js'));

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

test('LabRaxStudio.artworkWindow generalizes the reference window to wizard faceplates of any U span', () => {
  // A 1U wizard plate (252 x 42 mm, bottom at 0) gives exactly the reference window.
  assert.deepEqual(studio.artworkWindow(252, 42), { w: 216, h: 34, z: 21 });
  assert.deepEqual(studio.artworkRect({ x: 0.3, y: 0.7, scale: 0.8 }, 3, studio.artworkWindow(252, 42)),
                   studio.artworkRect({ x: 0.3, y: 0.7, scale: 0.8 }, 3));
  for (const u of [1, 2, 3, 5]) {
    const plateH = u * 44.45 - 2.45, win = studio.artworkWindow(252, plateH);
    assert.ok(Math.abs(win.z - plateH / 2) < 1e-9 && Math.abs(win.h - (plateH - 8)) < 1e-9);
    for (const art of [{}, { x: 0, y: 0, scale: 1 }, { x: 1, y: 1, scale: 1 }, { x: 1, y: 0, scale: 0.05 }, null]) {
      for (const aspect of [0.25, 1, 4, 10]) {
        const [x, z, w, h] = studio.artworkRect(art, aspect, win);
        assert.ok(w > 0 && h > 0 && Math.abs(w / h - aspect) < 1e-9);
        assert.ok(Math.abs(x) + w / 2 <= win.w / 2 + 1e-9, `x ${x} @${u}U`);
        assert.ok(z - h / 2 >= 4 - 1e-9 && z + h / 2 <= plateH - 4 + 1e-9, `z ${z} h ${h} @${u}U`);
      }
    }
  }
  // A tall image fills more of a 2U plate than of a 1U plate.
  assert.ok(studio.artworkRect({ scale: 1 }, 1, studio.artworkWindow(252, 86.45))[3] > studio.artworkRect({ scale: 1 }, 1)[3]);
});

test('LabRaxStudio.artworkRect keeps wizard images clear of port and keystone openings', () => {
  const overlaps = (r, o, gap) => Math.abs(r[0] - o.x) < (r[2] + o.w) / 2 + gap - 1e-9 && Math.abs(r[1] - o.z) < (r[3] + o.h) / 2 + gap - 1e-9;
  const cases = [
    [42, [{ x: -15, z: 21, w: 14.5, h: 16 }, { x: 10, z: 21, w: 14.5, h: 16 }, { x: 70, z: 21, w: 14.5, h: 16 }, { x: -90, z: 21, w: 15, h: 8 }]],
    [86.45, [{ x: 0, z: 43.225, w: 14.5, h: 16 }, { x: -60, z: 70, w: 30, h: 10 }]],
    [42, [{ x: 0, z: 21, w: 200, h: 4 }]],   // a full-width slot leaves strips above and below
  ];
  for (const [plateH, openings] of cases) {
    const win = { ...studio.artworkWindow(252, plateH), openings };
    for (const art of [{}, { x: 0, y: 0, scale: 1 }, { x: 1, y: 1, scale: 1 }, { x: 0.3, y: 0.8, scale: 0.4 }]) {
      for (const aspect of [0.5, 1, 3, 8]) {
        const r = studio.artworkRect(art, aspect, win);
        assert.ok(r[2] > 0 && Math.abs(r[2] / r[3] - aspect) < 1e-9);
        for (const o of openings) assert.ok(!overlaps(r, o, 2), `${JSON.stringify(r)} hits ${JSON.stringify(o)} @${aspect}`);
        assert.ok(Math.abs(r[0]) + r[2] / 2 <= 108 + 1e-9 && r[1] - r[3] / 2 >= 4 - 1e-9 && r[1] + r[3] / 2 <= plateH - 4 + 1e-9);
      }
    }
  }
  // No openings (or none inside the window) leaves the window unchanged.
  const plain = studio.artworkWindow(252, 42);
  assert.deepEqual(studio.artworkRect({}, 2, { ...plain, openings: [] }), studio.artworkRect({}, 2, plain));
  assert.equal(studio.clearWindow(plain, [{ x: 0, z: 60, w: 10, h: 10 }]), plain);
});

test('LabRaxStudio.selectionRect follows the plate front at any U height', () => {
  for (const u of [1, 2, 3, 5]) {
    const h = u * 44.45 - 2.45, [cx, cz, hx, hz, r] = studio.selectionRect(-126, 126, 0, h, 2.5);
    assert.deepEqual([cx, hx, r], [0, 126, 2.5]);
    assert.ok(Math.abs(cz - h / 2) < 1e-9 && Math.abs(hz - h / 2) < 1e-9);
  }
});

const ports = require(path.join(APP, 'cable-ports.js'));
const example = require('./example-fixture.js');
const portRack = () => ({ id: 'r', slots: 5, placements: [
  { id: 'pi', slot: 1, span: 1, equipment: 'eq-000000000004' }, { id: 'eq', slot: 3, span: 2, equipment: 'eq-0123456789ab' }] });
const wizardItem = { id: 'eq-0123456789ab', spec: { u: 2, dev_d: 80,
  ports: [{ id: 'p-lan', label: 'LAN', type: 'rj45', x: 10, z: 20, w: 16, h: 14 }],
  rear_ports: [{ id: 'p-pwr', label: 'Power', type: 'iec', x: -40, z: 30 }], keystones: [-60, 60] } };

test('LabRaxPorts library planning ports: nine ports, face UNKNOWN, front-edge ports point front and USB/Ethernet right', () => {
  const list = ports.portsFor(portRack(), portRack().placements[0], example);
  assert.equal(list.length, 9);
  assert.equal(new Set(list.map(p => p.id)).size, 9);
  for (const p of list) {
    assert.equal(p.face, null);
    assert.equal(p.source, 'wizard');
    assert.ok(ports.TYPES[p.type], p.id);
    assert.equal(p.key, 'pi/' + p.id);
  }
  assert.deepEqual(list.filter(p => p.points === 'front').map(p => p.id), ['usb-c-power', 'hdmi0', 'hdmi1', 'audio']);
  assert.ok(list.filter(p => p.points === 'right').every(p => p.x > 40));
});

test('LabRaxPorts wizard ports: front openings, rear ports and keystone pass-through pairs', () => {
  const list = ports.wizardPorts(wizardItem.spec);
  assert.deepEqual(list.map(p => p.id), ['p-lan', 'p-pwr', 'ks-1-front', 'ks-1-rear', 'ks-2-front', 'ks-2-rear']);
  const byId = Object.fromEntries(list.map(p => [p.id, p]));
  assert.equal(byId['p-lan'].face, 'front'); assert.equal(byId['p-lan'].y, -4);
  assert.equal(byId['p-pwr'].face, 'rear'); assert.equal(byId['p-pwr'].y, 12 + 80);
  for (const n of [1, 2]) {
    const f = byId[`ks-${n}-front`], r = byId[`ks-${n}-rear`];
    assert.equal(f.passThrough, r.id); assert.equal(r.passThrough, f.id);
    assert.equal(f.type, 'keystone'); assert.equal(f.x, r.x);
    assert.ok(Math.abs(f.z - (2 * 44.45 - 2.45) / 2) < 1e-9);
  }
  assert.deepEqual(ports.wizardPorts(null), []);
  assert.deepEqual(ports.portsFor(portRack(), portRack().placements[1], undefined), []);
});

test('LabRaxPorts wizard ports follow the slot tray placement (placement.tray wins over the library spec)', () => {
  const spec = { ...wizardItem.spec, dev_w: 100, dev_d: 80, standoff: 6, device_mount: 'inserts', u: 2 };
  const item = { ...wizardItem, spec };
  const ids = list => Object.fromEntries(list.map(p => [p.id, p]));
  // No tray settings: same as the library item.
  assert.deepEqual(ports.wizardPorts(spec, undefined), ports.wizardPorts(spec, {}));
  assert.deepEqual([ids(ports.wizardPorts(spec))['p-pwr'].x, ids(ports.wizardPorts(spec))['p-pwr'].y], [-40, 92]);
  // Offset, deeper front gap, other keystones, 1U plate, lower standoff.
  const moved = ids(ports.wizardPorts(spec, { dev_off_x: 5, dev_off_y: 10, keystones: [80], u: 1, standoff: 4 }));
  assert.deepEqual([moved['p-pwr'].x, moved['p-pwr'].y, moved['p-pwr'].z, moved['p-pwr'].points], [-35, 12 + 10 + 80, 28, 'rear']);
  assert.deepEqual(Object.keys(moved).filter(k => k.startsWith('ks-')), ['ks-1-front', 'ks-1-rear']);
  assert.equal(moved['ks-1-front'].x, 80);
  assert.ok(Math.abs(moved['ks-1-front'].z - (44.45 - 2.45) / 2) < 1e-9);
  // Faceplate opening follows the device (Brian, 2026-10-19): +5 offset, standoff 6 -> 4 = 2 mm lower.
  assert.deepEqual([moved['p-lan'].x, moved['p-lan'].y, moved['p-lan'].z], [15, -4, 18]);
  // Turned device: the opening stays where it was entered.
  assert.deepEqual([ids(ports.wizardPorts(spec, { dev_off_x: 5, dev_rot: 90 }))['p-lan'].x, ids(ports.wizardPorts(spec, { dev_off_x: 5, dev_rot: 90 }))['p-lan'].z], [10, 20]);
  // Straps drop the standoff (device sits on the floor).
  assert.equal(ids(ports.wizardPorts(spec, { device_mount: 'straps' }))['p-pwr'].z, 24);
  // Rotation (equipment_tray.scad dp()): rear port 10 mm from the left edge of a 100 x 80 device.
  const turn = r => ids(ports.wizardPorts(spec, { dev_rot: r }))['p-pwr'];
  assert.deepEqual(['x', 'y', 'points'].map(k => turn(90)[k]), [-40, 12 + 10, 'left']);
  assert.deepEqual(['x', 'y', 'points'].map(k => turn(180)[k]), [40, 12, 'front']);
  assert.deepEqual(['x', 'y', 'points'].map(k => turn(270)[k]), [40, 12 + 90, 'right']);
  // portsFor reads the placement's tray and says the rear port moved with it.
  const rack = portRack(), eq = { ...rack.placements[1], tray: { dev_off_y: 10, keystones: [] } };
  const list = ports.portsFor(rack, eq, item);
  assert.deepEqual(list.map(p => p.id), ['p-lan', 'p-pwr']);
  assert.equal(list[1].y, 102); assert.match(list[1].note, /this slot’s tray placement/);
  assert.match(ports.portsFor(rack, rack.placements[1], item)[1].note, /Position as entered/);
});

test('LabRaxPorts overrides merge, reset, custom ports and prune', () => {
  const rack = portRack(), [pi, eq] = rack.placements;
  ports.setOverride(rack, 'pi', 'ethernet', { face: 'rear', x: 40.123 });
  ports.setOverride(rack, 'pi', 'ethernet', { label: 'Uplink' });
  assert.deepEqual(rack.cabling.ports, [{ face: 'rear', x: 40.12, label: 'Uplink', allocation: 'pi', port: 'ethernet' }]);
  let eth = ports.portsFor(rack, pi, example).find(p => p.id === 'ethernet');
  assert.equal(eth.face, 'rear'); assert.equal(eth.label, 'Uplink'); assert.equal(eth.x, 40.12);
  assert.ok(eth.tuned && eth.edited); assert.equal(eth.points, 'right');
  const id = ports.newPortId(rack, 'eq');
  assert.match(id, /^custom-[a-z0-9]+$/);
  ports.setOverride(rack, 'eq', id, { label: 'Fan', type: 'dc-barrel', face: 'rear', x: 0, y: 60, z: 20 }, true);
  const custom = ports.portsFor(rack, eq, wizardItem).find(p => p.id === id);
  assert.ok(custom.custom); assert.equal(custom.points, 'rear'); assert.equal(custom.key, 'eq/' + id);
  // Reset removes only that entry; removing the last entry drops cabling entirely.
  ports.setOverride(rack, 'pi', 'ethernet', null);
  eth = ports.portsFor(rack, pi, example).find(p => p.id === 'ethernet');
  assert.equal(eth.face, null); assert.ok(!eth.edited);
  rack.cabling.guides = [{ id: 'g', post: 'RL', slot: 1 }];
  const pruned = ports.prune({ ...rack, placements: [pi] });
  assert.equal(pruned.cabling.ports, undefined); assert.equal(pruned.cabling.guides.length, 1);
  assert.equal(rack.cabling.ports.length, 1, 'prune does not change the draft');
  ports.setOverride(rack, 'eq', id, null);
  assert.deepEqual(rack.cabling, { guides: [{ id: 'g', post: 'RL', slot: 1 }] });
  delete rack.cabling.guides; ports.setOverride(rack, 'pi', 'audio', { face: 'front' }); ports.setOverride(rack, 'pi', 'audio', null);
  assert.equal(rack.cabling, undefined);
});

test('LabRaxPorts marker rotations are proper rotations and parts sit at the allocation base', () => {
  for (const [name, R] of Object.entries(ports.POINTS)) {
    const det = R[0] * (R[4] * R[8] - R[5] * R[7]) - R[1] * (R[3] * R[8] - R[5] * R[6]) + R[2] * (R[3] * R[7] - R[4] * R[6]);
    assert.ok(Math.abs(det - 1) < 1e-12, name);
    const out = [-R[1], -R[4], -R[7]];  // world direction of the marker's outward −Y
    assert.deepEqual(out.map(v => v + 0), { front: [0, -1, 0], rear: [0, 1, 0], right: [1, 0, 0], left: [-1, 0, 0] }[name]);
  }
  const rack = portRack(), parts = ports.markerParts(rack, rack.placements, [example, wizardItem], 'pi/hdmi0');
  assert.equal(parts.length, 9 + 6);
  assert.equal(parts.filter(p => p.selected).length, 1);
  const hdmi = parts.find(p => p.port === 'pi/hdmi0');
  assert.equal(hdmi.t[2], (5 - 1) * 44.45 + 18.8);
  const lan = parts.find(p => p.port === 'eq/p-lan');
  assert.equal(lan.t[2], (5 - 4) * 44.45 + 20);
  const pos = ports.positionFromHit(rack, rack.placements[0], [500, -90, 4 * 44.45 + 100]);
  assert.deepEqual(pos, { x: 150, y: -40, z: 44.45 + 10 });
});

test('LabRaxPorts marker meshes exist for every connector type', () => {
  const meshes = ports.markerMeshes(studio);
  for (const type of Object.keys(ports.TYPES)) {
    const m = meshes['port-' + type];
    assert.ok(m && m.triangles.length > 0, type);
    assert.ok(m.vertices.every(v => v.every(Number.isFinite)), type);
    const ys = m.vertices.map(v => v[1]);
    assert.ok(Math.min(...ys) >= -2.5 - 1e-9 && Math.max(...ys) <= 1e-9, type);
  }
});

const cableView = require(path.join(APP, 'cable-view.js'));

test('LabRaxCableView tube follows the path, is finite and has closed end caps', () => {
  const pts = cableView.sagPath([[0, 250, 0], [100, 250, 200], [100, 254, 300]]);
  assert.deepEqual(pts[0], [0, 250, 0]);
  assert.deepEqual(pts.at(-1), [100, 254, 300]);
  const m = cableView.tubeMesh(pts, 3, 8);
  assert.ok(m.vertices.length > 0 && m.triangles.length > 0);
  assert.ok(m.vertices.every(v => v.every(Number.isFinite)) && m.normals.every(v => v.every(Number.isFinite)));
  // Every ring vertex sits one radius from its path point (the caps add one centre point per end).
  const ring = 8;
  pts.forEach((p, i) => { for (let j = 0; j < ring; j++) assert.ok(Math.abs(Math.hypot(...m.vertices[i * ring + j].map((v, k) => v - p[k])) - 3) < 1e-6); });
  // Closed: every edge is shared by exactly two triangles.
  const edges = new Map();
  for (const t of m.triangles) for (let k = 0; k < 3; k++) { const a = t[k], b = t[(k + 1) % 3], key = Math.min(a, b) + ':' + Math.max(a, b); edges.set(key, (edges.get(key) || 0) + 1); }
  assert.ok([...edges.values()].every(n => n === 2));
  assert.equal(cableView.tubeMesh([[0, 0, 0]], 3).triangles.length, 0);
});

test('LabRaxCableView sag dips between points and stays put on vertical runs', () => {
  const flat = cableView.sagPath([[0, 0, 100], [500, 0, 100]], 10);
  assert.ok(Math.min(...flat.map(p => p[2])) < 100 - 19.9 && Math.min(...flat.map(p => p[2])) >= 100 - 20 - 1e-9);
  const vertical = cableView.sagPath([[0, 0, 0], [0, 0, 300]], 10);
  assert.ok(vertical.every(p => p[0] === 0 && p[1] === 0));
});

test('LabRaxCableView bundles cables side by side through a guide without overlap', () => {
  const off = cableView.bundleOffsets([{ id: 'a', guides: ['g1'], diameter: 6 }, { id: 'b', guides: ['g1', 'g2'], diameter: 4 }, { id: 'c', guides: ['g1'], diameter: 8 }]);
  const xs = ['a', 'b', 'c'].map(id => [off[id].g1, { a: 6, b: 4, c: 8 }[id]]).sort((p, q) => p[0] - q[0]);
  for (let i = 1; i < xs.length; i++) assert.ok(xs[i][0] - xs[i][1] / 2 >= xs[i - 1][0] + xs[i - 1][1] / 2 - 1e-9);
  assert.ok(Math.abs(xs[0][0] - xs[0][1] / 2 + (xs.at(-1)[0] + xs.at(-1)[1] / 2)) < 1e-9, 'centred on the guide');
  assert.equal(off.b.g2, 0);
});

test('LabRaxCableView exit grommets face outward with proper rotations', () => {
  const det = R => R[0] * (R[4] * R[8] - R[5] * R[7]) - R[1] * (R[3] * R[8] - R[5] * R[6]) + R[2] * (R[3] * R[7] - R[4] * R[6]);
  for (const [pos, n] of Object.entries(cableView.EXIT_NORMAL)) {
    const R = cableView.exitRotation(pos), out = [0, 1, 2].map(r => -R[r * 3 + 1]);
    assert.ok(Math.abs(det(R) - 1) < 1e-12, pos);
    assert.deepEqual(out.map(v => v + 0), n, pos);
  }
  const m = cableView.grommetMesh(studio);
  assert.ok(m.triangles.length > 0 && m.vertices.every(v => v.every(Number.isFinite)));
  assert.notEqual(cableView.geometryKey([[0, 0, 0], [1, 2, 3]], 3), cableView.geometryKey([[0, 0, 0], [1, 2, 4]], 3));
});


test('first-run UI has no retired equipment card, wording or implicit allocation', () => {
  for(const name of ['workspace.js','index.html']) {
    const source=fs.readFileSync(path.join(APP,name),'utf8');
    assert.doesNotMatch(source,/pi ?_?4|raspberry/i,name);
    assert.doesNotMatch(source,/equipment:["']pi4["']/i,name);
  }
  const workspace=fs.readFileSync(path.join(APP,'workspace.js'),'utf8');
  assert.match(workspace,/Choose equipment…/);
  assert.match(workspace,/equipment:item.id/);
});

test('root front-end assets match their hashes', () => {
  const crypto=require('node:crypto');
  for(const entry of JSON.parse(fs.readFileSync(path.join(APP,'asset-manifest.json'),'utf8')))
    assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(APP,entry.file))).digest('hex'),entry.sha256,entry.file);
});

test('new placements use the chosen library item and omit historical reference metadata', () => {
  const source=fs.readFileSync(path.join(APP,'workspace.js'),'utf8');
  const factory=source.slice(source.indexOf('  function newAssembly(){'),source.indexOf('  function clearBuild(){'));
  const place=source.slice(source.indexOf('  window.placeLibraryEquipment=function(item){'),source.indexOf('  // Place on tray window "Apply to draft"'));
  const rack={id:'r',slots:5,placements:[]};let calls=0;
  const box={window:{},capable:true,assemblyTemplate:{selections:{screw:{id:'s',revision:2}},inputs:{pilot:4},reference:{historical:true}},
    uid:()=> '12345678',active:()=>rack,selectedSlot:2,assigned:(r,s)=>r.placements.find(p=>s>=p.slot&&s<p.slot+p.span),
    markChanged:()=>calls++,renderTree:()=>{},setStage:()=>{},renderProperties:()=>{},notify:()=>{}};
  vm.runInNewContext(factory+place,box);
  assert.equal(box.window.placeLibraryEquipment({id:'eq-123456789abc',name:'Chosen router',span:2,spec:{u:1}}),true);
  assert.equal(calls,1);
  const p=rack.placements[0];assert.equal(p.equipment,'eq-123456789abc');assert.equal(p.geometry,'equipment-library');
  assert.equal(p.assembly.name,'Chosen router');assert.equal(p.tray.u,2);assert.equal(p.assembly.project.reference,undefined);
  assert.equal(p.assembly.project.selections.screw.revision,2);
});
