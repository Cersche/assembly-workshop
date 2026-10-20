const fs=require('fs'),vm=require('vm'),assert=require('assert');
const source=fs.readFileSync('outputs/Mechanical_Design_App/viewer.js','utf8').split('async function initAssemblyViewer')[0];
const context={};vm.createContext(context);vm.runInContext(source,context);
const triangle=(depth,color)=>({points:[[-4,-4,depth[0]],[4,-4,depth[1]],[0,4,depth[2]]],color});
const red=triangle([0,0,0],[255,0,0]),blue=triangle([-2,2,0],[0,0,255]);
function render(faces){return context.rasterizeAssemblyFaces(faces,12,12,1,{data:new Uint8ClampedArray(12*12*4)}).data}
const first=render([red,blue]),second=render([blue,red]);
assert.deepStrictEqual(first,second,'Crossing surfaces must be independent of triangle order');
function pixel(x,y){return Array.from(first.slice((y*12+x)*4,(y*12+x)*4+3))}
assert.deepStrictEqual(pixel(4,8),[255,0,0]);assert.deepStrictEqual(pixel(7,8),[0,0,255]);
const reverse={...blue,points:[...blue.points].reverse()};assert.deepStrictEqual(render([red,reverse]),first,'Both triangle windings supported');
assert.doesNotThrow(()=>render([{points:[[1,1,0],[1,1,0],[1,1,0]],color:[0,0,0]}]));
assert.doesNotThrow(()=>render([triangle([0,0,0],[1,2,3]),{points:[[-100,-100,0],[100,-100,0],[0,100,0]],color:[2,3,4]}]));
console.log('PASS: crossing-surface occlusion, order independence, winding, degenerate and viewport clipping.');
