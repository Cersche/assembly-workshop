from pathlib import Path
p=Path('work/test_viewer_v06.cjs');s=p.read_text().replace("elements['show-faceplate','show-hardware','hardwareStatus']", "elements['show-faceplate']");p.write_text(s)
