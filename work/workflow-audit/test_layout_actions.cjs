const assert=require('assert'),fs=require('fs'),vm=require('vm');
const A=require('../../outputs/Mechanical_Design_App/rack-references/rack-layout.js');
const p=(id,slot,span=1)=>({id,equipment:'pi4',slot,span,fit:'UNKNOWN',geometry:'pi4-clearance-v2-reference'});
const rack={id:'r',slots:5,placements:[p('one',1),p('two',2,2)]};
const before=JSON.stringify(rack);assert.throws(()=>A.change(rack,'two',1,2),/overlaps/);assert.equal(JSON.stringify(rack),before);
assert.throws(()=>A.change(rack,'two',5,2),/within/);assert.equal(JSON.stringify(rack),before);
A.change(rack,'two',4,2);assert.equal(rack.placements[1].slot,4);
const record=A.release(rack,'two');assert.equal(rack.placements.length,1);A.restore(rack,record);assert.equal(rack.placements[1].slot,4);
A.release(rack,'two');rack.slots=3;assert.throws(()=>A.restore(rack,record),/within/);assert.equal(rack.placements.length,1);
rack.slots=5;rack.placements.push(p('other',5));assert.throws(()=>A.restore(rack,record),/overlaps/);assert.equal(rack.placements.length,2);
// Saving moved to the unified atomic controller; its actual handler is checked here.
require('../gui-refinement/test_save.cjs');
