from pathlib import Path
import hashlib,json,shutil
src=Path(r'C:/Users/brian/AppData/Local/Temp/codex-clipboard-fa256ece-9d21-4932-8648-a46dab5babaf.png')
dst=Path('work/hardware-evidence/94459A140/user-supplied-reference-drawing.png')
if dst.exists():
    assert dst.read_bytes()==src.read_bytes(),'Refusing to overwrite differing evidence'
else:shutil.copy2(src,dst)
record={
 'date':'2026-10-18','part_number':'94459A140','supplier':'McMaster-Carr',
 'source_type':'User-supplied screenshot of exact-part supplier reference drawing; not original PDF',
 'local_asset':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),
 'drawing_note':'All dimensions are for reference only.',
 'observed_reference_dimensions_mm':{'knurled_outer_extent':4.72,'overall_length':5.74,'lower_section_outer_extent':3.91},
 'thread':{'diameter_mm':3,'pitch_mm':0.5},
 'supplier_installation_metadata':{'drill_bit_designation':'No. 22','maximum_hole_diameter_mm':4,'minimum_material_thickness_mm':6.5},
 'interpretation_limits':[
   'Outer extents are reference/nominal dimensions, not certified maximum diameters.',
   'No dimensional tolerances or usable threaded depth are supplied in this image.',
   '6.5 mm minimum material thickness must not be mapped to radial min_wall.',
   'Catalog 5.7 mm installed length and drawing 5.74 mm overall length have different labels; no tolerance or equality is inferred.',
   '3.91 mm lower-section extent is not a recommended pilot diameter.',
   'Physical fit, installation applicability and strength remain UNKNOWN.'
 ],
 'catalog_revision_changed':False,'project_pins_changed':False,'geometry_changed':False,
 'redistribution':'Local evidence retained; no permission to redistribute supplier drawing inferred.'}
Path('outputs/Phase7_Hardware_Evidence/94459A140_Drawing_Review.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps({'evidence_saved':True,'sha256':record['sha256'],'catalog_or_geometry_changed':False}))
