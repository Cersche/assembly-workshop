"""Keep the renderer's unset assembly colors consistent with the restored inspector."""
from pathlib import Path
p=Path(__file__).resolve().parents[2]/'outputs/Mechanical_Design_App/rack-references/rack-studio.js'
s=p.read_text(encoding='utf-8').replace("a.tray||'#d38292'","a.tray||'#4d8e6e'").replace("a.faceplate||'#bd794d'","a.faceplate||'#4e75a3'")
p.write_text(s,encoding='utf-8')
