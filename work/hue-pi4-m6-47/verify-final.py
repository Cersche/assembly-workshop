from pathlib import Path
import hashlib,json,re,zipfile,xml.etree.ElementTree as ET,subprocess,difflib
R=Path('D:/Projects/assembly-workshop');W=R/'work/hue-pi4-m6-47';O=R/'outputs/Hue_Pi4_M6-B_2026-10-28'
a=(R/'outputs/Hue_Pi4_M6_2026-10-28/src/HP4-M6-A.scad').read_text(encoding='utf-8');b=(O/'src/HP4-M6-B.scad').read_text(encoding='utf-8')
changes=[('tray_x0=-82.5; tray_x1=102;','tray_x0=-102; tray_x1=82.5;'),('cradle_x=-34.5;','cradle_x=34.5;'),('for(x=[16.5,39.5])','for(x=[-42.5,-19.5])'),('keystones=[-92.5];','keystones=[92.5];'),('dev_off_x=-34.5;','dev_off_x=34.5;'),('ports=[[55.0, 26.8, 15.0, 17.5, 1.0], [73.0, 26.8, 15.0, 17.5, 1.0], [91.7, 25.6, 17.5, 15.0, 1.0]];','ports=[[-93.0, 26.8, 15.0, 17.5, 1.0], [-75.0, 26.8, 15.0, 17.5, 1.0], [-56.3, 25.6, 17.5, 15.0, 1.0]];'),('joint_x=[-58.0, -12.0, 29.5];','joint_x=[-29.5, 11.0, 57.0];'),('dev2_off_x=74;  // Pi footprint X 46..102','dev2_off_x=-74;  // Pi footprint X -102..-46'),('translate([-35,0.01,8])','translate([34.5,0.01,8])'),('translate([-35,119,floor_top-0.6])','translate([34.5,119,floor_top-0.6])'),('keystone block -103..-82, tray floor -82.5..+102.','keystone block 82..103, tray floor -102..+82.5; keystone lane right, Pi edge at the left limit.')]
recovered=b.replace('HP4-M6-B','HP4-M6-A')
for old,new in changes:
 assert recovered.count(new)==1,(new,recovered.count(new));recovered=recovered.replace(new,old)
assert recovered==a,'Unlisted source change'
assert a.count('mirror(')==b.count('mirror(')==1
# Register literal per-object XML tag counts, not just namespace-aware parsing.
with zipfile.ZipFile(O/'HP4-M6-B_Hue_Pi4_M6_set.3mf') as z:xml=z.read('3D/3dmodel.model')
assert b'ns0:' not in xml
acc=json.loads((O/'checks/acceptance.json').read_text(encoding='utf-8'))
objects=[]
for raw in re.findall(rb'<object\b.*?</object>',xml,re.S):
 ob=ET.fromstring(raw);name=ob.attrib['name'];part='tray' if name.endswith('tray') else 'faceplate'
 vertices=raw.count(b'<vertex ');triangles=raw.count(b'<triangle ')
 assert triangles==acc[part]['triangles'] and vertices==acc[part]['vertices']
 objects.append({'name':name,'plain_vertex_tags':vertices,'plain_triangle_tags':triangles,'stl_vertices':acc[part]['vertices'],'stl_triangles':acc[part]['triangles']})
assert len(objects)==2
result={'source_scope_passed':True,'allowed_literal_changes':len(changes),'ID_comment_rename':'HP4-M6-A -> HP4-M6-B','mirror_calls_A':1,'mirror_calls_B':1,'mirror_usage':'unchanged to_rear helper only; no translated device/keystone uses it','xml_objects':objects,'ns0_prefixes':0}
(W/'final-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
