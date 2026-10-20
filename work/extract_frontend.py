from pathlib import Path
s=Path('outputs/Mechanical_Design_App/index.html').read_text(encoding='utf-8')
Path('work/app_frontend_check.js').write_text(s.split('<script>')[1].split('</script>')[0],encoding='utf-8')
