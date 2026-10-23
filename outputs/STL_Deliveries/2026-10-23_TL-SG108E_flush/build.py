"""TL-SG108E flush+lip: switch 1.5 mm back, faceplate side lips retain it at the front. Delivery-only patch."""
import sys, json
sys.path.insert(0, r'D:/Projects/assembly-workshop/outputs/Mechanical_Design_App')
import equipment
SPEC = {'name':'TP-Link TL-SG108E','dev_w':158,'dev_d':100,'dev_h':25,'u':1,'device_mount':'sleeve','joint':'screw','rear_support':False,
        'dev_rot':0,'dev_off_x':-15,'dev_off_y':0,'holes':[],'ports':[],'rear_ports':[],'keystones':[88],'tray_follow':True,'sleeve_top':0.8,
        'labels':[{'text':'UPLINK','x':88,'z':3.8,'size':4.5}]}
LIP_T, LIP_W, SETBACK = 1.5, 4.0, 1.8  # 0.3 mm front-to-back play
orig = equipment.template_source
def patched(spec):
    t = orig(spec)
    old = 'dev_y=sleeve?-plate_t:front_gap+dev_off_y;'
    assert t.count(old) == 1
    t = t.replace(old, f'dev_y=-plate_t+{SETBACK};')
    old = '  if(ks_style!="v2")ks_golden();'
    assert t.count(old) == 1
    t = t.replace(old, old + '\n  front_lips();')
    return t + f'''
// Front retention (Brian, 2026-10-23): {LIP_T} mm lips over {LIP_W} mm of the case's left/right ends, in front of the
// switch, which sits {SETBACK} mm back. Assumes the ports leave >= {LIP_W} mm of plain case at each end (UNKNOWN, not measured).
module front_lips(){{for(sx=[-1,1])translate([dev_off_x+sx*(sl_half-{LIP_W}/2)-{LIP_W}/2,-plate_t,sl_bottom])cube([{LIP_W},{LIP_T},sl_window_top-sl_bottom]);}}
'''
equipment.template_source = patched
f = equipment.render(SPEC, sys.argv[1])
print(f.name, json.load(open(f / 'revision.json'))['parts'])
