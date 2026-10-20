from pathlib import Path
import zipfile
root=Path('outputs/Mechanical_Design_App')
p=root/'README.md';s=p.read_text(encoding='utf-8')+'''\n\n## Version 0.6.1 — joint-focus correction\n\nBrian's screenshot confirmed selected hardware reached the viewer but revealed the faceplate obstructed the close-up. Reveal right joint now resets the camera angle and zoom to 2.5, shows tray/hardware, and hides the faceplate. Full assembly restores both parts and the original camera/zoom. The visibility checkbox reflects the change and can be overridden. No saved project, catalog or model data is changed by these controls.\n\nThe mocked-canvas regression verifies faceplate hiding, hardware visibility, useful zoom and restoration. JavaScript syntax checks pass. A live visual check of the corrected view remains pending. Phase 4 of 7 remains in progress.\n''';p.write_text(s,encoding='utf-8')
with zipfile.ZipFile('outputs/Mechanical_Design_App_Beta_0_6_1.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in root.iterdir():
  if p.is_file():z.write(p,Path(root.name)/p.name)
with zipfile.ZipFile('outputs/Mechanical_Design_App_Beta_0_6_1.zip') as z:assert z.testzip() is None
print('Beta 0.6.1 archive validated.')
