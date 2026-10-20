// Logical allocation edits only. Never changes hardware, meshes, or fit status.
(function(root){
  'use strict';
  function checkRange(rack,start,span,ignoreId=null){
    if(!Number.isInteger(start)||!Number.isInteger(span)||start<1||span<1||start+span-1>rack.slots)throw Error('Choose a whole slot range within the rack.');
    if(rack.placements.some(p=>p.id!==ignoreId&&start<p.slot+p.span&&p.slot<start+span))throw Error('That allocation overlaps another assembly.');
  }
  function change(rack,id,start,span){
    const old=rack.placements.find(p=>p.id===id);if(!old)throw Error('This allocation is no longer available.');
    checkRange(rack,start,span,id);
    const updated={...old,slot:start,span,fit:'UNKNOWN'};
    rack.placements=rack.placements.map(p=>p.id===id?updated:p);return updated;
  }
  function release(rack,id){
    const index=rack.placements.findIndex(p=>p.id===id);if(index<0)throw Error('This allocation is no longer available.');
    const record={rackId:rack.id,index,item:{...rack.placements[index]}};
    rack.placements=rack.placements.filter(p=>p.id!==id);return record;
  }
  function restore(rack,record){
    if(!record||record.rackId!==rack.id)throw Error('Open the original rack to restore this allocation.');
    if(rack.placements.some(p=>p.id===record.item.id))throw Error('This allocation is already present.');
    checkRange(rack,record.item.slot,record.item.span);
    const item={...record.item,fit:'UNKNOWN'};rack.placements.splice(Math.min(record.index,rack.placements.length),0,item);return item;
  }
  const api={checkRange,change,release,restore};if(typeof module!=='undefined'&&module.exports)module.exports=api;root.RackLayout=api;
})(typeof window==='undefined'?globalThis:window);
