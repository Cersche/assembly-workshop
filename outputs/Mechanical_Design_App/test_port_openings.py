import unittest
from copy import deepcopy
import port_openings as P


class ProtrusionPolishTests(unittest.TestCase):
    def base(self, **kw):
        s=dict(name='Disposable band fixture',dev_w=158,dev_d=101.1,dev_h=26.5,
               device_mount='flat',joint='screw',rear_support=True,rear_style='reinforced',
               front_position='setback',front_setback=70,u=1,holes=[])
        s.update(kw)
        return s

    def zone(self, x0=-74.5, x1=-64.5, z0=12.4, z1=22.9):
        # Known rack-frame cut after 0.5 mm padding; flat lift = 3.5 mm.
        return dict(face='back',x=x0+79+.5,y=101.1,z=z0-3.5+.5,
                    w=x1-x0-1,d=140,h=z1-z0-1,keep_clear=True)

    def test_merged_window_leaves_2_1_mm_and_does_not_change_spec_or_source(self):
        import equipment as E
        s=E.clean(self.base(protrusions=[self.zone()]))
        before=deepcopy(s);source=E.source(s)
        band=E.keep_clear_bands(s)[0]
        self.assertEqual(band['band'],2.1)
        self.assertEqual(band['normal_band'],5)
        self.assertEqual(band['nearest'],'style window')
        self.assertEqual(band['merged'],['style window'])
        self.assertEqual(band['collisions'],[])
        self.assertEqual(s,before);self.assertEqual(E.source(s),source)

    def test_joint_boss_pilot_and_plate_edge(self):
        import equipment as E
        for zone,expected in [(self.zone(-43,-37,12,17),['joint boss','joint pilot']),
                              (self.zone(-46,-44,12,17),['joint boss'])]:
            s=E.clean(self.base(protrusions=[zone]))
            b=E.keep_clear_bands(s)[0]
            self.assertEqual(b['collisions'],expected);self.assertEqual(b['band'],0)
        b=E.keep_clear_bands(E.clean(self.base(protrusions=[self.zone(-125,-115,1,8)])))[0]
        self.assertIn('rack slot',b['merged'])
        self.assertEqual(E.keep_clear_bands(E.clean(self.base(rear_support=False))),[])
        b=E.keep_clear_bands(E.clean(self.base(protrusions=[self.zone(-130,-120,10,18)])))[0]
        self.assertEqual(b['band'],0);self.assertEqual(b['nearest'],'plate edge')

    def test_task34_legacy_specs_and_source_bytes_unchanged(self):
        import equipment as E
        import importlib.util
        from pathlib import Path
        path=Path(__file__).resolve().parents[2]/'docs/archive/codex/2026-10-20/task34/equipment.py'
        loader=importlib.util.spec_from_file_location('before34',path)
        old=importlib.util.module_from_spec(loader);loader.loader.exec_module(old);old.TEMPLATE=E.ROOT.parents[1]/'docs/archive/codex/2026-10-21/task36/equipment_tray.scad'
        count=0
        for mount in ('flat','sleeve','inserts','pegs','clips','straps'):
            for style in ('solid','open','reinforced','slots','vents'):
                for u in (1,2,5):
                    for rot in (0,90,180,270):
                        raw=self.base(device_mount=mount,rear_style=style,u=u,dev_rot=rot,
                                      dev_w=85,dev_d=100,dev_h=20,holes=[[20,20]],front_position='today')
                        untouched=deepcopy(raw);before=old.clean(raw);after=E.clean(raw)
                        self.assertEqual(before,after);self.assertEqual(raw,untouched)
                        self.assertEqual(old.source(before).encode('utf-8'),E.source(after).encode('utf-8'))
                        self.assertEqual(E.source(after),E.source(E.clean(dict(raw,bezel='none',front_setback=16,bezel_size=1))))
                        count+=1
        self.assertEqual(count,360)

    def test_numeric_slot_edge_corner_vent_and_other_zone_gaps(self):
        import equipment as E
        import math
        def band(q, **kw):
            return E.keep_clear_bands(E.clean(self.base(rear_style='solid',
                                                       protrusions=[self.zone(*q)],**kw)))[0]
        b=band((108,110,6,7.2));self.assertEqual(b['nearest'],'rack slot');self.assertEqual(b['band'],3.2625)
        b=band((-10,-5,10,15));self.assertEqual(b['nearest'],'plate edge');self.assertEqual(b['band'],9.975)
        b=band((123.8,125,1,2.2));self.assertAlmostEqual(b['band'],2.5-math.hypot(1.5,1.525),places=6)
        # Small rectangle 0.4 mm above a vent; circumscribed circles are conservative
        # relative to the template's 24-sided polygons.
        s=E.clean(self.base(rear_style='vents'))
        x,z=E.rear_geometry(s)['holes'][0]
        s['protrusions']=[self.zone(x-.6,x+.6,z+3.65,z+5.65)]
        b=E.keep_clear_bands(s)[0];self.assertEqual(b['nearest'],'vent hole');self.assertAlmostEqual(b['band'],.4)
        s=E.clean(self.base(rear_style='solid',protrusions=[self.zone(-20,-15,10,15),self.zone(-13,-8,10,15)]))
        self.assertEqual([b['band'] for b in E.keep_clear_bands(s)],[2,2])

SPEC = {'ports': [{'id': 'lan', 'label': 'LAN', 'type': 'rj45', 'x': 0, 'z': 20, 'w': 17, 'h': 14, 'r': 1}], 'standoff': 6}

class PortOpenings(unittest.TestCase):
    def test_foot_case_budget_and_optiplex_sleeve_values(self):
        import equipment
        feet=[{'x':20,'y':14.5,'w':5.5,'d':76.5,'h':2},{'x':169,'y':14.5,'w':5.5,'d':76.5,'h':2}]
        spec=equipment.clean(dict(name='OptiPlex specimen',dev_w=194.5,dev_d=182.5,dev_h=38.8,u=1,device_mount='sleeve',joint='screw',holes=[],feet=feet,dev_rot=90))
        self.assertAlmostEqual(equipment.needed_height(spec),40.3)   # case 36.8 on the 3.5 floor top
        win=P.sleeve(spec)
        self.assertEqual((win['bottom'],round(win['top'],6),win['lip']),(3.5,40.6,3.0))   # 0.3 mm above the case top
        self.assertAlmostEqual(win['height'],37.1)
        self.assertAlmostEqual(spec['u']*P.RACK_PITCH-P.PLATE_GAP/2-win['top'],3.825)
        pockets=equipment.foot_pockets(spec)
        self.assertTrue(all(q['through'] for q in pockets))
        self.assertTrue(all(-99.25<=q['x0']<q['x1']<=99.25 and 0<=q['y0']<q['y1']<=198.5 for q in pockets))

    def test_sleeve_scad_assignments_are_not_commented_out(self):
        # 2026-10-20: a trailing comment once swallowed sl_window_top on the same line (renders failed, tests passed).
        from pathlib import Path
        for line in (Path(__file__).with_name('equipment_tray.scad')).read_text(encoding='utf-8').splitlines():
            code, _, comment = line.partition('//')
            for name in ('sl_window_top=', 'sl_bottom=', 'sl_lip=', 'foot_h='):
                self.assertNotIn(name, comment.replace(' ', ''), line)

    def test_no_feet_preserves_height_and_mount_defaults(self):
        import equipment
        for mount in ('inserts','pegs','clips','straps','flat','sleeve'):
            spec=equipment.clean(dict(name='Legacy',dev_w=85,dev_d=100,dev_h=20,u=1,device_mount=mount,joint='single',holes=[[5,5]] if mount in ('inserts','pegs') else []))
            self.assertNotIn('feet',spec)
            self.assertEqual(equipment.device_lift(spec), equipment.floor_z(spec)+3+(spec.get('standoff',6) if mount in ('inserts','pegs','clips') else 0))

    def test_foot_pocket_joint_strap_and_rear_stop_guards(self):
        import equipment
        with self.assertRaisesRegex(ValueError,'strap slot'):
            equipment.validate_foot_pockets({'device_mount':'flat','dev_w':100,'dev_d':100,'dev_h':20,'dev_rot':0,'dev_off_x':0,'dev_off_y':0,'joint':'single','feet':[{'x':-4,'y':25,'w':5,'d':5,'h':1}]},116)
        for foot,message in [({'x':8,'y':5,'w':2,'d':4,'h':1},'screw joint'),({'x':40,'y':98,'w':2,'d':2,'h':1},'rear stop')]:
            spec=dict(name='Guard',dev_w=100,dev_d=100,dev_h=20,u=1,device_mount='sleeve',joint='screw',holes=[],feet=[foot])
            with self.assertRaisesRegex(ValueError,message):equipment.clean(spec)

    def test_no_hole_flat_device_cleans(self):
        import equipment
        spec = equipment.clean(dict(name='Box', dev_w=180, dev_d=180, dev_h=36,
                                    u=1, device_mount='flat', joint='screw', holes=[]))
        self.assertEqual(spec['device_mount'], 'flat')
        self.assertEqual(spec['holes'], [])

    def test_movement_and_preservation(self):
        for tray, dx, dz in [(None,0,0), ({},0,0), ({'dev_off_x':11},11,0), ({'standoff':10},0,4), ({'device_mount':'straps'},0,-6), ({'ports':[], 'u':5, 'dev_off_y':100},0,0)]:
            before = deepcopy((SPEC,tray))
            self.assertEqual(P.front_openings(SPEC,tray), dict(ports=[{**SPEC['ports'][0], 'x':dx, 'z':20+dz}], dx=dx,dz=dz,follows=True,rotation=0,message=None))
            self.assertEqual((SPEC,tray),before)
        self.assertEqual(P.front_openings({**SPEC,'dev_off_x':5},{'dev_off_x':5})['dx'],0)
        self.assertEqual(P.lift({}),6)
        self.assertEqual(P.lift({'device_mount':'straps','standoff':10}),0)
        self.assertEqual(P.front_openings({'ports':[{'x':0.1234,'z':20.1234}]})['ports'][0]['x'],0.123)

    def test_rotation(self):
        for rotation in (90,180,270):
            tray={'dev_rot':rotation,'dev_off_x':11,'standoff':10}
            before=deepcopy((SPEC,tray))
            face='rear' if rotation==180 else 'side'
            message=f'The device is turned {rotation}°, so its front ports now face the {face} of the tray. The front openings no longer line up with them. The faceplate STL keeps the openings where they were entered in the library (not moved). Check them, or remove them in Edit library item.'
            result=P.front_openings(SPEC,tray)
            self.assertEqual(result,dict(ports=SPEC['ports'],dx=0,dz=0,follows=False,rotation=rotation,message=message))
            self.assertIsNot(result['ports'][0],SPEC['ports'][0])
            self.assertIsNone(P.front_openings({},tray)['message'])
            self.assertEqual((SPEC,tray),before)

    def test_sizes(self):
        sizes={'rj45':(17,14,1),'usb-a':(15,8,1),'usb-c':(12,7,3),'hdmi':(17,8,1),'micro-hdmi':(11,7,2),'dc-barrel':(11,11,5.5),'iec':(28,20,1),'other':(15,8,1)}
        for type,(w,h,r) in sizes.items(): self.assertEqual(P.default_size(type),dict(w=w,h=h,r=r))
        for type in (None,'unknown','toString'): self.assertEqual(P.default_size(type),dict(w=15,h=8,r=1))
        size=P.default_size('rj45');size['w']=999
        self.assertEqual(P.DEFAULT_SIZES['rj45']['w'],17)
        self.assertEqual(P.SIZE_NOTE,'Starting size for this connector type: a guess, not a measured size. Edit it to match your device.')

    def test_problems(self):
        base=dict(x=0,z=20,w=10,h=8)
        edge='Port 1 opening would run past the faceplate edge. Move the device back toward the centre or edit the port.'
        vertical='Port 1 opening would run off the top or bottom of the faceplate. Change the standoff or faceplate height, or edit the port.'
        fixtures=[(dict(x=125,z=0),[125],[edge]),(dict(z=5),[],[vertical]),(dict(z=39),[],[vertical]),(dict(x=60),[60],['Port 1 opening would cut into keystone 1 (at X = 60 mm). Move the device or the keystone.']),(dict(x=-60),[72.5,-60],['Port 1 opening would cut into keystone 2 (at X = -60 mm). Move the device or the keystone.']),(dict(x=72.5),[72.5],['Port 1 opening would cut into keystone 1 (at X = 72.5 mm). Move the device or the keystone.']),(dict(x=75.5),[60],[]),(dict(x=121,z=6.025),[],[])]
        for patch,ks,expected in fixtures:
            ports=[{**base,**patch}];before=deepcopy((ports,ks))
            self.assertEqual(P.problems(ports,1,ks),expected)
            self.assertEqual((ports,ks),before)
        for key in ('x','z','w','h'):
            for v in (float('nan'),float('inf'),-float('inf')): self.assertEqual(P.problems([{**base,key:v}],1,[]),[])
        joint='Port 1 opening sits in front of the tray screw joint at X = -40 mm; the cable would hit it. Move the device sideways or edit the port.'
        self.assertEqual(P.problems([{**base,'x':-30,'z':15,'w':16,'h':14}],1,[],[-40,40]),[joint])
        self.assertEqual(P.problems([{**base,'x':-58,'z':15,'w':16,'h':14}],1,[],[-40,40]),[])   # 1 mm clear of the zone
        self.assertEqual(P.problems([{**base,'x':-57.9,'z':15,'w':16,'h':14}],1,[],[-40,40]),[joint])
        self.assertEqual(P.problems([{**base,'x':-40,'z':38,'w':10,'h':6}],2,[],[-40,40]),[])   # above the joint post
        self.assertEqual(P.problems([{**base,'x':-30,'z':15,'w':16,'h':14}],1,[]),[])            # no joints given
        result=P.problems([{**base,'label':'LAN','x':125},{**base,'z':0}],1,[])
        self.assertEqual(len(result),2);self.assertTrue(result[0].startswith('LAN opening'))

    def test_joint_positions(self):
        # Brian, 2026-10-19 (option 3): default spot kept when clear; else nearest clear spot per side; else a problem.
        lan=[{'x':-30,'z':15,'w':16,'h':14}]
        self.assertEqual(P.joint_positions([],[],68),{'joints':[-40,40],'default':40,'moved':False,'problem':None})
        self.assertEqual(P.joint_positions([{'x':-40,'z':38,'w':10,'h':6}],[],68)['moved'],False)   # above the joint post
        self.assertEqual(P.joint_positions(lan,[],68)['joints'],[-48,40])
        self.assertEqual(P.joint_positions(lan,[],50.5)['joints'],[-12,38.5])                        # narrow tray: inward
        self.assertEqual(P.joint_positions([{'x':-40,'z':15,'w':16,'h':14},{'x':-58,'z':15,'w':16,'h':14}],[],68)['joints'],[-22,40])
        self.assertEqual(P.joint_positions([],[-50],68)['joints'],[-34,40])                          # keystone 16 mm rule
        r=P.joint_positions([{'x':0,'z':15,'w':200,'h':14}],[],68)
        self.assertEqual(r['joints'],[None,None])
        self.assertEqual(r['problem'],'The left and right tray screw joints cannot be placed clear of the openings and keystones anywhere on the tray. Move the device or an opening, or choose the single printed piece joint.')
        self.assertTrue(P.joint_positions([{'x':-30,'z':15,'w':90,'h':14}],[],68)['problem'].startswith('The left tray screw joint cannot'))
        before=deepcopy(lan);P.joint_positions(lan,[],68);self.assertEqual(lan,before)

if __name__ == '__main__': unittest.main()


class ProtrusionTests(unittest.TestCase):
    def base(self):
        import equipment as E
        return E.clean(dict(name='Test box',dev_w=100,dev_d=100,dev_h=20,u=1,device_mount='flat',joint='screw'))

    def test_validation_round_trip_and_legacy_bytes(self):
        import equipment as E
        from pathlib import Path
        import importlib.util
        old_path=Path(__file__).resolve().parents[2]/'docs/archive/codex/2026-10-20/task32/equipment.py'
        mod=importlib.util.spec_from_file_location('before32',old_path);old=importlib.util.module_from_spec(mod);mod.loader.exec_module(old);old.TEMPLATE=E.ROOT.parents[1]/'docs/archive/codex/2026-10-21/task36/equipment_tray.scad'
        for mount in ('flat','sleeve','inserts'):
            raw=dict(self.base(),device_mount=mount,holes=[[5,5]])
            self.assertEqual(E.source(E.clean(raw)),old.source(old.clean(raw)))
        p=dict(face='back',x=10,y=100,z=5,w=10,d=140,h=8,keep_clear=True)
        raw=dict(self.base(),protrusions=[p],rear_support=True)
        clean=E.clean(raw);self.assertEqual(E.clean(clean),clean)
        self.assertEqual(clean['protrusions'],[p]);self.assertTrue(E.rear_geometry(clean)['keep_clear']);self.assertFalse(E.rear_geometry(clean)['windows']);self.assertIn('keep_clear_cut();',E.source(clean))
        for value in ({},None,[p]*33,[dict(p,keep_clear=False)],[dict(p,w=float('nan'))],[dict(p,face='rear')]):
            with self.assertRaises(ValueError):E.clean(dict(raw,protrusions=value))
        self.assertNotIn('protrusions',E.clean(dict(raw,protrusions=[])))
        vents=E.rear_geometry(E.clean(dict(raw,rear_style='vents')))  # Claude review: zones never join the rounded style windows
        self.assertTrue(vents['keep_clear']);self.assertTrue(all(q not in vents['windows'] for q in vents['keep_clear']))

    def test_rotated_keep_clear_zone_hits_rear(self):
        import equipment as E
        s=dict(self.base(),rear_support=True,dev_rot=90,protrusions=[dict(face='left',x=100,y=40,z=4,w=140,d=10,h=8,keep_clear=True)])
        box=E.keep_clear_boxes(s)[0]
        self.assertEqual((box['y0'],box['y1']),(112,252))
        self.assertEqual(len(E.keep_clear_openings(s)),1)


class FrontPositionBezelTests(unittest.TestCase):
    def base(self,**kw):
        return dict(dict(name='Bench',dev_w=85,dev_d=100,dev_h=20,u=1,device_mount='inserts',joint='screw',holes=[[10,15]],ports=[]),**kw)

    def test_defaults_are_byte_identical_for_four_existing_shapes(self):
        import equipment as E
        from pathlib import Path
        import importlib.util
        path=Path(__file__).resolve().parents[2]/'docs/archive/codex/2026-10-20/task33/equipment.py'
        mod=importlib.util.spec_from_file_location('before33',path);old=importlib.util.module_from_spec(mod);mod.loader.exec_module(old);old.TEMPLATE=E.ROOT.parents[1]/'docs/archive/codex/2026-10-21/task36/equipment_tray.scad'
        for spec in [self.base(device_mount='sleeve',dev_w=182.5,dev_d=194.5,dev_h=36.8),self.base(ports=[dict(x=0,z=26,w=15,h=8,r=1)]),self.base(device_mount='flat'),self.base(u=2)]:
            with self.subTest(spec=spec):
                before=old.source(old.clean(spec))
                self.assertEqual(E.source(E.clean(spec)),before)
                self.assertEqual(E.source(E.clean(dict(spec,front_position='today',bezel='none',front_setback=16,bezel_size=1))),before)

    def test_position_and_flush_window(self):
        import equipment as E
        for mode,amount,y,window in [('flush',0,-4,True),('setback',3,-1,True),('setback',4,0,True),('setback',10,6,False)]:
            s=E.clean(self.base(joint='single',front_position=mode,front_setback=amount))
            self.assertEqual(P.device_y(s),y);self.assertEqual(bool(P.front_window(s)),window)
            self.assertEqual(E.clean(s),s)
            self.assertIn('dev_y='+str(float(y))+';',E.source(s))
            if window:self.assertIn('square([86.0,20.3]',E.source(s))
        for spec,message in [(self.base(front_position='flush'),'Sleeve mount'),(self.base(device_mount='flat',joint='single',front_position='flush'),'corner stops'),(self.base(device_mount='sleeve',front_position='setback',front_setback=10),'Sleeve set back'),(self.base(joint='single',front_position='flush',dev_h=35),'bands'),(self.base(joint='single',front_position='flush',holes=[[10,2]]),'standoff')]:
            with self.assertRaisesRegex(ValueError,message):E.clean(spec)

    def test_ranges_unknown_values_and_allocation_round_trip(self):
        import equipment as E
        for k,value in [('front_position','bad'),('bezel','bad'),('front_setback',True),('bezel_size',True),('front_setback',-1),('front_setback',101),('bezel_size',.4),('bezel_size',1.6),('bezel_size',float('nan'))]:
            with self.subTest(key=k,value=value):
                with self.assertRaises(ValueError):E.clean(self.base(**{k:value}))
                with self.assertRaises(ValueError):E.placement_settings({k:value})
        choices=dict(front_position='setback',front_setback=20,bezel='chamfer',bezel_size=1.2)
        self.assertEqual(E.placement_settings(choices),choices)
        s=E.clean(E.allocation_spec(self.base(),choices));self.assertEqual(P.device_y(s),16)
        self.assertEqual(E.clean(s),s)

    def test_bezel_web_reduction_pair_edge_slots_and_keystone(self):
        ports=[dict(x=-6.5,z=22,w=10,h=8,r=1),dict(x=6.5,z=22,w=10,h=8,r=1)]
        s=self.base(ports=ports,bezel='rounded',bezel_size=1.5)
        plan=P.bezel_plan(s);self.assertEqual([p['size'] for p in plan['openings']],[.5,.5]);self.assertEqual(len(plan['notes']),2)
        self.assertGreaterEqual(3-sum(p['size'] for p in plan['openings']),P.BEZEL_WEB)
        for port in [dict(x=120,z=6.323,w=5,h=4),dict(x=123,z=23,w=4,h=4),dict(x=0,z=3.025,w=10,h=2)]:
            q=P.bezel_plan(self.base(ports=[port],bezel='chamfer'))
            self.assertEqual(q['openings'][0]['size'],0);self.assertTrue(q['notes'])
        q=P.bezel_plan(self.base(ports=[dict(x=15,z=22,w=4,h=4)],keystones=[0],bezel='chamfer',bezel_size=1.5))
        self.assertEqual(q['openings'][0]['size'],.5)

    def test_geometry_is_only_front_opening_edges(self):
        import equipment as E
        base=self.base(ports=[dict(x=0,z=26,w=15,h=8,r=1)])
        a=E.source(E.clean(base));b=E.source(E.clean(dict(base,bezel='rounded')))
        self.assertNotIn('bezel_cuts',a);self.assertIn('bezel_cuts();',b);self.assertIn('bezel_rounded=true;',b);self.assertIn('bezel_rounded?8:1',b)
        self.assertEqual(a[a.index('module ks_cut'):a.index('module faceplate')],b[b.index('module ks_cut'):b.index('module faceplate')])
        self.assertEqual(a[a.index('module rear_bracket'):a.index('module device_features_add')],b[b.index('module rear_bracket'):b.index('module device_features_add')])
        self.assertNotIn('minkowski',b)
        s=E.clean(self.base(device_mount='sleeve',joint='single',bezel='chamfer'))
        self.assertEqual(P.bezel_plan(s)['openings'][0]['label'],'Front window')
        self.assertIn('bezel_shapes=[[',E.source(s))
