// Wiring sheet drawing (cable management Step 5; decisions in work/cable-management/Step5_Decisions.md).
// Planning documents made from the SAVED rack only: lengths are estimates; guide capacity, cable fit,
// bend tolerance and strength are UNKNOWN. Nothing here saves, prints or touches any STL.
(function(root){
  'use strict';
  const U=44.45,POST_X=118.26;
  const PAPER={letter:{label:'US Letter',css:'letter',w:279.4,h:215.9},a4:{label:'A4',css:'A4',w:297,h:210}};
  const COLORS={power:'#d85a30',data:'#1d9e75',patch:'#378add',guide:'#888780',ink:'#1d2733',muted:'#5f6b78',line:'#9aa5b1',fill:'#f3f5f7'};
  const EXIT_TEXT={'bottom-rear':'Bottom rear','top-rear':'Top rear',left:'Left side',right:'Right side'};
  const W=1000,H=700;
  const esc=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  const pad=n=>String(n).padStart(2,'0');
  const safeName=name=>String(name||'lab-rax').replace(/[^\w-]+/g,'_');
  const n1=v=>Math.round(v*10)/10;
  const list=(rack,key)=>rack.cabling?.[key]||[];
  const zmid=(rack,slot)=>(rack.slots-slot)*U+U/2;
  // Same anchors as cable-routes.js / workspace.js (x across the rack, z up from the bottom).
  const guideAnchor=(rack,g)=>[g.post[1]==='L'?-POST_X:POST_X,zmid(rack,g.slot)];
  function exitAnchor(rack,e){
    if(e.position==='bottom-rear')return [0,-10];
    if(e.position==='top-rear')return [0,rack.slots*U+10];
    return [e.position==='left'?-140:140,zmid(rack,e.slot)];
  }
  const exitLabel=e=>(EXIT_TEXT[e.position]||e.position)+(e.position==='left'||e.position==='right'?' U'+pad(e.slot):'');
  // Which way a cable leaves through an exit, in rack coordinates [dx, dz].
  const exitOut=e=>e.position==='bottom-rear'?[0,-1]:e.position==='top-rear'?[0,1]:[e.position==='left'?-1:1,0];
  function wrap(text,max){
    const out=[];let line='';
    for(const word of String(text).split(/\s+/).filter(Boolean)){
      if(line&&(line+' '+word).length>max){out.push(line);line=word;}else line=line?line+' '+word:word;
    }
    if(line)out.push(line);return out;
  }
  const clip=(text,max)=>{text=String(text);return text.length>max?text.slice(0,Math.max(1,max-1))+'…':text;};
  // Smooth line through the points (Catmull-Rom as cubic Béziers).
  function smooth(pts){
    if(pts.length<2)return '';
    let d=`M${n1(pts[0][0])} ${n1(pts[0][1])}`;
    for(let i=0;i<pts.length-1;i++){
      const p0=pts[i-1]||pts[i],p1=pts[i],p2=pts[i+1],p3=pts[i+2]||p2;
      const c1=[p1[0]+(p2[0]-p0[0])/6,p1[1]+(p2[1]-p0[1])/6],c2=[p2[0]-(p3[0]-p1[0])/6,p2[1]-(p3[1]-p1[1])/6];
      d+=` C${n1(c1[0])} ${n1(c1[1])} ${n1(c2[0])} ${n1(c2[1])} ${n1(p2[0])} ${n1(p2[1])}`;
    }
    return d;
  }
  function midpoint(pts){
    if(pts.length===1)return pts[0];
    const seg=pts.slice(1).map((p,i)=>Math.hypot(p[0]-pts[i][0],p[1]-pts[i][1])),total=seg.reduce((a,b)=>a+b,0);
    let left=total/2;
    for(let i=0;i<seg.length;i++){if(left<=seg[i]||i===seg.length-1){const t=seg[i]?Math.min(1,left/seg[i]):0;return [pts[i][0]+(pts[i+1][0]-pts[i][0])*t,pts[i][1]+(pts[i+1][1]-pts[i][1])*t];}left-=seg[i];}
    return pts[0];
  }
  function carriesOf(rack,cable,ctx){
    try{if(ctx.suggest)return ctx.suggest.carries(rack,cable,ctx);}catch(e){}
    return cable.carries==='power'?'power':'data';
  }
  // Rack-coordinate points of one cable, from its first end to its last, as drawn (endpoint ends run out of the exit).
  function cablePoints(rack,cable,ctx){
    const C=ctx.cables,a=C.endAnchor(rack,cable.from,ctx),b=C.endAnchor(rack,cable.to,ctx);
    const flat=p=>p?[p[0],p[2]]:null;
    const guides=(cable.route?.guides||[]).map(id=>list(rack,'guides').find(g=>g.id===id)).filter(Boolean).map(g=>guideAnchor(rack,g));
    const exit=list(rack,'exits').find(e=>e.id===cable.route?.exit)||null;
    const out=exit&&(cable.from?.endpoint||cable.to?.endpoint)?exitAnchor(rack,exit):null;
    const pts=cable.from?.endpoint?[out,...guides,flat(b)]:[flat(a),...guides,cable.to?.endpoint?out:null,cable.to?.endpoint?null:flat(b)];
    return {points:pts.filter(Boolean),exit:out?exit:null,endpoint:cable.from?.endpoint||cable.to?.endpoint||null};
  }
  function elevation(rack,ctx,face,box,s,svg){
    const rackH=rack.slots*U,cx=box.x+box.w/2,top=box.y;
    const X=x=>cx+(face==='rear'?-x:x)*s,Y=z=>top+(rackH-z)*s;
    const out=[];
    out.push(`<text x="${n1(cx)}" y="${n1(top-34)}" text-anchor="middle" font-size="13" fill="${COLORS.ink}" font-weight="bold">${face==='front'?'Front':'Rear (seen from behind)'}</text>`);
    const l=Math.min(X(-POST_X),X(POST_X)),r=Math.max(X(-POST_X),X(POST_X));
    out.push(`<rect x="${n1(l-3)}" y="${n1(Y(rackH))}" width="${n1(r-l+6)}" height="${n1(rackH*s)}" fill="none" stroke="${COLORS.ink}" stroke-width="1"/>`);
    const every=s*U>=10?1:Math.ceil(10/(s*U));
    for(let slot=1;slot<=rack.slots;slot++){
      const yTop=Y((rack.slots-slot+1)*U),yBot=Y((rack.slots-slot)*U);
      if(slot<rack.slots)out.push(`<line x1="${n1(l)}" y1="${n1(yBot)}" x2="${n1(r)}" y2="${n1(yBot)}" stroke="${COLORS.line}" stroke-width="0.4" stroke-dasharray="2 3"/>`);
      if((rack.slots-slot)%every===0)out.push(`<text x="${n1(l-8)}" y="${n1((yTop+yBot)/2+3)}" text-anchor="end" font-size="9" fill="${COLORS.muted}">U${pad(rack.slots-slot+1)}</text>`);
    }
    for(const p of rack.placements||[]){
      const yTop=Y((rack.slots-p.slot+1)*U)+1.5,yBot=Y((rack.slots-p.slot-p.span+1)*U)-1.5,x0=Math.min(X(-104),X(104)),x1=Math.max(X(-104),X(104));
      const item=(ctx.library||[]).find(i=>i.id===p.equipment),name=p.assembly?.name||item?.name||'Equipment',fs=Math.max(7,Math.min(11,(yBot-yTop)*.5));
      out.push(`<rect x="${n1(x0)}" y="${n1(yTop)}" width="${n1(x1-x0)}" height="${n1(Math.max(2,yBot-yTop))}" fill="${COLORS.fill}" stroke="${COLORS.line}" stroke-width="0.6"/>`);
      out.push(`<text x="${n1(x0+4)}" y="${n1(yTop+Math.min(fs+2,(yBot-yTop)/2+fs/2-1))}" font-size="${n1(fs)}" fill="${COLORS.ink}">${esc(clip(name,Math.floor((x1-x0-8)/(fs*.56))))}</text>`);
    }
    for(const x of [-POST_X,POST_X])out.push(`<rect x="${n1(X(x)-2.5)}" y="${n1(Y(rackH))}" width="5" height="${n1(rackH*s)}" fill="${COLORS.line}"/>`);
    const postName=face==='front'?'F':'R';
    for(const [x,side] of [[-POST_X,'L'],[POST_X,'R']])out.push(`<text x="${n1(X(x))}" y="${n1(Y(0)+13)}" text-anchor="middle" font-size="9" fill="${COLORS.muted}">${postName}${side}</text>`);
    for(const g of list(rack,'guides')){if(g.post[0]!==postName)continue;const [gx,gz]=guideAnchor(rack,g);
      out.push(`<rect x="${n1(X(gx)-6)}" y="${n1(Y(gz)-4)}" width="12" height="8" rx="2" fill="${COLORS.guide}"/>`);}
    const tags=[],cables=[];
    for(const cable of svg.cables){
      if(svg.faceOf(cable)!==face)continue;
      const info=cablePoints(rack,cable,ctx),pts=info.points.map(([x,z])=>[X(x),Y(z)]);
      const color=face==='front'?COLORS.patch:COLORS[carriesOf(rack,cable,ctx)]||COLORS.data;
      if(pts.length>=2)cables.push(`<path d="${smooth(pts)}" fill="none" stroke="${color}" stroke-width="2.4" stroke-linecap="round"/>`);
      if(info.exit&&info.endpoint)svg.outside.push({face,exit:info.exit,endpoint:info.endpoint,number:cable.number,X,Y});
      if(!pts.length)continue;
      let [tx,ty]=midpoint(pts);const tw=Math.max(18,String(cable.number).length*6+8);
      while(tags.some(t=>Math.abs(t[0]-tx)<(t[2]+tw)/2+2&&Math.abs(t[1]-ty)<14))ty+=14;
      tags.push([tx,ty,tw]);
      cables.push(`<g><rect x="${n1(tx-tw/2)}" y="${n1(ty-7)}" width="${tw}" height="14" rx="3" fill="#ffffff" stroke="${color}" stroke-width="1"/><text x="${n1(tx)}" y="${n1(ty+3.5)}" text-anchor="middle" font-size="10" font-weight="bold" fill="${COLORS.ink}">${esc(clip(cable.number,12))}</text></g>`);
    }
    out.push(...cables);
    if(face==='rear')for(const e of list(rack,'exits')){const [ex,ez]=exitAnchor(rack,e),px=X(ex),py=Y(ez);
      out.push(`<circle cx="${n1(px)}" cy="${n1(py)}" r="6" fill="#ffffff" stroke="${COLORS.ink}" stroke-width="1.2"/><circle cx="${n1(px)}" cy="${n1(py)}" r="2.2" fill="${COLORS.ink}"/>`);
      const below=e.position!=='top-rear';
      out.push(`<text x="${n1(px+9)}" y="${n1(py+(below?14:-8))}" font-size="9" fill="${COLORS.muted}">Exit · ${esc(exitLabel(e))}</text>`);}
    return out.join('');
  }
  // Outside endpoints: one box per endpoint under the rear elevation, with an arrow from each exit that serves it.
  function endpointsRow(rack,svg,box){
    const out=[],eps=list(rack,'endpoints'),used=new Map();
    for(const o of svg.outside){const k=o.endpoint;if(!used.has(k))used.set(k,{numbers:[],exits:new Map()});const u=used.get(k);u.numbers.push(o.number);u.exits.set(o.exit.id,o);}
    let x=box.x,y=box.y;const placed=[];
    for(const ep of eps){const u=used.get(ep.id);if(!u)continue;
      const text=clip(ep.name,30)+' · '+u.numbers.join(', '),w=Math.min(box.w,text.length*5.6+16);
      if(x+w>box.x+box.w&&x>box.x){x=box.x;y+=30;}
      placed.push({ep,u,x,y,w,text});x+=w+10;}
    for(const p of placed){
      for(const o of p.u.exits.values()){const [ex,ez]=exitAnchor(rack,o.exit),[dx,dz]=exitOut(o.exit),sx=o.X(ex+dx*14),sy=o.Y(ez+dz*14);
        // Bottom exits point straight at the box; top and side exits go round the outside of the rack, not across it.
        const cx=o.X(0),xm=cx+(o.X(ex)>=cx?1:-1)*(POST_X*Math.abs(o.X(1)-cx)+38),via=o.exit.position==='bottom-rear'?'':` L${n1(xm)} ${n1(sy)} L${n1(xm)} ${n1(p.y-14)}`;
        out.push(`<path d="M${n1(sx)} ${n1(sy)}${via} L${n1(p.x+p.w/2)} ${n1(p.y-3)}" fill="none" stroke="${COLORS.muted}" stroke-width="0.9" stroke-dasharray="4 3" marker-end="url(#ah)"/>`);}
      out.push(`<rect x="${n1(p.x)}" y="${n1(p.y)}" width="${n1(p.w)}" height="20" rx="4" fill="#ffffff" stroke="${COLORS.ink}" stroke-width="0.8"/><text x="${n1(p.x+p.w/2)}" y="${n1(p.y+13.5)}" text-anchor="middle" font-size="9.5" fill="${COLORS.ink}">${esc(p.text)}</text>`);
    }
    return out.join('');
  }
  // The wiring sheet as one landscape SVG. ctx = {ports, cables, suggest?, sheet, library}; opts = {stamp}.
  function sheetSvg(rack,ctx,opts={}){
    const S=ctx.sheet,cables=S.sortCables(rack),rackH=rack.slots*U;
    const svg={cables,outside:[],faceOf:c=>S.faceOf(rack,c,ctx)};
    const s=Math.min(1.1,420/(rackH+30));
    const out=[`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="Arial, Helvetica, sans-serif">`,
      `<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="${COLORS.muted}" stroke-width="1.5"/></marker></defs>`,
      `<rect width="${W}" height="${H}" fill="#ffffff"/>`,
      `<text x="24" y="32" font-size="17" font-weight="bold" fill="${COLORS.ink}">${esc(clip(rack.name||'Rack',60))} · wiring sheet</text>`,
      `<text x="${W-24}" y="32" text-anchor="end" font-size="10" fill="${COLORS.muted}">${esc(opts.stamp||'')}</text>`,
      `<text x="24" y="48" font-size="10" fill="${COLORS.muted}">${rack.slots}U rack · ${cables.length} cable${cables.length===1?'':'s'} · planning document, not a fit or capacity check</text>`];
    out.push(elevation(rack,ctx,'front',{x:30,y:110,w:300},s,svg));
    out.push(elevation(rack,ctx,'rear',{x:350,y:110,w:300},s,svg));
    out.push(endpointsRow(rack,svg,{x:350,y:Math.min(570,110+rackH*s+46),w:310}));
    // Right column: legend, then the notes box.
    const lx=690;let y=86;
    out.push(`<text x="${lx}" y="${y}" font-size="12" font-weight="bold" fill="${COLORS.ink}">Legend</text>`);y+=18;
    for(const [label,color] of [['Power',COLORS.power],['Data',COLORS.data],['Front patch cord',COLORS.patch]]){out.push(`<line x1="${lx}" y1="${y-4}" x2="${lx+22}" y2="${y-4}" stroke="${color}" stroke-width="2.4" stroke-linecap="round"/><text x="${lx+30}" y="${y}" font-size="10" fill="${COLORS.ink}">${label}</text>`);y+=16;}
    out.push(`<rect x="${lx+5}" y="${y-8}" width="12" height="8" rx="2" fill="${COLORS.guide}"/><text x="${lx+30}" y="${y}" font-size="10" fill="${COLORS.ink}">Cable guide on a post (FL, FR, RL, RR)</text>`);y+=16;
    out.push(`<circle cx="${lx+11}" cy="${y-4}" r="5" fill="#ffffff" stroke="${COLORS.ink}" stroke-width="1.2"/><text x="${lx+30}" y="${y}" font-size="10" fill="${COLORS.ink}">Exit point (marker only, no hole in any STL)</text>`);y+=16;
    out.push(`<rect x="${lx+2}" y="${y-10}" width="18" height="12" rx="3" fill="#ffffff" stroke="${COLORS.ink}" stroke-width="0.8"/><text x="${lx+30}" y="${y}" font-size="10" fill="${COLORS.ink}">Outside endpoint, with its cables</text>`);y+=16;
    out.push(`<text x="${lx}" y="${y+2}" font-size="9" fill="${COLORS.muted}">Lines are routes, not to scale; see the schedule for lengths.</text>`);y+=28;
    const notesTop=y-14,notesBottom=640;
    out.push(`<text x="${lx+10}" y="${y+4}" font-size="12" font-weight="bold" fill="${COLORS.ink}">Notes</text>`);y+=22;
    const limits=wrap(S.LIMITS,52),room=Math.floor((notesBottom-12-limits.length*13-8-y)/13);
    const lines=[];for(const n of S.notes(rack,ctx))for(const [i,t] of wrap(n.number+' · '+n.text,52).entries())lines.push({t,indent:i>0,n});
    let shown=lines;
    // Too many: keep whole notes only and point to the CSV for the rest.
    if(lines.length>room){shown=lines.slice(0,Math.max(0,room-1));while(shown.length&&lines[shown.length]?.indent)shown.pop();}
    if(!lines.length)shown=[{t:'No open cable warnings.',indent:false}];
    for(const l of shown){out.push(`<text x="${lx+10+(l.indent?10:0)}" y="${y}" font-size="10" fill="${COLORS.ink}">${esc(l.t)}</text>`);y+=13;}
    if(lines.length>shown.length&&lines.length){const rest=new Set(lines.slice(shown.length).map(l=>l.n)).size;out.push(`<text x="${lx+10}" y="${y}" font-size="10" fill="${COLORS.muted}">+ ${rest} more: see the Warnings column in the schedule CSV.</text>`);y+=13;}
    y=notesBottom-12-limits.length*13+10;
    for(const t of limits){out.push(`<text x="${lx+10}" y="${y}" font-size="10" font-weight="bold" fill="${COLORS.ink}">${esc(t)}</text>`);y+=13;}
    out.push(`<rect x="${lx}" y="${notesTop}" width="290" height="${notesBottom-notesTop}" rx="4" fill="none" stroke="${COLORS.line}" stroke-width="0.8"/>`);
    out.push(`<text x="24" y="${H-18}" font-size="9" fill="${COLORS.muted}">Made from the saved rack only; unsaved changes are never included. Cable numbers match the schedule CSV and the wrap labels. Personal planning use.</text>`);
    out.push('</svg>');
    return out.join('');
  }
  const pageStyle=(paper,orientation)=>{const p=PAPER[paper]||PAPER.letter,w=orientation==='landscape'?p.w:p.h,h=orientation==='landscape'?p.h:p.w;
    return `@page{size:${p.css} ${orientation};margin:10mm}*{box-sizing:border-box}body{margin:0;background:#e9edf1;color:${COLORS.ink};font-family:Arial,Helvetica,sans-serif}`+
      `.bar{display:flex;gap:12px;align-items:center;flex-wrap:wrap;padding:10px 16px;background:#1d2733;color:#fff;font-size:13px}.bar button{font:inherit;padding:6px 12px;border-radius:6px;border:0;cursor:pointer}`+
      `.page{width:${w-20}mm;height:${h-20}mm;margin:12px auto;background:#fff;padding:0;overflow:hidden;break-after:page;page-break-after:always}.page:last-child{break-after:auto;page-break-after:auto}`+
      `@media screen{.page{box-shadow:0 0 0 10mm #fff,0 2px 12px 10mm rgba(0,0,0,.18);margin:calc(12px + 10mm) auto}}`+
      `@media print{body{background:#fff}.bar{display:none}.page{margin:0;box-shadow:none}}`;};
  const bar=(paper,orientation,what)=>`<div class="bar"><button type="button" onclick="window.print()">Print or save as PDF</button><span>${esc(what)} · ${esc((PAPER[paper]||PAPER.letter).label)} ${orientation}. Planning document: lengths are estimates; fit and capacity UNKNOWN.</span></div>`;
  // Print-ready sheet page; images = [{label, src}] adds the 3D views page (decision 5).
  function sheetPage({svg,title,paper='letter',images=null}){
    const html=[`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><style>${pageStyle(paper,'landscape')}`,
      `.page svg{display:block;width:100%;height:100%}.views{display:flex;flex-direction:column;height:100%;padding:6mm}.views h2{margin:0 0 2mm;font-size:15pt}.views p{margin:0 0 4mm;font-size:9pt;color:${COLORS.muted}}`,
      `.views .row{flex:1;display:flex;gap:6mm;min-height:0}.views figure{flex:1;margin:0;display:flex;flex-direction:column;min-height:0}.views img{flex:1;min-height:0;width:100%;object-fit:contain;background:#151c26;border-radius:2mm}.views figcaption{font-size:10pt;font-weight:bold;margin-top:2mm;text-align:center}</style></head><body>`,
      bar(paper,'landscape','Wiring sheet'),`<div class="page">${svg.replace(/ width="\d+" height="\d+"/,'')}</div>`];
    if(images&&images.length)html.push(`<div class="page"><div class="views"><h2>3D views · Cables mode</h2><p>Snapshots of the app's 3D preview with cable numbers. Not to scale and not a fit check. They include local preview models for personal planning use only.</p><div class="row">`,
      ...images.map(i=>`<figure><img alt="${esc(i.label)} 3D view" src="${esc(i.src)}"><figcaption>${esc(i.label)}</figcaption></figure>`),'</div></div></div>');
    html.push('</body></html>');return html.join('');
  }
  // Print-ready wrap labels, one per cable end (decision 7), cut along the dashes.
  function labelsPage({labels,title,paper='letter',heading=''}){
    const cells=labels.length?labels.map(l=>`<div class="label"><div class="t">${esc(l.text)}</div><div class="s">${esc(l.sub)}</div></div>`).join(''):'<p>No connected cable ends to label yet.</p>';
    return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><style>${pageStyle(paper,'portrait')}`+
      `.page{height:auto;min-height:0;overflow:visible}.head{font-size:9pt;color:${COLORS.muted};margin:0 0 4mm}.grid{display:grid;grid-template-columns:repeat(3,1fr)}`+
      `.label{height:20mm;border:0.3mm dashed #7d8894;margin:-0.15mm;padding:2.5mm 3mm;display:flex;flex-direction:column;justify-content:center;break-inside:avoid;page-break-inside:avoid}`+
      `.label .t{font:bold 10pt ui-monospace,Consolas,monospace;line-height:1.2;max-height:2.4em;overflow:hidden;overflow-wrap:anywhere}.label .s{font-size:7.5pt;color:${COLORS.muted};margin-top:1mm;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}</style></head><body>`+
      bar(paper,'portrait','Cable labels')+`<div class="page"><p class="head">${esc(heading)}</p><div class="grid">${cells}</div></div></body></html>`;
  }
  const api={PAPER,COLORS,safeName,cablePoints,sheetSvg,sheetPage,labelsPage};
  root.LabRaxCableSheetView=api;if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(globalThis);
