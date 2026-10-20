from pathlib import Path
import zipfile
root=Path('outputs/Mechanical_Design_App')
p=root/'README.md';s=p.read_text(encoding='utf-8');s+='''\n\n## Version 0.3 — joint axial geometry\n\nSave & check now shows a to-scale axial preview of screw length, insert body length and available bore depth. Geometry JSON can be exported. Open inserts now receive a separate screw-tip/bore-envelope check, while physical bottom clearance remains unknown. The assumed continuous bore and entered stack are stated in the preview; this is not a full 3D geometry check. No CAD/STL modifications occur.\n\nFor the screenshot combination (10 mm screw, 4.3 mm insert, 3.3 mm stack and 8 mm available bore), the computed reach is 6.7 mm, extension beyond the insert body is 2.4 mm and modeled bore-end gap is 1.3 mm. Actual usable thread depth and insert outside diameter are still not verified from the accessible supplier source. We do not substitute body length for usable thread depth. The original 4.2 mm pilot still fails the supplier maximum check.\n\nEight automated tests pass, covering the geometry endpoint and open-insert bore overrun. Desktop/browser inspection was not performed. Update by stopping the server, replacing application files while retaining data/, restarting and refreshing the browser.\n''';p.write_text(s,encoding='utf-8')
with zipfile.ZipFile('outputs/Mechanical_Design_App_Beta_0_3.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in root.iterdir():
  if p.is_file():z.write(p,Path(root.name)/p.name)
with zipfile.ZipFile('outputs/Mechanical_Design_App_Beta_0_3.zip') as z:assert z.testzip() is None
print('Beta 0.3 packaged and archive validated.')
