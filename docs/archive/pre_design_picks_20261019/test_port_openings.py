import unittest
from copy import deepcopy
import port_openings as P

SPEC = {'ports': [{'id': 'lan', 'label': 'LAN', 'type': 'rj45', 'x': 0, 'z': 20, 'w': 17, 'h': 14, 'r': 1}], 'standoff': 6}

class PortOpenings(unittest.TestCase):
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
        fixtures=[(dict(x=125,z=0),[125],[edge]),(dict(z=5),[],[vertical]),(dict(z=39),[],[vertical]),(dict(x=60),[60],['Port 1 opening would cut into keystone 1 (at X = 60 mm). Move the device or the keystone.']),(dict(x=-60),[72.5,-60],['Port 1 opening would cut into keystone 2 (at X = -60 mm). Move the device or the keystone.']),(dict(x=72.5),[72.5],['Port 1 opening would cut into keystone 1 (at X = 72.5 mm). Move the device or the keystone.']),(dict(x=75.5),[60],[]),(dict(x=121,z=6),[],[])]
        for patch,ks,expected in fixtures:
            ports=[{**base,**patch}];before=deepcopy((ports,ks))
            self.assertEqual(P.problems(ports,1,ks),expected)
            self.assertEqual((ports,ks),before)
        for key in ('x','z','w','h'):
            for v in (float('nan'),float('inf'),-float('inf')): self.assertEqual(P.problems([{**base,key:v}],1,[]),[])
        result=P.problems([{**base,'label':'LAN','x':125},{**base,'z':0}],1,[])
        self.assertEqual(len(result),2);self.assertTrue(result[0].startswith('LAN opening'))

if __name__ == '__main__': unittest.main()
