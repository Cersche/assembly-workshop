"""TL-SG108E: ports flush, rear stop, spring bumps in the tray floor catch the switch's two keyholes (front retention).
Delivery-only patch on the app's generated source (Brian, 2026-10-23). Fit, retention, strength UNKNOWN."""
import sys, json
sys.path.insert(0, r'D:/Projects/assembly-workshop/outputs/Mechanical_Design_App')
import equipment
SPEC = {'name':'TP-Link TL-SG108E','dev_w':158,'dev_d':100,'dev_h':25,'u':1,'device_mount':'sleeve','joint':'screw','rear_support':False,
        'dev_rot':0,'dev_off_x':-15,'dev_off_y':0,'holes':[],'ports':[],'rear_ports':[],'keystones':[88],'tray_follow':True,'sleeve_top':0.8,
        'labels':[{'text':'UPLINK','x':88,'z':3.8,'size':4.5}]}
# Brian's measurements: keyhole round parts 48.5 mm behind the port face, centred on the width, 110 mm apart, ~8-9 mm across.
KEY_Y, KEY_PITCH = 48.5, 110
DETENT = f'''
// Keyhole detents (Brian, 2026-10-23). Arm: 8 mm wide, 1.8 mm thick, 26 mm long, root toward the front, 1.2 mm slot around it.
// Bump: 5 mm wide, stands 0.6 mm above the floor (keyholes are shallow); 45 deg ramp facing the front (switch rides over going in),
// 60 deg face toward the rear (catches the keyhole edge), 4 mm flat top centred on the keyhole.
key_y=-plate_t+{KEY_Y}; key_x=[dev_off_x-{KEY_PITCH/2},dev_off_x+{KEY_PITCH/2}];
arm_w=8; arm_t=1.8; arm_l=26; arm_gap=1.2; arm_end=key_y+5; arm_root=arm_end-arm_l;
bump_w=5; bump_up=0.6; bump_flat=4; bump_base=tray_z+arm_t; bump_top=floor_top+bump_up; bump_hh=bump_top-bump_base;
module detent_cut(){{for(x=key_x){{
 difference(){{translate([x-arm_w/2-arm_gap,arm_root,tray_z-0.1])cube([arm_w+2*arm_gap,arm_l+arm_gap,tray_t+0.2]);
  translate([x-arm_w/2,arm_root-0.1,tray_z-0.2])cube([arm_w,arm_l+0.1,tray_t+0.4]);}}
 translate([x-arm_w/2-0.01,arm_root+3,bump_base])cube([arm_w+0.02,arm_l-3+0.01,tray_t]);}}}}
module detent_add(){{for(x=key_x)translate([x-bump_w/2,0,0])rotate([90,0,90])linear_extrude(height=bump_w)
 polygon([[key_y-bump_flat/2-bump_hh,bump_base],[key_y-bump_flat/2,bump_top],[key_y+bump_flat/2,bump_top],[key_y+bump_flat/2+bump_hh*tan(30),bump_base]]);}}
'''
orig = equipment.template_source
def patched(spec):
    t = orig(spec)
    old = '  device_features_cut();'
    assert t.count(old) == 1
    t = t.replace(old, old + '\n  detent_cut();')
    old = ' else if(part=="tray")tray();'
    assert t.count(old) == 1
    t = t.replace(old, ' else if(part=="tray")union(){tray();detent_add();}')
    return t + DETENT
equipment.template_source = patched
f = equipment.render(SPEC, sys.argv[1])
print(f.name, json.load(open(f / 'revision.json'))['parts'])
