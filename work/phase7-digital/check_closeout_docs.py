from pathlib import Path
p=Path('HANDOFF.md');s=p.read_text(encoding='utf-8')
s=s.replace('App: python outputs/Mechanical_Design_App/app.py --port8767 --data work/NEW-disposable-folder (use actual separated CLI arguments --port 8767; --data points to a NEW folder).','App command: `& \'C:/Program Files/Python310/python.exe\' outputs/Mechanical_Design_App/app.py --port 8767 --data work/NEW-disposable-folder` (the data directory must be NEW for acceptance).')
p.write_text(s,encoding='utf-8')
assert 'READY FOR CLOSEOUT REVIEW' in Path('outputs/Phase7_Closeout/Closeout_Review.md').read_text(encoding='utf-8')
print('Current handoff and closeout review verified.')
