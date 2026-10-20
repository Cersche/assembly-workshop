from pathlib import Path
p=Path('C:/Users/brian/.codex/visualizations/2026/10/18/01a14f51-2a90-7a30-8627-77653e78e987/rack-studio-options.html')
s=p.read_text(encoding='utf-8').replace('min-height:670px;position:relative;isolation:isolate','min-height:740px;position:relative;isolation:isolate;display:flex;flex-direction:column')
s=s.replace('min-height:568px}', 'min-height:630px;flex:1}')
s=s.replace('width:100%;text-align:left;margin-top:7px}', 'width:100%;text-align:left;margin-top:7px;display:flex;align-items:center;gap:8px}')
s=s.replace("(n===1?'Tray + faceplate':'Ready for equipment')", "(n===1?'Tray + faceplate':'Available')")
s=s.replace('Save artwork in STL later.', 'STL artwork planned later.')
s=s.replace('min-height:1150px}', 'min-height:1280px}')
p.write_text(s,encoding='utf-8')
