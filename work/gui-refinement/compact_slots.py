from pathlib import Path
p=Path('outputs/Mechanical_Design_App/workspace.js');s=p.read_text(encoding='utf-8').replace("sub.textContent=item?'Reference allocation · fit unknown':'Ready for your equipment';","sub.textContent=item?'Fit UNKNOWN':'Available';");p.write_text(s,encoding='utf-8')
