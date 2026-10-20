from pathlib import Path
import shutil
p=Path('work/workflow-audit/test_layout_actions.cjs');backup=Path('work/gui-refinement/before-layout-actions.cjs')
if not backup.exists():shutil.copy2(p,backup)
s=p.read_text(encoding='utf-8');s=s[:s.index('// Exercise the actual workspace save handler')]+"// Saving moved to the unified atomic controller; its actual handler is checked here.\nrequire('../gui-refinement/test_save.cjs');\n";p.write_text(s,encoding='utf-8')
