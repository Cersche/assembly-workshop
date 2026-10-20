
(() => {
'use strict';
/* ================= constants & helpers ================= */
const U = 44.45, BASE_U = 5, DEG = Math.PI / 180;
let RU = 9; // total rack units, from the stack of levels
let glReady = false;
const PX = 125.98, DEPTH = 240, HOLE_X = 118.118;
const HOLE_Z = [38.13, 22.225, 6.32]; // a (top), b (middle), c (bottom) within a unit
const $ = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const uid = () => Math.random().toString(36).slice(2, 10);
const fmt = (v, d = 1) => (v < -0.05 ? '−' : '') + Math.abs(v).toFixed(d);
const FIBER = [
  {key:'blue',name:'Blue',hex:'#1f5fbf'},{key:'orange',name:'Orange',hex:'#e8751a'},{key:'green',name:'Green',hex:'#2e8b3e'},
  {key:'brown',name:'Brown',hex:'#8a5a2b'},{key:'slate',name:'Slate',hex:'#7a848a'},{key:'white',name:'White',hex:'#efefea'},
  {key:'red',name:'Red',hex:'#c8322b'},{key:'black',name:'Black',hex:'#26292b'},{key:'yellow',name:'Yellow',hex:'#e6c01e'},
  {key:'violet',name:'Violet',hex:'#7b4fb0'},{key:'rose',name:'Rose',hex:'#e58fa6'},{key:'aqua',name:'Aqua',hex:'#2bb3b1'}
];
const FRAME_COLORS = [['#232628','Black'],['#6b7276','Grey'],['#e8e9e5','White'],['#2a5aa8','Blue'],['#d9681c','Orange'],['#3c6e4a','Green']];
const fiberHex = k => (FIBER.find(f => f.key === k) || FIBER[0]).hex;
const hexRgb = h => { const n = parseInt(h.slice(1), 16); return [(n >> 16 & 255) / 255, (n >> 8 & 255) / 255, (n & 255) / 255]; };
const mixRgb = (a, b, t) => a.map((x, i) => x + (b[i] - x) * t);
const lum = c => 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
/* Dark PETG reads as a void on screen, so lift very dark filament a little toward grey. */
const lift = rgb => lum(rgb) < 0.12 ? mixRgb(rgb, [1, 1, 1], 0.13) : rgb;

/* ================= mesh data ================= */
function b64buf(s){ const bin = atob(s); const u = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i); return u.buffer; }
function bufB64(u8){ let s = ''; for (let i = 0; i < u8.length; i += 0x8000) s += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000)); return btoa(s); }
function decodeMesh(m){
  const q = new Int16Array(b64buf(m.v)), pos = new Float32Array(q.length);
  for (let i = 0; i < q.length; i += 3){ pos[i] = m.c[0] + q[i] * m.s; pos[i+1] = m.c[1] + q[i+1] * m.s; pos[i+2] = m.c[2] + q[i+2] * m.s; }
  const idx = m.i32 ? new Uint32Array(b64buf(m.i)) : new Uint16Array(b64buf(m.i));
  return {pos, idx, lo:m.lo.slice(), hi:m.hi.slice(), tris:idx.length / 3};
}
function packMesh(pos, idx){
  const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity];
  for (let i = 0; i < pos.length; i += 3) for (let k = 0; k < 3; k++){ const v = pos[i+k]; if (v < lo[k]) lo[k] = v; if (v > hi[k]) hi[k] = v; }
  const c = [0, 1, 2].map(k => (lo[k] + hi[k]) / 2), s = Math.max(1e-6, ...[0, 1, 2].map(k => (hi[k] - lo[k]) / 2)) / 32767;
  const q = new Int16Array(pos.length);
  for (let i = 0; i < pos.length; i += 3) for (let k = 0; k < 3; k++) q[i+k] = Math.round((pos[i+k] - c[k]) / s);
  const big = pos.length / 3 >= 65536, I = big ? Uint32Array.from(idx) : Uint16Array.from(idx);
  return {c, s, v:bufB64(new Uint8Array(q.buffer)), i:bufB64(new Uint8Array(I.buffer)), i32:big, lo, hi, tris:idx.length / 3};
}
const MESH = {};
const RAW = JSON.parse(document.getElementById('mesh-data').textContent);
for (const k in RAW) MESH[k] = decodeMesh(RAW[k]);

/* ================= rigid poses ================= */
const I3 = [1,0,0, 0,1,0, 0,0,1];
const RX180 = [1,0,0, 0,-1,0, 0,0,-1], RY180 = [-1,0,0, 0,1,0, 0,0,-1], RZ180 = [-1,0,0, 0,-1,0, 0,0,1], RZ90 = [0,-1,0, 1,0,0, 0,0,1];
const RX90 = [1,0,0, 0,0,-1, 0,1,0], RY90 = [0,0,1, 0,1,0, -1,0,0];
const ROT = [RX90, RY90, [0,-1,0, 1,0,0, 0,0,1]];
function m3(a, b){ const o = new Array(9); for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) o[r*3+c] = a[r*3]*b[c] + a[r*3+1]*b[3+c] + a[r*3+2]*b[6+c]; return o; }
const mv = (R, v) => [R[0]*v[0]+R[1]*v[1]+R[2]*v[2], R[3]*v[0]+R[4]*v[1]+R[5]*v[2], R[6]*v[0]+R[7]*v[1]+R[8]*v[2]];
const mtv = (R, v) => [R[0]*v[0]+R[3]*v[1]+R[6]*v[2], R[1]*v[0]+R[4]*v[1]+R[7]*v[2], R[2]*v[0]+R[5]*v[1]+R[8]*v[2]];
const add = (a, b) => [a[0]+b[0], a[1]+b[1], a[2]+b[2]];
const subv = (a, b) => [a[0]-b[0], a[1]-b[1], a[2]-b[2]];
const scl = (a, s) => [a[0]*s, a[1]*s, a[2]*s];
const dot = (a, b) => a[0]*b[0] + a[1]*b[1] + a[2]*b[2];
const crs = (a, b) => [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]];
const nrm = a => { const l = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0]/l, a[1]/l, a[2]/l]; };
const pose = (R, t) => ({R, t});
const comp = (a, b) => ({R:m3(a.R, b.R), t:add(mv(a.R, b.t), a.t)});
const papply = (p, v) => add(mv(p.R, v), p.t);
const ptrans = (p, d) => ({R:p.R, t:add(p.t, d)});
function poseMat(p){ const R = p.R, t = p.t; return new Float32Array([R[0],R[3],R[6],0, R[1],R[4],R[7],0, R[2],R[5],R[8],0, t[0],t[1],t[2],1]); }

/* ================= parts and slots ================= */
/* Frame poses come from the screw holes: each beam's end tabs land on the insert holes in the posts and side rails.
   The frame is a stack of levels. A post level puts one post on each corner (all the same height); a support-extension
   level puts one 1U support extension on each side. Every post size shares one profile and hole pattern, with insert
   holes 10 mm from each end, so levels stack straight on top of each other and the top frame rides on the stack. */
const CORNERS = [
  {c:'FL', R:I3, x:-PX, y:17.5, ex:[-1,-1]}, {c:'FR', R:RY180, x:PX, y:17.5, ex:[1,-1]},
  {c:'RL', R:RX180, x:-PX, y:DEPTH-17.5, ex:[-1,1]}, {c:'RR', R:RZ180, x:PX, y:DEPTH-17.5, ex:[1,1]}];
const CORNER_NAME = {FL:'Front-left', FR:'Front-right', RL:'Rear-left', RR:'Rear-right'};
function bottomSlots(){ return [
  {id:'BF', type:'beam_bottom', label:'Bottom front beam', R:I3, t:[0,27.425,-7.575], ex:[0,-1,-0.7]},
  {id:'BR', type:'beam_bottom', label:'Bottom rear beam', R:RZ180, t:[0,DEPTH-27.425,-7.575], ex:[0,1,-0.7]},
  {id:'BLR', type:'side_rail', label:'Bottom-left side rail', R:RX180, t:[-PX,120,-17.5], ex:[-1,0,-0.7]},
  {id:'BRR', type:'side_rail', label:'Bottom-right side rail', R:RY180, t:[PX,120,-17.5], ex:[1,0,-0.7]},
  {id:'PB', type:'panel_bottom', label:'Bottom panel', R:I3, t:[0,120,-31.5], ex:[0,0,-1.5]},
  {id:'FTFL', type:'foot', label:'Front-left foot', R:I3, t:[-124.73,55,-41], ex:[0,0,-1.3]},
  {id:'FTFR', type:'foot', label:'Front-right foot', R:I3, t:[124.73,55,-41], ex:[0,0,-1.3]},
  {id:'FTRL', type:'foot', label:'Rear-left foot', R:I3, t:[-124.73,185,-41], ex:[0,0,-1.3]},
  {id:'FTRR', type:'foot', label:'Rear-right foot', R:I3, t:[124.73,185,-41], ex:[0,0,-1.3]}]; }
function topSlots(dz, lift){ return [
  {id:'TF', type:'beam_top_front', label:'Top front beam', R:I3, t:[0,27.425,229.825 + dz], ex:[0,-1,0.7 + lift]},
  {id:'TR', type:'beam_top_rear', label:'Top rear beam', R:RZ180, t:[0,DEPTH-27.425,229.825 + dz], ex:[0,1,0.7 + lift]},
  {id:'TLR', type:'side_rail', label:'Top-left side rail', R:I3, t:[-PX,120,239.75 + dz], ex:[-1,0,0.7 + lift]},
  {id:'TRR', type:'side_rail', label:'Top-right side rail', R:RZ180, t:[PX,120,239.75 + dz], ex:[1,0,0.7 + lift]},
  {id:'PT', type:'panel_top', label:'Top panel', R:I3, t:[0,120,253.75 + dz], ex:[0,0,1.5 + lift]},
  {id:'HL', type:'handle', label:'Left handle', R:I3, t:[-124.789,120,276 + dz], ex:[0,0,1.3 + lift]},
  {id:'HR', type:'handle', label:'Right handle', R:RZ180, t:[124.789,120,276 + dz], ex:[0,0,1.3 + lift]}]; }
const levelU = l => l.k === 'mod' ? 1 : l.u;
function levelSlots(i, l, z0){
  const n = levelU(l), zc = z0 + n * U / 2, lift = 0.4 * i, k0 = Math.round(z0 / U), out = [];
  if (l.k === 'post'){
    for (const c of CORNERS) out.push({id:`P${i}${c.c}`, type:'post' + n, level:i, span:[k0, n], code:c.c, label:`${CORNER_NAME[c.c]} ${n}U post`, R:c.R, t:[c.x, c.y, zc], ex:[c.ex[0], c.ex[1], lift]});
    out.push({id:`S${i}L`, type:'panel' + n, level:i, span:[k0, n], label:`Left ${n}U side panel`, R:RZ90, t:[-138.48, 120, zc], ex:[-1.7, 0, lift]},
             {id:`S${i}R`, type:'panel' + n, level:i, span:[k0, n], label:`Right ${n}U side panel`, R:RZ90, t:[138.48, 120, zc], ex:[1.7, 0, lift]});
  } else {
    /* the 1U support extension: a 1U post section at each end joined by a full-depth side web; its tabs land on the
       insert holes at the top of the level below and the bottom of the level above (4 × M6 per side) */
    out.push({id:`M${i}L`, type:'ext_module', level:i, span:[k0, 1], label:'Left 1U support extension', R:I3, t:[-PX, 120, zc], ex:[-1.4, 0, lift]},
             {id:`M${i}R`, type:'ext_module', level:i, span:[k0, 1], label:'Right 1U support extension', R:RZ180, t:[PX, 120, zc], ex:[1.4, 0, lift]});
  }
  return out;
}
let SLOTS = [], SLOT = {};
function buildSlots(){
  const L = S ? S.levels : [];
  RU = L.reduce((s, l) => s + levelU(l), 0);
  SLOTS = bottomSlots(); let z = 0;
  L.forEach((l, i) => { SLOTS.push(...levelSlots(i, l, z)); z += levelU(l) * U; });
  SLOTS.push(...topSlots((RU - BASE_U) * U, 0.4 * L.length));
  SLOTS.push(...accessorySlots());
  SLOT = Object.fromEntries(SLOTS.map(s => [s.id, s]));
  if (glReady) buildLines();
}
const slotLevel = id => { const m = /^[PMS](\d+)/.exec(id || ''); return m ? +m[1] : -1; };
const POSTS = [{code:'FL', x:-HOLE_X, y0:0, y1:6}, {code:'FR', x:HOLE_X, y0:0, y1:6}, {code:'RL', x:-HOLE_X, y0:DEPTH-6, y1:DEPTH}, {code:'RR', x:HOLE_X, y0:DEPTH-6, y1:DEPTH}];

const POSTS_SRC = 'LabRax1-5UPostsPanels';
const TYPES = {
  beam_bottom:{name:'Bottom beam', fg:'base', meshes:[['beam_bottom','frame']], src:'Bottom Front Edge · 5ULabRaxX2D', hint:'front or rear, under the posts'},
  side_rail:{name:'Side rail', fg:'base', meshes:[['side_rail','frame']], src:'Top Left Edge · 5ULabRaxX2D', hint:'left or right, top or bottom'},
  panel_bottom:{name:'Bottom panel', fg:'base', meshes:[['panel_bottom','panel']], src:'Bottom Panel · 5ULabRaxX2D', hint:'slides into the bottom rails'},
  foot:{name:'Foot', fg:'base', meshes:[['foot','foot']], src:'Right Front Foot · 5ULabRaxX2D', hint:'under the bottom rails'},
  ext_module:{name:'1U support extension', fg:'stack', meshes:[['ext1u','frame']], src:'1U Support Extension · Lab Rax Upgraded 1U Extension Module', hint:'goes in any joint; move it up or down'},
  beam_top_front:{name:'Top front beam (logo)', fg:'top', meshes:[['beam_top_a','frame']], src:'Top Front Edge · 5ULabRaxX2D', hint:'rides on top of the stack'},
  beam_top_rear:{name:'Top rear beam', fg:'top', meshes:[['beam_top_b','frame']], src:'Top Front Edge (plain) · 5ULabRaxX2D', hint:'rides on top of the stack'},
  panel_top:{name:'Top panel, 120 mm fan', fg:'top', meshes:[['panel_top','panel']], src:'Top Panel · 5ULabRaxX2D', hint:'slides into the top rails'},
  handle:{name:'Handle', fg:'top', meshes:[['handle','frame']], src:'Left Handle · 5ULabRaxX2D', hint:'screws into the top rails'},
  cm1000_face:{name:'CM1000 faceplate', group:'cm1000', kind:'gear', hU:1, defU:0, color:'blue', meshes:[['cm1000_face','gear'],['cm1000_pipes','pipe']], count:1,
    mount:pose(I3, [-127, -3, 0]), src:'CM1000_LabRax_faceplate'},
  cm1000_rail_l:{name:'CM1000 left rail', group:'cm1000', kind:'attach', parent:'cm1000_face', color:'blue', shade:.22, meshes:[['cm1000_rail_l','gear']], count:1, src:'CM1000_LabRax_rails_v2 · rail L'},
  cm1000_rail_r:{name:'CM1000 right rail', group:'cm1000', kind:'attach', parent:'cm1000_face', color:'blue', shade:.22, meshes:[['cm1000_rail_r','gear']], count:1, src:'CM1000_LabRax_rails_v2 · rail R'}
};
for (let n = 5; n >= 1; n--){
  TYPES['post' + n] = {name:`Post, ${n}U`, fg:'stack', size:n, meshes:[[n === 5 ? 'post' : `post${n}u`, 'frame']], src:n === 5 ? 'Rack Edge · 5ULabRaxX2D (same as the 5U post in ' + POSTS_SRC + ')' : `${n}U Vertical Post · ${POSTS_SRC}`, hint:'one per corner, stacks on top'};
  TYPES['panel' + n] = {name:`Side panel, ${n}U`, fg:'panels', size:n, meshes:[[n === 5 ? 'panel_side' : `panel_side${n}u`, 'side']], src:`${n}U Side Panel · ${n === 5 ? '5ULabRaxX2D' : POSTS_SRC}`, hint:`fits a ${n}U post level`};
}
for (const k in TYPES){ const T = TYPES[k]; T.key = k; if (!T.kind){ T.kind = 'frame'; T.group = 'frame'; T.bin = true; } }
const isPanelSide = k => /^panel\d$/.test(k);
const FGROUPS = [['base','Base','goes in first, under the posts'],['stack','Posts and extensions','stack level by level from the base up'],['panels','Side panels','one per side of a post level'],['top','Top','rides on top of the stack']];
const GROUPS = [
  {id:'frame', title:'Lab Rax frame', sub:'5ULabRaxX2D + posts + extensions'},
  {id:'cm1000', title:'CM1000 bracket', sub:'faceplate + rails'},
  {id:'import', title:'Imported', sub:'STL / 3MF'}
];
const STACK_PRESETS = {nine:[{k:'post',u:5},{k:'mod'},{k:'post',u:3}], eight:[{k:'post',u:5},{k:'post',u:3}], five:[{k:'post',u:5}]};
let INST = [];
const instById = id => INST.find(i => i.id === id);
function rebuildInstances(){
  INST = [];
  for (const k in TYPES){ const T = TYPES[k]; if (T.bin) continue; for (let i = 0; i < T.count; i++) INST.push({id: T.group === 'import' ? 'imp-' + k.slice(4) : k + '-' + (i + 1), type:k}); }
  if (S) for (const [id, type] of Object.entries(S.frame)) if (TYPES[type] && TYPES[type].bin) INST.push({id, type});
}
function stackText(levels = S.levels){
  if (!levels.length) return 'no posts yet';
  return levels.map(l => l.k === 'mod' ? '1U support' : l.u + 'U posts').join(' + ');
}
/* ================= equipment, inserts, accessories, cables ================= */
/* Primitive mesh builders for the equipment models (boxes and cylinders, merged per material) */
function meshBuilder(){
  const pos = [], idx = [];
  const api = {
    box(lo, hi){
      const b = pos.length / 3, [x0,y0,z0] = lo, [x1,y1,z1] = hi;
      pos.push(x0,y0,z0, x1,y0,z0, x1,y1,z0, x0,y1,z0, x0,y0,z1, x1,y0,z1, x1,y1,z1, x0,y1,z1);
      for (const f of [[0,2,1,0,3,2],[4,5,6,4,6,7],[0,1,5,0,5,4],[1,2,6,1,6,5],[2,3,7,2,7,6],[3,0,4,3,4,7]]) for (const i of f) idx.push(b + i);
      return api;
    },
    cyl(c, r, h, axis = 2, seg = 20){ // axis: 0 x, 1 y, 2 z; c = centre of the bottom cap
      const b = pos.length / 3, P = (a, s, t) => { const v = [0,0,0]; const o = [(axis + 1) % 3, (axis + 2) % 3]; v[o[0]] = Math.cos(a) * r; v[o[1]] = Math.sin(a) * r; v[axis] = t; return [c[0] + v[0], c[1] + v[1], c[2] + v[2]]; };
      for (let i = 0; i < seg; i++){ const a = i / seg * Math.PI * 2; pos.push(...P(a, 0, 0), ...P(a, 0, h)); }
      const c0 = pos.length / 3; const cc = [...c]; pos.push(...cc); const cc2 = [...c]; cc2[axis] += h; pos.push(...cc2);
      for (let i = 0; i < seg; i++){ const j = (i + 1) % seg, a = b + i * 2, bb = b + j * 2; idx.push(a, bb, a + 1, bb, bb + 1, a + 1, c0, bb, a, c0 + 1, a + 1, bb + 1); }
      return api;
    },
    tube(c, ro, ri, h, axis = 1, seg = 20){ // ring (heat-set insert)
      const b = pos.length / 3, P = (a, r, t) => { const v = [0,0,0]; const o = [(axis + 1) % 3, (axis + 2) % 3]; v[o[0]] = Math.cos(a) * r; v[o[1]] = Math.sin(a) * r; v[axis] = t; return [c[0] + v[0], c[1] + v[1], c[2] + v[2]]; };
      for (let i = 0; i < seg; i++){ const a = i / seg * Math.PI * 2; pos.push(...P(a, ro, 0), ...P(a, ro, h), ...P(a, ri, 0), ...P(a, ri, h)); }
      for (let i = 0; i < seg; i++){ const j = (i + 1) % seg, A = b + i * 4, B = b + j * 4;
        idx.push(A, B, A + 1, B, B + 1, A + 1,  A + 2, A + 3, B + 2, B + 2, A + 3, B + 3,  A, A + 2, B, B, A + 2, B + 2,  A + 1, B + 1, A + 3, B + 1, B + 3, A + 3); }
      return api;
    },
    done(){
      const P = new Float32Array(pos), lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity];
      for (let i = 0; i < P.length; i += 3) for (let k = 0; k < 3; k++){ lo[k] = Math.min(lo[k], P[i + k]); hi[k] = Math.max(hi[k], P[i + k]); }
      return {pos:P, idx:new Uint32Array(idx), lo, hi, tris:idx.length / 3};
    },
    empty(){ return !idx.length; }
  };
  return api;
}
const DEVMESH = {};

/* Port kinds: the visible connector size and the cable family it takes */
const PORT = {
  rj45:{name:'Ethernet (RJ45)', w:16, h:13.5, color:'#e2b33c', cable:'cat6'},
  coax:{name:'Coax (F)', r:4.8, len:9, color:'#c3c7c9', cable:'coax'},
  dc:{name:'DC power', r:4, len:3, color:'#c8322b', cable:'dc'},
  usbc:{name:'USB-C', w:9, h:3.5, color:'#7b4fb0', cable:'dc'},
  usba:{name:'USB-A', w:14, h:6.5, color:'#1f5fbf', cable:'usb'},
  hdmi:{name:'micro HDMI', w:7.5, h:3.5, color:'#2e8b3e', cable:'hdmi'},
  dp:{name:'DisplayPort', w:17, h:6, color:'#2e8b3e', cable:'hdmi'},
  audio:{name:'3.5 mm audio', r:3, len:1.5, color:'#e58fa6', cable:'misc'},
  btn:{name:'button', r:3, len:1, color:'#7a848a', cable:null},
  ac:{name:'AC outlet', w:30, h:34, color:'#3a3f42', cable:'ac'},
  ant:{name:'antenna connector', r:3.2, len:6, color:'#c3c7c9', cable:null},
  run:{name:'in-wall run', r:3, len:6, color:'#e2b33c', cable:'cat6'}
};
const CABLE = {
  cat6:{name:'Cat6', r:1.9, color:'blue', data:true},
  coax:{name:'RG6 coax', r:3.4, color:'white', data:true},
  dc:{name:'DC / adapter cord', r:1.6, color:'black', data:false},
  ac:{name:'AC cord', r:3.1, color:'black', data:false},
  usb:{name:'USB', r:2, color:'slate', data:true},
  hdmi:{name:'Video', r:2.4, color:'slate', data:true},
  misc:{name:'Cable', r:1.8, color:'slate', data:true}
};
const PATCH_SIZES = [[152,'6″'],[305,'1 ft'],[457,'1.5 ft'],[610,'2 ft'],[914,'3 ft'],[1524,'5 ft'],[2134,'7 ft'],[3048,'10 ft']];

/* Equipment. Sizes in mm, x = width (left to right as you face the front), y = depth (front to back), z = height.
   Port positions are on a face: front/rear use (x, z), left/right use (y, z), top/bottom use (x, y). ≈ marks a
   position I placed from the maker's port list rather than measured; check those against the real unit. */
const DEVICES = [
  {key:'dev_cm1000', name:'Netgear CM1000 modem', short:'CM1000', zone:'attach', parent:'cm1000_face', origin:[52, 16, 4],
   W:150, D:220, H:36, color:'#2a2d30', hU:1,
   src:'Netgear CM1000 datasheet: 223.5 × 88.9 × 150 mm with the stand', approx:'Body size and the order of the rear ports are approximate.',
   mount:'Lies on its side in the CM1000 bracket (U9). The bracket’s bay (183.6 mm wide, 1U tall, open at the back) only fits the modem with its length running front to back, so the LED end sits against the faceplate’s light pipes and every cable leaves from the far end at the back of the rack.',
   ports:[{id:'coax', label:'Coax in', k:'coax', f:'rear', u:30, v:18, approx:1},{id:'eth', label:'Ethernet (LAN)', k:'rj45', f:'rear', u:62, v:18, approx:1},
          {id:'pwr', label:'Power in', k:'dc', f:'rear', u:92, v:18, approx:1},{id:'btn', label:'Power button', k:'btn', f:'rear', u:112, v:18, approx:1}]},
  {key:'dev_keystone', name:'½U keystone panel (12)', short:'Keystones', zone:'rack', hU:.5, side:'full', dep:'front', mountY:-3, floor:0,
   W:254, D:30, H:22.2, color:'#2b2f31', shape:'keystone', def:{U:2, half:'lower'},
   src:'MakerWorld ½U 12-port keystone panel', mount:'Lower half of U2. Keystones 3–9 are used, each directly above its switch port, so every front patch is a 6″ cable straight down. The device runs plug into the back of each jack.',
   ports:[...Array(12).keys()].flatMap(i => [{id:'f' + (i + 1), label:`Keystone ${i + 1} · front`, k:'rj45', f:'front', u:127 - 96.25 + i * 17.5, v:11.1},
                                              {id:'r' + (i + 1), label:`Keystone ${i + 1} · back`, k:'rj45', f:'rear', u:127 - 96.25 + i * 17.5, v:11.1}])},
  {key:'dev_switch', name:'TP-Link TL-SG108E switch', short:'Switch', zone:'rack', hU:1, side:'full', dep:'front', mountY:2, floor:9,
   W:158, D:101, H:25, color:'#3a3d40', def:{U:3},
   src:'TP-Link: 158 × 101 × 25 mm, 9 V 0.6 A adapter. TL-SG108 user guide: ports and LEDs on the front panel, power socket on the right side of the rear panel.',
   mount:'U3 in the SG108 Keystone mount, ports facing the front through the faceplate. The power socket is on the rear panel at the left end as you face the front (the right end seen from behind), so the power cord leaves from the back.',
   ports:[...Array(8).keys()].map(i => ({id:'p' + (i + 1), label:`Port ${i + 1}`, k:'rj45', f:'front', u:20 + i * 16.9, v:12})).concat([{id:'pwr', label:'Power in (9 V)', k:'dc', f:'rear', u:16, v:12.5}])},
  {key:'dev_optiplex', name:'Dell OptiPlex 7060 Micro', short:'OptiPlex', zone:'rack', hU:1, side:'full', dep:'full', mountY:1, floor:4,
   W:182, D:178, H:36, color:'#2b2e31', def:{U:4},
   src:'Expert Reviews: 182 × 36 × 178 mm. Dell visual guide: rear has power, Ethernet, 2 × DisplayPort, 4 × USB 3.1, antenna and an option slot; front has USB-A, USB-C and audio.',
   approx:'The rear ports are in Dell’s order but their exact spacing is approximate.',
   mount:'U4, lying flat in the flush-front mount. Power (65 W brick, 4.5 mm barrel), Ethernet, DisplayPort and USB all leave from the rear.',
   ports:[{id:'pbtn', label:'Power button', k:'btn', f:'front', u:12, v:26},{id:'fusba', label:'USB-A (front)', k:'usba', f:'front', u:32, v:16},{id:'fusbc', label:'USB-C (front)', k:'usbc', f:'front', u:50, v:16},
          {id:'audio', label:'Audio', k:'audio', f:'front', u:64, v:22},
          {id:'ant', label:'Antenna', k:'ant', f:'rear', u:12, v:26, approx:1},{id:'usb1', label:'USB 3.1 · rear 1', k:'usba', f:'rear', u:40, v:12, approx:1},{id:'usb2', label:'USB 3.1 · rear 2', k:'usba', f:'rear', u:40, v:24, approx:1},
          {id:'usb3', label:'USB 3.1 · rear 3', k:'usba', f:'rear', u:58, v:12, approx:1},{id:'eth', label:'Ethernet', k:'rj45', f:'rear', u:82, v:18, approx:1},{id:'usb4', label:'USB 3.1 · rear 4 (SmartPower)', k:'usba', f:'rear', u:104, v:18, approx:1},
          {id:'dp1', label:'DisplayPort 1', k:'dp', f:'rear', u:128, v:12, approx:1},{id:'dp2', label:'DisplayPort 2', k:'dp', f:'rear', u:128, v:25, approx:1},{id:'pwr', label:'Power in (19.5 V)', k:'dc', f:'rear', u:164, v:18, approx:1}]},
  {key:'dev_ssd', name:'500 GB SSD + USB-SATA', short:'SSD', zone:'rack', hU:1, side:'half', dep:'front', mountY:8, floor:5,
   W:69.85, D:118, H:7, color:'#9aa1a6', shape:'drive', def:{U:5, side:'L'},
   src:'2.5″ drive (100 × 69.85 × 7 mm) with a short USB-SATA adapter', mount:'U5, left bay of the four-drive rack. The adapter’s USB lead goes to an OptiPlex rear USB port.',
   ports:[{id:'usb', label:'USB lead', k:'usba', f:'rear', u:35, v:4}]},
  {key:'dev_hdd', name:'500 GB HDD + USB-SATA', short:'HDD', zone:'rack', hU:1, side:'half', dep:'front', mountY:8, floor:5,
   W:69.85, D:118, H:9.5, color:'#9aa1a6', shape:'drive', def:{U:5, side:'R'},
   src:'2.5″ drive (100 × 69.85 × 9.5 mm) with a short USB-SATA adapter', mount:'U5, right bay of the four-drive rack. The adapter’s USB lead goes to an OptiPlex rear USB port.',
   ports:[{id:'usb', label:'USB lead', k:'usba', f:'rear', u:35, v:4.5}]},
  {key:'dev_brick', name:'Dell 65 W power brick', short:'PC brick', zone:'rack', hU:1, side:'half', dep:'rear', mountY:130, floor:4,
   W:46, D:108, H:29, color:'#26292b', def:{U:5, side:'L'},
   src:'Dell 65 W adapter, about 108 × 46 × 29 mm (estimate)', approx:'Size is an estimate.',
   mount:'Strapped to the U5 drive rack behind the drives. Its DC lead runs to the OptiPlex; its AC cord runs to the power strip.',
   ports:[{id:'dc', label:'DC lead to the PC', k:'dc', f:'front', u:23, v:14},{id:'ac', label:'AC cord', k:'ac', f:'rear', u:23, v:14}]},
  {key:'dev_hue', name:'Philips Hue Bridge v2', short:'Hue Bridge', zone:'rack', hU:1, side:'half', dep:'front', mountY:6, floor:9,
   W:88, D:88, H:26, color:'#efefea', def:{U:6, side:'L'},
   src:'Hue Bridge v2: 88 × 88 × 26 mm', approx:'Port spacing on the rear edge is approximate.',
   mount:'U6, left side of the Hue + Pi tray. Ethernet and power are on its rear edge, facing the back of the rack.',
   ports:[{id:'eth', label:'Ethernet', k:'rj45', f:'rear', u:30, v:12, approx:1},{id:'pwr', label:'Power in', k:'dc', f:'rear', u:60, v:12, approx:1}]},
  {key:'dev_pi4', name:'Raspberry Pi 4', short:'Pi 4', zone:'rack', hU:1, side:'half', dep:'front', mountY:10, floor:6,
   W:56, D:85.6, H:17, color:'#2e6b3a', shape:'pi', def:{U:6, side:'R'},
   src:'Raspberry Pi 4 mechanical drawing (85.6 × 56 mm board)', mount:'U6, right side of the Hue + Pi tray, on 6 mm standoffs. SD card at the front, Ethernet and USB facing the rear, USB-C and micro HDMI facing the right post.',
   ports:[{id:'eth', label:'Ethernet', k:'rj45', f:'rear', u:10.25, v:8.3},{id:'usb3a', label:'USB 3 (upper)', k:'usba', f:'rear', u:29, v:10.5},{id:'usb3b', label:'USB 3 (lower)', k:'usba', f:'rear', u:29, v:3.5},
          {id:'usb2a', label:'USB 2 (upper)', k:'usba', f:'rear', u:47, v:10.5},{id:'usb2b', label:'USB 2 (lower)', k:'usba', f:'rear', u:47, v:3.5},
          {id:'pwr', label:'USB-C power (5 V 3 A)', k:'usbc', f:'right', u:11.2, v:3},{id:'hdmi0', label:'micro HDMI 0', k:'hdmi', f:'right', u:26, v:3},{id:'hdmi1', label:'micro HDMI 1', k:'hdmi', f:'right', u:39.5, v:3}]},
  {key:'dev_gwifi', name:'Google Wifi (2020)', short:'Google Wifi', zone:'top', W:105, D:105, H:69, color:'#f2f2ee', shape:'cyl', def:{top:1},
   src:'Google Wifi (GJ2CQ): about 105 mm across and 69 mm tall', approx:'Port spacing at the base is approximate.',
   mount:'On the top panel with the twist-lock ceiling mount. The power barrel and both Ethernet ports sit low on the back.',
   ports:[{id:'wan', label:'WAN (to modem)', k:'rj45', f:'rear', u:34, v:10, approx:1},{id:'lan', label:'LAN', k:'rj45', f:'rear', u:54, v:10, approx:1},{id:'pwr', label:'Power in', k:'dc', f:'rear', u:72, v:10, approx:1}]},
  {key:'dev_moca', name:'ScreenBeam ECB6250 MoCA adapter', short:'MoCA', zone:'wall', W:56, D:28, H:114, color:'#e4e5e1', def:{wall:[-62, 'U7']},
   src:'ScreenBeam ECB6250: 56 × 28 × 114 mm', approx:'Which end the ports are on is approximate.',
   mount:'On the wall behind U7. Coax, Ethernet and power on its top end.',
   ports:[{id:'coax', label:'Coax', k:'coax', f:'top', u:14, v:14, approx:1},{id:'eth', label:'Ethernet', k:'rj45', f:'top', u:34, v:14, approx:1},{id:'pwr', label:'Power in', k:'dc', f:'top', u:49, v:14, approx:1}]},
  {key:'dev_splitter', name:'MoCA 2-way splitter', short:'Splitter', zone:'wall', W:38, D:20, H:64, color:'#c9cdd0', def:{wall:[56, 'U7']},
   src:'ScreenBeam 2-way splitter, 5–1675 MHz', mount:'On the wall behind U7, between the upper grommet and the modem. IN at the bottom, two outputs on top.',
   ports:[{id:'in', label:'IN (from the wall)', k:'coax', f:'bottom', u:19, v:10},{id:'out1', label:'OUT 1', k:'coax', f:'top', u:10, v:10},{id:'out2', label:'OUT 2', k:'coax', f:'top', u:28, v:10}]},
  {key:'dev_grommet', name:'Wall plate (in-wall runs)', short:'Wall runs', zone:'wall', W:34, D:6, H:34, color:'#5a6064', shape:'grommet', def:{wall:[0, 'U8']},
   src:'Wall plate where the in-wall runs come out', mount:'Behind the rack where the in-wall runs come out: the office PC run, the work-laptop run and the coax from outside.',
   ports:[{id:'pc', label:'Office PC run', k:'run', f:'front', u:9, v:23},{id:'laptop', label:'Work laptop run', k:'run', f:'front', u:25, v:23},{id:'coax', label:'Coax from outside', k:'coax', f:'front', u:17, v:9}]},
  {key:'dev_strip', name:'6-outlet switched power strip', short:'Power strip', zone:'wall', W:350, D:38, H:65, color:'#b8bcbe', def:{wall:[0, -130]},
   src:'Metal 6-outlet surge strip, 350 × 65 mm', mount:'On the wall below the rack: outlets along the top edge with ground holes up, switches along the bottom, cord out of the left end.',
   ports:[...Array(6).keys()].map(i => ({id:'o' + (i + 1), label:`Outlet ${i + 1}`, k:'ac', f:'front', u:45 + i * 52, v:42})).concat([{id:'cord', label:'Cord to the wall', k:'ac', f:'left', u:19, v:32}])}
];
const DEV = Object.fromEntries(DEVICES.map(d => [d.key, d]));
const ZONE_NAME = {rack:'snaps to a U', top:'sits on top of the rack', wall:'goes on the wall', attach:'goes in its bracket'};

/* Build each device's mesh: a body plus coloured port connectors (one GPU mesh per material) */
function devFacePoint(d, f, u, v, out = 0){
  switch (f){
    case 'front': return [u, -out, v]; case 'rear': return [u, d.D + out, v];
    case 'left': return [-out, u, v]; case 'right': return [d.W + out, u, v];
    case 'top': return [u, v, d.H + out]; case 'bottom': return [u, v, -out];
  }
  return [u, 0, v];
}
const FACE_DIR = {front:[0,-1,0], rear:[0,1,0], left:[-1,0,0], right:[1,0,0], top:[0,0,1], bottom:[0,0,-1]};
function buildDeviceMeshes(d){
  const body = meshBuilder(), trim = meshBuilder(), ports = {};
  const {W, D, H} = d;
  if (d.shape === 'cyl'){ body.cyl([W / 2, D / 2, 0], W / 2, H, 2, 40); }
  else if (d.shape === 'pi'){
    body.box([0, 0, 6], [W, D, 7.6]);                          // board on standoffs
    for (const [x, y] of [[3.5, 3.5], [52.5, 3.5], [3.5, 61.5], [52.5, 61.5]]) trim.cyl([x, y, 0], 2.6, 6, 2, 10);
    trim.box([2, D - 21, 7.6], [18.5, D + 2, 21]);             // Ethernet jack
    trim.box([21, D - 17, 7.6], [37, D + 2, 23]);              // USB 3 stack
    trim.box([39, D - 17, 7.6], [55, D + 2, 23]);              // USB 2 stack
    trim.box([20, 26, 7.6], [35, 41, 9]);                      // SoC
  } else if (d.shape === 'drive'){
    body.box([0, 0, 0], [W, 100, H]);
    trim.box([W / 2 - 25, 100, 0], [W / 2 + 25, D, 9]);        // USB-SATA adapter
  } else if (d.shape === 'keystone'){
    body.box([0, 0, 0], [W, 3, H]);                            // panel with ears
    for (let i = 0; i < 12; i++){ const x = 127 - 96.25 + i * 17.5; trim.box([x - 7.5, 3, 2], [x + 7.5, D, H - 2]); }
  } else if (d.shape === 'grommet'){
    body.cyl([W / 2, 0, H / 2], 17, 3, 1, 28);
  } else body.box([0, 0, 0], [W, D, H]);
  for (const p of d.ports){
    const K = PORT[p.k], m = ports[p.k] || (ports[p.k] = meshBuilder()), c = devFacePoint(d, p.f, p.u, p.v, 0), n = FACE_DIR[p.f];
    if (K.r){ const axis = n[0] ? 0 : n[1] ? 1 : 2, sgn = n[axis]; const c2 = c.slice(); c2[axis] += sgn < 0 ? -K.len : 0; m.cyl(c2, K.r, K.len, axis, 16); }
    else {
      const ax = n[0] ? 0 : n[1] ? 1 : 2, sgn = n[ax], lo = c.slice(), hi = c.slice();
      const o = [0,1,2].filter(k => k !== ax), size = p.f === 'top' || p.f === 'bottom' ? [K.w, K.h] : [K.w, K.h];
      lo[o[0]] -= size[0] / 2; hi[o[0]] += size[0] / 2; lo[o[1]] -= size[1] / 2; hi[o[1]] += size[1] / 2;
      if (p.f === 'left' || p.f === 'right'){ lo[o[0]] = c[o[0]] - K.w / 2; hi[o[0]] = c[o[0]] + K.w / 2; }
      lo[ax] = c[ax] + (sgn < 0 ? -1.6 : -0.4); hi[ax] = c[ax] + (sgn < 0 ? 0.4 : 1.6);
      m.box(lo, hi);
    }
  }
  const out = [];
  const o = d.origin || [0,0,0];
  const shift = m => { for (let i = 0; i < m.pos.length; i += 3){ m.pos[i] += o[0]; m.pos[i+1] += o[1]; m.pos[i+2] += o[2]; } for (let k = 0; k < 3; k++){ m.lo[k] += o[k]; m.hi[k] += o[k]; } return m; };
  DEVMESH['dev:' + d.key + ':body'] = shift(body.done()); out.push(['dev:' + d.key + ':body', 'dev']);
  if (!trim.empty()){ DEVMESH['dev:' + d.key + ':trim'] = shift(trim.done()); out.push(['dev:' + d.key + ':trim', 'devtrim']); }
  for (const k in ports){ DEVMESH['dev:' + d.key + ':p:' + k] = shift(ports[k].done()); out.push(['dev:' + d.key + ':p:' + k, 'port:' + k]); }
  return out;
}
for (const d of DEVICES){
  TYPES[d.key] = {key:d.key, name:d.name, group:'equip', kind:d.zone === 'attach' ? 'attach' : 'gear', parent:d.parent || null, hU:d.hU || 1, dev:d,
    count:1, meshes:buildDeviceMeshes(d), src:d.src};
}
GROUPS.splice(2, 0, {id:'equip', title:'Equipment', sub:'your actual devices'});
{ const m = meshBuilder().tube([0, 0, 0], 4, 3, 4, 1, 18).done(); DEVMESH['dev:insert'] = m; }

/* ---- accessories in the frame builder ---- */
TYPES.cable_guide = {key:'cable_guide', name:'Cable guide', fg:'acc', meshes:[['guide','frame']], src:'Lab Rax Cable Guide · FrameCableHolder.3mf', hint:'1U on any post, 2 × M6 into inserts'};
TYPES.wall_tpl1 = {key:'wall_tpl1', name:'Wall template, 1U', fg:'acc', meshes:[['tpl1','tpl']], src:'Wall Mount Template · Lab Rax Wall Mounting Cleats', hint:'marks the wall screws for a cleat'};
TYPES.wall_tpl5 = {key:'wall_tpl5', name:'Wall template, 5U', fg:'acc', meshes:[['tpl5','tpl']], src:'Wall Mount Template · Lab Rax Wall Mounting Cleats', hint:'marks the wall screws for a cleat'};
for (const k of ['cable_guide','wall_tpl1','wall_tpl5']){ Object.assign(TYPES[k], {kind:'frame', group:'frame', bin:true}); }
FGROUPS.push(['acc','Accessories','bolt to the post holes; inserts are added for you']);
const WALL_Y = 255; // the wall behind the rack (rear posts about 15 mm off it; set by the wall cleats)
function accessorySlots(){
  const out = [];
  for (const c of CORNERS){
    const front = c.c[0] === 'F', x = c.x < 0 ? -HOLE_X : HOLE_X;
    for (let k = 0; k < RU; k++)
      out.push({id:`G${c.c}${k}`, type:'cable_guide', acc:{col:c.c, k}, span:[k, 1], code:c.c, label:`Cable guide on ${c.c}`,
        R:front ? RZ180 : I3, t:[x, front ? -14 : DEPTH + 14, k * U + U / 2], ex:[c.x < 0 ? -.6 : .6, front ? -1.2 : 1.2, 0]});
  }
  for (let k = 0; k < RU; k++) out.push({id:`W1${k}`, type:'wall_tpl1', span:[k, 1], label:'Wall template (1U)', R:I3, t:[0, WALL_Y - 1.2, k * U + U / 2], ex:[0, 1.5, 0]});
  for (let k = 0; k + 5 <= RU; k++) out.push({id:`W5${k}`, type:'wall_tpl5', span:[k, 5], label:'Wall template (5U)', R:I3, t:[0, WALL_Y - 1.2, k * U + 2.5 * U], ex:[0, 1.5, 0]});
  return out;
}
/* the screw holes a cable guide uses: a and c of its unit on its post */
const guideHoles = (col, k) => [`${col}:${k}:0`, `${col}:${k}:2`];

/* ---- heat-set inserts ---- */
const holeKey = (col, k, j) => `${col}:${k}:${j}`;
function holeWorld(key){
  const [col, k, j] = key.split(':'); const front = col[0] === 'F';
  return {p:[col[1] === 'L' ? -HOLE_X : HOLE_X, front ? 0 : DEPTH - 4, +k * U + HOLE_Z[+j]], front, col, k:+k, j:+j};
}
const holeName = key => { const h = holeWorld(key); return holeRef(h.col, h.k, h.j); };
/* holes that mounted gear and accessories screw into */
function neededHoles(){
  const need = new Map(); const addH = (key, why) => { if (!need.has(key)) need.set(key, new Set()); need.get(key).add(why); };
  for (const inst of INST){
    const a = S.at[inst.id], T = TYPES[inst.type]; if (!a || !placed(inst.id)) continue;
    if (a.s && inst.type === 'cable_guide'){ const s = SLOT[a.s]; if (s) for (const h of guideHoles(s.acc.col, s.acc.k)) addH(h, inst.id); continue; }
    if (a.u == null) continue;
    if (T.dev && (T.dev.dep === 'rear')) continue; // straps to a tray, no ears
    const hU = gearHU(inst.type), b = a.u, e = a.u + Math.round(hU * 2);
    for (let h = b; h < e; h++){
      const k = Math.floor(h / 2), upper = h % 2 === 1, full = h % 2 === 0 && h + 1 < e;
      const js = full ? [0, 2] : upper ? [0] : [2];
      if (full) h++;
      for (const j of js) for (const col of ['FL','FR']) addH(holeKey(col, k, j), inst.id);
    }
  }
  return need;
}
function insertSummary(){
  const need = neededHoles(), have = S.inserts || {};
  const missing = [...need.keys()].filter(k => !have[k]);
  return {need, have:Object.keys(have).length, missing};
}

/* ---- device poses, occupancy and placement ---- */
const CELL_X = {F:0, L:-55, R:55};
const topZ = () => (RU - BASE_U) * U + 255.25;
const wallZ = (z) => typeof z === 'string' ? (RU - +z.slice(1)) * U + U / 2 : z;
function devPose(T, a){
  const d = T.dev;
  if (a.u != null){ const cx = CELL_X[a.side || 'F'] || 0; return pose(I3, [cx - d.W / 2, d.mountY - 115 * explode, a.u * U / 2 + d.floor]); }
  if (a.top) return pose(I3, [-d.W / 2, 120 - d.D / 2, topZ() + 80 * explode]);
  if (a.wall) return pose(I3, [a.wall[0] - d.W / 2, WALL_Y - d.D + 40 * explode, wallZ(a.wall[1]) - d.H / 2]);
  return null;
}
/* rack cells a placed item fills: half-unit rows × left/right × front/rear */
function cellsFor(typeKey, a){
  const T = TYPES[typeKey]; if (!a || a.u == null) return [];
  const d = T.dev, h2 = Math.round(gearHU(typeKey) * 2);
  const sides = d && d.side === 'half' ? [a.side || 'L'] : ['L','R'];
  const deps = d && d.dep === 'rear' ? ['B'] : d && d.dep === 'front' ? ['F'] : ['F','B'];
  const out = [];
  for (let k = 0; k < h2; k++) for (const s of sides) for (const p of deps) out.push(`${a.u + k}|${s}|${p}`);
  return out;
}
/* brackets: a bracket's own devices share its cells (the CM1000 modem sits inside its bracket) */
function occupancy(exclude){
  const occ = new Map();
  for (const inst of INST){ const a = S.at[inst.id]; if (!a || a.u == null || inst.id === exclude) continue; for (const c of cellsFor(inst.type, a)) occ.set(c, inst.id); }
  return occ;
}
function cellsFree(typeKey, a, exclude){ const occ = occupancy(exclude); return cellsFor(typeKey, a).every(c => !occ.has(c)); }
function devCandidates(typeKey, instId){
  const T = TYPES[typeKey], d = T.dev, out = (T.dev.zone === 'rack' || T.dev.zone === 'top') ? bracketCandidates(typeKey, instId) : [];
  if (d.zone === 'rack'){
    const h2 = Math.round(d.hU * 2), step = d.hU % 1 ? 1 : 2;
    const sides = d.side === 'half' ? ['L','R'] : ['F'];
    for (let hb = RU * 2 - h2; hb >= 0; hb--){
      if (hb % step) continue;
      for (const side of sides){
        const at = {u:hb, side}; if (!cellsFree(typeKey, at, instId)) continue;
        const P = devPose(T, at);
        out.push({at, label:spanLabel(hb, d.hU) + (side === 'L' ? ' · left' : side === 'R' ? ' · right' : '') + (d.dep === 'rear' ? ' · rear' : ''),
          anchor:papply(P, [d.W / 2, d.dep === 'rear' ? d.D / 2 : -6, d.H / 2]), pose:P});
      }
    }
  } else if (d.zone === 'top'){
    const taken = INST.some(i => i.id !== instId && S.at[i.id] && S.at[i.id].top); if (!taken){ const at = {top:1}, P = devPose(T, at); out.push({at, label:'on top of the rack', anchor:papply(P, [d.W / 2, d.D / 2, d.H]), pose:P}); }
  } else if (d.zone === 'wall'){
    for (let x = -160; x <= 160; x += 20) for (let z = -160; z <= RU * U + 60; z += 20){
      const at = {wall:[x, z]}, P = devPose(T, at);
      out.push({at, label:`on the wall · ${x < 0 ? x + ' mm left' : x > 0 ? x + ' mm right' : 'centred'} · ${refFor([x, WALL_Y, z]).unit}`, anchor:papply(P, [d.W / 2, d.D, d.H / 2]), pose:P});
    }
  }
  return out;
}
function devWhere(id){
  const inst = instById(id), a = S.at[id], d = TYPES[inst.type].dev;
  if (a.u != null) return spanLabel(a.u, d.hU) + (a.side === 'L' ? ' · left' : a.side === 'R' ? ' · right' : '') + (d.dep === 'rear' ? ' · rear' : '');
  if (a.top) return 'On top of the rack';
  if (a.wall){ const z = wallZ(a.wall[1]); return `On the wall · ${refFor([a.wall[0], WALL_Y, z]).unit} · X ${fmt(a.wall[0], 0)} mm`; }
  if (a.p && instById(a.p)) return 'In ' + TYPES[instById(a.p).type].name + (placed(a.p) ? ' · ' + instWhere(a.p) : '');
  return '';
}
function applyPlannedLayout(){
  for (const d of DEVICES){
    const id = d.key + '-1', def = d.def; if (!instById(id)) continue;
    if (d.zone === 'attach'){ const par = INST.find(i => i.type === d.parent && placed(i.id)); if (par) S.at[id] = {p:par.id}; continue; }
    const at = defAt(d, id); if (at) S.at[id] = at;
  }
}

/* ---- ports in the world ---- */
function devPorts(instId){
  const inst = instById(instId); if (!inst) return [];
  const T = TYPES[inst.type]; if (!T.dev || !placed(instId)) return [];
  const P = worldPose(instId); if (!P) return [];
  const o = T.dev.origin || [0,0,0];
  return T.dev.ports.filter(p => PORT[p.k].cable).map(p => {
    const lp = devFacePoint(T.dev, p.f, p.u, p.v, PORT[p.k].len || 1.6);
    return {...p, inst:instId, p:papply(P, add(lp, o)), d:mv(P.R, FACE_DIR[p.f])};
  });
}
const portById = (instId, pid) => devPorts(instId).find(p => p.id === pid);

/* ---- cables ---- */
function cableKind(ka, kb){
  const s = new Set([ka, kb]);
  if (s.has('coax')) return 'coax';
  if (s.has('ac')) return [...s].every(k => k === 'ac') ? 'ac' : 'dc';
  if (s.has('dc') || (s.has('usbc') && !s.has('usba'))) return 'dc';
  if ([...s].every(k => k === 'rj45' || k === 'run')) return 'cat6';
  if (s.has('usba') || s.has('usbc')) return 'usb';
  if (s.has('hdmi') || s.has('dp')) return 'hdmi';
  return 'misc';
}
function guideZs(col){ // cable guides on a post: heights of their loops
  const zs = []; for (const i of INST){ const a = S.at[i.id]; if (i.type === 'cable_guide' && a && a.s && SLOT[a.s] && SLOT[a.s].acc.col === col) zs.push(SLOT[a.s].t[2]); }
  return zs.sort((a, b) => a - b);
}
/* Route: out of each port, back to a spine beside a rear post (data on the left, power on the right, as in the
   wiring plan), along the spine, then into the other port. Two front-facing ports get a short front patch.
   A spine with cable guides on its rear post runs through their loops. */
function routeCable(c){
  const A = portById(c.a.i, c.a.p), B = portById(c.b.i, c.b.p); if (!A || !B) return null;
  const kind = c.kind || cableKind(A.k, B.k), K = CABLE[kind];
  const out = d => scl(d, 14);
  const s = add(A.p, out(A.d)), e = add(B.p, out(B.d));
  let pts;
  const route = c.route || 'auto';
  if (route === 'direct'){ const m = scl(add(s, e), .5); m[2] -= Math.min(60, Math.hypot(...subv(s, e)) * .15); pts = [A.p, s, m, e, B.p]; }
  else if (route === 'patch' || (route === 'auto' && A.d[1] < -.6 && B.d[1] < -.6 && A.p[1] < 30 && B.p[1] < 30)){
    const m = scl(add(s, e), .5); m[1] = Math.min(s[1], e[1]) - 16; pts = [A.p, s, m, e, B.p];
  } else {
    const side = c.spine && c.spine !== 'auto' ? c.spine : (K.data ? 'L' : 'R'), col = side === 'L' ? 'RL' : 'RR', gz = guideZs(col);
    const sx = gz.length ? (side === 'L' ? -HOLE_X : HOLE_X) : (side === 'L' ? -100 : 100), sy = gz.length ? DEPTH + 15 : DEPTH + 7;
    const leg = (q, d, inst) => { // from a port's stub to the spine
      const L = [];
      if (d[1] < -.5 && q[1] < 60){ const x = q[0] < 0 ? -112 : 112; L.push([x, q[1], q[2]], [x, sy, q[2]]); }
      else if (d[1] < -.5){ const b = worldBox(inst), z = b ? b.hi[2] + 10 : q[2]; L.push([q[0], q[1], z], [q[0], sy, z], [sx, sy, z]); return L; }
      else L.push([q[0], sy, q[2]]);
      L.push([sx, sy, q[2]]);
      return L;
    };
    const la = leg(s, A.d, A.inst), lb = leg(e, B.d, B.inst).reverse();
    pts = [A.p, s, ...la, ...lb, e, B.p];
  }
  // drop repeated points
  const clean = [pts[0]]; for (const p of pts.slice(1)) if (Math.hypot(...subv(p, clean[clean.length - 1])) > .5) clean.push(p);
  const path = filletPath(clean, 14);
  let len = 0; for (let i = 1; i < path.length; i++) len += Math.hypot(...subv(path[i], path[i - 1]));
  return {kind, path, len:len + 25, A, B};
}
function filletPath(pts, r){
  if (pts.length < 3) return pts;
  const out = [pts[0]];
  for (let i = 1; i < pts.length - 1; i++){
    const p = pts[i], a = subv(pts[i - 1], p), b = subv(pts[i + 1], p), la = Math.hypot(...a), lb = Math.hypot(...b);
    const rr = Math.min(r, la * .45, lb * .45); if (rr < .5){ out.push(p); continue; }
    const p0 = add(p, scl(a, rr / la)), p2 = add(p, scl(b, rr / lb));
    for (let t = 0; t <= 1.0001; t += .2){ const u = 1 - t; out.push([u*u*p0[0] + 2*u*t*p[0] + t*t*p2[0], u*u*p0[1] + 2*u*t*p[1] + t*t*p2[1], u*u*p0[2] + 2*u*t*p[2] + t*t*p2[2]]); }
  }
  out.push(pts[pts.length - 1]);
  return out;
}
function tubeMesh(path, r, seg = 8){
  const pos = [], idx = []; const n = path.length; if (n < 2) return null;
  let prevN = null;
  for (let i = 0; i < n; i++){
    const t = nrm(subv(path[Math.min(n - 1, i + 1)], path[Math.max(0, i - 1)]));
    let nn = prevN ? subv(prevN, scl(t, dot(prevN, t))) : (Math.abs(t[2]) < .9 ? crs(t, [0,0,1]) : crs(t, [1,0,0]));
    nn = nrm(nn); const bb = crs(t, nn); prevN = nn;
    for (let k = 0; k < seg; k++){ const a = k / seg * Math.PI * 2, c = Math.cos(a) * r, s = Math.sin(a) * r; pos.push(path[i][0] + nn[0]*c + bb[0]*s, path[i][1] + nn[1]*c + bb[1]*s, path[i][2] + nn[2]*c + bb[2]*s); }
  }
  for (let i = 0; i < n - 1; i++) for (let k = 0; k < seg; k++){ const a = i * seg + k, b = i * seg + (k + 1) % seg, c = a + seg, d = b + seg; idx.push(a, b, c, b, d, c); }
  const P = new Float32Array(pos), lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity];
  for (let i = 0; i < P.length; i += 3) for (let k = 0; k < 3; k++){ lo[k] = Math.min(lo[k], P[i + k]); hi[k] = Math.max(hi[k], P[i + k]); }
  return {pos:P, idx:new Uint32Array(idx), lo, hi, tris:idx.length / 3};
}
function patchSize(kind, len){
  if (kind !== 'cat6') return null;
  const s = PATCH_SIZES.find(([mm]) => mm >= len); return s ? s[1] : 'longer than 10 ft';
}
const fmtLen = mm => `${Math.round(mm)} mm (${(mm / 25.4).toFixed(1)}″)`;
let ROUTES = new Map(), routeKey = '';
function updateRoutes(){
  const key = JSON.stringify([S.cables, S.at, explode, RU]);
  if (key === routeKey) return;
  routeKey = key;
  for (const k of Object.keys(GPU)) if (k.startsWith('cable:')) dropGPU(k);
  ROUTES = new Map();
  for (const c of S.cables || []){
    const r = routeCable(c); if (!r) continue;
    const m = tubeMesh(r.path, CABLE[r.kind].r); if (!m) continue;
    r.mesh = m; ROUTES.set(c.id, r);
    if (gl) uploadRaw('cable:' + c.id, m);
  }
}
function planWiring(){
  const ks = 'dev_keystone-1', sw = 'dev_switch-1';
  const W = [];
  const add2 = (ai, ap, bi, bp, extra = {}) => { if (instById(ai) && instById(bi) && placed(ai) && placed(bi)) W.push({id:'c' + uid(), a:{i:ai, p:ap}, b:{i:bi, p:bp}, ...extra}); };
  // front patches: switch port n → keystone n + 2, each straight up
  for (let n = 1; n <= 7; n++) add2(sw, 'p' + n, ks, 'f' + (n + 2), {route:'patch'});
  // device runs into the backs of the keystones
  add2('dev_gwifi-1', 'lan', ks, 'r3'); add2('dev_grommet-1', 'pc', ks, 'r4'); add2('dev_grommet-1', 'laptop', ks, 'r5');
  add2('dev_optiplex-1', 'eth', ks, 'r6'); add2('dev_hue-1', 'eth', ks, 'r7'); add2('dev_pi4-1', 'eth', ks, 'r8'); add2('dev_moca-1', 'eth', ks, 'r9');
  add2('dev_cm1000-1', 'eth', 'dev_gwifi-1', 'wan');
  // coax: wall → splitter → modem and MoCA
  add2('dev_grommet-1', 'coax', 'dev_splitter-1', 'in'); add2('dev_splitter-1', 'out1', 'dev_cm1000-1', 'coax'); add2('dev_splitter-1', 'out2', 'dev_moca-1', 'coax');
  // drives to the PC
  add2('dev_ssd-1', 'usb', 'dev_optiplex-1', 'usb1'); add2('dev_hdd-1', 'usb', 'dev_optiplex-1', 'usb3');
  // power: modem, Wifi, switch, Hue, Pi and the PC brick on the strip
  add2('dev_cm1000-1', 'pwr', 'dev_strip-1', 'o1'); add2('dev_gwifi-1', 'pwr', 'dev_strip-1', 'o2'); add2('dev_switch-1', 'pwr', 'dev_strip-1', 'o3');
  add2('dev_hue-1', 'pwr', 'dev_strip-1', 'o4'); add2('dev_pi4-1', 'pwr', 'dev_strip-1', 'o5'); add2('dev_brick-1', 'ac', 'dev_strip-1', 'o6');
  add2('dev_brick-1', 'dc', 'dev_optiplex-1', 'pwr');
  return W;
}
function validateCables(){
  const used = new Set();
  S.cables = (S.cables || []).filter(c => {
    const ok = c && c.a && c.b && instById(c.a.i) && instById(c.b.i) && TYPES[instById(c.a.i).type].dev && TYPES[instById(c.b.i).type].dev;
    if (!ok) return false;
    const ka = c.a.i + '/' + c.a.p, kb = c.b.i + '/' + c.b.p;
    if (ka === kb || used.has(ka) || used.has(kb)) return false; used.add(ka); used.add(kb); return true;
  });
}

/* ---- clashes: equipment, brackets and guides that overlap each other ---- */
function worldBox(instId){
  const inst = instById(instId), T = TYPES[inst.type], P = worldPose(instId); if (!P) return null;
  const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity];
  for (const [mk] of T.meshes){ const m = meshOf(mk); if (!m) continue; const b = rotBox(P.R, m.lo, m.hi); for (let k = 0; k < 3; k++){ lo[k] = Math.min(lo[k], b.lo[k] + P.t[k]); hi[k] = Math.max(hi[k], b.hi[k] + P.t[k]); } }
  return lo[0] < Infinity ? {lo, hi} : null;
}
function clashes(){
  if (explode > 0.01) return new Map();
  const items = INST.filter(i => placed(i.id) && (TYPES[i.type].dev || TYPES[i.type].kind === 'gear' || i.type === 'cable_guide')).map(i => ({i, b:worldBox(i.id)})).filter(x => x.b);
  const res = new Map(); const hit = (id, why) => { if (!res.has(id)) res.set(id, []); res.get(id).push(why); };
  const fam = id => { const r = rootOf(id); return r ? r.id : id; };
  for (let x = 0; x < items.length; x++) for (let y = x + 1; y < items.length; y++){
    const A = items[x], B = items[y]; if (fam(A.i.id) === fam(B.i.id)) continue;
    const ov = [0,1,2].every(k => Math.min(A.b.hi[k], B.b.hi[k]) - Math.max(A.b.lo[k], B.b.lo[k]) > 0.8);
    if (ov){ hit(A.i.id, 'overlaps the ' + instLabel(B.i.id)); hit(B.i.id, 'overlaps the ' + instLabel(A.i.id)); }
  }
  return res;
}

/* ---- default spots ---- */
function defAt(d, instId){
  const def = d.def; if (!def) return null;
  if (def.top) return INST.some(i => i.id !== instId && S.at[i.id] && S.at[i.id].top) ? null : {top:1};
  if (def.wall) return {wall:[def.wall[0], wallZ(def.wall[1])]};
  if (def.U){ const k = RU - def.U; if (k < 0) return null; const at = {u:k * 2 + (def.half === 'upper' ? 1 : 0), side:d.side === 'half' ? def.side : 'F'}; return cellsFree(d.key, at, instId) ? at : null; }
  return null;
}

/* ---- UI state ---- */
let selCable = null, insertTool = false, pendingPort = null;
const portLabel = (instId, pid) => { const inst = instById(instId), d = inst && TYPES[inst.type].dev, p = d && d.ports.find(x => x.id === pid); return d ? `${d.short} · ${p ? p.label : pid}` : pid; };
const cableAt = (instId, pid) => (S.cables || []).find(c => (c.a.i === instId && c.a.p === pid) || (c.b.i === instId && c.b.p === pid));
const cableName = c => `${portLabel(c.a.i, c.a.p)} → ${portLabel(c.b.i, c.b.p)}`;
function cableBuy(r){
  if (!r) return '';
  if (r.kind === 'cat6') return patchSize('cat6', r.len) + ' patch cable';
  if (r.kind === 'coax') return 'RG6 jumper, ' + (PATCH_SIZES.find(([mm]) => mm >= r.len)?.[1] || 'long');
  if (r.kind === 'dc' || r.kind === 'ac') return 'the device’s own cord — ' + (r.len > 1500 ? 'check it reaches' : 'reaches easily');
  if (r.kind === 'usb') return 'USB cable, ' + (PATCH_SIZES.find(([mm]) => mm >= r.len)?.[1] || 'long');
  return PATCH_SIZES.find(([mm]) => mm >= r.len)?.[1] || '';
}
function cableBOM(){
  updateRoutes();
  const rows = new Map();
  for (const c of S.cables || []){ const r = ROUTES.get(c.id); if (!r) continue; const k = r.kind === 'cat6' ? 'Cat6 patch · ' + patchSize('cat6', r.len) : r.kind === 'coax' ? 'RG6 coax jumper · ' + (PATCH_SIZES.find(([mm]) => mm >= r.len)?.[1] || 'long') : r.kind === 'usb' ? 'USB · ' + (PATCH_SIZES.find(([mm]) => mm >= r.len)?.[1] || 'long') : CABLE[r.kind].name + ' (device’s own)'; rows.set(k, (rows.get(k) || 0) + 1); }
  return [...rows.entries()].sort();
}
function pickCable(x, y){
  updateRoutes(); let best = null, bd = 7;
  for (const [id, r] of ROUTES){
    let prev = null;
    for (let i = 0; i < r.path.length; i += 1){
      const s = project(r.path[i]); if (!s){ prev = null; continue; }
      if (prev){ const dx = s[0] - prev[0], dy = s[1] - prev[1], L = dx * dx + dy * dy, t = L ? clamp(((x - prev[0]) * dx + (y - prev[1]) * dy) / L, 0, 1) : 0, d = Math.hypot(prev[0] + t * dx - x, prev[1] + t * dy - y); if (d < bd){ bd = d; best = id; } }
      prev = s;
    }
  }
  return best;
}
function connectPort(instId, pid){
  const existing = cableAt(instId, pid);
  if (!pendingPort){
    if (existing){ selCable = existing.id; sel = null; refreshAll(); return; }
    pendingPort = {i:instId, p:pid}; selCable = null; refreshAll(); toast(`${portLabel(instId, pid)} — now click the other end`); return;
  }
  if (pendingPort.i === instId && pendingPort.p === pid){ pendingPort = null; refreshAll(); return; }
  if (existing){ toast(`${portLabel(instId, pid)} already has a cable. Delete that one first`); return; }
  const A = portById(pendingPort.i, pendingPort.p), B = portById(instId, pid);
  if (A && B && PORT[A.k].cable && PORT[B.k].cable && cableKind(A.k, B.k) === 'misc' && A.k !== B.k){ toast(`A ${PORT[A.k].name} doesn’t plug into a ${PORT[B.k].name}`); return; }
  const c = {id:'c' + uid(), a:pendingPort, b:{i:instId, p:pid}, route:'auto', spine:'auto'};
  pendingPort = null;
  commit(() => { S.cables.push(c); selCable = c.id; });
  const r = ROUTES.get(c.id); toast(`${cableName(c)}${r ? ' · ' + fmtLen(r.len) : ''}`);
}
function deleteCable(id){ commit(() => { S.cables = S.cables.filter(c => c.id !== id); if (selCable === id) selCable = null; }); toast('Cable removed — Undo puts it back'); }
function moveDev(id, dx, dz){
  const a = S.at[id]; if (!a || !a.wall) return;
  commit(() => { S.at[id] = {wall:[clamp(a.wall[0] + dx, -200, 200), clamp(a.wall[1] + dz, -200, 1000)]}; });
}
function swapSide(id){
  const a = S.at[id], inst = instById(id); if (!a || a.u == null) return;
  const at = {u:a.u, side:a.side === 'L' ? 'R' : 'L'};
  if (!cellsFree(inst.type, at, id)){ toast('The other side of that unit is taken'); return; }
  commit(() => { S.at[id] = at; });
}

/* ---- inspector sections ---- */
function devSection(inst){
  const T = TYPES[inst.type], d = T.dev, on = placed(inst.id);
  const ports = d.ports.filter(p => PORT[p.k].cable || p.k === 'btn');
  const face = {front:'front', rear:'rear', left:'left side', right:'right side', top:'top', bottom:'bottom'};
  let html = bracketSection(inst) + `<div class="sec"><h3>Mounting</h3><p class="note">${esc(d.mount)}</p>${d.approx ? `<p class="note warn-note">≈ ${esc(d.approx)}</p>` : ''}</div>`;
  html += `<div class="sec"><h3>Connections</h3><ul class="portlist">${ports.map(p => {
    const c = cableAt(inst.id, p.id), other = c ? (c.a.i === inst.id && c.a.p === p.id ? c.b : c.a) : null;
    return `<li><span class="pk" style="background:${PORT[p.k].color}"></span><span>${esc(p.label)}${p.approx ? ' <span class="approx" title="Approximate position">≈</span>' : ''}<small>${esc(PORT[p.k].name)} · faces ${face[p.f]}</small></span>${PORT[p.k].cable ? (other ? `<button class="btn small" data-act="selCable" data-cable="${c.id}">→ ${esc(portLabel(other.i, other.p))}</button>` : '<span class="free">free</span>') : ''}</li>`;
  }).join('')}</ul></div>`;
  if (on && S.at[inst.id] && S.at[inst.id].u != null && d.dep !== 'rear'){
    const need = [...neededHoles().entries()].filter(([, ids]) => ids.has(inst.id)).map(([k]) => k);
    const miss = need.filter(k => !S.inserts[k]);
    if (need.length) html += `<div class="sec"><h3>Heat-set inserts</h3><p class="note">${need.map(k => `<span class="mono${S.inserts[k] ? '' : ' miss'}">${esc(holeName(k))}</span>`).join(' ')}</p>
      <p class="note">${miss.length ? `<b class="bad">${miss.length} missing.</b> Add them in Frame mode with <b>Inserts</b>, before you screw the mount in.` : 'All in.'}</p></div>`;
  }
  const cl = clashes().get(inst.id);
  if (cl) html += `<div class="sec"><h3>Fit</h3>${cl.map(x => `<p class="note"><b class="bad">Clash:</b> ${esc(x)}</p>`).join('')}</div>`;
  return html;
}
function cablePanel(){
  updateRoutes();
  const c = selCable && (S.cables || []).find(x => x.id === selCable);
  if (c){
    const r = ROUTES.get(c.id), kind = r ? r.kind : 'misc', cur = c.color || CABLE[kind].color;
    const seg = (id, val, opts) => `<div class="seg" role="group" id="${id}">${opts.map(([v, l]) => `<button data-v="${v}" aria-pressed="${val === v}">${l}</button>`).join('')}</div>`;
    return `<div class="insp-head"><span class="sw" style="background:${fiberHex(cur)}"></span><h3>${esc(CABLE[kind].name)} cable</h3><span class="pill">${r ? esc(fmtLen(r.len)) : 'an end is off the rack'}</span></div>
      <dl class="kv"><dt>From</dt><dd>${esc(portLabel(c.a.i, c.a.p))}<small class="dd2">${esc(placed(c.a.i) ? devWhere(c.a.i) : 'in the tray')}</small></dd>
        <dt>To</dt><dd>${esc(portLabel(c.b.i, c.b.p))}<small class="dd2">${esc(placed(c.b.i) ? devWhere(c.b.i) : 'in the tray')}</small></dd>
        <dt>Length</dt><dd class="mono">${r ? esc(fmtLen(r.len)) : '—'}</dd><dt>Buy</dt><dd>${esc(cableBuy(r))}</dd></dl>
      <div class="sec"><h3>Route</h3>${seg('cRoute', c.route || 'auto', [['auto','Auto'],['spine','Rear spine'],['patch','Front patch'],['direct','Direct']])}
        <div class="field" style="margin-top:8px">Spine${seg('cSpine', c.spine || 'auto', [['auto', CABLE[kind].data ? 'Auto (left)' : 'Auto (right)'],['L','Left'],['R','Right']])}</div>
        <p class="note">Data runs up the rear-left spine and power up the rear-right, so they stay apart. A spine runs through the loops of any cable guides on its rear post.</p></div>
      <div class="sec"><h3>Color</h3><div class="swatches" id="cColor">${FIBER.map(f => `<button data-ccolor="${f.key}" aria-pressed="${cur === f.key}" aria-label="${f.name}" title="${f.name}" style="background:${f.hex}"></button>`).join('')}</div></div>
      <div class="actions"><button class="btn danger" data-act="delCable">Delete cable</button></div>`;
  }
  const bom = cableBOM(), tot = [...ROUTES.values()].reduce((s, r) => s + r.len, 0);
  return `<h2>Cables</h2>
    ${pendingPort ? `<p class="note"><b>${esc(portLabel(pendingPort.i, pendingPort.p))}</b> picked. Click the port at the other end, or click it again to cancel.</p>` : `<p class="note">Click a coloured port dot to start a cable, then the port at the other end. Click a cable to change its route or colour.</p>`}
    <dl class="kv"><dt>Cables</dt><dd>${(S.cables || []).length}</dd><dt>Total run</dt><dd class="mono">${(tot / 1000).toFixed(2)} m</dd></dl>
    <div class="sec"><h3>Shopping list</h3>${bom.length ? `<ul class="bom">${bom.map(([k, n]) => `<li><span>${esc(k)}</span><b class="mono">× ${n}</b></li>`).join('')}</ul>` : '<p class="note">No cables yet.</p>'}
      <p class="note">Lengths follow the drawn route plus 25 mm of slack, rounded up to stock sizes.</p></div>
    <div class="sec"><h3>Port colours</h3><ul class="portlist">${Object.entries(PORT).filter(([, k]) => k.cable).map(([, k]) => `<li><span class="pk" style="background:${k.color}"></span><span>${esc(k.name)}</span></li>`).join('')}</ul></div>`;
}
function insertsBox(){
  const sum = insertSummary();
  return `<div class="stackbox"><span class="eyebrow">Heat-set inserts</span><b>${sum.have} in · ${sum.missing.length ? `<span class="bad">${sum.missing.length} needed</span>` : 'none missing'}</b>
    <small class="ok">M6 inserts in the post holes your mounts and cable guides screw into.</small>
    <div class="row"><button class="btn small${insertTool ? ' primary' : ''}" data-act="insTool" aria-pressed="${insertTool}">${insertTool ? 'Done' : 'Show holes'}</button>${sum.missing.length ? `<button class="btn small" data-act="insAll">Add the ${sum.missing.length} needed</button>` : ''}${sum.have ? `<button class="btn small" data-act="insClear">Clear</button>` : ''}</div></div>`;
}

/* ================= equipment mounted in brackets ================= */
/* A device can sit inside any bracket on the rack (an imported bracket or the CM1000 faceplate). It is stored as
   {p: bracket, off: [x, y, z], rz}: off is where the device's footprint corner sits, in rack axes, measured from the
   bracket's own origin, so the device rides along when the bracket moves to another U. */
const BRACKET_MATCH = {dev_optiplex:/optiplex|7060|micro/i, dev_switch:/sg108|switch/i, dev_hue:/hue/i, dev_pi4:/(^|[^a-z])pi(4|[^a-z]|$)|raspberry/i,
  dev_ssd:/drive|ssd|nas/i, dev_hdd:/drive|hdd|nas/i, dev_brick:/brick|psu|power.?supply/i, dev_gwifi:/wifi|google/i, dev_keystone:/keystone.*(mount|bracket)/i};
const RZN = n => { let R = I3; for (let i = 0; i < (n & 3); i++) R = m3(RZ90, R); return R; };
const isBracket = inst => { const T = inst && TYPES[inst.type]; return !!T && T.kind === 'gear' && !T.dev; };
function bracketsOnRack(){ return INST.filter(i => isBracket(i) && placed(i.id)); }
function matchingBracket(devKey){
  const re = BRACKET_MATCH[devKey]; if (!re) return null;
  return bracketsOnRack().find(b => re.test(TYPES[b.type].name) || (TYPES[b.type].imp && re.test(TYPES[b.type].imp.file || ''))
    || childrenOf(b.id).some(c => re.test(TYPES[c.type].name))) || null;
}
function devFoot(d, rz){ return rz & 1 ? [d.D, d.W, d.H] : [d.W, d.D, d.H]; }
function mountedPose(inst, a){
  const d = TYPES[inst.type].dev, pw = worldPose(a.p); if (!pw || !placed(a.p)) return null;
  const R = RZN(a.rz || 0), f = devFoot(d, a.rz || 0);
  const corner = add(pw.t, add(a.off, [0, 0, 30 * explode]));
  return pose(R, subv(add(corner, [f[0] / 2, f[1] / 2, 0]), mv(R, [d.W / 2, d.D / 2, 0])));
}
/* the bracket and the parts attached to it, ready for ray tests in world space */
function bracketParts(brId){
  const root = instById(brId); if (!root) return [];
  return [root, ...childrenOf(brId).filter(c => !TYPES[c.type].dev)].map(i => ({P:worldPose(i.id), keys:TYPES[i.type].meshes.map(m => m[0]).filter(k => meshOf(k))})).filter(p => p.P && p.keys.length);
}
function rayParts(parts, o, d, tmax){
  let best = null;
  for (const {P, keys} of parts){ const lo = mtv(P.R, subv(o, P.t)), ld = mtv(P.R, d); for (const k of keys){ const h = rayMesh(k, lo, ld, best ? best.t : tmax); if (h && (!best || h.t < best.t)) best = {t:h.t}; } }
  return best;
}
function partsBox(parts){
  const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity];
  for (const {P, keys} of parts) for (const k of keys){ const m = meshOf(k), b = rotBox(P.R, m.lo, m.hi); for (let q = 0; q < 3; q++){ lo[q] = Math.min(lo[q], b.lo[q] + P.t[q]); hi[q] = Math.max(hi[q], b.hi[q] + P.t[q]); } }
  return {lo, hi};
}
/* Find where a device sits in a bracket: centred across it (or beside devices already in it), its front against
   the back of the faceplate (or flush with the faceplate front when the faceplate has an opening the device fills),
   and resting on the bracket's floor. Then check its edges for anything they pass through. */
function fitInBracket(devKey, brId, rz = 0, excludeId = null){
  const d = DEV[devKey], keepEx = explode; explode = 0;
  try {
    const parts = bracketParts(brId), P0 = worldPose(brId); if (!parts.length || !P0) return null;
    const B = partsBox(parts), [w, dd, H] = devFoot(d, rz), warn = [];
    const others = INST.filter(i => i.id !== excludeId && TYPES[i.type].dev && S.at[i.id] && S.at[i.id].p === brId).map(i => worldBox(i.id)).filter(Boolean);
    const cx = (B.lo[0] + B.hi[0]) / 2, span = B.hi[0] - B.lo[0];
    const xs = []; if (w >= span - 1) xs.push(cx - w / 2); else for (let x = B.lo[0]; x <= B.hi[0] - w; x += 2) xs.push(x);
    xs.sort((a, b) => Math.abs(a + w / 2 - cx) - Math.abs(b + w / 2 - cx));
    const frontAt = (x0, z0) => {
      let pass = 0, n = 0, stop = -Infinity;
      for (let i = 0; i < 5; i++) for (let j = 0; j < 3; j++){
        const o = [x0 + 3 + (w - 6) * i / 4, B.lo[1] - 1, z0 + 2 + Math.max(0, H - 4) * j / 2]; n++;
        const h = rayParts(parts, o, [0, 1, 0], B.hi[1] - B.lo[1] + 2);
        if (!h || h.t > 26){ pass++; continue; }
        const o2 = [o[0], o[1] + h.t + 0.05, o[2]], h2 = rayParts(parts, o2, [0, 1, 0], 20);
        stop = Math.max(stop, h2 ? o2[1] + h2.t : o[1] + h.t);
      }
      return pass >= n * 0.8 || stop === -Infinity ? B.lo[1] : stop + 0.3;
    };
    const floorAt = (x0, y0) => {
      const zs = Math.min(B.hi[2] - 3, B.lo[2] + H + 6); let fl = B.lo[2];
      for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++){
        const o = [x0 + 3 + (w - 6) * i / 3, y0 + 3 + (Math.min(dd, B.hi[1] - y0) - 6) * j / 3, zs];
        const h = rayParts(parts, o, [0, 0, -1], zs - B.lo[2] + 1); if (h) fl = Math.max(fl, zs - h.t);
      }
      return fl + 0.2;
    };
    let pick = null;
    for (const x0 of xs.slice(0, 80)){
      let z0 = B.lo[2], y0 = frontAt(x0, z0); z0 = floorAt(x0, y0); y0 = frontAt(x0, z0);
      const box = {lo:[x0, y0, z0], hi:[x0 + w, y0 + dd, z0 + H]};
      if (others.some(o => [0, 1, 2].every(k => Math.min(o.hi[k], box.hi[k]) - Math.max(o.lo[k], box.lo[k]) > 0.5))) continue;
      pick = box; break;
    }
    if (!pick){ warn.push('no room left beside the other gear in this bracket'); const x0 = cx - w / 2, y0 = frontAt(x0, B.lo[2]); pick = {lo:[x0, y0, B.lo[2]], hi:[x0 + w, y0 + dd, B.lo[2] + H]}; }
    const off = subv(pick.lo, P0.t);
    return {off:off.map(v => +v.toFixed(2)), warn:warn.concat(fitWarnings(parts, B, pick))};
  } finally { explode = keepEx; }
}
function fitWarnings(parts, B, box){
  const out = [], s = 0.6, lo = box.lo.map(v => v + s), hi = box.hi.map(v => v - s);
  if (box.hi[2] > B.hi[2] + 0.5) out.push(`${(box.hi[2] - B.hi[2]).toFixed(1)} mm taller than the bracket`);
  if (box.hi[1] > B.hi[1] + 0.5) out.push(`sticks out ${(box.hi[1] - B.hi[1]).toFixed(0)} mm past the back of the bracket`);
  if (box.hi[1] > DEPTH + 2) out.push(`reaches ${(box.hi[1] - DEPTH).toFixed(0)} mm past the rear posts`);
  // the 12 box edges: anything they cross means the device and the bracket overlap
  const C = i => [i & 1 ? hi[0] : lo[0], i & 2 ? hi[1] : lo[1], i & 4 ? hi[2] : lo[2]];
  let hits = 0;
  for (const [a, b] of [[0,1],[2,3],[4,5],[6,7],[0,2],[1,3],[4,6],[5,7],[0,4],[1,5],[2,6],[3,7]]){
    const A = C(a), Bp = C(b), dv = subv(Bp, A), L = Math.hypot(...dv);
    if (rayParts(parts, A, scl(dv, 1 / L), L)) hits++;
  }
  if (hits) out.push('touches the bracket — it may be a tight fit or need turning');
  return out;
}
function mountDevice(id, brId, rz = 0){
  const inst = instById(id), f = fitInBracket(inst.type, brId, rz, id);
  if (!f){ toast('That bracket hasn’t loaded yet'); return false; }
  commit(() => { S.at[id] = {p:brId, off:f.off, rz}; sel = id; });
  toast(`${TYPES[inst.type].dev.short} → in ${TYPES[instById(brId).type].name}${f.warn.length ? ' · ' + f.warn[0] : ''}`);
  return true;
}
function mountedFit(id){ // the warnings for where it is now
  const a = S.at[id]; if (!a || !a.off) return [];
  const keepEx = explode; explode = 0;
  try { const parts = bracketParts(a.p); if (!parts.length) return []; const b = worldBox(id); return b ? fitWarnings(parts, partsBox(parts), b) : []; }
  finally { explode = keepEx; }
}
function nudgeMounted(id, dv){ const a = S.at[id]; if (!a || !a.off) return; commit(() => { S.at[id] = {...a, off:add(a.off, dv).map(v => +v.toFixed(2))}; }); }
function fillBrackets(){
  let n = 0;
  for (const d of DEVICES){
    const id = d.key + '-1', inst = instById(id); if (!inst || TYPES[inst.type].kind !== 'gear') continue;
    const a = S.at[id]; if (a && a.p) continue;
    const br = matchingBracket(d.key); if (!br) continue;
    const f = fitInBracket(d.key, br.id, 0, id); if (!f) continue;
    S.at[id] = {p:br.id, off:f.off, rz:0}; n++;
  }
  return n;
}
function bracketCandidates(typeKey, instId){
  const out = [];
  for (const br of bracketsOnRack()){
    const f = fitInBracket(typeKey, br.id, 0, instId); if (!f) continue;
    const at = {p:br.id, off:f.off, rz:0}, P = mountedPose({type:typeKey}, at); if (!P) continue;
    const d = DEV[typeKey];
    out.push({at, label:'in ' + TYPES[br.type].name + (f.warn.length ? ' (' + f.warn[0] + ')' : ''), anchor:papply(P, [d.W / 2, -4, d.H / 2]), pose:P});
  }
  return out;
}
function bracketSection(inst){
  const a = S.at[inst.id], d = TYPES[inst.type].dev, editable = canEdit(inst.id);
  if (d.zone !== 'rack' && d.zone !== 'top') return '';
  if (a && a.p && a.off){
    const br = instById(a.p), warn = mountedFit(inst.id);
    return `<div class="sec"><h3>Bracket</h3><p class="note">In <b>${esc(TYPES[br.type].name)}</b>${placed(a.p) ? ' · ' + esc(instWhere(a.p)) : ' (in the tray)'}. It moves with the bracket.</p>
      ${warn.length ? warn.map(w => `<p class="note"><b class="bad">Fit:</b> ${esc(w)}</p>`).join('') : '<p class="note">Fits without touching the bracket.</p>'}
      ${editable ? `<div class="row nudge"><button class="btn small" data-act="mnudge" data-v="-1,0,0">◀ 1 mm</button><button class="btn small" data-act="mnudge" data-v="1,0,0">1 mm ▶</button>
        <button class="btn small" data-act="mnudge" data-v="0,0,1">▲ 1 mm</button><button class="btn small" data-act="mnudge" data-v="0,0,-1">▼ 1 mm</button>
        <button class="btn small" data-act="mnudge" data-v="0,-1,0">Forward 1 mm</button><button class="btn small" data-act="mnudge" data-v="0,1,0">Back 1 mm</button></div>
      <div class="row"><button class="btn small" data-act="mrefit">Refit</button><button class="btn small" data-act="mturn">Turn 90°</button><button class="btn small" data-act="munmount">Take it out of the bracket</button></div>` : '<p class="note">Switch to <b>Gear</b> to change it.</p>'}</div>`;
  }
  const list = bracketsOnRack(), match = matchingBracket(inst.type);
  if (!list.length) return `<div class="sec"><h3>Bracket</h3><p class="note">No bracket on the rack yet. Import yours (Import STL / 3MF) and you can put this in it.</p></div>`;
  const opts = [match, ...list.filter(b => b !== match)].filter(Boolean);
  return `<div class="sec"><h3>Bracket</h3>${match ? `<p class="note">Looks like it goes in <b>${esc(TYPES[match.type].name)}</b>.</p>` : '<p class="note">Sitting on its own. Put it in a bracket to see how it fits.</p>'}
    ${editable ? `<div class="row"><select class="select" id="brSel">${opts.map(b => `<option value="${b.id}">${esc(TYPES[b.type].name)} · ${esc(instWhere(b.id))}</option>`).join('')}</select><button class="btn small primary" data-act="mount">Put it in</button></div>` : '<p class="note">Switch to <b>Gear</b> to change it.</p>'}</div>`;
}


/* ================= state ================= */
const DEFAULT_SETTINGS = {numbering:'top', labels:true, sides:'clear', frame:'#232628'};
let S = null, sel = null, hover = null, activeSpot = null, mode = 'frame', explode = 0;
try { const m = localStorage.getItem('labrax-assembler-mode'); if (['frame','gear','cables'].includes(m)) mode = m; } catch (e) {}
const IMPORT_MESH = {}; // import id -> decoded mesh, or 'loading' / 'missing'
const newFrameId = () => 'f' + uid();
/* fill every slot of a stack with a fresh piece */
function fillFrame(){ buildSlots(); const used = new Set(Object.values(S.at).filter(a => a && a.s).map(a => a.s));
  for (const s of SLOTS){ if (used.has(s.id) || TYPES[s.type].fg === 'acc') continue; const id = newFrameId(); S.frame[id] = s.type; S.at[id] = {s:s.id}; } }
function clearFrame(){ for (const id of Object.keys(S.frame)) delete S.at[id]; S.frame = {}; S.levels = []; }
function applyPreset(name){ clearFrame(); S.levels = STACK_PRESETS[name].map(l => ({...l})); fillFrame(); }
function freshState(){
  S = {v:3, levels:[], frame:{}, at:{}, colors:{}, hidden:{}, imports:[], inserts:{}, cables:[], settings:{...DEFAULT_SETTINGS}};
  applyPreset('nine');
  S.at['cm1000_face-1'] = {u:0}; S.at['cm1000_rail_l-1'] = {p:'cm1000_face-1'}; S.at['cm1000_rail_r-1'] = {p:'cm1000_face-1'};
  return S;
}
function sanitizeImport(m){
  if (!m || typeof m !== 'object' || typeof m.id !== 'string' || !/^[a-z0-9]{4,16}$/.test(m.id)) return null;
  const num = (v, d) => Number.isFinite(Number(v)) ? Number(v) : d;
  return {id:m.id, name:String(m.name || 'Imported part').slice(0, 60), role:m.role === 'attach' ? 'attach' : 'gear',
    parent: typeof m.parent === 'string' ? m.parent : null, asset: typeof m.asset === 'string' ? m.asset.slice(0, 80) : null,
    rot:[0,1,2].map(k => clamp(Math.round(num(m.rot && m.rot[k], 0)), 0, 3)), ear:clamp(num(m.ear, 3), 0, 40),
    nudge:[0,1,2].map(k => clamp(num(m.nudge && m.nudge[k], 0), -200, 200)), hU: m.hU == null ? null : clamp(Math.round(num(m.hU, 1) * 2) / 2, .5, 10),
    color:FIBER.some(f => f.key === m.color) ? m.color : 'slate', lo:(m.lo || [0,0,0]).map(Number), hi:(m.hi || [0,0,0]).map(Number), tris:num(m.tris, 0), file:String(m.file || '').slice(0, 120)};
}
function sanitize(raw){
  const s = raw && typeof raw === 'object' ? raw : {};
  const out = {v:3, levels:[], frame:{}, at:{}, colors:{}, hidden:{}, imports:[], inserts:{}, cables:[], settings:{...DEFAULT_SETTINGS, ...(s.settings || {})}};
  const st = out.settings;
  delete st.board;
  if (s.inserts && typeof s.inserts === 'object') for (const k in s.inserts) if (/^(FL|FR|RL|RR):\d{1,2}:[012]$/.test(k) && s.inserts[k] === true) out.inserts[k] = true;
  const end = e => e && typeof e === 'object' && typeof e.i === 'string' && typeof e.p === 'string' ? {i:e.i.slice(0, 40), p:e.p.slice(0, 20)} : null;
  out.cables = (Array.isArray(s.cables) ? s.cables : []).slice(0, 120).map(c => c && end(c.a) && end(c.b) ? {id:/^c[a-z0-9]{4,12}$/.test(c.id) ? c.id : 'c' + uid(), a:end(c.a), b:end(c.b),
    color:FIBER.some(f => f.key === c.color) ? c.color : undefined, route:['auto','direct','patch','spine'].includes(c.route) ? c.route : 'auto', spine:['auto','L','R'].includes(c.spine) ? c.spine : 'auto'} : null).filter(Boolean);
  out.planned = s.v !== 3;
  st.numbering = st.numbering === 'bottom' ? 'bottom' : 'top';
  st.labels = st.labels !== false;
  st.sides = ['clear','solid','hidden'].includes(st.sides) ? st.sides : 'clear';
  if (!/^#[0-9a-f]{6}$/i.test(st.frame)) st.frame = DEFAULT_SETTINGS.frame;
  for (const k of ['mid','ext','planU']) delete st[k];
  out.imports = (Array.isArray(s.imports) ? s.imports : []).map(sanitizeImport).filter(m => m && m.asset).slice(0, 40);
  const ids = new Set(out.imports.map(m => m.id));
  out.imports.forEach(m => { if (m.role === 'attach' && !ids.has(m.parent)) m.role = 'gear'; });
  if (s.colors && typeof s.colors === 'object') for (const k in s.colors) if (FIBER.some(f => f.key === s.colors[k])) out.colors[k] = s.colors[k];
  if (s.hidden && typeof s.hidden === 'object') for (const k in s.hidden) if (s.hidden[k] === true) out.hidden[k] = true;
  const at = s.at && typeof s.at === 'object' ? s.at : {};
  // gear placements carry over as they are
  for (const id in at) if (/^(cm1000_|imp-|dev_)/.test(id) && at[id] && typeof at[id] === 'object') out.at[id] = at[id];
  if (s.v === 2 || s.v === 3){
    out.levels = (Array.isArray(s.levels) ? s.levels : []).slice(0, 10).map(l => l && l.k === 'mod' ? {k:'mod'} : {k:'post', u:clamp(Math.round(Number(l && l.u) || 5), 1, 5)});
    if (s.frame && typeof s.frame === 'object') for (const id in s.frame) if (/^f[a-z0-9]{4,12}$/.test(id) && TYPES[s.frame[id]] && TYPES[s.frame[id]].bin){ out.frame[id] = s.frame[id]; if (at[id]) out.at[id] = at[id]; }
    out.migrated = false;
  } else {
    // saved before the frame could be built piece by piece: rebuild it from the old height settings, fully assembled
    const os = s.settings || {}, ext = clamp(Math.round(Number(os.ext ?? 3)), 0, 5), mid = os.mid == null ? 1 : (os.mid ? 1 : 0);
    out.levels = [{k:'post', u:5}, ...(mid ? [{k:'mod'}] : []), ...(ext ? [{k:'post', u:ext}] : [])];
    out.migrated = true;
  }
  return out;
}
function registerImports(){
  for (const k of Object.keys(TYPES)) if (TYPES[k].group === 'import') delete TYPES[k];
  for (const m of S.imports){
    const key = 'imp:' + m.id;
    TYPES[key] = {key, name:m.name, group:'import', kind:m.role, parent:m.role === 'attach' ? 'imp:' + m.parent : null, color:m.color,
      meshes:[[key, 'gear']], count:1, src:m.file || 'Imported file', imp:m};
  }
  rebuildInstances();
}
/* reorder levels: order[newIndex] = oldIndex; every slot id follows its level */
function reorderLevels(order){
  const map = {}; order.forEach((oldI, newI) => { map[oldI] = newI; });
  S.levels = order.map(i => S.levels[i]);
  for (const id in S.at){ const a = S.at[id]; if (!a || !a.s) continue; const m = /^([PMS])(\d+)(.*)$/.exec(a.s); if (m) a.s = m[1] + map[+m[2]] + m[3]; }
  buildSlots();
}
/* move level m so it sits at joint j (0 = bottom of the stack, levels.length = top), counted before the move */
function moveLevelTo(m, j){
  const order = S.levels.map((_, i) => i).filter(i => i !== m);
  order.splice(j > m ? j - 1 : j, 0, m);
  reorderLevels(order);
}
function insertLevel(j, lv){
  for (const id in S.at){ const a = S.at[id]; if (!a || !a.s) continue; const m = /^([PMS])(\d+)(.*)$/.exec(a.s); if (m && +m[2] >= j) a.s = m[1] + (+m[2] + 1) + m[3]; }
  S.levels.splice(j, 0, lv); buildSlots();
}
function jointName(j, skip){
  const below = S.levels.slice(0, j).filter((_, i) => i !== skip), above = S.levels.slice(j).filter((_, i) => i + j !== skip);
  const nm = l => l ? (l.k === 'mod' ? 'the 1U support' : `the ${l.u}U posts`) : null;
  const b = nm(below[below.length - 1]), a = nm(above[0]);
  return b && a ? `between ${b} and ${a}` : b ? `on top of ${b}` : a ? `under ${a}` : 'on the base';
}
/* drop empty levels: everything above slides down a level, like pulling a brick out of a stack */
function cleanLevels(){
  let changed = false;
  for (let i = S.levels.length - 1; i >= 0; i--){
    if (Object.values(S.at).some(a => a && a.s && slotLevel(a.s) === i)) continue;
    S.levels.splice(i, 1); changed = true;
    for (const id in S.at){ const a = S.at[id]; if (!a || !a.s) continue; const m = /^([PMS])(\d+)(.*)$/.exec(a.s); if (m && +m[2] > i) a.s = m[1] + (+m[2] - 1) + m[3]; }
  }
  if (changed) buildSlots();
}
function validateAt(){
  buildSlots(); rebuildInstances();
  const at = {}, slotUsed = {}, raw = S.at || {};
  for (const inst of INST){
    const a = raw[inst.id], T = TYPES[inst.type];
    if (!a || typeof a !== 'object') continue;
    if (T.kind === 'frame' && typeof a.s === 'string' && SLOT[a.s] && SLOT[a.s].type === inst.type && !slotUsed[a.s]){ at[inst.id] = {s:a.s}; slotUsed[a.s] = true; }
    else if (T.dev && T.kind === 'gear' && typeof a.p === 'string'){ const off = Array.isArray(a.off) && a.off.length === 3 && a.off.every(v => Number.isFinite(Number(v))) ? a.off.map(v => clamp(Number(v), -600, 600)) : null; if (off) at[inst.id] = {p:a.p, off, rz:(Number(a.rz) | 0) & 3}; }
    else if (T.kind === 'gear' && Number.isFinite(Number(a.u))){ at[inst.id] = {u:Math.round(Number(a.u))}; if (T.dev && T.dev.side === 'half') at[inst.id].side = a.side === 'R' ? 'R' : 'L'; else if (T.dev) at[inst.id].side = 'F'; }
    else if (T.dev && T.dev.zone === 'top' && a.top) at[inst.id] = {top:1};
    else if (T.dev && T.dev.zone === 'wall' && Array.isArray(a.wall) && a.wall.every(v => Number.isFinite(Number(v)))) at[inst.id] = {wall:[clamp(Number(a.wall[0]), -200, 200), clamp(Number(a.wall[1]), -200, 1000)]};
    else if (T.kind === 'attach' && typeof a.p === 'string') at[inst.id] = {p:a.p};
  }
  S.at = at;
  // a frame piece that isn't on the rack goes back into its bin
  for (const id of Object.keys(S.frame)) if (!S.at[id]) delete S.frame[id];
  cleanLevels(); rebuildInstances();
  // gear overlap and range: rack cells are half-unit rows × left/right × front/rear
  const occ = new Set();
  for (const inst of INST){
    const a = S.at[inst.id]; if (!a || a.u == null) continue;
    const h2 = Math.round(gearHU(inst.type) * 2), cells = cellsFor(inst.type, a);
    let ok = a.u >= 0 && a.u + h2 <= RU * 2 && (gearHU(inst.type) % 1 !== 0 || a.u % 2 === 0) && cells.every(c => !occ.has(c));
    if (!ok){ delete S.at[inst.id]; continue; }
    for (const c of cells) occ.add(c);
  }
  { let top = false; for (const inst of INST){ const a = S.at[inst.id]; if (a && a.top){ if (top) delete S.at[inst.id]; top = true; } } }
  // inserts only exist where a post or support extension carries that hole
  if (!S.inserts) S.inserts = {};
  for (const k of Object.keys(S.inserts)){ const [col, u] = k.split(':'); if (+u >= RU || !columnOwner(col, +u)) delete S.inserts[k]; }
  if (!Array.isArray(S.cables)) S.cables = [];
  // attachments: parent must be the right type, one child per type per parent
  const taken = new Set();
  for (const inst of INST){
    const a = S.at[inst.id]; if (!a || a.p == null) continue;
    const par = instById(a.p), T = TYPES[inst.type];
    if (T.dev && T.kind === 'gear'){ if (!isBracket(par)) delete S.at[inst.id]; continue; }
    if (!par || par.type !== T.parent || taken.has(a.p + '|' + inst.type)) { delete S.at[inst.id]; continue; }
    taken.add(a.p + '|' + inst.type);
  }
  validateCables();
}

/* history: one undo stack per mode, so Undo in Gear mode can never change the frame (and the other way round) */
const HIST = {frame:{past:[], future:[]}, gear:{past:[], future:[]}, cables:{past:[], future:[]}};
const histMode = () => mode === 'ask' ? lastBuildMode : mode;
const H = () => HIST[histMode()];
const gearAt = () => Object.fromEntries(Object.entries(S.at).filter(([id]) => !S.frame[id]));
function snap(m = histMode()){ return m === 'frame' ? JSON.stringify({at:S.at, frame:S.frame, levels:S.levels, inserts:S.inserts}) : m === 'cables' ? JSON.stringify({cables:S.cables}) : JSON.stringify({gear:gearAt()}); }
function restore(j, m = histMode()){
  const o = JSON.parse(j);
  if (m === 'cables'){ S.cables = o.cables; }
  else if (m === 'frame'){
    S.inserts = o.inserts || {};
    const gear = gearAt();
    // gear that a frame change knocked off comes back if it still fits
    for (const id in o.at) if (!o.frame[id] && !gear[id]) gear[id] = o.at[id];
    S.frame = o.frame; S.levels = o.levels;
    S.at = {...gear, ...Object.fromEntries(Object.entries(o.at).filter(([id]) => o.frame[id]))};
  } else {
    S.at = {...Object.fromEntries(Object.entries(S.at).filter(([id]) => S.frame[id])), ...o.gear};
  }
  validateAt();
}
function commit(fn, opts = {}){
  const before = snap();
  fn();
  validateAt();
  if (snap() !== before){ const h = H(); h.past.push(before); if (h.past.length > 80) h.past.shift(); h.future = []; markDirty(); }
  else if (opts.always) markDirty();
  refreshAll();
}
function undo(){ const h = H(); if (!h.past.length) return; h.future.push(snap()); restore(h.past.pop()); markDirty(); refreshAll(); toast('Undone'); }
function redo(){ const h = H(); if (!h.future.length) return; h.past.push(snap()); restore(h.future.pop()); markDirty(); refreshAll(); toast('Redone'); }
/* the frame is edited only in Frame mode, gear only in Gear mode */
const canEdit = id => { const i = instById(id); return !!i && (TYPES[i.type].kind === 'frame' ? 'frame' : 'gear') === histMode(); };

/* persistence: browser first, then the artifact database when it answers */
const LS_KEY = 'labrax-assembler-v1', LS_SPOTS = 'labrax-assembler-spots-v1';
let localMeta = {dirty:false, editedAt:0};
function loadState(raw){
  let planned = true;
  if (!raw){ freshState(); registerImports(); validateAt(); }
  else {
    const out = sanitize(raw); const migrated = out.migrated; planned = out.planned; delete out.migrated; delete out.planned;
    S = out; registerImports();
    if (migrated) fillFrame();
    validateAt();
  }
  // first time with the equipment library: put the devices where the build plan has them, and wire them up
  if (planned){ applyPlannedLayout(); validateAt(); S.cables = planWiring(); validateAt(); }
}
function saveLocal(){ try { localStorage.setItem(LS_KEY, JSON.stringify({state:S, dirty:localMeta.dirty, editedAt:localMeta.editedAt})); } catch (e) {} }
function markDirty(){ localMeta.dirty = true; localMeta.editedAt = Date.now(); saveLocal(); scheduleRemote(); }
(function loadLocal(){
  let rec = null;
  try { rec = JSON.parse(localStorage.getItem(LS_KEY) || 'null'); } catch (e) {}
  loadState(rec && rec.state);
  if (rec && rec.state) localMeta = {dirty:!!rec.dirty, editedAt:Number(rec.editedAt) || 0};
})();
const REMOTE_PATH = 'builds/main', CLIENT = uid();
let remoteRef = null, saving = false, again = false, remoteTimer = null, readOnly = false, lastApplied = 0, DB = null, ASSETS = null, SAMPLE = null;
function setStatus(s){
  const el = $('#status');
  el.dataset.s = s; el.textContent = {local:'Saved in this browser', saving:'Saving…', saved:'Saved', error:'Not saved — check connection', readonly:'View only'}[s];
}
function scheduleRemote(){ if (!remoteRef || readOnly) return; clearTimeout(remoteTimer); setStatus('saving'); remoteTimer = setTimeout(() => { remoteTimer = null; flushRemote(); }, 900); }
async function flushRemote(retried){
  if (!remoteRef || readOnly) return;
  if (saving){ again = true; return; }
  saving = true;
  const body = {state:JSON.parse(JSON.stringify(S)), savedAt:Date.now(), client:CLIENT};
  try { await remoteRef.set(body); lastApplied = body.savedAt; if (!remoteTimer && !again){ localMeta.dirty = false; saveLocal(); setStatus('saved'); } }
  catch (e) {
    const code = e && e.code;
    if (code === 'permission_denied' || code === 'not_granted'){ readOnly = true; setStatus('readonly'); }
    else if (code === 'unavailable' && !retried){ saving = false; setTimeout(() => flushRemote(true), 800 + Math.random() * 800); return; }
    else setStatus('error');
  }
  saving = false;
  if (again){ again = false; flushRemote(); }
}
function adoptRemote(d){
  if (!d || !d.state) return;
  loadState(d.state); lastApplied = Number(d.savedAt) || Date.now();
  loadImportMeshes();
  for (const h of Object.values(HIST)){ h.past = []; h.future = []; } localMeta.dirty = false; saveLocal(); if (sel && !instById(sel)) sel = null; refreshAll();
}

/* ================= WebGL renderer ================= */
const canvas = $('#gl'), stage = $('#stage'), overlay = $('#overlay');
const gl = canvas.getContext('webgl2', {antialias:true, alpha:false, premultipliedAlpha:false, preserveDrawingBuffer:false});
if (!gl){ $('#glFail').hidden = false; }
function shader(type, src){ const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s; }
function program(vs, fs){ const p = gl.createProgram(); gl.attachShader(p, shader(gl.VERTEX_SHADER, vs)); gl.attachShader(p, shader(gl.FRAGMENT_SHADER, fs)); gl.bindAttribLocation(p, 0, 'aPos'); gl.linkProgram(p); if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p)); return p; }
let P_MESH, P_LINE, U_M = {}, U_L = {};
const GPU = {};
let lineBufs = null, pinMesh = null;
const COL = {stage:[0.86,0.88,0.85], ink:[0.1,0.12,0.11], accent:[0.05,0.51,0.49], dark:false};
function readTheme(){
  const cs = getComputedStyle(document.documentElement);
  const parse = v => { v = v.trim(); if (v.startsWith('#')) return hexRgb(v.length === 4 ? '#' + [...v.slice(1)].map(c => c + c).join('') : v); const m = v.match(/[\d.]+/g); return m ? m.slice(0, 3).map(x => x / 255) : [0.5,0.5,0.5]; };
  COL.stage = parse(cs.getPropertyValue('--stage')); COL.ink = parse(cs.getPropertyValue('--ink')); COL.accent = parse(cs.getPropertyValue('--accent'));
  COL.dark = lum(COL.stage) < 0.3; requestRender();
}
function initGL(){
  P_MESH = program(`#version 300 es
    layout(location=0) in vec3 aPos; uniform mat4 uM, uVP; out vec3 vW;
    void main(){ vec4 w = uM * vec4(aPos, 1.0); vW = w.xyz; gl_Position = uVP * w; }`,
  `#version 300 es
    precision highp float; in vec3 vW; uniform vec4 uColor; uniform vec3 uEmit, uEye; uniform float uSpec; out vec4 o;
    void main(){
      vec3 n = normalize(cross(dFdx(vW), dFdy(vW))); vec3 v = normalize(uEye - vW); if (dot(n, v) < 0.0) n = -n;
      vec3 L1 = normalize(vec3(-0.45, -0.85, 0.95)), L2 = normalize(vec3(0.8, 0.35, 0.3));
      float d1 = max(dot(n, L1), 0.0), d2 = max(dot(n, L2), 0.0), hemi = 0.5 + 0.5 * n.z;
      vec3 c = uColor.rgb * (0.30 + 0.16 * hemi + 0.58 * d1 + 0.20 * d2);
      vec3 h = normalize(L1 + v); c += vec3(0.16) * pow(max(dot(n, h), 0.0), 36.0) * uSpec;
      c += uColor.rgb * 0.12 * pow(1.0 - max(dot(n, v), 0.0), 3.0);
      o = vec4(c + uEmit, uColor.a);
    }`);
  P_LINE = program(`#version 300 es
    layout(location=0) in vec3 aPos; uniform mat4 uVP, uM; void main(){ gl_Position = uVP * uM * vec4(aPos, 1.0); }`,
  `#version 300 es
    precision mediump float; uniform vec4 uColor; out vec4 o; void main(){ o = uColor; }`);
  for (const n of ['uM','uVP','uColor','uEmit','uEye','uSpec']) U_M[n] = gl.getUniformLocation(P_MESH, n);
  for (const n of ['uM','uVP','uColor']) U_L[n] = gl.getUniformLocation(P_LINE, n);
  for (const k in MESH) uploadMesh(k);
  DEVMESH['dev:unit'] = meshBuilder().box([0,0,0], [1,1,1]).done();
  for (const k in DEVMESH) uploadMesh(k);
  buildLines(); pinMesh = makePin(); uploadRaw('__pin', pinMesh); glReady = true;
  gl.enable(gl.DEPTH_TEST); gl.disable(gl.CULL_FACE);
}
function uploadRaw(key, m){
  const vao = gl.createVertexArray(); gl.bindVertexArray(vao);
  const vb = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vb); gl.bufferData(gl.ARRAY_BUFFER, m.pos, gl.STATIC_DRAW);
  gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0);
  const ib = gl.createBuffer(); gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ib); gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, m.idx, gl.STATIC_DRAW);
  gl.bindVertexArray(null);
  GPU[key] = {vao, count:m.idx.length, type:m.idx instanceof Uint32Array ? gl.UNSIGNED_INT : gl.UNSIGNED_SHORT, vb, ib};
}
function uploadMesh(k){ const m = meshOf(k); if (gl && m && !GPU[k]) uploadRaw(k, m); }
function dropGPU(k){ const g = GPU[k]; if (!g) return; gl.deleteBuffer(g.vb); gl.deleteBuffer(g.ib); gl.deleteVertexArray(g.vao); delete GPU[k]; }
function makePin(){
  const pos = [], idx = [], seg = 14, ring = 8, r = 3.2, cz = 13;
  pos.push(0, 0, 0); // tip
  for (let i = 0; i < seg; i++){ const a = i / seg * Math.PI * 2; pos.push(Math.cos(a) * 1.4, Math.sin(a) * 1.4, cz - r * .6); }
  for (let i = 0; i < seg; i++) idx.push(0, 1 + i, 1 + (i + 1) % seg);
  const base = pos.length / 3;
  for (let j = 0; j <= ring; j++){ const ph = j / ring * Math.PI; for (let i = 0; i < seg; i++){ const a = i / seg * Math.PI * 2; pos.push(Math.sin(ph) * Math.cos(a) * r, Math.sin(ph) * Math.sin(a) * r, cz + Math.cos(ph) * r); } }
  for (let j = 0; j < ring; j++) for (let i = 0; i < seg; i++){ const a = base + j * seg + i, b = base + j * seg + (i + 1) % seg, c = a + seg, d = b + seg; idx.push(a, c, b, b, c, d); }
  return {pos:new Float32Array(pos), idx:new Uint16Array(idx), lo:[-r,-r,0], hi:[r,r,cz + r]};
}
function buildLines(){
  if (lineBufs) for (const b of Object.values(lineBufs)) gl.deleteVertexArray(b.vao);
  const floor = [], floorMajor = [], ugrid = [], uhalf = [];
  const z0 = -47.2;
  for (let x = -260; x <= 260; x += 10) (x % 50 === 0 ? floorMajor : floor).push(x, -170, z0, x, 410, z0);
  for (let y = -170; y <= 410; y += 10) ((y + 170) % 50 === 0 ? floorMajor : floor).push(-260, y, z0, 260, y, z0);
  for (let k = 0; k <= RU; k++) ugrid.push(-HOLE_X - 7, -0.8, k * U, HOLE_X + 7, -0.8, k * U);
  for (let k = 0; k < RU; k++){ const z = k * U + U / 2; uhalf.push(-HOLE_X - 7, -0.8, z, -HOLE_X + 14, -0.8, z, HOLE_X - 14, -0.8, z, HOLE_X + 7, -0.8, z); }
  const mk = arr => { const vao = gl.createVertexArray(); gl.bindVertexArray(vao); const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(arr), gl.STATIC_DRAW); gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0); gl.bindVertexArray(null); return {vao, n:arr.length / 3}; };
  lineBufs = {floor:mk(floor), floorMajor:mk(floorMajor), ugrid:mk(ugrid), uhalf:mk(uhalf)};
}

/* ================= camera ================= */
const cam = {target:[0,120,112], yaw:-0.62, pitch:0.34, dist:900, fov:30 * DEG};
const VIEWS = {front:{yaw:0, pitch:0.03}, side:{yaw:Math.PI / 2, pitch:0.03}, top:{yaw:0, pitch:1.53}, iso:{yaw:-0.62, pitch:0.34}};
let camAnim = null, VP = null, VPinv = null, EYE = [0,0,0], vw = 1, vh = 1;
function fitDist(){ const asp = vw / vh; return 860 * (345 + (RU - BASE_U) * U) / 345 * Math.max(1, (asp < 0.85 ? 1.25 : 0.95) / asp); }
const camTarget = () => [0, 120, 112 + (RU - BASE_U) * U / 2];
let lastView = 'iso';
function setView(v, animate = true){
  lastView = v; const to = {...VIEWS[v], target:camTarget(), dist:fitDist()};
  if (!animate || matchMedia('(prefers-reduced-motion: reduce)').matches){ Object.assign(cam, to); requestRender(); return; }
  let dy = to.yaw - cam.yaw; while (dy > Math.PI) dy -= 2 * Math.PI; while (dy < -Math.PI) dy += 2 * Math.PI;
  camAnim = {from:{yaw:cam.yaw, pitch:cam.pitch, dist:cam.dist, target:cam.target.slice()}, to:{...to, yaw:cam.yaw + dy}, t0:performance.now(), dur:420};
  requestRender();
}
function eye(){ const cp = Math.cos(cam.pitch), sp = Math.sin(cam.pitch); return [cam.target[0] + cam.dist * cp * Math.sin(cam.yaw), cam.target[1] - cam.dist * cp * Math.cos(cam.yaw), cam.target[2] + cam.dist * sp]; }
function camBasis(){
  const e = eye(), f = nrm(subv(cam.target, e));
  let s = crs(f, [0, 0, 1]); if (Math.hypot(...s) < 1e-4) s = [Math.cos(cam.yaw), Math.sin(cam.yaw), 0]; s = nrm(s);
  return {e, f, s, u:crs(s, f)};
}
function matMul(a, b){ const o = new Float32Array(16); for (let c = 0; c < 4; c++) for (let r = 0; r < 4; r++){ let v = 0; for (let k = 0; k < 4; k++) v += a[k*4+r] * b[c*4+k]; o[c*4+r] = v; } return o; }
function matInv(m){
  const inv = new Float32Array(16), a = m;
  inv[0]=a[5]*a[10]*a[15]-a[5]*a[11]*a[14]-a[9]*a[6]*a[15]+a[9]*a[7]*a[14]+a[13]*a[6]*a[11]-a[13]*a[7]*a[10];
  inv[4]=-a[4]*a[10]*a[15]+a[4]*a[11]*a[14]+a[8]*a[6]*a[15]-a[8]*a[7]*a[14]-a[12]*a[6]*a[11]+a[12]*a[7]*a[10];
  inv[8]=a[4]*a[9]*a[15]-a[4]*a[11]*a[13]-a[8]*a[5]*a[15]+a[8]*a[7]*a[13]+a[12]*a[5]*a[11]-a[12]*a[7]*a[9];
  inv[12]=-a[4]*a[9]*a[14]+a[4]*a[10]*a[13]+a[8]*a[5]*a[14]-a[8]*a[6]*a[13]-a[12]*a[5]*a[10]+a[12]*a[6]*a[9];
  inv[1]=-a[1]*a[10]*a[15]+a[1]*a[11]*a[14]+a[9]*a[2]*a[15]-a[9]*a[3]*a[14]-a[13]*a[2]*a[11]+a[13]*a[3]*a[10];
  inv[5]=a[0]*a[10]*a[15]-a[0]*a[11]*a[14]-a[8]*a[2]*a[15]+a[8]*a[3]*a[14]+a[12]*a[2]*a[11]-a[12]*a[3]*a[10];
  inv[9]=-a[0]*a[9]*a[15]+a[0]*a[11]*a[13]+a[8]*a[1]*a[15]-a[8]*a[3]*a[13]-a[12]*a[1]*a[11]+a[12]*a[3]*a[9];
  inv[13]=a[0]*a[9]*a[14]-a[0]*a[10]*a[13]-a[8]*a[1]*a[14]+a[8]*a[2]*a[13]+a[12]*a[1]*a[10]-a[12]*a[2]*a[9];
  inv[2]=a[1]*a[6]*a[15]-a[1]*a[7]*a[14]-a[5]*a[2]*a[15]+a[5]*a[3]*a[14]+a[13]*a[2]*a[7]-a[13]*a[3]*a[6];
  inv[6]=-a[0]*a[6]*a[15]+a[0]*a[7]*a[14]+a[4]*a[2]*a[15]-a[4]*a[3]*a[14]-a[12]*a[2]*a[7]+a[12]*a[3]*a[6];
  inv[10]=a[0]*a[5]*a[15]-a[0]*a[7]*a[13]-a[4]*a[1]*a[15]+a[4]*a[3]*a[13]+a[12]*a[1]*a[7]-a[12]*a[3]*a[5];
  inv[14]=-a[0]*a[5]*a[14]+a[0]*a[6]*a[13]+a[4]*a[1]*a[14]-a[4]*a[2]*a[13]-a[12]*a[1]*a[6]+a[12]*a[2]*a[5];
  inv[3]=-a[1]*a[6]*a[11]+a[1]*a[7]*a[10]+a[5]*a[2]*a[11]-a[5]*a[3]*a[10]-a[9]*a[2]*a[7]+a[9]*a[3]*a[6];
  inv[7]=a[0]*a[6]*a[11]-a[0]*a[7]*a[10]-a[4]*a[2]*a[11]+a[4]*a[3]*a[10]+a[8]*a[2]*a[7]-a[8]*a[3]*a[6];
  inv[11]=-a[0]*a[5]*a[11]+a[0]*a[7]*a[9]+a[4]*a[1]*a[11]-a[4]*a[3]*a[9]-a[8]*a[1]*a[7]+a[8]*a[3]*a[5];
  inv[15]=a[0]*a[5]*a[10]-a[0]*a[6]*a[9]-a[4]*a[1]*a[10]+a[4]*a[2]*a[9]+a[8]*a[1]*a[6]-a[8]*a[2]*a[5];
  let det = a[0]*inv[0]+a[1]*inv[4]+a[2]*inv[8]+a[3]*inv[12]; det = det ? 1 / det : 0;
  for (let i = 0; i < 16; i++) inv[i] *= det; return inv;
}
function updateMatrices(){
  const {e, f, s, u} = camBasis(); EYE = e;
  const view = new Float32Array([s[0],u[0],-f[0],0, s[1],u[1],-f[1],0, s[2],u[2],-f[2],0, -dot(s,e),-dot(u,e),dot(f,e),1]);
  const n = 5, fa = 6000, t = 1 / Math.tan(cam.fov / 2), asp = vw / vh;
  const proj = new Float32Array([t/asp,0,0,0, 0,t,0,0, 0,0,(fa+n)/(n-fa),-1, 0,0,2*fa*n/(n-fa),0]);
  VP = matMul(proj, view); VPinv = matInv(VP);
}
function project(p){
  const x = VP[0]*p[0]+VP[4]*p[1]+VP[8]*p[2]+VP[12], y = VP[1]*p[0]+VP[5]*p[1]+VP[9]*p[2]+VP[13], w = VP[3]*p[0]+VP[7]*p[1]+VP[11]*p[2]+VP[15];
  if (w <= 0.01) return null;
  return [(x / w * 0.5 + 0.5) * vw, (1 - (y / w * 0.5 + 0.5)) * vh];
}
function rayAt(px, py){
  const nx = px / vw * 2 - 1, ny = 1 - py / vh * 2;
  const un = (z) => { const m = VPinv; const x = m[0]*nx+m[4]*ny+m[8]*z+m[12], y = m[1]*nx+m[5]*ny+m[9]*z+m[13], zz = m[2]*nx+m[6]*ny+m[10]*z+m[14], w = m[3]*nx+m[7]*ny+m[11]*z+m[15]; return [x/w, y/w, zz/w]; };
  const a = un(-1), b = un(1); return {o:a, d:nrm(subv(b, a))};
}

/* ================= world poses & materials ================= */
function gearHU(typeKey){
  const T = TYPES[typeKey]; if (!T) return 1;
  if (T.imp) return T.imp.hU || autoHU(T.imp);
  return T.hU || 1;
}
function impRotation(m){ let R = I3; for (let k = 0; k < 3; k++) for (let i = 0; i < m.rot[k]; i++) R = m3(ROT[k], R); return R; }
function rotBox(R, lo, hi){
  const l = [Infinity, Infinity, Infinity], h = [-Infinity, -Infinity, -Infinity];
  for (let i = 0; i < 8; i++){ const v = mv(R, [i & 1 ? hi[0] : lo[0], i & 2 ? hi[1] : lo[1], i & 4 ? hi[2] : lo[2]]); for (let k = 0; k < 3; k++){ l[k] = Math.min(l[k], v[k]); h[k] = Math.max(h[k], v[k]); } }
  return {lo:l, hi:h};
}
function autoHU(m){ const b = rotBox(impRotation(m), m.lo, m.hi); return clamp(Math.ceil((b.hi[2] - b.lo[2]) / (U / 2) - 0.04) / 2, 0.5, RU); }
function mountPose(typeKey){
  const T = TYPES[typeKey];
  if (T.mount) return T.mount;
  if (T.imp) return impPose(T.imp);
  return pose(I3, [0,0,0]);
}
function rootOf(instId){ let i = instById(instId), guard = 0; while (i && S.at[i.id] && S.at[i.id].p && guard++ < 6) i = instById(S.at[i.id].p); return i; }
function placed(instId){ let a = S.at[instId], guard = 0; while (a && a.p && guard++ < 6) a = S.at[a.p]; return !!a && (a.s != null || a.u != null || !!a.top || !!a.wall); }
function worldPose(instId, overrideAt){
  const inst = instById(instId); if (!inst) return null;
  const a = overrideAt || S.at[instId]; if (!a) return null;
  const T = TYPES[inst.type];
  if (a.s){ const s = SLOT[a.s]; return pose(s.R, add(s.t, scl(s.ex, 70 * explode))); }
  if (T.dev && (a.u != null || a.top || a.wall)) return devPose(T, a);
  if (T.dev && a.p && a.off) return mountedPose(inst, a);
  if (a.u != null){ const m = mountPose(inst.type); return ptrans(m, [0, -115 * explode, a.u * U / 2]); }
  if (a.p){ const pw = worldPose(a.p); if (!pw || !placed(a.p)) return null; return ptrans(pw, [0, 60 * explode, 0]); }
  return null;
}
function meshOf(key){ if (key.startsWith('dev:')) return DEVMESH[key] || null; if (key.startsWith('imp:')){ const m = IMPORT_MESH[key.slice(4)]; return m && typeof m === 'object' ? m : null; } return MESH[key]; }
function material(inst, role){
  const T = TYPES[inst.type];
  const frame = lift(hexRgb(S.settings.frame));
  if (role === 'frame') return {c:frame, a:1, spec:.7};
  if (role === 'panel') return {c:mixRgb(frame, [1,1,1], .05), a:1, spec:.5};
  if (role === 'foot') return {c:mixRgb(frame, [0,0,0], .2), a:1, spec:.3};
  if (role === 'side') return S.settings.sides === 'clear' ? {c:mixRgb(frame, [1,1,1], .25), a:.26, spec:.4, glass:true} : {c:mixRgb(frame, [1,1,1], .05), a:1, spec:.5};
  if (role === 'pipe') return {c:[0.9,0.95,0.97], a:.6, spec:1, glass:true};
  if (role === 'tpl') return {c:[0.93,0.86,0.42], a:1, spec:.3};
  if (role === 'dev'){ const c = lift(hexRgb(T.dev.color)); return {c, a:1, spec:.5}; }
  if (role === 'devtrim'){ const c = lift(hexRgb(T.dev.color)); return {c:lum(c) > .5 ? mixRgb(c, [0,0,0], .35) : mixRgb(c, [1,1,1], .25), a:1, spec:.6}; }
  if (role.startsWith('port:')) return {c:hexRgb(PORT[role.slice(5)].color), a:1, spec:.9};
  const col = S.colors[inst.type] || T.color || 'slate';
  let c = hexRgb(fiberHex(col)); if (T.shade) c = mixRgb(c, [0,0,0], T.shade);
  return {c, a:1, spec:.6};
}
function visibleInst(inst){
  if (!placed(inst.id) || S.hidden[inst.id]) return false;
  if (isPanelSide(inst.type) && S.settings.sides === 'hidden') return false;
  const T = TYPES[inst.type]; return T.meshes.every(([k]) => meshOf(k));
}

/* ================= rendering ================= */
let needRender = false, dragState = null;
function requestRender(){ if (!needRender){ needRender = true; requestAnimationFrame(frame); } }
function resize(){
  const r = stage.getBoundingClientRect(), dpr = Math.min(2, window.devicePixelRatio || 1);
  vw = Math.max(1, r.width); vh = Math.max(1, r.height);
  canvas.width = Math.round(vw * dpr); canvas.height = Math.round(vh * dpr);
  requestRender();
}
function frame(t){
  needRender = false;
  if (camAnim){
    const k = clamp((performance.now() - camAnim.t0) / camAnim.dur, 0, 1), e = k < .5 ? 2*k*k : 1 - Math.pow(-2*k + 2, 2) / 2, A = camAnim.from, B = camAnim.to;
    cam.yaw = A.yaw + (B.yaw - A.yaw) * e; cam.pitch = A.pitch + (B.pitch - A.pitch) * e; cam.dist = A.dist + (B.dist - A.dist) * e;
    cam.target = A.target.map((v, i) => v + (B.target[i] - v) * e);
    if (k >= 1) camAnim = null; else requestRender();
  }
  draw(); drawOverlay();
}
function setMeshUniforms(M, c, a, emit, spec){
  gl.uniformMatrix4fv(U_M.uM, false, M); gl.uniform4f(U_M.uColor, c[0], c[1], c[2], a); gl.uniform3f(U_M.uEmit, emit[0], emit[1], emit[2]); gl.uniform1f(U_M.uSpec, spec);
}
function draw(){
  if (!gl) return;
  updateMatrices();
  gl.viewport(0, 0, canvas.width, canvas.height);
  gl.clearColor(COL.stage[0], COL.stage[1], COL.stage[2], 1); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
  gl.enable(gl.DEPTH_TEST); gl.depthMask(true); gl.disable(gl.BLEND);
  gl.useProgram(P_MESH); gl.uniformMatrix4fv(U_M.uVP, false, VP); gl.uniform3f(U_M.uEye, EYE[0], EYE[1], EYE[2]);
  const acc = COL.accent, glass = [];
  const lifted = dragState && dragState.active && dragState.kind === 'placed' ? dragState.instId : null;
  for (const inst of INST){
    if (!visibleInst(inst)) continue;
    const P = worldPose(inst.id); if (!P) continue;
    const M = poseMat(P), T = TYPES[inst.type];
    const isSel = sel && (sel === inst.id), isHov = hover && hover.inst === inst.id && !isSel;
    const fade = (lifted && (inst.id === lifted || rootOf(inst.id) && rootOf(inst.id).id === lifted)) || (mode === 'frame' && TYPES[inst.type].kind !== 'frame');
    for (const [mk, role] of T.meshes){
      const g = GPU[mk]; if (!g) continue;
      const mat = material(inst, role);
      const emit = isSel ? scl(acc, COL.dark ? .26 : .2) : isHov ? scl(acc, .1) : [0,0,0];
      if (mat.glass || fade){ glass.push({g, M, c:mat.c, a:fade ? .22 : mat.a, emit, spec:mat.spec}); continue; }
      setMeshUniforms(M, mat.c, 1, emit, mat.spec);
      gl.bindVertexArray(g.vao); gl.drawElements(gl.TRIANGLES, g.count, g.type, 0);
    }
  }
  // heat-set inserts (hidden while exploded, since the posts move apart)
  if (explode < 0.01 && GPU['dev:insert']){
    const g = GPU['dev:insert'], brass = [0.80, 0.62, 0.25];
    gl.bindVertexArray(g.vao);
    for (const k in S.inserts){ const h = holeWorld(k); setMeshUniforms(poseMat(pose(I3, h.p)), brass, 1, [0,0,0], 1); gl.drawElements(gl.TRIANGLES, g.count, g.type, 0); }
  }
  // cables
  updateRoutes();
  for (const c of S.cables || []){
    const g = GPU['cable:' + c.id], r = ROUTES.get(c.id); if (!g || !r) continue;
    let col = hexRgb(fiberHex(c.color || CABLE[r.kind].color));
    if (lum(col) < .1) col = mixRgb(col, [1,1,1], .12);
    const on = selCable === c.id, dim = mode === 'cables' && selCable && !on;
    const emit = on ? scl(acc, .35) : [0,0,0];
    if (dim || mode === 'frame'){ glass.push({g, M:poseMat(pose(I3, [0,0,0])), c:col, a:mode === 'frame' ? .25 : .45, emit, spec:.4}); continue; }
    setMeshUniforms(poseMat(pose(I3, [0,0,0])), col, 1, emit, .5); gl.bindVertexArray(g.vao); gl.drawElements(gl.TRIANGLES, g.count, g.type, 0);
  }
  // lines: floor grid and the U grid on the front plane
  gl.useProgram(P_LINE); gl.uniformMatrix4fv(U_L.uVP, false, VP); gl.uniformMatrix4fv(U_L.uM, false, poseMat(pose(I3, [0,0,0])));
  gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); gl.depthMask(false);
  const ink = COL.ink;
  const line = (b, a, c = ink) => { gl.uniform4f(U_L.uColor, c[0], c[1], c[2], a); gl.bindVertexArray(b.vao); gl.drawArrays(gl.LINES, 0, b.n); };
  line(lineBufs.floor, COL.dark ? .05 : .06); line(lineBufs.floorMajor, COL.dark ? .11 : .13);
  const showU = S.settings.labels || (dragState && dragState.active && dragState.gear);
  if (showU){ line(lineBufs.ugrid, .55, acc); line(lineBufs.uhalf, .4, acc); }
  // transparent parts, then the drag ghost
  gl.useProgram(P_MESH);
  glass.sort((a, b) => (b.back ? 1 : 0) - (a.back ? 1 : 0));
  for (const it of glass){ setMeshUniforms(it.M, it.c, it.a, it.emit, it.spec); gl.bindVertexArray(it.g.vao); gl.drawElements(gl.TRIANGLES, it.g.count, it.g.type, 0); }
  if (dragState && dragState.active && dragState.best){
    const b = dragState.best, T = TYPES[dragState.type];
    const P = b.pose;
    for (const [mk] of T.meshes){ const g = GPU[mk]; if (!g) continue; setMeshUniforms(poseMat(P), mixRgb(acc, [1,1,1], .25), .5, scl(acc, .25), .3); gl.bindVertexArray(g.vao); gl.drawElements(gl.TRIANGLES, g.count, g.type, 0); }
    for (const ch of b.children || []){ const T2 = TYPES[ch.type]; for (const [mk] of T2.meshes){ const g = GPU[mk]; if (!g) continue; setMeshUniforms(poseMat(ch.pose), mixRgb(acc, [1,1,1], .25), .4, scl(acc, .2), .3); gl.bindVertexArray(g.vao); gl.drawElements(gl.TRIANGLES, g.count, g.type, 0); } }
  }
  // pins (solid, then a faint pass that shows through parts)
  gl.depthMask(true);
  const pins = spots.filter(s => s.pin);
  if (pins.length){
    const g = GPU.__pin;
    for (const pass of [0, 1]){
      if (pass === 1){ gl.disable(gl.DEPTH_TEST); }
      for (const sp of pins){
        const on = activeSpot === sp.id, c = on ? acc : mixRgb(acc, COL.dark ? [1,1,1] : [0,0,0], .25);
        setMeshUniforms(poseMat(pinPose(sp.pin)), c, pass ? .28 : 1, scl(acc, on ? .35 : .15), .4);
        gl.bindVertexArray(g.vao); gl.drawElements(gl.TRIANGLES, g.count, g.type, 0);
      }
    }
    gl.enable(gl.DEPTH_TEST);
  }
  gl.bindVertexArray(null); gl.disable(gl.BLEND);
}
function pinPose(pin){
  const z = nrm(pin.n), a = Math.abs(z[2]) < .9 ? [0,0,1] : [1,0,0], x = nrm(crs(a, z)), y = crs(z, x);
  return pose([x[0], y[0], z[0], x[1], y[1], z[1], x[2], y[2], z[2]], pin.p);
}

/* ================= overlay labels ================= */
const tagEls = new Map();
function occluded(p){
  const d = subv(p, EYE), L = Math.hypot(d[0], d[1], d[2]), dir = scl(d, 1 / L);
  for (const inst of INST){
    if (!visibleInst(inst) || (isPanelSide(inst.type) && S.settings.sides === 'clear')) continue;
    const P = worldPose(inst.id); if (!P) continue;
    const lo = mtv(P.R, subv(EYE, P.t)), ld = mtv(P.R, dir), inv = ld.map(x => 1 / (Math.abs(x) < 1e-12 ? 1e-12 : x));
    for (const [mk] of TYPES[inst.type].meshes){ const m = meshOf(mk); if (!m || !rayBox(lo, inv, m.lo, m.hi, L - 4)) continue; if (rayMesh(mk, lo, ld, L - 4)) return true; }
  }
  return false;
}
function tag(key, cls, text, p, dimHidden){
  let el = tagEls.get(key);
  if (!el){ el = document.createElement('div'); overlay.appendChild(el); tagEls.set(key, el); }
  el.used = true; if (el.className !== 'tag ' + cls) el.className = 'tag ' + cls;
  if (el.textContent !== text) el.textContent = text;
  const s = p && project(p);
  if (!s || s[0] < -40 || s[1] < -40 || s[0] > vw + 40 || s[1] > vh + 40){ el.hidden = true; return; }
  el.hidden = false; el.style.left = s[0] + 'px'; el.style.top = s[1] + 'px';
  el.style.opacity = dimHidden && occluded(p) ? '0.3' : '';
}
function dotEl(key, cls, p, dimHidden){
  let el = tagEls.get(key);
  if (!el){ el = document.createElement('button'); el.type = 'button'; overlay.appendChild(el); tagEls.set(key, el); }
  el.used = true; if (el.className !== cls) el.className = cls;
  const s = project(p);
  if (!s || s[0] < -20 || s[1] < -20 || s[0] > vw + 20 || s[1] > vh + 20){ el.hidden = true; return el; }
  el.hidden = false; el.style.left = s[0] + 'px'; el.style.top = s[1] + 'px';
  el.style.opacity = dimHidden && occluded(p) ? '0.35' : '';
  return el;
}
overlay.addEventListener('click', e => {
  const h = e.target.closest('[data-hole]');
  if (h && mode === 'frame'){ const k = h.dataset.hole, on = !S.inserts[k]; commit(() => { if (on) S.inserts[k] = true; else delete S.inserts[k]; }); toast(`${holeName(k)} · insert ${on ? 'added' : 'removed'}`); return; }
  const pd = e.target.closest('[data-port]');
  if (pd && mode === 'cables'){ const [i, p] = pd.dataset.port.split('/'); tab = 'part'; connectPort(i, p); }
});
function drawOverlay(){
  for (const el of tagEls.values()) el.used = false;
  if (S.settings.labels){
    for (let k = 0; k < RU; k++) tag('u' + k, 'u', unitLabel(k), [-PX - 18, 0, k * U + U / 2]);
    const fz = RU * U - 17;
    tag('pFL', 'post', 'FL', [-PX - 6, -1, fz], true); tag('pFR', 'post', 'FR', [PX + 6, -1, fz], true); tag('pRL', 'post', 'RL', [-PX - 6, DEPTH + 1, fz], true); tag('pRR', 'post', 'RR', [PX + 6, DEPTH + 1, fz], true);
  }
  if (S.settings.labels && mode !== 'frame') for (const inst of INST){
    const T = TYPES[inst.type]; if (!T.dev || !placed(inst.id) || S.hidden[inst.id] || inst.type === 'dev_keystone') continue;
    const b = worldBox(inst.id); if (!b) continue;
    const a = S.at[inst.id], p = a.wall || a.top ? [(b.lo[0] + b.hi[0]) / 2, b.lo[1], b.hi[2] + 6] : [(b.lo[0] + b.hi[0]) / 2, b.lo[1] - 2, (b.lo[2] + b.hi[2]) / 2];
    tag('d' + inst.id, 'dev', T.dev.short, p, true);
  }
  if (mode === 'frame' && insertTool && explode < 0.01){
    const need = neededHoles();
    for (const post of POSTS) for (let k = 0; k < RU; k++){
      if (!columnOwner(post.code, k)) continue;
      for (let j = 0; j < 3; j++){
        const key = holeKey(post.code, k, j), h = holeWorld(key), p = [h.p[0], h.front ? -0.6 : DEPTH + 0.6, h.p[2]];
        const cls = 'hdot' + (S.inserts[key] ? ' on' : need.has(key) ? ' need' : '');
        const el = dotEl('h' + key, cls, p, !h.front); el.dataset.hole = key; el.title = holeName(key) + (S.inserts[key] ? ' · insert in' : need.has(key) ? ' · needs an insert' : ' · empty');
      }
    }
  }
  if (mode === 'cables') for (const inst of INST){
    if (!TYPES[inst.type].dev || S.hidden[inst.id]) continue;
    for (const pt of devPorts(inst.id)){
      const used = cableAt(inst.id, pt.id), pend = pendingPort && pendingPort.i === inst.id && pendingPort.p === pt.id;
      const el = dotEl('p' + inst.id + '/' + pt.id, 'pdot' + (used ? ' used' : '') + (pend ? ' pend' : '') + (used && used.id === selCable ? ' sel' : ''), pt.p, true);
      el.dataset.port = inst.id + '/' + pt.id; el.style.setProperty('--pc', PORT[pt.k].color);
      el.title = portLabel(inst.id, pt.id) + (pt.approx ? ' (≈ position)' : '') + (used ? ' · ' + cableName(used) : ' · free');
    }
  }
  spots.forEach(sp => { if (!sp.pin) return; tag('pin' + sp.id, 'pin' + (activeSpot === sp.id ? ' is-on' : ''), String(sp.n), papply(pinPose(sp.pin), [0,0,13])); });
  if (dragState && dragState.active){
    dragState.cands.forEach((c, i) => {
      const key = 'c' + i; let el = tagEls.get(key);
      if (!el){ el = document.createElement('div'); overlay.appendChild(el); tagEls.set(key, el); }
      el.className = 'cand' + (dragState.best === c ? ' best' : ''); el.used = true; el.textContent = '';
      const s = c.screen; if (!s){ el.hidden = true; return; } el.hidden = false; el.style.left = s[0] + 'px'; el.style.top = s[1] + 'px';
    });
  }
  for (const el of tagEls.values()) if (!el.used) el.hidden = true;
}

/* ================= picking ================= */
const BVH = {};
function bvhFor(key){
  if (BVH[key]) return BVH[key];
  const m = meshOf(key); if (!m) return null;
  const I = m.idx, P = m.pos, n = I.length / 3;
  const cen = new Float32Array(n * 3), tlo = new Float32Array(n * 3), thi = new Float32Array(n * 3);
  for (let t = 0; t < n; t++) for (let k = 0; k < 3; k++){
    const a = P[I[t*3]*3+k], b = P[I[t*3+1]*3+k], c = P[I[t*3+2]*3+k];
    tlo[t*3+k] = Math.min(a, b, c); thi[t*3+k] = Math.max(a, b, c); cen[t*3+k] = (a + b + c) / 3;
  }
  const order = new Uint32Array(n); for (let i = 0; i < n; i++) order[i] = i;
  const nodes = [];
  function build(s, e){
    const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity], cl = [Infinity, Infinity, Infinity], ch = [-Infinity, -Infinity, -Infinity];
    for (let i = s; i < e; i++){ const t = order[i]; for (let k = 0; k < 3; k++){ lo[k] = Math.min(lo[k], tlo[t*3+k]); hi[k] = Math.max(hi[k], thi[t*3+k]); cl[k] = Math.min(cl[k], cen[t*3+k]); ch[k] = Math.max(ch[k], cen[t*3+k]); } }
    const node = {lo, hi, l:-1, r:-1, s, e}; const id = nodes.push(node) - 1;
    if (e - s <= 8) return id;
    const ax = (ch[0]-cl[0] >= ch[1]-cl[1] && ch[0]-cl[0] >= ch[2]-cl[2]) ? 0 : (ch[1]-cl[1] >= ch[2]-cl[2] ? 1 : 2);
    const sub = Array.from(order.subarray(s, e)).sort((a, b) => cen[a*3+ax] - cen[b*3+ax]); order.set(sub, s);
    const mid = (s + e) >> 1; node.l = build(s, mid); node.r = build(mid, e); return id;
  }
  build(0, n);
  return BVH[key] = {nodes, order, m};
}
function rayBox(o, inv, lo, hi, tmax){
  let t0 = 0, t1 = tmax;
  for (let k = 0; k < 3; k++){ let a = (lo[k] - o[k]) * inv[k], b = (hi[k] - o[k]) * inv[k]; if (a > b){ const x = a; a = b; b = x; } t0 = Math.max(t0, a); t1 = Math.min(t1, b); if (t0 > t1) return false; }
  return true;
}
function rayMesh(key, o, d, tmax){
  const B = bvhFor(key); if (!B) return null;
  const {nodes, order, m} = B, P = m.pos, I = m.idx, inv = d.map(x => 1 / (Math.abs(x) < 1e-12 ? 1e-12 : x));
  let best = null, bt = tmax; const stack = [0];
  while (stack.length){
    const nd = nodes[stack.pop()];
    if (!rayBox(o, inv, nd.lo, nd.hi, bt)) continue;
    if (nd.l < 0){
      for (let i = nd.s; i < nd.e; i++){
        const t = order[i], ia = I[t*3]*3, ib = I[t*3+1]*3, ic = I[t*3+2]*3;
        const e1 = [P[ib]-P[ia], P[ib+1]-P[ia+1], P[ib+2]-P[ia+2]], e2 = [P[ic]-P[ia], P[ic+1]-P[ia+1], P[ic+2]-P[ia+2]];
        const h = crs(d, e2), det = dot(e1, h); if (Math.abs(det) < 1e-12) continue;
        const f = 1 / det, s = [o[0]-P[ia], o[1]-P[ia+1], o[2]-P[ia+2]], u = f * dot(s, h); if (u < 0 || u > 1) continue;
        const q = crs(s, e1), v = f * dot(d, q); if (v < 0 || u + v > 1) continue;
        const tt = f * dot(e2, q); if (tt > 1e-4 && tt < bt){ bt = tt; best = {t:tt, n:nrm(crs(e1, e2))}; }
      }
    } else { stack.push(nd.l, nd.r); }
  }
  return best;
}
function pick(px, py){
  const r = rayAt(px, py); let best = null;
  for (const inst of INST){
    if (!visibleInst(inst)) continue;
    if (isPanelSide(inst.type) && S.settings.sides === 'clear') continue;
    if (mode === 'frame' && TYPES[inst.type].kind !== 'frame') continue;
    const P = worldPose(inst.id); if (!P) continue;
    const lo = mtv(P.R, subv(r.o, P.t)), ld = mtv(P.R, r.d);
    for (const [mk] of TYPES[inst.type].meshes){
      const m = meshOf(mk); if (!m) continue;
      const inv = ld.map(x => 1 / (Math.abs(x) < 1e-12 ? 1e-12 : x));
      if (!rayBox(lo, inv, m.lo, m.hi, best ? best.t : 1e7)) continue;
      const h = rayMesh(mk, lo, ld, best ? best.t : 1e7);
      if (h && (!best || h.t < best.t)){ let n = mv(P.R, h.n); if (dot(n, r.d) > 0) n = scl(n, -1); best = {t:h.t, inst:inst.id, p:add(r.o, scl(r.d, h.t)), n}; }
    }
  }
  // A ray aimed into a screw hole passes straight through it; report the hole itself.
  for (const [py, codes] of [[0, ['FL','FR']], [DEPTH, ['RL','RR']]]){
    if (Math.abs(r.d[1]) < 1e-6) continue;
    const t = (py - r.o[1]) / r.d[1]; if (t <= 0 || (best && best.t < t + 7)) continue;
    const q = add(r.o, scl(r.d, t));
    for (const code of codes){
      const hx = code[1] === 'L' ? -HOLE_X : HOLE_X;
      for (let k = 0; k < RU; k++) for (let j = 0; j < 3; j++){
        const owner = columnOwner(code, k);
        if (!owner || !visibleInst(owner)) continue;
        if (Math.hypot(q[0] - hx, q[2] - (k * U + HOLE_Z[j])) <= 4.2) return {t, inst:owner.id, p:[hx, py, k * U + HOLE_Z[j]], n:[0, py ? 1 : -1, 0], hole:true};
      }
    }
  }
  return best;
}

/* ================= references ================= */
const planU = () => RU; // units are numbered over the frame as built
/* the piece that carries unit k (counted from the bottom) of a post column */
function columnOwner(code, k){
  let z = 0;
  for (let i = 0; i < S.levels.length; i++){
    const n = levelU(S.levels[i]);
    if (k >= z && k < z + n){ const sid = S.levels[i].k === 'mod' ? `M${i}${code[1]}` : `P${i}${code}`; return INST.find(x => S.at[x.id] && S.at[x.id].s === sid) || null; }
    z += n;
  }
  return null;
}
function unitLabel(k){ return 'U' + (S.settings.numbering === 'top' ? planU() - k : k + 1); }
function spanLabel(hb, hU){
  const b = hb / 2, t = b + hU;
  if (b % 1 === 0 && t % 1 === 0){ const a = unitLabel(b), z = unitLabel(t - 1); return a === z ? a : (S.settings.numbering === 'top' ? z + '–' + a : a + '–' + z); }
  const loU = Math.floor(b), hiU = Math.ceil(t) - 1;
  if (loU === hiU) return unitLabel(loU) + (b % 1 ? ' upper ½' : ' lower ½');
  const lo = unitLabel(loU) + (b % 1 ? ' upper ½' : ''), hi = unitLabel(hiU) + (t % 1 ? ' lower ½' : '');
  return S.settings.numbering === 'top' ? hi + ' – ' + lo : lo + ' – ' + hi;
}
function holeRef(post, k, j){ return post + '-' + unitLabel(k) + 'abc'[j]; }
function refFor(p, n){
  const r = {};
  const k = Math.floor(p[2] / U);
  if (k >= 0 && k < RU) r.unit = unitLabel(k) + (p[2] - k * U >= U / 2 ? ' upper ½' : ' lower ½');
  else if (p[2] >= RU * U) r.unit = 'top frame (above ' + unitLabel(RU - 1) + ')';
  else r.unit = 'base frame (below ' + unitLabel(0) + ')';
  let best = null;
  for (const post of POSTS){
    if (p[1] < post.y0 - 2.5 || p[1] > post.y1 + 2.5) continue;
    for (let kk = 0; kk < RU; kk++) for (let j = 0; j < 3; j++){ const d = Math.hypot(p[0] - post.x, p[2] - (kk * U + HOLE_Z[j])); if (!best || d < best.d) best = {d, code:holeRef(post.code, kk, j)}; }
  }
  r.hole = best && best.d <= 6.5 ? best.code : null;
  r.side = Math.abs(p[0]) < 15 ? 'centre' : p[0] < 0 ? 'left' : 'right';
  r.depth = p[1] < 1.5 ? 'front face' : p[1] > DEPTH - 1.5 ? 'rear face' : Math.round(p[1]) + ' mm back';
  r.code = r.hole || (r.unit + ' · ' + r.side);
  r.xyz = `X ${fmt(p[0])} · Y ${fmt(p[1])} · Z ${fmt(p[2])} mm`;
  if (n){ const a = n.map(Math.abs), i = a.indexOf(Math.max(...a)); r.facing = [['right','left'],['rear','front'],['up','down']][i][n[i] > 0 ? 0 : 1]; }
  return r;
}
function instLabel(id){
  const inst = instById(id); if (!inst) return '';
  const T = TYPES[inst.type], a = S.at[id];
  if (a && a.s) return SLOT[a.s].label + (SLOT[a.s].code ? ' (' + SLOT[a.s].code + ')' : '');
  return T.name;
}
function instWhere(id){
  const inst = instById(id), a = S.at[id]; if (!inst || !a) return 'In the tray';
  if (a.s){ const sl = SLOT[a.s]; return sl.label + (sl.span ? ' · ' + spanLabel(sl.span[0] * 2, sl.span[1]) : ''); }
  if (TYPES[inst.type].dev && (a.u != null || a.top || a.wall || a.off)) return devWhere(id);
  if (a.u != null) return spanLabel(a.u, gearHU(inst.type));
  if (a.p){ const par = instById(a.p); return placed(id) ? 'On ' + TYPES[par.type].name + ' · ' + instWhere(a.p) : 'On ' + TYPES[par.type].name + ' (in the tray)'; }
  return '';
}

/* ================= placement ================= */
function gearOcc(exclude){ const occ = []; for (const inst of INST){ const a = S.at[inst.id]; if (!a || a.u == null || inst.id === exclude) continue; const h2 = Math.round(gearHU(inst.type) * 2); for (let k = 0; k < h2; k++) occ[a.u + k] = inst.id; } return occ; }
function childrenOf(id){ return INST.filter(i => S.at[i.id] && S.at[i.id].p === id); }
function candidates(typeKey, instId){
  const T = TYPES[typeKey], out = [];
  if (!T || !T.meshes.every(([k]) => meshOf(k))) return out;
  if (T.kind === 'frame'){
    const slotCand = (s, extra) => { const anchor = add(s.t, scl(s.ex, 70 * explode)); return {at:{s:s.id}, label:s.label + (s.span ? ' · ' + spanLabel(s.span[0] * 2, s.span[1]) : ''), anchor, pose:pose(s.R, anchor), ...extra}; };
    for (const s of SLOTS){
      if (s.type !== typeKey) continue;
      const occ = INST.find(i => S.at[i.id] && S.at[i.id].s === s.id);
      if (occ && occ.id !== instId) continue;
      out.push(slotCand(s));
    }
    if (typeKey === 'ext_module'){
      // a support extension can sit in any joint of the stack; moving one moves its whole level (both sides)
      const cur = instId && S.at[instId] ? slotLevel(S.at[instId].s) : -1, side = cur >= 0 ? S.at[instId].s.slice(-1) : null;
      if (cur >= 0) out.length = 0; // a placed extension only moves between joints
      let z = 0;
      for (let j = 0; j <= S.levels.length; j++){
        if (j > 0) z += levelU(S.levels[j - 1]) * U;
        if (cur >= 0 && (j === cur || j === cur + 1)) continue;
        if (RU + (cur >= 0 ? 0 : 1) > 15) break;
        const zj = cur >= 0 && j > cur ? z - U : z;
        for (const sl of levelSlots(j, {k:'mod'}, zj)) if (!side || sl.id.endsWith(side))
          out.push(slotCand(sl, {insertAt:j, moveFrom:cur >= 0 ? cur : null, label:sl.label + ' · ' + jointName(j, cur)}));
      }
    } else if (T.size && /^post/.test(typeKey)){
      const lv = {k:'post', u:T.size}, i = S.levels.length;
      const mine = instId && S.at[instId] && slotLevel(S.at[instId].s) === i - 1 && INST.filter(x => S.at[x.id] && slotLevel(S.at[x.id].s) === i - 1).length === 1;
      if (!mine && RU + levelU(lv) <= 15){
        const k0 = RU, nU = levelU(lv);
        for (const sl of levelSlots(i, lv, RU * U)) if (sl.type === typeKey)
          out.push(slotCand(sl, {newLevel:lv, label:sl.label + ' · new level on top (' + (S.settings.numbering === 'top' ? 'adds ' + nU + 'U' : spanLabel(k0 * 2, nU)) + ')'}));
      }
    }
  } else if (T.dev && T.kind === 'gear'){
    return devCandidates(typeKey, instId);
  } else if (T.kind === 'gear'){
    const hU = gearHU(typeKey), h2 = Math.round(hU * 2), step = hU % 1 ? 1 : 2;
    const kids = instId ? childrenOf(instId) : [];
    for (let hb = RU * 2 - h2; hb >= 0; hb -= 1){
      if (hb % step) continue;
      if (!cellsFree(typeKey, {u:hb}, instId)) continue;
      const m = mountPose(typeKey), P = ptrans(m, [0, -115 * explode, hb * U / 2]);
      out.push({at:{u:hb}, label:spanLabel(hb, hU), anchor:[0, -14, hb * U / 2 + hU * U / 2], pose:P,
        children:kids.map(ch => ({type:ch.type, pose:ptrans(P, [0, 60 * explode, 0])}))});
    }
  } else if (T.kind === 'attach'){
    for (const par of INST){
      if (par.type !== T.parent || !placed(par.id)) continue;
      const taken = INST.find(i => i.type === typeKey && i.id !== instId && S.at[i.id] && S.at[i.id].p === par.id);
      if (taken) continue;
      const P = ptrans(worldPose(par.id), [0, 60 * explode, 0]);
      const m = meshOf(T.meshes[0][0]); const c = papply(P, [(m.lo[0]+m.hi[0])/2, (m.lo[1]+m.hi[1])/2, (m.lo[2]+m.hi[2])/2]);
      out.push({at:{p:par.id}, label:'on ' + TYPES[par.type].name + ' · ' + instWhere(par.id), anchor:c, pose:P});
    }
  }
  return out;
}
function nextUnplaced(typeKey){ return INST.find(i => i.type === typeKey && !S.at[i.id]); }
function placeCandidate(typeKey, instId, c){
  let id = instId;
  if (c.insertAt != null){
    if (c.moveFrom != null){ moveLevelTo(c.moveFrom, c.insertAt); return id; } // the whole level moves; slot ids follow
    insertLevel(c.insertAt, {k:'mod'});
    c = {...c, at:{s:'M' + c.insertAt + c.at.s.slice(-1)}};
  }
  if (c.newLevel){ S.levels.push({...c.newLevel}); buildSlots(); }
  if (!id){ id = newFrameId(); S.frame[id] = typeKey; }
  S.at[id] = c.at;
  if (typeKey === 'cable_guide'){ const sl = SLOT[c.at.s]; if (sl) for (const h of guideHoles(sl.acc.col, sl.acc.k)) S.inserts[h] = true; }
  return id;
}
function installType(typeKey, quiet){
  const T = TYPES[typeKey];
  if (T.bin){
    const cands = candidates(typeKey, null);
    if (!cands.length){ if (!quiet) toast(isPanelSide(typeKey) ? `Add a ${T.size}U post level first` : `No open spot for a ${T.name.toLowerCase()}`); return false; }
    let c = cands.find(x => !x.newLevel && x.insertAt == null) || cands[cands.length - 1];
    if (typeKey === 'cable_guide'){ // first choice: a front post at a unit no mount's ears use
      const occ = occupancy(), freeU = k => ![2 * k, 2 * k + 1].some(h => occ.has(`${h}|L|F`) || occ.has(`${h}|R|F`));
      c = cands.filter(x => SLOT[x.at.s].acc.col[0] === 'F' && freeU(SLOT[x.at.s].acc.k)).pop() || c;
    }
    let id = null; commit(() => { id = placeCandidate(typeKey, null, c); sel = id; });
    if (!quiet) toast(`${T.name} → ${c.label}${typeKey === 'cable_guide' ? ' · inserts added at a and c' : ''}`);
    return true;
  }
  const inst = nextUnplaced(typeKey);
  if (!inst){ if (!quiet) toast(`Every ${T.name.toLowerCase()} is already on the rack`); return false; }
  const cands = candidates(typeKey, inst.id);
  if (!cands.length){ if (!quiet) toast(T.kind === 'attach' ? `Put the ${TYPES[T.parent].name} on the rack first` : `No open spot for the ${T.name}`); return false; }
  let c = cands[0];
  if (T.kind === 'gear' && T.defU != null) c = cands.find(x => x.at.u === T.defU) || c;
  if (T.dev){ const br = matchingBracket(T.key), f = br && fitInBracket(T.key, br.id, 0, inst.id);
    if (f) c = {at:{p:br.id, off:f.off, rz:0}, label:'in ' + TYPES[br.type].name};
    else { const at = defAt(T.dev, inst.id); if (at) c = {at, label:'its planned spot'}; } }
  if (quiet === 'batch'){ S.at[inst.id] = c.at; return true; }
  commit(() => { S.at[inst.id] = c.at; sel = inst.id; });
  toast(`${T.name} → ${c.label}`);
  return true;
}
function assembleAll(){
  if (mode === 'cables'){ commit(() => { S.cables = planWiring(); selCable = null; pendingPort = null; }); toast(`Planned wiring: ${S.cables.length} cables`); return; }
  if (mode === 'frame'){
    if (!S.levels.length){ toast('Pick a starting stack, or drag posts onto the base first'); return; }
    commit(() => fillFrame()); toast('Every open frame spot is filled'); return;
  }
  commit(() => {
    const order = Object.keys(TYPES).filter(k => !TYPES[k].bin).sort((a, b) => (TYPES[a].kind === 'gear' ? 0 : 1) - (TYPES[b].kind === 'gear' ? 0 : 1));
    for (let pass = 0; pass < 2; pass++) for (const k of order){ let guard = 0; while (guard++ < 12 && nextUnplaced(k) && installType(k, 'batch')) validateAt(); }
  });
  toast('All the gear that fits is on the rack');
}
function takeApart(){
  if (mode === 'cables'){ commit(() => { S.cables = []; selCable = null; pendingPort = null; }); toast('All cables removed — Undo puts them back'); return; }
  if (mode === 'frame'){ commit(() => { clearFrame(); sel = null; }); toast('Frame cleared — the gear is back in the tray. Undo puts it back'); return; }
  commit(() => { for (const i of INST) if (TYPES[i.type].kind !== 'frame') delete S.at[i.id]; sel = null; }); toast('All gear is back in the tray — Undo puts it back');
}
function usePreset(name){
  if (name === 'plan'){ let n = 0; commit(() => { for (const i of INST) if (TYPES[i.type].dev) delete S.at[i.id]; applyPlannedLayout(); validateAt(); n = fillBrackets(); sel = null; }); toast('Equipment is in its planned spots' + (n ? ` · ${n} in their brackets` : '')); return; }
  if (name === 'brackets'){ let n = 0; commit(() => { n = fillBrackets(); }); toast(n ? `${n} device${n > 1 ? 's' : ''} put in matching brackets` : 'No matching brackets on the rack (I match by the bracket’s file name)'); return; }
  commit(() => { applyPreset(name); sel = null; }); setView(lastView); toast(`Frame: ${stackText()} = ${RU}U`); }
function unplace(id){
  const inst = instById(id); if (!inst || !canEdit(id)) return; const T = TYPES[inst.type], wasRU = RU;
  commit(() => { delete S.at[id]; if (T.bin) delete S.frame[id]; if (sel === id) sel = null; });
  toast(T.bin ? `${T.name} removed${RU !== wasRU ? ` — the stack is now ${RU}U` : ''}` : `${T.name} is back in the tray`);
}
function moveLevel(id, dir){
  const a = S.at[id], i = a && a.s ? slotLevel(a.s) : -1; if (i < 0) return;
  const j = i + dir;
  if (j < 0 || j >= S.levels.length){ toast(dir > 0 ? 'Already at the top of the stack' : 'Already at the bottom of the stack'); return; }
  commit(() => { const order = S.levels.map((_, k) => k); order[i] = j; order[j] = i; reorderLevels(order); });
  const k = slotLevel(S.at[id].s); toast(`1U support extension → ${jointName(k, k)}`);
}
function moveGear(id, dir){
  const inst = instById(id), a = S.at[id]; if (!inst || !a) return;
  if (a.wall){ moveDev(id, 0, dir * 20); return; }
  if (a.u == null) return;
  const hU = gearHU(inst.type), step = hU % 1 ? 1 : 2, h2 = Math.round(hU * 2);
  for (let hb = a.u + dir * step; hb >= 0 && hb + h2 <= RU * 2; hb += dir * step){
    const at = {...a, u:hb};
    if (cellsFree(inst.type, at, id)){ commit(() => { S.at[id] = at; }); return; }
  }
  toast(dir > 0 ? 'Already at the highest open spot' : 'Already at the lowest open spot');
}

/* ================= UI: tray ================= */
function typeSwatch(T){
  if (T.kind === 'frame') return S.settings.frame;
  return fiberHex(S.colors[T.key] || T.color || 'slate');
}
function renderTray(){
  $('#trayTitle').textContent = mode === 'frame' ? 'Frame parts' : mode === 'cables' ? 'Cables' : 'Gear';
  $('#assembleAll').textContent = mode === 'frame' ? 'Fill open spots' : mode === 'cables' ? 'Planned wiring' : 'Put all gear on';
  $('#takeApart').textContent = mode === 'frame' ? 'Clear frame' : mode === 'cables' ? 'Remove all cables' : 'Take all gear off';
  const pr = $('#presetRow'); pr.hidden = mode === 'cables';
  const want = mode === 'frame' ? 'frame' : 'gear';
  if (pr.dataset.for !== want){
    pr.dataset.for = want;
    pr.innerHTML = want === 'frame' ? `<span class="eyebrow" style="align-self:center">Start from</span><button class="btn small" data-preset="nine">9U · 5 + 1 + 3</button><button class="btn small" data-preset="eight">8U · 5 + 3</button><button class="btn small" data-preset="five">5U</button>`
      : `<span class="eyebrow" style="align-self:center">Layout</span><button class="btn small" data-preset="plan">Planned layout</button><button class="btn small" data-preset="brackets" title="Put each device in the bracket whose name matches it">Gear into brackets</button>`;
  }
  $('#trayHint').textContent = mode === 'frame'
    ? 'Build bottom-up. Drop posts on the corners (or on top of the stack to start a new level), then cap it. Accessories bolt to the post holes. The bins never run out.'
    : mode === 'cables' ? 'Click a coloured port dot on a device, then the port at the other end. Cables route along the rear spines on their own; click one to change it.'
    : 'Drag gear onto the rack and it snaps to the nearest open spot: rack gear to a U (half-width gear to a side), the router to the top, and wall gear onto the wall behind the rack.';
  $('#trayDrop').textContent = mode === 'frame' ? 'Drag a selected frame part here to remove it' : 'Drag selected gear here to take it off the rack';
  $('#trayDrop').hidden = mode === 'cables';
  let html = '';
  if (mode === 'cables'){
    updateRoutes();
    const groups = {};
    for (const c of S.cables){ const r = ROUTES.get(c.id), k = r ? r.kind : 'off'; (groups[k] = groups[k] || []).push([c, r]); }
    const order = ['cat6','coax','usb','hdmi','dc','ac','misc','off'];
    html = order.filter(k => groups[k]).map(k => `<div class="group"><div class="group-h"><h3 class="eyebrow">${k === 'off' ? 'An end is off the rack' : esc(CABLE[k].name)}</h3><small>${groups[k].length}</small></div>${groups[k].map(([c, r]) => `<button class="part cablerow${selCable === c.id ? ' is-sel' : ''}" data-cable="${c.id}">
        <span class="sw" style="background:${fiberHex(c.color || (r ? CABLE[r.kind].color : 'slate'))}"></span>
        <span class="p-name">${esc(cableName(c))}<small>${r ? esc(cableBuy(r)) : 'not drawn'}</small></span>
        <span class="p-n mono">${r ? Math.round(r.len) + ' mm' : '—'}</span></button>`).join('')}</div>`).join('') || '<p class="hint">No cables yet. Use <b>Planned wiring</b> for the build plan, or click a port dot to start one.</p>';
    $('#trayList').innerHTML = html; return;
  }
  if (mode === 'frame'){
    html += `<div class="stackbox"><span class="eyebrow">Stack</span><b>${S.levels.length ? esc(stackText()) + ' = ' + RU + 'U' : 'Empty — drop posts on the base'}</b>${directJoints() ? `<small>${directJoints()} post-to-post joint${directJoints() > 1 ? 's need' : ' needs'} joiner plates (not modelled)</small>` : ''}</div>`;
    html += insertsBox();
    html += FGROUPS.map(([fg, title, sub]) => {
      const types = Object.values(TYPES).filter(T => T.bin && T.fg === fg);
      const rows = types.map(T => {
        const n = INST.filter(i => i.type === T.key && placed(i.id)).length, open = candidates(T.key, null).length;
        const loading = T.meshes.some(([k]) => !meshOf(k));
        return `<button class="part${open ? '' : ' is-done'}" data-type="${esc(T.key)}" ${loading ? 'disabled' : ''} title="${open ? 'Drag onto the rack, or click to add one' : 'No open spot right now'}">
          <span class="sw" style="background:${typeSwatch(T)}"></span>
          <span class="p-name">${esc(T.name)}<small>${esc(T.hint)}</small></span>
          <span class="p-n">${n ? `<b>${n}</b> on` : '—'}</span></button>`;
      }).join('');
      return `<div class="group"><div class="group-h"><h3 class="eyebrow">${esc(title)}</h3><small>${esc(sub)}</small></div>${rows}</div>`;
    }).join('');
  } else {
    html = GROUPS.filter(g => g.id !== 'frame').map(g => {
      const types = Object.values(TYPES).filter(T => T.group === g.id);
      if (!types.length && g.id !== 'import') return '';
      const insts = INST.filter(i => TYPES[i.type].group === g.id), on = insts.filter(i => placed(i.id)).length;
      const rows = types.map(T => {
        const all = INST.filter(i => i.type === T.key), n = all.filter(i => placed(i.id)).length, loose = all.filter(i => !S.at[i.id]).length;
        const loading = T.meshes.some(([k]) => !meshOf(k));
        const sub = T.dev ? (T.dev.zone === 'rack' ? `${fmtHU(T.dev.hU)}${T.dev.side === 'half' ? ' · half width' : ''} · ${ZONE_NAME.rack}` : T.dev.zone === 'attach' ? `goes in the ${TYPES[T.parent].name.replace(' faceplate', ' bracket')}` : ZONE_NAME[T.dev.zone])
          : T.kind === 'gear' ? `${fmtHU(gearHU(T.key))} · snaps to a U` : `attaches to ${TYPES[T.parent] ? TYPES[T.parent].name : 'its partner'}`;
        return `<button class="part${loose ? '' : ' is-done'}" data-type="${esc(T.key)}" ${loading ? 'disabled' : ''} title="${loose ? 'Drag onto the rack, or click to add it' : 'All placed'}">
          <span class="sw" style="background:${typeSwatch(T)}"></span>
          <span class="p-name">${esc(T.name)}<small>${loading ? (IMPORT_MESH[T.key.slice(4)] === 'missing' ? 'file missing' : 'loading…') : esc(sub)}</small></span>
          <span class="p-n"><b>${n}</b>/${all.length}</span></button>`;
      }).join('');
      const empty = g.id === 'import' && !types.length ? `<p class="hint">Import STL or 3MF files to add your own brackets. Files designed together keep their fit.</p>` : '';
      return `<div class="group"><div class="group-h"><h3 class="eyebrow">${esc(g.title)}</h3><small>${insts.length ? on + '/' + insts.length + ' on' : esc(g.sub)}</small></div>${rows}${empty}</div>`;
    }).join('');
  }
  $('#trayList').innerHTML = html;
}
/* post levels stacked straight onto each other (no support extension between) are held by joiner plates */
function directJoints(){ let n = 0; for (let i = 1; i < S.levels.length; i++) if (S.levels[i].k === 'post' && S.levels[i - 1].k === 'post') n++; return n; }
const fmtHU = h => (h % 1 ? (Math.floor(h) || '') + '½' : h) + 'U';

/* ================= UI: inspector ================= */
let tab = 'part', confirmDel = null;
function renderTabs(){
  document.querySelectorAll('.tabs [role=tab]').forEach(b => b.setAttribute('aria-selected', String(b.dataset.tab === tab)));
  $('#tab-part').hidden = tab !== 'part'; $('#tab-ask').hidden = tab !== 'ask'; $('#tab-ref').hidden = tab !== 'ref';
  const c = $('#spotCount'); c.hidden = !spots.length; c.textContent = spots.length;
}
function renderPart(){
  const el = $('#tab-part'), inst = sel && instById(sel);
  if (mode === 'cables' && (selCable || !inst)){ el.innerHTML = cablePanel(); return; }
  if (!inst){
    const tot = INST.length, on = INST.filter(i => placed(i.id)).length;
    const gr = GROUPS.map(g => { const ii = INST.filter(i => TYPES[i.type].group === g.id); if (!ii.length) return ''; const n = ii.filter(i => placed(i.id)).length;
      return `<div class="meter"><span>${esc(g.title)}</span><span class="mono">${n}/${ii.length}</span><div class="bar"><i style="width:${(n / ii.length * 100).toFixed(1)}%"></i></div></div>`; }).join('');
    el.innerHTML = `<h2>Build</h2>
      <p class="note">${on} of ${tot} parts on the rack. Click a part to see its position and options.</p>
      ${gr}
      <div class="sec"><h3>Controls</h3><dl class="keys">
        <dt>Drag</dt><dd style="margin:0">Orbit the view</dd>
        <dt>Right-drag or <kbd>Shift</kbd>+drag</dt><dd style="margin:0">Pan</dd>
        <dt>Scroll or pinch</dt><dd style="margin:0">Zoom</dd>
        <dt>Click a part, then drag it</dt><dd style="margin:0">Move it to another spot, or onto the tray</dd>
        <dt><kbd>↑</kbd> <kbd>↓</kbd></dt><dd style="margin:0">Move selected gear by its snap step</dd>
        <dt><kbd>Del</kbd></dt><dd style="margin:0">Take the selected part off</dd>
        <dt><kbd>Ctrl</kbd> <kbd>Z</kbd></dt><dd style="margin:0">Undo</dd>
      </dl></div>`;
    return;
  }
  const T = TYPES[inst.type], a = S.at[inst.id], on = placed(inst.id), P = on ? worldPose(inst.id) : null;
  let size = '', tris = 0;
  { const lo = [Infinity,Infinity,Infinity], hi = [-Infinity,-Infinity,-Infinity];
    for (const [mk] of T.meshes){ const m = meshOf(mk); if (!m) continue; tris += m.tris; const R = P ? P.R : (T.imp && T.imp.role === 'gear' ? impRotation(T.imp) : I3); const b = rotBox(R, m.lo, m.hi); for (let k = 0; k < 3; k++){ lo[k] = Math.min(lo[k], b.lo[k]); hi[k] = Math.max(hi[k], b.hi[k]); } }
    if (lo[0] < Infinity) size = `${(hi[0]-lo[0]).toFixed(1)} × ${(hi[1]-lo[1]).toFixed(1)} × ${(hi[2]-lo[2]).toFixed(1)} mm`; }
  const editable = canEdit(inst.id);
  const code = !on ? '' : a.s ? (SLOT[a.s].code ? SLOT[a.s].code + ' post' : SLOT[a.s].label) : instWhere(inst.id);
  const kids = childrenOf(inst.id);
  let html = `<div class="insp-head"><span class="sw" style="background:${typeSwatch(T)}"></span><h3>${esc(on ? instLabel(inst.id) : T.name)}</h3><span class="pill${on ? '' : ' off'}">${on ? 'On the rack' : 'In the tray'}</span></div>
    ${on ? `<div class="refbox"><code>${esc(code)}</code><button class="btn small" data-act="copyRef" data-ref="${esc(code)}">Copy</button></div>` : ''}
    <dl class="kv">
      <dt>Part</dt><dd>${esc(T.name)}</dd>
      <dt>Where</dt><dd>${esc(instWhere(inst.id))}</dd>
      ${kids.length ? `<dt>Attached</dt><dd>${kids.map(k => esc(TYPES[k.type].name)).join(', ')}</dd>` : ''}
      <dt>Size</dt><dd class="mono">${size || '—'}</dd>
      <dt>Source</dt><dd class="mono">${esc(T.src || '')}</dd>
      ${T.bin && !draggableNow(inst.id) ? '' : ''}
      <dt>Mesh</dt><dd class="mono">${tris.toLocaleString()} triangles</dd>
    </dl>
    <div class="actions">
      ${editable && (T.kind === 'gear' || inst.type === 'ext_module') && on && !(a && (a.top || a.off)) ? `<button class="btn" data-act="up">▲ Up</button><button class="btn" data-act="down">▼ Down</button>` : ''}
      ${editable && on && a && a.wall ? `<button class="btn" data-act="left">◀ Left</button><button class="btn" data-act="right">Right ▶</button>` : ''}
      ${editable && on && a && a.u != null && T.dev && T.dev.side === 'half' ? `<button class="btn" data-act="swap">Swap side</button>` : ''}
      ${!editable ? '' : on ? `<button class="btn" data-act="remove">${T.bin ? 'Remove' : 'Take off'}</button>` : `<button class="btn primary" data-act="install">Put on the rack</button>`}
      ${on ? `<button class="btn" data-act="hide">${S.hidden[inst.id] ? 'Show' : 'Hide'} in view</button>` : ''}
      <button class="btn" data-act="ask">Ask about this part</button>
    </div>
    ${editable ? '' : `<p class="note">${T.kind === 'frame' ? 'The frame is locked outside Frame mode. Switch to <b>Frame</b> to change it.' : 'Gear moves only in Gear mode. Switch to <b>Gear</b> to move it.'}</p>`}`;
  if (T.dev) html += devSection(inst);
  if (inst.type === 'cable_guide' && on){ const sl = SLOT[a.s], hs = guideHoles(sl.acc.col, sl.acc.k), cl = clashes().get(inst.id);
    html += `<div class="sec"><h3>Mounting</h3><p class="note">Two M6 × 10 screws into heat-set inserts at <span class="mono">${hs.map(holeName).join('</span> and <span class="mono">')}</span> (${hs.every(h => S.inserts[h]) ? 'both in' : '<b class="bad">add the inserts</b>'}). The loop holds a bundle up to about 20 mm across.</p>${cl ? cl.map(x => `<p class="note"><b class="bad">Clash:</b> ${esc(x)}</p>`).join('') : ''}</div>`; }
  if (T.kind !== 'frame' && !T.dev){
    const cur = S.colors[T.key] || T.color;
    html += `<div class="sec"><h3>Color · TIA-598 fiber code</h3><div class="swatches">${FIBER.map((f, i) => `<button data-color="${f.key}" aria-pressed="${cur === f.key}" title="${i + 1} · ${f.name}" aria-label="${f.name}" style="background:${f.hex}"></button>`).join('')}</div>
      ${T.group === 'cm1000' ? '<p class="note">Applies to every CM1000 part of this kind.</p>' : ''}</div>`;
  }
  if (T.imp){
    const m = T.imp, auto = autoHU(m), isGear = m.role === 'gear';
    html += `<div class="sec"><h3>Fit</h3>
      <div class="row"><button class="btn primary small" data-act="orient">Check orientation…</button></div>
      ${isGear ? `<p class="note">Opens a front, side and top preview against the rack lines, with Auto-orient and turn buttons. The fine controls below change it in place.</p>
      <div class="row"><button class="btn small" data-act="rot" data-ax="0">Rotate X 90°</button><button class="btn small" data-act="rot" data-ax="1">Rotate Y 90°</button><button class="btn small" data-act="rot" data-ax="2">Rotate Z 90°</button></div>
      <div class="row3">
        <label class="field">Ear depth<input class="input mono" type="number" step="0.5" id="f-ear" value="${m.ear}"></label>
        <label class="field">Height<select class="select" id="f-hu"><option value="">Auto (${fmtHU(auto)})</option>${[.5,1,1.5,2,2.5,3,4,5].map(h => `<option value="${h}" ${m.hU === h ? 'selected' : ''}>${fmtHU(h)}</option>`).join('')}</select></label>
        <span></span>
        <label class="field">Nudge X<input class="input mono" type="number" step="0.5" id="f-nx" value="${m.nudge[0]}"></label>
        <label class="field">Nudge Y<input class="input mono" type="number" step="0.5" id="f-ny" value="${m.nudge[1]}"></label>
        <label class="field">Nudge Z<input class="input mono" type="number" step="0.5" id="f-nz" value="${m.nudge[2]}"></label>
      </div>` : `<p class="note">Positioned from its partner file, so it moves and rotates with ${esc(TYPES[T.parent] ? TYPES[T.parent].name : 'its partner')}.</p>`}
      <div class="row">${confirmDel === m.id ? `<button class="btn danger" data-act="delImp">Delete for good${isGear && childrenImports(m.id).length ? ' (and its attached parts)' : ''}</button><button class="btn" data-act="cancelDel">Keep</button>` : `<button class="btn danger" data-act="delImp">Delete import</button>`}</div>
    </div>`;
  }
  el.innerHTML = html;
}
const childrenImports = id => S.imports.filter(m => m.role === 'attach' && m.parent === id);

/* ================= UI: reference tab ================= */
function renderRef(){
  const s = S.settings, top = s.numbering === 'top';
  const lab = k => unitLabel(k);
  // front view of the FL and FR posts with their holes, labelled
  const H = RU > 6 ? 30 : 40, y0 = 26, units = [...Array(RU).keys()].reverse(), Ht = RU * H;
  const rows = units.map((k, i) => {
    const yTop = y0 + i * H;
    const holes = [0, 1, 2].map(j => { const cy = yTop + (1 - HOLE_Z[j] / U) * H; return `<circle class="hole${k === 0 && j === 1 ? ' hl' : ''}" cx="52" cy="${cy.toFixed(1)}" r="${H > 34 ? 3 : 2.4}"/><circle class="hole" cx="208" cy="${cy.toFixed(1)}" r="${H > 34 ? 3 : 2.4}"/>${k === 0 || k === RU - 1 ? `<text x="62" y="${(cy + 3).toFixed(1)}">${'abc'[j]}</text>` : ''}`; }).join('');
    return `<line class="rule" x1="28" x2="250" y1="${yTop}" y2="${yTop}"/><text class="k" x="22" y="${yTop + H / 2 + 3}" text-anchor="end">${lab(k)}</text>${holes}`;
  }).join('');
  // level boundaries, labelled from the stack
  let joint = '', zU = 0;
  S.levels.forEach((l, i) => {
    const n = levelU(l), yb = y0 + (RU - zU) * H, yt = y0 + (RU - zU - n) * H;
    if (i > 0) joint += `<line class="ext" x1="66" x2="196" y1="${yb}" y2="${yb}"/>`;
    joint += `<text x="130" y="${((yb + yt) / 2 + 3).toFixed(1)}" text-anchor="middle">${l.k === 'mod' ? '1U support ext.' : n + 'U posts'}</text>`;
    zU += n;
  });
  $('#tab-ref').innerHTML = `<h2>Reference</h2>
    <p class="note">Every position in this app uses the same names, so you can quote them back to me.</p>
    <svg class="refdiag" viewBox="0 0 260 ${y0 + Ht + 26}" role="img" aria-label="Front posts with rack units and hole letters">
      <rect class="post" x="44" y="${y0}" width="16" height="${Ht}" rx="1.5"/>
      <rect class="post" x="200" y="${y0}" width="16" height="${Ht}" rx="1.5"/>
      ${rows}<line class="rule" x1="28" x2="250" y1="${y0 + Ht}" y2="${y0 + Ht}"/>${joint}
      <text x="52" y="${y0 + Ht + 14}" text-anchor="middle" class="k">FL</text><text x="208" y="${y0 + Ht + 14}" text-anchor="middle" class="k">FR</text>
      <text x="130" y="${y0 + (RU - 1) * H + H / 2 + 3}" text-anchor="middle">FL-${lab(0)}b = teal hole</text>
    </svg>
    <dl class="kv">
      <dt>Rack units</dt><dd>${top ? `Numbered from the top, U1 to ${lab(0)}.` : `Numbered from the bottom (EIA), U1 to U${RU}.`} Each U is 44.45 mm. Half units read “upper ½” and “lower ½”. Adding or removing a level renumbers them.</dd>
      <dt>Posts</dt><dd>FL, FR, RL, RR: front or rear, then left or right as you face the front. Each column runs up through every level (posts and support extensions), and the hole names run straight up it.</dd>
      <dt>Holes</dt><dd>Three per U on each post: a (top), b (middle), c (bottom). <span class="mono">FL-${lab(0)}b</span> is the middle hole of ${lab(0)} on the front-left post.</dd>
      <dt>Coordinates</dt><dd>Millimetres. X across (0 = centreline, − = left), Y depth (0 = front face of the posts), Z height (0 = bottom of ${lab(0)}).</dd>
    </dl>
    <div class="sec"><h3>Frame</h3>
      <p class="note"><b style="color:var(--ink)">${RU}U</b> · ${esc(stackText())}. Build it in Frame mode: drop posts and support extensions onto the stack.</p>
      ${directJoints() ? `<p class="note">Posts stacked straight onto posts are held by joiner plates and extension side panels from the Extension Side Panels &amp; Post Joiner file, which isn’t loaded, so those joints show the plain side panels.</p>` : ''}
    </div>
    <div class="sec"><h3>View</h3>
      <label class="check"><input type="checkbox" id="optLabels" ${s.labels ? 'checked' : ''}> Show unit labels, post names and the U grid</label>
      <div class="field">Side panels<div class="seg" role="group" aria-label="Side panels" id="optSides">${[['clear','See-through'],['solid','Solid'],['hidden','Hidden']].map(([v, l]) => `<button data-v="${v}" aria-pressed="${s.sides === v}">${l}</button>`).join('')}</div></div>
      <div class="field">Unit numbering<div class="seg" role="group" aria-label="Unit numbering" id="optNum"><button data-v="top" aria-pressed="${top}">From the top</button><button data-v="bottom" aria-pressed="${!top}">From the bottom</button></div></div>
      <div class="field">Frame filament<div class="swatches" id="optFrame">${FRAME_COLORS.map(([h, n]) => `<button data-frame="${h}" aria-pressed="${s.frame === h}" title="${n} PETG" aria-label="${n}" style="background:${h}"></button>`).join('')}</div></div>
    </div>`;
}
/* ================= UI: ask Claude ================= */
let spots = [], spotsRef = null, asking = null, sampleImages = false;
function spotById(id){ return spots.find(s => s.id === id); }
function renderAsk(){
  const el = $('#tab-ask'), sp = activeSpot && spotById(activeSpot);
  const list = spots.length ? `<div class="spots">${spots.map(s => `<button class="spot${s.id === activeSpot ? ' is-on' : ''}" data-spot="${s.id}"><span class="n">${s.n}</span><span class="t">${esc(s.title || s.pin.code)}<small>${esc(s.pin.code)}</small></span><span class="mono" style="font-size:11px;color:var(--muted)">${s.messages.length ? Math.ceil(s.messages.length / 2) + ' Q' : 'new'}</span></button>`).join('')}</div>` : '';
  let body;
  if (!sp){
    body = `<p class="empty">Switch to <b>Point &amp; ask</b>, then click any spot on the build. You get a reference for that exact point and can ask Claude about it, with a snapshot of the view.</p>
      <div class="row"><button class="btn primary" data-act="startPoint">Start pointing</button></div>`;
  } else {
    const pin = sp.pin;
    const msgs = sp.messages.map(m => `<div class="msg ${m.role}">${esc(m.content)}</div>`).join('');
    const live = asking && asking.spot === sp.id ? `<div class="msg assistant${asking.text ? '' : ' pending'}" id="liveMsg">${esc(asking.text || 'Thinking…')}</div>` : '';
    const err = sp.error ? `<div class="msg assistant err">${esc(sp.error)}</div>` : '';
    const composer = SAMPLE ? `<div class="composer">
        <label class="field" for="askInput">Your question</label>
        <textarea class="textarea" id="askInput" placeholder="e.g. Which screw goes here, and how deep is the insert?">${esc(sp.draft || '')}</textarea>
        <div class="row">${sampleImages ? `<label class="check"><input type="checkbox" id="askSnap" ${sp.noSnap ? '' : 'checked'}> Send a snapshot of the view</label>` : '<span></span>'}
          <button class="btn primary" data-act="send" ${asking ? 'disabled' : ''}>${asking && asking.spot === sp.id ? 'Asking…' : 'Ask Claude'}</button></div>
      </div>` : `<p class="note">Asking Claude isn't available in this view. Copy the reference and paste it into your chat.</p>`;
    body = `<div class="insp-head"><span class="spot" style="border:0;padding:0;background:transparent;grid-template-columns:22px"><span class="n">${sp.n}</span></span><h3>${esc(sp.title || 'Spot ' + sp.n)}</h3></div>
      <div class="refbox"><code>${esc(pin.code)}</code><button class="btn small" data-act="copySpot">Copy</button></div>
      <dl class="kv"><dt>On</dt><dd>${esc(pin.part)}</dd><dt>Where</dt><dd>${esc(pin.unit)} · ${esc(pin.side)} · ${esc(pin.depth)}</dd><dt>Point</dt><dd class="mono">${esc(pin.xyz)}</dd><dt>Surface</dt><dd>faces ${esc(pin.facing || '—')}</dd></dl>
      <div class="chat">${msgs}${live}${err}</div>${composer}
      <div class="row">${confirmDel === 'spot:' + sp.id ? `<button class="btn danger small" data-act="delSpot">Delete this spot</button><button class="btn small" data-act="cancelDel">Keep</button>` : `<button class="btn small danger" data-act="delSpot">Delete spot</button>`}</div>`;
  }
  el.innerHTML = `<h2>Ask Claude</h2>${list}${body}`;
}
function buildContext(sp){
  const pin = sp.pin, s = S.settings;
  const on = INST.filter(i => placed(i.id)).map(i => `${instLabel(i.id)} — ${instWhere(i.id)}`);
  const off = INST.filter(i => !placed(i.id)).map(i => TYPES[i.type].name);
  return [
    'You are helping someone assemble a Lab Rax 10-inch 3D-printed mini rack (mklements design, printed in PETG, M6 heat-set inserts and M6×10 button-head screws) in a 3D assembler app. Answer briefly and practically, in plain sentences.',
    'Reference system used by the app:',
    `- Coordinates in mm: X across the rack (0 = centreline, negative = left when facing the front), Y depth (0 = front face of the posts, positive toward the rear), Z height (0 = bottom of the lowest rack unit). The frame is ${DEPTH} mm deep.`,
    `- The frame is ${RU}U tall, stacked from the bottom: ${stackText()}. (A 1U support extension is a full-depth side brace with its own 1U of rack holes, bolted into the post ends with 4 M6 screws per side.)`,
    s.numbering === 'top' ? `- Rack units are numbered from the top: ${unitLabel(RU - 1)} is the top unit and ${unitLabel(0)} the bottom one. 1U = 44.45 mm.` : `- Rack units are numbered from the bottom, U1 to U${RU}. 1U = 44.45 mm.`,
    '- Posts are FL, FR, RL, RR (front/rear, left/right). Each post has three holes per U: a (top), b (middle), c (bottom). Example: FL-U8b is the middle hole of U8 on the front-left post.',
    'Installed parts: ' + (on.length ? on.join('; ') : 'none') + '.',
    `Heat-set inserts installed: ${Object.keys(S.inserts).length ? Object.keys(S.inserts).map(holeName).join(', ') : 'none'}. Still needed: ${insertSummary().missing.map(holeName).join(', ') || 'none'}.`,
    'Cables: ' + ((S.cables || []).map(c => { const r = ROUTES.get(c.id); return `${cableName(c)} (${r ? CABLE[r.kind].name + ', ' + Math.round(r.len) + ' mm' : 'not routed'})`; }).join('; ') || 'none') + '.',
    'The rack is wall mounted. Data cables run up the rear-left spine, power up the rear-right.',
    off.length ? 'Still in the tray: ' + off.join(', ') + '.' : 'Nothing left in the tray.',
    `The person pointed at ${pin.code} on the ${pin.part} (${pin.unit}, ${pin.side}, ${pin.depth}), at ${pin.xyz}; the surface there faces ${pin.facing || 'an unknown direction'}.`,
    'If an image is attached, it is the current view with that spot marked by a teal pin.'
  ].join('\n');
}
async function snapshot(sp){
  if (!gl) return null;
  const prevActive = activeSpot; activeSpot = sp.id; draw();
  const src = canvas, w = Math.min(1280, src.width), h = Math.round(src.height * w / src.width);
  const c2 = document.createElement('canvas'); c2.width = w; c2.height = h; c2.getContext('2d').drawImage(src, 0, 0, w, h);
  activeSpot = prevActive;
  return await new Promise(res => c2.toBlob(b => res(b), 'image/jpeg', 0.86));
}
async function sendQuestion(){
  const sp = spotById(activeSpot), ta = $('#askInput'); if (!sp || !ta || asking || !SAMPLE) return;
  const q = ta.value.trim(); if (!q){ ta.focus(); return; }
  const wantSnap = sampleImages && $('#askSnap') && $('#askSnap').checked;
  sp.draft = ''; sp.error = null; sp.messages.push({role:'user', content:q});
  if (!sp.title) sp.title = q.length > 54 ? q.slice(0, 52) + '…' : q;
  asking = {spot:sp.id, text:''}; renderAsk(); saveSpot(sp);
  const input = sp.messages.map((m, i) => i === 0 ? {role:'user', content:buildContext(sp) + '\n\nQuestion: ' + m.content} : m);
  try {
    const opts = {cache:false, onText:({text}) => { asking.text = text; const live = $('#liveMsg'); if (live){ live.textContent = text; live.classList.remove('pending'); } }};
    if (wantSnap){ const b = await snapshot(sp); if (b) opts.images = [b]; }
    const res = await SAMPLE(input, opts);
    sp.messages.push({role:'assistant', content:res.text + (res.truncated ? '\n\n(The answer was cut short.)' : '')});
  } catch (e) {
    const code = e && e.code;
    sp.error = code === 'not_granted' ? 'Claude was not allowed for this page. You can allow it from the page’s permissions.' : code === 'rate_limited' ? 'Too many questions in a row. Wait a minute and ask again.' : 'Claude could not answer just now. ' + ((e && e.message) || '');
    if (e && e.text) sp.messages.push({role:'assistant', content:e.text});
    else sp.messages.pop();
  }
  asking = null; saveSpot(sp); renderAsk(); renderTabs();
}
function createSpot(hit){
  const r = refFor(hit.p, hit.n), n = spots.reduce((m, s) => Math.max(m, s.n), 0) + 1;
  const sp = {id:uid(), n, title:'', createdAt:Date.now(), messages:[],
    pin:{p:hit.p.map(v => +v.toFixed(2)), n:hit.n.map(v => +v.toFixed(3)), inst:hit.inst, part:instLabel(hit.inst), code:r.code, unit:r.unit, side:r.side, depth:r.depth, xyz:r.xyz, facing:r.facing}};
  spots.push(sp); activeSpot = sp.id; tab = 'ask'; saveSpot(sp); renderTabs(); renderAsk(); requestRender();
  setTimeout(() => { const ta = $('#askInput'); if (ta) ta.focus({preventScroll:true}); }, 30);
  toast(`Spot ${n}: ${r.code}`);
}
function saveSpot(sp){
  const clean = {id:sp.id, n:sp.n, title:sp.title || '', createdAt:sp.createdAt, pin:sp.pin, messages:sp.messages.slice(-40)};
  if (spotsRef) spotsRef.doc(sp.id).set(clean).catch(() => toast('Couldn’t save this spot'));
  else saveSpotsLocal();
}
function saveSpotsLocal(){ try { localStorage.setItem(LS_SPOTS, JSON.stringify(spots.map(s => ({id:s.id, n:s.n, title:s.title, createdAt:s.createdAt, pin:s.pin, messages:s.messages})))); } catch (e) {} }
function sanitizeSpot(d){
  if (!d || typeof d !== 'object' || !d.pin || !Array.isArray(d.pin.p) || !Array.isArray(d.pin.n)) return null;
  const str = (v, n) => String(v ?? '').slice(0, n);
  return {id:str(d.id, 24), n:Number(d.n) || 1, title:str(d.title, 80), createdAt:Number(d.createdAt) || 0,
    pin:{p:d.pin.p.slice(0, 3).map(Number), n:d.pin.n.slice(0, 3).map(Number), inst:str(d.pin.inst, 40), part:str(d.pin.part, 80), code:str(d.pin.code, 80), unit:str(d.pin.unit, 60), side:str(d.pin.side, 20), depth:str(d.pin.depth, 40), xyz:str(d.pin.xyz, 80), facing:str(d.pin.facing, 20)},
    messages:(Array.isArray(d.messages) ? d.messages : []).filter(m => m && (m.role === 'user' || m.role === 'assistant')).map(m => ({role:m.role, content:str(m.content, 8000)}))};
}
(function loadSpotsLocal(){ try { spots = (JSON.parse(localStorage.getItem(LS_SPOTS) || '[]') || []).map(sanitizeSpot).filter(Boolean); } catch (e) { spots = []; } })();

/* ================= import ================= */
async function inflateRaw(u8){ const ds = new DecompressionStream('deflate-raw'); const out = new Blob([u8]).stream().pipeThrough(ds); return new Uint8Array(await new Response(out).arrayBuffer()); }
function readZip(buf){
  const dv = new DataView(buf), u8 = new Uint8Array(buf); let e = buf.byteLength - 22;
  while (e >= 0 && dv.getUint32(e, true) !== 0x06054b50) e--;
  if (e < 0) throw new Error('This 3MF is not a valid zip file');
  const n = dv.getUint16(e + 10, true); let p = dv.getUint32(e + 16, true);
  const files = new Map(), td = new TextDecoder();
  for (let i = 0; i < n; i++){
    if (dv.getUint32(p, true) !== 0x02014b50) break;
    const method = dv.getUint16(p + 10, true), csize = dv.getUint32(p + 20, true), nl = dv.getUint16(p + 28, true), xl = dv.getUint16(p + 30, true), cl = dv.getUint16(p + 32, true), lho = dv.getUint32(p + 42, true);
    files.set(td.decode(u8.subarray(p + 46, p + 46 + nl)).replace(/^\//, ''), {method, csize, lho}); p += 46 + nl + xl + cl;
  }
  return {
    has: name => files.has(name.replace(/^\//, '')),
    async get(name){ const f = files.get(name.replace(/^\//, '')); if (!f) return null; const nl = dv.getUint16(f.lho + 26, true), xl = dv.getUint16(f.lho + 28, true), s = f.lho + 30 + nl + xl, data = u8.subarray(s, s + f.csize); return f.method === 0 ? data : await inflateRaw(data); },
    async text(name){ const b = await this.get(name); return b ? new TextDecoder().decode(b) : null; }
  };
}
function weld(tri){ // tri: Float32Array of xyz per corner
  const map = new Map(), pos = [], idx = new Uint32Array(tri.length / 3);
  for (let i = 0; i < tri.length; i += 3){
    const key = Math.round(tri[i] * 1e4) + ',' + Math.round(tri[i+1] * 1e4) + ',' + Math.round(tri[i+2] * 1e4);
    let v = map.get(key); if (v === undefined){ v = pos.length / 3; pos.push(tri[i], tri[i+1], tri[i+2]); map.set(key, v); } idx[i / 3] = v;
  }
  return {pos:new Float32Array(pos), idx};
}
function parseSTL(buf, name){
  const dv = new DataView(buf); let tri;
  const bin = buf.byteLength >= 84 && 84 + dv.getUint32(80, true) * 50 === buf.byteLength;
  if (bin){
    const n = dv.getUint32(80, true); tri = new Float32Array(n * 9);
    for (let t = 0; t < n; t++) for (let k = 0; k < 9; k++) tri[t*9+k] = dv.getFloat32(84 + t * 50 + 12 + k * 4, true);
  } else {
    const txt = new TextDecoder().decode(new Uint8Array(buf)); const vals = []; const re = /vertex\s+([-+\d.eE]+)\s+([-+\d.eE]+)\s+([-+\d.eE]+)/g; let m;
    while ((m = re.exec(txt))) vals.push(+m[1], +m[2], +m[3]);
    if (!vals.length) throw new Error(name + ' has no triangles I can read');
    tri = new Float32Array(vals);
  }
  const w = weld(tri);
  return [{name:name.replace(/\.stl$/i, ''), file:name, parts:[{name, sub:'normal', ...w}]}];
}
const NS_P = 'http://schemas.microsoft.com/3dmanufacturing/production/2015/06';
async function parse3MF(buf, fname){
  const zip = readZip(buf);
  let root = '3D/3dmodel.model';
  const rels = await zip.text('_rels/.rels');
  if (rels){ const m = rels.match(/Target="([^"]+\.model)"/i); if (m) root = m[1].replace(/^\//, ''); }
  const xmlCache = new Map();
  const xmlOf = async path => { path = path.replace(/^\//, ''); if (!xmlCache.has(path)){ const t = await zip.text(path); if (!t) throw new Error('Missing ' + path + ' in ' + fname); xmlCache.set(path, new DOMParser().parseFromString(t, 'application/xml')); } return xmlCache.get(path); };
  const cfg = await zip.text('Metadata/model_settings.config');
  const names = {}, parts = {};
  if (cfg){
    for (const m of cfg.matchAll(/<object id="(\d+)">([\s\S]*?)<\/object>/g)){
      const nm = m[2].match(/key="name" value="([^"]*)"/); names[m[1]] = nm ? nm[1] : null;
      for (const p of m[2].matchAll(/<part id="(\d+)" subtype="(\w+)">([\s\S]*?)<\/part>/g)){ const pn = p[3].match(/key="name" value="([^"]*)"/); parts[m[1] + '|' + p[1]] = {name:pn ? pn[1] : p[1], sub:p[2]}; }
    }
  }
  const mainDoc = await xmlOf(root);
  const findObj = (doc, id) => { for (const o of doc.getElementsByTagName('object')) if (o.getAttribute('id') === id) return o; return null; };
  const mat = t => { const a = (t || '1 0 0 0 1 0 0 0 1 0 0 0').trim().split(/\s+/).map(Number); return a.length === 12 ? a : [1,0,0,0,1,0,0,0,1,0,0,0]; };
  const cmat = (A, B) => { // apply B then A (3MF row-vector matrices)
    const r = new Array(12);
    for (let c = 0; c < 3; c++){ for (let rr = 0; rr < 3; rr++) r[rr*3+c] = B[rr*3]*A[c] + B[rr*3+1]*A[3+c] + B[rr*3+2]*A[6+c]; r[9+c] = B[9]*A[c] + B[10]*A[3+c] + B[11]*A[6+c] + A[9+c]; }
    return r;
  };
  async function collect(doc, path, objEl, M, topId, out, depth){
    if (depth > 6) return;
    const mesh = objEl.getElementsByTagName('mesh')[0];
    if (mesh){
      const vs = mesh.getElementsByTagName('vertex'), ts = mesh.getElementsByTagName('triangle');
      const pos = new Float32Array(vs.length * 3);
      for (let i = 0; i < vs.length; i++){ const v = vs[i], x = +v.getAttribute('x'), y = +v.getAttribute('y'), z = +v.getAttribute('z');
        pos[i*3] = M[0]*x + M[3]*y + M[6]*z + M[9]; pos[i*3+1] = M[1]*x + M[4]*y + M[7]*z + M[10]; pos[i*3+2] = M[2]*x + M[5]*y + M[8]*z + M[11]; }
      const idx = new Uint32Array(ts.length * 3);
      for (let i = 0; i < ts.length; i++){ idx[i*3] = +ts[i].getAttribute('v1'); idx[i*3+1] = +ts[i].getAttribute('v2'); idx[i*3+2] = +ts[i].getAttribute('v3'); }
      const info = parts[topId + '|' + objEl.getAttribute('id')] || {name:objEl.getAttribute('name') || 'part', sub:'normal_part'};
      out.push({name:info.name, sub:info.sub === 'negative_part' ? 'negative' : info.sub === 'normal_part' ? 'normal' : 'skip', pos, idx});
      return;
    }
    const comps = objEl.getElementsByTagName('component');
    for (const c of comps){
      const p = c.getAttributeNS(NS_P, 'path') || c.getAttribute('p:path') || path;
      const d2 = p === path ? doc : await xmlOf(p);
      const o2 = findObj(d2, c.getAttribute('objectid')); if (!o2) continue;
      await collect(d2, p, o2, cmat(M, mat(c.getAttribute('transform'))), topId, out, depth + 1);
    }
  }
  const items = [...mainDoc.getElementsByTagName('item')].map(it => it.getAttribute('objectid'));
  const ids = items.length ? items : [...mainDoc.getElementsByTagName('object')].map(o => o.getAttribute('id'));
  const objs = [];
  for (const id of ids){
    const o = findObj(mainDoc, id); if (!o) continue;
    const out = []; await collect(mainDoc, root, o, mat(null), id, out, 0);
    const keep = out.filter(p => p.sub !== 'skip' && p.idx.length);
    if (keep.some(p => p.sub === 'normal')) objs.push({name:names[id] || o.getAttribute('name') || fname.replace(/\.3mf$/i, '') + ' ' + id, file:fname, parts:keep});
  }
  if (!objs.length) throw new Error(fname + ' has no printable objects');
  return objs;
}
let csgWorker = null, csgSeq = 0; const csgWait = new Map();
function runCSG(bodies, cutters){
  return new Promise((res, rej) => {
    try {
      if (!csgWorker){ csgWorker = new Worker(URL.createObjectURL(new Blob([document.getElementById('csg-src').textContent], {type:'text/javascript'})));
        csgWorker.onmessage = e => { const w = csgWait.get(e.data.id); if (!w) return; csgWait.delete(e.data.id); e.data.error ? w.rej(new Error(e.data.error)) : w.res(e.data.out); };
        csgWorker.onerror = e => { for (const w of csgWait.values()) w.rej(new Error('cut-out worker failed')); csgWait.clear(); csgWorker = null; }; }
      const id = ++csgSeq; csgWait.set(id, {res, rej}); csgWorker.postMessage({id, bodies, cutters});
    } catch (e) { rej(e); }
  });
}
async function finishObject(obj){
  const bodies = obj.parts.filter(p => p.sub === 'normal'), cutters = obj.parts.filter(p => p.sub === 'negative');
  let results = bodies;
  if (cutters.length){
    try { results = await runCSG(bodies.map(b => ({pos:b.pos, idx:b.idx})), cutters.map(c => ({pos:c.pos, idx:c.idx}))); obj.cut = cutters.length; }
    catch (e) { obj.cutFailed = true; }
  }
  let nv = 0, ni = 0; for (const r of results){ nv += r.pos.length; ni += r.idx.length; }
  const pos = new Float32Array(nv), idx = new Uint32Array(ni); let ov = 0, oi = 0;
  for (const r of results){ pos.set(r.pos, ov); for (let i = 0; i < r.idx.length; i++) idx[oi + i] = r.idx[i] + ov / 3; ov += r.pos.length; oi += r.idx.length; }
  const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity];
  for (let i = 0; i < pos.length; i += 3) for (let k = 0; k < 3; k++){ lo[k] = Math.min(lo[k], pos[i+k]); hi[k] = Math.max(hi[k], pos[i+k]); }
  return {name:obj.name, file:obj.file, pos, idx, lo, hi, tris:idx.length / 3, cut:obj.cut || 0, cutFailed:!!obj.cutFailed};
}
let pendingImport = null;
async function importFiles(files){
  if (!files.length) return;
  busy('Reading files…');
  const objs = [], errors = [];
  for (const f of files){
    try { const buf = await f.arrayBuffer(); const list = /\.3mf$/i.test(f.name) ? await parse3MF(buf, f.name) : parseSTL(buf, f.name); for (const o of list){ busy('Applying cut-outs…'); objs.push(await finishObject(o)); } }
    catch (e) { errors.push((e && e.message) || ('Could not read ' + f.name)); }
  }
  busy(null);
  if (!objs.length){ toast(errors[0] || 'Nothing to import'); return; }
  // Default roles: full-width pieces (a 10" panel is 254 mm) are rack gear. A narrower piece that sits against
  // one of them in the same design space attaches to it; anything else stands alone.
  const width = o => o.hi[0] - o.lo[0];
  const near = (a, b) => [0,1,2].every(k => a.lo[k] <= b.hi[k] + 10 && a.hi[k] >= b.lo[k] - 10);
  let gears = objs.map((o, i) => width(o) >= 200 ? i : -1).filter(i => i >= 0);
  if (!gears.length) gears = [objs.reduce((b, o, i) => width(o) > width(objs[b]) ? i : b, 0)];
  objs.forEach((o, i) => {
    if (gears.includes(i)){ o.role = 'gear'; return; }
    const g = gears.find(j => near(o, objs[j]) && (objs[j].file === o.file || objs.filter(x => x.file === o.file).length <= 2));
    o.role = g != null ? 'attach:' + g : 'gear';
  });
  objs.forEach(o => { o.ear = 3; o.hU = null; o.nudge = [0,0,0]; o.rot = o.role === 'gear' ? autoOrient(o) : [0,0,0]; o.autoDone = o.role === 'gear'; });
  pendingImport = {objs, errors};
  openImportModal();
}
/* ================= import preview: check and fix orientation before a part goes on the rack ================= */
/* where an imported gear part sits, in rack coordinates, before it is moved to a U: centred across the rack,
   its front face (the ear) just in front of the posts, its bottom on the bottom of the unit */
function impPose(m){
  const R = impRotation(m), b = rotBox(R, m.lo, m.hi);
  return pose(R, [-(b.lo[0] + b.hi[0]) / 2 + m.nudge[0], -(b.lo[1] + m.ear) + m.nudge[1], -b.lo[2] + m.nudge[2]]);
}
/* per-triangle area vectors and centroids, sampled for very large meshes */
function triStats(pos, idx){
  const n = idx.length / 3, step = Math.max(1, Math.ceil(n / 120000)), N = [], C = [], X = [];
  for (let t = 0; t < n; t += step){
    const a = idx[t*3]*3, b = idx[t*3+1]*3, c = idx[t*3+2]*3;
    const e1 = [pos[b]-pos[a], pos[b+1]-pos[a+1], pos[b+2]-pos[a+2]], e2 = [pos[c]-pos[a], pos[c+1]-pos[a+1], pos[c+2]-pos[a+2]];
    const cr = crs(e1, e2); N.push(cr[0] * step / 2, cr[1] * step / 2, cr[2] * step / 2);
    C.push((pos[a]+pos[b]+pos[c]) / 3, (pos[a+1]+pos[b+1]+pos[c+1]) / 3, (pos[a+2]+pos[b+2]+pos[c+2]) / 3);
    for (let k = 0; k < 3; k++) X.push(Math.min(pos[a+k], pos[b+k], pos[c+k]), Math.max(pos[a+k], pos[b+k], pos[c+k]));
  }
  return {N, C, X};
}
/* Guess how the part sits in the rack. A bracket is usually exported the way it prints (faceplate flat on the bed),
   so look for the largest flat face on the outside of the part: that becomes the front. The widest dimension runs
   across the rack, and the larger flat face at the bottom becomes the floor. */
function autoOrient(o){
  const st = o._st || (o._st = triStats(o.pos, o.idx)), seen = new Set();
  const ext = [0,1,2].map(k => o.hi[k] - o.lo[k]), maxExt = Math.max(...ext);
  let best = null;
  for (let a = 0; a < 4; a++) for (let b = 0; b < 4; b++) for (let c = 0; c < 4; c++){
    const rot = [a, b, c], R = impRotation({rot}), key = R.join(','); if (seen.has(key)) continue; seen.add(key);
    const bb = rotBox(R, o.lo, o.hi), W = bb.hi[0] - bb.lo[0], H = bb.hi[2] - bb.lo[2];
    let front = 0, bottom = 0, fx0 = Infinity, fx1 = -Infinity;
    const ax = [0, 1, 2].map(r => [0, 1, 2].reduce((b, k) => Math.abs(R[r * 3 + k]) > Math.abs(R[r * 3 + b]) ? k : b, 0)); // world x comes from object axis ax[0]
    for (let i = 0, t = 0; i < st.N.length; i += 3, t++){
      const n = mv(R, [st.N[i], st.N[i+1], st.N[i+2]]), A = Math.hypot(n[0], n[1], n[2]); if (A < 1e-9) continue;
      const cc = mv(R, [st.C[i], st.C[i+1], st.C[i+2]]);
      if (n[1] < -0.95 * A && cc[1] < bb.lo[1] + 2.5){ front += A; fx0 = Math.min(fx0, st.X[t * 6 + ax[0] * 2]); fx1 = Math.max(fx1, st.X[t * 6 + ax[0] * 2 + 1]); }
      if (n[2] < -0.95 * A && cc[2] < bb.lo[2] + 2.5) bottom += A;
    }
    // the faceplate runs the full width of the part (its ears reach both sides); a tray floor usually doesn't
    const fullFront = fx1 - fx0 >= W - 1.5;
    // trays and shelves are deeper than they are tall; a plain faceplate is thin, and a 1U part can go either way
    const D = bb.hi[1] - bb.lo[1], rackish = H <= D + 0.5 || H <= U + 1 || D <= 10;
    const score = (maxExt >= 200 && W >= maxExt - 0.5 ? 1e12 : 0) + (fullFront ? 1e11 : 0) + (rackish ? 5e10 : 0) + (W >= H ? 1e10 : 0) + 2 * front + bottom;
    if (!best || score > best.score + 1e-6) best = {rot, score};
  }
  return best.rot;
}
const ROT_NAMES = ['X','Y','Z'];

/* ---- drawing: three flat views with the rack's own lines behind the part ---- */
function previewMeshes(entry){ // [{pos, idx, main}]
  const out = [{pos:entry.pos, idx:entry.idx, main:true}];
  for (const k of entry.kids || []) out.push({pos:k.pos, idx:k.idx, main:false});
  return out;
}
function drawImpPreview(cv, m, meshes){
  const dpr = Math.min(2, window.devicePixelRatio || 1), cssW = Math.max(260, cv.clientWidth || 560);
  const P = impPose(m), R = P.R;
  // transformed bounds of everything drawn
  const lo = [Infinity, Infinity, Infinity], hi = [-Infinity, -Infinity, -Infinity];
  const pts = meshes.map(ms => { const p = new Float32Array(ms.pos.length); for (let i = 0; i < ms.pos.length; i += 3){ const v = papply(P, [ms.pos[i], ms.pos[i+1], ms.pos[i+2]]); p[i] = v[0]; p[i+1] = v[1]; p[i+2] = v[2]; for (let k = 0; k < 3; k++){ if (v[k] < lo[k]) lo[k] = v[k]; if (v[k] > hi[k]) hi[k] = v[k]; } } return p; });
  const hU = m.hU || clamp(Math.ceil((hi[2] - lo[2]) / (U / 2) - 0.04) / 2, 0.5, 10);
  // view windows in mm: front (x, z), side (y, z), top (x, y)
  const xr = [Math.min(lo[0], -140) - 6, Math.max(hi[0], 140) + 6], yr = [Math.min(lo[1], -12) - 6, Math.max(hi[1], DEPTH) + 8], zr = [Math.min(lo[2], 0) - 8, Math.max(hi[2], hU * U) + 10];
  const gap = 28, pad = 14, narrow = cssW < 560;
  const s = narrow ? Math.min((cssW - 2 * pad) / Math.max(xr[1] - xr[0], yr[1] - yr[0]), 2.2) : Math.min((cssW - 2 * pad - gap) / ((xr[1] - xr[0]) + (yr[1] - yr[0])), 2.2);
  const fW = (xr[1] - xr[0]) * s, sW = (yr[1] - yr[0]) * s, zH = (zr[1] - zr[0]) * s, tH = (yr[1] - yr[0]) * s;
  const cssH = Math.round(narrow ? pad + 3 * 16 + 2 * zH + 2 * gap + tH + pad : pad + 16 + zH + gap + 16 + tH + pad);
  cv.width = Math.round(cssW * dpr); cv.height = Math.round(cssH * dpr); cv.style.height = cssH + 'px';
  const g = cv.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, cssW, cssH);
  const cs = getComputedStyle(document.documentElement), col = n => cs.getPropertyValue(n).trim() || '#888';
  const ink = col('--ink'), muted = col('--muted'), acc = col('--accent'), line = col('--line'), warn = col('--warn');
  const F = {ox:pad, oy:pad + 16, w:fW, h:zH};
  const Sd = narrow ? {ox:pad, oy:F.oy + zH + gap, w:sW, h:zH} : {ox:pad + fW + gap, oy:pad + 16, w:sW, h:zH};
  const Tp = narrow ? {ox:pad, oy:Sd.oy + zH + gap, w:fW, h:tH} : {ox:pad, oy:pad + 16 + zH + gap + 16, w:fW, h:tH};
  // map functions: world -> screen for each view; depth value: larger = nearer the viewer
  const views = [
    {box:F, title:'Front — as you face the rack', sx:v => F.ox + (v[0] - xr[0]) * s, sy:v => F.oy + (zr[1] - v[2]) * s, dep:v => -v[1], dir:[0,-1,0]},
    {box:Sd, title:'Side — front on the left', sx:v => Sd.ox + (v[1] - yr[0]) * s, sy:v => Sd.oy + (zr[1] - v[2]) * s, dep:v => v[0], dir:[1,0,0]},
    {box:Tp, title:'Top — front at the bottom', sx:v => Tp.ox + (v[0] - xr[0]) * s, sy:v => Tp.oy + (yr[1] - v[1]) * s, dep:v => v[2], dir:[0,0,1]}];
  g.font = '600 11px ' + (col('--f-mono') || 'monospace'); g.textBaseline = 'alphabetic';
  for (const V of views){
    const b = V.box;
    g.fillStyle = muted; g.fillText(V.title, b.ox, b.oy - 6);
    g.save(); g.beginPath(); g.rect(b.ox, b.oy, b.w, b.h); g.clip();
    g.strokeStyle = line; g.lineWidth = 1; g.strokeRect(b.ox + .5, b.oy + .5, b.w - 1, b.h - 1);
    // rack reference lines
    g.setLineDash([4, 3]); g.strokeStyle = acc; g.globalAlpha = .55;
    const L = (a, c) => { g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(c[0], c[1]); g.stroke(); };
    if (V.box === F || V.box === Sd){
      for (let k = 0; k <= Math.ceil(hU); k++){ const z = k * U; const y = V.sy([0, 0, z]); L([b.ox, y], [b.ox + b.w, y]); }
    }
    if (V.box === F || V.box === Tp){ for (const x of [-HOLE_X, HOLE_X]){ const X = V.sx([x, 0, 0]); L([X, b.oy], [X, b.oy + b.h]); } }
    if (V.box === Sd || V.box === Tp){ for (const y of [0, DEPTH]){ const p = V.box === Sd ? V.sx([0, y, 0]) : V.sy([0, y, 0]); V.box === Sd ? L([p, b.oy], [p, b.oy + b.h]) : L([b.ox, p], [b.ox + b.w, p]); } }
    g.setLineDash([]); g.globalAlpha = 1;
    // the part: painter's algorithm, flat shaded
    const tris = [];
    meshes.forEach((ms, mi) => {
      const p = pts[mi], I = ms.idx, n = I.length / 3, step = Math.max(1, Math.ceil(n / 40000));
      for (let t = 0; t < n; t += step){
        const a = I[t*3]*3, bb = I[t*3+1]*3, c = I[t*3+2]*3;
        const A = [p[a], p[a+1], p[a+2]], B = [p[bb], p[bb+1], p[bb+2]], C = [p[c], p[c+1], p[c+2]];
        const nn = nrm(crs(subv(B, A), subv(C, A))), lit = Math.abs(dot(nn, V.dir));
        tris.push({A, B, C, d:(V.dep(A) + V.dep(B) + V.dep(C)) / 3, l:lit, main:ms.main});
      }
    });
    tris.sort((u, v) => u.d - v.d);
    const base = [[70, 120, 170], [222, 120, 40]];
    for (const t of tris){
      const c = base[t.main ? 0 : 1], k = 0.38 + 0.62 * t.l;
      g.fillStyle = `rgb(${c[0] * k | 0},${c[1] * k | 0},${c[2] * k | 0})`; g.strokeStyle = g.fillStyle; g.lineWidth = .4;
      g.beginPath(); g.moveTo(V.sx(t.A), V.sy(t.A)); g.lineTo(V.sx(t.B), V.sy(t.B)); g.lineTo(V.sx(t.C), V.sy(t.C)); g.closePath(); g.fill(); g.stroke();
    }
    g.restore();
  }
  // labels on the reference lines
  g.fillStyle = acc; g.font = '600 10px ' + (col('--f-mono') || 'monospace');
  g.fillText('post screw holes', views[0].sx([HOLE_X, 0, 0]) - 92, F.oy + F.h - 4);
  for (let k = 1; k <= Math.ceil(hU); k++) g.fillText(k + 'U', F.ox + 3, views[0].sy([0, 0, k * U]) + 11);
  g.fillText('post front', views[1].sx([0, 0, 0]) + 3, Sd.oy + 11); g.fillText('rear posts', views[1].sx([0, DEPTH, 0]) - 58, Sd.oy + 11);
  // fit summary
  const W = hi[0] - lo[0], D = hi[1] - lo[1], H = hi[2] - lo[2], notes = [];
  if (W > 2 * PX + 20) notes.push(['bad', `${W.toFixed(0)} mm wide — wider than the rack`]);
  else notes.push(['ok', `${W.toFixed(0)} mm wide${W >= 240 ? ' — full 10″ width' : ''}`]);
  notes.push(['ok', `${H.toFixed(1)} mm tall → ${fmtHU(hU)}`]);
  notes.push([D > DEPTH + m.ear + 5 ? 'bad' : 'ok', `${D.toFixed(0)} mm deep${D > DEPTH + m.ear + 5 ? ' — sticks out past the rear posts' : ''}`]);
  return notes;
}

/* ---- the modal ---- */
function impRowHTML(o, i, objs, edit){
  const isGear = o.role === 'gear';
  return `<div class="imp-row" data-i="${i}">
    <label class="field">Name<input class="input" id="imp-name-${i}" maxlength="60" value="${esc(o.name)}"></label>
    ${edit ? '<span></span>' : `<label class="field">Role<select class="select imp-role" id="imp-role-${i}">
      <option value="gear" ${isGear ? 'selected' : ''}>Rack gear: snaps to a U</option>
      ${objs.map((p, j) => j === i ? '' : `<option value="attach:${j}" ${o.role === 'attach:' + j ? 'selected' : ''}>Attaches to ${esc(p.name)}</option>`).join('')}
    </select></label>`}
    <div class="meta">${esc(o.file)} · ${o.tris.toLocaleString()} triangles · ${(o.hi[0]-o.lo[0]).toFixed(1)} × ${(o.hi[1]-o.lo[1]).toFixed(1)} × ${(o.hi[2]-o.lo[2]).toFixed(1)} mm as exported${o.cut ? ` · ${o.cut} cut-outs applied` : ''}${o.cutFailed ? ' · cut-outs could not be applied' : ''}${o.tris > 400000 ? ' · large mesh, the view may slow down' : ''}</div>
    ${isGear ? `<div class="imp-prev-wrap">
      <canvas class="imp-prev" id="imp-cv-${i}" aria-label="Preview of ${esc(o.name)} in the rack: front, side and top views"></canvas>
      <div class="imp-fit" id="imp-fit-${i}"></div>
      <div class="row imp-tools">
        <button class="btn small" data-imp="auto" data-i="${i}" title="Find the faceplate and turn it to face you">Auto-orient</button>
        ${[0,1,2].map(k => `<button class="btn small" data-imp="rot" data-ax="${k}" data-i="${i}">Turn ${ROT_NAMES[k]} 90°</button>`).join('')}
        <button class="btn small" data-imp="flip" data-i="${i}" title="Turn it around so the back faces you">Front ↔ back</button>
        <button class="btn small" data-imp="upside" data-i="${i}">Upside down</button>
      </div>
      <div class="row3">
        <label class="field">Ear depth (mm)<input class="input mono" type="number" step="0.5" min="0" max="40" id="imp-ear-${i}" value="${o.ear}"></label>
        <label class="field">Height<select class="select" id="imp-hu-${i}"><option value="">Auto</option>${[.5,1,1.5,2,2.5,3,4,5].map(h => `<option value="${h}" ${o.hU === h ? 'selected' : ''}>${fmtHU(h)}</option>`).join('')}</select></label>
        <span></span>
      </div>
    </div>` : `<p class="note imp-att">Turns and moves with ${o.role.startsWith('attach:') ? esc(objs[+o.role.slice(7)].name) : 'its partner'} — check it in that part’s preview (orange).</p>`}
  </div>`;
}
function readImpInputs(){
  if (!pendingImport) return;
  pendingImport.objs.forEach((o, i) => {
    const n = $('#imp-name-' + i); if (n) o.name = n.value.trim() || o.name;
    const r = $('#imp-role-' + i); if (r) o.role = r.value;
    const e = $('#imp-ear-' + i); if (e && Number.isFinite(Number(e.value))) o.ear = clamp(Number(e.value), 0, 40);
    const h = $('#imp-hu-' + i); if (h) o.hU = h.value ? Number(h.value) : null;
  });
}
function redrawImpPreviews(){
  if (!pendingImport) return;
  const {objs} = pendingImport;
  objs.forEach((o, i) => {
    const cv = $('#imp-cv-' + i); if (!cv || o.role !== 'gear') return;
    const kids = pendingImport.edit ? pendingImport.kids : objs.filter(p => p.role === 'attach:' + i);
    const notes = drawImpPreview(cv, o, previewMeshes({pos:o.pos, idx:o.idx, kids}));
    $('#imp-fit-' + i).innerHTML = notes.map(([k, t]) => `<span class="${k === 'bad' ? 'bad' : ''}">${esc(t)}</span>`).join('<span class="dot">·</span>');
  });
}
function openImportModal(){
  const {objs, errors, edit} = pendingImport;
  $('#impTitle').textContent = edit ? 'Check the orientation' : 'Preview the import';
  $('#impOk').textContent = edit ? 'Apply' : 'Add to the build';
  $('#impNote').textContent = edit ? 'Turn the part until the Front view shows its faceplate facing you. Blue is this part, orange is anything attached to it. The dashed lines are the rack: U heights, the post screw holes, and the front and rear posts.'
    : 'Check each part before it goes on the rack: the Front view should show its faceplate facing you. I turned each part the way it most likely sits; fix it with the buttons if not. ' +
      (ASSETS ? 'Parts are saved with this build. ' : 'This view can’t save files, so imported parts last until you close the page. ') + (errors && errors.length ? ' Skipped: ' + errors.join('; ') : '');
  $('#impList').innerHTML = objs.map((o, i) => impRowHTML(o, i, objs, edit)).join('');
  $('#importModal').hidden = false;
  requestAnimationFrame(redrawImpPreviews);
  $('#impOk').focus({preventScroll:true});
}
$('#impList').addEventListener('click', e => {
  const b = e.target.closest('[data-imp]'); if (!b || !pendingImport) return;
  readImpInputs();
  const o = pendingImport.objs[+b.dataset.i]; if (!o) return;
  const turn = (ax, n) => { const R = m3(impRotation({rot:[ax === 0 ? n : 0, ax === 1 ? n : 0, ax === 2 ? n : 0]}), impRotation(o)); o.rot = rotFor(R); };
  if (b.dataset.imp === 'auto') o.rot = autoOrient(o);
  if (b.dataset.imp === 'rot') turn(+b.dataset.ax, 1);
  if (b.dataset.imp === 'flip') turn(2, 2);
  if (b.dataset.imp === 'upside') turn(1, 2);
  redrawImpPreviews();
});
$('#impList').addEventListener('change', e => {
  if (!pendingImport) return;
  const roleChanged = e.target.classList.contains('imp-role');
  readImpInputs();
  if (roleChanged){ const o = pendingImport.objs[+e.target.closest('.imp-row').dataset.i]; if (o.role === 'gear' && !o.autoDone){ o.rot = autoOrient(o); o.autoDone = true; } openImportModal(); }
  else redrawImpPreviews();
});
window.addEventListener('resize', () => { if (pendingImport && !$('#importModal').hidden) redrawImpPreviews(); });
/* the rotation counts that give a rotation matrix (every 90° rotation is reachable) */
function rotFor(R){
  const key = R.map(v => Math.round(v)).join(',');
  for (let a = 0; a < 4; a++) for (let b = 0; b < 4; b++) for (let c = 0; c < 4; c++) if (impRotation({rot:[a, b, c]}).map(v => Math.round(v)).join(',') === key) return [a, b, c];
  return [0, 0, 0];
}
/* reopen the preview for a part that's already imported */
function openOrientEditor(id){
  const m = S.imports.find(x => x.id === id), mesh = IMPORT_MESH[id];
  if (!m || !mesh || typeof mesh !== 'object'){ toast('That part’s mesh hasn’t loaded yet'); return; }
  const kids = childrenImports(id).map(k => IMPORT_MESH[k.id]).filter(x => x && typeof x === 'object');
  pendingImport = {edit:id, kids, errors:[], objs:[{name:m.name, file:m.file, role:'gear', pos:mesh.pos, idx:mesh.idx, lo:m.lo, hi:m.hi, tris:m.tris,
    rot:m.rot.slice(), ear:m.ear, hU:m.hU, nudge:m.nudge.slice()}]};
  openImportModal();
}
function applyOrientEdit(){
  readImpInputs();
  const {edit, objs} = pendingImport, o = objs[0];
  $('#importModal').hidden = true; pendingImport = null;
  if (mode !== 'gear') setMode('gear');
  updateImport(edit, x => { x.name = o.name.slice(0, 60); x.rot = o.rot.slice(); x.ear = o.ear; x.hU = o.hU; });
  registerImports(); refreshAll();
  toast('Orientation updated');
}

async function confirmImport(){
  if (!pendingImport) return;
  if (pendingImport.edit){ applyOrientEdit(); return; }
  readImpInputs();
  const {objs} = pendingImport; $('#importModal').hidden = true;
  objs.forEach(o => { o.name = o.name.slice(0, 60); });
  // attach chains must end at a gear
  objs.forEach((o, i) => { let j = i, guard = 0; while (objs[j].role.startsWith('attach:') && guard++ < objs.length) j = +objs[j].role.slice(7); if (guard >= objs.length || j === i && o.role !== 'gear') o.role = 'gear'; });
  busy('Saving parts…');
  objs.forEach(o => { o.id = uid(); });
  const recs = [];
  for (const o of objs){
    const packed = packMesh(o.pos, o.idx);
    let asset = null;
    if (ASSETS){ try { const r = await ASSETS.upload(new Blob([JSON.stringify(packed)], {type:'application/json'}), {contentType:'application/json'}); asset = r.id; } catch (e) { toast('Couldn’t save ' + o.name + ' — it lasts until you close the page'); } }
    IMPORT_MESH[o.id] = decodeMesh(packed);
    const parent = o.role.startsWith('attach:') ? objs[+o.role.slice(7)].id : null;
    const usedColors = new Set(S.imports.map(m => m.color));
    recs.push({id:o.id, name:o.name, role:parent ? 'attach' : 'gear', parent, asset, rot:parent ? [0,0,0] : o.rot.slice(), ear:parent ? 3 : o.ear, nudge:[0,0,0], hU:parent ? null : o.hU,
      color:(FIBER.find(f => !usedColors.has(f.key) && !['black','white','blue'].includes(f.key)) || FIBER[4]).key, lo:o.lo.map(v => +v.toFixed(3)), hi:o.hi.map(v => +v.toFixed(3)), tris:o.tris, file:o.file});
  }
  busy(null);
  pendingImport = null;
  const firstGear = recs.find(r => r.role === 'gear');
  commit(() => {
    S.imports.push(...recs);
    registerImports();
    for (const r of recs){ uploadMesh('imp:' + r.id); if (!r.asset) r.sessionOnly = true; }
    for (const r of recs.filter(r => r.role === 'gear')) installType('imp:' + r.id, 'batch');
    validateAt();
    for (const r of recs.filter(r => r.role === 'attach')) installType('imp:' + r.id, 'batch');
    if (firstGear) sel = 'imp-' + firstGear.id;
  }, {always:true});
  toast(firstGear && placed('imp-' + firstGear.id) ? `${firstGear.name} → ${instWhere('imp-' + firstGear.id)}` : 'Added to the tray');
}
function loadImportMeshes(){
  for (const m of S.imports){
    if (IMPORT_MESH[m.id]) continue;
    if (!m.asset){ IMPORT_MESH[m.id] = 'missing'; continue; }
    IMPORT_MESH[m.id] = 'loading';
    fetch('/_blob/' + encodeURIComponent(m.asset)).then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(j => { IMPORT_MESH[m.id] = decodeMesh(j); uploadMesh('imp:' + m.id); refreshAll(); })
      .catch(() => { IMPORT_MESH[m.id] = 'missing'; refreshAll(); });
  }
}
function updateImport(id, fn){
  const m = S.imports.find(x => x.id === id); if (!m) return;
  fn(m); delete BVH['imp:' + id];
  const inst = instById('imp-' + id), a = inst && S.at[inst.id];
  validateAt();
  if (a && a.u != null && !S.at[inst.id]) toast('It no longer fits there, so it went back to the tray');
  markDirty(); refreshAll();
}
async function deleteImport(id){
  const ids = [id, ...childrenImports(id).map(m => m.id)];
  const gone = S.imports.filter(m => ids.includes(m.id));
  commit(() => { S.imports = S.imports.filter(m => !ids.includes(m.id)); for (const x of ids){ delete S.at['imp-' + x]; delete S.colors['imp:' + x]; dropGPU('imp:' + x); delete IMPORT_MESH[x]; delete BVH['imp:' + x]; } registerImports(); if (ids.some(x => sel === 'imp-' + x)) sel = null; }, {always:true});
  confirmDel = null;
  if (ASSETS) for (const m of gone) if (m.asset) ASSETS.delete(m.asset).catch(() => {});
  toast('Import deleted');
}

/* ================= interaction: canvas ================= */
let ptrs = new Map(), gesture = null, hoverQueued = false, lastHoverXY = null;
function stageXY(e){ const r = stage.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; }
canvas.addEventListener('pointerdown', e => {
  canvas.focus({preventScroll:true});
  ptrs.set(e.pointerId, stageXY(e));
  try { canvas.setPointerCapture(e.pointerId); } catch (err) {}
  if (ptrs.size === 2){ const [a, b] = [...ptrs.values()]; gesture = {kind:'pinch', d0:Math.hypot(a[0]-b[0], a[1]-b[1]), dist0:cam.dist, mid0:[(a[0]+b[0])/2, (a[1]+b[1])/2], target0:cam.target.slice()}; return; }
  const xy = stageXY(e), panMode = e.button === 2 || e.button === 1 || e.shiftKey;
  let hit = null;
  if (mode !== 'ask' && !panMode){ hit = pick(xy[0], xy[1]); }
  if (hit && hit.inst === sel && S.at[sel] && mode !== 'ask' && draggableNow(sel)) gesture = {kind:'maybePart', x0:xy[0], y0:xy[1], hit, pid:e.pointerId};
  else gesture = {kind:panMode ? 'pan' : 'maybeOrbit', x0:xy[0], y0:xy[1], last:xy, hit, pid:e.pointerId, button:e.button};
});
canvas.addEventListener('pointermove', e => {
  const xy = stageXY(e);
  if (ptrs.has(e.pointerId)) ptrs.set(e.pointerId, xy);
  if (gesture && gesture.kind === 'pinch' && ptrs.size === 2){
    const [a, b] = [...ptrs.values()], d = Math.hypot(a[0]-b[0], a[1]-b[1]);
    cam.dist = clamp(gesture.dist0 * gesture.d0 / Math.max(d, 10), 180, 3200); camAnim = null; requestRender(); return;
  }
  if (!gesture){ queueHover(xy); return; }
  const dx = xy[0] - gesture.x0, dy = xy[1] - gesture.y0, far = Math.hypot(dx, dy) > 5;
  if (gesture.kind === 'maybePart' && far){ startDrag({kind:'placed', instId:gesture.hit.inst, type:instById(gesture.hit.inst).type, pid:gesture.pid}); gesture = null; updateDrag(e.clientX, e.clientY); return; }
  if (gesture.kind === 'maybeOrbit' && far){ gesture.kind = 'orbit'; stage.classList.add('is-orbit'); }
  if (gesture.kind === 'orbit' || gesture.kind === 'pan'){
    const mx = xy[0] - gesture.last[0], my = xy[1] - gesture.last[1]; gesture.last = xy; camAnim = null;
    if (gesture.kind === 'orbit'){ cam.yaw -= mx * 0.0075; cam.pitch = clamp(cam.pitch + my * 0.0075, -1.45, 1.54); }
    else { const {s, u} = camBasis(), k = cam.dist * Math.tan(cam.fov / 2) * 2 / vh; cam.target = add(cam.target, add(scl(s, -mx * k), scl(u, my * k))); }
    requestRender();
  }
});
function endPointer(e){
  ptrs.delete(e.pointerId);
  stage.classList.remove('is-orbit');
  if (!gesture){ return; }
  if (gesture.kind === 'pinch'){ if (ptrs.size < 2) gesture = null; return; }
  const g = gesture; gesture = null;
  if (e.type === 'pointercancel') return;
  if (g.kind === 'maybeOrbit' || g.kind === 'maybePart'){
    const xy = stageXY(e);
    if (mode === 'ask'){ const hit = pick(xy[0], xy[1]); if (hit) createSpot(hit); else toast('Click on a part of the build'); return; }
    const hit = g.hit || null;
    if (mode === 'cables'){ const cid = pickCable(xy[0], xy[1]); if (cid){ selCable = cid; sel = null; tab = 'part'; refreshAll(); return; } selCable = null; }
    sel = hit ? hit.inst : null;
    tab = 'part'; refreshAll();
  }
}
canvas.addEventListener('pointerup', endPointer);
canvas.addEventListener('pointercancel', endPointer);
canvas.addEventListener('pointerleave', () => { if (!gesture && hover){ hover = null; setReadout(null); requestRender(); } });
canvas.addEventListener('contextmenu', e => e.preventDefault());
canvas.addEventListener('wheel', e => { e.preventDefault(); camAnim = null; cam.dist = clamp(cam.dist * Math.exp(e.deltaY * (e.deltaMode === 1 ? 0.04 : 0.0012)), 180, 3200); requestRender(); }, {passive:false});
function queueHover(xy){ lastHoverXY = xy; if (hoverQueued) return; hoverQueued = true; requestAnimationFrame(() => { hoverQueued = false; doHover(lastHoverXY); }); }
function doHover(xy){
  const hit = pick(xy[0], xy[1]);
  const prev = hover && hover.inst; hover = hit;
  stage.classList.toggle('over-part', !!hit && mode !== 'ask' && hit.inst !== sel);
  stage.classList.toggle('over-sel', !!hit && mode !== 'ask' && hit.inst === sel && draggableNow(sel));
  setReadout(hit);
  if ((hit && hit.inst) !== prev) requestRender();
}
const draggableNow = id => mode !== 'ask' && canEdit(id);
function setReadout(hit){
  if (!hit){ $('#roCode').textContent = sel ? instWhere(sel) : '—'; $('#roWhat').textContent = sel ? instLabel(sel) : (mode === 'ask' ? 'Click a spot on the build to ask about it' : 'Hover the rack to read a position'); $('#roXyz').textContent = ''; return; }
  const r = refFor(hit.p, hit.n);
  $('#roCode').textContent = r.code; $('#roWhat').textContent = instLabel(hit.inst) + (r.hole ? '' : ' · ' + r.depth); $('#roXyz').textContent = r.xyz;
}

/* ================= interaction: drag and drop ================= */
function startDrag(d){
  const T = TYPES[d.type];
  dragState = {...d, active:true, gear:T.kind === 'gear', cands:candidates(d.type, d.instId || null), best:null};
  document.body.style.userSelect = 'none';
  const lab = $('#dragLabel'); lab.hidden = false;
  requestRender();
}
function updateDrag(cx, cy){
  if (!dragState) return;
  const r = stage.getBoundingClientRect(), x = cx - r.left, y = cy - r.top;
  const tr = $('#tray').getBoundingClientRect();
  const overTray = dragState.kind === 'placed' && cx >= tr.left && cx <= tr.right && cy >= tr.top && cy <= tr.bottom;
  $('#tray').classList.toggle('is-over', overTray);
  let best = null, bd = Infinity;
  const inStage = x >= 0 && y >= 0 && x <= r.width && y <= r.height;
  for (const c of dragState.cands){
    c.screen = project(c.anchor);
    if (!c.screen || !inStage || overTray) continue;
    const d = Math.hypot(c.screen[0] - x, c.screen[1] - y);
    if (d < bd){ bd = d; best = c; }
  }
  const lim = dragState.gear ? 220 : 140;
  dragState.best = best && bd <= lim ? best : null;
  dragState.overTray = overTray;
  const T = TYPES[dragState.type], lab = $('#dragLabel');
  lab.innerHTML = `${esc(T.name)}<small>${overTray ? 'Release to take it off' : dragState.best ? '→ ' + esc(dragState.best.label) : dragState.cands.length ? 'Move toward a teal dot' : (T.kind === 'attach' ? 'Put its partner on the rack first' : 'No open spot')}</small>`;
  lab.style.left = (cx + 14) + 'px'; lab.style.top = (cy + 12) + 'px';
  requestRender();
}
function endDrag(cancel){
  if (!dragState) return;
  const d = dragState; dragState = null; document.body.style.userSelect = '';
  $('#dragLabel').hidden = true; $('#tray').classList.remove('is-over');
  if (!cancel){
    if (d.kind === 'placed' && d.overTray) unplace(d.instId);
    else if (d.best){
      const T = TYPES[d.type];
      if (T.bin){ let id = null; commit(() => { id = placeCandidate(d.type, d.instId || null, d.best); sel = id; tab = 'part'; }); toast(`${T.name} → ${d.best.label}${d.type === 'cable_guide' ? ' · inserts added at a and c' : ''}`); if (d.best.newLevel) setView(lastView); }
      else {
        const inst = d.instId ? instById(d.instId) : nextUnplaced(d.type);
        if (inst){ commit(() => { S.at[inst.id] = d.best.at; sel = inst.id; tab = 'part'; }); toast(`${T.name} → ${d.best.label}`); }
      }
    } else if (d.kind === 'tray') toast(d.cands.length ? 'Drop it onto a teal dot to snap it in' : 'There’s no open spot for that part');
  }
  requestRender();
}
let trayDrag = null;
$('#trayList').addEventListener('pointerdown', e => {
  const b = e.target.closest('.part'); if (!b || b.disabled || e.button !== 0 || !b.dataset.type) return;
  trayDrag = {type:b.dataset.type, x0:e.clientX, y0:e.clientY, pid:e.pointerId, started:false};
});
window.addEventListener('pointermove', e => {
  if (trayDrag && e.pointerId === trayDrag.pid && !trayDrag.started && Math.hypot(e.clientX - trayDrag.x0, e.clientY - trayDrag.y0) > 6){
    if (!TYPES[trayDrag.type].bin && !nextUnplaced(trayDrag.type)){ trayDrag = null; return; }
    trayDrag.started = true; startDrag({kind:'tray', type:trayDrag.type, instId:null});
  }
  if (dragState) updateDrag(e.clientX, e.clientY);
});
window.addEventListener('pointerup', e => {
  if (dragState){ endDrag(false); trayDrag = null; suppressClick = true; setTimeout(() => { suppressClick = false; }, 0); return; }
  trayDrag = null;
});
window.addEventListener('pointercancel', () => { if (dragState) endDrag(true); trayDrag = null; });
let suppressClick = false;
$('#trayList').addEventListener('click', e => {
  if (suppressClick) return;
  const act = e.target.closest('[data-act]');
  if (act){
    const sum = insertSummary();
    if (act.dataset.act === 'insTool'){ insertTool = !insertTool; if (insertTool && explode > 0.01){ explode = 0; $('#explode').value = 0; } renderTray(); requestRender(); if (insertTool) toast('Click a hole to add or remove an insert. Red rings need one'); }
    if (act.dataset.act === 'insAll'){ commit(() => { for (const k of sum.missing) S.inserts[k] = true; }); toast(`${sum.missing.length} inserts added`); }
    if (act.dataset.act === 'insClear'){ commit(() => { S.inserts = {}; }); toast('Inserts cleared — Undo puts them back'); }
    return;
  }
  const cb = e.target.closest('[data-cable]'); if (cb){ selCable = cb.dataset.cable; sel = null; pendingPort = null; tab = 'part'; refreshAll(); return; }
  const b = e.target.closest('.part'); if (!b || b.disabled || !b.dataset.type) return;
  installType(b.dataset.type);
});

/* ================= interaction: panels and keys ================= */
$('#modeSeg').addEventListener('click', e => { const b = e.target.closest('button'); if (b) setMode(b.dataset.mode); });
function setMode(m){
  mode = m; document.querySelectorAll('#modeSeg button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.mode === m)));
  if (m !== 'ask'){ try { localStorage.setItem('labrax-assembler-mode', m); } catch (e) {} }
  stage.classList.toggle('mode-ask', m === 'ask');
  if (m !== 'cables'){ selCable = null; pendingPort = null; }
  if (m !== 'frame') insertTool = false;
  if (m === 'ask'){ tab = 'ask'; renderTabs(); renderAsk(); }
  else if (m === 'cables'){ if (sel && !TYPES[instById(sel)?.type]?.dev) sel = null; tab = 'part'; renderTabs(); }
  else if (sel && !draggableNow(sel)) sel = null;
  if (m !== 'ask') lastBuildMode = m;
  renderTray(); renderPart(); setReadout(null); requestRender();
  $('#undoBtn').disabled = !H().past.length; $('#redoBtn').disabled = !H().future.length;
}
let lastBuildMode = mode;
document.querySelector('#presetRow').addEventListener('click', e => { const b = e.target.closest('[data-preset]'); if (b) usePreset(b.dataset.preset); });
$('#viewSeg').addEventListener('click', e => { const b = e.target.closest('button'); if (b) setView(b.dataset.view); });
$('#explode').addEventListener('input', e => { explode = Number(e.target.value) / 100; requestRender(); });
$('#assembleAll').addEventListener('click', assembleAll);
$('#takeApart').addEventListener('click', takeApart);
$('#undoBtn').addEventListener('click', undo); $('#redoBtn').addEventListener('click', redo);
$('#importBtn').addEventListener('click', () => $('#importFile').click());
$('#importFile').addEventListener('change', e => { const fs = [...(e.target.files || [])]; e.target.value = ''; importFiles(fs); });
$('#impCancel').addEventListener('click', () => { $('#importModal').hidden = true; pendingImport = null; });
$('#impOk').addEventListener('click', confirmImport);
$('#importModal').addEventListener('click', e => { if (e.target.id === 'importModal'){ $('#importModal').hidden = true; pendingImport = null; } });
document.querySelector('.tabs').addEventListener('click', e => { const b = e.target.closest('[role=tab]'); if (b){ tab = b.dataset.tab; renderTabs(); if (tab === 'ask') renderAsk(); } });
async function copyText(t){ try { await navigator.clipboard.writeText(t); toast('Copied ' + t); } catch (e) { toast('Copy blocked — select the reference text instead'); } }
$('#tab-part').addEventListener('click', e => {
  const sc = e.target.closest('[data-act="selCable"]'); if (sc){ setMode('cables'); selCable = sc.dataset.cable; sel = null; refreshAll(); return; }
  const cc = e.target.closest('[data-ccolor]'); if (cc && selCable){ commit(() => { const c = S.cables.find(x => x.id === selCable); if (c) c.color = cc.dataset.ccolor; }); return; }
  const rb = e.target.closest('#cRoute button, #cSpine button');
  if (rb && selCable){ const key = rb.closest('#cRoute') ? 'route' : 'spine'; commit(() => { const c = S.cables.find(x => x.id === selCable); if (c) c[key] = rb.dataset.v; }); return; }
  if (e.target.closest('[data-act="delCable"]') && selCable){ deleteCable(selCable); return; }
  const c = e.target.closest('[data-color]');
  if (c && sel){ const inst = instById(sel); S.colors[inst.type] = c.dataset.color; if (TYPES[inst.type].imp) TYPES[inst.type].imp.color = c.dataset.color; markDirty(); refreshAll(); return; }
  const a = e.target.closest('[data-act]'); if (!a || !sel) return;
  const inst = instById(sel), T = TYPES[inst.type];
  if (['up','down','left','right','swap','remove','install','rot','delImp','mount','mnudge','mrefit','mturn','munmount'].includes(a.dataset.act) && !canEdit(sel)){ toast(T.kind === 'frame' ? 'Switch to Frame mode to change the frame' : 'Switch to Gear mode to change gear'); return; }
  ({ up:() => inst.type === 'ext_module' ? moveLevel(sel, 1) : moveGear(sel, 1), down:() => inst.type === 'ext_module' ? moveLevel(sel, -1) : moveGear(sel, -1), remove:() => unplace(sel),
     left:() => moveDev(sel, -20, 0), right:() => moveDev(sel, 20, 0), swap:() => swapSide(sel),
     install:() => { const cands = candidates(inst.type, inst.id); if (!cands.length){ toast(T.kind === 'attach' ? `Put the ${TYPES[T.parent].name} on the rack first` : 'No open spot'); return; } commit(() => { S.at[inst.id] = cands[0].at; }); },
     hide:() => { if (S.hidden[sel]) delete S.hidden[sel]; else S.hidden[sel] = true; markDirty(); refreshAll(); },
     ask:() => { setMode('ask'); toast('Click the spot on this part you want to ask about'); },
     copyRef:() => copyText(a.dataset.ref),
     rot:() => updateImport(T.imp.id, m => { m.rot[+a.dataset.ax] = (m.rot[+a.dataset.ax] + 1) % 4; }),
     delImp:() => { if (confirmDel === T.imp.id) deleteImport(T.imp.id); else { confirmDel = T.imp.id; renderPart(); } },
     cancelDel:() => { confirmDel = null; renderPart(); },
     orient:() => openOrientEditor(T.imp.role === 'attach' ? T.imp.parent : T.imp.id),
     mount:() => { const v = $('#brSel') && $('#brSel').value; if (v) mountDevice(sel, v); },
     mnudge:() => nudgeMounted(sel, a.dataset.v.split(',').map(Number)),
     mrefit:() => { const at = S.at[sel]; mountDevice(sel, at.p, at.rz || 0); },
     mturn:() => { const at = S.at[sel]; mountDevice(sel, at.p, ((at.rz || 0) + 1) & 3); },
     munmount:() => { const id = sel, at = defAt(TYPES[inst.type].dev, id); commit(() => { if (at) S.at[id] = at; else delete S.at[id]; }); toast(at ? `${TYPES[inst.type].dev.short} → ${instWhere(id)}` : `${TYPES[inst.type].dev.short} is back in the tray`); }
  })[a.dataset.act]?.();
});
$('#tab-part').addEventListener('change', e => {
  const inst = sel && instById(sel), m = inst && TYPES[inst.type].imp; if (!m) return;
  const v = Number(e.target.value);
  if (e.target.id === 'f-ear' && Number.isFinite(v)) updateImport(m.id, x => { x.ear = clamp(v, 0, 40); });
  if (e.target.id === 'f-hu') updateImport(m.id, x => { x.hU = e.target.value ? clamp(v, .5, RU) : null; });
  if (/^f-n[xyz]$/.test(e.target.id) && Number.isFinite(v)) updateImport(m.id, x => { x.nudge['xyz'.indexOf(e.target.id.slice(-1))] = clamp(v, -200, 200); });
});
$('#tab-ask').addEventListener('click', e => {
  const s = e.target.closest('[data-spot]'); if (s){ activeSpot = s.dataset.spot; confirmDel = null; renderAsk(); requestRender(); return; }
  const a = e.target.closest('[data-act]'); if (!a) return;
  const sp = activeSpot && spotById(activeSpot);
  ({ startPoint:() => setMode('ask'), send:sendQuestion, copySpot:() => sp && copyText(sp.pin.code + ' (' + sp.pin.part + ', ' + sp.pin.xyz + ')'),
     delSpot:() => { if (!sp) return; if (confirmDel === 'spot:' + sp.id){ spots = spots.filter(x => x.id !== sp.id); if (spotsRef) spotsRef.doc(sp.id).delete().catch(() => {}); else saveSpotsLocal(); activeSpot = null; confirmDel = null; renderTabs(); renderAsk(); requestRender(); } else { confirmDel = 'spot:' + sp.id; renderAsk(); } },
     cancelDel:() => { confirmDel = null; renderAsk(); }
  })[a.dataset.act]?.();
});
$('#tab-ask').addEventListener('input', e => { if (e.target.id === 'askInput'){ const sp = spotById(activeSpot); if (sp) sp.draft = e.target.value; } if (e.target.id === 'askSnap'){ const sp = spotById(activeSpot); if (sp) sp.noSnap = !e.target.checked; } });
$('#tab-ask').addEventListener('keydown', e => { if (e.target.id === 'askInput' && e.key === 'Enter' && (e.metaKey || e.ctrlKey)){ e.preventDefault(); sendQuestion(); } });
$('#tab-ref').addEventListener('change', e => {
  if (e.target.id === 'optLabels'){ S.settings.labels = e.target.checked; markDirty(); refreshAll(); }
});
$('#tab-ref').addEventListener('click', e => {
  const b = e.target.closest('button'); if (!b) return;
  if (b.closest('#optSides')){ S.settings.sides = b.dataset.v; markDirty(); refreshAll(); }
  if (b.closest('#optNum')){ S.settings.numbering = b.dataset.v; markDirty(); refreshAll(); }
  if (b.dataset.frame){ S.settings.frame = b.dataset.frame; markDirty(); refreshAll(); }
});
document.addEventListener('keydown', e => {
  if (!$('#importModal').hidden){ if (e.key === 'Escape'){ $('#importModal').hidden = true; pendingImport = null; } return; }
  const typing = e.target.matches('input, textarea, select'), mod = e.ctrlKey || e.metaKey;
  if (mod && e.key.toLowerCase() === 'z' && !typing){ e.preventDefault(); e.shiftKey ? redo() : undo(); return; }
  if (mod && e.key.toLowerCase() === 'y' && !typing){ e.preventDefault(); redo(); return; }
  if (typing) return;
  if (e.key === 'Escape'){ if (dragState){ endDrag(true); return; } if (mode === 'ask'){ setMode(lastBuildMode); return; } if (pendingPort || selCable){ pendingPort = null; selCable = null; refreshAll(); return; } sel = null; refreshAll(); return; }
  if (mode === 'cables' && selCable && (e.key === 'Delete' || e.key === 'Backspace')){ e.preventDefault(); deleteCable(selCable); return; }
  if (!sel) return;
  const a = S.at[sel];
  if (['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Delete','Backspace'].includes(e.key) && !canEdit(sel) && (S.at[sel] || e.key.startsWith('Arrow'))){ e.preventDefault(); toast(TYPES[instById(sel).type].kind === 'frame' ? 'Switch to Frame mode to change the frame' : 'Switch to Gear mode to change gear'); return; }
  if (e.key.startsWith('Arrow') && a && a.off){ e.preventDefault(); nudgeMounted(sel, {ArrowLeft:[-1,0,0], ArrowRight:[1,0,0], ArrowUp:[0,0,1], ArrowDown:[0,0,-1]}[e.key]); }
  else if ((e.key === 'ArrowLeft' || e.key === 'ArrowRight') && a && a.wall){ e.preventDefault(); moveDev(sel, e.key === 'ArrowLeft' ? -20 : 20, 0); }
  else if ((e.key === 'ArrowUp' || e.key === 'ArrowDown') && a && a.wall){ e.preventDefault(); moveDev(sel, 0, e.key === 'ArrowUp' ? 20 : -20); }
  else if ((e.key === 'ArrowUp' || e.key === 'ArrowDown') && a && a.u != null){ e.preventDefault(); moveGear(sel, e.key === 'ArrowUp' ? 1 : -1); }
  else if ((e.key === 'ArrowUp' || e.key === 'ArrowDown') && a && a.s && instById(sel).type === 'ext_module'){ e.preventDefault(); moveLevel(sel, e.key === 'ArrowUp' ? 1 : -1); }
  else if ((e.key === 'Delete' || e.key === 'Backspace') && a){ e.preventDefault(); unplace(sel); }
});

/* ================= misc ================= */
let toastTimer = null;
function toast(msg){ const t = $('#toast'); t.textContent = msg; t.classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => t.classList.remove('show'), 2800); }
function busy(msg){ const b = $('#busy'); if (msg){ b.textContent = msg; b.hidden = false; } else b.hidden = true; }
function refreshAll(){
  $('#undoBtn').disabled = !H().past.length; $('#redoBtn').disabled = !H().future.length;
  const s = S.settings;
  $('#sub').textContent = !RU ? `Lab Rax · no posts yet · ${INST.filter(i => placed(i.id)).length} parts on` : `Lab Rax ${RU}U${S.levels.length > 1 ? ' (' + S.levels.map(l => levelU(l) + 'U').join(' + ') + ')' : ''} · ${unitLabel(RU - 1)}–${unitLabel(0)} · ${INST.filter(i => placed(i.id)).length}/${INST.length} parts on`;
  if (sel && !instById(sel)) sel = null;
  renderTray(); renderTabs(); renderPart(); renderRef(); renderAsk(); setReadout(null); requestRender();
}

/* ================= boot ================= */
if (location.hash === '#debug') window.__lr = {project:p => project(p), pick:(x, y) => pick(x, y), state:() => S, inst:() => INST, refFor, worldPose, spots:() => spots,
  routes:() => { updateRoutes(); return ROUTES; }, ports:devPorts, clashes, insertSummary, setMode:m => setMode(m), sel:id => { sel = id; refreshAll(); }, selCable:id => { selCable = id; refreshAll(); }, connectPort, explode:v => { explode = v; requestRender(); }};
try { if (gl) initGL(); } catch (err) { console.error(err); $('#glFail').hidden = false; $('#glFail').textContent = 'The 3D view could not start: ' + err.message; }
new ResizeObserver(resize).observe(stage);
resize(); cam.dist = fitDist();
readTheme();
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', readTheme);
new MutationObserver(readTheme).observe(document.documentElement, {attributes:true, attributeFilter:['data-theme']});
loadImportMeshes();
refreshAll();
setView('iso', false);
setMode(mode);

(async () => {
  const c = window.claude;
  if (!c || typeof c.use !== 'function'){ setStatus('local'); return; }
  const [db, assets, sample] = await Promise.all(['db', 'assets', 'sample'].map(n => c.use(n).catch(() => null)));
  ASSETS = assets; SAMPLE = sample || null;
  if (SAMPLE){ try { const lim = await SAMPLE.limits(); sampleImages = !!(lim && lim.images); } catch (e) {} }
  renderAsk();
  if (!db){ setStatus('local'); return; }
  DB = db;
  try { remoteRef = db.doc(REMOTE_PATH); } catch (e) { setStatus('local'); return; }
  let snapDoc;
  try { snapDoc = await remoteRef.get(); } catch (e) { remoteRef = null; setStatus('local'); return; }
  if (snapDoc.exists){
    const d = snapDoc.data();
    if (localMeta.dirty && localMeta.editedAt > (Number(d.savedAt) || 0)) scheduleRemote();
    else { adoptRemote(d); setStatus('saved'); }
  } else if (localMeta.dirty) scheduleRemote();
  else setStatus('saved');
  remoteRef.onSnapshot(s => {
    if (!s.exists || s.metadata.hasPendingWrites) return;
    const d = s.data();
    if (!d || d.client === CLIENT || saving || remoteTimer) return;
    if ((Number(d.savedAt) || 0) <= lastApplied) return;
    adoptRemote(d); toast('Updated from another device');
  }, () => {});
  try {
    spotsRef = db.collection('spots');
    const localSpots = spots.slice();
    spotsRef.onSnapshot(q => {
      const remote = q.docs.map(d => sanitizeSpot({...d.data(), id:d.id})).filter(Boolean);
      const keepDrafts = new Map(spots.map(s => [s.id, s]));
      spots = remote.sort((a, b) => a.createdAt - b.createdAt).map(s => { const o = keepDrafts.get(s.id); if (o){ s.draft = o.draft; s.noSnap = o.noSnap; if (asking && asking.spot === s.id) s.messages = o.messages; } return s; });
      if (activeSpot && !spotById(activeSpot)) activeSpot = null;
      renderTabs(); if (tab === 'ask') renderAsk(); requestRender();
    }, () => {});
    for (const s of localSpots) saveSpot(s);
    try { localStorage.removeItem(LS_SPOTS); } catch (e) {}
  } catch (e) { spotsRef = null; }
})();
})();
