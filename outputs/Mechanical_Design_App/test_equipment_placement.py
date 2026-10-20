import re
import subprocess
import unittest
from pathlib import Path

import equipment as eq

HERE = Path(__file__).resolve().parent
BASE = {'name': 'Placement test', 'dev_w': 85, 'dev_d': 56, 'dev_h': 20, 'device_mount': 'inserts',
        'joint': 'screw', 'holes': [[3.5, 3.5], [61.5, 49.5]]}


class PlacementSettings(unittest.TestCase):
    def test_template_declares_settings_with_neutral_defaults(self):
        t = eq.TEMPLATE.read_text(encoding='utf-8')
        for line in ('dev_off_x=0;', 'dev_off_y=0;', 'dev_rot=0;'):
            self.assertIn(line, t)
        # Default expressions reduce exactly to the previous centred layout.
        self.assertIn('tray_w=2*(abs(dev_off_x)+fp_w/2+(sleeve?max(margin,sl_side+sl_wall):margin))', t)
        self.assertIn('dev_x=-fp_w/2+dev_off_x; dev_y=sleeve?-plate_t:front_gap+dev_off_y;', t)
        self.assertIn('dev_rot==0||dev_rot==90||dev_rot==180||dev_rot==270', t)

    def test_older_items_without_keys_keep_identical_override_block(self):
        s = eq.clean(dict(BASE))
        self.assertEqual((s['dev_off_x'], s['dev_off_y'], s['dev_rot']), (0, 0, 0))
        tail = eq.source(s)[len(eq.TEMPLATE.read_text(encoding='utf-8')):]
        self.assertNotRegex(tail, r'dev_off_|dev_rot')
        explicit = eq.source(eq.clean(dict(BASE, dev_off_x=0, dev_off_y=0, dev_rot=0)))
        self.assertEqual(explicit, eq.source(s))

    def test_moved_rotated_item_writes_settings(self):
        src = eq.source(eq.clean(dict(BASE, dev_off_x=-10, dev_off_y=5, dev_rot='90')))
        self.assertIn('dev_off_x=-10.0;', src)
        self.assertIn('dev_off_y=5.0;', src)
        self.assertIn('dev_rot=90;', src)

    def test_invalid_placements_are_rejected(self):
        for bad in ({'dev_rot': 45}, {'dev_rot': 'x'}, {'dev_off_y': -13}, {'dev_off_x': 70},
                    {'dev_off_x': 50, 'dev_w': 120}):
            with self.assertRaises(ValueError):
                eq.clean(dict(BASE, **bad))
        # Rotation swaps width/depth: a 200 mm wide device fits only unrotated, a 60 mm deep one rotated.
        eq.clean(dict(BASE, dev_w=180, dev_d=60, holes=[], device_mount='straps'))
        eq.clean(dict(BASE, dev_w=180, dev_d=60, holes=[], device_mount='straps', dev_rot=90))
        with self.assertRaises(ValueError):
            eq.clean(dict(BASE, dev_w=60, dev_d=220, holes=[], device_mount='straps', dev_rot=90, u=1))

    def test_feet_pockets_reduce_flat_and_sleeve_height_budget(self):
        feet=[{'x':20,'y':14.5,'w':5.5,'d':76.5,'h':2},{'x':169,'y':14.5,'w':5.5,'d':76.5,'h':2}]
        s=eq.clean(dict(BASE,dev_w=194.5,dev_d=182.5,dev_h=38.8,device_mount='sleeve',joint='screw',holes=[],feet=feet,dev_rot=90,u=1))
        self.assertAlmostEqual(eq.needed_height(s),40.0)
        win=eq.port_openings.sleeve(s)
        self.assertEqual((win['bottom'],win['top'],win['lip']),(3.2,40.3,3.0))
        self.assertAlmostEqual(win['height'],37.1)
        self.assertAlmostEqual(s['u']*eq.RACK_PITCH-eq.PLATE_GAP/2-win['top'],4.125)
        self.assertEqual(len(eq.foot_pockets(s)),2)
        self.assertTrue(all(p['through'] for p in eq.foot_pockets(s)))
        src=eq.source(s)
        self.assertIn('feet=[[20.0, 14.5, 5.5, 76.5, 2.0]',src)
        flat=eq.clean(dict(BASE,dev_w=194.5,dev_d=182.5,dev_h=38.8,device_mount='flat',joint='screw',holes=[],feet=feet,dev_rot=90,u=1))
        self.assertAlmostEqual(eq.needed_height(flat),40.0)

    def test_feet_values_are_validated_and_old_specs_keep_height(self):
        old=eq.clean(dict(BASE,device_mount='flat'))
        self.assertNotIn('feet',old)
        self.assertEqual(eq.needed_height(old),23.5)
        for bad in ([{'x':-1,'y':0,'w':4,'d':4,'h':2}], [{'x':0,'y':0,'w':3,'d':3,'h':301}], [{'x':0,'y':0,'w':1,'d':3,'h':1}], ['bad']):
            with self.assertRaises(ValueError):eq.clean(dict(BASE,device_mount='flat',feet=bad))

    def test_pocket_collisions_block_straps_joints_and_sleeve_edges(self):
        def check(mount, foot):
            return eq.clean(dict(BASE,dev_w=100,dev_d=100,dev_h=20,device_mount=mount,joint='screw',holes=[],feet=[foot],u=1))
        with self.assertRaisesRegex(ValueError,'strap slot'):
            eq.validate_foot_pockets({'device_mount':'flat','dev_w':100,'dev_d':100,'dev_h':20,'dev_rot':0,'dev_off_x':0,'dev_off_y':0,'joint':'single','feet':[{'x':-4,'y':25,'w':5,'d':5,'h':1}]},116)
        with self.assertRaisesRegex(ValueError,'screw joint'):
            check('sleeve',{'x':8,'y':5,'w':2,'d':4,'h':1})
        with self.assertRaisesRegex(ValueError,'rear stop'):
            check('sleeve',{'x':40,'y':98,'w':2,'d':2,'h':1})


if __name__ == '__main__':
    unittest.main()
