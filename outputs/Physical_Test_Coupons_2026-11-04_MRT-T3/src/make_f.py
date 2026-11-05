"""Generates MRT-F.scad from MRT-E.scad: screw-on covers over the cable channels, M3 insert pillars on the tray and jig. Plate and shoes unchanged."""
import pathlib
s = pathlib.Path('MRT-E.scad').read_text(encoding='utf-8')
def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)
rep(s.split('\n')[0], '// MRT-F (2026-11-04): MRT-E plus three screw-on covers over the cable channels and the M3 insert pillars that hold them. Channel layout unchanged. Plate still MRT-E-P, shoes still MRT-C-L / MRT-C-R.')
rep('// part: plate, tray, jig, slice, shoe_left', '// part: plate, tray, cover_j, cover_o, cover_i, jig, slice, shoe_left')
rep('id="MRT-E";', 'id="MRT-F";')
rep('module tray(){difference(){', r'''// ---- Channel covers. M3 countersunk screw down through the cover into an M3 x 3 x 5 insert (4.2 bore, 4 deep) in a 9.5 pillar on the channel's outer wall face.
// Below the insert, a 3.4 clearance hole so a longer screw won't bottom out. Screw length on hand UNKNOWN. Fit, retention and strength UNKNOWN.
cov_t=3; cov_off=2.75; pil_d=9.5; cov_ear=11; csk_d=6.6; csk_h=1.8; screw_clear=3.4; relief=12;
ri=R-chan/2-wall_t-cov_off; ro=R+chan/2+wall_t+cov_off; cov_w=chan/2+wall_t;
function pol(c,a,r)=[c[0]+r*cos(a),c[1]+r*sin(a)];
cov_j=[pol(c_jump,12,ri),pol(c_jump,55,ro),[c_jump[0]-30,c_jump[1]+R+cov_w+cov_off]];
cov_o=[pol(c_out2,-80,ri),pol(c_out2,-40,ro),[c_out2[0]+R+cov_w+cov_off,196]];
cov_i=[[split_wall+cov_off,90],pol(c_in,240,ro),pol(c_in,255,ri),[c_in[0]-R+cov_w+cov_off,196]];
cov_all=concat(cov_j,cov_o,cov_i);
module sector2d(c,a0,da,r0,r1){n=48;translate(c)polygon(concat([for(i=[0:n])let(a=a0+da*i/n)[r1*cos(a),r1*sin(a)]],[for(i=[n:-1:0])let(a=a0+da*i/n)[r0*cos(a),r0*sin(a)]]));}
module cov2d(pts){offset(r=-2)offset(r=2)union(){children();for(p=pts)translate(p)circle(d=cov_ear);}}
module cov_solid(pts,tag,tp,ta){difference(){
  translate([0,0,wall_top])linear_extrude(cov_t)cov2d(pts)children();
  for(p=pts)translate([p[0],p[1],wall_top-1]){cylinder(d=screw_clear,h=cov_t+2);translate([0,0,1+cov_t-csk_h])cylinder(d1=screw_clear,d2=csk_d,h=csk_h+0.01);}
  translate([tp[0],tp[1],wall_top+cov_t-0.6])rotate(ta)linear_extrude(1)text(tag,size=4,font="Liberation Sans:style=Bold",halign="center",valign="center");
}}
module cover_j(){cov_solid(cov_j,"MRT-F-C1",[c_jump[0]-14,c_jump[1]+R],0){sector2d(c_jump,0,90,R-cov_w,R+cov_w);translate([c_jump[0]-34,c_jump[1]+R-cov_w])square([34.01,2*cov_w]);}}
module cover_o(){cov_solid(cov_o,"MRT-F-C2",[c_out2[0]+R,188],90){sector2d(c_out2,-90,90,R-cov_w,R+cov_w);translate([c_out2[0]+R-cov_w,c_out2[1]-0.01])square([2*cov_w,bar_y1-c_out2[1]]);}}
module cover_i(){cov_solid(cov_i,"MRT-F-C3",[11,130],90){sector2d(c_in,180,90,R-cov_w,R+cov_w);translate([c_in[0]-R-cov_w,c_in[1]-0.01])square([2*cov_w,bar_y1-c_in[1]]);translate([tx0,70])square([split_wall-tx0,bar_y1-70]);}}
module cov_pillars(z0){for(p=cov_all)translate([p[0],p[1],z0])cylinder(d=pil_d,h=wall_top-z0);}
module cov_bores(){for(p=cov_all)translate([p[0],p[1],0]){translate([0,0,wall_top-ins_dp])cylinder(d=ins_d,h=ins_dp+1);translate([0,0,wall_top-ins_dp-relief])cylinder(d=screw_clear,h=relief+0.01);}}
module tray(){difference(){''')
rep('    channels();\n    // ScreenBeam', '    channels();\n    cov_pillars(fl_z);\n    // ScreenBeam') if '    channels();\n    // ScreenBeam' in s else None
if 'cov_pillars(fl_z);' not in s:
    rep('    channels();\n', '    channels();\n    cov_pillars(fl_z);\n')
rep("  // ScreenBeam foot pockets\n  for(f=sb_feet)translate([f[0],f[1],case_z-foot_dp])cylinder(d=foot_d,h=foot_dp+pad);\n  // Velcro", "  cov_bores();\n  // ScreenBeam foot pockets\n  for(f=sb_feet)translate([f[0],f[1],case_z-foot_dp])cylinder(d=foot_d,h=foot_dp+pad);\n  // Velcro")
rep('    channels(); rear_rib();\n', '    channels(); rear_rib(); cov_pillars(fl_top-jf);\n')
rep("  translate([xc,c_in[1]+35,fl_top-0.6])linear_extrude(1)text(\"MRT-T1\"", "  cov_bores();\n  translate([xc,c_in[1]+35,fl_top-0.6])linear_extrude(1)text(\"MRT-T3\"")
rep('module sector2d(c,a0,da,r0,r1){n=24;', 'module sector2d_old(c,a0,da,r0,r1){n=24;')
rep('if(part=="jig")jig();', 'if(part=="cover_j")cover_j();\nif(part=="cover_o")cover_o();\nif(part=="cover_i")cover_i();\nif(part=="jig")jig();')
rep('// ---- MRT-T1 channel forming jig:', '// ---- MRT-T3 channel forming jig (MRT-T1 plus the cover pillars):')
pathlib.Path('MRT-F.scad').write_text(s, encoding='utf-8')
