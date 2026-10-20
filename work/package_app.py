from pathlib import Path
import zipfile
root=Path('outputs/Mechanical_Design_App')
p=root/'README.md';s=p.read_text().replace('loopback HTTP routes, session-token enforcement and exports.','HTTP request handlers in memory, session-token enforcement and exports. The five tests pass. An attempted live loopback HTTP integration test was blocked by Windows socket permissions in this execution environment; end-to-end browser operation remains unverified.')
p.write_text(s,encoding='utf-8')
p=Path('outputs/Mechanical_Design_App_Beta_Spec.md');s=p.read_text(encoding='utf-8-sig')
s=s.replace('Preserve this as an unresolved migration item. Do not claim that all original features were retained.','The user has explicitly waived recovery of the original requirements. This specification is the new baseline; recovering the original app is not a prerequisite.')
s=s.replace('| Application framework and original feature migration | Unresolved; inspect supplied original app before choosing architecture |','| Original app recovery | Waived by the user; use this specification as the baseline |')
s=s.replace('Keep the storage implementation behind an adapter until the original app architecture is available.','Keep the storage implementation behind an adapter so the geometry engine and UI can evolve independently.')
s=s.replace('1. Recover the original application description/source and reconcile its feature list with this spec. Preserve original files. Identify the actual framework before implementation.','1. Build from this specification as the approved baseline. Initial implementation: local Python/SQLite service and browser UI, with geometry operations added through adapters.')
p.write_text(s,encoding='utf-8')
with zipfile.ZipFile('outputs/Mechanical_Design_App_Beta_0_1.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in root.iterdir():
  if p.is_file():z.write(p,Path(root.name)/p.name)
 assert z.testzip() is None
print('App package created. Source and documentation included; no database or runtime cache bundled.')
