// Quality sliders (Brian, 2026-10-19: "a quality slider bar for the rendering", both kinds).
// Preview quality: Low / Medium / High for the on-screen 3D views. A per-viewer, per-browser preference only
// (never in the rack, library or project data). Medium is exactly today's look; Low draws at a lower
// resolution and merges nearby mesh points (drawn meshes only); High draws at a higher resolution.
// Export quality: Draft / Standard / Fine = OpenSCAD $fn 24 / 48 / 96 for the generic equipment_tray.scad STLs
// (mirrors equipment.EXPORT_QUALITY). Standard is the template's own $fn=48. Curve resolution changes the mesh
// only; fit and strength stay UNKNOWN at every level.
(function(root){
  'use strict';
  const PREVIEW={low:{label:'Low',scale:0.6,cell:1.5,segments:12},medium:{label:'Medium',scale:1,cell:0,segments:24},
    high:{label:'High',scale:1.5,cell:0,segments:48}};
  const PREVIEW_ORDER=['low','medium','high'],PREVIEW_DEFAULT='medium';
  const EXPORT={draft:{label:'Draft',fn:24},standard:{label:'Standard',fn:48},fine:{label:'Fine',fn:96}};
  const EXPORT_ORDER=['draft','standard','fine'],EXPORT_DEFAULT='standard';
  const KEY='assemblyWorkshop.previewQuality.',EXPORT_KEY='assemblyWorkshop.exportQuality';
  // Browser storage can be missing or throw (private windows, blocked site data): fall back to the defaults.
  function read(key){try{return root.localStorage?.getItem(key)??null;}catch(e){return null;}}
  function write(key,value){try{root.localStorage?.setItem(key,value);}catch(e){}}
  const previewLevel=viewer=>{const v=read(KEY+viewer);return PREVIEW[v]?v:PREVIEW_DEFAULT;};
  const setPreviewLevel=(viewer,level)=>{if(PREVIEW[level])write(KEY+viewer,level);};
  const exportLevel=()=>{const v=read(EXPORT_KEY);return EXPORT[v]?v:EXPORT_DEFAULT;};
  const setExportLevel=level=>{if(EXPORT[level])write(EXPORT_KEY,level);};
  // Canvas pixel ratio for a viewer: its usual ratio (today's) times the level's scale.
  // Medium returns the base unchanged, so today's views are untouched.
  function pixelRatio(viewer,base){
    const b=base>0?base:1,scale=PREVIEW[previewLevel(viewer)].scale;
    return scale===1?b:Math.max(0.5,Math.min(3,b*scale));
  }
  const segments=viewer=>PREVIEW[previewLevel(viewer)].segments;
  // Low detail: vertex clustering on a flat triangle list [x,y,z, x,y,z, x,y,z, ...]. Points in the same
  // cell (mm) snap to the cell's first point; triangles that collapse are dropped. Drawing only; the
  // source mesh is never changed. cell 0 returns the same array.
  const cache=new WeakMap();
  function simplify(v,cell){
    if(!cell||!v||v.length<9)return v;
    let byCell=cache.get(v);if(byCell&&byCell.has(cell))return byCell.get(cell);
    const reps=new Map(),out=[],key=new Array(3);
    for(let i=0;i<v.length;i+=9){
      for(let k=0;k<3;k++){const j=i+3*k,id=Math.round(v[j]/cell)+','+Math.round(v[j+1]/cell)+','+Math.round(v[j+2]/cell);
        if(!reps.has(id))reps.set(id,[v[j],v[j+1],v[j+2]]);key[k]=id;}
      if(key[0]===key[1]||key[1]===key[2]||key[0]===key[2])continue;
      for(let k=0;k<3;k++)out.push(...reps.get(key[k]));
    }
    if(!byCell){byCell=new Map();cache.set(v,byCell);}byCell.set(cell,out);
    return out;
  }
  const cell=viewer=>PREVIEW[previewLevel(viewer)].cell;
  const exportNote=level=>`${EXPORT[level].label} ($fn ${EXPORT[level].fn})`;
  const api={PREVIEW,PREVIEW_ORDER,PREVIEW_DEFAULT,EXPORT,EXPORT_ORDER,EXPORT_DEFAULT,previewLevel,setPreviewLevel,
    exportLevel,setExportLevel,pixelRatio,segments,simplify,cell,exportNote};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;
  root.RenderQuality=api;
  if(typeof document==='undefined')return;

  // A 3-stop range slider with its current label. onchange(level) runs after the level is stored.
  function slider(order,table,current,title,onpick,cls){
    const wrap=document.createElement('label'),input=document.createElement('input'),out=document.createElement('output');
    wrap.className='rq-slider'+(cls?' '+cls:'');wrap.title=title;
    const name=document.createElement('span');name.className='rq-name';name.textContent=title.split(':')[0];
    input.type='range';input.min='0';input.max=String(order.length-1);input.step='1';input.value=String(order.indexOf(current));
    input.setAttribute('aria-label',title.split(':')[0]);
    const show=()=>{const level=order[+input.value];out.textContent=table[level].label;input.setAttribute('aria-valuetext',table[level].label);return level;};
    show();input.oninput=()=>onpick(show());
    wrap.append(name,input,out);
    return wrap;
  }
  // Preview slider for one viewer; redraw() repaints that viewer.
  api.previewSlider=(viewer,redraw,cls)=>slider(PREVIEW_ORDER,PREVIEW,previewLevel(viewer),
    'Preview quality: Low is faster, High is sharper. Display only; saved in this browser for this view.',
    level=>{setPreviewLevel(viewer,level);redraw&&redraw(level);},cls);
  // Export slider; the label next to the export button shows the level and its $fn.
  api.exportSlider=(onpick,cls)=>{
    const s=slider(EXPORT_ORDER,EXPORT,exportLevel(),'Export quality: curve detail of the STL files (OpenSCAD $fn). Standard = $fn 48, as before.',
      level=>{setExportLevel(level);s.querySelector('output').textContent=exportNote(level);onpick&&onpick(level);},cls);
    s.querySelector('output').textContent=exportNote(exportLevel());
    return s;
  };
  const style=document.createElement('style');
  style.textContent='.rq-slider{display:inline-flex;align-items:center;gap:6px;font-size:12px;white-space:nowrap}.rq-slider input[type=range]{width:72px;margin:0}.rq-slider output{min-width:46px;color:#cfd6df}.rq-slider .rq-name{color:#9aa7b6}';
  (document.head||document.documentElement).append(style);
})(typeof window!=='undefined'?window:globalThis);
