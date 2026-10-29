"""Run existing HDT triangle proof in a fresh Revision 2 scratch directory."""
from pathlib import Path
root=Path(__file__).resolve().parents[2]
here=Path(__file__).resolve().parent
code=(here/'verify_hdt.py').read_text(encoding='utf-8')
code=code.replace("folder = HERE / 'hdt-regression'","folder = HERE / 'revision2/hdt-regression'")
code=code.replace("(HERE/'hdt-regression.json')","(HERE/'revision2/hdt-regression.json')")
exec(compile(code,str(here/'verify_hdt.py'),'exec'),{'__file__':str(here/'verify_hdt.py'),'__name__':'__main__'})
