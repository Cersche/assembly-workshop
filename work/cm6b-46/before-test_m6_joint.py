"""M6 bracket hardware (Brian, 2026-10-28; reproduces HDT-M6-A): opt-in m6_joint source and validation tests; no renders."""
import json
import unittest
import hashlib
import subprocess
from pathlib import Path
import equipment as eq

HDT = json.loads((Path(__file__).resolve().parents[1] / 'Hard_Drive_Tray_2026-10-25' / 'revision.json').read_text(encoding='utf-8'))['spec']
FLAT = dict(name='Box', dev_w=150, dev_d=120, dev_h=30, device_mount='flat', joint='screw', standoff=0, u=1)


class M6JointTests(unittest.TestCase):
    def test_off_keeps_legacy_source(self):
        for spec in (HDT, FLAT, dict(FLAT, m6_joint=False)):
            src = eq.source(eq.clean(spec))
            self.assertNotIn('m6', src)
            self.assertIn('front_gap=12;', src)
            self.assertNotIn('m6_joint', eq.clean(spec))

    def test_on_hooks_every_legacy_line(self):
        for spec in (HDT, FLAT):
            s = eq.clean(dict(spec, m6_joint=True))
            self.assertIs(s['m6_joint'], True)
            src = eq.source(s)
            for old, new in eq.M6_HOOKS:
                self.assertNotIn(old, src)
                self.assertIn(new, src)
            self.assertIn('// @m6-begin', src)

    def test_joint_layout(self):
        self.assertEqual(eq.m6_joints(195.45 / 2), [-87.225, -40, 40, 87.225])
        self.assertEqual(eq.m6_joints(60), [-49.5, 49.5])  # narrow tray: edge pair only, never overlapping tabs

    def test_rejects_unsupported(self):
        for extra in (dict(device_mount='sleeve'), dict(rear_support=True), dict(dev_off_y=-3),
                      dict(device_mount='inserts', holes=[[10, 10]], standoff=6), dict(m6_joint='yes')):
            with self.assertRaises(ValueError, msg=extra):
                eq.clean(dict(dict(FLAT, m6_joint=True), **extra))
        eq.clean(dict(FLAT, m6_joint=True, device_mount='inserts', holes=[[10, 10]], standoff=6, u=2))

    def test_opening_in_front_of_joint(self):
        with self.assertRaises(ValueError):
            eq.clean(dict(FLAT, m6_joint=True, ports=[{'x': 40, 'z': 20, 'w': 10, 'h': 10, 'r': 1}]))
        eq.clean(dict(FLAT, m6_joint=True, ports=[{'x': 0, 'z': 20, 'w': 10, 'h': 10, 'r': 1}]))

    def test_placement_key(self):
        self.assertIn('m6_joint', eq.PLACEMENT_KEYS)
        self.assertEqual(eq.placement_settings({'m6_joint': True}), {'m6_joint': True})


class SplitRailsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[2]
        cls.spec=json.loads((cls.root/'work/m6-rails-43/cm6b-spec.json').read_text(encoding='utf-8'))

    def test_explicit_cm6a_positions_and_parts(self):
        s=eq.clean(self.spec)
        self.assertEqual(s['m6_joint_x'],[-104.4,104.4])
        self.assertEqual([x+127 for x in s['m6_joint_x']],[22.599999999999994,231.4])
        self.assertEqual(s['m6_joint_z'],[8.6,35.85])
        self.assertEqual(eq.clean(s),s)
        src=eq.source(s)
        self.assertIn('mr_rail(0);mr_rail(1);',src)
        self.assertNotIn('// @m6-begin',src)

    def test_validation_messages_and_js_agreement(self):
        from test_tray_placement import node
        cases=[({},None),({'m6_joint':False},'Split rails need M6 hardware'),
               ({'ports':[dict(x=104.4,z=20,w=6,h=6,r=0)]},'front opening or keystone'),
               ({'keystones':[100]},'front opening or keystone'),
               ({'dev_w':230},'too wide'),({'m6_joint_x':[-113,113]},'too wide'),
               ({'m6_usable_depth':100},'longer than the usable depth'),
               ({'m6_pocket_profile':[[-106.3,3.3],[106.3,3.3],[106.3,41.3],[-106.3,41.3]]},'at least 2 mm'),
               ({'m6_rail_t':2.4},'Rail thickness'),({'test_id':'bad ID'},'Test ID'),
               ({'device_mount':'sleeve'},'Sits flat'),({'rear_support':True},'rear bracket'),
               ({'m6_joint_z':[8.6,36.1]},'at least 2.5 mm'),({'dev_rot':90},'unrotated'),
               ({'m6_rail_t':2.5},'3 mm of top material'),({'bezel':'chamfer'},'front-edge bezel')]
        for extra,message in cases:
            spec=dict(self.spec,**extra)
            if message:
                with self.assertRaisesRegex(ValueError,message):eq.clean(spec)
            else:eq.clean(spec)
            code='const T=require("./tray-placement.js"),s=JSON.parse(process.argv[1]);console.log(JSON.stringify(T.problems(s,T.values(s))));'
            p=subprocess.run([node(),'-e',code,json.dumps(spec)],cwd=eq.ROOT,capture_output=True,text=True,check=True)
            errors=json.loads(p.stdout)
            self.assertEqual(bool(errors),bool(message),(extra,errors))
            if message:self.assertIn(message,' '.join(errors))

    def test_legacy_sha256_corpus(self):
        cases=json.loads((self.root/'work/m6-rails-43/legacy-before.json').read_text(encoding='utf-8'))
        self.assertEqual(len(cases),14)
        for case in cases:
            for spec in (case['spec'],dict(case['spec'],m6_rails=False)):
                self.assertEqual(hashlib.sha256(eq.source(eq.clean(spec)).encode('utf-8')).hexdigest(),case['sha256'],case['label'])

    def test_split_layout_preserves_three_objects(self):
        import print_layout
        import zipfile
        import io
        import xml.etree.ElementTree as ET
        part='solid t\nfacet normal 0 0 1\nouter loop\nvertex 0 0 0\nvertex 1 0 0\nvertex 0 1 0\nendloop\nendfacet\nendsolid t\n'
        blob=print_layout.layout_3mf(dict(faceplate=part,rail_l=part,rail_r=part))
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            root=ET.fromstring(z.read('3D/3dmodel.model'))
        ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
        self.assertEqual(len(root.findall('m:resources/m:object',ns)),3)
        self.assertEqual(len(root.findall('m:build/m:item',ns)),3)

    def test_disconnected_solids_block_a_split_part(self):
        import m6_rails
        tetra=[[0,1,2],[0,3,1],[0,2,3],[1,3,2]]
        m6_rails.check_connected({'triangles':tetra})
        with self.assertRaisesRegex(ValueError,'one connected closed solid'):
            m6_rails.check_connected({'triangles':tetra+[[i+4 for i in t] for t in tetra]})


class SplitRailFidelityTests(unittest.TestCase):
    def setUp(self):
        self.spec=json.loads((Path(__file__).resolve().parents[2]/'work/m6-fidelity-44/revision2/spec.json').read_text(encoding='utf-8'))

    def test_numeric_sections_and_colours_round_trip(self):
        s=eq.clean(self.spec)
        self.assertEqual(eq.clean(s),s)
        self.assertEqual(s['m6_rail_len'],121.62)
        self.assertEqual(len(s['m6_light_pipes']),5)
        self.assertEqual(len(s['m6_vectors']),9)
        self.assertEqual(eq.placement_settings(s)['m6_stub_sections'],s['m6_stub_sections'])
        code=eq.source(s)
        self.assertNotIn('import(',code)
        self.assertIn('mf_loft(m6_stub_sections[s])',code)
        self.assertIn('if(part=="vector_9")mf_vector(8)',code)
        for name in ['pipe_1','pipe_5','vector_1','vector_9']:self.assertTrue(eq.mesh_part_name(name))
        for name in ['../pipe_1','pipe_0','pipe_1.stl','vector_bad',None]:self.assertFalse(eq.mesh_part_name(name))

    def test_each_setting_rejects_malformed_values(self):
        bad={'m6_rail_len':300,'m6_bay_h':30,'m6_bay_d':0,'m6_edge_radius':-1,
             'm6_rail_profiles':[[[0,0],[1,1],[2,2]]], 'm6_side_windows':[[[0,0]]],
             'm6_stub_sections':[[[0,[[0,0],[1,0],[0,1]]]]],
             'm6_retention_slot':[0,0,-1,4,0], 'm6_light_pipes':[[0,0,-8,8.72]],
             'm6_vectors':[[2,[[[0,0],[1,0],[0,1]]]]], 'm6_nose_bridge':[[2,1],[[[0,0],[1,0],[0,1]]]]}
        for key,value in bad.items():
            with self.subTest(key=key),self.assertRaises(ValueError):eq.clean(dict(self.spec,**{key:value}))
        s=dict(self.spec);s['m6_stub_sections']=json.loads(json.dumps(s['m6_stub_sections']))
        s['m6_stub_sections'][0][1][0]=s['m6_stub_sections'][0][0][0]
        with self.assertRaisesRegex(ValueError,'Loft stations'):eq.clean(s)

    def test_default_length_and_explicit_bay_source(self):
        spec=json.loads((Path(__file__).resolve().parents[2]/'work/m6-rails-43/cm6b-spec.json').read_text(encoding='utf-8'))
        self.assertIn('mr_length=138;',eq.source(eq.clean(spec)))
        code=eq.source(eq.clean(dict(spec,m6_rail_len=121.62,m6_bay_h=14,m6_bay_d=44.69)))
        self.assertIn('mr_length=121.62;',code)
        self.assertIn('44.69,14',code)

    def test_profile_group_and_finite_coordinates(self):
        spec=dict(self.spec);spec.pop('m6_side_windows')
        with self.assertRaisesRegex(ValueError,'together'):eq.clean(spec)
        for value in [True,float('nan'),float('inf')]:
            with self.assertRaises(ValueError):eq.clean(dict(self.spec,m6_light_pipes=[[value,30,8,8.72]]))

    def test_colour_layout_uses_plate_transform(self):
        import print_layout
        import io,zipfile,xml.etree.ElementTree as ET
        tetra='solid a\n'+''.join('facet normal 0 0 1\nouter loop\n'+''.join('vertex %s %s %s\n'%v for v in tri)+'endloop\nendfacet\n' for tri in [[(0,-4,1),(1,-4,1),(0,-3.8,2)]])+'endsolid a\n'
        parts={'faceplate':tetra,'rail_l':tetra,'rail_r':tetra,'pipe_1':tetra,'vector_1':tetra}
        placed=dict(print_layout.place(parts))
        self.assertEqual(placed['faceplate'],placed['pipe_1'])
        self.assertEqual(placed['faceplate'],placed['vector_1'])
        with zipfile.ZipFile(io.BytesIO(print_layout.layout_3mf(parts))) as z:
            root=ET.fromstring(z.read('3D/3dmodel.model'))
        ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
        self.assertEqual(len(root.findall('m:resources/m:object',ns)),5)
        self.assertEqual(len(root.findall('m:resources/m:basematerials/m:base',ns)),2)


if __name__ == '__main__':
    unittest.main()
