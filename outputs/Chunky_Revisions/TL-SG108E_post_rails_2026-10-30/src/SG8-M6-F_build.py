"""SG8-M6-F (2026-10-30): TP-Link TL-SG108E tray hung on two post rails ("cheeks" in the source) (concept A, Brian's pick).
Each post rail bolts to the front post with 3 x M6 x 8 (middle front-flange hole from behind + both side-flange holes).
The tray slides in from the front on two runners that ride the cheeks' 45 deg ledges; the faceplate is a cover only
(no bosses, no load): it keeps the tray from sliding forward, the cheeks' rear stops keep it from going back.
Switch fit is SG8-M6-D's (device 158 x 100 x 25, offset X -15, side play 0.5, top 1.35, 1.3 set back, detents, rear stop,
flush window, keystone +88, UPLINK inlay). Built by patching D's exact source. Fit, strength, inserts: UNKNOWN.
Usage: python SG8-M6-F_build.py <out_dir>   (writes src/SG8-M6-F.scad, STLs into out_dir)"""
import pathlib, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'AGENTS.md').exists())
D_SCAD = ROOT / 'outputs/TL-SG108E_M6_2026-10-28/previous_SG8-M6-D/SG8-M6-D.scad'
OPENSCAD = r'C:/Program Files/OpenSCAD/openscad.exe'

F = r'''
// ---- SG8-M6-F (2026-10-30): tray hangs on two post cheeks; the faceplate is a cover only. Fit/strength UNKNOWN.
// Frame: X centred, plate back Y=0, Z=0 slot bottom. u = |X| (cheek/runner profiles are drawn for the right side, s=+1).
// Post (Lab Rax 1U, measured from the creator mesh, local only): front flange Y 0..6 for u 111.1..141.1, holes O7.6 at
// u 118.2625, Z 6.32 / 22.225 / 38.13 (faceplate uses the outer two); side flange u 134.1..139.6, Y 6..35, holes O7.6 on the
// X axis at Y 22.5, Z 22.225 -/+ 12.23 -- BUT Brian's rack uses the 4U posts: at U8 (mid-post) the side wall is solid, 14 mm,
// inner face u 127.12, no holes (side holes only near post ends). So: one screw per rail (middle hole) + the plate joint.
// Inner corner fillet: u >= 125.2 at Y 6.2, out to u 127.1 up to Y ~11.3, so the rail stays at u <= 125 in front of Y 11.8. M6 heat-set inserts assumed in all used holes.
win_drop=0.3;              // window bottom 0.3 below the tray floor top: tolerance for the tray resting on the ledges
tr_front=0.3;              // tray front 0.3 behind the plate back (plate only stops it sliding forward)
run_y1=80.3;               // runner rear end (ahead of the tray's R20 rear corners)
ru0=100.5; ru1=102; rb=107.5; rz_bot=1.5; rz_mid=9.0; ri=103.5;   // runner profile (u,z)
cl_bear=0.1; cl=0.25;      // ledge under the runner's 45 deg bearing face / everywhere else
ch_in=103; ch_wall=111; ch_out=126.9; ch_z0=0.5; ch_z1=44.0; ch_y0=6.2; ch_y0b=11.8; ch_blk=38; ch_y1=85;
stop_y=run_y1+0.3;
post_x=118.2625; mid_z=22.225; face_dz=15.902; side_y=22.5; side_dz=12.23;
m6_clear=6.6; m6_head=11.5; web=2.5; relief_d=9; relief_l=10;
module runner_profile(){polygon([[ru0,0.5],[ru1,0.5],[ru1,rz_bot],[rb,rz_bot+rb-ru1],[rb,rz_mid],[ri,rz_mid+rb-ri],[ru0,rz_mid+rb-ri]]);}
module along_y(y0,y1){translate([0,y1,0])rotate([90,0,0])linear_extrude(height=y1-y0)children();}
module runner(s){scale([s,1,1])along_y(tr_front,run_y1)runner_profile();}
// Right side: floor wing under the keystone (keystone block bottom Z 7.2) out to the runner.
module wing(){translate([70.5,tr_front,tray_z])cube([ru0-70.5+0.01,run_y1-tr_front,6.0]);}
// Lip notch under each plate boss (boss Y 0..8, upright from Y 8.3): 0.3 clear each side.
module lip_notch(){for(x=hs_x)translate([x-6.3,-1,sl_window_top-0.1])cube([12.6,9.3,sl_lip+0.2]);}
module tray_f(){intersection(){
 difference(){union(){tray();detent_add();top_uprights();for(s=[-1,1])runner(s);wing();}tray_id();lip_notch();}
 union(){tray_round();translate([0,0,-1])linear_extrude(200)translate([0,(tr_front+run_y1)/2])rrect(2*rb,run_y1-tr_front,4);}
 translate([-200,tr_front,-1])cube([400,300,100]);
}}
// Channel the runner slides in: bearing face cl_bear below the runner's, cl clear on the outer face and the hold-down slope.
module channel_profile(){
 polygon([[ru1-1,rz_bot-cl_bear-1],[rb,rz_bot+rb-ru1-cl_bear],[rb+cl,rz_bot+rb-ru1-cl_bear],
          [rb+cl,rz_mid+cl*1.4-cl],[ru1-1,rz_mid+cl*1.4+rb-ru1+1]]);}
module cheek_id(s){translate([ch_in+0.6,60,26])rotate([90,0,-90])linear_extrude(1)mirror([s<0?1:0,0])
 text("SG8-M6-F",size=4.5,font="Liberation Sans:style=Bold",halign="center",valign="center");}
module cheek(s){scale([s,1,1])difference(){
 union(){
  translate([ch_in,ch_y0,ch_z0])cube([ch_wall-ch_in,ch_y1-ch_y0,ch_z1-ch_z0]);              // wall + ledge
  translate([ch_in,ch_y0,ch_z0])cube([125-ch_in,ch_blk-ch_y0,ch_z1-ch_z0]);                // block behind the front flange
  translate([125-0.01,ch_y0b,ch_z0])cube([ch_out-125+0.01,ch_blk-ch_y0b,ch_z1-ch_z0]);     // braced against the 4U post's side wall (0.22 gap)
 }
 along_y(ch_y0-1,stop_y)channel_profile();
 // Front flange middle hole, screw from behind: 2.5 web, head pocket open to the rear.
 translate([post_x,ch_y0-0.1,mid_z])rotate([-90,0,0])cylinder(d=m6_clear,h=web+0.2,$fn=48);
 translate([post_x,ch_y0+web,mid_z])rotate([-90,0,0])cylinder(d=m6_head,h=ch_blk,$fn=64);
 // Room for the faceplate screw tips / inserts in the outer two front holes.
 for(dz=[-face_dz,face_dz])translate([post_x,ch_y0-0.1,mid_z+dz])rotate([-90,0,0])cylinder(d=relief_d,h=relief_l,$fn=48);
 cheek_id(s);
}}
'''

def patch(t):
    def rep(old, new, n=1):
        nonlocal t
        assert t.count(old) == n, (old, t.count(old))
        t = t.replace(old, new)
    # Brian, 2026-10-30: keep D's hidden M6 plate joint as well (U8 posts have no side holes). Bosses moved off the sleeve
    # walls (over the switch, 0.4 above its top) so they never sit on a wall; the sleeve lip is notched under each boss.
    rep('hs_x=[dev_off_x-sl_half-sl_wall+8, dev_off_x+sl_half+sl_wall-8];', 'hs_x=[-88, 56];')
    rep('text("SG8-M6-D"', 'text("SG8-M6-F"')
    # Brian, 2026-10-30: no strap slots on this tray (wall notches + floor slots under the walls); unused, a pain to print.
    rep(' if(sleeve)for(side=[-1,1],y=[dev_y+fp_d*0.25,dev_y+fp_d*0.75])', ' if(false)for(side=[-1,1],y=[dev_y+fp_d*0.25,dev_y+fp_d*0.75])')
    rep('y=[dev_y+fp_d*0.25,dev_y+fp_d*0.75])\n  translate([x,y-6,tray_z-0.1])', 'y=[dev_y+fp_d*0.25,dev_y+fp_d*0.75])\n  if(false)translate([x,y-6,tray_z-0.1])')
    rep('translate([dev_off_x,(sl_bottom+sl_window_top)/2])square([2*sl_half,sl_window_top-sl_bottom],center=true);',
        'translate([dev_off_x,(sl_bottom-win_drop+sl_window_top)/2])square([2*sl_half,sl_window_top-sl_bottom+win_drop],center=true);')
    rep(' else if(part=="tray")intersection(){difference(){union(){tray();detent_add();top_uprights();}tray_id();}tray_round();}',
        ' else if(part=="tray")tray_f();\n else if(part=="cheek_left")cheek(-1);\n else if(part=="cheek_right")cheek(1);\n'
        ' else if(part=="assembly")union(){color("steelblue")difference(){faceplate();plate_id();}color("silver")tray_f();color("orange"){cheek(-1);cheek(1);}}')
    return t + F

def main(out):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    scad = HERE / 'SG8-M6-F.scad'
    scad.write_text(patch(D_SCAD.read_text(encoding='utf-8')), encoding='utf-8')
    for part, name in [('faceplate', 'SG8-M6-F_faceplate'), ('tray', 'SG8-M6-F_tray'),
                       ('cheek_left', 'SG8-M6-F_post-rail_left'), ('cheek_right', 'SG8-M6-F_post-rail_right')]:
        r = subprocess.run([OPENSCAD, '-o', str(out / f'{name}.stl'), '-D', f'part="{part}"', str(scad)],
                           capture_output=True, text=True)
        print(name, r.returncode, [l for l in r.stderr.splitlines() if 'WARNING' in l or 'ERROR' in l][:5])

if __name__ == '__main__':
    main(sys.argv[1])
