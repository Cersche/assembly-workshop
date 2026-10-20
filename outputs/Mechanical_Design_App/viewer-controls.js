// Shared canvas input. Offsets are CSS pixels; cameras remain owned by each viewer.
(function(root){
  'use strict';
  const bindings=new WeakMap();
  const action=button=>button===0?'orbit':button===1||button===2?'pan':null;
  const moved=(a,b)=>Math.hypot(b.x-a.x,b.y-a.y)>4;
  function zoomAt(v,z,x,y){
    const ratio=z/v.zoom;
    return {...v,zoom:z,panX:x-(x-(v.panX||0))*ratio,panY:y-(y-(v.panY||0))*ratio};
  }
  // Apply the same screen transform to GPU projection, labels and picking rays.
  function camera(view,w,h,v){
    const z=v.zoom,px=v.panX||0,py=v.panY||0,m=new Float32Array(view.matrix);
    for(let i=0;i<4;i++){m[i*4]=view.matrix[i*4]*z+2*px/w*view.matrix[i*4+3];m[i*4+1]=view.matrix[i*4+1]*z-2*py/h*view.matrix[i*4+3];}
    return {...view,matrix:m,project:p=>{const q=view.project(p);return [w/2+(q[0]-w/2)*z+px,h/2+(q[1]-h/2)*z+py,q[2]];},
      ray:(x,y)=>view.ray(w/2+(x-w/2-px)/z,h/2+(y-h/2-py)/z)};
  }
  function attach(canvas,options){
    if(bindings.has(canvas)){bindings.get(canvas).options=options;return;}
    const state={options,points:new Map(),hover:false};bindings.set(canvas,state);
    const doc=canvas.ownerDocument;
    canvas.tabIndex=0;canvas.style.touchAction='none';
    canvas.title='Left drag: orbit · Right/middle drag: pan · Wheel: zoom at cursor · Z: fit · 0–7: views';
    const get=()=>state.options.getView(),set=v=>{state.options.setView(v);state.options.redraw();};
    const point=e=>({x:e.clientX,y:e.clientY});
    const zoom=(factor,p)=>{
      const rect=canvas.getBoundingClientRect(),v=get();
      const z=Math.max(state.options.minZoom||.1,Math.min(state.options.maxZoom||10,v.zoom*factor));
      set(zoomAt(v,z,p.x-rect.left-rect.width/2,p.y-rect.top-rect.height/2));
    };
    const preset=name=>{
      const v=state.options.presets?.[name];if(v){state.options.onPreset?.(name);set({...get(),...v,panX:0,panY:0});}
    };
    const fit=()=>{if(state.options.fit)state.options.fit();else set({...get(),zoom:1,panX:0,panY:0});};
    canvas.addEventListener('pointerenter',()=>state.hover=true);
    canvas.addEventListener('pointerleave',()=>state.hover=false);
    canvas.addEventListener('contextmenu',e=>e.preventDefault());
    canvas.addEventListener('pointerdown',e=>{
      if(!action(e.button))return;e.preventDefault();canvas.focus({preventScroll:true});
      const p=point(e);state.points.set(e.pointerId,{...p,start:p,button:e.button,moved:false});
      if(state.points.size>1)for(const p of state.points.values())p.moved=true;
      canvas.setPointerCapture(e.pointerId);
    });
    canvas.addEventListener('pointermove',e=>{
      const p=state.points.get(e.pointerId);if(!p)return;
      const next=point(e),all=[...state.points.values()];
      if(all.length>2)return;
      if(all.length===2){
        const other=all.find(q=>q!==p),oldDistance=Math.hypot(p.x-other.x,p.y-other.y),distance=Math.hypot(next.x-other.x,next.y-other.y);
        if(oldDistance>0)zoom(distance/oldDistance,{x:(p.x+other.x)/2,y:(p.y+other.y)/2});
        const v=get();set({...v,panX:(v.panX||0)+(next.x-p.x)/2,panY:(v.panY||0)+(next.y-p.y)/2});
      }else{
        p.moved=p.moved||moved(p.start,next);if(!p.moved)return;
        const dx=next.x-p.x,dy=next.y-p.y,v=get();
        if(action(p.button)==='pan')set({...v,panX:(v.panX||0)+dx,panY:(v.panY||0)+dy});
        else{state.options.onOrbit?.();set({...get(),yaw:v.yaw+dx*.008,pitch:Math.max(-Math.PI/2,Math.min(Math.PI/2,v.pitch+dy*.008))});}
      }
      Object.assign(p,next);
    });
    canvas.addEventListener('pointerup',e=>{
      const p=state.points.get(e.pointerId);state.points.delete(e.pointerId);
      if(p&&!p.moved&&!moved(p.start,point(e))){if(p.button===0)state.options.onClick?.(e);if(p.button===2)state.options.onRightClick?.(e);}
      if(canvas.hasPointerCapture(e.pointerId))canvas.releasePointerCapture(e.pointerId);
    });
    const cancel=e=>state.points.delete(e.pointerId);
    canvas.addEventListener('pointercancel',cancel);canvas.addEventListener('lostpointercapture',cancel);
    canvas.addEventListener('wheel',e=>{e.preventDefault();zoom(Math.exp(-e.deltaY*(e.deltaMode===1?.016:e.deltaMode===2?.4:.001)),point(e));},{passive:false});
    // One document listener per document; detached wizard canvases are not retained.
    if(!doc.__viewerControlsKeys){
      doc.__viewerControlsKeys=true;
      doc.addEventListener('keydown',e=>{
        if(e.target?.closest?.('input,textarea,select,[contenteditable]:not([contenteditable="false"])')||e.altKey||e.metaKey)return;
        const canvases=[...doc.querySelectorAll('canvas')];
        const cv=canvases.find(c=>bindings.get(c)?.hover)||canvases.find(c=>c===doc.activeElement);
        bindings.get(cv)?.key(e);
      });
    }
    state.key=e=>{
      const names=['iso','top','bottom','front','rear','left','right','iso'];
      if(e.key.toLowerCase()==='z'&&!e.ctrlKey){e.preventDefault();fit();}
      else if(/^[0-7]$/.test(e.key)){e.preventDefault();preset(names[+e.key]);}
    };
    if(state.options.toolbar!==false){
      const bar=doc.createElement('div');bar.className='viewer-controls';bar.setAttribute('role','group');bar.setAttribute('aria-label','Camera views');
      for(const [label,name] of [['Iso','iso'],['Top','top'],['Front','front'],['Fit','fit']]){
        const b=doc.createElement('button');b.type='button';b.textContent=label;b.onclick=()=>name==='fit'?fit():preset(name);bar.appendChild(b);
      }
      canvas.after(bar);
    }
  }
  const presets={iso:{yaw:-.55,pitch:.55,zoom:1},top:{yaw:0,pitch:Math.PI/2,zoom:1},bottom:{yaw:0,pitch:-Math.PI/2,zoom:1},
    front:{yaw:0,pitch:0,zoom:1},rear:{yaw:Math.PI,pitch:0,zoom:1},left:{yaw:Math.PI/2,pitch:0,zoom:1},right:{yaw:-Math.PI/2,pitch:0,zoom:1}};
  root.ViewerControls={attach,action,moved,zoomAt,camera,presets};
  if(typeof module!=='undefined')module.exports=root.ViewerControls;
})(typeof window==='undefined'?globalThis:window);
