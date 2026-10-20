const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'../..'),assets=path.join(root,'outputs/Mechanical_Design_App/rack-references');
const studio=require(path.join(assets,'rack-studio.js')),scene=require(path.join(assets,'rack-scene.js'));
const mesh=JSON.parse(fs.readFileSync(path.join(assets,'component_1_23.json'),'utf8')),logo=JSON.parse(fs.readFileSync(path.join(assets,'rack-logo-faces.json'),'utf8'));
const original=JSON.stringify(mesh),split=studio.logoMeshes({...mesh,logo_faces:logo.triangles});
assert.equal(split.logo.triangles.length,448);assert.equal(split.body.triangles.length+split.logo.triangles.length,mesh.triangles.length);
assert.equal(split.logo.vertices,mesh.vertices);assert.equal(split.body.vertices,mesh.vertices);assert.equal(JSON.stringify(mesh),original);
const partitions=new Set([...split.logo.triangles,...split.body.triangles]);assert.equal(partitions.size,mesh.triangles.length);
assert.throws(()=>studio.logoMeshes({...mesh,logo_faces:[-1]}));
const meshes={};for(const [key,[r,id]] of Object.entries(scene.sources))if(key!=='extension')meshes[key]=JSON.parse(fs.readFileSync(path.join(assets,`component_${r}_${id}.json`),'utf8'));
meshes.beam_top_front={...mesh,logo_faces:logo.triangles};
const renderer=Object.create(studio.Renderer.prototype);renderer.logoCache=new WeakMap();renderer.geometry=studio.equipment();
for(const slots of [1,5,6,48])for(const visible of [true,false]){
 const frame=scene.frame(slots),rack={slots,placements:[],appearance:{logo_color:'#ff0000',post_labels:visible}},objects=renderer.objects(frame,meshes,rack);
 assert.deepEqual(objects.find(o=>o.key==='beam_top_front-logo').color,[1,0,0]);
 assert.equal(objects.reduce((s,o)=>s+o.mesh.triangles.length,0),frame.parts.reduce((s,p)=>s+meshes[p.key].triangles.length,0));
 assert.equal(objects.filter(o=>o.postLabels).length,visible?frame.levels.length*2:0);
 for(const o of objects.filter(o=>o.postLabels))assert.equal(o.rackSlots,slots);
}
console.log('PASS original logo partition, unchanged source geometry/counts, independent color and post toggles at1/5/6/48U');
