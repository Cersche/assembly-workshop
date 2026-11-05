import pathlib
s=pathlib.Path('MRT-C.scad').read_text(encoding='utf-8')
def rep(a,b):
    global s
    assert s.count(a)==1,a
    s=s.replace(a,b)
rep(s[:s.index('\n')],'// MRT-D (2026-11-04): MRT-C tray with the thin rear bar replaced (Brian: too thin to hold stiff coax). Channels and floor run back to a notched rear rib. Shoes unchanged, still MRT-C-L / MRT-C-R.')
rep('id="MRT-C";','id="MRT-D";')
rep('wall_y(c_out2[0]+R-chan/2-wall_t,c_out2[1]-0.01,depth);','wall_y(c_out2[0]+R-chan/2-wall_t,c_out2[1]-0.01,bar_y1);')
rep('wall_y(c_out2[0]+R+chan/2,c_out2[1]-0.01,depth);','wall_y(c_out2[0]+R+chan/2,c_out2[1]-0.01,bar_y1);')
rep('wall_y(c_in[0]-R-chan/2-wall_t,c_in[1]-0.01,depth);','wall_y(c_in[0]-R-chan/2-wall_t,c_in[1]-0.01,bar_y1);')
rep('wall_y(c_in[0]-R+chan/2,c_in[1]-0.01,depth);','wall_y(c_in[0]-R+chan/2,c_in[1]-0.01,bar_y1);')
rep('    translate([tx0,bar_y0,fl_z])cube([tx1-tx0,bar_y1-bar_y0,fl_top-fl_z]);\n','''    translate([tx0,bar_y0,fl_z])cube([tx1-tx0,bar_y1-bar_y0,fl_top-fl_z]);
    // floor carried back under the cords, coax IN and coax OUT
    translate([tx0,depth-6,fl_z])cube([c_in[0]-R+chan/2+wall_t-tx0,bar_y0-depth+6.01,fl_top-fl_z]);
    translate([c_out2[0]+R-chan/2-wall_t,depth-6,fl_z])cube([chan+2*wall_t,bar_y0-depth+6.01,fl_top-fl_z]);
    rear_rib();
''')
rep('module tray(){difference(){','''// ---- Rear rib: a stiff wall across the back. Each run sits in a notch and presses past a 45 deg lip, so the rib takes the cable's push, not a tie.
rib_y0=bar_y1-4; rib_top=18; lip_u=12.5;
module rib_lip(f,p){translate([0,bar_y1,0])rotate([90,0,0])linear_extrude(bar_y1-rib_y0)polygon([[f-0.4,lip_u],[f,lip_u],[f+p,lip_u+p],[f+p,rib_top],[f-0.4,rib_top]]);}
module rear_rib(){
  difference(){
    translate([tx0,rib_y0,fl_top-0.01])cube([tx1-tx0,bar_y1-rib_y0,rib_top-fl_top+0.01]);
    for(n=[[tx0+side_t,split_wall-wall_t],[c_in[0]-R-chan/2,c_in[0]-R+chan/2],[c_out2[0]+R-chan/2,c_out2[0]+R+chan/2]])
      translate([n[0],rib_y0-1,fl_top])cube([n[1]-n[0],bar_y1-rib_y0+2,rib_top]);
  }
  rib_lip(tx0+side_t,lip_pl); rib_lip(c_in[0]-R-chan/2,lip_p); rib_lip(c_out2[0]+R-chan/2,lip_p);
}
module tray(){difference(){''')
rep('''  for(x=[11,c_in[0]-R,c_out2[0]+R]){tie([x,(bar_y0+bar_y1)/2],90,5.5);tie_groove([x,(bar_y0+bar_y1)/2],90,5.5);}
''','''  for(t=[[(tx0+side_t+split_wall-wall_t)/2,5.5],[c_in[0]-R,3.5],[c_out2[0]+R,3.5]]){tie([t[0],186],90,t[1]);tie_groove([t[0],186],90,t[1]);}
''')
rep('  // tie slots in the rear bar for the cords and both coax runs','  // tie slots in the floor behind the tray, inside each channel')
pathlib.Path('MRT-D.scad').write_text(s,encoding='utf-8')
c=pathlib.Path('check_c.py').read_text(encoding='utf-8').replace('MRT-C','MRT-D').replace("'screenbeam', 'splitter', 'cables'","'cables'").replace("'shoe_left', 'shoe_right', ","")
pathlib.Path('check_d.py').write_text(c,encoding='utf-8')
t=pathlib.Path('clash_c.py').read_text(encoding='utf-8').replace('MRT-C.scad','MRT-D.scad').replace('python clash_c','python clash_d')
i=t.index("for name, a, b in [");
t=t[:i]+"""for name, a, b in [
    ('CONTROL cables 2 left x tray (must overlap)', T('[-2,0,0]', 'cables'), S['tray']),
    ('tray x shoe L', S['tray'], S['bl']), ('tray x shoe R', S['tray'], S['br']), ('tray 16 forward x shoe L', T('[0,-16,0]', 'tray'), S['bl']),
    ('tray x rear post L', S['tray'], S['rpL']), ('cables x tray', S['cables'], S['tray']), ('cables x shoe L', S['cables'], S['bl']), ('cables x shoe R', S['cables'], S['br']),
    ('devices x tray', S['dev'], S['tray'])]:
    print(name, '=>', go(a, b), flush=True)
"""
pathlib.Path('clash_d.py').write_text(t,encoding='utf-8')
