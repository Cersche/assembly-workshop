(function(root){
  'use strict';
  const unknown='__unknown__';
  const value=v=>v===undefined||v===null||v===''?null:v;
  function filter(parts,c){
    let selected=parts;
    if(c.latest){
      const revisions=new Map();
      parts.forEach(p=>revisions.set(p.id,Math.max(revisions.get(p.id)||0,p.revision)));
      selected=parts.filter(p=>p.revision===revisions.get(p.id));
    }
    return selected.filter(p=>{
      if(c.q&&!JSON.stringify(p).toLowerCase().includes(c.q.toLowerCase()))return false;
      if(c.kind&&p.kind!==c.kind)return false;
      for(const k of ['diameter','pitch'])if(c[k]!==''&&c[k]!==undefined&&Number(c[k])!==p[k])return false;
      for(const k of ['head_style','material','installation_method']){
        if(c[k]===unknown&&value(p[k])!==null)return false;
        if(c[k]&&c[k]!==unknown&&p[k]!==c[k])return false;
      }
      const min=c.min_length,max=c.max_length;
      if(min!==''&&min!==undefined&&(value(p.length)===null||p.length<Number(min)))return false;
      if(max!==''&&max!==undefined&&(value(p.length)===null||p.length>Number(max)))return false;
      return true;
    });
  }
  const effects={diameter:'Thread compatibility, bore and joint sizing',pitch:'Thread compatibility and engagement',length:'Screw reach or insert pocket depth',length_convention:'Reach calculation',threaded_length:'Threaded shank clearance',head_diameter:'Head clearance',head_height:'Head clearance',head_style:'Bearing/head geometry',drive:'Driver access',outside_diameter:'Insert envelope and boss wall',hole_diameter:'Installation hole',hole_diameter_tolerance_mm:'Installation hole range',hole_profile:'Installation hole geometry',usable_depth:'Engagement and bottoming',min_wall:'Boss wall',end_type:'Bottoming and screw-tip space',material:'Material/process suitability',finish:'Surface/material suitability',installation_method:'Installation process and access'};
  function changes(before,after){
    if(!after)return [];
    const fields=['id','revision',...Object.keys(effects),'installation_hole_segments','manufacturer_installation_evidence','installation_evidence_resolution','unknown_fields','field_sources','source_document','redistribution_status','pilot_diameter_mm','recommended_hole_entrance_diameter_mm','recommended_hole_entrance_tolerance_mm','hole_included_angle_degrees','dimensional_tolerances','manufacturing_standard','verification','source'];
    return fields.flatMap(field=>{
      const previous=value(before?.[field]),next=value(after[field]);
      if(JSON.stringify(previous)===JSON.stringify(next))return [];
      return [{field,before:previous,after:next,effect:effects[field]||(['pilot_diameter_mm','recommended_hole_entrance_diameter_mm','recommended_hole_entrance_tolerance_mm','hole_included_angle_degrees'].includes(field)?'Insert and installation-hole geometry':field==='dimensional_tolerances'?'Dimension and clearance bounds':'Pinned identity or source evidence')}];
    });
  }
  const api={filter,changes,unknown};root.WorkshopCatalog=api;
  if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
