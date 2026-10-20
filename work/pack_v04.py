from pathlib import Path
import zipfile
root=Path('outputs/Mechanical_Design_App')
p=root/'README.md';s=p.read_text(encoding='utf-8');s+='''\n\n## Version 0.4 — Phase 4 of 7\n\nThe app displays the seven-phase roadmap with Phase 4 (geometry integration) in progress and three phases complete. This is milestone position, not a percentage-of-effort estimate.\n\nThe axial preview loads on startup and updates automatically when selections or dimensions change. Draft previews do not save or change project selections; Save project and Save & check remain explicit persistence actions. Exports save current inputs first. Pending preview responses are discarded when a newer edit is made. A bore envelope is visible even before hardware is selected. This also addresses the blank initial preview shown in the previous screenshot.\n\nNine backend tests pass, including HTTP preview handling and confirmation that drafts never alter the saved project. Frontend JavaScript passes Node syntax checking. This update has not been visually inspected in a live browser. No desktop access, printer actions or manufacturing geometry changes occurred.\n\nUpdate: stop the server, replace application files while retaining data/, restart start.bat, and refresh the browser. Next Phase 4 milestone is integrating actual assembly/reference geometry; this release still uses an axial model.\n''';p.write_text(s,encoding='utf-8')
with zipfile.ZipFile('outputs/Mechanical_Design_App_Beta_0_4.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in root.iterdir():
  if p.is_file():z.write(p,Path(root.name)/p.name)
with zipfile.ZipFile('outputs/Mechanical_Design_App_Beta_0_4.zip') as z:assert z.testzip() is None
print('Beta 0.4 package validated.')
