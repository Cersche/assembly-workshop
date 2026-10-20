// Cable drawing for the rack view (cable management Step 3): smooth tubes with slight sag, side by side through guides,
// and grommet markers for exit points. Preview only: nothing here is geometry for any STL. Diameters are nominal display sizes.
(function(root){
  'use strict';
  const sub=(a,b)=>a.map((v,i)=>v-b[i]),add=(a,b)=>a.map((v,i)=>v+b[i]),scale=(a,s)=>a.map(v=>v*s);
  const dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2],len=a=>Math.hypot(a[0],a[1],a[2]);
  const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
  const unit=a=>{const l=len(a)||1;return a.map(v=>v/l);};
  // Exit grommet facing: outward normal of the opening for each exit position.
  const EXIT_NORMAL={'bottom-rear':[0,0,-1],'top-rear':[0,0,1],left:[-1,0,0],right:[1,0,0]};
  // Offsets so cables sharing a guide lie side by side (along X, centred on the guide) instead of overlapping.
  // runs = [{id, guides:[ids], diameter}] -> {cableId: {guideId: offsetX}}
  function bundleOffsets(runs,gap=1.5){
    const by={},out={};
    for(const r of runs)for(const g of r.guides||[])(by[g]=by[g]||[]).push(r);
    for(const [g,list] of Object.entries(by)){
      const sorted=[...list].sort((a,b)=>String(a.id).localeCompare(String(b.id))),width=sorted.reduce((s,r)=>s+r.diameter+gap,0)-gap;
      let x=-width/2;for(const r of sorted){(out[r.id]=out[r.id]||{})[g]=x+r.diameter/2;x+=r.diameter+gap;}
    }
    return out;
  }
  // Densify a route polyline with a gentle downward sag between consecutive points (parabola, deepest mid-span).
  // Sag = 4% of the horizontal span, at most 25 mm; vertical runs barely sag.
  function sagPath(points,steps=10){
    if(points.length<2)return points.slice();const out=[points[0]];
    for(let i=0;i+1<points.length;i++){const a=points[i],b=points[i+1],span=Math.hypot(b[0]-a[0],b[1]-a[1]),sag=Math.min(25,span*.04);
      for(let k=1;k<=steps;k++){const t=k/steps,p=add(a,scale(sub(b,a),t));p[2]-=sag*4*t*(1-t);out.push(p);}}
    return out;
  }
  // Tube along a polyline with parallel-transport frames, closed end caps. Returns {vertices, triangles, normals}.
  function tubeMesh(points,radius,sides=10){
    const pts=points.filter((p,i)=>i===0||len(sub(p,points[i-1]))>1e-6),mesh={vertices:[],triangles:[],normals:[]};
    if(pts.length<2)return mesh;
    const tangents=pts.map((p,i)=>unit(sub(pts[Math.min(i+1,pts.length-1)],pts[Math.max(i-1,0)])));
    let normal=unit(cross(tangents[0],Math.abs(tangents[0][2])<.9?[0,0,1]:[1,0,0]));
    const rings=[];
    pts.forEach((p,i)=>{
      if(i){const t0=tangents[i-1],t1=tangents[i],axis=cross(t0,t1),s=len(axis);
        if(s>1e-8){const k=unit(axis),c=Math.max(-1,Math.min(1,dot(t0,t1))),sin=Math.sqrt(1-c*c);
          // Rodrigues rotation of the frame normal from t0 to t1.
          normal=add(add(scale(normal,c),scale(cross(k,normal),sin)),scale(k,dot(k,normal)*(1-c)));}
        normal=unit(sub(normal,scale(t1,dot(normal,t1))));}
      const binormal=cross(tangents[i],normal),ring=[];
      for(let j=0;j<sides;j++){const a=j/sides*Math.PI*2,n=add(scale(normal,Math.cos(a)),scale(binormal,Math.sin(a)));ring.push(mesh.vertices.length);mesh.vertices.push(add(p,scale(n,radius)));mesh.normals.push(n);}
      rings.push(ring);
    });
    for(let i=0;i+1<rings.length;i++)for(let j=0;j<sides;j++){const a=rings[i][j],b=rings[i][(j+1)%sides],c=rings[i+1][(j+1)%sides],d=rings[i+1][j];mesh.triangles.push([a,b,c],[a,c,d]);}
    for(const [ring,p,t,flip] of [[rings[0],pts[0],tangents[0],true],[rings.at(-1),pts.at(-1),tangents.at(-1),false]]){
      const centre=mesh.vertices.length;mesh.vertices.push(p);mesh.normals.push(flip?scale(t,-1):t);
      for(let j=0;j<sides;j++){const a=ring[j],b=ring[(j+1)%sides];mesh.triangles.push(flip?[centre,b,a]:[centre,a,b]);}}
    return mesh;
  }
  // Grommet: a 3 mm thick ring (Ø24 outside, Ø14 opening) facing local −Y, built with LabRaxStudio.slab.
  function grommetMesh(S){
    const ring=(r,n)=>Array.from({length:n},(_,i)=>[r*Math.cos(i*Math.PI*2/n),r*Math.sin(i*Math.PI*2/n)]);
    const m=new S.Mesh();S.slab(m,ring(12,40),[ring(7,32)],-3,0,(x,z,y)=>[x,y,z]);return m;
  }
  // Row-major rotation turning the grommet's −Y onto the exit's outward normal.
  function exitRotation(position){
    switch(position){
      case 'bottom-rear':return [1,0,0,0,0,-1,0,1,0];
      case 'top-rear':return [1,0,0,0,0,1,0,-1,0];
      case 'left':return [0,1,0,-1,0,0,0,0,1];
      case 'right':return [0,-1,0,1,0,0,0,0,1];
      default:return [1,0,0,0,1,0,0,0,1];
    }
  }
  // A short stable key for a tube's geometry, so the renderer's per-key GPU buffer cache never reuses a stale shape.
  function geometryKey(points,radius){let h=2166136261;const s=points.map(p=>p.map(v=>v.toFixed(1)).join(',')).join(';')+'|'+radius;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619);}return (h>>>0).toString(36);}
  const api={EXIT_NORMAL,bundleOffsets,sagPath,tubeMesh,grommetMesh,exitRotation,geometryKey};
  root.LabRaxCableView=api;if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(typeof window==='undefined'?globalThis:window);
