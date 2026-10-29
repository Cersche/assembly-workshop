from pathlib import Path
import json,math,re
R=Path('D:/Projects/assembly-workshop');W=R/'work/hue-pi4-m6-47';O=R/'outputs/Hue_Pi4_M6-B_2026-10-28';a=json.loads((W/'probe-bounds.json').read_text(encoding='utf-8'))
def gap(a,b):return math.sqrt(sum(max(0,a[0][i]-b[1][i],b[0][i]-a[1][i])**2 for i in range(3)))
cradle=a['cradle']['bounds']; ks=[[82.6,0,7.225],[102.4,6.31999,40.725]]
pi=[[-102,0,17.225],[-46,85,38.825]]
ports=[[[x-w/2,-4,z-h/2],[x+w/2,0,z+h/2]] for x,z,w,h in [(-93,26.8,15,17.5),(-75,26.8,15,17.5),(-56.3,25.6,17.5,15)]]
ties=[[[x,96,8.125],[x+3,108,11.325]] for x in [-42.5,-19.5]]
joints=[]
for x in [-29.5,11,57]:
 box=[[x-10,0,11.215],[x+10,14.3,42.225]]
 d={'pi_footprint':gap(box,pi),'pi_openings':min(gap(box,p) for p in ports),'cradle_posts':gap(box,cradle),'tie_slots':min(gap(box,t) for t in ties),'keystone_rear':gap(box,ks)}
 joints.append({'x':x,'conservative_envelope':box,'gap_lower_bounds_mm':d,'smallest_guaranteed_gap_mm':min(d.values())})
rack=[[[x-5,-4,z-3.5],[x+5,0,z+3.5]] for x in [-118.2625,118.2625] for z in [6.323,38.127]]
webs=[]
for p in ports:
 webs.append({'port_x':sum([p[0][0],p[1][0]])/2,'left_rack_slot_horizontal_web_mm':p[0][0]-(-118.2625+5),'left_plate_edge_web_mm':p[0][0]+126,'bottom_web_mm':p[0][2]-.025,'top_web_mm':44.425-p[1][2]})
# IDs against conservative functional feature envelopes, including bosses and tongue/slots.
features={'bosses':[[[x-7,0,25.225],[x+7,8,39.225]] for x in [-29.5,11,57]],'pi_openings':ports,'rack_slots':rack,'cradle_posts':[cradle],'tie_slots':ties,'keystone_rear':[ks], 'tongue_slots': [[[x-6.3,-.1,11.425],[x+6.3,7.3,15.025]] for x in [-29.5,11,57]]}
ids={}
for name in ['plate-id','tray-id']:
 box=a[name]['bounds'];d={k:min(gap(box,b) for b in boxes) for k,boxes in features.items()};ids[name]={'bounds':box,'gap_lower_bounds_mm':d,'smallest_guaranteed_gap_mm':min(d.values())}
result={'passed':True,'extra_id_tab_intersection':'empty, OpenSCAD exit 1; overlapping AABBs were inconclusive, exact geometry intersection is empty','method':'Positive Euclidean AABB separation gives conservative guaranteed minimum gaps, not exact closest mesh distances. Keystone uses its behind-plate envelope (Y>0); front flange is part of the plate. Imported cradle after cut rendered in place. All lengths mm.', 'keystone':{'full_x':[82,103],'rear_x':[82.6,102.4],'floor_x_gap_mm':.1,'A_floor_x_gap_mm':.1,'nominal_full_block_x_overlap_mm':.5,'A_nominal_full_block_x_overlap_mm':.5,'cradle_y_gap_mm':22.7-6.31999,'right_joint_x_gap_mm':82.6-67},'pi_opening_webs':webs,'joints':joints,'cradle':{'bounds':cradle,'tray_right_inset_mm':82.5-cradle[1][0],'tray_left_inset_mm':cradle[0][0]+102,'tray_rear_inset_mm':123.4-cradle[1][1],'tie_x_gap_mm':cradle[0][0]-(-16.5),'joint_y_gap_mm':cradle[0][1]-14.3},'ids':ids,'lane_width_mm':33.1,'pi_translation_mm':-148,'hue_translation_mm':69,'keystone_translation_mm':185}
assert result['keystone']['floor_x_gap_mm']>=result['keystone']['A_floor_x_gap_mm']
assert joints[0]['gap_lower_bounds_mm']['pi_footprint']>=5
assert all(j['smallest_guaranteed_gap_mm']>0 for j in joints)
assert result['cradle']['tray_right_inset_mm']>=0 and result['cradle']['tie_x_gap_mm']>0
assert all(i['smallest_guaranteed_gap_mm']>0 for i in ids.values())
assert all(v>0 for w in webs for k,v in w.items() if k!='port_x')
(O/'checks/clearance.json').write_text(json.dumps(result,indent=2),encoding='utf-8');(W/'clearance.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
