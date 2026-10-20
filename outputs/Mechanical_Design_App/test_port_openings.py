import unittest
from copy import deepcopy
import port_openings as P

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
