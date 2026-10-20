from pathlib import Path
p=Path('outputs/Mechanical_Design_App/index.html');s=p.read_text(encoding='utf-8').replace("new Event('workshop-dirty')","new CustomEvent('workshop-dirty',{detail:null})");p.write_text(s,encoding='utf-8')
