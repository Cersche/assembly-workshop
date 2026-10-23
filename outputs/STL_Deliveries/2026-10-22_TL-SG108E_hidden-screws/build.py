"""TL-SG108E hidden-screw variant (hand-made delivery, not an app feature).

The app's hidden joint puts the joint blocks outside the sleeve walls (max 150 mm devices).
Here the switch is set back SETBACK mm inside the sleeve so the joint blocks sit in FRONT of
it, inside the sleeve footprint; the plate window is narrowed to the port cavity so the plate
stays solid at the bosses; the rear stop is removed so the switch loads from the rear and
stops against the joint uprights. Run: python build.py  (from this folder)
"""
import json, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
APP = HERE.parents[1] / 'Mechanical_Design_App'
sys.path.insert(0, str(APP))
import equipment as eq

SETBACK = 17      # device front moves from y=-4 to y=13 (joint upright ends at 11.3)
WIN_HALF = 65     # plate window half-width: 128 mm port cavity (centred, from STEP) + 1 mm
SPEC = {"dev_w": 158, "dev_d": 101, "dev_h": 25, "u": 1, "device_mount": "sleeve", "joint": "screw",
        "dev_off_x": -15, "keystones": [88], "tray_follow": True, "sleeve_top": 0.8,
        "labels": [{"text": "UPLINK", "x": 88, "z": 3.8, "size": 4.5}]}
PATCHES = [
    # tray no longer widens for joints outside the walls
    ('hidden_joint?sl_side+sl_wall+hj_gap+2*hj_half:0)', '0)'),
    # tray deeper by the setback
    ('sleeve?-plate_t+fp_d+margin:', f'sleeve?-plate_t+{SETBACK}+fp_d+margin:'),
    ('dev_y=sleeve?-plate_t:', f'dev_y=sleeve?-plate_t+{SETBACK}:'),
    # joints just outside the narrowed window, in front of the device
    ('hj_x=[dev_off_x-sl_half-sl_wall-hj_gap-hj_half,dev_off_x+sl_half+sl_wall+hj_gap+hj_half];',
     f'hj_x=[dev_off_x-{WIN_HALF}-hj_gap-hj_half,dev_off_x+{WIN_HALF}+hj_gap+hj_half];'),
    ('if(sleeve)translate([dev_off_x,(sl_bottom+sl_window_top)/2])square([2*sl_half,',
     f'if(sleeve)translate([dev_off_x,(sl_bottom+sl_window_top)/2])square([{2*WIN_HALF},'),
    # no rear stop: switch loads from the rear
    ('  translate([dev_x,sl_rear,floor_top])cube([fp_w,sl_stop_t,min(sl_stop_h,dev_h-foot_h)]);\n', ''),
]

clean = eq.clean(SPEC)
clean['hidden_joint'] = True  # set after clean(): its width check assumes joints outside the walls
src = eq.source(clean)
# tray_follow appends tray_w/tray_x computed with the outside-joint width; replace with plain sleeve width
PATCHES.append(('tray_w=211.0;\ntray_x=-120.5;', 'tray_w=171.0;\ntray_x=-100.5;'))
for old, new in PATCHES:
    assert src.count(old) == 1, old
    src = src.replace(old, new)
scad = HERE / 'TL-SG108E_hidden-screws.scad'
scad.write_text(src, encoding='utf-8', newline='\n')
exe = 'C:/Program Files/OpenSCAD/openscad.exe'
for part in ('faceplate', 'tray'):
    out = HERE / f'TL-SG108E_1U_hidden-screws_{part}.stl'
    subprocess.run([exe, '-o', str(out), '-D', f'part="{part}"', str(scad)], check=True)
print(json.dumps(SPEC))
