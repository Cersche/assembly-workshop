from pathlib import Path
p=Path('outputs/Mechanical_Design_App/index.html');p.write_text(p.read_text(encoding='utf-8').replace('/workspace.css?v=3','/workspace.css?v=4'),encoding='utf-8')
