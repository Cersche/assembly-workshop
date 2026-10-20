from pathlib import Path
import json
root=Path('outputs/Mechanical_Design_App');records=[]
for length,number in [(6,3817),(8,3818),(10,3819)]:
 pn=f'SSCF-M3-{length}-A2'
 records.append(dict(id='accu-'+pn.lower(),revision=1,name=f'Accu M3 × {length} socket cap · A2',kind='screw',manufacturer='Accu',part_number=pn,diameter=3,pitch=.5,length=length,threaded_length=length,length_convention='under_head',head_diameter=5.5,head_height=3,drive='2.5 mm hex',material='A2 stainless steel',finish='Natural',verification='documented',source=f'https://www.accu.co.uk/metric-cap-head-screws/{number}-{pn}',retrieved='2026-10-17',availability='Not checked',cad_status='Supplier CAD link only; no model downloaded',notes='Nominal dimensions; head diameter tolerance +0/-0.18 mm, height +0/-0.14 mm. Full-thread specification from supplier.'))
for length,pn in [(3.4,'94459A769'),(4.3,'94459A130'),(5.7,'94459A140')]:
 records.append(dict(id='mcmaster-'+pn.lower(),revision=1,name=f'McMaster M3 heat-set · {length} mm',kind='heatset',part_number=pn,diameter=3,pitch=.5,length=length,hole_max_diameter=4,hole_profile='straight',end_type='open',material='Brass',verification='partial',source='https://www.mcmaster.com/products/94459a170/',retrieved='2026-10-17',availability='Not checked',cad_status='No CAD downloaded',notes='Catalog standard-profile brass row. 4 mm is For Max. Hole Dia., not an exact installation target. Outside diameter, usable thread depth and minimum wall remain unverified.'))
(root/'starter-hardware.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
