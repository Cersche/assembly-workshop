from pathlib import Path
import json,hashlib
app=Path(r'D:\Projects\assembly-workshop\outputs\Mechanical_Design_App')
p=app/'equipment.py';t=p.read_text(encoding='utf-8').replace("r'// @wall-begin\\n.*?// @wall-end\\n'","r'// @wall-begin\\n.*?// @wall-end\\n\\n'")
p.write_text(t,encoding='utf-8',newline='\n')
# Pair checks must use the final shared joints, not an individual tray's earlier joint positions.
p=app/'tray-placement.js';t=p.read_text(encoding='utf-8').replace('function problems(spec,v){','function problems(spec,v,pair=false){').replace('const wp=wallProblem(spec,v);','const wp=pair?\'\':wallProblem(spec,v);')
# UI first-device checks are shared with pair checks below.
t=t.replace('TrayPlacement.problems(', 'TrayPlacement.problems(')
p.write_text(t,encoding='utf-8',newline='\n')
p=app/'tray-pair.js';t=p.read_text(encoding='utf-8').replace('T().problems(spec2,m)','T().problems(spec2,m,true)');p.write_text(t,encoding='utf-8',newline='\n')
tests='''import unittest,json,hashlib
from pathlib import Path
import equipment as eq

class WallTests(unittest.TestCase):
    def raw(self, **kw):
        return dict(dict(name='Wall test',dev_w=90.7,dev_d=90.4,dev_h=25.4,device_mount='wall',joint='screw',dev_off_y=2),**kw)

    def test_accepted_floor_and_round_trip(self):
        s=eq.clean(self.raw())
        self.assertEqual(s['wall_open'],['rear'])
        self.assertEqual(eq.clean(s),s)
        self.assertEqual(eq.device_lift(s),11.225)
        self.assertEqual(eq.placement_settings({'wall_open':['right','rear']}),{'wall_open':['rear','right']})
        self.assertEqual(eq.PAIR_REACH['wall'],2.5)

    def test_bad_sides_and_height(self):
        for sides in ([],['front','rear','left','right'],['back'],'rear',[None],None):
            with self.subTest(sides=sides),self.assertRaisesRegex(ValueError,'Open sides'):
                eq.clean(self.raw(wall_open=sides))
        with self.assertRaisesRegex(ValueError,'taller than 2'):eq.clean(self.raw(dev_h=2))

    def test_clash_actual_returns_and_rotations(self):
        for rot in (0,90,180,270):
            with self.subTest(rot=rot),self.assertRaisesRegex(ValueError,'wall would hit'):
                eq.clean(self.raw(dev_off_y=1,dev_rot=rot))
            eq.clean(self.raw(dev_off_y=2,dev_rot=rot))
        # An open front gap can clear a central joint; the corner returns still collide.
        s=eq.clean(self.raw(wall_open=['front'],dev_off_y=0,joint='single'))
        eq.validate_wall(dict(s,joint='screw'),[0])
        with self.assertRaisesRegex(ValueError,'wall would hit'):eq.validate_wall(dict(s,joint='screw'),[-45])
        with self.assertRaisesRegex(ValueError,'wall would hit'):eq.clean(self.raw(joint='single',dev_off_y=-11))

    def test_boxes_notches_returns_small_and_short(self):
        s=eq.clean(self.raw());b=eq.wall_rectangles(s)
        self.assertEqual(len(b),9) # front + rear returns + left/right three notch sections
        self.assertEqual(sorted(set(q[4] for q in b)),[4,12])
        tiny=eq.clean(self.raw(dev_w=20,dev_d=20,dev_h=5,joint='single'))
        self.assertEqual(len(eq.wall_rectangles(tiny)),3)
        self.assertEqual(set(q[4] for q in eq.wall_rectangles(tiny)),{3})

    def test_pair_both_orders_and_wall_open(self):
        a=self.raw(dev_w=60,dev_d=70,dev_h=20,dev_off_x=-40)
        b=dict(a,dev_off_x=40,wall_open=['front','left'])
        for first,second in ((a,b),(dict(a,device_mount='straps'),b),(a,dict(b,device_mount='straps'))):
            s=eq.clean(dict(first,second=second));src=eq.source(s)
            self.assertEqual(eq.clean(s),s)
            self.assertIn('module wall2_add()',src)
            if second['device_mount']=='wall':
                self.assertEqual(s['second']['wall_open'],['front','left'])
                self.assertIn('dev2_wall_open=["front", "left"];',src)
            self.assertIn('wall2_add();',src)
        with self.assertRaisesRegex(ValueError,'either both'):eq.clean(dict(a,second=dict(b,device_mount='flat')))

    def test_legacy_sources_match_before_sha256(self):
        fixture=Path(__file__).resolve().parents[2]/'work/wall-device-42/legacy-before.json'
        for r in json.loads(fixture.read_text(encoding='utf-8')):
            with self.subTest(label=r['label']):
                self.assertEqual(hashlib.sha256(eq.source(eq.clean(r['spec'])).encode('utf-8')).hexdigest(),r['before'])
'''
(app/'test_wall_mount.py').write_text(tests,encoding='utf-8')
p=Path(r'D:\Projects\assembly-workshop\work\gui-refinement\check_python.py');t=p.read_text(encoding='utf-8').replace("'test_wall_box'):","'test_wall_box','test_wall_mount'):");p.write_text(t,encoding='utf-8',newline='\n')
js=''''use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const T=require('../tray-placement.js'),P=require('../port-openings.js'),Pair=require('../tray-pair.js'),C=require('../cable-ports.js');
const spec={name:'Wall',dev_w:90.7,dev_d:90.4,dev_h:25.4,device_mount:'wall',joint:'screw',dev_off_y:2,holes:[],ports:[],rear_ports:[],u:1};
test('Wall accepted; floor, ports and placement round trip',()=>{
 const v=T.values(spec);assert.deepEqual(T.problems(spec,v),[]);assert.equal(P.deviceLift({...spec,...v}),11.225);assert.equal(P.lift(spec),0);assert.equal(P.usesStandoffs(spec),false);
 assert.equal(Pair.REACH.wall,2.5);assert.deepEqual(T.diff(spec,v),{});
 const changed={...v,wall_open:['front','right']};assert.deepEqual(T.diff(spec,changed),{wall_open:['front','right']});
 assert.deepEqual(Pair.diff(spec,Pair.values(spec,{wall_open:['left']})),{wall_open:['left']});
 const ports=C.wizardPorts({...spec,rear_ports:[{id:'r',x:0,z:20}]},{standoff:29});assert.equal(ports[0].z,20);
});
test('Wall rejects missing cable access, all open and unknown sides',()=>{
 for(const wall_open of [[],['front','rear','left','right'],['back'],'rear',null])assert(T.problems(spec,T.values(spec,{wall_open})).some(x=>x.includes('Open sides')));
 assert(T.problems({...spec,dev_h:2},T.values(spec)).some(x=>x.includes('taller than 2')));
});
test('Wall clash and rotated preview geometry',()=>{
 for(const dev_rot of [0,90,180,270]){
  const v=T.values(spec,{dev_rot,dev_off_y:1});assert(T.problems(spec,v).includes(T.WALL_MESSAGE));
  v.dev_off_y=2;assert.deepEqual(T.problems(spec,v),[]);const q=T.wallBoxes(spec,v);assert.equal(q.length,9);assert.deepEqual([...new Set(q.map(q=>q[4]))].sort((a,b)=>a-b),[4,12]);
  const wall=T.schematic(spec,v)[1].v,strap=T.schematic(spec,{...v,device_mount:'straps'})[1].v;assert(wall.length>strap.length);
 }
 const small={...spec,dev_w:20,dev_d:20,dev_h:5};assert.equal(T.wallBoxes(small,T.values(small)).length,3);
});
test('Two-device wall, own open sides, floor and mixed mount rules',()=>{
 const a={...spec,dev_w:60,dev_d:70,dev_h:20,dev_off_x:-40},b={...a,dev_off_x:40},v=T.values(a),v2=Pair.values(b,{wall_open:['front','left']});
 assert.deepEqual(Pair.problems(a,v,b,v2),[]);assert.deepEqual(Pair.merged(v,v2).wall_open,['front','left']);
 assert.deepEqual(Pair.problems(a,v,b,{...v2,device_mount:'straps'}),[]);
 assert(Pair.problems(a,v,b,{...v2,device_mount:'flat'}).some(x=>x.includes('either both')));
 assert(Pair.schematic(a,v,b,v2)[1].v.length>T.schematic(a,v)[1].v.length);
});
test('Wall side UI is attached to the active device',()=>{
 const fs=require('node:fs'),path=require('node:path'),src=fs.readFileSync(path.join(__dirname,'../tray-placement.js'),'utf8');
 assert(src.includes('Open sides (cables):'));assert(src.includes('dv.wall_open=WALL_SIDES.filter'));assert(src.includes('...wallOpts'));
});
'''
(app/'js-tests/wall-mount.js').write_text(js,encoding='utf-8')
p=app/'run_checks.ps1';t=p.read_text(encoding='utf-8').replace("    Write-Host '== JavaScript front openings", "    & $node --test-reporter=spec (Join-Path $app 'js-tests\\wall-mount.js')\n    if ($LASTEXITCODE) { $failed = $true }\n    Write-Host '== JavaScript front openings");p.write_text(t,encoding='utf-8',newline='\n')
p=app/'asset-manifest.json';m=json.loads(p.read_text(encoding='utf-8'))
for row in m:
 f=app/row['file']
 if f.exists():row['sha256']=hashlib.sha256(f.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
p.write_text(json.dumps(m,indent=1)+'\n',encoding='utf-8')
print('Tests added and legacy whitespace reversal fixed')
