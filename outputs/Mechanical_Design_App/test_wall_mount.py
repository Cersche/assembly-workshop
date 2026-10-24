import unittest,json,hashlib
from pathlib import Path
import equipment as eq

class WallTests(unittest.TestCase):
    def raw(self, **kw):
        return dict(dict(name='Wall test',dev_w=90.7,dev_d=90.4,dev_h=25.4,device_mount='wall',joint='screw',dev_off_y=13),**kw)

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
            eq.clean(self.raw(dev_off_y=13,dev_rot=rot))
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
