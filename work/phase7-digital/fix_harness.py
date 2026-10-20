from pathlib import Path
p=Path('work/phase7-digital/accept.py')
s=p.read_text(encoding='utf-8')
a=s.index('loader=unittest.TestLoader()');b=s.index("packs=catalog_packs",a)
block=s[a:b]
s=s[:a]+"if '--integration-only' not in sys.argv:\n"+''.join('    '+line+'\n' for line in block.splitlines())+"else:\n    summary=json.loads((out/'Test_Summary.json').read_text(encoding='utf-8'));assert summary['failures']==0 and summary['errors']==0\n"+s[b:]
s=s.replace("store=Store(data/'library.sqlite3')","data.mkdir(parents=True)\nstore=Store(data/'library.sqlite3')")
s=s.replace("assert counts==dict(pass_=7) if False else counts=={'pass':7,'fail':0,'unknown':6}","assert counts=={'pass':7,'fail':0,'unknown':6}")
p.write_text(s,encoding='utf-8')
