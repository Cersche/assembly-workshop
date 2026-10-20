from pathlib import Path
import base64,re
p=Path('C:/Users/brian/.codex/visualizations/2026/10/18/01a14f51-2a90-7a30-8627-77653e78e987/rack-studio-options.html')
s=p.read_text(encoding='utf-8')
for marker,path in [('RACK_IMAGE','work/assembly-instances/Rack_Colors_Full.png'),('ART_IMAGE','work/assembly-instances/preview-artwork.png')]:
    s=s.replace(marker,'data:image/png;base64,'+base64.b64encode(Path(path).read_bytes()).decode('ascii'))
p.write_text(s,encoding='utf-8')
print(p.stat().st_size)
assert len(s)<1000000
assert '\\"' not in s
Path('work/assembly-instances/options-script.js').write_text(re.search(r'<script>([\s\S]*)</script>',s).group(1),encoding='utf-8')
